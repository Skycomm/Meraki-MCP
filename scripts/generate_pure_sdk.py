#!/usr/bin/env python3
"""
Generate pure SDK files with exact official method counts (no extras).
"""

import json
import re

def camel_to_snake_case(camel_str):
    """Convert camelCase to snake_case for tool names."""
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', camel_str)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def generate_generic_tool_function(method_name, category):
    """Generate a generic tool function for any SDK method."""
    
    tool_name = camel_to_snake_case(method_name)
    
    # Basic description based on method name
    if method_name.startswith('get'):
        desc_verb = "Retrieve"
    elif method_name.startswith('create'):
        desc_verb = "Create"
    elif method_name.startswith('update'):
        desc_verb = "Update"
    elif method_name.startswith('delete'):
        desc_verb = "Delete"
    elif method_name.startswith('bulk'):
        desc_verb = "Bulk operation on"
    else:
        desc_verb = "Manage"
    
    # Extract object type
    object_type = method_name
    for prefix in ['get', 'create', 'update', 'delete', 'bulk', 'Device', 'Network', 'Organization']:
        object_type = object_type.replace(prefix, '')
    
    if not object_type:
        object_type = f"{category} resource"
    
    description = f"{desc_verb} {object_type.lower()}"
    
    # Determine parameters based on method scope
    params = []
    param_docs = []
    sdk_params = []
    
    if method_name.startswith('getDevice') or method_name.startswith('updateDevice') or method_name.startswith('createDevice'):
        params.append("serial: str")
        param_docs.append("        serial: Device serial number")
        sdk_params.append("serial")
    elif method_name.startswith('getNetwork') or method_name.startswith('updateNetwork') or method_name.startswith('createNetwork') or method_name.startswith('deleteNetwork'):
        params.append("network_id: str")
        param_docs.append("        network_id: Network ID") 
        sdk_params.append("network_id")
    elif method_name.startswith('getOrganization') or method_name.startswith('updateOrganization') or method_name.startswith('createOrganization') or method_name.startswith('deleteOrganization') or method_name.startswith('bulk'):
        params.append("organization_id: str")
        param_docs.append("        organization_id: Organization ID")
        sdk_params.append("organization_id")
    
    # Add common patterns
    if method_name.startswith('create') or method_name.startswith('update'):
        params.append("**kwargs")
        param_docs.append("        **kwargs: Additional parameters for the operation")
        
    if 'History' in method_name:
        params.append("timespan: int = 86400")
        param_docs.append("        timespan: Timespan in seconds (default: 86400)")
        sdk_params.append("timespan=timespan")
    
    params_str = ", ".join(params)
    param_docs_str = "\n".join(param_docs)
    
    # Build SDK call
    if method_name.startswith('create') or method_name.startswith('update'):
        if sdk_params:
            sdk_params_str = ", ".join(sdk_params) + ", **kwargs"
        else:
            sdk_params_str = "**kwargs"
    else:
        sdk_params_str = ", ".join(sdk_params) if sdk_params else ""
    
    if sdk_params_str:
        sdk_call = f"result = meraki_client.dashboard.{category}.{method_name}({sdk_params_str})"
    else:
        sdk_call = f"result = meraki_client.dashboard.{category}.{method_name}()"
    
    function_code = f'''@app.tool(
    name="{tool_name}",
    description="{description}"
)
def {tool_name}({params_str}):
    """
    {description}
    
    Args:
{param_docs_str}
    
    Returns:
        dict: API response with {object_type.lower()} data
    """
    try:
        {sdk_call}
        return result
    except meraki.APIError as e:
        return {{"error": f"API Error: {{e}}"}}
    except Exception as e:
        return {{"error": f"Error: {{e}}"}}'''
    
    return function_code

def generate_pure_sdk_file(category, methods):
    """Generate a pure SDK file with exact official methods."""
    
    print(f"🔧 Generating pure {category} SDK with {len(methods)} methods...")
    
    # Category display names
    display_names = {
        'cellularGateway': '📡',
        'devices': '📱', 
        'networks': '🌐',
        'switch': '🔀'
    }
    
    icon = display_names.get(category, '🔧')
    
    # Generate file header
    header = f'''"""
Cisco Meraki MCP Server - {category.title()} SDK Tools
Complete implementation of all {len(methods)} official Meraki {category.title()} API methods.

This module provides 100% coverage of the {category.title()} category from the official Meraki Dashboard API SDK.
Each tool corresponds directly to a method in the meraki.dashboard.{category} namespace.

🎯 PURE SDK IMPLEMENTATION - No custom tools, exact match to official SDK
"""

from server.main import app, meraki_client
import meraki


def register_{category}_tools():
    """Register all {category} SDK tools."""
    print(f"{icon} Registering {len(methods)} {category} SDK tools...")


'''
    
    # Generate all tool functions
    all_functions = []
    for method in methods:
        func_code = generate_generic_tool_function(method, category)
        all_functions.append(func_code)
    
    # Combine everything
    complete_file = header + "\n\n".join(all_functions)
    
    # Write the file
    filename = f'server/tools_SDK_{category}.py'
    with open(filename, 'w') as f:
        f.write(complete_file)
    
    print(f"✅ Generated {filename} with {len(methods)} methods")
    return len(methods)

def generate_pure_sdks():
    """Generate pure SDK files that had custom tools removed."""
    
    # Load the SDK methods
    with open('official_sdk_methods.json', 'r') as f:
        sdk_methods = json.load(f)
    
    # Generate pure versions of files that had extras
    categories_to_fix = ['cellularGateway', 'devices', 'networks', 'switch']
    
    total_generated = 0
    
    for category in categories_to_fix:
        if category in sdk_methods:
            methods = sdk_methods[category]['methods']
            total_generated += generate_pure_sdk_file(category, methods)
    
    print(f"\n🎉 Generated {total_generated} pure SDK methods across {len(categories_to_fix)} categories")
    return total_generated

if __name__ == "__main__":
    total = generate_pure_sdks()
    print(f"\n✅ All pure SDK files generated with {total} methods")