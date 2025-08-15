"""System Service - Main service controller for always-on monitoring and learning"""
import json
import time
import os
import sys
from pathlib import Path

SERVICE_CONFIG = Path(__file__).parent / "system_service_config.json"
SERVICE_STATUS = Path(__file__).parent / "service_status.json"

def get_system_service():
    """Get system service status and controls"""
    try:
        # Load service configuration
        if SERVICE_CONFIG.exists():
            with open(SERVICE_CONFIG, 'r') as f:
                config = json.load(f)
        else:
            config = {
                "auto_start": False,
                "monitoring_enabled": True,
                "learning_enabled": True,
                "service_port": 8080,
                "log_level": "INFO",
                "data_retention_days": 30
            }
            with open(SERVICE_CONFIG, 'w') as f:
                json.dump(config, f, indent=2)
        
        # Check service status
        service_status = _get_service_status()
        
        return {
            "status": service_status["status"],
            "configuration": config,
            "service_info": service_status,
            "installation_options": {
                "windows_service": {
                    "description": "Install as Windows Service for automatic startup",
                    "command": "python service_installer.py install",
                    "benefits": ["Starts automatically with Windows", "Runs in background", "Survives user logoff"]
                },
                "startup_script": {
                    "description": "Add to Windows startup folder",
                    "location": "shell:startup",
                    "benefits": ["Simple installation", "User-level startup", "Easy to modify"]
                },
                "task_scheduler": {
                    "description": "Use Windows Task Scheduler",
                    "benefits": ["Flexible scheduling", "Conditional startup", "Built-in logging"]
                }
            },
            "service_features": {
                "always_on_monitoring": "24/7 system monitoring and data collection",
                "continuous_learning": "ML models continuously improve from your usage",
                "automatic_optimization": "System automatically optimizes based on patterns",
                "predictive_alerts": "Get warned before problems occur",
                "behavioral_adaptation": "System adapts to your changing habits",
                "low_resource_usage": "Minimal impact on system performance"
            },
            "data_collection": {
                "system_metrics": "CPU, memory, disk, network usage every 30 seconds",
                "user_activity": "Application usage, input patterns, session times",
                "performance_data": "Response times, error rates, resource bottlenecks",
                "behavioral_patterns": "Usage habits, productivity cycles, preferences"
            },
            "learning_process": {
                "data_analysis": "Analyze collected data for patterns every hour",
                "model_updates": "Update ML models with new insights",
                "pattern_recognition": "Identify new usage patterns automatically",
                "anomaly_detection": "Learn what's normal to detect what's not",
                "predictive_modeling": "Build models to predict future needs"
            },
            "privacy_controls": {
                "local_processing": "All data stays on your computer",
                "selective_monitoring": "Choose what to monitor and what to ignore",
                "data_retention": "Automatic cleanup of old data",
                "anonymization": "Personal information is anonymized",
                "opt_out": "Disable monitoring for specific applications or times"
            }
        }
    except Exception as e:
        return {"error": str(e)}

def _get_service_status():
    """Get current service status"""
    try:
        # Check if background processes are running
        from .background_monitor import get_service_status as get_monitor_status
        from .continuous_learning import get_learning_status
        
        monitor_status = get_monitor_status()
        learning_status = get_learning_status()
        
        overall_status = "running" if (monitor_status["running"] and learning_status["active"]) else "stopped"
        
        status = {
            "status": overall_status,
            "monitoring_active": monitor_status["running"],
            "learning_active": learning_status["active"],
            "uptime_hours": _calculate_uptime(),
            "data_points_collected": monitor_status.get("data_buffer_size", 0),
            "models_learning": learning_status.get("queue_size", 0),
            "last_activity": max(
                monitor_status.get("last_collection", 0),
                learning_status.get("last_update", 0)
            )
        }
        
        # Save status
        with open(SERVICE_STATUS, 'w') as f:
            json.dump(status, f, indent=2)
        
        return status
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

def _calculate_uptime():
    """Calculate service uptime in hours"""
    try:
        if SERVICE_STATUS.exists():
            with open(SERVICE_STATUS, 'r') as f:
                status = json.load(f)
                start_time = status.get("start_time", time.time())
        else:
            start_time = time.time()
        
        return round((time.time() - start_time) / 3600, 2)
    except:
        return 0

def start_all_services():
    """Start all background services"""
    try:
        from .background_monitor import start_service as start_monitor
        from .continuous_learning import start_learning
        
        monitor_started = start_monitor()
        learning_started = start_learning()
        
        # Update service status
        status = {
            "start_time": time.time(),
            "monitoring_started": monitor_started,
            "learning_started": learning_started,
            "status": "running" if (monitor_started and learning_started) else "partial"
        }
        
        with open(SERVICE_STATUS, 'w') as f:
            json.dump(status, f, indent=2)
        
        return {
            "success": True,
            "monitoring": monitor_started,
            "learning": learning_started,
            "message": "Services started successfully" if (monitor_started and learning_started) else "Some services failed to start"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def stop_all_services():
    """Stop all background services"""
    try:
        from .background_monitor import stop_service as stop_monitor
        from .continuous_learning import stop_learning
        
        monitor_stopped = stop_monitor()
        learning_stopped = stop_learning()
        
        return {
            "success": True,
            "monitoring": monitor_stopped,
            "learning": learning_stopped,
            "message": "Services stopped successfully"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def install_as_service():
    """Install as Windows service (placeholder)"""
    return {
        "message": "Service installation requires administrator privileges",
        "instructions": [
            "1. Run command prompt as administrator",
            "2. Navigate to the system directory",
            "3. Run: python service_installer.py install",
            "4. Start service: net start SystemMonitoringService"
        ],
        "alternative": "Use Task Scheduler or startup folder for simpler installation"
    }