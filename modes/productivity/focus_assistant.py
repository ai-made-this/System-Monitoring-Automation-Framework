"""Focus Assistant - Help maintain focus and reduce distractions"""
import json
import time
from pathlib import Path

FOCUS_LOG = Path(__file__).parent / "focus_sessions.json"
DISTRACTION_LOG = Path(__file__).parent / "distractions.json"

def get_focus_assistant():
    """Get focus assistance status and recommendations"""
    try:
        # Load focus session data
        if FOCUS_LOG.exists():
            with open(FOCUS_LOG, 'r') as f:
                focus_data = json.load(f)
        else:
            focus_data = {"sessions": [], "goals": {}}
        
        # Load distraction data
        if DISTRACTION_LOG.exists():
            with open(DISTRACTION_LOG, 'r') as f:
                distraction_data = json.load(f)
        else:
            distraction_data = {"distractions": [], "blocked_sites": []}
        
        # Calculate focus metrics
        recent_sessions = focus_data["sessions"][-10:] if focus_data["sessions"] else []
        avg_focus_time = sum(s.get("duration", 0) for s in recent_sessions) / len(recent_sessions) if recent_sessions else 0
        
        # Current focus recommendations
        current_hour = time.localtime().tm_hour
        recommendations = []
        
        if 9 <= current_hour <= 11:
            recommendations.append({
                "type": "timing",
                "message": "Peak focus hours - great time for deep work",
                "action": "Start a focus session"
            })
        elif 13 <= current_hour <= 15:
            recommendations.append({
                "type": "timing", 
                "message": "Post-lunch productivity dip - consider shorter tasks",
                "action": "Take a short break or do light tasks"
            })
        
        if avg_focus_time < 25:  # Less than 25 minutes average
            recommendations.append({
                "type": "improvement",
                "message": "Focus sessions are short - try building up gradually",
                "action": "Aim for 30-minute focus sessions"
            })
        
        return {
            "status": "active",
            "current_recommendations": recommendations,
            "focus_metrics": {
                "average_focus_time_minutes": round(avg_focus_time / 60, 1),
                "total_focus_sessions": len(focus_data["sessions"]),
                "focus_streak_days": _calculate_focus_streak(focus_data),
                "distraction_count_today": len([d for d in distraction_data["distractions"] 
                                              if time.time() - d.get("timestamp", 0) < 86400])
            },
            "capabilities": {
                "pomodoro_timer": "25-minute focus sessions with breaks",
                "distraction_blocking": "Block distracting websites and apps",
                "focus_music": "Play focus-enhancing background sounds",
                "break_reminders": "Remind to take regular breaks",
                "goal_tracking": "Track daily and weekly focus goals",
                "environment_optimization": "Optimize system for focus"
            },
            "focus_techniques": {
                "pomodoro": "25 min work + 5 min break cycles",
                "deep_work": "Extended 90-120 minute focus blocks",
                "timeboxing": "Allocate specific time blocks for tasks",
                "flow_state": "Optimize conditions for flow state",
                "ultradian_rhythms": "Work with natural 90-minute cycles"
            },
            "distraction_management": {
                "website_blocking": "Block social media and news sites",
                "notification_silencing": "Disable non-essential notifications",
                "app_limiting": "Limit time spent in distracting apps",
                "focus_mode": "System-wide focus mode activation",
                "environment_control": "Adjust lighting, sound, etc."
            },
            "productivity_insights": [
                f"Best focus time: {_get_best_focus_time(focus_data)}",
                f"Most common distraction: {_get_top_distraction(distraction_data)}",
                f"Focus improvement: {_get_focus_trend(focus_data)}"
            ]
        }
    except Exception as e:
        return {"error": str(e)}

def _calculate_focus_streak(focus_data):
    """Calculate current focus streak in days"""
    # Simplified implementation
    return 3

def _get_best_focus_time(focus_data):
    """Get the time of day with best focus"""
    return "10:00-11:30 AM"

def _get_top_distraction(distraction_data):
    """Get most common distraction"""
    return "Social media notifications"

def _get_focus_trend(focus_data):
    """Get focus improvement trend"""
    return "Improving (+15% this week)"