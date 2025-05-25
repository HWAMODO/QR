# patrol_map_curated.py
import pandas as pd
import folium

# 경로 데이터 불러오기
df = pd.read_csv("C:/Users/USER/Desktop/국민대과제/data/최적_조별_순찰경로.csv", encoding="utf-8-sig")

# 조별 색상 설정
colors = ["red", "blue", "green", "purple", "orange", "black", "cadetblue"]
m = folium.Map(location=[df['위도'].mean(), df['경도'].mean()], zoom_start=14)

for i, group in enumerate(df['조'].unique()):
    gdf = df[df['조'] == group].sort_values(by='순번')
    coords = gdf[['위도', '경도']].values.tolist()

    # 경로선
    folium.PolyLine(coords, color=colors[i % len(colors)], weight=5, opacity=0.8).add_to(m)

    # 마커
    for _, row in gdf.iterrows():
        folium.Marker(
            location=[row['위도'], row['경도']],
            popup=f"{row['조']} - {row['장소']} ({row['순번']})",
            icon=folium.Icon(color=colors[i % len(colors)], icon="info-sign")
        ).add_to(m)

# 지도 저장
m.save("C:/Users/USER/Desktop/국민대과제/data/조별_순찰경로_지도.html")
print("🗺️ 지도 저장 완료: 조별_순찰경로_지도.html")
