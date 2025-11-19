import streamlit as st
import pandas as pd
import random
from pathlib import Path
from ai_model import RNNModel
from streamlit_autorefresh import st_autorefresh
from utils import calculate_total_score  # eski score hesaplama fonksiyonun

# -----------------------------
st.set_page_config(page_title="⚡ AI Task Manager", layout="wide")
st.title("⚡ AI Task Manager - AI Weighted Total Score Table + Inline Delete")

DATA_FILE = Path("tasks_data.csv")

# -----------------------------
# Session state
if "tasks" not in st.session_state:
    st.session_state.tasks = []

if "rnn_model" not in st.session_state:
    st.session_state.rnn_model = RNNModel()

# -----------------------------
# Auto-refresh every 3 seconds
st_autorefresh(interval=3000, key="table_refresh")

# -----------------------------
# Append-only CSV log
def log_task_change(task):
    df = pd.DataFrame([task])
    if DATA_FILE.exists():
        df.to_csv(DATA_FILE, mode='a', header=False, index=False)
    else:
        df.to_csv(DATA_FILE, mode='w', header=True, index=False)

# -----------------------------
# Initialize dummy tasks
if not st.session_state.tasks:
    dummy_tasks = ["Fix API", "Write Report", "Test Module", "Update Script", "Analyze Document"]
    for desc in dummy_tasks:
        st.session_state.tasks.append({
            "desc": desc,
            "CPU": random.randint(10,50),
            "RAM": random.randint(50,300),
            "score": 0.0
        })

# -----------------------------
# Add Task Form
st.subheader("➕ Add Task")
with st.form("add_task_form"):
    task_desc_input = st.text_input("Task Description")
    submit = st.form_submit_button("Add Task")
    if submit and task_desc_input:
        task_entry = {
            "desc": task_desc_input,
            "CPU": random.randint(10,50),
            "RAM": random.randint(50,500),
            "score": 0.0
        }
        st.session_state.tasks.append(task_entry)
        log_task_change(task_entry)
        st.success(f"Task '{task_desc_input}' added.")

# -----------------------------
# Update CPU/RAM/Score and total_score
for t in st.session_state.tasks:
    t["CPU"] = random.randint(5,80)
    t["RAM"] = random.randint(50,500)

    # AI prediction
    t["score"] = st.session_state.rnn_model.predict({"CPU": t["CPU"], "RAM": t["RAM"]})

    # Eski score
    old_score = calculate_total_score(t)

    # Total score: %70 AI, %30 old_score
    t["total_score"] = t["score"]*0.7 + old_score*0.3

    # Append-only CSV log
    log_task_change(t)

# -----------------------------
# Sort by total_score
tasks_sorted = sorted(st.session_state.tasks, key=lambda x: x["total_score"], reverse=True)

# -----------------------------
# Table header
st.subheader("📋 Tasks Table")
col_desc, col_cpu, col_ram, col_score, col_total, col_delete = st.columns([4,1,1,1,1,1])
col_desc.markdown("**Task**")
col_cpu.markdown("**CPU**")
col_ram.markdown("**RAM**")
col_score.markdown("**Score**")
col_total.markdown("**Total Score**")
col_delete.markdown("**Action**")

# Table rows
for t in tasks_sorted:
    col_desc, col_cpu, col_ram, col_score, col_total, col_delete = st.columns([4,1,1,1,1,1])
    col_desc.write(f"{t['desc']}")
    col_cpu.write(f"{t['CPU']}")
    col_ram.write(f"{t['RAM']}")
    col_score.write(f"{t['score']:.2f}")
    col_total.write(f"{t['total_score']:.2f}")
    if col_delete.button("Delete", key=f"del_{t['desc']}"):
        st.session_state.tasks.remove(t)
