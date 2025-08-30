"""
Wireless Client Analytics and Health Tools for the Cisco Meraki MCP Server.
Implements client health scores, connection stats, and detailed client analytics.
Previously named tools_wireless_100.py
"""

from typing import Optional, List, Dict, Any
import json

# Global variables to store app and meraki client
app = None
meraki_client = None

def register_wireless_100_tools(mcp_app, meraki):
    """
    Register wireless client analytics and health monitoring tools.
    Includes client health scores, connection stats, and identity PSK management.
    
    Args:
        mcp_app: MCP server instance
        meraki: Meraki client instance
    """
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    
    # Register all client analytics and health tool handlers
    register_identity_psk_crud_tools()
    register_client_specific_stats_tools()
    register_rf_profile_crud_tools()
    register_radio_settings_tools()
    register_update_operations_tools()
    register_specialized_features_tools()

# ==================== IDENTITY PSK CRUD ====================

def register_identity_psk_crud_tools():
    """Register Identity PSK CRUD operations."""
    
    @app.tool(
        name="get_network_wireless_ssid_identity_psk",
        description="📡🔑 Get a specific identity PSK by ID"
    )
    def get_network_wireless_ssid_identity_psk(
        network_id: str,
        number: str,
        identity_psk_id: str
    ):
        """Get a specific identity PSK."""
        try:
            result = meraki_client.dashboard.wireless.getNetworkWirelessSsidIdentityPsk(
                network_id, number, identity_psk_id
            )
            
            response = f"# 🔑 Identity PSK Details\n\n"
            response += f"**ID**: {result.get('id')}\n"
            response += f"**Name**: {result.get('name')}\n"
            response += f"**Email**: {result.get('email', 'N/A')}\n"
            response += f"**Passphrase**: {'[SET]' if result.get('passphrase') else '[NOT SET]'}\n"
            response += f"**Group Policy ID**: {result.get('groupPolicyId', 'None')}\n"
            response += f"**Expires At**: {result.get('expiresAt', 'Never')}\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error getting identity PSK: {str(e)}"
    
    # DUPLICATE: Commented out - also defined in tools_wireless_advanced.py
    '''
    @app.tool(
        name="create_network_wireless_ssid_identity_psk",
        description="📡🔑 Create a new identity PSK"
    )
    def create_network_wireless_ssid_identity_psk(
        network_id: str,
        number: str,
        name: str,
        passphrase: Optional[str] = None,
        group_policy_id: Optional[str] = None,
        email: Optional[str] = None,
        expires_at: Optional[str] = None
    ):
        """Create a new identity PSK."""
        try:
            kwargs = {'name': name}
            
            if passphrase:
                kwargs['passphrase'] = passphrase
            if group_policy_id:
                kwargs['groupPolicyId'] = group_policy_id
            if email:
                kwargs['email'] = email
            if expires_at:
                kwargs['expiresAt'] = expires_at
            
            result = meraki_client.dashboard.wireless.createNetworkWirelessSsidIdentityPsk(
                network_id, number, **kwargs
            )
            
            return f"✅ Created identity PSK '{result.get('name')}' - ID: {result.get('id')}"
            
        except Exception as e:
            return f"❌ Error creating identity PSK: {str(e)}"
    '''
    
    # DUPLICATE: Commented out - also defined in tools_wireless_advanced.py
    '''
    @app.tool(
        name="update_network_wireless_ssid_identity_psk",
        description="📡🔑 Update an existing identity PSK"
    )
    def update_network_wireless_ssid_identity_psk(
        network_id: str,
        number: str,
        identity_psk_id: str,
        name: Optional[str] = None,
        passphrase: Optional[str] = None,
        group_policy_id: Optional[str] = None,
        email: Optional[str] = None,
        expires_at: Optional[str] = None
    ):
        """Update an identity PSK."""
        try:
            kwargs = {}
            
            if name:
                kwargs['name'] = name
            if passphrase:
                kwargs['passphrase'] = passphrase
            if group_policy_id:
                kwargs['groupPolicyId'] = group_policy_id
            if email:
                kwargs['email'] = email
            if expires_at:
                kwargs['expiresAt'] = expires_at
            
            result = meraki_client.dashboard.wireless.updateNetworkWirelessSsidIdentityPsk(
                network_id, number, identity_psk_id, **kwargs
            )
            
            return f"✅ Updated identity PSK '{result.get('name')}'"
            
        except Exception as e:
            return f"❌ Error updating identity PSK: {str(e)}"
    '''
    
    # DUPLICATE: Commented out - also defined in tools_wireless_advanced.py
    '''
    @app.tool(
        name="delete_network_wireless_ssid_identity_psk",
        description="📡🔑 Delete an identity PSK"
    )
    def delete_network_wireless_ssid_identity_psk(
        network_id: str,
        number: str,
        identity_psk_id: str
    ):
        """Delete an identity PSK."""
        try:
            meraki_client.dashboard.wireless.deleteNetworkWirelessSsidIdentityPsk(
                network_id, number, identity_psk_id
            )
            
            return f"✅ Deleted identity PSK {identity_psk_id}"
            
        except Exception as e:
            return f"❌ Error deleting identity PSK: {str(e)}"
    '''

