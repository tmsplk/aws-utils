import boto3

# Configure AWS access
AWS_ACCESS_KEY_ID = 'YOUR_ACCESS_KEY'
AWS_SECRET_ACCESS_KEY = 'YOUR_SECRET_KEY'

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def delete_files_from_s3(file_with_paths, log_file_path, error_file_path):
    # Create an S3 client
    s3 = boto3.client('s3')
    
    # List to keep track of deleted files
    error_files = []
    deleted_files = []

    # Read the file paths
    with open(file_with_paths, 'r') as file:
        paths = file.readlines()

    # Loop over each path, strip newline, and delete the file
    for path in paths:
        path = path.strip()
        bucket_name, key = path.replace('s3://', '').split('/', 1)

        try:
            # Attempt to delete the file
            response = s3.delete_object(Bucket=bucket_name, Key=key)
            print(f"Deleted: {path}")
            deleted_files.append(path)

        except Exception as e:
            # Log any errors that occur
            print(f"Error deleting {path}: {str(e)}")
            error_files.append(path)

    # Write the list of deleted files to a log file
    with open(log_file_path, 'w') as log_file:
        for file in deleted_files:
            log_file.write(file + '\n')

    with open(error_file_path, 'w') as error_log_file:
        for file in error_files:
            error_log_file.write(file + '\n')

    return deleted_files, error_files

log_file_path = 'deleted_files_log.txt'
error_file_path = 'error_files_log.txt'

source_file_path = 'files-to-erase.txt'

deleted_files, error_files = delete_files_from_s3(source_file_path, log_file_path, error_file_path)