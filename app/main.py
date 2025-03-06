from fastapi import Depends, FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from starlette.middleware.sessions import SessionMiddleware

from app.api.api import api_router
from app.config import settings
from app.database import engine, Base
from app.api.deps import get_session_user

# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)

# FastAPI 앱 생성
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION
)

# 세션 미들웨어 추가
app.add_middleware(
    SessionMiddleware, 
    secret_key=settings.SECRET_KEY
)

# 정적 파일 마운트
app.mount("/static", StaticFiles(directory=settings.STATIC_DIR), name="static")

# 템플릿 설정
templates = Jinja2Templates(directory=settings.TEMPLATES_DIR)

# API 라우터 등록
app.include_router(api_router, prefix="/api")

# 웹 페이지 라우트
@app.get("/", response_class=HTMLResponse)
async def home(request: Request, user = Depends(get_session_user)):
    """홈 페이지"""
    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "user": user}
    )

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request, user = Depends(get_session_user)):
    """로그인 페이지"""
    # 이미 로그인되어 있으면 홈으로 리다이렉트
    if user:
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url="/")
    
    return templates.TemplateResponse(
        "login.html", 
        {"request": request}
    )

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request, user = Depends(get_session_user)):
    """회원가입 페이지"""
    # 이미 로그인되어 있으면 홈으로 리다이렉트
    if user:
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url="/")
    
    return templates.TemplateResponse(
        "register.html", 
        {"request": request}
    )

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request, user = Depends(get_active_session_user)):
    """대시보드 페이지 (로그인 필요)"""
    return templates.TemplateResponse(
        "dashboard.html", 
        {"request": request, "user": user}
    )

# 실행 명령: uvicorn app.main:app --reload