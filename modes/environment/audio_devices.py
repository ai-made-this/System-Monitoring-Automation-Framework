"""Audio Devices Monitor - Lists audio input/output devices"""
import platform
import subprocess

def get_audio_devices():
    """Get audio device information"""
    try:
        if platform.system() == "Windows":
            # Get audio devices using PowerShell
            ps_script = """
            Get-WmiObject -Class Win32_SoundDevice | Select-Object Name, Status | ConvertTo-Json
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
                        devices = [devices]
                    
                    return {
                        "platform": "Windows",
                        "audio_devices": devices,
                        "device_count": len(devices)
                    }
                except json.JSONDecodeError:
                    return {"error": "Failed to parse audio device data"}
            else:
                return {"error": "Failed to get audio devices"}
        else:
            return {"error": f"Audio device detection not implemented for {platform.system()}"}
    except Exception as e:
        return {"error": str(e)}