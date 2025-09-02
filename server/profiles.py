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
            'SDK_wireless',  # Consolidated wireless module
            'helpers',
            'search'
        ],
        'tool_count': 160
    },
    
    'NETWORK': {
        'name': 'Network Infrastructure', 
        'description': 'Switch, appliance, and network infrastructure',
        'modules': [
            'resources',
            'SDK_networks',        # 117 tools (100% coverage)
            'SDK_switch',          # ~130 tools (100% coverage)  
            'SDK_appliance',       # ~130 tools (consolidated)
            'SDK_cellularGateway', # ~50 tools
            'helpers',
            'search'
        ],
        'tool_count': 450
    },
    
    'ORGANIZATIONS': {
        'name': 'Organization Management',
        'description': 'Organization-level administration and policies',
        'modules': [
            'resources',
            'SDK_organizations',  # Consolidated organizations module
            'SDK_administered',
            'SDK_licensing',
            'helpers',
            'search'
        ],
        'tool_count': 140
    },
    
    'MONITORING': {
        'name': 'Device Monitoring',
        'description': 'Device management, cameras, and sensors',
        'modules': [
            'resources', 
            'SDK_devices',
            'SDK_camera',
            'SDK_sensor',
            'SDK_sm',
            'SDK_insight',
            'monitoring',
            'analytics',
            'live',
            'helpers',
            'search'
        ],
        'tool_count': 200
    },
    
    'SDK_CORE': {
        'name': 'Pure SDK Categories (816 methods)',
        'description': 'Pure SDK categories - matches official Meraki SDK exactly',
        'modules': [
            'resources',
            # Official SDK categories only (13 categories, 816 total methods)
            'SDK_administered',      # 4 methods
            'SDK_appliance',         # 130 methods 
            'SDK_camera',            # 45 methods
            'SDK_cellularGateway',   # 24 methods
            'SDK_devices',           # 27 methods
            'SDK_insight',           # 7 methods
            'SDK_licensing',         # 8 methods
            'SDK_networks',          # 114 methods
            'SDK_organizations',     # 173 methods
            'SDK_sensor',            # 18 methods
            'SDK_sm',                # 49 methods
            'SDK_switch',            # 101 methods
            'SDK_wireless'           # 116 methods
        ],
        'tool_count': 816
    },
    
    'MINIMAL': {
        'name': 'Essential Only',
        'description': 'Basic read-only operations',
        'modules': [
            'resources',
            'SDK_organizations',
            'SDK_networks', 
            'SDK_devices',
            'helpers'
        ],
        'tool_count': 80
    }
}

# Module groups for custom configurations
MODULE_GROUPS = {
    'sdk_core': [
        'resources',
        'SDK_administered',
        'SDK_appliance',
        'SDK_camera',
        'SDK_cellularGateway',
        'SDK_devices',
        'SDK_insight',
        'SDK_licensing',
        'SDK_networks',
        'SDK_organizations',
        'SDK_sensor',
        'SDK_sm',
        'SDK_switch',
        'SDK_wireless'
    ],
    'custom_tools': [
        'Custom_alerts',
        'Custom_analytics',
        'Custom_batch',
        'Custom_beta',
        'Custom_helpers',
        'Custom_live',
        'Custom_monitoring',
        'Custom_policy',
        'Custom_search',
        'Custom_vpn'
    ],
    'network_stack': [
        'SDK_networks',
        'SDK_switch',
        'SDK_appliance',
        'SDK_cellularGateway',
        'vpn'
    ],
    'device_management': [
        'SDK_devices',
        'SDK_camera',
        'SDK_sensor',
        'SDK_sm',
        'SDK_insight',
        'monitoring',
        'live'
    ],
    'admin_tools': [
        'SDK_organizations',
        'SDK_administered',
        'SDK_licensing',
        'SDK_batch',
        'policy'
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