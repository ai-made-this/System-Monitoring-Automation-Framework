"""Process Monitor - Returns running processes info"""
import psutil

def get_processes():
    """Get running processes information"""
    try:
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        # Sort by CPU usage
        processes.sort(key=lambda x: x['cpu_percent'] or 0, reverse=True)
        
        return {
            "process_count": len(processes),
            "top_cpu_processes": processes[:10],
            "total_processes": len(psutil.pids())
        }
    except Exception as e:
        return {"error": str(e)}