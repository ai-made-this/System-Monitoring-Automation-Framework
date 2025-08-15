"""Application Usage Monitor - Tracks per-app resource usage"""
import psutil

def get_app_usage():
    """Get per-application resource usage"""
    try:
        apps = {}
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'memory_info']):
            try:
                name = proc.info['name']
                if name not in apps:
                    apps[name] = {
                        "instances": 0,
                        "total_cpu": 0,
                        "total_memory_mb": 0,
                        "pids": []
                    }
                
                apps[name]["instances"] += 1
                apps[name]["total_cpu"] += proc.info['cpu_percent'] or 0
                apps[name]["total_memory_mb"] += (proc.info['memory_info'].rss / 1024 / 1024) if proc.info['memory_info'] else 0
                apps[name]["pids"].append(proc.info['pid'])
                
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        # Sort by CPU usage
        sorted_apps = sorted(apps.items(), key=lambda x: x[1]['total_cpu'], reverse=True)
        
        return {
            "applications": dict(sorted_apps[:20]),  # Top 20 apps
            "total_applications": len(apps)
        }
    except Exception as e:
        return {"error": str(e)}