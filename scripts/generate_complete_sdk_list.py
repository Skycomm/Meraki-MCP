#!/usr/bin/env python3
"""
Generate complete list of all official Meraki SDK methods by category.
This will help us identify exactly what methods we need to add.
"""

import meraki
import json

def get_all_sdk_methods():
    """Get all SDK methods organized by category."""
    
    # Create dashboard API instance
    dashboard = meraki.DashboardAPI('test', suppress_logging=True)
    
    all_methods = {}
    total_count = 0
    
    print("🔍 Scanning Official Meraki SDK...")
    print("=" * 50)
    
    # Get all categories
    for attr in sorted(dir(dashboard)):
        if not attr.startswith('_'):
            obj = getattr(dashboard, attr)
            if hasattr(obj, '__class__') and 'meraki' in str(obj.__class__):
                # Get all methods in this category
                methods = []
                for method in sorted(dir(obj)):
                    if not method.startswith('_') and callable(getattr(obj, method)):
                        methods.append(method)
                
                if methods:  # Only include categories that have methods
                    all_methods[attr] = {
                        'count': len(methods),
                        'methods': methods
                    }
                    total_count += len(methods)
                    print(f"📁 {attr}: {len(methods)} methods")
    
    print("=" * 50)
    print(f"📊 TOTAL: {total_count} methods across {len(all_methods)} categories")
    
    # Save to file for reference
    with open('official_sdk_methods.json', 'w') as f:
        json.dump(all_methods, f, indent=2)
    
    return all_methods, total_count

if __name__ == "__main__":
    methods, total = get_all_sdk_methods()
    print(f"\n💾 Complete method list saved to: official_sdk_methods.json")
    print(f"✅ Total methods to implement: {total}")