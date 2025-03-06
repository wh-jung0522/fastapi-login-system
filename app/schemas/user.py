from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

# 사용자 생성 시 필요한 정보
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)

# 사용자 업데이트 시 사용되는 스키마
class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8)
    is_active: Optional[bool] = None

# 사용자 정보를 반환할 때 사용되는 스키마
class UserOut(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# 로그인 시 사용되는 스키마
class UserLogin(BaseModel):
    username: str
    password: str