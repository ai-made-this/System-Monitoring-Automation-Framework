"""Network Latency Monitor - Measures ping/latency"""
import subprocess
import platform
import re

def get_net_latency():
    """Get network latency by pinging Google DNS"""
    try:
        target_host = "8.8.8.8"
        # Use appropriate ping command for OS
        if platform.system().lower() == "windows":
            cmd = ["ping", "-n", "4", target_host]
        else:
            cmd = ["ping", "-c", "4", target_host]

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)

        if result.returncode == 0:
            output = result.stdout
            avg_time = None

            # Regex for Windows: "Average = 23ms"
            win_match = re.search(r"Average = (\d+)ms", output)
            # Regex for Unix: "rtt min/avg/max/mdev = 14.3/15.1/16.2/0.5 ms"
            unix_match = re.search(r"min/avg/max/mdev = [\d.]+/([\d.]+)/", output)

            if win_match:
                avg_time = float(win_match.group(1))
            elif unix_match:
                avg_time = float(unix_match.group(1))

            if avg_time is not None:
                return {"latency_ms": avg_time, "status": "success"}
            else:
                return {"error": "Could not parse ping output", "status": "failed"}
        else:
            return {"error": "ping command failed", "status": "failed", "details": result.stderr.strip()}
    except Exception as e:
        return {"error": str(e)}
