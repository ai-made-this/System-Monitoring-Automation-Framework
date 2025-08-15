"""CPU Usage Monitor - Returns CPU usage percentage"""
import psutil

def get_cpu_usage():
    """Get CPU usage percentage"""
    try:
        return {
            "usage_percent": psutil.cpu_percent(interval=1),
            "per_core": psutil.cpu_percent(interval=1, percpu=True),
            "core_count": psutil.cpu_count()
        }
    except Exception as e:
        return {"error": str(e)}