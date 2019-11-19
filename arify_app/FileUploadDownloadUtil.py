import boto3
from botocore.exceptions import NoCredentialsError

from arify_backend import settings


def upload_to_aws(local_file, bucket, s3_file):

    AWS_ACCESS_KEY = 'XXXXXXXXXXXXXXXXXXXXXXX'
    AWS_SECRET_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)

    try:
        s3.upload_file(local_file, bucket, s3_file)
        print("Upload Successful")
        url = s3.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': settings.BUCKET_NAME,
                'Key': s3_file
            }
        )
        print("Presigned url is " + str(url))
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False