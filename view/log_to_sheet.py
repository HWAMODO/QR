import streamlit as st
import json
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials
import gspread

# ✅ 인증 범위
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# ✅ secrets에서 서비스 계정 정보 불러오기
keyfile_dict = json.loads(st.secrets["gcp_service_account"])
credentials = ServiceAccountCredentials.from_json_keyfile_dict(keyfile_dict, scope)

# ✅ 구글시트 클라이언트 생성
client = gspread.authorize(credentials)

# ✅ 체크인 기록 함수 정의
def log_checkin(name, school):
    try:
        sheet = client.open("체크인기록").worksheet("Sheet1")  # 시트 이름 정확히 확인!
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sheet.append_row([name, school, now])
        print("✅ 시트에 기록 완료:", name, school)
    except Exception as e:
        print(f"❌ 구글시트 기록 실패: {e}")
