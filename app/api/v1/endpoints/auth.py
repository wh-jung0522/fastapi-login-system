from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.deps import get_session_user
from app.database import get_db
from app.schemas.token import Token, SessionResponse
from app.schemas.user import UserCreate, UserOut
from app.services.auth import (
    authenticate_user, 
    create_access_token, 
    create_session, 
    delete_session
)
from app.services.user import create_user
from app.config import settings

router = APIRouter()

@router.post("/register", response_model=UserOut)
def register(
    user_in: UserCreate,
    db: Session = Depends(get_db)
):
    """새 사용자 등록"""
    return create_user(db=db, user=user_in)

@router.post("/login", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """사용자 로그인 (JWT 토큰 발급)"""
    # 사용자 인증
    user = authenticate_user(db, form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 토큰 만료 시간 설정
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # 토큰 생성
    access_token = create_access_token(
        data={"sub": user.username}, 
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/session-login", response_model=SessionResponse)
def login_with_session(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """사용자 로그인 (세션 기반)"""
    # 사용자 인증
    user = authenticate_user(db, form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    # 세션 생성
    session_id = create_session(db, user.id)
    
    # 쿠키 설정
    response.set_cookie(
        key=settings.SESSION_COOKIE_NAME, 
        value=session_id,
        httponly=True,
        max_age=settings.SESSION_EXPIRE_DAYS * 24 * 60 * 60,  # 일 -> 초
        samesite="lax"
    )
    
    return {"message": "Login successful"}

@router.post("/logout", response_model=SessionResponse)
def logout(
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
    user = Depends(get_session_user)
):
    """로그아웃 (세션 기반)"""
    # 사용자가 인증되어 있지 않으면 에러 없이 처리
    if user:
        # 세션 아이디 가져오기
        session_id = request.cookies.get(settings.SESSION_COOKIE_NAME)
        
        if session_id:
            # 세션 삭제
            delete_session(db, session_id)
    
    # 쿠키 삭제
    response.delete_cookie(key=settings.SESSION_COOKIE_NAME)
    
    return {"message": "Logout successful"}