"""System Uptime Monitor - Returns system uptime"""
import psutil
from datetime import datetime, timedelta

def get_uptime():
    """Get system uptime"""
    try:
        boot_time = psutil.boot_time()
        uptime_seconds = datetime.now().timestamp() - boot_time
        uptime_delta = timedelta(seconds=uptime_seconds)
        
        return {
            "boot_time": datetime.fromtimestamp(boot_time).isoformat(),
            "uptime_seconds": int(uptime_seconds),
            "uptime_formatted": str(uptime_delta).split('.')[0],
            "uptime_days": uptime_delta.days,
            "uptime_hours": uptime_delta.seconds // 3600
        }
    except Exception as e:
        return {"error": str(e)}