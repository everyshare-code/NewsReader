from fastapi import APIRouter, status
from pydantic import BaseModel
from typing import Optional
from core.config import settings

router = APIRouter()


class HealthCheck(BaseModel):
    env: Optional[str] = None
    address: Optional[str] = None
    port: Optional[int] = None
    status: str = "OK"

# Query 사용시 parameter가 없을 경우 자동으로 400에러 발생)
@router.get("",
            summary="서버 응답 확인용 API",
            response_description="HTTP Status Code 200 반환 (OK)",
            status_code=status.HTTP_200_OK,
            response_model=HealthCheck
)
async def heath_check() -> HealthCheck:
    return HealthCheck(
        status="OK",
        env=settings.ENVIRONMENT,
        address=settings.HOST,
        port=settings.PORT,
    )

