import streamlit as st
import pandas as pd
import numpy as np
import os

# --- 페이지 기본 설정 ---
st.set_page_config(page_title="찾아보농", page_icon="🌾")

# --- 커스텀 CSS ---
st.markdown("""
<style>
    /* Streamlit 기본 버튼을 찾아서 색상 변경 */
    .stButton > button {
        border-color: #2E7D32; /* 테두리 색 */
        background-color: #4CAF50; /* 배경색 */
        color: white; /* 글자색 */
    }
    /* 마우스를 올렸을 때 색상 변경 */
    .stButton > button:hover {
        background-color: #2E7D32;
        border-color: #2E7D32;
    }
    /* 설문 문항 텍스트 크기 키우기 (st.radio에서는 markdown으로 처리) */
</style>
""", unsafe_allow_html=True)


# --- 데이터 로딩 ---
@st.cache_data
def load_data():
    try:
        current_file_path = os.path.abspath(__file__)
        pages_dir = os.path.dirname(current_file_path)
        project_root = os.path.dirname(pages_dir)
        database_dir = os.path.join(project_root, 'database')
        region_data_path = os.path.join(database_dir, "region_data.csv")
        crop_data_path = os.path.join(database_dir, "crop_data.csv")
        
        if not os.path.exists(region_data_path) or not os.path.exists(crop_data_path):
            st.error("데이터 파일을 찾을 수 없습니다. 'database' 폴더에 region_data.csv와 crop_data.csv 파일이 있는지 확인해주세요.")
            return None, None
            
        region_df = pd.read_csv(region_data_path, encoding='utf-8')
        crop_df = pd.read_csv(crop_data_path, encoding='utf-8')
        
        return region_df, crop_df
        
    except Exception as e:
        st.error(f"데이터 파일 로딩 중 오류가 발생했습니다: {e}")
        return None, None

# 데이터 로드 실행
region_data, crop_data = load_data()

# --- 설문 문항 및 로직 ---
QUESTIONS = {
    'Q1': "나는 한 번 시작한 일은 결과가 나올 때까지 끈기 있게 파고드는 편이다. (성실성)",
    'Q2': "나는 병충해나 기후 변화 같은 돌발 상황에 꼼꼼하게 계획을 세워 대처하는 것을 즐긴다. (계획성)",
    'Q3': "나는 1년 내내 땀 흘려 일하더라도 안정적이고 예측 가능한 결과를 얻는 것이 중요하다. (안정성)",
    'Q4': "나는 빠르게 수확해서 바로 수익을 낼 수 있는 실용적인 방식을 선호한다. (효율성)",
    'Q5': "나는 드론, 빅데이터, 스마트팜 등 최신 기술을 활용하는 것에 큰 매력을 느낀다. (기술 수용성)",
    'Q6': "농사가 주 수입원이 아니어도 좋다. 자연과 함께하는 여유로운 삶이 더 중요하다. (워라밸)",
    'Q7': "나는 이웃과 함께 품앗이하고 마을 행사에 참여하는 공동체적인 삶을 꿈꾼다. (공동체성)",
    'Q8': "초기 투자 비용이 들더라도, 성공했을 때 높은 수익을 기대할 수 있는 일에 도전하고 싶다. (위험 감수)",
    'Q9': "나는 최소한의 노력으로 최대의 효율을 내는 자동화된 시스템을 구축하고 싶다. (자동화 선호)",
    'Q10': "나는 복잡한 관리 없이, 심어두면 알아서 잘 자라는 품종이 마음 편하고 좋다. (단순함 선호)"
}

# 각 질문이 어떤 지역 특성과 연결되는지 매핑
QUESTION_TO_FEATURE_MAP = {
    'Q1': '소비자물가지수',      # 성실성 -> 안정적 소비 환경
    'Q2': '면적당 병원 수',     # 계획성 -> 인프라 중요
    'Q3': '공시지가',             # 안정성 -> 안정적 자산 가치
    'Q4': '㎡당 거래가(만원)',  # 효율성 -> 활발한 거래
    'Q5': '면적당 학교 수',     # 기술 수용성 -> 교육/혁신 인프라
    'Q6': '녹지 비율',           # 워라밸 -> 자연 환경
    'Q7': '커뮤니티 활성화 지수',# 공동체성 -> 활발한 커뮤니티
    'Q8': '인구밀도 (명/㎢)',   # 위험 감수 -> 도시화/시장 접근성
    'Q9': '대기질 지수',         # 자동화 선호 -> 쾌적한 환경
    'Q10': '수질 지수',          # 단순함 선호 -> 깨끗한 자연환경
}
# 지역 데이터에서 사용할 특성 컬럼 목록
FEATURE_COLS = list(QUESTION_TO_FEATURE_MAP.values())

