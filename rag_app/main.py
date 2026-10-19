# import streamlit as st
# import os
# import base64

# # --- 1. 페이지 기본 설정 ---
# st.set_page_config(
#     page_title="물어보농 - 귀농 길라잡이",
#     page_icon="🌱",
#     layout="wide"
# )

# # --- 2. 세션 상태 초기화 ---
# if 'logged_in' not in st.session_state:
#     st.session_state.logged_in = False
# if 'user_id' not in st.session_state:
#     st.session_state.user_id = None
# if 'email' not in st.session_state:
#     st.session_state.email = None
# # 'page' 세션 상태 변수 초기화
# if 'page' not in st.session_state:
#     st.session_state.page = 'home'

# # URL 쿼리 파라미터를 사용하여 페이지 상태 업데이트
# query_params = st.query_params
# if 'page' in query_params:
#     st.session_state.page = query_params['page']
# else:
#     st.session_state.page = 'home'

# # 로그아웃 쿼리 파라미터 처리
# try:
#     if 'logout' in query_params:
#         st.session_state.logged_in = False
#         st.session_state.user_id = None
#         st.session_state.email = None
#         st.success("로그아웃되었습니다.")
#         st.rerun()
# except Exception:
#     pass


# # 로고 이미지 로딩
# def _load_logo_base64():
#     candidate_paths = [
#         os.path.join(os.path.dirname(__file__), 'assets', 'brand.png'),
#         os.path.join(os.path.dirname(__file__), 'assets', 'logo.png'),
#     ]
#     for p in candidate_paths:
#         try:
#             if os.path.exists(p):
#                 with open(p, 'rb') as f:
#                     return base64.b64encode(f.read()).decode('utf-8')
#         except Exception:
#             continue
#     return None


# _logo_b64 = _load_logo_base64()
# _logo_html = f'<img class="header-icon" src="data:image/png;base64,{_logo_b64}" alt="logo"/> ' if _logo_b64 else '🌱 '

# # --- 3. CSS 스타일링 ---
# st.markdown("""
# <style>
#     /* 전체 페이지 배경색 및 폰트 설정 */
#     @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;600;700&display=swap');

#     .stApp {
#         background-color: #F8F9FA;
#         font-family: 'Noto Sans KR', sans-serif;
#         color: #333333;
#     }

#     /* 전체 컨테이너 패딩 및 너비 조정 */
#     .block-container {
#         padding-top: 2rem;
#         padding-bottom: 2rem;
#         padding-left: 3rem;
#         padding-right: 3rem;
#         max-width: 1400px;
#     }

#     /* 헤더 스타일 */
#     .header-container {
#         background: white;
#         padding: 1.25rem 3rem;
#         border-radius: 15px;
#         box-shadow: 0 4px 20px rgba(0,0,0,0.05);
#         margin-bottom: 2.5rem;
#         position: sticky;
#         top: 1.5rem;
#         z-index: 1000;
#         backdrop-filter: blur(10px);
#         -webkit-backdrop-filter: blur(10px);
#     }

#     .header-logo {
#         font-size: 2.5em;
#         font-weight: 700;
#         color: #1a642e; /* 짙은 녹색 */
#         display: flex;
#         align-items: center;
#         gap: 12px;
#         white-space: nowrap;
#     }
#     .header-icon {
#         width: 48px;
#         height: 48px;
#         border-radius: 8px;
#         object-fit: cover;
#     }

#     /* 상단 네비게이션 바 */
#     .topnav {
#         display: flex;
#         align-items: center;
#         justify-content: space-between;
#         gap: 1.5rem;
#     }
#     .topnav-center {
#         display: flex;
#         gap: 1.5rem;
#         align-items: center;
#         justify-content: center;
#         flex: 1;
#     }
#     .topnav-center a {
#         text-decoration: none;
#         color: #6c757d;
#         font-weight: 500;
#         padding: 0.75rem 1.2rem;
#         border-radius: 999px;
#         transition: all 0.3s ease;
#         white-space: nowrap;
#     }
#     .topnav-center a:hover, .topnav-center a.active {
#         background-color: #eaf3ed;
#         color: #1a642e;
#         transform: translateY(-2px);
#         box-shadow: 0 2px 10px rgba(0,0,0,0.05);
#     }
#     .topnav-right {
#         display: flex;
#         align-items: center;
#         gap: 1rem;
#         white-space: nowrap;
#     }
#     .btn-auth {
#         background-color: #4a905a;
#         color: #fff !important;
#         text-decoration: none;
#         padding: 0.75rem 1.5rem;
#         border-radius: 999px;
#         font-weight: 600;
#         transition: all 0.3s ease;
#         display: inline-flex;
#         align-items: center;
#         justify-content: center;
#     }
#     .btn-auth:hover { background-color: #3b7448; transform: translateY(-2px); }

