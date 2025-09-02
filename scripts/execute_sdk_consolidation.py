#!/usr/bin/env python3
"""
Execute the SDK module consolidation.
This script performs the actual file reorganization.
"""

import os
import shutil
import re
from pathlib import Path

def backup_current_modules():
    """Create backup of current modules.""" 
    backup_dir = Path('server_backup_pre_sdk')
    if backup_dir.exists():
        shutil.rmtree(backup_dir)
    
    print("📦 Creating backup...")
    shutil.copytree('server', backup_dir)
    print(f"✅ Backup created: {backup_dir}")

def read_module_content(file_path):
    """Read and return the content of a module file."""
    if not Path(file_path).exists():
        return ""
    
    with open(file_path, 'r') as f:
        return f.read()

def extract_tools_from_module(content):
    """Extract tool definitions from module content."""
    # Find @app.tool decorations and the functions they decorate
    tool_pattern = r'(@app\.tool[^)]*\))\s*\n(def\s+\w+[^:]+:.*?)(?=\n@|\n\ndef|\nif\s+__name__|$)'
    matches = re.findall(tool_pattern, content, re.DOTALL)
    
    tools = []
    for decorator, function in matches:
        tools.append(f"{decorator}\n{function}")
    
    return tools

def create_module_header(category, description):
    """Create standard header for SDK modules."""
    return f'''#!/usr/bin/env python3
"""
Meraki SDK Tools: {category.title()}
{description}

This module contains tools that map 1:1 with the official Meraki Dashboard API SDK.
"""

from mcp.server.fastmcp import FastMCP
from meraki_client import MerakiClient
from utils.helpers import create_resource, create_content, format_error_message

def register_{category}_tools(app: FastMCP, meraki: MerakiClient):
    """Register all {category} tools with the MCP server."""
    
'''

def consolidate_appliance_modules():
    """Consolidate all appliance modules into tools_SDK_appliance.py"""
    print("\n🔧 Consolidating appliance modules...")
    
    appliance_files = [
        'server/tools_appliance.py',
        'server/tools_appliance_additional.py', 
        'server/tools_appliance_firewall.py',
        'server/tools_appliance_consolidated.py'
    ]
    
    # Read all appliance content
    all_content = []
    imports = set()
    
    for file_path in appliance_files:
        if not Path(file_path).exists():
            continue
            
        print(f"   Reading {file_path}...")
        content = read_module_content(file_path)
        
        # Extract imports 
        import_lines = re.findall(r'^(from|import)\s+.*$', content, re.MULTILINE)
        imports.update(import_lines)
        
        # Extract tools
        tools = extract_tools_from_module(content)
        all_content.extend(tools)
    
    # Create consolidated file
    header = create_module_header('appliance', 'MX Security Appliances - DNS, VPN, Firewall, Traffic Management')
    
    # Add imports
    import_section = '\n'.join(sorted(set(imports))) + '\n\n'
    
    # Add tools
    tools_section = '\n\n'.join(all_content) + '\n'
    
    # Create final content
    final_content = header + import_section + tools_section
    
    # Write new file
    new_file = 'server/tools_SDK_appliance.py'
    with open(new_file, 'w') as f:
        f.write(final_content)
    
    print(f"   ✅ Created {new_file} with {len(all_content)} tools")
    return len(all_content)

def consolidate_organizations_modules():
    """Consolidate all organizations modules into tools_SDK_organizations.py"""
    print("\n🏢 Consolidating organizations modules...")
    
    org_files = [
        'server/tools_organizations_core.py',
        'server/tools_organizations_admin.py',
        'server/tools_organizations_adaptive_policy.py', 
        'server/tools_organizations_alerts.py',
        'server/tools_organizations_config.py',
        'server/tools_organizations_earlyAccess.py',
        'server/tools_organizations_inventory.py',
        'server/tools_organizations_licensing.py',
        'server/tools_organizations_misc.py'
    ]
    
    # Read all organizations content
    all_content = []
    imports = set()
    
    for file_path in org_files:
        if not Path(file_path).exists():
            continue
            
        print(f"   Reading {file_path}...")
        content = read_module_content(file_path)
        
        # Extract imports
        import_lines = re.findall(r'^(from|import)\s+.*$', content, re.MULTILINE)
        imports.update(import_lines)
        
        # Extract tools
        tools = extract_tools_from_module(content)
        all_content.extend(tools)
    
    # Create consolidated file
    header = create_module_header('organizations', 'Organization Management - Admin, Policies, Inventory, Licensing')
    
    # Add imports
    import_section = '\n'.join(sorted(set(imports))) + '\n\n'
    
    # Add tools
    tools_section = '\n\n'.join(all_content) + '\n'
    
    # Create final content
    final_content = header + import_section + tools_section
    
    # Write new file
    new_file = 'server/tools_SDK_organizations.py'
    with open(new_file, 'w') as f:
        f.write(final_content)
    
    print(f"   ✅ Created {new_file} with {len(all_content)} tools")
    return len(all_content)

