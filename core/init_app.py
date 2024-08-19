import ssl
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.news_api import router as news_router
from api.health_check_api import router as hc_router
from core.config import settings
from fastapi import Request, Response
from datetime import timedelta
from utils import generate_session_id, get_session_id_from_cookie
# ssl._create_default_https_context = ssl._create_unverified_context

def create_app() -> FastAPI:
    app = FastAPI()

    # CORS 설정
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOW_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],  # 모든 HTTP 메소드 허용
        allow_headers=["*"]   # 모든 HTTP 헤더 허용
    )

    # 라우터 포함
    app.include_router(news_router, prefix="/news", tags=["news"])
    app.include_router(hc_router, prefix="/env", tags=["heathcheck"])

    @app.get("/")
    async def root(request: Request, response: Response):
        session_id = get_session_id_from_cookie(request)
        if not session_id:
            session_id = generate_session_id()
            response.set_cookie(key="session_id", value=session_id, httponly=True,
                                max_age=timedelta(days=1).total_seconds())
        return {"session_id": session_id}

    # 앱 시작 시 실행되는 초기화 함수
    @app.on_event("startup")
    async def startup_event():
        pass
    return app
