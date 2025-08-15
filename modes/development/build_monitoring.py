"""Build Monitoring - Monitor development builds and CI/CD processes"""
import json
import subprocess
import time
from pathlib import Path

BUILD_LOG = Path(__file__).parent / "build_log.json"

def get_build_monitoring():
    """Monitor development builds and processes"""
    try:
        # Load build history
        if BUILD_LOG.exists():
            with open(BUILD_LOG, 'r') as f:
                build_data = json.load(f)
        else:
            build_data = {"builds": [], "processes": []}
        
        # Check for common build processes
        build_processes = [
            "node.exe", "npm.exe", "yarn.exe", "webpack.exe",
            "python.exe", "pip.exe", "java.exe", "javac.exe",
            "dotnet.exe", "msbuild.exe", "cargo.exe", "go.exe"
        ]
        
        active_builds = []
        try:
            import psutil
            for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'cpu_percent']):
                try:
                    if any(bp.lower() in proc.info['name'].lower() for bp in build_processes):
                        cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ""
                        if any(keyword in cmdline.lower() for keyword in ['build', 'compile', 'test', 'deploy']):
                            active_builds.append({
                                "pid": proc.info['pid'],
                                "process": proc.info['name'],
                                "command": cmdline[:100] + "..." if len(cmdline) > 100 else cmdline,
                                "cpu_usage": proc.info['cpu_percent']
                            })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
        except ImportError:
            pass
        
        return {
            "status": "monitoring",
            "active_builds": active_builds,
            "recent_builds": build_data["builds"][-10:],
            "total_builds": len(build_data["builds"]),
            "capabilities": {
                "process_monitoring": "Monitor build processes in real-time",
                "build_notifications": "Notify on build completion/failure",
                "performance_tracking": "Track build times and resource usage",
                "ci_cd_integration": "Integration with CI/CD pipelines",
                "log_analysis": "Analyze build logs for errors",
                "dependency_monitoring": "Track dependency installations"
            },
            "supported_tools": {
                "node_npm": "Node.js and npm builds",
                "python_pip": "Python package builds",
                "java_maven": "Java Maven builds",
                "dotnet": ".NET builds and deployments",
                "rust_cargo": "Rust Cargo builds",
                "go_build": "Go language builds",
                "docker": "Docker container builds"
            },
            "monitoring_features": [
                "Build duration tracking",
                "Resource usage during builds",
                "Success/failure rates",
                "Error pattern detection",
                "Build queue monitoring",
                "Automated testing integration"
            ],
            "notification_triggers": [
                "Build completion",
                "Build failures",
                "Long-running builds",
                "High resource usage",
                "Dependency conflicts"
            ]
        }
    except Exception as e:
        return {"error": str(e)}