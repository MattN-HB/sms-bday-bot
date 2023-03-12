#!/usr/bin/env python3
import os
import aws_cdk as cdk
from test.test_stack import TestStack
import yaml
from aws_cdk import App
from aws_cdk import Aspects
from aws_cdk import Tags
from cdk_nag import AwsSolutionsChecks
from cdk_nag import NagSuppressions
from cdk_nag import NIST80053R5Checks
from notification.notification import NotificationStack

def load_config_file():
    with open(r"config.yaml") as config_file:
        stack_config = yaml.safe_load(config_file)
    return stack_config

stack_config = load_config_file()

app = cdk.App()
notification_stack = NotificationStack(app, "NotificationStack", stack_config)


# Add tag(s) to all resources based on what is in the config.yaml
Tags.of(notification_stack).add("Name", stack_config["name_tag"])
Tags.of(notification_stack).add("TechOwner", stack_config["techowner_tag"])
Tags.of(notification_stack).add("Environment", stack_config["environment_tag"])
Tags.of(notification_stack).add("Project", stack_config["project_tag"])
# TestStack(app, "TestStack",
#     )

NagSuppressions.add_stack_suppressions(
    notification_stack,
    [
        {
            "id": "AwsSolutions-IAM4",
            "reason": "Accepting risk for dev to use the aws managed execution role",
        },
        {
            "id": "AwsSolutions-IAM5",
            "reason": "Backlog for prod to lockdown wildcard to specific object from bucket",
        }, 
        {
            "id": "AwsSolutions-SNS2",
            "reason": "Backlog for prod to have topic have server side encryption but low risk due to in transit and done by AWS",
        },       
        {
            "id": "AwsSolutions-SNS3",
            "reason": "Backlog for prod to have topic to require publisher to use ssl",
        }, 
    ]
)

Aspects.of(app).add(AwsSolutionsChecks())
# Aspects.of(app).add(NIST80053R5Checks())
app.synth()
