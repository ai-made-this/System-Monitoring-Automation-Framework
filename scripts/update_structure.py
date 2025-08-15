#!/usr/bin/env python3
"""
Auto-Update Structure Script
Automatically updates Current_Structure.txt when modules are added/changed
"""

import os
import json
from pathlib import Path
from datetime import datetime

def scan_modes_directory():
    """Scan the modes directory and build structure data"""
    modes_dir = Path(__file__).parent.parent / "modes"
    if not modes_dir.exists():
        return {}
    
    structure = {}
    total_modules = 0
    
    for category_dir in sorted(modes_dir.iterdir()):
        if not category_dir.is_dir() or category_dir.name.startswith('.') or category_dir.name == '__pycache__':
            continue
        
        category_name = category_dir.name
        modules = []
        
        # Find all .py files that aren't __init__.py or aggregator.py
        for py_file in category_dir.glob("*.py"):
            if py_file.name not in ["__init__.py", "aggregator.py"]:
                modules.append(py_file.stem)
        
        if modules:  # Only include categories with modules
            structure[category_name] = {
                "modules": sorted(modules),
                "count": len(modules),
                "description": _get_category_description(category_name)
            }
            total_modules += len(modules)
    
    return structure, total_modules

def _get_category_description(category_name):
    """Get description for each category"""
    descriptions = {
        "ai": "AI & Intelligence",
        "applications": "Application monitoring",
        "audio": "Audio monitoring and optimization",
        "automation": "Task automation & recording",
        "cloud": "Cloud integration",
        "communication": "External communication",
        "cpu": "CPU monitoring",
        "development": "Development tools",
        "environment": "Hardware environment",
        "files": "File system operations",
        "gaming": "Gaming automation",
        "gpu": "GPU monitoring",
        "health": "System health & diagnostics",
        "input": "User input tracking",
        "memory": "Memory monitoring",
        "ml": "Machine Learning",
        "network": "Network monitoring",
        "performance": "Performance analysis",
        "power": "Power management",
        "productivity": "Productivity tracking",
        "security": "Security monitoring",
        "service": "Background services",
        "storage": "Storage monitoring",
        "system": "System information",
        "system_control": "System control operations",
        "visual": "Visual analysis"
    }
    return descriptions.get(category_name, f"{category_name.title()} modules")

