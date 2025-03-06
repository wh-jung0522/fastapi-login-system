from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base

class Session(Base):
    __tablename__ = "sessions"
    
    id = Column(String(36), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    data = Column(Text, nullable=True)
    expires = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 관계 설정 (선택 사항)
    user = relationship("User", backref="sessions")