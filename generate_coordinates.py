import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

# 주소만 있는 원본 파일
input_file = "C:/Users/USER/Desktop/국민대과제/data/초등학교_좌표포함.csv"
# 좌표 포함 저장 파일
output_file = "C:/Users/USER/Desktop/국민대과제/data/초등학교_좌표완성본.csv"

# 데이터 불러오기
df = pd.read_csv(input_file, encoding='utf-8')

# 지오코딩 준비
geolocator = Nominatim(user_agent="local_mapper")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

# 주소 → 위도/경도
df['location'] = df['도로명주소'].apply(geocode)
df['위도'] = df['location'].apply(lambda loc: loc.latitude if loc else None)
df['경도'] = df['location'].apply(lambda loc: loc.longitude if loc else None)
df = df.dropna(subset=['위도', '경도'])

# 저장
df.to_csv(output_file, index=False, encoding='utf-8-sig')
print(f"✅ 좌표 포함 파일 저장 완료: {output_file}")
