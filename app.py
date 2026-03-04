import streamlit as st
import pandas as pd
from datetime import time

# --- PAGE CONFIG ---
st.set_page_config(page_title="Cafe Scheduler Simple", layout="wide", page_icon="☕")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { background-color: #1a237e; color: white; border-radius: 8px; }
    .block-card { padding: 20px; border-radius: 10px; background-color: white; border-left: 5px solid #1a237e; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.title("☕ Cafe Schedule: Daily Overview")

if 'roster' not in st.session_state:
    st.session_state.roster = []

# --- SIDEBAR ---
with st.sidebar:
    st.header("👤 Staff Entry")
    name = st.text_input("Name")
    exp = st.selectbox("Skill", ["High Experience", "Less Experienced", "New"])
    
    st.write("**Weekly Availability**")
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    weekly_hours = {}
    for day in days:
        with st.expander(f"{day} Hours"):
            off = st.checkbox("Off Day", key=f"off_{day}")
            if not off:
                start = st.time_input("Start", time(6, 30), key=f"s_{day}")
                end = st.time_input("End", time(23, 0), key=f"e_{day}")
                weekly_hours[day] = (start, end)
            else:
                weekly_hours[day] = None

    if st.button("➕ Add Employee"):
        if name:
            st.session_state.roster.append({"Name": name, "Level": exp, "Schedule": weekly_hours})
            st.rerun()

    if st.button("🗑️ Reset"):
        st.session_state.roster = []
        st.rerun()

# --- MAIN VIEW ---
if st.session_state.roster:
    day_tabs = st.tabs(days)
    
    for i, tab in enumerate(day_tabs):
        current_day = days[i]
        with tab:
            st.header(f"📅 {current_day} Assignments")
            
            # Shift Definitions
            shifts = [
                ("Morning Shift", time(6, 30), time
