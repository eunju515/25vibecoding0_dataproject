import streamlit as st
import pandas as pd

st.title('AI와 함께하는 미래역량 특강 등록부')  # 특강제목 등록부 타이틀

uploaded_file = st.file_uploader("설문 결과 CSV 파일을 업로드하세요.", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    # 학번, 이름 컬럼 추출 및 컬럼명 정리
    registration_df = df[['학번을 쓰시오', '이름을 쓰시오.']].copy()
    registration_df.columns = ['학번', '이름']
    # 구분, 서명, 비고 컬럼 추가
    registration_df.insert(0, '구분', '')      # 첫 번째 열에 '구분' 추가
    registration_df['서명'] = ''
    registration_df['비고'] = ''
    st.write('아래는 특강 등록부입니다. (구분/서명/비고란 포함)')
    st.dataframe(registration_df)
else:
    st.info("CSV 파일을 업로드하면 등록부가 표시됩니다.")
