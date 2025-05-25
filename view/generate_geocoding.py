import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

locations = [
    {"장소": "중동중학교", "주소": "서울특별시 강남구 일원로8길 37"},
    {"장소": "밀알학교", "주소": "서울특별시 강남구 일원본동 일원로 90"},
    {"장소": "개포동근린공원", "주소": "서울특별시 강남구 개포동 180"},
    {"장소": "개원중학교", "주소": "서울특별시 강남구 영동대로 101"},
    {"장소": "대진공원", "주소": "서울특별시 강남구 개포동 12"},
    {"장소": "마루공원", "주소": "서울특별시 강남구 개포동 18-35"},
    {"장소": "중동고등학교", "주소": "서울특별시 강남구 일원로 7"},
    {"장소": "일원에코파크", "주소": "서울특별시 강남구 일원동 4-12"},
    {"장소": "서울로봇고등학교", "주소": "서울특별시 강남구 광평로20길 63"},
]

geolocator = Nominatim(user_agent="local_mapper")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

results = []
for loc in locations:
    g = geocode(loc["주소"])
    results.append({
        "장소": loc["장소"],
        "주소": loc["주소"],
        "위도": g.latitude if g else None,
        "경도": g.longitude if g else None
    })

df = pd.DataFrame(results)
df.to_csv("C:/Users/USER/Desktop/국민대과제/data/순찰지_지오코딩.csv", index=False, encoding="utf-8-sig")
print("✅ 좌표 저장 완료: 순찰지_지오코딩.csv")
