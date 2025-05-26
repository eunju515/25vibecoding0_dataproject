import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from io import BytesIO

# 지도용 위도/경도 간단 매핑 (예시용, 실제 좌표 필요시 더 보완 가능)
gyeonggi_coords = {
    "수원시": (37.2636, 127.0286),
    "성남시": (37.4202, 127.1265),
    "용인시": (37.2411, 127.1776),
    "고양시": (37.6584, 126.8320),
    "화성시": (37.1995, 126.8310),
    "부천시": (37.5034, 126.7660),
    "남양주시": (37.6360, 127.2165),
    "안산시": (37.3219, 126.8309),
    "안양시": (37.3943, 126.9568),
    "평택시": (36.9946, 127.0880),
    # 필요시 추가
}

@st.cache_data
def load_data():
    df_gender = pd.read_csv("202504_202504_연령별인구현황_월간(남여구분).csv", encoding='cp949')
    df_total = pd.read_csv("202504_202504_연령별인구현황_월간(남여합계).csv", encoding='cp949')

    df_gender['시도'] = df_gender['행정구역'].str.extract(r'^([\w\s]+?[시도])')
    df_gender['시군구'] = df_gender['행정구역'].str.extract(r'^[\w\s]+?[시도]\s([\w\s]+[군구시])')

    return df_gender, df_total

df_gender, df_total = load_data()

st.title("📍 경기도 인구 통계 시각화")

# ✅ 경기도만 필터링
df_gg_gender = df_gender[df_gender['시도'] == '경기도']
df_gg_total = df_total[df_total['행정구역'].str.startswith('경기도')]

# 시군구 선택
available_sigungu = sorted(df_gg_gender['시군구'].dropna().unique().tolist())
selected_sigungu = st.selectbox("경기도 시/군/구 선택", available_sigungu)

# 연령 구간 선택
age_ranges = {
    '전체 연령': list(range(0, 101)) + ['100세 이상'],
    '0~19세': list(range(0, 20)),
    '20~64세': list(range(20, 65)),
    '65세 이상': list(range(65, 101)) + ['100세 이상'],
}
age_range_label = st.radio("연령대 선택", list(age_ranges.keys()), horizontal=True)
selected_ages = age_ranges[age_range_label]

def age_label(age): return f"{age}세" if isinstance(age, int) else age
age_labels = [age_label(age) for age in selected_ages]

# 컬럼
male_cols = [f'2025년04월_남_{age}' for age in age_labels]
female_cols = [f'2025년04월_여_{age}' for age in age_labels]
total_cols = [f'2025년04월_계_{age}' for age in age_labels]

gu_name = f"경기도 {selected_sigungu}".strip()

row_gender = df_gg_gender[df_gg_gender['행정구역'].str.strip() == gu_name].iloc[0]
row_total = df_gg_total[df_gg_total['행정구역'].str.strip() == gu_name].iloc[0]

def parse_num(x): return int(str(x).replace(",", "")) if pd.notna(x) else 0

male_pop = [-parse_num(row_gender.get(col, 0)) for col in male_cols]
female_pop = [parse_num(row_gender.get(col, 0)) for col in female_cols]
total_pop = [parse_num(row_total.get(col, 0)) for col in total_cols]

total_male = sum(abs(m) for m in male_pop)
total_female = sum(female_pop)
sex_ratio = total_female / total_male if total_male else 0

# 📊 인구 피라미드
fig_pyramid = go.Figure()
fig_pyramid.add_trace(go.Bar(y=age_labels, x=male_pop, name='남성', orientation='h', marker_color='blue'))
fig_pyramid.add_trace(go.Bar(y=age_labels, x=female_pop, name='여성', orientation='h', marker_color='red'))
fig_pyramid.update_layout(
    title=f"{gu_name} 인구 피라미드",
    barmode='relative',
    xaxis_title='인구 수',
    yaxis_title='연령',
    height=700
)

# 📈 총인구 그래프
df_bar = pd.DataFrame({'연령': age_labels, '총인구': total_pop})
fig_total = px.bar(df_bar, x='총인구', y='연령', orientation='h', height=700, title=f"{gu_name} 연령별 총인구")

# 🗺️ 지도 시각화
st.subheader("📍 지도 기반 위치")
lat, lon = gyeonggi_coords.get(selected_sigungu, (37.4, 127.0))
map_df = pd.DataFrame({
    '시군구': [selected_sigungu],
    '인구수': [sum(total_pop)],
    'lat': [lat],
    'lon': [lon]
})
fig_map = px.scatter_mapbox(
    map_df,
    lat='lat',
    lon='lon',
    size='인구수',
    hover_name='시군구',
    zoom=9,
    mapbox_style='open-street-map',
    title=f"{selected_sigungu} 위치 및 인구 규모"
)

# 시각화 출력
st.plotly_chart(fig_map, use_container_width=True)
st.plotly_chart(fig_pyramid, use_container_width=True)
st.markdown(f"🔸 성비 (여성 / 남성): **{sex_ratio:.2f} : 1**")
st.plotly_chart(fig_total, use_container_width=True)

# 📥 그래프 저장
st.subheader("📥 그래프 저장")
selected_chart = st.radio("저장할 그래프", ["인구 피라미드", "총인구 그래프"])

if st.button("📥 다운로드"):
    buffer = BytesIO()
    if selected_chart == "인구 피라미드":
        fig_pyramid.write_image(buffer, format="png")
        st.download_button("인구 피라미드 저장", buffer.getvalue(), file_name="pyramid.png", mime="image/png")
    else:
        fig_total.write_image(buffer, format="png")
        st.download_button("총인구 그래프 저장", buffer.getvalue(), file_name="total.png", mime="image/png")
