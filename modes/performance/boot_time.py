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

        # Windows-specific boot duration analysis for a more valuable performance metric.
        if platform.system() == "Windows":
            # This enhancement might fail if PowerShell is unavailable or logs are restricted.
            # We catch specific errors to ensure the base psutil data is always returned.
            try:
                # Get last boot duration from the performance diagnostics log (Event ID 100)
                ps_script = """
                $bootEvent = Get-WinEvent -ProviderName Microsoft-Windows-Diagnostics-Performance -LogName 'Microsoft-Windows-Diagnostics-Performance/Operational' -FilterXPath "*[System[EventID=100]]" -MaxEvents 1
                if ($bootEvent) {
                    $durationMs = $bootEvent.Properties[0].Value
                    @{ BootDurationMS = $durationMs } | ConvertTo-Json
                }
                """

                ps_result = subprocess.run(
                    ["powershell", "-Command", ps_script],
                    capture_output=True, text=True, timeout=15, check=False
                )

                if ps_result.returncode == 0 and ps_result.stdout:
                    import json
                    event_data = json.loads(ps_result.stdout.strip())
                    if "BootDurationMS" in event_data:
                        result["boot_duration_ms"] = int(event_data["BootDurationMS"])
            except (subprocess.TimeoutExpired, FileNotFoundError, json.JSONDecodeError):
                pass

        return result
    except Exception as e:
        return {"error": str(e)}
