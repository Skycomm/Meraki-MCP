#!/usr/bin/env python3
"""Find the exact missing API methods to reach 100% coverage."""

import meraki
import os
import re

# Get all available API methods from the SDK
dashboard = meraki.DashboardAPI('dummy_key', suppress_logging=True)

# Get all SDK methods
sdk_methods = {}
for category in dir(dashboard):
    if not category.startswith('_'):
        category_obj = getattr(dashboard, category)
        if hasattr(category_obj, '__dict__'):
            methods = [m for m in dir(category_obj) if not m.startswith('_') and callable(getattr(category_obj, m))]
            if methods:
                sdk_methods[category] = methods

# Get implemented methods
implemented_methods = set()

for file in os.listdir('server'):
    if file.startswith('tools_') and file.endswith('.py'):
        try:
            with open(f'server/{file}', 'r') as f:
                content = f.read()
                
                # Find all function names that call meraki_client.dashboard
                # Pattern 1: meraki_client.dashboard.category.methodName
                pattern1 = r'meraki_client\.dashboard\.(\w+)\.(\w+)\('
                matches1 = re.findall(pattern1, content)
                for cat, method in matches1:
                    implemented_methods.add(f"{cat}.{method}")
                
                # Pattern 2: meraki.dashboard.category.methodName (in case of different naming)
                pattern2 = r'meraki\.dashboard\.(\w+)\.(\w+)\('
                matches2 = re.findall(pattern2, content)
                for cat, method in matches2:
                    implemented_methods.add(f"{cat}.{method}")
                    
        except Exception as e:
            print(f"Error reading {file}: {e}")

# Find missing methods
missing_by_category = {}
total_missing = 0

print("=" * 60)
print("EXACT MISSING METHODS FOR 100% COVERAGE")
print("=" * 60)

for category, methods in sorted(sdk_methods.items()):
    missing_in_category = []
    for method in methods:
        full_method = f"{category}.{method}"
        if full_method not in implemented_methods:
            missing_in_category.append(method)
    
    if missing_in_category:
        missing_by_category[category] = missing_in_category
        total_missing += len(missing_in_category)

if missing_by_category:
    print(f"\n📊 Total Missing: {total_missing} methods\n")
    
    for category, methods in sorted(missing_by_category.items()):
        print(f"\n📁 {category} ({len(methods)} missing):")
        for method in sorted(methods):
            print(f"  - {method}")
else:
    print("\n✅ 100% COVERAGE ACHIEVED! No missing methods.")

# Generate implementation code for missing methods
if missing_by_category:
    print("\n" + "=" * 60)
    print("GENERATING IMPLEMENTATION CODE")
    print("=" * 60)
    
    for category, methods in missing_by_category.items():
        filename = f"server/tools_{category}_missing.py"
        
        print(f"\nGenerating {filename} with {len(methods)} methods...")
        
        code = f'''"""
Missing {category} API implementations for 100% coverage.
Auto-generated to reach complete API parity.
"""

# Global variables to store app and meraki client
app = None
meraki_client = None

def register_{category}_missing_tools(mcp_app, meraki):
    """
    Register missing {category} tools with the MCP server.
    
    Args:
        mcp_app: MCP server instance
        meraki: Meraki client instance
    """
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    
    # Register all missing {category} tools
    register_{category}_missing_handlers()

def register_{category}_missing_handlers():
    """Register missing {category} tool handlers."""
'''
        
        for method in sorted(methods):
            # Convert camelCase to snake_case for tool name
            tool_name = re.sub('([A-Z])', r'_\1', method).lower().strip('_')
            
            # Determine operation type for emoji
            if method.startswith('get') or method.startswith('list'):
                emoji = "📊"
                desc_prefix = "Get"
            elif method.startswith('create') or method.startswith('add'):
                emoji = "➕"
                desc_prefix = "Create"
            elif method.startswith('update') or method.startswith('set'):
                emoji = "✏️"
                desc_prefix = "Update"
            elif method.startswith('delete') or method.startswith('remove'):
                emoji = "🗑️"
                desc_prefix = "Delete"
            else:
                emoji = "⚡"
                desc_prefix = "Execute"
            
            # Generate function code
            code += f'''
    @app.tool(
        name="{tool_name}",
        description="{emoji} {desc_prefix} {tool_name.replace('_', ' ')}"
    )
    def {tool_name}(**kwargs):
        """Execute {method} API call."""
        try:
            result = meraki_client.dashboard.{category}.{method}(**kwargs)
            
            if result is None:
                return "✅ Operation completed successfully!"
            elif isinstance(result, dict):
                return f"✅ Result: {{result}}"
            elif isinstance(result, list):
                return f"✅ Found {{len(result)}} items"
            else:
                return f"✅ Result: {{result}}"
                
        except Exception as e:
            return f"Error calling {method}: {{str(e)}}"
'''
        
        # Write the file
        with open(filename, 'w') as f:
            f.write(code)
        
        print(f"✅ Created {filename}")

    # Update main.py imports
    print("\n" + "=" * 60)
    print("ADD THESE TO server/main.py:")
    print("=" * 60)
    
    print("\n# Add to imports section:")
    for category in missing_by_category.keys():
        print(f"from server.tools_{category}_missing import register_{category}_missing_tools")
    
    print("\n# Add to registration section:")
    for category in missing_by_category.keys():
        print(f"    register_{category}_missing_tools(app, meraki)")

print("\n" + "=" * 60)
print("DONE!")
print("=" * 60)