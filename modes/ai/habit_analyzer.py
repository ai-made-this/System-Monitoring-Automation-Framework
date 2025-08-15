"""Habit Analyzer - Analyzes user behavior patterns from collected data"""
import json
import time
from pathlib import Path
from collections import defaultdict, Counter

DATA_DIR = Path(__file__).parent / "data"
HABITS_FILE = DATA_DIR / "user_habits.json"

def get_habit_analyzer():
    """Analyze user habits from collected monitoring data"""
    try:
        if not DATA_DIR.exists():
            DATA_DIR.mkdir(exist_ok=True)
        
        if not HABITS_FILE.exists():
            return {
                "status": "no_data",
                "message": "No habit data collected yet. Start monitoring to build patterns."
            }
        
        with open(HABITS_FILE, 'r') as f:
            habits = json.load(f)
        
        # Analyze patterns
        analysis = {
            "most_used_apps": Counter(habits.get("app_usage", {})).most_common(10),
            "peak_activity_hours": _analyze_time_patterns(habits.get("activity_times", [])),
            "keyboard_patterns": _analyze_keyboard_habits(habits.get("keyboard_data", {})),
            "resource_usage_patterns": _analyze_resource_patterns(habits.get("resource_data", {})),
            "habit_strength": _calculate_habit_strength(habits),
            "last_updated": habits.get("last_updated", "unknown")
        }
        
        return {
            "status": "analyzed",
            "habits": analysis,
            "data_points": len(habits.get("sessions", [])),
            "analysis_confidence": _calculate_confidence(habits)
        }
    except Exception as e:
        return {"error": str(e)}

def _analyze_time_patterns(activity_times):
    """Analyze when user is most active"""
    if not activity_times:
        return {"message": "No time pattern data"}
    
    hour_counts = Counter()
    for timestamp in activity_times:
        hour = time.localtime(timestamp).tm_hour
        hour_counts[hour] += 1
    
    return {
        "peak_hours": hour_counts.most_common(5),
        "total_sessions": len(activity_times)
    }

def _analyze_keyboard_habits(keyboard_data):
    """Analyze typing patterns and shortcuts"""
    if not keyboard_data:
        return {"message": "No keyboard data"}
    
    return {
        "avg_keys_per_minute": keyboard_data.get("avg_kpm", 0),
        "most_used_shortcuts": keyboard_data.get("shortcuts", {}),
        "typing_sessions": keyboard_data.get("session_count", 0)
    }

def _analyze_resource_patterns(resource_data):
    """Analyze system resource usage patterns"""
    if not resource_data:
        return {"message": "No resource data"}
    
    return {
        "avg_cpu_usage": resource_data.get("avg_cpu", 0),
        "avg_memory_usage": resource_data.get("avg_memory", 0),
        "peak_usage_times": resource_data.get("peak_times", [])
    }

def _calculate_habit_strength(habits):
    """Calculate how strong/consistent user habits are"""
    sessions = habits.get("sessions", [])
    if len(sessions) < 10:
        return {"strength": "insufficient_data", "score": 0}
    
    # Simple consistency score based on session count and regularity
    consistency_score = min(len(sessions) / 100, 1.0) * 100
    
    return {
        "strength": "strong" if consistency_score > 70 else "moderate" if consistency_score > 30 else "weak",
        "score": round(consistency_score, 2),
        "sessions_analyzed": len(sessions)
    }

def _calculate_confidence(habits):
    """Calculate confidence in habit analysis"""
    data_points = len(habits.get("sessions", []))
    if data_points < 5:
        return "low"
    elif data_points < 20:
        return "moderate"
    else:
        return "high"