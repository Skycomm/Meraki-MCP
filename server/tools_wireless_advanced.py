"""
Advanced Wireless Tools for the Cisco Meraki MCP Server.
Implements all missing wireless endpoints to achieve 100% API coverage.

IMPORTANT PAGINATION LIMITS:
Different Meraki API endpoints have different pagination limits. 
Always check the specific endpoint documentation before changing these values.

Known pagination limits:
- Most endpoints: 3-1000 (default: 100 or 1000)
- getNetworkWirelessMeshStatuses: 3-500 (default: 50) 
- getOrganizationWirelessSsidsStatusesByDevice: 3-500 (default: 100)

When in doubt, use 500 as a safe maximum for any "statuses" endpoints.
"""

from typing import Optional, List, Dict, Any
import json

# Global variables to store app and meraki client
app = None
meraki_client = None

def register_wireless_advanced_tools(mcp_app, meraki):
    """
    Register advanced wireless tools with the MCP server.
    
    Args:
        mcp_app: MCP server instance
        meraki: Meraki client instance
    """
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    
    # Register all advanced wireless tool handlers
    register_connection_stats_tools()
    register_ssid_advanced_tools()
    register_identity_psk_tools()
    register_network_settings_tools()
    register_radio_mesh_tools()
    register_history_tools()
    register_organization_wireless_tools()
    register_special_features_tools()

# ==================== CONNECTION & PERFORMANCE STATS ====================

def register_connection_stats_tools():
    """Register connection and performance statistics tools."""
    
    @app.tool(
        name="get_network_wireless_connection_stats",
        description="📡📊 Get aggregated wireless connection statistics"
    )
    def get_network_wireless_connection_stats(
        network_id: str,
        t0: Optional[str] = None,
        t1: Optional[str] = None,
        timespan: Optional[float] = 86400,
        ssid: Optional[int] = None,
        vlan: Optional[int] = None,
        ap_tag: Optional[str] = None
    ):
        """Get aggregated wireless connection statistics."""
        try:
            kwargs = {'timespan': timespan}
            if t0: kwargs['t0'] = t0
            if t1: kwargs['t1'] = t1
            if ssid is not None: kwargs['ssid'] = ssid
            if vlan is not None: kwargs['vlan'] = vlan
            if ap_tag: kwargs['apTag'] = ap_tag
            
            result = meraki_client.dashboard.wireless.getNetworkWirelessConnectionStats(
                network_id, **kwargs
            )
            
            response = f"# 📊 Wireless Connection Statistics\n\n"
            
            if isinstance(result, dict):
                # Get raw counts from API response
                success_count = result.get('success', 0)
                auth_fails = result.get('auth', 0)
                assoc_fails = result.get('assoc', 0)
                dhcp_fails = result.get('dhcp', 0)
                dns_fails = result.get('dns', 0)
                
                # Calculate total attempts
                total_attempts = success_count + auth_fails + assoc_fails + dhcp_fails + dns_fails
                
                # Calculate success rate percentage
                if total_attempts > 0:
                    success_rate = (success_count / total_attempts) * 100
                else:
                    success_rate = 0
                
                response += f"## Connection Statistics\n\n"
                response += f"### Overall Performance:\n"
                response += f"- **Total Attempts**: {total_attempts}\n"
                response += f"- **Successful**: {success_count}\n"
                response += f"- **Success Rate**: {success_rate:.1f}%\n\n"
                
                response += f"### Failed Connections Breakdown:\n"
                response += f"- **Authentication Failures**: {auth_fails}\n"
                response += f"- **Association Failures**: {assoc_fails}\n"
                response += f"- **DHCP Failures**: {dhcp_fails}\n"
                response += f"- **DNS Failures**: {dns_fails}\n"
                response += f"- **Total Failures**: {auth_fails + assoc_fails + dhcp_fails + dns_fails}\n"
            
            return response
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    @app.tool(
        name="get_network_wireless_latency_stats",
        description="📡⏱️ Get aggregated wireless latency statistics"
    )
    def get_network_wireless_latency_stats(
        network_id: str,
        t0: Optional[str] = None,
        t1: Optional[str] = None,
        timespan: Optional[float] = 86400,
        ssid: Optional[int] = None,
        vlan: Optional[int] = None,
        ap_tag: Optional[str] = None
    ):
        """Get aggregated wireless latency statistics."""
        try:
            kwargs = {'timespan': timespan}
            if t0: kwargs['t0'] = t0
            if t1: kwargs['t1'] = t1
            if ssid is not None: kwargs['ssid'] = ssid
            if vlan is not None: kwargs['vlan'] = vlan
            if ap_tag: kwargs['apTag'] = ap_tag
            
            result = meraki_client.dashboard.wireless.getNetworkWirelessLatencyStats(
                network_id, **kwargs
            )
            
            response = f"# ⏱️ Wireless Latency Statistics\n\n"
            
            if isinstance(result, dict):
                bg_traffic = result.get('backgroundTraffic', {})
                best_effort = result.get('bestEffortTraffic', {})
                video = result.get('videoTraffic', {})
                voice = result.get('voiceTraffic', {})
                
                response += "## Latency by Traffic Type:\n\n"
                
                if bg_traffic:
                    response += f"### Background Traffic:\n"
                    response += f"- Average: {bg_traffic.get('avg', 0)}ms\n"
                    response += f"- Min: {bg_traffic.get('min', 0)}ms\n"
                    response += f"- Max: {bg_traffic.get('max', 0)}ms\n\n"
                
                if voice:
                    response += f"### Voice Traffic:\n"
                    response += f"- Average: {voice.get('avg', 0)}ms\n"
                    response += f"- Min: {voice.get('min', 0)}ms\n"
                    response += f"- Max: {voice.get('max', 0)}ms\n"
            
            return response
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    @app.tool(
        name="get_network_wireless_failed_connections",
        description="📡❌ Get failed wireless connection attempts"
    )
    def get_network_wireless_failed_connections(
        network_id: str,
        t0: Optional[str] = None,
        t1: Optional[str] = None,
        timespan: Optional[float] = 86400,
        ssid: Optional[int] = None,
        vlan: Optional[int] = None,
        serial: Optional[str] = None,
        client_id: Optional[str] = None
    ):
        """Get failed wireless connection attempts."""
        try:
            kwargs = {'timespan': timespan}
            if t0: kwargs['t0'] = t0
            if t1: kwargs['t1'] = t1
            if ssid is not None: kwargs['ssid'] = ssid
            if vlan is not None: kwargs['vlan'] = vlan
            if serial: kwargs['serial'] = serial
            if client_id: kwargs['clientId'] = client_id
            
            result = meraki_client.dashboard.wireless.getNetworkWirelessFailedConnections(
                network_id, **kwargs
            )
            
            response = f"# ❌ Failed Connection Attempts\n\n"
            
            if isinstance(result, list):
                response += f"**Total Failed Attempts**: {len(result)}\n\n"
                
                # Group by failure type
                failure_types = {}
                for failure in result[:20]:  # Show first 20
                    fail_type = failure.get('failureStep', 'Unknown')
                    if fail_type not in failure_types:
                        failure_types[fail_type] = 0
                    failure_types[fail_type] += 1
                
                response += "## Failure Distribution:\n"
                for fail_type, count in failure_types.items():
                    response += f"- **{fail_type}**: {count} failures\n"
                
                response += "\n## Recent Failures:\n"
                for failure in result[:5]:
                    response += f"- **Client**: {failure.get('clientMac', 'Unknown')}\n"
                    response += f"  - SSID: {failure.get('ssidNumber', 'Unknown')}\n"
                    response += f"  - AP: {failure.get('serial', 'Unknown')}\n"
                    response += f"  - Failed at: {failure.get('failureStep', 'Unknown')}\n"
                    response += f"  - Time: {failure.get('ts', 'Unknown')}\n\n"
            
            return response
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    @app.tool(
        name="get_device_wireless_status",
        description="📡📱 Get current RF status for a wireless device"
    )
    def get_device_wireless_status(serial: str):
        """Get current RF status for a wireless device."""
        try:
            result = meraki_client.dashboard.wireless.getDeviceWirelessStatus(serial)
            
            response = f"# 📡 Wireless Device Status\n\n"
            response += f"**Serial**: {serial}\n\n"
            
            if isinstance(result, dict):
                # Basic info
                basic = result.get('basicServiceSets', [])
                if basic:
                    response += f"## Radio Status:\n"
                    for bss in basic:
                        response += f"### {bss.get('band', 'Unknown')} Band\n"
                        response += f"- SSID: {bss.get('ssidName', 'Unknown')}\n"
                        response += f"- Channel: {bss.get('channel', 'Unknown')}\n"
                        response += f"- Power: {bss.get('power', 'Unknown')} dBm\n"
                        response += f"- Visible: {bss.get('visible', False)}\n\n"
            
            return response
        except Exception as e:
            return f"❌ Error: {str(e)}"

