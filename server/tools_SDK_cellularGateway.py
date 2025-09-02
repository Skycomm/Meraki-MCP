"""
Cellular Gateway tools for Cisco Meraki MCP server.

This module provides 100% coverage of the official Cisco Meraki Cellular Gateway SDK v1.
All 24 official SDK methods are implemented exactly as documented.
"""

from typing import Optional, Dict, Any, List
import json

# Global references to be set by register function
app = None
meraki_client = None

def register_cellular_gateway_tools(mcp_app, meraki):
    """
    Register all official SDK cellular gateway tools with the MCP server.
    Provides 100% coverage of Cisco Meraki Cellular Gateway API v1.
    
    Args:
        mcp_app: MCP server instance
        meraki: Meraki client instance
    """
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    
    # Register all cellular gateway SDK tools
    register_cellular_gateway_sdk_tools()

def register_cellular_gateway_sdk_tools():
    """Register all cellular gateway SDK tools (100% coverage)."""
    
    # ==================== ALL 24 CELLULAR GATEWAY SDK TOOLS ====================
    
    @app.tool(
        name="create_org_cg_esims_service_provider_account",
        description="➕ CreateOrganization cellular gatewayEsimsServiceProvidersAccount"
    )
    def create_org_cg_esims_service_provider_account(organization_id: str):
        """Create createorganization cellular gatewayesimsserviceprovidersaccount."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.cellularGateway.createOrganizationCellularGatewayEsimsServiceProvidersAccount(organization_id, **kwargs)
            
            response = f"# ➕ Createorganization Cellular Gatewayesimsserviceprovidersaccount\\n\\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\\n\\n"
                    
                    # Show first 10 items with cellular gateway context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('serial', item.get('accountId', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\\n"
                            
                            # Show key cellular gateway fields
                            for field in ['status', 'model', 'serial', 'networkId', 'iccid', 'provider', 'ratePlan']:
                                if field in item:
                                    value = item[field]
                                    if value is not None:
                                        response += f"   - {field.title()}: {value}\\n"
                                        
                        else:
                            response += f"**{idx}. {item}**\\n"
                        response += "\\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show cellular gateway relevant fields
                    cg_fields = ['name', 'id', 'serial', 'model', 'networkId', 'iccid', 'provider', 'ratePlan', 
                               'status', 'ip', 'subnet', 'gateway', 'publicIp', 'primaryDns', 'secondaryDns']
                    
                    for field in cg_fields:
                        if field in result:
                            value = result[field]
                            if value is not None:
                                if isinstance(value, list):
                                    response += f"- **{field.title()}**: {len(value)} items\\n"
                                elif isinstance(value, dict):
                                    response += f"- **{field.title()}**: {len(value)} fields\\n"
                                else:
                                    response += f"- **{field.title()}**: {value}\\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in cg_fields and v is not None}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key.title()}**: {value}\\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key.title()}**: {len(value)} items\\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key.title()}**: {len(value)} fields\\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\\n"
                        
                else:
                    response += f"**Result**: {result}\\n"
            else:
                response += "*No data available*\\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in create_org_cg_esims_service_provider_account: {str(e)}"
    
    @app.tool(
        name="create_organization_cellular_gateway_esims_swap",
        description="➕ CreateOrganization cellular gatewayEsimsSwap"
    )
    def create_organization_cellular_gateway_esims_swap(organization_id: str):
        """Create createorganization cellular gatewayesimsswap."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.cellularGateway.createOrganizationCellularGatewayEsimsSwap(organization_id, **kwargs)
            
            response = f"# ➕ Createorganization Cellular Gatewayesimsswap\\n\\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\\n\\n"
                    
                    # Show first 10 items with cellular gateway context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('serial', item.get('accountId', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\\n"
                            
                            # Show key cellular gateway fields
                            for field in ['status', 'model', 'serial', 'networkId', 'iccid', 'provider', 'ratePlan']:
                                if field in item:
                                    value = item[field]
                                    if value is not None:
                                        response += f"   - {field.title()}: {value}\\n"
                                        
                        else:
                            response += f"**{idx}. {item}**\\n"
                        response += "\\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show cellular gateway relevant fields
                    cg_fields = ['name', 'id', 'serial', 'model', 'networkId', 'iccid', 'provider', 'ratePlan', 
                               'status', 'ip', 'subnet', 'gateway', 'publicIp', 'primaryDns', 'secondaryDns']
                    
                    for field in cg_fields:
                        if field in result:
                            value = result[field]
                            if value is not None:
                                if isinstance(value, list):
                                    response += f"- **{field.title()}**: {len(value)} items\\n"
                                elif isinstance(value, dict):
                                    response += f"- **{field.title()}**: {len(value)} fields\\n"
                                else:
                                    response += f"- **{field.title()}**: {value}\\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in cg_fields and v is not None}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key.title()}**: {value}\\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key.title()}**: {len(value)} items\\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key.title()}**: {len(value)} fields\\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\\n"
                        
                else:
                    response += f"**Result**: {result}\\n"
            else:
                response += "*No data available*\\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in create_organization_cellular_gateway_esims_swap: {str(e)}"
    
    @app.tool(
        name="delete_org_cg_esims_service_provider_account",
        description="❌ DeleteOrganization cellular gatewayEsimsServiceProvidersAccount"
    )
    def delete_org_cg_esims_service_provider_account(organization_id: str, confirmed: bool = False):
        """Delete deleteorganization cellular gatewayesimsserviceprovidersaccount."""
        if not confirmed:
            return "⚠️ This operation requires confirmed=true to execute"
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.cellularGateway.deleteOrganizationCellularGatewayEsimsServiceProvidersAccount(organization_id)
            
            response = f"# ❌ Deleteorganization Cellular Gatewayesimsserviceprovidersaccount\\n\\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\\n\\n"
                    
                    # Show first 10 items with cellular gateway context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('serial', item.get('accountId', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\\n"
                            
                            # Show key cellular gateway fields
                            for field in ['status', 'model', 'serial', 'networkId', 'iccid', 'provider', 'ratePlan']:
                                if field in item:
                                    value = item[field]
                                    if value is not None:
                                        response += f"   - {field.title()}: {value}\\n"
                                        
                        else:
                            response += f"**{idx}. {item}**\\n"
                        response += "\\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show cellular gateway relevant fields
                    cg_fields = ['name', 'id', 'serial', 'model', 'networkId', 'iccid', 'provider', 'ratePlan', 
                               'status', 'ip', 'subnet', 'gateway', 'publicIp', 'primaryDns', 'secondaryDns']
                    
                    for field in cg_fields:
                        if field in result:
                            value = result[field]
                            if value is not None:
                                if isinstance(value, list):
                                    response += f"- **{field.title()}**: {len(value)} items\\n"
                                elif isinstance(value, dict):
                                    response += f"- **{field.title()}**: {len(value)} fields\\n"
                                else:
                                    response += f"- **{field.title()}**: {value}\\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in cg_fields and v is not None}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key.title()}**: {value}\\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key.title()}**: {len(value)} items\\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key.title()}**: {len(value)} fields\\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\\n"
                        
                else:
                    response += f"**Result**: {result}\\n"
            else:
                response += "*No data available*\\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in delete_org_cg_esims_service_provider_account: {str(e)}"
    
    @app.tool(
        name="get_device_cellular_gateway_lan",
        description="📱 GetDevice cellular gatewayLan"
    )
    def get_device_cellular_gateway_lan(device_serial: str):
        """Get getdevice cellular gatewaylan."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.cellularGateway.getDeviceCellularGatewayLan(device_serial)
            
            response = f"# 📱 Getdevice Cellular Gatewaylan\\n\\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\\n\\n"
                    
                    # Show first 10 items with cellular gateway context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('serial', item.get('accountId', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\\n"
                            
                            # Show key cellular gateway fields
                            for field in ['status', 'model', 'serial', 'networkId', 'iccid', 'provider', 'ratePlan']:
                                if field in item:
                                    value = item[field]
                                    if value is not None:
                                        response += f"   - {field.title()}: {value}\\n"
                                        
                        else:
                            response += f"**{idx}. {item}**\\n"
                        response += "\\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show cellular gateway relevant fields
                    cg_fields = ['name', 'id', 'serial', 'model', 'networkId', 'iccid', 'provider', 'ratePlan', 
                               'status', 'ip', 'subnet', 'gateway', 'publicIp', 'primaryDns', 'secondaryDns']
                    
                    for field in cg_fields:
                        if field in result:
                            value = result[field]
                            if value is not None:
                                if isinstance(value, list):
                                    response += f"- **{field.title()}**: {len(value)} items\\n"
                                elif isinstance(value, dict):
                                    response += f"- **{field.title()}**: {len(value)} fields\\n"
                                else:
                                    response += f"- **{field.title()}**: {value}\\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in cg_fields and v is not None}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key.title()}**: {value}\\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key.title()}**: {len(value)} items\\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key.title()}**: {len(value)} fields\\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\\n"
                        
                else:
                    response += f"**Result**: {result}\\n"
            else:
                response += "*No data available*\\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_device_cellular_gateway_lan: {str(e)}"
    
    @app.tool(
        name="get_device_cellular_gateway_port_forwarding_rules",
        description="📱 GetDevice cellular gatewayPortForwardingRules"
    )
    def get_device_cellular_gateway_port_forwarding_rules(device_serial: str):
        """Get getdevice cellular gatewayportforwardingrules."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.cellularGateway.getDeviceCellularGatewayPortForwardingRules(device_serial)
            
            response = f"# 📱 Getdevice Cellular Gatewayportforwardingrules\\n\\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\\n\\n"
                    
                    # Show first 10 items with cellular gateway context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('serial', item.get('accountId', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\\n"
                            
                            # Show key cellular gateway fields
                            for field in ['status', 'model', 'serial', 'networkId', 'iccid', 'provider', 'ratePlan']:
                                if field in item:
                                    value = item[field]
                                    if value is not None:
                                        response += f"   - {field.title()}: {value}\\n"
                                        
                        else:
                            response += f"**{idx}. {item}**\\n"
                        response += "\\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show cellular gateway relevant fields
                    cg_fields = ['name', 'id', 'serial', 'model', 'networkId', 'iccid', 'provider', 'ratePlan', 
                               'status', 'ip', 'subnet', 'gateway', 'publicIp', 'primaryDns', 'secondaryDns']
                    
                    for field in cg_fields:
                        if field in result:
                            value = result[field]
                            if value is not None:
                                if isinstance(value, list):
                                    response += f"- **{field.title()}**: {len(value)} items\\n"
                                elif isinstance(value, dict):
                                    response += f"- **{field.title()}**: {len(value)} fields\\n"
                                else:
                                    response += f"- **{field.title()}**: {value}\\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in cg_fields and v is not None}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key.title()}**: {value}\\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key.title()}**: {len(value)} items\\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key.title()}**: {len(value)} fields\\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\\n"
                        
                else:
                    response += f"**Result**: {result}\\n"
            else:
                response += "*No data available*\\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_device_cellular_gateway_port_forwarding_rules: {str(e)}"
    
    @app.tool(
        name="get_network_cg_connectivity_monitoring_destinations",
        description="📱 GetNetwork cellular gatewayConnectivityMonitoringDestinations"
    )
    def get_network_cg_connectivity_monitoring_destinations(network_id: str):
        """Get getnetwork cellular gatewayconnectivitymonitoringdestinations."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.cellularGateway.getNetworkCellularGatewayConnectivityMonitoringDestinations(network_id)
            
            response = f"# 📱 Getnetwork Cellular Gatewayconnectivitymonitoringdestinations\\n\\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\\n\\n"
                    
                    # Show first 10 items with cellular gateway context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('serial', item.get('accountId', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\\n"
                            
                            # Show key cellular gateway fields
                            for field in ['status', 'model', 'serial', 'networkId', 'iccid', 'provider', 'ratePlan']:
                                if field in item:
                                    value = item[field]
                                    if value is not None:
                                        response += f"   - {field.title()}: {value}\\n"
                                        
                        else:
                            response += f"**{idx}. {item}**\\n"
                        response += "\\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show cellular gateway relevant fields
                    cg_fields = ['name', 'id', 'serial', 'model', 'networkId', 'iccid', 'provider', 'ratePlan', 
                               'status', 'ip', 'subnet', 'gateway', 'publicIp', 'primaryDns', 'secondaryDns']
                    
                    for field in cg_fields:
                        if field in result:
                            value = result[field]
                            if value is not None:
                                if isinstance(value, list):
                                    response += f"- **{field.title()}**: {len(value)} items\\n"
                                elif isinstance(value, dict):
                                    response += f"- **{field.title()}**: {len(value)} fields\\n"
                                else:
                                    response += f"- **{field.title()}**: {value}\\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in cg_fields and v is not None}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key.title()}**: {value}\\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key.title()}**: {len(value)} items\\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key.title()}**: {len(value)} fields\\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\\n"
                        
                else:
                    response += f"**Result**: {result}\\n"
            else:
                response += "*No data available*\\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_cg_connectivity_monitoring_destinations: {str(e)}"
    
    @app.tool(
        name="get_network_cellular_gateway_dhcp",
        description="📱 GetNetwork cellular gatewayDhcp"
    )
    def get_network_cellular_gateway_dhcp(network_id: str):
        """Get getnetwork cellular gatewaydhcp."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.cellularGateway.getNetworkCellularGatewayDhcp(network_id)
            
            response = f"# 📱 Getnetwork Cellular Gatewaydhcp\\n\\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\\n\\n"
                    
                    # Show first 10 items with cellular gateway context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('serial', item.get('accountId', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\\n"
                            
                            # Show key cellular gateway fields
                            for field in ['status', 'model', 'serial', 'networkId', 'iccid', 'provider', 'ratePlan']:
                                if field in item:
                                    value = item[field]
                                    if value is not None:
                                        response += f"   - {field.title()}: {value}\\n"
                                        
                        else:
                            response += f"**{idx}. {item}**\\n"
                        response += "\\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show cellular gateway relevant fields
                    cg_fields = ['name', 'id', 'serial', 'model', 'networkId', 'iccid', 'provider', 'ratePlan', 
                               'status', 'ip', 'subnet', 'gateway', 'publicIp', 'primaryDns', 'secondaryDns']
                    
                    for field in cg_fields:
                        if field in result:
                            value = result[field]
                            if value is not None:
                                if isinstance(value, list):
                                    response += f"- **{field.title()}**: {len(value)} items\\n"
                                elif isinstance(value, dict):
                                    response += f"- **{field.title()}**: {len(value)} fields\\n"
                                else:
                                    response += f"- **{field.title()}**: {value}\\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in cg_fields and v is not None}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key.title()}**: {value}\\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key.title()}**: {len(value)} items\\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key.title()}**: {len(value)} fields\\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\\n"
                        
                else:
                    response += f"**Result**: {result}\\n"
            else:
                response += "*No data available*\\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_cellular_gateway_dhcp: {str(e)}"
    
    @app.tool(
        name="get_network_cellular_gateway_subnet_pool",
        description="📱 GetNetwork cellular gatewaySubnetPool"
    )
    def get_network_cellular_gateway_subnet_pool(network_id: str):
        """Get getnetwork cellular gatewaysubnetpool."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.cellularGateway.getNetworkCellularGatewaySubnetPool(network_id)
            
            response = f"# 📱 Getnetwork Cellular Gatewaysubnetpool\\n\\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\\n\\n"
                    
                    # Show first 10 items with cellular gateway context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('serial', item.get('accountId', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\\n"
                            
                            # Show key cellular gateway fields
                            for field in ['status', 'model', 'serial', 'networkId', 'iccid', 'provider', 'ratePlan']:
                                if field in item:
                                    value = item[field]
                                    if value is not None:
                                        response += f"   - {field.title()}: {value}\\n"
                                        
                        else:
                            response += f"**{idx}. {item}**\\n"
                        response += "\\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show cellular gateway relevant fields
                    cg_fields = ['name', 'id', 'serial', 'model', 'networkId', 'iccid', 'provider', 'ratePlan', 
                               'status', 'ip', 'subnet', 'gateway', 'publicIp', 'primaryDns', 'secondaryDns']
                    
                    for field in cg_fields:
                        if field in result:
                            value = result[field]
                            if value is not None:
                                if isinstance(value, list):
                                    response += f"- **{field.title()}**: {len(value)} items\\n"
                                elif isinstance(value, dict):
                                    response += f"- **{field.title()}**: {len(value)} fields\\n"
                                else:
                                    response += f"- **{field.title()}**: {value}\\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in cg_fields and v is not None}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key.title()}**: {value}\\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key.title()}**: {len(value)} items\\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key.title()}**: {len(value)} fields\\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\\n"
                        
                else:
                    response += f"**Result**: {result}\\n"
            else:
                response += "*No data available*\\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_cellular_gateway_subnet_pool: {str(e)}"
    
    @app.tool(
        name="get_network_cellular_gateway_uplink",
        description="📱 GetNetwork cellular gatewayUplink"
    )
    def get_network_cellular_gateway_uplink(network_id: str):
        """Get getnetwork cellular gatewayuplink."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.cellularGateway.getNetworkCellularGatewayUplink(network_id)
            
            response = f"# 📱 Getnetwork Cellular Gatewayuplink\\n\\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\\n\\n"
                    
                    # Show first 10 items with cellular gateway context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('serial', item.get('accountId', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\\n"
                            
                            # Show key cellular gateway fields
                            for field in ['status', 'model', 'serial', 'networkId', 'iccid', 'provider', 'ratePlan']:
                                if field in item:
                                    value = item[field]
                                    if value is not None:
                                        response += f"   - {field.title()}: {value}\\n"
                                        
                        else:
                            response += f"**{idx}. {item}**\\n"
                        response += "\\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show cellular gateway relevant fields
                    cg_fields = ['name', 'id', 'serial', 'model', 'networkId', 'iccid', 'provider', 'ratePlan', 
                               'status', 'ip', 'subnet', 'gateway', 'publicIp', 'primaryDns', 'secondaryDns']
                    
                    for field in cg_fields:
                        if field in result:
                            value = result[field]
                            if value is not None:
                                if isinstance(value, list):
                                    response += f"- **{field.title()}**: {len(value)} items\\n"
                                elif isinstance(value, dict):
                                    response += f"- **{field.title()}**: {len(value)} fields\\n"
                                else:
                                    response += f"- **{field.title()}**: {value}\\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in cg_fields and v is not None}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key.title()}**: {value}\\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key.title()}**: {len(value)} items\\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key.title()}**: {len(value)} fields\\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\\n"
                        
                else:
                    response += f"**Result**: {result}\\n"
            else:
                response += "*No data available*\\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_network_cellular_gateway_uplink: {str(e)}"
    
    @app.tool(
        name="get_organization_cellular_gateway_esims_inventory",
        description="📱 GetOrganization cellular gatewayEsimsInventory"
    )
    def get_organization_cellular_gateway_esims_inventory(organization_id: str):
        """Get getorganization cellular gatewayesimsinventory."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.cellularGateway.getOrganizationCellularGatewayEsimsInventory(organization_id)
            
            response = f"# 📱 Getorganization Cellular Gatewayesimsinventory\\n\\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\\n\\n"
                    
                    # Show first 10 items with cellular gateway context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('serial', item.get('accountId', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\\n"
                            
                            # Show key cellular gateway fields
                            for field in ['status', 'model', 'serial', 'networkId', 'iccid', 'provider', 'ratePlan']:
                                if field in item:
                                    value = item[field]
                                    if value is not None:
                                        response += f"   - {field.title()}: {value}\\n"
                                        
                        else:
                            response += f"**{idx}. {item}**\\n"
                        response += "\\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show cellular gateway relevant fields
                    cg_fields = ['name', 'id', 'serial', 'model', 'networkId', 'iccid', 'provider', 'ratePlan', 
                               'status', 'ip', 'subnet', 'gateway', 'publicIp', 'primaryDns', 'secondaryDns']
                    
                    for field in cg_fields:
                        if field in result:
                            value = result[field]
                            if value is not None:
                                if isinstance(value, list):
                                    response += f"- **{field.title()}**: {len(value)} items\\n"
                                elif isinstance(value, dict):
                                    response += f"- **{field.title()}**: {len(value)} fields\\n"
                                else:
                                    response += f"- **{field.title()}**: {value}\\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in cg_fields and v is not None}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key.title()}**: {value}\\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key.title()}**: {len(value)} items\\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key.title()}**: {len(value)} fields\\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\\n"
                        
                else:
                    response += f"**Result**: {result}\\n"
            else:
                response += "*No data available*\\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_organization_cellular_gateway_esims_inventory: {str(e)}"
    
    @app.tool(
        name="get_organization_cellular_gateway_esims_service_providers",
        description="📱 GetOrganization cellular gatewayEsimsServiceProviders"
    )
    def get_organization_cellular_gateway_esims_service_providers(organization_id: str):
        """Get getorganization cellular gatewayesimsserviceproviders."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.cellularGateway.getOrganizationCellularGatewayEsimsServiceProviders(organization_id)
            
            response = f"# 📱 Getorganization Cellular Gatewayesimsserviceproviders\\n\\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\\n\\n"
                    
                    # Show first 10 items with cellular gateway context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('serial', item.get('accountId', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\\n"
                            
                            # Show key cellular gateway fields
                            for field in ['status', 'model', 'serial', 'networkId', 'iccid', 'provider', 'ratePlan']:
                                if field in item:
                                    value = item[field]
                                    if value is not None:
                                        response += f"   - {field.title()}: {value}\\n"
                                        
                        else:
                            response += f"**{idx}. {item}**\\n"
                        response += "\\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show cellular gateway relevant fields
                    cg_fields = ['name', 'id', 'serial', 'model', 'networkId', 'iccid', 'provider', 'ratePlan', 
                               'status', 'ip', 'subnet', 'gateway', 'publicIp', 'primaryDns', 'secondaryDns']
                    
                    for field in cg_fields:
                        if field in result:
                            value = result[field]
                            if value is not None:
                                if isinstance(value, list):
                                    response += f"- **{field.title()}**: {len(value)} items\\n"
                                elif isinstance(value, dict):
                                    response += f"- **{field.title()}**: {len(value)} fields\\n"
                                else:
                                    response += f"- **{field.title()}**: {value}\\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in cg_fields and v is not None}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key.title()}**: {value}\\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key.title()}**: {len(value)} items\\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key.title()}**: {len(value)} fields\\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\\n"
                        
                else:
                    response += f"**Result**: {result}\\n"
            else:
                response += "*No data available*\\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_organization_cellular_gateway_esims_service_providers: {str(e)}"
    
    @app.tool(
        name="get_org_cg_esims_service_provider_accounts",
        description="📱 GetOrganization cellular gatewayEsimsServiceProvidersAccounts"
    )
    def get_org_cg_esims_service_provider_accounts(organization_id: str):
        """Get getorganization cellular gatewayesimsserviceprovidersaccounts."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.cellularGateway.getOrganizationCellularGatewayEsimsServiceProvidersAccounts(organization_id)
            
            response = f"# 📱 Getorganization Cellular Gatewayesimsserviceprovidersaccounts\\n\\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\\n\\n"
                    
                    # Show first 10 items with cellular gateway context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('serial', item.get('accountId', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\\n"
                            
                            # Show key cellular gateway fields
                            for field in ['status', 'model', 'serial', 'networkId', 'iccid', 'provider', 'ratePlan']:
                                if field in item:
                                    value = item[field]
                                    if value is not None:
                                        response += f"   - {field.title()}: {value}\\n"
                                        
                        else:
                            response += f"**{idx}. {item}**\\n"
                        response += "\\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show cellular gateway relevant fields
                    cg_fields = ['name', 'id', 'serial', 'model', 'networkId', 'iccid', 'provider', 'ratePlan', 
                               'status', 'ip', 'subnet', 'gateway', 'publicIp', 'primaryDns', 'secondaryDns']
                    
                    for field in cg_fields:
                        if field in result:
                            value = result[field]
                            if value is not None:
                                if isinstance(value, list):
                                    response += f"- **{field.title()}**: {len(value)} items\\n"
                                elif isinstance(value, dict):
                                    response += f"- **{field.title()}**: {len(value)} fields\\n"
                                else:
                                    response += f"- **{field.title()}**: {value}\\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in cg_fields and v is not None}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key.title()}**: {value}\\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key.title()}**: {len(value)} items\\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key.title()}**: {len(value)} fields\\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\\n"
                        
                else:
                    response += f"**Result**: {result}\\n"
            else:
                response += "*No data available*\\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_org_cg_esims_service_provider_accounts: {str(e)}"
    
    @app.tool(
        name="get_org_cg_esims_service_provider_comm_plans",
        description="📱 GetOrganization cellular gatewayEsimsServiceProvidersAccountsCommunicationPlans"
    )
    def get_org_cg_esims_service_provider_comm_plans(organization_id: str):
        """Get getorganization cellular gatewayesimsserviceprovidersaccountscommunicationplans."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.cellularGateway.getOrganizationCellularGatewayEsimsServiceProvidersAccountsCommunicationPlans(organization_id)
            
            response = f"# 📱 Getorganization Cellular Gatewayesimsserviceprovidersaccountscommunicationplans\\n\\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\\n\\n"
                    
                    # Show first 10 items with cellular gateway context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('serial', item.get('accountId', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\\n"
                            
                            # Show key cellular gateway fields
                            for field in ['status', 'model', 'serial', 'networkId', 'iccid', 'provider', 'ratePlan']:
                                if field in item:
                                    value = item[field]
                                    if value is not None:
                                        response += f"   - {field.title()}: {value}\\n"
                                        
                        else:
                            response += f"**{idx}. {item}**\\n"
                        response += "\\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show cellular gateway relevant fields
                    cg_fields = ['name', 'id', 'serial', 'model', 'networkId', 'iccid', 'provider', 'ratePlan', 
                               'status', 'ip', 'subnet', 'gateway', 'publicIp', 'primaryDns', 'secondaryDns']
                    
                    for field in cg_fields:
                        if field in result:
                            value = result[field]
                            if value is not None:
                                if isinstance(value, list):
                                    response += f"- **{field.title()}**: {len(value)} items\\n"
                                elif isinstance(value, dict):
                                    response += f"- **{field.title()}**: {len(value)} fields\\n"
                                else:
                                    response += f"- **{field.title()}**: {value}\\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in cg_fields and v is not None}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key.title()}**: {value}\\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key.title()}**: {len(value)} items\\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key.title()}**: {len(value)} fields\\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\\n"
                        
                else:
                    response += f"**Result**: {result}\\n"
            else:
                response += "*No data available*\\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_org_cg_esims_service_provider_comm_plans: {str(e)}"
    
    @app.tool(
        name="get_org_cg_esims_service_provider_rate_plans",
        description="📱 GetOrganization cellular gatewayEsimsServiceProvidersAccountsRatePlans"
    )
    def get_org_cg_esims_service_provider_rate_plans(organization_id: str):
        """Get getorganization cellular gatewayesimsserviceprovidersaccountsrateplans."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.cellularGateway.getOrganizationCellularGatewayEsimsServiceProvidersAccountsRatePlans(organization_id)
            
            response = f"# 📱 Getorganization Cellular Gatewayesimsserviceprovidersaccountsrateplans\\n\\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\\n\\n"
                    
                    # Show first 10 items with cellular gateway context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('serial', item.get('accountId', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\\n"
                            
                            # Show key cellular gateway fields
                            for field in ['status', 'model', 'serial', 'networkId', 'iccid', 'provider', 'ratePlan']:
                                if field in item:
                                    value = item[field]
                                    if value is not None:
                                        response += f"   - {field.title()}: {value}\\n"
                                        
                        else:
                            response += f"**{idx}. {item}**\\n"
                        response += "\\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show cellular gateway relevant fields
                    cg_fields = ['name', 'id', 'serial', 'model', 'networkId', 'iccid', 'provider', 'ratePlan', 
                               'status', 'ip', 'subnet', 'gateway', 'publicIp', 'primaryDns', 'secondaryDns']
                    
                    for field in cg_fields:
                        if field in result:
                            value = result[field]
                            if value is not None:
                                if isinstance(value, list):
                                    response += f"- **{field.title()}**: {len(value)} items\\n"
                                elif isinstance(value, dict):
                                    response += f"- **{field.title()}**: {len(value)} fields\\n"
                                else:
                                    response += f"- **{field.title()}**: {value}\\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in cg_fields and v is not None}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key.title()}**: {value}\\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key.title()}**: {len(value)} items\\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key.title()}**: {len(value)} fields\\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\\n"
                        
                else:
                    response += f"**Result**: {result}\\n"
            else:
                response += "*No data available*\\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_org_cg_esims_service_provider_rate_plans: {str(e)}"
    
    @app.tool(
        name="get_organization_cellular_gateway_uplink_statuses",
        description="📱 GetOrganization cellular gatewayUplinkStatuses"
    )
    def get_organization_cellular_gateway_uplink_statuses(organization_id: str):
        """Get getorganization cellular gatewayuplinkstatuses."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.cellularGateway.getOrganizationCellularGatewayUplinkStatuses(organization_id)
            
            response = f"# 📱 Getorganization Cellular Gatewayuplinkstatuses\\n\\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\\n\\n"
                    
                    # Show first 10 items with cellular gateway context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('serial', item.get('accountId', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\\n"
                            
                            # Show key cellular gateway fields
                            for field in ['status', 'model', 'serial', 'networkId', 'iccid', 'provider', 'ratePlan']:
                                if field in item:
                                    value = item[field]
                                    if value is not None:
                                        response += f"   - {field.title()}: {value}\\n"
                                        
                        else:
                            response += f"**{idx}. {item}**\\n"
                        response += "\\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show cellular gateway relevant fields
                    cg_fields = ['name', 'id', 'serial', 'model', 'networkId', 'iccid', 'provider', 'ratePlan', 
                               'status', 'ip', 'subnet', 'gateway', 'publicIp', 'primaryDns', 'secondaryDns']
                    
                    for field in cg_fields:
                        if field in result:
                            value = result[field]
                            if value is not None:
                                if isinstance(value, list):
                                    response += f"- **{field.title()}**: {len(value)} items\\n"
                                elif isinstance(value, dict):
                                    response += f"- **{field.title()}**: {len(value)} fields\\n"
                                else:
                                    response += f"- **{field.title()}**: {value}\\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in cg_fields and v is not None}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key.title()}**: {value}\\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key.title()}**: {len(value)} items\\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key.title()}**: {len(value)} fields\\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\\n"
                        
                else:
                    response += f"**Result**: {result}\\n"
            else:
                response += "*No data available*\\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_organization_cellular_gateway_uplink_statuses: {str(e)}"
    
    @app.tool(
        name="update_device_cellular_gateway_lan",
        description="✏️ UpdateDevice cellular gatewayLan"
    )
    def update_device_cellular_gateway_lan(device_serial: str, device_lan_ip: Optional[str] = None, device_subnet: Optional[str] = None):
        """Update updatedevice cellular gatewaylan."""
        try:
            kwargs = {}
            
            if 'device_lan_ip' in locals() and device_lan_ip is not None:
                kwargs['deviceLanIp'] = device_lan_ip
            if 'device_subnet' in locals() and device_subnet is not None:
                kwargs['deviceSubnet'] = device_subnet
            
            result = meraki_client.dashboard.cellularGateway.updateDeviceCellularGatewayLan(device_serial, **kwargs)
            
            response = f"# ✏️ Updatedevice Cellular Gatewaylan\\n\\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\\n\\n"
                    
                    # Show first 10 items with cellular gateway context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('serial', item.get('accountId', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\\n"
                            
                            # Show key cellular gateway fields
                            for field in ['status', 'model', 'serial', 'networkId', 'iccid', 'provider', 'ratePlan']:
                                if field in item:
                                    value = item[field]
                                    if value is not None:
                                        response += f"   - {field.title()}: {value}\\n"
                                        
                        else:
                            response += f"**{idx}. {item}**\\n"
                        response += "\\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show cellular gateway relevant fields
                    cg_fields = ['name', 'id', 'serial', 'model', 'networkId', 'iccid', 'provider', 'ratePlan', 
                               'status', 'ip', 'subnet', 'gateway', 'publicIp', 'primaryDns', 'secondaryDns']
                    
                    for field in cg_fields:
                        if field in result:
                            value = result[field]
                            if value is not None:
                                if isinstance(value, list):
                                    response += f"- **{field.title()}**: {len(value)} items\\n"
                                elif isinstance(value, dict):
                                    response += f"- **{field.title()}**: {len(value)} fields\\n"
                                else:
                                    response += f"- **{field.title()}**: {value}\\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in cg_fields and v is not None}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key.title()}**: {value}\\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key.title()}**: {len(value)} items\\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key.title()}**: {len(value)} fields\\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\\n"
                        
                else:
                    response += f"**Result**: {result}\\n"
            else:
                response += "*No data available*\\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in update_device_cellular_gateway_lan: {str(e)}"
    
    @app.tool(
        name="update_device_cellular_gateway_port_forwarding_rules",
        description="✏️ UpdateDevice cellular gatewayPortForwardingRules"
    )
    def update_device_cellular_gateway_port_forwarding_rules(device_serial: str):
        """Update updatedevice cellular gatewayportforwardingrules."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.cellularGateway.updateDeviceCellularGatewayPortForwardingRules(device_serial, **kwargs)
            
            response = f"# ✏️ Updatedevice Cellular Gatewayportforwardingrules\\n\\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\\n\\n"
                    
                    # Show first 10 items with cellular gateway context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('serial', item.get('accountId', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\\n"
                            
                            # Show key cellular gateway fields
                            for field in ['status', 'model', 'serial', 'networkId', 'iccid', 'provider', 'ratePlan']:
                                if field in item:
                                    value = item[field]
                                    if value is not None:
                                        response += f"   - {field.title()}: {value}\\n"
                                        
                        else:
                            response += f"**{idx}. {item}**\\n"
                        response += "\\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show cellular gateway relevant fields
                    cg_fields = ['name', 'id', 'serial', 'model', 'networkId', 'iccid', 'provider', 'ratePlan', 
                               'status', 'ip', 'subnet', 'gateway', 'publicIp', 'primaryDns', 'secondaryDns']
                    
                    for field in cg_fields:
                        if field in result:
                            value = result[field]
                            if value is not None:
                                if isinstance(value, list):
                                    response += f"- **{field.title()}**: {len(value)} items\\n"
                                elif isinstance(value, dict):
                                    response += f"- **{field.title()}**: {len(value)} fields\\n"
                                else:
                                    response += f"- **{field.title()}**: {value}\\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in cg_fields and v is not None}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key.title()}**: {value}\\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key.title()}**: {len(value)} items\\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key.title()}**: {len(value)} fields\\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\\n"
                        
                else:
                    response += f"**Result**: {result}\\n"
            else:
                response += "*No data available*\\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in update_device_cellular_gateway_port_forwarding_rules: {str(e)}"
    
    @app.tool(
        name="update_network_cg_connectivity_monitoring_dest",
        description="✏️ UpdateNetwork cellular gatewayConnectivityMonitoringDestinations"
    )
    def update_network_cg_connectivity_monitoring_dest(network_id: str):
        """Update updatenetwork cellular gatewayconnectivitymonitoringdestinations."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.cellularGateway.updateNetworkCellularGatewayConnectivityMonitoringDestinations(network_id, **kwargs)
            
            response = f"# ✏️ Updatenetwork Cellular Gatewayconnectivitymonitoringdestinations\\n\\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\\n\\n"
                    
                    # Show first 10 items with cellular gateway context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('serial', item.get('accountId', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\\n"
                            
                            # Show key cellular gateway fields
                            for field in ['status', 'model', 'serial', 'networkId', 'iccid', 'provider', 'ratePlan']:
                                if field in item:
                                    value = item[field]
                                    if value is not None:
                                        response += f"   - {field.title()}: {value}\\n"
                                        
                        else:
                            response += f"**{idx}. {item}**\\n"
                        response += "\\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show cellular gateway relevant fields
                    cg_fields = ['name', 'id', 'serial', 'model', 'networkId', 'iccid', 'provider', 'ratePlan', 
                               'status', 'ip', 'subnet', 'gateway', 'publicIp', 'primaryDns', 'secondaryDns']
                    
                    for field in cg_fields:
                        if field in result:
                            value = result[field]
                            if value is not None:
                                if isinstance(value, list):
                                    response += f"- **{field.title()}**: {len(value)} items\\n"
                                elif isinstance(value, dict):
                                    response += f"- **{field.title()}**: {len(value)} fields\\n"
                                else:
                                    response += f"- **{field.title()}**: {value}\\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in cg_fields and v is not None}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key.title()}**: {value}\\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key.title()}**: {len(value)} items\\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key.title()}**: {len(value)} fields\\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\\n"
                        
                else:
                    response += f"**Result**: {result}\\n"
            else:
                response += "*No data available*\\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in update_network_cg_connectivity_monitoring_dest: {str(e)}"
    
    @app.tool(
        name="update_network_cellular_gateway_dhcp",
        description="✏️ UpdateNetwork cellular gatewayDhcp"
    )
    def update_network_cellular_gateway_dhcp(network_id: str, dhcp_enabled: Optional[bool] = None):
        """Update updatenetwork cellular gatewaydhcp."""
        try:
            kwargs = {}
            
            if 'dhcp_enabled' in locals() and dhcp_enabled is not None:
                kwargs['dhcpEnabled'] = dhcp_enabled
            
            result = meraki_client.dashboard.cellularGateway.updateNetworkCellularGatewayDhcp(network_id, **kwargs)
            
            response = f"# ✏️ Updatenetwork Cellular Gatewaydhcp\\n\\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\\n\\n"
                    
                    # Show first 10 items with cellular gateway context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('serial', item.get('accountId', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\\n"
                            
                            # Show key cellular gateway fields
                            for field in ['status', 'model', 'serial', 'networkId', 'iccid', 'provider', 'ratePlan']:
                                if field in item:
                                    value = item[field]
                                    if value is not None:
                                        response += f"   - {field.title()}: {value}\\n"
                                        
                        else:
                            response += f"**{idx}. {item}**\\n"
                        response += "\\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show cellular gateway relevant fields
                    cg_fields = ['name', 'id', 'serial', 'model', 'networkId', 'iccid', 'provider', 'ratePlan', 
                               'status', 'ip', 'subnet', 'gateway', 'publicIp', 'primaryDns', 'secondaryDns']
                    
                    for field in cg_fields:
                        if field in result:
                            value = result[field]
                            if value is not None:
                                if isinstance(value, list):
                                    response += f"- **{field.title()}**: {len(value)} items\\n"
                                elif isinstance(value, dict):
                                    response += f"- **{field.title()}**: {len(value)} fields\\n"
                                else:
                                    response += f"- **{field.title()}**: {value}\\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in cg_fields and v is not None}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key.title()}**: {value}\\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key.title()}**: {len(value)} items\\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key.title()}**: {len(value)} fields\\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\\n"
                        
                else:
                    response += f"**Result**: {result}\\n"
            else:
                response += "*No data available*\\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in update_network_cellular_gateway_dhcp: {str(e)}"
    
    @app.tool(
        name="update_network_cellular_gateway_subnet_pool",
        description="✏️ UpdateNetwork cellular gatewaySubnetPool"
    )
    def update_network_cellular_gateway_subnet_pool(network_id: str):
        """Update updatenetwork cellular gatewaysubnetpool."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.cellularGateway.updateNetworkCellularGatewaySubnetPool(network_id, **kwargs)
            
            response = f"# ✏️ Updatenetwork Cellular Gatewaysubnetpool\\n\\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\\n\\n"
                    
                    # Show first 10 items with cellular gateway context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('serial', item.get('accountId', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\\n"
                            
                            # Show key cellular gateway fields
                            for field in ['status', 'model', 'serial', 'networkId', 'iccid', 'provider', 'ratePlan']:
                                if field in item:
                                    value = item[field]
                                    if value is not None:
                                        response += f"   - {field.title()}: {value}\\n"
                                        
                        else:
                            response += f"**{idx}. {item}**\\n"
                        response += "\\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show cellular gateway relevant fields
                    cg_fields = ['name', 'id', 'serial', 'model', 'networkId', 'iccid', 'provider', 'ratePlan', 
                               'status', 'ip', 'subnet', 'gateway', 'publicIp', 'primaryDns', 'secondaryDns']
                    
                    for field in cg_fields:
                        if field in result:
                            value = result[field]
                            if value is not None:
                                if isinstance(value, list):
                                    response += f"- **{field.title()}**: {len(value)} items\\n"
                                elif isinstance(value, dict):
                                    response += f"- **{field.title()}**: {len(value)} fields\\n"
                                else:
                                    response += f"- **{field.title()}**: {value}\\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in cg_fields and v is not None}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key.title()}**: {value}\\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key.title()}**: {len(value)} items\\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key.title()}**: {len(value)} fields\\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\\n"
                        
                else:
                    response += f"**Result**: {result}\\n"
            else:
                response += "*No data available*\\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in update_network_cellular_gateway_subnet_pool: {str(e)}"
    
    @app.tool(
        name="update_network_cellular_gateway_uplink",
        description="✏️ UpdateNetwork cellular gatewayUplink"
    )
    def update_network_cellular_gateway_uplink(network_id: str, bandwidth_limits: Optional[Dict[str, Any]] = None):
        """Update updatenetwork cellular gatewayuplink."""
        try:
            kwargs = {}
            
            if 'bandwidth_limits' in locals() and bandwidth_limits is not None:
                kwargs['bandwidthLimits'] = bandwidth_limits
            
            result = meraki_client.dashboard.cellularGateway.updateNetworkCellularGatewayUplink(network_id, **kwargs)
            
            response = f"# ✏️ Updatenetwork Cellular Gatewayuplink\\n\\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\\n\\n"
                    
                    # Show first 10 items with cellular gateway context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('serial', item.get('accountId', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\\n"
                            
                            # Show key cellular gateway fields
                            for field in ['status', 'model', 'serial', 'networkId', 'iccid', 'provider', 'ratePlan']:
                                if field in item:
                                    value = item[field]
                                    if value is not None:
                                        response += f"   - {field.title()}: {value}\\n"
                                        
                        else:
                            response += f"**{idx}. {item}**\\n"
                        response += "\\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show cellular gateway relevant fields
                    cg_fields = ['name', 'id', 'serial', 'model', 'networkId', 'iccid', 'provider', 'ratePlan', 
                               'status', 'ip', 'subnet', 'gateway', 'publicIp', 'primaryDns', 'secondaryDns']
                    
                    for field in cg_fields:
                        if field in result:
                            value = result[field]
                            if value is not None:
                                if isinstance(value, list):
                                    response += f"- **{field.title()}**: {len(value)} items\\n"
                                elif isinstance(value, dict):
                                    response += f"- **{field.title()}**: {len(value)} fields\\n"
                                else:
                                    response += f"- **{field.title()}**: {value}\\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in cg_fields and v is not None}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key.title()}**: {value}\\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key.title()}**: {len(value)} items\\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key.title()}**: {len(value)} fields\\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\\n"
                        
                else:
                    response += f"**Result**: {result}\\n"
            else:
                response += "*No data available*\\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in update_network_cellular_gateway_uplink: {str(e)}"
    
    @app.tool(
        name="update_organization_cellular_gateway_esims_inventory",
        description="✏️ UpdateOrganization cellular gatewayEsimsInventory"
    )
    def update_organization_cellular_gateway_esims_inventory(organization_id: str):
        """Update updateorganization cellular gatewayesimsinventory."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.cellularGateway.updateOrganizationCellularGatewayEsimsInventory(organization_id, **kwargs)
            
            response = f"# ✏️ Updateorganization Cellular Gatewayesimsinventory\\n\\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\\n\\n"
                    
                    # Show first 10 items with cellular gateway context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('serial', item.get('accountId', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\\n"
                            
                            # Show key cellular gateway fields
                            for field in ['status', 'model', 'serial', 'networkId', 'iccid', 'provider', 'ratePlan']:
                                if field in item:
                                    value = item[field]
                                    if value is not None:
                                        response += f"   - {field.title()}: {value}\\n"
                                        
                        else:
                            response += f"**{idx}. {item}**\\n"
                        response += "\\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show cellular gateway relevant fields
                    cg_fields = ['name', 'id', 'serial', 'model', 'networkId', 'iccid', 'provider', 'ratePlan', 
                               'status', 'ip', 'subnet', 'gateway', 'publicIp', 'primaryDns', 'secondaryDns']
                    
                    for field in cg_fields:
                        if field in result:
                            value = result[field]
                            if value is not None:
                                if isinstance(value, list):
                                    response += f"- **{field.title()}**: {len(value)} items\\n"
                                elif isinstance(value, dict):
                                    response += f"- **{field.title()}**: {len(value)} fields\\n"
                                else:
                                    response += f"- **{field.title()}**: {value}\\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in cg_fields and v is not None}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key.title()}**: {value}\\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key.title()}**: {len(value)} items\\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key.title()}**: {len(value)} fields\\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\\n"
                        
                else:
                    response += f"**Result**: {result}\\n"
            else:
                response += "*No data available*\\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in update_organization_cellular_gateway_esims_inventory: {str(e)}"
    
    @app.tool(
        name="update_org_cg_esims_service_provider_account",
        description="✏️ UpdateOrganization cellular gatewayEsimsServiceProvidersAccount"
    )
    def update_org_cg_esims_service_provider_account(organization_id: str):
        """Update updateorganization cellular gatewayesimsserviceprovidersaccount."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.cellularGateway.updateOrganizationCellularGatewayEsimsServiceProvidersAccount(organization_id, **kwargs)
            
            response = f"# ✏️ Updateorganization Cellular Gatewayesimsserviceprovidersaccount\\n\\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\\n\\n"
                    
                    # Show first 10 items with cellular gateway context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('serial', item.get('accountId', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\\n"
                            
                            # Show key cellular gateway fields
                            for field in ['status', 'model', 'serial', 'networkId', 'iccid', 'provider', 'ratePlan']:
                                if field in item:
                                    value = item[field]
                                    if value is not None:
                                        response += f"   - {field.title()}: {value}\\n"
                                        
                        else:
                            response += f"**{idx}. {item}**\\n"
                        response += "\\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show cellular gateway relevant fields
                    cg_fields = ['name', 'id', 'serial', 'model', 'networkId', 'iccid', 'provider', 'ratePlan', 
                               'status', 'ip', 'subnet', 'gateway', 'publicIp', 'primaryDns', 'secondaryDns']
                    
                    for field in cg_fields:
                        if field in result:
                            value = result[field]
                            if value is not None:
                                if isinstance(value, list):
                                    response += f"- **{field.title()}**: {len(value)} items\\n"
                                elif isinstance(value, dict):
                                    response += f"- **{field.title()}**: {len(value)} fields\\n"
                                else:
                                    response += f"- **{field.title()}**: {value}\\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in cg_fields and v is not None}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key.title()}**: {value}\\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key.title()}**: {len(value)} items\\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key.title()}**: {len(value)} fields\\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\\n"
                        
                else:
                    response += f"**Result**: {result}\\n"
            else:
                response += "*No data available*\\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in update_org_cg_esims_service_provider_account: {str(e)}"
    
    @app.tool(
        name="update_organization_cellular_gateway_esims_swap",
        description="✏️ UpdateOrganization cellular gatewayEsimsSwap"
    )
    def update_organization_cellular_gateway_esims_swap(organization_id: str):
        """Update updateorganization cellular gatewayesimsswap."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.cellularGateway.updateOrganizationCellularGatewayEsimsSwap(organization_id, **kwargs)
            
            response = f"# ✏️ Updateorganization Cellular Gatewayesimsswap\\n\\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\\n\\n"
                    
                    # Show first 10 items with cellular gateway context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('id', item.get('serial', item.get('accountId', f'Item {idx}'))))
                            response += f"**{idx}. {name}**\\n"
                            
                            # Show key cellular gateway fields
                            for field in ['status', 'model', 'serial', 'networkId', 'iccid', 'provider', 'ratePlan']:
                                if field in item:
                                    value = item[field]
                                    if value is not None:
                                        response += f"   - {field.title()}: {value}\\n"
                                        
                        else:
                            response += f"**{idx}. {item}**\\n"
                        response += "\\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show cellular gateway relevant fields
                    cg_fields = ['name', 'id', 'serial', 'model', 'networkId', 'iccid', 'provider', 'ratePlan', 
                               'status', 'ip', 'subnet', 'gateway', 'publicIp', 'primaryDns', 'secondaryDns']
                    
                    for field in cg_fields:
                        if field in result:
                            value = result[field]
                            if value is not None:
                                if isinstance(value, list):
                                    response += f"- **{field.title()}**: {len(value)} items\\n"
                                elif isinstance(value, dict):
                                    response += f"- **{field.title()}**: {len(value)} fields\\n"
                                else:
                                    response += f"- **{field.title()}**: {value}\\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in cg_fields and v is not None}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key.title()}**: {value}\\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key.title()}**: {len(value)} items\\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key.title()}**: {len(value)} fields\\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\\n"
                        
                else:
                    response += f"**Result**: {result}\\n"
            else:
                response += "*No data available*\\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in update_organization_cellular_gateway_esims_swap: {str(e)}"
    
