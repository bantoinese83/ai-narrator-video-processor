import boto3
from botocore.exceptions import NoCredentialsError
import logging

logging.basicConfig(level=logging.INFO)


class S3Client:
    def __init__(self, bucket_name, aws_access_key, aws_secret_key):
        self.bucket_name = bucket_name
        self.s3 = boto3.client('s3', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)

    def upload_file(self, file_path, file_name):
        try:
            self.s3.upload_file(file_path, self.bucket_name, file_name)
            logging.info(f"File uploaded successfully to {self.bucket_name}/{file_name}")
        except NoCredentialsError:
            logging.error("Credentials not available")

    def generate_presigned_url(self, file_name):
        try:
            url = self.s3.generate_presigned_url('get_object', Params={'Bucket': self.bucket_name, 'Key': file_name})
            logging.info(f"Presigned URL generated: {url}")
            return url
        except Exception as e:
            logging.error(f"Failed to generate presigned URL: {e}")
            raise
