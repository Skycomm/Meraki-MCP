#!/usr/bin/env python3
"""
Generate complete tools_SDK_organizations.py with all 173 official methods.
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

def generate_tool_function(method_name, category="organizations"):
    """Generate a complete tool function for a given SDK method."""
    
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
    elif method_name.startswith('claim'):
        verb = "Claim"
        desc_verb = "Claim"
    elif method_name.startswith('assign'):
        verb = "Assign"
        desc_verb = "Assign"
    elif method_name.startswith('bulk'):
        verb = "Bulk"
        desc_verb = "Perform bulk operation on"
    elif method_name.startswith('combine'):
        verb = "Combine"
        desc_verb = "Combine"
    elif method_name.startswith('clone'):
        verb = "Clone"
        desc_verb = "Clone"
    else:
        verb = "Manage"
        desc_verb = "Manage"
    
    # Extract object type from method name
    object_type = method_name.replace('Organization', '').replace('get', '').replace('create', '').replace('update', '').replace('delete', '').replace('bulk', '').replace('claim', '').replace('assign', '').replace('combine', '').replace('clone', '')
    if not object_type:
        object_type = "organization resource"
    
    description = f"{desc_verb} {object_type.lower()}"
    
    # Common parameters based on method patterns
    params = []
    param_docs = []
    sdk_params = []
    
    # Always need organization_id for org methods
    params.append("organization_id: str")
    param_docs.append("        organization_id: Organization ID")
    sdk_params.append("organization_id")
    
    # Add common parameters based on method name patterns
    if 'Network' in method_name or 'network' in method_name.lower():
        params.append("network_id: str = None")
        param_docs.append("        network_id: Network ID (optional)")
        sdk_params.append("networkId=network_id")
        
    if 'Device' in method_name or 'device' in method_name.lower():
        params.append("serial: str = None")
        param_docs.append("        serial: Device serial number (optional)")
        sdk_params.append("serial=serial")
        
    if 'Admin' in method_name:
        params.append("admin_id: str = None")
        param_docs.append("        admin_id: Admin ID (optional)")
        sdk_params.append("adminId=admin_id")
        
    if method_name.startswith('create') or method_name.startswith('update'):
        params.append("**kwargs")
        param_docs.append("        **kwargs: Additional parameters for the operation")
        
    if method_name.startswith('get') and 'History' in method_name:
        params.append("timespan: int = 86400")
        param_docs.append("        timespan: Timespan in seconds (default: 86400)")
        sdk_params.append("timespan=timespan")
        
    params_str = ", ".join(params)
    param_docs_str = "\n".join(param_docs)
    sdk_params_str = ", ".join(sdk_params)
    
    # Handle different SDK call patterns
    if sdk_params:
        sdk_call = f"result = meraki_client.dashboard.{category}.{method_name}({sdk_params_str})"
    else:
        sdk_call = f"result = meraki_client.dashboard.{category}.{method_name}(organization_id)"
        
    # Add kwargs handling for create/update methods
    if method_name.startswith('create') or method_name.startswith('update'):
        sdk_call = f"result = meraki_client.dashboard.{category}.{method_name}(organization_id, **kwargs)"
    
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

def generate_organizations_sdk():
    """Generate complete organizations SDK file."""
    
    # Load the SDK methods
    with open('official_sdk_methods.json', 'r') as f:
        sdk_methods = json.load(f)
    
    organizations_methods = sdk_methods['organizations']['methods']
    
    print(f"🏢 Generating organizations SDK with {len(organizations_methods)} methods...")
    
    # Generate file header
    header = '''"""
Cisco Meraki MCP Server - Organizations SDK Tools
Complete implementation of all 173 official Meraki Organizations API methods.

This module provides 100% coverage of the Organizations category from the official Meraki Dashboard API SDK.
Each tool corresponds directly to a method in the meraki.dashboard.organizations namespace.
"""

from server.main import app, meraki_client
import meraki


def register_organizations_tools():
    """Register all organizations SDK tools."""
    print(f"📊 Registering {len(organizations_methods)} organizations SDK tools...")


'''
    
    # Generate all tool functions
    all_functions = []
    for method in organizations_methods:
        func_code = generate_tool_function(method, "organizations")
        all_functions.append(func_code)
    
    # Combine everything
    complete_file = header + "\n\n".join(all_functions)
    
    # Write the file
    with open('server/tools_SDK_organizations.py', 'w') as f:
        f.write(complete_file)
    
    print(f"✅ Generated server/tools_SDK_organizations.py with {len(organizations_methods)} methods")
    print(f"📁 File size: {len(complete_file):,} characters")

if __name__ == "__main__":
    generate_organizations_sdk()