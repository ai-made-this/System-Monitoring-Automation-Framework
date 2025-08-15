"""Network Usage Monitor - Tracks cumulative bandwidth usage since boot"""
import psutil

def _format_stats(stats):
    """Helper to format a psutil net_io_counters object into a dictionary."""
    return {
        "bytes_sent": stats.bytes_sent,
        "bytes_recv": stats.bytes_recv,
        "gb_sent": round(stats.bytes_sent / (1024**3), 3),
        "gb_recv": round(stats.bytes_recv / (1024**3), 3),
        "packets_sent": stats.packets_sent,
        "packets_recv": stats.packets_recv,
        "errors_in": stats.errin,
        "errors_out": stats.errout,
        "dropped_in": stats.dropin,
        "dropped_out": stats.dropout
    }

def get_net_usage():
    """Get cumulative network I/O statistics, for all and per-interface."""
    try:
        # Get total usage for all interfaces
        total_stats = psutil.net_io_counters(pernic=False)

        # Get usage per interface
        per_nic_stats = psutil.net_io_counters(pernic=True)

        interfaces_data = []
        for nic_name, stats in per_nic_stats.items():
            interface_data = _format_stats(stats)
            interface_data['name'] = nic_name
            interfaces_data.append(interface_data)

        return {
            "total_usage": _format_stats(total_stats),
            "interfaces": interfaces_data
        }
    except Exception as e:
        return {"error": str(e)}
