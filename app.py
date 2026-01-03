import streamlit as st
import pandas as pd

# 점수 계산 함수
def calculate_score(row, preference):
    score = 0
    base_rate = row["기본금리(%)"]
    bonus_rate = row.get("우대금리(%)", 0)
    total_rate = base_rate + bonus_rate

    if preference == "금리 중시":
        score += total_rate * 2
        score += 1 if row["상품유형"] == "적금" else 0
    elif preference == "기간 중시":
        score += total_rate
        if row["기간(개월)"] <= 6:
            score += 3
        elif row["기간(개월)"] <= 12:
            score += 2
    elif preference == "적금 선호":
        score += total_rate
        score += 3 if row["상품유형"] == "적금" else 0

    if row.get("이자지급방식") == "복리":
        score += 1

    if row.get("최소가입금액", 0) <= 10000:
        score += 1

    return round(score, 2)


# 페이지 설정
st.set_page_config(
    page_title="예·적금 비교 서비스",
    page_icon="🏦",
    layout="wide"
)


# 데이터 불러오기
df = pd.read_csv("deposit_data.csv")

# 사이드바 – 필터
st.sidebar.header("🔍 필터")
product_type = st.sidebar.selectbox("상품 유형", options=["전체", "예금", "적금"])
bank = st.sidebar.multiselect("은행 선택", options=df["은행"].unique(), default=df["은행"].unique())
period = st.sidebar.selectbox("가입 기간(개월)", options=["전체"] + sorted(df["기간(개월)"].unique().tolist()))
rate_range = st.sidebar.slider(
    "금리 범위 (%)",
    min_value=float(df["기본금리(%)"].min()),
    max_value=float(df["기본금리(%)"].max() + df.get("우대금리(%)", 0).max()),
    value=(float(df["기본금리(%)"].min()), float(df["기본금리(%)"].max())),
    step=0.1
)
preference = st.sidebar.radio("추천 기준", ["금리 중시", "기간 중시", "적금 선호"])

# 홈 + 상품 비교
st.title("🏦 예·적금 금리 비교 서비스")
st.write("""
은행별 예·적금 상품을 비교하고, 사용자의 선호 기준에 따라 추천 점수를 계산합니다.
""")
st.write("💡 사이드바에서 필터를 조절하면 아래 상품 비교 결과가 업데이트 됩니다.")

# 필터링
filtered_df = df.copy()
if product_type != "전체":
    filtered_df = filtered_df[filtered_df["상품유형"] == product_type]
filtered_df = filtered_df[filtered_df["은행"].isin(bank)]
if period != "전체":
    filtered_df = filtered_df[filtered_df["기간(개월)"] == period]
filtered_df = filtered_df[
    (filtered_df["기본금리(%)"] >= rate_range[0]) &
    (filtered_df["기본금리(%)"] <= rate_range[1])
]

filtered_df["추천점수"] = filtered_df.apply(lambda row: calculate_score(row, preference), axis=1)
filtered_df = filtered_df.sort_values(by="추천점수", ascending=False)

# 상품 비교 결과 – 카드형 + 색상 강조
st.subheader("🔍 상품 비교 결과")
for idx, row in filtered_df.iterrows():
    is_top = idx == filtered_df.index[0]  # 최고 점수 상품
    bg_color = "#d4edda" if is_top else ("#cce5ff" if row['상품유형']=='예금' else "#fff3cd")  # 예금/적금 색상
    with st.container():
        st.markdown(f"""
        <div style="background-color:{bg_color}; padding:10px; border-radius:8px; margin-bottom:5px;">
        <b>{row['상품명']}</b>  |  {row['은행']}  |  {row['상품유형']}  |  기간: {row['기간(개월)']}개월  |  
        금리: {row['기본금리(%)']}% (+{row.get('우대금리(%)',0)}%)  |  점수: <b>{row['추천점수']}</b>
        </div>
        """, unsafe_allow_html=True)
        with st.expander("📄 상세 정보 보기"):
            st.write(f"- 가입조건: {row.get('가입조건', 'N/A')}")
            st.write(f"- 이자 지급 방식: {row.get('이자지급방식', '단리')}")
            st.write(f"- 최소 가입금액: {row.get('최소가입금액', 'N/A')}")
            st.write(f"- 최고금리: {row.get('최고금리(%)', 0)}%")
            st.write(f"- 추천 기준: {preference}")

st.markdown("---")


# 오늘의 추천 – 상위 3개 카드
st.subheader("🏆 오늘의 추천 상품")
df["추천점수"] = df.apply(lambda row: calculate_score(row, preference), axis=1)
top_df = df.sort_values(by="추천점수", ascending=False).head(3)

for idx, row in top_df.iterrows():
    bg_color = "#4d80f0" if idx == top_df.index[0] else "#c0d1ff"  # 최고 1개 진한 초록
    with st.container():
        st.markdown(f"""
        <div style="background-color:{bg_color}; padding:12px; border-radius:10px; margin-bottom:8px;">
        <h4>{row['상품명']}  |  {row['은행']}  |  점수: <b>{row['추천점수']}</b></h4>
        <p>기간: {row['기간(개월)']}개월 | 금리: {row['기본금리(%)']}% (+{row.get('우대금리(%)',0)}%) | 유형: {row['상품유형']} | {row.get('이자지급방식', '단리')}</p>
        </div>
        """, unsafe_allow_html=True)
        with st.expander("📄 상세 정보 보기"):
            st.write(f"- 가입조건: {row.get('가입조건', 'N/A')}")
            st.write(f"- 최소 가입금액: {row.get('최소가입금액', 'N/A')}")
            st.write(f"- 최고금리: {row.get('최고금리(%)', 0)}%")
            st.write(f"- 추천 기준: {preference}")
