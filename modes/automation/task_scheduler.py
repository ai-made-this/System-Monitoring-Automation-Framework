"""Task Scheduler - Manages automated task scheduling"""
import json
import time
from pathlib import Path

TASKS_FILE = Path(__file__).parent / "scheduled_tasks.json"

def get_task_scheduler():
    """Get scheduled automation tasks"""
    try:
        if not TASKS_FILE.exists():
            return {"scheduled_tasks": [], "status": "no_tasks"}
        
        with open(TASKS_FILE, 'r') as f:
            tasks = json.load(f)
        
        active_tasks = []
        for task in tasks:
            # Check if task should be running
            next_run = task.get("next_run", 0)
            status = "pending" if next_run > time.time() else "ready"
            
            active_tasks.append({
                "name": task.get("name", "unnamed"),
                "type": task.get("type", "unknown"),
                "schedule": task.get("schedule", "manual"),
                "status": status,
                "next_run": next_run,
                "last_run": task.get("last_run", None)
            })
        
        return {
            "scheduled_tasks": active_tasks,
            "task_count": len(active_tasks),
            "ready_tasks": len([t for t in active_tasks if t["status"] == "ready"])
        }
    except Exception as e:
        return {"error": str(e)}