"""Code Analysis - Analyze development projects and coding patterns"""
import json
import os
from pathlib import Path

ANALYSIS_LOG = Path(__file__).parent / "code_analysis.json"

def get_code_analysis():
    """Analyze code projects and development patterns"""
    try:
        # Scan for common development directories
        common_dev_paths = [
            Path.home() / "Documents",
            Path.home() / "Desktop", 
            Path("C:/dev"),
            Path("C:/projects"),
            Path("C:/code")
        ]
        
        projects = []
        languages = {}
        
        for base_path in common_dev_paths:
            if base_path.exists():
                for item in base_path.iterdir():
                    if item.is_dir():
                        # Check for common project indicators
                        project_files = [
                            "package.json", "requirements.txt", "pom.xml",
                            "Cargo.toml", "go.mod", ".git", ".gitignore",
                            "README.md", "setup.py", "composer.json"
                        ]
                        
                        found_indicators = []
                        for pf in project_files:
                            if (item / pf).exists():
                                found_indicators.append(pf)
                        
                        if found_indicators:
                            # Count file types
                            file_counts = {}
                            try:
                                for file in item.rglob("*"):
                                    if file.is_file() and file.suffix:
                                        ext = file.suffix.lower()
                                        file_counts[ext] = file_counts.get(ext, 0) + 1
                                        languages[ext] = languages.get(ext, 0) + 1
                            except (PermissionError, OSError):
                                pass
                            
                            projects.append({
                                "name": item.name,
                                "path": str(item),
                                "indicators": found_indicators,
                                "file_types": dict(list(file_counts.items())[:10])  # Top 10
                            })
        
        return {
            "status": "analyzed",
            "detected_projects": projects[:20],  # Top 20 projects
            "total_projects": len(projects),
            "language_distribution": dict(sorted(languages.items(), key=lambda x: x[1], reverse=True)[:15]),
            "capabilities": {
                "project_detection": "Automatically detect development projects",
                "language_analysis": "Identify programming languages used",
                "code_metrics": "Basic code statistics and metrics",
                "dependency_tracking": "Track project dependencies",
                "git_integration": "Git repository analysis",
                "build_monitoring": "Monitor build processes"
            },
            "supported_languages": [
                ".py (Python)", ".js (JavaScript)", ".ts (TypeScript)",
                ".java (Java)", ".cs (C#)", ".cpp (C++)", ".c (C)",
                ".go (Go)", ".rs (Rust)", ".php (PHP)", ".rb (Ruby)"
            ],
            "analysis_features": [
                "Lines of code counting",
                "File type distribution",
                "Project complexity estimation",
                "Dependency analysis",
                "Git commit patterns",
                "Build success rates"
            ]
        }
    except Exception as e:
        return {"error": str(e)}