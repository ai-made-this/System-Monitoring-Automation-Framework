"""Disk Total Monitor - Returns total disk space for all drives"""
import psutil

def get_disk_total():
    """Get total disk space for all drives"""
    try:
        disks = {}
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disks[partition.device] = {
                    "total_bytes": usage.total,
                    "total_gb": round(usage.total / (1024**3), 2),
                    "total_tb": round(usage.total / (1024**4), 3),
                    "filesystem": partition.fstype,
                    "mountpoint": partition.mountpoint
                }
            except PermissionError:
                disks[partition.device] = {"error": "permission_denied"}
        return {"disks": disks}
    except Exception as e:
        return {"error": str(e)}