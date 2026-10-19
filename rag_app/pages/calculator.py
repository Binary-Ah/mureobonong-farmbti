import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import requests
from datetime import datetime, timedelta
import json

# --- 1. 페이지 설정 ---
st.set_page_config(
    page_title="작물 수익 계산기 - 어디가농",
    page_icon="🧮",
    layout="wide"
)

# --- 2. 로그인 확인 ---
if not st.session_state.get('logged_in', False):
    st.warning("로그인이 필요합니다. 먼저 로그인해주세요.")
    if st.button("로그인 페이지로 이동"):
        st.switch_page("pages/login.py")
    st.stop()

# --- 3. CSS 스타일링 ---
st.markdown("""
<style>
    .calculator-container { max-width: 1200px; margin: auto; padding: 2rem; }
    .calculator-header { text-align: center; margin-bottom: 3rem; padding: 2rem; background: linear-gradient(135deg, #E8F5E8 0%, #C8E6C9 100%); border-radius: 20px; }
    .calculator-title { font-size: 3em; font-weight: bold; color: #1B5E20; margin-bottom: 1rem; }
    .calculator-subtitle { font-size: 1.3em; color: #2E7D32; }
    .input-section { background: white; padding: 2rem; border-radius: 15px; margin-bottom: 2rem; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
    .section-title { color: #2E7D32; border-bottom: 3px solid #E8F5E8; padding-bottom: 0.5rem; margin-bottom: 1.5rem; font-size: 1.5em; }
    .result-section { background: white; padding: 2rem; border-radius: 15px; margin-bottom: 2rem; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
    .result-card { background: #F8F9FA; padding: 1.5rem; border-radius: 15px; margin-bottom: 1rem; border-left: 4px solid #2E7D32; text-align: center; }
    .result-value { font-size: 2em; font-weight: bold; color: #2E7D32; margin-bottom: 0.5rem; }
    .result-label { color: #666; font-size: 1.1em; }
    .back-button { background: #2E7D32; color: white; padding: 0.5rem 1rem; border-radius: 20px; text-decoration: none; border: none; cursor: pointer; margin-bottom: 2rem; }
</style>
""", unsafe_allow_html=True)

# --- 4. 작물 데이터 (수정된 구조) ---
crops_data = {
    "쌀": {
        "yield_per_1000m2": 500,      # kg/1000m2
        "price_per_kg": 2000,          # 원/kg (기본 가격)
        "cost_per_1000m2": 800000,    # 원/1000m2
        "season": "여름",
        "growth_period": 120           # 일
    },
    "감자": {
        "yield_per_1000m2": 3000,
        "price_per_kg": 1500,
        "cost_per_1000m2": 1200000,
        "season": "봄/가을",
        "growth_period": 90
    },
    "양파": {
        "yield_per_1000m2": 4000,
        "price_per_kg": 1200,
        "cost_per_1000m2": 1500000,
        "season": "봄",
        "growth_period": 150
    },
    "고구마": {
        "yield_per_1000m2": 2500,
        "price_per_kg": 1800,
        "cost_per_1000m2": 1000000,
        "season": "봄",
        "growth_period": 120
    },
    "배추": {
        "yield_per_1000m2": 5000,
        "price_per_kg": 800,
        "cost_per_1000m2": 800000,
        "season": "가을",
        "growth_period": 60
    },
    "사과": {
        "yield_per_1000m2": 2000,
        "price_per_kg": 3000,
        "cost_per_1000m2": 2000000,
        "season": "가을",
        "growth_period": 180
    },
    "포도": {
        "yield_per_1000m2": 1500,
        "price_per_kg": 4000,
        "cost_per_1000m2": 2500000,
        "season": "가을",
        "growth_period": 150
    }
}

# --- API 설정 ---
API_KEY = os.environ.get("KAMIS_API_KEY", "")  # set via environment variable
API_ID = "user"
API_URL = "http://www.kamis.or.kr/service/price/xml.do"

# 작물별 API 품목명 매핑
crop_api_mapping = {
    "쌀": {"itemcode": "111", "kindcode": "01", "unit": "20kg"},
    "감자": {"itemcode": "151", "kindcode": "01", "unit": "20kg"},
    "양파": {"itemcode": "245", "kindcode": "00", "unit": "1kg"},
    "고구마": {"itemcode": "152", "kindcode": "01", "unit": "10kg"},
    "배추": {"itemcode": "211", "kindcode": "01", "unit": "10kg"},
    "사과": {"itemcode": "411", "kindcode": "05", "unit": "10kg"},
    "포도": {"itemcode": "422", "kindcode": "01", "unit": "2kg"}
}

