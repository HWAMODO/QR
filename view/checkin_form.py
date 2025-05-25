# view/checkin_form.py
import streamlit as st
from log_to_sheet import log_checkin

st.set_page_config(page_title="체크인 폼", layout="centered")

st.title("👮 아동안전지킴이 체크인 폼")

name = st.text_input("👤 이름")
school = st.text_input("🏫 순찰 학교명")

if st.button("✅ 체크인"):
    if name and school:
        log_checkin(name, school)
        st.success(f"{name}님, '{school}' 체크인 완료!")
    else:
        st.warning("모든 항목을 입력해주세요.")
