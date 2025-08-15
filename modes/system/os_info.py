"""OS Info Monitor - Returns OS name/version"""
import platform
import psutil

def get_os_info():
    """Get operating system information"""
    try:
        return {
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "architecture": platform.architecture()[0],
            "hostname": platform.node(),
            "python_version": platform.python_version()
        }
    except Exception as e:
        return {"error": str(e)}