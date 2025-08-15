"""Process Manager - Advanced process control and monitoring"""
import psutil
import time

def get_process_manager():
    """Get detailed process management information"""
    try:
        processes = []
        total_cpu = 0
        total_memory = 0
        
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status', 'create_time']):
            try:
                info = proc.info
                if info['cpu_percent'] is not None:
                    total_cpu += info['cpu_percent']
                if info['memory_percent'] is not None:
                    total_memory += info['memory_percent']
                
                # Calculate process age
                create_time = info.get('create_time', time.time())
                age_seconds = time.time() - create_time
                age_hours = age_seconds / 3600
                
                processes.append({
                    "pid": info['pid'],
                    "name": info['name'],
                    "cpu_percent": info['cpu_percent'] or 0,
                    "memory_percent": info['memory_percent'] or 0,
                    "status": info['status'],
                    "age_hours": round(age_hours, 2)
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        # Sort by CPU usage
        processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
        
        # Count by status
        status_counts = {}
        for proc in processes:
            status = proc['status']
            status_counts[status] = status_counts.get(status, 0) + 1
        
        return {
            "total_processes": len(processes),
            "top_cpu_processes": processes[:10],
            "status_breakdown": status_counts,
            "system_cpu_total": round(total_cpu, 2),
            "system_memory_total": round(total_memory, 2)
        }
    except Exception as e:
        return {"error": str(e)}