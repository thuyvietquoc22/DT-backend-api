from typing import Any, Literal, Union

import boto3
from botocore.exceptions import ClientError
from app.utils.logging import logger
from app.core.config import settings
from email.header import Header

client: Any = boto3.client(
    'ses',
    region_name=settings.AWS_REGION_NAME,
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
)


def verify_email(email_address: str) -> Literal['Failed', 'Pending', 'Success']:
    try:
        if _identity_verification(email_address) != 'Success':
            res = client.verify_email_identity(EmailAddress=email_address)
            return 'Pending' if res.get('ResponseMetadata').get('HTTPStatusCode') == 200 else 'Failed'
        return 'Success'
    except Exception:
        logger.exception("failure verify mail")
        return 'Failed'


def ses_send_mail(
        subject: str, content: str, sender_email: str,
        recipient_email: list[str], sender_name: str, cc_email: list[str]
) -> Union[str, bool]:
    if sender_email is None or not _check_identity(sender_email):
        logger.info(f'Sender Not Verify. {sender_email}')
        sender_email = settings.SENDER_EMAIL

    logger.info(f'sender_name: {sender_name}')
    logger.info(f'subject: {subject}')
    logger.info(f'content: {content}')
    logger.info(f'sender_email:{sender_email}')
    logger.info(f'recipient_email: {recipient_email}')
    charset: str = 'UTF-8'

    if not recipient_email:
        logger.info('recipient_email does not exist')
        return False

    send_mail_successfully: str = ''
    try:
        # Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': recipient_email,
                'CcAddresses': cc_email,
            },
            Message={
                'Body': {'Html': {'Charset': charset, 'Data': content}},
                'Subject': {'Charset': charset, 'Data': subject},
            },
            Source=_encoding_email_header(sender_name, sender_email),
        )
    # Display an error if something goes wrong.
    except ClientError as e:
        logger.info(str(e.response))
    else:
        logger.info(
            f'{sender_email} sent email to {recipient_email} Message ID: {response["MessageId"]}'
        )
        send_mail_successfully = response['MessageId']

    return send_mail_successfully


def _identity_verification(identity: str) -> Literal['Failed', 'Pending', 'Success']:
    try:
        res = client.get_identity_verification_attributes(Identities=[identity, ])
        return res.get('VerificationAttributes').get(identity).get('VerificationStatus') or 'Failed'
    except Exception:
        logger.exception("failure identity verification")
        return 'Failed'


def _check_identity(email_address: str) -> bool:
    try:
        if _identity_verification(email_address) == 'Success':
            return True
        return False
    except Exception:
        return False


def _encoding_email_header(sender_name: str, sender_email: str) -> str:
    try:
        return f'{Header(sender_name.encode("iso-2022-jp"), "iso-2022-jp").encode()} <{sender_email}>'
    except UnicodeEncodeError as e:
        logger.exception(f'mail encode error: {str(e)}')
    try:
        return '%s <%s>' % (Header(sender_name.encode('utf-8'), 'utf-8').encode(), sender_email)
    except Exception:
        logger.exception("mail error")
        return f'{sender_name} <{sender_email}>'
