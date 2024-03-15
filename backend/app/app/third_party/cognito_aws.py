import base64
import hashlib
import hmac
from typing import Any

import boto3
from botocore.exceptions import ClientError
from fastapi import HTTPException

from app.core.config import settings
from app.utils.logging import logger

client: Any = boto3.client(
    'cognito-idp',
    region_name=settings.AWS_REGION_NAME,
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
)


def create_user(username, password, email):
    logger.info(f'Create moblie: {settings.COGNITO_USER_POOL_ID}')
    logger.info(f'Create moblie: {settings.COGNITO_CLIENT_ID}')
    logger.info(f'Create moblie: {settings.AWS_REGION_NAME}')
    logger.info(f'Create moblie: {settings.AWS_ACCESS_KEY_ID}')
    logger.info(f'Create moblie: {settings.AWS_SECRET_ACCESS_KEY}')
    if is_email_registered(username):
        raise HTTPException(status_code=400, detail='Username already exists')
    if is_email_registered(email):
        raise HTTPException(status_code=400, detail='Username already exists')
    # Create a new moblie with a temporary password and moblie information.
    try:
        response = client.admin_create_user(
            UserPoolId=settings.COGNITO_USER_POOL_ID,
            Username=username,
            TemporaryPassword=password,
            ForceAliasCreation=True,
            MessageAction='SUPPRESS',
            DesiredDeliveryMediums=['EMAIL'],
            UserAttributes=[
                {
                    'Name': 'email',
                    'Value': email
                },
            ]
        )

    except Exception as e:

        raise HTTPException(status_code=400, detail=e.response['Error']['Code'])

    # Set up a password for the new moblie.
    try:
        client.admin_set_user_password(
            UserPoolId=settings.COGNITO_USER_POOL_ID,
            Username=username,
            Password=password,
            Permanent=True
        )
    except Exception as e:
        client.admin_set_user_password(
            UserPoolId=settings.COGNITO_USER_POOL_ID,
            Username=email,
            Password=password,
            Permanent=True
        )

    return response


def is_email_registered(email):
    try:
        # Call api to get moblie information
        response = client.admin_get_user(
            UserPoolId=settings.COGNITO_USER_POOL_ID,
            Username=email
        )
    except ClientError as e:
        # If email is not registered, API will return an error
        error_code = e.response['Error']['Code']
        if error_code == 'UserNotFoundException':
            return False
        else:
            # Handle other errors
            error = e.response['Error']['Message']
            return {'error': error}
    else:
        # If email exists, API will return moblie information
        return True


def get_user_by_email(email):
    try:
        # Call api to get moblie information
        response = client.admin_get_user(
            UserPoolId=settings.COGNITO_USER_POOL_ID,
            Username=email
        )
    except ClientError as e:
        # If email is not registered, API will return an error
        error_code = e.response['Error']['Code']
        if error_code == 'UserNotFoundException':
            return False
        else:
            # Handle other errors
            error = e.response['Error']['Message']
            return {'error': error}
    else:
        # If email exists, API will return moblie information
        return response.get('Username')


def login(username, password):
    if not is_email_registered(username):
        raise HTTPException(status_code=400, detail='Username dose not exists')
    try:
        auth_response = client.initiate_auth(
            ClientId=settings.COGNITO_CLIENT_ID,
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': username,
                'PASSWORD': password
            }
        )
    except ClientError as e:
        print(e)
        return None

    return auth_response['AuthenticationResult']['AccessToken']


def verify_token(token):
    try:
        auth_response = client.admin_initiate_auth(
            UserPoolId=settings.COGNITO_USER_POOL_ID,
            ClientId=settings.COGNITO_CLIENT_ID,
            AuthFlow='ADMIN_NO_SRP_AUTH',
            # dummy_username is temporary username, you can use any username
            AuthParameters={
                'USERNAME': 'dummy_username',
                'SECRET_HASH': client.get_secret_hash(settings.COGNITO_CLIENT_ID, settings.SECRET_KEY),
                'REFRESH_TOKEN': token
            }
        )
    except ClientError as e:
        print(e)
        return None

    return auth_response['AuthenticationResult']['AccessToken']


def get_secret_hash(username):
    client_id = settings.COGNITO_CLIENT_ID
    client_secret = settings.SECRET_KEY
    message = bytes(username + client_id, 'utf-8')
    secret = client_secret
    digest = hmac.new(str(secret).encode('utf-8'), msg=message, digestmod=hashlib.sha256).digest()
    dec_digest = base64.b64encode(digest).decode()

    return dec_digest


def initiate_auth_with_username_password(username, password):
    # secret_hash = get_secret_hash(username)

    try:
        response = client.initiate_auth(
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': username,
                'PASSWORD': password,
            },
            ClientId=settings.COGNITO_CLIENT_ID
        )

        access_token = response['AuthenticationResult']['AccessToken']
        id_token = response['AuthenticationResult']['IdToken']
        refresh_token = response['AuthenticationResult']['RefreshToken']

        return access_token, id_token, refresh_token

    except ClientError as e:
        error = e.response['Error']['Code']
        if error == 'NotAuthorizedException':
            logger.exception('The username or password is incorrect.')
        elif error == 'UserNotConfirmedException':
            logger.exception('The moblie is not confirmed yet.')
        elif error == 'PasswordResetRequiredException':
            logger.exception('The password must be reset before the moblie can sign in.')
        elif error == 'UserNotFoundException':
            logger.exception('The username or password is incorrect.')
        else:
            logger.exception('Unexpected error occurred: %s' % e)

        return None, None, None


def update_password(email: str, password: str):
    if not is_email_registered(email):
        raise HTTPException(status_code=400, detail='Username dose not exists')
    response = client.admin_set_user_password(
        UserPoolId=settings.COGNITO_USER_POOL_ID,
        Username=email,
        Password=password,
        Permanent=True
    )
    return response


def revoke_access_token(token: str):
    try:
        response = client.revoke_token(
            Token=token,
            ClientId=settings.COGNITO_CLIENT_ID
        )
        return response
    except ClientError as e:
        print(e)
        return None


def get_email_by_user_id(user_id: str):
    try:
        response = client.admin_get_user(
            UserPoolId=settings.COGNITO_USER_POOL_ID,
            Username=user_id
        )
        email = ''
        for item in response['UserAttributes']:
            if item['Name'] == 'email':
                email = item['Value']
        return email
    except ClientError as e:
        print(e)
        return None


def refresh_access_token(token: str):
    try:
        auth_response = client.initiate_auth(
            ClientId=settings.COGNITO_CLIENT_ID,
            AuthFlow='REFRESH_TOKEN',
            AuthParameters={
                'REFRESH_TOKEN': token,
                'CLIENT_ID': settings.COGNITO_CLIENT_ID
            }
        )
    except ClientError as e:
        print(e)
        return None

    return auth_response['AuthenticationResult']['AccessToken']


def disable_account(user_name: str):
    try:
        client.admin_disable_user(
            UserPoolId=settings.COGNITO_USER_POOL_ID,
            Username=user_name
        )
    except ClientError as e:
        print(e)
        return None
