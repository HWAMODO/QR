import streamlit as st
import json
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# ✅ secrets에 저장한 키 dict 불러오기
json_key = st.secrets["google_service_account"]

# ✅ dict로부터 credentials 생성
credentials = ServiceAccountCredentials.from_json_keyfile_dict(json_key, scope)
