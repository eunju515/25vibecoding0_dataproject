import streamlit as st
import pandas as pd

# 설문 결과 파일명 (같은 폴더에 있어야 함)
file_path = 'AIwa-hamggehaneun-miraeyeogryang-teuggang-sinceong-eungdab-seolmunji-eungdab-siteu1.csv'

# CSV 파일에서 학번과 이름만 추출
df = pd.read_csv(file_path)
registration_df = df[['학번을 쓰시오', '이름을 쓰시오.']].copy()
registration_df.columns = ['학번', '이름']

st.title('특강 등록부')
st.write('학번과 이름으로 구성된 특강 등록부입니다.')
st.dataframe(registration_df)
