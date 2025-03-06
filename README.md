# AWS Utilities

## Overview
This repository contains a set of **AWS utility scripts** for interacting with various AWS services, including **S3, SNS, and SQS**. These scripts help automate common tasks such as file management, message publishing, and queue processing.

## Features
- **S3 Utilities**
  - Delete files from an S3 bucket.
  - Restore files in S3.
  - Copy files using `aws s3api`.
- **SNS Utilities**
  - Publish messages to an SNS topic.
- **SQS Utilities**
  - Read messages from an SQS queue.

## Project Structure
```
/aws-utils-main
│-- aws-s3-delete-files/
│   ├── main.py              # Delete files from S3
│-- aws-s3-restore-files/
│   ├── main.py              # Restore files in S3
│-- aws-s3api-copy-files/
│   ├── runner.sh            # Copy files using aws s3api
│-- aws-sns-publish-messages/
│   ├── main.py              # Publish messages to SNS
│   ├── messages.txt         # Sample messages
│-- aws-sqs-read-messages/
│   ├── main.py              # Read messages from SQS
│-- README.md                # Project documentation
```

## Prerequisites
- Python 3.x
- AWS CLI installed and configured (`aws configure`)
- Required AWS permissions for S3, SNS, and SQS

## Installation
```sh
# Clone the repository
git clone <repo_url>
cd aws-utils-main

# Install dependencies
pip install boto3
```

## Usage
### S3 Utilities
```sh
# Delete files from S3
python aws-s3-delete-files/main.py

# Restore files in S3
python aws-s3-restore-files/main.py

# Copy files using aws s3api
bash aws-s3api-copy-files/runner.sh
```

### SNS Utilities
```sh
# Publish messages to SNS
python aws-sns-publish-messages/main.py
```

### SQS Utilities
```sh
# Read messages from SQS
python aws-sqs-read-messages/main.py
```

## License
This project is licensed under the MIT License.

## Contributors
- **[@tmsplk](https://github.com/tmsplk)** - Maintainer