def calculate_total_score(task):
    """Simple formula: weighted sum of CPU, RAM, and score"""
    return 0.3*task["CPU"] + 0.3*task["RAM"]/10 + 0.4*task["score"]
