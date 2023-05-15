import json
import boto3
import os

session = boto3.Session(
    aws_access_key_id=os.environ["ACCESS_KEY"],
    aws_secret_access_key=os.environ["SECRET_KEY"]
)
sqs = session.client('sqs')
SQS_OCCURENCE_QUEUE_URL = os.environ["SQS_OCCURENCE_QUEUE_URL"]
SQS_CURRENT_QUEUE_URL = os.environ["SQS_CURRENT_QUEUE_URL"]


class SqsService:

    def send_messager_to_occurence(message_body):
        messager = {
            "CurrentQueue": SQS_CURRENT_QUEUE_URL,
            "Messager": message_body
        }

        sqs.send_message(
            QueueUrl=SQS_OCCURENCE_QUEUE_URL,
            MessageBody=json.dumps(messager)
        )

    def delete_current_messager(receipt_handle):
        sqs.delete_message(
            QueueUrl=SQS_CURRENT_QUEUE_URL,
            ReceiptHandle=receipt_handle
        )
