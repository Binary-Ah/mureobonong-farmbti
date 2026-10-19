# 물어보농 — 귀농 정책 RAG 플랫폼 · 농Bti 지역 추천

**2025학년도 ICT프로젝트 챌린지 – ICT경진대회 최우수상** (숭실대학교 × (주)렛유인에듀, 전공 6조, 2025.08.30)
팀 레포: [RAGfarmer/RAG](https://github.com/RAGfarmer/RAG) (비공개) · 이 레포는 **내가 작성한 파트만** 분리해 공개한 것

## Problem
귀농 정책 정보는 부처·지자체·교육기관에 흩어져 있어 예비 귀농인이 자기 상황에 맞는 정책을 찾기 어렵다. 정책 문서를 임베딩·검색하는 RAG 챗봇(팀) 위에, 사용자 성향 설문으로 검색 조건을 자동으로 채워주는 **농Bti**와 작물 수익 계산기를 붙였다.

## 전체 서비스 구성 (팀)
Streamlit 멀티페이지 앱 — 가이드북 / 지역 추천(농Bti) / 작물 수익 계산기 / 지원 혜택 / 귀농 뉴스 / RAG 챗봇(bge-m3 임베딩 + Chroma, LangChain agent) / Firebase 로그인

## My part
- **RAG 검색 파이프라인** (`pages/chatbot_logic/retriever`, 팀원과 공동 작업): 부처·지자체 귀농 정책 문서를 청킹·임베딩(bge-m3)해 Chroma 벡터 DB에 적재하고, 사용자 질문에 맞는 정책을 검색하는 로직을 팀원과 함께 설계·구현. 해당 코드는 팀원 계정으로 커밋되어 있어 이 레포에는 넣지 않았다 (팀 레포 참조).
- 아래는 내 계정(`Binary-Ah`)으로 커밋한 파일들:

| 파일 | 내용 |
|---|---|
| `rag_app/main.py` | 메인 랜딩 페이지 — 서비스 카드·네비게이션·로그인 분기·CSS (Streamlit) |
| `rag_app/pages/test.py` | **농Bti** 설문 페이지 — 10문항 → F/A/R/M 점수 → 유형 판정·캐릭터 이미지 |
| `rag_app/pages/calculator.py` | **작물 수익 계산기** — 작물별 단위면적 수확량·비용 테이블, KAMIS 실시간 도매가격 API 연동, 경험 수준·품질 등급 반영, 월별 수익 Plotly 시각화 |
| `rag_app/pages/data_loader/api_crawler.py` | 농사로(nongsaro) OpenAPI 크롤러 — 작물별 소득·작업 단계 수·병해충 수 수집 |
| `rag_app/pages/data_loader/create_final_region_data.py` | 140여 시·군 `region_data.csv` 생성 — 지역 특성 10개 피처 정규화 + 한줄평 |
| `rag_app/assets/*보농.png` | 농Bti 유형별 캐릭터 이미지 |
| `farmbti_api/` | 농Bti를 FastAPI + Streamlit 으로 분리한 독립 버전 — 사용자 F/A/R/M 점수 벡터와 지역 특성 벡터(공시지가·거래가·물가·학교/병원 밀도·인구밀도·커뮤니티·대기/수질·녹지) 간 **코사인 유사도**로 Top-3 지역 추천 |

## How to run
```bash
pip install streamlit pandas numpy plotly requests fastapi uvicorn
export KAMIS_API_KEY=...      # https://www.kamis.or.kr  (calculator.py)
export NONGSARO_API_KEY=...   # https://api.nongsaro.go.kr (api_crawler.py)

# 농Bti 독립 버전
cd farmbti_api && streamlit run streamlit_app.py
uvicorn app.main:app --reload   # API 서버
```
`rag_app/`은 팀 레포의 일부 파일만 있어 단독 실행되지 않는다 (챗봇·로그인 페이지는 팀원 코드).

## Docs
- `docs/물어보농_발표자료.pdf` — 최종 발표 자료

## Note
- 원본 코드의 API 키는 모두 환경변수로 치환했다. `.env`, `secrets.toml`, `chat.db`, 벡터 DB는 포함하지 않는다.
