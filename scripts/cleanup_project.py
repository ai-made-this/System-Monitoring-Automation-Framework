#!/usr/bin/env python3
"""
Project Cleanup Script
Organizes files, creates proper directory structure, and prepares for backup
"""

import os
import shutil
from pathlib import Path

def create_directory_structure():
    """Create organized directory structure"""
    directories = [
        "docs",
        "scripts", 
        "config",
        "logs",
        "backups",
        "tests"
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created directory: {directory}/")

def organize_documentation():
    """Move documentation files to docs directory"""
    doc_files = [
        "README.md",
        "Current_Structure.txt", 
        "FINAL_SYSTEM_OVERVIEW.md",
        "AI_SYSTEM_SUMMARY.md",
        "AUDIO_SYSTEM_SUMMARY.md",
        "AUTO_UPDATE_SYSTEM.md",
        "EXPANSION_SUMMARY.md",
        "ML_SYSTEM_SUMMARY.md"
    ]
    
    docs_dir = Path("docs")
    moved_files = []
    
    for doc_file in doc_files:
        if Path(doc_file).exists():
            # Keep README.md in root, copy others to docs
            if doc_file == "README.md":
                shutil.copy2(doc_file, docs_dir / doc_file)
                print(f"📄 Copied {doc_file} to docs/")
            else:
                shutil.move(doc_file, docs_dir / doc_file)
                moved_files.append(doc_file)
                print(f"📄 Moved {doc_file} to docs/")
    
    return moved_files

def organize_scripts():
    """Move utility scripts to scripts directory"""
    script_files = [
        "build_aggregators.py",
        "update_structure.py", 
        "watch_structure.py",
        "setup_auto_update.py",
        "cleanup_project.py",
        "install_service.py",
        "start_service.py"
    ]
    
    scripts_dir = Path("scripts")
    moved_files = []
    
    for script_file in script_files:
        if Path(script_file).exists():
            # Keep main scripts in root, copy others to scripts
            if script_file in ["build_aggregators.py", "main_aggregator.py", "start_service.py"]:
                shutil.copy2(script_file, scripts_dir / script_file)
                print(f"🔧 Copied {script_file} to scripts/")
            else:
                shutil.move(script_file, scripts_dir / script_file)
                moved_files.append(script_file)
                print(f"🔧 Moved {script_file} to scripts/")
    
    return moved_files

def organize_config():
    """Move configuration files to config directory"""
    config_files = [
        "global_config.json"
    ]
    
    config_dir = Path("config")
    moved_files = []
    
    for config_file in config_files:
        if Path(config_file).exists():
            shutil.move(config_file, config_dir / config_file)
            moved_files.append(config_file)
            print(f"⚙️ Moved {config_file} to config/")
    
    return moved_files

def organize_batch_files():
    """Move batch files to scripts directory"""
    batch_files = [
        "update_structure.bat",
        "watch_structure.bat", 
        "build_and_update.bat"
    ]
    
    scripts_dir = Path("scripts")
    moved_files = []
    
    for batch_file in batch_files:
        if Path(batch_file).exists():
            shutil.move(batch_file, scripts_dir / batch_file)
            moved_files.append(batch_file)
            print(f"📜 Moved {batch_file} to scripts/")
    
    return moved_files

def create_requirements_file():
    """Create requirements.txt file"""
    requirements = """# System Monitoring Framework Requirements

# Core dependencies (required for basic functionality)
psutil>=5.9.0

# Audio processing (for audio modules)
# pyaudio>=0.2.11
# sounddevice>=0.4.6
# pycaw>=20230407

# Machine learning (for ML modules)  
# scikit-learn>=1.3.0
# numpy>=1.24.0
# tensorflow>=2.13.0
# torch>=2.0.0

# Computer vision (for visual modules)
# opencv-python>=4.8.0
# pillow>=10.0.0
# pytesseract>=0.3.10

# System control (Windows-specific)
# pywin32>=306
# wmi>=1.5.1

# Development dependencies
# pytest>=7.4.0
# black>=23.7.0
# flake8>=6.0.0

# Note: Many dependencies are commented out as they require
# platform-specific installation and configuration.
# Uncomment and install as needed for full functionality.
"""
    
    with open("requirements.txt", "w") as f:
        f.write(requirements)
    
    print("📋 Created requirements.txt")

def create_project_info():
    """Create project information files"""
    
    # Create VERSION file
    with open("VERSION", "w") as f:
        f.write("0.1.0-beta\n")
    print("📌 Created VERSION file")
    
    # Create CHANGELOG.md
    changelog = """# Changelog

## [0.1.0-beta] - 2024-01-15

### Added
- Initial proof of concept implementation
- 26 module categories with 94+ individual modules
- Auto-aggregating module system
- AI and ML framework integration
- Audio monitoring and optimization system
- Gaming automation capabilities
- Always-on background service system
- Auto-updating documentation system
- Comprehensive CLI interface

### Status
- Framework architecture: COMPLETE
- Module scaffolding: COMPLETE  
- Real implementations: IN PROGRESS
- Testing: NOT STARTED
- Production ready: NO

### Notes
- This is a proof of concept / beta version
- Many modules contain simulated data
- Extensive testing required before production use
- Security review needed for system control features
"""
    
    with open("CHANGELOG.md", "w") as f:
        f.write(changelog)
    print("📝 Created CHANGELOG.md")

def create_final_backup():
    """Create final organized backup"""
    import datetime
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"SystemMonitoringFramework_ORGANIZED_{timestamp}.zip"
    
    try:
        import zipfile
        
        with zipfile.ZipFile(backup_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Add all files and directories
            for root, dirs, files in os.walk("."):
                # Skip backup files and __pycache__
                dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
                
                for file in files:
                    if not file.endswith('.zip') and not file.startswith('.'):
                        file_path = Path(root) / file
                        arcname = str(file_path).replace('\\', '/')
                        zipf.write(file_path, arcname)
        
        print(f"📦 Created organized backup: {backup_name}")
        return backup_name
        
    except Exception as e:
        print(f"❌ Failed to create backup: {e}")
        return None

def main():
    """Main cleanup function"""
    print("🧹 Project Cleanup & Organization")
    print("=" * 40)
    
    # Create directory structure
    print("\n📁 Creating directory structure...")
    create_directory_structure()
    
    # Organize files
    print("\n📄 Organizing documentation...")
    organize_documentation()
    
    print("\n🔧 Organizing scripts...")
    organize_scripts()
    
    print("\n⚙️ Organizing configuration...")
    organize_config()
    
    print("\n📜 Organizing batch files...")
    organize_batch_files()
    
    # Create project files
    print("\n📋 Creating project files...")
    create_requirements_file()
    create_project_info()
    
    # Create final backup
    print("\n📦 Creating organized backup...")
    backup_file = create_final_backup()
    
    # Summary
    print("\n" + "=" * 40)
    print("✅ Project cleanup completed!")
    
    print("\n📊 Organized Structure:")
    print("   📁 docs/ - All documentation files")
    print("   📁 scripts/ - Utility and setup scripts") 
    print("   📁 config/ - Configuration files")
    print("   📁 modes/ - Module system (unchanged)")
    print("   📁 logs/ - For future log files")
    print("   📁 tests/ - For future test files")
    print("   📁 backups/ - For backup files")
    
    print("\n📋 Key Files:")
    print("   📄 README.md - Main project documentation")
    print("   📄 requirements.txt - Python dependencies")
    print("   📄 VERSION - Current version (0.1.0-beta)")
    print("   📄 CHANGELOG.md - Version history")
    
    if backup_file:
        print(f"\n📦 Backup Created: {backup_file}")
    
    print("\n🎯 Next Steps:")
    print("   1. Review organized structure")
    print("   2. Test functionality after reorganization")
    print("   3. Begin implementing real module functionality")
    print("   4. Add comprehensive testing")
    print("   5. Security review and hardening")
    
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())