from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_user, get_active_session_user
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserOut, UserUpdate
from app.services.user import update_user

router = APIRouter()

@router.get("/me", response_model=UserOut)
def read_users_me(
    current_user: User = Depends(get_current_active_user)
):
    """JWT 토큰을 통한 현재 사용자 정보 조회"""
    return current_user

@router.get("/session-me", response_model=UserOut)
def read_session_me(
    current_user: User = Depends(get_active_session_user)
):
    """세션을 통한 현재 사용자 정보 조회"""
    return current_user

@router.put("/me", response_model=UserOut)
def update_user_me(
    user_in: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """현재 사용자 정보 업데이트 (JWT 인증)"""
    return update_user(db=db, user_id=current_user.id, user=user_in)

@router.put("/session-me", response_model=UserOut)
def update_session_user_me(
    user_in: UserUpdate,
    current_user: User = Depends(get_active_session_user),
    db: Session = Depends(get_db)
):
    """현재 사용자 정보 업데이트 (세션 인증)"""
    return update_user(db=db, user_id=current_user.id, user=user_in)