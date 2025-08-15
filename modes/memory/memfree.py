"""Memory Free Monitor - Returns available memory"""
import psutil

def get_mem_free():
    """Get available/free memory"""
    try:
        mem = psutil.virtual_memory()
        return {
            "available_bytes": mem.available,
            "available_gb": round(mem.available / (1024**3), 2),
            "free_bytes": mem.free,
            "free_gb": round(mem.free / (1024**3), 2)
        }
    except Exception as e:
        return {"error": str(e)}