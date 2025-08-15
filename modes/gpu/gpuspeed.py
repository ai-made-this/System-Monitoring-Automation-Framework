"""GPU Speed Monitor - Returns GPU clock speeds"""
try:
    import GPUtil
    GPU_AVAILABLE = True
except ImportError:
    GPU_AVAILABLE = False

try:
    import pynvml
    PYNVML_AVAILABLE = True
except ImportError:
    PYNVML_AVAILABLE = False

def get_gpu_speed():
    """Get GPU clock speeds"""
    if not GPU_AVAILABLE:
        return {"error": "GPUtil not installed. Run: pip install GPUtil"}

    try:
        gpus = GPUtil.getGPUs()
        if not gpus:
            return {"error": "No GPUs detected"}

        gpu_speeds = []
        
        # Try to initialize pynvml for NVIDIA GPUs
        pynvml_initialized = False
        if PYNVML_AVAILABLE:
            try:
                pynvml.nvmlInit()
                pynvml_initialized = True
            except Exception:
                pass

        for i, gpu in enumerate(gpus):
            gpu_data = {
                "name": gpu.name,
                "memory_total_mb": gpu.memoryTotal,
                "memory_used_mb": gpu.memoryUsed,
                "memory_free_mb": gpu.memoryFree
            }
            
            # Try to get clock speeds using pynvml for NVIDIA GPUs
            if pynvml_initialized and "nvidia" in gpu.name.lower():
                try:
                    handle = pynvml.nvmlDeviceGetHandleByIndex(i)
                    
                    # Get current clock speeds
                    graphics_clock = pynvml.nvmlDeviceGetClockInfo(handle, pynvml.NVML_CLOCK_GRAPHICS)
                    memory_clock = pynvml.nvmlDeviceGetClockInfo(handle, pynvml.NVML_CLOCK_MEM)
                    
                    # Get max clock speeds
                    try:
                        max_graphics_clock = pynvml.nvmlDeviceGetMaxClockInfo(handle, pynvml.NVML_CLOCK_GRAPHICS)
                        max_memory_clock = pynvml.nvmlDeviceGetMaxClockInfo(handle, pynvml.NVML_CLOCK_MEM)
                    except Exception:
                        max_graphics_clock = None
                        max_memory_clock = None
                    
                    gpu_data.update({
                        "graphics_clock_mhz": graphics_clock,
                        "memory_clock_mhz": memory_clock,
                        "max_graphics_clock_mhz": max_graphics_clock,
                        "max_memory_clock_mhz": max_memory_clock,
                        "clock_info_available": True
                    })
                except Exception as e:
                    gpu_data.update({
                        "clock_info_available": False,
                        "clock_error": str(e)
                    })
            else:
                gpu_data.update({
                    "clock_info_available": False,
                    "note": "Real-time clock speeds require pynvml for NVIDIA GPUs. Run: pip install pynvml"
                })
            
            gpu_speeds.append(gpu_data)
        
        return {"gpu_speed": gpu_speeds}
    except Exception as e:
        return {"error": str(e)}
