import pandas as pd
from pyproj import Transformer

# 좌표계 변환기 설정 (ITRF2000 → WGS84)
transformer = Transformer.from_crs("EPSG:6677", "EPSG:4326", always_xy=True)

# 파일 경로
input_path = "C:/Users/USER/Desktop/국민대과제/data/서울시 녹지대 위치정보 (좌표계_ ITRF2000).csv"
output_path = "C:/Users/USER/Desktop/국민대과제/data/녹지대_WGS84.csv"

# CSV 읽기 (공백 포함된 열 이름 처리)
df = pd.read_csv(input_path, encoding="cp949")
df = df.rename(columns={"X 좌표": "X", "Y 좌표": "Y"})

# 위도/경도 계산
df[['경도', '위도']] = df.apply(lambda row: pd.Series(transformer.transform(row['X'], row['Y'])), axis=1)

# 필요한 컬럼만 저장
df[['녹지대명', '녹지대분류', '위도', '경도']].to_csv(output_path, index=False, encoding='utf-8-sig')

print("✅ 녹지대 좌표 변환 완료! →", output_path)

