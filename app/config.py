import os
from dotenv import load_dotenv
from pathlib import Path

# .env 파일 로드
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

class Settings:
    PROJECT_NAME: str = "FastAPI Login System"
    PROJECT_VERSION: str = "1.0.0"
    
    # 데이터베이스 설정
    DB_USER: str = os.getenv("DB_USER", "root")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: str = os.getenv("DB_PORT", "3306")
    DB_NAME: str = os.getenv("DB_NAME", "fastapi_login")
    DATABASE_URL: str = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
    # 보안 설정
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-for-jwt")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    SESSION_COOKIE_NAME: str = "session_id"
    SESSION_EXPIRE_DAYS: int = 1
    
    # 템플릿 및 정적 파일 설정
    TEMPLATES_DIR: str = "app/templates"
    STATIC_DIR: str = "static"

settings = Settings()