#     /* 히어로 섹션 스타일 */
#     .hero-section {
#         background: linear-gradient(120deg, #d3e9d8 0%, #a4cfb1 100%);
#         border-radius: 25px;
#         text-align: center;
#         padding: 6rem 4rem;
#         color: #1a642e;
#         position: relative;
#         overflow: hidden;
#         margin-bottom: 3.5rem;
#         box-shadow: 0 8px 30px rgba(0,0,0,0.1);
#     }

#     .hero-title {
#         font-size: 4.5em;
#         font-weight: 700;
#         color: #0f3f1e;
#         margin-bottom: 1.5rem;
#         line-height: 1.2;
#         letter-spacing: -2px;
#     }

#     .hero-subtitle {
#         font-size: 1.5em;
#         color: #1a642e;
#         margin-bottom: 2.5rem;
#         opacity: 0.9;
#         font-weight: 400;
#         line-height: 1.6;
#     }

#     /* 주요 서비스 섹션 스타일 */
#     .services-section {
#         text-align: center;
#         margin-bottom: 3.5rem;
#     }

#     .services-title {
#         font-size: 3em;
#         font-weight: 700;
#         color: #1a642e;
#         margin-bottom: 1rem;
#     }

#     .services-subtitle {
#         font-size: 1.2em;
#         color: #6c757d;
#         margin-bottom: 3rem;
#     }

#     /* 서비스 링크 버튼 스타일링 */
#     .service-link {
#         display: flex;
#         flex-direction: column;
#         align-items: center;
#         justify-content: center;
#         gap: 0.75rem;
#         text-decoration: none;
#         color: inherit;
#         background-color: #ffffff;
#         border: 1px solid #e0e0e0;
#         border-radius: 15px;
#         padding: 2rem 1rem;
#         box-shadow: 0 4px 15px rgba(0,0,0,0.05);
#         transition: all 0.3s ease;
#         height: 100%;
#         cursor: pointer;
#     }

#     .service-link:hover {
#         transform: translateY(-8px);
#         background-color: #f7f9fa;
#         box-shadow: 0 8px 25px rgba(0,0,0,0.1);
#         border-color: #a4cfb1;
#     }

#     .service-link .service-icon-wrapper {
#         font-size: 2.5em;
#         line-height: 1;
#         color: #4a905a;
#         transition: color 0.3s ease;
#     }

#     .service-link:hover .service-icon-wrapper {
#         color: #1a642e;
#     }

#     .service-link .service-label-text {
#         font-weight: 600;
#         color: #333333;
#         font-size: 1.1em;
#         white-space: nowrap;
#         transition: color 0.3s ease;
#     }

#     .service-link:hover .service-label-text {
#         color: #1a642e;
#     }

#     /* 혜택 섹션 */
#     .benefits-section {
#         background: #ffffff;
#         border-radius: 20px;
#         padding: 3rem;
#         margin-bottom: 3.5rem;
#         box-shadow: 0 4px 20px rgba(0,0,0,0.05);
#     }

#     .benefits-title {
#         font-size: 2.5em;
#         font-weight: 700;
#         color: #1a642e;
#         margin-bottom: 2rem;
#         text-align: center;
#     }

#     .benefits-grid {
#         display: grid;
#         grid-template-columns: repeat(3, 1fr);
#         gap: 2rem;
#     }

#     .benefit-card {
#         background: #f7f9fa;
#         padding: 2rem;
#         border-radius: 18px;
#         border-left: 5px solid #a4cfb1;
#         transition: transform 0.3s ease, box-shadow 0.3s ease;
#         box-shadow: 0 2px 10px rgba(0,0,0,0.05);
#     }

#     .benefit-card:hover {
#         transform: translateY(-5px);
#         box-shadow: 0 6px 20px rgba(0,0,0,0.1);
#     }

#     .benefit-location {
#         color: #1a642e;
#         font-weight: 600;
#         font-size: 0.95em;
#         margin-bottom: 0.75rem;
#         letter-spacing: -0.5px;
#     }

#     .benefit-title {
#         font-weight: 700;
#         color: #333333;
#         margin-bottom: 0.5rem;
#         font-size: 1.25em;
#         line-height: 1.4;
#     }

#     .benefit-desc {
#         color: #6c757d;
#         font-size: 0.95em;
#         margin-bottom: 1.5rem;
#         line-height: 1.6;
#     }

#     .benefit-link {
#         color: #4a905a;
#         text-decoration: none;
#         font-weight: 600;
#         font-size: 1em;
#         transition: color 0.3s ease;
#     }
#     .benefit-link:hover {
#         color: #3b7448;
#     }

#     /* 뉴스 섹션 */
#     .news-section {
#         background: #ffffff;
#         border-radius: 20px;
#         padding: 3rem;
#         margin-bottom: 3.5rem;
#         box-shadow: 0 4px 20px rgba(0,0,0,0.05);
#     }