def consolidate_wireless_modules():
    """Consolidate all wireless modules into tools_SDK_wireless.py"""
    print("\n📡 Consolidating wireless modules...")
    
    wireless_files = [
        'server/tools_wireless.py',
        'server/tools_wireless_advanced.py',
        'server/tools_wireless_client_analytics.py',
        'server/tools_wireless_firewall.py',
        'server/tools_wireless_infrastructure.py', 
        'server/tools_wireless_organization.py',
        'server/tools_wireless_rf_profiles.py',
        'server/tools_wireless_ssid_features.py'
    ]
    
    # Read all wireless content
    all_content = []
    imports = set()
    
    for file_path in wireless_files:
        if not Path(file_path).exists():
            continue
            
        print(f"   Reading {file_path}...")
        content = read_module_content(file_path)
        
        # Extract imports
        import_lines = re.findall(r'^(from|import)\s+.*$', content, re.MULTILINE)
        imports.update(import_lines)
        
        # Extract tools
        tools = extract_tools_from_module(content)
        all_content.extend(tools)
    
    # Create consolidated file  
    header = create_module_header('wireless', 'Wireless Networks - APs, SSIDs, RF Profiles, Client Analytics')
    
    # Add imports
    import_section = '\n'.join(sorted(set(imports))) + '\n\n'
    
    # Add tools
    tools_section = '\n\n'.join(all_content) + '\n'
    
    # Create final content
    final_content = header + import_section + tools_section
    
    # Write new file
    new_file = 'server/tools_SDK_wireless.py'
    with open(new_file, 'w') as f:
        f.write(final_content)
    
    print(f"   ✅ Created {new_file} with {len(all_content)} tools")
    return len(all_content)

def rename_single_sdk_modules():
    """Rename single-file SDK modules to tools_SDK_* format."""
    print("\n📝 Renaming single SDK modules...")
    
    renames = {
        'server/tools_administered.py': 'server/tools_SDK_administered.py',
        'server/tools_batch.py': 'server/tools_SDK_batch.py', 
        'server/tools_camera.py': 'server/tools_SDK_camera.py',
        'server/tools_cellularGateway.py': 'server/tools_SDK_cellularGateway.py',
        'server/tools_devices.py': 'server/tools_SDK_devices.py',
        'server/tools_insight.py': 'server/tools_SDK_insight.py',
        'server/tools_licensing.py': 'server/tools_SDK_licensing.py',
        'server/tools_sensor.py': 'server/tools_SDK_sensor.py',
        'server/tools_sm.py': 'server/tools_SDK_sm.py',
        'server/tools_switch.py': 'server/tools_SDK_switch.py'
    }
    
    for old_name, new_name in renames.items():
        if Path(old_name).exists():
            print(f"   {old_name} → {new_name}")
            shutil.move(old_name, new_name)
            
            # Update function name in file
            with open(new_name, 'r') as f:
                content = f.read()
            
            # Extract category from filename
            category = Path(new_name).stem.replace('tools_SDK_', '')
            old_func = f'register_{category}_tools'
            
            # Update function name and imports if needed
            content = re.sub(
                rf'def register_\w*{category}\w*_tools\(',
                f'def register_{category}_tools(',
                content
            )
            
            with open(new_name, 'w') as f:
                f.write(content)
        else:
            print(f"   ⚠️  {old_name} not found")

