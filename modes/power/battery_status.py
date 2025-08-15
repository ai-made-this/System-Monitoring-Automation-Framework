"""Battery Status Monitor - Returns battery information"""
import psutil

def get_battery_status():
    """Get battery status information"""
    try:
        battery = psutil.sensors_battery()
        if battery is None:
            return {"error": "No battery detected (desktop system?)"}

        # Determine a clear status string
        if battery.power_plugged:
            status = "Fully Charged" if battery.percent == 100 else "Charging"
        else:
            status = "Discharging"

        # Handle special values for time left for clearer output
        secs_left = battery.secsleft
        if secs_left in [psutil.POWER_TIME_UNLIMITED, psutil.POWER_TIME_UNKNOWN]:
            time_left_seconds = None
            # Provide more context than just "Unknown"
            time_left_formatted = "N/A" if status == "Fully Charged" else "Calculating..."
        else:
            time_left_seconds = secs_left
            time_left_formatted = f"{secs_left // 3600}h {(secs_left % 3600) // 60}m"

        return {
            "status": status,
            "percent": round(battery.percent, 2),
            "plugged_in": battery.power_plugged,
            "time_left_seconds": time_left_seconds,
            "time_left_formatted": time_left_formatted
        }
    except Exception as e:
        return {"error": str(e)}
