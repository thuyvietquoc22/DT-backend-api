import os
import redis
import uvicorn
from fastapi import FastAPI
from app.core.config import settings
# from app.db.main import generate_table
from app.internal.db import initialize_db
from app.routers.router import api_router

app = FastAPI()

# db = initialize_db()
# generate_table(db)
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get('/')
def index():
    return 'Hello World!'


# Approach #1: Create global variable for redis
global_cache = redis.Redis(
    host=os.environ.get('REDIS_HOST', 'localhost'),
    port=os.environ.get('REDIS_PORT', 6379),
    db=os.environ.get('REDIS_DB', 0),
    decode_responses=True
)

if __name__ == '__main__':
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, log_level="info", reload=True)
