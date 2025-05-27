import streamlit as st
import pandas as pd
import io

st.header("특강 등록부 생성")

uploaded_file = st.file_uploader("설문 결과 CSV 파일을 업로드하세요.", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # 학번, 이름만 추출 및 정렬
    registration_df = df[['학번을 쓰시오', '이름을 쓰시오.']].copy()
    registration_df.columns = ['학번', '이름']
    def 학번정렬키(x):
        try:
            return int(str(x).replace('-', ''))
        except:
            return str(x)
    registration_df = registration_df.sort_values(by='학번', key=lambda col: col.map(학번정렬키)).reset_index(drop=True)
    registration_df.insert(0, '구분', range(1, len(registration_df)+1))
    registration_df['서명'] = ''
    registration_df['비고'] = ''
    registration_df = registration_df[['구분', '학번', '이름', '서명', '비고']]

    # --- 미리보기 (상위 10명, 가운데 정렬) ---
    st.subheader("등록부 미리보기 (상위 10명)")
    st.dataframe(
        registration_df.head(10),
        use_container_width=True,
        hide_index=True,
        height=350,
        column_order=['구분', '학번', '이름', '서명', '비고']
    )

    # --- 엑셀 다운로드 (테두리, 제목+항목명 반복) ---
    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
        # 제목과 헤더를 모두 데이터로 넣기 위해 startrow=1
        registration_df.to_excel(writer, index=False, sheet_name='등록부', startrow=1)
        workbook = writer.book
        worksheet = writer.sheets['등록부']

        # 제목 추가 (1행, 0-based index 0)
        title_format = workbook.add_format({
            'bold': True,
            'font_size': 16,
            'align': 'center',
            'valign': 'vcenter'
        })
        worksheet.merge_range('A1:E1', 'AI와 함께하는 미래역량 특강 등록부', title_format)

        # 헤더 및 셀 서식
        header_format = workbook.add_format({
            'bold': True,
            'font_size': 12,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'bg_color': '#D9E1F2'
        })
        cell_format = workbook.add_format({
            'border': 1,
            'font_size': 12,
            'align': 'center',
            'valign': 'vcenter'
        })

        # 컬럼 너비 조정
        worksheet.set_column('A:A', 8)
        worksheet.set_column('B:B', 16)
        worksheet.set_column('C:C', 16)
        worksheet.set_column('D:E', 18)

        # 헤더 서식 적용 (2행, 0-based index 1)
        for col_num, value in enumerate(registration_df.columns.values):
            worksheet.write(1, col_num, value, header_format)

        # 데이터 서식 적용 (3행부터, 0-based index 2)
        for row_num in range(len(registration_df)):
            worksheet.set_row(row_num+2, 22)
            for col_num, value in enumerate(registration_df.iloc[row_num]):
                worksheet.write(row_num+2, col_num, value, cell_format)

        # 인쇄 시 1~2행(제목+헤더)이 모든 페이지 상단에 반복되도록 설정
        worksheet.repeat_rows(0, 1)  # 0-based index: 0~1행 반복[4][2]

    excel_buffer.seek(0)

    st.download_button(
        label="엑셀(xlsx)로 등록부 다운로드",
        data=excel_buffer,
        file_name="특강등록부.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    st.success("엑셀 인쇄 시 모든 페이지 상단에 제목과 항목명이 반복됩니다.")
else:
    st.info("CSV 파일을 업로드하면 미리보기와 편집 가능한 엑셀 파일을 다운로드할 수 있습니다.")
