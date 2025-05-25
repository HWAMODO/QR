import streamlit as st
import json
from oauth2client.service_account import ServiceAccountCredentials

# ✅ 구글 API 접근 범위 정의
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

# ✅ secrets에서 JSON 문자열 가져와 dict로 변환
keyfile_dict = json.loads(st.secrets["gcp_service_account"])

# ✅ 인증 객체 생성
credentials = ServiceAccountCredentials.from_json_keyfile_dict(keyfile_dict, scope)
