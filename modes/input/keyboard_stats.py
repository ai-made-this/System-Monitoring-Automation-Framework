"""Keyboard Statistics - Basic keyboard usage stats"""
import time
import json
from pathlib import Path

STATS_FILE = Path(__file__).parent / "keyboard_stats.json"

def get_keyboard_stats():
    """Get keyboard usage statistics"""
    try:
        if STATS_FILE.exists():
            with open(STATS_FILE, 'r') as f:
                stats = json.load(f)
        else:
            stats = {
                "total_keystrokes": 0,
                "session_start": time.time(),
                "last_activity": time.time(),
                "keys_per_minute": 0
            }
        
        # Calculate keys per minute
        elapsed_minutes = (time.time() - stats["session_start"]) / 60
        if elapsed_minutes > 0:
            stats["keys_per_minute"] = round(stats["total_keystrokes"] / elapsed_minutes, 2)
        
        return stats
    except Exception as e:
        return {"error": str(e)}