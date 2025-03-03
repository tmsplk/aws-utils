import boto3
import os

AWS_REGION = "us-east-1"  # Replace with AWS region
SNS_TOPIC_ARN = "arn:aws:sns:us-east-1:123456789012:MySNSTopic"  # Replace with your SNS Topic ARN
MESSAGE_FILE = "messages.txt"

def read_messages_from_file(file_path):
    #Reads messages from a text file.s
    if not os.path.exists(file_path):
        print(f"Error: {file_path} does not exist.")
        return []

    with open(file_path, "r", encoding="utf-8") as file:
        messages = [line.strip() for line in file if line.strip()]
    return messages

def publish_to_sns(messages, topic_arn):
    #Publishes messages to SNS topic
    sns_client = boto3.client("sns", region_name=AWS_REGION)

    for message in messages:
        response = sns_client.publish(
            TopicArn=topic_arn,
            Message=message
        )
        print(f"Published message: {message}, MessageId: {response['MessageId']}")

if __name__ == "__main__":
    messages = read_messages_from_file(MESSAGE_FILE)
    if messages:
        publish_to_sns(messages, SNS_TOPIC_ARN)
    else:
        print("No messages found in the file.")