import os

import redis
import uvicorn
from fastapi import FastAPI

from app.core.cloudinary_config import load_cloudinary_config
from app.exceptions.exception_handler import register_exception_handler
from app.middlewares import register_middlewares
from app.routers.router import register_router

app = FastAPI(
    swagger_ui_parameters={
        "tagsSorter": "alpha",
    }
)

# db = initialize_db()
# generate_table(db)

load_cloudinary_config()
register_exception_handler(app)
register_middlewares(app)
register_router(app)

# Approach #1: Create global variable for redis
global_cache = redis.Redis(
    host=os.environ.get('REDIS_HOST', 'localhost'),
    port=os.environ.get('REDIS_PORT', 6379),
    db=os.environ.get('REDIS_DB', 0),
    decode_responses=True
)

if __name__ == '__main__':
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, log_level="info", reload=True)
