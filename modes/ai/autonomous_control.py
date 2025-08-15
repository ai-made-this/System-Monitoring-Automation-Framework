"""Autonomous Control - Takes control of system/applications when requested"""
import json
import time
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
CONTROL_LOG = DATA_DIR / "control_sessions.json"
ACTIVE_SESSION = DATA_DIR / "active_session.json"

def get_autonomous_control():
    """Get status of autonomous control system"""
    try:
        if not DATA_DIR.exists():
            DATA_DIR.mkdir(exist_ok=True)
        
        # Check if there's an active control session
        active_session = _get_active_session()
        
        # Get control capabilities
        capabilities = _get_control_capabilities()
        
        # Get recent control history
        history = _get_control_history()
        
        return {
            "status": "ready",
            "active_session": active_session,
            "capabilities": capabilities,
            "recent_sessions": history,
            "safety_features": _get_safety_features()
        }
    except Exception as e:
        return {"error": str(e)}

def _get_active_session():
    """Check for active autonomous control session"""
    if ACTIVE_SESSION.exists():
        with open(ACTIVE_SESSION, 'r') as f:
            session = json.load(f)
        
        # Check if session is still valid (not expired)
        if time.time() - session.get("start_time", 0) < session.get("max_duration", 3600):
            return {
                "active": True,
                "session_id": session.get("session_id"),
                "start_time": session.get("start_time"),
                "application": session.get("application"),
                "control_type": session.get("control_type"),
                "remaining_time": session.get("max_duration", 3600) - (time.time() - session.get("start_time", 0))
            }
        else:
            # Session expired, clean up
            ACTIVE_SESSION.unlink()
    
    return {"active": False}

def _get_control_capabilities():
    """Get available autonomous control capabilities"""
    return {
        "application_control": {
            "description": "Take control of specific applications",
            "supported_apps": ["games", "browsers", "text_editors"],
            "actions": ["keyboard_input", "mouse_control", "menu_navigation"]
        },
        "system_control": {
            "description": "Control system-level operations",
            "actions": ["process_management", "file_operations", "system_settings"]
        },
        "macro_execution": {
            "description": "Execute recorded macros and action sequences",
            "features": ["speed_control", "repeat_loops", "conditional_execution"]
        },
        "task_automation": {
            "description": "Automate repetitive tasks",
            "capabilities": ["form_filling", "data_entry", "file_processing"]
        }
    }

def _get_control_history():
    """Get recent autonomous control sessions"""
    if not CONTROL_LOG.exists():
        return []
    
    with open(CONTROL_LOG, 'r') as f:
        history = json.load(f)
    
    # Return last 10 sessions
    return history.get("sessions", [])[-10:]

def _get_safety_features():
    """Get safety features for autonomous control"""
    return {
        "emergency_stop": {
            "description": "Immediate stop via ESC key or emergency command",
            "hotkey": "ESC",
            "command": "ai_stop_control"
        },
        "time_limits": {
            "description": "Maximum session duration limits",
            "default_limit": "1 hour",
            "max_limit": "4 hours"
        },
        "application_whitelist": {
            "description": "Only control approved applications",
            "status": "enabled",
            "approved_apps": ["notepad", "calculator", "browser"]
        },
        "user_confirmation": {
            "description": "Require confirmation for sensitive operations",
            "enabled": True,
            "sensitive_operations": ["file_deletion", "system_changes", "network_operations"]
        },
        "activity_logging": {
            "description": "Log all autonomous actions for review",
            "enabled": True,
            "log_level": "detailed"
        }
    }