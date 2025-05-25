import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

# 파일 경로
school_path = "C:/Users/USER/Desktop/국민대과제/data/서울시 강남구 학교 기본정보.csv"
save_path = "C:/Users/USER/Desktop/국민대과제/data/초등학교_좌표포함.csv"

# 스트림릿 설정
st.set_page_config(layout="wide")
st.title("👮‍♀️ 아동안전지킴이 초등학교 순찰지도")

# CSV 읽기
try:
    df = pd.read_csv(school_path, encoding='cp949')
    st.success("✅ 학교 기본정보 불러오기 성공!")
except FileNotFoundError:
    st.error(f"❌ 파일을 찾을 수 없습니다: {school_path}")
    st.stop()

# 초등학교만 추출
elem_df = df[df['학교종류명'] == '초등학교'].copy()
st.write("📋 초등학교 목록", elem_df[['학교명', '도로명주소']].head())

# 지오코딩 설정
geolocator = Nominatim(user_agent="local_mapper")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

# 주소 → 위경도 변환
with st.spinner("📡 초등학교 주소를 위도/경도로 변환 중... (최초 1회만 수행)"):
    elem_df['location'] = elem_df['도로명주소'].apply(geocode)
    elem_df['위도'] = elem_df['location'].apply(lambda loc: loc.latitude if loc else None)
    elem_df['경도'] = elem_df['location'].apply(lambda loc: loc.longitude if loc else None)
    elem_df = elem_df.dropna(subset=['위도', '경도'])
    st.success("✅ 좌표 변환 완료!")

# 좌표 저장
elem_df.to_csv(save_path, index=False, encoding='utf-8-sig')
st.info(f"💾 변환된 데이터 저장 완료: {save_path}")

# 지도 만들기
center = [37.517236, 127.047325]
m = folium.Map(location=center, zoom_start=13)

# 마커 추가
for _, row in elem_df.iterrows():
    folium.Marker(
        location=[row['위도'], row['경도']],
        popup=row['학교명'],
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)

# 지도 보여주기
st.subheader("🗺️ 초등학교 지도 시각화")
st_folium(m, width=1000, height=600)
