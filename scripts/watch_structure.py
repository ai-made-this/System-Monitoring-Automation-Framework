#!/usr/bin/env python3
"""
Structure File Watcher
Automatically updates Current_Structure.txt when files change in modes directory
"""

import time
import os
from pathlib import Path
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))
from update_structure import update_structure_file

class SimpleFileWatcher:
    def __init__(self, watch_dir):
        self.watch_dir = Path(__file__).parent.parent / watch_dir
        self.last_scan = {}
        self.scan_directory()
    
    def scan_directory(self):
        """Scan directory and record file modification times"""
        current_scan = {}
        
        if not self.watch_dir.exists():
            return current_scan
        
        for root, dirs, files in os.walk(self.watch_dir):
            # Skip __pycache__ directories
            dirs[:] = [d for d in dirs if d != '__pycache__']
            
            for file in files:
                if file.endswith('.py'):
                    file_path = Path(root) / file
                    try:
                        current_scan[str(file_path)] = file_path.stat().st_mtime
                    except OSError:
                        pass
        
        return current_scan
    
    def check_for_changes(self):
        """Check if any files have changed"""
        current_scan = self.scan_directory()
        
        # Check for new, modified, or deleted files
        changes = []
        
        # New or modified files
        for file_path, mtime in current_scan.items():
            if file_path not in self.last_scan:
                changes.append(f"Added: {file_path}")
            elif self.last_scan[file_path] != mtime:
                changes.append(f"Modified: {file_path}")
        
        # Deleted files
        for file_path in self.last_scan:
            if file_path not in current_scan:
                changes.append(f"Deleted: {file_path}")
        
        self.last_scan = current_scan
        return changes

def main():
    """Main file watcher function"""
    print("👁️  Structure File Watcher")
    print("=" * 40)
    print("🔄 Watching modes/ directory for changes...")
    print("📝 Will auto-update Current_Structure.txt when modules are added/changed")
    print("🛑 Press Ctrl+C to stop")
    print()
    
    watcher = SimpleFileWatcher("modes")
    
    try:
        while True:
            changes = watcher.check_for_changes()
            
            if changes:
                print(f"🔍 Detected {len(changes)} changes:")
                for change in changes[:5]:  # Show first 5 changes
                    print(f"   {change}")
                if len(changes) > 5:
                    print(f"   ... and {len(changes) - 5} more")
                
                print("🔄 Updating structure file...")
                if update_structure_file():
                    print("✅ Structure file updated successfully")
                else:
                    print("❌ Failed to update structure file")
                print()
            
            time.sleep(2)  # Check every 2 seconds
            
    except KeyboardInterrupt:
        print("\n🛑 File watcher stopped")
        return 0
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1

if __name__ == "__main__":
    import sys
    sys.exit(main())