def merge_networks_modules():
    """Merge tools_networks.py + tools_networks_complete.py"""
    print("\n🌐 Merging networks modules...")
    
    base_file = 'server/tools_networks.py'
    extended_file = 'server/tools_networks_complete.py'
    
    if not Path(base_file).exists():
        print(f"   ⚠️  {base_file} not found")
        return 0
        
    # Read base networks file
    base_content = read_module_content(base_file)
    
    # Read extended networks file if exists
    extended_content = ""
    if Path(extended_file).exists():
        extended_content = read_module_content(extended_file)
    
    # Extract tools from both
    base_tools = extract_tools_from_module(base_content)
    extended_tools = extract_tools_from_module(extended_content) if extended_content else []
    
    all_tools = base_tools + extended_tools
    
    # Create new consolidated networks file
    header = create_module_header('networks', 'Network Infrastructure - VLANs, Group Policies, Firmware, Floor Plans')
    
    # Extract imports from both files
    imports = set()
    import_lines = re.findall(r'^(from|import)\s+.*$', base_content, re.MULTILINE)
    imports.update(import_lines)
    if extended_content:
        import_lines = re.findall(r'^(from|import)\s+.*$', extended_content, re.MULTILINE)
        imports.update(import_lines)
    
    import_section = '\n'.join(sorted(imports)) + '\n\n'
    tools_section = '\n\n'.join(all_tools) + '\n'
    
    final_content = header + import_section + tools_section
    
    # Write new file
    new_file = 'server/tools_SDK_networks.py'
    with open(new_file, 'w') as f:
        f.write(final_content)
    
    print(f"   ✅ Created {new_file} with {len(all_tools)} tools")
    return len(all_tools)

def consolidate_custom_modules():
    """Consolidate all custom/helper modules into tools_CUSTOM_extensions.py"""
    print("\n🛠️  Consolidating custom modules...")
    
    custom_files = [
        'server/tools_helpers.py',
        'server/tools_search.py',
        'server/tools_analytics.py', 
        'server/tools_alerts.py',
        'server/tools_live.py',
        'server/tools_monitoring.py',
        'server/tools_monitoring_dashboard.py',
        'server/tools_policy.py',
        'server/tools_vpn.py',
        'server/tools_beta.py',
        'server/tools_event_analysis.py',
        'server/tools_adaptive_policy.py',
        'server/tools_custom_helpers.py',
        'server/tools_custom_analytics.py',
        'server/tools_custom_alerts.py',
        'server/tools_custom_beta.py',
        'server/tools_custom_event_analysis.py',
        'server/tools_custom_live.py',
        'server/tools_custom_monitoring.py',
        'server/tools_custom_monitoring_dashboard.py',
        'server/tools_custom_policy.py',
        'server/tools_custom_search.py',
        'server/tools_custom_vpn.py'
    ]
    
    # Read all custom content
    all_content = []
    imports = set()
    
    for file_path in custom_files:
        if not Path(file_path).exists():
            continue
            
        print(f"   Reading {file_path}...")
        content = read_module_content(file_path)
        
        # Extract imports
        import_lines = re.findall(r'^(from|import)\s+.*$', content, re.MULTILINE)
        imports.update(import_lines)
        
        # Extract tools
        tools = extract_tools_from_module(content)
        all_content.extend(tools)
    
    # Create consolidated custom file
    header = '''#!/usr/bin/env python3
"""
Meraki Custom Extensions
All non-SDK functionality: helpers, analytics, monitoring, VPN, live tools, etc.

This module contains custom tools that extend beyond the official Meraki SDK.
"""

from mcp.server.fastmcp import FastMCP
from meraki_client import MerakiClient
from utils.helpers import create_resource, create_content, format_error_message

def register_custom_extensions_tools(app: FastMCP, meraki: MerakiClient):
    """Register all custom extension tools with the MCP server."""
    
'''
    
    # Add imports
    import_section = '\n'.join(sorted(set(imports))) + '\n\n'
    
    # Add tools
    tools_section = '\n\n'.join(all_content) + '\n'
    
    # Create final content
    final_content = header + import_section + tools_section
    
    # Write new file
    new_file = 'server/tools_CUSTOM_extensions.py'
    with open(new_file, 'w') as f:
        f.write(final_content)
    
    print(f"   ✅ Created {new_file} with {len(all_content)} tools")
    return len(all_content)

