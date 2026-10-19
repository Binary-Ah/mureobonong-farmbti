from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict

from app.services.recommendation import get_recommendations_from_scores

# 설문조사 답변(FARM 점수)을 위한 Pydantic 모델 정의
class SurveyInput(BaseModel):
    F: float
    A: float
    R: float
    M: float

# 추천 결과를 위한 Pydantic 모델 정의
class RecommendationResult(BaseModel):
    region_name: str
    match_score: float

router = APIRouter()

@router.post("/recommend", response_model=List[RecommendationResult])
async def get_recommendations(survey_data: SurveyInput):
    """
    사용자의 FARM 점수를 받아 추천 결과를 반환하는 API 엔드포인트입니다.
    """
    # Pydantic 모델 객체를 딕셔너리로 변환
    user_scores = survey_data.dict()

    # 서비스 파일의 함수를 호출하여 실제 추천 결과를 받습니다.
    results = get_recommendations_from_scores(user_scores)

    # 딕셔너리 리스트 형태로 반환
    return results