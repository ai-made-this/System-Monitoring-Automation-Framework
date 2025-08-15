"""Scheduled Tasks Module - Manage system scheduled tasks/cron jobs"""
import subprocess
import platform
from datetime import datetime

def create_scheduled_task(task_name, command, schedule_type="daily", schedule_time="09:00"):
    """Create a scheduled task"""
    try:
        if platform.system() == "Windows":
            # Windows Task Scheduler
            result = subprocess.run([
                "schtasks", "/create",
                "/tn", task_name,
                "/tr", command,
                "/sc", schedule_type,
                "/st", schedule_time,
                "/f"  # Force overwrite if exists
            ], capture_output=True, text=True, timeout=30)
            
            success = result.returncode == 0
            return {
                "success": success,
                "task_name": task_name,
                "command": command,
                "schedule_type": schedule_type,
                "schedule_time": schedule_time,
                "platform": "Windows",
                "output": result.stdout.strip(),
                "error": result.stderr.strip() if not success else None,
                "created_at": datetime.now().isoformat()
            }
        else:
            # Unix/Linux cron
            # Convert schedule to cron format
            cron_schedule = _convert_to_cron_schedule(schedule_type, schedule_time)
            cron_entry = f"{cron_schedule} {command}  # {task_name}"
            
            # Add to crontab
            result = subprocess.run(
                ["crontab", "-l"],
                capture_output=True, text=True
            )
            
            current_crontab = result.stdout if result.returncode == 0 else ""
            new_crontab = current_crontab + "\n" + cron_entry + "\n"
            
            # Write new crontab
            process = subprocess.Popen(
                ["crontab", "-"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            stdout, stderr = process.communicate(input=new_crontab)
            success = process.returncode == 0
            
            return {
                "success": success,
                "task_name": task_name,
                "command": command,
                "cron_schedule": cron_schedule,
                "platform": platform.system(),
                "output": stdout,
                "error": stderr if not success else None,
                "created_at": datetime.now().isoformat()
            }
    except Exception as e:
        return {"error": str(e)}

def delete_scheduled_task(task_name):
    """Delete a scheduled task"""
    try:
        if platform.system() == "Windows":
            result = subprocess.run([
                "schtasks", "/delete",
                "/tn", task_name,
                "/f"
            ], capture_output=True, text=True, timeout=30)
            
            success = result.returncode == 0
            return {
                "success": success,
                "task_name": task_name,
                "platform": "Windows",
                "output": result.stdout.strip(),
                "error": result.stderr.strip() if not success else None,
                "deleted_at": datetime.now().isoformat()
            }
        else:
            # Remove from crontab
            result = subprocess.run(
                ["crontab", "-l"],
                capture_output=True, text=True
            )
            
            if result.returncode != 0:
                return {"error": "No crontab found"}
            
            current_crontab = result.stdout
            lines = current_crontab.split('\n')
            new_lines = [line for line in lines if f"# {task_name}" not in line]
            new_crontab = '\n'.join(new_lines)
            
            # Write new crontab
            process = subprocess.Popen(
                ["crontab", "-"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            stdout, stderr = process.communicate(input=new_crontab)
            success = process.returncode == 0
            
            return {
                "success": success,
                "task_name": task_name,
                "platform": platform.system(),
                "output": stdout,
                "error": stderr if not success else None,
                "deleted_at": datetime.now().isoformat()
            }
    except Exception as e:
        return {"error": str(e)}

def list_scheduled_tasks():
    """List all scheduled tasks"""
    try:
        tasks = []
        
        if platform.system() == "Windows":
            result = subprocess.run([
                "schtasks", "/query", "/fo", "csv"
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                if len(lines) > 1:  # Skip header
                    for line in lines[1:]:
                        parts = [p.strip('"') for p in line.split('","')]
                        if len(parts) >= 4:
                            tasks.append({
                                "name": parts[0],
                                "next_run": parts[1],
                                "status": parts[2],
                                "last_run": parts[3] if len(parts) > 3 else None
                            })
        else:
            # List cron jobs
            result = subprocess.run(
                ["crontab", "-l"],
                capture_output=True, text=True
            )
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        parts = line.split()
                        if len(parts) >= 6:
                            schedule = ' '.join(parts[:5])
                            command = ' '.join(parts[5:])
                            task_name = "Unknown"
                            
                            # Extract task name from comment if present
                            if '#' in line:
                                comment_part = line.split('#', 1)[1].strip()
                                task_name = comment_part
                            
                            tasks.append({
                                "name": task_name,
                                "schedule": schedule,
                                "command": command,
                                "status": "enabled"
                            })
        
        return {
            "success": True,
            "platform": platform.system(),
            "task_count": len(tasks),
            "tasks": tasks
        }
    except Exception as e:
        return {"error": str(e)}

def _convert_to_cron_schedule(schedule_type, schedule_time):
    """Convert schedule type and time to cron format"""
    hour, minute = schedule_time.split(':')
    
    if schedule_type == "daily":
        return f"{minute} {hour} * * *"
    elif schedule_type == "weekly":
        return f"{minute} {hour} * * 0"  # Sunday
    elif schedule_type == "monthly":
        return f"{minute} {hour} 1 * *"  # First day of month
    else:
        return f"{minute} {hour} * * *"  # Default to daily

def get_scheduled_tasks():
    """Get scheduled tasks management capabilities"""
    try:
        return {
            "functions": {
                "create_scheduled_task": "create_scheduled_task(task_name, command, schedule_type='daily', schedule_time='09:00')",
                "delete_scheduled_task": "delete_scheduled_task(task_name)",
                "list_scheduled_tasks": "list_scheduled_tasks()"
            },
            "schedule_types": ["daily", "weekly", "monthly"],
            "time_format": "HH:MM (24-hour format)",
            "examples": {
                "create_daily": "create_scheduled_task('backup', 'python backup.py', 'daily', '02:00')",
                "create_weekly": "create_scheduled_task('cleanup', 'cleanup.bat', 'weekly', '23:30')",
                "list_tasks": "list_scheduled_tasks()"
            },
            "platform_notes": {
                "Windows": "Uses Windows Task Scheduler (schtasks)",
                "Unix/Linux": "Uses cron jobs (crontab)"
            }
        }
    except Exception as e:
        return {"error": str(e)}