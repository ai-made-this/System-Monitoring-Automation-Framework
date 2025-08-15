"""Network Speed Monitor - Measures upload/download speed"""
import psutil
import time

def get_net_speed():
    """Get network speed by measuring bytes transferred over 1 second"""
    try:
        # For a more accurate measurement, record the actual time elapsed,
        # as time.sleep(1) is not guaranteed to be exactly one second.
        start_time = time.monotonic()
        # Get initial stats
        stats1 = psutil.net_io_counters()
        time.sleep(1)
        end_time = time.monotonic()
        stats2 = psutil.net_io_counters()

        elapsed_time = end_time - start_time
        if elapsed_time == 0:
            return {"error": "Measurement interval was zero, cannot calculate speed."}

        # Calculate speed
        upload_speed_bps = (stats2.bytes_sent - stats1.bytes_sent) / elapsed_time
        download_speed_bps = (stats2.bytes_recv - stats1.bytes_recv) / elapsed_time

        return {
            "upload_bytes_per_sec": round(upload_speed_bps),
            "download_bytes_per_sec": round(download_speed_bps),
            "upload_mbps": round((upload_speed_bps * 8) / (1024**2), 2),
            "download_mbps": round((download_speed_bps * 8) / (1024**2), 2)
        }
    except Exception as e:
        return {"error": str(e)}