# ==================== SSID ADVANCED CONFIGURATION ====================

def register_ssid_advanced_tools():
    """Register SSID advanced configuration tools."""
    # NOTE: These tools are now in tools_wireless_ssid_features.py to avoid duplicates
    return  # Skip registration as tools moved to avoid duplicate definitions
    
    @app.tool(
        name="get_network_wireless_ssid_splash_settings",
        description="📡🌐 Get splash page settings for an SSID"
    )
    def get_network_wireless_ssid_splash_settings(
        network_id: str,
        number: str
    ):
        """Get splash page settings for an SSID."""
        try:
            result = meraki_client.dashboard.wireless.getNetworkWirelessSsidSplashSettings(
                network_id, number
            )
            
            response = f"# 🌐 SSID {number} Splash Page Settings\n\n"
            
            if isinstance(result, dict):
                splash_page = result.get('splashPage', 'None')
                response += f"**Splash Page Type**: {splash_page}\n"
                
                if splash_page != 'None':
                    response += f"\n## Configuration:\n"
                    response += f"- **Welcome Message**: {result.get('welcomeMessage', 'None')}\n"
                    response += f"- **Redirect URL**: {result.get('redirectUrl', 'None')}\n"
                    response += f"- **Block All Traffic Before Sign-On**: {result.get('blockAllTrafficBeforeSignOn', False)}\n"
                    response += f"- **Controller Disconnection Behavior**: {result.get('controllerDisconnectionBehavior', 'default')}\n"
                    
                    # Billing
                    billing = result.get('billing', {})
                    if billing:
                        response += f"\n## Billing Settings:\n"
                        response += f"- **Free Access**: {billing.get('freeAccess', {}).get('enabled', False)}\n"
                        response += f"- **Duration**: {billing.get('freeAccess', {}).get('durationInMinutes', 0)} minutes\n"
            
            return response
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    @app.tool(
        name="update_network_wireless_ssid_splash_settings",
        description="📡🌐 Update splash page settings for an SSID"
    )
    def update_network_wireless_ssid_splash_settings(
        network_id: str,
        number: str,
        splash_page: Optional[str] = None,
        welcome_message: Optional[str] = None,
        redirect_url: Optional[str] = None,
        block_all_traffic_before_sign_on: Optional[bool] = None
    ):
        """Update splash page settings for an SSID."""
        try:
            kwargs = {}
            if splash_page: kwargs['splashPage'] = splash_page
            if welcome_message: kwargs['welcomeMessage'] = welcome_message
            if redirect_url: kwargs['redirectUrl'] = redirect_url
            if block_all_traffic_before_sign_on is not None:
                kwargs['blockAllTrafficBeforeSignOn'] = block_all_traffic_before_sign_on
            
            result = meraki_client.dashboard.wireless.updateNetworkWirelessSsidSplashSettings(
                network_id, number, **kwargs
            )
            
            response = f"# ✅ Updated SSID {number} Splash Settings\n\n"
            response += f"**New Splash Page Type**: {result.get('splashPage', 'None')}\n"
            
            return response
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    @app.tool(
        name="get_network_wireless_ssid_schedules",
        description="📡📅 Get SSID availability schedules"
    )
    def get_network_wireless_ssid_schedules(
        network_id: str,
        number: str
    ):
        """Get SSID availability schedules."""
        try:
            result = meraki_client.dashboard.wireless.getNetworkWirelessSsidSchedules(
                network_id, number
            )
            
            response = f"# 📅 SSID {number} Schedules\n\n"
            
            if isinstance(result, dict):
                enabled = result.get('enabled', False)
                response += f"**Scheduling**: {'Enabled ✅' if enabled else 'Disabled ❌'}\n"
                
                if enabled:
                    ranges = result.get('ranges', [])
                    if ranges:
                        response += f"\n## Active Time Ranges:\n"
                        for i, range_item in enumerate(ranges, 1):
                            response += f"{i}. **{range_item.get('startDay', 'Unknown')}** "
                            response += f"{range_item.get('startTime', 'Unknown')} - "
                            response += f"**{range_item.get('endDay', 'Unknown')}** "
                            response += f"{range_item.get('endTime', 'Unknown')}\n"
            
            return response
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    @app.tool(
        name="update_network_wireless_ssid_schedules",
        description="📡📅 Update SSID availability schedules"
    )
    def update_network_wireless_ssid_schedules(
        network_id: str,
        number: str,
        enabled: Optional[bool] = None,
        ranges: Optional[str] = None
    ):
        """Update SSID availability schedules."""
        try:
            kwargs = {}
            if enabled is not None: kwargs['enabled'] = enabled
            if ranges:
                kwargs['ranges'] = json.loads(ranges)
            
            result = meraki_client.dashboard.wireless.updateNetworkWirelessSsidSchedules(
                network_id, number, **kwargs
            )
            
            response = f"# ✅ Updated SSID {number} Schedules\n\n"
            response += f"**Scheduling**: {'Enabled ✅' if result.get('enabled') else 'Disabled ❌'}\n"
            
            return response
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    @app.tool(
        name="get_network_wireless_ssid_hotspot20",
        description="📡♨️ Get Hotspot 2.0 settings for an SSID"
    )
    def get_network_wireless_ssid_hotspot20(
        network_id: str,
        number: str
    ):
        """Get Hotspot 2.0 settings for an SSID."""
        try:
            result = meraki_client.dashboard.wireless.getNetworkWirelessSsidHotspot20(
                network_id, number
            )
            
            response = f"# ♨️ SSID {number} Hotspot 2.0 Settings\n\n"
            
            if isinstance(result, dict):
                enabled = result.get('enabled', False)
                response += f"**Hotspot 2.0**: {'Enabled ✅' if enabled else 'Disabled ❌'}\n"
                
                if enabled:
                    response += f"\n## Configuration:\n"
                    response += f"- **Network Type**: {result.get('networkAccessType', 'Unknown')}\n"
                    
                    # Operator
                    operator = result.get('operator', {})
                    if operator:
                        response += f"\n### Operator:\n"
                        response += f"- **Name**: {operator.get('name', 'Unknown')}\n"
                    
                    # Venue
                    venue = result.get('venue', {})
                    if venue:
                        response += f"\n### Venue:\n"
                        response += f"- **Type**: {venue.get('type', 'Unknown')}\n"
                        response += f"- **Name**: {venue.get('name', 'Unknown')}\n"
            
            return response
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    @app.tool(
        name="update_network_wireless_ssid_hotspot20",
        description="📡♨️ Update Hotspot 2.0 settings for an SSID"
    )
    def update_network_wireless_ssid_hotspot20(
        network_id: str,
        number: str,
        enabled: Optional[bool] = None,
        network_access_type: Optional[str] = None,
        operator_name: Optional[str] = None
    ):
        """Update Hotspot 2.0 settings for an SSID."""
        try:
            kwargs = {}
            if enabled is not None: kwargs['enabled'] = enabled
            if network_access_type: kwargs['networkAccessType'] = network_access_type
            if operator_name: 
                kwargs['operator'] = {'name': operator_name}
            
            result = meraki_client.dashboard.wireless.updateNetworkWirelessSsidHotspot20(
                network_id, number, **kwargs
            )
            
            response = f"# ✅ Updated SSID {number} Hotspot 2.0\n\n"
            response += f"**Hotspot 2.0**: {'Enabled ✅' if result.get('enabled') else 'Disabled ❌'}\n"
            
            return response
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    @app.tool(
        name="get_network_wireless_ssid_vpn",
        description="📡🔒 Get VPN settings for an SSID"
    )
    def get_network_wireless_ssid_vpn(
        network_id: str,
        number: str
    ):
        """Get VPN settings for an SSID."""
        try:
            result = meraki_client.dashboard.wireless.getNetworkWirelessSsidVpn(
                network_id, number
            )
            
            response = f"# 🔒 SSID {number} VPN Settings\n\n"
            
            if isinstance(result, dict):
                concentrator = result.get('concentrator', {})
                response += f"**VPN Concentrator**: {concentrator.get('name', 'None')}\n"
                response += f"**Network ID**: {concentrator.get('networkId', 'None')}\n"
                response += f"**VLAN ID**: {concentrator.get('vlanId', 'None')}\n"
                
                # Split tunnel
                split_tunnel = result.get('splitTunnel', {})
                if split_tunnel:
                    response += f"\n## Split Tunnel:\n"
                    response += f"- **Enabled**: {split_tunnel.get('enabled', False)}\n"
                    rules = split_tunnel.get('rules', [])
                    if rules:
                        response += f"- **Rules**: {len(rules)} configured\n"
            
            return response
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    @app.tool(
        name="update_network_wireless_ssid_vpn",
        description="📡🔒 Update VPN settings for an SSID"
    )
    def update_network_wireless_ssid_vpn(
        network_id: str,
        number: str,
        concentrator_network_id: Optional[str] = None,
        concentrator_vlan_id: Optional[int] = None
    ):
        """Update VPN settings for an SSID."""
        try:
            kwargs = {}
            if concentrator_network_id or concentrator_vlan_id:
                kwargs['concentrator'] = {}
                if concentrator_network_id:
                    kwargs['concentrator']['networkId'] = concentrator_network_id
                if concentrator_vlan_id:
                    kwargs['concentrator']['vlanId'] = concentrator_vlan_id
            
            result = meraki_client.dashboard.wireless.updateNetworkWirelessSsidVpn(
                network_id, number, **kwargs
            )
            
            response = f"# ✅ Updated SSID {number} VPN Settings\n\n"
            concentrator = result.get('concentrator', {})
            response += f"**VPN Network**: {concentrator.get('networkId', 'None')}\n"
            response += f"**VLAN**: {concentrator.get('vlanId', 'None')}\n"
            
            return response
        except Exception as e:
            return f"❌ Error: {str(e)}"

