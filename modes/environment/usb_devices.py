"""USB Devices Monitor - Lists connected USB devices"""
import platform
import subprocess

def get_usb_devices():
    """Get connected USB devices"""
    try:
        if platform.system() == "Windows":
            # Get USB devices using PowerShell
            ps_script = """
            Get-WmiObject -Class Win32_USBControllerDevice | ForEach-Object {
                [wmi]($_.Dependent)
            } | Where-Object {$_.Description -ne $null} | Select-Object Description, DeviceID | ConvertTo-Json
            """
            
            result = subprocess.run(
                ["powershell", "-Command", ps_script],
                capture_output=True, text=True, timeout=15
            )
            
            if result.returncode == 0:
                import json
                try:
                    devices = json.loads(result.stdout)
                    if not isinstance(devices, list):
                        devices = [devices] if devices else []
                    
                    return {
                        "platform": "Windows",
                        "usb_devices": devices,
                        "device_count": len(devices)
                    }
                except json.JSONDecodeError:
                    return {"error": "Failed to parse USB device data"}
            else:
                return {"error": "Failed to get USB devices"}
        else:
            return {"error": f"USB device detection not implemented for {platform.system()}"}
    except Exception as e:
        return {"error": str(e)}