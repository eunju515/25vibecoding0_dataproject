import streamlit as st
import yfinance as yf
import plotly.graph_objs as go
from datetime import datetime, timedelta

st.set_page_config(page_title="글로벌 TOP10 주가 시각화", layout="wide")
st.title("🌎 글로벌 시가총액 TOP 10 기업 - 1년간 주가 변화")

# 시가총액 상위 10개 기업
companies = {
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Saudi Aramco": "2222.SR",
    "Alphabet (Google)": "GOOGL",
    "Amazon": "AMZN",
    "NVIDIA": "NVDA",
    "Berkshire Hathaway": "BRK-B",
    "Meta": "META",
    "TSMC": "TSM",
    "Tesla": "TSLA"
}

# 사용자 선택
selected = st.multiselect("비교할 기업을 선택하세요 (최대 5개 추천)", list(companies.keys()), default=["Apple", "Microsoft", "Amazon"])

# 날짜 범위 설정
end_date = datetime.today()
start_date = end_date - timedelta(days=365)

# Plotly 그래프 생성
fig = go.Figure()

for name in selected:
    ticker = companies[name]
    try:
        df = yf.download(ticker, start=start_date, end=end_date)
        fig.add_trace(go.Scatter(x=df.index, y=df['Close'], mode='lines', name=name))
    except Exception as e:
        st.error(f"{name} 데이터 로딩 실패: {e}")

fig.update_layout(
    title="최근 1년간 주가 변화 비교",
    xaxis_title="날짜",
    yaxis_title="종가 (USD)",
    hovermode="x unified",
    template="plotly_white",
    height=600
)

st.plotly_chart(fig, use_container_width=True)
