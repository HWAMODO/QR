import pandas as pd
import folium
from folium.plugins import MarkerCluster

# 좌표 포함된 파일 경로
file_path = "C:/Users/USER/Desktop/국민대과제/data/초등학교_좌표완성본.csv"

# CSV 불러오기
df = pd.read_csv(file_path, encoding='utf-8')

# 데이터 확인
print(f"학교 수: {len(df)}")
print(df[['학교명', '위도', '경도']].head())

# 지도 중심 좌표 계산
center = [df['위도'].mean(), df['경도'].mean()]
m = folium.Map(location=center, zoom_start=13)

# 마커 클러스터링
cluster = MarkerCluster().add_to(m)

# 마커 추가
for _, row in df.iterrows():
    folium.Marker(
        location=[row['위도'], row['경도']],
        popup=row['학교명'],
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(cluster)

# 지도 저장
save_path = "C:/Users/USER/Desktop/국민대과제/data/초등학교_테스트지도.html"
m.save(save_path)
print(f"✅ 지도 저장 완료: {save_path}")
