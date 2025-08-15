"""Browser Tabs Monitor - Estimates browser tab usage"""
import psutil

def get_browser_tabs():
    """Estimate browser tab usage by process count"""
    try:
        browsers = {
            "chrome.exe": 0,
            "firefox.exe": 0,
            "msedge.exe": 0,
            "opera.exe": 0,
            "brave.exe": 0,
            "safari": 0
        }
        
        total_browser_memory = 0
        
        for proc in psutil.process_iter(['name', 'memory_info']):
            try:
                name = proc.info['name'].lower()
                for browser in browsers:
                    if browser.replace('.exe', '') in name:
                        browsers[browser] += 1
                        if proc.info['memory_info']:
                            total_browser_memory += proc.info['memory_info'].rss
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        return {
            "browser_processes": browsers,
            "estimated_total_tabs": sum(browsers.values()),
            "total_browser_memory_mb": round(total_browser_memory / 1024 / 1024, 2)
        }
    except Exception as e:
        return {"error": str(e)}