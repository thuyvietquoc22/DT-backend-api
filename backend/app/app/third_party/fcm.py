from fastapi import HTTPException
from firebase_admin import credentials, messaging, initialize_app

from app.utils.logging import logger

# Khởi tạo Firebase Admin SDK với file cấu hình JSON
cred = credentials.Certificate("../app/firebase-config.json")
initialize_app(cred)

# Gửi thông báo đến một người
def send_message(message_data: dict):
    try:
        # Extract thông tin từ dữ liệu nhận được
        registration_token = message_data['registration_token']
        message_title = message_data['message_title']
        message_body = message_data['message_body']

        # Gửi thông điệp đến thiết bị
        message = messaging.Message(
            notification=messaging.Notification(
                title=message_title,
                body=message_body,
            ),
            token=registration_token,
        )

        response = messaging.send(message)
        print('Messages sent successfully.')

        return {'success': True, 'response': response}

    except Exception as e:
        logger.info(f'exception as {e}')
        raise HTTPException(status_code=500, detail=str(e))


# Gửi thông điệp đến nhiều người dùng
def send_fcm_to_many_users(message_data, tokens):
    try:
        # tokens: danh sách token moblie cần gửi message
        # Kiểm tra nếu không có token
        if not tokens:
            print('No tokens found.')
            return

        # Gửi thông điệp đến từng token
        for user_id, user_tokens in tokens.items():
            for token in user_tokens:
                try:
                    message = messaging.Message(
                        notification=messaging.Notification(
                            title=message_data['title'],
                            body=message_data['body'],
                        ),
                        token=token,
                    )
                    messaging.send(message)
                except Exception as e:
                    logger.info(f'{id} {e}')
                    continue

        logger.info('Messages sent successfully.')
    except Exception as e:
        print(f'Error sending FCM: {e}')

# Cheat test send message FCM
def send_message_cheat_test():
    try:
        # Extract thông tin từ dữ liệu nhận được
        registration_token = "e-itrrcdtoodv7rkx6g2yy:apa91bfu1hczrzpaubya9umv3d3guzt_dcz8zhfgbxaltse4fbamcv2kklf6ekdmxhg_g9inwamja8-6vfzfrlqkpm8mi956ncfcsa-jrsmp50qsbblehgiz9ezo7ih3h1aavrodl_jn"
        message_title = "Hello App"
        message_body = "You have ....."

        # Gửi thông điệp đến thiết bị
        message = messaging.Message(
            notification=messaging.Notification(
                title=message_title,
                body=message_body,
            ),
            token=registration_token,
        )

        response = messaging.send(message)
        print('Messages sent successfully.')

        return {'success': True, 'response': response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))