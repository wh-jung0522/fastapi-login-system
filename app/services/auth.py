from datetime import datetime, timedelta
from typing import Optional
import uuid
import json

from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.config import settings
from app.models.user import User
from app.models.session import Session as SessionModel

# 비밀번호 해싱 컨텍스트
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """비밀번호 검증"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """비밀번호 해싱"""
    return pwd_context.hash(password)

def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    """사용자 인증"""
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """JWT 액세스 토큰 생성"""
    to_encode = data.copy()
    
    # 만료 시간 설정
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    
    # 토큰 인코딩
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

# 세션 관련 함수
def create_session(db: Session, user_id: int, data: dict = None) -> str:
    """새 세션 생성"""
    session_id = str(uuid.uuid4())
    expires = datetime.utcnow() + timedelta(days=settings.SESSION_EXPIRE_DAYS)
    
    db_session = SessionModel(
        id=session_id,
        user_id=user_id,
        data=json.dumps(data) if data else "{}",
        expires=expires
    )
    
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    
    return session_id

def get_session(db: Session, session_id: str) -> Optional[SessionModel]:
    """세션 조회"""
    session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    
    # 세션이 없거나 만료된 경우
    if not session or session.expires < datetime.utcnow():
        return None
        
    return session

def delete_session(db: Session, session_id: str) -> bool:
    """세션 삭제"""
    session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    if session:
        db.delete(session)
        db.commit()
        return True
    return False

def clean_expired_sessions(db: Session) -> int:
    """만료된 세션 정리"""
    expired_sessions = db.query(SessionModel).filter(
        SessionModel.expires < datetime.utcnow()
    ).all()
    
    count = len(expired_sessions)
    
    for session in expired_sessions:
        db.delete(session)
    
    db.commit()
    return count