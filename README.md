# IssueDashboard

IssueDashboard는 공개 뉴스 검색 결과를 수집하여 오늘의 주요 이슈를 한눈에 파악할 수 있도록 요약, 키워드 분석, 시각화를 제공하는 Streamlit 기반 뉴스 이슈 대시보드입니다.
본 프로젝트는 공개 웹 페이지에서 최소한의 정보(기사 제목, 링크)만을 수집합니다.

---

## 🔍 주요 기능

* Daum 뉴스 검색 결과 크롤링
* 카테고리별 뉴스 수집 (경제 / IT / 사회)
* 기사 제목 기반 키워드 분석
* 워드클라우드 및 키워드 빈도 차트 시각화
* 기사 목록 카드형 UI 제공
* 기사 즐겨찾기 기능
* CSV 다운로드 기능

---

## 🛠 기술 스택

* **Language**: Python 3
* **Framework**: Streamlit
* **Crawling**: requests, BeautifulSoup
* **Data Handling**: pandas
* **Visualization**: matplotlib, wordcloud

---

## 📂 프로젝트 구조

```
IssueDashboard/
├─ app.py              # Streamlit 메인 애플리케이션
├─ crawler.py          # 뉴스 크롤링 로직
├─ requirements.txt    # 의존성 패키지 목록
└─ README.md
```

---

## ▶ 실행 방법

### 1️⃣ 패키지 설치

```bash
pip install -r requirements.txt
```

### 2️⃣ 애플리케이션 실행

```bash
streamlit run app.py
```

---

## 크롤링 관련 안내

* 본 프로젝트는 **공개된 뉴스 검색 결과 페이지**만을 대상으로 합니다.
* 로그인, 인증, 기사 본문 수집은 수행하지 않습니다.
* 개인 학습 및 포트폴리오 목적의 소규모 사용을 전제로 합니다.

---
