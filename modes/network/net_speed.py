"""Network Speed Monitor - Measures upload/download speed"""
import psutil
import time

def get_net_speed():
    """Get network speed by measuring bytes transferred over 1 second"""
    try:
        # Get initial stats
        stats1 = psutil.net_io_counters()
        time.sleep(1)
        stats2 = psutil.net_io_counters()
        
        # Calculate speed
        bytes_sent = stats2.bytes_sent - stats1.bytes_sent
        bytes_recv = stats2.bytes_recv - stats1.bytes_recv
        
        return {
            "upload_bytes_per_sec": bytes_sent,
            "download_bytes_per_sec": bytes_recv,
            "upload_mbps": round((bytes_sent * 8) / (1024 * 1024), 2),
            "download_mbps": round((bytes_recv * 8) / (1024 * 1024), 2)
        }
    except Exception as e:
        return {"error": str(e)}