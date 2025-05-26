import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from io import BytesIO

# 데이터 불러오기
@st.cache_data
def load_data():
    df_gender = pd.read_csv("202504_202504_연령별인구현황_월간(남여구분).csv", encoding='cp949')
    df_total = pd.read_csv("202504_202504_연령별인구현황_월간(남여합계).csv", encoding='cp949')
    return df_gender, df_total

df_gender, df_total = load_data()

# 시도/시군구 분리
df_gender['시도'] = df_gender['행정구역'].str.extract(r'^([\w\s]+?[시도])')
df_gender['시군구'] = df_gender['행정구역'].str.extract(r'^[\w\s]+?[시도]\s([\w\s]+[시군구])')

# 시도 선택
st.title("대한민국 연령별 인구 시각화 (2025년 4월)")
selected_sido = st.selectbox("시/도 선택", df_gender['시도'].dropna().unique())

# 시군구 선택
filtered_df = df_gender[df_gender['시도'] == selected_sido]
selected_sigungu = st.selectbox("시/군/구 선택", filtered_df['시군구'].dropna().unique())

# 연령대 필터
age_ranges = {
    '전체 연령': list(range(0, 101)) + ['100세 이상'],
    '0~19세': list(range(0, 20)),
    '20~64세': list(range(20, 65)),
    '65세 이상': list(range(65, 101)) + ['100세 이상'],
}
age_range_label = st.radio("연령대 범위 선택", list(age_ranges.keys()), horizontal=True)
selected_ages = age_ranges[age_range_label]

def age_label(age):
    return f"{age}세" if isinstance(age, int) else age
age_labels = [age_label(age) for age in selected_ages]

# 컬럼명
male_cols = [f'2025년04월_남_{age}' for age in age_labels]
female_cols = [f'2025년04월_여_{age}' for age in age_labels]
total_cols = [f'2025년04월_계_{age}' for age in age_labels]

def parse_num(x):
    try:
        return int(str(x).replace(",", ""))
    except:
        return 0

# 행정구역명 매칭
gu_name = f"{selected_sido} {selected_sigungu}".strip()

gender_match = df_gender[df_gender['행정구역'].str.strip() == gu_name]
total_match = df_total[df_total['행정구역'].str.strip() == gu_name]

if gender_match.empty or total_match.empty:
    st.error(f"⚠️ '{gu_name}'에 대한 데이터를 찾을 수 없습니다. 다른 지역을 선택해 주세요.")
    st.stop()

row_gender = gender_match.iloc[0]
row_total = total_match.iloc[0]

# 데이터 추출
male_pop = [-parse_num(row_gender.get(col, 0)) for col in male_cols]
female_pop = [parse_num(row_gender.get(col, 0)) for col in female_cols]
total_pop = [parse_num(row_total.get(col, 0)) for col in total_cols]

# 📊 인구 피라미드
fig_pyramid = go.Figure()
fig_pyramid.add_trace(go.Bar(y=age_labels, x=male_pop, name='남성', orientation='h', marker_color='blue'))
fig_pyramid.add_trace(go.Bar(y=age_labels, x=female_pop, name='여성', orientation='h', marker_color='red'))
fig_pyramid.update_layout(
    title=f"{gu_name} 인구 피라미드",
    barmode='relative',
    xaxis=dict(title='인구 수', tickformat=',d'),
    yaxis=dict(title='연령'),
    height=800
)

# 📊 총인구 그래프
df_bar = pd.DataFrame({'연령': age_labels, '총인구': total_pop})
fig_total = px.bar(
    df_bar,
    x='총인구',
    y='연령',
    orientation='h',
    title=f"{gu_name} 연령별 총인구",
    height=800,
    color='총인구',
    color_continuous_scale='Blues'
)

# 📈 성비 계산
total_male = sum(abs(m) for m in male_pop)
total_female = sum(female_pop)
sex_ratio = total_female / total_male if total_male else 0

st.subheader("1. 연령별 인구 피라미드")
st.plotly_chart(fig_pyramid, use_container_width=True)
st.markdown(f"🔹 **성비 (여성 / 남성)** : {sex_ratio:.2f} : 1")

st.subheader("2. 연령별 총인구 그래프")
st.plotly_chart(fig_total, use_container_width=True)

# 📥 시각화 저장
st.subheader("3. 시각화 저장")
selected_chart = st.radio("저장할 그래프 선택", ["인구 피라미드", "총인구 그래프"])

if st.button("📥 그래프 이미지 저장 (PNG)"):
    buffer = BytesIO()
    if selected_chart == "인구 피라미드":
        fig_pyramid.write_image(buffer, format='png')
        st.download_button("📥 인구 피라미드 다운로드", data=buffer.getvalue(), file_name="population_pyramid.png", mime="image/png")
    else:
        fig_total.write_image(buffer, format='png')
        st.download_button("📥 총인구 그래프 다운로드", data=buffer.getvalue(), file_name="total_population.png", mime="image/png")
