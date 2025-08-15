"""Memory Total Monitor - Returns total system memory"""
import psutil

def get_mem_total():
    """
    Get total system memory information.
    Returns:
        dict: {"total_bytes": int, "total_gb": float, "total_mb": float} or {"error": str}
    """
    try:
        mem = psutil.virtual_memory()
        return {
            "total_bytes": mem.total,
            "total_gb": round(mem.total / (1024**3), 2),
            "total_mb": round(mem.total / (1024**2), 2)
        }
    except Exception as e:
        return {"error": str(e)}