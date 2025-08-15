"""Resource Alerts Monitor - Checks for resource usage alerts"""
import psutil

def get_resource_alerts():
    """Check for resource usage that exceeds thresholds"""
    try:
        alerts = []
        
        # CPU usage alert
        cpu_percent = psutil.cpu_percent(interval=1)
        if cpu_percent > 80:
            alerts.append({
                "type": "cpu",
                "level": "warning" if cpu_percent < 90 else "critical",
                "message": f"High CPU usage: {cpu_percent}%",
                "value": cpu_percent,
                "threshold": 80
            })
        
        # Memory usage alert
        memory = psutil.virtual_memory()
        if memory.percent > 85:
            alerts.append({
                "type": "memory",
                "level": "warning" if memory.percent < 95 else "critical",
                "message": f"High memory usage: {memory.percent}%",
                "value": memory.percent,
                "threshold": 85
            })
        
        # Disk usage alerts
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                usage_percent = (usage.used / usage.total) * 100
                if usage_percent > 90:
                    alerts.append({
                        "type": "disk",
                        "level": "warning" if usage_percent < 95 else "critical",
                        "message": f"High disk usage on {partition.device}: {usage_percent:.1f}%",
                        "value": usage_percent,
                        "threshold": 90,
                        "device": partition.device
                    })
            except PermissionError:
                pass
        
        return {
            "alerts": alerts,
            "alert_count": len(alerts),
            "status": "critical" if any(a["level"] == "critical" for a in alerts) else "warning" if alerts else "ok"
        }
    except Exception as e:
        return {"error": str(e)}