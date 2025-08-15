"""Process Control Module - Start, stop, and manage processes"""
import subprocess
import psutil
import platform
from datetime import datetime

def start_process(command, args=None, working_dir=None, detached=False):
    """Start a new process"""
    try:
        if args is None:
            args = []
        
        full_command = [command] + args
        
        if detached:
            # Start detached process
            if platform.system() == "Windows":
                process = subprocess.Popen(
                    full_command,
                    cwd=working_dir,
                    creationflags=subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS
                )
            else:
                process = subprocess.Popen(
                    full_command,
                    cwd=working_dir,
                    start_new_session=True
                )
        else:
            # Start attached process
            process = subprocess.Popen(
                full_command,
                cwd=working_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
        
        return {
            "success": True,
            "pid": process.pid,
            "command": command,
            "args": args,
            "working_dir": working_dir,
            "detached": detached,
            "started_at": datetime.now().isoformat()
        }
    except Exception as e:
        return {"error": str(e)}

def kill_process(pid=None, name=None, force=False):
    """Kill a process by PID or name"""
    try:
        killed_processes = []
        
        if pid:
            # Kill by PID
            try:
                proc = psutil.Process(pid)
                proc_info = {
                    "pid": proc.pid,
                    "name": proc.name(),
                    "cpu_percent": proc.cpu_percent(),
                    "memory_mb": round(proc.memory_info().rss / 1024 / 1024, 2)
                }
                
                if force:
                    proc.kill()
                else:
                    proc.terminate()
                
                killed_processes.append(proc_info)
            except psutil.NoSuchProcess:
                return {"error": f"Process with PID {pid} not found"}
        
        elif name:
            # Kill by name
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    if proc.info['name'].lower() == name.lower():
                        process = psutil.Process(proc.info['pid'])
                        proc_info = {
                            "pid": process.pid,
                            "name": process.name(),
                            "cpu_percent": process.cpu_percent(),
                            "memory_mb": round(process.memory_info().rss / 1024 / 1024, 2)
                        }
                        
                        if force:
                            process.kill()
                        else:
                            process.terminate()
                        
                        killed_processes.append(proc_info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
        else:
            return {"error": "Must specify either pid or name"}
        
        return {
            "success": True,
            "killed_count": len(killed_processes),
            "killed_processes": killed_processes,
            "force": force,
            "killed_at": datetime.now().isoformat()
        }
    except Exception as e:
        return {"error": str(e)}

def get_process_info(pid=None, name=None):
    """Get detailed information about a process"""
    try:
        processes = []
        
        if pid:
            # Get by PID
            try:
                proc = psutil.Process(pid)
                processes.append(_get_detailed_process_info(proc))
            except psutil.NoSuchProcess:
                return {"error": f"Process with PID {pid} not found"}
        
        elif name:
            # Get by name
            for proc in psutil.process_iter():
                try:
                    if proc.name().lower() == name.lower():
                        processes.append(_get_detailed_process_info(proc))
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
        else:
            return {"error": "Must specify either pid or name"}
        
        return {
            "success": True,
            "process_count": len(processes),
            "processes": processes
        }
    except Exception as e:
        return {"error": str(e)}

def _get_detailed_process_info(proc):
    """Get detailed information about a psutil Process object"""
    try:
        with proc.oneshot():
            return {
                "pid": proc.pid,
                "name": proc.name(),
                "status": proc.status(),
                "cpu_percent": proc.cpu_percent(),
                "memory_percent": proc.memory_percent(),
                "memory_mb": round(proc.memory_info().rss / 1024 / 1024, 2),
                "create_time": datetime.fromtimestamp(proc.create_time()).isoformat(),
                "num_threads": proc.num_threads(),
                "username": proc.username() if hasattr(proc, 'username') else None,
                "cmdline": " ".join(proc.cmdline()) if proc.cmdline() else None
            }
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return {"error": "Access denied or process no longer exists"}

def get_process_control():
    """Get process control capabilities"""
    try:
        return {
            "functions": {
                "start_process": "start_process(command, args=None, working_dir=None, detached=False)",
                "kill_process": "kill_process(pid=None, name=None, force=False)",
                "get_process_info": "get_process_info(pid=None, name=None)"
            },
            "features": [
                "Start processes attached or detached",
                "Kill processes by PID or name",
                "Graceful termination or force kill",
                "Detailed process information"
            ],
            "examples": {
                "start_detached": "start_process('notepad.exe', detached=True)",
                "kill_by_name": "kill_process(name='notepad.exe')",
                "get_info": "get_process_info(name='python.exe')"
            }
        }
    except Exception as e:
        return {"error": str(e)}