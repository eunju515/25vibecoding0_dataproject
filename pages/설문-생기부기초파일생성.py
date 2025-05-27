import streamlit as st
import pandas as pd
import io
import re

st.header("생활기록부 기초파일 생성기")

uploaded_file = st.file_uploader("설문 결과 CSV 파일을 업로드하세요.", type="csv")

def extract_main_word(question):
    q = question
    q = re.sub(r'\s*\(.*\)\s*', '', q)
    q = re.sub(r'[\s.,?…!]*$', '', q)
    q = re.sub(r'(을|를|에|의|은|는|도|가|이|으로|로)\s*', '', q)
    q = re.sub(r'(쓰시오|적으시오|입력하시오|작성|적기|써주세요|다시 입력하시오)', '', q)
    q = q.strip()
    return q if q else question

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    columns = list(df.columns)
    id_col = [col for col in columns if '학번' in col][0]
    name_col = [col for col in columns if '이름' in col][0]

    # 세션 상태 관리
    if 'sel_cols' not in st.session_state:
        st.session_state.sel_cols = []

    # 항목 추가 UI
    selectable_cols = [col for col in columns if col not in [id_col, name_col] + st.session_state.sel_cols]
    st.write("생기부 기초파일에 포함할 항목을 추가/제거하세요.")
    
    col1, col2 = st.columns(2)
    with col1:
        add_cols = st.multiselect(
            "추가할 설문 항목 선택 (중복 불가)",
            selectable_cols,
            key='add_cols'
        )
        if st.button("항목 추가하기"):
            for col in add_cols:
                if col not in st.session_state.sel_cols:
                    st.session_state.sel_cols.append(col)
            st.session_state.add_cols = []

    # 항목 제거 UI
    with col2:
        if st.session_state.sel_cols:
            remove_cols = st.multiselect(
                "제거할 설문 항목 선택",
                st.session_state.sel_cols,
                key='remove_cols'
            )
            if st.button("항목 제거하기"):
                st.session_state.sel_cols = [col for col in st.session_state.sel_cols if col not in remove_cols]
                st.session_state.remove_cols = []

    # 모든 항목 초기화 버튼
    if st.button("모든 항목 초기화"):
        st.session_state.sel_cols = []

    # 최종 컬럼 및 항목명 변환
    final_cols = [id_col, name_col] + st.session_state.sel_cols
    new_col_names = [extract_main_word(col) for col in final_cols]

    st.markdown(f"**현재 선택된 항목:** {' → '.join(new_col_names)}")

    # 미리보기 (NaN/빈값 처리)
    if final_cols:
        preview_df = df[final_cols].fillna('').replace('nan', '').head(10)
        preview_df.columns = new_col_names
        st.subheader("생기부 기초파일 미리보기 (상위 10명)")
        st.dataframe(preview_df, use_container_width=True, hide_index=True)

        # 엑셀 다운로드
        output = io.BytesIO()
        base_df = df[final_cols].fillna('')
        base_df.columns = new_col_names
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            base_df.to_excel(writer, index=False, sheet_name="생기부기초")
            workbook = writer.book
            worksheet = writer.sheets["생기부기초"]
            header_format = workbook.add_format({
                'bold': True, 'font_size': 12, 'align': 'center', 'valign': 'vcenter', 'border': 1, 'bg_color': '#D9E1F2'
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
        st.warning("최소 1개 이상의 항목을 추가해 주세요.")
else:
    st.info("CSV 파일을 업로드하면 항목을 추가/제거하며 생기부 기초파일을 만들 수 있습니다.")
