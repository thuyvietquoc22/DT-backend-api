import boto3
from boto3.resources.base import ServiceResource

from app.core.config import settings


def initialize_db() -> ServiceResource:
    if settings.ENV == "local":
        ddb = boto3.resource(
            "dynamodb",
            endpoint_url=settings.AWS_DB_ENDPOINT_URL,
            region_name=settings.AWS_REGION_NAME
        )
    else:
        ddb = boto3.resource(
            "dynamodb",
            region_name=settings.AWS_REGION_NAME,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )

    return ddb