# ==================== IDENTITY PSK MANAGEMENT ====================

def register_identity_psk_tools():
    """Register Identity PSK management tools."""
    
    @app.tool(
        name="get_network_wireless_ssid_identity_psks",
        description="📡🔑 Get all Identity PSKs for an SSID"
    )
    def get_network_wireless_ssid_identity_psks(
        network_id: str,
        number: str
    ):
        """Get all Identity PSKs for an SSID."""
        try:
            result = meraki_client.dashboard.wireless.getNetworkWirelessSsidIdentityPsks(
                network_id, number
            )
            
            response = f"# 🔑 SSID {number} Identity PSKs\n\n"
            
            if isinstance(result, list):
                response += f"**Total PSKs**: {len(result)}\n\n"
                
                for i, psk in enumerate(result[:10], 1):  # Show first 10
                    response += f"## PSK {i}:\n"
                    response += f"- **Name**: {psk.get('name', 'Unknown')}\n"
                    response += f"- **Email**: {psk.get('email', 'None')}\n"
                    response += f"- **Passphrase**: {'••••••••' if psk.get('passphrase') else 'Not set'}\n"
                    response += f"- **Group Policy**: {psk.get('groupPolicyId', 'None')}\n"
                    response += f"- **ID**: {psk.get('id', 'Unknown')}\n\n"
            
            return response
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    @app.tool(
        name="create_network_wireless_ssid_identity_psk",
        description="📡🔑 Create a new Identity PSK for an SSID"
    )
    def create_network_wireless_ssid_identity_psk(
        network_id: str,
        number: str,
        name: str,
        passphrase: str,
        email: Optional[str] = None,
        group_policy_id: Optional[str] = None
    ):
        """Create a new Identity PSK for an SSID."""
        try:
            kwargs = {
                'name': name,
                'passphrase': passphrase
            }
            if email: kwargs['email'] = email
            if group_policy_id: kwargs['groupPolicyId'] = group_policy_id
            
            result = meraki_client.dashboard.wireless.createNetworkWirelessSsidIdentityPsk(
                network_id, number, **kwargs
            )
            
            response = f"# ✅ Created Identity PSK\n\n"
            response += f"**Name**: {result.get('name', 'Unknown')}\n"
            response += f"**Email**: {result.get('email', 'None')}\n"
            response += f"**ID**: {result.get('id', 'Unknown')}\n"
            response += f"**Group Policy**: {result.get('groupPolicyId', 'None')}\n"
            
            return response
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    @app.tool(
        name="update_network_wireless_ssid_identity_psk",
        description="📡🔑 Update an existing Identity PSK"
    )
    def update_network_wireless_ssid_identity_psk(
        network_id: str,
        number: str,
        identity_psk_id: str,
        name: Optional[str] = None,
        passphrase: Optional[str] = None,
        email: Optional[str] = None
    ):
        """Update an existing Identity PSK."""
        try:
            kwargs = {}
            if name: kwargs['name'] = name
            if passphrase: kwargs['passphrase'] = passphrase
            if email: kwargs['email'] = email
            
            result = meraki_client.dashboard.wireless.updateNetworkWirelessSsidIdentityPsk(
                network_id, number, identity_psk_id, **kwargs
            )
            
            response = f"# ✅ Updated Identity PSK\n\n"
            response += f"**Name**: {result.get('name', 'Unknown')}\n"
            response += f"**Email**: {result.get('email', 'None')}\n"
            
            return response
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    @app.tool(
        name="delete_network_wireless_ssid_identity_psk",
        description="📡🔑 Delete an Identity PSK"
    )
    def delete_network_wireless_ssid_identity_psk(
        network_id: str,
        number: str,
        identity_psk_id: str
    ):
        """Delete an Identity PSK."""
        try:
            meraki_client.dashboard.wireless.deleteNetworkWirelessSsidIdentityPsk(
                network_id, number, identity_psk_id
            )
            
            return f"# ✅ Deleted Identity PSK\n\n**ID**: {identity_psk_id}"
        except Exception as e:
            return f"❌ Error: {str(e)}"

