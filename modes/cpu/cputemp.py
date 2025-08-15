"""CPU Temperature Monitor - Returns CPU temperature"""
import psutil

def get_cpu_temp():
    """Get CPU temperature in Celsius"""
    try:
        temps = psutil.sensors_temperatures()
        if 'coretemp' in temps:
            return {
                "temp_celsius": temps['coretemp'][0].current,
                "high_threshold": temps['coretemp'][0].high,
                "critical_threshold": temps['coretemp'][0].critical
            }
        return {"temp_celsius": "unavailable", "reason": "no temperature sensors found"}
    except Exception as e:
        return {"error": str(e)}