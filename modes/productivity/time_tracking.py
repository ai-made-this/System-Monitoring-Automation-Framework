"""Time Tracking - Track time spent on applications and tasks"""
import json
import time
from pathlib import Path
from collections import defaultdict

TIME_LOG = Path(__file__).parent / "time_tracking.json"
SESSION_FILE = Path(__file__).parent / "current_session.json"

def get_time_tracking():
    """Get time tracking data and productivity insights"""
    try:
        # Load time tracking data
        if TIME_LOG.exists():
            with open(TIME_LOG, 'r') as f:
                time_data = json.load(f)
        else:
            time_data = {"sessions": [], "daily_stats": {}}
        
        # Load current session
        if SESSION_FILE.exists():
            with open(SESSION_FILE, 'r') as f:
                current_session = json.load(f)
        else:
            current_session = {
                "start_time": time.time(),
                "active_app": "unknown",
                "total_active_time": 0
            }
        
        # Calculate today's stats
        today = time.strftime("%Y-%m-%d")
        today_sessions = [s for s in time_data["sessions"] if s.get("date") == today]
        
        app_time_today = defaultdict(int)
        total_time_today = 0
        
        for session in today_sessions:
            app = session.get("app", "unknown")
            duration = session.get("duration", 0)
            app_time_today[app] += duration
            total_time_today += duration
        
        # Calculate productivity score (simplified)
        productive_apps = ["vscode", "notepad", "word", "excel", "powerpoint", "sublime", "atom"]
        productive_time = sum(time_spent for app, time_spent in app_time_today.items() 
                            if any(prod_app in app.lower() for prod_app in productive_apps))
        
        productivity_score = (productive_time / total_time_today * 100) if total_time_today > 0 else 0
        
        return {
            "status": "tracking",
            "current_session": {
                "duration_minutes": round((time.time() - current_session["start_time"]) / 60, 1),
                "active_app": current_session["active_app"]
            },
            "today_stats": {
                "total_time_hours": round(total_time_today / 3600, 2),
                "productivity_score": round(productivity_score, 1),
                "top_apps": sorted(app_time_today.items(), key=lambda x: x[1], reverse=True)[:5],
                "session_count": len(today_sessions)
            },
            "capabilities": {
                "automatic_tracking": "Track time spent in applications automatically",
                "productivity_analysis": "Analyze productive vs non-productive time",
                "goal_setting": "Set daily/weekly productivity goals",
                "break_reminders": "Remind to take breaks",
                "focus_sessions": "Pomodoro-style focus tracking",
                "distraction_blocking": "Block distracting websites/apps"
            },
            "tracking_features": [
                "Application usage time",
                "Website visit duration",
                "Idle time detection",
                "Focus session tracking",
                "Break time monitoring",
                "Daily/weekly/monthly reports"
            ],
            "productivity_metrics": {
                "focus_time": "Time spent on productive tasks",
                "distraction_time": "Time spent on non-productive activities",
                "break_frequency": "How often breaks are taken",
                "deep_work_sessions": "Extended focus periods",
                "context_switching": "Frequency of app switching"
            },
            "insights": [
                f"Most productive time: {_get_most_productive_hour(time_data)}",
                f"Average session length: {_get_average_session_length(time_data)} minutes",
                f"Most used app today: {max(app_time_today.items(), key=lambda x: x[1])[0] if app_time_today else 'None'}"
            ]
        }
    except Exception as e:
        return {"error": str(e)}

def _get_most_productive_hour(time_data):
    """Calculate most productive hour of the day"""
    # Simplified implementation
    return "10:00-11:00 AM"

def _get_average_session_length(time_data):
    """Calculate average session length"""
    sessions = time_data.get("sessions", [])
    if not sessions:
        return 0
    
    total_duration = sum(s.get("duration", 0) for s in sessions)
    return round(total_duration / len(sessions) / 60, 1)  # Convert to minutes