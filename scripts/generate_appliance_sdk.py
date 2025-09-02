#!/usr/bin/env python3
"""
Generate complete tools_SDK_appliance.py with all 130 official methods.
"""

import json
import re

def snake_to_camel_case(snake_str):
    """Convert snake_case to camelCase for SDK parameters."""
    components = snake_str.split('_')
    return components[0] + ''.join(word.capitalize() for word in components[1:])

def camel_to_snake_case(camel_str):
    """Convert camelCase to snake_case for tool names."""
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', camel_str)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def generate_appliance_tool_function(method_name, category="appliance"):
    """Generate a complete tool function for a given appliance SDK method."""
    
    # Convert to snake_case for tool name
    tool_name = camel_to_snake_case(method_name)
    
    # Basic description based on method name
    if method_name.startswith('get'):
        verb = "Get"
        desc_verb = "Retrieve"
    elif method_name.startswith('create'):
        verb = "Create"
        desc_verb = "Create a new"
    elif method_name.startswith('update'):
        verb = "Update" 
        desc_verb = "Update an existing"
    elif method_name.startswith('delete'):
        verb = "Delete"
        desc_verb = "Delete an existing"
    elif method_name.startswith('bulk'):
        verb = "Bulk"
        desc_verb = "Perform bulk operation on"
    else:
        verb = "Manage"
        desc_verb = "Manage"
    
    # Extract object type from method name - appliance specific parsing
    object_type = method_name.replace('Network', '').replace('Device', '').replace('Organization', '')
    object_type = object_type.replace('Appliance', '').replace('get', '').replace('create', '').replace('update', '').replace('delete', '').replace('bulk', '')
    if not object_type:
        object_type = "appliance resource"
    
    description = f"{desc_verb} {object_type.lower()}"
    
    # Common parameters based on method patterns
    params = []
    param_docs = []
    sdk_params = []
    
    # Determine primary parameter based on method scope
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
    
    # Add specific parameters based on method patterns
    if 'Vlan' in method_name and not method_name.endswith('Vlans'):
        params.append("vlan_id: str")
        param_docs.append("        vlan_id: VLAN ID")
        sdk_params.append("vlan_id")
        
    if 'StaticRoute' in method_name and not method_name.endswith('StaticRoutes'):
        params.append("static_route_id: str")
        param_docs.append("        static_route_id: Static route ID")
        sdk_params.append("static_route_id")
        
    if 'RfProfile' in method_name and not method_name.endswith('RfProfiles'):
        params.append("rf_profile_id: str")
        param_docs.append("        rf_profile_id: RF profile ID")
        sdk_params.append("rf_profile_id")
        
    if 'TrafficShapingCustomPerformanceClass' in method_name and 'Classes' not in method_name:
        params.append("custom_performance_class_id: str")
        param_docs.append("        custom_performance_class_id: Custom performance class ID")
        sdk_params.append("custom_performance_class_id")
        
    if method_name.startswith('create') or method_name.startswith('update'):
        params.append("**kwargs")
        param_docs.append("        **kwargs: Additional parameters for the operation")
        
    if method_name.startswith('get') and ('History' in method_name or 'Performance' in method_name):
        params.append("timespan: int = 86400")
        param_docs.append("        timespan: Timespan in seconds (default: 86400)")
        sdk_params.append("timespan=timespan")
        
    params_str = ", ".join(params)
    param_docs_str = "\n".join(param_docs)
    
    # Build SDK parameters string
    if method_name.startswith('create') or method_name.startswith('update'):
        if len(sdk_params) > 0:
            sdk_params_str = ", ".join(sdk_params) + ", **kwargs"
        else:
            sdk_params_str = "**kwargs"
    else:
        sdk_params_str = ", ".join(sdk_params) if sdk_params else ""
    
    # Generate SDK call
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

def generate_appliance_sdk():
    """Generate complete appliance SDK file."""
    
    # Load the SDK methods
    with open('official_sdk_methods.json', 'r') as f:
        sdk_methods = json.load(f)
    
    appliance_methods = sdk_methods['appliance']['methods']
    
    print(f"🏠 Generating appliance SDK with {len(appliance_methods)} methods...")
    
    # Generate file header
    header = f'''"""
Cisco Meraki MCP Server - Appliance SDK Tools
Complete implementation of all {len(appliance_methods)} official Meraki Appliance API methods.

This module provides 100% coverage of the Appliance category from the official Meraki Dashboard API SDK.
Each tool corresponds directly to a method in the meraki.dashboard.appliance namespace.
"""

from server.main import app, meraki_client
import meraki


def register_appliance_tools():
    """Register all appliance SDK tools."""
    print(f"🏠 Registering {len(appliance_methods)} appliance SDK tools...")


'''
    
    # Generate all tool functions
    all_functions = []
    for method in appliance_methods:
        func_code = generate_appliance_tool_function(method, "appliance")
        all_functions.append(func_code)
    
    # Combine everything
    complete_file = header + "\n\n".join(all_functions)
    
    # Write the file
    with open('server/tools_SDK_appliance.py', 'w') as f:
        f.write(complete_file)
    
    print(f"✅ Generated server/tools_SDK_appliance.py with {len(appliance_methods)} methods")
    print(f"📁 File size: {len(complete_file):,} characters")

if __name__ == "__main__":
    generate_appliance_sdk()