def get_api_price(selected_crop):
    """KAMIS API를 통해 실시간 가격 정보 조회"""
    try:
        # 오늘 날짜
        today = datetime.now().strftime("%Y-%m-%d")
        
        # 작물별 API 매핑 정보 가져오기
        crop_info = crop_api_mapping.get(selected_crop)
        if not crop_info:
            return None
        
        # API 파라미터 설정
        params = {
            "p_cert_key": API_KEY,
            "p_cert_id": API_ID,
            "p_returntype": "json",
            "p_itemcode": crop_info["itemcode"],
            "p_kindcode": crop_info["kindcode"],
            "p_convert_kg_yn": "Y",
            "p_regday": today,
            "p_itemcategorycode": "",
            "p_productclscode": "01",
            "p_countrycode": "1101"  # 서울
        }
        
        # API 호출
        response = requests.get(API_URL, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            # 가격 데이터 추출
            if "data" in data and "item" in data["data"]:
                items = data["data"]["item"]
                if isinstance(items, list) and len(items) > 0:
                    item = items[0]
                elif isinstance(items, dict):
                    item = items
                else:
                    return None
                
                # 가격 정보 추출 (dpr1: 당일 가격)
                if "dpr1" in item:
                    price_str = str(item["dpr1"]).replace(",", "")
                    if price_str and price_str != "-" and price_str.isdigit():
                        price = float(price_str)
                        
                        # 단위 변환 (kg당 가격으로 통일)
                        unit = crop_info["unit"]
                        if "20kg" in unit:
                            price = price / 20
                        elif "10kg" in unit:
                            price = price / 10
                        elif "2kg" in unit:
                            price = price / 2
                        
                        return price
        
        return None
        
    except Exception as e:
        st.warning(f"API 가격 조회 실패: {str(e)}")
        return None

# --- 5. 작물 계산기 ---
st.markdown('<div class="calculator-container">', unsafe_allow_html=True)

if st.button("← 메인 페이지로 돌아가기", key="back_btn"):
    st.switch_page("main.py")

st.markdown("""
<div class="calculator-header">
    <h1 class="calculator-title">🧮 작물 수익 계산기</h1>
    <p class="calculator-subtitle">내 작물로 얻는 수익을 계산해보세요</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="input-section">
    <h2 class="section-title">📊 작물 정보 입력</h2>
</div>
""", unsafe_allow_html=True)

with st.form("crop_calculator"):
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("1. 기본 정보")
        land_area = st.number_input(
            "경지 면적 (1000m² 단위)",
            min_value=0.1,
            max_value=100.0,
            value=1.0,
            step=0.1,
            help="1 = 1000m² (약 300평)"
        )
        
        selected_crop = st.selectbox(
            "재배 작물 선택",
            list(crops_data.keys()),
            help="재배하고자 하는 작물을 선택하세요"
        )
        
        farming_experience = st.selectbox(
            "농업 경험",
            ["초보자", "경험자", "전문가"],
            help="농업 경험 수준을 선택하세요"
        )
    
    with col2:
        st.subheader("2. 추가 옵션")
        quality_grade = st.selectbox(
            "품질 등급",
            ["일반", "고급", "프리미엄"],
            help="생산하고자 하는 품질 등급을 선택하세요"
        )
        
        market_type = st.selectbox(
            "판매 방식",
            ["직판", "도매", "온라인", "가공"],
            help="주요 판매 방식을 선택하세요"
        )
        
        organic_farming = st.checkbox(
            "유기농 재배",
            help="유기농 재배 여부를 선택하세요"
        )
    
    submit_button = st.form_submit_button("수익 계산하기", use_container_width=True)

if submit_button:
    st.markdown("""
    <div class="result-section">
        <h2 class="section-title">📈 수익 분석 결과</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # API를 통한 실시간 가격 조회
    with st.spinner("실시간 가격 정보를 조회하고 있습니다..."):
        api_price = get_api_price(selected_crop)
    
    # 작물 정보 가져오기
    crop_info = crops_data[selected_crop].copy()
    
    # API 가격이 있으면 사용, 없으면 기본 가격 사용
    if api_price:
        current_price = api_price
        st.success(f"✅ 실시간 시장 가격 적용: {current_price:,.0f}원/kg")
    else:
        current_price = crop_info["price_per_kg"]
        st.info(f"ℹ️ 기본 가격 적용: {current_price:,.0f}원/kg")
    
    # 기본 수확량 및 비용 계산
    base_yield = crop_info["yield_per_1000m2"] * land_area
    base_cost = crop_info["cost_per_1000m2"] * land_area
    
    # 경험에 따른 수확량 조정
    experience_multiplier = {"초보자": 0.7, "경험자": 1.0, "전문가": 1.3}
    adjusted_yield = base_yield * experience_multiplier[farming_experience]
    
    # 품질에 따른 가격 조정
    quality_multiplier = {"일반": 1.0, "고급": 1.3, "프리미엄": 1.6}
    adjusted_price = current_price * quality_multiplier[quality_grade]
    
    # 판매 방식에 따른 수익 조정
    market_multiplier = {"직판": 1.2, "도매": 0.8, "온라인": 1.1, "가공": 0.9}
    base_revenue = adjusted_yield * adjusted_price
    market_revenue = base_revenue * market_multiplier[market_type]
    
    # 유기농 재배 시 추가 비용 및 프리미엄
    if organic_farming:
        organic_cost = base_cost * 0.3
        organic_premium = 1.2
        final_revenue = market_revenue * organic_premium
        final_cost = base_cost + organic_cost
    else:
        final_revenue = market_revenue
        final_cost = base_cost
    
    # 최종 수익 계산
    final_profit = final_revenue - final_cost
    profit_margin = (final_profit / final_revenue) * 100 if final_revenue > 0 else 0
    
    # 결과 표시
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="result-card">
            <div class="result-value">{adjusted_yield:,.0f}kg</div>
            <div class="result-label">예상 수확량</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="result-card">
            <div class="result-value">{final_revenue:,.0f}원</div>
            <div class="result-label">예상 매출</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        profit_color = "#2E7D32" if final_profit > 0 else "#D32F2F"
        st.markdown(f"""
        <div class="result-card">
            <div class="result-value" style="color: {profit_color}">{final_profit:,.0f}원</div>
            <div class="result-label">예상 순익</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.subheader("📊 상세 분석")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**비용 분석**")
        st.write(f"• 기본 생산 비용: {base_cost:,.0f}원")
        if organic_farming:
            st.write(f"• 유기농 추가 비용: {organic_cost:,.0f}원")
        st.write(f"• **총 비용: {final_cost:,.0f}원**")
        
        st.markdown("**수익성 지표**")
        st.write(f"• 수익률: {profit_margin:.1f}%")
        if final_cost > 0:
            roi = (final_profit/final_cost)*100
            st.write(f"• 투자 대비 수익(ROI): {roi:.1f}%")
    
    with col2:
        st.markdown("**시장 분석**")
        st.write(f"• 기본 시장 가격: {current_price:,.0f}원/kg")
        st.write(f"• 조정된 가격: {adjusted_price:,.0f}원/kg")
        st.write(f"• 판매 방식: {market_type} (x{market_multiplier[market_type]})")
        if organic_farming:
            st.write(f"• 유기농 프리미엄: +20%")
        
        st.markdown("**생산 정보**")
        st.write(f"• 재배 기간: {crop_info['growth_period']}일")
        st.write(f"• 재배 시기: {crop_info['season']}")
        st.write(f"• 경지 면적: {land_area:,.1f} (1000m²)")
    
    st.markdown("---")
    st.subheader("📈 월별 수익 추이 예측")
    
    # 작물별 수확 시기에 따른 월별 수익 분포
    months = ["1월", "2월", "3월", "4월", "5월", "6월", "7월", "8월", "9월", "10월", "11월", "12월"]
    
    # 작물별 수확 패턴 정의
    harvest_patterns = {
        "쌀": [0, 0, 0, 0, 0, 0, 0, 0, 0.8, 0.2, 0, 0],
        "감자": [0, 0, 0, 0, 0, 0.5, 0.5, 0, 0, 0, 0, 0],
        "양파": [0, 0, 0, 0, 0, 0.7, 0.3, 0, 0, 0, 0, 0],
        "고구마": [0, 0, 0, 0, 0, 0, 0, 0, 0.3, 0.7, 0, 0],
        "배추": [0, 0, 0, 0, 0.3, 0.2, 0, 0, 0, 0.3, 0.2, 0],
        "사과": [0, 0, 0, 0, 0, 0, 0, 0, 0.2, 0.6, 0.2, 0],
        "포도": [0, 0, 0, 0, 0, 0, 0, 0.3, 0.5, 0.2, 0, 0]
    }
    
    pattern = harvest_patterns.get(selected_crop, [0]*12)
    monthly_revenue = [final_revenue * p for p in pattern]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=months,
        y=monthly_revenue,
        name="월별 수익",
        marker_color='#2E7D32',
        text=[f'{v:,.0f}원' if v > 0 else '' for v in monthly_revenue],
        textposition='outside'
    ))
    
    fig.update_layout(
        title="월별 예상 수익 분포",
        xaxis_title="월",
        yaxis_title="수익 (원)",
        showlegend=False,
        height=400,
        yaxis=dict(tickformat=',.0f')
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # 투자 회수 기간 계산
    if final_profit > 0:
        monthly_profit = final_profit / 12
        payback_period = final_cost / monthly_profit
        st.info(f"💡 **투자 회수 기간**: 약 {payback_period:.1f}개월")
    elif final_profit < 0:
        st.warning("⚠️ **주의**: 현재 설정으로는 손실이 예상됩니다.")
    
    st.markdown("---")
    st.subheader("💡 수익 개선을 위한 맞춤 조언")
    
    if profit_margin < 20:
        st.warning("⚠️ **수익률이 낮습니다** (20% 미만)")
        st.markdown("""
        **개선 방안:**
        - 🌟 고품질 작물 생산으로 프리미엄 가격 달성
        - 🏪 직판 등 직접 판매 방식으로 전환
        - 💰 생산비 절감을 위한 효율적인 농법 도입
        - 🤝 공동 구매/판매를 통한 규모의 경제 실현
        """)
    elif profit_margin < 40:
        st.info("ℹ️ **보통 수준의 수익률입니다** (20-40%)")
        st.markdown("""
        **성장 전략:**
        - 🌿 유기농 등 특수 작물 재배로 차별화
        - 🏭 가공 제품 생산으로 부가가치 창출
        - 📅 계절별 작물 조합으로 수익 안정화
        - 📱 온라인 판매 채널 다각화
        """)
    else:
        st.success("✅ **우수한 수익률입니다!** (40% 이상)")
        st.markdown("""
        **확장 전략:**
        - 📈 규모 확장을 통한 경제성 증대
        - 🌾 새로운 고수익 작물 도입 검토
        - 🎯 농업 관광, 체험 프로그램 등 부가 사업
        - 🔄 스마트팜 도입으로 생산성 극대화
        """)
    
    # 추가 팁
    with st.expander("🔍 더 자세한 분석 보기"):
        st.markdown("### 손익분기점 분석")
        breakeven_yield = final_cost / adjusted_price if adjusted_price > 0 else 0
        st.write(f"• 손익분기 수확량: {breakeven_yield:,.0f}kg")
        st.write(f"• 현재 예상 수확량: {adjusted_yield:,.0f}kg")
        st.write(f"• 여유율: {((adjusted_yield - breakeven_yield) / breakeven_yield * 100):.1f}%")
        
        st.markdown("### 시나리오 분석")
        # 최악의 경우 (수확량 30% 감소)
        worst_yield = adjusted_yield * 0.7
        worst_revenue = worst_yield * adjusted_price * market_multiplier[market_type]
        if organic_farming:
            worst_revenue *= 1.2
        worst_profit = worst_revenue - final_cost
        
        # 최선의 경우 (수확량 30% 증가)
        best_yield = adjusted_yield * 1.3
        best_revenue = best_yield * adjusted_price * market_multiplier[market_type]
        if organic_farming:
            best_revenue *= 1.2
        best_profit = best_revenue - final_cost
        
        scenario_df = pd.DataFrame({
            '시나리오': ['최악 (-30%)', '기본', '최선 (+30%)'],
            '수확량(kg)': [worst_yield, adjusted_yield, best_yield],
            '매출(원)': [worst_revenue, final_revenue, best_revenue],
            '순익(원)': [worst_profit, final_profit, best_profit]
        })
        
        st.dataframe(scenario_df.style.format({
            '수확량(kg)': '{:,.0f}',
            '매출(원)': '{:,.0f}',
            '순익(원)': '{:,.0f}'
        }))

st.markdown('</div>', unsafe_allow_html=True)

# --- 6. 사이드바 ---
with st.sidebar:
    st.header("🧮 계산기 가이드")
    st.info("""
    **계산에 포함된 요소:**
    
    📊 **기본 정보**
    - 경지 면적
    - 작물 종류
    - 농업 경험
    
    🎯 **품질 요소**
    - 품질 등급
    - 판매 방식
    - 유기농 여부
    
    💰 **수익 요소**
    - 예상 수확량
    - 시장 가격 (실시간)
    - 생산 비용
    """)
    
    st.divider()
    
    st.header("📈 수익성 지표")
    st.info("""
    **수익률 기준:**
    - 🔴 20% 미만: 낮음
    - 🟡 20-40%: 보통
    - 🟢 40% 이상: 높음
    
    **투자 회수 기간:**
    - ⭐ 12개월 이하: 우수
    - ✅ 12-24개월: 보통
    - ⚠️ 24개월 이상: 장기
    """)
    
    st.divider()
    
    st.header("💡 수익 개선 팁")
    st.info("""
    **주요 전략:**
    • 고품질 작물 생산
    • 직접 판매 방식 도입
    • 유기농 등 특수 작물
    • 가공 제품 생산
    • 계절별 작물 조합
    • 스마트팜 기술 도입
    """)
    
    st.divider()
    
    st.caption("💚 어디가농 - 스마트한 농업의 시작")
