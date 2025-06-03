import streamlit as st
import pandas as pd
import io
import os

st.header("특강 등록부 생성")

uploaded_file = st.file_uploader("설문 결과 CSV 파일을 업로드하세요.", type="csv")

def find_column_by_keywords(columns, keywords):
    for col in columns:
        for kw in keywords:
            if kw.lower() in col.lower():
                return col
    return None

if uploaded_file is not None:
    # 파일명에서 확장자 제거하여 제목 생성
    base_title = os.path.splitext(uploaded_file.name)[0]
    title_text = f"{base_title} 등록부"

    df = pd.read_csv(uploaded_file)

    # 컬럼 정리
    df.columns = df.columns.str.strip().str.replace('\ufeff', '', regex=False)

    # 학번/이름 관련 키워드 정의
    id_keywords = ['학번', 'student id', 'id']
    name_keywords = ['이름', '성명', 'name']

    id_col = find_column_by_keywords(df.columns, id_keywords)
    name_col = find_column_by_keywords(df.columns, name_keywords)

    if not id_col or not name_col:
        st.error("❌ CSV에서 '학번' 또는 '이름'에 해당하는 컬럼을 찾을 수 없습니다.\n\n💡 설문 항목 이름에 '학번' 또는 '이름'이라는 단어가 포함되어야 합니다.")
        st.write("현재 컬럼 목록:", list(df.columns))
        st.stop()

    st.success(f"✅ 자동으로 인식된 컬럼: 학번 → `{id_col}`, 이름 → `{name_col}`")

    registration_df = df[[id_col, name_col]].copy()
    registration_df.columns = ['학번', '이름']

    # 학번 정렬
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

    # --- 미리보기 ---
    st.subheader("등록부 미리보기 (상위 10명)")
    st.dataframe(
        registration_df.head(10),
        use_container_width=True,
        hide_index=True,
        height=350,
        column_order=['구분', '학번', '이름', '서명', '비고']
    )

    # --- 엑셀 다운로드 ---
    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
        registration_df.to_excel(writer, index=False, sheet_name='등록부', startrow=2)
        workbook = writer.book
        worksheet = writer.sheets['등록부']

        # 제목 서식
        title_format = workbook.add_format({
            'bold': True,
            'font_size': 22,
            'align': 'center',
            'valign': 'vcenter'
        })
        worksheet.merge_range('A1:E1', '(         ) 특강 등록부', title_format)
        worksheet.set_row(1, 10)

        # 헤더 및 셀 서식
        header_format = workbook.add_format({
            'bold': True,
            'font_size': 14,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'bg_color': '#D9E1F2'
        })
        cell_format = workbook.add_format({
            'border': 1,
            'font_size': 14,
            'align': 'center',
            'valign': 'vcenter'
        })

        # 컬럼 너비 조정
        worksheet.set_column('A:A', 8)
        worksheet.set_column('B:B', 16)
        worksheet.set_column('C:C', 16)
        worksheet.set_column('D:E', 18)

        # 헤더 작성
        for col_num, value in enumerate(registration_df.columns.values):
            worksheet.write(2, col_num, value, header_format)

        # 데이터 작성
        for row_num in range(len(registration_df)):
            worksheet.set_row(row_num+3, 35)
            for col_num, value in enumerate(registration_df.iloc[row_num]):
                worksheet.write(row_num+3, col_num, value, cell_format)

        # 인쇄 반복
        worksheet.repeat_rows(0, 2)

    excel_buffer.seek(0)

    st.download_button(
        label="엑셀(xlsx)로 등록부 다운로드",
        data=excel_buffer,
        file_name=f"{base_title}_등록부.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    st.success(f"엑셀 인쇄 시 모든 페이지 상단에 '{title_text}'와 항목명이 반복되고, 제목/항목 행 높이는 자동, 데이터 행은 35로 고정됩니다.")

else:
    st.info("CSV 파일을 업로드하면 미리보기와 편집 가능한 엑셀 파일을 다운로드할 수 있습니다.")
