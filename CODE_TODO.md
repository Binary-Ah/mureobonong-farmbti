# CODE_TODO — mureobonong-farmbti

- [ ] **역할 표현 확인**: 지원서·CV에는 "RAG 검색 파이프라인 구현(정책 문서 임베딩·검색 로직 설계)"으로 썼지만, 팀 레포 git log 상 `Binary-Ah` 커밋은 main.py / 농Bti(test.py) / calculator.py / data_loader / region_data 뿐이다. `pages/chatbot_logic/retriever` 는 다른 팀원 커밋. RAG 파트에 실제 기여(설계 회의, 문서 청킹 등)가 있었다면 README "My part"에 근거와 함께 추가하고, 아니면 지원서 표현을 "농Bti·수익 계산기·데이터 파이프라인 담당"으로 맞출 것
- [ ] `farmbti_api/app/services/recommendation.py` 가 읽는 `data/FARM_normalized_updated.csv` 가 없음 — `region_data.csv` 로 경로 통일하거나 파일 추가
- [ ] `rag_app/pages/test.py` 파일명이 `test.py` — 레포에서는 `farmbti.py` 로 바꾸는 것을 권장 (main.py의 switch_page 경로도 함께)
- [ ] `docs/물어보농_발표자료.pdf` 24MB — 올릴지 결정 (GitHub 100MB 제한 내이지만 클론이 무거워짐; 링크로 대체 가능)
- [ ] 팀원(박성진·Suyeon-j·junekyu02)에게 개인 파트 공개 레포 생성 사실 공유
- [ ] `WhereToFarm/`(어디가농, D209_우아한자매들)은 다른 팀의 포팅 매뉴얼이 포함된 참고용 클론으로 보임 — 포트폴리오에 포함하지 말 것
