"""Boot Time Monitor - Measures system boot performance"""
import psutil
import platform
import subprocess
from datetime import datetime

def get_boot_time():
    """Get boot time and startup performance metrics"""
    try:
        boot_timestamp = psutil.boot_time()
        boot_datetime = datetime.fromtimestamp(boot_timestamp)
        
        result = {
            "boot_timestamp": boot_timestamp,
            "boot_time": boot_datetime.isoformat(),
            "platform": platform.system()
        }
        
        # Windows-specific boot time analysis
        if platform.system() == "Windows":
            try:
                # Get last boot time from system log
                ps_script = """
                Get-WinEvent -FilterHashtable @{LogName='System'; ID=6005} -MaxEvents 1 | 
                Select-Object TimeCreated | ConvertTo-Json
                """
                
                ps_result = subprocess.run(
                    ["powershell", "-Command", ps_script],
                    capture_output=True, text=True, timeout=10
                )
                
                if ps_result.returncode == 0:
                    import json
                    event_data = json.loads(ps_result.stdout)
                    result["last_boot_event"] = event_data.get("TimeCreated")
            except:
                pass
        
        return result
    except Exception as e:
        return {"error": str(e)}