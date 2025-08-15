"""Power Plan Monitor - Returns current power plan"""
import subprocess
import platform

def get_power_plan():
    """Get current power plan"""
    try:
        if platform.system() == "Windows":
            result = subprocess.run(
                ["powercfg", "/getactivescheme"],
                capture_output=True, text=True, timeout=10
            )
            
            if result.returncode == 0:
                output = result.stdout.strip()
                # Extract power plan name from output
                if "(" in output and ")" in output:
                    plan_name = output.split("(")[1].split(")")[0]
                else:
                    plan_name = "Unknown"
                
                return {
                    "platform": "Windows",
                    "active_plan": plan_name,
                    "raw_output": output
                }
            else:
                return {"error": "Failed to get power plan"}
        else:
            return {"error": f"Power plan detection not implemented for {platform.system()}"}
    except Exception as e:
        return {"error": str(e)}