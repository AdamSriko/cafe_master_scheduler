import streamlit as st
import pandas as pd
import random
from datetime import time, datetime, timedelta

st.set_page_config(page_title="Cafe Scheduler Pro", layout="wide", page_icon="☕")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { background-color: #1a237e; color: white; font-weight: bold; border-radius: 8px; border: none; }
    .stDownloadButton>button { background-color: #2e7d32; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("☕ Cafe Management System")
st.subheader("7-Day Hourly Optimizer | 06:30 - 23:00")

if 'roster' not in st.session_state:
    st.session_state.roster = []

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
                "Name": name, "Level": exp, "Type": job_type, "Schedule": weekly_hours
            })
            st.rerun()
    
    st.divider()
    if st.button("⚡ Bulk Load 12 Test Staff"):
        test_names = ["Adam", "Sarah", "Mike", "Elena", "Chris", "Beth", "David", "Julie", "Kevin", "Nora", "Oscar", "Paul"]
        for t_name in test_names:
            t_sched = {d: (time(6,30), time(23,0)) if random.random() > 0.1 else None for d in days}
            st.session_state.roster.append({
                "Name": f"T-{t_name}", 
                "Level": random.choice(["High Experience", "Less Experienced", "New"]),
                "Type": random.choice(["Full-Time", "Part-Time"]),
                "Schedule": t_sched
            })
        st.rerun()

    if st.button("🗑️ Reset All Data"):
        st.session_state.roster = []
        st.rerun()

if st.session_state.roster:
    st.write("### 📋 Staff Database")
    summary_df = pd.DataFrame([{"Name": e['Name'], "Level": e['Level'], "Type": e['Type']} for e in st.session_state.roster])
    st.dataframe(summary_df, use_container_width=True, hide_index=True)

    if st.button("🚀 GENERATE MASTER WEEKLY SCHEDULE"):
        start_dt = datetime.combine(datetime.today(), time(6, 30))
        end_dt = datetime.combine(datetime.today(), time(23, 0))
        hour_slots = []
        curr = start_dt
        while curr < end_dt:
            hour_slots.append(curr.time())
            curr += timedelta(hours=1)

        weekly_final = []
        for day in days:
            for t_slot in hour_slots:
                available = []
                for e in st.session_state.roster:
                    day_sched = e['Schedule'].get(day)
                    if day_sched:
                        s_time, e_time = day_sched
                        slot_end = (datetime.combine(datetime.today(), t_slot) + timedelta(hours=1)).time()
                        if s_time <= t_slot and e_time >= slot_end:
                            available.append(e)
                
                available.sort(key=lambda x: (x['Type'] != "Full-Time", ["High Experience", "Less Experienced", "New"].index(x['Level'])))

                if len(available) >= 3:
                    selected = available[:3]
                    selected.sort(key=lambda x: ["High Experience", "Less Experienced", "New"].index(x['Level']))
                    weekly_final.append({
                        "Day": day, "Time": t_slot.strftime("%H:%M"),
                        "Espresso Bar ☕": selected[0]['Name'],
                        "Traditional 🥤": selected[1]['Name'],
                        "Cashier 💰": selected[2]['Name']
                    })
                else:
                    weekly_final.append({
                        "Day": day, "Time": t_slot.strftime("%H:%M"),
                        "Espresso Bar ☕": "⚠️ UNDERSTAFFED", "Traditional 🥤": "---", "Cashier 💰": "---"
                    })

        st.write("### ✅ Master Weekly Schedule")
        df_result = pd.DataFrame(weekly_final)
        day_tabs = st.tabs(days)
        for i, tab in enumerate(day_tabs):
            with tab:
                day_data = df_result[df_result['Day'] == days[i]].drop(columns=['Day'])
                st.dataframe(day_data, use_container_width=True, hide_index=True)

        csv = df_result.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Master Schedule", data=csv, file_name="cafe_weekly_master.csv", mime="text/csv")
else:
    st.info("👈 Add employees in the sidebar to begin.")
