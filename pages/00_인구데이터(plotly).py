import streamlit as st
import pandas as pd
import plotly.graph_objects as go

@st.cache_data
def load_data():
    df = pd.read_csv("202504_202504_연령별인구현황_월간(남여구분).csv", encoding='cp949')
    return df

df = load_data()

# 구 리스트 추출
gu_list = df[df['행정구역'].str.contains('서울특별시 ') & (df['행정구역'].str.len() <= 25)]
gu_names = gu_list['행정구역'].str.extract(r'(서울특별시\s[\w\d]+구)')[0].dropna().unique()

st.title("서울특별시 연령별 인구 피라미드 (2025년 4월)")

selected_gu = st.selectbox("구 선택", options=gu_names)

# 연령대 정의
age_ranges = {
    '전체 연령': list(range(0, 101)) + ['100세 이상'],
    '0~19세': list(range(0, 20)),
    '20~64세': list(range(20, 65)),
    '65세 이상': list(range(65, 101)) + ['100세 이상'],
}
age_range_label = st.radio("연령대 범위 선택", list(age_ranges.keys()), horizontal=True)
selected_ages = age_ranges[age_range_label]

# 연령 텍스트 라벨 생성
def age_label(age):
    return f"{age}세" if isinstance(age, int) else age

age_labels = [age_label(age) for age in selected_ages]
male_cols = [f'2025년04월_남_{label}' for label in age_labels]
female_cols = [f'2025년04월_여_{label}' for label in age_labels]

# 선택된 구 데이터
selected_row = df[df['행정구역'].str.contains(selected_gu)].iloc[0]

def parse_num(x):
    try:
        return int(str(x).replace(",", ""))
    except:
        return 0

# KeyError 방지를 위해 get 사용
male_population = [-parse_num(selected_row.get(col, 0)) for col in male_cols]
female_population = [parse_num(selected_row.get(col, 0)) for col in female_cols]

# 그래프 생성
fig = go.Figure()
fig.add_trace(go.Bar(y=age_labels, x=male_population, name='남성', orientation='h', marker_color='blue'))
fig.add_trace(go.Bar(y=age_labels, x=female_population, name='여성', orientation='h', marker_color='red'))

fig.update_layout(
    title=f'{selected_gu} 연령별 인구 피라미드',
    barmode='relative',
    xaxis=dict(title='인구 수', tickformat=',d'),
    yaxis=dict(title='연령'),
    bargap=0.1,
    height=800
)

st.plotly_chart(fig, use_container_width=True)