# ==================== CLIENT-SPECIFIC STATS ====================

def register_client_specific_stats_tools():
    """Register client-specific statistics tools."""
    
    @app.tool(
        name="get_network_wireless_client_latency_stats",
        description="📡📊 Get latency stats for a specific wireless client (REQUIRES: client_id)"
    )
    def get_network_wireless_client_latency_stats(
        network_id: str,
        client_id: str,
        t0: Optional[str] = None,
        t1: Optional[str] = None,
        timespan: Optional[float] = 86400,
        band: Optional[str] = None,
        ssid: Optional[int] = None,
        vlan: Optional[int] = None,
        ap_tag: Optional[str] = None,
        fields: Optional[str] = None
    ):
        """Get latency statistics for a specific client."""
        try:
            kwargs = {}
            
            if t0:
                kwargs['t0'] = t0
            if t1:
                kwargs['t1'] = t1
            if timespan:
                kwargs['timespan'] = timespan
            if band:
                kwargs['band'] = band
            if ssid is not None:
                kwargs['ssid'] = ssid
            if vlan is not None:
                kwargs['vlan'] = vlan
            if ap_tag:
                kwargs['apTag'] = ap_tag
            if fields:
                kwargs['fields'] = fields
            
            result = meraki_client.dashboard.wireless.getNetworkWirelessClientLatencyStats(
                network_id, client_id, **kwargs
            )
            
            response = f"# 📊 Client {client_id} - Latency Stats\n\n"
            
            if isinstance(result, dict):
                response += f"**Background Traffic**: {result.get('backgroundTraffic', {}).get('avg', 0):.1f} ms avg\n"
                response += f"**Best Effort**: {result.get('bestEffortTraffic', {}).get('avg', 0):.1f} ms avg\n"
                response += f"**Video**: {result.get('videoTraffic', {}).get('avg', 0):.1f} ms avg\n"
                response += f"**Voice**: {result.get('voiceTraffic', {}).get('avg', 0):.1f} ms avg\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error getting client latency stats: {str(e)}"
    
    @app.tool(
        name="get_network_wireless_clients_connection_stats",
        description="📡📊 Get connection stats for multiple wireless clients"
    )
    def get_network_wireless_clients_connection_stats(
        network_id: str,
        t0: Optional[str] = None,
        t1: Optional[str] = None,
        timespan: Optional[float] = 86400,
        band: Optional[str] = None,
        ssid: Optional[int] = None,
        vlan: Optional[int] = None,
        ap_tag: Optional[str] = None
    ):
        """Get connection statistics for multiple clients."""
        try:
            kwargs = {}
            
            if t0:
                kwargs['t0'] = t0
            if t1:
                kwargs['t1'] = t1
            if timespan:
                kwargs['timespan'] = timespan
            if band:
                kwargs['band'] = band
            if ssid is not None:
                kwargs['ssid'] = ssid
            if vlan is not None:
                kwargs['vlan'] = vlan
            if ap_tag:
                kwargs['apTag'] = ap_tag
            
            result = meraki_client.dashboard.wireless.getNetworkWirelessClientsConnectionStats(
                network_id, **kwargs
            )
            
            response = f"# 📊 Clients Connection Stats\n\n"
            
            if isinstance(result, list):
                response += f"**Total Clients**: {len(result)}\n\n"
                
                for client in result[:5]:  # Show first 5
                    response += f"## Client: {client.get('mac')}\n"
                    response += f"- Connection: {client.get('connectionStats', {}).get('assoc', 0)} associations\n"
                    response += f"- Auth: {client.get('connectionStats', {}).get('auth', 0)} authentications\n"
                    response += f"- DHCP: {client.get('connectionStats', {}).get('dhcp', 0)} attempts\n"
                    response += f"- DNS: {client.get('connectionStats', {}).get('dns', 0)} queries\n"
                    response += f"- Success: {client.get('connectionStats', {}).get('success', 0)} connections\n\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error getting clients connection stats: {str(e)}"
    
    @app.tool(
        name="get_network_wireless_clients_latency_stats",
        description="📡📊 Get latency stats for multiple wireless clients"
    )
    def get_network_wireless_clients_latency_stats(
        network_id: str,
        t0: Optional[str] = None,
        t1: Optional[str] = None,
        timespan: Optional[float] = 86400,
        band: Optional[str] = None,
        ssid: Optional[int] = None,
        vlan: Optional[int] = None,
        ap_tag: Optional[str] = None,
        fields: Optional[str] = None
    ):
        """Get latency statistics for multiple clients."""
        try:
            kwargs = {}
            
            if t0:
                kwargs['t0'] = t0
            if t1:
                kwargs['t1'] = t1
            if timespan:
                kwargs['timespan'] = timespan
            if band:
                kwargs['band'] = band
            if ssid is not None:
                kwargs['ssid'] = ssid
            if vlan is not None:
                kwargs['vlan'] = vlan
            if ap_tag:
                kwargs['apTag'] = ap_tag
            if fields:
                kwargs['fields'] = fields
            
            result = meraki_client.dashboard.wireless.getNetworkWirelessClientsLatencyStats(
                network_id, **kwargs
            )
            
            response = f"# 📊 Clients Latency Stats\n\n"
            
            if isinstance(result, list):
                response += f"**Total Clients**: {len(result)}\n\n"
                
                # Sort by average latency
                sorted_clients = sorted(result, 
                    key=lambda x: x.get('latencyStats', {}).get('backgroundTraffic', {}).get('avg', 0),
                    reverse=True)
                
                response += "## Clients with Highest Latency\n"
                for client in sorted_clients[:5]:
                    response += f"- **{client.get('mac')}**\n"
                    stats = client.get('latencyStats', {})
                    response += f"  - Background: {stats.get('backgroundTraffic', {}).get('avg', 0):.1f} ms\n"
                    response += f"  - Best Effort: {stats.get('bestEffortTraffic', {}).get('avg', 0):.1f} ms\n"
                    response += f"  - Video: {stats.get('videoTraffic', {}).get('avg', 0):.1f} ms\n"
                    response += f"  - Voice: {stats.get('voiceTraffic', {}).get('avg', 0):.1f} ms\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error getting clients latency stats: {str(e)}"
    
    @app.tool(
        name="get_device_wireless_connection_stats",
        description="📡📊 Get connection stats for a specific wireless device"
    )
    def get_device_wireless_connection_stats(
        serial: str,
        t0: Optional[str] = None,
        t1: Optional[str] = None,
        timespan: Optional[float] = 86400,
        band: Optional[str] = None,
        ssid: Optional[int] = None,
        vlan: Optional[int] = None,
        ap_tag: Optional[str] = None
    ):
        """Get connection statistics for a specific device."""
        try:
            kwargs = {}
            
            if t0:
                kwargs['t0'] = t0
            if t1:
                kwargs['t1'] = t1
            if timespan:
                kwargs['timespan'] = timespan
            if band:
                kwargs['band'] = band
            if ssid is not None:
                kwargs['ssid'] = ssid
            if vlan is not None:
                kwargs['vlan'] = vlan
            if ap_tag:
                kwargs['apTag'] = ap_tag
            
            result = meraki_client.dashboard.wireless.getDeviceWirelessConnectionStats(
                serial, **kwargs
            )
            
            response = f"# 📊 Device {serial} - Connection Stats\n\n"
            response += f"**Time Period**: {timespan/3600:.0f} hours\n\n"
            
            if isinstance(result, dict):
                # Check if all values are 0 or None
                has_data = any([
                    result.get('assoc', 0) > 0,
                    result.get('auth', 0) > 0,
                    result.get('dhcp', 0) > 0,
                    result.get('dns', 0) > 0,
                    result.get('success', 0) > 0
                ])
                
                if not has_data:
                    response += "⚠️ **No connection activity in this time period**\n\n"
                    response += "**Possible reasons:**\n"
                    response += "- No clients connected to this AP during the timespan\n"
                    response += "- AP was offline or rebooting\n"
                    response += "- Analytics data collection not enabled\n\n"
                    response += "💡 **Tips:**\n"
                    response += "- Try a longer timespan (e.g., 86400 for 24 hours)\n"
                    response += "- Check if the AP has connected clients: get_device_wireless_status\n"
                    response += "- Use get_network_wireless_connection_stats for network-wide stats\n"
                else:
                    response += f"**Associations**: {result.get('assoc', 0)}\n"
                    response += f"**Authentications**: {result.get('auth', 0)}\n"
                    response += f"**DHCP**: {result.get('dhcp', 0)}\n"
                    response += f"**DNS**: {result.get('dns', 0)}\n"
                    response += f"**Successful Connections**: {result.get('success', 0)}\n"
                    
                    # Calculate success rate if there were attempts
                    total_attempts = result.get('assoc', 0)
                    if total_attempts > 0:
                        success_rate = (result.get('success', 0) / total_attempts) * 100
                        response += f"\n**Success Rate**: {success_rate:.1f}%\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error getting device connection stats: {str(e)}"

