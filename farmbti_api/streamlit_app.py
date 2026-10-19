import streamlit as st
import pandas as pd
import numpy as np
import openai  # OpenAI 라이브러리 추가

# --- 데이터 로딩 ---
@st.cache_data
def load_data():
    try:
        region_df = pd.read_csv("data/region_data.csv")
        crop_df = pd.read_csv("data/crop_data.csv")
        return region_df, crop_df
    except FileNotFoundError as e:
        st.error(f"데이터 파일 로딩 오류: {e}. 'data' 폴더에 region_data.csv와 crop_data.csv 파일이 있는지 확인해주세요.")
        return None, None

region_data, crop_data = load_data()

# --- 설문 문항 및 채점 로직 (기존과 동일) ---
QUESTIONS = {
    'Q1': "나는 한 번 시작한 일은 결과가 나올 때까지 끈기 있게 파고드는 편이다.",
    'Q2': "나는 병충해나 기후 변화 같은 돌발 상황에 꼼꼼하게 계획을 세워 대처하는 것을 즐긴다.",
    'Q3': "나는 1년 내내 땀 흘려 일하더라도 안정적이고 예측 가능한 결과를 얻는 것이 중요하다.",
    'Q4': "나는 빠르게 수확해서 바로 수익을 낼 수 있는 실용적인 방식을 선호한다.",
    'Q5': "나는 드론, 빅데이터, 스마트팜 등 최신 기술을 활용하는 것에 큰 매력을 느낀다.",
    'Q6': "농사가 주 수입원이 아니어도 좋다. 자연과 함께하는 여유로운 삶이 더 중요하다.",
    'Q7': "나는 이웃과 함께 품앗이하고 마을 행사에 참여하는 공동체적인 삶을 꿈꾼다.",
    'Q8': "초기 투자 비용이 들더라도, 성공했을 때 높은 수익을 기대할 수 있는 일에 도전하고 싶다.",
    'Q9': "나는 최소한의 노력으로 최대의 효율을 내는 자동화된 시스템을 구축하고 싶다.",
    'Q10': "나는 복잡한 관리 없이, 심어두면 알아서 잘 자라는 품종이 마음 편하고 좋다."
}

SCORING_MATRIX = {
    'Q1': ['벼보농', '사과보농'], 'Q2': ['사과보농', '고구마보농'], 'Q3': ['벼보농', '고구마보농'],
    'Q4': ['상추보농'], 'Q5': ['도전보농'], 'Q6': ['힐링보농'],
    'Q7': ['힐링보농', '고구마보농'], 'Q8': ['도전보농', '사과보농'], 'Q9': ['도전보농', '상추보농'],
    'Q10': ['벼보농', '힐링보농']
}

TYPE_DESCRIPTIONS = {
    '벼보농': "끈기 있고 묵묵하게 해내는 당신은 '벼보농' 타입!",
    '사과보농': "꼼꼼하고 기다림에 익숙한 당신은 '사과보농' 타입!",
    '고구마보농': "따뜻하고 성실한 당신은 '고구마보농' 타입!",
    '상추보농': "빠른 성과와 실용성을 중시하는 당신은 '상추보농' 타입!",
    '도전보농': "새로운 기술에 대한 호기심이 많은 당신은 '도전보농' 타입!",
    '힐링보농': "전원생활의 여유를 꿈꾸는 당신은 '힐링보농' 타입!"
}

