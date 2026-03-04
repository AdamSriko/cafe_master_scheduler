import streamlit as st
import pandas as pd
from datetime import time

st.set_page_config(page_title="Cafe Scheduler", layout="wide", page_icon="☕")

# Custom UI Styling
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { background-color: #1a237e; color: white; border-radius: 8px; width: 100%; }
    .shift-header { background-color: #e3f2fd; padding: 10px; border-radius: 5px; border-left: 5px solid #1e88e5; }
    </style>
    """, unsafe_allow_html=True)

st.title("☕ Cafe Daily Schedule")

if 'roster' not in st.session_state:
    st.session_state.roster = []

# --- SIDEBAR ---
with st.sidebar:
    st.header("👤 Staff Entry")
    name = st.text_input("Employee Name")
    exp = st.selectbox("Skill Level", ["High Experience", "Less Experienced", "New"])
    
    st.write("---")
    st.write("**Weekly Availability**")
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    
    # Store availability here
    avail_data = {}
    for d in days:
        with st.expander(f"{d} Hours"):
            is_off = st.checkbox("Off Day", key=f"off_{d}")
            if not is_off:
                start = st.time_input("Start Time", time(6, 30), key=f"s_{d}")
                end = st.time_input("End Time", time(23, 0), key=f"e_{d}")
                avail_data[d] = (start, end)
            else:
                avail_data[d] = None

    if st.button("➕ Add Employee"):
        if name:
            st.session_state.roster.append({
                "Name": name, 
                "Level": exp, 
                "Schedule": avail_data
            })
            st.rerun()

    if st.button("🗑️ Reset All Data"):
        st.session_state.roster = []
        st.rerun()

# --- MAIN DISPLAY ---
if st.session_state.roster:
    tabs = st.tabs(days)
    
    for i, tab in enumerate(tabs):
        day_name = days[i]
        with tab:
            st.subheader(f"📅 Schedule for {day_name}")
            
            # 1. Morning Shift (06:30 - 15:00)
            st.markdown("<div class='shift-header'>☀️ Morning Shift (06:30 - 15:00)</div>", unsafe_allow_html=True)
            m_staff = []
            for emp in st.session_state.roster:
                s_data = emp['Schedule'].get(day_name)
                if s_data:
                    e_start, e_end = s_data
                    if e_start < time(15, 0) and e_end > time(6, 30):
                        m_staff.append({
                            "Staff": emp['Name'],
                            "Hours": f"{e_start.strftime('%H:%M')} - {e_end.strftime('%H:%M')}",
                            "Position": "Barista (Senior)" if emp['Level'] == "High Experience" else "Floor/Cash"
                        })
            if m_staff:
                st.table(pd.DataFrame(m_staff))
            else:
                st.info("No staff assigned for morning.")

            st.write("") # Spacer

            # 2. Evening Shift (15:00 - 23:00)
            st.markdown("<div class='shift-header'>🌙 Evening Shift (15:00 - 23:00)</div>", unsafe_allow_html=True)
            e_staff = []
            for emp in st.session_state.roster:
                s_data = emp['Schedule'].get(day_name)
                if s_data:
                    e_start, e_end = s_data
                    # Check if they work during any part of the 15:00-23:00 block
                    if e_start < time(23, 0) and e_end > time(15, 0):
                        e_staff.append({
                            "Staff": emp['Name'],
                            "Hours": f"{e_start.strftime('%H:%M')} - {e_end.strftime('%H:%M')}",
                            "Position": "Barista (Senior)" if emp['Level'] == "High Experience" else "Floor/Cash"
                        })
            
            if e_staff:
                st.table(pd.DataFrame(e_staff))
            else:
                st.info("No staff assigned for evening.")
else:
    st.info("👈 Use the sidebar to add employees and their specific hours for each day.")
