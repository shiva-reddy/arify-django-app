import os

import boto3
from botocore.exceptions import NoCredentialsError


def upload_to_aws(local_file, bucket, s3_file):

    AWS_ACCESS_KEY,AWS_SECRET_KEY = os.environ['S3_KEY'], os.environ['S3_SECRET']

    try:
        s3_session = boto3.session.Session(aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
        s3 = s3_session.resource('s3')
        bucket = s3.Bucket(bucket)
        bucket.upload_file(local_file, s3_file, ExtraArgs={'ACL': 'public-read'})
        return "https://arify-resource-storage.s3.amazonaws.com/" + s3_file

    except FileNotFoundError:
        print("The file was not found")
        raise FileNotFoundError
    except NoCredentialsError:
        print("Credentials not available")
        raise NoCredentialsError