# ==================== RF PROFILE CRUD ====================

def register_rf_profile_crud_tools():
    """Register RF Profile CRUD operations."""
    # DUPLICATE: Commented out - these tools are defined in tools_wireless_rf_profiles.py
    return  # Skip registration to avoid duplicates
    '''
    @app.tool(
        name="create_network_wireless_rf_profile",
        description="📡📻 Create a new RF profile for network"
    )
    def create_network_wireless_rf_profile(
        network_id: str,
        name: str,
        band_selection_type: str,
        client_balancing_enabled: Optional[bool] = None,
        min_bitrate_type: Optional[str] = None,
        ap_band_settings: Optional[str] = None,
        two_four_ghz_settings: Optional[str] = None,
        five_ghz_settings: Optional[str] = None,
        six_ghz_settings: Optional[str] = None
    ):
        """Create a new RF profile."""
        try:
            kwargs = {
                'name': name,
                'bandSelectionType': band_selection_type
            }
            
            if client_balancing_enabled is not None:
                kwargs['clientBalancingEnabled'] = client_balancing_enabled
            if min_bitrate_type:
                kwargs['minBitrateType'] = min_bitrate_type
            if ap_band_settings:
                kwargs['apBandSettings'] = json.loads(ap_band_settings) if isinstance(ap_band_settings, str) else ap_band_settings
            if two_four_ghz_settings:
                kwargs['twoFourGhzSettings'] = json.loads(two_four_ghz_settings) if isinstance(two_four_ghz_settings, str) else two_four_ghz_settings
            if five_ghz_settings:
                kwargs['fiveGhzSettings'] = json.loads(five_ghz_settings) if isinstance(five_ghz_settings, str) else five_ghz_settings
            if six_ghz_settings:
                kwargs['sixGhzSettings'] = json.loads(six_ghz_settings) if isinstance(six_ghz_settings, str) else six_ghz_settings
            
            result = meraki_client.dashboard.wireless.createNetworkWirelessRfProfile(
                network_id, **kwargs
            )
            
            return f"✅ Created RF profile '{result.get('name')}' - ID: {result.get('id')}"
            
        except Exception as e:
            return f"❌ Error creating RF profile: {str(e)}"
    
    @app.tool(
        name="update_network_wireless_rf_profile",
        description="📡📻 Update an existing RF profile"
    )
    def update_network_wireless_rf_profile(
        network_id: str,
        rf_profile_id: str,
        name: Optional[str] = None,
        band_selection_type: Optional[str] = None,
        client_balancing_enabled: Optional[bool] = None,
        min_bitrate_type: Optional[str] = None,
        ap_band_settings: Optional[str] = None
    ):
        """Update an RF profile."""
        try:
            kwargs = {}
            
            if name:
                kwargs['name'] = name
            if band_selection_type:
                kwargs['bandSelectionType'] = band_selection_type
            if client_balancing_enabled is not None:
                kwargs['clientBalancingEnabled'] = client_balancing_enabled
            if min_bitrate_type:
                kwargs['minBitrateType'] = min_bitrate_type
            if ap_band_settings:
                kwargs['apBandSettings'] = json.loads(ap_band_settings) if isinstance(ap_band_settings, str) else ap_band_settings
            
            result = meraki_client.dashboard.wireless.updateNetworkWirelessRfProfile(
                network_id, rf_profile_id, **kwargs
            )
            
            return f"✅ Updated RF profile '{result.get('name')}'"
            
        except Exception as e:
            return f"❌ Error updating RF profile: {str(e)}"
    
    @app.tool(
        name="delete_network_wireless_rf_profile",
        description="📡📻 Delete an RF profile from network"
    )
    def delete_network_wireless_rf_profile(
        network_id: str,
        rf_profile_id: str
    ):
        """Delete an RF profile."""
        try:
            meraki_client.dashboard.wireless.deleteNetworkWirelessRfProfile(
                network_id, rf_profile_id
            )
            
            return f"✅ Deleted RF profile {rf_profile_id}"
            
        except Exception as e:
            return f"❌ Error deleting RF profile: {str(e)}"
    '''

