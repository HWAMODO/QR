import streamlit as st
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

def show_dashboard():
    st.subheader("📋 실시간 체크인 기록 조회")

    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    keyfile_dict = dict(st.secrets["gcp_service_account"])
    keyfile_dict["private_key"] = keyfile_dict["private_key"].replace("\\n", "\n")

    credentials = ServiceAccountCredentials.from_json_keyfile_dict(keyfile_dict, scope)
    client = gspread.authorize(credentials)

    try:
        sheet = client.open("체크인기록").worksheet("Sheet1")
        data = sheet.get_all_records()
        df = pd.DataFrame(data)
        df.columns = df.columns.str.strip()
        df = df.reset_index(drop=True)

        # ✅ 연번 처리
        if "연번" in df.columns:
        df = df[df["연번"].astype(str).str.isnumeric()]
        df["연번"] = df["연번"].astype(int)


        if df.empty:
            st.info("아직 체크인 기록이 없습니다.")
        else:
            st.success(f"총 {len(df)}건의 체크인 기록이 조회되었습니다.")
            st.dataframe(df.set_index("연번"))

            st.subheader("🏫 학교별 체크인 횟수")
            st.bar_chart(df["근무장소"].value_counts())

    except Exception as e:
        st.error(f"시트를 불러오는 중 오류 발생: {e}")
