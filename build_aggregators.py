#!/usr/bin/env python3
"""
Auto-Aggregator Generator
Scans modes/<category>/ folders, detects .py mini-modules, and creates:
- aggregator.py per category
- config.json per category (with default 'all' mode)
"""

import os
import json
import importlib
import sys
from pathlib import Path


BASE_DIR = Path(__file__).parent / "modes"

def build_aggregator(category):
    category_path = BASE_DIR / category
    if not category_path.exists():
        print(f"Skipping {category} - no folder found.", file=sys.stderr)
        return
    
    # Use os.listdir to count .py files for reporting
    py_files = [f for f in os.listdir(category_path) if f.endswith('.py') and f not in ('__init__.py', 'aggregator.py')]
    modules = [Path(f).stem for f in py_files]
    print(f"Found {len(modules)} Python modules in {category}: {', '.join(modules)}")
    
    if not modules:
        print(f"No modules found in {category}", file=sys.stderr)
        return
    
    # Generate default config
    config_path = category_path / "config.json"
    if not config_path.exists():
        config_data = {
            "all": modules,
            "basic": modules[:2] if len(modules) > 2 else modules,
            "detailed": modules
        }
        with open(config_path, "w") as f:
            json.dump(config_data, f, indent=2)
        print(f"Created config.json for {category}")
    
    # Use importlib to check if each module can be imported (report errors)
    import_errors = []
    for mod_name in modules:
        try:
            importlib.import_module(f"modes.{category}.{mod_name}")
        except Exception as e:
            import_errors.append((mod_name, str(e)))
    if import_errors:
        print(f"Import errors in {category}: {import_errors}", file=sys.stderr)
    
    # Create aggregator.py
    aggregator_code = f'''"""
Auto-generated aggregator for {category} modules
"""
import importlib
import json
from pathlib import Path

CONFIG_FILE = Path(__file__).parent / "config.json"

with open(CONFIG_FILE) as f:
    MODES = json.load(f)

def run_mode(mode_name="all"):
    """Run specified mode for {category} monitoring"""
    if mode_name not in MODES:
        raise ValueError(f"Unknown mode: {{mode_name}}. Available: {{list(MODES.keys())}}")
    results = {{}}
    for module_name in MODES[mode_name]:
        try:
            mod = importlib.import_module(f".{{module_name}}", __package__)
            all_funcs = [f for f in dir(mod) if not f.startswith("_") and callable(getattr(mod, f))]
            excluded = {{'Path', 'datetime', 'os', 'sys', 'json', 'time', 'subprocess', 'platform', 'shutil'}}
            funcs = [f for f in all_funcs if f.startswith('get_') and f not in excluded]
            if not funcs:
                funcs = [f for f in all_funcs if f not in excluded and not f[0].isupper()]
            if funcs:
                func = getattr(mod, funcs[0])
                result = func()
                if result is None:
                    results[module_name] = {{"error": "Module returned None"}}
                else:
                    results[module_name] = result
        except Exception as e:
            results[module_name] = {{"error": f"Exception: {{e}}"}}
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
'''
    
    with open(category_path / "aggregator.py", "w") as f:
        f.write(aggregator_code)
    print(f"Built aggregator.py for {category}")

def main():
    """Build aggregators for all category folders"""
    if not BASE_DIR.exists():
        BASE_DIR.mkdir(parents=True)
        print(f"Created {BASE_DIR}", file=sys.stderr)

    categories = [d.name for d in BASE_DIR.iterdir() if d.is_dir()]

    if not categories:
        print("No category folders found. Creating example structure...", file=sys.stderr)
        return

    for cat in categories:
        build_aggregator(cat)

    print(f"\nProcessed {len(categories)} categories: {', '.join(categories)}")

    # Auto-update structure file
    try:
        print("\n🔄 Auto-updating Current_Structure.txt...")
        sys.path.append('scripts')
        try:
            from scripts.update_structure import update_structure_file
        except ImportError:
            print("💡 Run 'python scripts/update_structure.py' to update structure file", file=sys.stderr)
            return
        if update_structure_file():
            print("✅ Structure file updated automatically")
        else:
            print("⚠️  Structure file update failed", file=sys.stderr)
    except Exception as e:
        print(f"⚠️  Structure update error: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
