# streamlit_app.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import pydeck as pdk

# 데이터 로드
@st.cache_data
def load_data():
    df_gender = pd.read_csv("202504_202504_연령별인구현황_월간(남여구분).csv", encoding="cp949")
    df_total = pd.read_csv("202504_202504_연령별인구현황_월간(남여합계).csv", encoding="cp949")
    return df_gender, df_total

df_gender, df_total = load_data()

# 경기도만 필터링
df_gender = df_gender[df_gender['행정구역'].str.startswith("경기도")]
df_total = df_total[df_total['행정구역'].str.startswith("경기도")]

# 시군구 추출
df_gender['시군구'] = df_gender['행정구역'].str.replace("경기도", "").str.strip()
df_total['시군구'] = df_total['행정구역'].str.replace("경기도", "").str.strip()

# 사용자 선택
selected_sigungu = st.selectbox("시/군/구 선택", df_gender['시군구'].unique())

# 연령대 범위 선택
age_groups = {
    "전체": list(range(0, 101)),
    "0-19세": list(range(0, 20)),
    "20-64세": list(range(20, 65)),
    "65세 이상": list(range(65, 101))
}
selected_group = st.selectbox("연령대 범위 선택", age_groups.keys())
age_range = age_groups[selected_group]

# 열 이름 생성
male_cols = [f"2025년04월_남_{age}세" if age < 100 else "2025년04월_남_100세 이상" for age in age_range]
female_cols = [f"2025년04월_여_{age}세" if age < 100 else "2025년04월_여_100세 이상" for age in age_range]
total_cols = [f"2025년04월_계_{age}세" if age < 100 else "2025년04월_계_100세 이상" for age in age_range]

# 숫자 파싱 함수
def parse_num(val):
    try:
        return int(str(val).replace(",", ""))
    except:
        return 0

# 해당 시군구 데이터 추출
gu_name = f"경기도 {selected_sigungu}"
row_gender = df_gender[df_gender['행정구역'].str.strip() == gu_name]
row_total = df_total[df_total['행정구역'].str.strip() == gu_name]

# 오류 방지 처리
if row_gender.empty or row_total.empty:
    st.error(f"{gu_name} 지역 데이터가 없습니다.")
    st.stop()

row_gender = row_gender.iloc[0]
row_total = row_total.iloc[0]

# 시각화용 데이터 추출
male_pop = [-parse_num(row_gender[col]) if col in row_gender else 0 for col in male_cols]
female_pop = [parse_num(row_gender[col]) if col in row_gender else 0 for col in female_cols]
total_pop = [parse_num(row_total[col]) if col in row_total else 0 for col in total_cols]
ages = [f"{age}세" if age < 100 else "100세 이상" for age in age_range]

# 성비 비율 계산
male_sum = -sum(male_pop)
female_sum = sum(female_pop)
if female_sum > 0:
    ratio = round(male_sum / female_sum * 100, 2)
else:
    ratio = 0

# 인구 피라미드 시각화
fig = go.Figure()
fig.add_trace(go.Bar(y=ages, x=male_pop, name='남성', orientation='h', marker_color='blue'))
fig.add_trace(go.Bar(y=ages, x=female_pop, name='여성', orientation='h', marker_color='red'))

fig.update_layout(
    title=f"{selected_sigungu} 인구 피라미드 ({selected_group}) - 남성:여성 = {ratio}:100",
    barmode='relative',
    xaxis_title="인구수",
    yaxis_title="연령대",
    template="plotly_white"
)

st.plotly_chart(fig)

# 총 인구 막대그래프
bar_fig = go.Figure()
bar_fig.add_trace(go.Bar(x=ages, y=total_pop, marker_color='green'))
bar_fig.update_layout(title=f"{selected_sigungu} 총 인구 분포", xaxis_title="연령대", yaxis_title="인구수")
st.plotly_chart(bar_fig)

# 저장 기능
if st.button("시각화 저장"):
    fig.write_image("인구피라미드.png")
    bar_fig.write_image("총인구분포.png")
    st.success("시각화 이미지 저장 완료!")

# 지도 기반 시각화 (중심은 수원시청)
st.subheader("경기도 중심 지도 시각화")
st.pydeck_chart(pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state=pdk.ViewState(
        latitude=37.2636,
        longitude=127.0286,
        zoom=8,
        pitch=50,
    ),
    layers=[
        pdk.Layer(
            "HexagonLayer",
            data=pd.DataFrame({'lat': [37.2636], 'lon': [127.0286]}),
            get_position='[lon, lat]',
            radius=10000,
            elevation_scale=50,
            elevation_range=[0, 1000],
            pickable=True,
            extruded=True,
        ),
    ],
))
