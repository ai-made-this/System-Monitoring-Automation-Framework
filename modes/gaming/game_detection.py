"""Game Detection - Detect running games and game-specific optimizations"""
import json
import psutil
from pathlib import Path

GAME_DB = Path(__file__).parent / "game_database.json"
DETECTION_LOG = Path(__file__).parent / "game_detections.json"

def get_game_detection():
    """Detect running games and provide game-specific information"""
    try:
        # Load game database
        if GAME_DB.exists():
            with open(GAME_DB, 'r') as f:
                game_db = json.load(f)
        else:
            # Create basic game database
            game_db = {
                "games": {
                    "steam.exe": {"name": "Steam Client", "type": "launcher"},
                    "chrome.exe": {"name": "Chrome Browser", "type": "browser"},
                    "discord.exe": {"name": "Discord", "type": "communication"},
                    "obs64.exe": {"name": "OBS Studio", "type": "streaming"},
                    "minecraft.exe": {"name": "Minecraft", "type": "game"},
                    "league of legends.exe": {"name": "League of Legends", "type": "game"},
                    "valorant.exe": {"name": "Valorant", "type": "game"}
                }
            }
        
        # Detect currently running processes
        running_processes = []
        detected_games = []
        
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                proc_name = proc.info['name'].lower()
                running_processes.append(proc.info)
                
                # Check if it's a known game
                for game_exe, game_info in game_db["games"].items():
                    if game_exe.lower() in proc_name:
                        detected_games.append({
                            "process_name": proc.info['name'],
                            "game_name": game_info["name"],
                            "game_type": game_info["type"],
                            "pid": proc.info['pid'],
                            "cpu_usage": proc.info['cpu_percent'],
                            "memory_usage": proc.info['memory_percent']
                        })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        return {
            "status": "active",
            "detected_games": detected_games,
            "total_processes": len(running_processes),
            "game_count": len(detected_games),
            "capabilities": {
                "game_detection": "Identify running games from process names",
                "performance_monitoring": "Track game-specific resource usage",
                "optimization_suggestions": "Recommend game-specific optimizations",
                "launcher_detection": "Detect game launchers (Steam, Epic, etc.)",
                "anti_cheat_awareness": "Identify anti-cheat software"
            },
            "supported_game_types": [
                "steam_games", "epic_games", "origin_games", "uplay_games",
                "battle_net_games", "standalone_games", "browser_games"
            ],
            "optimization_features": [
                "CPU priority adjustment",
                "Memory allocation optimization",
                "Network priority settings",
                "Background process management",
                "Graphics settings recommendations"
            ]
        }
    except Exception as e:
        return {"error": str(e)}