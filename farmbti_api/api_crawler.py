import requests
import pandas as pd
import xml.etree.ElementTree as ET
import time
import os # 폴더 및 파일 경로 관리를 위해 import

# --- 설정 부분 ---
API_KEY = os.environ.get("NONGSARO_API_KEY", "")  # set via environment variable
TARGET_CROPS = ['쌀', '사과', '고구마', '상추', '딸기', '고추', '허브']

# --- API 호출 함수 (이전과 동일) ---
def get_income_data(crop_name):
    url = 'http://api.nongsaro.go.kr/service/income/incomeList'
    params = {'apiKey': API_KEY, 'itemNm': crop_name}
    try:
        response = requests.get(url, params=params)
        root = ET.fromstring(response.content)
        item = root.find('.//item')
        income = item.find('income').text if item and item.find('income') is not None else '0'
        return int(income.replace(',', ''))
    except Exception: return 0

def get_work_schedule_count(crop_name):
    url = 'http://api.nongsaro.go.kr/service/farmWorkingPlan/farmWorkingPlanList'
    params = {'apiKey': API_KEY, 'sType': 'sCntntsSj', 'sText': crop_name}
    try:
        response = requests.get(url, params=params)
        root = ET.fromstring(response.content)
        return len(root.findall('.//workStepNm'))
    except Exception: return 0

def get_pest_info_count(crop_name):
    url = 'http://api.nongsaro.go.kr/service/pesticide/cropPestiList'
    params = {'apiKey': API_KEY, 'cropName': crop_name}
    try:
        response = requests.get(url, params=params)
        root = ET.fromstring(response.content)
        return len(root.findall('.//item'))
    except Exception: return 0

# --- 메인 실행 로직 ---
if __name__ == "__main__":
    crop_details = []
    print("농사로 API를 통해 작물 데이터 수집을 시작합니다...")

    for crop in TARGET_CROPS:
        print(f"'{crop}' 데이터 수집 중...")
        crop_details.append({
            '작물명': crop, '소득정보': get_income_data(crop),
            '작업단계수': get_work_schedule_count(crop), '병해충정보수': get_pest_info_count(crop)
        })
        time.sleep(1)

    df = pd.DataFrame(crop_details)
    
    # CARE 점수 계산 (정규화)
    df['CARE_R'] = (df['소득정보'] - df['소득정보'].min()) / (df['소득정보'].max() - df['소득정보'].min()) if df['소득정보'].max() > df['소득정보'].min() else 0
    df['CARE_A'] = (df['작업단계수'] - df['작업단계수'].min()) / (df['작업단계수'].max() - df['작업단계수'].min()) if df['작업단계수'].max() > df['작업단계수'].min() else 0
    df['CARE_C'] = (df['병해충정보수'] - df['병해충정보수'].min()) / (df['병해충정보수'].max() - df['병해충정보수'].min()) if df['병해충정보수'].max() > df['병해충정보수'].min() else 0
    df['CARE_E'] = 0.5 # 효율성은 기본값 설정 후 수동 조절 권장
    final_df = df[['작물명', 'CARE_C', 'CARE_A', 'CARE_R', 'CARE_E']].fillna(0)

    # 유형 및 특징 추가 (수동 관리 영역)
    type_mapping = {'쌀': '벼보농', '사과': '사과보농', '고구마': '고구마보농', '상추': '상추보농', '딸기': '도전보농', '고추': '고구마보농', '허브': '힐링보농'}
    feature_mapping = {'쌀': '안정적인 판로 확보가 장점', '사과': '브랜드 가치가 높음', '고구마': '비교적 관리가 쉬움', '상추': '빠른 결과 확인 가능', '딸기': '최신 기술 활용', '고추': '다양한 요리에 활용', '허브': '소규모 텃밭에 적합'}
    final_df['추천유형'] = final_df['작물명'].map(type_mapping)
    final_df['특징'] = final_df['작물명'].map(feature_mapping)
    
    # 'data' 폴더 생성 및 저장 경로 설정
    os.makedirs('data', exist_ok=True) 
    save_path = os.path.join('data', 'crop_data.csv')
    
    final_df.to_csv(save_path, index=False, encoding='utf-8-sig')

    print(f"\n✅ API 데이터 수집 완료! '{save_path}' 파일이 생성되었습니다.")
    print("이 파일을 직접 검토하고 수정하여 완성도를 높여주세요.")
    print(final_df)