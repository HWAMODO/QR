# view/log_to_sheet.py
import os
from oauth2client.service_account import ServiceAccountCredentials
import gspread
from datetime import datetime

def log_checkin(name, school_name):
    # 현재 경로 기준으로 키 파일 참조
    current_dir = os.path.dirname(__file__)
    key_path = os.path.join(current_dir, "..", "credentials", "google_sheets_key.json")

    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]

    credentials = ServiceAccountCredentials.from_json_keyfile_name(key_path, scope)
    client = gspread.authorize(credentials)

    # Google Sheet 열기
    sheet = client.open("체크인기록").worksheet("시트1")  # 정확한 이름 확인 필요

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sheet.append_row([now, name, school_name])
