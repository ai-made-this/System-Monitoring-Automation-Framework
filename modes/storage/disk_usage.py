"""Disk Usage Monitor - Returns disk usage percentage"""
import psutil

def get_disk_usage():
    """Get disk usage percentage for all drives"""
    try:
        disks = {}
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disks[partition.device] = {
                    "used_bytes": usage.used,
                    "used_gb": round(usage.used / (1024**3), 2),
                    "used_percent": round((usage.used / usage.total) * 100, 2)
                }
            except PermissionError:
                disks[partition.device] = {"error": "permission_denied"}
        return {"disks": disks}
    except Exception as e:
        return {"error": str(e)}