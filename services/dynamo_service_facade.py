
import boto3
from boto3.dynamodb.conditions import Key
from decouple import config

dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id=config('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=config('AWS_SECRET_ACCESS_KEY'),
    region_name=config('AWS_REGION_NAME')
)
table = dynamodb.Table('warmly-test')


async def get_data_by_phone(phone: str):
    results = []
    response = table.query(
        IndexName='phone-index',
        KeyConditionExpression=boto3.dynamodb.conditions.Key('phone').eq(phone)
    )
    results.extend(response.get('Items', []))
    return results


async def get_data_by_email(email: str):
    results = []
    response = table.query(
        IndexName='email-index',
        KeyConditionExpression=boto3.dynamodb.conditions.Key('email').eq(email)
    )
    results.extend(response.get('Items', []))
    return results
