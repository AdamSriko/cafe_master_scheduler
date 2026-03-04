import streamlit as st
import pandas as pd
import random
from datetime import time, datetime, timedelta

# --- PAGE CONFIG ---
st.set_page_config(page_title="Cafe Scheduler Pro", layout="wide", page_icon="☕")

# Custom CSS for a professional look
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { background-color: #1a237e; color: white; font-weight: bold; border-radius: 8px; border: none; }
    .stDownloadButton>button { background-color: #2e7d32; color: white; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { background-color: #e0e0e0; border-radius: 5px 5px 0 0; padding: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("☕ Cafe Management System")
st.subheader("7-Day Hourly Optimizer | 06:30 - 23:00")

# --- INITIALIZE SESSION STATE ---
if 'roster' not in st.session_state:
    st.session_state.roster = []

# --- SIDEBAR: STAFF INPUT ---
with st.sidebar:
    st.header("👤 Add Staff Member")
    name = st.text_input("Full Name")
    exp = st.selectbox("Skill Level", ["High Experience", "Less Experienced", "New"])
    job_type = st.radio("Contract", ["Full-Time", "Part-Time"])
    
    st.write("---")
    st.write("**Weekly Availability**")
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    
    weekly_hours = {}
    for day in days:
        with st.expander(f"Set Hours for {day}"):
            off = st.checkbox("Off Day", key=f"off_{day}_{name}")
            if not off:
                start = st.time_input("Start", time(6, 30), key=f"s_{day}_{name}")
                end = st.time_input("End", time(23, 0), key=f"e_{day}_{name}")
                weekly_hours[day] = (start, end)
            else:
                weekly_hours[day] = None

    if st.button("➕ Add Employee to System"):
        if name:
            st.session_state.roster.append({
                "Name": name, "Level": exp, "Type
