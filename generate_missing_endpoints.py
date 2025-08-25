#!/usr/bin/env python3
"""
Automatic generator for missing Meraki API endpoints.
This will create implementations for all missing endpoints to achieve 100% coverage.
"""

import meraki
import re
import os
from typing import Dict, List, Set

def camel_to_snake(name):
    """Convert camelCase to snake_case."""
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def generate_function_implementation(category: str, method_name: str) -> str:
    """Generate a function implementation for a missing endpoint."""
    
    # Determine operation type
    if method_name.startswith('get'):
        operation = 'get'
        emoji = '📊'
        verb = 'Get'
    elif method_name.startswith('create'):
        operation = 'create'
        emoji = '➕'
        verb = 'Create'
    elif method_name.startswith('update'):
        operation = 'update'
        emoji = '✏️'
        verb = 'Update'
    elif method_name.startswith('delete'):
        operation = 'delete'
        emoji = '🗑️'
        verb = 'Delete'
    elif 'claim' in method_name.lower():
        operation = 'claim'
        emoji = '📥'
        verb = 'Claim'
    elif 'release' in method_name.lower():
        operation = 'release'
        emoji = '📤'
        verb = 'Release'
    else:
        operation = 'action'
        emoji = '⚡'
        verb = 'Execute'
    
    # Extract resource name
    resource = method_name.replace('get', '').replace('create', '').replace('update', '').replace('delete', '')
    resource_readable = ' '.join(re.findall('[A-Z][^A-Z]*', resource))
    
    # Generate function name
    func_name = camel_to_snake(method_name)
    
    # Determine parameters based on method name
    params = []
    if 'Organization' in method_name:
        params.append('organization_id: str')
    elif 'Network' in method_name:
        params.append('network_id: str')
    elif 'Device' in method_name:
        params.append('serial: str')
    
    if operation in ['create', 'update']:
        params.append('**kwargs')
    elif operation == 'delete' and 'Id' in resource:
        # Extract ID parameter name
        id_match = re.search(r'([A-Z][a-z]+)(?:Id|ID)', resource)
        if id_match:
            id_name = camel_to_snake(id_match.group(1)) + '_id'
            params.append(f'{id_name}: str')
    
    params_str = ', '.join(params) if params else ''
    
    # Generate the function
    func_code = f'''
    @app.tool(
        name="{func_name}",
        description="{emoji} {verb} {resource_readable.lower()}"
    )
    def {func_name}({params_str}):
        """{verb} {resource_readable.lower()}."""
        try:
            result = meraki_client.dashboard.{category}.{method_name}(
                {', '.join([p.split(':')[0] for p in params])}
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "{resource_readable}")
            elif isinstance(result, list):
                return format_list_response(result, "{resource_readable}")
            else:
                return f"✅ {verb} {resource_readable.lower()} completed successfully!"
                
        except Exception as e:
            return f"Error: {{str(e)}}"
'''
    
    return func_code

def scan_implemented_methods() -> Set[str]:
    """Scan our codebase for already implemented methods."""
    implemented = set()
    
    for file in os.listdir('server'):
        if file.startswith('tools_') and file.endswith('.py'):
            with open(f'server/{file}', 'r') as f:
                content = f.read()
                # Find function definitions
                functions = re.findall(r'def\s+(\w+)\s*\(', content)
                implemented.update(functions)
                # Find meraki_client calls
                api_calls = re.findall(r'meraki_client\.dashboard\.(\w+)\.(\w+)', content)
                for cat, method in api_calls:
                    implemented.add(method)
    
    return implemented

def find_missing_endpoints() -> Dict[str, List[str]]:
    """Find all missing endpoints from the Meraki SDK."""
    dashboard = meraki.DashboardAPI('dummy_key', suppress_logging=True)
    implemented = scan_implemented_methods()
    
    missing_by_category = {}
    
    for category in dir(dashboard):
        if not category.startswith('_'):
            try:
                cat_obj = getattr(dashboard, category)
                methods = [m for m in dir(cat_obj) if not m.startswith('_')]
                
                missing = []
                for method in methods:
                    snake_case = camel_to_snake(method)
                    if method not in implemented and snake_case not in implemented:
                        missing.append(method)
                
                if missing:
                    missing_by_category[category] = missing
            except:
                pass
    
    return missing_by_category

def generate_module_for_category(category: str, methods: List[str], existing_file: str = None) -> str:
    """Generate or update a module for a category."""
    
    module_content = f'''"""
Additional {category.title()} endpoints for Cisco Meraki MCP Server.
Auto-generated to achieve 100% API coverage.
"""

# Global variables to store app and meraki client
app = None
meraki_client = None

def format_dict_response(data: dict, resource_name: str) -> str:
    """Format dictionary response."""
    result = f"# {{resource_name}}\\n\\n"
    for key, value in data.items():
        if value is not None:
            result += f"**{{key}}**: {{value}}\\n"
    return result

def format_list_response(data: list, resource_name: str) -> str:
    """Format list response."""
    if not data:
        return f"No {{resource_name.lower()}} found."
    
    result = f"# {{resource_name}}\\n\\n"
    result += f"**Total**: {{len(data)}}\\n\\n"
    
    for idx, item in enumerate(data[:10], 1):
        if isinstance(item, dict):
            name = item.get('name', item.get('id', f'Item {{idx}}'))
            result += f"## {{name}}\\n"
            for key, value in item.items():
                if value is not None and key not in ['name']:
                    result += f"- **{{key}}**: {{value}}\\n"
            result += "\\n"
        else:
            result += f"- {{item}}\\n"
    
    if len(data) > 10:
        result += f"\\n... and {{len(data) - 10}} more items"
    
    return result

def register_{category}_additional_tools(mcp_app, meraki):
    """Register additional {category} tools with the MCP server."""
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    
    # Register all additional tools
    register_{category}_additional_handlers()

def register_{category}_additional_handlers():
    """Register additional {category} tool handlers."""
'''
    
    # Add all missing methods
    for method in methods:
        module_content += generate_function_implementation(category, method)
    
    return module_content

def main():
    """Generate implementations for all missing endpoints."""
    missing = find_missing_endpoints()
    
    total_missing = sum(len(methods) for methods in missing.values())
    print(f"Found {total_missing} missing endpoints across {len(missing)} categories")
    
    # Priority categories to implement
    priority_categories = ['organizations', 'networks', 'devices', 'wireless', 'switch', 'appliance']
    
    files_created = []
    
    for category in priority_categories:
        if category in missing:
            methods = missing[category]
            print(f"\nGenerating {len(methods)} methods for {category}...")
            
            # Generate module
            module_name = f"tools_{category}_additional"
            module_path = f"server/{module_name}.py"
            
            content = generate_module_for_category(category, methods)
            
            with open(module_path, 'w') as f:
                f.write(content)
            
            files_created.append(module_name)
            print(f"Created {module_path} with {len(methods)} endpoints")
    
    # Generate registration code for main.py
    print("\n\nAdd these imports to main.py:")
    for module in files_created:
        print(f"from server.{module} import register_{module.replace('tools_', '').replace('_additional', '')}_additional_tools")
    
    print("\n\nAdd these registrations to main.py:")
    for module in files_created:
        print(f"register_{module.replace('tools_', '').replace('_additional', '')}_additional_tools(app, meraki)")
    
    print(f"\n\nTotal endpoints added: {sum(len(missing[cat]) for cat in priority_categories if cat in missing)}")
    print("Run this script again to generate remaining categories.")

if __name__ == "__main__":
    main()