import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="세계의 수도 관광지도", layout="wide")

st.title("🌍 세계의 수도와 유명 관광지 지도")
st.write("세계 주요 수도를 클릭하면 대표 관광지의 이미지나 링크를 확인할 수 있어요!")

# 수도 + 명소 + 이미지/링크 데이터
capitals = [
    (
        "서울 (Seoul)", 37.5665, 126.9780,
        "경복궁",
        ""https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/Geunjeongjeon%2C_Gyeongbokgung_Palace.jpg/640px-Geunjeongjeon%2C_Gyeongbokgung_Palace.jpg"
    ),
    (
        "워싱턴 D.C. (Washington, D.C.)", 38.8951, -77.0364,
        "백악관",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9e/White_House_north_and_south_sides.jpg/800px-White_House_north_and_south_sides.jpg"
    ),
    (
        "도쿄 (Tokyo)", 35.6895, 139.6917,
        "도쿄타워",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/0/06/Tokyo_Tower_and_surrounding_buildings.jpg/800px-Tokyo_Tower_and_surrounding_buildings.jpg"
    ),
    (
        "베이징 (Beijing)", 39.9042, 116.4074,
        "자금성",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b7/Forbidden_City_Beijing_Shenwumen_Gate.JPG/800px-Forbidden_City_Beijing_Shenwumen_Gate.JPG"
    ),
    (
        "런던 (London)", 51.5074, -0.1278,
        "버킹엄 궁전",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/6/61/Buckingham_Palace_%282%29.jpg/800px-Buckingham_Palace_%282%29.jpg"
    ),
    (
        "파리 (Paris)", 48.8566, 2.3522,
        "에펠탑",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/a/af/Tour_Eiffel_Wikimedia_Commons.jpg/800px-Tour_Eiffel_Wikimedia_Commons.jpg"
    ),
    (
        "베를린 (Berlin)", 52.52, 13.405,
        "브란덴부르크 문",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Brandenburger_Tor_abends.jpg/800px-Brandenburger_Tor_abends.jpg"
    ),
    (
        "모스크바 (Moscow)", 55.7558, 37.6173,
        "크렘린",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/Moscow_Kremlin_and_Moskva_River.jpg/800px-Moscow_Kremlin_and_Moskva_River.jpg"
    ),
    (
        "오타와 (Ottawa)", 45.4215, -75.6999,
        "국회의사당",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2e/Parliament_Ottawa.jpg/800px-Parliament_Ottawa.jpg"
    ),
    (
        "캔버라 (Canberra)", -35.2809, 149.1300,
        "호주 국회의사당",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/8/88/Parliament_House_Canberra.jpg/800px-Parliament_House_Canberra.jpg"
    ),
    (
        "브라질리아 (Brasília)", -15.7939, -47.8828,
        "브라질 대성당",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5d/Catedral_Brasilia_Exterior.jpg/800px-Catedral_Brasilia_Exterior.jpg"
    ),
    (
        "뉴델리 (New Delhi)", 28.6139, 77.2090,
        "인디아 게이트",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/India_Gate_in_New_Delhi_03-2016_img3.jpg/800px-India_Gate_in_New_Delhi_03-2016_img3.jpg"
    ),
    (
        "자카르타 (Jakarta)", -6.2088, 106.8456,
        "모나스 타워",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/5/52/Monumen_Nasional_2018.jpg/800px-Monumen_Nasional_2018.jpg"
    ),
    (
        "마드리드 (Madrid)", 40.4168, -3.7038,
        "왕궁",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9b/Palacio_Real_Madrid_2016.jpg/800px-Palacio_Real_Madrid_2016.jpg"
    ),
    (
        "카이로 (Cairo)", 30.0444, 31.2357,
        "피라미드",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e3/Kheops-Pyramid.jpg/800px-Kheops-Pyramid.jpg"
    ),
]

# 지도 생성
m = folium.Map(location=[20, 0], zoom_start=2)

# 마커 추가
for name, lat, lon, attraction, img_url in capitals:
    html = f"""
    <b>{name}</b><br>
    관광지: {attraction}<br>
    <img src="{img_url}" width="200"><br>
    <a href="{img_url}" target="_blank">[이미지 원본 보기]</a>
    """
    popup = folium.Popup(folium.IFrame(html=html, width=220, height=280), max_width=300)
    folium.Marker([lat, lon], tooltip=name, popup=popup).add_to(m)

# Streamlit에 지도 표시
st_folium(m, width=1000, height=600)
