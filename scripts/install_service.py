#!/usr/bin/env python3
"""
Service Installation Script
Install the System Monitoring Service to start automatically
"""

import os
import sys
import shutil
from pathlib import Path

def install_startup_script():
    """Install service to Windows startup folder"""
    try:
        # Get Windows startup folder
        startup_folder = Path(os.path.expandvars(r'%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup'))
        
        if not startup_folder.exists():
            print("❌ Windows startup folder not found")
            return False
        
        # Create startup script
        current_dir = Path(__file__).parent.parent.absolute()
        startup_script_content = f'''@echo off
cd /d "{current_dir}"
python start_service.py
pause
'''
        
        startup_script = startup_folder / "SystemMonitoringService.bat"
        
        with open(startup_script, 'w') as f:
            f.write(startup_script_content)
        
        print(f"✅ Startup script installed: {startup_script}")
        print("🔄 Service will start automatically when Windows starts")
        return True
        
    except Exception as e:
        print(f"❌ Failed to install startup script: {e}")
        return False

def create_desktop_shortcut():
    """Create desktop shortcut for manual service control"""
    try:
        desktop = Path(os.path.expandvars(r'%USERPROFILE%\Desktop'))
        current_dir = Path(__file__).parent.parent.absolute()
        
        # Create start service shortcut
        start_shortcut_content = f'''@echo off
title System Monitoring Service
cd /d "{current_dir}"
python start_service.py
pause
'''
        
        start_shortcut = desktop / "Start System Monitoring.bat"
        with open(start_shortcut, 'w') as f:
            f.write(start_shortcut_content)
        
        # Create status check shortcut
        status_shortcut_content = f'''@echo off
title System Monitoring Status
cd /d "{current_dir}"
python -m modes.service.aggregator detailed
pause
'''
        
        status_shortcut = desktop / "Check System Monitoring Status.bat"
        with open(status_shortcut, 'w') as f:
            f.write(status_shortcut_content)
        
        print(f"✅ Desktop shortcuts created:")
        print(f"   📊 {start_shortcut}")
        print(f"   📈 {status_shortcut}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to create desktop shortcuts: {e}")
        return False

def install_task_scheduler():
    """Create Windows Task Scheduler entry"""
    try:
        current_dir = Path(__file__).parent.parent.absolute()
        python_exe = sys.executable
        
        # Create XML for task scheduler
        task_xml = f'''<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo>
    <Date>2024-01-01T00:00:00</Date>
    <Author>System Monitoring Framework</Author>
    <Description>Always-on system monitoring and machine learning service</Description>
  </RegistrationInfo>
  <Triggers>
    <LogonTrigger>
      <Enabled>true</Enabled>
    </LogonTrigger>
  </Triggers>
  <Principals>
    <Principal id="Author">
      <LogonType>InteractiveToken</LogonType>
      <RunLevel>LeastPrivilege</RunLevel>
    </Principal>
  </Principals>
  <Settings>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>
    <AllowHardTerminate>true</AllowHardTerminate>
    <StartWhenAvailable>true</StartWhenAvailable>
    <RunOnlyIfNetworkAvailable>false</RunOnlyIfNetworkAvailable>
    <IdleSettings>
      <StopOnIdleEnd>false</StopOnIdleEnd>
      <RestartOnIdle>false</RestartOnIdle>
    </IdleSettings>
    <AllowStartOnDemand>true</AllowStartOnDemand>
    <Enabled>true</Enabled>
    <Hidden>false</Hidden>
    <RunOnlyIfIdle>false</RunOnlyIfIdle>
    <WakeToRun>false</WakeToRun>
    <ExecutionTimeLimit>PT0S</ExecutionTimeLimit>
    <Priority>7</Priority>
  </Settings>
  <Actions>
    <Exec>
      <Command>{python_exe}</Command>
      <Arguments>start_service.py</Arguments>
      <WorkingDirectory>{current_dir}</WorkingDirectory>
    </Exec>
  </Actions>
</Task>'''
        
        # Save task XML
        task_file = current_dir / "SystemMonitoringTask.xml"
        with open(task_file, 'w', encoding='utf-16') as f:
            f.write(task_xml)
        
        print(f"✅ Task Scheduler XML created: {task_file}")
        print("\n📋 To install the scheduled task:")
        print("1. Open Task Scheduler (taskschd.msc)")
        print("2. Click 'Import Task...'")
        print(f"3. Select: {task_file}")
        print("4. Click 'OK' to install")
        print("\n🔄 The service will start automatically at login")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to create task scheduler entry: {e}")
        return False

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import psutil
        print("✅ psutil is installed")
    except ImportError:
        print("❌ psutil is not installed")
        print("💡 Install with: pip install psutil")
        return False
    
    # Check if service modules exist
    service_dir = Path(__file__).parent.parent / "modes" / "service"
    if not service_dir.exists():
        print("❌ Service modules not found")
        return False
    
    print("✅ All dependencies are available")
    return True

def main():
    """Main installation function"""
    print("🚀 System Monitoring Service Installer")
    print("=" * 50)
    
    if not check_dependencies():
        print("\n❌ Installation cannot proceed due to missing dependencies")
        return 1
    
    print("\n📋 Installation Options:")
    print("1. Startup Folder (Recommended)")
    print("2. Task Scheduler (Advanced)")
    print("3. Desktop Shortcuts Only")
    print("4. All Options")
    
    try:
        choice = input("\nSelect option (1-4): ").strip()
        
        success = True
        
        if choice in ['1', '4']:
            print("\n📁 Installing to startup folder...")
            success &= install_startup_script()
        
        if choice in ['2', '4']:
            print("\n⏰ Creating task scheduler entry...")
            success &= install_task_scheduler()
        
        if choice in ['3', '4'] or choice in ['1', '2']:
            print("\n🖥️ Creating desktop shortcuts...")
            success &= create_desktop_shortcut()
        
        if success:
            print("\n" + "=" * 50)
            print("✅ Installation completed successfully!")
            print("\n🎯 What happens now:")
            print("   • Service will start automatically with Windows")
            print("   • Continuous monitoring and learning begins")
            print("   • ML models improve over time")
            print("   • System optimizes based on your usage")
            
            print("\n📊 Manual Controls:")
            print("   • Start: Double-click 'Start System Monitoring.bat'")
            print("   • Status: Double-click 'Check System Monitoring Status.bat'")
            print("   • Stop: Press Ctrl+C in the service window")
            
            print("\n🔧 Configuration:")
            print("   • Config files: modes/service/")
            print("   • Logs: modes/service/service_log.json")
            print("   • Learning data: modes/ml/data/")
            
            start_now = input("\n🚀 Start the service now? (y/n): ").strip().lower()
            if start_now == 'y':
                print("\n🔄 Starting service...")
                os.system("python start_service.py")
        else:
            print("\n❌ Installation completed with some errors")
            return 1
            
    except KeyboardInterrupt:
        print("\n\n🛑 Installation cancelled by user")
        return 1
    except Exception as e:
        print(f"\n❌ Installation error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)