"""File Delete Module - Safely deletes files and directories"""
import os
from pathlib import Path
import shutil
import send2trash
from datetime import datetime

def delete_file(filepath, use_recycle_bin=True, force=False):
    """Delete a file or directory"""
    try:
        file_path = Path(filepath)
        
        if not file_path.exists():
            return {"error": f"Path {filepath} does not exist"}
        
        file_info = {
            "path": str(file_path.absolute()),
            "is_directory": file_path.is_dir(),
            "size_bytes": file_path.stat().st_size if file_path.is_file() else 0,
            "deleted_at": datetime.now().isoformat()
        }
        
        # Use recycle bin if available and requested
        if use_recycle_bin:
            try:
                send2trash.send2trash(str(file_path))
                file_info["method"] = "recycle_bin"
            except ImportError:
                # Fallback to permanent deletion if send2trash not available
                if file_path.is_dir():
                    shutil.rmtree(file_path)
                else:
                    file_path.unlink()
                file_info["method"] = "permanent_delete"
                file_info["warning"] = "send2trash not available, used permanent deletion"
        else:
            # Permanent deletion
            if file_path.is_dir():
                if force:
                    shutil.rmtree(file_path)
                else:
                    file_path.rmdir()  # Only works if directory is empty
            else:
                file_path.unlink()
            file_info["method"] = "permanent_delete"
        
        return {
            "success": True,
            **file_info
        }
    except Exception as e:
        return {"error": str(e)}

def cleanup_temp_files(directory, older_than_days=7, file_patterns=None):
    """Clean up temporary files older than specified days"""
    try:
        dir_path = Path(directory)
        if not dir_path.exists():
            return {"error": f"Directory {directory} does not exist"}
        
        if file_patterns is None:
            file_patterns = ["*.tmp", "*.temp", "*.log", "*~", "*.bak"]
        
        import time
        cutoff_time = time.time() - (older_than_days * 24 * 60 * 60)
        
        deleted_files = []
        total_size_freed = 0
        
        for pattern in file_patterns:
            for file_path in dir_path.glob(pattern):
                if file_path.is_file() and file_path.stat().st_mtime < cutoff_time:
                    try:
                        size = file_path.stat().st_size
                        send2trash.send2trash(str(file_path))
                        deleted_files.append({
                            "name": file_path.name,
                            "size_bytes": size
                        })
                        total_size_freed += size
                    except:
                        pass
        
        return {
            "success": True,
            "directory": str(dir_path.absolute()),
            "deleted_count": len(deleted_files),
            "deleted_files": deleted_files,
            "total_size_freed_mb": round(total_size_freed / 1024 / 1024, 2),
            "older_than_days": older_than_days,
            "patterns": file_patterns
        }
    except Exception as e:
        return {"error": str(e)}

def get_file_delete():
    """Get file deletion capabilities"""
    try:
        return {
            "functions": {
                "delete_file": "delete_file(filepath, use_recycle_bin=True, force=False)",
                "cleanup_temp_files": "cleanup_temp_files(directory, older_than_days=7, file_patterns=None)"
            },
            "safety_features": [
                "Recycle bin support (requires send2trash: pip install send2trash)",
                "Force flag required for non-empty directories",
                "File size and timestamp tracking"
            ],
            "examples": {
                "safe_delete": "delete_file('unwanted.txt')",
                "permanent_delete": "delete_file('unwanted.txt', use_recycle_bin=False)",
                "cleanup_temp": "cleanup_temp_files('/temp/folder', older_than_days=3)"
            }
        }
    except Exception as e:
        return {"error": str(e)}