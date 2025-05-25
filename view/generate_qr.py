# generate_qr.py
import pandas as pd
import qrcode
import os

# 입력 및 출력 경로
input_path = r"C:/Users/USER/Desktop/국민대과제/data/최적순찰경로.csv"
qr_output_dir = r"C:/Users/USER/Desktop/국민대과제/data/qrcodes"
os.makedirs(qr_output_dir, exist_ok=True)

# 체크인 주소 기본 URL (예시)
BASE_URL = "https://checkin.localhost/?place="

# 데이터 불러오기
df = pd.read_csv(input_path)
df = df[df['순서'] != 0]  # 출발지 제외

# 중복 제거: 조 + 장소 기준으로 한 번만 생성
unique_places = df[['조', '장소']].drop_duplicates()

for _, row in unique_places.iterrows():
    group = row['조']
    place = row['장소']
    label = f"{group}_{place}"
    url = BASE_URL + label.replace(" ", "%20")

    img = qrcode.make(url)
    file_path = os.path.join(qr_output_dir, f"{label}.png")
    img.save(file_path)
    print(f"✅ QR 저장됨: {file_path}")

print("🎯 QR 생성 완료!")
