import streamlit as st
import pandas as pd

st.title('특강 등록부')

uploaded_file = st.file_uploader("설문 결과 CSV 파일을 업로드하세요.", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    registration_df = df[['학번을 쓰시오', '이름을 쓰시오.']].copy()
    registration_df.columns = ['학번', '이름']
    st.write('학번과 이름으로 구성된 특강 등록부입니다.')
    st.dataframe(registration_df)
else:
    st.info("CSV 파일을 업로드하면 등록부가 표시됩니다.")
