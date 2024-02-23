from boto3 import Session
import boto3
import time
import json

from app.core.config import settings

client = Session(aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)


def save_to_s3(bucket_name, key_name, media_data):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    bucket.put_object(Key=key_name, Body=media_data)

    # Return the S3 object URL
    object_url = f'{settings.CLOUDFRONT_DOMAIN}{key_name}'
    return object_url


def save_avatar_to_s3(bucket_name, key_name, media_data, content_type):
    cloudfront_client = boto3.client('cloudfront')
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    bucket.put_object(Key=key_name, Body=media_data, ContentType=content_type)

    cloudfront_client.create_invalidation(
        DistributionId=settings.CLOUDFRONT_DISTRIBUTION_ID,
        InvalidationBatch={
            'Paths': {
                'Quantity': 1,
                'Items': ['/' + key_name]
            },
            'CallerReference': f'Invalidation {key_name} {int(time.time())}'  # Provide a unique caller reference
        }
    )
    # Return the S3 object URL
    object_url = f'{settings.CLOUDFRONT_DOMAIN}{key_name}'
    return object_url
