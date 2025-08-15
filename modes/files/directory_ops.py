"""Directory Operations Module - Create, manage, and organize directories"""
import os
from pathlib import Path
import shutil
from datetime import datetime

def create_directory(directory_path, parents=True, exist_ok=True):
    """Create a directory"""
    try:
        dir_path = Path(directory_path)
        dir_path.mkdir(parents=parents, exist_ok=exist_ok)
        
        return {
            "success": True,
            "path": str(dir_path.absolute()),
            "created": datetime.now().isoformat(),
            "parents_created": parents,
            "already_existed": False  # Can't check after creation
        }
    except Exception as e:
        return {"error": str(e)}

def organize_files_by_extension(source_dir, destination_dir=None, create_subdirs=True):
    """Organize files into subdirectories by extension"""
    try:
        src_path = Path(source_dir)
        if not src_path.exists():
            return {"error": f"Source directory {source_dir} does not exist"}
        
        dst_path = Path(destination_dir) if destination_dir else src_path
        dst_path.mkdir(parents=True, exist_ok=True)
        
        organized_files = {}
        moved_count = 0
        
        for file_path in src_path.iterdir():
            if file_path.is_file():
                extension = file_path.suffix.lower() or "no_extension"
                
                # Create subdirectory for extension
                if create_subdirs:
                    ext_dir = dst_path / extension.replace('.', '')
                    ext_dir.mkdir(exist_ok=True)
                    dest_file = ext_dir / file_path.name
                else:
                    dest_file = dst_path / file_path.name
                
                # Move file
                if file_path != dest_file:
                    shutil.move(str(file_path), str(dest_file))
                    moved_count += 1
                    
                    if extension not in organized_files:
                        organized_files[extension] = []
                    organized_files[extension].append({
                        "original": str(file_path),
                        "new_location": str(dest_file)
                    })
        
        return {
            "success": True,
            "source_directory": str(src_path.absolute()),
            "destination_directory": str(dst_path.absolute()),
            "moved_count": moved_count,
            "extensions_found": list(organized_files.keys()),
            "organized_files": organized_files
        }
    except Exception as e:
        return {"error": str(e)}

def organize_files_by_date(source_dir, destination_dir=None, date_format="YYYY/MM"):
    """Organize files into subdirectories by creation/modification date"""
    try:
        src_path = Path(source_dir)
        if not src_path.exists():
            return {"error": f"Source directory {source_dir} does not exist"}
        
        dst_path = Path(destination_dir) if destination_dir else src_path
        dst_path.mkdir(parents=True, exist_ok=True)
        
        organized_files = {}
        moved_count = 0
        
        for file_path in src_path.iterdir():
            if file_path.is_file():
                # Get file modification time
                mod_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                
                # Create date-based subdirectory
                if date_format == "YYYY/MM":
                    date_dir = dst_path / str(mod_time.year) / f"{mod_time.month:02d}"
                elif date_format == "YYYY/MM/DD":
                    date_dir = dst_path / str(mod_time.year) / f"{mod_time.month:02d}" / f"{mod_time.day:02d}"
                elif date_format == "YYYY":
                    date_dir = dst_path / str(mod_time.year)
                else:
                    date_dir = dst_path / mod_time.strftime(date_format)
                
                date_dir.mkdir(parents=True, exist_ok=True)
                dest_file = date_dir / file_path.name
                
                # Move file
                if file_path != dest_file:
                    shutil.move(str(file_path), str(dest_file))
                    moved_count += 1
                    
                    date_key = str(date_dir.relative_to(dst_path))
                    if date_key not in organized_files:
                        organized_files[date_key] = []
                    organized_files[date_key].append({
                        "original": str(file_path),
                        "new_location": str(dest_file),
                        "date": mod_time.isoformat()
                    })
        
        return {
            "success": True,
            "source_directory": str(src_path.absolute()),
            "destination_directory": str(dst_path.absolute()),
            "moved_count": moved_count,
            "date_format": date_format,
            "organized_files": organized_files
        }
    except Exception as e:
        return {"error": str(e)}

def get_directory_stats(directory):
    """Get comprehensive directory statistics"""
    try:
        dir_path = Path(directory)
        if not dir_path.exists():
            return {"error": f"Directory {directory} does not exist"}
        
        stats = {
            "path": str(dir_path.absolute()),
            "total_files": 0,
            "total_directories": 0,
            "total_size_bytes": 0,
            "file_extensions": {},
            "largest_files": [],
            "oldest_file": None,
            "newest_file": None
        }
        
        oldest_time = float('inf')
        newest_time = 0
        
        for item in dir_path.rglob("*"):
            if item.is_file():
                stats["total_files"] += 1
                size = item.stat().st_size
                stats["total_size_bytes"] += size
                
                # Track extensions
                ext = item.suffix.lower() or "no_extension"
                if ext not in stats["file_extensions"]:
                    stats["file_extensions"][ext] = {"count": 0, "total_size": 0}
                stats["file_extensions"][ext]["count"] += 1
                stats["file_extensions"][ext]["total_size"] += size
                
                # Track largest files
                stats["largest_files"].append({
                    "path": str(item),
                    "size_mb": round(size / 1024 / 1024, 2)
                })
                
                # Track oldest/newest
                mod_time = item.stat().st_mtime
                if mod_time < oldest_time:
                    oldest_time = mod_time
                    stats["oldest_file"] = {
                        "path": str(item),
                        "modified": datetime.fromtimestamp(mod_time).isoformat()
                    }
                if mod_time > newest_time:
                    newest_time = mod_time
                    stats["newest_file"] = {
                        "path": str(item),
                        "modified": datetime.fromtimestamp(mod_time).isoformat()
                    }
            
            elif item.is_dir():
                stats["total_directories"] += 1
        
        # Sort largest files and keep top 10
        stats["largest_files"].sort(key=lambda x: x["size_mb"], reverse=True)
        stats["largest_files"] = stats["largest_files"][:10]
        
        # Convert total size to readable format
        stats["total_size_mb"] = round(stats["total_size_bytes"] / 1024 / 1024, 2)
        stats["total_size_gb"] = round(stats["total_size_bytes"] / 1024 / 1024 / 1024, 2)
        
        return {
            "success": True,
            **stats
        }
    except Exception as e:
        return {"error": str(e)}

def get_directory_ops():
    """Get directory operations capabilities"""
    try:
        return {
            "functions": {
                "create_directory": "create_directory(directory_path, parents=True, exist_ok=True)",
                "organize_files_by_extension": "organize_files_by_extension(source_dir, destination_dir=None, create_subdirs=True)",
                "organize_files_by_date": "organize_files_by_date(source_dir, destination_dir=None, date_format='YYYY/MM')",
                "get_directory_stats": "get_directory_stats(directory)"
            },
            "organization_methods": [
                "By file extension",
                "By creation/modification date",
                "Custom patterns"
            ],
            "date_formats": ["YYYY", "YYYY/MM", "YYYY/MM/DD", "custom strftime format"],
            "examples": {
                "create_dir": "create_directory('/new/path/to/dir')",
                "organize_by_ext": "organize_files_by_extension('/messy/folder')",
                "organize_by_date": "organize_files_by_date('/photos', date_format='YYYY/MM')",
                "get_stats": "get_directory_stats('/some/directory')"
            }
        }
    except Exception as e:
        return {"error": str(e)}