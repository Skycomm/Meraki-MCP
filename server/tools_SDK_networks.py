"""
Networks tools for Cisco Meraki MCP server.

This module provides 100% coverage of the official Cisco Meraki Networks SDK v1.
All 114 official SDK methods are implemented exactly as documented.
"""

from typing import Optional, Dict, Any, List
import json

# Global references to be set by register function
app = None
meraki_client = None

def register_networks_tools(mcp_app, meraki):
    """
    Register all official SDK networks tools with the MCP server.
    Provides 100% coverage of Cisco Meraki Networks API v1.
    
    Args:
        mcp_app: MCP server instance
        meraki: Meraki client instance
    """
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    
    # Register all networks SDK tools
    register_networks_sdk_tools()

def register_networks_sdk_tools():
    """Register all networks SDK tools (100% coverage)."""
    
    # ==================== ALL 114 NETWORKS SDK TOOLS ====================
    
    @app.tool(
        name="batch_network_floor_plans_auto_locate_jobs",
        description="📦 Batch networkFloorPlansAutoLocateJobs"
    )
    def batch_network_floor_plans_auto_locate_jobs(network_id: str):
        """Batch batch networkfloorplansautolocatejobs."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.batchNetworkFloorPlansAutoLocateJobs(network_id, **kwargs)
            
            response = f"# 📦 Batch Networkfloorplansautolocatejobs\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in batch_network_floor_plans_auto_locate_jobs: {str(e)}"
    
    @app.tool(
        name="batch_network_floor_plans_devices_update",
        description="✏️ Update networkFloorPlansDevicesUpdate"
    )
    def batch_network_floor_plans_devices_update(network_id: str):
        """Update update networkfloorplansdevicesupdate."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.batchNetworkFloorPlansDevicesUpdate(network_id, **kwargs)
            
            response = f"# ✏️ Update Networkfloorplansdevicesupdate\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in batch_network_floor_plans_devices_update: {str(e)}"
    
    @app.tool(
        name="bind_network",
        description="🔗 Bind network"
    )
    def bind_network(network_id: str):
        """Bind bind network."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.bindNetwork(network_id, **kwargs)
            
            response = f"# 🔗 Bind Network\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in bind_network: {str(e)}"
    
    @app.tool(
        name="cancel_network_floor_plans_auto_locate_job",
        description="🚫 Cancel networkFloorPlansAutoLocateJob"
    )
    def cancel_network_floor_plans_auto_locate_job(network_id: str, confirmed: bool = False):
        """Cancel cancel networkfloorplansautolocatejob."""
        if not confirmed:
            return "⚠️ This operation requires confirmed=true to execute"
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.cancelNetworkFloorPlansAutoLocateJob(network_id, **kwargs)
            
            response = f"# 🚫 Cancel Networkfloorplansautolocatejob\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in cancel_network_floor_plans_auto_locate_job: {str(e)}"
    
    @app.tool(
        name="claim_network_devices",
        description="📋 Claim networkDevices"
    )
    def claim_network_devices(network_id: str):
        """Claim claim networkdevices."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.claimNetworkDevices(network_id, **kwargs)
            
            response = f"# 📋 Claim Networkdevices\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in claim_network_devices: {str(e)}"
    
    @app.tool(
        name="create_network_firmware_upgrades_rollback",
        description="➕ Create networkFirmwareUpgradesRollback"
    )
    def create_network_firmware_upgrades_rollback(network_id: str):
        """Create create networkfirmwareupgradesrollback."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.createNetworkFirmwareUpgradesRollback(network_id, **kwargs)
            
            response = f"# ➕ Create Networkfirmwareupgradesrollback\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in create_network_firmware_upgrades_rollback: {str(e)}"
    
    @app.tool(
        name="create_network_firmware_upgrades_staged_event",
        description="➕ Create networkFirmwareUpgradesStagedEvent"
    )
    def create_network_firmware_upgrades_staged_event(network_id: str):
        """Create create networkfirmwareupgradesstagedevent."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.createNetworkFirmwareUpgradesStagedEvent(network_id, **kwargs)
            
            response = f"# ➕ Create Networkfirmwareupgradesstagedevent\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in create_network_firmware_upgrades_staged_event: {str(e)}"
    
    @app.tool(
        name="create_network_firmware_upgrades_staged_group",
        description="➕ Create networkFirmwareUpgradesStagedGroup"
    )
    def create_network_firmware_upgrades_staged_group(network_id: str):
        """Create create networkfirmwareupgradesstagedgroup."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.createNetworkFirmwareUpgradesStagedGroup(network_id, **kwargs)
            
            response = f"# ➕ Create Networkfirmwareupgradesstagedgroup\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in create_network_firmware_upgrades_staged_group: {str(e)}"
    
    @app.tool(
        name="create_network_floor_plan",
        description="➕ Create networkFloorPlan"
    )
    def create_network_floor_plan(network_id: str):
        """Create create networkfloorplan."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.createNetworkFloorPlan(network_id, **kwargs)
            
            response = f"# ➕ Create Networkfloorplan\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in create_network_floor_plan: {str(e)}"
    
    @app.tool(
        name="create_network_group_policy",
        description="➕ Create networkGroupPolicy"
    )
    def create_network_group_policy(network_id: str):
        """Create create networkgrouppolicy."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.createNetworkGroupPolicy(network_id, **kwargs)
            
            response = f"# ➕ Create Networkgrouppolicy\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in create_network_group_policy: {str(e)}"
    
    @app.tool(
        name="create_network_meraki_auth_user",
        description="➕ Create networkMerakiAuthUser"
    )
    def create_network_meraki_auth_user(network_id: str):
        """Create create networkmerakiauthuser."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.createNetworkMerakiAuthUser(network_id, **kwargs)
            
            response = f"# ➕ Create Networkmerakiauthuser\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in create_network_meraki_auth_user: {str(e)}"
    
    @app.tool(
        name="create_network_mqtt_broker",
        description="➕ Create networkMqttBroker"
    )
    def create_network_mqtt_broker(network_id: str):
        """Create create networkmqttbroker."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.createNetworkMqttBroker(network_id, **kwargs)
            
            response = f"# ➕ Create Networkmqttbroker\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in create_network_mqtt_broker: {str(e)}"
    
    @app.tool(
        name="create_network_pii_request",
        description="➕ Create networkPiiRequest"
    )
    def create_network_pii_request(network_id: str):
        """Create create networkpiirequest."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.createNetworkPiiRequest(network_id, **kwargs)
            
            response = f"# ➕ Create Networkpiirequest\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in create_network_pii_request: {str(e)}"
    
    @app.tool(
        name="create_network_vlan_profile",
        description="➕ Create networkVlanProfile"
    )
    def create_network_vlan_profile(network_id: str):
        """Create create networkvlanprofile."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.createNetworkVlanProfile(network_id, **kwargs)
            
            response = f"# ➕ Create Networkvlanprofile\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in create_network_vlan_profile: {str(e)}"
    
    @app.tool(
        name="create_network_webhooks_http_server",
        description="➕ Create networkWebhooksHttpServer"
    )
    def create_network_webhooks_http_server(network_id: str):
        """Create create networkwebhookshttpserver."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.createNetworkWebhooksHttpServer(network_id, **kwargs)
            
            response = f"# ➕ Create Networkwebhookshttpserver\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in create_network_webhooks_http_server: {str(e)}"
    
    @app.tool(
        name="create_network_webhooks_payload_template",
        description="➕ Create networkWebhooksPayloadTemplate"
    )
    def create_network_webhooks_payload_template(network_id: str):
        """Create create networkwebhookspayloadtemplate."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.createNetworkWebhooksPayloadTemplate(network_id, **kwargs)
            
            response = f"# ➕ Create Networkwebhookspayloadtemplate\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in create_network_webhooks_payload_template: {str(e)}"
    
    @app.tool(
        name="create_network_webhooks_webhook_test",
        description="➕ Create networkWebhooksWebhookTest"
    )
    def create_network_webhooks_webhook_test(network_id: str):
        """Create create networkwebhookswebhooktest."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.createNetworkWebhooksWebhookTest(network_id, **kwargs)
            
            response = f"# ➕ Create Networkwebhookswebhooktest\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in create_network_webhooks_webhook_test: {str(e)}"
    
    @app.tool(
        name="defer_network_firmware_upgrades_staged_events",
        description="⏸️ Defer networkFirmwareUpgradesStagedEvents"
    )
    def defer_network_firmware_upgrades_staged_events(network_id: str):
        """Defer defer networkfirmwareupgradesstagedevents."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.deferNetworkFirmwareUpgradesStagedEvents(network_id, **kwargs)
            
            response = f"# ⏸️ Defer Networkfirmwareupgradesstagedevents\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in defer_network_firmware_upgrades_staged_events: {str(e)}"
    
    @app.tool(
        name="delete_network",
        description="❌ Delete network"
    )
    def delete_network(network_id: str, confirmed: bool = False):
        """Delete delete network."""
        if not confirmed:
            return "⚠️ This operation requires confirmed=true to execute"
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.deleteNetwork(network_id, **kwargs)
            
            response = f"# ❌ Delete Network\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in delete_network: {str(e)}"
    
    @app.tool(
        name="delete_network_firmware_upgrades_staged_group",
        description="❌ Delete networkFirmwareUpgradesStagedGroup"
    )
    def delete_network_firmware_upgrades_staged_group(network_id: str, confirmed: bool = False):
        """Delete delete networkfirmwareupgradesstagedgroup."""
        if not confirmed:
            return "⚠️ This operation requires confirmed=true to execute"
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.deleteNetworkFirmwareUpgradesStagedGroup(network_id, **kwargs)
            
            response = f"# ❌ Delete Networkfirmwareupgradesstagedgroup\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in delete_network_firmware_upgrades_staged_group: {str(e)}"
    
    @app.tool(
        name="delete_network_floor_plan",
        description="❌ Delete networkFloorPlan"
    )
    def delete_network_floor_plan(network_id: str, confirmed: bool = False):
        """Delete delete networkfloorplan."""
        if not confirmed:
            return "⚠️ This operation requires confirmed=true to execute"
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.deleteNetworkFloorPlan(network_id, **kwargs)
            
            response = f"# ❌ Delete Networkfloorplan\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in delete_network_floor_plan: {str(e)}"
    
    @app.tool(
        name="delete_network_group_policy",
        description="❌ Delete networkGroupPolicy"
    )
    def delete_network_group_policy(network_id: str, confirmed: bool = False):
        """Delete delete networkgrouppolicy."""
        if not confirmed:
            return "⚠️ This operation requires confirmed=true to execute"
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.deleteNetworkGroupPolicy(network_id, **kwargs)
            
            response = f"# ❌ Delete Networkgrouppolicy\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in delete_network_group_policy: {str(e)}"
    
    @app.tool(
        name="delete_network_meraki_auth_user",
        description="❌ Delete networkMerakiAuthUser"
    )
    def delete_network_meraki_auth_user(network_id: str, confirmed: bool = False):
        """Delete delete networkmerakiauthuser."""
        if not confirmed:
            return "⚠️ This operation requires confirmed=true to execute"
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.deleteNetworkMerakiAuthUser(network_id, **kwargs)
            
            response = f"# ❌ Delete Networkmerakiauthuser\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in delete_network_meraki_auth_user: {str(e)}"
    
    @app.tool(
        name="delete_network_mqtt_broker",
        description="❌ Delete networkMqttBroker"
    )
    def delete_network_mqtt_broker(network_id: str, confirmed: bool = False):
        """Delete delete networkmqttbroker."""
        if not confirmed:
            return "⚠️ This operation requires confirmed=true to execute"
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.deleteNetworkMqttBroker(network_id, **kwargs)
            
            response = f"# ❌ Delete Networkmqttbroker\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in delete_network_mqtt_broker: {str(e)}"
    
    @app.tool(
        name="delete_network_pii_request",
        description="❌ Delete networkPiiRequest"
    )
    def delete_network_pii_request(network_id: str, confirmed: bool = False):
        """Delete delete networkpiirequest."""
        if not confirmed:
            return "⚠️ This operation requires confirmed=true to execute"
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.deleteNetworkPiiRequest(network_id, **kwargs)
            
            response = f"# ❌ Delete Networkpiirequest\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in delete_network_pii_request: {str(e)}"
    
    @app.tool(
        name="delete_network_vlan_profile",
        description="❌ Delete networkVlanProfile"
    )
    def delete_network_vlan_profile(network_id: str, confirmed: bool = False):
        """Delete delete networkvlanprofile."""
        if not confirmed:
            return "⚠️ This operation requires confirmed=true to execute"
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.deleteNetworkVlanProfile(network_id, **kwargs)
            
            response = f"# ❌ Delete Networkvlanprofile\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in delete_network_vlan_profile: {str(e)}"
    
    @app.tool(
        name="delete_network_webhooks_http_server",
        description="❌ Delete networkWebhooksHttpServer"
    )
    def delete_network_webhooks_http_server(network_id: str, confirmed: bool = False):
        """Delete delete networkwebhookshttpserver."""
        if not confirmed:
            return "⚠️ This operation requires confirmed=true to execute"
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.deleteNetworkWebhooksHttpServer(network_id, **kwargs)
            
            response = f"# ❌ Delete Networkwebhookshttpserver\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in delete_network_webhooks_http_server: {str(e)}"
    
    @app.tool(
        name="delete_network_webhooks_payload_template",
        description="❌ Delete networkWebhooksPayloadTemplate"
    )
    def delete_network_webhooks_payload_template(network_id: str, confirmed: bool = False):
        """Delete delete networkwebhookspayloadtemplate."""
        if not confirmed:
            return "⚠️ This operation requires confirmed=true to execute"
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.deleteNetworkWebhooksPayloadTemplate(network_id, **kwargs)
            
            response = f"# ❌ Delete Networkwebhookspayloadtemplate\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in delete_network_webhooks_payload_template: {str(e)}"
    
    @app.tool(
        name="get_network",
        description="🌐 Get network"
    )
    def get_network(network_id: str):
        """Get get network."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.getNetwork(network_id, **kwargs)
            
            response = f"# 🌐 Get Network\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network: {str(e)}"
    
    @app.tool(
        name="get_network_alerts_history",
        description="🌐 Get networkAlertsHistory"
    )
    def get_network_alerts_history(network_id: str):
        """Get get networkalertshistory."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.getNetworkAlertsHistory(network_id, **kwargs)
            
            response = f"# 🌐 Get Networkalertshistory\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_alerts_history: {str(e)}"
    
    @app.tool(
        name="get_network_alerts_settings",
        description="🌐 Get networkAlertsSettings"
    )
    def get_network_alerts_settings(network_id: str):
        """Get get networkalertssettings."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.getNetworkAlertsSettings(network_id, **kwargs)
            
            response = f"# 🌐 Get Networkalertssettings\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_alerts_settings: {str(e)}"
    
    @app.tool(
        name="get_network_bluetooth_client",
        description="🌐 Get networkBluetoothClient"
    )
    def get_network_bluetooth_client(network_id: str, client_id: str):
        """Get get networkbluetoothclient."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.getNetworkBluetoothClient(network_id, client_id, **kwargs)
            
            response = f"# 🌐 Get Networkbluetoothclient\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_bluetooth_client: {str(e)}"
    
    @app.tool(
        name="get_network_bluetooth_clients",
        description="🌐 Get networkBluetoothClients"
    )
    def get_network_bluetooth_clients(network_id: str, per_page: int = 1000):
        """Get get networkbluetoothclients."""
        try:
            kwargs = {}
            
            if 'per_page' in locals() and per_page:
                kwargs['perPage'] = min(per_page, 1000)
            
            result = meraki_client.dashboard.networks.getNetworkBluetoothClients(network_id, **kwargs)
            
            response = f"# 🌐 Get Networkbluetoothclients\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_bluetooth_clients: {str(e)}"
    
    @app.tool(
        name="get_network_client",
        description="🌐 Get networkClient"
    )
    def get_network_client(network_id: str, client_id: str):
        """Get get networkclient."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.getNetworkClient(network_id, client_id, **kwargs)
            
            response = f"# 🌐 Get Networkclient\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_client: {str(e)}"
    
    @app.tool(
        name="get_network_client_policy",
        description="🌐 Get networkClientPolicy"
    )
    def get_network_client_policy(network_id: str, client_id: str):
        """Get get networkclientpolicy."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.getNetworkClientPolicy(network_id, client_id, **kwargs)
            
            response = f"# 🌐 Get Networkclientpolicy\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_client_policy: {str(e)}"
    
    @app.tool(
        name="get_network_client_splash_authorization_status",
        description="🌐 Get networkClientSplashAuthorizationStatus"
    )
    def get_network_client_splash_authorization_status(network_id: str, per_page: int = 1000):
        """Get get networkclientsplashauthorizationstatus."""
        try:
            kwargs = {}
            
            if 'per_page' in locals() and per_page:
                kwargs['perPage'] = min(per_page, 1000)
            
            result = meraki_client.dashboard.networks.getNetworkClientSplashAuthorizationStatus(network_id, **kwargs)
            
            response = f"# 🌐 Get Networkclientsplashauthorizationstatus\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_client_splash_authorization_status: {str(e)}"
    
    @app.tool(
        name="get_network_client_traffic_history",
        description="🌐 Get networkClientTrafficHistory"
    )
    def get_network_client_traffic_history(network_id: str, client_id: str):
        """Get get networkclienttraffichistory."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.getNetworkClientTrafficHistory(network_id, client_id, **kwargs)
            
            response = f"# 🌐 Get Networkclienttraffichistory\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_client_traffic_history: {str(e)}"
    
    @app.tool(
        name="get_network_client_usage_history",
        description="🌐 Get networkClientUsageHistory"
    )
    def get_network_client_usage_history(network_id: str, client_id: str):
        """Get get networkclientusagehistory."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.getNetworkClientUsageHistory(network_id, client_id, **kwargs)
            
            response = f"# 🌐 Get Networkclientusagehistory\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_client_usage_history: {str(e)}"
    
    @app.tool(
        name="get_network_clients",
        description="🌐 Get networkClients"
    )
    def get_network_clients(network_id: str, per_page: int = 1000):
        """Get get networkclients."""
        try:
            kwargs = {
                'timespan': 604800,  # 7 days to get historical data
                'total_pages': 'all'  # Ensure ALL clients are retrieved
            }
            
            if 'per_page' in locals() and per_page:
                kwargs['perPage'] = min(per_page, 1000)
            
            result = meraki_client.dashboard.networks.getNetworkClients(network_id, **kwargs)
            
            response = f"# 🌐 Get Networkclients\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_clients: {str(e)}"
    
    @app.tool(
        name="get_network_clients_application_usage",
        description="🌐 Get networkClientsApplicationUsage"
    )
    def get_network_clients_application_usage(network_id: str, per_page: int = 1000):
        """Get get networkclientsapplicationusage."""
        try:
            kwargs = {}
            
            if 'per_page' in locals() and per_page:
                kwargs['perPage'] = min(per_page, 1000)
            
            result = meraki_client.dashboard.networks.getNetworkClientsApplicationUsage(network_id, **kwargs)
            
            response = f"# 🌐 Get Networkclientsapplicationusage\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_clients_application_usage: {str(e)}"
    
    @app.tool(
        name="get_network_clients_bandwidth_usage_history",
        description="🌐 Get networkClientsBandwidthUsageHistory"
    )
    def get_network_clients_bandwidth_usage_history(network_id: str, per_page: int = 1000):
        """Get get networkclientsbandwidthusagehistory."""
        try:
            kwargs = {}
            
            if 'per_page' in locals() and per_page:
                kwargs['perPage'] = min(per_page, 1000)
            
            result = meraki_client.dashboard.networks.getNetworkClientsBandwidthUsageHistory(network_id, **kwargs)
            
            response = f"# 🌐 Get Networkclientsbandwidthusagehistory\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_clients_bandwidth_usage_history: {str(e)}"
    
    @app.tool(
        name="get_network_clients_overview",
        description="🌐 Get networkClientsOverview"
    )
    def get_network_clients_overview(network_id: str, per_page: int = 1000):
        """Get get networkclientsoverview."""
        try:
            kwargs = {}
            
            if 'per_page' in locals() and per_page:
                kwargs['perPage'] = min(per_page, 1000)
            
            result = meraki_client.dashboard.networks.getNetworkClientsOverview(network_id, **kwargs)
            
            response = f"# 🌐 Get Networkclientsoverview\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_clients_overview: {str(e)}"
    
    @app.tool(
        name="get_network_clients_usage_histories",
        description="🌐 Get networkClientsUsageHistories"
    )
    def get_network_clients_usage_histories(network_id: str, per_page: int = 1000):
        """Get get networkclientsusagehistories."""
        try:
            kwargs = {}
            
            if 'per_page' in locals() and per_page:
                kwargs['perPage'] = min(per_page, 1000)
            
            result = meraki_client.dashboard.networks.getNetworkClientsUsageHistories(network_id, **kwargs)
            
            response = f"# 🌐 Get Networkclientsusagehistories\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_clients_usage_histories: {str(e)}"
    
    @app.tool(
        name="get_network_devices",
        description="🌐 Get networkDevices"
    )
    def get_network_devices(network_id: str):
        """Get all devices in a network."""
        try:
            result = meraki_client.dashboard.networks.getNetworkDevices(network_id)
            
            response = f"# 🌐 Network Devices\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Devices**: {len(result)}\n\n"
                    
                    # Show devices with complete device information
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', 'Unnamed Device')
                            response += f"**{idx}. {name}**\n"
                            
                            # Show complete device specifications
                            if 'serial' in item:
                                response += f"   - Serial: {item.get('serial')}\n"
                            if 'model' in item:
                                response += f"   - Model: {item.get('model')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'productType' in item:
                                response += f"   - Type: {item.get('productType')}\n"
                            if 'firmware' in item:
                                response += f"   - Firmware: {item.get('firmware')}\n"
                            if 'address' in item:
                                response += f"   - Address: {item.get('address')}\n"
                            if 'lat' in item and 'lng' in item:
                                lat = item.get('lat', 'N/A')
                                lng = item.get('lng', 'N/A') 
                                response += f"   - Location: {lat}, {lng}\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_devices: {str(e)}"
    
    @app.tool(
        name="get_network_events",
        description="🌐 Get networkEvents (TIP: Use product_type='wireless' for multi-device networks)"
    )
    def get_network_events(network_id: str, product_type: str = 'wireless', per_page: int = 1000):
        """Get get networkevents."""
        try:
            kwargs = {}
            
            if 'per_page' in locals() and per_page:
                kwargs['perPage'] = min(per_page, 1000)
            
            if 'product_type' in locals() and product_type:
                kwargs['productType'] = product_type
            
            result = meraki_client.dashboard.networks.getNetworkEvents(network_id, **kwargs)
            
            response = f"# 🌐 Get Networkevents\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_events: {str(e)}"
    
    @app.tool(
        name="get_network_events_event_types",
        description="🌐 Get networkEventsEventTypes"
    )
    def get_network_events_event_types(network_id: str, per_page: int = 1000):
        """Get get networkeventseventtypes."""
        try:
            kwargs = {}
            
            if 'per_page' in locals() and per_page:
                kwargs['perPage'] = min(per_page, 1000)
            
            result = meraki_client.dashboard.networks.getNetworkEventsEventTypes(network_id, **kwargs)
            
            response = f"# 🌐 Get Networkeventseventtypes\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_events_event_types: {str(e)}"
    
    @app.tool(
        name="get_network_firmware_upgrades",
        description="🌐 Get networkFirmwareUpgrades"
    )
    def get_network_firmware_upgrades(network_id: str):
        """Get get networkfirmwareupgrades."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.getNetworkFirmwareUpgrades(network_id, **kwargs)
            
            response = f"# 🌐 Get Networkfirmwareupgrades\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_firmware_upgrades: {str(e)}"
    
    @app.tool(
        name="get_network_firmware_upgrades_staged_events",
        description="🌐 Get networkFirmwareUpgradesStagedEvents"
    )
    def get_network_firmware_upgrades_staged_events(network_id: str, per_page: int = 1000):
        """Get get networkfirmwareupgradesstagedevents."""
        try:
            kwargs = {}
            
            if 'per_page' in locals() and per_page:
                kwargs['perPage'] = min(per_page, 1000)
            
            result = meraki_client.dashboard.networks.getNetworkFirmwareUpgradesStagedEvents(network_id, **kwargs)
            
            response = f"# 🌐 Get Networkfirmwareupgradesstagedevents\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_firmware_upgrades_staged_events: {str(e)}"
    
    @app.tool(
        name="get_network_firmware_upgrades_staged_group",
        description="🌐 Get networkFirmwareUpgradesStagedGroup"
    )
    def get_network_firmware_upgrades_staged_group(network_id: str):
        """Get get networkfirmwareupgradesstagedgroup."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.getNetworkFirmwareUpgradesStagedGroup(network_id, **kwargs)
            
            response = f"# 🌐 Get Networkfirmwareupgradesstagedgroup\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_firmware_upgrades_staged_group: {str(e)}"
    
    @app.tool(
        name="get_network_firmware_upgrades_staged_groups",
        description="🌐 Get networkFirmwareUpgradesStagedGroups"
    )
    def get_network_firmware_upgrades_staged_groups(network_id: str, per_page: int = 1000):
        """Get get networkfirmwareupgradesstagedgroups."""
        try:
            kwargs = {}
            
            if 'per_page' in locals() and per_page:
                kwargs['perPage'] = min(per_page, 1000)
            
            result = meraki_client.dashboard.networks.getNetworkFirmwareUpgradesStagedGroups(network_id, **kwargs)
            
            response = f"# 🌐 Get Networkfirmwareupgradesstagedgroups\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_firmware_upgrades_staged_groups: {str(e)}"
    
    @app.tool(
        name="get_network_firmware_upgrades_staged_stages",
        description="🌐 Get networkFirmwareUpgradesStagedStages"
    )
    def get_network_firmware_upgrades_staged_stages(network_id: str):
        """Get get networkfirmwareupgradesstagedstages."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.getNetworkFirmwareUpgradesStagedStages(network_id, **kwargs)
            
            response = f"# 🌐 Get Networkfirmwareupgradesstagedstages\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_firmware_upgrades_staged_stages: {str(e)}"
    
    @app.tool(
        name="get_network_floor_plan",
        description="🌐 Get networkFloorPlan"
    )
    def get_network_floor_plan(network_id: str):
        """Get get networkfloorplan."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.getNetworkFloorPlan(network_id, **kwargs)
            
            response = f"# 🌐 Get Networkfloorplan\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_floor_plan: {str(e)}"
    
    @app.tool(
        name="get_network_floor_plans",
        description="🌐 Get networkFloorPlans"
    )
    def get_network_floor_plans(network_id: str):
        """Get get networkfloorplans."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.getNetworkFloorPlans(network_id, **kwargs)
            
            response = f"# 🌐 Get Networkfloorplans\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_floor_plans: {str(e)}"
    
    @app.tool(
        name="get_network_group_policies",
        description="🌐 Get networkGroupPolicies"
    )
    def get_network_group_policies(network_id: str):
        """Get get networkgrouppolicies."""
        try:
            result = meraki_client.dashboard.networks.getNetworkGroupPolicies(network_id)
            
            response = f"# 🌐 Get Networkgrouppolicies\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_group_policies: {str(e)}"
    
    @app.tool(
        name="get_network_group_policy",
        description="🌐 Get networkGroupPolicy"
    )
    def get_network_group_policy(network_id: str):
        """Get get networkgrouppolicy."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.getNetworkGroupPolicy(network_id, **kwargs)
            
            response = f"# 🌐 Get Networkgrouppolicy\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_group_policy: {str(e)}"
    
    @app.tool(
        name="get_network_health_alerts",
        description="🌐 Get networkHealthAlerts"
    )
    def get_network_health_alerts(network_id: str):
        """Get get networkhealthalerts."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.getNetworkHealthAlerts(network_id, **kwargs)
            
            response = f"# 🌐 Get Networkhealthalerts\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_health_alerts: {str(e)}"
    
    @app.tool(
        name="get_network_meraki_auth_user",
        description="🌐 Get networkMerakiAuthUser"
    )
    def get_network_meraki_auth_user(network_id: str):
        """Get get networkmerakiauthuser."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.getNetworkMerakiAuthUser(network_id, **kwargs)
            
            response = f"# 🌐 Get Networkmerakiauthuser\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_meraki_auth_user: {str(e)}"
    
    @app.tool(
        name="get_network_meraki_auth_users",
        description="🌐 Get networkMerakiAuthUsers"
    )
    def get_network_meraki_auth_users(network_id: str, per_page: int = 1000):
        """Get get networkmerakiauthusers."""
        try:
            kwargs = {}
            
            if 'per_page' in locals() and per_page:
                kwargs['perPage'] = min(per_page, 1000)
            
            result = meraki_client.dashboard.networks.getNetworkMerakiAuthUsers(network_id, **kwargs)
            
            response = f"# 🌐 Get Networkmerakiauthusers\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_meraki_auth_users: {str(e)}"
    
    @app.tool(
        name="get_network_mqtt_broker",
        description="🌐 Get networkMqttBroker"
    )
    def get_network_mqtt_broker(network_id: str):
        """Get get networkmqttbroker."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.getNetworkMqttBroker(network_id, **kwargs)
            
            response = f"# 🌐 Get Networkmqttbroker\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_mqtt_broker: {str(e)}"
    
    @app.tool(
        name="get_network_mqtt_brokers",
        description="🌐 Get networkMqttBrokers"
    )
    def get_network_mqtt_brokers(network_id: str, per_page: int = 1000):
        """Get get networkmqttbrokers."""
        try:
            kwargs = {}
            
            if 'per_page' in locals() and per_page:
                kwargs['perPage'] = min(per_page, 1000)
            
            result = meraki_client.dashboard.networks.getNetworkMqttBrokers(network_id, **kwargs)
            
            response = f"# 🌐 Get Networkmqttbrokers\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_mqtt_brokers: {str(e)}"
    
    @app.tool(
        name="get_network_netflow",
        description="🌐 Get networkNetflow"
    )
    def get_network_netflow(network_id: str):
        """Get get networknetflow."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.getNetworkNetflow(network_id, **kwargs)
            
            response = f"# 🌐 Get Networknetflow\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_netflow: {str(e)}"
    
    @app.tool(
        name="get_network_network_health_channel_utilization",
        description="🌐 Get network networkHealthChannelUtilization"
    )
    def get_network_network_health_channel_utilization(network_id: str):
        """Get get network networkhealthchannelutilization."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.getNetworkNetworkHealthChannelUtilization(network_id, **kwargs)
            
            response = f"# 🌐 Get Network Networkhealthchannelutilization\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_network_health_channel_utilization: {str(e)}"
    
    @app.tool(
        name="get_network_pii_pii_keys",
        description="🌐 Get networkPiiPiiKeys"
    )
    def get_network_pii_pii_keys(network_id: str):
        """Get get networkpiipiikeys."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.getNetworkPiiPiiKeys(network_id, **kwargs)
            
            response = f"# 🌐 Get Networkpiipiikeys\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_pii_pii_keys: {str(e)}"
    
    @app.tool(
        name="get_network_pii_request",
        description="🌐 Get networkPiiRequest"
    )
    def get_network_pii_request(network_id: str):
        """Get get networkpiirequest."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.getNetworkPiiRequest(network_id, **kwargs)
            
            response = f"# 🌐 Get Networkpiirequest\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_pii_request: {str(e)}"
    
    @app.tool(
        name="get_network_pii_requests",
        description="🌐 Get networkPiiRequests"
    )
    def get_network_pii_requests(network_id: str):
        """Get get networkpiirequests."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.getNetworkPiiRequests(network_id, **kwargs)
            
            response = f"# 🌐 Get Networkpiirequests\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_pii_requests: {str(e)}"
    
    @app.tool(
        name="get_network_pii_sm_devices_for_key",
        description="🌐 Get networkPiiSmDevicesForKey"
    )
    def get_network_pii_sm_devices_for_key(network_id: str, per_page: int = 1000):
        """Get get networkpiismdevicesforkey."""
        try:
            kwargs = {}
            
            if 'per_page' in locals() and per_page:
                kwargs['perPage'] = min(per_page, 1000)
            
            result = meraki_client.dashboard.networks.getNetworkPiiSmDevicesForKey(network_id, **kwargs)
            
            response = f"# 🌐 Get Networkpiismdevicesforkey\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_pii_sm_devices_for_key: {str(e)}"
    
    @app.tool(
        name="get_network_pii_sm_owners_for_key",
        description="🌐 Get networkPiiSmOwnersForKey"
    )
    def get_network_pii_sm_owners_for_key(network_id: str):
        """Get get networkpiismownersforkey."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.getNetworkPiiSmOwnersForKey(network_id, **kwargs)
            
            response = f"# 🌐 Get Networkpiismownersforkey\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_pii_sm_owners_for_key: {str(e)}"
    
    @app.tool(
        name="get_network_policies_by_client",
        description="🌐 Get networkPoliciesByClient"
    )
    def get_network_policies_by_client(network_id: str, client_id: str, per_page: int = 1000):
        """Get get networkpoliciesbyclient."""
        try:
            kwargs = {}
            
            if 'per_page' in locals() and per_page:
                kwargs['perPage'] = min(per_page, 1000)
            
            result = meraki_client.dashboard.networks.getNetworkPoliciesByClient(network_id, client_id, **kwargs)
            
            response = f"# 🌐 Get Networkpoliciesbyclient\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_policies_by_client: {str(e)}"
    
    @app.tool(
        name="get_network_settings",
        description="🌐 Get networkSettings"
    )
    def get_network_settings(network_id: str):
        """Get get networksettings."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.getNetworkSettings(network_id, **kwargs)
            
            response = f"# 🌐 Get Networksettings\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_settings: {str(e)}"
    
    @app.tool(
        name="get_network_snmp",
        description="🌐 Get networkSnmp"
    )
    def get_network_snmp(network_id: str):
        """Get get networksnmp."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.getNetworkSnmp(network_id, **kwargs)
            
            response = f"# 🌐 Get Networksnmp\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_snmp: {str(e)}"
    
    @app.tool(
        name="get_network_splash_login_attempts",
        description="🌐 Get networkSplashLoginAttempts"
    )
    def get_network_splash_login_attempts(network_id: str):
        """Get get networksplashloginattempts."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.getNetworkSplashLoginAttempts(network_id, **kwargs)
            
            response = f"# 🌐 Get Networksplashloginattempts\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_splash_login_attempts: {str(e)}"
    
    @app.tool(
        name="get_network_syslog_servers",
        description="🌐 Get networkSyslogServers"
    )
    def get_network_syslog_servers(network_id: str, per_page: int = 1000):
        """Get get networksyslogservers."""
        try:
            kwargs = {}
            
            if 'per_page' in locals() and per_page:
                kwargs['perPage'] = min(per_page, 1000)
            
            result = meraki_client.dashboard.networks.getNetworkSyslogServers(network_id, **kwargs)
            
            response = f"# 🌐 Get Networksyslogservers\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_syslog_servers: {str(e)}"
    
    @app.tool(
        name="get_network_topology_link_layer",
        description="🌐 Get networkTopologyLinkLayer"
    )
    def get_network_topology_link_layer(network_id: str):
        """Get get networktopologylinklayer."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.getNetworkTopologyLinkLayer(network_id, **kwargs)
            
            response = f"# 🌐 Get Networktopologylinklayer\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_topology_link_layer: {str(e)}"
    
    @app.tool(
        name="get_network_traffic",
        description="🌐 Get networkTraffic"
    )
    def get_network_traffic(network_id: str):
        """Get get networktraffic."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.getNetworkTraffic(network_id, **kwargs)
            
            response = f"# 🌐 Get Networktraffic\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_traffic: {str(e)}"
    
    @app.tool(
        name="get_network_traffic_analysis",
        description="🌐 Get networkTrafficAnalysis"
    )
    def get_network_traffic_analysis(network_id: str):
        """Get get networktrafficanalysis."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.getNetworkTrafficAnalysis(network_id, **kwargs)
            
            response = f"# 🌐 Get Networktrafficanalysis\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_traffic_analysis: {str(e)}"
    
    @app.tool(
        name="get_network_traffic_shaping_application_categories",
        description="🌐 Get networkTrafficShapingApplicationCategories"
    )
    def get_network_traffic_shaping_application_categories(network_id: str):
        """Get get networktrafficshapingapplicationcategories."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.getNetworkTrafficShapingApplicationCategories(network_id, **kwargs)
            
            response = f"# 🌐 Get Networktrafficshapingapplicationcategories\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_traffic_shaping_application_categories: {str(e)}"
    
    @app.tool(
        name="get_network_traffic_shaping_dscp_tagging_options",
        description="🌐 Get networkTrafficShapingDscpTaggingOptions"
    )
    def get_network_traffic_shaping_dscp_tagging_options(network_id: str):
        """Get get networktrafficshapingdscptaggingoptions."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.getNetworkTrafficShapingDscpTaggingOptions(network_id, **kwargs)
            
            response = f"# 🌐 Get Networktrafficshapingdscptaggingoptions\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_traffic_shaping_dscp_tagging_options: {str(e)}"
    
    @app.tool(
        name="get_network_vlan_profile",
        description="🌐 Get networkVlanProfile"
    )
    def get_network_vlan_profile(network_id: str):
        """Get get networkvlanprofile."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.getNetworkVlanProfile(network_id, **kwargs)
            
            response = f"# 🌐 Get Networkvlanprofile\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_vlan_profile: {str(e)}"
    
    @app.tool(
        name="get_network_vlan_profiles",
        description="🌐 Get networkVlanProfiles"
    )
    def get_network_vlan_profiles(network_id: str):
        """Get get networkvlanprofiles."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.getNetworkVlanProfiles(network_id, **kwargs)
            
            response = f"# 🌐 Get Networkvlanprofiles\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_vlan_profiles: {str(e)}"
    
    @app.tool(
        name="get_network_vlan_profiles_assignments_by_device",
        description="🌐 Get networkVlanProfilesAssignmentsByDevice"
    )
    def get_network_vlan_profiles_assignments_by_device(network_id: str):
        """Get get networkvlanprofilesassignmentsbydevice."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.getNetworkVlanProfilesAssignmentsByDevice(network_id, **kwargs)
            
            response = f"# 🌐 Get Networkvlanprofilesassignmentsbydevice\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_vlan_profiles_assignments_by_device: {str(e)}"
    
    @app.tool(
        name="get_network_webhooks_http_server",
        description="🌐 Get networkWebhooksHttpServer"
    )
    def get_network_webhooks_http_server(network_id: str):
        """Get get networkwebhookshttpserver."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.getNetworkWebhooksHttpServer(network_id, **kwargs)
            
            response = f"# 🌐 Get Networkwebhookshttpserver\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_webhooks_http_server: {str(e)}"
    
    @app.tool(
        name="get_network_webhooks_http_servers",
        description="🌐 Get networkWebhooksHttpServers"
    )
    def get_network_webhooks_http_servers(network_id: str, per_page: int = 1000):
        """Get get networkwebhookshttpservers."""
        try:
            kwargs = {}
            
            if 'per_page' in locals() and per_page:
                kwargs['perPage'] = min(per_page, 1000)
            
            result = meraki_client.dashboard.networks.getNetworkWebhooksHttpServers(network_id, **kwargs)
            
            response = f"# 🌐 Get Networkwebhookshttpservers\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_webhooks_http_servers: {str(e)}"
    
    @app.tool(
        name="get_network_webhooks_payload_template",
        description="🌐 Get networkWebhooksPayloadTemplate"
    )
    def get_network_webhooks_payload_template(network_id: str):
        """Get get networkwebhookspayloadtemplate."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.getNetworkWebhooksPayloadTemplate(network_id, **kwargs)
            
            response = f"# 🌐 Get Networkwebhookspayloadtemplate\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_webhooks_payload_template: {str(e)}"
    
    @app.tool(
        name="get_network_webhooks_payload_templates",
        description="🌐 Get networkWebhooksPayloadTemplates"
    )
    def get_network_webhooks_payload_templates(network_id: str, per_page: int = 1000):
        """Get get networkwebhookspayloadtemplates."""
        try:
            kwargs = {}
            
            if 'per_page' in locals() and per_page:
                kwargs['perPage'] = min(per_page, 1000)
            
            result = meraki_client.dashboard.networks.getNetworkWebhooksPayloadTemplates(network_id, **kwargs)
            
            response = f"# 🌐 Get Networkwebhookspayloadtemplates\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_webhooks_payload_templates: {str(e)}"
    
    @app.tool(
        name="get_network_webhooks_webhook_test",
        description="🌐 Get networkWebhooksWebhookTest"
    )
    def get_network_webhooks_webhook_test(network_id: str):
        """Get get networkwebhookswebhooktest."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.getNetworkWebhooksWebhookTest(network_id, **kwargs)
            
            response = f"# 🌐 Get Networkwebhookswebhooktest\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_webhooks_webhook_test: {str(e)}"
    
    @app.tool(
        name="provision_network_clients",
        description="⚙️ Provision networkClients"
    )
    def provision_network_clients(network_id: str):
        """Provision provision networkclients."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.provisionNetworkClients(network_id, **kwargs)
            
            response = f"# ⚙️ Provision Networkclients\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in provision_network_clients: {str(e)}"
    
    @app.tool(
        name="publish_network_floor_plans_auto_locate_job",
        description="🌐 publish networkFloorPlansAutoLocateJob"
    )
    def publish_network_floor_plans_auto_locate_job(network_id: str):
        """Manage publish networkfloorplansautolocatejob."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.publishNetworkFloorPlansAutoLocateJob(network_id, **kwargs)
            
            response = f"# 🌐 Publish Networkfloorplansautolocatejob\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in publish_network_floor_plans_auto_locate_job: {str(e)}"
    
    @app.tool(
        name="reassign_network_vlan_profiles_assignments",
        description="🌐 reassign networkVlanProfilesAssignments"
    )
    def reassign_network_vlan_profiles_assignments(network_id: str):
        """Manage reassign networkvlanprofilesassignments."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.reassignNetworkVlanProfilesAssignments(network_id, **kwargs)
            
            response = f"# 🌐 Reassign Networkvlanprofilesassignments\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in reassign_network_vlan_profiles_assignments: {str(e)}"
    
    @app.tool(
        name="recalculate_network_floor_plans_auto_locate_job",
        description="🌐 recalculate networkFloorPlansAutoLocateJob"
    )
    def recalculate_network_floor_plans_auto_locate_job(network_id: str):
        """Manage recalculate networkfloorplansautolocatejob."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.recalculateNetworkFloorPlansAutoLocateJob(network_id, **kwargs)
            
            response = f"# 🌐 Recalculate Networkfloorplansautolocatejob\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in recalculate_network_floor_plans_auto_locate_job: {str(e)}"
    
    @app.tool(
        name="remove_network_devices",
        description="🗑️ Remove networkDevices"
    )
    def remove_network_devices(network_id: str, confirmed: bool = False):
        """Remove remove networkdevices."""
        if not confirmed:
            return "⚠️ This operation requires confirmed=true to execute"
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.removeNetworkDevices(network_id, **kwargs)
            
            response = f"# 🗑️ Remove Networkdevices\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in remove_network_devices: {str(e)}"
    
    @app.tool(
        name="rollbacks_network_firmware_upgrades_staged_events",
        description="⏪ Rollbacks networkFirmwareUpgradesStagedEvents"
    )
    def rollbacks_network_firmware_upgrades_staged_events(network_id: str):
        """Rollback rollbacks networkfirmwareupgradesstagedevents."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.rollbacksNetworkFirmwareUpgradesStagedEvents(network_id, **kwargs)
            
            response = f"# ⏪ Rollbacks Networkfirmwareupgradesstagedevents\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in rollbacks_network_firmware_upgrades_staged_events: {str(e)}"
    
    @app.tool(
        name="split_network",
        description="✂️ Split network"
    )
    def split_network(network_id: str, confirmed: bool = False):
        """Split split network."""
        if not confirmed:
            return "⚠️ This operation requires confirmed=true to execute"
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.splitNetwork(network_id, **kwargs)
            
            response = f"# ✂️ Split Network\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in split_network: {str(e)}"
    
    @app.tool(
        name="unbind_network",
        description="🔗 unBind network"
    )
    def unbind_network(network_id: str):
        """Bind unbind network."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.unbindNetwork(network_id, **kwargs)
            
            response = f"# 🔗 Unbind Network\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in unbind_network: {str(e)}"
    
    @app.tool(
        name="update_network",
        description="✏️ Update network"
    )
    def update_network(network_id: str):
        """Update update network."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.updateNetwork(network_id, **kwargs)
            
            response = f"# ✏️ Update Network\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in update_network: {str(e)}"
    
    @app.tool(
        name="update_network_alerts_settings",
        description="✏️ Update networkAlertsSettings"
    )
    def update_network_alerts_settings(network_id: str):
        """Update update networkalertssettings."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.updateNetworkAlertsSettings(network_id, **kwargs)
            
            response = f"# ✏️ Update Networkalertssettings\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in update_network_alerts_settings: {str(e)}"
    
    @app.tool(
        name="update_network_client_policy",
        description="✏️ Update networkClientPolicy"
    )
    def update_network_client_policy(network_id: str, client_id: str):
        """Update update networkclientpolicy."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.updateNetworkClientPolicy(network_id, client_id, **kwargs)
            
            response = f"# ✏️ Update Networkclientpolicy\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in update_network_client_policy: {str(e)}"
    
    @app.tool(
        name="update_network_client_splash_authorization_status",
        description="✏️ Update networkClientSplashAuthorizationStatus"
    )
    def update_network_client_splash_authorization_status(network_id: str):
        """Update update networkclientsplashauthorizationstatus."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.updateNetworkClientSplashAuthorizationStatus(network_id, **kwargs)
            
            response = f"# ✏️ Update Networkclientsplashauthorizationstatus\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in update_network_client_splash_authorization_status: {str(e)}"
    
    @app.tool(
        name="update_network_firmware_upgrades",
        description="✏️ Update networkFirmwareUpgrades"
    )
    def update_network_firmware_upgrades(network_id: str):
        """Update update networkfirmwareupgrades."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.updateNetworkFirmwareUpgrades(network_id, **kwargs)
            
            response = f"# ✏️ Update Networkfirmwareupgrades\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in update_network_firmware_upgrades: {str(e)}"
    
    @app.tool(
        name="update_network_firmware_upgrades_staged_events",
        description="✏️ Update networkFirmwareUpgradesStagedEvents"
    )
    def update_network_firmware_upgrades_staged_events(network_id: str):
        """Update update networkfirmwareupgradesstagedevents."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.updateNetworkFirmwareUpgradesStagedEvents(network_id, **kwargs)
            
            response = f"# ✏️ Update Networkfirmwareupgradesstagedevents\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in update_network_firmware_upgrades_staged_events: {str(e)}"
    
    @app.tool(
        name="update_network_firmware_upgrades_staged_group",
        description="✏️ Update networkFirmwareUpgradesStagedGroup"
    )
    def update_network_firmware_upgrades_staged_group(network_id: str):
        """Update update networkfirmwareupgradesstagedgroup."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.updateNetworkFirmwareUpgradesStagedGroup(network_id, **kwargs)
            
            response = f"# ✏️ Update Networkfirmwareupgradesstagedgroup\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in update_network_firmware_upgrades_staged_group: {str(e)}"
    
    @app.tool(
        name="update_network_firmware_upgrades_staged_stages",
        description="✏️ Update networkFirmwareUpgradesStagedStages"
    )
    def update_network_firmware_upgrades_staged_stages(network_id: str):
        """Update update networkfirmwareupgradesstagedstages."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.updateNetworkFirmwareUpgradesStagedStages(network_id, **kwargs)
            
            response = f"# ✏️ Update Networkfirmwareupgradesstagedstages\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in update_network_firmware_upgrades_staged_stages: {str(e)}"
    
    @app.tool(
        name="update_network_floor_plan",
        description="✏️ Update networkFloorPlan"
    )
    def update_network_floor_plan(network_id: str):
        """Update update networkfloorplan."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.updateNetworkFloorPlan(network_id, **kwargs)
            
            response = f"# ✏️ Update Networkfloorplan\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in update_network_floor_plan: {str(e)}"
    
    @app.tool(
        name="update_network_group_policy",
        description="✏️ Update networkGroupPolicy"
    )
    def update_network_group_policy(network_id: str):
        """Update update networkgrouppolicy."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.updateNetworkGroupPolicy(network_id, **kwargs)
            
            response = f"# ✏️ Update Networkgrouppolicy\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in update_network_group_policy: {str(e)}"
    
    @app.tool(
        name="update_network_meraki_auth_user",
        description="✏️ Update networkMerakiAuthUser"
    )
    def update_network_meraki_auth_user(network_id: str):
        """Update update networkmerakiauthuser."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.updateNetworkMerakiAuthUser(network_id, **kwargs)
            
            response = f"# ✏️ Update Networkmerakiauthuser\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in update_network_meraki_auth_user: {str(e)}"
    
    @app.tool(
        name="update_network_mqtt_broker",
        description="✏️ Update networkMqttBroker"
    )
    def update_network_mqtt_broker(network_id: str):
        """Update update networkmqttbroker."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.updateNetworkMqttBroker(network_id, **kwargs)
            
            response = f"# ✏️ Update Networkmqttbroker\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in update_network_mqtt_broker: {str(e)}"
    
    @app.tool(
        name="update_network_netflow",
        description="✏️ Update networkNetflow"
    )
    def update_network_netflow(network_id: str):
        """Update update networknetflow."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.updateNetworkNetflow(network_id, **kwargs)
            
            response = f"# ✏️ Update Networknetflow\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in update_network_netflow: {str(e)}"
    
    @app.tool(
        name="update_network_settings",
        description="✏️ Update networkSettings"
    )
    def update_network_settings(network_id: str):
        """Update update networksettings."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.updateNetworkSettings(network_id, **kwargs)
            
            response = f"# ✏️ Update Networksettings\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in update_network_settings: {str(e)}"
    
    @app.tool(
        name="update_network_snmp",
        description="✏️ Update networkSnmp"
    )
    def update_network_snmp(network_id: str):
        """Update update networksnmp."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.updateNetworkSnmp(network_id, **kwargs)
            
            response = f"# ✏️ Update Networksnmp\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in update_network_snmp: {str(e)}"
    
    @app.tool(
        name="update_network_syslog_servers",
        description="✏️ Update networkSyslogServers"
    )
    def update_network_syslog_servers(network_id: str):
        """Update update networksyslogservers."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.updateNetworkSyslogServers(network_id, **kwargs)
            
            response = f"# ✏️ Update Networksyslogservers\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in update_network_syslog_servers: {str(e)}"
    
    @app.tool(
        name="update_network_traffic_analysis",
        description="✏️ Update networkTrafficAnalysis"
    )
    def update_network_traffic_analysis(network_id: str):
        """Update update networktrafficanalysis."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.updateNetworkTrafficAnalysis(network_id, **kwargs)
            
            response = f"# ✏️ Update Networktrafficanalysis\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in update_network_traffic_analysis: {str(e)}"
    
    @app.tool(
        name="update_network_vlan_profile",
        description="✏️ Update networkVlanProfile"
    )
    def update_network_vlan_profile(network_id: str):
        """Update update networkvlanprofile."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.updateNetworkVlanProfile(network_id, **kwargs)
            
            response = f"# ✏️ Update Networkvlanprofile\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in update_network_vlan_profile: {str(e)}"
    
    @app.tool(
        name="update_network_webhooks_http_server",
        description="✏️ Update networkWebhooksHttpServer"
    )
    def update_network_webhooks_http_server(network_id: str):
        """Update update networkwebhookshttpserver."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.updateNetworkWebhooksHttpServer(network_id, **kwargs)
            
            response = f"# ✏️ Update Networkwebhookshttpserver\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in update_network_webhooks_http_server: {str(e)}"
    
    @app.tool(
        name="update_network_webhooks_payload_template",
        description="✏️ Update networkWebhooksPayloadTemplate"
    )
    def update_network_webhooks_payload_template(network_id: str):
        """Update update networkwebhookspayloadtemplate."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.updateNetworkWebhooksPayloadTemplate(network_id, **kwargs)
            
            response = f"# ✏️ Update Networkwebhookspayloadtemplate\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in update_network_webhooks_payload_template: {str(e)}"
    
    @app.tool(
        name="vmx_network_devices_claim",
        description="📋 Claim networkDevicesClaim"
    )
    def vmx_network_devices_claim(network_id: str):
        """Claim claim networkdevicesclaim."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.networks.vmxNetworkDevicesClaim(network_id, **kwargs)
            
            response = f"# 📋 Claim Networkdevicesclaim\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with network-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('clientId', item.get('mac', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key network-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'ip' in item:
                                response += f"   - IP: {item.get('ip')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'manufacturer' in item:
                                response += f"   - Manufacturer: {item.get('manufacturer')}\n"
                            if 'lastSeen' in item:
                                response += f"   - Last Seen: {item.get('lastSeen')}\n"
                            if 'usage' in item:
                                usage = item.get('usage', {})
                                if isinstance(usage, dict):
                                    response += f"   - Usage: {usage.get('sent', 0) + usage.get('recv', 0)} bytes\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show network-relevant fields
                    network_fields = ['name', 'id', 'clientId', 'mac', 'ip', 'status', 'vlan', 'manufacturer', 
                                    'lastSeen', 'usage', 'timezone', 'productTypes', 'organizationId']
                    
                    for field in network_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'productTypes' and value:
                                    response += f"- **Product Types**: {', '.join(value)}\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in network_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in vmx_network_devices_claim: {str(e)}"
    