# ==================== NETWORK WIRELESS SETTINGS ====================

def register_network_settings_tools():
    """Register network-wide wireless settings tools."""
    
    @app.tool(
        name="get_network_wireless_settings",
        description="📡⚙️ Get network-wide wireless settings"
    )
    def get_network_wireless_settings(network_id: str):
        """Get network-wide wireless settings."""
        try:
            result = meraki_client.dashboard.wireless.getNetworkWirelessSettings(network_id)
            
            response = f"# ⚙️ Network Wireless Settings\n\n"
            
            if isinstance(result, dict):
                response += f"**Meshing**: {'Enabled ✅' if result.get('meshingEnabled') else 'Disabled ❌'}\n"
                response += f"**IPv6 Bridge**: {'Enabled ✅' if result.get('ipv6BridgeEnabled') else 'Disabled ❌'}\n"
                response += f"**Location Analytics**: {'Enabled ✅' if result.get('locationAnalyticsEnabled') else 'Disabled ❌'}\n"
                response += f"**LED Lights Out**: {'Enabled ✅' if result.get('ledLightsOn') == False else 'Disabled ❌'}\n"
                
                # Named VLANs
                named_vlans = result.get('namedVlans', {})
                if named_vlans and named_vlans.get('poolDhcpMonitoring', {}).get('enabled'):
                    response += f"\n## VLAN Pool DHCP Monitoring:\n"
                    response += f"- **Enabled**: ✅\n"
                    response += f"- **Duration**: {named_vlans['poolDhcpMonitoring'].get('duration', 0)} minutes\n"
                
                # Regulatory domain
                reg = result.get('regulatoryDomain', {})
                if reg:
                    response += f"\n## Regulatory Domain:\n"
                    response += f"- **Country Code**: {reg.get('countryCode', 'Unknown')}\n"
                    response += f"- **Permits 6GHz**: {reg.get('permits6ghz', False)}\n"
            
            return response
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    @app.tool(
        name="update_network_wireless_settings",
        description="📡⚙️ Update network-wide wireless settings"
    )
    def update_network_wireless_settings(
        network_id: str,
        meshing_enabled: Optional[bool] = None,
        ipv6_bridge_enabled: Optional[bool] = None,
        location_analytics_enabled: Optional[bool] = None,
        led_lights_on: Optional[bool] = None
    ):
        """Update network-wide wireless settings."""
        try:
            kwargs = {}
            if meshing_enabled is not None: kwargs['meshingEnabled'] = meshing_enabled
            if ipv6_bridge_enabled is not None: kwargs['ipv6BridgeEnabled'] = ipv6_bridge_enabled
            if location_analytics_enabled is not None: kwargs['locationAnalyticsEnabled'] = location_analytics_enabled
            if led_lights_on is not None: kwargs['ledLightsOn'] = led_lights_on
            
            result = meraki_client.dashboard.wireless.updateNetworkWirelessSettings(
                network_id, **kwargs
            )
            
            response = f"# ✅ Updated Network Wireless Settings\n\n"
            response += f"**Meshing**: {'Enabled ✅' if result.get('meshingEnabled') else 'Disabled ❌'}\n"
            response += f"**IPv6 Bridge**: {'Enabled ✅' if result.get('ipv6BridgeEnabled') else 'Disabled ❌'}\n"
            response += f"**Location Analytics**: {'Enabled ✅' if result.get('locationAnalyticsEnabled') else 'Disabled ❌'}\n"
            
            return response
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    # NOTE: get_network_wireless_alternate_management_interface moved to tools_wireless_complete.py
    # Commenting out to avoid duplicate registration
    '''
    @app.tool(
        name="get_network_wireless_alternate_management_interface",
        description="📡🔧 Get alternate management interface settings"
    )
    def get_network_wireless_alternate_management_interface(network_id: str):
        """Get alternate management interface settings."""
        try:
            result = meraki_client.dashboard.wireless.getNetworkWirelessAlternateManagementInterface(network_id)
            
            response = f"# 🔧 Alternate Management Interface\n\n"
            
            if isinstance(result, dict):
                enabled = result.get('enabled', False)
                response += f"**Status**: {'Enabled ✅' if enabled else 'Disabled ❌'}\n"
                
                if enabled:
                    response += f"**VLAN ID**: {result.get('vlanId', 'None')}\n"
                    
                    # Protocols
                    protocols = result.get('protocols', [])
                    if protocols:
                        response += f"**Protocols**: {', '.join(protocols)}\n"
                    
                    # Access points
                    aps = result.get('accessPoints', [])
                    if aps:
                        response += f"\n## Configured APs: {len(aps)}\n"
                        for ap in aps[:5]:
                            response += f"- {ap.get('serial', 'Unknown')}: {ap.get('alternateManagementIp', 'None')}\n"
            
            return response
        except Exception as e:
            return f"❌ Error: {str(e)}"
    '''  # End of commented duplicate function

