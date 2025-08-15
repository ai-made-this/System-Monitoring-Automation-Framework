"""Active Window Monitor - Tracks currently active window"""
import platform

def get_active_window():
    """Get currently active window information"""
    try:
        if platform.system() == "Windows":
            try:
                import win32gui
                hwnd = win32gui.GetForegroundWindow()
                window_title = win32gui.GetWindowText(hwnd)
                return {
                    "title": window_title,
                    "platform": "Windows",
                    "window_id": hwnd
                }
            except ImportError:
                return {"error": "win32gui not available. Install: pip install pywin32"}
        else:
            return {"error": f"Active window detection not implemented for {platform.system()}"}
    except Exception as e:
        return {"error": str(e)}