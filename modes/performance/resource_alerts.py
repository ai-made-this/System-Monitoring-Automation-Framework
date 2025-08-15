"""Resource Alerts Monitor - Checks for resource usage alerts"""
import psutil
import json
from pathlib import Path

def _create_alert(alerts, resource_type, value, thresholds, message_template, device=None):
    """Helper to check a value against thresholds and create an alert if needed."""
    critical_threshold = thresholds.get('critical', 101)  # Default to an unreachable value
    warning_threshold = thresholds.get('warning', 101)

    level = None
    threshold = None
    if value > critical_threshold:
        level = "critical"
        threshold = critical_threshold
    elif value > warning_threshold:
        level = "warning"
        threshold = warning_threshold

    if level:
        alert = {
            "type": resource_type,
            "level": level,
            "message": message_template.format(value=value, device=device),
            "value": round(value, 2),
            "threshold": threshold
        }
        if device:
            alert["device"] = device
        alerts.append(alert)

def get_resource_alerts():
    """Check for resource usage that exceeds thresholds"""
    try:
        # Load configurable thresholds, with safe defaults
        config_path = Path(__file__).parent / "resource_alerts_config.json"
        thresholds = {
            "cpu": {"warning": 80, "critical": 90},
            "memory": {"warning": 85, "critical": 95},
            "disk": {"warning": 90, "critical": 95}
        }
        if config_path.is_file():
            try:
                with open(config_path) as f:
                    config_data = json.load(f)
                    for key, value in config_data.items():
                        if key in thresholds:
                            thresholds[key].update(value)
            except (json.JSONDecodeError, IOError):
                pass  # Use defaults if config is malformed or unreadable

        alerts = []

        # CPU usage alert
        cpu_percent = psutil.cpu_percent(interval=1)
        _create_alert(alerts, "cpu", cpu_percent, thresholds['cpu'], "High CPU usage: {value:.1f}%")

        # Memory usage alert
        memory = psutil.virtual_memory()
        _create_alert(alerts, "memory", memory.percent, thresholds['memory'], "High memory usage: {value:.1f}%")

        # Disk usage alerts
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                _create_alert(
                    alerts, "disk", usage.percent, thresholds['disk'],
                    "High disk usage on {device}: {value:.1f}%",
                    device=partition.device
                )
            except (PermissionError, FileNotFoundError):
                # Ignore drives that are not accessible (e.g., empty CD-ROM)
                pass

        return {
            "alerts": alerts,
            "alert_count": len(alerts),
            "status": "critical" if any(a["level"] == "critical" for a in alerts) else "warning" if alerts else "ok"
        }
    except Exception as e:
        return {"error": str(e)}
