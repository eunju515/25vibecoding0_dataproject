import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

# 시가총액 Top 10 기업 및 티커 매핑 (2025년 2월 기준)
top10_companies = {
    'AAPL': 'Apple',
    'NVDA': 'NVIDIA',
    'MSFT': 'Microsoft',
    'AMZN': 'Amazon',
    'GOOGL': 'Alphabet',
    'META': 'Meta Platforms',
    '2222.SR': 'Saudi Aramco',
    'TSLA': 'Tesla',
    'AVGO': 'Broadcom',
    'TSM': 'TSMC'
}

st.title('글로벌 시가총액 Top 10 기업 주가 분석')

# 데이터 불러오기
@st.cache_data
def load_stock_data():
    end_date = pd.Timestamp.now()
    start_date = end_date - pd.DateOffset(years=1)
    
    data = yf.download(
        tickers=list(top10_companies.keys()),
        start=start_date,
        end=end_date,
        group_by='ticker'
    )
    return data

df = load_stock_data()

# 기업 선택 위젯
selected_company = st.selectbox(
    '분석할 기업 선택',
    options=list(top10_companies.values())
)

# 선택된 기업 티커 추출
ticker = [k for k, v in top10_companies.items() if v == selected_company][0]

# 주가 데이터 추출
try:
    company_df = df[ticker][['Close']].reset_index()
    company_df.columns = ['Date', 'Close Price']
    
    # Plotly 시각화
    fig = px.line(
        company_df,
        x='Date',
        y='Close Price',
        title=f'{selected_company} 주가 추이 (최근 1년)',
        labels={'Close Price': '주가(USD)'}
    )
    
    st.plotly_chart(fig)
    
except KeyError:
    st.error(f"{selected_company} 데이터를 불러오는 데 실패했습니다.")

# 추가 분석 옵션
st.subheader("추가 분석 옵션")
if st.checkbox('모든 기업 주가 비교 보기'):
    close_prices = pd.DataFrame({
        company: df[ticker]['Close'] 
        for ticker, company in top10_companies.items()
        if 'Close' in df[ticker]
    })
    
    fig = px.line(
        close_prices,
        title='Top 10 기업 주가 비교',
        labels={'value': '주가(USD)', 'variable': '기업'}
    )
    st.plotly_chart(fig)
