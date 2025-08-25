"""
Additional Cellulargateway endpoints for Cisco Meraki MCP Server.
Auto-generated to achieve 100% API coverage.
"""

# Global variables to store app and meraki client
app = None
meraki_client = None

def format_dict_response(data: dict, resource_name: str) -> str:
    """Format dictionary response."""
    result = f"# {resource_name}\n\n"
    for key, value in data.items():
        if value is not None:
            result += f"**{key}**: {value}\n"
    return result

def format_list_response(data: list, resource_name: str) -> str:
    """Format list response."""
    if not data:
        return f"No {resource_name.lower()} found."
    
    result = f"# {resource_name}\n\n"
    result += f"**Total**: {len(data)}\n\n"
    
    for idx, item in enumerate(data[:10], 1):
        if isinstance(item, dict):
            name = item.get('name', item.get('id', f'Item {idx}'))
            result += f"## {name}\n"
            for key, value in item.items():
                if value is not None and key not in ['name']:
                    result += f"- **{key}**: {value}\n"
            result += "\n"
        else:
            result += f"- {item}\n"
    
    if len(data) > 10:
        result += f"\n... and {len(data) - 10} more items"
    
    return result

def register_cellularGateway_additional_tools(mcp_app, meraki):
    """Register additional cellularGateway tools with the MCP server."""
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    
    # Register all additional tools
    register_cellularGateway_additional_handlers()

