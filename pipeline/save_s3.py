import boto3
import os

def upload_file_to_s3(file_path, bucket_name, object_name=None):
    s3 = boto3.client("s3")
    
    if object_name is None:
        object_name = os.path.basename(file_path)
    
    s3.upload_file(file_path, bucket_name, object_name)
    print(f"Archivo subido a S3: s3://{bucket_name}/{object_name}")