# --- ✨ 개선된 추천 엔진 클래스 ---
class RecommendationEngine:
    def __init__(self, region_df, crop_df):
        self.region_df = region_df
        self.crop_df = crop_df
        self.feature_cols = ['공시지가', '㎡당 거래가(만원)', '소비자물가지수', '면적당 학교 수', '면적당 병원 수', 
                             '인구밀도 (명/㎢)', '커뮤니티 활성화 지수', '대기질 지수', '수질 지수', '녹지 비율']

    def _cosine_similarity(self, arr1, arr2):
        dot_product = np.dot(arr1, arr2)
        norm1 = np.linalg.norm(arr1)
        norm2 = np.linalg.norm(arr2)
        return dot_product / (norm1 * norm2) if norm1 > 0 and norm2 > 0 else 0.0

    def _calculate_user_vectors(self, answers):
        user_region_vector = np.array([
            (answers.get('Q3', 3) + answers.get('Q8', 3)) / 2, (answers.get('Q8', 3) + answers.get('Q4', 3)) / 2,
            answers.get('Q3', 3), answers.get('Q11', 3) if 'Q11' in answers else 3, answers.get('Q11', 3) if 'Q11' in answers else 3,
            answers.get('Q7', 3), answers.get('Q7', 3), (answers.get('Q6', 3) + (6 - answers.get('Q5', 3))) / 2,
            answers.get('Q6', 3), answers.get('Q6', 3)
        ])
        user_region_vector = (user_region_vector - 1) / 4

        user_care_vector = np.array([
            (answers.get('Q2', 3) + (6 - answers.get('Q10', 3))) / 2, (answers.get('Q1', 3) + answers.get('Q3', 3)) / 2,
            answers.get('Q8', 3), (answers.get('Q5', 3) + answers.get('Q9', 3)) / 2
        ])
        user_care_vector = (user_care_vector - 1) / 4
        return user_region_vector, user_care_vector

    def _recommend_regions_cosine(self, user_region_vector, top_n=10):
        self.region_df['similarity'] = self.region_df.apply(
            lambda row: self._cosine_similarity(row[self.feature_cols].values.astype(float), user_region_vector), axis=1
        )
        return self.region_df.nlargest(top_n, 'similarity')

    def _get_llm_recommendations(self, answers, candidate_regions_df):
        user_profile = ", ".join([f"{QUESTIONS[q_id]}: {score}점" for q_id, score in answers.items()])
        candidate_info = "\n".join([f"- {row['full_region']}: {row['한줄평']}" for _, row in candidate_regions_df.iterrows()])
        prompt = f"""
        당신은 대한민국 최고의 귀농귀촌 컨설턴트입니다. 다음 정보를 바탕으로 사용자에게 가장 적합한 지역 3곳과 그 이유를 창의적인 '한줄평'으로 추천해주세요.
        [사용자 설문 결과]: {user_profile}
        [추천 후보 지역 목록]:\n{candidate_info}
        
        결과는 아래 형식으로만 응답해주세요:
        지역명1: 생성된 한줄평1
        지역명2: 생성된 한줄평2
        지역명3: 생성된 한줄평3
        """
        try:
            # st.secrets를 사용하여 API 키를 안전하게 관리하는 것을 권장합니다.
            # 예: openai.api_key = st.secrets["OPENAI_API_KEY"]
            # response = openai.ChatCompletion.create(...) 
            
            # --- API 호출 코드 (실제 사용 시 주석 해제) ---
            # response = openai.chat.completions.create(
            #     model="gpt-4-turbo",
            #     messages=[{"role": "user", "content": prompt}]
            # )
            # llm_response_text = response.choices[0].message.content
            
            # (API 호출 코드 대신 임시 결과 반환)
            llm_response_text = "강원도 평창군: 끈기 있는 당신의 성실함이 빛을 발할 청정 고원입니다.\n전라남도 담양군: 꼼꼼한 당신의 손길로 대나무처럼 곧고 푸른 결실을 맺어보세요.\n경기도 양평군: 빠른 실행력의 당신에게, 수도권과 가까운 이곳은 최고의 기회가 될 것입니다."

            recommendations = {}
            for line in llm_response_text.strip().split('\n'):
                parts = line.split(':')
                if len(parts) == 2:
                    recommendations[parts[0].strip()] = parts[1].strip()
            return recommendations
        except Exception as e:
            st.error(f"LLM 추천 생성 중 오류: {e}")
            # LLM 실패 시 코사인 유사도 기반 지역의 기존 한줄평을 사용
            return {row['full_region']: row['한줄평'] for _, row in candidate_regions_df.head(3).iterrows()}

    def get_recommendations(self, answers):
        final_type, _ = calculate_archetype(answers)
        user_region_vector, user_care_vector = self._calculate_user_vectors(answers)
        
        top_10_regions = self._recommend_regions_cosine(user_region_vector, top_n=10)
        
        with st.spinner("🤖 AI 컨설턴트가 맞춤형 추천 결과를 생성 중입니다..."):
            llm_recommendations = self._get_llm_recommendations(answers, top_10_regions)
        
        final_regions_df = self.region_df[self.region_df['full_region'].isin(llm_recommendations.keys())]
        
        crop_recommendations = {}
        care_cols = ['CARE_C', 'CARE_A', 'CARE_R', 'CARE_E']
        for _, region in final_regions_df.iterrows():
            region_name = region['full_region']
            self.crop_df['similarity'] = self.crop_df.apply(
                lambda row: self._cosine_similarity(row[care_cols].values.astype(float), user_care_vector), axis=1
            )
            top_crops = self.crop_df.nlargest(2, 'similarity')
            crop_recommendations[region_name] = top_crops.to_dict('records')
            
        return final_type, llm_recommendations, crop_recommendations

