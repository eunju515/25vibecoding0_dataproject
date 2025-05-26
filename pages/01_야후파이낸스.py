import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

# 2025년 기준 글로벌 시가총액 Top 10 (미국 중심, 데이터 수집 안정성 고려)
top10_companies = {
    'AAPL': 'Apple',
    'MSFT': 'Microsoft',
    'NVDA': 'NVIDIA',
    'AMZN': 'Amazon',
    'GOOGL': 'Alphabet',
    'META': 'Meta Platforms',
    'TSLA': 'Tesla',
    'AVGO': 'Broadcom',
    'TSM': 'TSMC',
    'BRK-B': 'Berkshire Hathaway'
}

st.title("글로벌 시가총액 Top 10 기업의 최근 1년 주가 변화")

@st.cache_data
def load_stock_data(tickers):
    end_date = pd.Timestamp.now()
    start_date = end_date - pd.DateOffset(years=1)
    data = {}
    for ticker in tickers:
        try:
            df = yf.download(ticker, start=start_date, end=end_date, progress=False)
            if not df.empty:
                data[ticker] = df['Close']
        except Exception as e:
            st.warning(f"{ticker} 데이터 다운로드 실패: {e}")
    if not data:
        st.error("모든 티커의 데이터를 불러오는 데 실패했습니다.")
        st.stop()
    return pd.DataFrame(data)

df = load_stock_data(list(top10_companies.keys()))

# 결측치 선형 보간
df = df.interpolate(method='time')

# 날짜 인덱스 컬럼화
df = df.reset_index()

# 기업 선택
company_names = [top10_companies[ticker] for ticker in df.columns if ticker != 'Date']
selected_company = st.selectbox("기업을 선택하세요", company_names)

# 티커 역매핑
ticker_map = {v: k for k, v in top10_companies.items()}
selected_ticker = ticker_map[selected_company]

# 단일 기업 시각화
fig = px.line(
    df,
    x='Date',
    y=selected_ticker,
    title=f"{selected_company} (최근 1년 주가)",
    labels={selected_ticker: "주가(USD)", "Date": "날짜"}
)
st.plotly_chart(fig, use_container_width=True)

# 전체 비교 옵션
st.subheader("Top 10 기업 주가 비교")
if st.checkbox("모든 기업 주가를 한 번에 보기"):
    fig_all = px.line(
        df,
        x='Date',
        y=[ticker for ticker in top10_companies.keys() if ticker in df.columns],
        labels={"value": "주가(USD)", "variable": "기업", "Date": "날짜"},
        title="Top 10 기업 주가 비교 (최근 1년)"
    )
    # 기업명으로 범례 표시
    fig_all.for_each_trace(
        lambda t: t.update(name=top10_companies.get(t.name, t.name))
    )
    st.plotly_chart(fig_all, use_container_width=True)

st.caption("데이터 출처: Yahoo Finance / 결측치는 선형 보간 처리됨")
