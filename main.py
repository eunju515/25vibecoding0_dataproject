import streamlit as st
import folium
from streamlit_folium import st_folium

# 페이지 제목
st.title("🌍 세계의 수도 위치 지도")
st.write("아래 지도에는 세계 주요 수도들이 표시되어 있습니다.")

# 예시: 세계 주요 수도들 (도시명, 위도, 경도)
capitals = [
    ("서울 (Seoul)", 37.5665, 126.9780),
    ("워싱턴 D.C. (Washington, D.C.)", 38.8951, -77.0364),
    ("도쿄 (Tokyo)", 35.6895, 139.6917),
    ("베이징 (Beijing)", 39.9042, 116.4074),
    ("런던 (London)", 51.5074, -0.1278),
    ("파리 (Paris)", 48.8566, 2.3522),
    ("베를린 (Berlin)", 52.52, 13.405),
    ("모스크바 (Moscow)", 55.7558, 37.6173),
    ("오타와 (Ottawa)", 45.4215, -75.6999),
    ("캔버라 (Canberra)", -35.2809, 149.1300),
    ("브라질리아 (Brasília)", -15.7939, -47.8828),
    ("뉴델리 (New Delhi)", 28.6139, 77.2090),
    ("자카르타 (Jakarta)", -6.2088, 106.8456),
    ("마드리드 (Madrid)", 40.4168, -3.7038),
    ("카이로 (Cairo)", 30.0444, 31.2357),
]

# 지도 생성 (중심: 서울)
m = folium.Map(location=[20, 0], zoom_start=2)

# 수도들 지도에 추가
for name, lat, lon in capitals:
    folium.Marker([lat, lon], tooltip=name).add_to(m)

# Streamlit에 지도 표시
st_folium(m, width=800, height=500)