def calculate_archetype(answers):
    scores = { type_name: 0 for type_name in TYPE_DESCRIPTIONS.keys() }
    for q_id, score in answers.items():
        for farm_type in SCORING_MATRIX.get(q_id, []):
            scores[farm_type] += score
    return max(scores, key=scores.get), scores

# --- Streamlit UI ---
st.set_page_config(page_title="찾아보농", page_icon="🌾")

if 'page' not in st.session_state:
    st.session_state.page = 'intro'

if region_data is not None and crop_data is not None:
    if st.session_state.page == 'intro':
        st.title("🌾 찾아보농")
        st.header("나는 어떤 농부가 될 수 있을까?", divider='rainbow')
        st.markdown("간단한 테스트를 통해 나에게 꼭 맞는 귀농 지역과 추천 작물을 알아보세요!")
        if st.button("테스트 시작하기", type="primary", use_container_width=True):
            st.session_state.page = 'survey'
            st.session_state.answers = {q_id: 3 for q_id in QUESTIONS}
            st.rerun()

    elif st.session_state.page == 'survey':
        st.header("🔍 나의 귀농 스타일 찾기",  divider='rainbow')
        # ... (설문 페이지 UI는 이전과 동일) ...
        with st.form("survey_form"):
            for q_id, question in QUESTIONS.items():
                st.session_state.answers[q_id] = st.slider(question, 1, 5, st.session_state.answers.get(q_id, 3), key=q_id)
            if st.form_submit_button("결과 보기", type="primary", use_container_width=True):
                st.session_state.page = 'result'
                st.rerun()

    elif st.session_state.page == 'result':
        st.header("💡 '찾아보농' 테스트 결과", divider='rainbow')
        st.balloons()
        
        engine = RecommendationEngine(region_data, crop_data)
        final_type, llm_recommendations, crop_recommendations = engine.get_recommendations(st.session_state.answers)
        
        st.subheader("당신의 귀농 유형은...")
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image(f"images/{final_type}.png", width=200)
        with col2:
            st.title(f"**{final_type}**")
            st.markdown(f"#### {TYPE_DESCRIPTIONS[final_type]}")
        st.markdown("---")

        st.subheader("🌟 AI 컨설턴트의 맞춤 추천 지역 TOP 3")
        for region_name, comment in llm_recommendations.items():
            with st.container(border=True):
                st.markdown(f"#### 📍 {region_name}")
                st.success(f"💡 **{comment}**")
                
                crops = crop_recommendations.get(region_name, [])
                if crops:
                    for crop in crops:
                        feature = crop.get('특징', '추천 작물입니다.')
                        st.info(f"**추천 작물: {crop['작물명']}** - {feature}")

        st.markdown("---")
        if st.button("테스트 다시하기", use_container_width=True):
            st.session_state.page = 'intro'
            if 'answers' in st.session_state:
                del st.session_state.answers
            st.rerun()