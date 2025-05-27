import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder

st.title('AI와 함께하는 미래역량 특강 등록부')

uploaded_file = st.file_uploader("설문 결과 CSV 파일을 업로드하세요.", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    # 학번과 이름만 추출
    registration_df = df[['학번을 쓰시오', '이름을 쓰시오.']].copy()
    registration_df.columns = ['학번', '이름']
    # 일련번호(구분) 추가
    registration_df.insert(0, '구분', range(1, len(registration_df)+1))
    # 서명, 비고 컬럼 추가
    registration_df['서명'] = ''
    registration_df['비고'] = ''
    # 컬럼 순서 재정렬
    registration_df = registration_df[['구분', '학번', '이름', '서명', '비고']]
    
    # AgGrid 옵션: 모든 컬럼 가운데 정렬
    gb = GridOptionsBuilder.from_dataframe(registration_df)
    for col in registration_df.columns:
        gb.configure_column(col, cellStyle={'textAlign': 'center'})
    grid_options = gb.build()
    
    st.write('아래는 특강 등록부입니다. (모든 셀 가운데 정렬)')
    AgGrid(
        registration_df,
        gridOptions=grid_options,
        fit_columns_on_grid_load=True,
        height=500
    )
else:
    st.info("CSV 파일을 업로드하면 등록부가 표시됩니다.")
