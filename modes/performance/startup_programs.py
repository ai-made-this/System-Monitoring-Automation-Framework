"""Startup Programs Monitor - Lists programs that start with system"""
import platform
import subprocess

def get_startup_programs():
    """Get programs that start with the system"""
    try:
        if platform.system() == "Windows":
            # Get startup programs from registry and startup folder
            # This script is more comprehensive, fetching the command and checking more locations.
            ps_script = """
            $startupItems = @()

            # 1. Registry locations
            $regLocations = @(
                @{ Path = 'HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run'; Scope = 'All Users' },
                @{ Path = 'HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run'; Scope = 'Current User' },
                @{ Path = 'HKLM:\\SOFTWARE\\WOW6432Node\\Microsoft\\Windows\\CurrentVersion\\Run'; Scope = 'All Users (32-bit)' }
            )

            foreach ($loc in $regLocations) {
                if (Test-Path $loc.Path) {
                    Get-ItemProperty -Path $loc.Path | ForEach-Object {
                        $item = $_
                        $item.PSObject.Properties | Where-Object { $_.Name -notlike 'PS*' } | ForEach-Object {
                            $startupItems += @{
                                Name     = $_.Name
                                Command  = $_.Value
                                Location = $loc.Path
                                Type     = 'Registry'
                            }
                        }
                    }
                }
            }

            # 2. Startup folders
            $folderLocations = @(
                @{ Path = "$env:ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"; Scope = 'All Users' },
                @{ Path = "$env:APPDATA\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"; Scope = 'Current User' }
            )

            foreach ($loc in $folderLocations) {
                if (Test-Path $loc.Path) {
                    Get-ChildItem -Path $loc.Path | ForEach-Object {
                        $startupItems += @{ Name = $_.Name; Command = $_.FullName; Location = $loc.Path; Type = 'Startup Folder' }
                    }
                }
            }

            $startupItems | ConvertTo-Json
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
