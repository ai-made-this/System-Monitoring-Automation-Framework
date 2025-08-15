"""Energy Usage Monitor - Estimates power consumption"""
import psutil
import time

def get_energy_usage():
    """Estimate energy usage based on system load"""
    try:
        cpu_percent = psutil.cpu_percent(interval=1)
        memory_percent = psutil.virtual_memory().percent
        
        # Rough estimation based on typical desktop power consumption
        base_power = 50  # Base system power in watts
        cpu_power = (cpu_percent / 100) * 65  # CPU can use up to 65W
        memory_power = (memory_percent / 100) * 10  # RAM uses ~10W
        
        estimated_watts = base_power + cpu_power + memory_power
        
        return {
            "estimated_watts": round(estimated_watts, 2),
            "cpu_contribution": round(cpu_power, 2),
            "memory_contribution": round(memory_power, 2),
            "base_consumption": base_power,
            "note": "Rough estimation based on system load"
        }
    except Exception as e:
        return {"error": str(e)}