# ==================== RADIO SETTINGS ====================

def register_radio_settings_tools():
    """Register radio settings tools."""
    # DUPLICATE: Commented out - defined in tools_wireless_advanced.py  
    return  # Skip registration to avoid duplicates
    '''
    @app.tool(
        name="get_device_wireless_radio_settings",
        description="📡📻 Get radio settings for a wireless device"
    )
    def get_device_wireless_radio_settings(serial: str):
        """Get device radio settings."""
        try:
            result = meraki_client.dashboard.wireless.getDeviceWirelessRadioSettings(serial)
            
            response = f"# 📻 Device {serial} - Radio Settings\n\n"
            response += f"**RF Profile ID**: {result.get('rfProfileId', 'None')}\n"
            
            # 2.4 GHz settings
            two_four = result.get('twoFourGhzSettings', {})
            if two_four:
                response += f"\n## 2.4 GHz Settings\n"
                response += f"- Channel: {two_four.get('channel', 'Auto')}\n"
                response += f"- Target Power: {two_four.get('targetPower', 'Auto')} dBm\n"
            
            # 5 GHz settings
            five = result.get('fiveGhzSettings', {})
            if five:
                response += f"\n## 5 GHz Settings\n"
                response += f"- Channel: {five.get('channel', 'Auto')}\n"
                response += f"- Channel Width: {five.get('channelWidth', 'Auto')}\n"
                response += f"- Target Power: {five.get('targetPower', 'Auto')} dBm\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error getting radio settings: {str(e)}"
    
    @app.tool(
        name="update_device_wireless_radio_settings",
        description="📡📻 Update radio settings for a wireless device"
    )
    def update_device_wireless_radio_settings(
        serial: str,
        rf_profile_id: Optional[str] = None,
        two_four_ghz_settings: Optional[str] = None,
        five_ghz_settings: Optional[str] = None
    ):
        """Update device radio settings."""
        try:
            kwargs = {}
            
            if rf_profile_id:
                kwargs['rfProfileId'] = rf_profile_id
            if two_four_ghz_settings:
                kwargs['twoFourGhzSettings'] = json.loads(two_four_ghz_settings) if isinstance(two_four_ghz_settings, str) else two_four_ghz_settings
            if five_ghz_settings:
                kwargs['fiveGhzSettings'] = json.loads(five_ghz_settings) if isinstance(five_ghz_settings, str) else five_ghz_settings
            
            result = meraki_client.dashboard.wireless.updateDeviceWirelessRadioSettings(
                serial, **kwargs
            )
            
            return f"✅ Updated radio settings for device {serial}"
            
        except Exception as e:
            return f"❌ Error updating radio settings: {str(e)}"
    '''

