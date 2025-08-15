"""GPU Temperature Monitor - Returns GPU temperature"""
try:
    import GPUtil
    GPU_AVAILABLE = True
except ImportError:
    GPU_AVAILABLE = False

def get_gpu_temp():
    """Get GPU temperature"""
    if not GPU_AVAILABLE:
        return {"error": "GPUtil not installed. Run: pip install GPUtil"}
    
    try:
        gpus = GPUtil.getGPUs()
        if not gpus:
            return {"error": "No GPUs detected"}
        
        gpu_temps = []
        for gpu in gpus:
            gpu_temps.append({
                "name": gpu.name,
                "temperature": gpu.temperature
            })
        return {"gpu_temperatures": gpu_temps}
    except Exception as e:
        return {"error": str(e)}