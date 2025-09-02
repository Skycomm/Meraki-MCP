"""
Cisco Meraki MCP Server - Wireless SDK Tools
Complete implementation of all 116 official Meraki Wireless API methods.

This module provides 100% coverage of the Wireless category from the official Meraki Dashboard API SDK.
Each tool corresponds directly to a method in the meraki.dashboard.wireless namespace.
"""

# Import removed to avoid circular import
import meraki


def register_wireless_tools(app, meraki_client):
    """Register all wireless SDK tools."""
    print(f"📶 Registering 116 wireless SDK tools...")


@app.tool(
    name="assign_network_wireless_ethernet_ports_profiles",
    description="Manage assignethernetportsprofiles"
)
def assign_network_wireless_ethernet_ports_profiles():
    """
    Manage assignethernetportsprofiles
    
    Args:

    
    Returns:
        dict: API response with assignethernetportsprofiles data
    """
    try:
        result = meraki_client.dashboard.wireless.assignNetworkWirelessEthernetPortsProfiles()
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="create_network_wireless_air_marshal_rule",
    description="Create a new airmarshalrule"
)
def create_network_wireless_air_marshal_rule(network_id: str, **kwargs):
    """
    Create a new airmarshalrule
    
    Args:
        network_id: Network ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with airmarshalrule data
    """
    try:
        result = meraki_client.dashboard.wireless.createNetworkWirelessAirMarshalRule(network_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="create_network_wireless_ethernet_ports_profile",
    description="Create a new ethernetportsprofile"
)
def create_network_wireless_ethernet_ports_profile(network_id: str, profile_id: str, **kwargs):
    """
    Create a new ethernetportsprofile
    
    Args:
        network_id: Network ID
        profile_id: Profile ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with ethernetportsprofile data
    """
    try:
        result = meraki_client.dashboard.wireless.createNetworkWirelessEthernetPortsProfile(network_id, profile_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="create_network_wireless_rf_profile",
    description="Create a new rfprofile"
)
def create_network_wireless_rf_profile(network_id: str, rf_profile_id: str, **kwargs):
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
        result = meraki_client.dashboard.wireless.createNetworkWirelessRfProfile(network_id, rf_profile_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="create_network_wireless_ssid_identity_psk",
    description="Create a new ssididentitypsk"
)
def create_network_wireless_ssid_identity_psk(network_id: str, ssid_number: str, **kwargs):
    """
    Create a new ssididentitypsk
    
    Args:
        network_id: Network ID
        ssid_number: SSID number
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with ssididentitypsk data
    """
    try:
        result = meraki_client.dashboard.wireless.createNetworkWirelessSsidIdentityPsk(network_id, ssid_number, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="create_organization_wireless_devices_radsec_certificates_authority",
    description="Create a new sradseccertificatesauthority"
)
def create_organization_wireless_devices_radsec_certificates_authority(organization_id: str, **kwargs):
    """
    Create a new sradseccertificatesauthority
    
    Args:
        organization_id: Organization ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with sradseccertificatesauthority data
    """
    try:
        result = meraki_client.dashboard.wireless.createOrganizationWirelessDevicesRadsecCertificatesAuthority(organization_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="create_organization_wireless_location_scanning_receiver",
    description="Create a new locationscanningreceiver"
)
def create_organization_wireless_location_scanning_receiver(organization_id: str, **kwargs):
    """
    Create a new locationscanningreceiver
    
    Args:
        organization_id: Organization ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with locationscanningreceiver data
    """
    try:
        result = meraki_client.dashboard.wireless.createOrganizationWirelessLocationScanningReceiver(organization_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="create_organization_wireless_ssids_firewall_isolation_allowlist_entry",
    description="Create a new ssidsfirewallisolationallowlistentry"
)
def create_organization_wireless_ssids_firewall_isolation_allowlist_entry(organization_id: str, ssid_number: str, **kwargs):
    """
    Create a new ssidsfirewallisolationallowlistentry
    
    Args:
        organization_id: Organization ID
        ssid_number: SSID number
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with ssidsfirewallisolationallowlistentry data
    """
    try:
        result = meraki_client.dashboard.wireless.createOrganizationWirelessSsidsFirewallIsolationAllowlistEntry(organization_id, ssid_number, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="delete_network_wireless_air_marshal_rule",
    description="Delete an existing airmarshalrule"
)
def delete_network_wireless_air_marshal_rule(network_id: str):
    """
    Delete an existing airmarshalrule
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with airmarshalrule data
    """
    try:
        result = meraki_client.dashboard.wireless.deleteNetworkWirelessAirMarshalRule(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="delete_network_wireless_ethernet_ports_profile",
    description="Delete an existing ethernetportsprofile"
)
def delete_network_wireless_ethernet_ports_profile(network_id: str, profile_id: str):
    """
    Delete an existing ethernetportsprofile
    
    Args:
        network_id: Network ID
        profile_id: Profile ID
    
    Returns:
        dict: API response with ethernetportsprofile data
    """
    try:
        result = meraki_client.dashboard.wireless.deleteNetworkWirelessEthernetPortsProfile(network_id, profile_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="delete_network_wireless_rf_profile",
    description="Delete an existing rfprofile"
)
def delete_network_wireless_rf_profile(network_id: str, rf_profile_id: str):
    """
    Delete an existing rfprofile
    
    Args:
        network_id: Network ID
        rf_profile_id: RF profile ID
    
    Returns:
        dict: API response with rfprofile data
    """
    try:
        result = meraki_client.dashboard.wireless.deleteNetworkWirelessRfProfile(network_id, rf_profile_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="delete_network_wireless_ssid_identity_psk",
    description="Delete an existing ssididentitypsk"
)
def delete_network_wireless_ssid_identity_psk(network_id: str, ssid_number: str):
    """
    Delete an existing ssididentitypsk
    
    Args:
        network_id: Network ID
        ssid_number: SSID number
    
    Returns:
        dict: API response with ssididentitypsk data
    """
    try:
        result = meraki_client.dashboard.wireless.deleteNetworkWirelessSsidIdentityPsk(network_id, ssid_number)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="delete_organization_wireless_location_scanning_receiver",
    description="Delete an existing locationscanningreceiver"
)
def delete_organization_wireless_location_scanning_receiver(organization_id: str):
    """
    Delete an existing locationscanningreceiver
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with locationscanningreceiver data
    """
    try:
        result = meraki_client.dashboard.wireless.deleteOrganizationWirelessLocationScanningReceiver(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="delete_organization_wireless_ssids_firewall_isolation_allowlist_entry",
    description="Delete an existing ssidsfirewallisolationallowlistentry"
)
def delete_organization_wireless_ssids_firewall_isolation_allowlist_entry(organization_id: str, ssid_number: str):
    """
    Delete an existing ssidsfirewallisolationallowlistentry
    
    Args:
        organization_id: Organization ID
        ssid_number: SSID number
    
    Returns:
        dict: API response with ssidsfirewallisolationallowlistentry data
    """
    try:
        result = meraki_client.dashboard.wireless.deleteOrganizationWirelessSsidsFirewallIsolationAllowlistEntry(organization_id, ssid_number)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_device_wireless_bluetooth_settings",
    description="Retrieve bluetoothsettings"
)
def get_device_wireless_bluetooth_settings(serial: str):
    """
    Retrieve bluetoothsettings
    
    Args:
        serial: Device serial number
    
    Returns:
        dict: API response with bluetoothsettings data
    """
    try:
        result = meraki_client.dashboard.wireless.getDeviceWirelessBluetoothSettings(serial)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_device_wireless_connection_stats",
    description="Retrieve connectionstats"
)
def get_device_wireless_connection_stats(serial: str):
    """
    Retrieve connectionstats
    
    Args:
        serial: Device serial number
    
    Returns:
        dict: API response with connectionstats data
    """
    try:
        result = meraki_client.dashboard.wireless.getDeviceWirelessConnectionStats(serial)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_device_wireless_electronic_shelf_label",
    description="Retrieve electronicshelflabel"
)
def get_device_wireless_electronic_shelf_label(serial: str):
    """
    Retrieve electronicshelflabel
    
    Args:
        serial: Device serial number
    
    Returns:
        dict: API response with electronicshelflabel data
    """
    try:
        result = meraki_client.dashboard.wireless.getDeviceWirelessElectronicShelfLabel(serial)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_device_wireless_latency_stats",
    description="Retrieve latencystats"
)
def get_device_wireless_latency_stats(serial: str):
    """
    Retrieve latencystats
    
    Args:
        serial: Device serial number
    
    Returns:
        dict: API response with latencystats data
    """
    try:
        result = meraki_client.dashboard.wireless.getDeviceWirelessLatencyStats(serial)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_device_wireless_radio_settings",
    description="Retrieve radiosettings"
)
def get_device_wireless_radio_settings(serial: str):
    """
    Retrieve radiosettings
    
    Args:
        serial: Device serial number
    
    Returns:
        dict: API response with radiosettings data
    """
    try:
        result = meraki_client.dashboard.wireless.getDeviceWirelessRadioSettings(serial)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_device_wireless_status",
    description="Retrieve status"
)
def get_device_wireless_status(serial: str):
    """
    Retrieve status
    
    Args:
        serial: Device serial number
    
    Returns:
        dict: API response with status data
    """
    try:
        result = meraki_client.dashboard.wireless.getDeviceWirelessStatus(serial)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_wireless_air_marshal",
    description="Retrieve airmarshal"
)
def get_network_wireless_air_marshal(network_id: str):
    """
    Retrieve airmarshal
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with airmarshal data
    """
    try:
        result = meraki_client.dashboard.wireless.getNetworkWirelessAirMarshal(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_wireless_alternate_management_interface",
    description="Retrieve alternatemanagementinterface"
)
def get_network_wireless_alternate_management_interface(network_id: str):
    """
    Retrieve alternatemanagementinterface
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with alternatemanagementinterface data
    """
    try:
        result = meraki_client.dashboard.wireless.getNetworkWirelessAlternateManagementInterface(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_wireless_billing",
    description="Retrieve billing"
)
def get_network_wireless_billing(network_id: str):
    """
    Retrieve billing
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with billing data
    """
    try:
        result = meraki_client.dashboard.wireless.getNetworkWirelessBilling(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_wireless_bluetooth_settings",
    description="Retrieve bluetoothsettings"
)
def get_network_wireless_bluetooth_settings(network_id: str):
    """
    Retrieve bluetoothsettings
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with bluetoothsettings data
    """
    try:
        result = meraki_client.dashboard.wireless.getNetworkWirelessBluetoothSettings(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_wireless_channel_utilization_history",
    description="Retrieve channelutilizationhistory"
)
def get_network_wireless_channel_utilization_history(network_id: str, timespan: int = 86400, device_serial: str = None, client_id: str = None):
    """
    Retrieve channelutilizationhistory
    
    Args:
        network_id: Network ID
        timespan: Timespan in seconds (default: 86400)
        device_serial: Device serial number (optional)
        client_id: Client ID (optional)
    
    Returns:
        dict: API response with channelutilizationhistory data
    """
    try:
        result = meraki_client.dashboard.wireless.getNetworkWirelessChannelUtilizationHistory(network_id, timespan=timespan, deviceSerial=device_serial, clientId=client_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_wireless_client_connection_stats",
    description="Retrieve clientconnectionstats"
)
def get_network_wireless_client_connection_stats(network_id: str):
    """
    Retrieve clientconnectionstats
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with clientconnectionstats data
    """
    try:
        result = meraki_client.dashboard.wireless.getNetworkWirelessClientConnectionStats(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_wireless_client_connectivity_events",
    description="Retrieve clientconnectivityevents"
)
def get_network_wireless_client_connectivity_events(network_id: str):
    """
    Retrieve clientconnectivityevents
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with clientconnectivityevents data
    """
    try:
        result = meraki_client.dashboard.wireless.getNetworkWirelessClientConnectivityEvents(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_wireless_client_count_history",
    description="Retrieve clientcounthistory"
)
def get_network_wireless_client_count_history(network_id: str, timespan: int = 86400, device_serial: str = None, client_id: str = None):
    """
    Retrieve clientcounthistory
    
    Args:
        network_id: Network ID
        timespan: Timespan in seconds (default: 86400)
        device_serial: Device serial number (optional)
        client_id: Client ID (optional)
    
    Returns:
        dict: API response with clientcounthistory data
    """
    try:
        result = meraki_client.dashboard.wireless.getNetworkWirelessClientCountHistory(network_id, timespan=timespan, deviceSerial=device_serial, clientId=client_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_wireless_client_latency_history",
    description="Retrieve clientlatencyhistory"
)
def get_network_wireless_client_latency_history(network_id: str, timespan: int = 86400, device_serial: str = None, client_id: str = None):
    """
    Retrieve clientlatencyhistory
    
    Args:
        network_id: Network ID
        timespan: Timespan in seconds (default: 86400)
        device_serial: Device serial number (optional)
        client_id: Client ID (optional)
    
    Returns:
        dict: API response with clientlatencyhistory data
    """
    try:
        result = meraki_client.dashboard.wireless.getNetworkWirelessClientLatencyHistory(network_id, timespan=timespan, deviceSerial=device_serial, clientId=client_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_wireless_client_latency_stats",
    description="Retrieve clientlatencystats"
)
def get_network_wireless_client_latency_stats(network_id: str):
    """
    Retrieve clientlatencystats
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with clientlatencystats data
    """
    try:
        result = meraki_client.dashboard.wireless.getNetworkWirelessClientLatencyStats(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_wireless_clients_connection_stats",
    description="Retrieve clientsconnectionstats"
)
def get_network_wireless_clients_connection_stats(network_id: str):
    """
    Retrieve clientsconnectionstats
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with clientsconnectionstats data
    """
    try:
        result = meraki_client.dashboard.wireless.getNetworkWirelessClientsConnectionStats(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_wireless_clients_latency_stats",
    description="Retrieve clientslatencystats"
)
def get_network_wireless_clients_latency_stats(network_id: str):
    """
    Retrieve clientslatencystats
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with clientslatencystats data
    """
    try:
        result = meraki_client.dashboard.wireless.getNetworkWirelessClientsLatencyStats(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_wireless_connection_stats",
    description="Retrieve connectionstats"
)
def get_network_wireless_connection_stats(network_id: str):
    """
    Retrieve connectionstats
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with connectionstats data
    """
    try:
        result = meraki_client.dashboard.wireless.getNetworkWirelessConnectionStats(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_wireless_data_rate_history",
    description="Retrieve dataratehistory"
)
def get_network_wireless_data_rate_history(network_id: str, timespan: int = 86400, device_serial: str = None, client_id: str = None):
    """
    Retrieve dataratehistory
    
    Args:
        network_id: Network ID
        timespan: Timespan in seconds (default: 86400)
        device_serial: Device serial number (optional)
        client_id: Client ID (optional)
    
    Returns:
        dict: API response with dataratehistory data
    """
    try:
        result = meraki_client.dashboard.wireless.getNetworkWirelessDataRateHistory(network_id, timespan=timespan, deviceSerial=device_serial, clientId=client_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_wireless_devices_connection_stats",
    description="Retrieve sconnectionstats"
)
def get_network_wireless_devices_connection_stats(network_id: str):
    """
    Retrieve sconnectionstats
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with sconnectionstats data
    """
    try:
        result = meraki_client.dashboard.wireless.getNetworkWirelessDevicesConnectionStats(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_wireless_devices_latency_stats",
    description="Retrieve slatencystats"
)
def get_network_wireless_devices_latency_stats(network_id: str):
    """
    Retrieve slatencystats
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with slatencystats data
    """
    try:
        result = meraki_client.dashboard.wireless.getNetworkWirelessDevicesLatencyStats(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_wireless_electronic_shelf_label",
    description="Retrieve electronicshelflabel"
)
def get_network_wireless_electronic_shelf_label(network_id: str):
    """
    Retrieve electronicshelflabel
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with electronicshelflabel data
    """
    try:
        result = meraki_client.dashboard.wireless.getNetworkWirelessElectronicShelfLabel(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_wireless_electronic_shelf_label_configured_devices",
    description="Retrieve electronicshelflabelconfigureds"
)
def get_network_wireless_electronic_shelf_label_configured_devices(network_id: str):
    """
    Retrieve electronicshelflabelconfigureds
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with electronicshelflabelconfigureds data
    """
    try:
        result = meraki_client.dashboard.wireless.getNetworkWirelessElectronicShelfLabelConfiguredDevices(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_wireless_ethernet_ports_profile",
    description="Retrieve ethernetportsprofile"
)
def get_network_wireless_ethernet_ports_profile(network_id: str, profile_id: str):
    """
    Retrieve ethernetportsprofile
    
    Args:
        network_id: Network ID
        profile_id: Profile ID
    
    Returns:
        dict: API response with ethernetportsprofile data
    """
    try:
        result = meraki_client.dashboard.wireless.getNetworkWirelessEthernetPortsProfile(network_id, profile_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_wireless_ethernet_ports_profiles",
    description="Retrieve ethernetportsprofiles"
)
def get_network_wireless_ethernet_ports_profiles(network_id: str):
    """
    Retrieve ethernetportsprofiles
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with ethernetportsprofiles data
    """
    try:
        result = meraki_client.dashboard.wireless.getNetworkWirelessEthernetPortsProfiles(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_wireless_failed_connections",
    description="Retrieve failedconnections"
)
def get_network_wireless_failed_connections(network_id: str):
    """
    Retrieve failedconnections
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with failedconnections data
    """
    try:
        result = meraki_client.dashboard.wireless.getNetworkWirelessFailedConnections(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_wireless_latency_history",
    description="Retrieve latencyhistory"
)
def get_network_wireless_latency_history(network_id: str, timespan: int = 86400, device_serial: str = None, client_id: str = None):
    """
    Retrieve latencyhistory
    
    Args:
        network_id: Network ID
        timespan: Timespan in seconds (default: 86400)
        device_serial: Device serial number (optional)
        client_id: Client ID (optional)
    
    Returns:
        dict: API response with latencyhistory data
    """
    try:
        result = meraki_client.dashboard.wireless.getNetworkWirelessLatencyHistory(network_id, timespan=timespan, deviceSerial=device_serial, clientId=client_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_wireless_latency_stats",
    description="Retrieve latencystats"
)
def get_network_wireless_latency_stats(network_id: str):
    """
    Retrieve latencystats
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with latencystats data
    """
    try:
        result = meraki_client.dashboard.wireless.getNetworkWirelessLatencyStats(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_wireless_mesh_statuses",
    description="Retrieve meshstatuses"
)
def get_network_wireless_mesh_statuses(network_id: str):
    """
    Retrieve meshstatuses
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with meshstatuses data
    """
    try:
        result = meraki_client.dashboard.wireless.getNetworkWirelessMeshStatuses(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_wireless_rf_profile",
    description="Retrieve rfprofile"
)
def get_network_wireless_rf_profile(network_id: str, rf_profile_id: str):
    """
    Retrieve rfprofile
    
    Args:
        network_id: Network ID
        rf_profile_id: RF profile ID
    
    Returns:
        dict: API response with rfprofile data
    """
    try:
        result = meraki_client.dashboard.wireless.getNetworkWirelessRfProfile(network_id, rf_profile_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_wireless_rf_profiles",
    description="Retrieve rfprofiles"
)
def get_network_wireless_rf_profiles(network_id: str):
    """
    Retrieve rfprofiles
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with rfprofiles data
    """
    try:
        result = meraki_client.dashboard.wireless.getNetworkWirelessRfProfiles(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_wireless_settings",
    description="Retrieve settings"
)
def get_network_wireless_settings(network_id: str):
    """
    Retrieve settings
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with settings data
    """
    try:
        result = meraki_client.dashboard.wireless.getNetworkWirelessSettings(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_wireless_signal_quality_history",
    description="Retrieve signalqualityhistory"
)
def get_network_wireless_signal_quality_history(network_id: str, timespan: int = 86400, device_serial: str = None, client_id: str = None):
    """
    Retrieve signalqualityhistory
    
    Args:
        network_id: Network ID
        timespan: Timespan in seconds (default: 86400)
        device_serial: Device serial number (optional)
        client_id: Client ID (optional)
    
    Returns:
        dict: API response with signalqualityhistory data
    """
    try:
        result = meraki_client.dashboard.wireless.getNetworkWirelessSignalQualityHistory(network_id, timespan=timespan, deviceSerial=device_serial, clientId=client_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_wireless_ssid",
    description="Retrieve ssid"
)
def get_network_wireless_ssid(network_id: str, ssid_number: str):
    """
    Retrieve ssid
    
    Args:
        network_id: Network ID
        ssid_number: SSID number
    
    Returns:
        dict: API response with ssid data
    """
    try:
        result = meraki_client.dashboard.wireless.getNetworkWirelessSsid(network_id, ssid_number)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_wireless_ssid_bonjour_forwarding",
    description="Retrieve ssidbonjourforwarding"
)
def get_network_wireless_ssid_bonjour_forwarding(network_id: str, ssid_number: str):
    """
    Retrieve ssidbonjourforwarding
    
    Args:
        network_id: Network ID
        ssid_number: SSID number
    
    Returns:
        dict: API response with ssidbonjourforwarding data
    """
    try:
        result = meraki_client.dashboard.wireless.getNetworkWirelessSsidBonjourForwarding(network_id, ssid_number)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_wireless_ssid_device_type_group_policies",
    description="Retrieve ssidtypegrouppolicies"
)
def get_network_wireless_ssid_device_type_group_policies(network_id: str, ssid_number: str):
    """
    Retrieve ssidtypegrouppolicies
    
    Args:
        network_id: Network ID
        ssid_number: SSID number
    
    Returns:
        dict: API response with ssidtypegrouppolicies data
    """
    try:
        result = meraki_client.dashboard.wireless.getNetworkWirelessSsidDeviceTypeGroupPolicies(network_id, ssid_number)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_wireless_ssid_eap_override",
    description="Retrieve ssideapoverride"
)
def get_network_wireless_ssid_eap_override(network_id: str, ssid_number: str):
    """
    Retrieve ssideapoverride
    
    Args:
        network_id: Network ID
        ssid_number: SSID number
    
    Returns:
        dict: API response with ssideapoverride data
    """
    try:
        result = meraki_client.dashboard.wireless.getNetworkWirelessSsidEapOverride(network_id, ssid_number)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_wireless_ssid_firewall_l3_firewall_rules",
    description="Retrieve ssidfirewalll3firewallrules"
)
def get_network_wireless_ssid_firewall_l3_firewall_rules(network_id: str, ssid_number: str):
    """
    Retrieve ssidfirewalll3firewallrules
    
    Args:
        network_id: Network ID
        ssid_number: SSID number
    
    Returns:
        dict: API response with ssidfirewalll3firewallrules data
    """
    try:
        result = meraki_client.dashboard.wireless.getNetworkWirelessSsidFirewallL3FirewallRules(network_id, ssid_number)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_wireless_ssid_firewall_l7_firewall_rules",
    description="Retrieve ssidfirewalll7firewallrules"
)
def get_network_wireless_ssid_firewall_l7_firewall_rules(network_id: str, ssid_number: str):
    """
    Retrieve ssidfirewalll7firewallrules
    
    Args:
        network_id: Network ID
        ssid_number: SSID number
    
    Returns:
        dict: API response with ssidfirewalll7firewallrules data
    """
    try:
        result = meraki_client.dashboard.wireless.getNetworkWirelessSsidFirewallL7FirewallRules(network_id, ssid_number)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_wireless_ssid_hotspot20",
    description="Retrieve ssidhotspot20"
)
def get_network_wireless_ssid_hotspot20(network_id: str, ssid_number: str):
    """
    Retrieve ssidhotspot20
    
    Args:
        network_id: Network ID
        ssid_number: SSID number
    
    Returns:
        dict: API response with ssidhotspot20 data
    """
    try:
        result = meraki_client.dashboard.wireless.getNetworkWirelessSsidHotspot20(network_id, ssid_number)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_wireless_ssid_identity_psk",
    description="Retrieve ssididentitypsk"
)
def get_network_wireless_ssid_identity_psk(network_id: str, ssid_number: str):
    """
    Retrieve ssididentitypsk
    
    Args:
        network_id: Network ID
        ssid_number: SSID number
    
    Returns:
        dict: API response with ssididentitypsk data
    """
    try:
        result = meraki_client.dashboard.wireless.getNetworkWirelessSsidIdentityPsk(network_id, ssid_number)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_wireless_ssid_identity_psks",
    description="Retrieve ssididentitypsks"
)
def get_network_wireless_ssid_identity_psks(network_id: str, ssid_number: str):
    """
    Retrieve ssididentitypsks
    
    Args:
        network_id: Network ID
        ssid_number: SSID number
    
    Returns:
        dict: API response with ssididentitypsks data
    """
    try:
        result = meraki_client.dashboard.wireless.getNetworkWirelessSsidIdentityPsks(network_id, ssid_number)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_wireless_ssid_schedules",
    description="Retrieve ssidschedules"
)
def get_network_wireless_ssid_schedules(network_id: str, ssid_number: str):
    """
    Retrieve ssidschedules
    
    Args:
        network_id: Network ID
        ssid_number: SSID number
    
    Returns:
        dict: API response with ssidschedules data
    """
    try:
        result = meraki_client.dashboard.wireless.getNetworkWirelessSsidSchedules(network_id, ssid_number)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_wireless_ssid_splash_settings",
    description="Retrieve ssidsplashsettings"
)
def get_network_wireless_ssid_splash_settings(network_id: str, ssid_number: str):
    """
    Retrieve ssidsplashsettings
    
    Args:
        network_id: Network ID
        ssid_number: SSID number
    
    Returns:
        dict: API response with ssidsplashsettings data
    """
    try:
        result = meraki_client.dashboard.wireless.getNetworkWirelessSsidSplashSettings(network_id, ssid_number)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_wireless_ssid_traffic_shaping_rules",
    description="Retrieve ssidtrafficshapingrules"
)
def get_network_wireless_ssid_traffic_shaping_rules(network_id: str, ssid_number: str):
    """
    Retrieve ssidtrafficshapingrules
    
    Args:
        network_id: Network ID
        ssid_number: SSID number
    
    Returns:
        dict: API response with ssidtrafficshapingrules data
    """
    try:
        result = meraki_client.dashboard.wireless.getNetworkWirelessSsidTrafficShapingRules(network_id, ssid_number)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_wireless_ssid_vpn",
    description="Retrieve ssidvpn"
)
def get_network_wireless_ssid_vpn(network_id: str, ssid_number: str):
    """
    Retrieve ssidvpn
    
    Args:
        network_id: Network ID
        ssid_number: SSID number
    
    Returns:
        dict: API response with ssidvpn data
    """
    try:
        result = meraki_client.dashboard.wireless.getNetworkWirelessSsidVpn(network_id, ssid_number)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_wireless_ssids",
    description="Retrieve ssids"
)
def get_network_wireless_ssids(network_id: str):
    """
    Retrieve ssids
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with ssids data
    """
    try:
        result = meraki_client.dashboard.wireless.getNetworkWirelessSsids(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_wireless_usage_history",
    description="Retrieve usagehistory"
)
def get_network_wireless_usage_history(network_id: str, timespan: int = 86400, device_serial: str = None, client_id: str = None):
    """
    Retrieve usagehistory
    
    Args:
        network_id: Network ID
        timespan: Timespan in seconds (default: 86400)
        device_serial: Device serial number (optional)
        client_id: Client ID (optional)
    
    Returns:
        dict: API response with usagehistory data
    """
    try:
        result = meraki_client.dashboard.wireless.getNetworkWirelessUsageHistory(network_id, timespan=timespan, deviceSerial=device_serial, clientId=client_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_wireless_air_marshal_rules",
    description="Retrieve airmarshalrules"
)
def get_organization_wireless_air_marshal_rules(organization_id: str):
    """
    Retrieve airmarshalrules
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with airmarshalrules data
    """
    try:
        result = meraki_client.dashboard.wireless.getOrganizationWirelessAirMarshalRules(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_wireless_air_marshal_settings_by_network",
    description="Retrieve airmarshalsettingsby"
)
def get_organization_wireless_air_marshal_settings_by_network(organization_id: str):
    """
    Retrieve airmarshalsettingsby
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with airmarshalsettingsby data
    """
    try:
        result = meraki_client.dashboard.wireless.getOrganizationWirelessAirMarshalSettingsByNetwork(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_wireless_clients_overview_by_device",
    description="Retrieve clientsoverviewby"
)
def get_organization_wireless_clients_overview_by_device(organization_id: str):
    """
    Retrieve clientsoverviewby
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with clientsoverviewby data
    """
    try:
        result = meraki_client.dashboard.wireless.getOrganizationWirelessClientsOverviewByDevice(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_wireless_devices_channel_utilization_by_device",
    description="Retrieve schannelutilizationby"
)
def get_organization_wireless_devices_channel_utilization_by_device(organization_id: str, timespan: int = 86400):
    """
    Retrieve schannelutilizationby
    
    Args:
        organization_id: Organization ID
        timespan: Timespan in seconds (default: 86400)
    
    Returns:
        dict: API response with schannelutilizationby data
    """
    try:
        result = meraki_client.dashboard.wireless.getOrganizationWirelessDevicesChannelUtilizationByDevice(organization_id, timespan=timespan)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_wireless_devices_channel_utilization_by_network",
    description="Retrieve schannelutilizationby"
)
def get_organization_wireless_devices_channel_utilization_by_network(organization_id: str, timespan: int = 86400):
    """
    Retrieve schannelutilizationby
    
    Args:
        organization_id: Organization ID
        timespan: Timespan in seconds (default: 86400)
    
    Returns:
        dict: API response with schannelutilizationby data
    """
    try:
        result = meraki_client.dashboard.wireless.getOrganizationWirelessDevicesChannelUtilizationByNetwork(organization_id, timespan=timespan)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_wireless_devices_channel_utilization_history_by_device_by_interval",
    description="Retrieve schannelutilizationhistorybybyinterval"
)
def get_organization_wireless_devices_channel_utilization_history_by_device_by_interval(organization_id: str, timespan: int = 86400):
    """
    Retrieve schannelutilizationhistorybybyinterval
    
    Args:
        organization_id: Organization ID
        timespan: Timespan in seconds (default: 86400)
    
    Returns:
        dict: API response with schannelutilizationhistorybybyinterval data
    """
    try:
        result = meraki_client.dashboard.wireless.getOrganizationWirelessDevicesChannelUtilizationHistoryByDeviceByInterval(organization_id, timespan=timespan)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_wireless_devices_channel_utilization_history_by_network_by_interval",
    description="Retrieve schannelutilizationhistorybybyinterval"
)
def get_organization_wireless_devices_channel_utilization_history_by_network_by_interval(organization_id: str, timespan: int = 86400):
    """
    Retrieve schannelutilizationhistorybybyinterval
    
    Args:
        organization_id: Organization ID
        timespan: Timespan in seconds (default: 86400)
    
    Returns:
        dict: API response with schannelutilizationhistorybybyinterval data
    """
    try:
        result = meraki_client.dashboard.wireless.getOrganizationWirelessDevicesChannelUtilizationHistoryByNetworkByInterval(organization_id, timespan=timespan)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_wireless_devices_ethernet_statuses",
    description="Retrieve sethernetstatuses"
)
def get_organization_wireless_devices_ethernet_statuses(organization_id: str):
    """
    Retrieve sethernetstatuses
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with sethernetstatuses data
    """
    try:
        result = meraki_client.dashboard.wireless.getOrganizationWirelessDevicesEthernetStatuses(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_wireless_devices_packet_loss_by_client",
    description="Retrieve spacketlossbyclient"
)
def get_organization_wireless_devices_packet_loss_by_client(organization_id: str):
    """
    Retrieve spacketlossbyclient
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with spacketlossbyclient data
    """
    try:
        result = meraki_client.dashboard.wireless.getOrganizationWirelessDevicesPacketLossByClient(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_wireless_devices_packet_loss_by_device",
    description="Retrieve spacketlossby"
)
def get_organization_wireless_devices_packet_loss_by_device(organization_id: str):
    """
    Retrieve spacketlossby
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with spacketlossby data
    """
    try:
        result = meraki_client.dashboard.wireless.getOrganizationWirelessDevicesPacketLossByDevice(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_wireless_devices_packet_loss_by_network",
    description="Retrieve spacketlossby"
)
def get_organization_wireless_devices_packet_loss_by_network(organization_id: str):
    """
    Retrieve spacketlossby
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with spacketlossby data
    """
    try:
        result = meraki_client.dashboard.wireless.getOrganizationWirelessDevicesPacketLossByNetwork(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_wireless_devices_power_mode_history",
    description="Retrieve spowermodehistory"
)
def get_organization_wireless_devices_power_mode_history(organization_id: str, timespan: int = 86400):
    """
    Retrieve spowermodehistory
    
    Args:
        organization_id: Organization ID
        timespan: Timespan in seconds (default: 86400)
    
    Returns:
        dict: API response with spowermodehistory data
    """
    try:
        result = meraki_client.dashboard.wireless.getOrganizationWirelessDevicesPowerModeHistory(organization_id, timespan=timespan)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_wireless_devices_radsec_certificates_authorities",
    description="Retrieve sradseccertificatesauthorities"
)
def get_organization_wireless_devices_radsec_certificates_authorities(organization_id: str):
    """
    Retrieve sradseccertificatesauthorities
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with sradseccertificatesauthorities data
    """
    try:
        result = meraki_client.dashboard.wireless.getOrganizationWirelessDevicesRadsecCertificatesAuthorities(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_wireless_devices_radsec_certificates_authorities_crls",
    description="Retrieve sradseccertificatesauthoritiescrls"
)
def get_organization_wireless_devices_radsec_certificates_authorities_crls(organization_id: str):
    """
    Retrieve sradseccertificatesauthoritiescrls
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with sradseccertificatesauthoritiescrls data
    """
    try:
        result = meraki_client.dashboard.wireless.getOrganizationWirelessDevicesRadsecCertificatesAuthoritiesCrls(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_wireless_devices_radsec_certificates_authorities_crls_deltas",
    description="Retrieve sradseccertificatesauthoritiescrlsdeltas"
)
def get_organization_wireless_devices_radsec_certificates_authorities_crls_deltas(organization_id: str):
    """
    Retrieve sradseccertificatesauthoritiescrlsdeltas
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with sradseccertificatesauthoritiescrlsdeltas data
    """
    try:
        result = meraki_client.dashboard.wireless.getOrganizationWirelessDevicesRadsecCertificatesAuthoritiesCrlsDeltas(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_wireless_devices_system_cpu_load_history",
    description="Retrieve ssystemcpuloadhistory"
)
def get_organization_wireless_devices_system_cpu_load_history(organization_id: str, timespan: int = 86400):
    """
    Retrieve ssystemcpuloadhistory
    
    Args:
        organization_id: Organization ID
        timespan: Timespan in seconds (default: 86400)
    
    Returns:
        dict: API response with ssystemcpuloadhistory data
    """
    try:
        result = meraki_client.dashboard.wireless.getOrganizationWirelessDevicesSystemCpuLoadHistory(organization_id, timespan=timespan)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_wireless_devices_wireless_controllers_by_device",
    description="Retrieve scontrollersby"
)
def get_organization_wireless_devices_wireless_controllers_by_device(organization_id: str):
    """
    Retrieve scontrollersby
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with scontrollersby data
    """
    try:
        result = meraki_client.dashboard.wireless.getOrganizationWirelessDevicesWirelessControllersByDevice(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_wireless_location_scanning_by_network",
    description="Retrieve locationscanningby"
)
def get_organization_wireless_location_scanning_by_network(organization_id: str):
    """
    Retrieve locationscanningby
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with locationscanningby data
    """
    try:
        result = meraki_client.dashboard.wireless.getOrganizationWirelessLocationScanningByNetwork(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_wireless_location_scanning_receivers",
    description="Retrieve locationscanningreceivers"
)
def get_organization_wireless_location_scanning_receivers(organization_id: str):
    """
    Retrieve locationscanningreceivers
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with locationscanningreceivers data
    """
    try:
        result = meraki_client.dashboard.wireless.getOrganizationWirelessLocationScanningReceivers(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_wireless_rf_profiles_assignments_by_device",
    description="Retrieve rfprofilesassignmentsby"
)
def get_organization_wireless_rf_profiles_assignments_by_device(organization_id: str, rf_profile_id: str):
    """
    Retrieve rfprofilesassignmentsby
    
    Args:
        organization_id: Organization ID
        rf_profile_id: RF profile ID
    
    Returns:
        dict: API response with rfprofilesassignmentsby data
    """
    try:
        result = meraki_client.dashboard.wireless.getOrganizationWirelessRfProfilesAssignmentsByDevice(organization_id, rf_profile_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_wireless_ssids_firewall_isolation_allowlist_entries",
    description="Retrieve ssidsfirewallisolationallowlistentries"
)
def get_organization_wireless_ssids_firewall_isolation_allowlist_entries(organization_id: str, ssid_number: str):
    """
    Retrieve ssidsfirewallisolationallowlistentries
    
    Args:
        organization_id: Organization ID
        ssid_number: SSID number
    
    Returns:
        dict: API response with ssidsfirewallisolationallowlistentries data
    """
    try:
        result = meraki_client.dashboard.wireless.getOrganizationWirelessSsidsFirewallIsolationAllowlistEntries(organization_id, ssid_number)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_wireless_ssids_statuses_by_device",
    description="Retrieve ssidsstatusesby"
)
def get_organization_wireless_ssids_statuses_by_device(organization_id: str, ssid_number: str):
    """
    Retrieve ssidsstatusesby
    
    Args:
        organization_id: Organization ID
        ssid_number: SSID number
    
    Returns:
        dict: API response with ssidsstatusesby data
    """
    try:
        result = meraki_client.dashboard.wireless.getOrganizationWirelessSsidsStatusesByDevice(organization_id, ssid_number)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="recalculate_organization_wireless_radio_auto_rf_channels",
    description="Recalculate radioautorfchannels"
)
def recalculate_organization_wireless_radio_auto_rf_channels(organization_id: str):
    """
    Recalculate radioautorfchannels
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with radioautorfchannels data
    """
    try:
        result = meraki_client.dashboard.wireless.recalculateOrganizationWirelessRadioAutoRfChannels(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="set_network_wireless_ethernet_ports_profiles_default",
    description="Set ethernetportsprofilesdefault"
)
def set_network_wireless_ethernet_ports_profiles_default(network_id: str, profile_id: str, **kwargs):
    """
    Set ethernetportsprofilesdefault
    
    Args:
        network_id: Network ID
        profile_id: Profile ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with ethernetportsprofilesdefault data
    """
    try:
        result = meraki_client.dashboard.wireless.setNetworkWirelessEthernetPortsProfilesDefault(network_id, profile_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_device_wireless_alternate_management_interface_ipv6",
    description="Update an existing alternatemanagementinterfaceipv6"
)
def update_device_wireless_alternate_management_interface_ipv6(serial: str, **kwargs):
    """
    Update an existing alternatemanagementinterfaceipv6
    
    Args:
        serial: Device serial number
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with alternatemanagementinterfaceipv6 data
    """
    try:
        result = meraki_client.dashboard.wireless.updateDeviceWirelessAlternateManagementInterfaceIpv6(serial, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_device_wireless_bluetooth_settings",
    description="Update an existing bluetoothsettings"
)
def update_device_wireless_bluetooth_settings(serial: str, **kwargs):
    """
    Update an existing bluetoothsettings
    
    Args:
        serial: Device serial number
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with bluetoothsettings data
    """
    try:
        result = meraki_client.dashboard.wireless.updateDeviceWirelessBluetoothSettings(serial, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_device_wireless_electronic_shelf_label",
    description="Update an existing electronicshelflabel"
)
def update_device_wireless_electronic_shelf_label(serial: str, **kwargs):
    """
    Update an existing electronicshelflabel
    
    Args:
        serial: Device serial number
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with electronicshelflabel data
    """
    try:
        result = meraki_client.dashboard.wireless.updateDeviceWirelessElectronicShelfLabel(serial, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_device_wireless_radio_settings",
    description="Update an existing radiosettings"
)
def update_device_wireless_radio_settings(serial: str, **kwargs):
    """
    Update an existing radiosettings
    
    Args:
        serial: Device serial number
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with radiosettings data
    """
    try:
        result = meraki_client.dashboard.wireless.updateDeviceWirelessRadioSettings(serial, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_network_wireless_air_marshal_rule",
    description="Update an existing airmarshalrule"
)
def update_network_wireless_air_marshal_rule(network_id: str, **kwargs):
    """
    Update an existing airmarshalrule
    
    Args:
        network_id: Network ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with airmarshalrule data
    """
    try:
        result = meraki_client.dashboard.wireless.updateNetworkWirelessAirMarshalRule(network_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_network_wireless_air_marshal_settings",
    description="Update an existing airmarshalsettings"
)
def update_network_wireless_air_marshal_settings(network_id: str, **kwargs):
    """
    Update an existing airmarshalsettings
    
    Args:
        network_id: Network ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with airmarshalsettings data
    """
    try:
        result = meraki_client.dashboard.wireless.updateNetworkWirelessAirMarshalSettings(network_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_network_wireless_alternate_management_interface",
    description="Update an existing alternatemanagementinterface"
)
def update_network_wireless_alternate_management_interface(network_id: str, **kwargs):
    """
    Update an existing alternatemanagementinterface
    
    Args:
        network_id: Network ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with alternatemanagementinterface data
    """
    try:
        result = meraki_client.dashboard.wireless.updateNetworkWirelessAlternateManagementInterface(network_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_network_wireless_billing",
    description="Update an existing billing"
)
def update_network_wireless_billing(network_id: str, **kwargs):
    """
    Update an existing billing
    
    Args:
        network_id: Network ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with billing data
    """
    try:
        result = meraki_client.dashboard.wireless.updateNetworkWirelessBilling(network_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_network_wireless_bluetooth_settings",
    description="Update an existing bluetoothsettings"
)
def update_network_wireless_bluetooth_settings(network_id: str, **kwargs):
    """
    Update an existing bluetoothsettings
    
    Args:
        network_id: Network ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with bluetoothsettings data
    """
    try:
        result = meraki_client.dashboard.wireless.updateNetworkWirelessBluetoothSettings(network_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_network_wireless_electronic_shelf_label",
    description="Update an existing electronicshelflabel"
)
def update_network_wireless_electronic_shelf_label(network_id: str, **kwargs):
    """
    Update an existing electronicshelflabel
    
    Args:
        network_id: Network ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with electronicshelflabel data
    """
    try:
        result = meraki_client.dashboard.wireless.updateNetworkWirelessElectronicShelfLabel(network_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_network_wireless_ethernet_ports_profile",
    description="Update an existing ethernetportsprofile"
)
def update_network_wireless_ethernet_ports_profile(network_id: str, profile_id: str, **kwargs):
    """
    Update an existing ethernetportsprofile
    
    Args:
        network_id: Network ID
        profile_id: Profile ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with ethernetportsprofile data
    """
    try:
        result = meraki_client.dashboard.wireless.updateNetworkWirelessEthernetPortsProfile(network_id, profile_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_network_wireless_location_scanning",
    description="Update an existing locationscanning"
)
def update_network_wireless_location_scanning(network_id: str, **kwargs):
    """
    Update an existing locationscanning
    
    Args:
        network_id: Network ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with locationscanning data
    """
    try:
        result = meraki_client.dashboard.wireless.updateNetworkWirelessLocationScanning(network_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_network_wireless_rf_profile",
    description="Update an existing rfprofile"
)
def update_network_wireless_rf_profile(network_id: str, rf_profile_id: str, **kwargs):
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
        result = meraki_client.dashboard.wireless.updateNetworkWirelessRfProfile(network_id, rf_profile_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_network_wireless_settings",
    description="Update an existing settings"
)
def update_network_wireless_settings(network_id: str, **kwargs):
    """
    Update an existing settings
    
    Args:
        network_id: Network ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with settings data
    """
    try:
        result = meraki_client.dashboard.wireless.updateNetworkWirelessSettings(network_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_network_wireless_ssid",
    description="Update an existing ssid"
)
def update_network_wireless_ssid(network_id: str, ssid_number: str, **kwargs):
    """
    Update an existing ssid
    
    Args:
        network_id: Network ID
        ssid_number: SSID number
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with ssid data
    """
    try:
        result = meraki_client.dashboard.wireless.updateNetworkWirelessSsid(network_id, ssid_number, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_network_wireless_ssid_bonjour_forwarding",
    description="Update an existing ssidbonjourforwarding"
)
def update_network_wireless_ssid_bonjour_forwarding(network_id: str, ssid_number: str, **kwargs):
    """
    Update an existing ssidbonjourforwarding
    
    Args:
        network_id: Network ID
        ssid_number: SSID number
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with ssidbonjourforwarding data
    """
    try:
        result = meraki_client.dashboard.wireless.updateNetworkWirelessSsidBonjourForwarding(network_id, ssid_number, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_network_wireless_ssid_device_type_group_policies",
    description="Update an existing ssidtypegrouppolicies"
)
def update_network_wireless_ssid_device_type_group_policies(network_id: str, ssid_number: str, **kwargs):
    """
    Update an existing ssidtypegrouppolicies
    
    Args:
        network_id: Network ID
        ssid_number: SSID number
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with ssidtypegrouppolicies data
    """
    try:
        result = meraki_client.dashboard.wireless.updateNetworkWirelessSsidDeviceTypeGroupPolicies(network_id, ssid_number, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_network_wireless_ssid_eap_override",
    description="Update an existing ssideapoverride"
)
def update_network_wireless_ssid_eap_override(network_id: str, ssid_number: str, **kwargs):
    """
    Update an existing ssideapoverride
    
    Args:
        network_id: Network ID
        ssid_number: SSID number
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with ssideapoverride data
    """
    try:
        result = meraki_client.dashboard.wireless.updateNetworkWirelessSsidEapOverride(network_id, ssid_number, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_network_wireless_ssid_firewall_l3_firewall_rules",
    description="Update an existing ssidfirewalll3firewallrules"
)
def update_network_wireless_ssid_firewall_l3_firewall_rules(network_id: str, ssid_number: str, **kwargs):
    """
    Update an existing ssidfirewalll3firewallrules
    
    Args:
        network_id: Network ID
        ssid_number: SSID number
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with ssidfirewalll3firewallrules data
    """
    try:
        result = meraki_client.dashboard.wireless.updateNetworkWirelessSsidFirewallL3FirewallRules(network_id, ssid_number, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_network_wireless_ssid_firewall_l7_firewall_rules",
    description="Update an existing ssidfirewalll7firewallrules"
)
def update_network_wireless_ssid_firewall_l7_firewall_rules(network_id: str, ssid_number: str, **kwargs):
    """
    Update an existing ssidfirewalll7firewallrules
    
    Args:
        network_id: Network ID
        ssid_number: SSID number
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with ssidfirewalll7firewallrules data
    """
    try:
        result = meraki_client.dashboard.wireless.updateNetworkWirelessSsidFirewallL7FirewallRules(network_id, ssid_number, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_network_wireless_ssid_hotspot20",
    description="Update an existing ssidhotspot20"
)
def update_network_wireless_ssid_hotspot20(network_id: str, ssid_number: str, **kwargs):
    """
    Update an existing ssidhotspot20
    
    Args:
        network_id: Network ID
        ssid_number: SSID number
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with ssidhotspot20 data
    """
    try:
        result = meraki_client.dashboard.wireless.updateNetworkWirelessSsidHotspot20(network_id, ssid_number, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_network_wireless_ssid_identity_psk",
    description="Update an existing ssididentitypsk"
)
def update_network_wireless_ssid_identity_psk(network_id: str, ssid_number: str, **kwargs):
    """
    Update an existing ssididentitypsk
    
    Args:
        network_id: Network ID
        ssid_number: SSID number
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with ssididentitypsk data
    """
    try:
        result = meraki_client.dashboard.wireless.updateNetworkWirelessSsidIdentityPsk(network_id, ssid_number, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_network_wireless_ssid_schedules",
    description="Update an existing ssidschedules"
)
def update_network_wireless_ssid_schedules(network_id: str, ssid_number: str, **kwargs):
    """
    Update an existing ssidschedules
    
    Args:
        network_id: Network ID
        ssid_number: SSID number
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with ssidschedules data
    """
    try:
        result = meraki_client.dashboard.wireless.updateNetworkWirelessSsidSchedules(network_id, ssid_number, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_network_wireless_ssid_splash_settings",
    description="Update an existing ssidsplashsettings"
)
def update_network_wireless_ssid_splash_settings(network_id: str, ssid_number: str, **kwargs):
    """
    Update an existing ssidsplashsettings
    
    Args:
        network_id: Network ID
        ssid_number: SSID number
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with ssidsplashsettings data
    """
    try:
        result = meraki_client.dashboard.wireless.updateNetworkWirelessSsidSplashSettings(network_id, ssid_number, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_network_wireless_ssid_traffic_shaping_rules",
    description="Update an existing ssidtrafficshapingrules"
)
def update_network_wireless_ssid_traffic_shaping_rules(network_id: str, ssid_number: str, **kwargs):
    """
    Update an existing ssidtrafficshapingrules
    
    Args:
        network_id: Network ID
        ssid_number: SSID number
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with ssidtrafficshapingrules data
    """
    try:
        result = meraki_client.dashboard.wireless.updateNetworkWirelessSsidTrafficShapingRules(network_id, ssid_number, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_network_wireless_ssid_vpn",
    description="Update an existing ssidvpn"
)
def update_network_wireless_ssid_vpn(network_id: str, ssid_number: str, **kwargs):
    """
    Update an existing ssidvpn
    
    Args:
        network_id: Network ID
        ssid_number: SSID number
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with ssidvpn data
    """
    try:
        result = meraki_client.dashboard.wireless.updateNetworkWirelessSsidVpn(network_id, ssid_number, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_organization_wireless_devices_radsec_certificates_authorities",
    description="Update an existing sradseccertificatesauthorities"
)
def update_organization_wireless_devices_radsec_certificates_authorities(organization_id: str, **kwargs):
    """
    Update an existing sradseccertificatesauthorities
    
    Args:
        organization_id: Organization ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with sradseccertificatesauthorities data
    """
    try:
        result = meraki_client.dashboard.wireless.updateOrganizationWirelessDevicesRadsecCertificatesAuthorities(organization_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_organization_wireless_location_scanning_receiver",
    description="Update an existing locationscanningreceiver"
)
def update_organization_wireless_location_scanning_receiver(organization_id: str, **kwargs):
    """
    Update an existing locationscanningreceiver
    
    Args:
        organization_id: Organization ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with locationscanningreceiver data
    """
    try:
        result = meraki_client.dashboard.wireless.updateOrganizationWirelessLocationScanningReceiver(organization_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_organization_wireless_ssids_firewall_isolation_allowlist_entry",
    description="Update an existing ssidsfirewallisolationallowlistentry"
)
def update_organization_wireless_ssids_firewall_isolation_allowlist_entry(organization_id: str, ssid_number: str, **kwargs):
    """
    Update an existing ssidsfirewallisolationallowlistentry
    
    Args:
        organization_id: Organization ID
        ssid_number: SSID number
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with ssidsfirewallisolationallowlistentry data
    """
    try:
        result = meraki_client.dashboard.wireless.updateOrganizationWirelessSsidsFirewallIsolationAllowlistEntry(organization_id, ssid_number, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}