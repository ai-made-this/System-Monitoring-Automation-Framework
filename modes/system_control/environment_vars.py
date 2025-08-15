"""Environment Variables Module - Manage system environment variables"""
import os
import subprocess
import platform
from datetime import datetime

def get_environment_variable(var_name):
    """Get an environment variable value"""
    try:
        value = os.environ.get(var_name)
        return {
            "success": True,
            "variable_name": var_name,
            "value": value,
            "exists": value is not None
        }
    except Exception as e:
        return {"error": str(e)}

def set_environment_variable(var_name, var_value, user_scope=True, permanent=False):
    """Set an environment variable"""
    try:
        # Set for current session
        os.environ[var_name] = str(var_value)
        
        result = {
            "success": True,
            "variable_name": var_name,
            "value": var_value,
            "user_scope": user_scope,
            "permanent": permanent,
            "session_set": True,
            "timestamp": datetime.now().isoformat()
        }
        
        # Set permanently if requested
        if permanent:
            if platform.system() == "Windows":
                scope = "USER" if user_scope else "MACHINE"
                cmd_result = subprocess.run(
                    ["setx", var_name, str(var_value), "/M" if not user_scope else ""],
                    capture_output=True, text=True, timeout=10
                )
                result["permanent_set"] = cmd_result.returncode == 0
                result["setx_output"] = cmd_result.stdout.strip()
                if cmd_result.returncode != 0:
                    result["setx_error"] = cmd_result.stderr.strip()
            else:
                # For Unix-like systems, add to shell profile
                shell_profile = os.path.expanduser("~/.bashrc")
                if os.path.exists(os.path.expanduser("~/.zshrc")):
                    shell_profile = os.path.expanduser("~/.zshrc")
                
                with open(shell_profile, "a") as f:
                    f.write(f"\nexport {var_name}='{var_value}'\n")
                
                result["permanent_set"] = True
                result["profile_updated"] = shell_profile
        
        return result
    except Exception as e:
        return {"error": str(e)}

def delete_environment_variable(var_name, permanent=False):
    """Delete an environment variable"""
    try:
        # Remove from current session
        if var_name in os.environ:
            del os.environ[var_name]
            session_deleted = True
        else:
            session_deleted = False
        
        result = {
            "success": True,
            "variable_name": var_name,
            "session_deleted": session_deleted,
            "permanent": permanent,
            "timestamp": datetime.now().isoformat()
        }
        
        # Remove permanently if requested
        if permanent:
            if platform.system() == "Windows":
                # Delete from registry
                for scope in ["USER", "MACHINE"]:
                    try:
                        subprocess.run(
                            ["reg", "delete", f"HKEY_CURRENT_USER\\Environment" if scope == "USER" else "HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Environment",
                             "/v", var_name, "/f"],
                            capture_output=True, timeout=10
                        )
                    except:
                        pass
                result["permanent_deleted"] = True
            else:
                # Remove from shell profiles
                for profile in ["~/.bashrc", "~/.zshrc", "~/.profile"]:
                    profile_path = os.path.expanduser(profile)
                    if os.path.exists(profile_path):
                        try:
                            with open(profile_path, "r") as f:
                                lines = f.readlines()
                            
                            with open(profile_path, "w") as f:
                                for line in lines:
                                    if not (line.strip().startswith(f"export {var_name}=") or 
                                           line.strip().startswith(f"{var_name}=")):
                                        f.write(line)
                        except:
                            pass
                result["permanent_deleted"] = True
        
        return result
    except Exception as e:
        return {"error": str(e)}

def list_environment_variables(filter_pattern=None):
    """List all environment variables"""
    try:
        variables = {}
        
        for key, value in os.environ.items():
            if filter_pattern is None or filter_pattern.lower() in key.lower():
                variables[key] = {
                    "value": value,
                    "length": len(value)
                }
        
        return {
            "success": True,
            "variable_count": len(variables),
            "variables": variables,
            "filter_pattern": filter_pattern,
            "platform": platform.system()
        }
    except Exception as e:
        return {"error": str(e)}

def get_path_variable():
    """Get and parse the PATH environment variable"""
    try:
        path_value = os.environ.get("PATH", "")
        separator = ";" if platform.system() == "Windows" else ":"
        path_entries = [p.strip() for p in path_value.split(separator) if p.strip()]
        
        # Check which paths exist
        existing_paths = []
        missing_paths = []
        
        for path in path_entries:
            if os.path.exists(path):
                existing_paths.append({
                    "path": path,
                    "is_directory": os.path.isdir(path),
                    "readable": os.access(path, os.R_OK)
                })
            else:
                missing_paths.append(path)
        
        return {
            "success": True,
            "path_count": len(path_entries),
            "existing_count": len(existing_paths),
            "missing_count": len(missing_paths),
            "existing_paths": existing_paths,
            "missing_paths": missing_paths,
            "separator": separator,
            "full_path": path_value
        }
    except Exception as e:
        return {"error": str(e)}

def get_environment_vars():
    """Get environment variables management capabilities"""
    try:
        return {
            "functions": {
                "get_environment_variable": "get_environment_variable(var_name)",
                "set_environment_variable": "set_environment_variable(var_name, var_value, user_scope=True, permanent=False)",
                "delete_environment_variable": "delete_environment_variable(var_name, permanent=False)",
                "list_environment_variables": "list_environment_variables(filter_pattern=None)",
                "get_path_variable": "get_path_variable()"
            },
            "features": [
                "Get/set/delete environment variables",
                "Session and permanent changes",
                "User and system scope (Windows)",
                "PATH variable analysis",
                "Variable filtering and search"
            ],
            "examples": {
                "get_var": "get_environment_variable('PATH')",
                "set_temp": "set_environment_variable('MY_VAR', 'value')",
                "set_permanent": "set_environment_variable('MY_VAR', 'value', permanent=True)",
                "list_filtered": "list_environment_variables('PYTHON')"
            },
            "platform_notes": {
                "Windows": "Uses setx for permanent changes, supports USER/MACHINE scope",
                "Unix/Linux": "Updates shell profiles (.bashrc, .zshrc) for permanent changes"
            }
        }
    except Exception as e:
        return {"error": str(e)}