import streamlit as st
import pandas as pd
import random
from datetime import time

# --- 1. PAGE SETUP ---
st.set_page_config(page_title="Cafe Scheduler Pro", layout="wide", page_icon="☕")

# Custom UI Styling
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { background-color: #1a237e; color: white; border-radius: 8px; width: 100%; }
    .shift-header { background-color: #e3f2fd; padding: 10px; border-radius: 5px; border-left: 5px solid #1e88e5; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("☕ Cafe Daily Schedule")

# Initialize the staff list if it doesn't exist
if 'roster' not in st.session_state:
    st.session_state.roster = []

# --- 2. ADMIN CHECK (Secret Access) ---
# Use: your-url.streamlit.app/?admin=true
is_admin = st.query_params.get("admin") == "true"

# --- 3. SIDEBAR (STAFF ENTRY) ---
with st.sidebar:
    st.header("👤 Staff Entry")
    
    # Unique keys prevent "DuplicateElementId" errors
    name = st.text_input("Employee Name", key="input_name")
    exp = st.selectbox("Skill Level", ["High Experience", "Less Experienced", "New"], key="input_exp")
    
    st.write("---")
    st.write("**Weekly Availability**")
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    
    avail_data = {}
    for d in days:
        with st.expander(f"{d} Hours"):
            # Using name in the key ensures uniqueness for each staff member added
            is_off = st.checkbox("Off Day", key=f"off_{d}_{name}")
            if not is_off:
                start = st.time_input("Start Time", time(6, 30), key=f"s_{d}_{name}")
                end = st.time_input("End Time", time(23, 0), key=f"e_{d}_{name}")
                avail_data[d] = (start, end)
            else:
                avail_data[d] = None

    if st.button("➕ Add Employee", key="btn_add_staff"):
        if name:
            st.session_state.roster.append({
                "Name": name, 
                "Level": exp, 
                "Schedule": avail_data
            })
            st.rerun()

    # --- PROTECTED ADMIN TOOLS ---
    if is_admin:
        st.divider()
        st.warning("🛠️ ADMIN MODE ACTIVE")
        
        if st.button("⚡ Bulk Load 12 Test Staff", key="btn_admin_bulk"):
            test_names = ["Adam", "Sarah", "Mike", "Elena", "Chris", "Beth", "David", "Julie", "Kevin", "Nora", "Oscar", "Paul"]
            for t_name in test_names:
                # Set random availability for testing
                if st.button("🗑️ Reset All Data", key="btn_admin_reset"):
            st.session_state.roster = []
            st.rerun()

# --- 4. MAIN DISPLAY (SCHEDULE) ---
if st.session_state.roster:
    # Create a tab for each day of the week
    tabs = st.tabs(days)
    
    for i, tab in enumerate(tabs):
        day_name = days[i]
        with tab:
            st.subheader(f"📅 {day_name} Assignments")
            
            # MORNING BLOCK (06:30 - 15:00)
            st.markdown("<div class='shift-header'>☀️ Morning Shift (06:30 - 15:00)</div>", unsafe_allow_html=True)
            m_staff = []
            for emp in st.session_state.roster:
                s_data = emp['Schedule'].get(day_name)
                if s_data:
                    e_start, e_end = s_data
                    # Check if their hours overlap with the morning block
                    if e_start < time(15, 0) and e_end > time(6, 30):
                        m_staff.append({
                            "Staff Name": emp['Name'],
                            "Shift Hours": f"{e_start.strftime('%H:%M')} - {e_end.strftime('%H:%M')}",
                            "Position": "Barista (Senior)" if emp['Level'] == "High Experience" else "Floor/Cashier"
                        })
            
            if m_staff:
                st.table(pd.DataFrame(m_staff))
            else:
                st.info("No staff scheduled for this morning.")

            st.write("") # Gap between blocks

            # EVENING BLOCK (15:00 - 23:00)
            st.markdown("<div class='shift-header'>🌙 Evening Shift (15:00 - 23:00)</div>", unsafe_allow_html=True)
            e_staff = []
            for emp in st.session_state.roster:
                s_data = emp['Schedule'].get(day_name)
                if s_data:
                    e_start, e_end = s_data
                    # Check if
