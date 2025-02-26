import boto3
from concurrent.futures import ThreadPoolExecutor
import os
import logging

# Configure AWS access
AWS_ACCESS_KEY_ID = 'YOUR_ACCESS_KEY'
AWS_SECRET_ACCESS_KEY = 'YOUR_SECRET_KEY'
s3Bucket = '<S3_BUCKET>'
regionName='<AWS_REGION>'

s3 = boto3.client('s3')

file_types = ['*.parquet', '*.csv']
min_year = 2023

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def parse_line(line):
    fields = line.strip().split()
    if len(fields) < 2:
        return None, None
    erase_time_str, is_latest_str = fields[0], fields[1].lower()
    
    # Parse erase time from ISO format to datetime object
    try:
        erase_time = datetime.strptime(erase_time_str, '%Y-%m-%dT%H:%M:%S').timestamp()
    except ValueError:
        return None, None
    
    is_latest = (is_latest_str == 'true' or is_latest_str == 'True')
    
    # Get last modified date from the key
    try:
        mod_date = datetime.strptime(response['Lastmods'][0].date(), '%Y-%m-%d').date()
    except (IndexError, ValueError):
        return None, None
    
    return erase_time, is_latest, mod_date

def restore_file(key, bucket_name=s3Bucket):
    logger.info(f"Attempting to restore {key}")
    
    try:
        with ThreadPoolExecutor(max_workers=4) as executor:
            future = executor.submit(s3.download_fileobj, bucket_name, key, f"restored_files/{os.path.basename(key)}")
            
            if not future.futures:
                logger.warning(f"File {key} does not exist in S3. Skipping restoration.")
                return
            
            # Handle asynchronous download and check existence
            result = future.result()
            
        # Check if it's a latest version based on IsLatest flag
        is_latest = False
        mod_date = None
        
        try:
            line = next(iter([line for line in open('input_lines.txt', 'r').readlines() if line.strip().startswith(f"{key} "))))
        except StopIteration:
            logger.warning(f"Could not find corresponding {key} line to verify latest version.")
            os.remove("restored_files/" + os.path.basename(key))
            return
        
        erase_time, is_latest_flag, mod_date = parse_line(line)
        
        if is_latest_flag and mod_date >= datetime.combine(datetime.minyear, datetime.maxtimedelta):
            try:
                for f in glob.glob(f"restored_files/*{os.path.basename(key)}*"):
                    os.remove(f)
            except Exception as e:
                logger.error(f"Error removing file {f}: {e}")
            
            logger.info(f"Restored latest version of {key}")
            
    except Exception as e:
        logger.error(f"Failed to restore {key}: {str(e)}")
        os.remove("restored_files/" + os.path.basename(key))

try:
    response = s3.list_objects_v2(Bucket=s3Bucket)
    
    filtered_objects = []
    for key in response['Keys']:
        try:
            if 'Lastmods' in response and response['Lastmods']:
                mod_date = datetime.strptime(response['Lastmods'][0].date(), '%Y-%m-%d').date()
                
                # Filter based on file type
                match = False
                for ft in file_types:
                    if ft in key.lower():
                        match = True
                        break
                
                # Check modification date and min_year
                if mod_date >= datetime.combine(datetime.minyear, datetime.maxtimedelta) and match:
                    filtered_objects.append((key, mod_date))
        
        except (IndexError, AttributeError) as e:
            print(f"Skipping {key} due to error: {e}")
            continue
    
    # Sort files by erase timestamp in descending order
    sorted_files = sort_files(filtered_objects)
    
    os.makedirs('restored_files', exist_ok=True)
    
    for item in sorted_files:
        key, mod_date = item[0], item[1]
        
        try:
            restore_file(key)
            
            # Only keep the latest version if it's present
            last_key = f"{key}_last_version"
            if os.path.exists(last_key):
                os.remove(last_key)
                
            logger.info(f"Successfully restored {key}")
        except Exception as e:
            logger.error(f"Failed to restore {key}: {str(e)}")
            os.remove("restored_files/" + os.path.basename(key))
    
    # Clean up the temporary directory
    if os.path.exists('corrupted_or_missing'):
        for f in glob.glob('corrupted_or_missing/*'):
            os.remove(f)
        
    print("Restoration process completed. Corrupted or missing files have been removed.")
    
except Exception as e:
    logging.error(f"An error occurred during restoration: {str(e)}")