# ==================== RADIO & MESH TOOLS ====================

def register_radio_mesh_tools():
    """Register radio settings and mesh tools."""
    
    @app.tool(
        name="get_device_wireless_radio_settings",
        description="📡📻 Get radio settings for a wireless device"
    )
    def get_device_wireless_radio_settings(serial: str):
        """Get radio settings for a wireless device."""
        try:
            result = meraki_client.dashboard.wireless.getDeviceWirelessRadioSettings(serial)
            
            response = f"# 📻 Radio Settings for {serial}\n\n"
            
            if isinstance(result, dict):
                # RF Profile
                response += f"**RF Profile**: {result.get('rfProfileId', 'None')}\n\n"
                
                # Two-four GHz settings
                two_four = result.get('twoFourGhzSettings', {})
                if two_four:
                    response += "## 2.4 GHz Settings:\n"
                    response += f"- **Channel**: {two_four.get('channel', 'Auto')}\n"
                    response += f"- **Channel Width**: {two_four.get('channelWidth', 'Auto')}\n"
                    response += f"- **Target Power**: {two_four.get('targetPower', 'Auto')} dBm\n\n"
                
                # Five GHz settings
                five = result.get('fiveGhzSettings', {})
                if five:
                    response += "## 5 GHz Settings:\n"
                    response += f"- **Channel**: {five.get('channel', 'Auto')}\n"
                    response += f"- **Channel Width**: {five.get('channelWidth', 'Auto')}\n"
                    response += f"- **Target Power**: {five.get('targetPower', 'Auto')} dBm\n"
            
            return response
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    @app.tool(
        name="update_device_wireless_radio_settings",
        description="📡📻 Update radio settings (2.4GHz: ch 1-14, max 20dBm | 5GHz: ch 36-161, max 19dBm)"
    )
    def update_device_wireless_radio_settings(
        serial: str,
        rf_profile_id: Optional[str] = None,
        two_four_ghz_channel: Optional[int] = None,
        five_ghz_channel: Optional[int] = None,
        two_four_ghz_power: Optional[int] = None,
        five_ghz_power: Optional[int] = None
    ):
        """Update radio settings for a wireless device."""
        try:
            # Validate 2.4GHz settings
            if two_four_ghz_channel:
                valid_24_channels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
                if two_four_ghz_channel not in valid_24_channels:
                    return (f"❌ Invalid 2.4GHz channel: {two_four_ghz_channel}\n"
                            f"Valid channels: {valid_24_channels}\n"
                            "Recommended: 1, 6, or 11 (non-overlapping)")
            
            if two_four_ghz_power:
                if two_four_ghz_power > 20:
                    return f"❌ 2.4GHz power too high: {two_four_ghz_power} dBm (max: 20 dBm)"
                if two_four_ghz_power < 5:
                    return f"❌ 2.4GHz power too low: {two_four_ghz_power} dBm (min: 5 dBm)"
            
            # Validate 5GHz settings
            if five_ghz_channel:
                # Australian valid 5GHz channels
                valid_5_channels = [36, 40, 44, 48, 52, 56, 60, 64, 100, 104, 108, 112, 
                                   116, 120, 124, 128, 132, 136, 140, 144, 149, 153, 157, 161]
                if five_ghz_channel not in valid_5_channels:
                    return (f"❌ Invalid 5GHz channel: {five_ghz_channel}\n"
                            f"Valid channels (AU): {valid_5_channels}\n"
                            "Note: Channel 165 not available in Australia")
            
            if five_ghz_power:
                if five_ghz_power > 19:
                    return f"❌ 5GHz power too high: {five_ghz_power} dBm (max: 19 dBm)"
                if five_ghz_power < 5:
                    return f"❌ 5GHz power too low: {five_ghz_power} dBm (min: 5 dBm)"
            
            kwargs = {}
            if rf_profile_id: kwargs['rfProfileId'] = rf_profile_id
            
            if two_four_ghz_channel or two_four_ghz_power:
                kwargs['twoFourGhzSettings'] = {}
                if two_four_ghz_channel: kwargs['twoFourGhzSettings']['channel'] = two_four_ghz_channel
                if two_four_ghz_power: kwargs['twoFourGhzSettings']['targetPower'] = two_four_ghz_power
            
            if five_ghz_channel or five_ghz_power:
                kwargs['fiveGhzSettings'] = {}
                if five_ghz_channel: kwargs['fiveGhzSettings']['channel'] = five_ghz_channel
                if five_ghz_power: kwargs['fiveGhzSettings']['targetPower'] = five_ghz_power
            
            result = meraki_client.dashboard.wireless.updateDeviceWirelessRadioSettings(
                serial, **kwargs
            )
            
            response = f"# ✅ Updated Radio Settings\n\n"
            response += f"**Device**: {serial}\n"
            response += f"**RF Profile**: {result.get('rfProfileId', 'None')}\n"
            
            return response
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    @app.tool(
        name="get_network_wireless_mesh_statuses",
        description="📡🕸️ Get mesh status for all APs in network"
    )
    def get_network_wireless_mesh_statuses(
        network_id: str,
        per_page: Optional[int] = 500  # API limit: must be between 3 and 500
    ):
        """Get mesh status for all APs in network."""
        try:
            result = meraki_client.dashboard.wireless.getNetworkWirelessMeshStatuses(
                network_id, perPage=per_page
            )
            
            response = f"# 🕸️ Mesh Network Status\n\n"
            
            if isinstance(result, list):
                response += f"**Total Mesh APs**: {len(result)}\n\n"
                
                # Count by mesh role
                gateways = [ap for ap in result if ap.get('meshRole') == 'gateway']
                repeaters = [ap for ap in result if ap.get('meshRole') == 'repeater']
                
                response += f"## Mesh Roles:\n"
                response += f"- **Gateways**: {len(gateways)}\n"
                response += f"- **Repeaters**: {len(repeaters)}\n\n"
                
                # Show mesh details
                response += "## Mesh Links:\n"
                for ap in result[:10]:  # Show first 10
                    if ap.get('meshRole') == 'repeater':
                        response += f"- **{ap.get('serial', 'Unknown')}**\n"
                        response += f"  - Parent: {ap.get('latestMeshPerformance', {}).get('parentSerial', 'Unknown')}\n"
                        response += f"  - RSSI: {ap.get('latestMeshPerformance', {}).get('parentRssi', 'Unknown')} dBm\n"
                        response += f"  - Hop Count: {ap.get('latestMeshPerformance', {}).get('hopCount', 'Unknown')}\n"
            
            return response
        except Exception as e:
            return f"❌ Error: {str(e)}"