def register_cellularGateway_additional_handlers():
    """Register additional cellularGateway tool handlers."""

    @app.tool(
        name="create_org_cellular_esims_provider",
        description="➕ Create organization cellular gateway esims service providers account"
    )
    def create_organization_cellular_gateway_esims_service_providers_account(organization_id: str, **kwargs):
        """Create organization cellular gateway esims service providers account."""
        try:
            result = meraki_client.dashboard.cellularGateway.createOrganizationCellularGatewayEsimsServiceProvidersAccount(
                organization_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Cellular Gateway Esims Service Providers Account")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Cellular Gateway Esims Service Providers Account")
            else:
                return f"✅ Create organization cellular gateway esims service providers account completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="create_organization_cellular_gateway_esims_swap",
        description="➕ Create organization cellular gateway esims swap"
    )
    def create_organization_cellular_gateway_esims_swap(organization_id: str, **kwargs):
        """Create organization cellular gateway esims swap."""
        try:
            result = meraki_client.dashboard.cellularGateway.createOrganizationCellularGatewayEsimsSwap(
                organization_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Cellular Gateway Esims Swap")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Cellular Gateway Esims Swap")
            else:
                return f"✅ Create organization cellular gateway esims swap completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="delete_org_cellular_esims_provider",
        description="🗑️ Delete organization cellular gateway esims service providers account"
    )
    def delete_organization_cellular_gateway_esims_service_providers_account(organization_id: str):
        """Delete organization cellular gateway esims service providers account."""
        try:
            result = meraki_client.dashboard.cellularGateway.deleteOrganizationCellularGatewayEsimsServiceProvidersAccount(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Cellular Gateway Esims Service Providers Account")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Cellular Gateway Esims Service Providers Account")
            else:
                return f"✅ Delete organization cellular gateway esims service providers account completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_network_cellular_monitoring_dest",
        description="📊 Get network cellular gateway connectivity monitoring destinations"
    )
    def get_network_cellular_gateway_connectivity_monitoring_destinations(network_id: str):
        """Get network cellular gateway connectivity monitoring destinations."""
        try:
            result = meraki_client.dashboard.cellularGateway.getNetworkCellularGatewayConnectivityMonitoringDestinations(
                network_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Cellular Gateway Connectivity Monitoring Destinations")
            elif isinstance(result, list):
                return format_list_response(result, "Network Cellular Gateway Connectivity Monitoring Destinations")
            else:
                return f"✅ Get network cellular gateway connectivity monitoring destinations completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_network_cellular_gateway_dhcp",
        description="📊 Get network cellular gateway dhcp"
    )
    def get_network_cellular_gateway_dhcp(network_id: str):
        """Get network cellular gateway dhcp."""
        try:
            result = meraki_client.dashboard.cellularGateway.getNetworkCellularGatewayDhcp(
                network_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Cellular Gateway Dhcp")
            elif isinstance(result, list):
                return format_list_response(result, "Network Cellular Gateway Dhcp")
            else:
                return f"✅ Get network cellular gateway dhcp completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_network_cellular_gateway_subnet_pool",
        description="📊 Get network cellular gateway subnet pool"
    )
    def get_network_cellular_gateway_subnet_pool(network_id: str):
        """Get network cellular gateway subnet pool."""
        try:
            result = meraki_client.dashboard.cellularGateway.getNetworkCellularGatewaySubnetPool(
                network_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Cellular Gateway Subnet Pool")
            elif isinstance(result, list):
                return format_list_response(result, "Network Cellular Gateway Subnet Pool")
            else:
                return f"✅ Get network cellular gateway subnet pool completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_network_cellular_gateway_uplink",
        description="📊 Get network cellular gateway uplink"
    )
    def get_network_cellular_gateway_uplink(network_id: str):
        """Get network cellular gateway uplink."""
        try:
            result = meraki_client.dashboard.cellularGateway.getNetworkCellularGatewayUplink(
                network_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Cellular Gateway Uplink")
            elif isinstance(result, list):
                return format_list_response(result, "Network Cellular Gateway Uplink")
            else:
                return f"✅ Get network cellular gateway uplink completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_org_cellular_esims_providers",
        description="📊 Get organization cellular gateway esims service providers accounts"
    )
    def get_organization_cellular_gateway_esims_service_providers_accounts(organization_id: str):
        """Get organization cellular gateway esims service providers accounts."""
        try:
            result = meraki_client.dashboard.cellularGateway.getOrganizationCellularGatewayEsimsServiceProvidersAccounts(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Cellular Gateway Esims Service Providers Accounts")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Cellular Gateway Esims Service Providers Accounts")
            else:
                return f"✅ Get organization cellular gateway esims service providers accounts completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_org_cellular_esims_comm_plans",
        description="📊 Get organization cellular gateway esims service providers accounts communication plans"
    )
    def get_organization_cellular_gateway_esims_service_providers_accounts_communication_plans(organization_id: str):
        """Get organization cellular gateway esims service providers accounts communication plans."""
        try:
            result = meraki_client.dashboard.cellularGateway.getOrganizationCellularGatewayEsimsServiceProvidersAccountsCommunicationPlans(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Cellular Gateway Esims Service Providers Accounts Communication Plans")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Cellular Gateway Esims Service Providers Accounts Communication Plans")
            else:
                return f"✅ Get organization cellular gateway esims service providers accounts communication plans completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_org_cellular_esims_rate_plans",
        description="📊 Get organization cellular gateway esims service providers accounts rate plans"
    )
    def get_organization_cellular_gateway_esims_service_providers_accounts_rate_plans(organization_id: str):
        """Get organization cellular gateway esims service providers accounts rate plans."""
        try:
            result = meraki_client.dashboard.cellularGateway.getOrganizationCellularGatewayEsimsServiceProvidersAccountsRatePlans(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Cellular Gateway Esims Service Providers Accounts Rate Plans")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Cellular Gateway Esims Service Providers Accounts Rate Plans")
            else:
                return f"✅ Get organization cellular gateway esims service providers accounts rate plans completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_cellular_gateway_uplink_statuses",
        description="📊 Get organization cellular gateway uplink statuses"
    )
    def get_organization_cellular_gateway_uplink_statuses(organization_id: str):
        """Get organization cellular gateway uplink statuses."""
        try:
            result = meraki_client.dashboard.cellularGateway.getOrganizationCellularGatewayUplinkStatuses(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Cellular Gateway Uplink Statuses")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Cellular Gateway Uplink Statuses")
            else:
                return f"✅ Get organization cellular gateway uplink statuses completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="update_device_cellular_gateway_lan",
        description="✏️ Update device cellular gateway lan"
    )
    def update_device_cellular_gateway_lan(serial: str, **kwargs):
        """Update device cellular gateway lan."""
        try:
            result = meraki_client.dashboard.cellularGateway.updateDeviceCellularGatewayLan(
                serial, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Device Cellular Gateway Lan")
            elif isinstance(result, list):
                return format_list_response(result, "Device Cellular Gateway Lan")
            else:
                return f"✅ Update device cellular gateway lan completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="update_device_cellular_gateway_port_forwarding_rules",
        description="✏️ Update device cellular gateway port forwarding rules"
    )
    def update_device_cellular_gateway_port_forwarding_rules(serial: str, **kwargs):
        """Update device cellular gateway port forwarding rules."""
        try:
            result = meraki_client.dashboard.cellularGateway.updateDeviceCellularGatewayPortForwardingRules(
                serial, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Device Cellular Gateway Port Forwarding Rules")
            elif isinstance(result, list):
                return format_list_response(result, "Device Cellular Gateway Port Forwarding Rules")
            else:
                return f"✅ Update device cellular gateway port forwarding rules completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="update_network_cellular_monitoring_dest",
        description="✏️ Update network cellular gateway connectivity monitoring destinations"
    )
    def update_network_cellular_gateway_connectivity_monitoring_destinations(network_id: str, **kwargs):
        """Update network cellular gateway connectivity monitoring destinations."""
        try:
            result = meraki_client.dashboard.cellularGateway.updateNetworkCellularGatewayConnectivityMonitoringDestinations(
                network_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Cellular Gateway Connectivity Monitoring Destinations")
            elif isinstance(result, list):
                return format_list_response(result, "Network Cellular Gateway Connectivity Monitoring Destinations")
            else:
                return f"✅ Update network cellular gateway connectivity monitoring destinations completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="update_network_cellular_gateway_dhcp",
        description="✏️ Update network cellular gateway dhcp"
    )
    def update_network_cellular_gateway_dhcp(network_id: str, **kwargs):
        """Update network cellular gateway dhcp."""
        try:
            result = meraki_client.dashboard.cellularGateway.updateNetworkCellularGatewayDhcp(
                network_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Cellular Gateway Dhcp")
            elif isinstance(result, list):
                return format_list_response(result, "Network Cellular Gateway Dhcp")
            else:
                return f"✅ Update network cellular gateway dhcp completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="update_network_cellular_gateway_subnet_pool",
        description="✏️ Update network cellular gateway subnet pool"
    )
    def update_network_cellular_gateway_subnet_pool(network_id: str, **kwargs):
        """Update network cellular gateway subnet pool."""
        try:
            result = meraki_client.dashboard.cellularGateway.updateNetworkCellularGatewaySubnetPool(
                network_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Cellular Gateway Subnet Pool")
            elif isinstance(result, list):
                return format_list_response(result, "Network Cellular Gateway Subnet Pool")
            else:
                return f"✅ Update network cellular gateway subnet pool completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="update_network_cellular_gateway_uplink",
        description="✏️ Update network cellular gateway uplink"
    )
    def update_network_cellular_gateway_uplink(network_id: str, **kwargs):
        """Update network cellular gateway uplink."""
        try:
            result = meraki_client.dashboard.cellularGateway.updateNetworkCellularGatewayUplink(
                network_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Cellular Gateway Uplink")
            elif isinstance(result, list):
                return format_list_response(result, "Network Cellular Gateway Uplink")
            else:
                return f"✅ Update network cellular gateway uplink completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="update_organization_cellular_gateway_esims_inventory",
        description="✏️ Update organization cellular gateway esims inventory"
    )
    def update_organization_cellular_gateway_esims_inventory(organization_id: str, **kwargs):
        """Update organization cellular gateway esims inventory."""
        try:
            result = meraki_client.dashboard.cellularGateway.updateOrganizationCellularGatewayEsimsInventory(
                organization_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Cellular Gateway Esims Inventory")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Cellular Gateway Esims Inventory")
            else:
                return f"✅ Update organization cellular gateway esims inventory completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="update_org_cellular_esims_provider",
        description="✏️ Update organization cellular gateway esims service providers account"
    )
    def update_organization_cellular_gateway_esims_service_providers_account(organization_id: str, **kwargs):
        """Update organization cellular gateway esims service providers account."""
        try:
            result = meraki_client.dashboard.cellularGateway.updateOrganizationCellularGatewayEsimsServiceProvidersAccount(
                organization_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Cellular Gateway Esims Service Providers Account")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Cellular Gateway Esims Service Providers Account")
            else:
                return f"✅ Update organization cellular gateway esims service providers account completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="update_organization_cellular_gateway_esims_swap",
        description="✏️ Update organization cellular gateway esims swap"
    )
    def update_organization_cellular_gateway_esims_swap(organization_id: str, **kwargs):
        """Update organization cellular gateway esims swap."""
        try:
            result = meraki_client.dashboard.cellularGateway.updateOrganizationCellularGatewayEsimsSwap(
                organization_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Cellular Gateway Esims Swap")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Cellular Gateway Esims Swap")
            else:
                return f"✅ Update organization cellular gateway esims swap completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"