#     .news-title {
#         font-size: 2.5em;
#         font-weight: 700;
#         color: #1a642e;
#         margin-bottom: 2rem;
#         text-align: center;
#     }

#     .news-grid {
#         display: grid;
#         grid-template-columns: repeat(3, 1fr);
#         gap: 2rem;
#     }

#     .news-card {
#         background: #f7f9fa;
#         border-radius: 18px;
#         overflow: hidden;
#         transition: all 0.3s ease;
#         box-shadow: 0 2px 10px rgba(0,0,0,0.05);
#     }

#     .news-card:hover {
#         transform: translateY(-5px);
#         box-shadow: 0 6px 20px rgba(0,0,0,0.1);
#     }

#     .news-image {
#         width: 100%;
#         height: 180px;
#         background: linear-gradient(45deg, #eaf3ed, #d3e9d8);
#         display: flex;
#         align-items: center;
#         justify-content: center;
#         font-size: 3em;
#         color: #1a642e;
#     }

#     .news-content {
#         padding: 1.5rem;
#     }

#     .news-text {
#         color: #333333;
#         font-weight: 500;
#         line-height: 1.5;
#         font-size: 1.1em;
#     }

#     /* 하단 카드들 */
#     .bottom-cards {
#         display: grid;
#         grid-template-columns: repeat(2, 1fr);
#         gap: 2.5rem;
#         margin-bottom: 4rem;
#     }

#     .bottom-card {
#         background: white;
#         border-radius: 25px;
#         padding: 2.5rem;
#         box-shadow: 0 8px 25px rgba(0,0,0,0.05);
#         display: flex;
#         align-items: center;
#         gap: 2.5rem;
#         transition: transform 0.3s ease, box-shadow 0.3s ease;
#     }

#     .bottom-card:hover {
#         transform: translateY(-8px);
#         box-shadow: 0 12px 35px rgba(0,0,0,0.1);
#     }

#     .bottom-card.green {
#         background: linear-gradient(135deg, #eaf3ed 0%, #c8e6c9 100%);
#     }

#     .bottom-card.blue {
#         background: linear-gradient(135deg, #e3f2fd 0%, #bbdeff 100%);
#     }

#     .bottom-card-content {
#         flex: 1;
#     }

#     .bottom-card-title {
#         font-size: 1.75em;
#         font-weight: 700;
#         color: #1a642e;
#         margin-bottom: 1rem;
#     }

#     .bottom-card-link {
#         color: #4a905a;
#         text-decoration: none;
#         font-weight: 600;
#         font-size: 1.2em;
#         transition: all 0.3s ease;
#     }
#     .bottom-card-link:hover {
#         color: #3b7448;
#         letter-spacing: 0.5px;
#     }

#     .bottom-card-icon {
#         font-size: 5em;
#         color: #1a642e;
#         transition: transform 0.3s ease;
#     }
#     .bottom-card:hover .bottom-card-icon {
#         transform: rotate(5deg) scale(1.1);
#     }

#     /* 푸터 */
#     .footer {
#         text-align: center;
#         padding: 2.5rem;
#         color: #95a5a6;
#         border-top: 1px solid #e0e0e0;
#         margin-top: 4rem;
#         font-size: 0.9em;
#     }

#     /* 반응형 디자인 */
#     @media (max-width: 1200px) {
#         .benefits-grid, .news-grid {
#             grid-template-columns: repeat(2, 1fr);
#         }
#         .bottom-cards {
#             grid-template-columns: 1fr;
#         }
#     }

#     @media (max-width: 768px) {
#         .block-container {
#             padding-left: 1rem;
#             padding-right: 1rem;
#         }
#         .header-container {
#             padding: 1rem;
#         }
#         .topnav-center {
#             display: none;
#         }
#         .topnav-right {
#             flex: 1;
#             justify-content: flex-end;
#         }
#         .hero-section {
#             padding: 4rem 2rem;
#         }
#         .hero-title {
#             font-size: 3em;
#         }
#         .hero-subtitle {
#             font-size: 1.1em;
#         }
#         .service-grid, .benefits-grid, .news-grid {
#             grid-template-columns: 1fr;
#         }
#     }
# </style>
# """, unsafe_allow_html=True)

