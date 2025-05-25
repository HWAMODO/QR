import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium

# CSV 경로 (좌표 포함된 버전!)
file_path = "C:/Users/USER/Desktop/국민대과제/data/초등학교_좌표완성본.csv"

# Streamlit 설정
st.set_page_config(layout="wide")
st.title("🚸 초등학교 순찰지도 (최적화 버전)")

# CSV 로딩
try:
    df = pd.read_csv(file_path, encoding='utf-8')
    st.success(f"✅ 초등학교 {len(df)}개 로드 완료!")
except FileNotFoundError:
    st.error(f"❌ 파일이 존재하지 않습니다: {file_path}")
    st.stop()

# 지도 중심: 전체 평균
center = [df['위도'].mean(), df['경도'].mean()]
m = folium.Map(location=center, zoom_start=13)

# 마커 클러스터 추가
cluster = MarkerCluster().add_to(m)

for _, row in df.iterrows():
    folium.Marker(
        location=[row['위도'], row['경도']],
        popup=row['학교명'],
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(cluster)

# 지도 출력
st.subheader("🗺️ 초등학교 위치 시각화")
st_folium(m, width=1200, height=800)

# 테이블 출력
st.subheader("📋 초등학교 전체 목록")
st.dataframe(df[['학교명', '도로명주소', '위도', '경도']])
