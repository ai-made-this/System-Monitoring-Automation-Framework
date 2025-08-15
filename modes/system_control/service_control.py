"""Service Control Module - Manage system services"""
import subprocess
import platform
from datetime import datetime

def get_service_status(service_name):
    """Get status of a system service"""
    try:
        if platform.system() == "Windows":
            result = subprocess.run(
                ["sc", "query", service_name],
                capture_output=True, text=True, timeout=10
            )
            
            if result.returncode == 0:
                output = result.stdout
                status = "unknown"
                
                if "RUNNING" in output:
                    status = "running"
                elif "STOPPED" in output:
                    status = "stopped"
                elif "PAUSED" in output:
                    status = "paused"
                
                return {
                    "success": True,
                    "service_name": service_name,
                    "status": status,
                    "platform": "Windows",
                    "raw_output": output.strip()
                }
            else:
                return {"error": f"Service {service_name} not found or access denied"}
        else:
            # Linux/Unix systems
            result = subprocess.run(
                ["systemctl", "is-active", service_name],
                capture_output=True, text=True, timeout=10
            )
            
            status = result.stdout.strip()
            return {
                "success": True,
                "service_name": service_name,
                "status": status,
                "platform": platform.system()
            }
    except Exception as e:
        return {"error": str(e)}

def start_service(service_name):
    """Start a system service"""
    try:
        if platform.system() == "Windows":
            result = subprocess.run(
                ["sc", "start", service_name],
                capture_output=True, text=True, timeout=30
            )
            
            success = result.returncode == 0
            return {
                "success": success,
                "service_name": service_name,
                "action": "start",
                "platform": "Windows",
                "output": result.stdout.strip(),
                "error": result.stderr.strip() if not success else None,
                "timestamp": datetime.now().isoformat()
            }
        else:
            result = subprocess.run(
                ["sudo", "systemctl", "start", service_name],
                capture_output=True, text=True, timeout=30
            )
            
            success = result.returncode == 0
            return {
                "success": success,
                "service_name": service_name,
                "action": "start",
                "platform": platform.system(),
                "output": result.stdout.strip(),
                "error": result.stderr.strip() if not success else None,
                "timestamp": datetime.now().isoformat()
            }
    except Exception as e:
        return {"error": str(e)}

def stop_service(service_name):
    """Stop a system service"""
    try:
        if platform.system() == "Windows":
            result = subprocess.run(
                ["sc", "stop", service_name],
                capture_output=True, text=True, timeout=30
            )
            
            success = result.returncode == 0
            return {
                "success": success,
                "service_name": service_name,
                "action": "stop",
                "platform": "Windows",
                "output": result.stdout.strip(),
                "error": result.stderr.strip() if not success else None,
                "timestamp": datetime.now().isoformat()
            }
        else:
            result = subprocess.run(
                ["sudo", "systemctl", "stop", service_name],
                capture_output=True, text=True, timeout=30
            )
            
            success = result.returncode == 0
            return {
                "success": success,
                "service_name": service_name,
                "action": "stop",
                "platform": platform.system(),
                "output": result.stdout.strip(),
                "error": result.stderr.strip() if not success else None,
                "timestamp": datetime.now().isoformat()
            }
    except Exception as e:
        return {"error": str(e)}

def list_services(status_filter=None):
    """List system services"""
    try:
        services = []
        
        if platform.system() == "Windows":
            result = subprocess.run(
                ["sc", "query"],
                capture_output=True, text=True, timeout=30
            )
            
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                current_service = {}
                
                for line in lines:
                    line = line.strip()
                    if line.startswith("SERVICE_NAME:"):
                        if current_service:
                            services.append(current_service)
                        current_service = {"name": line.split(":", 1)[1].strip()}
                    elif line.startswith("DISPLAY_NAME:"):
                        current_service["display_name"] = line.split(":", 1)[1].strip()
                    elif line.startswith("STATE"):
                        state_info = line.split()
                        if len(state_info) >= 4:
                            current_service["status"] = state_info[3].lower()
                
                if current_service:
                    services.append(current_service)
        else:
            result = subprocess.run(
                ["systemctl", "list-units", "--type=service", "--all"],
                capture_output=True, text=True, timeout=30
            )
            
            if result.returncode == 0:
                lines = result.stdout.split('\n')[1:]  # Skip header
                for line in lines:
                    parts = line.split()
                    if len(parts) >= 4:
                        services.append({
                            "name": parts[0],
                            "status": parts[2],
                            "description": " ".join(parts[4:]) if len(parts) > 4 else ""
                        })
        
        # Filter by status if requested
        if status_filter:
            services = [s for s in services if s.get("status") == status_filter.lower()]
        
        return {
            "success": True,
            "platform": platform.system(),
            "service_count": len(services),
            "services": services,
            "status_filter": status_filter
        }
    except Exception as e:
        return {"error": str(e)}

def get_service_control():
    """Get service control capabilities"""
    try:
        return {
            "functions": {
                "get_service_status": "get_service_status(service_name)",
                "start_service": "start_service(service_name)",
                "stop_service": "stop_service(service_name)",
                "list_services": "list_services(status_filter=None)"
            },
            "supported_platforms": ["Windows", "Linux", "Unix"],
            "status_filters": ["running", "stopped", "paused", "active", "inactive"],
            "examples": {
                "check_status": "get_service_status('Spooler')",
                "start_service": "start_service('Spooler')",
                "list_running": "list_services(status_filter='running')"
            },
            "note": "Administrative privileges may be required for start/stop operations"
        }
    except Exception as e:
        return {"error": str(e)}