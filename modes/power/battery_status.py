"""Battery Status Monitor - Returns battery information"""
import psutil

def get_battery_status():
    """Get battery status information"""
    try:
        battery = psutil.sensors_battery()
        if battery is None:
            return {"error": "No battery detected (desktop system?)"}
        
        return {
            "percent": battery.percent,
            "plugged_in": battery.power_plugged,
            "time_left_seconds": battery.secsleft if battery.secsleft != psutil.POWER_TIME_UNLIMITED else None,
            "time_left_formatted": f"{battery.secsleft // 3600}h {(battery.secsleft % 3600) // 60}m" if battery.secsleft not in [psutil.POWER_TIME_UNLIMITED, psutil.POWER_TIME_UNKNOWN] else "Unknown"
        }
    except Exception as e:
        return {"error": str(e)}