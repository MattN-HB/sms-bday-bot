# sms-bday-bot

Send message to your contacts on an important date (e.g. <name>! Happy Birthday, <name>! Happy anniversary!)

## Architecture

![Alt architecture](/docs/architecture-smsbdaybot.png)

## Examples

### Example SMS

![Alt sms message](/docs/example_text.jpeg)

### Example Slack Message

![Alt slack message](/docs/example_slack.jpeg)

## Setup

0.  [AWS cli is installed](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
1.  [AWS CDK is installed](https://docs.aws.amazon.com/cdk/v2/guide/getting_started.html)
2.  As of June 1,2021 sending unregistered texts via SNS in US is not allowed. Go to [AWS Pinpoint console](https://us-east-1.console.aws.amazon.com/pinpoint/home?region=us-east-1) register TFN for $2/month and it will auto associate to SNS. See issue #3.
3.  Update `config.yaml` this includes tags for the resources:

```
name_tag: NotificationDateBot
techowner_tag: name
environment_tag: Dev
project_tag: NotificationDateBot
```

2.  Edit `file.json` with your contacts bday and numbers

```
    {
      "name": "dave",
      "phone": "12325558888",
      "birthday": "1973-03-05",
      "message": "Happy Birthday! Have a fantastic day. From, YOUR_NAME! https://giphy.com/gifs/theoffice-nbc-the-office-tv-lNByEO1uTbVAikv8oT PS This is noreply number"
    },
```

3.  To manually create a virtualenv on MacOS and Linux:

    ```
    $ python3 -m venv .venv
    ```

4.  After the init process completes and the virtualenv is created, you can use the following
    step to activate your virtualenv.

        ```
        $ source .venv/bin/activate
        ```
        If you are a Windows platform, you would activate the virtualenv like this:

        ```
        % .venv\Scripts\activate.bat
        ```

5.  Once the virtualenv is activated, you can install the required dependencies.

    ```
    $ pip install -r requirements.txt
    ```

6.  At this point you can now synthesize the CloudFormation template for this code.

    ```
    $ cdk synth
    ```

7.  If you have not `cdk bootstrap` your environment execute that command
8.  `cdk deploy`

### Extras:

- if deploying to different region than `us-east-1` change the boto3 to that region in `loop.py`
- add your slack lambda as subscriber to the SNS topic so you can get alerted when text is sent...[Slack example in python](https://github.com/thibeault/lambda-slack-birthday-bot/blob/master/run.py)
- add your email to `notification.py` `__snstopic` function if want to be alerted when text sends

```
    def __snstopic(self, stack_config: dict):
        # Uncomment below if you want to add email subscriber to be notified when text sends
        # email = "<YOUREMAIL>"
        self.notificationtopic = sns.Topic(self, "NotificationTopic",
            display_name="NotificationTopic")
        # notificationtopic.add_subscription(subscriptions.EmailSubscription(email))
```

## Useful commands

- `cdk ls` list all stacks in the app
- `cdk synth` emits the synthesized CloudFormation template
- `cdk deploy` deploy this stack to your default AWS account/region
- `cdk diff` compare deployed stack with current state
- `cdk docs` open CDK documentation

## Troubleshooting

If you get a:

```
Could not assume role in target account using current credentials Socket timed out without establishing a connection . Please make sure that this role exists in the account. If it doesn't exist, (re)-bootstrap the environment with the right '--trust', using the latest version of the CDK CLI.
current credentials could not be used to assume
```

Remediation from github cdk issues using the `--asset-parallelism=false`:

```
cdk deploy --trust=<account_id> --cloudformation-execution-policies=arn:aws:iam::aws:policy/AdministratorAccess --asset-parallelism=false --verbose
```

## Resources and Inspiration

- [SMS Code](https://www.qloudx.com/how-to-send-an-sms-from-aws-lambda/)
- [Slack example in python](https://github.com/thibeault/lambda-slack-birthday-bot/blob/master/run.py)
- [Call S3 file with lambda](http://www.awslessons.com/2017/accessing-s3-with-lambda-functions/)
- [Querying Dynamodb tool](https://dynobase.dev/dynamodb-query/)
- [DynamoDB cheat sheet](https://dynobase.dev/dynamodb-python-with-boto3/)

Enjoy!
