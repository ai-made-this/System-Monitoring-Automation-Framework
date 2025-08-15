import psutil

def get_cpu_usage():
    """
    Get CPU usage percentage and per-core usage.
    Returns:
        dict: {"usage_percent": float, "per_core": list, "core_count": int} or {"error": str}
    """
    try:
        per_core_usage = psutil.cpu_percent(interval=1, percpu=True)
        return {
            "usage_percent": sum(per_core_usage) / len(per_core_usage) if per_core_usage else 0,
            "per_core": per_core_usage,
            "core_count": psutil.cpu_count()
        }
    except Exception as e:
        return {"error": str(e)}