def generate_structure_content(structure, total_modules):
    """Generate the content for Current_Structure.txt"""
    category_count = len(structure)
    
    content = f"""# System Monitoring & Automation Framework - Current Structure

## Overview
A comprehensive modular system with {category_count} categories and {total_modules}+ individual modules for monitoring hardware, system performance, user activity, and automating tasks. Each module performs a single function with auto-generated aggregators.

## Key Features
- **Modular Design**: Each .py file does exactly one thing
- **Auto-Aggregation**: Drop files in folders, run build script, everything's wired
- **Mode System**: basic/detailed/all modes per category  
- **CLI Access**: Every module accessible via command line
- **Cross-Platform**: Windows-focused with extensibility

## Total: {category_count} Categories, {total_modules}+ Individual Modules

modes/
"""
    
    # Add each category
    for category_name, category_data in structure.items():
        module_count = category_data["count"]
        description = category_data["description"]
        
        content += f"├── {category_name}/{'':20} # {description} ({module_count} modules)\n"
        
        # Add modules for this category
        modules = category_data["modules"]
        for i, module in enumerate(modules):
            is_last_module = (i == len(modules) - 1)
            prefix = "│   ├── " if not is_last_module else "│   ├── "
            
            # Add module description
            module_desc = _get_module_description(category_name, module)
            content += f"{prefix}{module}.py{'':15} # {module_desc}\n"
        
        # Add auto-generated files
        content += f"│   ├── aggregator.py{'':10} # Auto-generated\n"
        content += f"│   └── config.json{'':12} # Auto-generated\n"
    
    content += "└── __init__.py\n\n"
    
    # Add footer
    content += f"""build_aggregators.py       # Auto-generates all aggregators
main_aggregator.py         # Master controller
global_config.json         # System-wide settings
update_structure.py        # Auto-update structure file

## Usage Examples
```bash
# Monitor everything
python main_aggregator.py all

# Specific categories
python main_aggregator.py detailed cpu memory audio ai

# List all categories
python main_aggregator.py list

# Individual category
python -m modes.audio.aggregator detailed
```

## Auto-Update System
This structure file is automatically updated when:
- New modules are added to any category
- New categories are created
- Modules are renamed or moved
- Run: python update_structure.py

Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    return content

def _get_module_description(category, module):
    """Get description for individual modules"""
    descriptions = {
        # AI modules
        "habit_analyzer": "User behavior pattern analysis",
        "pattern_recognition": "System usage pattern detection", 
        "predictive_analysis": "Future needs prediction",
        "decision_engine": "Intelligent decision making",
        "autonomous_control": "Take control of apps/games",
        "learning_engine": "Continuous learning system",
        "query_processor": "Natural language queries",
        
        # Audio modules
        "audio_levels": "Real-time audio level monitoring",
        "device_manager": "Audio device management",
        "sound_analysis": "Advanced audio analysis",
        "voice_activity": "Voice activity detection",
        "audio_optimization": "Intelligent audio optimization",
        "meeting_audio": "Meeting audio enhancement",
        
        # ML modules
        "anomaly_detection": "ML-based anomaly detection",
        "behavioral_modeling": "User behavior prediction",
        "performance_prediction": "System performance forecasting",
        "neural_networks": "Deep learning infrastructure",
        "feature_engineering": "Advanced feature extraction",
        "model_training": "ML training pipeline",
        
        # Service modules
        "background_monitor": "Continuous system monitoring",
        "continuous_learning": "Always-on ML learning",
        "system_service": "Service management and control",
        
        # CPU modules
        "cpuspeed": "Clock speed monitoring",
        "cputemp": "Temperature monitoring", 
        "cpu_usage": "Usage percentage",
        
        # Memory modules
        "memtotal": "Total memory",
        "memfree": "Available memory",
        "memusage": "Memory usage percentage",
        
        # GPU modules
        "gpuspeed": "GPU clock speed",
        "gputemp": "GPU temperature",
        "gpu_usage": "GPU usage/memory",
        
        # Add more as needed...
    }
    
    return descriptions.get(module, f"{module.replace('_', ' ').title()}")

def update_structure_file():
    """Update the Current_Structure.txt file"""
    try:
        print("🔄 Scanning modes directory...")
        structure, total_modules = scan_modes_directory()
        
        if not structure:
            print("❌ No modules found in modes directory")
            return False
        
        print(f"📊 Found {len(structure)} categories with {total_modules} total modules")
        
        # Generate new content
        print("📝 Generating structure content...")
        content = generate_structure_content(structure, total_modules)
        
        # Write to file
        structure_file = Path(__file__).parent.parent / "Current_Structure.txt"
        with open(structure_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Updated {structure_file}")
        print(f"📈 System now has {len(structure)} categories and {total_modules} modules")
        
        # Show summary
        print("\n📋 Category Summary:")
        for category, data in structure.items():
            print(f"   {category:15} - {data['count']:2} modules - {data['description']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error updating structure: {e}")
        return False

def watch_for_changes():
    """Watch for changes in the modes directory (basic implementation)"""
    print("👁️  Watching modes directory for changes...")
    print("💡 Run this script manually after adding modules, or integrate with file watcher")
    print("🔄 To auto-update: python update_structure.py")

def main():
    """Main function"""
    print("🚀 System Structure Auto-Updater")
    print("=" * 40)
    
    success = update_structure_file()
    
    if success:
        print("\n🎉 Structure file updated successfully!")
        print("\n💡 Integration options:")
        print("   • Run manually: python update_structure.py")
        print("   • Add to build_aggregators.py for automatic updates")
        print("   • Set up file watcher for real-time updates")
    else:
        print("\n❌ Failed to update structure file")
        return 1
    
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())