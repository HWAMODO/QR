# patrol_map.py
import pandas as pd
import folium
import random
from folium.plugins import MarkerCluster

# 경로
input_path = r"C:/Users/USER/Desktop/국민대과제/data/최적순찰경로.csv"
output_html = r"C:/Users/USER/Desktop/국민대과제/data/순찰경로_지도.html"

# 데이터 불러오기
df = pd.read_csv(input_path)

# 지도 중심
center = [df['위도'].mean(), df['경도'].mean()]
m = folium.Map(location=center, zoom_start=14)

# 조별 색상 지정
color_pool = ["red", "blue", "green", "purple", "orange", "cadetblue", "black"]
group_colors = {name: color_pool[i % len(color_pool)] for i, name in enumerate(df['조'].unique())}

# 조별로 순찰 경로 시각화
for name, group in df.groupby('조'):
    group = group.sort_values('순서')
    coords = list(zip(group['위도'], group['경도']))
    color = group_colors[name]

    # 경로선
    folium.PolyLine(coords, color=color, weight=4, opacity=0.8).add_to(m)

    # 마커
    for _, row in group.iterrows():
        folium.Marker(
            location=(row['위도'], row['경도']),
            popup=f"{row['조']} - {row['장소']} ({row['순서']})",
            icon=folium.Icon(color=color)
        ).add_to(m)

# 지도 저장
m.save(output_html)
print(f"🗺️ 지도 저장 완료: {output_html}")
