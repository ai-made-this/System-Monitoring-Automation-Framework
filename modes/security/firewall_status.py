"""Firewall Status Monitor - Checks firewall status"""
import subprocess
import platform

def get_firewall_status():
    """Get firewall status"""
    try:
        if platform.system() == "Windows":
            result = subprocess.run(
                ["netsh", "advfirewall", "show", "allprofiles", "state"],
                capture_output=True, text=True, timeout=10
            )
            
            if result.returncode == 0:
                output = result.stdout
                profiles = {}
                current_profile = None
                
                for line in output.split('\n'):
                    if 'Profile Settings' in line:
                        current_profile = line.split()[0]
                    elif 'State' in line and current_profile:
                        state = line.split()[-1]
                        profiles[current_profile] = state
                
                return {
                    "platform": "Windows",
                    "profiles": profiles,
                    "status": "active" if any(state == "ON" for state in profiles.values()) else "inactive"
                }
            else:
                return {"error": "Failed to check firewall status"}
        else:
            return {"error": f"Firewall check not implemented for {platform.system()}"}
    except Exception as e:
        return {"error": str(e)}