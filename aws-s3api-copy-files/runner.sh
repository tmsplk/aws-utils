#!/bin/bash

SOURCE_BUCKET="<SOURCE_BUCKET>"
TARGET_BUCKET="<OUTPUT_BUCKET>"

# This script excepts paths.txt file to exist, which should contain one S3 path per row
while read -r TARGET_KEY; do
    TARGET_KEY="${KEY/copied_files/}"

    # Copy each object to the new location
    aws s3api copy-object --bucket $TARGET_BUCKET --copy-source "${SOURCE_BUCKET}/${KEY}" --key "$TARGET_KEY" --acl bucket-owner-full-control

    # Check if the copy was successful
    if [[ $? -eq 0 ]]; then
        echo "Successfully copied to: $TARGET_KEY"
    else
        echo "Failed to copy $KEY"
    fi
done < paths.txt