SCORING_MATRIX = {
    'Q1': ['벼보농', '사과보농'], 'Q2': ['사과보농', '고구마보농'], 'Q3': ['벼보농', '고구마보농'],
    'Q4': ['상추보농'], 'Q5': ['도전보농'], 'Q6': ['힐링보농'],
    'Q7': ['힐링보농', '고구마보농'], 'Q8': ['도전보농', '사과보농'], 'Q9': ['도전보농', '상추보농'],
    'Q10': ['벼보농', '힐링보농']
}
TYPE_DESCRIPTIONS = {
    '벼보농': "끈기 있고 묵묵하게 해내는 당신은 '벼보농' 타입! 안정적인 환경에서 성실하게 목표를 달성하는 것을 선호하는군요.",
    '사과보농': "꼼꼼하고 기다림에 익숙한 당신은 '사과보농' 타입! 장기적인 안목으로 정성을 들여 고품질의 결과를 만들어내는군요.",
    '고구마보농': "따뜻하고 성실한 당신은 '고구마보농' 타입! 사람들과 어울리며 묵묵히 자신의 역할을 다하는 모습이 돋보여요.",
    '상추보농': "빠른 성과와 실용성을 중시하는 당신은 '상추보농' 타입! 효율적인 방식으로 빠르게 결과를 확인하는 것을 즐기는군요.",
    '도전보농': "새로운 기술에 대한 호기심이 많은 당신은 '도전보농' 타입! 스마트팜과 같은 혁신적인 기술로 농업의 미래를 이끌고 싶어해요.",
    '힐링보농': "전원생활의 여유를 꿈꾸는 당신은 '힐링보농' 타입! 수익보다는 자연과 함께하는 삶과 공동체의 가치를 더 중요하게 생각하는군요."
}

# --- 최종 추천 로직 ---
def cosine_similarity(arr1, arr2):
    dot_product = np.dot(arr1, arr2)
    norm1 = np.linalg.norm(arr1)
    norm2 = np.linalg.norm(arr2)
    return dot_product / (norm1 * norm2) if norm1 > 0 and norm2 > 0 else 0.0

def calculate_archetype_and_vector(answers):
    scores = {type_name: 0 for type_name in TYPE_DESCRIPTIONS.keys()}
    user_vector = []
    score_map = {'전혀 그렇지 않다': 1, '그렇지 않다': 2, '보통이다': 3, '그렇다': 4, '매우 그렇다': 5}
    
    # Q1부터 Q10까지 순서대로 user_vector 생성
    for q_id in QUESTIONS.keys():
        answer_text = answers.get(q_id, '보통이다')
        score = score_map.get(answer_text, 3)
        user_vector.append(score)
        
        if q_id in SCORING_MATRIX:
            for farm_type in SCORING_MATRIX[q_id]:
                if farm_type in scores:
                    scores[farm_type] += score
                    
    final_type = max(scores, key=scores.get)
    return final_type, scores, np.array(user_vector)

def recommend_regions(user_vector, region_df):
    if not all(col in region_df.columns for col in FEATURE_COLS):
        st.error("지역 데이터에 필요한 컬럼이 부족합니다. CSV 파일을 확인해주세요.")
        return pd.DataFrame()

    # 지역 데이터를 0~1 사이 값으로 정규화 (Min-Max Scaling)
    normalized_df = region_df.copy()
    for col in FEATURE_COLS:
        min_val = normalized_df[col].min()
        max_val = normalized_df[col].max()
        if (max_val - min_val) > 0:
            normalized_df[col] = (normalized_df[col] - min_val) / (max_val - min_val)
        else:
            normalized_df[col] = 0 # 모든 값이 같을 경우
            
    # 사용자 벡터를 0~1 사이 값으로 정규화 (1~5 점수 -> 0~1)
    normalized_user_vector = (user_vector - 1) / 4

    # 코사인 유사도 계산
    normalized_df['similarity'] = normalized_df.apply(
        lambda row: cosine_similarity(row[FEATURE_COLS].values.astype(float), normalized_user_vector), axis=1
    )
    return normalized_df.nlargest(3, 'similarity')

