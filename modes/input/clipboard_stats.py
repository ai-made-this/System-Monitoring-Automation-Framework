"""Clipboard Statistics - Basic clipboard usage stats"""
import time
import json
from pathlib import Path

STATS_FILE = Path(__file__).parent / "clipboard_stats.json"

def get_clipboard_stats():
    """Get clipboard usage statistics"""
    try:
        if STATS_FILE.exists():
            with open(STATS_FILE, 'r') as f:
                stats = json.load(f)
        else:
            stats = {
                "copy_events": 0,
                "paste_events": 0,
                "last_copy_time": None,
                "last_paste_time": None,
                "session_start": time.time()
            }
        
        return stats
    except Exception as e:
        return {"error": str(e)}