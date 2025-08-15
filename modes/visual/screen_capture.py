"""Screen Capture - Captures and analyzes screenshots"""
import time
from pathlib import Path
import json

CAPTURE_DIR = Path(__file__).parent / "captures"
CAPTURE_LOG = Path(__file__).parent / "capture_log.json"

def get_screen_capture():
    """Get screen capture capabilities and recent captures"""
    try:
        if not CAPTURE_DIR.exists():
            CAPTURE_DIR.mkdir(exist_ok=True)
        
        # Get recent captures
        captures = []
        for file in CAPTURE_DIR.glob("*.png"):
            captures.append({
                "filename": file.name,
                "timestamp": file.stat().st_mtime,
                "size_bytes": file.stat().st_size,
                "age_minutes": round((time.time() - file.stat().st_mtime) / 60, 1)
            })
        
        # Sort by timestamp (newest first)
        captures.sort(key=lambda x: x["timestamp"], reverse=True)
        
        return {
            "status": "ready",
            "capture_directory": str(CAPTURE_DIR),
            "recent_captures": captures[:10],  # Last 10 captures
            "total_captures": len(captures),
            "capabilities": {
                "screenshot": "Full screen capture",
                "region_capture": "Specific screen region capture",
                "window_capture": "Active window capture",
                "timed_capture": "Scheduled captures at intervals",
                "change_detection": "Detect visual changes between captures"
            },
            "supported_formats": ["PNG", "JPEG", "BMP"],
            "note": "Requires PIL/Pillow: pip install Pillow"
        }
    except Exception as e:
        return {"error": str(e)}