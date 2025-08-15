"""Registry Operations Module - Windows Registry management"""
import platform
import subprocess
from datetime import datetime

def read_registry_key(key_path, value_name=None):
    """Read a Windows registry key"""
    try:
        if platform.system() != "Windows":
            return {"error": "Registry operations only available on Windows"}
        
        if value_name:
            # Read specific value
            result = subprocess.run(
                ["reg", "query", key_path, "/v", value_name],
                capture_output=True, text=True, timeout=10
            )
        else:
            # Read all values in key
            result = subprocess.run(
                ["reg", "query", key_path],
                capture_output=True, text=True, timeout=10
            )
        
        if result.returncode == 0:
            output = result.stdout.strip()
            values = {}
            
            lines = output.split('\n')
            for line in lines:
                line = line.strip()
                if 'REG_' in line:
                    parts = line.split(None, 2)
                    if len(parts) >= 3:
                        name = parts[0]
                        reg_type = parts[1]
                        value = parts[2] if len(parts) > 2 else ""
                        values[name] = {"type": reg_type, "value": value}
            
            return {
                "success": True,
                "key_path": key_path,
                "value_name": value_name,
                "values": values,
                "raw_output": output
            }
        else:
            return {"error": f"Failed to read registry key: {result.stderr.strip()}"}
    except Exception as e:
        return {"error": str(e)}

def write_registry_key(key_path, value_name, value_data, value_type="REG_SZ"):
    """Write to Windows registry"""
    try:
        if platform.system() != "Windows":
            return {"error": "Registry operations only available on Windows"}
        
        result = subprocess.run(
            ["reg", "add", key_path, "/v", value_name, "/t", value_type, "/d", str(value_data), "/f"],
            capture_output=True, text=True, timeout=10
        )
        
        success = result.returncode == 0
        return {
            "success": success,
            "key_path": key_path,
            "value_name": value_name,
            "value_data": value_data,
            "value_type": value_type,
            "output": result.stdout.strip(),
            "error": result.stderr.strip() if not success else None,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {"error": str(e)}

def delete_registry_key(key_path, value_name=None):
    """Delete Windows registry key or value"""
    try:
        if platform.system() != "Windows":
            return {"error": "Registry operations only available on Windows"}
        
        if value_name:
            # Delete specific value
            result = subprocess.run(
                ["reg", "delete", key_path, "/v", value_name, "/f"],
                capture_output=True, text=True, timeout=10
            )
        else:
            # Delete entire key
            result = subprocess.run(
                ["reg", "delete", key_path, "/f"],
                capture_output=True, text=True, timeout=10
            )
        
        success = result.returncode == 0
        return {
            "success": success,
            "key_path": key_path,
            "value_name": value_name,
            "action": "delete_value" if value_name else "delete_key",
            "output": result.stdout.strip(),
            "error": result.stderr.strip() if not success else None,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {"error": str(e)}

def backup_registry_key(key_path, backup_file):
    """Backup Windows registry key to file"""
    try:
        if platform.system() != "Windows":
            return {"error": "Registry operations only available on Windows"}
        
        result = subprocess.run(
            ["reg", "export", key_path, backup_file, "/y"],
            capture_output=True, text=True, timeout=30
        )
        
        success = result.returncode == 0
        return {
            "success": success,
            "key_path": key_path,
            "backup_file": backup_file,
            "action": "backup",
            "output": result.stdout.strip(),
            "error": result.stderr.strip() if not success else None,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {"error": str(e)}

def get_registry_ops():
    """Get registry operations capabilities"""
    try:
        return {
            "functions": {
                "read_registry_key": "read_registry_key(key_path, value_name=None)",
                "write_registry_key": "write_registry_key(key_path, value_name, value_data, value_type='REG_SZ')",
                "delete_registry_key": "delete_registry_key(key_path, value_name=None)",
                "backup_registry_key": "backup_registry_key(key_path, backup_file)"
            },
            "supported_types": [
                "REG_SZ (String)",
                "REG_DWORD (32-bit number)",
                "REG_QWORD (64-bit number)",
                "REG_BINARY (Binary data)",
                "REG_MULTI_SZ (Multi-string)"
            ],
            "common_keys": [
                "HKEY_CURRENT_USER\\Software",
                "HKEY_LOCAL_MACHINE\\SOFTWARE",
                "HKEY_CURRENT_USER\\Environment"
            ],
            "examples": {
                "read_key": "read_registry_key('HKCU\\\\Software\\\\Microsoft\\\\Windows\\\\CurrentVersion\\\\Run')",
                "write_value": "write_registry_key('HKCU\\\\Software\\\\MyApp', 'Version', '1.0')",
                "backup": "backup_registry_key('HKCU\\\\Software\\\\MyApp', 'backup.reg')"
            },
            "platform": "Windows only",
            "warning": "Registry modifications can affect system stability. Always backup before making changes."
        }
    except Exception as e:
        return {"error": str(e)}