"""Screen Info Monitor - Returns display information"""
import platform

def get_screen_info():
    """Get screen/display information"""
    try:
        if platform.system() == "Windows":
            try:
                import win32api
                monitors = []
                for i, monitor in enumerate(win32api.EnumDisplayMonitors()):
                    monitor_info = win32api.GetMonitorInfo(monitor[0])
                    monitors.append({
                        "monitor_id": i,
                        "primary": monitor_info["Flags"] == 1,
                        "work_area": monitor_info["Work"],
                        "monitor_area": monitor_info["Monitor"]
                    })
                
                return {
                    "platform": "Windows",
                    "monitor_count": len(monitors),
                    "monitors": monitors
                }
            except ImportError:
                return {"error": "win32api not available. Install: pip install pywin32"}
        else:
            return {"error": f"Screen info not implemented for {platform.system()}"}
    except Exception as e:
        return {"error": str(e)}