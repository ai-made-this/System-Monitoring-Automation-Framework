"""Disk I/O Monitor - Returns disk read/write statistics"""
import psutil

def get_disk_io():
    """Get disk I/O statistics"""
    try:
        io = psutil.disk_io_counters()
        return {
            "read_bytes": io.read_bytes,
            "write_bytes": io.write_bytes,
            "read_count": io.read_count,
            "write_count": io.write_count,
            "read_gb": round(io.read_bytes / (1024**3), 2),
            "write_gb": round(io.write_bytes / (1024**3), 2)
        }
    except Exception as e:
        return {"error": str(e)}