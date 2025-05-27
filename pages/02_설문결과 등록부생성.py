import streamlit as st
import pandas as pd

st.set_page_config(page_title="AI와 함께하는 미래역량 특강 등록부")  # 웹페이지 타이틀

st.header("특강 등록부")  # 특강등록부의 제목(표 위에 크게 표시)

uploaded_file = st.file_uploader("설문 결과 CSV 파일을 업로드하세요.", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    # 학번, 이름 컬럼 추출 및 컬럼명 정리
    registration_df = df[['학번을 쓰시오', '이름을 쓰시오.']].copy()
    registration_df.columns = ['학번', '이름']
    # 일련번호(구분) 추가
    registration_df.insert(0, '구분', range(1, len(registration_df)+1))
    # 서명, 비고 컬럼 추가
    registration_df['서명'] = ''
    registration_df['비고'] = ''
    # 컬럼 순서 재정렬
    registration_df = registration_df[['구분', '학번', '이름', '서명', '비고']]

    # 표와 헤더 모두 가운데 정렬: HTML/CSS 사용
    styled_table = registration_df.style.set_properties(**{'text-align': 'center'}) \
        .set_table_styles([{'selector': 'th', 'props': [('text-align', 'center')]}])

    # 표 표시 (HTML 렌더링)
    st.markdown(
        styled_table.to_html(escape=False, index=False),
        unsafe_allow_html=True
    )

    # 다운로드 버튼용 CSV 변환 함수
    @st.cache_data
    def convert_df(df):
        return df.to_csv(index=False).encode('utf-8')

    csv = convert_df(registration_df)
    st.download_button(
        label="등록부 CSV 다운로드",
        data=csv,
        file_name='특강등록부.csv',
        mime='text/csv'
    )
else:
    st.info("CSV 파일을 업로드하면 등록부가 표시되고 다운로드할 수 있습니다.")
