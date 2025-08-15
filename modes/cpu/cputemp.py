"""CPU Temperature Monitor - Returns CPU temperature"""
import psutil

def get_cpu_temp():
    """Get CPU temperature in Celsius"""
    try:
        temps = psutil.sensors_temperatures()
        # Prioritize 'coretemp' (common on Linux) and average the readings.
        if temps and 'coretemp' in temps and temps['coretemp']:
            core_temps = temps['coretemp']
            avg_temp = sum(t.current for t in core_temps) / len(core_temps)
            # High/critical thresholds are often the same across a package.
            high_thresh = core_temps[0].high
            crit_thresh = core_temps[0].critical
            return {
                "temp_celsius": round(avg_temp, 2),
                "high_threshold": high_thresh,
                "critical_threshold": crit_thresh
            }
        # Fallback for other systems (e.g., Windows) or if 'coretemp' is absent.
        elif temps:
            # Return the first available sensor reading.
            for sensor_name in temps:
                if temps[sensor_name]:
                    first_sensor = temps[sensor_name][0]
                    return {
                        "temp_celsius": first_sensor.current,
                        "high_threshold": first_sensor.high,
                        "critical_threshold": first_sensor.critical
                    }
        return {"error": "No compatible temperature sensors found."}
    except Exception as e:
        return {"error": str(e)}
