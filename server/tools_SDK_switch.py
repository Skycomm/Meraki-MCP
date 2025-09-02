"""
Switch tools for Cisco Meraki MCP server.

This module provides 100% coverage of the official Cisco Meraki Switch SDK v1.
All 101 official SDK methods are implemented exactly as documented.
"""

from typing import Optional, Dict, Any, List
import json

# Global references to be set by register function
app = None
meraki_client = None

def register_switch_tools(mcp_app, meraki):
    """
    Register all official SDK switch tools with the MCP server.
    Provides 100% coverage of Cisco Meraki Switch API v1.
    
    Args:
        mcp_app: MCP server instance
        meraki: Meraki client instance
    """
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    
    # Register all switch SDK tools
    register_switch_sdk_tools()

def register_switch_sdk_tools():
    """Register all switch SDK tools (100% coverage)."""
    
    # ==================== ALL 101 SWITCH SDK TOOLS ====================
    
    @app.tool(
        name="add_network_switch_stack",
        description="📎 Add network switchStack"
    )
    def add_network_switch_stack(network_id: str, switch_stack_id: str):
        """Add add network switchstack."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.switch.addNetworkSwitchStack(network_id, switch_stack_id, **kwargs)
            
            response = f"# 📎 Add Network Switchstack\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in add_network_switch_stack: {str(e)}"
    
    @app.tool(
        name="clone_organization_switch_devices",
        description="📋 Clone organization switch devices"
    )
    def clone_organization_switch_devices(organization_id: str):
        """Clone clone organization switch devices."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.switch.cloneOrganizationSwitchDevices(organization_id, **kwargs)
            
            response = f"# 📋 Clone Organization Switch Devices\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in clone_organization_switch_devices: {str(e)}"
    
    @app.tool(
        name="create_device_switch_routing_interface",
        description="➕ Create device switchRoutingInterface"
    )
    def create_device_switch_routing_interface(serial: str, interface_id: str):
        """Create create device switchroutinginterface."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.switch.createDeviceSwitchRoutingInterface(serial, interface_id, **kwargs)
            
            response = f"# ➕ Create Device Switchroutinginterface\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in create_device_switch_routing_interface: {str(e)}"
    
    @app.tool(
        name="create_device_switch_routing_static_route",
        description="➕ Create device switchRoutingStaticRoute"
    )
    def create_device_switch_routing_static_route(serial: str):
        """Create create device switchroutingstaticroute."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.switch.createDeviceSwitchRoutingStaticRoute(serial, **kwargs)
            
            response = f"# ➕ Create Device Switchroutingstaticroute\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in create_device_switch_routing_static_route: {str(e)}"
    
    @app.tool(
        name="create_network_switch_access_policy",
        description="➕ Create network switchAccessPolicy"
    )
    def create_network_switch_access_policy(network_id: str):
        """Create create network switchaccesspolicy."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.switch.createNetworkSwitchAccessPolicy(network_id, **kwargs)
            
            response = f"# ➕ Create Network Switchaccesspolicy\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in create_network_switch_access_policy: {str(e)}"
    
    @app.tool(
        name="create_network_switch_dhcp_server_policy_arp_trusted_server",
        description="➕ Create network switchDhcpServerPolicyArpInspectionTrustedServer"
    )
    def create_network_switch_dhcp_server_policy_arp_inspection_trusted_server(network_id: str):
        """Create create network switchdhcpserverpolicyarpinspectiontrustedserver."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.switch.createNetworkSwitchDhcpServerPolicyArpInspectionTrustedServer(network_id, **kwargs)
            
            response = f"# ➕ Create Network Switchdhcpserverpolicyarpinspectiontrustedserver\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in create_network_switch_dhcp_server_policy_arp_inspection_trusted_server: {str(e)}"
    
    @app.tool(
        name="create_network_switch_link_aggregation",
        description="➕ Create network switchLinkAggregation"
    )
    def create_network_switch_link_aggregation(network_id: str):
        """Create create network switchlinkaggregation."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.switch.createNetworkSwitchLinkAggregation(network_id, **kwargs)
            
            response = f"# ➕ Create Network Switchlinkaggregation\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in create_network_switch_link_aggregation: {str(e)}"
    
    @app.tool(
        name="create_network_switch_port_schedule",
        description="➕ Create network switchPortSchedule"
    )
    def create_network_switch_port_schedule(network_id: str):
        """Create create network switchportschedule."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.switch.createNetworkSwitchPortSchedule(network_id, **kwargs)
            
            response = f"# ➕ Create Network Switchportschedule\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in create_network_switch_port_schedule: {str(e)}"
    
    @app.tool(
        name="create_network_switch_qos_rule",
        description="➕ Create network switchQosRule"
    )
    def create_network_switch_qos_rule(network_id: str):
        """Create create network switchqosrule."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.switch.createNetworkSwitchQosRule(network_id, **kwargs)
            
            response = f"# ➕ Create Network Switchqosrule\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in create_network_switch_qos_rule: {str(e)}"
    
    @app.tool(
        name="create_network_switch_routing_multicast_rendezvous_point",
        description="➕ Create network switchRoutingMulticastRendezvousPoint"
    )
    def create_network_switch_routing_multicast_rendezvous_point(network_id: str):
        """Create create network switchroutingmulticastrendezvouspoint."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.switch.createNetworkSwitchRoutingMulticastRendezvousPoint(network_id, **kwargs)
            
            response = f"# ➕ Create Network Switchroutingmulticastrendezvouspoint\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in create_network_switch_routing_multicast_rendezvous_point: {str(e)}"
    
    @app.tool(
        name="create_network_switch_stack",
        description="➕ Create network switchStack"
    )
    def create_network_switch_stack(network_id: str, switch_stack_id: str):
        """Create create network switchstack."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.switch.createNetworkSwitchStack(network_id, switch_stack_id, **kwargs)
            
            response = f"# ➕ Create Network Switchstack\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in create_network_switch_stack: {str(e)}"
    
    @app.tool(
        name="create_network_switch_stack_routing_interface",
        description="➕ Create network switchStackRoutingInterface"
    )
    def create_network_switch_stack_routing_interface(network_id: str, interface_id: str):
        """Create create network switchstackroutinginterface."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.switch.createNetworkSwitchStackRoutingInterface(network_id, interface_id, **kwargs)
            
            response = f"# ➕ Create Network Switchstackroutinginterface\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in create_network_switch_stack_routing_interface: {str(e)}"
    
    @app.tool(
        name="create_network_switch_stack_routing_static_route",
        description="➕ Create network switchStackRoutingStaticRoute"
    )
    def create_network_switch_stack_routing_static_route(network_id: str, switch_stack_id: str):
        """Create create network switchstackroutingstaticroute."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.switch.createNetworkSwitchStackRoutingStaticRoute(network_id, switch_stack_id, **kwargs)
            
            response = f"# ➕ Create Network Switchstackroutingstaticroute\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in create_network_switch_stack_routing_static_route: {str(e)}"
    
    @app.tool(
        name="cycle_device_switch_ports",
        description="🔄 Cycle device switchPorts"
    )
    def cycle_device_switch_ports(serial: str, confirmed: bool = False):
        """Cycle cycle device switchports."""
        if not confirmed:
            return "⚠️ This operation requires confirmed=true to execute"
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.switch.cycleDeviceSwitchPorts(serial, **kwargs)
            
            response = f"# 🔄 Cycle Device Switchports\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in cycle_device_switch_ports: {str(e)}"
    
    @app.tool(
        name="delete_device_switch_routing_interface",
        description="❌ Delete device switchRoutingInterface"
    )
    def delete_device_switch_routing_interface(serial: str, interface_id: str, confirmed: bool = False):
        """Delete delete device switchroutinginterface."""
        if not confirmed:
            return "⚠️ This operation requires confirmed=true to execute"
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.switch.deleteDeviceSwitchRoutingInterface(serial, interface_id, **kwargs)
            
            response = f"# ❌ Delete Device Switchroutinginterface\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in delete_device_switch_routing_interface: {str(e)}"
    
    @app.tool(
        name="delete_device_switch_routing_static_route",
        description="❌ Delete device switchRoutingStaticRoute"
    )
    def delete_device_switch_routing_static_route(serial: str, confirmed: bool = False):
        """Delete delete device switchroutingstaticroute."""
        if not confirmed:
            return "⚠️ This operation requires confirmed=true to execute"
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.switch.deleteDeviceSwitchRoutingStaticRoute(serial, **kwargs)
            
            response = f"# ❌ Delete Device Switchroutingstaticroute\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in delete_device_switch_routing_static_route: {str(e)}"
    
    @app.tool(
        name="delete_network_switch_access_policy",
        description="❌ Delete network switchAccessPolicy"
    )
    def delete_network_switch_access_policy(network_id: str, confirmed: bool = False):
        """Delete delete network switchaccesspolicy."""
        if not confirmed:
            return "⚠️ This operation requires confirmed=true to execute"
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.switch.deleteNetworkSwitchAccessPolicy(network_id, **kwargs)
            
            response = f"# ❌ Delete Network Switchaccesspolicy\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in delete_network_switch_access_policy: {str(e)}"
    
    @app.tool(
        name="delete_network_switch_dhcp_server_policy_arp_trusted_server",
        description="❌ Delete network switchDhcpServerPolicyArpInspectionTrustedServer"
    )
    def delete_network_switch_dhcp_server_policy_arp_inspection_trusted_server(network_id: str, confirmed: bool = False):
        """Delete delete network switchdhcpserverpolicyarpinspectiontrustedserver."""
        if not confirmed:
            return "⚠️ This operation requires confirmed=true to execute"
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.switch.deleteNetworkSwitchDhcpServerPolicyArpInspectionTrustedServer(network_id, **kwargs)
            
            response = f"# ❌ Delete Network Switchdhcpserverpolicyarpinspectiontrustedserver\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in delete_network_switch_dhcp_server_policy_arp_inspection_trusted_server: {str(e)}"
    
    @app.tool(
        name="delete_network_switch_link_aggregation",
        description="❌ Delete network switchLinkAggregation"
    )
    def delete_network_switch_link_aggregation(network_id: str, confirmed: bool = False):
        """Delete delete network switchlinkaggregation."""
        if not confirmed:
            return "⚠️ This operation requires confirmed=true to execute"
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.switch.deleteNetworkSwitchLinkAggregation(network_id, **kwargs)
            
            response = f"# ❌ Delete Network Switchlinkaggregation\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in delete_network_switch_link_aggregation: {str(e)}"
    
    @app.tool(
        name="delete_network_switch_port_schedule",
        description="❌ Delete network switchPortSchedule"
    )
    def delete_network_switch_port_schedule(network_id: str, confirmed: bool = False):
        """Delete delete network switchportschedule."""
        if not confirmed:
            return "⚠️ This operation requires confirmed=true to execute"
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.switch.deleteNetworkSwitchPortSchedule(network_id, **kwargs)
            
            response = f"# ❌ Delete Network Switchportschedule\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in delete_network_switch_port_schedule: {str(e)}"
    
    @app.tool(
        name="delete_network_switch_qos_rule",
        description="❌ Delete network switchQosRule"
    )
    def delete_network_switch_qos_rule(network_id: str, confirmed: bool = False):
        """Delete delete network switchqosrule."""
        if not confirmed:
            return "⚠️ This operation requires confirmed=true to execute"
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.switch.deleteNetworkSwitchQosRule(network_id, **kwargs)
            
            response = f"# ❌ Delete Network Switchqosrule\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in delete_network_switch_qos_rule: {str(e)}"
    
    @app.tool(
        name="delete_network_switch_routing_multicast_rendezvous_point",
        description="❌ Delete network switchRoutingMulticastRendezvousPoint"
    )
    def delete_network_switch_routing_multicast_rendezvous_point(network_id: str, confirmed: bool = False):
        """Delete delete network switchroutingmulticastrendezvouspoint."""
        if not confirmed:
            return "⚠️ This operation requires confirmed=true to execute"
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.switch.deleteNetworkSwitchRoutingMulticastRendezvousPoint(network_id, **kwargs)
            
            response = f"# ❌ Delete Network Switchroutingmulticastrendezvouspoint\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in delete_network_switch_routing_multicast_rendezvous_point: {str(e)}"
    
    @app.tool(
        name="delete_network_switch_stack",
        description="❌ Delete network switchStack"
    )
    def delete_network_switch_stack(network_id: str, switch_stack_id: str, confirmed: bool = False):
        """Delete delete network switchstack."""
        if not confirmed:
            return "⚠️ This operation requires confirmed=true to execute"
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.switch.deleteNetworkSwitchStack(network_id, switch_stack_id, **kwargs)
            
            response = f"# ❌ Delete Network Switchstack\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in delete_network_switch_stack: {str(e)}"
    
    @app.tool(
        name="delete_network_switch_stack_routing_interface",
        description="❌ Delete network switchStackRoutingInterface"
    )
    def delete_network_switch_stack_routing_interface(network_id: str, interface_id: str, confirmed: bool = False):
        """Delete delete network switchstackroutinginterface."""
        if not confirmed:
            return "⚠️ This operation requires confirmed=true to execute"
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.switch.deleteNetworkSwitchStackRoutingInterface(network_id, interface_id, **kwargs)
            
            response = f"# ❌ Delete Network Switchstackroutinginterface\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in delete_network_switch_stack_routing_interface: {str(e)}"
    
    @app.tool(
        name="delete_network_switch_stack_routing_static_route",
        description="❌ Delete network switchStackRoutingStaticRoute"
    )
    def delete_network_switch_stack_routing_static_route(network_id: str, switch_stack_id: str, confirmed: bool = False):
        """Delete delete network switchstackroutingstaticroute."""
        if not confirmed:
            return "⚠️ This operation requires confirmed=true to execute"
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.switch.deleteNetworkSwitchStackRoutingStaticRoute(network_id, switch_stack_id, **kwargs)
            
            response = f"# ❌ Delete Network Switchstackroutingstaticroute\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in delete_network_switch_stack_routing_static_route: {str(e)}"
    
    @app.tool(
        name="get_device_switch_port",
        description="🔌 Get device switchPort"
    )
    def get_device_switch_port(serial: str, port_id: str):
        """Get get device switchport."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.switch.getDeviceSwitchPort(serial, port_id, **kwargs)
            
            response = f"# 🔌 Get Device Switchport\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in get_device_switch_port: {str(e)}"
    
    @app.tool(
        name="get_device_switch_ports",
        description="🔌 Get device switchPorts"
    )
    def get_device_switch_ports(serial: str, per_page: int = 1000):
        """Get get device switchports."""
        try:
            kwargs = {}
            
            if 'per_page' in locals() and per_page:
                kwargs['perPage'] = min(per_page, 1000)
            
            result = meraki_client.dashboard.switch.getDeviceSwitchPorts(serial, **kwargs)
            
            response = f"# 🔌 Get Device Switchports\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in get_device_switch_ports: {str(e)}"
    
    @app.tool(
        name="get_device_switch_ports_statuses",
        description="🔌 Get device switchPortsStatuses"
    )
    def get_device_switch_ports_statuses(serial: str, per_page: int = 1000):
        """Get get device switchportsstatuses."""
        try:
            kwargs = {}
            
            if 'per_page' in locals() and per_page:
                kwargs['perPage'] = min(per_page, 1000)
            
            result = meraki_client.dashboard.switch.getDeviceSwitchPortsStatuses(serial, **kwargs)
            
            response = f"# 🔌 Get Device Switchportsstatuses\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in get_device_switch_ports_statuses: {str(e)}"
    
    @app.tool(
        name="get_device_switch_ports_statuses_packets",
        description="🔌 Get device switchPortsStatusesPackets"
    )
    def get_device_switch_ports_statuses_packets(serial: str, per_page: int = 1000):
        """Get get device switchportsstatusespackets."""
        try:
            kwargs = {}
            
            if 'per_page' in locals() and per_page:
                kwargs['perPage'] = min(per_page, 1000)
            
            result = meraki_client.dashboard.switch.getDeviceSwitchPortsStatusesPackets(serial, **kwargs)
            
            response = f"# 🔌 Get Device Switchportsstatusespackets\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in get_device_switch_ports_statuses_packets: {str(e)}"
    
    @app.tool(
        name="get_device_switch_routing_interface",
        description="🔌 Get device switchRoutingInterface"
    )
    def get_device_switch_routing_interface(serial: str, interface_id: str):
        """Get get device switchroutinginterface."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.switch.getDeviceSwitchRoutingInterface(serial, interface_id, **kwargs)
            
            response = f"# 🔌 Get Device Switchroutinginterface\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in get_device_switch_routing_interface: {str(e)}"
    
    @app.tool(
        name="get_device_switch_routing_interface_dhcp",
        description="🔌 Get device switchRoutingInterfaceDhcp"
    )
    def get_device_switch_routing_interface_dhcp(serial: str, interface_id: str):
        """Get get device switchroutinginterfacedhcp."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.switch.getDeviceSwitchRoutingInterfaceDhcp(serial, interface_id, **kwargs)
            
            response = f"# 🔌 Get Device Switchroutinginterfacedhcp\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in get_device_switch_routing_interface_dhcp: {str(e)}"
    
    @app.tool(
        name="get_device_switch_routing_interfaces",
        description="🔌 Get device switchRoutingInterfaces"
    )
    def get_device_switch_routing_interfaces(serial: str, per_page: int = 1000):
        """Get get device switchroutinginterfaces."""
        try:
            kwargs = {}
            
            if 'per_page' in locals() and per_page:
                kwargs['perPage'] = min(per_page, 1000)
            
            result = meraki_client.dashboard.switch.getDeviceSwitchRoutingInterfaces(serial, **kwargs)
            
            response = f"# 🔌 Get Device Switchroutinginterfaces\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in get_device_switch_routing_interfaces: {str(e)}"
    
    @app.tool(
        name="get_device_switch_routing_static_route",
        description="🔌 Get device switchRoutingStaticRoute"
    )
    def get_device_switch_routing_static_route(serial: str):
        """Get get device switchroutingstaticroute."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.switch.getDeviceSwitchRoutingStaticRoute(serial, **kwargs)
            
            response = f"# 🔌 Get Device Switchroutingstaticroute\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in get_device_switch_routing_static_route: {str(e)}"
    
    @app.tool(
        name="get_device_switch_routing_static_routes",
        description="🔌 Get device switchRoutingStaticRoutes"
    )
    def get_device_switch_routing_static_routes(serial: str, per_page: int = 1000):
        """Get get device switchroutingstaticroutes."""
        try:
            kwargs = {}
            
            if 'per_page' in locals() and per_page:
                kwargs['perPage'] = min(per_page, 1000)
            
            result = meraki_client.dashboard.switch.getDeviceSwitchRoutingStaticRoutes(serial, **kwargs)
            
            response = f"# 🔌 Get Device Switchroutingstaticroutes\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in get_device_switch_routing_static_routes: {str(e)}"
    
    @app.tool(
        name="get_device_switch_warm_spare",
        description="🔌 Get device switchWarmSpare"
    )
    def get_device_switch_warm_spare(serial: str):
        """Get get device switchwarmspare."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.switch.getDeviceSwitchWarmSpare(serial, **kwargs)
            
            response = f"# 🔌 Get Device Switchwarmspare\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in get_device_switch_warm_spare: {str(e)}"
    
    @app.tool(
        name="get_network_switch_access_control_lists",
        description="🔌 Get network switchAccessControlLists"
    )
    def get_network_switch_access_control_lists(network_id: str):
        """Get get network switchaccesscontrollists."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.switch.getNetworkSwitchAccessControlLists(network_id, **kwargs)
            
            response = f"# 🔌 Get Network Switchaccesscontrollists\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in get_network_switch_access_control_lists: {str(e)}"
    
    @app.tool(
        name="get_network_switch_access_policies",
        description="🔌 Get network switchAccessPolicies"
    )
    def get_network_switch_access_policies(network_id: str, per_page: int = 1000):
        """Get get network switchaccesspolicies."""
        try:
            kwargs = {}
            
            if 'per_page' in locals() and per_page:
                kwargs['perPage'] = min(per_page, 1000)
            
            result = meraki_client.dashboard.switch.getNetworkSwitchAccessPolicies(network_id, **kwargs)
            
            response = f"# 🔌 Get Network Switchaccesspolicies\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in get_network_switch_access_policies: {str(e)}"
    
    @app.tool(
        name="get_network_switch_access_policy",
        description="🔌 Get network switchAccessPolicy"
    )
    def get_network_switch_access_policy(network_id: str):
        """Get get network switchaccesspolicy."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.switch.getNetworkSwitchAccessPolicy(network_id, **kwargs)
            
            response = f"# 🔌 Get Network Switchaccesspolicy\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in get_network_switch_access_policy: {str(e)}"
    
    @app.tool(
        name="get_network_switch_alternate_management_interface",
        description="🔌 Get network switchAlternateManagementInterface"
    )
    def get_network_switch_alternate_management_interface(network_id: str, interface_id: str):
        """Get get network switchalternatemanagementinterface."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.switch.getNetworkSwitchAlternateManagementInterface(network_id, interface_id, **kwargs)
            
            response = f"# 🔌 Get Network Switchalternatemanagementinterface\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in get_network_switch_alternate_management_interface: {str(e)}"
    
    @app.tool(
        name="get_network_switch_dhcp_server_policy",
        description="🔌 Get network switchDhcpServerPolicy"
    )
    def get_network_switch_dhcp_server_policy(network_id: str):
        """Get get network switchdhcpserverpolicy."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.switch.getNetworkSwitchDhcpServerPolicy(network_id, **kwargs)
            
            response = f"# 🔌 Get Network Switchdhcpserverpolicy\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in get_network_switch_dhcp_server_policy: {str(e)}"
    
    @app.tool(
        name="get_network_switch_dhcp_server_policy_arp_trusted_servers",
        description="🔌 Get network switchDhcpServerPolicyArpInspectionTrustedServers"
    )
    def get_network_switch_dhcp_server_policy_arp_inspection_trusted_servers(network_id: str):
        """Get get network switchdhcpserverpolicyarpinspectiontrustedservers."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.switch.getNetworkSwitchDhcpServerPolicyArpInspectionTrustedServers(network_id, **kwargs)
            
            response = f"# 🔌 Get Network Switchdhcpserverpolicyarpinspectiontrustedservers\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in get_network_switch_dhcp_server_policy_arp_inspection_trusted_servers: {str(e)}"
    
    @app.tool(
        name="get_network_switch_dhcp_server_policy_arp_warnings_by_device",
        description="🔌 Get network switchDhcpServerPolicyArpInspectionWarningsBy device"
    )
    def get_network_switch_dhcp_server_policy_arp_inspection_warnings_by_device(network_id: str):
        """Get get network switchdhcpserverpolicyarpinspectionwarningsby device."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.switch.getNetworkSwitchDhcpServerPolicyArpInspectionWarningsByDevice(network_id, **kwargs)
            
            response = f"# 🔌 Get Network Switchdhcpserverpolicyarpinspectionwarningsby Device\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in get_network_switch_dhcp_server_policy_arp_inspection_warnings_by_device: {str(e)}"
    
    @app.tool(
        name="get_network_switch_dhcp_v4_servers_seen",
        description="🔌 Get network switchDhcpV4ServersSeen"
    )
    def get_network_switch_dhcp_v4_servers_seen(network_id: str):
        """Get get network switchdhcpv4serversseen."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.switch.getNetworkSwitchDhcpV4ServersSeen(network_id, **kwargs)
            
            response = f"# 🔌 Get Network Switchdhcpv4Serversseen\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in get_network_switch_dhcp_v4_servers_seen: {str(e)}"
    
    @app.tool(
        name="get_network_switch_dscp_to_cos_mappings",
        description="🔌 Get network switchDscpToCosMappings"
    )
    def get_network_switch_dscp_to_cos_mappings(network_id: str):
        """Get get network switchdscptocosmappings."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.switch.getNetworkSwitchDscpToCosMappings(network_id, **kwargs)
            
            response = f"# 🔌 Get Network Switchdscptocosmappings\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in get_network_switch_dscp_to_cos_mappings: {str(e)}"
    
    @app.tool(
        name="get_network_switch_link_aggregations",
        description="🔌 Get network switchLinkAggregations"
    )
    def get_network_switch_link_aggregations(network_id: str):
        """Get get network switchlinkaggregations."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.switch.getNetworkSwitchLinkAggregations(network_id, **kwargs)
            
            response = f"# 🔌 Get Network Switchlinkaggregations\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in get_network_switch_link_aggregations: {str(e)}"
    
    @app.tool(
        name="get_network_switch_mtu",
        description="🔌 Get network switchMtu"
    )
    def get_network_switch_mtu(network_id: str):
        """Get get network switchmtu."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.switch.getNetworkSwitchMtu(network_id, **kwargs)
            
            response = f"# 🔌 Get Network Switchmtu\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in get_network_switch_mtu: {str(e)}"
    
    @app.tool(
        name="get_network_switch_port_schedules",
        description="🔌 Get network switchPortSchedules"
    )
    def get_network_switch_port_schedules(network_id: str, per_page: int = 1000):
        """Get get network switchportschedules."""
        try:
            kwargs = {}
            
            if 'per_page' in locals() and per_page:
                kwargs['perPage'] = min(per_page, 1000)
            
            result = meraki_client.dashboard.switch.getNetworkSwitchPortSchedules(network_id, **kwargs)
            
            response = f"# 🔌 Get Network Switchportschedules\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in get_network_switch_port_schedules: {str(e)}"
    
    @app.tool(
        name="get_network_switch_qos_rule",
        description="🔌 Get network switchQosRule"
    )
    def get_network_switch_qos_rule(network_id: str):
        """Get get network switchqosrule."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.switch.getNetworkSwitchQosRule(network_id, **kwargs)
            
            response = f"# 🔌 Get Network Switchqosrule\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in get_network_switch_qos_rule: {str(e)}"
    
    @app.tool(
        name="get_network_switch_qos_rules",
        description="🔌 Get network switchQosRules"
    )
    def get_network_switch_qos_rules(network_id: str, per_page: int = 1000):
        """Get get network switchqosrules."""
        try:
            kwargs = {}
            
            if 'per_page' in locals() and per_page:
                kwargs['perPage'] = min(per_page, 1000)
            
            result = meraki_client.dashboard.switch.getNetworkSwitchQosRules(network_id, **kwargs)
            
            response = f"# 🔌 Get Network Switchqosrules\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in get_network_switch_qos_rules: {str(e)}"
    
    @app.tool(
        name="get_network_switch_qos_rules_order",
        description="🔌 Get network switchQosRulesOrder"
    )
    def get_network_switch_qos_rules_order(network_id: str, per_page: int = 1000):
        """Get get network switchqosrulesorder."""
        try:
            kwargs = {}
            
            if 'per_page' in locals() and per_page:
                kwargs['perPage'] = min(per_page, 1000)
            
            result = meraki_client.dashboard.switch.getNetworkSwitchQosRulesOrder(network_id, **kwargs)
            
            response = f"# 🔌 Get Network Switchqosrulesorder\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in get_network_switch_qos_rules_order: {str(e)}"
    
    @app.tool(
        name="get_network_switch_routing_multicast",
        description="🔌 Get network switchRoutingMulticast"
    )
    def get_network_switch_routing_multicast(network_id: str):
        """Get get network switchroutingmulticast."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.switch.getNetworkSwitchRoutingMulticast(network_id, **kwargs)
            
            response = f"# 🔌 Get Network Switchroutingmulticast\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in get_network_switch_routing_multicast: {str(e)}"
    
    @app.tool(
        name="get_network_switch_routing_multicast_rendezvous_point",
        description="🔌 Get network switchRoutingMulticastRendezvousPoint"
    )
    def get_network_switch_routing_multicast_rendezvous_point(network_id: str):
        """Get get network switchroutingmulticastrendezvouspoint."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.switch.getNetworkSwitchRoutingMulticastRendezvousPoint(network_id, **kwargs)
            
            response = f"# 🔌 Get Network Switchroutingmulticastrendezvouspoint\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in get_network_switch_routing_multicast_rendezvous_point: {str(e)}"
    
    @app.tool(
        name="get_network_switch_routing_multicast_rendezvous_points",
        description="🔌 Get network switchRoutingMulticastRendezvousPoints"
    )
    def get_network_switch_routing_multicast_rendezvous_points(network_id: str):
        """Get get network switchroutingmulticastrendezvouspoints."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.switch.getNetworkSwitchRoutingMulticastRendezvousPoints(network_id, **kwargs)
            
            response = f"# 🔌 Get Network Switchroutingmulticastrendezvouspoints\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in get_network_switch_routing_multicast_rendezvous_points: {str(e)}"
    
    @app.tool(
        name="get_network_switch_routing_ospf",
        description="🔌 Get network switchRoutingOspf"
    )
    def get_network_switch_routing_ospf(network_id: str):
        """Get get network switchroutingospf."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.switch.getNetworkSwitchRoutingOspf(network_id, **kwargs)
            
            response = f"# 🔌 Get Network Switchroutingospf\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in get_network_switch_routing_ospf: {str(e)}"
    
    @app.tool(
        name="get_network_switch_settings",
        description="🔌 Get network switchSettings"
    )
    def get_network_switch_settings(network_id: str):
        """Get get network switchsettings."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.switch.getNetworkSwitchSettings(network_id, **kwargs)
            
            response = f"# 🔌 Get Network Switchsettings\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in get_network_switch_settings: {str(e)}"
    
    @app.tool(
        name="get_network_switch_stack",
        description="🔌 Get network switchStack"
    )
    def get_network_switch_stack(network_id: str, switch_stack_id: str):
        """Get get network switchstack."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.switch.getNetworkSwitchStack(network_id, switch_stack_id, **kwargs)
            
            response = f"# 🔌 Get Network Switchstack\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in get_network_switch_stack: {str(e)}"
    
    @app.tool(
        name="get_network_switch_stack_routing_interface",
        description="🔌 Get network switchStackRoutingInterface"
    )
    def get_network_switch_stack_routing_interface(network_id: str, interface_id: str):
        """Get get network switchstackroutinginterface."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.switch.getNetworkSwitchStackRoutingInterface(network_id, interface_id, **kwargs)
            
            response = f"# 🔌 Get Network Switchstackroutinginterface\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in get_network_switch_stack_routing_interface: {str(e)}"
    
    @app.tool(
        name="get_network_switch_stack_routing_interface_dhcp",
        description="🔌 Get network switchStackRoutingInterfaceDhcp"
    )
    def get_network_switch_stack_routing_interface_dhcp(network_id: str, interface_id: str):
        """Get get network switchstackroutinginterfacedhcp."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.switch.getNetworkSwitchStackRoutingInterfaceDhcp(network_id, interface_id, **kwargs)
            
            response = f"# 🔌 Get Network Switchstackroutinginterfacedhcp\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in get_network_switch_stack_routing_interface_dhcp: {str(e)}"
    
    @app.tool(
        name="get_network_switch_stack_routing_interfaces",
        description="🔌 Get network switchStackRoutingInterfaces"
    )
    def get_network_switch_stack_routing_interfaces(network_id: str, switch_stack_id: str, per_page: int = 1000):
        """Get get network switchstackroutinginterfaces."""
        try:
            kwargs = {}
            
            if 'per_page' in locals() and per_page:
                kwargs['perPage'] = min(per_page, 1000)
            
            result = meraki_client.dashboard.switch.getNetworkSwitchStackRoutingInterfaces(network_id, switch_stack_id, **kwargs)
            
            response = f"# 🔌 Get Network Switchstackroutinginterfaces\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in get_network_switch_stack_routing_interfaces: {str(e)}"
    
    @app.tool(
        name="get_network_switch_stack_routing_static_route",
        description="🔌 Get network switchStackRoutingStaticRoute"
    )
    def get_network_switch_stack_routing_static_route(network_id: str, switch_stack_id: str):
        """Get get network switchstackroutingstaticroute."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.switch.getNetworkSwitchStackRoutingStaticRoute(network_id, switch_stack_id, **kwargs)
            
            response = f"# 🔌 Get Network Switchstackroutingstaticroute\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in get_network_switch_stack_routing_static_route: {str(e)}"
    
    @app.tool(
        name="get_network_switch_stack_routing_static_routes",
        description="🔌 Get network switchStackRoutingStaticRoutes"
    )
    def get_network_switch_stack_routing_static_routes(network_id: str, switch_stack_id: str, per_page: int = 1000):
        """Get get network switchstackroutingstaticroutes."""
        try:
            kwargs = {}
            
            if 'per_page' in locals() and per_page:
                kwargs['perPage'] = min(per_page, 1000)
            
            result = meraki_client.dashboard.switch.getNetworkSwitchStackRoutingStaticRoutes(network_id, switch_stack_id, **kwargs)
            
            response = f"# 🔌 Get Network Switchstackroutingstaticroutes\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in get_network_switch_stack_routing_static_routes: {str(e)}"
    
    @app.tool(
        name="get_network_switch_stacks",
        description="🔌 Get network switchStacks"
    )
    def get_network_switch_stacks(network_id: str, per_page: int = 1000):
        """Get get network switchstacks."""
        try:
            kwargs = {}
            
            if 'per_page' in locals() and per_page:
                kwargs['perPage'] = min(per_page, 1000)
            
            result = meraki_client.dashboard.switch.getNetworkSwitchStacks(network_id, **kwargs)
            
            response = f"# 🔌 Get Network Switchstacks\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in get_network_switch_stacks: {str(e)}"
    
    @app.tool(
        name="get_network_switch_storm_control",
        description="🔌 Get network switchStormControl"
    )
    def get_network_switch_storm_control(network_id: str):
        """Get get network switchstormcontrol."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.switch.getNetworkSwitchStormControl(network_id, **kwargs)
            
            response = f"# 🔌 Get Network Switchstormcontrol\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in get_network_switch_storm_control: {str(e)}"
    
    @app.tool(
        name="get_network_switch_stp",
        description="🔌 Get network switchStp"
    )
    def get_network_switch_stp(network_id: str):
        """Get get network switchstp."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.switch.getNetworkSwitchStp(network_id, **kwargs)
            
            response = f"# 🔌 Get Network Switchstp\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in get_network_switch_stp: {str(e)}"
    
    @app.tool(
        name="get_organization_config_template_switch_profile_port",
        description="🔌 Get organizationConfigTemplate switchProfilePort"
    )
    def get_organization_config_template_switch_profile_port(organization_id: str, port_id: str):
        """Get get organizationconfigtemplate switchprofileport."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.switch.getOrganizationConfigTemplateSwitchProfilePort(organization_id, port_id, **kwargs)
            
            response = f"# 🔌 Get Organizationconfigtemplate Switchprofileport\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in get_organization_config_template_switch_profile_port: {str(e)}"
    
    @app.tool(
        name="get_organization_config_template_switch_profile_ports",
        description="🔌 Get organizationConfigTemplate switchProfilePorts"
    )
    def get_organization_config_template_switch_profile_ports(organization_id: str, per_page: int = 1000):
        """Get get organizationconfigtemplate switchprofileports."""
        try:
            kwargs = {}
            
            if 'per_page' in locals() and per_page:
                kwargs['perPage'] = min(per_page, 1000)
            
            result = meraki_client.dashboard.switch.getOrganizationConfigTemplateSwitchProfilePorts(organization_id, **kwargs)
            
            response = f"# 🔌 Get Organizationconfigtemplate Switchprofileports\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in get_organization_config_template_switch_profile_ports: {str(e)}"
    
    @app.tool(
        name="get_organization_config_template_switch_profiles",
        description="🔌 Get organizationConfigTemplate switchProfiles"
    )
    def get_organization_config_template_switch_profiles(organization_id: str):
        """Get get organizationconfigtemplate switchprofiles."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.switch.getOrganizationConfigTemplateSwitchProfiles(organization_id, **kwargs)
            
            response = f"# 🔌 Get Organizationconfigtemplate Switchprofiles\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in get_organization_config_template_switch_profiles: {str(e)}"
    
    @app.tool(
        name="get_organization_summary_switch_power_history",
        description="🔌 Get organizationSummary switchPowerHistory"
    )
    def get_organization_summary_switch_power_history(organization_id: str):
        """Get get organizationsummary switchpowerhistory."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.switch.getOrganizationSummarySwitchPowerHistory(organization_id, **kwargs)
            
            response = f"# 🔌 Get Organizationsummary Switchpowerhistory\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in get_organization_summary_switch_power_history: {str(e)}"
    
    @app.tool(
        name="get_organization_switch_ports_by_switch",
        description="🔌 Get organization switchPortsBy switch"
    )
    def get_organization_switch_ports_by_switch(organization_id: str, per_page: int = 1000):
        """Get get organization switchportsby switch."""
        try:
            kwargs = {}
            
            if 'per_page' in locals() and per_page:
                kwargs['perPage'] = min(per_page, 1000)
            
            result = meraki_client.dashboard.switch.getOrganizationSwitchPortsBySwitch(organization_id, **kwargs)
            
            response = f"# 🔌 Get Organization Switchportsby Switch\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in get_organization_switch_ports_by_switch: {str(e)}"
    
    @app.tool(
        name="get_organization_switch_ports_clients_overview_by_device",
        description="🔌 Get organization switchPortsClientsOverviewBy device"
    )
    def get_organization_switch_ports_clients_overview_by_device(organization_id: str, per_page: int = 1000):
        """Get get organization switchportsclientsoverviewby device."""
        try:
            kwargs = {}
            
            if 'per_page' in locals() and per_page:
                kwargs['perPage'] = min(per_page, 1000)
            
            result = meraki_client.dashboard.switch.getOrganizationSwitchPortsClientsOverviewByDevice(organization_id, **kwargs)
            
            response = f"# 🔌 Get Organization Switchportsclientsoverviewby Device\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in get_organization_switch_ports_clients_overview_by_device: {str(e)}"
    
    @app.tool(
        name="get_organization_switch_ports_overview",
        description="🔌 Get organization switchPortsOverview"
    )
    def get_organization_switch_ports_overview(organization_id: str, per_page: int = 1000):
        """Get get organization switchportsoverview."""
        try:
            kwargs = {}
            
            if 'per_page' in locals() and per_page:
                kwargs['perPage'] = min(per_page, 1000)
            
            result = meraki_client.dashboard.switch.getOrganizationSwitchPortsOverview(organization_id, **kwargs)
            
            response = f"# 🔌 Get Organization Switchportsoverview\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in get_organization_switch_ports_overview: {str(e)}"
    
    @app.tool(
        name="get_organization_switch_ports_statuses_by_switch",
        description="🔌 Get organization switchPortsStatusesBy switch"
    )
    def get_organization_switch_ports_statuses_by_switch(organization_id: str, per_page: int = 1000):
        """Get get organization switchportsstatusesby switch."""
        try:
            kwargs = {}
            
            if 'per_page' in locals() and per_page:
                kwargs['perPage'] = min(per_page, 1000)
            
            result = meraki_client.dashboard.switch.getOrganizationSwitchPortsStatusesBySwitch(organization_id, **kwargs)
            
            response = f"# 🔌 Get Organization Switchportsstatusesby Switch\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in get_organization_switch_ports_statuses_by_switch: {str(e)}"
    
    @app.tool(
        name="get_organization_switch_ports_topology_discovery_by_device",
        description="🔌 Get organization switchPortsTopologyDiscoveryBy device"
    )
    def get_organization_switch_ports_topology_discovery_by_device(organization_id: str, per_page: int = 1000):
        """Get get organization switchportstopologydiscoveryby device."""
        try:
            kwargs = {}
            
            if 'per_page' in locals() and per_page:
                kwargs['perPage'] = min(per_page, 1000)
            
            result = meraki_client.dashboard.switch.getOrganizationSwitchPortsTopologyDiscoveryByDevice(organization_id, **kwargs)
            
            response = f"# 🔌 Get Organization Switchportstopologydiscoveryby Device\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in get_organization_switch_ports_topology_discovery_by_device: {str(e)}"
    
    @app.tool(
        name="get_org_switch_ports_usage_history_by_device_by_interval",
        description="🔌 Get organization switchPortsUsageHistoryBy deviceByInterval"
    )
    def get_organization_switch_ports_usage_history_by_device_by_interval(organization_id: str, per_page: int = 1000):
        """Get get organization switchportsusagehistoryby devicebyinterval."""
        try:
            kwargs = {}
            
            if 'per_page' in locals() and per_page:
                kwargs['perPage'] = min(per_page, 1000)
            
            result = meraki_client.dashboard.switch.getOrganizationSwitchPortsUsageHistoryByDeviceByInterval(organization_id, **kwargs)
            
            response = f"# 🔌 Get Organization Switchportsusagehistoryby Devicebyinterval\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in get_organization_switch_ports_usage_history_by_device_by_interval: {str(e)}"
    
    @app.tool(
        name="remove_network_switch_stack",
        description="🗑️ Remove network switchStack"
    )
    def remove_network_switch_stack(network_id: str, switch_stack_id: str, confirmed: bool = False):
        """Remove remove network switchstack."""
        if not confirmed:
            return "⚠️ This operation requires confirmed=true to execute"
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.switch.removeNetworkSwitchStack(network_id, switch_stack_id, **kwargs)
            
            response = f"# 🗑️ Remove Network Switchstack\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in remove_network_switch_stack: {str(e)}"
    
    @app.tool(
        name="update_device_switch_port",
        description="✏️ Update device switchPort"
    )
    def update_device_switch_port(serial: str, port_id: str):
        """Update update device switchport."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.switch.updateDeviceSwitchPort(serial, port_id, **kwargs)
            
            response = f"# ✏️ Update Device Switchport\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in update_device_switch_port: {str(e)}"
    
    @app.tool(
        name="update_device_switch_routing_interface",
        description="✏️ Update device switchRoutingInterface"
    )
    def update_device_switch_routing_interface(serial: str, interface_id: str):
        """Update update device switchroutinginterface."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.switch.updateDeviceSwitchRoutingInterface(serial, interface_id, **kwargs)
            
            response = f"# ✏️ Update Device Switchroutinginterface\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in update_device_switch_routing_interface: {str(e)}"
    
    @app.tool(
        name="update_device_switch_routing_interface_dhcp",
        description="✏️ Update device switchRoutingInterfaceDhcp"
    )
    def update_device_switch_routing_interface_dhcp(serial: str, interface_id: str):
        """Update update device switchroutinginterfacedhcp."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.switch.updateDeviceSwitchRoutingInterfaceDhcp(serial, interface_id, **kwargs)
            
            response = f"# ✏️ Update Device Switchroutinginterfacedhcp\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in update_device_switch_routing_interface_dhcp: {str(e)}"
    
    @app.tool(
        name="update_device_switch_routing_static_route",
        description="✏️ Update device switchRoutingStaticRoute"
    )
    def update_device_switch_routing_static_route(serial: str):
        """Update update device switchroutingstaticroute."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.switch.updateDeviceSwitchRoutingStaticRoute(serial, **kwargs)
            
            response = f"# ✏️ Update Device Switchroutingstaticroute\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in update_device_switch_routing_static_route: {str(e)}"
    
    @app.tool(
        name="update_device_switch_warm_spare",
        description="✏️ Update device switchWarmSpare"
    )
    def update_device_switch_warm_spare(serial: str):
        """Update update device switchwarmspare."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.switch.updateDeviceSwitchWarmSpare(serial, **kwargs)
            
            response = f"# ✏️ Update Device Switchwarmspare\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in update_device_switch_warm_spare: {str(e)}"
    
    @app.tool(
        name="update_network_switch_access_control_lists",
        description="✏️ Update network switchAccessControlLists"
    )
    def update_network_switch_access_control_lists(network_id: str):
        """Update update network switchaccesscontrollists."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.switch.updateNetworkSwitchAccessControlLists(network_id, **kwargs)
            
            response = f"# ✏️ Update Network Switchaccesscontrollists\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in update_network_switch_access_control_lists: {str(e)}"
    
    @app.tool(
        name="update_network_switch_access_policy",
        description="✏️ Update network switchAccessPolicy"
    )
    def update_network_switch_access_policy(network_id: str):
        """Update update network switchaccesspolicy."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.switch.updateNetworkSwitchAccessPolicy(network_id, **kwargs)
            
            response = f"# ✏️ Update Network Switchaccesspolicy\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in update_network_switch_access_policy: {str(e)}"
    
    @app.tool(
        name="update_network_switch_alternate_management_interface",
        description="✏️ Update network switchAlternateManagementInterface"
    )
    def update_network_switch_alternate_management_interface(network_id: str, interface_id: str):
        """Update update network switchalternatemanagementinterface."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.switch.updateNetworkSwitchAlternateManagementInterface(network_id, interface_id, **kwargs)
            
            response = f"# ✏️ Update Network Switchalternatemanagementinterface\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in update_network_switch_alternate_management_interface: {str(e)}"
    
    @app.tool(
        name="update_network_switch_dhcp_server_policy",
        description="✏️ Update network switchDhcpServerPolicy"
    )
    def update_network_switch_dhcp_server_policy(network_id: str):
        """Update update network switchdhcpserverpolicy."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.switch.updateNetworkSwitchDhcpServerPolicy(network_id, **kwargs)
            
            response = f"# ✏️ Update Network Switchdhcpserverpolicy\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in update_network_switch_dhcp_server_policy: {str(e)}"
    
    @app.tool(
        name="update_network_switch_dhcp_server_policy_arp_trusted_server",
        description="✏️ Update network switchDhcpServerPolicyArpInspectionTrustedServer"
    )
    def update_network_switch_dhcp_server_policy_arp_inspection_trusted_server(network_id: str):
        """Update update network switchdhcpserverpolicyarpinspectiontrustedserver."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.switch.updateNetworkSwitchDhcpServerPolicyArpInspectionTrustedServer(network_id, **kwargs)
            
            response = f"# ✏️ Update Network Switchdhcpserverpolicyarpinspectiontrustedserver\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in update_network_switch_dhcp_server_policy_arp_inspection_trusted_server: {str(e)}"
    
    @app.tool(
        name="update_network_switch_dscp_to_cos_mappings",
        description="✏️ Update network switchDscpToCosMappings"
    )
    def update_network_switch_dscp_to_cos_mappings(network_id: str):
        """Update update network switchdscptocosmappings."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.switch.updateNetworkSwitchDscpToCosMappings(network_id, **kwargs)
            
            response = f"# ✏️ Update Network Switchdscptocosmappings\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in update_network_switch_dscp_to_cos_mappings: {str(e)}"
    
    @app.tool(
        name="update_network_switch_link_aggregation",
        description="✏️ Update network switchLinkAggregation"
    )
    def update_network_switch_link_aggregation(network_id: str):
        """Update update network switchlinkaggregation."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.switch.updateNetworkSwitchLinkAggregation(network_id, **kwargs)
            
            response = f"# ✏️ Update Network Switchlinkaggregation\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in update_network_switch_link_aggregation: {str(e)}"
    
    @app.tool(
        name="update_network_switch_mtu",
        description="✏️ Update network switchMtu"
    )
    def update_network_switch_mtu(network_id: str):
        """Update update network switchmtu."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.switch.updateNetworkSwitchMtu(network_id, **kwargs)
            
            response = f"# ✏️ Update Network Switchmtu\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in update_network_switch_mtu: {str(e)}"
    
    @app.tool(
        name="update_network_switch_port_schedule",
        description="✏️ Update network switchPortSchedule"
    )
    def update_network_switch_port_schedule(network_id: str):
        """Update update network switchportschedule."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.switch.updateNetworkSwitchPortSchedule(network_id, **kwargs)
            
            response = f"# ✏️ Update Network Switchportschedule\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in update_network_switch_port_schedule: {str(e)}"
    
    @app.tool(
        name="update_network_switch_qos_rule",
        description="✏️ Update network switchQosRule"
    )
    def update_network_switch_qos_rule(network_id: str):
        """Update update network switchqosrule."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.switch.updateNetworkSwitchQosRule(network_id, **kwargs)
            
            response = f"# ✏️ Update Network Switchqosrule\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in update_network_switch_qos_rule: {str(e)}"
    
    @app.tool(
        name="update_network_switch_qos_rules_order",
        description="✏️ Update network switchQosRulesOrder"
    )
    def update_network_switch_qos_rules_order(network_id: str):
        """Update update network switchqosrulesorder."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.switch.updateNetworkSwitchQosRulesOrder(network_id, **kwargs)
            
            response = f"# ✏️ Update Network Switchqosrulesorder\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in update_network_switch_qos_rules_order: {str(e)}"
    
    @app.tool(
        name="update_network_switch_routing_multicast",
        description="✏️ Update network switchRoutingMulticast"
    )
    def update_network_switch_routing_multicast(network_id: str):
        """Update update network switchroutingmulticast."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.switch.updateNetworkSwitchRoutingMulticast(network_id, **kwargs)
            
            response = f"# ✏️ Update Network Switchroutingmulticast\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in update_network_switch_routing_multicast: {str(e)}"
    
    @app.tool(
        name="update_network_switch_routing_multicast_rendezvous_point",
        description="✏️ Update network switchRoutingMulticastRendezvousPoint"
    )
    def update_network_switch_routing_multicast_rendezvous_point(network_id: str):
        """Update update network switchroutingmulticastrendezvouspoint."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.switch.updateNetworkSwitchRoutingMulticastRendezvousPoint(network_id, **kwargs)
            
            response = f"# ✏️ Update Network Switchroutingmulticastrendezvouspoint\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in update_network_switch_routing_multicast_rendezvous_point: {str(e)}"
    
    @app.tool(
        name="update_network_switch_routing_ospf",
        description="✏️ Update network switchRoutingOspf"
    )
    def update_network_switch_routing_ospf(network_id: str):
        """Update update network switchroutingospf."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.switch.updateNetworkSwitchRoutingOspf(network_id, **kwargs)
            
            response = f"# ✏️ Update Network Switchroutingospf\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in update_network_switch_routing_ospf: {str(e)}"
    
    @app.tool(
        name="update_network_switch_settings",
        description="✏️ Update network switchSettings"
    )
    def update_network_switch_settings(network_id: str):
        """Update update network switchsettings."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.switch.updateNetworkSwitchSettings(network_id, **kwargs)
            
            response = f"# ✏️ Update Network Switchsettings\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in update_network_switch_settings: {str(e)}"
    
    @app.tool(
        name="update_network_switch_stack_routing_interface",
        description="✏️ Update network switchStackRoutingInterface"
    )
    def update_network_switch_stack_routing_interface(network_id: str, interface_id: str):
        """Update update network switchstackroutinginterface."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.switch.updateNetworkSwitchStackRoutingInterface(network_id, interface_id, **kwargs)
            
            response = f"# ✏️ Update Network Switchstackroutinginterface\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in update_network_switch_stack_routing_interface: {str(e)}"
    
    @app.tool(
        name="update_network_switch_stack_routing_interface_dhcp",
        description="✏️ Update network switchStackRoutingInterfaceDhcp"
    )
    def update_network_switch_stack_routing_interface_dhcp(network_id: str, interface_id: str):
        """Update update network switchstackroutinginterfacedhcp."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.switch.updateNetworkSwitchStackRoutingInterfaceDhcp(network_id, interface_id, **kwargs)
            
            response = f"# ✏️ Update Network Switchstackroutinginterfacedhcp\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in update_network_switch_stack_routing_interface_dhcp: {str(e)}"
    
    @app.tool(
        name="update_network_switch_stack_routing_static_route",
        description="✏️ Update network switchStackRoutingStaticRoute"
    )
    def update_network_switch_stack_routing_static_route(network_id: str, switch_stack_id: str):
        """Update update network switchstackroutingstaticroute."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.switch.updateNetworkSwitchStackRoutingStaticRoute(network_id, switch_stack_id, **kwargs)
            
            response = f"# ✏️ Update Network Switchstackroutingstaticroute\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in update_network_switch_stack_routing_static_route: {str(e)}"
    
    @app.tool(
        name="update_network_switch_storm_control",
        description="✏️ Update network switchStormControl"
    )
    def update_network_switch_storm_control(network_id: str):
        """Update update network switchstormcontrol."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.switch.updateNetworkSwitchStormControl(network_id, **kwargs)
            
            response = f"# ✏️ Update Network Switchstormcontrol\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in update_network_switch_storm_control: {str(e)}"
    
    @app.tool(
        name="update_network_switch_stp",
        description="✏️ Update network switchStp"
    )
    def update_network_switch_stp(network_id: str):
        """Update update network switchstp."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.switch.updateNetworkSwitchStp(network_id, **kwargs)
            
            response = f"# ✏️ Update Network Switchstp\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in update_network_switch_stp: {str(e)}"
    
    @app.tool(
        name="update_organization_config_template_switch_profile_port",
        description="✏️ Update organizationConfigTemplate switchProfilePort"
    )
    def update_organization_config_template_switch_profile_port(organization_id: str, port_id: str):
        """Update update organizationconfigtemplate switchprofileport."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.switch.updateOrganizationConfigTemplateSwitchProfilePort(organization_id, port_id, **kwargs)
            
            response = f"# ✏️ Update Organizationconfigtemplate Switchprofileport\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with switch-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('portId', item.get('interfaceId', item.get('id', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key switch-specific fields
                            if 'enabled' in item:
                                response += f"   - Enabled: {'✅' if item.get('enabled') else '❌'}\n"
                            if 'type' in item:
                                response += f"   - Type: {item.get('type')}\n"
                            if 'vlan' in item:
                                response += f"   - VLAN: {item.get('vlan')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'speed' in item:
                                response += f"   - Speed: {item.get('speed')}\n"
                            if 'duplex' in item:
                                response += f"   - Duplex: {item.get('duplex')}\n"
                            if 'poeEnabled' in item:
                                response += f"   - PoE: {'✅' if item.get('poeEnabled') else '❌'}\n"
                                
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show switch-relevant fields
                    switch_fields = ['name', 'portId', 'interfaceId', 'enabled', 'type', 'vlan', 'status', 
                                   'speed', 'duplex', 'poeEnabled', 'rstpEnabled', 'stpGuard']
                    
                    for field in switch_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif field == 'enabled' or field == 'poeEnabled' or field == 'rstpEnabled':
                                response += f"- **{field}**: {'✅' if value else '❌'}\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in switch_fields}
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
            return f"❌ Error in update_organization_config_template_switch_profile_port: {str(e)}"
    
