"""
Additional Wireless endpoints for Cisco Meraki MCP Server.
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

def register_wireless_additional_tools(mcp_app, meraki):
    """Register additional wireless tools with the MCP server."""
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    
    # Register all additional tools
    register_wireless_additional_handlers()

def register_wireless_additional_handlers():
    """Register additional wireless tool handlers."""

    @app.tool(
        name="create_network_wireless_air_marshal_rule",
        description="➕ Create network wireless air marshal rule"
    )
    def create_network_wireless_air_marshal_rule(network_id: str, **kwargs):
        """Create network wireless air marshal rule."""
        try:
            result = meraki_client.dashboard.wireless.createNetworkWirelessAirMarshalRule(
                network_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Wireless Air Marshal Rule")
            elif isinstance(result, list):
                return format_list_response(result, "Network Wireless Air Marshal Rule")
            else:
                return f"✅ Create network wireless air marshal rule completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="create_org_wireless_radsec_cert_auth",
        description="➕ Create organization wireless devices radsec certificates authority"
    )
    def create_organization_wireless_devices_radsec_certificates_authority(organization_id: str, **kwargs):
        """Create organization wireless devices radsec certificates authority."""
        try:
            result = meraki_client.dashboard.wireless.createOrganizationWirelessDevicesRadsecCertificatesAuthority(
                organization_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Wireless Devices Radsec Certificates Authority")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Wireless Devices Radsec Certificates Authority")
            else:
                return f"✅ Create organization wireless devices radsec certificates authority completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="create_organization_wireless_location_scanning_receiver",
        description="➕ Create organization wireless location scanning receiver"
    )
    def create_organization_wireless_location_scanning_receiver(organization_id: str, **kwargs):
        """Create organization wireless location scanning receiver."""
        try:
            result = meraki_client.dashboard.wireless.createOrganizationWirelessLocationScanningReceiver(
                organization_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Wireless Location Scanning Receiver")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Wireless Location Scanning Receiver")
            else:
                return f"✅ Create organization wireless location scanning receiver completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="create_org_wireless_ssid_allowlist",
        description="➕ Create organization wireless ssids firewall isolation allowlist entry"
    )
    def create_organization_wireless_ssids_firewall_isolation_allowlist_entry(organization_id: str, **kwargs):
        """Create organization wireless ssids firewall isolation allowlist entry."""
        try:
            result = meraki_client.dashboard.wireless.createOrganizationWirelessSsidsFirewallIsolationAllowlistEntry(
                organization_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Wireless Ssids Firewall Isolation Allowlist Entry")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Wireless Ssids Firewall Isolation Allowlist Entry")
            else:
                return f"✅ Create organization wireless ssids firewall isolation allowlist entry completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="delete_network_wireless_air_marshal_rule",
        description="🗑️ Delete network wireless air marshal rule"
    )
    def delete_network_wireless_air_marshal_rule(network_id: str):
        """Delete network wireless air marshal rule."""
        try:
            result = meraki_client.dashboard.wireless.deleteNetworkWirelessAirMarshalRule(
                network_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Wireless Air Marshal Rule")
            elif isinstance(result, list):
                return format_list_response(result, "Network Wireless Air Marshal Rule")
            else:
                return f"✅ Delete network wireless air marshal rule completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="delete_organization_wireless_location_scanning_receiver",
        description="🗑️ Delete organization wireless location scanning receiver"
    )
    def delete_organization_wireless_location_scanning_receiver(organization_id: str):
        """Delete organization wireless location scanning receiver."""
        try:
            result = meraki_client.dashboard.wireless.deleteOrganizationWirelessLocationScanningReceiver(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Wireless Location Scanning Receiver")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Wireless Location Scanning Receiver")
            else:
                return f"✅ Delete organization wireless location scanning receiver completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="delete_org_wireless_ssid_allowlist",
        description="🗑️ Delete organization wireless ssids firewall isolation allowlist entry"
    )
    def delete_organization_wireless_ssids_firewall_isolation_allowlist_entry(organization_id: str):
        """Delete organization wireless ssids firewall isolation allowlist entry."""
        try:
            result = meraki_client.dashboard.wireless.deleteOrganizationWirelessSsidsFirewallIsolationAllowlistEntry(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Wireless Ssids Firewall Isolation Allowlist Entry")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Wireless Ssids Firewall Isolation Allowlist Entry")
            else:
                return f"✅ Delete organization wireless ssids firewall isolation allowlist entry completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_device_wireless_bluetooth_settings",
        description="📊 Get device wireless bluetooth settings"
    )
    def get_device_wireless_bluetooth_settings(serial: str):
        """Get device wireless bluetooth settings."""
        try:
            result = meraki_client.dashboard.wireless.getDeviceWirelessBluetoothSettings(
                serial
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Device Wireless Bluetooth Settings")
            elif isinstance(result, list):
                return format_list_response(result, "Device Wireless Bluetooth Settings")
            else:
                return f"✅ Get device wireless bluetooth settings completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_device_wireless_connection_stats",
        description="📊 Get device wireless connection stats"
    )
    def get_device_wireless_connection_stats(serial: str):
        """Get device wireless connection stats."""
        try:
            result = meraki_client.dashboard.wireless.getDeviceWirelessConnectionStats(
                serial
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Device Wireless Connection Stats")
            elif isinstance(result, list):
                return format_list_response(result, "Device Wireless Connection Stats")
            else:
                return f"✅ Get device wireless connection stats completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_device_wireless_electronic_shelf_label",
        description="📊 Get device wireless electronic shelf label"
    )
    def get_device_wireless_electronic_shelf_label(serial: str):
        """Get device wireless electronic shelf label."""
        try:
            result = meraki_client.dashboard.wireless.getDeviceWirelessElectronicShelfLabel(
                serial
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Device Wireless Electronic Shelf Label")
            elif isinstance(result, list):
                return format_list_response(result, "Device Wireless Electronic Shelf Label")
            else:
                return f"✅ Get device wireless electronic shelf label completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_device_wireless_latency_stats",
        description="📊 Get device wireless latency stats"
    )
    def get_device_wireless_latency_stats(serial: str):
        """Get device wireless latency stats."""
        try:
            result = meraki_client.dashboard.wireless.getDeviceWirelessLatencyStats(
                serial
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Device Wireless Latency Stats")
            elif isinstance(result, list):
                return format_list_response(result, "Device Wireless Latency Stats")
            else:
                return f"✅ Get device wireless latency stats completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_device_wireless_radio_settings",
        description="📊 Get device wireless radio settings"
    )
    def get_device_wireless_radio_settings(serial: str):
        """Get device wireless radio settings."""
        try:
            result = meraki_client.dashboard.wireless.getDeviceWirelessRadioSettings(
                serial
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Device Wireless Radio Settings")
            elif isinstance(result, list):
                return format_list_response(result, "Device Wireless Radio Settings")
            else:
                return f"✅ Get device wireless radio settings completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_device_wireless_status",
        description="📊 Get device wireless status"
    )
    def get_device_wireless_status(serial: str):
        """Get device wireless status."""
        try:
            result = meraki_client.dashboard.wireless.getDeviceWirelessStatus(
                serial
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Device Wireless Status")
            elif isinstance(result, list):
                return format_list_response(result, "Device Wireless Status")
            else:
                return f"✅ Get device wireless status completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_network_wireless_client_connection_stats",
        description="📊 Get network wireless client connection stats"
    )
    def get_network_wireless_client_connection_stats(network_id: str):
        """Get network wireless client connection stats."""
        try:
            result = meraki_client.dashboard.wireless.getNetworkWirelessClientConnectionStats(
                network_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Wireless Client Connection Stats")
            elif isinstance(result, list):
                return format_list_response(result, "Network Wireless Client Connection Stats")
            else:
                return f"✅ Get network wireless client connection stats completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_network_wireless_client_connectivity_events",
        description="📊 Get network wireless client connectivity events"
    )
    def get_network_wireless_client_connectivity_events(network_id: str):
        """Get network wireless client connectivity events."""
        try:
            result = meraki_client.dashboard.wireless.getNetworkWirelessClientConnectivityEvents(
                network_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Wireless Client Connectivity Events")
            elif isinstance(result, list):
                return format_list_response(result, "Network Wireless Client Connectivity Events")
            else:
                return f"✅ Get network wireless client connectivity events completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_network_wireless_client_latency_history",
        description="📊 Get network wireless client latency history"
    )
    def get_network_wireless_client_latency_history(network_id: str):
        """Get network wireless client latency history."""
        try:
            result = meraki_client.dashboard.wireless.getNetworkWirelessClientLatencyHistory(
                network_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Wireless Client Latency History")
            elif isinstance(result, list):
                return format_list_response(result, "Network Wireless Client Latency History")
            else:
                return f"✅ Get network wireless client latency history completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_network_wireless_client_latency_stats",
        description="📊 Get network wireless client latency stats"
    )
    def get_network_wireless_client_latency_stats(network_id: str):
        """Get network wireless client latency stats."""
        try:
            result = meraki_client.dashboard.wireless.getNetworkWirelessClientLatencyStats(
                network_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Wireless Client Latency Stats")
            elif isinstance(result, list):
                return format_list_response(result, "Network Wireless Client Latency Stats")
            else:
                return f"✅ Get network wireless client latency stats completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_network_wireless_clients_connection_stats",
        description="📊 Get network wireless clients connection stats"
    )
    def get_network_wireless_clients_connection_stats(network_id: str):
        """Get network wireless clients connection stats."""
        try:
            result = meraki_client.dashboard.wireless.getNetworkWirelessClientsConnectionStats(
                network_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Wireless Clients Connection Stats")
            elif isinstance(result, list):
                return format_list_response(result, "Network Wireless Clients Connection Stats")
            else:
                return f"✅ Get network wireless clients connection stats completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_network_wireless_clients_latency_stats",
        description="📊 Get network wireless clients latency stats"
    )
    def get_network_wireless_clients_latency_stats(network_id: str):
        """Get network wireless clients latency stats."""
        try:
            result = meraki_client.dashboard.wireless.getNetworkWirelessClientsLatencyStats(
                network_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Wireless Clients Latency Stats")
            elif isinstance(result, list):
                return format_list_response(result, "Network Wireless Clients Latency Stats")
            else:
                return f"✅ Get network wireless clients latency stats completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_network_wireless_devices_connection_stats",
        description="📊 Get network wireless devices connection stats"
    )
    def get_network_wireless_devices_connection_stats(network_id: str):
        """Get network wireless devices connection stats."""
        try:
            result = meraki_client.dashboard.wireless.getNetworkWirelessDevicesConnectionStats(
                network_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Wireless Devices Connection Stats")
            elif isinstance(result, list):
                return format_list_response(result, "Network Wireless Devices Connection Stats")
            else:
                return f"✅ Get network wireless devices connection stats completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_network_wireless_electronic_shelf_label_configured_devices",
        description="📊 Get network wireless electronic shelf label configured devices"
    )
    def get_network_wireless_electronic_shelf_label_configured_devices(network_id: str):
        """Get network wireless electronic shelf label configured devices."""
        try:
            result = meraki_client.dashboard.wireless.getNetworkWirelessElectronicShelfLabelConfiguredDevices(
                network_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Wireless Electronic Shelf Label Configured Devices")
            elif isinstance(result, list):
                return format_list_response(result, "Network Wireless Electronic Shelf Label Configured Devices")
            else:
                return f"✅ Get network wireless electronic shelf label configured devices completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_network_wireless_ethernet_ports_profile",
        description="📊 Get network wireless ethernet ports profile"
    )
    def get_network_wireless_ethernet_ports_profile(network_id: str):
        """Get network wireless ethernet ports profile."""
        try:
            result = meraki_client.dashboard.wireless.getNetworkWirelessEthernetPortsProfile(
                network_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Wireless Ethernet Ports Profile")
            elif isinstance(result, list):
                return format_list_response(result, "Network Wireless Ethernet Ports Profile")
            else:
                return f"✅ Get network wireless ethernet ports profile completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_network_wireless_rf_profile",
        description="📊 Get network wireless rf profile"
    )
    def get_network_wireless_rf_profile(network_id: str):
        """Get network wireless rf profile."""
        try:
            result = meraki_client.dashboard.wireless.getNetworkWirelessRfProfile(
                network_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Wireless Rf Profile")
            elif isinstance(result, list):
                return format_list_response(result, "Network Wireless Rf Profile")
            else:
                return f"✅ Get network wireless rf profile completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_network_wireless_ssid_identity_psk",
        description="📊 Get network wireless ssid identity psk"
    )
    def get_network_wireless_ssid_identity_psk(network_id: str):
        """Get network wireless ssid identity psk."""
        try:
            result = meraki_client.dashboard.wireless.getNetworkWirelessSsidIdentityPsk(
                network_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Wireless Ssid Identity Psk")
            elif isinstance(result, list):
                return format_list_response(result, "Network Wireless Ssid Identity Psk")
            else:
                return f"✅ Get network wireless ssid identity psk completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_wireless_air_marshal_rules",
        description="📊 Get organization wireless air marshal rules"
    )
    def get_organization_wireless_air_marshal_rules(organization_id: str):
        """Get organization wireless air marshal rules."""
        try:
            result = meraki_client.dashboard.wireless.getOrganizationWirelessAirMarshalRules(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Wireless Air Marshal Rules")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Wireless Air Marshal Rules")
            else:
                return f"✅ Get organization wireless air marshal rules completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_wireless_air_marshal_settings_by_network",
        description="📊 Get organization wireless air marshal settings by network"
    )
    def get_organization_wireless_air_marshal_settings_by_network(organization_id: str):
        """Get organization wireless air marshal settings by network."""
        try:
            result = meraki_client.dashboard.wireless.getOrganizationWirelessAirMarshalSettingsByNetwork(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Wireless Air Marshal Settings By Network")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Wireless Air Marshal Settings By Network")
            else:
                return f"✅ Get organization wireless air marshal settings by network completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_wireless_clients_overview_by_device",
        description="📊 Get organization wireless clients overview by device"
    )
    def get_organization_wireless_clients_overview_by_device(organization_id: str):
        """Get organization wireless clients overview by device."""
        try:
            result = meraki_client.dashboard.wireless.getOrganizationWirelessClientsOverviewByDevice(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Wireless Clients Overview By Device")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Wireless Clients Overview By Device")
            else:
                return f"✅ Get organization wireless clients overview by device completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_wireless_devices_ethernet_statuses",
        description="📊 Get organization wireless devices ethernet statuses"
    )
    def get_organization_wireless_devices_ethernet_statuses(organization_id: str):
        """Get organization wireless devices ethernet statuses."""
        try:
            result = meraki_client.dashboard.wireless.getOrganizationWirelessDevicesEthernetStatuses(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Wireless Devices Ethernet Statuses")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Wireless Devices Ethernet Statuses")
            else:
                return f"✅ Get organization wireless devices ethernet statuses completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_wireless_devices_power_mode_history",
        description="📊 Get organization wireless devices power mode history"
    )
    def get_organization_wireless_devices_power_mode_history(organization_id: str):
        """Get organization wireless devices power mode history."""
        try:
            result = meraki_client.dashboard.wireless.getOrganizationWirelessDevicesPowerModeHistory(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Wireless Devices Power Mode History")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Wireless Devices Power Mode History")
            else:
                return f"✅ Get organization wireless devices power mode history completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_org_wireless_radsec_cert_auths",
        description="📊 Get organization wireless devices radsec certificates authorities"
    )
    def get_organization_wireless_devices_radsec_certificates_authorities(organization_id: str):
        """Get organization wireless devices radsec certificates authorities."""
        try:
            result = meraki_client.dashboard.wireless.getOrganizationWirelessDevicesRadsecCertificatesAuthorities(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Wireless Devices Radsec Certificates Authorities")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Wireless Devices Radsec Certificates Authorities")
            else:
                return f"✅ Get organization wireless devices radsec certificates authorities completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_org_wireless_radsec_crls",
        description="📊 Get organization wireless devices radsec certificates authorities crls"
    )
    def get_organization_wireless_devices_radsec_certificates_authorities_crls(organization_id: str):
        """Get organization wireless devices radsec certificates authorities crls."""
        try:
            result = meraki_client.dashboard.wireless.getOrganizationWirelessDevicesRadsecCertificatesAuthoritiesCrls(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Wireless Devices Radsec Certificates Authorities Crls")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Wireless Devices Radsec Certificates Authorities Crls")
            else:
                return f"✅ Get organization wireless devices radsec certificates authorities crls completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_org_wireless_radsec_crl_deltas",
        description="📊 Get organization wireless devices radsec certificates authorities crls deltas"
    )
    def get_organization_wireless_devices_radsec_certificates_authorities_crls_deltas(organization_id: str):
        """Get organization wireless devices radsec certificates authorities crls deltas."""
        try:
            result = meraki_client.dashboard.wireless.getOrganizationWirelessDevicesRadsecCertificatesAuthoritiesCrlsDeltas(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Wireless Devices Radsec Certificates Authorities Crls Deltas")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Wireless Devices Radsec Certificates Authorities Crls Deltas")
            else:
                return f"✅ Get organization wireless devices radsec certificates authorities crls deltas completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_wireless_devices_system_cpu_load_history",
        description="📊 Get organization wireless devices system cpu load history"
    )
    def get_organization_wireless_devices_system_cpu_load_history(organization_id: str):
        """Get organization wireless devices system cpu load history."""
        try:
            result = meraki_client.dashboard.wireless.getOrganizationWirelessDevicesSystemCpuLoadHistory(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Wireless Devices System Cpu Load History")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Wireless Devices System Cpu Load History")
            else:
                return f"✅ Get organization wireless devices system cpu load history completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_wireless_devices_wireless_controllers_by_device",
        description="📊 Get organization wireless devices wireless controllers by device"
    )
    def get_organization_wireless_devices_wireless_controllers_by_device(organization_id: str):
        """Get organization wireless devices wireless controllers by device."""
        try:
            result = meraki_client.dashboard.wireless.getOrganizationWirelessDevicesWirelessControllersByDevice(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Wireless Devices Wireless Controllers By Device")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Wireless Devices Wireless Controllers By Device")
            else:
                return f"✅ Get organization wireless devices wireless controllers by device completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_wireless_location_scanning_by_network",
        description="📊 Get organization wireless location scanning by network"
    )
    def get_organization_wireless_location_scanning_by_network(organization_id: str):
        """Get organization wireless location scanning by network."""
        try:
            result = meraki_client.dashboard.wireless.getOrganizationWirelessLocationScanningByNetwork(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Wireless Location Scanning By Network")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Wireless Location Scanning By Network")
            else:
                return f"✅ Get organization wireless location scanning by network completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_wireless_location_scanning_receivers",
        description="📊 Get organization wireless location scanning receivers"
    )
    def get_organization_wireless_location_scanning_receivers(organization_id: str):
        """Get organization wireless location scanning receivers."""
        try:
            result = meraki_client.dashboard.wireless.getOrganizationWirelessLocationScanningReceivers(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Wireless Location Scanning Receivers")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Wireless Location Scanning Receivers")
            else:
                return f"✅ Get organization wireless location scanning receivers completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_wireless_rf_profiles_assignments_by_device",
        description="📊 Get organization wireless rf profiles assignments by device"
    )
    def get_organization_wireless_rf_profiles_assignments_by_device(organization_id: str):
        """Get organization wireless rf profiles assignments by device."""
        try:
            result = meraki_client.dashboard.wireless.getOrganizationWirelessRfProfilesAssignmentsByDevice(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Wireless Rf Profiles Assignments By Device")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Wireless Rf Profiles Assignments By Device")
            else:
                return f"✅ Get organization wireless rf profiles assignments by device completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_org_wireless_ssid_allowlist",
        description="📊 Get organization wireless ssids firewall isolation allowlist entries"
    )
    def get_organization_wireless_ssids_firewall_isolation_allowlist_entries(organization_id: str):
        """Get organization wireless ssids firewall isolation allowlist entries."""
        try:
            result = meraki_client.dashboard.wireless.getOrganizationWirelessSsidsFirewallIsolationAllowlistEntries(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Wireless Ssids Firewall Isolation Allowlist Entries")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Wireless Ssids Firewall Isolation Allowlist Entries")
            else:
                return f"✅ Get organization wireless ssids firewall isolation allowlist entries completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_wireless_ssids_statuses_by_device",
        description="📊 Get organization wireless ssids statuses by device"
    )
    def get_organization_wireless_ssids_statuses_by_device(organization_id: str):
        """Get organization wireless ssids statuses by device."""
        try:
            result = meraki_client.dashboard.wireless.getOrganizationWirelessSsidsStatusesByDevice(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Wireless Ssids Statuses By Device")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Wireless Ssids Statuses By Device")
            else:
                return f"✅ Get organization wireless ssids statuses by device completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="recalculate_organization_wireless_radio_auto_rf_channels",
        description="⚡ Execute organization wireless radio auto rf channels"
    )
    def recalculate_organization_wireless_radio_auto_rf_channels(organization_id: str):
        """Execute organization wireless radio auto rf channels."""
        try:
            result = meraki_client.dashboard.wireless.recalculateOrganizationWirelessRadioAutoRfChannels(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Wireless Radio Auto Rf Channels")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Wireless Radio Auto Rf Channels")
            else:
                return f"✅ Execute organization wireless radio auto rf channels completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="set_network_wireless_ethernet_ports_profiles_default",
        description="⚡ Execute network wireless ethernet ports profiles default"
    )
    def set_network_wireless_ethernet_ports_profiles_default(network_id: str):
        """Execute network wireless ethernet ports profiles default."""
        try:
            result = meraki_client.dashboard.wireless.setNetworkWirelessEthernetPortsProfilesDefault(
                network_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Wireless Ethernet Ports Profiles Default")
            elif isinstance(result, list):
                return format_list_response(result, "Network Wireless Ethernet Ports Profiles Default")
            else:
                return f"✅ Execute network wireless ethernet ports profiles default completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="update_device_wireless_bluetooth_settings",
        description="✏️ Update device wireless bluetooth settings"
    )
    def update_device_wireless_bluetooth_settings(serial: str, **kwargs):
        """Update device wireless bluetooth settings."""
        try:
            result = meraki_client.dashboard.wireless.updateDeviceWirelessBluetoothSettings(
                serial, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Device Wireless Bluetooth Settings")
            elif isinstance(result, list):
                return format_list_response(result, "Device Wireless Bluetooth Settings")
            else:
                return f"✅ Update device wireless bluetooth settings completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="update_device_wireless_electronic_shelf_label",
        description="✏️ Update device wireless electronic shelf label"
    )
    def update_device_wireless_electronic_shelf_label(serial: str, **kwargs):
        """Update device wireless electronic shelf label."""
        try:
            result = meraki_client.dashboard.wireless.updateDeviceWirelessElectronicShelfLabel(
                serial, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Device Wireless Electronic Shelf Label")
            elif isinstance(result, list):
                return format_list_response(result, "Device Wireless Electronic Shelf Label")
            else:
                return f"✅ Update device wireless electronic shelf label completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="update_device_wireless_radio_settings",
        description="✏️ Update device wireless radio settings"
    )
    def update_device_wireless_radio_settings(serial: str, **kwargs):
        """Update device wireless radio settings."""
        try:
            result = meraki_client.dashboard.wireless.updateDeviceWirelessRadioSettings(
                serial, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Device Wireless Radio Settings")
            elif isinstance(result, list):
                return format_list_response(result, "Device Wireless Radio Settings")
            else:
                return f"✅ Update device wireless radio settings completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="update_network_wireless_air_marshal_rule",
        description="✏️ Update network wireless air marshal rule"
    )
    def update_network_wireless_air_marshal_rule(network_id: str, **kwargs):
        """Update network wireless air marshal rule."""
        try:
            result = meraki_client.dashboard.wireless.updateNetworkWirelessAirMarshalRule(
                network_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Wireless Air Marshal Rule")
            elif isinstance(result, list):
                return format_list_response(result, "Network Wireless Air Marshal Rule")
            else:
                return f"✅ Update network wireless air marshal rule completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="update_network_wireless_air_marshal_settings",
        description="✏️ Update network wireless air marshal settings"
    )
    def update_network_wireless_air_marshal_settings(network_id: str, **kwargs):
        """Update network wireless air marshal settings."""
        try:
            result = meraki_client.dashboard.wireless.updateNetworkWirelessAirMarshalSettings(
                network_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Wireless Air Marshal Settings")
            elif isinstance(result, list):
                return format_list_response(result, "Network Wireless Air Marshal Settings")
            else:
                return f"✅ Update network wireless air marshal settings completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="update_network_wireless_location_scanning",
        description="✏️ Update network wireless location scanning"
    )
    def update_network_wireless_location_scanning(network_id: str, **kwargs):
        """Update network wireless location scanning."""
        try:
            result = meraki_client.dashboard.wireless.updateNetworkWirelessLocationScanning(
                network_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Wireless Location Scanning")
            elif isinstance(result, list):
                return format_list_response(result, "Network Wireless Location Scanning")
            else:
                return f"✅ Update network wireless location scanning completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="update_org_wireless_radsec_cert_auth",
        description="✏️ Update organization wireless devices radsec certificates authorities"
    )
    def update_organization_wireless_devices_radsec_certificates_authorities(organization_id: str, **kwargs):
        """Update organization wireless devices radsec certificates authorities."""
        try:
            result = meraki_client.dashboard.wireless.updateOrganizationWirelessDevicesRadsecCertificatesAuthorities(
                organization_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Wireless Devices Radsec Certificates Authorities")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Wireless Devices Radsec Certificates Authorities")
            else:
                return f"✅ Update organization wireless devices radsec certificates authorities completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="update_organization_wireless_location_scanning_receiver",
        description="✏️ Update organization wireless location scanning receiver"
    )
    def update_organization_wireless_location_scanning_receiver(organization_id: str, **kwargs):
        """Update organization wireless location scanning receiver."""
        try:
            result = meraki_client.dashboard.wireless.updateOrganizationWirelessLocationScanningReceiver(
                organization_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Wireless Location Scanning Receiver")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Wireless Location Scanning Receiver")
            else:
                return f"✅ Update organization wireless location scanning receiver completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="update_org_wireless_ssid_allowlist",
        description="✏️ Update organization wireless ssids firewall isolation allowlist entry"
    )
    def update_organization_wireless_ssids_firewall_isolation_allowlist_entry(organization_id: str, **kwargs):
        """Update organization wireless ssids firewall isolation allowlist entry."""
        try:
            result = meraki_client.dashboard.wireless.updateOrganizationWirelessSsidsFirewallIsolationAllowlistEntry(
                organization_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Wireless Ssids Firewall Isolation Allowlist Entry")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Wireless Ssids Firewall Isolation Allowlist Entry")
            else:
                return f"✅ Update organization wireless ssids firewall isolation allowlist entry completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"
