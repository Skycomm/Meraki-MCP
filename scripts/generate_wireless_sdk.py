#!/usr/bin/env python3
"""
Generate complete tools_SDK_wireless.py with all 116 official methods.
"""

import json
import re

def camel_to_snake_case(camel_str):
    """Convert camelCase to snake_case for tool names."""
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', camel_str)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def generate_wireless_tool_function(method_name, category="wireless"):
    """Generate a complete tool function for a given wireless SDK method."""
    
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
    elif method_name.startswith('set'):
        verb = "Set"
        desc_verb = "Set"
    elif method_name.startswith('recalculate'):
        verb = "Recalculate"
        desc_verb = "Recalculate"
    else:
        verb = "Manage"
        desc_verb = "Manage"
    
    # Extract object type from method name - wireless specific parsing
    object_type = method_name.replace('Network', '').replace('Device', '').replace('Organization', '')
    object_type = object_type.replace('Wireless', '').replace('get', '').replace('create', '').replace('update', '').replace('delete', '').replace('bulk', '').replace('set', '').replace('recalculate', '')
    if not object_type:
        object_type = "wireless resource"
    
    description = f"{desc_verb} {object_type.lower()}"
    
    # Common parameters based on method patterns
    params = []
    param_docs = []
    sdk_params = []
    
    # Determine primary parameter based on method scope
    if method_name.startswith('getDevice') or method_name.startswith('updateDevice'):
        params.append("serial: str")
        param_docs.append("        serial: Device serial number")
        sdk_params.append("serial")
    elif method_name.startswith('getNetwork') or method_name.startswith('updateNetwork') or method_name.startswith('createNetwork') or method_name.startswith('deleteNetwork') or method_name.startswith('setNetwork'):
        params.append("network_id: str")
        param_docs.append("        network_id: Network ID")
        sdk_params.append("network_id")
    elif method_name.startswith('getOrganization') or method_name.startswith('updateOrganization') or method_name.startswith('createOrganization') or method_name.startswith('deleteOrganization') or method_name.startswith('bulk') or method_name.startswith('recalculate'):
        params.append("organization_id: str")
        param_docs.append("        organization_id: Organization ID")
        sdk_params.append("organization_id")
    
    # Add specific wireless parameters based on method patterns
    if 'Ssid' in method_name and not method_name.endswith('Ssids'):
        params.append("ssid_number: str")
        param_docs.append("        ssid_number: SSID number")
        sdk_params.append("ssid_number")
        
    if 'RfProfile' in method_name and not method_name.endswith('RfProfiles'):
        params.append("rf_profile_id: str")
        param_docs.append("        rf_profile_id: RF profile ID")
        sdk_params.append("rf_profile_id")
        
    if 'EthernetPort' in method_name and 'Ports' not in method_name:
        params.append("ethernet_port_id: str")
        param_docs.append("        ethernet_port_id: Ethernet port ID")
        sdk_params.append("ethernet_port_id")
        
    if 'Profile' in method_name and 'RfProfile' not in method_name and not method_name.endswith('Profiles'):
        params.append("profile_id: str")
        param_docs.append("        profile_id: Profile ID")
        sdk_params.append("profile_id")
        
    if method_name.startswith('create') or method_name.startswith('update') or method_name.startswith('set'):
        params.append("**kwargs")
        param_docs.append("        **kwargs: Additional parameters for the operation")
        
    # Add common optional parameters for analytics/history methods
    if 'History' in method_name or 'Usage' in method_name or 'Quality' in method_name or 'Utilization' in method_name:
        params.append("timespan: int = 86400")
        param_docs.append("        timespan: Timespan in seconds (default: 86400)")
        sdk_params.append("timespan=timespan")
        
        # Many wireless analytics methods need device_serial OR client_id
        if 'device' not in method_name.lower() and method_name.startswith('getNetwork'):
            params.append("device_serial: str = None")
            params.append("client_id: str = None")
            param_docs.append("        device_serial: Device serial number (optional)")
            param_docs.append("        client_id: Client ID (optional)")
            sdk_params.append("deviceSerial=device_serial")
            sdk_params.append("clientId=client_id")
    
    params_str = ", ".join(params)
    param_docs_str = "\n".join(param_docs)
    
    # Build SDK parameters string
    if method_name.startswith('create') or method_name.startswith('update') or method_name.startswith('set'):
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

def generate_wireless_sdk():
    """Generate complete wireless SDK file."""
    
    # Load the SDK methods
    with open('official_sdk_methods.json', 'r') as f:
        sdk_methods = json.load(f)
    
    wireless_methods = sdk_methods['wireless']['methods']
    
    print(f"📶 Generating wireless SDK with {len(wireless_methods)} methods...")
    
    # Generate file header
    header = f'''"""
Cisco Meraki MCP Server - Wireless SDK Tools
Complete implementation of all {len(wireless_methods)} official Meraki Wireless API methods.

This module provides 100% coverage of the Wireless category from the official Meraki Dashboard API SDK.
Each tool corresponds directly to a method in the meraki.dashboard.wireless namespace.
"""

from server.main import app, meraki_client
import meraki


def register_wireless_tools():
    """Register all wireless SDK tools."""
    print(f"📶 Registering {len(wireless_methods)} wireless SDK tools...")


'''
    
    # Generate all tool functions
    all_functions = []
    for method in wireless_methods:
        func_code = generate_wireless_tool_function(method, "wireless")
        all_functions.append(func_code)
    
    # Combine everything
    complete_file = header + "\n\n".join(all_functions)
    
    # Write the file
    with open('server/tools_SDK_wireless.py', 'w') as f:
        f.write(complete_file)
    
    print(f"✅ Generated server/tools_SDK_wireless.py with {len(wireless_methods)} methods")
    print(f"📁 File size: {len(complete_file):,} characters")

if __name__ == "__main__":
    generate_wireless_sdk()