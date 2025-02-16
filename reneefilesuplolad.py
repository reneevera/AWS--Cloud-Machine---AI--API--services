import boto3
import os
import logging
from botocore.exceptions import ClientError
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# AWS credentials setup from environment variables
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')
AWS_REGION = os.getenv('AWS_REGION')
BUCKET_NAME = 'contentcen301345205.aws.ai'
FOLDER_NAME = 'assignment1'

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def aws_connect():
    try:
        # Create a session using your credentials
        session = boto3.Session(
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY,
            region_name=AWS_REGION
        )
        
        # Example: Create an S3 client
        s3_client = session.client('s3')
        
        # Test connection by listing S3 buckets
        response = s3_client.list_buckets()
        print("Connected to AWS successfully!")
        print("Available S3 buckets:")
        for bucket in response['Buckets']:
            print(f"- {bucket['Name']}")
            
        return s3_client
        
    except Exception as e:
        print(f"Error connecting to AWS: {str(e)}")
        return None

def upload_files_to_s3(s3_client):
    if not s3_client:
        logger.error("No S3 client connection available")
        return

    # List of files to upload
    files_to_upload = ['renee1.txt', 'renee2.txt', 'renee3.txt']
    
    # Record start time
    start_time = datetime.now()
    print(f"Upload process started at: {start_time}")

    try:
        for file_name in files_to_upload:
            # Construct the file path
            file_path = os.path.join(os.path.dirname(__file__), file_name)
            
            # Construct the S3 key (path in bucket)
            s3_key = f"{FOLDER_NAME}/{file_name}"
            
            print(f"Starting upload of {file_name}...")
            
            try:
                s3_client.upload_file(file_path, BUCKET_NAME, s3_key)
                print(f"Successfully uploaded {file_name} to S3")
                
            except ClientError as e:
                logger.error(f"Error uploading {file_name}: {e}")
                continue
            except FileNotFoundError:
                logger.error(f"File not found: {file_name}")
                continue
    
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    
    # Record end time and calculate duration
    end_time = datetime.now()
    duration = end_time - start_time
    print(f"Upload process completed at: {end_time}")
    print(f"Total duration: {duration}")

if __name__ == '__main__':
    s3_client = aws_connect()
    if s3_client:
        upload_files_to_s3(s3_client)