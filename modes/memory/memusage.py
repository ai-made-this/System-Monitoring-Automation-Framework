"""Memory Usage Monitor - Returns memory usage percentage"""
import psutil

def get_mem_usage():
    """Get memory usage percentage"""
    try:
        mem = psutil.virtual_memory()
        return {
            "usage_percent": mem.percent,
            "used_bytes": mem.used,
            "used_gb": round(mem.used / (1024**3), 2)
        }
    except Exception as e:
        return {"error": str(e)}