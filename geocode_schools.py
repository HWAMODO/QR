import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

# 파일 경로
input_path = r"C:/Users/USER/Desktop/국민대과제/data/서울시 강남구 학교 기본정보.csv"
output_path = r"C:/Users/USER/Desktop/국민대과제/data/학교_지오코딩완료.csv"

# 주소 불러오기
df = pd.read_csv(input_path, encoding='cp949')
df = df[df['학교종류명'].isin(['중학교', '고등학교'])]
df = df[['학교명', '학교종류명', '도로명주소']].dropna()

# 지오코더 설정
geolocator = Nominatim(user_agent="school_mapper")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

# 주소 → 좌표 변환
def get_coords(addr):
    location = geocode(addr)
    if location:
        return pd.Series([location.latitude, location.longitude])
    return pd.Series([None, None])

print("📡 지오코딩 시작...")
df[['위도', '경도']] = df['도로명주소'].apply(get_coords)
print("✅ 변환 완료")

# 저장
df.to_csv(output_path, index=False, encoding='utf-8-sig')
print(f"💾 저장 완료: {output_path}")
