"""Action Replay - Replays recorded user actions"""
import json
import time
from pathlib import Path

RECORDINGS_DIR = Path(__file__).parent / "recordings"

def get_action_replay():
    """Get available recordings and replay capabilities"""
    try:
        if not RECORDINGS_DIR.exists():
            RECORDINGS_DIR.mkdir(exist_ok=True)
            return {"recordings": [], "status": "no_recordings"}
        
        recordings = []
        for file in RECORDINGS_DIR.glob("*.json"):
            try:
                with open(file, 'r') as f:
                    data = json.load(f)
                    recordings.append({
                        "name": file.stem,
                        "duration": data.get("duration", 0),
                        "action_count": len(data.get("actions", [])),
                        "created": data.get("created", "unknown")
                    })
            except Exception as e:
                recordings.append({
                    "name": file.stem,
                    "error": str(e)
                })
        
        return {
            "available_recordings": recordings,
            "recording_count": len(recordings),
            "recordings_dir": str(RECORDINGS_DIR)
        }
    except Exception as e:
        return {"error": str(e)}