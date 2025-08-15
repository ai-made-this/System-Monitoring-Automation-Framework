"""Performance Optimization - Game-specific performance optimizations"""
import json
import psutil
from pathlib import Path

OPTIMIZATION_LOG = Path(__file__).parent / "optimizations.json"

def get_performance_optimization():
    """Get game performance optimization status and recommendations"""
    try:
        # Get current system state
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        
        # Generate optimization recommendations
        recommendations = []
        
        if cpu_percent > 80:
            recommendations.append({
                "type": "cpu_optimization",
                "priority": "high",
                "description": "High CPU usage detected - consider closing background applications",
                "actions": ["close_unused_apps", "adjust_game_settings", "set_cpu_priority"]
            })
        
        if memory.percent > 85:
            recommendations.append({
                "type": "memory_optimization",
                "priority": "high",
                "description": "High memory usage - consider memory cleanup",
                "actions": ["clear_memory_cache", "close_memory_heavy_apps", "adjust_graphics_settings"]
            })
        
        # Load optimization history
        if OPTIMIZATION_LOG.exists():
            with open(OPTIMIZATION_LOG, 'r') as f:
                history = json.load(f)
        else:
            history = {"optimizations": []}
        
        return {
            "status": "monitoring",
            "current_recommendations": recommendations,
            "system_status": {
                "cpu_usage": cpu_percent,
                "memory_usage": memory.percent,
                "available_memory_gb": round(memory.available / (1024**3), 2)
            },
            "optimization_history": history["optimizations"][-5:],
            "capabilities": {
                "real_time_monitoring": "Monitor performance during gameplay",
                "automatic_optimization": "Apply optimizations automatically",
                "game_specific_profiles": "Custom optimization per game",
                "resource_prioritization": "Prioritize game processes",
                "background_management": "Manage background applications"
            },
            "optimization_types": [
                "cpu_priority", "memory_management", "graphics_optimization",
                "network_optimization", "disk_optimization", "power_management"
            ],
            "automatic_actions": [
                "Close unnecessary background apps",
                "Adjust Windows game mode",
                "Set process priority to high",
                "Clear system memory cache",
                "Disable Windows updates during gaming",
                "Optimize network settings for gaming"
            ],
            "performance_metrics": [
                "FPS monitoring", "Frame time analysis", "CPU/GPU usage",
                "Memory allocation", "Network latency", "Disk I/O"
            ]
        }
    except Exception as e:
        return {"error": str(e)}