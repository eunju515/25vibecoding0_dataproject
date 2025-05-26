import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# 데이터 불러오기 함수
@st.cache_data
def load_data():
    df_gender = pd.read_csv("202504_202504_연령별인구현황_월간(남여구분).csv", encoding='cp949')
    df_total = pd.read_csv("202504_202504_연령별인구현황_월간(남여합계).csv", encoding='cp949')
    return df_gender, df_total

df_gender, df_total = load_data()

# 구 리스트 추출
gu_names = df_gender[df_gender['행정구역'].str.contains('서울특별시 ') & (df_gender['행정구역'].str.len() <= 25)]['행정구역'] \
    .str.extract(r'(서울특별시\s[\w\d]+구)')[0].dropna().unique()

# UI
st.title("서울시 연령별 인구 통합 시각화 (2025년 4월)")
selected_gu = st.selectbox("구 선택", options=gu_names)

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

# 컬럼명 생성
male_cols = [f'2025년04월_남_{age}' for age in age_labels]
female_cols = [f'2025년04월_여_{age}' for age in age_labels]
total_cols = [f'2025년04월_계_{age}' for age in age_labels]

# 숫자 파싱 함수
def parse_num(x):
    try:
        return int(str(x).replace(",", ""))
    except:
        return 0

# 남녀구분 데이터 추출
row_gender = df_gender[df_gender['행정구역'].str.contains(selected_gu)].iloc[0]
male_pop = [-parse_num(row_gender.get(col, 0)) for col in male_cols]
female_pop = [parse_num(row_gender.get(col, 0)) for col in female_cols]

# 총인구 데이터 추출
row_total = df_total[df_total['행정구역'].str.contains(selected_gu)].iloc[0]
total_pop = [parse_num(row_total.get(col, 0)) for col in total_cols]

# 📊 인구 피라미드 (남/여)
fig_pyramid = go.Figure()
fig_pyramid.add_trace(go.Bar(y=age_labels, x=male_pop, name='남성', orientation='h', marker_color='blue'))
fig_pyramid.add_trace(go.Bar(y=age_labels, x=female_pop, name='여성', orientation='h', marker_color='red'))

fig_pyramid.update_layout(
    title=f"{selected_gu} 인구 피라미드",
    barmode='relative',
    xaxis=dict(title='인구 수', tickformat=',d'),
    yaxis=dict(title='연령'),
    height=800,
)

# 📊 총인구 막대 그래프
df_bar = pd.DataFrame({'연령': age_labels, '총인구': total_pop})
fig_total = px.bar(
    df_bar,
    x='총인구',
    y='연령',
    orientation='h',
    title=f"{selected_gu} 연령별 총인구",
    height=800,
    color='총인구',
    color_continuous_scale='Blues'
)

# 📈 시각화 출력
st.subheader("1. 연령별 인구 피라미드 (남/여)")
st.plotly_chart(fig_pyramid, use_container_width=True)

st.subheader("2. 연령별 총인구 그래프 (남+여 합계)")
st.plotly_chart(fig_total, use_container_width=True)
