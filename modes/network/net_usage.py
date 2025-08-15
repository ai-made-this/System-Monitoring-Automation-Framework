"""Network Usage Monitor - Tracks bandwidth usage"""
import psutil

def get_net_usage():
    """Get network usage statistics"""
    try:
        stats = psutil.net_io_counters()
        return {
            "bytes_sent": stats.bytes_sent,
            "bytes_recv": stats.bytes_recv,
            "packets_sent": stats.packets_sent,
            "packets_recv": stats.packets_recv,
            "gb_sent": round(stats.bytes_sent / (1024**3), 2),
            "gb_recv": round(stats.bytes_recv / (1024**3), 2)
        }
    except Exception as e:
        return {"error": str(e)}