# # --- 4. 헤더 구현 (상단 고정형 내비게이션 바) ---
# st.markdown(
#     f"""
# <div class="header-container topnav">
#   <div class="header-logo">{'<a href="/?page=home" target="_self" style="text-decoration:none; color:inherit;">' if st.session_state.logged_in else ''}{_logo_html}물어보농{'</a>' if st.session_state.logged_in else ''}</div>
#   <nav class="topnav-center">
#     <a href="/?page=home" target="_self" class="{'active' if st.session_state.page == 'home' else ''}">홈</a>
#     <a href="/?page=region" target="_self" class="{'active' if st.session_state.page == 'region' else ''}">지역 추천 받기</a>
#     <a href="/?page=calculator" target="_self" class="{'active' if st.session_state.page == 'calculator' else ''}">작물 수익 계산기</a>
#     <a href="/?page=mentor" target="_self" class="{'active' if st.session_state.page == 'mentor' else ''}">귀농 멘토 찾기</a>
#     <a href="/?page=benefit" target="_self" class="{'active' if st.session_state.page == 'benefit' else ''}">혜택</a>
#   </nav>
#   <div class="topnav-right">
#     {('<span style="color:#2E7D32;font-weight:600;">안녕하세요, ' + (st.session_state.email or '') + '님!</span> <a class="btn-auth" href="?logout=1" target="_self">로그아웃</a>') if st.session_state.logged_in else ('<a class="btn-auth" href="/?page=login" target="_self">로그인</a>')}
#   </div>
# </div>
# """,
#     unsafe_allow_html=True,
# )

# # --- 5. 히어로 섹션 ---
# st.markdown("""
# <div class="hero-section">
#     <h1 class="hero-title">나에게 물어보농!</h1>
#     <h1 class="hero-title">나에게 딱 맞는 귀농 길라잡이</h1>
#     <p class="hero-subtitle">
#         어디서 무엇을 시작해야 할지 막막하신가요?<br>
#         물어보농이 복잡한 귀농 정보를 쉽고 친절하게 알려드려요.
#     </p>
# </div>
# """, unsafe_allow_html=True)

# # --- 6. 주요 서비스 섹션 ---
# st.markdown("""
# <div class="services-section">
#     <h2 class="services-title">주요 서비스</h2>
#     <p class="services-subtitle">
#         귀농인의 삶을 시작하기 위한 첫 걸음,<br>
#         물어보농과 함께라면 더 이상 막막하지 않아요.
#     </p>
# </div>
# """, unsafe_allow_html=True)

# # 서비스 아이템들을 클릭 가능한 버튼으로 구현
# service_cols = st.columns(6)
# for i, service in enumerate([
#     {"icon": "📚", "label": "가이드북", "page": "guide"},
#     {"icon": "📍", "label": "지역 추천", "page": "region"},
#     {"icon": "💬", "label": "물어보농", "page": "app"},
#     {"icon": "🧮", "label": "작물 계산기", "page": "calculator"},
#     {"icon": "👨‍🌾", "label": "멘토 찾기", "page": "mentor"},
#     {"icon": "🎁", "label": "혜택", "page": "benefit"}
# ]):
#     with service_cols[i]:
#         st.markdown(
#             f"""
#             <a href="/?page={service['page']}" class="service-link">
#                 <span class="service-icon-wrapper">{service["icon"]}</span>
#                 <span class="service-label-text">{service["label"]}</span>
#             </a>
#             """,
#             unsafe_allow_html=True
#         )

# # --- 7. 혜택 섹션 ---
# st.markdown("""
# <div class="benefits-section">
#     <h2 class="benefits-title">귀농 정착을 돕는<br>다양한 혜택을 찾아보세요</h2>
#     <div class="benefits-grid">
# """, unsafe_allow_html=True)

# benefits = [
#     {"location": "충청남도 청양군", "title": "검정고시 합격 장학금", "description": "귀농인의 교육 기회를 확대하고 안정적인 정착을 지원하기 위한 장학금 지원 사업입니다."},
#     {"location": "경상북도 문경시", "title": "귀농인 농어촌 진흥기금", "description": "영농 시설 구축, 대형 농기계 구입 등 초기 정착에 필요한 자금을 지원해 드립니다."},
#     {"location": "충청남도 공주시", "title": "오이 연작장해방지 및 생육증진",
#      "description": "오이 재배 농가의 안정적인 생산을 위해 토양개량용 및 작물생육용 자재를 지원합니다."}
# ]

# benefit_cols = st.columns(3)
# for i, benefit in enumerate(benefits):
#     with benefit_cols[i]:
#         st.markdown(f"""
#         <div class="benefit-card">
#             <div class="benefit-location">📍 {benefit['location']}</div>
#             <div class="benefit-title">{benefit['title']}</div>
#             <div class="benefit-desc">{benefit['description']}</div>
#             <a href="#" class="benefit-link">자세히 보기 →</a>
#         </div>
#         """, unsafe_allow_html=True)
# st.markdown("</div></div>", unsafe_allow_html=True)

# # --- 8. 뉴스 섹션 ---
# st.markdown("""
# <div class="news-section">
#     <h2 class="news-title">귀농·귀촌, 새로운 삶의<br>다양한 소식을 접해보세요</h2>
#     <div class="news-grid">
# """, unsafe_allow_html=True)

# news_items = [
#     {"icon": "🌾", "title": "진도군, '진도에서 살아보기' 프로그램 인기 만점"},
#     {"icon": "🚜", "title": "음성군, 귀농·귀촌 희망 도시민 '상상대로 음성에서 살아보기' 진행"},
#     {"icon": "👥", "title": "완주군, 귀농귀촌 1번지 위상 확립 위해 농식품부 현장간담회 개최"}
# ]

