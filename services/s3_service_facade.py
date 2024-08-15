import boto3
import logging
from botocore.exceptions import NoCredentialsError
from decouple import config

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def upload_to_s3(file_name, bucket, object_name=None):
    if object_name is None:
        object_name = file_name

    s3_client = boto3.client(
        's3',
        aws_access_key_id=config('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=config('AWS_SECRET_ACCESS_KEY'),
    )
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except NoCredentialsError:
        logger.error("Credentials not available")
        return False
    return True
