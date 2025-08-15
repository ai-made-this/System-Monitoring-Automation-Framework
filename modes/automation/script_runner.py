"""Script Runner Module - Execute scripts and commands"""
import subprocess
import os
from pathlib import Path
from datetime import datetime
import tempfile

def run_script(script_path, args=None, working_dir=None, timeout=300, capture_output=True):
    """Run a script file"""
    try:
        script_file = Path(script_path)
        if not script_file.exists():
            return {"error": f"Script file {script_path} does not exist"}
        
        if args is None:
            args = []
        
        # Determine how to run the script based on extension
        extension = script_file.suffix.lower()
        if extension == '.py':
            command = ['python', str(script_file)] + args
        elif extension == '.bat' or extension == '.cmd':
            command = [str(script_file)] + args
        elif extension == '.ps1':
            command = ['powershell', '-ExecutionPolicy', 'Bypass', '-File', str(script_file)] + args
        elif extension == '.sh':
            command = ['bash', str(script_file)] + args
        else:
            # Try to run directly
            command = [str(script_file)] + args
        
        start_time = datetime.now()
        
        if capture_output:
            result = subprocess.run(
                command,
                cwd=working_dir,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            return {
                "success": result.returncode == 0,
                "script_path": str(script_file.absolute()),
                "command": command,
                "return_code": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "execution_time_seconds": (datetime.now() - start_time).total_seconds(),
                "started_at": start_time.isoformat(),
                "working_dir": working_dir
            }
        else:
            # Run without capturing output
            process = subprocess.Popen(
                command,
                cwd=working_dir
            )
            
            return {
                "success": True,
                "script_path": str(script_file.absolute()),
                "command": command,
                "pid": process.pid,
                "started_at": start_time.isoformat(),
                "working_dir": working_dir,
                "note": "Script running in background, output not captured"
            }
    except subprocess.TimeoutExpired:
        return {"error": f"Script execution timed out after {timeout} seconds"}
    except Exception as e:
        return {"error": str(e)}

def run_command(command, args=None, working_dir=None, timeout=60, shell=False):
    """Run a system command"""
    try:
        if args is None:
            args = []
        
        if shell:
            # Run as shell command
            full_command = f"{command} {' '.join(args)}"
            cmd_list = full_command
        else:
            # Run as separate command and args
            cmd_list = [command] + args
        
        start_time = datetime.now()
        
        result = subprocess.run(
            cmd_list,
            cwd=working_dir,
            capture_output=True,
            text=True,
            timeout=timeout,
            shell=shell
        )
        
        return {
            "success": result.returncode == 0,
            "command": command,
            "args": args,
            "return_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "execution_time_seconds": (datetime.now() - start_time).total_seconds(),
            "started_at": start_time.isoformat(),
            "working_dir": working_dir,
            "shell": shell
        }
    except subprocess.TimeoutExpired:
        return {"error": f"Command execution timed out after {timeout} seconds"}
    except Exception as e:
        return {"error": str(e)}

def create_and_run_script(script_content, script_type="python", args=None, cleanup=True):
    """Create a temporary script and run it"""
    try:
        # Determine file extension
        extensions = {
            "python": ".py",
            "batch": ".bat",
            "powershell": ".ps1",
            "bash": ".sh"
        }
        
        extension = extensions.get(script_type, ".txt")
        
        # Create temporary script file
        with tempfile.NamedTemporaryFile(mode='w', suffix=extension, delete=False) as temp_file:
            temp_file.write(script_content)
            temp_script_path = temp_file.name
        
        try:
            # Run the script
            result = run_script(temp_script_path, args)
            result["temporary_script"] = True
            result["script_content_length"] = len(script_content)
            result["script_type"] = script_type
            
            return result
        finally:
            # Cleanup temporary file if requested
            if cleanup:
                try:
                    os.unlink(temp_script_path)
                    if "success" in result:
                        result["temp_file_cleaned"] = True
                except:
                    if "success" in result:
                        result["temp_file_cleaned"] = False
    except Exception as e:
        return {"error": str(e)}

def batch_run_scripts(script_list, parallel=False, stop_on_error=True):
    """Run multiple scripts in sequence or parallel"""
    try:
        results = []
        
        if parallel:
            # Run scripts in parallel
            import concurrent.futures
            
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = []
                for script_info in script_list:
                    if isinstance(script_info, str):
                        future = executor.submit(run_script, script_info)
                    else:
                        future = executor.submit(
                            run_script,
                            script_info.get("path"),
                            script_info.get("args"),
                            script_info.get("working_dir")
                        )
                    futures.append(future)
                
                for i, future in enumerate(futures):
                    try:
                        result = future.result(timeout=300)
                        result["script_index"] = i
                        results.append(result)
                    except Exception as e:
                        results.append({
                            "script_index": i,
                            "error": str(e)
                        })
        else:
            # Run scripts sequentially
            for i, script_info in enumerate(script_list):
                if isinstance(script_info, str):
                    result = run_script(script_info)
                else:
                    result = run_script(
                        script_info.get("path"),
                        script_info.get("args"),
                        script_info.get("working_dir")
                    )
                
                result["script_index"] = i
                results.append(result)
                
                # Stop on error if requested
                if stop_on_error and not result.get("success", False):
                    break
        
        successful_count = sum(1 for r in results if r.get("success", False))
        
        return {
            "success": True,
            "total_scripts": len(script_list),
            "executed_scripts": len(results),
            "successful_scripts": successful_count,
            "failed_scripts": len(results) - successful_count,
            "parallel": parallel,
            "stop_on_error": stop_on_error,
            "results": results
        }
    except Exception as e:
        return {"error": str(e)}

def get_script_runner():
    """Get script runner capabilities"""
    try:
        return {
            "functions": {
                "run_script": "run_script(script_path, args=None, working_dir=None, timeout=300, capture_output=True)",
                "run_command": "run_command(command, args=None, working_dir=None, timeout=60, shell=False)",
                "create_and_run_script": "create_and_run_script(script_content, script_type='python', args=None, cleanup=True)",
                "batch_run_scripts": "batch_run_scripts(script_list, parallel=False, stop_on_error=True)"
            },
            "supported_script_types": [
                "Python (.py)",
                "Batch (.bat, .cmd)",
                "PowerShell (.ps1)",
                "Bash (.sh)",
                "Direct execution"
            ],
            "features": [
                "Timeout control",
                "Output capture",
                "Working directory support",
                "Parallel execution",
                "Temporary script creation",
                "Batch processing"
            ],
            "examples": {
                "run_python": "run_script('script.py', ['arg1', 'arg2'])",
                "run_command": "run_command('dir', shell=True)",
                "temp_script": "create_and_run_script('print(\"Hello World\")', 'python')",
                "batch_run": "batch_run_scripts(['script1.py', 'script2.py'], parallel=True)"
            }
        }
    except Exception as e:
        return {"error": str(e)}