from fastapi import FastAPI
from app.api.endpoints import recommendation

app = FastAPI(
    title="FarmBTI API",
    description="사용자 맞춤형 지역 추천 서비스 API"
)

app.include_router(recommendation.router, prefix="/api", tags=["recommendation"])