# ==================== UPDATE OPERATIONS ====================

def register_update_operations_tools():
    """Register update operations for existing features."""
    # DUPLICATE: Commented out - defined in tools_wireless_advanced.py
    return  # Skip registration to avoid duplicates

# ==================== SPECIALIZED FEATURES ====================

def register_specialized_features_tools():
    """Register specialized feature tools."""
    
    @app.tool(
        name="get_network_wireless_l7_firewall_rules_application_categories",
        description="📡🔥 Get L7 firewall application categories"
    )
    def get_network_wireless_l7_firewall_rules_application_categories(
        network_id: str
    ):
        """Get L7 firewall application categories."""
        try:
            result = meraki_client.dashboard.wireless.getNetworkWirelessSsidFirewallL7FirewallRulesApplicationCategories(
                network_id
            )
            
            response = f"# 🔥 L7 Application Categories\n\n"
            
            if isinstance(result, dict):
                categories = result.get('applicationCategories', [])
                response += f"**Total Categories**: {len(categories)}\n\n"
                
                for category in categories[:20]:  # Show first 20
                    response += f"- **{category.get('name')}**\n"
                    response += f"  - ID: {category.get('id')}\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error getting L7 categories: {str(e)}"
    
    @app.tool(
        name="get_network_wireless_rf_profiles_assignments_by_device",
        description="📡📻 Get RF profile assignments by device"
    )
    def get_network_wireless_rf_profiles_assignments_by_device(
        network_id: str,
        per_page: Optional[int] = 1000
    ):
        """Get RF profile assignments by device."""
        try:
            result = meraki_client.dashboard.wireless.getNetworkWirelessRfProfilesAssignmentsByDevice(
                network_id,
                perPage=per_page
            )
            
            response = f"# 📻 RF Profile Assignments by Device\n\n"
            
            if isinstance(result, list):
                response += f"**Total Devices**: {len(result)}\n\n"
                
                # Group by profile
                profiles = {}
                for device in result:
                    profile_id = device.get('rfProfile', {}).get('id', 'None')
                    if profile_id not in profiles:
                        profiles[profile_id] = []
                    profiles[profile_id].append(device)
                
                response += f"## Profiles ({len(profiles)})\n"
                for profile_id, devices in profiles.items():
                    profile_name = devices[0].get('rfProfile', {}).get('name', 'Default') if devices else 'Unknown'
                    response += f"- **{profile_name}**: {len(devices)} devices\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error getting RF profile assignments: {str(e)}"
    
    @app.tool(
        name="get_organization_wireless_devices_ethernet_statuses",
        description="📡🔌 Get Ethernet port statuses for wireless devices"
    )
    def get_organization_wireless_devices_ethernet_statuses(
        organization_id: str,
        network_ids: Optional[str] = None,
        per_page: Optional[int] = 1000
    ):
        """Get Ethernet port statuses for wireless devices."""
        try:
            kwargs = {'perPage': per_page}
            
            if network_ids:
                kwargs['networkIds'] = json.loads(network_ids) if isinstance(network_ids, str) else network_ids
            
            result = meraki_client.dashboard.wireless.getOrganizationWirelessDevicesEthernetStatuses(
                organization_id, **kwargs
            )
            
            response = f"# 🔌 Wireless Devices Ethernet Statuses\n\n"
            
            if isinstance(result, list):
                response += f"**Total Devices**: {len(result)}\n\n"
                
                for device in result[:10]:  # Show first 10
                    response += f"## {device.get('name')} ({device.get('serial')})\n"
                    response += f"- Network: {device.get('network', {}).get('name')}\n"
                    
                    ports = device.get('ports', [])
                    if ports:
                        response += f"- Ports ({len(ports)}):\n"
                        for port in ports:
                            response += f"  - Port {port.get('name')}: "
                            response += f"{'🟢 Enabled' if port.get('enabled') else '🔴 Disabled'}\n"
                            response += f"    - VLAN: {port.get('vlan', 'N/A')}\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error getting Ethernet statuses: {str(e)}"
    
    @app.tool(
        name="get_network_wireless_devices_connection_stats",
        description="📡📊 Get connection stats for all wireless devices in network"
    )
    def get_network_wireless_devices_connection_stats(
        network_id: str,
        t0: Optional[str] = None,
        t1: Optional[str] = None,
        timespan: Optional[float] = 86400,
        band: Optional[str] = None,
        ssid: Optional[int] = None,
        vlan: Optional[int] = None
    ):
        """Get connection stats for all wireless devices in network."""
        try:
            kwargs = {}
            
            if t0:
                kwargs['t0'] = t0
            if t1:
                kwargs['t1'] = t1
            if timespan:
                kwargs['timespan'] = timespan
            if band:
                kwargs['band'] = band
            if ssid is not None:
                kwargs['ssid'] = ssid
            if vlan is not None:
                kwargs['vlan'] = vlan
            
            result = meraki_client.dashboard.wireless.getNetworkWirelessDevicesConnectionStats(
                network_id, **kwargs
            )
            
            response = f"# 📊 Network Devices Connection Stats\n\n"
            
            if isinstance(result, list):
                response += f"**Total Devices**: {len(result)}\n\n"
                
                # Sort by total connections
                sorted_devices = sorted(result, 
                    key=lambda x: x.get('connectionStats', {}).get('success', 0),
                    reverse=True)
                
                response += "## Top Devices by Successful Connections\n"
                for device in sorted_devices[:10]:
                    response += f"- **{device.get('serial')}**\n"
                    stats = device.get('connectionStats', {})
                    response += f"  - Successful: {stats.get('success', 0)}\n"
                    response += f"  - Associations: {stats.get('assoc', 0)}\n"
                    response += f"  - Authentications: {stats.get('auth', 0)}\n"
                    response += f"  - DHCP: {stats.get('dhcp', 0)}\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error getting devices connection stats: {str(e)}"
    
    @app.tool(
        name="get_network_wireless_air_marshal",
        description="📡🛡️ Get Air Marshal scan results for network"
    )
    def get_network_wireless_air_marshal(
        network_id: str,
        timespan: Optional[int] = 7200
    ):
        """Get Air Marshal scan results."""
        try:
            result = meraki_client.dashboard.wireless.getNetworkWirelessAirMarshal(
                network_id,
                timespan=timespan
            )
            
            response = f"# 🛡️ Air Marshal Scan Results\n\n"
            response += f"**Timespan**: {timespan/3600:.1f} hours\n\n"
            
            if isinstance(result, list):
                response += f"**Total SSIDs Detected**: {len(result)}\n\n"
                
                # Categorize by containment
                contained = [s for s in result if s.get('containment', {}).get('contained')]
                rogue = [s for s in result if not s.get('wiredMacs') and not s.get('containment', {}).get('contained')]
                
                response += f"## Summary\n"
                response += f"- 🔴 Rogue SSIDs: {len(rogue)}\n"
                response += f"- 🟢 Contained: {len(contained)}\n"
                response += f"- 🔵 Total: {len(result)}\n\n"
                
                if rogue:
                    response += f"## Top Rogue SSIDs\n"
                    for ssid in rogue[:5]:
                        response += f"- **{ssid.get('ssid')}**\n"
                        response += f"  - BSSID: {ssid.get('bssid')}\n"
                        response += f"  - Channel: {ssid.get('channel')}\n"
                        response += f"  - RSSI: {ssid.get('rssi')} dBm\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error getting Air Marshal data: {str(e)}"
    
    @app.tool(
        name="get_network_wireless_channel_utilization_history",
        description="📡📈 Get channel utilization history (REQUIRES: device_serial + band OR client_id)"
    )
    def get_network_wireless_channel_utilization_history(
        network_id: str,
        t0: Optional[str] = None,
        t1: Optional[str] = None,
        timespan: Optional[float] = 86400,
        resolution: Optional[int] = 300,
        auto_resolution: Optional[bool] = True,
        client_id: Optional[str] = None,
        device_serial: Optional[str] = None,
        ap_tag: Optional[str] = None,
        band: Optional[str] = None
    ):
        """Get channel utilization history. Requires either device_serial+band OR client_id."""
        try:
            # API requires either device or client
            if not device_serial and not client_id:
                return ("❌ Error: Must specify either:\n"
                        "  • device_serial + band parameters (e.g., band='2.4' or '5')\n"
                        "  • client_id parameter\n\n"
                        "💡 Examples:\n"
                        f"  • get_network_wireless_channel_utilization_history('{network_id}', device_serial='Q2XX-XXXX-XXXX', band='2.4')\n"
                        f"  • get_network_wireless_channel_utilization_history('{network_id}', client_id='k74272e')")
            
            # When device_serial is provided, band is required
            if device_serial and not band:
                return ("❌ Error: When using device_serial, band parameter is required\n\n"
                        "💡 Valid band values: '2.4', '5', or '6'\n\n"
                        "Example:\n"
                        f"  get_network_wireless_channel_utilization_history('{network_id}', device_serial='{device_serial}', band='2.4')")
            
            kwargs = {}
            
            if t0:
                kwargs['t0'] = t0
            if t1:
                kwargs['t1'] = t1
            if timespan:
                kwargs['timespan'] = timespan
            # Only set resolution if auto_resolution is False or None
            if auto_resolution is not None:
                kwargs['autoResolution'] = auto_resolution
                if not auto_resolution and resolution:
                    kwargs['resolution'] = resolution
            elif resolution:
                kwargs['resolution'] = resolution
            if client_id:
                kwargs['clientId'] = client_id
            if device_serial:
                kwargs['deviceSerial'] = device_serial
            if ap_tag:
                kwargs['apTag'] = ap_tag
            if band:
                kwargs['band'] = band
            
            result = meraki_client.dashboard.wireless.getNetworkWirelessChannelUtilizationHistory(
                network_id, **kwargs
            )
            
            response = f"# 📈 Channel Utilization History\n\n"
            response += f"**Timespan**: {timespan/3600:.1f} hours\n"
            
            if isinstance(result, list) and result:
                response += f"**Data Points**: {len(result)}\n\n"
                
                # Get average utilization - handle None values
                valid_utils = [d.get('utilization80211') for d in result if d.get('utilization80211') is not None]
                if valid_utils:
                    avg_util = sum(valid_utils) / len(valid_utils)
                    response += f"## Statistics\n"
                    response += f"- **Average 802.11 Utilization**: {avg_util:.1f}%\n"
                    
                    # Find peak utilization
                    peak = max(result, key=lambda x: x.get('utilization80211', 0) if x.get('utilization80211') is not None else 0)
                    peak_val = peak.get('utilization80211')
                    if peak_val is not None:
                        response += f"- **Peak Utilization**: {peak_val:.1f}%\n"
                        response += f"- **Peak Time**: {peak.get('startTs')}\n"
                else:
                    response += "## Statistics\n"
                    response += "- **No utilization data available**\n"
                
                # Show recent data points
                response += f"\n## Recent Utilization\n"
                for point in result[-5:]:  # Last 5 points
                    response += f"- {point.get('startTs')}: "
                    wifi_util = point.get('utilization80211')
                    non_wifi_util = point.get('utilizationNon80211')
                    
                    if wifi_util is not None:
                        response += f"WiFi {wifi_util:.1f}%, "
                    else:
                        response += f"WiFi N/A, "
                    
                    if non_wifi_util is not None:
                        response += f"Non-WiFi {non_wifi_util:.1f}%\n"
                    else:
                        response += f"Non-WiFi N/A\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error getting channel utilization history: {str(e)}"