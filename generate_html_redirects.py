import pandas as pd
import os

# 파일 경로
INPUT_CSV = "C:/Users/USER/Desktop/국민대과제/view/초등학교_좌표포함.csv"
OUTPUT_FOLDER = "C:/Users/USER/Desktop/국민대과제/html_pages"

# ✅ school 이름만 파라미터로 전달되도록 수정
STREAMLIT_BASE = "https://qr--main--hwamodo.streamlit.app/view/checkin_form.py?school="

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

df = pd.read_csv(INPUT_CSV)
df.columns = df.columns.str.strip()
school_names = df["학교명"].dropna().unique()

for school in school_names:
    streamlit_url = f"{STREAMLIT_BASE}{school}"
    filename = os.path.join(OUTPUT_FOLDER, f"{school}.html")

    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{school} QR 체크인</title>
  <script>
    setTimeout(function () {{
      window.location.href = "{streamlit_url}";
    }}, 3000);
  </script>
</head>
<body style="text-align:center; font-family:sans-serif; padding-top:50px;">
  <h2>📱 {school} QR 체크인 안내</h2>
  <p>자동으로 체크인 페이지로 이동합니다.</p>
  <p>안 열릴 경우 아래 버튼을 누르세요.</p>
  <a href="googlechrome://{streamlit_url.replace('https://', '')}">
    <button style="padding:10px 20px; font-size:16px;">📦 Chrome으로 열기</button>
  </a>
  <br/><br/>
  <small>위 링크가 열리지 않으면 직접 Chrome 브라우저로 복사해 여세요.</small>
</body>
</html>"""

    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)

print("🎉 HTML 브릿지 페이지 생성 완료!")
