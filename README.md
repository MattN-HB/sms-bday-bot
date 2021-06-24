# sms-bday-bot
Objective: Send a birthday or any type of event driven text message to list of people on their birthday/other event due to if your like me you forget people's birthdays/important dates :(. It uses AWS services of Lambda, Pinpoint, SNS, cloudwatch rules, and S3 to automate sending messages via sms.

Update 6/25/2021:  ```[birthday]``` changed to ```[eventdate]``` to be used for any type of event. [See issue #6](https://github.com/MattN-HB/sms-bday-bot/issues/6)

Update 6/15/2021: ```[msg]``` added as value in json file so you can customize your messages per person allowing be used not just for birthdays. See [issue #5](https://github.com/MattN-HB/sms-bday-bot/issues/5)

## Setup
 0. As of June 1,2021 sending unregistered texts via SNS in US is not allowed. Go to AWS Pinpoint console register TFN for $2/month and it will auto associate to SNS. See [issue #3](https://github.com/MattN-HB/sms-bday-bot/issues/3).
 1. Deploy Lambda function ```lambda_function.py``` to your AWS Lambda via console
 2. Create custom IAM Role with below managed tweaked policies (s3 read, sns write (make sure set resource to * ). Best practice to keep the accesses as 'least privilege' as possible.
![image](https://user-images.githubusercontent.com/44328319/120417072-3760cc00-c32c-11eb-98f5-d17ea86a403d.png)

 4. Attach policy to Lambda
![image](https://user-images.githubusercontent.com/44328319/120416980-139d8600-c32c-11eb-814a-9df402952326.png)

 6. Edit your contacts in ```file.json``` and then Upload ```file.json``` into s3 bucket. DO NOT MAKE PUBLIC and encrypt with your key or SSE.
 7. Load ```[BUCKETNAME]``` and ```[FILENAME]``` into the Lambda script ```lambda_function.py```
 8. If you want to get alerted when message is sent create SNS topic and edit field ```[YOURSNSARN] ```. I have sent to my email and slack.
 9. Test via lambda console using 'test' user in the json file and today's date. Note:the timezone executed is GMT
 10. Set up cloudwatch event rule with cron job frequency of trigger to your lambda.I set it up as ``` 0 14 * * ? *  ``` which is 1400 Daily GMT or 0900 CST 

![image](https://user-images.githubusercontent.com/44328319/120416540-527f0c00-c32b-11eb-9593-021d9e560963.png)

## Resources
* [SMS Code](https://www.qloudx.com/how-to-send-an-sms-from-aws-lambda/)
* [Slack example in python](https://github.com/thibeault/lambda-slack-birthday-bot/blob/master/run.py)
* [Call S3 file with lambda](http://www.awslessons.com/2017/accessing-s3-with-lambda-functions/)
* [CLI S3 cheat sheet](https://acloudguru.com/blog/engineering/aws-s3-cheat-sheet)
* [Boto3 SNS Doc](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.Client.publish)
* [SNS Access Policy Examples](https://docs.aws.amazon.com/sns/latest/dg/sns-access-policy-use-cases.html)
* [Querying Dynamodb tool](https://dynobase.dev/dynamodb-query/)
* [DynamoDB cheat sheet](https://dynobase.dev/dynamodb-python-with-boto3/)
