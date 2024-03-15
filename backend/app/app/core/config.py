from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = 'dt.secret_key'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 5
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    BACKEND_CORS_ORIGINS: str = "http://localhost:3000"

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

    # MONGODB_URL
    MONGODB_URL: str = "mongodb://localhost:27017"

    class Config:
        case_sensitive = True


settings = Settings()
