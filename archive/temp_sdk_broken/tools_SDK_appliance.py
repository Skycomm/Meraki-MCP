"""
Cisco Meraki MCP Server - Appliance SDK Tools
Complete implementation of all 130 official Meraki Appliance API methods.

This module provides 100% coverage of the Appliance category from the official Meraki Dashboard API SDK.
Each tool corresponds directly to a method in the meraki.dashboard.appliance namespace.
"""

# Import removed to avoid circular import
import meraki


def register_appliance_tools(app, meraki_client):
    """Register all appliance SDK tools."""
    print(f"🏠 Registering 130 appliance SDK tools...")


@app.tool(
    name="bulk_organization_appliance_dns_local_profiles_assignments_create",
    description="Perform bulk operation on dnslocalprofilesassignmentscreate"
)
def bulk_organization_appliance_dns_local_profiles_assignments_create(organization_id: str):
    """
    Perform bulk operation on dnslocalprofilesassignmentscreate
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with dnslocalprofilesassignmentscreate data
    """
    try:
        result = meraki_client.dashboard.appliance.bulkOrganizationApplianceDnsLocalProfilesAssignmentsCreate(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="create_device_appliance_vmx_authentication_token",
    description="Create a new vmxauthenticationtoken"
)
def create_device_appliance_vmx_authentication_token(serial: str, **kwargs):
    """
    Create a new vmxauthenticationtoken
    
    Args:
        serial: Device serial number
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with vmxauthenticationtoken data
    """
    try:
        result = meraki_client.dashboard.appliance.createDeviceApplianceVmxAuthenticationToken(serial, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="create_network_appliance_prefixes_delegated_static",
    description="Create a new prefixesdelegatedstatic"
)
def create_network_appliance_prefixes_delegated_static(network_id: str, **kwargs):
    """
    Create a new prefixesdelegatedstatic
    
    Args:
        network_id: Network ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with prefixesdelegatedstatic data
    """
    try:
        result = meraki_client.dashboard.appliance.createNetworkAppliancePrefixesDelegatedStatic(network_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="create_network_appliance_rf_profile",
    description="Create a new rfprofile"
)
def create_network_appliance_rf_profile(network_id: str, rf_profile_id: str, **kwargs):
    """
    Create a new rfprofile
    
    Args:
        network_id: Network ID
        rf_profile_id: RF profile ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with rfprofile data
    """
    try:
        result = meraki_client.dashboard.appliance.createNetworkApplianceRfProfile(network_id, rf_profile_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="create_network_appliance_static_route",
    description="Create a new staticroute"
)
def create_network_appliance_static_route(network_id: str, static_route_id: str, **kwargs):
    """
    Create a new staticroute
    
    Args:
        network_id: Network ID
        static_route_id: Static route ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with staticroute data
    """
    try:
        result = meraki_client.dashboard.appliance.createNetworkApplianceStaticRoute(network_id, static_route_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="create_network_appliance_traffic_shaping_custom_performance_class",
    description="Create a new trafficshapingcustomperformanceclass"
)
def create_network_appliance_traffic_shaping_custom_performance_class(network_id: str, custom_performance_class_id: str, **kwargs):
    """
    Create a new trafficshapingcustomperformanceclass
    
    Args:
        network_id: Network ID
        custom_performance_class_id: Custom performance class ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with trafficshapingcustomperformanceclass data
    """
    try:
        result = meraki_client.dashboard.appliance.createNetworkApplianceTrafficShapingCustomPerformanceClass(network_id, custom_performance_class_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="create_network_appliance_vlan",
    description="Create a new vlan"
)
def create_network_appliance_vlan(network_id: str, vlan_id: str, **kwargs):
    """
    Create a new vlan
    
    Args:
        network_id: Network ID
        vlan_id: VLAN ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with vlan data
    """
    try:
        result = meraki_client.dashboard.appliance.createNetworkApplianceVlan(network_id, vlan_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="create_organization_appliance_dns_local_profile",
    description="Create a new dnslocalprofile"
)
def create_organization_appliance_dns_local_profile(organization_id: str, **kwargs):
    """
    Create a new dnslocalprofile
    
    Args:
        organization_id: Organization ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with dnslocalprofile data
    """
    try:
        result = meraki_client.dashboard.appliance.createOrganizationApplianceDnsLocalProfile(organization_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="create_organization_appliance_dns_local_profiles_assignments_bulk_delete",
    description="Create a new dnslocalprofilesassignmentsbulkdelete"
)
def create_organization_appliance_dns_local_profiles_assignments_bulk_delete(organization_id: str, **kwargs):
    """
    Create a new dnslocalprofilesassignmentsbulkdelete
    
    Args:
        organization_id: Organization ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with dnslocalprofilesassignmentsbulkdelete data
    """
    try:
        result = meraki_client.dashboard.appliance.createOrganizationApplianceDnsLocalProfilesAssignmentsBulkDelete(organization_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="create_organization_appliance_dns_local_record",
    description="Create a new dnslocalrecord"
)
def create_organization_appliance_dns_local_record(organization_id: str, **kwargs):
    """
    Create a new dnslocalrecord
    
    Args:
        organization_id: Organization ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with dnslocalrecord data
    """
    try:
        result = meraki_client.dashboard.appliance.createOrganizationApplianceDnsLocalRecord(organization_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="create_organization_appliance_dns_split_profile",
    description="Create a new dnssplitprofile"
)
def create_organization_appliance_dns_split_profile(organization_id: str, **kwargs):
    """
    Create a new dnssplitprofile
    
    Args:
        organization_id: Organization ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with dnssplitprofile data
    """
    try:
        result = meraki_client.dashboard.appliance.createOrganizationApplianceDnsSplitProfile(organization_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="create_organization_appliance_dns_split_profiles_assignments_bulk_create",
    description="Create a new dnssplitprofilesassignmentsbulkcreate"
)
def create_organization_appliance_dns_split_profiles_assignments_bulk_create(organization_id: str, **kwargs):
    """
    Create a new dnssplitprofilesassignmentsbulkcreate
    
    Args:
        organization_id: Organization ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with dnssplitprofilesassignmentsbulkcreate data
    """
    try:
        result = meraki_client.dashboard.appliance.createOrganizationApplianceDnsSplitProfilesAssignmentsBulkCreate(organization_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="create_organization_appliance_dns_split_profiles_assignments_bulk_delete",
    description="Create a new dnssplitprofilesassignmentsbulkdelete"
)
def create_organization_appliance_dns_split_profiles_assignments_bulk_delete(organization_id: str, **kwargs):
    """
    Create a new dnssplitprofilesassignmentsbulkdelete
    
    Args:
        organization_id: Organization ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with dnssplitprofilesassignmentsbulkdelete data
    """
    try:
        result = meraki_client.dashboard.appliance.createOrganizationApplianceDnsSplitProfilesAssignmentsBulkDelete(organization_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="delete_network_appliance_prefixes_delegated_static",
    description="Delete an existing prefixesdelegatedstatic"
)
def delete_network_appliance_prefixes_delegated_static(network_id: str):
    """
    Delete an existing prefixesdelegatedstatic
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with prefixesdelegatedstatic data
    """
    try:
        result = meraki_client.dashboard.appliance.deleteNetworkAppliancePrefixesDelegatedStatic(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="delete_network_appliance_rf_profile",
    description="Delete an existing rfprofile"
)
def delete_network_appliance_rf_profile(network_id: str, rf_profile_id: str):
    """
    Delete an existing rfprofile
    
    Args:
        network_id: Network ID
        rf_profile_id: RF profile ID
    
    Returns:
        dict: API response with rfprofile data
    """
    try:
        result = meraki_client.dashboard.appliance.deleteNetworkApplianceRfProfile(network_id, rf_profile_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="delete_network_appliance_static_route",
    description="Delete an existing staticroute"
)
def delete_network_appliance_static_route(network_id: str, static_route_id: str):
    """
    Delete an existing staticroute
    
    Args:
        network_id: Network ID
        static_route_id: Static route ID
    
    Returns:
        dict: API response with staticroute data
    """
    try:
        result = meraki_client.dashboard.appliance.deleteNetworkApplianceStaticRoute(network_id, static_route_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="delete_network_appliance_traffic_shaping_custom_performance_class",
    description="Delete an existing trafficshapingcustomperformanceclass"
)
def delete_network_appliance_traffic_shaping_custom_performance_class(network_id: str, custom_performance_class_id: str):
    """
    Delete an existing trafficshapingcustomperformanceclass
    
    Args:
        network_id: Network ID
        custom_performance_class_id: Custom performance class ID
    
    Returns:
        dict: API response with trafficshapingcustomperformanceclass data
    """
    try:
        result = meraki_client.dashboard.appliance.deleteNetworkApplianceTrafficShapingCustomPerformanceClass(network_id, custom_performance_class_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="delete_network_appliance_vlan",
    description="Delete an existing vlan"
)
def delete_network_appliance_vlan(network_id: str, vlan_id: str):
    """
    Delete an existing vlan
    
    Args:
        network_id: Network ID
        vlan_id: VLAN ID
    
    Returns:
        dict: API response with vlan data
    """
    try:
        result = meraki_client.dashboard.appliance.deleteNetworkApplianceVlan(network_id, vlan_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="delete_organization_appliance_dns_local_profile",
    description="Delete an existing dnslocalprofile"
)
def delete_organization_appliance_dns_local_profile(organization_id: str):
    """
    Delete an existing dnslocalprofile
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with dnslocalprofile data
    """
    try:
        result = meraki_client.dashboard.appliance.deleteOrganizationApplianceDnsLocalProfile(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="delete_organization_appliance_dns_local_record",
    description="Delete an existing dnslocalrecord"
)
def delete_organization_appliance_dns_local_record(organization_id: str):
    """
    Delete an existing dnslocalrecord
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with dnslocalrecord data
    """
    try:
        result = meraki_client.dashboard.appliance.deleteOrganizationApplianceDnsLocalRecord(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="delete_organization_appliance_dns_split_profile",
    description="Delete an existing dnssplitprofile"
)
def delete_organization_appliance_dns_split_profile(organization_id: str):
    """
    Delete an existing dnssplitprofile
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with dnssplitprofile data
    """
    try:
        result = meraki_client.dashboard.appliance.deleteOrganizationApplianceDnsSplitProfile(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_device_appliance_dhcp_subnets",
    description="Retrieve dhcpsubnets"
)
def get_device_appliance_dhcp_subnets(serial: str):
    """
    Retrieve dhcpsubnets
    
    Args:
        serial: Device serial number
    
    Returns:
        dict: API response with dhcpsubnets data
    """
    try:
        result = meraki_client.dashboard.appliance.getDeviceApplianceDhcpSubnets(serial)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_device_appliance_performance",
    description="Retrieve performance"
)
def get_device_appliance_performance(serial: str, timespan: int = 86400):
    """
    Retrieve performance
    
    Args:
        serial: Device serial number
        timespan: Timespan in seconds (default: 86400)
    
    Returns:
        dict: API response with performance data
    """
    try:
        result = meraki_client.dashboard.appliance.getDeviceAppliancePerformance(serial, timespan=timespan)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_device_appliance_prefixes_delegated",
    description="Retrieve prefixesdelegated"
)
def get_device_appliance_prefixes_delegated(serial: str):
    """
    Retrieve prefixesdelegated
    
    Args:
        serial: Device serial number
    
    Returns:
        dict: API response with prefixesdelegated data
    """
    try:
        result = meraki_client.dashboard.appliance.getDeviceAppliancePrefixesDelegated(serial)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_device_appliance_prefixes_delegated_vlan_assignments",
    description="Retrieve prefixesdelegatedvlanassignments"
)
def get_device_appliance_prefixes_delegated_vlan_assignments(serial: str, vlan_id: str):
    """
    Retrieve prefixesdelegatedvlanassignments
    
    Args:
        serial: Device serial number
        vlan_id: VLAN ID
    
    Returns:
        dict: API response with prefixesdelegatedvlanassignments data
    """
    try:
        result = meraki_client.dashboard.appliance.getDeviceAppliancePrefixesDelegatedVlanAssignments(serial, vlan_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_device_appliance_radio_settings",
    description="Retrieve radiosettings"
)
def get_device_appliance_radio_settings(serial: str):
    """
    Retrieve radiosettings
    
    Args:
        serial: Device serial number
    
    Returns:
        dict: API response with radiosettings data
    """
    try:
        result = meraki_client.dashboard.appliance.getDeviceApplianceRadioSettings(serial)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_device_appliance_uplinks_settings",
    description="Retrieve uplinkssettings"
)
def get_device_appliance_uplinks_settings(serial: str):
    """
    Retrieve uplinkssettings
    
    Args:
        serial: Device serial number
    
    Returns:
        dict: API response with uplinkssettings data
    """
    try:
        result = meraki_client.dashboard.appliance.getDeviceApplianceUplinksSettings(serial)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_appliance_client_security_events",
    description="Retrieve clientsecurityevents"
)
def get_network_appliance_client_security_events(network_id: str):
    """
    Retrieve clientsecurityevents
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with clientsecurityevents data
    """
    try:
        result = meraki_client.dashboard.appliance.getNetworkApplianceClientSecurityEvents(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_appliance_connectivity_monitoring_destinations",
    description="Retrieve connectivitymonitoringdestinations"
)
def get_network_appliance_connectivity_monitoring_destinations(network_id: str):
    """
    Retrieve connectivitymonitoringdestinations
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with connectivitymonitoringdestinations data
    """
    try:
        result = meraki_client.dashboard.appliance.getNetworkApplianceConnectivityMonitoringDestinations(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_appliance_content_filtering",
    description="Retrieve contentfiltering"
)
def get_network_appliance_content_filtering(network_id: str):
    """
    Retrieve contentfiltering
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with contentfiltering data
    """
    try:
        result = meraki_client.dashboard.appliance.getNetworkApplianceContentFiltering(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_appliance_content_filtering_categories",
    description="Retrieve contentfilteringcategories"
)
def get_network_appliance_content_filtering_categories(network_id: str):
    """
    Retrieve contentfilteringcategories
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with contentfilteringcategories data
    """
    try:
        result = meraki_client.dashboard.appliance.getNetworkApplianceContentFilteringCategories(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_appliance_firewall_cellular_firewall_rules",
    description="Retrieve firewallcellularfirewallrules"
)
def get_network_appliance_firewall_cellular_firewall_rules(network_id: str):
    """
    Retrieve firewallcellularfirewallrules
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with firewallcellularfirewallrules data
    """
    try:
        result = meraki_client.dashboard.appliance.getNetworkApplianceFirewallCellularFirewallRules(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_appliance_firewall_firewalled_service",
    description="Retrieve firewallfirewalledservice"
)
def get_network_appliance_firewall_firewalled_service(network_id: str):
    """
    Retrieve firewallfirewalledservice
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with firewallfirewalledservice data
    """
    try:
        result = meraki_client.dashboard.appliance.getNetworkApplianceFirewallFirewalledService(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_appliance_firewall_firewalled_services",
    description="Retrieve firewallfirewalledservices"
)
def get_network_appliance_firewall_firewalled_services(network_id: str):
    """
    Retrieve firewallfirewalledservices
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with firewallfirewalledservices data
    """
    try:
        result = meraki_client.dashboard.appliance.getNetworkApplianceFirewallFirewalledServices(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_appliance_firewall_inbound_cellular_firewall_rules",
    description="Retrieve firewallinboundcellularfirewallrules"
)
def get_network_appliance_firewall_inbound_cellular_firewall_rules(network_id: str):
    """
    Retrieve firewallinboundcellularfirewallrules
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with firewallinboundcellularfirewallrules data
    """
    try:
        result = meraki_client.dashboard.appliance.getNetworkApplianceFirewallInboundCellularFirewallRules(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_appliance_firewall_inbound_firewall_rules",
    description="Retrieve firewallinboundfirewallrules"
)
def get_network_appliance_firewall_inbound_firewall_rules(network_id: str):
    """
    Retrieve firewallinboundfirewallrules
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with firewallinboundfirewallrules data
    """
    try:
        result = meraki_client.dashboard.appliance.getNetworkApplianceFirewallInboundFirewallRules(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_appliance_firewall_l3_firewall_rules",
    description="Retrieve firewalll3firewallrules"
)
def get_network_appliance_firewall_l3_firewall_rules(network_id: str):
    """
    Retrieve firewalll3firewallrules
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with firewalll3firewallrules data
    """
    try:
        result = meraki_client.dashboard.appliance.getNetworkApplianceFirewallL3FirewallRules(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_appliance_firewall_l7_firewall_rules",
    description="Retrieve firewalll7firewallrules"
)
def get_network_appliance_firewall_l7_firewall_rules(network_id: str):
    """
    Retrieve firewalll7firewallrules
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with firewalll7firewallrules data
    """
    try:
        result = meraki_client.dashboard.appliance.getNetworkApplianceFirewallL7FirewallRules(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_appliance_firewall_l7_firewall_rules_application_categories",
    description="Retrieve firewalll7firewallrulesapplicationcategories"
)
def get_network_appliance_firewall_l7_firewall_rules_application_categories(network_id: str):
    """
    Retrieve firewalll7firewallrulesapplicationcategories
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with firewalll7firewallrulesapplicationcategories data
    """
    try:
        result = meraki_client.dashboard.appliance.getNetworkApplianceFirewallL7FirewallRulesApplicationCategories(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_appliance_firewall_one_to_many_nat_rules",
    description="Retrieve firewallonetomanynatrules"
)
def get_network_appliance_firewall_one_to_many_nat_rules(network_id: str):
    """
    Retrieve firewallonetomanynatrules
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with firewallonetomanynatrules data
    """
    try:
        result = meraki_client.dashboard.appliance.getNetworkApplianceFirewallOneToManyNatRules(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_appliance_firewall_one_to_one_nat_rules",
    description="Retrieve firewallonetoonenatrules"
)
def get_network_appliance_firewall_one_to_one_nat_rules(network_id: str):
    """
    Retrieve firewallonetoonenatrules
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with firewallonetoonenatrules data
    """
    try:
        result = meraki_client.dashboard.appliance.getNetworkApplianceFirewallOneToOneNatRules(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_appliance_firewall_port_forwarding_rules",
    description="Retrieve firewallportforwardingrules"
)
def get_network_appliance_firewall_port_forwarding_rules(network_id: str):
    """
    Retrieve firewallportforwardingrules
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with firewallportforwardingrules data
    """
    try:
        result = meraki_client.dashboard.appliance.getNetworkApplianceFirewallPortForwardingRules(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_appliance_firewall_settings",
    description="Retrieve firewallsettings"
)
def get_network_appliance_firewall_settings(network_id: str):
    """
    Retrieve firewallsettings
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with firewallsettings data
    """
    try:
        result = meraki_client.dashboard.appliance.getNetworkApplianceFirewallSettings(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_appliance_port",
    description="Retrieve port"
)
def get_network_appliance_port(network_id: str):
    """
    Retrieve port
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with port data
    """
    try:
        result = meraki_client.dashboard.appliance.getNetworkAppliancePort(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_appliance_ports",
    description="Retrieve ports"
)
def get_network_appliance_ports(network_id: str):
    """
    Retrieve ports
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with ports data
    """
    try:
        result = meraki_client.dashboard.appliance.getNetworkAppliancePorts(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_appliance_prefixes_delegated_static",
    description="Retrieve prefixesdelegatedstatic"
)
def get_network_appliance_prefixes_delegated_static(network_id: str):
    """
    Retrieve prefixesdelegatedstatic
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with prefixesdelegatedstatic data
    """
    try:
        result = meraki_client.dashboard.appliance.getNetworkAppliancePrefixesDelegatedStatic(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_appliance_prefixes_delegated_statics",
    description="Retrieve prefixesdelegatedstatics"
)
def get_network_appliance_prefixes_delegated_statics(network_id: str):
    """
    Retrieve prefixesdelegatedstatics
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with prefixesdelegatedstatics data
    """
    try:
        result = meraki_client.dashboard.appliance.getNetworkAppliancePrefixesDelegatedStatics(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_appliance_rf_profile",
    description="Retrieve rfprofile"
)
def get_network_appliance_rf_profile(network_id: str, rf_profile_id: str):
    """
    Retrieve rfprofile
    
    Args:
        network_id: Network ID
        rf_profile_id: RF profile ID
    
    Returns:
        dict: API response with rfprofile data
    """
    try:
        result = meraki_client.dashboard.appliance.getNetworkApplianceRfProfile(network_id, rf_profile_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_appliance_rf_profiles",
    description="Retrieve rfprofiles"
)
def get_network_appliance_rf_profiles(network_id: str):
    """
    Retrieve rfprofiles
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with rfprofiles data
    """
    try:
        result = meraki_client.dashboard.appliance.getNetworkApplianceRfProfiles(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_appliance_security_events",
    description="Retrieve securityevents"
)
def get_network_appliance_security_events(network_id: str):
    """
    Retrieve securityevents
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with securityevents data
    """
    try:
        result = meraki_client.dashboard.appliance.getNetworkApplianceSecurityEvents(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_appliance_security_intrusion",
    description="Retrieve securityintrusion"
)
def get_network_appliance_security_intrusion(network_id: str):
    """
    Retrieve securityintrusion
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with securityintrusion data
    """
    try:
        result = meraki_client.dashboard.appliance.getNetworkApplianceSecurityIntrusion(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_appliance_security_malware",
    description="Retrieve securitymalware"
)
def get_network_appliance_security_malware(network_id: str):
    """
    Retrieve securitymalware
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with securitymalware data
    """
    try:
        result = meraki_client.dashboard.appliance.getNetworkApplianceSecurityMalware(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_appliance_settings",
    description="Retrieve settings"
)
def get_network_appliance_settings(network_id: str):
    """
    Retrieve settings
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with settings data
    """
    try:
        result = meraki_client.dashboard.appliance.getNetworkApplianceSettings(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_appliance_single_lan",
    description="Retrieve singlelan"
)
def get_network_appliance_single_lan(network_id: str):
    """
    Retrieve singlelan
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with singlelan data
    """
    try:
        result = meraki_client.dashboard.appliance.getNetworkApplianceSingleLan(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_appliance_ssid",
    description="Retrieve ssid"
)
def get_network_appliance_ssid(network_id: str):
    """
    Retrieve ssid
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with ssid data
    """
    try:
        result = meraki_client.dashboard.appliance.getNetworkApplianceSsid(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_appliance_ssids",
    description="Retrieve ssids"
)
def get_network_appliance_ssids(network_id: str):
    """
    Retrieve ssids
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with ssids data
    """
    try:
        result = meraki_client.dashboard.appliance.getNetworkApplianceSsids(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_appliance_static_route",
    description="Retrieve staticroute"
)
def get_network_appliance_static_route(network_id: str, static_route_id: str):
    """
    Retrieve staticroute
    
    Args:
        network_id: Network ID
        static_route_id: Static route ID
    
    Returns:
        dict: API response with staticroute data
    """
    try:
        result = meraki_client.dashboard.appliance.getNetworkApplianceStaticRoute(network_id, static_route_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_appliance_static_routes",
    description="Retrieve staticroutes"
)
def get_network_appliance_static_routes(network_id: str):
    """
    Retrieve staticroutes
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with staticroutes data
    """
    try:
        result = meraki_client.dashboard.appliance.getNetworkApplianceStaticRoutes(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_appliance_traffic_shaping",
    description="Retrieve trafficshaping"
)
def get_network_appliance_traffic_shaping(network_id: str):
    """
    Retrieve trafficshaping
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with trafficshaping data
    """
    try:
        result = meraki_client.dashboard.appliance.getNetworkApplianceTrafficShaping(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_appliance_traffic_shaping_custom_performance_class",
    description="Retrieve trafficshapingcustomperformanceclass"
)
def get_network_appliance_traffic_shaping_custom_performance_class(network_id: str, custom_performance_class_id: str, timespan: int = 86400):
    """
    Retrieve trafficshapingcustomperformanceclass
    
    Args:
        network_id: Network ID
        custom_performance_class_id: Custom performance class ID
        timespan: Timespan in seconds (default: 86400)
    
    Returns:
        dict: API response with trafficshapingcustomperformanceclass data
    """
    try:
        result = meraki_client.dashboard.appliance.getNetworkApplianceTrafficShapingCustomPerformanceClass(network_id, custom_performance_class_id, timespan=timespan)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_appliance_traffic_shaping_custom_performance_classes",
    description="Retrieve trafficshapingcustomperformanceclasses"
)
def get_network_appliance_traffic_shaping_custom_performance_classes(network_id: str, timespan: int = 86400):
    """
    Retrieve trafficshapingcustomperformanceclasses
    
    Args:
        network_id: Network ID
        timespan: Timespan in seconds (default: 86400)
    
    Returns:
        dict: API response with trafficshapingcustomperformanceclasses data
    """
    try:
        result = meraki_client.dashboard.appliance.getNetworkApplianceTrafficShapingCustomPerformanceClasses(network_id, timespan=timespan)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_appliance_traffic_shaping_rules",
    description="Retrieve trafficshapingrules"
)
def get_network_appliance_traffic_shaping_rules(network_id: str):
    """
    Retrieve trafficshapingrules
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with trafficshapingrules data
    """
    try:
        result = meraki_client.dashboard.appliance.getNetworkApplianceTrafficShapingRules(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_appliance_traffic_shaping_uplink_bandwidth",
    description="Retrieve trafficshapinguplinkbandwidth"
)
def get_network_appliance_traffic_shaping_uplink_bandwidth(network_id: str):
    """
    Retrieve trafficshapinguplinkbandwidth
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with trafficshapinguplinkbandwidth data
    """
    try:
        result = meraki_client.dashboard.appliance.getNetworkApplianceTrafficShapingUplinkBandwidth(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_appliance_traffic_shaping_uplink_selection",
    description="Retrieve trafficshapinguplinkselection"
)
def get_network_appliance_traffic_shaping_uplink_selection(network_id: str):
    """
    Retrieve trafficshapinguplinkselection
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with trafficshapinguplinkselection data
    """
    try:
        result = meraki_client.dashboard.appliance.getNetworkApplianceTrafficShapingUplinkSelection(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_appliance_uplinks_usage_history",
    description="Retrieve uplinksusagehistory"
)
def get_network_appliance_uplinks_usage_history(network_id: str, timespan: int = 86400):
    """
    Retrieve uplinksusagehistory
    
    Args:
        network_id: Network ID
        timespan: Timespan in seconds (default: 86400)
    
    Returns:
        dict: API response with uplinksusagehistory data
    """
    try:
        result = meraki_client.dashboard.appliance.getNetworkApplianceUplinksUsageHistory(network_id, timespan=timespan)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_appliance_vlan",
    description="Retrieve vlan"
)
def get_network_appliance_vlan(network_id: str, vlan_id: str):
    """
    Retrieve vlan
    
    Args:
        network_id: Network ID
        vlan_id: VLAN ID
    
    Returns:
        dict: API response with vlan data
    """
    try:
        result = meraki_client.dashboard.appliance.getNetworkApplianceVlan(network_id, vlan_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_appliance_vlans",
    description="Retrieve vlans"
)
def get_network_appliance_vlans(network_id: str):
    """
    Retrieve vlans
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with vlans data
    """
    try:
        result = meraki_client.dashboard.appliance.getNetworkApplianceVlans(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_appliance_vlans_settings",
    description="Retrieve vlanssettings"
)
def get_network_appliance_vlans_settings(network_id: str, vlan_id: str):
    """
    Retrieve vlanssettings
    
    Args:
        network_id: Network ID
        vlan_id: VLAN ID
    
    Returns:
        dict: API response with vlanssettings data
    """
    try:
        result = meraki_client.dashboard.appliance.getNetworkApplianceVlansSettings(network_id, vlan_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_appliance_vpn_bgp",
    description="Retrieve vpnbgp"
)
def get_network_appliance_vpn_bgp(network_id: str):
    """
    Retrieve vpnbgp
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with vpnbgp data
    """
    try:
        result = meraki_client.dashboard.appliance.getNetworkApplianceVpnBgp(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_appliance_vpn_site_to_site_vpn",
    description="Retrieve vpnsitetositevpn"
)
def get_network_appliance_vpn_site_to_site_vpn(network_id: str):
    """
    Retrieve vpnsitetositevpn
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with vpnsitetositevpn data
    """
    try:
        result = meraki_client.dashboard.appliance.getNetworkApplianceVpnSiteToSiteVpn(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_appliance_warm_spare",
    description="Retrieve warmspare"
)
def get_network_appliance_warm_spare(network_id: str):
    """
    Retrieve warmspare
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with warmspare data
    """
    try:
        result = meraki_client.dashboard.appliance.getNetworkApplianceWarmSpare(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_appliance_dns_local_profiles",
    description="Retrieve dnslocalprofiles"
)
def get_organization_appliance_dns_local_profiles(organization_id: str):
    """
    Retrieve dnslocalprofiles
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with dnslocalprofiles data
    """
    try:
        result = meraki_client.dashboard.appliance.getOrganizationApplianceDnsLocalProfiles(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_appliance_dns_local_profiles_assignments",
    description="Retrieve dnslocalprofilesassignments"
)
def get_organization_appliance_dns_local_profiles_assignments(organization_id: str):
    """
    Retrieve dnslocalprofilesassignments
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with dnslocalprofilesassignments data
    """
    try:
        result = meraki_client.dashboard.appliance.getOrganizationApplianceDnsLocalProfilesAssignments(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_appliance_dns_local_records",
    description="Retrieve dnslocalrecords"
)
def get_organization_appliance_dns_local_records(organization_id: str):
    """
    Retrieve dnslocalrecords
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with dnslocalrecords data
    """
    try:
        result = meraki_client.dashboard.appliance.getOrganizationApplianceDnsLocalRecords(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_appliance_dns_split_profiles",
    description="Retrieve dnssplitprofiles"
)
def get_organization_appliance_dns_split_profiles(organization_id: str):
    """
    Retrieve dnssplitprofiles
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with dnssplitprofiles data
    """
    try:
        result = meraki_client.dashboard.appliance.getOrganizationApplianceDnsSplitProfiles(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_appliance_dns_split_profiles_assignments",
    description="Retrieve dnssplitprofilesassignments"
)
def get_organization_appliance_dns_split_profiles_assignments(organization_id: str):
    """
    Retrieve dnssplitprofilesassignments
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with dnssplitprofilesassignments data
    """
    try:
        result = meraki_client.dashboard.appliance.getOrganizationApplianceDnsSplitProfilesAssignments(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_appliance_firewall_multicast_forwarding_by_network",
    description="Retrieve firewallmulticastforwardingby"
)
def get_organization_appliance_firewall_multicast_forwarding_by_network(organization_id: str):
    """
    Retrieve firewallmulticastforwardingby
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with firewallmulticastforwardingby data
    """
    try:
        result = meraki_client.dashboard.appliance.getOrganizationApplianceFirewallMulticastForwardingByNetwork(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_appliance_security_events",
    description="Retrieve securityevents"
)
def get_organization_appliance_security_events(organization_id: str):
    """
    Retrieve securityevents
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with securityevents data
    """
    try:
        result = meraki_client.dashboard.appliance.getOrganizationApplianceSecurityEvents(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_appliance_security_intrusion",
    description="Retrieve securityintrusion"
)
def get_organization_appliance_security_intrusion(organization_id: str):
    """
    Retrieve securityintrusion
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with securityintrusion data
    """
    try:
        result = meraki_client.dashboard.appliance.getOrganizationApplianceSecurityIntrusion(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_appliance_traffic_shaping_vpn_exclusions_by_network",
    description="Retrieve trafficshapingvpnexclusionsby"
)
def get_organization_appliance_traffic_shaping_vpn_exclusions_by_network(organization_id: str):
    """
    Retrieve trafficshapingvpnexclusionsby
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with trafficshapingvpnexclusionsby data
    """
    try:
        result = meraki_client.dashboard.appliance.getOrganizationApplianceTrafficShapingVpnExclusionsByNetwork(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_appliance_uplink_statuses",
    description="Retrieve uplinkstatuses"
)
def get_organization_appliance_uplink_statuses(organization_id: str):
    """
    Retrieve uplinkstatuses
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with uplinkstatuses data
    """
    try:
        result = meraki_client.dashboard.appliance.getOrganizationApplianceUplinkStatuses(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_appliance_uplinks_statuses_overview",
    description="Retrieve uplinksstatusesoverview"
)
def get_organization_appliance_uplinks_statuses_overview(organization_id: str):
    """
    Retrieve uplinksstatusesoverview
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with uplinksstatusesoverview data
    """
    try:
        result = meraki_client.dashboard.appliance.getOrganizationApplianceUplinksStatusesOverview(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_appliance_uplinks_usage_by_network",
    description="Retrieve uplinksusageby"
)
def get_organization_appliance_uplinks_usage_by_network(organization_id: str):
    """
    Retrieve uplinksusageby
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with uplinksusageby data
    """
    try:
        result = meraki_client.dashboard.appliance.getOrganizationApplianceUplinksUsageByNetwork(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_appliance_vpn_stats",
    description="Retrieve vpnstats"
)
def get_organization_appliance_vpn_stats(organization_id: str):
    """
    Retrieve vpnstats
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with vpnstats data
    """
    try:
        result = meraki_client.dashboard.appliance.getOrganizationApplianceVpnStats(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_appliance_vpn_statuses",
    description="Retrieve vpnstatuses"
)
def get_organization_appliance_vpn_statuses(organization_id: str):
    """
    Retrieve vpnstatuses
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with vpnstatuses data
    """
    try:
        result = meraki_client.dashboard.appliance.getOrganizationApplianceVpnStatuses(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_appliance_vpn_third_party_vpn_peers",
    description="Retrieve vpnthirdpartyvpnpeers"
)
def get_organization_appliance_vpn_third_party_vpn_peers(organization_id: str):
    """
    Retrieve vpnthirdpartyvpnpeers
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with vpnthirdpartyvpnpeers data
    """
    try:
        result = meraki_client.dashboard.appliance.getOrganizationApplianceVpnThirdPartyVPNPeers(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_appliance_vpn_vpn_firewall_rules",
    description="Retrieve vpnvpnfirewallrules"
)
def get_organization_appliance_vpn_vpn_firewall_rules(organization_id: str):
    """
    Retrieve vpnvpnfirewallrules
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with vpnvpnfirewallrules data
    """
    try:
        result = meraki_client.dashboard.appliance.getOrganizationApplianceVpnVpnFirewallRules(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="swap_network_appliance_warm_spare",
    description="Manage swapwarmspare"
)
def swap_network_appliance_warm_spare():
    """
    Manage swapwarmspare
    
    Args:

    
    Returns:
        dict: API response with swapwarmspare data
    """
    try:
        result = meraki_client.dashboard.appliance.swapNetworkApplianceWarmSpare()
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_device_appliance_radio_settings",
    description="Update an existing radiosettings"
)
def update_device_appliance_radio_settings(serial: str, **kwargs):
    """
    Update an existing radiosettings
    
    Args:
        serial: Device serial number
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with radiosettings data
    """
    try:
        result = meraki_client.dashboard.appliance.updateDeviceApplianceRadioSettings(serial, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_device_appliance_uplinks_settings",
    description="Update an existing uplinkssettings"
)
def update_device_appliance_uplinks_settings(serial: str, **kwargs):
    """
    Update an existing uplinkssettings
    
    Args:
        serial: Device serial number
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with uplinkssettings data
    """
    try:
        result = meraki_client.dashboard.appliance.updateDeviceApplianceUplinksSettings(serial, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_network_appliance_connectivity_monitoring_destinations",
    description="Update an existing connectivitymonitoringdestinations"
)
def update_network_appliance_connectivity_monitoring_destinations(network_id: str, **kwargs):
    """
    Update an existing connectivitymonitoringdestinations
    
    Args:
        network_id: Network ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with connectivitymonitoringdestinations data
    """
    try:
        result = meraki_client.dashboard.appliance.updateNetworkApplianceConnectivityMonitoringDestinations(network_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_network_appliance_content_filtering",
    description="Update an existing contentfiltering"
)
def update_network_appliance_content_filtering(network_id: str, **kwargs):
    """
    Update an existing contentfiltering
    
    Args:
        network_id: Network ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with contentfiltering data
    """
    try:
        result = meraki_client.dashboard.appliance.updateNetworkApplianceContentFiltering(network_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_network_appliance_firewall_cellular_firewall_rules",
    description="Update an existing firewallcellularfirewallrules"
)
def update_network_appliance_firewall_cellular_firewall_rules(network_id: str, **kwargs):
    """
    Update an existing firewallcellularfirewallrules
    
    Args:
        network_id: Network ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with firewallcellularfirewallrules data
    """
    try:
        result = meraki_client.dashboard.appliance.updateNetworkApplianceFirewallCellularFirewallRules(network_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_network_appliance_firewall_firewalled_service",
    description="Update an existing firewallfirewalledservice"
)
def update_network_appliance_firewall_firewalled_service(network_id: str, **kwargs):
    """
    Update an existing firewallfirewalledservice
    
    Args:
        network_id: Network ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with firewallfirewalledservice data
    """
    try:
        result = meraki_client.dashboard.appliance.updateNetworkApplianceFirewallFirewalledService(network_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_network_appliance_firewall_inbound_cellular_firewall_rules",
    description="Update an existing firewallinboundcellularfirewallrules"
)
def update_network_appliance_firewall_inbound_cellular_firewall_rules(network_id: str, **kwargs):
    """
    Update an existing firewallinboundcellularfirewallrules
    
    Args:
        network_id: Network ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with firewallinboundcellularfirewallrules data
    """
    try:
        result = meraki_client.dashboard.appliance.updateNetworkApplianceFirewallInboundCellularFirewallRules(network_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_network_appliance_firewall_inbound_firewall_rules",
    description="Update an existing firewallinboundfirewallrules"
)
def update_network_appliance_firewall_inbound_firewall_rules(network_id: str, **kwargs):
    """
    Update an existing firewallinboundfirewallrules
    
    Args:
        network_id: Network ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with firewallinboundfirewallrules data
    """
    try:
        result = meraki_client.dashboard.appliance.updateNetworkApplianceFirewallInboundFirewallRules(network_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_network_appliance_firewall_l3_firewall_rules",
    description="Update an existing firewalll3firewallrules"
)
def update_network_appliance_firewall_l3_firewall_rules(network_id: str, **kwargs):
    """
    Update an existing firewalll3firewallrules
    
    Args:
        network_id: Network ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with firewalll3firewallrules data
    """
    try:
        result = meraki_client.dashboard.appliance.updateNetworkApplianceFirewallL3FirewallRules(network_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_network_appliance_firewall_l7_firewall_rules",
    description="Update an existing firewalll7firewallrules"
)
def update_network_appliance_firewall_l7_firewall_rules(network_id: str, **kwargs):
    """
    Update an existing firewalll7firewallrules
    
    Args:
        network_id: Network ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with firewalll7firewallrules data
    """
    try:
        result = meraki_client.dashboard.appliance.updateNetworkApplianceFirewallL7FirewallRules(network_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_network_appliance_firewall_multicast_forwarding",
    description="Update an existing firewallmulticastforwarding"
)
def update_network_appliance_firewall_multicast_forwarding(network_id: str, **kwargs):
    """
    Update an existing firewallmulticastforwarding
    
    Args:
        network_id: Network ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with firewallmulticastforwarding data
    """
    try:
        result = meraki_client.dashboard.appliance.updateNetworkApplianceFirewallMulticastForwarding(network_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_network_appliance_firewall_one_to_many_nat_rules",
    description="Update an existing firewallonetomanynatrules"
)
def update_network_appliance_firewall_one_to_many_nat_rules(network_id: str, **kwargs):
    """
    Update an existing firewallonetomanynatrules
    
    Args:
        network_id: Network ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with firewallonetomanynatrules data
    """
    try:
        result = meraki_client.dashboard.appliance.updateNetworkApplianceFirewallOneToManyNatRules(network_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_network_appliance_firewall_one_to_one_nat_rules",
    description="Update an existing firewallonetoonenatrules"
)
def update_network_appliance_firewall_one_to_one_nat_rules(network_id: str, **kwargs):
    """
    Update an existing firewallonetoonenatrules
    
    Args:
        network_id: Network ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with firewallonetoonenatrules data
    """
    try:
        result = meraki_client.dashboard.appliance.updateNetworkApplianceFirewallOneToOneNatRules(network_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_network_appliance_firewall_port_forwarding_rules",
    description="Update an existing firewallportforwardingrules"
)
def update_network_appliance_firewall_port_forwarding_rules(network_id: str, **kwargs):
    """
    Update an existing firewallportforwardingrules
    
    Args:
        network_id: Network ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with firewallportforwardingrules data
    """
    try:
        result = meraki_client.dashboard.appliance.updateNetworkApplianceFirewallPortForwardingRules(network_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_network_appliance_firewall_settings",
    description="Update an existing firewallsettings"
)
def update_network_appliance_firewall_settings(network_id: str, **kwargs):
    """
    Update an existing firewallsettings
    
    Args:
        network_id: Network ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with firewallsettings data
    """
    try:
        result = meraki_client.dashboard.appliance.updateNetworkApplianceFirewallSettings(network_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_network_appliance_port",
    description="Update an existing port"
)
def update_network_appliance_port(network_id: str, **kwargs):
    """
    Update an existing port
    
    Args:
        network_id: Network ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with port data
    """
    try:
        result = meraki_client.dashboard.appliance.updateNetworkAppliancePort(network_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_network_appliance_prefixes_delegated_static",
    description="Update an existing prefixesdelegatedstatic"
)
def update_network_appliance_prefixes_delegated_static(network_id: str, **kwargs):
    """
    Update an existing prefixesdelegatedstatic
    
    Args:
        network_id: Network ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with prefixesdelegatedstatic data
    """
    try:
        result = meraki_client.dashboard.appliance.updateNetworkAppliancePrefixesDelegatedStatic(network_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_network_appliance_rf_profile",
    description="Update an existing rfprofile"
)
def update_network_appliance_rf_profile(network_id: str, rf_profile_id: str, **kwargs):
    """
    Update an existing rfprofile
    
    Args:
        network_id: Network ID
        rf_profile_id: RF profile ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with rfprofile data
    """
    try:
        result = meraki_client.dashboard.appliance.updateNetworkApplianceRfProfile(network_id, rf_profile_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_network_appliance_sdwan_internet_policies",
    description="Update an existing sdwaninternetpolicies"
)
def update_network_appliance_sdwan_internet_policies(network_id: str, **kwargs):
    """
    Update an existing sdwaninternetpolicies
    
    Args:
        network_id: Network ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with sdwaninternetpolicies data
    """
    try:
        result = meraki_client.dashboard.appliance.updateNetworkApplianceSdwanInternetPolicies(network_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_network_appliance_security_intrusion",
    description="Update an existing securityintrusion"
)
def update_network_appliance_security_intrusion(network_id: str, **kwargs):
    """
    Update an existing securityintrusion
    
    Args:
        network_id: Network ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with securityintrusion data
    """
    try:
        result = meraki_client.dashboard.appliance.updateNetworkApplianceSecurityIntrusion(network_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_network_appliance_security_malware",
    description="Update an existing securitymalware"
)
def update_network_appliance_security_malware(network_id: str, **kwargs):
    """
    Update an existing securitymalware
    
    Args:
        network_id: Network ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with securitymalware data
    """
    try:
        result = meraki_client.dashboard.appliance.updateNetworkApplianceSecurityMalware(network_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_network_appliance_settings",
    description="Update an existing settings"
)
def update_network_appliance_settings(network_id: str, **kwargs):
    """
    Update an existing settings
    
    Args:
        network_id: Network ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with settings data
    """
    try:
        result = meraki_client.dashboard.appliance.updateNetworkApplianceSettings(network_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_network_appliance_single_lan",
    description="Update an existing singlelan"
)
def update_network_appliance_single_lan(network_id: str, **kwargs):
    """
    Update an existing singlelan
    
    Args:
        network_id: Network ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with singlelan data
    """
    try:
        result = meraki_client.dashboard.appliance.updateNetworkApplianceSingleLan(network_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_network_appliance_ssid",
    description="Update an existing ssid"
)
def update_network_appliance_ssid(network_id: str, **kwargs):
    """
    Update an existing ssid
    
    Args:
        network_id: Network ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with ssid data
    """
    try:
        result = meraki_client.dashboard.appliance.updateNetworkApplianceSsid(network_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_network_appliance_static_route",
    description="Update an existing staticroute"
)
def update_network_appliance_static_route(network_id: str, static_route_id: str, **kwargs):
    """
    Update an existing staticroute
    
    Args:
        network_id: Network ID
        static_route_id: Static route ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with staticroute data
    """
    try:
        result = meraki_client.dashboard.appliance.updateNetworkApplianceStaticRoute(network_id, static_route_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_network_appliance_traffic_shaping",
    description="Update an existing trafficshaping"
)
def update_network_appliance_traffic_shaping(network_id: str, **kwargs):
    """
    Update an existing trafficshaping
    
    Args:
        network_id: Network ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with trafficshaping data
    """
    try:
        result = meraki_client.dashboard.appliance.updateNetworkApplianceTrafficShaping(network_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_network_appliance_traffic_shaping_custom_performance_class",
    description="Update an existing trafficshapingcustomperformanceclass"
)
def update_network_appliance_traffic_shaping_custom_performance_class(network_id: str, custom_performance_class_id: str, **kwargs):
    """
    Update an existing trafficshapingcustomperformanceclass
    
    Args:
        network_id: Network ID
        custom_performance_class_id: Custom performance class ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with trafficshapingcustomperformanceclass data
    """
    try:
        result = meraki_client.dashboard.appliance.updateNetworkApplianceTrafficShapingCustomPerformanceClass(network_id, custom_performance_class_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_network_appliance_traffic_shaping_rules",
    description="Update an existing trafficshapingrules"
)
def update_network_appliance_traffic_shaping_rules(network_id: str, **kwargs):
    """
    Update an existing trafficshapingrules
    
    Args:
        network_id: Network ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with trafficshapingrules data
    """
    try:
        result = meraki_client.dashboard.appliance.updateNetworkApplianceTrafficShapingRules(network_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_network_appliance_traffic_shaping_uplink_bandwidth",
    description="Update an existing trafficshapinguplinkbandwidth"
)
def update_network_appliance_traffic_shaping_uplink_bandwidth(network_id: str, **kwargs):
    """
    Update an existing trafficshapinguplinkbandwidth
    
    Args:
        network_id: Network ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with trafficshapinguplinkbandwidth data
    """
    try:
        result = meraki_client.dashboard.appliance.updateNetworkApplianceTrafficShapingUplinkBandwidth(network_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_network_appliance_traffic_shaping_uplink_selection",
    description="Update an existing trafficshapinguplinkselection"
)
def update_network_appliance_traffic_shaping_uplink_selection(network_id: str, **kwargs):
    """
    Update an existing trafficshapinguplinkselection
    
    Args:
        network_id: Network ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with trafficshapinguplinkselection data
    """
    try:
        result = meraki_client.dashboard.appliance.updateNetworkApplianceTrafficShapingUplinkSelection(network_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_network_appliance_traffic_shaping_vpn_exclusions",
    description="Update an existing trafficshapingvpnexclusions"
)
def update_network_appliance_traffic_shaping_vpn_exclusions(network_id: str, **kwargs):
    """
    Update an existing trafficshapingvpnexclusions
    
    Args:
        network_id: Network ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with trafficshapingvpnexclusions data
    """
    try:
        result = meraki_client.dashboard.appliance.updateNetworkApplianceTrafficShapingVpnExclusions(network_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_network_appliance_vlan",
    description="Update an existing vlan"
)
def update_network_appliance_vlan(network_id: str, vlan_id: str, **kwargs):
    """
    Update an existing vlan
    
    Args:
        network_id: Network ID
        vlan_id: VLAN ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with vlan data
    """
    try:
        result = meraki_client.dashboard.appliance.updateNetworkApplianceVlan(network_id, vlan_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_network_appliance_vlans_settings",
    description="Update an existing vlanssettings"
)
def update_network_appliance_vlans_settings(network_id: str, vlan_id: str, **kwargs):
    """
    Update an existing vlanssettings
    
    Args:
        network_id: Network ID
        vlan_id: VLAN ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with vlanssettings data
    """
    try:
        result = meraki_client.dashboard.appliance.updateNetworkApplianceVlansSettings(network_id, vlan_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_network_appliance_vpn_bgp",
    description="Update an existing vpnbgp"
)
def update_network_appliance_vpn_bgp(network_id: str, **kwargs):
    """
    Update an existing vpnbgp
    
    Args:
        network_id: Network ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with vpnbgp data
    """
    try:
        result = meraki_client.dashboard.appliance.updateNetworkApplianceVpnBgp(network_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_network_appliance_vpn_site_to_site_vpn",
    description="Update an existing vpnsitetositevpn"
)
def update_network_appliance_vpn_site_to_site_vpn(network_id: str, **kwargs):
    """
    Update an existing vpnsitetositevpn
    
    Args:
        network_id: Network ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with vpnsitetositevpn data
    """
    try:
        result = meraki_client.dashboard.appliance.updateNetworkApplianceVpnSiteToSiteVpn(network_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_network_appliance_warm_spare",
    description="Update an existing warmspare"
)
def update_network_appliance_warm_spare(network_id: str, **kwargs):
    """
    Update an existing warmspare
    
    Args:
        network_id: Network ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with warmspare data
    """
    try:
        result = meraki_client.dashboard.appliance.updateNetworkApplianceWarmSpare(network_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_organization_appliance_dns_local_profile",
    description="Update an existing dnslocalprofile"
)
def update_organization_appliance_dns_local_profile(organization_id: str, **kwargs):
    """
    Update an existing dnslocalprofile
    
    Args:
        organization_id: Organization ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with dnslocalprofile data
    """
    try:
        result = meraki_client.dashboard.appliance.updateOrganizationApplianceDnsLocalProfile(organization_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_organization_appliance_dns_local_record",
    description="Update an existing dnslocalrecord"
)
def update_organization_appliance_dns_local_record(organization_id: str, **kwargs):
    """
    Update an existing dnslocalrecord
    
    Args:
        organization_id: Organization ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with dnslocalrecord data
    """
    try:
        result = meraki_client.dashboard.appliance.updateOrganizationApplianceDnsLocalRecord(organization_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_organization_appliance_dns_split_profile",
    description="Update an existing dnssplitprofile"
)
def update_organization_appliance_dns_split_profile(organization_id: str, **kwargs):
    """
    Update an existing dnssplitprofile
    
    Args:
        organization_id: Organization ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with dnssplitprofile data
    """
    try:
        result = meraki_client.dashboard.appliance.updateOrganizationApplianceDnsSplitProfile(organization_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_organization_appliance_security_intrusion",
    description="Update an existing securityintrusion"
)
def update_organization_appliance_security_intrusion(organization_id: str, **kwargs):
    """
    Update an existing securityintrusion
    
    Args:
        organization_id: Organization ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with securityintrusion data
    """
    try:
        result = meraki_client.dashboard.appliance.updateOrganizationApplianceSecurityIntrusion(organization_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_organization_appliance_vpn_third_party_vpn_peers",
    description="Update an existing vpnthirdpartyvpnpeers"
)
def update_organization_appliance_vpn_third_party_vpn_peers(organization_id: str, **kwargs):
    """
    Update an existing vpnthirdpartyvpnpeers
    
    Args:
        organization_id: Organization ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with vpnthirdpartyvpnpeers data
    """
    try:
        result = meraki_client.dashboard.appliance.updateOrganizationApplianceVpnThirdPartyVPNPeers(organization_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_organization_appliance_vpn_vpn_firewall_rules",
    description="Update an existing vpnvpnfirewallrules"
)
def update_organization_appliance_vpn_vpn_firewall_rules(organization_id: str, **kwargs):
    """
    Update an existing vpnvpnfirewallrules
    
    Args:
        organization_id: Organization ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with vpnvpnfirewallrules data
    """
    try:
        result = meraki_client.dashboard.appliance.updateOrganizationApplianceVpnVpnFirewallRules(organization_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}