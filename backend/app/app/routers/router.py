from fastapi import APIRouter

from app.routers.auth.auth import AuthRouter

api_router = APIRouter()

# db = initialize_db()


# Authenticate
auth_router = AuthRouter()

api_router.include_router(auth_router.router)
