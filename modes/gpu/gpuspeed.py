"""GPU Speed Monitor - Returns GPU clock speed"""
try:
    import GPUtil
    GPU_AVAILABLE = True
except ImportError:
    GPU_AVAILABLE = False

def get_gpu_speed():
    """Get GPU clock speed"""
    if not GPU_AVAILABLE:
        return {"error": "GPUtil not installed. Run: pip install GPUtil"}
    
    try:
        gpus = GPUtil.getGPUs()
        if not gpus:
            return {"error": "No GPUs detected"}
        
        gpu_data = []
        for gpu in gpus:
            gpu_data.append({
                "name": gpu.name,
                "memory_total": gpu.memoryTotal,
                "memory_used": gpu.memoryUsed,
                "memory_free": gpu.memoryFree
            })
        return {"gpus": gpu_data}
    except Exception as e:
        return {"error": str(e)}