import json
import boto3 
from boto3.dynamodb.conditions import Key
import os 
from datetime import datetime, date
import logging

# Initialize logger and set log level
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize SNS client for US East region
session = boto3.Session(
    region_name="us-east-1"
)
sns_client = session.client('sns')
# Intialize s3
s3 = boto3.client('s3')
def lambda_handler(event, context):
    bucketname_variable = os.environ["BUCKETNAME_VARIABLE"]
    filename_variable = os.environ["FILENAME_VARIABLE"]
    SNS_variable = os.environ["SNS_ARN"]

    # Get file from s3 bucket
    file = s3.get_object(Bucket=bucketname_variable, Key=filename_variable) 
    json_string = file["Body"].read().decode()

    # This is where the json data is being stored into a dictionary
    jdata = json.loads(json_string)

    # Gets todays date
    today = date.today()
    friends = "None"

    for value in jdata['members']:
        checker = datetime.strptime(value['birthday'], "%Y-%m-%d").date()
        if checker.month == today.month and checker.day == today.day:
            response = sns_client.publish(
                PhoneNumber=value['phone'],
                Message=value['name'] + '!' + ' ' + value['message'],
                )
            # Optional to send to SNS topic so you know it worked I sent to Slack channel via SNS to Lambda
            response = sns_client.publish(
                TargetArn=SNS_variable,
                Message='FYI the following was sent to ' + value['name'] + ' : ' + value['message']
                )

    return str(datetime.now())
