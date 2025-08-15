"""Service Manager - Monitors and manages system services"""
import subprocess
import platform

def get_service_manager():
    """Get system services status"""
    try:
        if platform.system() == "Windows":
            # Get Windows services
            result = subprocess.run([
                "sc", "query", "state=", "all"
            ], capture_output=True, text=True, timeout=15)
            
            if result.returncode == 0:
                services = []
                lines = result.stdout.split('\n')
                current_service = {}
                
                for line in lines:
                    line = line.strip()
                    if line.startswith("SERVICE_NAME:"):
                        if current_service:
                            services.append(current_service)
                        current_service = {"name": line.split(":", 1)[1].strip()}
                    elif line.startswith("STATE"):
                        state_info = line.split(":", 1)[1].strip()
                        current_service["state"] = state_info.split()[0]
                
                if current_service:
                    services.append(current_service)
                
                running_services = [s for s in services if s.get("state") == "RUNNING"]
                
                return {
                    "platform": "Windows",
                    "total_services": len(services),
                    "running_services": len(running_services),
                    "top_services": services[:20]  # First 20 services
                }
            else:
                return {"error": "Failed to query services"}
        else:
            return {"error": f"Service management not implemented for {platform.system()}"}
    except Exception as e:
        return {"error": str(e)}