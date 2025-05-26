import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Plotly로 데이터 시각화하기")

# 파일 업로드 기능
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])

if uploaded_file is not None:
    # 사용자가 파일을 업로드한 경우
    df = pd.read_csv(uploaded_file)
    st.write("업로드한 데이터 미리보기:")
    st.dataframe(df)
else:
    # 예시 데이터 사용
    st.info("예시 데이터를 사용합니다.")
    data = {
        'Category': ['A', 'B', 'C', 'D'],
        'Value': [10, 15, 7, 12]
    }
    df = pd.DataFrame(data)
    st.dataframe(df)

# 컬럼 선택 (x, y)
x_col = st.selectbox("x축 컬럼 선택", df.columns)
y_col = st.selectbox("y축 컬럼 선택", df.columns)

# Plotly 그래프 그리기
fig = px.bar(df, x=x_col, y=y_col, title=f"{x_col}별 {y_col} 값")

st.plotly_chart(fig)
