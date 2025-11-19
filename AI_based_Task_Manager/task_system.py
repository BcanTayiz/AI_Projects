import pandas as pd
import random
from pathlib import Path

TASKS_FILE = Path("tasks_data.csv")
folders = ["System/Kernel", "User/Documents", "User/Projects", "User/Downloads"]

tasks_store = []

def generate_dummy_tasks(n=5):
    actions = ["Fix", "Update", "Test", "Write", "Analyze", "Deploy", "Debug", "Refactor"]
    objects = ["API", "Module", "Script", "Report", "Document", "Feature", "System", "Project"]
    dummy_tasks = []
    for _ in range(n):
        desc = f"{random.choice(actions)} {random.choice(objects)}"
        folder = random.choice(folders)
        CPU = random.randint(10,50)
        RAM = random.randint(50,300)
        score = random.uniform(10,80)
        dummy_tasks.append({"desc": desc, "folder": folder, "CPU": CPU, "RAM": RAM, "score": score})
    return dummy_tasks

def add_task(task, folder):
    task_copy = task.copy()
    task_copy["folder"] = folder
    tasks_store.append(task_copy)

def get_all_tasks():
    for t in tasks_store:
        t["CPU"] = random.randint(5, 80)
        t["RAM"] = random.randint(50, 500)
    return tasks_store

def delete_task(desc, folder):
    global tasks_store
    tasks_store = [t for t in tasks_store if not (t["desc"]==desc and t["folder"]==folder)]

def log_to_csv():
    df = pd.DataFrame(tasks_store)
    if not df.empty:
        df["timestamp"] = pd.Timestamp.now()
        if TASKS_FILE.exists():
            df.to_csv(TASKS_FILE, mode='a', index=False, header=False)
        else:
            df.to_csv(TASKS_FILE, index=False)
