"""Network Latency Monitor - Measures ping/latency"""
import subprocess
import platform

def get_net_latency():
    """Get network latency by pinging Google DNS"""
    try:
        # Use appropriate ping command for OS
        if platform.system().lower() == "windows":
            cmd = ["ping", "-n", "4", "8.8.8.8"]
        else:
            cmd = ["ping", "-c", "4", "8.8.8.8"]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            # Parse ping output for average time
            output = result.stdout
            if "Average" in output:  # Windows
                avg_line = [line for line in output.split('\n') if 'Average' in line][0]
                avg_time = avg_line.split('=')[-1].strip().replace('ms', '')
            else:  # Unix-like
                avg_line = [line for line in output.split('\n') if 'avg' in line]
                if avg_line:
                    avg_time = avg_line[0].split('/')[-2]
                else:
                    avg_time = "unknown"
            
            return {
                "latency_ms": avg_time,
                "status": "success"
            }
        else:
            return {"error": "ping failed", "status": "failed"}
    except Exception as e:
        return {"error": str(e)}