def update_main_imports():
    """Update main.py to import new SDK modules only.""" 
    print("\n⚙️  Updating main.py imports...")
    
    new_imports = '''#!/usr/bin/env python3
"""
Cisco Meraki MCP Server - Modern implementation using FastMCP.
"""

from mcp.server.fastmcp import FastMCP
from meraki_client import MerakiClient
from config import SERVER_NAME, SERVER_VERSION
from utils.helpers import create_resource, create_content, format_error_message

# Initialize the Meraki client
meraki = MerakiClient()

# Initialize MCP server with the modern FastMCP class
app = FastMCP(SERVER_NAME)

# Import all SDK modules - exact 1:1 mapping with official Meraki SDK
from server.resources import register_resources
from server.tools_SDK_administered import register_administered_tools
from server.tools_SDK_appliance import register_appliance_tools
from server.tools_SDK_batch import register_batch_tools
from server.tools_SDK_camera import register_camera_tools
from server.tools_SDK_cellularGateway import register_cellularGateway_tools
from server.tools_SDK_devices import register_devices_tools
from server.tools_SDK_insight import register_insight_tools
from server.tools_SDK_licensing import register_licensing_tools
from server.tools_SDK_networks import register_networks_tools
from server.tools_SDK_organizations import register_organizations_tools
from server.tools_SDK_sensor import register_sensor_tools
from server.tools_SDK_sm import register_sm_tools
from server.tools_SDK_switch import register_switch_tools
from server.tools_SDK_wireless import register_wireless_tools

# Import custom extensions
from server.tools_CUSTOM_extensions import register_custom_extensions_tools

# Register all tools
register_resources(app, meraki)

# Register SDK tools (14 categories - exact SDK mapping)
register_administered_tools(app, meraki)
register_appliance_tools(app, meraki)  
register_batch_tools(app, meraki)
register_camera_tools(app, meraki)
register_cellularGateway_tools(app, meraki)
register_devices_tools(app, meraki)
register_insight_tools(app, meraki)
register_licensing_tools(app, meraki)
register_networks_tools(app, meraki)
register_organizations_tools(app, meraki)
register_sensor_tools(app, meraki)
register_sm_tools(app, meraki)
register_switch_tools(app, meraki)
register_wireless_tools(app, meraki)

# Register custom extensions
register_custom_extensions_tools(app, meraki)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="localhost", port=3000, reload=True)
'''
    
    with open('server/main.py', 'w') as f:
        f.write(new_imports)
    
    print("   ✅ Updated main.py with clean SDK imports")

def main():
    """Execute the full consolidation."""
    print("🚀 EXECUTING SDK MODULE CONSOLIDATION")
    print("=" * 60)
    
    # Step 1: Backup
    backup_current_modules()
    
    # Step 2: Consolidate multi-file categories
    appliance_count = consolidate_appliance_modules()
    orgs_count = consolidate_organizations_modules() 
    wireless_count = consolidate_wireless_modules()
    networks_count = merge_networks_modules()
    custom_count = consolidate_custom_modules()
    
    # Step 3: Rename single-file modules
    rename_single_sdk_modules()
    
    # Step 4: Update main.py
    update_main_imports()
    
    print("\n🎉 CONSOLIDATION COMPLETE!")
    print("=" * 60)
    print(f"✅ Created 14 SDK modules:")
    print(f"   • tools_SDK_appliance.py: {appliance_count} tools")
    print(f"   • tools_SDK_organizations.py: {orgs_count} tools") 
    print(f"   • tools_SDK_wireless.py: {wireless_count} tools")
    print(f"   • tools_SDK_networks.py: {networks_count} tools")
    print(f"   • 10 other SDK modules (renamed)")
    print()
    print(f"✅ Created 1 custom module:")
    print(f"   • tools_CUSTOM_extensions.py: {custom_count} tools")
    print()
    print(f"📊 Result: 15 modules total (from 78)")
    print(f"🔍 Next: Test with 'python meraki_server.py'")

if __name__ == '__main__':
    main()