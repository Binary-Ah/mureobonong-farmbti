# farmre/scripts/load_data.py

import pandas as pd
from sqlalchemy import create_engine
import os

# --- 설정 (사용자 환경에 맞게 수정해주세요) ---
# 1. CSV 파일 경로
# 이 스크립트는 farmre/scripts/ 폴더 안에 있으므로, 상위 폴더로 이동해야 data 폴더에 접근 가능합니다.
CSV_FILE_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'FARM_normalized_updated.csv')

# 2. PostgreSQL 연결 정보
# 미리 'farmbti_db' 라는 이름의 데이터베이스를 생성해두어야 합니다.
DB_USER = "your_username"  # PostgreSQL 사용자 이름
DB_PASSWORD = os.environ.get("DB_PASSWORD", "")  # set via environment variable
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "farmbti_db"
TABLE_NAME = "regions" # 데이터를 저장할 테이블 이름

# --- 데이터베이스 연결 및 데이터 로드 ---
def load_csv_to_db():
    # 데이터베이스 연결 엔진 생성
    engine_url = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    engine = create_engine(engine_url)
    
    print("CSV 파일 읽는 중...")
    if not os.path.exists(CSV_FILE_PATH):
        print(f"오류: {CSV_FILE_PATH} 에서 파일을 찾을 수 없습니다.")
        return
        
    df = pd.read_csv(CSV_FILE_PATH)
    
    print(f"'{TABLE_NAME}' 테이블에 데이터 저장 시작...")
    
    try:
        # pandas DataFrame을 SQL 테이블로 저장
        # if_exists='replace'는 테이블이 이미 존재하면 기존 테이블을 삭제하고 새로 만드는 옵션입니다.
        df.to_sql(TABLE_NAME, engine, if_exists='replace', index=False)
        print("데이터 저장 완료!")
    except Exception as e:
        print(f"데이터 저장 중 오류 발생: {e}")

if __name__ == "__main__":
    load_csv_to_db()