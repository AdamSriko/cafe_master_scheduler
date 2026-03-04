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
    # --- ADMIN CHECK (HIDDEN) ---
# To access: your-url.streamlit.app/?admin=true
is_admin = st.query_params.get("admin") == "true"

with st.sidebar:
  # --- ADMIN CHECK (HIDDEN) ---
# Access via: your-url.streamlit.app/?admin=true
is_admin = st.query_params.get("admin") == "true"

with st.sidebar:
    st.header("👤 Staff Entry")
    # Added a unique key here to prevent the DuplicateElementId error
    name = st.text_input("Employee Name", key="main_name_input")
    exp = st.selectbox("Skill Level", ["High Experience", "Less Experienced", "New"], key="main_exp_select")
    
    st.write("---")
    st.write("**Weekly Availability**")
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    
    avail_data = {}
    for d in days:
        with st.expander(f"{d} Hours"):
            # We use the 'name' variable in the key to keep it unique per person
            is_off = st.checkbox("Off Day", key=f"off_{d}_{name}")
            if not is_off:
                start = st.time_input("Start Time", time(6, 30), key=f"s_{d}_{name}")
                end = st.time_input("End Time", time(23, 0), key=f"e_{d}_{name}")
                avail_data[d] = (start, end)
            else:
                avail_data[d] = None

    if st.button("➕ Add Employee", key="add_emp_btn"):
        if name:
            st.session_state.roster.append({
                "Name": name, 
                "Level": exp, 
                "Schedule": avail_data
            })
            st.rerun()

    # --- PROTECTED ADMIN SECTION ---
    if is_admin:
        st.divider()
        st.warning("🛠️ ADMIN MODE")
        if st.button("⚡ Bulk Load 12 Test Staff", key="admin_bulk_btn"):
            import random # Ensure random is available
            test_names = ["Adam", "Sarah", "Mike", "Elena", "Chris", "Beth", "David", "Julie", "Kevin", "Nora", "Oscar", "Paul"]
            for t_name in test_names:
                t_sched = {day: (time(6,30), time(23,0)) if random.random() > 0.1 else None for day in days}
                st.session_state.roster.append({
                    "Name": f"T-{t_name}", 
                    "Level": random.choice(["High Experience", "Less Experienced", "New"]),
                    "Schedule": t_sched
                })
            st.rerun()

        if st.button("🗑️ Reset All Data", key="admin_reset_btn"):
            st.session_state.roster = []
            st.rerun()

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
