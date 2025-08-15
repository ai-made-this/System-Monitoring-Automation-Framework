#!/usr/bin/env python3
"""
Setup Auto-Update System
Configure automatic structure file updates
"""

import os
import sys
from pathlib import Path


def setup_git_hooks():
    """Setup git hooks to auto-update structure on commits"""
    try:
        git_dir = Path(".git")
        if not git_dir.exists():
            print("⚠️  No git repository found - skipping git hooks")
            return False

        hooks_dir = git_dir / "hooks"
        hooks_dir.mkdir(exist_ok=True)

        # Create pre-commit hook
        pre_commit_hook = hooks_dir / "pre-commit"
        hook_content = """#!/bin/sh
# Auto-update structure file before commit
echo "🔄 Auto-updating Current_Structure.txt..."
python update_structure.py
git add Current_Structure.txt
"""

        with open(pre_commit_hook, "w") as f:
            f.write(hook_content)

        # Make executable (Unix/Linux/Mac)
        if os.name != "nt":
            os.chmod(pre_commit_hook, 0o755)

        print(f"✅ Created git pre-commit hook: {pre_commit_hook}")
        return True

    except Exception as e:
        print(f"❌ Failed to setup git hooks: {e}")
        return False


def setup_vscode_tasks():
    """Setup VS Code tasks for easy structure updates"""
    try:
        vscode_dir = Path(".vscode")
        vscode_dir.mkdir(exist_ok=True)

        tasks_file = vscode_dir / "tasks.json"

        tasks_config = {
            "version": "2.0.0",
            "tasks": [
                {
                    "label": "Update Structure File",
                    "type": "shell",
                    "command": "python",
                    "args": ["update_structure.py"],
                    "group": "build",
                    "presentation": {
                        "echo": True,
                        "reveal": "always",
                        "focus": False,
                        "panel": "shared",
                    },
                    "problemMatcher": [],
                },
                {
                    "label": "Build Aggregators + Update Structure",
                    "type": "shell",
                    "command": "python",
                    "args": ["build_aggregators.py"],
                    "group": {"kind": "build", "isDefault": True},
                    "presentation": {
                        "echo": True,
                        "reveal": "always",
                        "focus": False,
                        "panel": "shared",
                    },
                    "problemMatcher": [],
                },
                {
                    "label": "Watch Structure Changes",
                    "type": "shell",
                    "command": "python",
                    "args": ["watch_structure.py"],
                    "group": "build",
                    "presentation": {
                        "echo": True,
                        "reveal": "always",
                        "focus": True,
                        "panel": "dedicated",
                    },
                    "isBackground": True,
                    "problemMatcher": [],
                },
            ],
        }

        import json

        with open(tasks_file, "w") as f:
            json.dump(tasks_config, f, indent=2)

        print(f"✅ Created VS Code tasks: {tasks_file}")
        print("💡 Use Ctrl+Shift+P -> 'Tasks: Run Task' to access")
        return True

    except Exception as e:
        print(f"❌ Failed to setup VS Code tasks: {e}")
        return False


def create_batch_scripts():
    """Create convenient batch scripts for Windows"""
    try:
        # Update structure script
        update_bat = Path("update_structure.bat")
        with open(update_bat, "w", encoding="utf-8") as f:
            f.write("""@echo off
title Update Structure File
echo Updating Current_Structure.txt...
python update_structure.py
pause
""")

        # Watch structure script
        watch_bat = Path("watch_structure.bat")
        with open(watch_bat, "w", encoding="utf-8") as f:
            f.write("""@echo off
title Structure File Watcher
echo Starting structure file watcher...
python watch_structure.py
pause
""")

        # Build and update script
        build_bat = Path("build_and_update.bat")
        with open(build_bat, "w", encoding="utf-8") as f:
            f.write("""@echo off
title Build Aggregators and Update Structure
echo Building aggregators and updating structure...
python build_aggregators.py
pause
""")

        print("✅ Created Windows batch scripts:")
        print(f"   📝 {update_bat}")
        print(f"   👁️ {watch_bat}")
        print(f"   🔧 {build_bat}")
        return True

    except Exception as e:
        print(f"❌ Failed to create batch scripts: {e}")
        return False


def test_auto_update():
    """Test the auto-update system"""
    try:
        print("🧪 Testing auto-update system...")

        sys.path.append(str(Path(__file__).parent))
        from update_structure import update_structure_file

        success = update_structure_file()

        if success:
            print("✅ Auto-update system working correctly")
            return True
        else:
            print("❌ Auto-update system test failed")
            return False

    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False


def main():
    """Main setup function"""
    print("🚀 Auto-Update System Setup")
    print("=" * 40)

    success_count = 0
    total_tasks = 4

    # Test the system first
    if test_auto_update():
        success_count += 1
        print()

    # Setup git hooks
    if setup_git_hooks():
        success_count += 1
    print()

    # Setup VS Code tasks
    if setup_vscode_tasks():
        success_count += 1
    print()

    # Create batch scripts
    if create_batch_scripts():
        success_count += 1
    print()

    # Summary
    print("📊 Setup Summary:")
    print(f"   ✅ {success_count}/{total_tasks} tasks completed successfully")

    if success_count == total_tasks:
        print("\n🎉 Auto-update system fully configured!")
        print("\n💡 How to use:")
        print("   • Automatic: Structure updates when you run build_aggregators.py")
        print(
            "   • Manual: Run update_structure.py or double-click update_structure.bat"
        )
        print(
            "   • Real-time: Run watch_structure.py or double-click watch_structure.bat"
        )
        print("   • VS Code: Use Ctrl+Shift+P -> 'Tasks: Run Task'")
        print("   • Git: Structure auto-updates on commits (if git repo)")

        print("\n🔄 Integration Status:")
        print("   ✅ build_aggregators.py - Auto-updates structure after building")
        print("   ✅ update_structure.py - Manual structure updates")
        print("   ✅ watch_structure.py - Real-time file watching")
        print("   ✅ Git hooks - Auto-update on commits")
        print("   ✅ VS Code tasks - IDE integration")
        print("   ✅ Batch scripts - Windows convenience scripts")

    else:
        print(f"\n⚠️  Setup completed with {total_tasks - success_count} issues")
        print("💡 You can still use the basic auto-update functionality")

    return 0 if success_count >= 2 else 1


if __name__ == "__main__":
    sys.exit(main())
