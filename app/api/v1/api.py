from fastapi import APIRouter

from app.api.v1.endpoints import auth, users

api_router = APIRouter()

# 인증 관련 엔드포인트
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])

# 사용자 관련 엔드포인트
api_router.include_router(users.router, prefix="/users", tags=["users"])