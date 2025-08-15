"""File Copy Module - Copies files and directories"""
import shutil
from pathlib import Path
from datetime import datetime
import hashlib

def copy_file(source, destination, preserve_metadata=True, verify_copy=False):
    """Copy a file or directory"""
    try:
        src_path = Path(source)
        dst_path = Path(destination)
        
        if not src_path.exists():
            return {"error": f"Source {source} does not exist"}
        
        # Create destination directory if needed
        if src_path.is_file():
            dst_path.parent.mkdir(parents=True, exist_ok=True)
        else:
            dst_path.mkdir(parents=True, exist_ok=True)
        
        # Perform copy
        if src_path.is_file():
            if preserve_metadata:
                shutil.copy2(src_path, dst_path)
            else:
                shutil.copy(src_path, dst_path)
        else:
            shutil.copytree(src_path, dst_path, dirs_exist_ok=True)
        
        result = {
            "success": True,
            "source": str(src_path.absolute()),
            "destination": str(dst_path.absolute()),
            "is_directory": src_path.is_dir(),
            "copied_at": datetime.now().isoformat(),
            "preserve_metadata": preserve_metadata
        }
        
        # Verify copy if requested
        if verify_copy and src_path.is_file():
            try:
                src_hash = _get_file_hash(src_path)
                dst_hash = _get_file_hash(dst_path)
                result["verified"] = src_hash == dst_hash
                result["source_hash"] = src_hash
                result["destination_hash"] = dst_hash
            except Exception as e:
                result["verification_error"] = str(e)
        
        return result
    except Exception as e:
        return {"error": str(e)}

def batch_copy(source_dir, destination_dir, file_pattern="*", preserve_structure=True):
    """Batch copy files matching pattern"""
    try:
        src_path = Path(source_dir)
        dst_path = Path(destination_dir)
        
        if not src_path.exists():
            return {"error": f"Source directory {source_dir} does not exist"}
        
        dst_path.mkdir(parents=True, exist_ok=True)
        
        copied_files = []
        errors = []
        total_size = 0
        
        for file_path in src_path.rglob(file_pattern):
            if file_path.is_file():
                try:
                    if preserve_structure:
                        # Maintain directory structure
                        rel_path = file_path.relative_to(src_path)
                        dest_file = dst_path / rel_path
                        dest_file.parent.mkdir(parents=True, exist_ok=True)
                    else:
                        # Flatten structure
                        dest_file = dst_path / file_path.name
                    
                    shutil.copy2(file_path, dest_file)
                    size = file_path.stat().st_size
                    total_size += size
                    
                    copied_files.append({
                        "source": str(file_path),
                        "destination": str(dest_file),
                        "size_bytes": size
                    })
                except Exception as e:
                    errors.append({
                        "file": str(file_path),
                        "error": str(e)
                    })
        
        return {
            "success": True,
            "source_directory": str(src_path.absolute()),
            "destination_directory": str(dst_path.absolute()),
            "copied_count": len(copied_files),
            "copied_files": copied_files,
            "total_size_mb": round(total_size / 1024 / 1024, 2),
            "errors": errors,
            "pattern": file_pattern,
            "preserve_structure": preserve_structure
        }
    except Exception as e:
        return {"error": str(e)}

def _get_file_hash(file_path):
    """Calculate MD5 hash of a file"""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def get_file_copy():
    """Get file copy capabilities"""
    try:
        return {
            "functions": {
                "copy_file": "copy_file(source, destination, preserve_metadata=True, verify_copy=False)",
                "batch_copy": "batch_copy(source_dir, destination_dir, file_pattern='*', preserve_structure=True)"
            },
            "features": [
                "Metadata preservation",
                "Copy verification with hash comparison",
                "Batch copying with pattern matching",
                "Directory structure preservation"
            ],
            "examples": {
                "simple_copy": "copy_file('source.txt', 'backup.txt')",
                "verified_copy": "copy_file('important.txt', 'backup.txt', verify_copy=True)",
                "batch_copy": "batch_copy('/source/dir', '/backup/dir', '*.txt')"
            }
        }
    except Exception as e:
        return {"error": str(e)}