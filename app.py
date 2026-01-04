import streamlit as st
import pandas as pd
from crawler import crawl_news
from collections import Counter
import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from datetime import datetime

# 기본 설정
st.set_page_config(
    page_title="오늘의 이슈 대시보드",
    layout="wide"
)

st.title("📰 오늘의 이슈 대시보드")
st.caption("실시간 뉴스 크롤링 기반 키워드 트렌드 분석")

# 사이드바 (컨트롤 센터)
st.sidebar.header("⚙️ 대시보드 설정")

category = st.sidebar.radio(
    "뉴스 카테고리",
    ["경제", "IT", "사회"]
)

max_page = st.sidebar.slider(
    "수집 페이지 수",
    1, 5, 3
)

search_term = st.sidebar.text_input(
    "🔍 제목 검색",
    placeholder="예: 삼성, 금리, AI"
)

show_wordcloud = st.sidebar.checkbox(
    "워드클라우드 표시",
    True
)

show_chart = st.sidebar.checkbox(
    "키워드 TOP 차트 표시",
    True
)

auto_refresh = st.sidebar.checkbox(
    "🔄 새로고침 (캐시 초기화)"
)

# 데이터 로드
@st.cache_data(ttl=600)
def load_data(keyword, max_page):
    return crawl_news(keyword, max_page)

if auto_refresh:
    st.cache_data.clear()

df = load_data(category, max_page)

st.success(f"🔄 마지막 업데이트: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if df.empty:
    st.warning("뉴스 데이터가 없습니다.")
    st.stop()

# 제목 검색 필터
if search_term:
    df = df[df["title"].str.contains(search_term, case=False, na=False)]

st.metric("📰 수집 기사 수", len(df))

# 탭 구성
tab1, tab2 = st.tabs(["📊 요약 & 키워드 분석", "🗞 기사 목록"])

# 📊 요약 & 키워드 분석
with tab1:
    # 키워드 전처리
    text = " ".join(df["title"].astype(str))
    words = re.findall(r"[가-힣]{2,}", text)

    STOPWORDS = {
        "있다","한다","했다","기자","뉴스","보도","관련","대한",
        "이번","통해","위해","때문","오늘","지난","면서","까지",
        "것","수","등","더","및","중"
    }

    words = [w for w in words if w not in STOPWORDS]

    if not words:
        st.warning("분석할 키워드가 부족합니다.")
        st.stop()

    top_word, top_count = Counter(words).most_common(1)[0]

    # 메트릭
    c1, c2, c3 = st.columns(3)
    c1.metric("총 기사 수", len(df))
    c2.metric("최다 키워드", top_word)
    c3.metric("등장 횟수", top_count)

    st.divider()

    # 본문 레이아웃
    col1, col2 = st.columns(2)

    # 기사 요약
    with col1:
        with st.expander("📰 주요 기사 TOP 10", expanded=True):
            st.dataframe(df.head(10), use_container_width=True)

            st.download_button(
                "📥 기사 목록 CSV 다운로드",
                df.to_csv(index=False).encode("utf-8-sig"),
                "news.csv",
                "text/csv"
            )

    # 키워드 분석
    with col2:
        with st.expander("📊 키워드 분석", expanded=True):

            if show_wordcloud:
                wc = WordCloud(
                    font_path="C:/Windows/Fonts/malgun.ttf",
                    background_color="white",
                    width=600,
                    height=300
                ).generate(" ".join(words))

                fig, ax = plt.subplots()
                ax.imshow(wc)
                ax.axis("off")
                st.pyplot(fig)

            if show_chart:
                counter = Counter(words)
                counter = {k: v for k, v in counter.items() if v >= 2}
                word_df = pd.DataFrame(
                    counter.items(),
                    columns=["단어", "빈도"]
                ).sort_values("빈도", ascending=False).head(10)

                st.bar_chart(word_df.set_index("단어"))

# 🗞 기사 목록
with tab2:
    st.subheader("기사 원문 바로가기")

    for _, row in df.iterrows():
        st.markdown(f"- [{row['title']}]({row['link']})")
