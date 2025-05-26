import streamlit as st
import folium
from streamlit_folium import st_folium

# 페이지 제목
st.title("🌍 세계의 수도와 유명 관광지 지도")
st.write("세계 주요 수도를 클릭하면 해당 도시의 대표 관광지를 볼 수 있어요!")

# 수도 + 대표 관광명소 데이터 (도시명, 위도, 경도, 관광명소)
capitals = [
    ("서울 (Seoul)", 37.5665, 126.9780, "경복궁, 남산타워"),
    ("워싱턴 D.C. (Washington, D.C.)", 38.8951, -77.0364, "백악관, 국회의사당"),
    ("도쿄 (Tokyo)", 35.6895, 139.6917, "도쿄타워, 아사쿠사 신사"),
    ("베이징 (Beijing)", 39.9042, 116.4074, "자금성, 만리장성"),
    ("런던 (London)", 51.5074, -0.1278, "버킹엄 궁전, 런던 아이"),
    ("파리 (Paris)", 48.8566, 2.3522, "에펠탑, 루브르 박물관"),
    ("베를린 (Berlin)", 52.52, 13.405, "브란덴부르크 문, 베를린 장벽"),
    ("모스크바 (Moscow)", 55.7558, 37.6173, "크렘린, 붉은 광장"),
    ("오타와 (Ottawa)", 45.4215, -75.6999, "국회의사당, 리도 운하"),
    ("캔버라 (Canberra)", -35.2809, 149.1300, "호주 국회의사당, 워민가 국립공원"),
    ("브라질리아 (Brasília)", -15.7939, -47.8828, "브라질 국회의사당, 대성당"),
    ("뉴델리 (New Delhi)", 28.6139, 77.2090, "인디아게이트, 붉은 요새"),
    ("자카르타 (Jakarta)", -6.2088, 106.8456, "모나스 타워, 따만 미니 인도네시아"),
    ("마드리드 (Madrid)", 40.4168, -3.7038, "프라도 미술관, 왕궁"),
    ("카이로 (Cairo)", 30.0444, 31.2357, "피라미드, 이집트 박물관"),
]

# folium 지도 생성 (중심: 지구 중심 근처)
m = folium.Map(location=[20, 0], zoom_start=2)

# 마커에 popup 추가하여 관광명소 정보 제공
for name, lat, lon, attraction in capitals:
    popup_text = f"<b>{name}</b><br>유명 관광지: {attraction}"
    folium.Marker(
        [lat, lon],
        tooltip=name,
        popup=folium.Popup(popup_text, max_width=250)
    ).add_to(m)

# Streamlit에 folium 지도 표시
st_folium(m, width=800, height=500)
