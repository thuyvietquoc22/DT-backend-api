from fastapi import APIRouter

from app.domain.auth.auth import AuthDomain

from app.routers.auth.auth import AuthRouter

api_router = APIRouter()

# db = initialize_db()


# Auth
auth_domain = AuthDomain(

)
auth_router = AuthRouter(auth_domain)


api_router.include_router(auth_router.router)

