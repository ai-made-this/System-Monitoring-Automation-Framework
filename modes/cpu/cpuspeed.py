"""CPU Speed Monitor - Returns current CPU clock speed"""
import psutil

def get_cpu_speed():
    """Get current CPU frequency in MHz"""
    try:
        freq = psutil.cpu_freq()
        return {
            "current_mhz": freq.current,
            "min_mhz": freq.min,
            "max_mhz": freq.max
        }
    except Exception as e:
        return {"error": str(e)}