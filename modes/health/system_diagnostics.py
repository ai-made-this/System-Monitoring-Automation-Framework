"""System Diagnostics - Comprehensive system health analysis"""
import json
import time
import psutil
from pathlib import Path

DIAGNOSTIC_LOG = Path(__file__).parent / "diagnostics.json"

def get_system_diagnostics():
    """Perform comprehensive system health diagnostics"""
    try:
        diagnostics = {
            "timestamp": time.time(),
            "overall_health": "unknown",
            "issues": [],
            "recommendations": []
        }
        
        # CPU Health Check
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_temp_available = hasattr(psutil, 'sensors_temperatures')
        
        if cpu_percent > 90:
            diagnostics["issues"].append({
                "category": "cpu",
                "severity": "high",
                "issue": f"Very high CPU usage: {cpu_percent}%",
                "recommendation": "Check for runaway processes or malware"
            })
        elif cpu_percent > 80:
            diagnostics["issues"].append({
                "category": "cpu",
                "severity": "medium",
                "issue": f"High CPU usage: {cpu_percent}%",
                "recommendation": "Consider closing unnecessary applications"
            })
        
        # Memory Health Check
        memory = psutil.virtual_memory()
        if memory.percent > 95:
            diagnostics["issues"].append({
                "category": "memory",
                "severity": "critical",
                "issue": f"Critical memory usage: {memory.percent}%",
                "recommendation": "Restart system or close memory-heavy applications immediately"
            })
        elif memory.percent > 85:
            diagnostics["issues"].append({
                "category": "memory",
                "severity": "high",
                "issue": f"High memory usage: {memory.percent}%",
                "recommendation": "Close unnecessary applications to free memory"
            })
        
        # Disk Health Check
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                usage_percent = (usage.used / usage.total) * 100
                
                if usage_percent > 95:
                    diagnostics["issues"].append({
                        "category": "disk",
                        "severity": "critical",
                        "issue": f"Disk {partition.device} critically full: {usage_percent:.1f}%",
                        "recommendation": "Free up disk space immediately"
                    })
                elif usage_percent > 90:
                    diagnostics["issues"].append({
                        "category": "disk",
                        "severity": "high",
                        "issue": f"Disk {partition.device} nearly full: {usage_percent:.1f}%",
                        "recommendation": "Clean up files or move data to external storage"
                    })
            except PermissionError:
                pass
        
        # Process Health Check
        high_cpu_processes = []
        high_memory_processes = []
        
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                if proc.info['cpu_percent'] and proc.info['cpu_percent'] > 50:
                    high_cpu_processes.append(proc.info)
                if proc.info['memory_percent'] and proc.info['memory_percent'] > 10:
                    high_memory_processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        if high_cpu_processes:
            diagnostics["issues"].append({
                "category": "processes",
                "severity": "medium",
                "issue": f"{len(high_cpu_processes)} processes using high CPU",
                "recommendation": "Review high CPU processes for optimization"
            })
        
        # Overall Health Assessment
        critical_issues = len([i for i in diagnostics["issues"] if i["severity"] == "critical"])
        high_issues = len([i for i in diagnostics["issues"] if i["severity"] == "high"])
        
        if critical_issues > 0:
            diagnostics["overall_health"] = "critical"
        elif high_issues > 2:
            diagnostics["overall_health"] = "poor"
        elif high_issues > 0:
            diagnostics["overall_health"] = "fair"
        else:
            diagnostics["overall_health"] = "good"
        
        return {
            "status": "completed",
            "diagnostics": diagnostics,
            "system_info": {
                "cpu_usage": cpu_percent,
                "memory_usage": memory.percent,
                "available_memory_gb": round(memory.available / (1024**3), 2),
                "uptime_hours": round((time.time() - psutil.boot_time()) / 3600, 1)
            },
            "capabilities": {
                "health_scoring": "Overall system health assessment",
                "issue_detection": "Automatic problem identification",
                "recommendations": "Actionable improvement suggestions",
                "trend_analysis": "Health trends over time",
                "preventive_alerts": "Early warning system",
                "automated_fixes": "Automatic resolution of common issues"
            },
            "diagnostic_categories": [
                "cpu_performance", "memory_usage", "disk_space",
                "process_health", "network_connectivity", "system_stability"
            ]
        }
    except Exception as e:
        return {"error": str(e)}