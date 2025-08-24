#!/usr/bin/env python3
"""
Minimal test to check if server starts
"""

import sys
import importlib.util

# Load the main module
spec = importlib.util.spec_from_file_location("main", "server/main.py")
main_module = importlib.util.module_from_spec(spec)
sys.modules["main"] = main_module

try:
    spec.loader.exec_module(main_module)
    app = main_module.app
    
    # Count tools
    tools_count = len(getattr(app, '_tools', {}))
    print(f"Total tools registered: {tools_count}")
    
    # Check for long names
    long_names = []
    for i, (name, tool) in enumerate(getattr(app, '_tools', {}).items()):
        if len(name) > 60:
            long_names.append((i, name, len(name)))
    
    if long_names:
        print("\nTools with names > 60 characters:")
        for idx, name, length in long_names:
            print(f"  Index {idx}: {name} ({length} chars)")
    
    # Try to find what's at index 277
    tools_list = list(getattr(app, '_tools', {}).items())
    if len(tools_list) > 277:
        name, tool = tools_list[277]
        print(f"\nTool at index 277: {name} ({len(name)} chars)")
        
except Exception as e:
    print(f"Error loading server: {e}")
    import traceback
    traceback.print_exc()