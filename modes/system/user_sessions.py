"""User Sessions Monitor - Lists active sessions/users"""
import psutil

def get_user_sessions():
    """Get active user sessions"""
    try:
        users = psutil.users()
        sessions = []
        for user in users:
            sessions.append({
                "name": user.name,
                "terminal": user.terminal,
                "host": user.host,
                "started": user.started,
                "pid": user.pid if hasattr(user, 'pid') else None
            })
        return {"active_sessions": sessions, "session_count": len(sessions)}
    except Exception as e:
        return {"error": str(e)}