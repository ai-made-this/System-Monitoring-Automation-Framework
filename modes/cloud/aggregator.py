"""
Auto-generated aggregator for cloud modules
"""
import importlib
import json
from pathlib import Path

CONFIG_FILE = Path(__file__).parent / "config.json"

with open(CONFIG_FILE) as f:
    MODES = json.load(f)

def run_mode(mode_name="all"):
    """Run specified mode for cloud monitoring"""
    if mode_name not in MODES:
        raise ValueError(f"Unknown mode: {mode_name}. Available: {list(MODES.keys())}")
    
    results = {}
    for module_name in MODES[mode_name]:
        try:
            mod = importlib.import_module(f".{module_name}", __package__)
            # Find the main function (look for get_* functions first, then others)
            all_funcs = [f for f in dir(mod) if not f.startswith("_") and callable(getattr(mod, f))]
            # Prioritize get_* functions, exclude common imports
            excluded = {'Path', 'datetime', 'os', 'sys', 'json', 'time', 'subprocess', 'platform', 'shutil'}
            funcs = [f for f in all_funcs if f.startswith('get_') and f not in excluded]
            if not funcs:
                funcs = [f for f in all_funcs if f not in excluded and not f[0].isupper()]
            if funcs:
                func = getattr(mod, funcs[0])
                results[module_name] = func()
        except Exception as e:
            results[module_name] = f"Error: {e}"
    
    return results

def list_modes():
    """List available modes"""
    return list(MODES.keys())

def list_modules():
    """List available modules"""
    all_modules = set()
    for modules in MODES.values():
        all_modules.update(modules)
    return sorted(all_modules)

if __name__ == "__main__":
    import sys
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    print(json.dumps(run_mode(mode), indent=2))
