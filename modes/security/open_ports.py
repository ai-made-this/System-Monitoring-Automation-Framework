"""Open Ports Monitor - Lists open network ports"""
import psutil

def get_open_ports():
    """Get open network ports"""
    try:
        connections = psutil.net_connections()
        listening_ports = []
        established_connections = []
        
        for conn in connections:
            if conn.status == 'LISTEN':
                listening_ports.append({
                    "port": conn.laddr.port,
                    "address": conn.laddr.ip,
                    "family": conn.family.name,
                    "type": conn.type.name,
                    "pid": conn.pid
                })
            elif conn.status == 'ESTABLISHED':
                established_connections.append({
                    "local_port": conn.laddr.port,
                    "remote_address": conn.raddr.ip if conn.raddr else None,
                    "remote_port": conn.raddr.port if conn.raddr else None,
                    "pid": conn.pid
                })
        
        return {
            "listening_ports": listening_ports,
            "listening_count": len(listening_ports),
            "established_connections": established_connections[:10],  # Top 10
            "established_count": len(established_connections)
        }
    except Exception as e:
        return {"error": str(e)}