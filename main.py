import streamlit as st

import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="세계의 수도 관광지도", layout="wide")
st.title("🌍 세계의 수도와 유명 관광지 지도")
st.write("세계 주요 수도를 클릭하면 대표 관광지의 이미지와 링크를 확인할 수 있어요!")

# 수도 + 명소 + 이미지 (위키미디어의 CORS-허용된 이미지 사용)
capitals = [
    (
        "서울 (Seoul)", 37.5665, 126.9780, "경복궁",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/Geunjeongjeon%2C_Gyeongbokgung_Palace.jpg/640px-Geunjeongjeon%2C_Gyeongbokgung_Palace.jpg"
    ),
    (
        "워싱턴 D.C.", 38.8951, -77.0364, "백악관",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fd/White_House_north_side.jpg/640px-White_House_north_side.jpg"
    ),
    (
        "도쿄 (Tokyo)", 35.6895, 139.6917, "도쿄타워",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2e/Tokyo_Tower_and_zojoji.jpg/640px-Tokyo_Tower_and_zojoji.jpg"
    ),
    (
        "베이징 (Beijing)", 39.9042, 116.4074, "자금성",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/7/78/Forbidden_City_Beijing_Shenwumen_Gate.jpg/640px-Forbidden_City_Beijing_Shenwumen_Gate.jpg"
    ),
    (
        "런던 (London)", 51.5074, -0.1278, "버킹엄 궁전",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/8/84/Buckingham_Palace_from_gardens%2C_London%2C_UK_-_Diliff.jpg/640px-Buckingham_Palace_from_gardens%2C_London%2C_UK_-_Diliff.jpg"
    ),
    (
        "파리 (Paris)", 48.8566, 2.3522, "에펠탑",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a8/Tour_Eiffel_Wikimedia_Commons.jpg/640px-Tour_Eiffel_Wikimedia_Commons.jpg"
    ),
    (
        "베를린 (Berlin)", 52.52, 13.405, "브란덴부르크 문",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/4/44/Brandenburger_Tor_abends.jpg/640px-Brandenburger_Tor_abends.jpg"
    ),
    (
        "모스크바 (Moscow)", 55.7558, 37.6173, "크렘린",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Kremlin_Moscow.jpg/640px-Kremlin_Moscow.jpg"
    ),
    (
        "오타와 (Ottawa)", 45.4215, -75.6999, "국회의사당",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/5/54/Ottawa-Parliament.jpg/640px-Ottawa-Parliament.jpg"
    ),
    (
        "캔버라 (Canberra)", -35.2809, 149.1300, "호주 국회의사당",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2e/Parliament_House_Canberra.jpg/640px-Parliament_House_Canberra.jpg"
    ),
    (
        "브라질리아 (Brasília)", -15.7939, -47.8828, "브라질 대성당",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/Brasilia_cathedral_roof.jpg/640px-Brasilia_cathedral_roof.jpg"
    ),
    (
        "뉴델리 (New Delhi)", 28.6139, 77.2090, "인디아 게이트",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/India_Gate_in_New_Delhi_03-2016_img3.jpg/640px-India_Gate_in_New_Delhi_03-2016_img3.jpg"
    ),
    (
        "자카르타 (Jakarta)", -6.2088, 106.8456, "모나스 타워",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6a/Monas_Jakarta.jpg/640px-Monas_Jakarta.jpg"
    ),
    (
        "마드리드 (Madrid)", 40.4168, -3.7038, "왕궁",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9b/Palacio_Real_Madrid_2016.jpg/640px-Palacio_Real_Madrid_2016.jpg"
    ),
    (
        "카이로 (Cairo)", 30.0444, 31.2357, "기자 피라미드",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e3/Kheops-Pyramid.jpg/640px-Kheops-Pyramid.jpg"
    ),
]

# 지도 생성
m = folium.Map(location=[20, 0], zoom_start=2)

# 마커 및 팝업 생성
for name, lat, lon, attraction, img_url in capitals:
    html = f"""
    <b>{name}</b><br>
    관광지: {attraction}<br>
    <img src="{img_url}" width="200" onerror="this.src='https://via.placeholder.com/200x150?text=No+Image';"><br>
    <a href="{img_url}" target="_blank">[이미지 원본 보기]</a>
    """
    popup = folium.Popup(folium.IFrame(html=html, width=220, height=280), max_width=300)
    folium.Marker([lat, lon], tooltip=name, popup=popup).add_to(m)

# Streamlit에 지도 표시
st_folium(m, width=1000, height=600)
