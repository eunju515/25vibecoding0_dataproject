import streamlit as st
import pandas as pd
from docx import Document
from docx.shared import Pt, Inches
from docx.oxml.ns import qn
from docx.enum.text import WD_ALIGN_PARAGRAPH
import io

st.header("특강 등록부")

uploaded_file = st.file_uploader("설문 결과 CSV 파일을 업로드하세요.", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    registration_df = df[['학번을 쓰시오', '이름을 쓰시오.']].copy()
    registration_df.columns = ['학번', '이름']
    registration_df.insert(0, '구분', range(1, len(registration_df)+1))
    registration_df['서명'] = ''
    registration_df['비고'] = ''
    registration_df = registration_df[['구분', '학번', '이름', '서명', '비고']]

    doc = Document()
    doc.add_heading('AI와 함께하는 미래역량 특강 등록부', 0)

    table = doc.add_table(rows=1, cols=5)
    table.autofit = False
    table.allow_autofit = False
    table.style = 'Table Grid'

    # 헤더
    hdr_cells = table.rows[0].cells
    for i, col in enumerate(['구분', '학번', '이름', '서명', '비고']):
        hdr_cells[i].text = str(col)
        for paragraph in hdr_cells[i].paragraphs:
            paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = paragraph.runs[0]
            run.font.size = Pt(12)
            run.font.name = '맑은 고딕'  # 한글 폰트

    # 데이터
    for idx, row in registration_df.iterrows():
        row_cells = table.add_row().cells
        for i, value in enumerate(row):
            row_cells[i].text = str(value)
            for paragraph in row_cells[i].paragraphs:
                paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
                run = paragraph.runs[0]
                run.font.size = Pt(12)
                run.font.name = '맑은 고딕'

    # 셀 너비/높이 조정
    for row in table.rows:
        for cell in row.cells:
            cell.width = Inches(1.2)
            cell.height = Inches(0.4)

    # 저장
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)

    st.download_button(
        label="Word로 등록부 다운로드",
        data=buffer,
        file_name="특강등록부.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
    st.success("다운로드 후 바로 인쇄할 수 있습니다.")
else:
    st.info("CSV 파일을 업로드하면 등록부를 Word로 다운로드할 수 있습니다.")
