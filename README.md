# FastAPI 로그인 시스템

FastAPI와 MySQL을 이용한 로그인 시스템 구현 예제입니다. 이 프로젝트는 JWT 토큰 기반 인증과 세션 기반 인증 두 가지 방식을 모두 지원합니다.

## 주요 기능

- 회원가입 및 로그인 기능
- JWT 토큰 기반 인증 (API용)
- 세션 기반 인증 (웹 페이지용)
- 사용자 프로필 정보 조회 및 수정
- MySQL 데이터베이스를 활용한 사용자 및 세션 관리

## 기술 스택

- [FastAPI](https://fastapi.tiangolo.com/): 빠르고 현대적인 Python 웹 프레임워크
- [SQLAlchemy](https://www.sqlalchemy.org/): Python SQL 툴킷 및 ORM 
- [MySQL](https://www.mysql.com/): 데이터베이스
- [Jinja2](https://jinja.palletsprojects.com/): HTML 템플릿 엔진
- [jose](https://python-jose.readthedocs.io/): JWT 구현을 위한 라이브러리
- [Passlib](https://passlib.readthedocs.io/): 비밀번호 해싱 라이브러리

## 설치 및 설정

### 사전 요구사항

- Python 3.7 이상
- MySQL 서버

### 설치 방법

1. 저장소 클론:
```bash
git clone <repository-url>
cd fastapi-login-system
```

2. 가상 환경 생성 및 활성화:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
```

3. 필요한 패키지 설치:
```bash
pip install -r requirements.txt
```

4. MySQL 데이터베이스 생성:
```sql
CREATE DATABASE fastapi_login;
```

5. `.env` 파일 설정:
   - `.env` 파일에서 데이터베이스 연결 정보와 비밀 키를 수정

### 실행 방법

```bash
uvicorn app.main:app --reload
```

서버가 시작되면 `http://localhost:8000`으로 접속할 수 있습니다.

## API 문서

FastAPI에서 제공하는 자동 문서를 통해 API를 확인할 수 있습니다:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 프로젝트 구조

```
fastapi-login-system/
├── app/                    # 애플리케이션 코드
│   ├── main.py             # 애플리케이션 진입점
│   ├── config.py           # 설정 파일
│   ├── database.py         # 데이터베이스 연결 설정
│   ├── models/             # 데이터베이스 모델
│   ├── schemas/            # Pydantic 스키마
│   ├── services/           # 비즈니스 로직
│   ├── api/                # API 라우터
│   └── templates/          # HTML 템플릿
├── static/                 # 정적 파일
├── requirements.txt        # 필요한 패키지
├── .env                    # 환경 변수
└── README.md               # 프로젝트 설명
```

## 인증 흐름

### JWT 토큰 기반 인증 (API용)

1. 클라이언트가 `/api/v1/auth/login`에 사용자 인증 정보 전송
2. 서버는 인증 정보를 검증하고 JWT 토큰 발급
3. 클라이언트는 이후 요청에 `Authorization: Bearer {token}` 헤더를 포함
4. 서버는 토큰을 검증하고 요청 처리

### 세션 기반 인증 (웹 페이지용)

1. 클라이언트가 `/api/v1/auth/session-login`에 사용자 인증 정보 전송
2. 서버는 인증 정보를 검증하고 세션을 생성하여 데이터베이스에 저장
3. 세션 ID가 쿠키에 저장됨
4. 이후 요청에서 서버는 쿠키를 통해 세션 확인
5. 서버는 세션을 검증하고 요청 처리

## 라이선스

이 프로젝트는 MIT 라이선스하에 배포됩니다.