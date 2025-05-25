import streamlit as st
import json
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# ✅ 키파일을 secrets에서 문자열로 불러와 파싱
keyfile_dict = json.loads(st.secrets["gcp_service_account"])

credentials = ServiceAccountCredentials.from_json_keyfile_dict(keyfile_dict, scope)

def log_checkin(name, school):
    # 여기에 Google Sheets에 데이터를 기록하는 로직을 작성하자냥
    pass
