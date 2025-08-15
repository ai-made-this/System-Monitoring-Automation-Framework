"""Mouse Statistics - Basic mouse usage stats"""
import time
import json
from pathlib import Path

STATS_FILE = Path(__file__).parent / "mouse_stats.json"

def get_mouse_stats():
    """Get mouse usage statistics"""
    try:
        if STATS_FILE.exists():
            with open(STATS_FILE, 'r') as f:
                stats = json.load(f)
        else:
            stats = {
                "total_clicks": 0,
                "left_clicks": 0,
                "right_clicks": 0,
                "scroll_events": 0,
                "session_start": time.time(),
                "last_activity": time.time()
            }
        
        return stats
    except Exception as e:
        return {"error": str(e)}