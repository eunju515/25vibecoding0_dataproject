import streamlit as st
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim

# 앱 제목
st.title("기관 위치 지도 표시 앱")
st.markdown("기관명을 입력하면 해당 위치를 지도에 표시해드려요! 🗺️")

# 사용자 입력 받기
place_name = st.text_input("기관명을 입력하세요:", "")

# 위치 탐색 및 지도 생성
if place_name:
    geolocator = Nominatim(user_agent="streamlit_app")
    location = geolocator.geocode(place_name)

    if location:
        # 지도 생성
        m = folium.Map(location=[location.latitude, location.longitude], zoom_start=15)
        folium.Marker([location.latitude, location.longitude], popup=place_name).add_to(m)

        # 지도 출력
        st.success(f"'{place_name}'의 위치를 찾았어요!")
        st_folium(m, width=700, height=500)
    else:
        st.error("위치를 찾을 수 없어요. 정확한 기관명을 입력해주세요.")

