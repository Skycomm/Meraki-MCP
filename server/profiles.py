#!/usr/bin/env python3
"""
MCP Server Profile Configuration

Defines different tool profiles to work around Claude Desktop's ~850 tool limit.
Each profile loads a specific subset of tools for focused functionality.
"""

# Profile definitions based on SDK categories
PROFILES = {
    'FULL': {
        'name': 'Full Server (All Tools)',
        'description': 'Complete Meraki API coverage - all SDK categories + custom tools',
        'modules': 'all',  # Special keyword to load everything
        'tool_count': 800
    },
    
    'WIRELESS': {
        'name': 'Wireless Specialist',
        'description': 'Wireless network management and optimization',
        'modules': [
            'resources',
            'wireless',  # Consolidated wireless module
            'custom_helpers',
            'custom_search'
        ],
        'tool_count': 160
    },
    
    'NETWORK': {
        'name': 'Network Infrastructure', 
        'description': 'Switch, appliance, and network infrastructure',
        'modules': [
            'resources',
            'networks',
            'networks_complete',
            'switch',
            'appliance',  # Consolidated appliance module
            'cellularGateway',
            'custom_vpn',
            'custom_helpers',
            'custom_search'
        ],
        'tool_count': 350
    },
    
    'ORGANIZATIONS': {
        'name': 'Organization Management',
        'description': 'Organization-level administration and policies',
        'modules': [
            'resources',
            'organizations',  # Consolidated organizations module
            'administered',
            'licensing',
            'custom_helpers',
            'custom_search'
        ],
        'tool_count': 140
    },
    
    'MONITORING': {
        'name': 'Device Monitoring',
        'description': 'Device management, cameras, and sensors',
        'modules': [
            'resources', 
            'devices',
            'camera',
            'sensor',
            'sm',
            'insight',
            'custom_monitoring',
            'custom_analytics',
            'custom_live',
            'custom_helpers',
            'custom_search'
        ],
        'tool_count': 200
    },
    
    'SDK_CORE': {
        'name': 'SDK Core Categories',
        'description': 'Pure SDK categories - matches official Meraki SDK exactly',
        'modules': [
            'resources',
            # Official SDK categories only
            'administered',
            'appliance', 
            'batch',
            'camera',
            'cellularGateway',
            'devices',
            'insight',
            'licensing',
            'networks',
            'organizations',
            'sensor',
            'sm',
            'switch',
            'wireless'
        ],
        'tool_count': 600
    },
    
    'MINIMAL': {
        'name': 'Essential Only',
        'description': 'Basic read-only operations',
        'modules': [
            'resources',
            'organizations',
            'networks', 
            'devices',
            'custom_helpers'
        ],
        'tool_count': 80
    }
}

# Module groups for custom configurations
MODULE_GROUPS = {
    'sdk_core': [
        'resources',
        'administered',
        'appliance',
        'batch', 
        'camera',
        'cellularGateway',
        'devices',
        'insight',
        'licensing',
        'networks',
        'organizations',
        'sensor',
        'sm',
        'switch',
        'wireless'
    ],
    'custom_tools': [
        'custom_helpers',
        'custom_search',
        'custom_alerts',
        'custom_analytics',
        'custom_live',
        'custom_monitoring',
        'custom_monitoring_dashboard',
        'custom_policy',
        'custom_vpn',
        'custom_event_analysis',
        'custom_beta'
    ],
    'network_stack': [
        'networks',
        'networks_complete',
        'switch',
        'appliance',
        'cellularGateway',
        'custom_vpn'
    ],
    'device_management': [
        'devices',
        'camera',
        'sensor',
        'sm',
        'insight',
        'custom_monitoring',
        'custom_live'
    ],
    'admin_tools': [
        'organizations',
        'administered',
        'licensing',
        'batch',
        'custom_policy'
    ]
}

def get_profile_modules(profile_name):
    """
    Get the list of modules to load for a given profile.
    
    Args:
        profile_name: Name of the profile (e.g., 'WIRELESS', 'FULL')
    
    Returns:
        List of module names to load, or 'all' for full server
    """
    profile = PROFILES.get(profile_name.upper(), PROFILES['FULL'])
    return profile['modules']

def get_modules_from_env(env_modules):
    """
    Parse MCP_MODULES environment variable into module list.
    
    Args:
        env_modules: Comma-separated list of modules or groups
    
    Returns:
        List of module names to load
    """
    if not env_modules:
        return []
    
    modules = []
    for item in env_modules.split(','):
        item = item.strip()
        # Check if it's a module group
        if item in MODULE_GROUPS:
            modules.extend(MODULE_GROUPS[item])
        else:
            # It's a single module
            modules.append(item)
    
    # Remove duplicates while preserving order
    seen = set()
    unique_modules = []
    for m in modules:
        if m not in seen:
            seen.add(m)
            unique_modules.append(m)
    
    return unique_modules

def should_load_module(module_name, profile_name, custom_modules=None, excluded_modules=None):
    """
    Determine if a module should be loaded based on profile and environment.
    
    Args:
        module_name: Name of the module (without 'tools_' prefix)
        profile_name: Active profile name
        custom_modules: List of custom modules from MCP_MODULES env var
        excluded_modules: List of modules to exclude from MCP_EXCLUDE env var
    
    Returns:
        Boolean indicating if module should be loaded
    """
    # Check exclusions first
    if excluded_modules and module_name in excluded_modules:
        return False
    
    # If custom modules specified, use those
    if custom_modules:
        return module_name in custom_modules
    
    # Otherwise use profile
    profile_modules = get_profile_modules(profile_name)
    
    # 'all' means load everything
    if profile_modules == 'all':
        return True
    
    return module_name in profile_modules

def print_profile_info(profile_name):
    """
    Print information about the active profile.
    
    Args:
        profile_name: Name of the active profile
    """
    profile = PROFILES.get(profile_name.upper(), PROFILES['FULL'])
    print(f"🚀 MCP Server Profile: {profile['name']}")
    print(f"   {profile['description']}")
    print(f"   Tool Count: ~{profile['tool_count']} tools")
    print()