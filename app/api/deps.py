from typing import Generator, Optional
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.token import TokenData
from app.config import settings
from app.services.auth import get_session
from app.services.user import get_user_by_username, get_user_by_id

# OAuth2 스키마 설정
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """JWT 토큰으로 현재 사용자 가져오기"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # 토큰 디코딩
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        
        if username is None:
            raise credentials_exception
            
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    # 사용자 조회
    user = get_user_by_username(db, username=token_data.username)
    
    if user is None:
        raise credentials_exception
    
    return user

async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """활성 상태인 현재 사용자 가져오기"""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user

async def get_session_user(
    request: Request,
    db: Session = Depends(get_db)
) -> Optional[User]:
    """세션에서 현재 사용자 가져오기"""
    session_id = request.cookies.get(settings.SESSION_COOKIE_NAME)
    
    if not session_id:
        return None
    
    session = get_session(db, session_id)
    
    if not session:
        return None
    
    user = get_user_by_id(db, session.user_id)
    
    return user

async def get_active_session_user(
    user: Optional[User] = Depends(get_session_user)
) -> User:
    """세션에서 활성 상태인 현재 사용자 가져오기 (없으면 예외 발생)"""
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    return user