"""Network Speedtest Monitor - Internet speed testing using speedtest-cli"""
try:
    import speedtest
    SPEEDTEST_AVAILABLE = True
except ImportError:
    SPEEDTEST_AVAILABLE = False

def get_net_speedtest():
    """Get internet speed test results"""
    if not SPEEDTEST_AVAILABLE:
        return {"error": "speedtest-cli not installed. Run: pip install speedtest-cli"}

    try:
        # Create speedtest instance
        st = speedtest.Speedtest()
        
        # Get best server based on ping
        st.get_best_server()
        
        # Perform download test
        download_speed = st.download()
        
        # Perform upload test  
        upload_speed = st.upload()
        
        # Get ping
        ping = st.results.ping
        
        # Get server info
        server = st.results.server
        
        return {
            "download_mbps": round((download_speed / 1_000_000), 2),
            "upload_mbps": round((upload_speed / 1_000_000), 2),
            "download_bytes_per_sec": int(download_speed / 8),
            "upload_bytes_per_sec": int(upload_speed / 8),
            "ping_ms": round(ping, 2),
            "server": {
                "name": server.get("name", "Unknown"),
                "country": server.get("country", "Unknown"),
                "sponsor": server.get("sponsor", "Unknown"),
                "id": server.get("id", "Unknown")
            },
            "test_completed": True
        }
    except Exception as e:
        return {"error": str(e), "test_completed": False}