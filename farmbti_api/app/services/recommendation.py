import pandas as pd
import numpy as np

try:
    # 데이터 파일 경로를 정확하게 지정해주세요.
    df_regions = pd.read_csv("./data/FARM_normalized_updated.csv")
except FileNotFoundError:
    df_regions = None

def calculate_cosine_similarity(arr1: np.ndarray, arr2: np.ndarray) -> float:
    """두 벡터 간 코사인 유사도를 계산합니다."""
    dot_product = np.dot(arr1, arr2)
    norm1 = np.linalg.norm(arr1)
    norm2 = np.linalg.norm(arr2)
    return float(dot_product / (norm1 * norm2)) if norm1 != 0 and norm2 != 0 else 0.0

def get_recommendations_from_scores(user_scores: dict, top_k: int = 3):
    """
    사용자 FARM 점수를 기반으로 추천 지역을 반환합니다.
    """
    if df_regions is None:
        return []

    # 사용자 점수를 기반으로 10차원 벡터 생성
    # 이 벡터는 각 FARM 요소에 대한 점수를 10개의 지역 특징에 매핑합니다.
    user_vector = np.array([
        user_scores["F"], user_scores["F"], user_scores["F"],
        user_scores["A"], user_scores["A"],
        user_scores["R"], user_scores["R"],
        user_scores["M"], user_scores["M"], user_scores["M"]
    ])

    # 지역별 특징 벡터와 유사도 계산
    # 이 로직은 pandas.apply()를 사용하며, DataFrame의 각 행에 대해 유사도를 계산합니다.
    df_regions['similarity'] = df_regions.apply(
        lambda row: calculate_cosine_similarity(
            np.array(row[["공시지가", "㎡당 거래가(만원)", "소비자물가지수",
                          "면적당 학교 수", "면적당 병원 수", "인구밀도 (명/㎢)",
                          "커뮤니티 활성화 지수", "대기질 지수", "수질 지수", "녹지 비율"]]),
            user_vector
        ), axis=1
    )

    # 유사도가 높은 상위 N개 지역 추천
    recommended = df_regions.nlargest(top_k, 'similarity')

    return recommended[['full_region', 'similarity']].to_dict('records')