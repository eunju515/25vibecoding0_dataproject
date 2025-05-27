import streamlit as st
import pandas as pd
import io
import re

st.header("생활기록부 기초파일 생성기")

uploaded_file = st.file_uploader("설문 결과 CSV 파일을 업로드하세요.", type="csv")

def extract_main_word(question):
    q = re.sub(r'\s*\(.*\)\s*', '', question)
    q = re.sub(r'[\s.,?…!]*$', '', q)
    q = re.sub(r'(을|를|에|의|은|는|도|가|이|으로|로)\s*', '', q)
    q = re.sub(r'(쓰시오|적으시오|입력하시오|작성|적기|써주세요|다시 입력하시오)', '', q)
    return q.strip() or question

def add_items():
    for col in st.session_state.get('add_cols', []):
        if col not in st.session_state.sel_cols:
            st.session_state.sel_cols.append(col)
    st.session_state.add_cols = []

def remove_items():
    st.session_state.sel_cols = [
        col for col in st.session_state.sel_cols 
        if col not in st.session_state.get('remove_cols', [])
    ]
    st.session_state.remove_cols = []

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    columns = list(df.columns)
    
    # 학번, 이름 컬럼 자동 탐지
    id_col = next((col for col in columns if '학번' in col), None)
    name_col = next((col for col in columns if '이름' in col), None)
    
    if not id_col or not name_col:
        st.error("CSV 파일에 학번 또는 이름 컬럼이 존재하지 않습니다.")
        st.stop()

    # 세션 상태 초기화
    if 'sel_cols' not in st.session_state:
        st.session_state.sel_cols = []

    # 항목 추가/제거 UI
    st.write("생기부 기초파일에 포함할 항목을 추가/제거하세요.")
    
    col1, col2 = st.columns(2)
    with col1:
        selectable_cols = [col for col in columns if col not in [id_col, name_col] + st.session_state.sel_cols]
        add_cols = st.multiselect(
            "추가할 설문 항목 선택 (중복 불가)",
            selectable_cols,
            key='add_cols'
        )
        st.button("항목 추가하기", on_click=add_items)

    with col2:
        if st.session_state.sel_cols:
            remove_cols = st.multiselect(
                "제거할 설문 항목 선택",
                st.session_state.sel_cols,
                key='remove_cols'
            )
            st.button("항목 제거하기", on_click=remove_items)

    if st.button("모든 항목 초기화"):
        st.session_state.sel_cols = []

    # 최종 컬럼 및 항목명 변환
    final_cols = [id_col, name_col] + st.session_state.sel_cols
    new_col_names = [extract_main_word(col) for col in final_cols]

    st.markdown(f"**현재 선택된 항목:** {' → '.join(new_col_names)}")

    # 미리보기 생성 (컬럼 존재 여부 확인)
    if all(col in df.columns for col in final_cols):
        preview_df = df[final_cols].fillna('').replace('nan', '').head(10)
        preview_df.columns = new_col_names
        st.subheader("생기부 기초파일 미리보기 (상위 10명)")
        st.dataframe(preview_df, use_container_width=True, hide_index=True)
    else:
        st.error("선택한 항목 중 일부가 CSV 파일에 존재하지 않습니다.")

    # 엑셀 다운로드
    if final_cols and all(col in df.columns for col in final_cols):
        output = io.BytesIO()
        base_df = df[final_cols].fillna('')
        base_df.columns = new_col_names
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            base_df.to_excel(writer, index=False, sheet_name="생기부기초")
            workbook = writer.book
            worksheet = writer.sheets["생기부기초"]
            header_format = workbook.add_format({
                'bold': True, 'font_size': 12, 'align': 'center', 
                'valign': 'vcenter', 'border': 1, 'bg_color': '#D9E1F2'
            })
            cell_format = workbook.add_format({
                'font_size': 12, 'align': 'center', 'valign': 'vcenter', 'border': 1
            })
            worksheet.set_row(0, 28)
            for col_num, value in enumerate(new_col_names):
                worksheet.write(0, col_num, value, header_format)
                worksheet.set_column(col_num, col_num, 18)
            for row_num in range(1, len(base_df)+1):
                worksheet.set_row(row_num, 22)
                for col_num in range(len(new_col_names)):
                    worksheet.write(row_num, col_num, base_df.iloc[row_num-1, col_num], cell_format)
        output.seek(0)
        st.download_button(
            label="생기부 기초 엑셀파일 다운로드",
            data=output,
            file_name="생기부기초.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.warning("다운로드 가능한 데이터가 없습니다.")
else:
    st.info("CSV 파일을 업로드하면 항목을 추가/제거하며 생기부 기초파일을 만들 수 있습니다.")