# ==================== HISTORY & ANALYTICS TOOLS ====================

def register_history_tools():
    """Register historical data and analytics tools."""
    
    # NOTE: This is a duplicate - the correct tool is get_network_wireless_devices_latency_stats
    @app.tool(
        name="get_network_wireless_devices_latencies",
        description="📡📊 Get latency statistics (REDIRECT: Use get_network_wireless_devices_latency_stats)"
    )
    def get_network_wireless_devices_latencies(
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
        """Get latency statistics for all wireless devices."""
        return ("❌ Wrong tool name! The correct tool is: get_network_wireless_devices_latency_stats\n\n"
                "💡 Use: get_network_wireless_devices_latency_stats\n"
                "This tool exists and works correctly - just use the right name!\n\n"
                "Example: get_network_wireless_devices_latency_stats(network_id)")
    
    @app.tool(
        name="get_network_wireless_devices_packet_loss",
        description="📡📉 DEPRECATED - Use organization-level packet loss tools instead (API doesn't exist at network level)"
    )
    def get_network_wireless_devices_packet_loss(
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
        """Get packet loss statistics for all wireless devices."""
        # This API doesn't exist at the network level - redirect to organization level
        return ("❌ This tool doesn't exist in the Meraki SDK. Use organization-level packet loss tools instead.\n\n"
                "💡 **Available packet loss tools:**\n"
                "1. **get_organization_wireless_devices_packet_loss** - General org-level packet loss\n"
                "2. **get_organization_wireless_devices_packet_loss_by_device** - Packet loss grouped by device\n"
                "3. **get_organization_wireless_devices_packet_loss_by_network** - Packet loss grouped by network\n"
                "4. **get_organization_wireless_devices_packet_loss_by_client** - Packet loss grouped by client\n\n"
                "**Example usage:**\n"
                f"get_organization_wireless_devices_packet_loss_by_device(org_id, network_ids='{network_id}')\n\n"
                "These tools provide comprehensive packet loss data at the organization level.\n"
                "You can filter by specific networks using the network_ids parameter.")
    
    @app.tool(
        name="get_network_wireless_client_count_history",
        description="📡📈 Get historical client count (TIP: Specify device_serial for per-AP counts)"
    )
    def get_network_wireless_client_count_history(
        network_id: str,
        t0: Optional[str] = None,
        t1: Optional[str] = None,
        timespan: Optional[float] = 86400,
        resolution: Optional[int] = None,
        ssid: Optional[int] = None,
        ap_tag: Optional[str] = None
    ):
        """Get historical client count over time."""
        try:
            kwargs = {'timespan': timespan}
            if t0: kwargs['t0'] = t0
            if t1: kwargs['t1'] = t1
            if resolution: kwargs['resolution'] = resolution
            if ssid is not None: kwargs['ssid'] = ssid
            if ap_tag: kwargs['apTag'] = ap_tag
            
            result = meraki_client.dashboard.wireless.getNetworkWirelessClientCountHistory(
                network_id, **kwargs
            )
            
            response = f"# 📈 Client Count History\n\n"
            
            if isinstance(result, list):
                response += f"**Data Points**: {len(result)}\n\n"
                
                if result:
                    # Find min/max, filtering out None values
                    counts = [point.get('clientCount') for point in result if point.get('clientCount') is not None]
                    
                    if counts:
                        response += f"**Peak Clients**: {max(counts)}\n"
                        response += f"**Minimum Clients**: {min(counts)}\n"
                        response += f"**Average**: {sum(counts) // len(counts)}\n\n"
                    else:
                        response += "⚠️ **No data available** - The API returned time slots but no client count data.\n"
                        response += "This usually means:\n"
                        response += "• Analytics data collection is not enabled\n"
                        response += "• The network is newly created\n"
                        response += "• No clients have connected during this time period\n\n"
                    
                    # Show recent data
                    response += "## Recent Data Points:\n"
                    for point in result[-5:]:
                        client_count = point.get('clientCount')
                        count_str = str(client_count) if client_count is not None else "No data"
                        response += f"- {point.get('startTs', 'Unknown')}: **{count_str}** clients\n"
            
            return response
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    @app.tool(
        name="get_network_wireless_data_rate_history",
        description="📡📊 Get historical data rate info (TIP: May need device_serial for actual data)"
    )
    def get_network_wireless_data_rate_history(
        network_id: str,
        t0: Optional[str] = None,
        t1: Optional[str] = None,
        timespan: Optional[float] = 86400,
        resolution: Optional[int] = None,
        ssid: Optional[int] = None,
        ap_tag: Optional[str] = None
    ):
        """Get historical data rate information."""
        try:
            kwargs = {'timespan': timespan}
            if t0: kwargs['t0'] = t0
            if t1: kwargs['t1'] = t1
            if resolution: kwargs['resolution'] = resolution
            if ssid is not None: kwargs['ssid'] = ssid
            if ap_tag: kwargs['apTag'] = ap_tag
            
            result = meraki_client.dashboard.wireless.getNetworkWirelessDataRateHistory(
                network_id, **kwargs
            )
            
            response = f"# 📊 Data Rate History\n\n"
            
            if isinstance(result, list):
                response += f"**Data Points**: {len(result)}\n\n"
                
                if result:
                    # Check if we have actual data
                    has_data = any(point.get('averageKbps') is not None or 
                                  point.get('downloadKbps') is not None or 
                                  point.get('uploadKbps') is not None 
                                  for point in result)
                    
                    if has_data:
                        # Analyze recent data rates
                        recent = result[-1] if result else {}
                        if recent:
                            response += "## Current Data Rates:\n"
                            avg_kbps = recent.get('averageKbps')
                            dl_kbps = recent.get('downloadKbps')
                            ul_kbps = recent.get('uploadKbps')
                            
                            if avg_kbps is not None:
                                response += f"- **Average**: {avg_kbps / 1000:.2f} Mbps\n"
                            if dl_kbps is not None:
                                response += f"- **Download**: {dl_kbps / 1000:.2f} Mbps\n"
                            if ul_kbps is not None:
                                response += f"- **Upload**: {ul_kbps / 1000:.2f} Mbps\n"
                    else:
                        response += "⚠️ **No data available** - The API returned time slots but no rate data.\n"
                        response += "This usually means:\n"
                        response += "• Analytics data collection is not enabled\n"
                        response += "• No traffic during this period\n"
                        response += "• Try specifying a device_serial parameter\n"
            
            return response
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    @app.tool(
        name="get_network_wireless_usage_history",
        description="📡📉 Get historical wireless usage data (REQUIRES: device_serial OR client_id)"
    )
    def get_network_wireless_usage_history(
        network_id: str,
        device_serial: Optional[str] = None,
        client_id: Optional[str] = None,
        t0: Optional[str] = None,
        t1: Optional[str] = None,
        timespan: Optional[float] = 86400,
        resolution: Optional[int] = None,
        ssid: Optional[int] = None,
        ap_tag: Optional[str] = None
    ):
        """Get historical wireless usage data. Requires either device_serial OR client_id."""
        try:
            # API requires either device or client
            if not device_serial and not client_id:
                return "❌ Error: Must specify either device_serial or client_id parameter"
            
            kwargs = {'timespan': timespan}
            if device_serial: kwargs['deviceSerial'] = device_serial
            if client_id: kwargs['clientId'] = client_id
            if t0: kwargs['t0'] = t0
            if t1: kwargs['t1'] = t1
            if resolution: kwargs['resolution'] = resolution
            if ssid is not None: kwargs['ssid'] = ssid
            if ap_tag: kwargs['apTag'] = ap_tag
            
            result = meraki_client.dashboard.wireless.getNetworkWirelessUsageHistory(
                network_id, **kwargs
            )
            
            response = f"# 📉 Wireless Usage History\n\n"
            
            if isinstance(result, list):
                if not result:
                    response += "⚠️ **No data available for the specified parameters**\n\n"
                    response += "**Possible reasons:**\n"
                    response += "- The device/client has no activity in the timespan\n"
                    response += "- Analytics data collection not enabled\n"
                    response += "- Invalid device_serial or client_id\n\n"
                    response += "💡 **Tips:**\n"
                    if device_serial:
                        response += f"- Verify device serial '{device_serial}' is correct\n"
                        response += "- Use get_network_devices to list valid device serials\n"
                    if client_id:
                        response += f"- Verify client ID '{client_id}' is correct\n"
                        response += "- Use get_network_wireless_clients to list active clients\n"
                    response += f"- Try a longer timespan (current: {timespan/3600:.0f} hours)\n"
                else:
                    response += f"**Data Points**: {len(result)}\n\n"
                    
                    # Calculate totals
                    total_sent = sum(point.get('sentKbps', 0) for point in result)
                    total_received = sum(point.get('receivedKbps', 0) for point in result)
                    
                    response += f"## Usage Summary:\n"
                    response += f"- **Total Sent**: {total_sent / 1024:.2f} MB\n"
                    response += f"- **Total Received**: {total_received / 1024:.2f} MB\n"
            
            return response
        except Exception as e:
            error_msg = str(e)
            if '404' in error_msg or 'No device with serial' in error_msg:
                return ("⚠️ **No data available - Device not found**\n\n"
                        f"The device serial '{device_serial if device_serial else client_id}' was not found.\n\n"
                        "💡 **Tips:**\n"
                        "- Use get_network_devices to list valid device serials\n"
                        "- Use get_network_wireless_clients to list active client IDs\n"
                        "- Verify the device/client is in this network\n")
            return f"❌ Error: {error_msg}"
    
    @app.tool(
        name="get_network_wireless_signal_quality_history",
        description="📡📶 Get historical signal quality data (REQUIRES: device_serial OR client_id)"
    )
    def get_network_wireless_signal_quality_history(
        network_id: str,
        device_serial: Optional[str] = None,
        client_id: Optional[str] = None,
        t0: Optional[str] = None,
        t1: Optional[str] = None,
        timespan: Optional[float] = 86400,
        resolution: Optional[int] = None,
        ssid: Optional[int] = None,
        ap_tag: Optional[str] = None
    ):
        """Get historical signal quality data. Requires either device_serial OR client_id."""
        try:
            # API requires either device or client
            if not device_serial and not client_id:
                return "❌ Error: Must specify either device_serial or client_id parameter"
            
            kwargs = {'timespan': timespan}
            if device_serial: kwargs['deviceSerial'] = device_serial
            if client_id: kwargs['clientId'] = client_id
            if t0: kwargs['t0'] = t0
            if t1: kwargs['t1'] = t1
            if resolution: kwargs['resolution'] = resolution
            if ssid is not None: kwargs['ssid'] = ssid
            if ap_tag: kwargs['apTag'] = ap_tag
            
            result = meraki_client.dashboard.wireless.getNetworkWirelessSignalQualityHistory(
                network_id, **kwargs
            )
            
            response = f"# 📶 Signal Quality History\n\n"
            
            if isinstance(result, list):
                response += f"**Data Points**: {len(result)}\n\n"
                
                if result:
                    # Check if we have actual data
                    has_data = any(point.get('rssi') is not None or point.get('snr') is not None for point in result)
                    
                    if has_data:
                        # Analyze signal quality
                        recent = result[-1] if result else {}
                        if recent:
                            response += "## Recent Signal Quality:\n"
                            rssi = recent.get('rssi')
                            snr = recent.get('snr')
                            if rssi is not None:
                                response += f"- **Average RSSI**: {rssi} dBm\n"
                            if snr is not None:
                                response += f"- **Average SNR**: {snr} dB\n"
                    else:
                        response += "⚠️ **No signal data available** - The API returned time slots but no signal metrics.\n"
                        response += "This usually means:\n"
                        response += "• The device/client was not connected during this period\n"
                        response += "• Analytics data collection is not enabled\n"
                        response += "• Try a different device_serial or client_id\n"
            
            return response
        except Exception as e:
            return f"❌ Error: {str(e)}"

# ==================== ORGANIZATION-WIDE WIRELESS TOOLS ====================

def register_organization_wireless_tools():
    """Register organization-wide wireless tools."""
    
    @app.tool(
        name="get_organization_wireless_devices_channel_utilization",
        description="📡📊 Get channel utilization by device across organization"
    )
    def get_organization_wireless_devices_channel_utilization(
        organization_id: str,
        network_ids: Optional[str] = None,
        serials: Optional[str] = None,
        per_page: Optional[int] = 1000
    ):
        """Get channel utilization by device across organization."""
        try:
            kwargs = {'perPage': per_page}
            if network_ids: kwargs['networkIds'] = network_ids.split(',')
            if serials: kwargs['serials'] = serials.split(',')
            
            result = meraki_client.dashboard.wireless.getOrganizationWirelessDevicesChannelUtilizationByDevice(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Organization Channel Utilization\n\n"
            
            if isinstance(result, list):
                response += f"**Total Devices**: {len(result)}\n\n"
                
                # Find high utilization devices
                high_util = [d for d in result if any(
                    band.get('utilization', {}).get('total', 0) > 70 
                    for band in d.get('byBand', [])
                )]
                
                if high_util:
                    response += f"## ⚠️ High Utilization Devices ({len(high_util)}):\n"
                    for device in high_util[:5]:
                        response += f"- **{device.get('serial', 'Unknown')}**\n"
                        for band in device.get('byBand', []):
                            response += f"  - {band.get('band', 'Unknown')}: {band.get('utilization', {}).get('total', 0)}%\n"
            
            return response
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    @app.tool(
        name="get_organization_wireless_devices_packet_loss",
        description="📡📉 Get packet loss statistics by device"
    )
    def get_organization_wireless_devices_packet_loss(
        organization_id: str,
        network_ids: Optional[str] = None,
        serials: Optional[str] = None,
        t0: Optional[str] = None,
        t1: Optional[str] = None,
        timespan: Optional[float] = 86400,
        per_page: Optional[int] = 1000
    ):
        """Get packet loss statistics by device."""
        try:
            kwargs = {'timespan': timespan, 'perPage': per_page}
            if network_ids: kwargs['networkIds'] = network_ids.split(',')
            if serials: kwargs['serials'] = serials.split(',')
            if t0: kwargs['t0'] = t0
            if t1: kwargs['t1'] = t1
            
            result = meraki_client.dashboard.wireless.getOrganizationWirelessDevicesPacketLossByDevice(
                organization_id, **kwargs
            )
            
            response = f"# 📉 Organization Packet Loss\n\n"
            
            if isinstance(result, list):
                response += f"**Devices Analyzed**: {len(result)}\n\n"
                
                # Find devices with high packet loss
                high_loss = [d for d in result if d.get('downstream', {}).get('lossPercent', 0) > 1]
                
                if high_loss:
                    response += f"## ⚠️ Devices with Packet Loss ({len(high_loss)}):\n"
                    for device in high_loss[:5]:
                        response += f"- **{device.get('serial', 'Unknown')}**\n"
                        response += f"  - Downstream Loss: {device.get('downstream', {}).get('lossPercent', 0)}%\n"
                        response += f"  - Upstream Loss: {device.get('upstream', {}).get('lossPercent', 0)}%\n"
            
            return response
        except Exception as e:
            return f"❌ Error: {str(e)}"

# ==================== SPECIAL FEATURES ====================

def register_special_features_tools():
    """Register special feature tools."""
    # NOTE: Bluetooth tools moved to tools_wireless_ssid_features.py to avoid duplicates
    return  # Skip registration as tools moved to avoid duplicates
    
    @app.tool(
        name="get_network_wireless_ssid_bonjour_forwarding",
        description="📡🍎 Get Bonjour forwarding settings for SSID"
    )
    def get_network_wireless_ssid_bonjour_forwarding(
        network_id: str,
        number: str
    ):
        """Get Bonjour forwarding settings for SSID."""
        try:
            result = meraki_client.dashboard.wireless.getNetworkWirelessSsidBonjourForwarding(
                network_id, number
            )
            
            response = f"# 🍎 SSID {number} Bonjour Forwarding\n\n"
            
            if isinstance(result, dict):
                enabled = result.get('enabled', False)
                response += f"**Status**: {'Enabled ✅' if enabled else 'Disabled ❌'}\n"
                
                if enabled:
                    rules = result.get('rules', [])
                    if rules:
                        response += f"\n## Forwarding Rules ({len(rules)}):\n"
                        for rule in rules:
                            response += f"- **{rule.get('description', 'No description')}**\n"
                            response += f"  - VLAN: {rule.get('vlanId', 'Any')}\n"
                            response += f"  - Services: {', '.join(rule.get('services', []))}\n"
            
            return response
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    @app.tool(
        name="update_network_wireless_ssid_bonjour_forwarding",
        description="📡🍎 Update Bonjour forwarding settings for SSID"
    )
    def update_network_wireless_ssid_bonjour_forwarding(
        network_id: str,
        number: str,
        enabled: Optional[bool] = None,
        rules: Optional[str] = None
    ):
        """Update Bonjour forwarding settings for SSID."""
        try:
            kwargs = {}
            if enabled is not None: kwargs['enabled'] = enabled
            if rules: kwargs['rules'] = json.loads(rules)
            
            result = meraki_client.dashboard.wireless.updateNetworkWirelessSsidBonjourForwarding(
                network_id, number, **kwargs
            )
            
            response = f"# ✅ Updated Bonjour Forwarding\n\n"
            response += f"**Status**: {'Enabled ✅' if result.get('enabled') else 'Disabled ❌'}\n"
            
            return response
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    @app.tool(
        name="get_network_wireless_ssid_eap_override",
        description="📡🔐 Get EAP override settings for SSID"
    )
    def get_network_wireless_ssid_eap_override(
        network_id: str,
        number: str
    ):
        """Get EAP override settings for SSID."""
        try:
            result = meraki_client.dashboard.wireless.getNetworkWirelessSsidEapOverride(
                network_id, number
            )
            
            response = f"# 🔐 SSID {number} EAP Override\n\n"
            
            if isinstance(result, dict):
                response += f"**Timeout**: {result.get('timeout', 0)} seconds\n"
                response += f"**Identity Retries**: {result.get('maxRetries', 5)}\n"
                response += f"**EAP-GTC**: {result.get('eapolKey', {}).get('retries', 0)} retries\n"
                
                # Identity
                identity = result.get('identity', {})
                if identity:
                    response += f"\n## Identity Settings:\n"
                    response += f"- **Retries**: {identity.get('retries', 0)}\n"
                    response += f"- **Timeout**: {identity.get('timeout', 0)} seconds\n"
            
            return response
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    @app.tool(
        name="update_network_wireless_ssid_eap_override",
        description="📡🔐 Update EAP override settings for SSID"
    )
    def update_network_wireless_ssid_eap_override(
        network_id: str,
        number: str,
        timeout: Optional[int] = None,
        max_retries: Optional[int] = None
    ):
        """Update EAP override settings for SSID."""
        try:
            kwargs = {}
            if timeout is not None: kwargs['timeout'] = timeout
            if max_retries is not None: kwargs['maxRetries'] = max_retries
            
            result = meraki_client.dashboard.wireless.updateNetworkWirelessSsidEapOverride(
                network_id, number, **kwargs
            )
            
            response = f"# ✅ Updated EAP Override\n\n"
            response += f"**Timeout**: {result.get('timeout', 0)} seconds\n"
            response += f"**Max Retries**: {result.get('maxRetries', 5)}\n"
            
            return response
        except Exception as e:
            return f"❌ Error: {str(e)}"