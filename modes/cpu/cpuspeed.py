import psutil

def get_cpu_speed():
    """
    Get current CPU frequency in MHz.
    Returns:
        dict: {"current_mhz": float, "min_mhz": float, "max_mhz": float} or {"error": str}
    """
    try:
        freq = psutil.cpu_freq()
        if freq:
            return {
                "current_mhz": freq.current,
                "min_mhz": freq.min,
                "max_mhz": freq.max
            }
        else:
            return {"error": "CPU frequency could not be determined."}
    except Exception as e:
        return {"error": str(e)}
