import pandas as pd
import qrcode
import os

# 파일 경로
INPUT_CSV = "C:/Users/USER/Desktop/국민대과제/view/초등학교_좌표포함.csv"
OUTPUT_FOLDER = "data/qrcodes"
BASE_URL = "https://so8jj7x5vbt7rxbp4jgbpm.streamlit.app/?school="


# 폴더 없으면 생성
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# CSV 로딩
df = pd.read_csv(INPUT_CSV)
df.columns = df.columns.str.strip()

# 학교명 리스트에서 중복 제거
school_names = df["학교명"].dropna().unique()

# QR 생성
for school in school_names:
    url = f"{BASE_URL}{school}"
    img = qrcode.make(url)
    filename = f"{school}_QR.png"
    img.save(os.path.join(OUTPUT_FOLDER, filename))

print("🎉 모든 QR코드 생성 완료!")