# news_cols = st.columns(3)
# for i, news in enumerate(news_items):
#     with news_cols[i]:
#         st.markdown(f"""
#         <a href="#" class="news-card" style="text-decoration:none; color:inherit;">
#             <div class="news-image">{news['icon']}</div>
#             <div class="news-content">
#                 <div class="news-text">{news['title']}</div>
#             </div>
#         </a>
#         """, unsafe_allow_html=True)
# st.markdown("</div></div>", unsafe_allow_html=True)

# # --- 9. 하단 카드들 ---
# st.markdown("""
# <div class="bottom-cards">
# """, unsafe_allow_html=True)

# st.markdown("""
# <a href="/?page=mentor" target="_self" class="bottom-card green" style="text-decoration:none; color:inherit;">
#     <div class="bottom-card-content">
#         <div class="bottom-card-title">귀농 선배들의 삶이 궁금하다면?</div>
#         <div class="bottom-card-link">멘토 찾기로 바로가기 →</div>
#     </div>
#     <div class="bottom-card-icon">👨‍🌾</div>
# </a>
# """, unsafe_allow_html=True)

# st.markdown("""
# <a href="/?page=calculator" target="_self" class="bottom-card blue" style="text-decoration:none; color:inherit;">
#     <div class="bottom-card-content">
#         <div class="bottom-card-title">내 작물로 얻는 수익은 얼마일까?</div>
#         <div class="bottom-card-link">작물 계산기로 바로가기 →</div>
#     </div>
#     <div class="bottom-card-icon">🧮</div>
# </a>
# """, unsafe_allow_html=True)
# st.markdown("</div>", unsafe_allow_html=True)

# # --- 10. 푸터 ---
# st.markdown("""
# <div class="footer">
#     <p>© 2025 물어보농 | All Rights Reserved.</p>
#     <p>데이터 출처: 농림축산식품부, 통계청, 농식품빅데이터 거래소 등</p>
# </div>
# """, unsafe_allow_html=True)



import streamlit as st
import os
import base64

# --- 1. 페이지 기본 설정 ---
st.set_page_config(
    page_title="물어보농 - 귀농 길라잡이",
    page_icon="🌱",
    layout="wide"
)

# --- 2. 세션 상태 초기화 ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'email' not in st.session_state:
    st.session_state.email = None

# 로그아웃 쿼리 파라미터 처리 (상단바에서 로그아웃 링크 클릭 시)
try:
    query_params = st.query_params
    if 'logout' in query_params:
        # 모든 관련 세션 상태 초기화
        for key in ['logged_in', 'user_id', 'email', 'messages', 'chat_created_at', 'current_user_id']:
            if key in st.session_state:
                del st.session_state[key]

        st.success("로그아웃되었습니다.")
        # 파라미터 제거 후 새로고침
        try:
            del st.query_params['logout']
        except Exception:
            pass
        st.rerun()
except Exception:
    pass


