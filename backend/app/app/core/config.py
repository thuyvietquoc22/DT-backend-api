import os.path
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BasePath = Path(__file__).resolve().parent.parent.parent
env_path = os.path.join(BasePath, os.environ.get('ENV_FILE', 'dev.env'))


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=env_path, env_file_encoding='utf-8')

    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = 'dt.secret_key'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 5
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    BACKEND_CORS_ORIGINS: str = "*"

    ENV: str = "local"
    AWS_DB_ENDPOINT_URL: str = ""
    AWS_REGION_NAME: str = "ap-northeast-1"
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    COGNITO_USER_POOL_ID: str = ""
    COGNITO_CLIENT_ID: str = ""
    BUCKET_NAME: str = "app.your-studio.site"
    BUCKET_SNS_CONVERTED: str = "sns-converted"
    SENDER_EMAIL: str = 'test@x.com'
    FIREBASE_DATABASE_URL: str = 'test'

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6380
    JWT_SECRET_KEY: str = SECRET_KEY

    OPEN_SEARCH_HOST: str = ''
    OPEN_SEARCH_USERNAME: str = ''
    OPEN_SEARCH_PASSWORD: str = ''
    OPEN_SEARCH_PORT: str = '443'
    OPEN_SEARCH_OS_USER_INDEX: str = 'develop_users'
    OPEN_SEARCH_OS_POST_INDEX: str = 'develop_posts'

    DEFAULT_PASSWORD: str = 'Test123@'

    NUMBER_THREADS: int = 5
    CLOUDFRONT_DOMAIN: str = ""
    CLOUDFRONT_DISTRIBUTION_ID: str = ""

    # AES_KEY
    AES_KEY: str = "1234567890123456"
    # IV
    AES_IV: str = "1234567890123456"

    # MONGODB_URL
    MONGODB_URL: str = "mongodb+srv://quocthinhtme:dQ1T85lyamzav2LN@digitaltwin.ln93u1m.mongodb.net/?retryWrites=true&w=majority&appName=DigitalTwin"
    # MONGODB_URL: str = "mongodb://localhost:27017"

    # CLOUDINARY
    CLOUDINARY_CLOUD_NAME: str = "dunezoucn"
    CLOUDINARY_API_KEY: str = "727316736938961"
    CLOUDINARY_API_SECRET: str = "dryjjj8kaOZKknQDhcdha29FGKI"
    CLOUDINARY_URL: str = "CLOUDINARY_URL=cloudinary://727316736938961:dryjjj8kaOZKknQDhcdha29FGKI@dunezoucn"

    # MAP 4D KEY
    MAP_4D_KEY: str = "7e24e8dae5b5b72a7d742a9b38444128"


settings = Settings()
