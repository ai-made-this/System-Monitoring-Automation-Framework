"""GPU Memory Monitor - Returns GPU memory details"""
try:
    import GPUtil
    GPU_AVAILABLE = True
except ImportError:
    GPU_AVAILABLE = False

def get_gpu_memory():
    """Get GPU memory details in MiB"""
    if not GPU_AVAILABLE:
        return {"error": "GPUtil not installed. Run: pip install GPUtil"}

    try:
        gpus = GPUtil.getGPUs()
        if not gpus:
            return {"error": "No GPUs detected"}

        gpu_memory_data = []
        for gpu in gpus:
            gpu_memory_data.append({
                "name": gpu.name,
                "memory_total_mib": gpu.memoryTotal,
                "memory_used_mib": gpu.memoryUsed,
                "memory_free_mib": gpu.memoryFree
            })
        return {"gpu_memory": gpu_memory_data}
    except Exception as e:
        return {"error": str(e)}
