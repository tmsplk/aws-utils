import boto3
import json
import os

AWS_REGION = "us-east-1"  # Replace with AWS region
SQS_QUEUE_URL = "https://sqs.us-east-1.amazonaws.com/123456789012/MyQueue"  # Replace with queue URL
OUTPUT_FILE = "output.txt"
NUM_MESSAGES = 10  # Number of messages to read at a time

def receive_messages(queue_url, num_messages=10):
    #Reads messages from an AWS SQS queue
    sqs_client = boto3.client("sqs", region_name=AWS_REGION)
    
    try:
        response = sqs_client.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=min(num_messages, 10),
            WaitTimeSeconds=5,  # Long polling to reduce API costs
            MessageAttributeNames=["All"]
        )

        messages = response.get("Messages", [])
        return messages
    except Exception as e:
        print(f"Error fetching messages: {e}")
        return []

def save_messages_to_file(messages, file_path):
    #Saves messages to a text file
    with open(file_path, "a", encoding="utf-8") as file:
        for message in messages:
            message_body = message.get("Body", "")
            file.write(json.dumps(message_body, indent=2) + "\n")
    print(f"Saved {len(messages)} messages to {file_path}")

def delete_messages(queue_url, messages):
    #Deletes messages from the SQS queue after processing
    sqs_client = boto3.client("sqs", region_name=AWS_REGION)
    
    for message in messages:
        receipt_handle = message["ReceiptHandle"]
        try:
            sqs_client.delete_message(
                QueueUrl=queue_url,
                ReceiptHandle=receipt_handle
            )
            print(f"Deleted message: {message['MessageId']}")
        except Exception as e:
            print(f"Error deleting message: {e}")

if __name__ == "__main__":
    messages = receive_messages(SQS_QUEUE_URL, NUM_MESSAGES)
    
    if messages:
        save_messages_to_file(messages, OUTPUT_FILE)
        #delete_messages(SQS_QUEUE_URL, messages) # unocmment if you wish to delete messages from queue
    else:
        print("No messages retrieved from SQS.")