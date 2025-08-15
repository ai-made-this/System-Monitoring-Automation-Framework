#!/usr/bin/env python3
"""
Main System Aggregator
Runs monitoring across all categories (CPU, GPU, Memory, Network)
"""

import json
import importlib
from pathlib import Path

MODES_DIR = Path(__file__).parent / "modes"

def run_system_mode(mode="basic", categories=None):
    """
    Run monitoring across specified categories
    
    Args:
        mode: Mode to run (basic, detailed, all)
        categories: List of categories to monitor (default: all available)
    """
    if categories is None:
        categories = [d.name for d in MODES_DIR.iterdir() 
                     if d.is_dir() and (d / "aggregator.py").exists()]
    
    results = {}
    
    for category in categories:
        try:
            # Import the category's aggregator
            mod = importlib.import_module(f"modes.{category}.aggregator")
            results[category] = mod.run_mode(mode)
        except Exception as e:
            results[category] = {"error": str(e)}
    
    return results

def list_categories():
    """List all available monitoring categories"""
    return [d.name for d in MODES_DIR.iterdir() 
            if d.is_dir() and (d / "aggregator.py").exists()]

def get_category_modes(category):
    """Get available modes for a specific category"""
    try:
        mod = importlib.import_module(f"modes.{category}.aggregator")
        return mod.list_modes()
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "list":
            print("Available categories:", list_categories())
        elif sys.argv[1] == "modes":
            cat = sys.argv[2] if len(sys.argv) > 2 else "cpu"
            print(f"Modes for {cat}:", get_category_modes(cat))
        else:
            mode = sys.argv[1]
            categories = sys.argv[2:] if len(sys.argv) > 2 else None
            print(json.dumps(run_system_mode(mode, categories), indent=2))
    else:
        print(json.dumps(run_system_mode(), indent=2))