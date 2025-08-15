"""File Search Module - Search for files and content"""
import os
from pathlib import Path
import re
from datetime import datetime, timedelta

def search_files(directory, name_pattern=None, content_pattern=None, file_extension=None, 
                modified_within_days=None, size_min_mb=None, size_max_mb=None):
    """Search for files based on various criteria"""
    try:
        dir_path = Path(directory)
        if not dir_path.exists():
            return {"error": f"Directory {directory} does not exist"}
        
        found_files = []
        
        # Calculate time threshold if specified
        time_threshold = None
        if modified_within_days:
            time_threshold = datetime.now() - timedelta(days=modified_within_days)
        
        for file_path in dir_path.rglob("*"):
            if not file_path.is_file():
                continue
            
            # Check file extension
            if file_extension and not file_path.suffix.lower() == file_extension.lower():
                continue
            
            # Check name pattern
            if name_pattern and not re.search(name_pattern, file_path.name, re.IGNORECASE):
                continue
            
            # Check file size
            file_size_mb = file_path.stat().st_size / 1024 / 1024
            if size_min_mb and file_size_mb < size_min_mb:
                continue
            if size_max_mb and file_size_mb > size_max_mb:
                continue
            
            # Check modification time
            if time_threshold:
                mod_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                if mod_time < time_threshold:
                    continue
            
            # Check content pattern
            content_match = False
            if content_pattern:
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        if re.search(content_pattern, content, re.IGNORECASE):
                            content_match = True
                        else:
                            continue
                except:
                    continue
            
            # File matches all criteria
            file_info = {
                "path": str(file_path.absolute()),
                "name": file_path.name,
                "size_mb": round(file_size_mb, 2),
                "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
                "extension": file_path.suffix
            }
            
            if content_pattern and content_match:
                file_info["content_match"] = True
            
            found_files.append(file_info)
        
        return {
            "success": True,
            "directory": str(dir_path.absolute()),
            "found_count": len(found_files),
            "found_files": found_files,
            "search_criteria": {
                "name_pattern": name_pattern,
                "content_pattern": content_pattern,
                "file_extension": file_extension,
                "modified_within_days": modified_within_days,
                "size_min_mb": size_min_mb,
                "size_max_mb": size_max_mb
            }
        }
    except Exception as e:
        return {"error": str(e)}

def find_duplicates(directory, compare_by="name"):
    """Find duplicate files in directory"""
    try:
        dir_path = Path(directory)
        if not dir_path.exists():
            return {"error": f"Directory {directory} does not exist"}
        
        files_dict = {}
        duplicates = []
        
        for file_path in dir_path.rglob("*"):
            if not file_path.is_file():
                continue
            
            if compare_by == "name":
                key = file_path.name
            elif compare_by == "size":
                key = file_path.stat().st_size
            elif compare_by == "content":
                try:
                    import hashlib
                    hash_md5 = hashlib.md5()
                    with open(file_path, "rb") as f:
                        for chunk in iter(lambda: f.read(4096), b""):
                            hash_md5.update(chunk)
                    key = hash_md5.hexdigest()
                except:
                    continue
            else:
                return {"error": "compare_by must be 'name', 'size', or 'content'"}
            
            if key in files_dict:
                files_dict[key].append(file_path)
            else:
                files_dict[key] = [file_path]
        
        # Find duplicates
        for key, file_list in files_dict.items():
            if len(file_list) > 1:
                duplicate_group = {
                    "key": key,
                    "count": len(file_list),
                    "files": [
                        {
                            "path": str(f.absolute()),
                            "size_mb": round(f.stat().st_size / 1024 / 1024, 2),
                            "modified": datetime.fromtimestamp(f.stat().st_mtime).isoformat()
                        }
                        for f in file_list
                    ]
                }
                duplicates.append(duplicate_group)
        
        return {
            "success": True,
            "directory": str(dir_path.absolute()),
            "duplicate_groups": len(duplicates),
            "duplicates": duplicates,
            "compare_by": compare_by
        }
    except Exception as e:
        return {"error": str(e)}

def get_file_search():
    """Get file search capabilities"""
    try:
        return {
            "functions": {
                "search_files": "search_files(directory, name_pattern=None, content_pattern=None, file_extension=None, modified_within_days=None, size_min_mb=None, size_max_mb=None)",
                "find_duplicates": "find_duplicates(directory, compare_by='name')"
            },
            "search_criteria": [
                "File name pattern (regex)",
                "File content pattern (regex)",
                "File extension",
                "Modification time",
                "File size range"
            ],
            "duplicate_detection": ["by name", "by size", "by content (hash)"],
            "examples": {
                "name_search": "search_files('/path', name_pattern='.*\\.py$')",
                "content_search": "search_files('/path', content_pattern='TODO')",
                "recent_files": "search_files('/path', modified_within_days=7)",
                "find_duplicates": "find_duplicates('/path', compare_by='content')"
            }
        }
    except Exception as e:
        return {"error": str(e)}