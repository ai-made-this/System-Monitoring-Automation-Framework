"""Startup Programs Monitor - Lists programs that start with system"""
import platform
import subprocess

def get_startup_programs():
    """Get programs that start with the system"""
    try:
        if platform.system() == "Windows":
            # Get startup programs from registry and startup folder
            ps_script = """
            $startup = @()
            
            # Get from registry
            $regPaths = @(
                'HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run',
                'HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run'
            )
            
            foreach ($path in $regPaths) {
                if (Test-Path $path) {
                    Get-ItemProperty $path | Get-Member -MemberType NoteProperty | 
                    Where-Object {$_.Name -ne 'PSPath' -and $_.Name -ne 'PSParentPath' -and $_.Name -ne 'PSChildName' -and $_.Name -ne 'PSDrive' -and $_.Name -ne 'PSProvider'} |
                    ForEach-Object {
                        $startup += @{
                            Name = $_.Name
                            Location = $path
                            Type = 'Registry'
                        }
                    }
                }
            }
            
            $startup | ConvertTo-Json
            """
            
            result = subprocess.run(
                ["powershell", "-Command", ps_script],
                capture_output=True, text=True, timeout=15
            )
            
            if result.returncode == 0:
                import json
                try:
                    programs = json.loads(result.stdout)
                    if not isinstance(programs, list):
                        programs = [programs] if programs else []
                    
                    return {
                        "platform": "Windows",
                        "startup_programs": programs,
                        "program_count": len(programs)
                    }
                except json.JSONDecodeError:
                    return {"error": "Failed to parse startup programs data"}
            else:
                return {"error": "Failed to get startup programs"}
        else:
            return {"error": f"Startup programs detection not implemented for {platform.system()}"}
    except Exception as e:
        return {"error": str(e)}