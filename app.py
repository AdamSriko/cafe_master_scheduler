import streamlit as st
import pandas as pd
import random
from datetime import time

# --- 1. PAGE SETUP ---
st.set_page_config(page_title="Cafe Scheduler Pro", layout="wide", page_icon="☕")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { background-color: #1a237e; color: white; border-radius: 8px; width: 100%; }
    .shift-header { background-color: #e3f2fd; padding: 10px; border-radius: 5px; border-left: 5px solid #1e88e5; font-weight: bold; margin-top: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.title("☕ Cafe Daily Schedule")
st.subheader("Shift Overview: Clock-In & Clock-Out Times")

if 'roster' not in st.session_state:
    st.session_state.roster = []

# Admin Check via URL: ?admin=true
is_admin = st.query_params.get("admin") == "true"

# --- 2. SIDEBAR (STAFF ENTRY) ---
with st.sidebar:
    st.header("👤 Staff Entry")
    name = st.text_input("Employee Name", key="input_name")
    exp = st.selectbox("Skill Level", ["High Experience", "Less Experienced", "New"], key="input_exp")
    job_type = st.radio("Contract Type", ["Full-Time", "Part-Time"], key="input_type")
    
    st.write("---")
    st.write("**Weekly Availability**")
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    
    avail_data = {}
    for d in days:
        with st.expander(f"{d} Hours"):
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
                "Type": job_type,
                "Schedule": avail_data
            })
            st.rerun()

    if is_admin:
        st.divider()
        st.warning("🛠️ ADMIN MODE")
        if st.button("⚡ Bulk Load 12 Test Staff", key="btn_bulk"):
            test_names = ["Adam", "Sarah", "Mike", "Elena", "Chris", "Beth", "David", "Julie", "Kevin", "Nora", "Oscar", "Paul"]
            for t_name in test_names:
                t_sched = {day: (time(random.randint(7,10),0), time(random.randint(15,22),0)) if random.random() > 0.1 else None for day in days}
                st.session_state.roster.append({
                    "Name": f"T-{t_name}", 
                    "Level": random.choice(["High Experience", "Less Experienced", "New"]),
                    "Type": random.choice(["Full-Time", "Part-Time"]),
                    "Schedule": t_sched
                })
            st.rerun()
        if st.button("🗑️ Reset All", key="btn_reset"):
            st.session_state.roster = []
            st.rerun()

# --- 3. MAIN DISPLAY ---
if st.session_state.roster:
    tabs = st.tabs(days)
    
   # --- 3. MAIN DISPLAY ---
if st.session_state.roster:
    tabs = st.tabs(days)
    
    for i, tab in enumerate(tabs):
        day_name = days[i]
        with tab:
            st.subheader(f"📅 {day_name} Assignments")
            
            # WE DEFINE THE SHIFTS HERE SO THE LOOP CAN SEE THEM
            shifts = [
                ("☀️ Morning Block (06:30 - 15:00)", time(6, 30), time(15, 0)),
                ("🌙 Evening Block (15:00 - 23:00)", time(15, 0), time(23, 0))
            ]
            
            for s_label, s_start, s_end in shifts:
                st.markdown(f"<div class='shift-header'>{s_label}</div>", unsafe_allow_html=True)
                
                on_duty = []
                for emp in st.session_state.roster:
                    day_sched = emp['Schedule'].get(day_name)
                    if day_sched:
                        e_s, e_e = day_sched
                        # Check if worker's hours overlap with this shift block
                        if e_s < s_end and e_e > s_start:
                            on_duty.append({
                                "Staff Member": emp['Name'],
                                "Status": emp['Type'],
                                "CLOCK IN": e_s.strftime('%H:%M'),
                                "CLOCK OUT": e_e.strftime('%H:%M'),
                                "Position": "Lead Barista" if emp['Level'] == "High Experience" else "Floor/Cashier"
                            })
                
                if on_duty:
                    df_view = pd.DataFrame(on_duty).sort_values(by="CLOCK IN")
                    st.table(df_view)
                else:
                    st.info(f"No staff scheduled for this block.")
else:
    st.info("👈 Please enter staff members in the sidebar to generate the view.")
