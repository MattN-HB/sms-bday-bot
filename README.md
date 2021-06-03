# sms-bday-bot
Utiizing AWS services of Lambda, SNS, and S3 automate sending your birthday texts to your contacts
## Setup
 1. Deploy Lambda function 'lambda_function.py' 
 2. Create custom IAM Role with below managed tweaked policies (s3 read, sns write (make sure set resource to * )
![image](https://user-images.githubusercontent.com/44328319/120417072-3760cc00-c32c-11eb-98f5-d17ea86a403d.png)

 4. Attach policy to Lambda
![image](https://user-images.githubusercontent.com/44328319/120416980-139d8600-c32c-11eb-814a-9df402952326.png)

 6. Edit and then Upload 'file.json' into s3 bucket. DO NOT MAKE PUBLIC
 7. Load BUCKETNAME and FILENAME into the Lambda script
 8. Test
 9. Set up cloudwatch event rule with cron job frequency of trigger to your lambda of 0 5 * * ? * NOTE THIS IS GMT TIME
![image](https://user-images.githubusercontent.com/44328319/120416540-527f0c00-c32b-11eb-9593-021d9e560963.png)

## Resources
* [SMS Code](https://www.qloudx.com/how-to-send-an-sms-from-aws-lambda/)
* [Slack example in python](https://github.com/thibeault/lambda-slack-birthday-bot/blob/master/run.py)
* [Call S3 file with lambda](http://www.awslessons.com/2017/accessing-s3-with-lambda-functions/)
* [Querying Dynamodb tool](https://dynobase.dev/dynamodb-query/)
* [DynamoDB cheat sheet](https://dynobase.dev/dynamodb-python-with-boto3/)
