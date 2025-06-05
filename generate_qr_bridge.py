import os
import qrcode

# 1. 설정
HTML_FOLDER = "C:/Users/USER/Desktop/국민대과제/html_pages"
OUTPUT_FOLDER = "C:/Users/USER/Desktop/국민대과제/data/qr2"

# ✅ school 파라미터에서 .html 제거
BRIDGE_BASE = "https://qr--main--hwamodo.streamlit.app/view/checkin_form.py?school="

# 2. 출력 폴더 준비
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# 3. html_pages 폴더 내 .html 파일 불러오기
html_files = [f for f in os.listdir(HTML_FOLDER) if f.endswith(".html")]

# 4. QR 생성
for filename in html_files:
    school_name = os.path.splitext(filename)[0]  # 확장자 제거
    qr_url = f"{BRIDGE_BASE}{school_name}"       # ✅ .html 제거된 school_name만 사용

    img = qrcode.make(qr_url)
    save_path = os.path.join(OUTPUT_FOLDER, f"{school_name}_QR.png")
    img.save(save_path)
    print(f"✅ {school_name} QR 생성 완료 → {save_path}")

print("🎉 모든 QR코드 생성 완료! data/qr2 폴더를 확인하세요.")
