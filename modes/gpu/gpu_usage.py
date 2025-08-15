"""GPU Usage Monitor - Returns GPU usage percentage"""
try:
    import GPUtil
    GPU_AVAILABLE = True
except ImportError:
    GPU_AVAILABLE = False

def get_gpu_usage():
    """Get GPU usage percentage"""
    if not GPU_AVAILABLE:
        return {"error": "GPUtil not installed. Run: pip install GPUtil"}

    try:
        gpus = GPUtil.getGPUs()
        if not gpus:
            return {"error": "No GPUs detected"}

        gpu_usage = []
        for gpu in gpus:
            gpu_usage.append({
                "name": gpu.name,
                "load_percent": round(gpu.load * 100, 2),
                "memory_util_percent": round((gpu.memoryUsed / gpu.memoryTotal) * 100, 2) if gpu.memoryTotal > 0 else 0
            })
        return {"gpu_usage": gpu_usage}
    except Exception as e:
        return {"error": str(e)}