def recommend_crops(final_type, top_regions, crop_df):
    recommendations = {}
    original_indices = top_regions.index # 추천된 지역의 원본 인덱스
    
    for idx in original_indices:
        region = region_data.loc[idx] # 원본 데이터프레임에서 지역 정보 가져오기
        region_name = region['full_region']
        
        matched_crops = crop_df[crop_df['추천유형'] == final_type]
        if not matched_crops.empty:
            recommendations[region_name] = matched_crops.head(2).to_dict('records')
        else:
            # 매칭되는 작물이 없으면 전체 작물 중 랜덤 추천
            recommendations[region_name] = crop_df.sample(2).to_dict('records')
    return recommendations


# --- Streamlit UI 페이지 관리 ---
if 'page' not in st.session_state:
    st.session_state.page = 'intro'

if region_data is not None and crop_data is not None:
    if st.session_state.page == 'intro':
        st.title("🌾 찾아보농")
        st.markdown("#### 나는 어떤 농부가 될 수 있을까?")
        st.markdown("간단한 테스트를 통해 나에게 꼭 맞는 귀농 지역과 추천 작물을 알아보세요!")
        if st.button("테스트 시작하기", use_container_width=True):
            st.session_state.page = 'survey'
            st.session_state.answers = {q_id: '보통이다' for q_id in QUESTIONS}
            st.rerun()

    elif st.session_state.page == 'survey':
        st.title("🔍 나의 귀농 스타일 찾기")
        st.markdown("##### 각 질문에 대해 자신의 생각과 얼마나 일치하는지 선택해주세요.")
        
        options = ['전혀 그렇지 않다', '그렇지 않다', '보통이다', '그렇다', '매우 그렇다']
        
        with st.form("survey_form"):
            for q_id, question in QUESTIONS.items():
                st.markdown(f"**{question}**")
                st.session_state.answers[q_id] = st.radio(
                    "답변 선택", 
                    options, 
                    index=options.index(st.session_state.answers.get(q_id, '보통이다')), 
                    key=f"{q_id}_radio",
                    horizontal=True,
                    label_visibility="collapsed"
                )
                st.markdown("---")

            if st.form_submit_button("결과 보기", use_container_width=True):
                st.session_state.page = 'result'
                st.rerun()

    elif st.session_state.page == 'result':
        st.title("💡 '찾아보농' 테스트 결과")
        st.balloons()
        
        answers = st.session_state.answers
        final_type, scores, user_vector = calculate_archetype_and_vector(answers)
        top_regions = recommend_regions(user_vector, region_data)
        crop_recommendations = recommend_crops(final_type, top_regions, crop_data)
        
        st.markdown("### 당신의 귀농 유형은...")
        col1, col2 = st.columns([1, 2])
        
        with col1:
            try:
                current_file_path = os.path.abspath(__file__)
                pages_dir = os.path.dirname(current_file_path)
                project_root = os.path.dirname(pages_dir)
                assets_dir = os.path.join(project_root, 'assets')
                image_path = os.path.join(assets_dir, f"{final_type}.png")
                
                if os.path.exists(image_path):
                    st.image(image_path, width=200)
                else:
                    st.markdown(f"""
                    <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #E8F5E8 0%, #C8E6C9 100%); border-radius: 20px; border: 3px solid #2E7D32; box-shadow: 0 8px 25px rgba(46, 125, 50, 0.3);">
                        <div style="font-size: 4em; margin-bottom: 1rem;">🌾</div>
                        <div style="font-size: 1.5em; font-weight: bold; color: #1B5E20;">{final_type}</div>
                    </div>
                    """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"결과 이미지를 표시하는 중 오류: {e}")

        with col2:
            st.markdown(f"## **{final_type}**")
            st.markdown(f"#### {TYPE_DESCRIPTIONS.get(final_type, '결과를 분석 중입니다.')}")
        
        st.markdown("---")

        st.markdown("### 🌟 당신을 위한 추천 지역과 작물은?")
        if not top_regions.empty:
            for region_name, crops in crop_recommendations.items():
                with st.container(border=True):
                    st.markdown(f"#### 📍 {region_name}")
                    if crops:
                        for crop in crops:
                            st.success(f"**추천 작물: {crop.get('작물명', 'N/A')}** - {crop.get('특징', 'N/A')}")
                    else:
                        st.warning("이 지역에 대한 맞춤 작물 정보가 아직 준비되지 않았어요.")
        else:
            st.warning("추천 지역을 계산하는 데 문제가 발생했습니다.")
        
        st.markdown("---")
        if st.button("테스트 다시하기", use_container_width=True):
            st.session_state.page = 'intro'
            if 'answers' in st.session_state:
                del st.session_state.answers
            st.rerun()

else:
    st.error("데이터를 불러오지 못해 앱을 실행할 수 없습니다. 파일 경로와 내용을 확인해주세요.")
