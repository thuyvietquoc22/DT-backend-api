import base64

import requests
from fastapi import HTTPException
from pydantic import BaseModel, Field

from app.core.config import settings
from app.utils.utils_logging import logger


class UserTwitterResponseModel(BaseModel):
    access_token: str = Field(...,
                              example='IGQVJVZAHN4RFdqWHFYdGNiWGJQUnB2T2dpdHpEYWFnSjZAIN2V4OFd6TnM2UE1aaFJma0p....')
    token_type: str = Field(..., example='bearer')
    expires_in: int = Field(..., example=7200)
    scope: str = Field(..., example='users.read follows.read tweet.read follows.write offline.access')


API_TWITTER_URL = 'https://api.twitter.com/2/'


def get_access_token_twitter(code: str):
    url = API_TWITTER_URL + 'oauth2/token'
    payload = {
        'client_id': settings.TWITTER_CLIENT_ID,
        'grant_type': 'authorization_code',
        'code_verifier': 'challenge',
        'redirect_uri': settings.TWITTER_REDIRECT_URI,
        'code': code
    }
    credentials = f'{settings.TWITTER_USERNAME}:{settings.TWITTER_PASSWORD}'.encode('ascii')
    base64_credentials = base64.b64encode(credentials).decode('ascii')
    # set up the headers
    headers = {
        'Authorization': f'Basic {base64_credentials}',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    response = requests.post(url, headers=headers, data=payload)

    if response.status_code == 200:
        data = response.json()
        twitter_info = get_user_info_twitter(data['access_token'])
        data['user_id'] = twitter_info['data']['id']
        data['user_name'] = twitter_info['data']['username']
        return data
    else:
        logger.error(f'Failed to call get_access_token_twitter API: {response.text}')
        raise HTTPException(status_code=400, detail='Failed to call Twitter API')


def get_user_info_twitter(access_token: str):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    params = {
        "moblie.fields": "created_at,description,id,location,name,profile_image_url,url,username"
    }
    response = requests.get(
        f"{API_TWITTER_URL}users/me", headers=headers, params=params
    )
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        logger.error(f'Failed to call get_user_info_twitter API: {response.text}')
        raise HTTPException(status_code=400, detail='Failed to call Twitter API')


def get_my_post_twitter(access_token: str, user_id: int, since: str, until: str):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    params = {
        'max_results': 100,
        'expansions': 'attachments.media_keys,author_id',
        'tweet.fields': 'attachments,author_id,context_annotations,conversation_id,created_at,id,'
                        'in_reply_to_user_id,lang,possibly_sensitive,public_metrics,referenced_tweets,'
                        'reply_settings,source,text,withheld,edit_history_tweet_ids',
        'media.fields': 'duration_ms,height,media_key,preview_image_url,type,url,width,alt_text,variants',
        'moblie.fields': 'created_at,id,name,profile_image_url,public_metrics,url,username',
        'end_time': until,
    }
    if since:
        params['start_time'] = since
    url = f"{API_TWITTER_URL}users/{user_id}/tweets"

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        if response.status_code == 401 and response.reason == 'Unauthorized':
            return response.json()
        logger.error(f'Failed to call get_my_post_twitter API: {response.text}')
        raise HTTPException(status_code=400, detail='Failed to call Twitter API')


def refresh_access_token(refresh_token: str):
    url = API_TWITTER_URL + 'oauth2/token'
    payload = {
        'client_id': settings.TWITTER_CLIENT_ID,
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    }

    response = requests.post(url, data=payload)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        logger.error(f'Failed to call get_access_token_twitter API: {response.text}')
        raise HTTPException(status_code=400, detail='Failed to call Twitter API')

