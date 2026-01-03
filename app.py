import streamlit as st
import pandas as pd


def calculate_score(row):
    score = 0

    # 1. 금리 점수 (가중치 0.6)
    score += row["금리(%)"] * 0.6

    # 2. 기간 점수 (짧을수록 점수 높음)
    if row["기간(개월)"] <= 6:
        score += 2
    elif row["기간(개월)"] <= 12:
        score += 1

    # 3. 상품유형 가중치
    if row["상품유형"] == "적금":
        score += 1.5

    return round(score, 2)


# -------------------------
# 1. 페이지 설정
# -------------------------
st.set_page_config(
    page_title="예·적금 금리 비교",
    page_icon="🏦",
    layout="wide"
)

st.title("🏦 예·적금 금리 비교 서비스")
st.write("은행별 예·적금 상품을 한눈에 비교할 수 있습니다.")

# -------------------------
# 2. 더미 데이터 생성
# -------------------------
data = [
    {"은행": "국민은행", "상품명": "KB Star 정기예금", "상품유형": "예금", "금리(%)": 3.20, "기간(개월)": 12},
    {"은행": "신한은행", "상품명": "쏠편한 정기예금", "상품유형": "예금", "금리(%)": 3.35, "기간(개월)": 12},
    {"은행": "우리은행", "상품명": "WON 정기예금", "상품유형": "예금", "금리(%)": 3.10, "기간(개월)": 6},
    {"은행": "하나은행", "상품명": "하나의 정기예금", "상품유형": "예금", "금리(%)": 3.25, "기간(개월)": 12},
    {"은행": "국민은행", "상품명": "KB 자유적금", "상품유형": "적금", "금리(%)": 3.80, "기간(개월)": 12},
    {"은행": "신한은행", "상품명": "신한 My 적금", "상품유형": "적금", "금리(%)": 4.00, "기간(개월)": 12},
    {"은행": "우리은행", "상품명": "우리 WON 적금", "상품유형": "적금", "금리(%)": 3.70, "기간(개월)": 6},
    {"은행": "하나은행", "상품명": "하나 청년 적금", "상품유형": "적금", "금리(%)": 4.10, "기간(개월)": 12},
]

df = pd.DataFrame(data)

# -------------------------
# 3. 사이드바 필터
# -------------------------
st.sidebar.header("🔍 필터 설정")

product_type = st.sidebar.selectbox(
    "상품 유형",
    options=["전체", "예금", "적금"]
)

bank = st.sidebar.multiselect(
    "은행 선택",
    options=df["은행"].unique(),
    default=df["은행"].unique()
)

period = st.sidebar.selectbox(
    "가입 기간(개월)",
    options=["전체"] + sorted(df["기간(개월)"].unique().tolist())
)

rate_range = st.sidebar.slider(
    "금리 범위 (%)",
    min_value=float(df["금리(%)"].min()),
    max_value=float(df["금리(%)"].max()),
    value=(float(df["금리(%)"].min()), float(df["금리(%)"].max())),
    step=0.1
)

# -------------------------
# 4. 필터링 로직
# -------------------------
filtered_df = df.copy()

if product_type != "전체":
    filtered_df = filtered_df[filtered_df["상품유형"] == product_type]

filtered_df = filtered_df[filtered_df["은행"].isin(bank)]

if period != "전체":
    filtered_df = filtered_df[filtered_df["기간(개월)"] == period]

filtered_df = filtered_df[
    (filtered_df["금리(%)"] >= rate_range[0]) &
    (filtered_df["금리(%)"] <= rate_range[1])
]

filtered_df["추천점수"] = filtered_df.apply(calculate_score, axis=1)

# 추천 점수 기준 정렬
filtered_df = filtered_df.sort_values(by="추천점수", ascending=False)


# -------------------------
# 5. 금리순 정렬
# -------------------------
filtered_df = filtered_df.sort_values(by="금리(%)", ascending=False)

# -------------------------
# 6. 결과 출력
# -------------------------
st.subheader("📊 상품 비교 결과")
st.dataframe(filtered_df, use_container_width=True)


st.subheader("🏦 은행별 평균 금리")

avg_rate_by_bank = (
    filtered_df
    .groupby("은행")["금리(%)"]
    .mean()
    .reset_index()
)

st.bar_chart(avg_rate_by_bank.set_index("은행"))


st.subheader("📈 예금 vs 적금 평균 금리")

avg_rate_by_type = (
    filtered_df
    .groupby("상품유형")["금리(%)"]
    .mean()
    .reset_index()
)

st.bar_chart(avg_rate_by_type.set_index("상품유형"))


# -------------------------
# 7. 최고 금리 상품 강조
# -------------------------
if not filtered_df.empty:
    top = filtered_df.iloc[0]
    st.success(
        f"🤖 추천 1위: [{top['은행']}] {top['상품명']} | "
        f"금리 {top['금리(%)']}% | 추천점수 {top['추천점수']}"
    )

else:
    st.warning("조건에 맞는 상품이 없습니다.")
