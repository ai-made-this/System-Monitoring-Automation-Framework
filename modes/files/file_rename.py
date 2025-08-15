"""File Rename Module - Renames files and directories"""
import os
from pathlib import Path
import shutil
from datetime import datetime

def rename_file(old_path, new_path, create_backup=False):
    """Rename a file or directory"""
    try:
        old_file = Path(old_path)
        new_file = Path(new_path)
        
        if not old_file.exists():
            return {"error": f"Source path {old_path} does not exist"}
        
        if new_file.exists():
            return {"error": f"Destination path {new_path} already exists"}
        
        # Create backup if requested
        backup_path = None
        if create_backup and old_file.is_file():
            backup_path = old_file.with_suffix(old_file.suffix + '.backup')
            shutil.copy2(old_file, backup_path)
        
        # Perform rename
        old_file.rename(new_file)
        
        return {
            "success": True,
            "old_path": str(old_file.absolute()),
            "new_path": str(new_file.absolute()),
            "backup_created": str(backup_path.absolute()) if backup_path else None,
            "is_directory": new_file.is_dir(),
            "renamed_at": datetime.now().isoformat()
        }
    except Exception as e:
        return {"error": str(e)}

def batch_rename(directory, pattern, replacement, file_extension=None):
    """Batch rename files in a directory"""
    try:
        dir_path = Path(directory)
        if not dir_path.exists() or not dir_path.is_dir():
            return {"error": f"Directory {directory} does not exist"}
        
        renamed_files = []
        errors = []
        
        for file_path in dir_path.iterdir():
            if file_path.is_file():
                # Filter by extension if specified
                if file_extension and not file_path.suffix.lower() == file_extension.lower():
                    continue
                
                # Apply pattern replacement
                if pattern in file_path.stem:
                    new_name = file_path.stem.replace(pattern, replacement) + file_path.suffix
                    new_path = file_path.parent / new_name
                    
                    try:
                        file_path.rename(new_path)
                        renamed_files.append({
                            "old_name": file_path.name,
                            "new_name": new_name
                        })
                    except Exception as e:
                        errors.append({
                            "file": file_path.name,
                            "error": str(e)
                        })
        
        return {
            "success": True,
            "directory": str(dir_path.absolute()),
            "renamed_count": len(renamed_files),
            "renamed_files": renamed_files,
            "errors": errors,
            "pattern": pattern,
            "replacement": replacement
        }
    except Exception as e:
        return {"error": str(e)}

def get_file_rename():
    """Get file rename capabilities and statistics"""
    try:
        return {
            "functions": {
                "rename_file": "rename_file(old_path, new_path, create_backup=False)",
                "batch_rename": "batch_rename(directory, pattern, replacement, file_extension=None)"
            },
            "examples": {
                "single_rename": "rename_file('old_name.txt', 'new_name.txt')",
                "with_backup": "rename_file('important.txt', 'important_v2.txt', create_backup=True)",
                "batch_rename": "batch_rename('/path/to/files', 'old_pattern', 'new_pattern', '.txt')"
            }
        }
    except Exception as e:
        return {"error": str(e)}