# --- 3. CSS 스타일링 ---
st.markdown("""
<style>
    /* 전체 페이지 배경색 */
    .stApp {
        background-color: #F7F9FC;
    }

    .block-container {
        padding-top: 3rem;
        padding-bottom: 3rem;
        padding-left: 3rem;
        padding-right: 3rem;
        max-width: 1200px;
        margin: 0 auto;
    }

    /* 간단한 헤더 스타일 */
    .simple-header {
        background: white;
        padding: 2rem 3rem;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.06);
        margin-bottom: 3rem;
        text-align: center;
    }

    /* 로고 영역 */
    .header-logo-simple {
        font-size: 2.5em;
        font-weight: bold;
        color: #2E7D32;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 15px;
        white-space: nowrap;
        margin-bottom: 1rem;
    }
    .header-icon {
        width: 56px;
        height: 56px;
        border-radius: 12px;
        object-fit: cover;
        box-shadow: 0 2px 8px rgba(0,0,0,0.15);
        transition: transform 0.3s ease;
    }

    .header-icon:hover {
        transform: scale(1.05);
    }



    .header-icon-emoji:hover {
        transform: scale(1.05);
    }

    /* 사용자 정보 간단 스타일 */
    .user-info-simple {
        color: #2E7D32;
        font-weight: 600;
        font-size: 0.9em;
        padding: 0.5rem 1rem;
        background: #F1F8E9;
        border-radius: 15px;
        border: 1px solid #C8E6C9;
        white-space: nowrap;
        text-align: center;
    }
    /* 버튼 스타일 */
    .btn-auth, .btn-logout, .login-btn {
        background: linear-gradient(135deg, #2E7D32 0%, #388E3C 100%);
        color: #fff !important;
        text-decoration: none;
        padding: 0.75rem 1.5rem;
        border-radius: 25px;
        font-weight: 600;
        transition: all 0.3s ease;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        border: none;
        cursor: pointer;
        box-shadow: 0 2px 10px rgba(46, 125, 50, 0.3);
        font-size: 0.9em;
    }

    .btn-auth:hover, .login-btn:hover {
        background: linear-gradient(135deg, #1B5E20 0%, #2E7D32 100%);
        transform: translateY(-2px);
        box-shadow: 0 4px 20px rgba(46, 125, 50, 0.4);
    }

    .btn-logout {
        background: linear-gradient(135deg, #F44336 0%, #D32F2F 100%);
        box-shadow: 0 2px 10px rgba(244, 67, 54, 0.3);
    }

    .btn-logout:hover {
        background: linear-gradient(135deg, #D32F2F 0%, #B71C1C 100%);
        transform: translateY(-2px);
        box-shadow: 0 4px 20px rgba(244, 67, 54, 0.4);
    }

    /* 히어로 섹션 스타일 */
    .hero-section {
        background: linear-gradient(135deg, #E8F5E8 0%, #C8E6C9 100%);
        border-radius: 25px;
        text-align: center;
        padding: 5rem 4rem;
        color: #333;
        position: relative;
        overflow: hidden;
        margin-bottom: 4rem;
        box-shadow: 0 12px 40px rgba(0,0,0,0.08);
    }

    .hero-title {
        font-size: 3.5em;
        font-weight: bold;
        color: #1B5E20;
        margin-bottom: 1rem;
        line-height: 1.2;
    }

    .hero-subtitle {
        font-size: 1.3em;
        color: #2E7D32;
        margin-bottom: 2rem;
        opacity: 0.9;
    }

    /* 주요 서비스 섹션 스타일 */
    .services-section {
        text-align: center;
        margin-bottom: 4rem;
        padding: 2rem 0;
    }

    .services-title {
        font-size: 2.8em;
        font-weight: bold;
        color: #333;
        margin-bottom: 1.5rem;
    }

    .services-subtitle {
        font-size: 1.2em;
        color: #666;
        margin-bottom: 4rem;
        line-height: 1.6;
    }

    /* 서비스 버튼 컨테이너 */
    .service-buttons-container {
        margin: 2rem 0 4rem 0;
        padding: 2rem;
        background: white;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.06);
    }

    .service-grid {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 1.5rem;
        margin-bottom: 3rem;
    }

    .service-item {
        background: white;
        padding: 2rem 1rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        cursor: pointer;
    }

    .service-item:hover {
        transform: translateY(-8px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }

    .service-icon {
        font-size: 3em;
        margin-bottom: 1rem;
        color: #2E7D32;
    }

    .service-label {
        font-weight: 600;
        color: #333;
        font-size: 1.1em;
    }

    /* 혜택 섹션 */
    .benefits-section {
        background: white;
        border-radius: 25px;
        padding: 3rem;
        margin-bottom: 4rem;
        box-shadow: 0 12px 40px rgba(0,0,0,0.08);
    }

    .benefits-title {
        font-size: 2em;
        font-weight: bold;
        color: #333;
        margin-bottom: 1.5rem;
        text-align: center;
    }

    .benefits-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1.5rem;
    }

    .benefit-card {
        background: #F8F9FA;
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 4px solid #2E7D32;
    }

    .benefit-location {
        color: #2E7D32;
        font-weight: 600;
        font-size: 0.9em;
        margin-bottom: 0.5rem;
    }

    .benefit-title {
        font-weight: bold;
        color: #333;
        margin-bottom: 0.5rem;
        font-size: 1.1em;
    }

    .benefit-desc {
        color: #666;
        font-size: 0.9em;
        margin-bottom: 1rem;
        line-height: 1.4;
    }

    .benefit-link {
        color: #2E7D32;
        text-decoration: none;
        font-weight: 500;
        font-size: 0.9em;
    }

    /* 뉴스 섹션 */
    .news-section {
        background: white;
        border-radius: 25px;
        padding: 3rem;
        margin-bottom: 4rem;
        box-shadow: 0 12px 40px rgba(0,0,0,0.08);
    }

    .news-title {
        font-size: 2em;
        font-weight: bold;
        color: #333;
        margin-bottom: 1.5rem;
        text-align: center;
    }

    .news-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1.5rem;
    }

    .news-card {
        background: #F8F9FA;
        border-radius: 15px;
        overflow: hidden;
        transition: all 0.3s ease;
    }

    .news-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }

    .news-image {
        width: 100%;
        height: 150px;
        background: linear-gradient(45deg, #E8F5E8, #C8E6C9);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2em;
        color: #2E7D32;
    }

    .news-content {
        padding: 1.5rem;
    }

    .news-text {
        color: #333;
        font-weight: 500;
        line-height: 1.4;
    }

    /* 하단 카드들 */
    .bottom-cards {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 3rem;
        margin-bottom: 4rem;
    }

    .bottom-card {
        background: white;
        border-radius: 25px;
        padding: 3rem;
        box-shadow: 0 12px 40px rgba(0,0,0,0.08);
        display: flex;
        align-items: center;
        gap: 2.5rem;
    }

    .bottom-card.green {
        background: linear-gradient(135deg, #E8F5E8 0%, #C8E6C9 100%);
    }

    .bottom-card.blue {
        background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%);
    }

    .bottom-card-content {
        flex: 1;
    }

    .bottom-card-title {
        font-size: 1.5em;
        font-weight: bold;
        color: #333;
        margin-bottom: 1rem;
    }

    .bottom-card-link {
        color: #2E7D32;
        text-decoration: none;
        font-weight: 500;
        font-size: 1.1em;
    }

    .bottom-card-icon {
        font-size: 4em;
        color: #2E7D32;
    }

    /* 푸터 */
    .footer {
        text-align: center;
        padding: 3rem;
        color: #666;
        border-top: 1px solid #E0E0E0;
        margin-top: 4rem;
        background: white;
        border-radius: 25px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.06);
    }

    /* 반응형 디자인 */
    @media (max-width: 1200px) {
        .header-content {
            gap: 1.5rem;
        }

        .nav-menu {
            gap: 0.3rem;
        }

        .nav-menu button {
            padding: 0.6rem 1rem;
            font-size: 0.9em;
        }
    }

    @media (max-width: 992px) {
        .header-content {
            flex-direction: column;
            gap: 1rem;
            text-align: center;
            min-height: auto;
        }

        .header-content::before {
            display: none; /* 세로 배치에서는 가로선 숨김 */
        }

        .nav-menu {
            justify-content: center;
            gap: 0.5rem;
        }

        .auth-section {
            justify-content: center;
        }
    }

    @media (max-width: 768px) {
        .header-container {
            padding: 1rem;
        }

        .header-logo {
            font-size: 1.8em;
        }

        .header-icon {
            width: 48px;
            height: 48px;
        }

        .nav-menu {
            gap: 0.2rem;
        }

        .nav-menu button {
            padding: 0.5rem 0.8rem;
            font-size: 0.85em;
        }

        .btn-auth, .btn-logout, .login-btn {
            padding: 0.6rem 1.2rem;
            font-size: 0.9em;
        }

        .service-grid {
            grid-template-columns: repeat(2, 1fr);
        }

        .benefits-grid, .news-grid {
            grid-template-columns: 1fr;
        }

        .bottom-cards {
            grid-template-columns: 1fr;
        }
    }

    @media (max-width: 576px) {
        .nav-menu {
            flex-direction: column;
            gap: 0.5rem;
        }

        .nav-menu button {
            width: 100%;
            text-align: center;
        }

        .auth-section {
            flex-direction: column;
            gap: 0.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)



# 우측 상단에 로그인/로그아웃 버튼
col_logo, col_auth = st.columns([4, 1])
with col_logo:
    st.markdown(f'''
    <div class="header-logo-simple">
        🌱 물어보농
    </div>
    ''', unsafe_allow_html=True)

with col_auth:
    if st.session_state.logged_in:
        st.markdown(f'<div class="user-info-simple">안녕하세요, {st.session_state.email or ""}님!</div>', unsafe_allow_html=True)
        if st.button("로그아웃", key="logout_btn"):
            # 세션 상태 초기화
            for k in ["logged_in", "user_id", "email"]:
                if k in st.session_state:
                    del st.session_state[k]
            st.success("로그아웃 되었습니다.")
            st.switch_page("pages/login.py")
    else:
        if st.button("로그인", key="login_btn"):
            st.switch_page("pages/login.py")

st.markdown('</div>', unsafe_allow_html=True)

service_cols = st.columns(7)
for i, service in enumerate([
    {"icon": "📚", "label": "읽어보농", "page": "pages/guide.py"},
    {"icon": "📍", "label": "찾아보농", "page": "pages/test.py"},
    {"icon": "💬", "label": "물어보농", "page": "pages/app.py"},
    {"icon": "🧮", "label": "계산보농", "page": "pages/calculator.py"},
    {"icon": "👨‍🌾", "label": "만나보농", "page": "pages/mentor.py"},
    {"icon": "📃", "label": "둘러보농", "page": "pages/news.py"},
    {"icon": "🎁", "label": "알아보농", "page": "pages/benefit.py"}
]):
    with service_cols[i]:
        if st.button(f"{service['icon']}\n{service['label']}", key=f"service_{i}"):
            st.switch_page(service['page'])
st.markdown('</div>', unsafe_allow_html=True)

# --- 5. 히어로 섹션 ---
st.markdown("""
<div class="hero-section">
    <h1 class="hero-title">나에게 물어보농</h1>
    <p class="hero-subtitle">
        어디서 무엇을 시작해야 할지 막막하신가요?<br>
        물어보농이 나에게 딱 맞는 귀농 정보를 알려드려요.
    </p>
</div>
""", unsafe_allow_html=True)

# 히어로 섹션 아래에 Streamlit 버튼 배치
col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    st.markdown("""
    <div class="huge-hero-btn">
    """, unsafe_allow_html=True)
    if st.button("🌱 물어보농 시작하기", key="hero_app_button", help="물어보농 챗봇으로 이동", use_container_width=True):
        st.switch_page("pages/app.py")
    st.markdown("</div>", unsafe_allow_html=True)


# 서비스 아이템들을 클릭 가능한 버튼으로 구현
service_cols = st.columns(6)
for i, service in enumerate([
    {"icon": "📚", "label": "가이드북", "page": "guide"},
    {"icon": "📍", "label": "찾아보농", "page": "region"},
    {"icon": "💬", "label": "물어보농", "page": "app"},
    {"icon": "🧮", "label": "작물 계산기", "page": "calculator"},
    {"icon": "👨‍🌾", "label": "멘토 찾기", "page": "mentor"},
    {"icon": "🎁", "label": "혜택", "page": "benefit"}
]):
    with service_cols[i]:
        st.markdown(
            f"""
            <a href="/?page={service['page']}" class="service-link">
                <span class="service-icon-wrapper">{service["icon"]}</span>
                <span class="service-label-text">{service["label"]}</span>
            </a>
            """,
            unsafe_allow_html=True
        )

# --- 7. 혜택 섹션 ---
st.markdown("""
<div class="benefits-section">
    <h2 class="benefits-title">관심있는 지원정책을 찾아보세요</h2>
    <div class="benefits-grid">
""", unsafe_allow_html=True)

benefits = [
    {"location": "충청남도 청양군", "title": "검정고시 합격장학금", "description": "검정고시 합격장학금 지원으로 귀농인의 교육 기회를 확대합니다."},
    {"location": "경상북도 문경시", "title": "귀농인 농어촌 진흥기금 지원사업", "description": "시설자금: 건축물, 대형 농기계 구입 등, 운영자금: 소모성농자재, 소형 농기계 지원"},
    {"location": "충청남도 공주시", "title": "2025년 오이 연작장해방지 및 생육증진", "description": "토양개량용 및 작물생육용자재, 영농자재 지원"}
]

benefit_cols = st.columns(3)
for i, benefit in enumerate(benefits):
    with benefit_cols[i]:
        st.markdown(f"""
        <div class="benefit-card">
            <div class="benefit-location">{benefit['location']}</div>
            <div class="benefit-title">{benefit['title']}</div>
            <div class="benefit-desc">{benefit['description']}</div>
            <a href="#" class="benefit-link">다른 혜택도 보기 ></a>
        </div>
        """, unsafe_allow_html=True)
st.markdown("</div></div>", unsafe_allow_html=True)

# --- 8. 뉴스 섹션 ---
st.markdown("""
<div class="news-section">
    <h2 class="news-title">더 많은 귀농 소식이 있어요</h2>
    <div class="news-grid">
""", unsafe_allow_html=True)

news_items = [
    {"icon": "🌾", "title": "진도군, '진도에서 살아보기' 인기 만점"},
    {"icon": "🚜", "title": "음성군, 귀농·귀촌 희망 도시민 '상상대로 음성에서 살아보기' 진행"},
    {"icon": "👥", "title": "귀농귀촌 1번지 완주군서 농식품부 현장간담회"}
]

news_cols = st.columns(3)
for i, news in enumerate(news_items):
    with news_cols[i]:
        st.markdown(f"""
        <div class="news-card">
            <div class="news-image">{news['icon']}</div>
            <div class="news-content">
                <div class="news-text">{news['title']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
st.markdown("</div></div>", unsafe_allow_html=True)

# --- 9. 하단 카드들 ---
st.markdown("""
<div class="bottom-cards">
""", unsafe_allow_html=True)

st.markdown("""
<div class="bottom-card green">
    <div class="bottom-card-content">
        <div class="bottom-card-title">귀농인의 삶이 궁금하다면?</div>
        <a href="/mentor" class="bottom-card-link" target="_self">'멘토 찾기'로 바로가기 →</a>
    </div>
    <div class="bottom-card-icon">👨‍🌾</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="bottom-card blue">
    <div class="bottom-card-content">
        <div class="bottom-card-title">내 작물로 얻는 수익은 얼마일까?</div>
        <a href="/calculator" class="bottom-card-link" target="_self">'작물 계산기'로 바로가기 →</a>
    </div>
    <div class="bottom-card-icon">🧮</div>
</div>
""", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# --- 10. 푸터 ---
st.markdown("""
<div class="footer">
    <p>© 2025 물어보농 | 모든 권리 보유</p>
    <p>데이터 출처: 농림축산식품부, 통계청, 농식품빅데이터 거래소 등 정부 및 지자체 공공데이터</p>
</div>
""", unsafe_allow_html=True)


