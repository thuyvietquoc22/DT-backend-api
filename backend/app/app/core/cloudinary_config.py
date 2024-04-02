import cloudinary
import cloudinary.api
import cloudinary.uploader

from app.core.config import settings


def load_cloudinary_config():
    cloudinary.config(
        cloud_name=settings.CLOUDINARY_CLOUD_NAME,
        api_key=settings.CLOUDINARY_API_KEY,
        api_secret=settings.CLOUDINARY_API_SECRET,
        secure=True
    )
