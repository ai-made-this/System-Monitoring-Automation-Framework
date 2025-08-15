"""Disk Free Monitor - Returns available disk space"""
import psutil

def get_disk_free():
    """Get free disk space for all drives"""
    try:
        disks = {}
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disks[partition.device] = {
                    "free_bytes": usage.free,
                    "free_gb": round(usage.free / (1024**3), 2),
                    "free_percent": round((usage.free / usage.total) * 100, 2)
                }
            except PermissionError:
                disks[partition.device] = {"error": "permission_denied"}
        return {"disks": disks}
    except Exception as e:
        return {"error": str(e)}