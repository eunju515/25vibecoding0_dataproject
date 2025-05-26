import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

# 티커 및 기업명 매핑
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

st.title('글로벌 시가총액 Top 10 기업 주가 분석 (결측치 보간 적용)')

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

selected_company = st.selectbox('분석할 기업 선택', list(top10_companies.values()))
ticker = [k for k, v in top10_companies.items() if v == selected_company][0]

try:
    company_df = df[ticker][['Close']].reset_index()
    company_df.columns = ['Date', 'Close Price']
    # 결측치 보간 처리
    company_df['Close Price'] = company_df['Close Price'].interpolate(method='time')
    fig = px.line(
        company_df,
        x='Date',
        y='Close Price',
        title=f'{selected_company} 주가 추이 (최근 1년, 결측치 보간)',
        labels={'Close Price': '주가(USD)'}
    )
    st.plotly_chart(fig)
except KeyError:
    st.error(f"{selected_company} 데이터를 불러오는 데 실패했습니다.")
