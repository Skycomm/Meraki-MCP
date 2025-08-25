#!/usr/bin/env python3
"""Check API coverage after removing custom tools."""

import meraki
import os
import re

# Get all available API methods from the SDK
dashboard = meraki.DashboardAPI('dummy_key', suppress_logging=True)

# Count SDK methods
sdk_methods = {}
for category in dir(dashboard):
    if not category.startswith('_'):
        category_obj = getattr(dashboard, category)
        if hasattr(category_obj, '__dict__'):
            methods = [m for m in dir(category_obj) if not m.startswith('_')]
            if methods:
                sdk_methods[category] = methods

total_sdk_methods = sum(len(methods) for methods in sdk_methods.values())

# Count implemented tools
implemented_tools = 0
modules_loaded = []

for file in os.listdir('server'):
    if file.startswith('tools_') and file.endswith('.py'):
        modules_loaded.append(file[:-3])
        try:
            with open(f'server/{file}', 'r') as f:
                content = f.read()
                # Count @app.tool decorators
                tool_count = len(re.findall(r'@app\.tool\(', content))
                implemented_tools += tool_count
        except:
            pass

print("=" * 60)
print("MERAKI API COVERAGE REPORT")
print("=" * 60)
print(f"\n📊 STATISTICS:")
print(f"  SDK API Methods Available: {total_sdk_methods}")
print(f"  Tool Functions Implemented: {implemented_tools}")
print(f"  Coverage Percentage: {(implemented_tools/total_sdk_methods*100):.1f}%")
print(f"  Modules Loaded: {len(modules_loaded)}")

print(f"\n📁 API CATEGORIES IN SDK ({len(sdk_methods)}):")
for category, methods in sorted(sdk_methods.items())[:10]:
    print(f"  - {category}: {len(methods)} methods")
print(f"  ... and {len(sdk_methods)-10} more categories")

print(f"\n✅ CURRENT MODULES ({len(modules_loaded)}):")
# Group by type
core_modules = [m for m in modules_loaded if not m.endswith('_additional')]
additional_modules = [m for m in modules_loaded if m.endswith('_additional')]

print(f"\nCore Modules ({len(core_modules)}):")
for module in sorted(core_modules)[:10]:
    print(f"  - {module}")
if len(core_modules) > 10:
    print(f"  ... and {len(core_modules)-10} more")

print(f"\nAdditional Coverage Modules ({len(additional_modules)}):")
for module in sorted(additional_modules)[:5]:
    print(f"  - {module}")
if len(additional_modules) > 5:
    print(f"  ... and {len(additional_modules)-5} more")

# Check for missing categories
module_categories = set()
for m in modules_loaded:
    # Extract category from module name
    category = m.replace('tools_', '').replace('_additional', '')
    module_categories.add(category)

sdk_categories = set(sdk_methods.keys())
missing_categories = sdk_categories - module_categories

if missing_categories:
    print(f"\n⚠️ POTENTIALLY MISSING CATEGORIES:")
    for cat in sorted(missing_categories)[:10]:
        print(f"  - {cat} ({len(sdk_methods.get(cat, []))} methods)")
else:
    print(f"\n✅ All SDK categories appear to be covered!")

print("\n" + "=" * 60)
print("SUMMARY: Official Meraki API implementation with custom tools removed")
print("=" * 60)