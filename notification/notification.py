import aws_cdk as cdk
from aws_cdk import Stack
from aws_cdk import aws_sns as sns
from aws_cdk import aws_sns_subscriptions as subscriptions
from aws_cdk import aws_events as events
from aws_cdk import aws_iam as iam
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_s3_deployment as s3_deployment
from aws_cdk import aws_kms as kms
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_events_targets as targets
from constructs import Construct
import os

class NotificationStack(Stack):

    def __init__(self, scope: Construct, id:str, stack_config: dict, **kwargs)-> None:
        super().__init__(scope, id, **kwargs)
        
        self.__build_bucket(stack_config)
        self.__copyobject_bucket(stack_config)
        self.__snstopic(stack_config)
        self.__looplambda(stack_config)
        self.__cloudwatchevent(stack_config)


    def __build_bucket(self,stack_config: dict):

        self.databucket = s3.Bucket(self, "Bucket",
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            encryption=s3.BucketEncryption.S3_MANAGED,
            server_access_logs_prefix="logs",
            enforce_ssl=True,
            bucket_name=Stack.of(self).account + '-' + Stack.of(self).region + '-data-bucket',
            auto_delete_objects=False,
            versioned=True
        )
    def __copyobject_bucket(self, stack_config: dict):
        s3_deployment.BucketDeployment(self.databucket, "DeployObject",
            sources=[s3_deployment.Source.asset('assets')],
            destination_bucket=self.databucket
        )
    
    def __looplambda(self, stack_config: dict):
        self.loop_lambda = _lambda.Function(
            self, 'loopHandler',
            description="Lambda that loops the json file looking for date of today and send SNS message",
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset('./assets/lambda/code'),
            handler='loop.lambda_handler',
            environment={
                'BUCKETNAME_VARIABLE': self.databucket.bucket_name,
                'FILENAME_VARIABLE': "file.json",
                'SNS_ARN': self.notificationtopic.topic_arn
            }
        )
        self.loop_lambda.add_to_role_policy(
            iam.PolicyStatement(
                actions=["s3:GetObject"],
                resources=[self.databucket.arn_for_objects("*")]
            )
        )
        self.loop_lambda.add_to_role_policy(
            iam.PolicyStatement(
                actions=["sns:Publish"],
                # Below needs be wildcard due to SNS boto3 sending to phone numbers 
                resources=["*"] #[self.notificationtopic.topic_arn]
            )
        )

    def __cloudwatchevent(self, stack_config: dict):
        dailyrule = events.Rule(self, "Rule",
            description="rule that runs at 14th hr of GMT daily",
            schedule=events.Schedule.cron(minute="0", hour="14")
            )
        dailyrule.add_target(targets.LambdaFunction(self.loop_lambda))
    
    def __snstopic(self, stack_config: dict):
        # Uncomment below if you want to add email subscriber to be notified when text sends
        # email = "<YOUREMAIL>"
        self.notificationtopic = sns.Topic(self, "NotificationTopic",
            display_name="NotificationTopic")
        # notificationtopic.add_subscription(subscriptions.EmailSubscription(email))
    
    

