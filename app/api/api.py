from fastapi import APIRouter

from app.api.v1.api import api_router as api_v1_router

api_router = APIRouter()

# API v1 라우터 포함
api_router.include_router(api_v1_router, prefix="/v1")