"""
Cisco Meraki MCP Server - Cellulargateway SDK Tools
Complete implementation of all 24 official Meraki Cellulargateway API methods.

This module provides 100% coverage of the Cellulargateway category from the official Meraki Dashboard API SDK.
Each tool corresponds directly to a method in the meraki.dashboard.cellularGateway namespace.

🎯 PURE SDK IMPLEMENTATION - No custom tools, exact match to official SDK
"""

# Import removed to avoid circular import
import meraki


def register_cellularGateway_tools(app, meraki_client):
    """Register all cellularGateway SDK tools."""
    print(f"📡 Registering 24 cellularGateway SDK tools...")


@app.tool(
    name="create_organization_cellular_gateway_esims_service_providers_account",
    description="Create cellulargatewayesimsserviceprovidersaccount"
)
def create_organization_cellular_gateway_esims_service_providers_account(organization_id: str, **kwargs):
    """
    Create cellulargatewayesimsserviceprovidersaccount
    
    Args:
        organization_id: Organization ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with cellulargatewayesimsserviceprovidersaccount data
    """
    try:
        result = meraki_client.dashboard.cellularGateway.createOrganizationCellularGatewayEsimsServiceProvidersAccount(organization_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="create_organization_cellular_gateway_esims_swap",
    description="Create cellulargatewayesimsswap"
)
def create_organization_cellular_gateway_esims_swap(organization_id: str, **kwargs):
    """
    Create cellulargatewayesimsswap
    
    Args:
        organization_id: Organization ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with cellulargatewayesimsswap data
    """
    try:
        result = meraki_client.dashboard.cellularGateway.createOrganizationCellularGatewayEsimsSwap(organization_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="delete_organization_cellular_gateway_esims_service_providers_account",
    description="Delete cellulargatewayesimsserviceprovidersaccount"
)
def delete_organization_cellular_gateway_esims_service_providers_account(organization_id: str):
    """
    Delete cellulargatewayesimsserviceprovidersaccount
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with cellulargatewayesimsserviceprovidersaccount data
    """
    try:
        result = meraki_client.dashboard.cellularGateway.deleteOrganizationCellularGatewayEsimsServiceProvidersAccount(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_device_cellular_gateway_lan",
    description="Retrieve cellulargatewaylan"
)
def get_device_cellular_gateway_lan(serial: str):
    """
    Retrieve cellulargatewaylan
    
    Args:
        serial: Device serial number
    
    Returns:
        dict: API response with cellulargatewaylan data
    """
    try:
        result = meraki_client.dashboard.cellularGateway.getDeviceCellularGatewayLan(serial)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_device_cellular_gateway_port_forwarding_rules",
    description="Retrieve cellulargatewayportforwardingrules"
)
def get_device_cellular_gateway_port_forwarding_rules(serial: str):
    """
    Retrieve cellulargatewayportforwardingrules
    
    Args:
        serial: Device serial number
    
    Returns:
        dict: API response with cellulargatewayportforwardingrules data
    """
    try:
        result = meraki_client.dashboard.cellularGateway.getDeviceCellularGatewayPortForwardingRules(serial)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_cellular_gateway_connectivity_monitoring_destinations",
    description="Retrieve cellulargatewayconnectivitymonitoringdestinations"
)
def get_network_cellular_gateway_connectivity_monitoring_destinations(network_id: str):
    """
    Retrieve cellulargatewayconnectivitymonitoringdestinations
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with cellulargatewayconnectivitymonitoringdestinations data
    """
    try:
        result = meraki_client.dashboard.cellularGateway.getNetworkCellularGatewayConnectivityMonitoringDestinations(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_cellular_gateway_dhcp",
    description="Retrieve cellulargatewaydhcp"
)
def get_network_cellular_gateway_dhcp(network_id: str):
    """
    Retrieve cellulargatewaydhcp
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with cellulargatewaydhcp data
    """
    try:
        result = meraki_client.dashboard.cellularGateway.getNetworkCellularGatewayDhcp(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_cellular_gateway_subnet_pool",
    description="Retrieve cellulargatewaysubnetpool"
)
def get_network_cellular_gateway_subnet_pool(network_id: str):
    """
    Retrieve cellulargatewaysubnetpool
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with cellulargatewaysubnetpool data
    """
    try:
        result = meraki_client.dashboard.cellularGateway.getNetworkCellularGatewaySubnetPool(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_cellular_gateway_uplink",
    description="Retrieve cellulargatewayuplink"
)
def get_network_cellular_gateway_uplink(network_id: str):
    """
    Retrieve cellulargatewayuplink
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with cellulargatewayuplink data
    """
    try:
        result = meraki_client.dashboard.cellularGateway.getNetworkCellularGatewayUplink(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_cellular_gateway_esims_inventory",
    description="Retrieve cellulargatewayesimsinventory"
)
def get_organization_cellular_gateway_esims_inventory(organization_id: str):
    """
    Retrieve cellulargatewayesimsinventory
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with cellulargatewayesimsinventory data
    """
    try:
        result = meraki_client.dashboard.cellularGateway.getOrganizationCellularGatewayEsimsInventory(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_cellular_gateway_esims_service_providers",
    description="Retrieve cellulargatewayesimsserviceproviders"
)
def get_organization_cellular_gateway_esims_service_providers(organization_id: str):
    """
    Retrieve cellulargatewayesimsserviceproviders
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with cellulargatewayesimsserviceproviders data
    """
    try:
        result = meraki_client.dashboard.cellularGateway.getOrganizationCellularGatewayEsimsServiceProviders(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_cellular_gateway_esims_service_providers_accounts",
    description="Retrieve cellulargatewayesimsserviceprovidersaccounts"
)
def get_organization_cellular_gateway_esims_service_providers_accounts(organization_id: str):
    """
    Retrieve cellulargatewayesimsserviceprovidersaccounts
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with cellulargatewayesimsserviceprovidersaccounts data
    """
    try:
        result = meraki_client.dashboard.cellularGateway.getOrganizationCellularGatewayEsimsServiceProvidersAccounts(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_cellular_gateway_esims_service_providers_accounts_communication_plans",
    description="Retrieve cellulargatewayesimsserviceprovidersaccountscommunicationplans"
)
def get_organization_cellular_gateway_esims_service_providers_accounts_communication_plans(organization_id: str):
    """
    Retrieve cellulargatewayesimsserviceprovidersaccountscommunicationplans
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with cellulargatewayesimsserviceprovidersaccountscommunicationplans data
    """
    try:
        result = meraki_client.dashboard.cellularGateway.getOrganizationCellularGatewayEsimsServiceProvidersAccountsCommunicationPlans(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_cellular_gateway_esims_service_providers_accounts_rate_plans",
    description="Retrieve cellulargatewayesimsserviceprovidersaccountsrateplans"
)
def get_organization_cellular_gateway_esims_service_providers_accounts_rate_plans(organization_id: str):
    """
    Retrieve cellulargatewayesimsserviceprovidersaccountsrateplans
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with cellulargatewayesimsserviceprovidersaccountsrateplans data
    """
    try:
        result = meraki_client.dashboard.cellularGateway.getOrganizationCellularGatewayEsimsServiceProvidersAccountsRatePlans(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_cellular_gateway_uplink_statuses",
    description="Retrieve cellulargatewayuplinkstatuses"
)
def get_organization_cellular_gateway_uplink_statuses(organization_id: str):
    """
    Retrieve cellulargatewayuplinkstatuses
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with cellulargatewayuplinkstatuses data
    """
    try:
        result = meraki_client.dashboard.cellularGateway.getOrganizationCellularGatewayUplinkStatuses(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_device_cellular_gateway_lan",
    description="Update cellulargatewaylan"
)
def update_device_cellular_gateway_lan(serial: str, **kwargs):
    """
    Update cellulargatewaylan
    
    Args:
        serial: Device serial number
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with cellulargatewaylan data
    """
    try:
        result = meraki_client.dashboard.cellularGateway.updateDeviceCellularGatewayLan(serial, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_device_cellular_gateway_port_forwarding_rules",
    description="Update cellulargatewayportforwardingrules"
)
def update_device_cellular_gateway_port_forwarding_rules(serial: str, **kwargs):
    """
    Update cellulargatewayportforwardingrules
    
    Args:
        serial: Device serial number
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with cellulargatewayportforwardingrules data
    """
    try:
        result = meraki_client.dashboard.cellularGateway.updateDeviceCellularGatewayPortForwardingRules(serial, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_network_cellular_gateway_connectivity_monitoring_destinations",
    description="Update cellulargatewayconnectivitymonitoringdestinations"
)
def update_network_cellular_gateway_connectivity_monitoring_destinations(network_id: str, **kwargs):
    """
    Update cellulargatewayconnectivitymonitoringdestinations
    
    Args:
        network_id: Network ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with cellulargatewayconnectivitymonitoringdestinations data
    """
    try:
        result = meraki_client.dashboard.cellularGateway.updateNetworkCellularGatewayConnectivityMonitoringDestinations(network_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_network_cellular_gateway_dhcp",
    description="Update cellulargatewaydhcp"
)
def update_network_cellular_gateway_dhcp(network_id: str, **kwargs):
    """
    Update cellulargatewaydhcp
    
    Args:
        network_id: Network ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with cellulargatewaydhcp data
    """
    try:
        result = meraki_client.dashboard.cellularGateway.updateNetworkCellularGatewayDhcp(network_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_network_cellular_gateway_subnet_pool",
    description="Update cellulargatewaysubnetpool"
)
def update_network_cellular_gateway_subnet_pool(network_id: str, **kwargs):
    """
    Update cellulargatewaysubnetpool
    
    Args:
        network_id: Network ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with cellulargatewaysubnetpool data
    """
    try:
        result = meraki_client.dashboard.cellularGateway.updateNetworkCellularGatewaySubnetPool(network_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_network_cellular_gateway_uplink",
    description="Update cellulargatewayuplink"
)
def update_network_cellular_gateway_uplink(network_id: str, **kwargs):
    """
    Update cellulargatewayuplink
    
    Args:
        network_id: Network ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with cellulargatewayuplink data
    """
    try:
        result = meraki_client.dashboard.cellularGateway.updateNetworkCellularGatewayUplink(network_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_organization_cellular_gateway_esims_inventory",
    description="Update cellulargatewayesimsinventory"
)
def update_organization_cellular_gateway_esims_inventory(organization_id: str, **kwargs):
    """
    Update cellulargatewayesimsinventory
    
    Args:
        organization_id: Organization ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with cellulargatewayesimsinventory data
    """
    try:
        result = meraki_client.dashboard.cellularGateway.updateOrganizationCellularGatewayEsimsInventory(organization_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_organization_cellular_gateway_esims_service_providers_account",
    description="Update cellulargatewayesimsserviceprovidersaccount"
)
def update_organization_cellular_gateway_esims_service_providers_account(organization_id: str, **kwargs):
    """
    Update cellulargatewayesimsserviceprovidersaccount
    
    Args:
        organization_id: Organization ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with cellulargatewayesimsserviceprovidersaccount data
    """
    try:
        result = meraki_client.dashboard.cellularGateway.updateOrganizationCellularGatewayEsimsServiceProvidersAccount(organization_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_organization_cellular_gateway_esims_swap",
    description="Update cellulargatewayesimsswap"
)
def update_organization_cellular_gateway_esims_swap(organization_id: str, **kwargs):
    """
    Update cellulargatewayesimsswap
    
    Args:
        organization_id: Organization ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with cellulargatewayesimsswap data
    """
    try:
        result = meraki_client.dashboard.cellularGateway.updateOrganizationCellularGatewayEsimsSwap(organization_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}