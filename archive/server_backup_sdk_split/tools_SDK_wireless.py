"""
Wireless SSID Advanced Features Tools for the Cisco Meraki MCP Server.
Implements advanced SSID features like Hotspot 2.0, Splash Pages, Schedules, Identity PSKs, etc.
Previously named tools_wireless_complete.py
"""

from typing import Optional, List, Dict, Any
import json

# Global variables to store app and meraki client
app = None
meraki_client = None

def register_wireless_tools(mcp_app, meraki):
    """
    Register SSID advanced feature tools with the MCP server.
    Includes Hotspot 2.0, Splash Pages, Schedules, Identity PSKs, and more.
    
    Args:
        mcp_app: MCP server instance
        meraki: Meraki client instance
    """
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    
    # Register all SSID advanced feature tool handlers
    register_hotspot_tools()
    register_splash_tools()
    register_schedule_tools()
    register_vpn_tools()
    register_bonjour_tools()
    register_eap_tools()
    register_device_type_tools()
    register_alt_mgmt_tools()
    register_bluetooth_tools()
    register_air_marshal_tools()
    register_ethernet_ports_tools()
    register_location_scanning_tools()
    register_radsec_tools()
    register_esl_tools()
    register_billing_tools()
    register_isolation_allowlist_tools()

# ==================== HOTSPOT 2.0 ====================

def register_hotspot_tools():
    """Register Hotspot 2.0 configuration tools."""
    
    @app.tool(
        name="get_network_wireless_ssid_hotspot20",
        description="📡🔥 Get Hotspot 2.0 settings for a wireless SSID"
    )
    def get_network_wireless_ssid_hotspot20(
        network_id: str,
        number: str
    ):
        """Get Hotspot 2.0 configuration for an SSID."""
        try:
            result = meraki_client.dashboard.wireless.getNetworkWirelessSsidHotspot20(
                network_id, number
            )
            
            response = f"# 📡 SSID {number} - Hotspot 2.0 Settings\n\n"
            response += f"**Enabled**: {result.get('enabled', False)}\n"
            
            if result.get('enabled'):
                response += f"**Operator**: {result.get('operator', {}).get('name', 'N/A')}\n"
                response += f"**Venue**: {result.get('venue', {}).get('name', 'N/A')}\n"
                response += f"**Network Type**: {result.get('networkAccessType', 'N/A')}\n"
                
                domains = result.get('domains', [])
                if domains:
                    response += f"\n## Domains ({len(domains)})\n"
                    for domain in domains:
                        response += f"- {domain}\n"
                
                roam = result.get('roamConsortOis', [])
                if roam:
                    response += f"\n## Roaming Consortiums ({len(roam)})\n"
                    for oi in roam:
                        response += f"- {oi}\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error getting Hotspot 2.0 settings: {str(e)}"
    
    @app.tool(
        name="update_network_wireless_ssid_hotspot20",
        description="📡🔥 Update Hotspot 2.0 settings for a wireless SSID"
    )
    def update_network_wireless_ssid_hotspot20(
        network_id: str,
        number: str,
        enabled: bool,
        operator_name: Optional[str] = None,
        venue_name: Optional[str] = None,
        venue_type: Optional[str] = None,
        network_access_type: Optional[str] = None,
        domains: Optional[str] = None,
        roam_consort_ois: Optional[str] = None
    ):
        """Update Hotspot 2.0 configuration for an SSID."""
        try:
            kwargs = {'enabled': enabled}
            
            if operator_name:
                kwargs['operator'] = {'name': operator_name}
            
            if venue_name or venue_type:
                kwargs['venue'] = {}
                if venue_name:
                    kwargs['venue']['name'] = venue_name
                if venue_type:
                    kwargs['venue']['type'] = venue_type
            
            if network_access_type:
                kwargs['networkAccessType'] = network_access_type
            
            if domains:
                kwargs['domains'] = json.loads(domains) if isinstance(domains, str) else domains
            
            if roam_consort_ois:
                kwargs['roamConsortOis'] = json.loads(roam_consort_ois) if isinstance(roam_consort_ois, str) else roam_consort_ois
            
            result = meraki_client.dashboard.wireless.updateNetworkWirelessSsidHotspot20(
                network_id, number, **kwargs
            )
            
            return f"✅ Updated SSID {number} Hotspot 2.0 settings - Enabled: {result.get('enabled')}"
            
        except Exception as e:
            return f"❌ Error updating Hotspot 2.0: {str(e)}"

# ==================== SPLASH PAGE ====================

def register_splash_tools():
    """Register splash page configuration tools."""
    
    @app.tool(
        name="get_network_wireless_ssid_splash_settings",
        description="📡💦 Get splash page settings for a wireless SSID"
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
            
            response = f"# 📡 SSID {number} - Splash Page Settings\n\n"
            response += f"**Splash Page**: {result.get('splashPage', 'None')}\n"
            
            if result.get('splashUrl'):
                response += f"**Splash URL**: {result.get('splashUrl')}\n"
            
            if result.get('splashTimeout'):
                response += f"**Timeout**: {result.get('splashTimeout')} minutes\n"
            
            if result.get('redirectUrl'):
                response += f"**Redirect URL**: {result.get('redirectUrl')}\n"
            
            if result.get('welcomeMessage'):
                response += f"**Welcome Message**: {result.get('welcomeMessage')}\n"
            
            if result.get('blockAllTrafficBeforeSignOn') is not None:
                response += f"**Block Traffic Before Sign-On**: {result.get('blockAllTrafficBeforeSignOn')}\n"
            
            if result.get('guestSponsorship'):
                sponsor = result.get('guestSponsorship')
                response += f"\n## Guest Sponsorship\n"
                response += f"- **Duration**: {sponsor.get('durationInMinutes')} minutes\n"
                response += f"- **Guest Can Request**: {sponsor.get('guestCanRequestTimeframe')}\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error getting splash settings: {str(e)}"
    
    @app.tool(
        name="update_network_wireless_ssid_splash_settings",
        description="📡💦 Update splash page settings for a wireless SSID"
    )
    def update_network_wireless_ssid_splash_settings(
        network_id: str,
        number: str,
        splash_page: Optional[str] = None,
        splash_url: Optional[str] = None,
        splash_timeout: Optional[int] = None,
        redirect_url: Optional[str] = None,
        welcome_message: Optional[str] = None,
        block_all_traffic_before_sign_on: Optional[bool] = None
    ):
        """Update splash page settings for an SSID."""
        try:
            kwargs = {}
            
            if splash_page:
                kwargs['splashPage'] = splash_page
            if splash_url:
                kwargs['splashUrl'] = splash_url
            if splash_timeout:
                kwargs['splashTimeout'] = splash_timeout
            if redirect_url:
                kwargs['redirectUrl'] = redirect_url
            if welcome_message:
                kwargs['welcomeMessage'] = welcome_message
            if block_all_traffic_before_sign_on is not None:
                kwargs['blockAllTrafficBeforeSignOn'] = block_all_traffic_before_sign_on
            
            result = meraki_client.dashboard.wireless.updateNetworkWirelessSsidSplashSettings(
                network_id, number, **kwargs
            )
            
            return f"✅ Updated SSID {number} splash settings - Type: {result.get('splashPage', 'None')}"
            
        except Exception as e:
            return f"❌ Error updating splash settings: {str(e)}"

# ==================== SSID SCHEDULES ====================

def register_schedule_tools():
    """Register SSID schedule configuration tools."""
    
    @app.tool(
        name="get_network_wireless_ssid_schedules",
        description="📡⏰ Get scheduling settings for a wireless SSID"
    )
    def get_network_wireless_ssid_schedules(
        network_id: str,
        number: str
    ):
        """Get SSID scheduling configuration."""
        try:
            result = meraki_client.dashboard.wireless.getNetworkWirelessSsidSchedules(
                network_id, number
            )
            
            response = f"# 📡 SSID {number} - Schedule Settings\n\n"
            response += f"**Scheduling Enabled**: {result.get('enabled', False)}\n"
            
            if result.get('enabled') and result.get('ranges'):
                response += f"\n## Active Schedule Ranges\n"
                for range_item in result.get('ranges', []):
                    response += f"- **{range_item.get('day')}**: "
                    response += f"{range_item.get('from')} - {range_item.get('to')}\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error getting SSID schedules: {str(e)}"
    
    @app.tool(
        name="update_network_wireless_ssid_schedules",
        description="📡⏰ Update scheduling settings for a wireless SSID"
    )
    def update_network_wireless_ssid_schedules(
        network_id: str,
        number: str,
        enabled: bool,
        ranges: Optional[str] = None
    ):
        """Update SSID scheduling configuration."""
        try:
            kwargs = {'enabled': enabled}
            
            if ranges and enabled:
                kwargs['ranges'] = json.loads(ranges) if isinstance(ranges, str) else ranges
            
            result = meraki_client.dashboard.wireless.updateNetworkWirelessSsidSchedules(
                network_id, number, **kwargs
            )
            
            status = "Enabled ✅" if result.get('enabled') else "Disabled ❌"
            return f"✅ Updated SSID {number} schedules - {status}"
            
        except Exception as e:
            return f"❌ Error updating schedules: {str(e)}"

# ==================== SSID VPN ====================

def register_vpn_tools():
    """Register SSID VPN configuration tools."""
    
    @app.tool(
        name="get_network_wireless_ssid_vpn",
        description="📡🔐 Get VPN settings for a wireless SSID"
    )
    def get_network_wireless_ssid_vpn(
        network_id: str,
        number: str
    ):
        """Get SSID VPN configuration."""
        try:
            result = meraki_client.dashboard.wireless.getNetworkWirelessSsidVpn(
                network_id, number
            )
            
            response = f"# 📡 SSID {number} - VPN Settings\n\n"
            
            concentrator = result.get('concentrator')
            if concentrator:
                response += f"**Concentrator Network**: {concentrator.get('networkId', 'N/A')}\n"
                response += f"**VLAN**: {concentrator.get('vlanId', 'N/A')}\n"
            
            failover = result.get('failover')
            if failover:
                response += f"\n## Failover Settings\n"
                response += f"- **Request IP**: {failover.get('requestIp')}\n"
                response += f"- **Heartbeat Interval**: {failover.get('heartbeatInterval')} seconds\n"
                response += f"- **Idle Timeout**: {failover.get('idleTimeout')} seconds\n"
            
            split_tunnel = result.get('splitTunnel')
            if split_tunnel:
                response += f"\n## Split Tunnel\n"
                response += f"**Enabled**: {split_tunnel.get('enabled')}\n"
                if split_tunnel.get('rules'):
                    response += f"**Rules**: {len(split_tunnel.get('rules'))} configured\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error getting VPN settings: {str(e)}"
    
    @app.tool(
        name="update_network_wireless_ssid_vpn",
        description="📡🔐 Update VPN settings for a wireless SSID"
    )
    def update_network_wireless_ssid_vpn(
        network_id: str,
        number: str,
        concentrator_network_id: Optional[str] = None,
        concentrator_vlan_id: Optional[int] = None,
        failover_request_ip: Optional[str] = None,
        failover_heartbeat_interval: Optional[int] = None,
        failover_idle_timeout: Optional[int] = None
    ):
        """Update SSID VPN configuration."""
        try:
            kwargs = {}
            
            if concentrator_network_id or concentrator_vlan_id:
                kwargs['concentrator'] = {}
                if concentrator_network_id:
                    kwargs['concentrator']['networkId'] = concentrator_network_id
                if concentrator_vlan_id:
                    kwargs['concentrator']['vlanId'] = concentrator_vlan_id
            
            if any([failover_request_ip, failover_heartbeat_interval, failover_idle_timeout]):
                kwargs['failover'] = {}
                if failover_request_ip:
                    kwargs['failover']['requestIp'] = failover_request_ip
                if failover_heartbeat_interval:
                    kwargs['failover']['heartbeatInterval'] = failover_heartbeat_interval
                if failover_idle_timeout:
                    kwargs['failover']['idleTimeout'] = failover_idle_timeout
            
            result = meraki_client.dashboard.wireless.updateNetworkWirelessSsidVpn(
                network_id, number, **kwargs
            )
            
            return f"✅ Updated SSID {number} VPN settings"
            
        except Exception as e:
            return f"❌ Error updating VPN settings: {str(e)}"

# ==================== BONJOUR FORWARDING ====================

def register_bonjour_tools():
    """Register Bonjour forwarding configuration tools."""
    
    @app.tool(
        name="get_network_wireless_ssid_bonjour_forwarding",
        description="📡🍎 Get Bonjour forwarding settings for a wireless SSID"
    )
    def get_network_wireless_ssid_bonjour_forwarding(
        network_id: str,
        number: str
    ):
        """Get SSID Bonjour forwarding configuration."""
        try:
            result = meraki_client.dashboard.wireless.getNetworkWirelessSsidBonjourForwarding(
                network_id, number
            )
            
            response = f"# 📡 SSID {number} - Bonjour Forwarding\n\n"
            response += f"**Enabled**: {result.get('enabled', False)}\n"
            
            if result.get('enabled') and result.get('rules'):
                response += f"\n## Forwarding Rules ({len(result.get('rules'))})\n"
                for rule in result.get('rules', []):
                    response += f"- **Description**: {rule.get('description')}\n"
                    response += f"  - VLAN: {rule.get('vlanId')}\n"
                    response += f"  - Services: {', '.join(rule.get('services', []))}\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error getting Bonjour forwarding: {str(e)}"
    
    @app.tool(
        name="update_network_wireless_ssid_bonjour_forwarding",
        description="📡🍎 Update Bonjour forwarding settings for a wireless SSID"
    )
    def update_network_wireless_ssid_bonjour_forwarding(
        network_id: str,
        number: str,
        enabled: bool,
        rules: Optional[str] = None
    ):
        """Update SSID Bonjour forwarding configuration."""
        try:
            kwargs = {'enabled': enabled}
            
            if rules and enabled:
                kwargs['rules'] = json.loads(rules) if isinstance(rules, str) else rules
            
            result = meraki_client.dashboard.wireless.updateNetworkWirelessSsidBonjourForwarding(
                network_id, number, **kwargs
            )
            
            status = "Enabled ✅" if result.get('enabled') else "Disabled ❌"
            return f"✅ Updated SSID {number} Bonjour forwarding - {status}"
            
        except Exception as e:
            return f"❌ Error updating Bonjour forwarding: {str(e)}"

# ==================== EAP SETTINGS ====================

def register_eap_tools():
    """Register EAP override configuration tools."""
    
    @app.tool(
        name="get_network_wireless_ssid_eap_override",
        description="📡🔑 Get EAP override settings for a wireless SSID"
    )
    def get_network_wireless_ssid_eap_override(
        network_id: str,
        number: str
    ):
        """Get SSID EAP override configuration."""
        try:
            result = meraki_client.dashboard.wireless.getNetworkWirelessSsidEapOverride(
                network_id, number
            )
            
            response = f"# 📡 SSID {number} - EAP Override Settings\n\n"
            
            if result.get('timeout'):
                response += f"**Timeout**: {result.get('timeout')} seconds\n"
            
            if result.get('maxRetries'):
                response += f"**Max Retries**: {result.get('maxRetries')}\n"
            
            if result.get('identity'):
                response += f"**Identity Request**: {result.get('identity', {}).get('timeout')} seconds\n"
                response += f"**Identity Retries**: {result.get('identity', {}).get('retries')}\n"
            
            if result.get('eapolKey'):
                eapol = result.get('eapolKey', {})
                response += f"\n## EAPOL Key Settings\n"
                response += f"- **Timeout**: {eapol.get('timeout')} ms\n"
                response += f"- **Retries**: {eapol.get('retries')}\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error getting EAP override: {str(e)}"
    
    @app.tool(
        name="update_network_wireless_ssid_eap_override",
        description="📡🔑 Update EAP override settings for a wireless SSID"
    )
    def update_network_wireless_ssid_eap_override(
        network_id: str,
        number: str,
        timeout: Optional[int] = None,
        max_retries: Optional[int] = None,
        eapol_key_timeout: Optional[int] = None,
        eapol_key_retries: Optional[int] = None
    ):
        """Update SSID EAP override configuration."""
        try:
            kwargs = {}
            
            if timeout:
                kwargs['timeout'] = timeout
            if max_retries:
                kwargs['maxRetries'] = max_retries
            
            if eapol_key_timeout or eapol_key_retries:
                kwargs['eapolKey'] = {}
                if eapol_key_timeout:
                    kwargs['eapolKey']['timeout'] = eapol_key_timeout
                if eapol_key_retries:
                    kwargs['eapolKey']['retries'] = eapol_key_retries
            
            result = meraki_client.dashboard.wireless.updateNetworkWirelessSsidEapOverride(
                network_id, number, **kwargs
            )
            
            return f"✅ Updated SSID {number} EAP override settings"
            
        except Exception as e:
            return f"❌ Error updating EAP override: {str(e)}"

# ==================== DEVICE TYPE GROUP POLICIES ====================

def register_device_type_tools():
    """Register device type group policy tools."""
    
    @app.tool(
        name="get_network_wireless_ssid_device_type_group_policies",
        description="📡📱 Get device type group policies for a wireless SSID"
    )
    def get_network_wireless_ssid_device_type_group_policies(
        network_id: str,
        number: str
    ):
        """Get SSID device type group policies."""
        try:
            result = meraki_client.dashboard.wireless.getNetworkWirelessSsidDeviceTypeGroupPolicies(
                network_id, number
            )
            
            response = f"# 📡 SSID {number} - Device Type Group Policies\n\n"
            response += f"**Enabled**: {result.get('enabled', False)}\n"
            
            if result.get('enabled') and result.get('deviceTypePolicies'):
                response += f"\n## Device Policies ({len(result.get('deviceTypePolicies'))})\n"
                for policy in result.get('deviceTypePolicies', []):
                    response += f"- **Device Type**: {policy.get('deviceType')}\n"
                    response += f"  - Policy: {policy.get('devicePolicy')}\n"
                    if policy.get('groupPolicyId'):
                        response += f"  - Group Policy ID: {policy.get('groupPolicyId')}\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error getting device type policies: {str(e)}"
    
    @app.tool(
        name="update_network_wireless_ssid_device_type_group_policies",
        description="📡📱 Update device type group policies for a wireless SSID"
    )
    def update_network_wireless_ssid_device_type_group_policies(
        network_id: str,
        number: str,
        enabled: bool,
        device_type_policies: Optional[str] = None
    ):
        """Update SSID device type group policies."""
        try:
            kwargs = {'enabled': enabled}
            
            if device_type_policies and enabled:
                kwargs['deviceTypePolicies'] = json.loads(device_type_policies) if isinstance(device_type_policies, str) else device_type_policies
            
            result = meraki_client.dashboard.wireless.updateNetworkWirelessSsidDeviceTypeGroupPolicies(
                network_id, number, **kwargs
            )
            
            status = "Enabled ✅" if result.get('enabled') else "Disabled ❌"
            return f"✅ Updated SSID {number} device type policies - {status}"
            
        except Exception as e:
            return f"❌ Error updating device type policies: {str(e)}"

# ==================== ALTERNATE MANAGEMENT INTERFACE ====================

def register_alt_mgmt_tools():
    """Register alternate management interface tools."""
    
    @app.tool(
        name="get_network_wireless_alternate_management_interface",
        description="📡🔧 Get alternate management interface settings for wireless network"
    )
    def get_network_wireless_alternate_management_interface(network_id: str):
        """Get alternate management interface configuration."""
        try:
            result = meraki_client.dashboard.wireless.getNetworkWirelessAlternateManagementInterface(
                network_id
            )
            
            response = f"# 📡 Alternate Management Interface\n\n"
            response += f"**Enabled**: {result.get('enabled', False)}\n"
            
            if result.get('enabled'):
                response += f"**VLAN**: {result.get('vlanId', 'N/A')}\n"
                response += f"**Protocol**: {result.get('protocols', [])}\n"
                
                access_points = result.get('accessPoints', [])
                if access_points:
                    response += f"\n## Configured APs ({len(access_points)})\n"
                    for ap in access_points[:5]:  # Show first 5
                        response += f"- {ap.get('serial')}: {ap.get('name', 'Unnamed')}\n"
                        response += f"  - IP: {ap.get('alternateManagementIp')}\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error getting alternate management interface: {str(e)}"
    
    @app.tool(
        name="update_network_wireless_alternate_management_interface",
        description="📡🔧 Update alternate management interface settings for wireless network"
    )
    def update_network_wireless_alternate_management_interface(
        network_id: str,
        enabled: bool,
        vlan_id: Optional[int] = None,
        protocols: Optional[str] = None,
        access_points: Optional[str] = None
    ):
        """Update alternate management interface configuration."""
        try:
            kwargs = {'enabled': enabled}
            
            if vlan_id and enabled:
                kwargs['vlanId'] = vlan_id
            
            if protocols and enabled:
                kwargs['protocols'] = json.loads(protocols) if isinstance(protocols, str) else protocols
            
            if access_points and enabled:
                kwargs['accessPoints'] = json.loads(access_points) if isinstance(access_points, str) else access_points
            
            result = meraki_client.dashboard.wireless.updateNetworkWirelessAlternateManagementInterface(
                network_id, **kwargs
            )
            
            status = "Enabled ✅" if result.get('enabled') else "Disabled ❌"
            return f"✅ Updated alternate management interface - {status}"
            
        except Exception as e:
            return f"❌ Error updating alternate management interface: {str(e)}"

# ==================== BLUETOOTH SETTINGS ====================

def register_bluetooth_tools():
    """Register Bluetooth configuration tools."""
    
    @app.tool(
        name="get_network_wireless_bluetooth_settings",
        description="📡🔵 Get Bluetooth settings for wireless network"
    )
    def get_network_wireless_bluetooth_settings(network_id: str):
        """Get network Bluetooth settings."""
        try:
            result = meraki_client.dashboard.wireless.getNetworkWirelessBluetoothSettings(
                network_id
            )
            
            response = f"# 📡 Network Bluetooth Settings\n\n"
            response += f"**Scanning Enabled**: {result.get('scanningEnabled', False)}\n"
            response += f"**Advertising Enabled**: {result.get('advertisingEnabled', False)}\n"
            
            if result.get('uuid'):
                response += f"**UUID**: {result.get('uuid')}\n"
            
            if result.get('majorMinorAssignmentMode'):
                response += f"**Major/Minor Mode**: {result.get('majorMinorAssignmentMode')}\n"
            
            if result.get('major'):
                response += f"**Major**: {result.get('major')}\n"
            
            if result.get('minor'):
                response += f"**Minor**: {result.get('minor')}\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error getting Bluetooth settings: {str(e)}"
    
    @app.tool(
        name="update_network_wireless_bluetooth_settings",
        description="📡🔵 Update Bluetooth settings (majorMinorMode: 'Unique' or 'Non-unique')"
    )
    def update_network_wireless_bluetooth_settings(
        network_id: str,
        scanning_enabled: Optional[bool] = None,
        advertising_enabled: Optional[bool] = None,
        uuid: Optional[str] = None,
        major_minor_mode: Optional[str] = None,
        major: Optional[int] = None,
        minor: Optional[int] = None
    ):
        """Update network Bluetooth settings."""
        try:
            kwargs = {}
            
            if scanning_enabled is not None:
                kwargs['scanningEnabled'] = scanning_enabled
            if advertising_enabled is not None:
                kwargs['advertisingEnabled'] = advertising_enabled
            if uuid:
                kwargs['uuid'] = uuid
            if major_minor_mode:
                kwargs['majorMinorAssignmentMode'] = major_minor_mode
                # Major and minor only valid when mode is 'Non-unique'
                if major_minor_mode == 'Non-unique':
                    if major is not None:
                        kwargs['major'] = major
                    if minor is not None:
                        kwargs['minor'] = minor
            elif major is not None or minor is not None:
                # If no mode specified but major/minor provided, assume Non-unique
                kwargs['major'] = major
                kwargs['minor'] = minor
            
            result = meraki_client.dashboard.wireless.updateNetworkWirelessBluetoothSettings(
                network_id, **kwargs
            )
            
            scan = "✅" if result.get('scanningEnabled') else "❌"
            adv = "✅" if result.get('advertisingEnabled') else "❌"
            return f"✅ Updated Bluetooth - Scanning: {scan}, Advertising: {adv}"
            
        except Exception as e:
            return f"❌ Error updating Bluetooth settings: {str(e)}"
    
    @app.tool(
        name="get_device_wireless_bluetooth_settings",
        description="📡🔵 Get Bluetooth settings for a specific wireless device"
    )
    def get_device_wireless_bluetooth_settings(serial: str):
        """Get device Bluetooth settings."""
        try:
            result = meraki_client.dashboard.wireless.getDeviceWirelessBluetoothSettings(serial)
            
            response = f"# 📡 Device {serial} - Bluetooth Settings\n\n"
            response += f"**UUID**: {result.get('uuid', 'N/A')}\n"
            response += f"**Major**: {result.get('major', 'N/A')}\n"
            response += f"**Minor**: {result.get('minor', 'N/A')}\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error getting device Bluetooth settings: {str(e)}"
    
    @app.tool(
        name="update_device_wireless_bluetooth_settings",
        description="📡🔵 Update Bluetooth settings for a specific wireless device"
    )
    def update_device_wireless_bluetooth_settings(
        serial: str,
        uuid: Optional[str] = None,
        major: Optional[int] = None,
        minor: Optional[int] = None
    ):
        """Update device Bluetooth settings."""
        try:
            kwargs = {}
            
            if uuid:
                kwargs['uuid'] = uuid
            if major is not None:
                kwargs['major'] = major
            if minor is not None:
                kwargs['minor'] = minor
            
            result = meraki_client.dashboard.wireless.updateDeviceWirelessBluetoothSettings(
                serial, **kwargs
            )
            
            return f"✅ Updated device {serial} Bluetooth settings"
            
        except Exception as e:
            return f"❌ Error updating device Bluetooth: {str(e)}"

# ==================== AIR MARSHAL RULES ====================

def register_air_marshal_tools():
    """Register Air Marshal security tools."""
    
    @app.tool(
        name="get_organization_wireless_air_marshal_rules",
        description="📡🛡️ Get Air Marshal rules for organization"
    )
    def get_organization_wireless_air_marshal_rules(
        organization_id: str,
        network_ids: Optional[str] = None
    ):
        """Get organization Air Marshal rules."""
        try:
            kwargs = {}
            if network_ids:
                kwargs['networkIds'] = json.loads(network_ids) if isinstance(network_ids, str) else network_ids
            
            result = meraki_client.dashboard.wireless.getOrganizationWirelessAirMarshalRules(
                organization_id, **kwargs
            )
            
            response = f"# 🛡️ Organization Air Marshal Rules\n\n"
            
            items = result.get('items', [])
            if items:
                response += f"**Total Rules**: {len(items)}\n\n"
                for rule in items[:10]:  # Show first 10
                    response += f"## Rule: {rule.get('ruleId')}\n"
                    response += f"- **Type**: {rule.get('type')}\n"
                    response += f"- **Match**: {rule.get('match', {})}\n"
                    if rule.get('network'):
                        response += f"- **Network**: {rule.get('network', {}).get('name')}\n"
            else:
                response += "No Air Marshal rules configured\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error getting Air Marshal rules: {str(e)}"
    
    # @app.tool(
    # name="create_network_wireless_air_marshal_rule",
    # description="📡🛡️ Create an Air Marshal rule for network"
    # )
    # def create_network_wireless_air_marshal_rule(
    # network_id: str,
    # type: str,
    # match_string: Optional[str] = None,
    # match_type: Optional[str] = None
    # ):
    # """Create network Air Marshal rule."""
    #     try:
    #         kwargs = {'type': type}
    #         
    #         if match_string and match_type:
    #             kwargs['match'] = {
    #                 'string': match_string,
    #                 'type': match_type
    #             }
    #         
    #         result = meraki_client.dashboard.wireless.createNetworkWirelessAirMarshalRule(
    #             network_id, **kwargs
    #         )
    #         
    #         return f"✅ Created Air Marshal rule - Type: {result.get('type')}"
    #         
    #     except Exception as e:
    #         return f"❌ Error creating Air Marshal rule: {str(e)}"
    
    @app.tool(
        name="update_network_wireless_air_marshal_rule",
        description="📡🛡️ Update an Air Marshal rule for network"
    )
    def update_network_wireless_air_marshal_rule(
        network_id: str,
        rule_id: str,
        type: Optional[str] = None,
        match_string: Optional[str] = None,
        match_type: Optional[str] = None
    ):
        """Update network Air Marshal rule."""
        try:
            kwargs = {}
            
            if type:
                kwargs['type'] = type
            
            if match_string and match_type:
                kwargs['match'] = {
                    'string': match_string,
                    'type': match_type
                }
            
            result = meraki_client.dashboard.wireless.updateNetworkWirelessAirMarshalRule(
                network_id, rule_id, **kwargs
            )
            
            return f"✅ Updated Air Marshal rule {rule_id}"
            
        except Exception as e:
            return f"❌ Error updating Air Marshal rule: {str(e)}"
    
    # @app.tool(
    # name="delete_network_wireless_air_marshal_rule",
    # description="📡🛡️ Delete an Air Marshal rule from network"
    # )
    # def delete_network_wireless_air_marshal_rule(
    # network_id: str,
    # rule_id: str
    # ):
    # """Delete network Air Marshal rule."""
    # try:
    #     meraki_client.dashboard.wireless.deleteNetworkWirelessAirMarshalRule(
    #         network_id, rule_id
    #     )
    #     
    #     return f"✅ Deleted Air Marshal rule {rule_id}"
    #     
    # except Exception as e:
    #     return f"❌ Error deleting Air Marshal rule: {str(e)}"
    
    @app.tool(
        name="update_network_wireless_air_marshal_settings",
        description="📡🛡️ Update Air Marshal settings for network"
    )
    def update_network_wireless_air_marshal_settings(
        network_id: str,
        default_policy: str
    ):
        """Update network Air Marshal settings."""
        try:
            result = meraki_client.dashboard.wireless.updateNetworkWirelessAirMarshalSettings(
                network_id,
                defaultPolicy=default_policy
            )
            
            return f"✅ Updated Air Marshal settings - Default Policy: {result.get('defaultPolicy')}"
            
        except Exception as e:
            return f"❌ Error updating Air Marshal settings: {str(e)}"

# ==================== ETHERNET PORTS PROFILES ====================

def register_ethernet_ports_tools():
    """Register Ethernet ports profile tools."""
    
    @app.tool(
        name="get_network_wireless_ethernet_ports_profiles",
        description="📡🔌 Get Ethernet ports profiles for wireless network"
    )
    def get_network_wireless_ethernet_ports_profiles(network_id: str):
        """Get network Ethernet ports profiles."""
        try:
            result = meraki_client.dashboard.wireless.getNetworkWirelessEthernetPortsProfiles(
                network_id
            )
            
            response = f"# 📡 Ethernet Ports Profiles\n\n"
            
            profiles = result
            if profiles:
                response += f"**Total Profiles**: {len(profiles)}\n\n"
                for profile in profiles:
                    response += f"## Profile: {profile.get('name')}\n"
                    response += f"- **ID**: {profile.get('profileId')}\n"
                    response += f"- **Is Default**: {profile.get('isDefault', False)}\n"
                    
                    ports = profile.get('ports', [])
                    if ports:
                        response += f"- **Ports**: {len(ports)} configured\n"
                        for port in ports:
                            response += f"  - Port {port.get('name')}: "
                            response += f"VLAN {port.get('vlan')}, "
                            response += f"Enabled: {port.get('enabled')}\n"
            else:
                response += "No Ethernet ports profiles configured\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error getting Ethernet ports profiles: {str(e)}"
    
    @app.tool(
        name="create_network_wireless_ethernet_ports_profile",
        description="📡🔌 Create an Ethernet ports profile for wireless network"
    )
    def create_network_wireless_ethernet_ports_profile(
        network_id: str,
        name: str,
        ports: str,
        usb_ports: Optional[str] = None
    ):
        """Create network Ethernet ports profile."""
        try:
            kwargs = {
                'name': name,
                'ports': json.loads(ports) if isinstance(ports, str) else ports
            }
            
            if usb_ports:
                kwargs['usbPorts'] = json.loads(usb_ports) if isinstance(usb_ports, str) else usb_ports
            
            result = meraki_client.dashboard.wireless.createNetworkWirelessEthernetPortsProfile(
                network_id, **kwargs
            )
            
            return f"✅ Created Ethernet ports profile '{result.get('name')}' - ID: {result.get('profileId')}"
            
        except Exception as e:
            return f"❌ Error creating Ethernet ports profile: {str(e)}"
    
    @app.tool(
        name="update_network_wireless_ethernet_ports_profile",
        description="📡🔌 Update an Ethernet ports profile for wireless network"
    )
    def update_network_wireless_ethernet_ports_profile(
        network_id: str,
        profile_id: str,
        name: Optional[str] = None,
        ports: Optional[str] = None,
        usb_ports: Optional[str] = None
    ):
        """Update network Ethernet ports profile."""
        try:
            kwargs = {}
            
            if name:
                kwargs['name'] = name
            if ports:
                kwargs['ports'] = json.loads(ports) if isinstance(ports, str) else ports
            if usb_ports:
                kwargs['usbPorts'] = json.loads(usb_ports) if isinstance(usb_ports, str) else usb_ports
            
            result = meraki_client.dashboard.wireless.updateNetworkWirelessEthernetPortsProfile(
                network_id, profile_id, **kwargs
            )
            
            return f"✅ Updated Ethernet ports profile '{result.get('name')}'"
            
        except Exception as e:
            return f"❌ Error updating Ethernet ports profile: {str(e)}"
    
    @app.tool(
        name="delete_network_wireless_ethernet_ports_profile",
        description="📡🔌 Delete an Ethernet ports profile from wireless network"
    )
    def delete_network_wireless_ethernet_ports_profile(
        network_id: str,
        profile_id: str
    ):
        """Delete network Ethernet ports profile."""
        try:
            meraki_client.dashboard.wireless.deleteNetworkWirelessEthernetPortsProfile(
                network_id, profile_id
            )
            
            return f"✅ Deleted Ethernet ports profile {profile_id}"
            
        except Exception as e:
            return f"❌ Error deleting Ethernet ports profile: {str(e)}"
    
    @app.tool(
        name="assign_network_wireless_ethernet_ports_profiles",
        description="📡🔌 Assign Ethernet ports profiles to APs"
    )
    def assign_network_wireless_ethernet_ports_profiles(
        network_id: str,
        serials: str,
        profile_id: str
    ):
        """Assign Ethernet ports profiles to APs."""
        try:
            result = meraki_client.dashboard.wireless.assignNetworkWirelessEthernetPortsProfiles(
                network_id,
                serials=json.loads(serials) if isinstance(serials, str) else serials,
                profileId=profile_id
            )
            
            assigned = result.get('serials', [])
            return f"✅ Assigned profile {profile_id} to {len(assigned)} APs"
            
        except Exception as e:
            return f"❌ Error assigning Ethernet ports profiles: {str(e)}"

# ==================== LOCATION SCANNING ====================

def register_location_scanning_tools():
    """Register location scanning tools."""
    
    @app.tool(
        name="get_network_wireless_location_scanning",
        description="📡📍 Get location scanning settings (Note: Requires location analytics license)"
    )
    def get_network_wireless_location_scanning(network_id: str):
        """Get network location scanning settings."""
        try:
            # Get network info to find org ID
            network = meraki_client.dashboard.networks.getNetwork(network_id)
            org_id = network.get('organizationId')
            
            # Use org-level method to get location scanning by network
            result = meraki_client.dashboard.wireless.getOrganizationWirelessLocationScanningByNetwork(
                org_id
            )
            
            # Extract items from result (API returns dict with 'items' key)
            all_networks = result.get('items', []) if isinstance(result, dict) else result
            
            # Find this network's settings
            network_settings = None
            for net in all_networks:
                if net.get('networkId') == network_id:
                    network_settings = net
                    break
            
            if not network_settings:
                return f"# 📡 Location Scanning Settings\n\nLocation scanning not configured for this network.\n\n💡 Use 'update_network_wireless_location_scanning' to enable."
            
            response = f"# 📡 Location Scanning Settings\n\n"
            response += f"**Network**: {network_settings.get('name', network_id)}\n"
            response += f"**Location Analytics Enabled**: {network_settings.get('enabled', False)}\n"
            
            api_settings = network_settings.get('api', {})
            response += f"**Scanning API Enabled**: {api_settings.get('enabled', False)}\n"
            
            if api_settings.get('validator', {}).get('string'):
                response += f"**Validator**: [CONFIGURED]\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error getting location scanning: {str(e)}"
    
    @app.tool(
        name="update_network_wireless_location_scanning",
        description="📡📍 Update location scanning settings for wireless network"
    )
    def update_network_wireless_location_scanning(
        network_id: str,
        analytics_enabled: Optional[bool] = None,
        scanning_api_enabled: Optional[bool] = None,
        scanning_api_receiver_secret: Optional[str] = None
    ):
        """Update network location scanning settings."""
        try:
            kwargs = {}
            
            if analytics_enabled is not None:
                kwargs['analyticsEnabled'] = analytics_enabled
            if scanning_api_enabled is not None:
                kwargs['scanningApiEnabled'] = scanning_api_enabled
            if scanning_api_receiver_secret:
                kwargs['scanningApiReceiverSecret'] = scanning_api_receiver_secret
            
            result = meraki_client.dashboard.wireless.updateNetworkWirelessLocationScanning(
                network_id, **kwargs
            )
            
            analytics = "✅" if result.get('analyticsEnabled') else "❌"
            api = "✅" if result.get('scanningApiEnabled') else "❌"
            return f"✅ Updated location scanning - Analytics: {analytics}, API: {api}"
            
        except Exception as e:
            return f"❌ Error updating location scanning: {str(e)}"

# ==================== RADSEC CERTIFICATES ====================

def register_radsec_tools():
    """Register RADSEC certificate tools."""
    
    @app.tool(
        name="get_organization_wireless_radsec_certificate_authorities",
        description="📡🔒 Get RADSEC certificate authorities for organization"
    )
    def get_organization_wireless_radsec_certificate_authorities(
        organization_id: str
    ):
        """Get organization RADSEC certificate authorities."""
        try:
            result = meraki_client.dashboard.wireless.getOrganizationWirelessDevicesRadsecCertificateAuthorities(
                organization_id
            )
            
            response = f"# 🔒 RADSEC Certificate Authorities\n\n"
            
            cas = result
            if cas:
                response += f"**Total CAs**: {len(cas)}\n\n"
                for ca in cas:
                    response += f"## CA: {ca.get('name')}\n"
                    response += f"- **ID**: {ca.get('certificateId')}\n"
                    response += f"- **Contents**: {ca.get('contents', '')[:100]}...\n"
                    response += f"- **Root**: {ca.get('root', False)}\n"
            else:
                response += "No RADSEC certificate authorities configured\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error getting RADSEC CAs: {str(e)}"
    
    @app.tool(
        name="create_organization_wireless_radsec_certificate_authority",
        description="📡🔒 Create a RADSEC certificate authority for organization"
    )
    def create_organization_wireless_radsec_certificate_authority(
        organization_id: str,
        name: str,
        contents: str,
        root: Optional[bool] = False
    ):
        """Create organization RADSEC certificate authority."""
        try:
            result = meraki_client.dashboard.wireless.createOrganizationWirelessDevicesRadsecCertificateAuthority(
                organization_id,
                name=name,
                contents=contents,
                root=root
            )
            
            return f"✅ Created RADSEC CA '{result.get('name')}' - ID: {result.get('certificateId')}"
            
        except Exception as e:
            return f"❌ Error creating RADSEC CA: {str(e)}"
    
    @app.tool(
        name="update_organization_wireless_radsec_certificate_authorities",
        description="📡🔒 Update RADSEC certificate authorities for organization"
    )
    def update_organization_wireless_radsec_certificate_authorities(
        organization_id: str,
        certificate_ids: str
    ):
        """Update organization RADSEC certificate authorities."""
        try:
            result = meraki_client.dashboard.wireless.updateOrganizationWirelessDevicesRadsecCertificateAuthorities(
                organization_id,
                certificateIds=json.loads(certificate_ids) if isinstance(certificate_ids, str) else certificate_ids
            )
            
            return f"✅ Updated RADSEC certificate authorities"
            
        except Exception as e:
            return f"❌ Error updating RADSEC CAs: {str(e)}"

# ==================== ELECTRONIC SHELF LABELS ====================

def register_esl_tools():
    """Register Electronic Shelf Label tools."""
    
    @app.tool(
        name="get_network_wireless_electronic_shelf_label",
        description="📡🏷️ Get Electronic Shelf Label settings for network"
    )
    def get_network_wireless_electronic_shelf_label(network_id: str):
        """Get network ESL settings."""
        try:
            result = meraki_client.dashboard.wireless.getNetworkWirelessElectronicShelfLabel(
                network_id
            )
            
            response = f"# 🏷️ Electronic Shelf Label Settings\n\n"
            response += f"**Enabled**: {result.get('enabled', False)}\n"
            
            if result.get('enabled'):
                response += f"**Provider**: {result.get('provider', 'N/A')}\n"
                if result.get('hostname'):
                    response += f"**Hostname**: {result.get('hostname')}\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error getting ESL settings: {str(e)}"
    
    @app.tool(
        name="update_network_wireless_electronic_shelf_label",
        description="📡🏷️ Update Electronic Shelf Label settings for network"
    )
    def update_network_wireless_electronic_shelf_label(
        network_id: str,
        enabled: bool,
        provider: Optional[str] = None,
        hostname: Optional[str] = None
    ):
        """Update network ESL settings."""
        try:
            kwargs = {'enabled': enabled}
            
            if provider and enabled:
                kwargs['provider'] = provider
            if hostname and enabled:
                kwargs['hostname'] = hostname
            
            result = meraki_client.dashboard.wireless.updateNetworkWirelessElectronicShelfLabel(
                network_id, **kwargs
            )
            
            status = "Enabled ✅" if result.get('enabled') else "Disabled ❌"
            return f"✅ Updated ESL settings - {status}"
            
        except Exception as e:
            return f"❌ Error updating ESL settings: {str(e)}"
    
    @app.tool(
        name="get_device_wireless_electronic_shelf_label",
        description="📡🏷️ Get Electronic Shelf Label settings for device"
    )
    def get_device_wireless_electronic_shelf_label(serial: str):
        """Get device ESL settings."""
        try:
            result = meraki_client.dashboard.wireless.getDeviceWirelessElectronicShelfLabel(serial)
            
            response = f"# 🏷️ Device {serial} - ESL Settings\n\n"
            response += f"**Enabled**: {result.get('enabled', False)}\n"
            
            if result.get('enabled'):
                response += f"**Provider**: {result.get('provider', 'N/A')}\n"
                response += f"**Channel**: {result.get('channel', 'N/A')}\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error getting device ESL settings: {str(e)}"
    
    @app.tool(
        name="update_device_wireless_electronic_shelf_label",
        description="📡🏷️ Update Electronic Shelf Label settings for device"
    )
    def update_device_wireless_electronic_shelf_label(
        serial: str,
        enabled: Optional[bool] = None,
        channel: Optional[str] = None
    ):
        """Update device ESL settings."""
        try:
            kwargs = {}
            
            if enabled is not None:
                kwargs['enabled'] = enabled
            if channel:
                kwargs['channel'] = channel
            
            result = meraki_client.dashboard.wireless.updateDeviceWirelessElectronicShelfLabel(
                serial, **kwargs
            )
            
            status = "Enabled ✅" if result.get('enabled') else "Disabled ❌"
            return f"✅ Updated device ESL settings - {status}"
            
        except Exception as e:
            return f"❌ Error updating device ESL: {str(e)}"

# ==================== BILLING ====================

def register_billing_tools():
    """Register wireless billing tools."""
    
    @app.tool(
        name="get_network_wireless_billing",
        description="📡💰 Get wireless billing settings for network"
    )
    def get_network_wireless_billing(network_id: str):
        """Get network wireless billing settings."""
        try:
            result = meraki_client.dashboard.wireless.getNetworkWirelessBilling(
                network_id
            )
            
            response = f"# 💰 Wireless Billing Settings\n\n"
            response += f"**Currency**: {result.get('currency', 'N/A')}\n"
            
            plans = result.get('plans', [])
            if plans:
                response += f"\n## Billing Plans ({len(plans)})\n"
                for plan in plans:
                    response += f"- **{plan.get('id')}**: {plan.get('name')}\n"
                    response += f"  - Price: {plan.get('price')} {result.get('currency')}\n"
                    response += f"  - Time Limit: {plan.get('timeLimit')} minutes\n"
                    response += f"  - Bandwidth Limit: {plan.get('bandwidthLimits', {})}\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error getting billing settings: {str(e)}"
    
    @app.tool(
        name="update_network_wireless_billing",
        description="📡💰 Update wireless billing settings for network"
    )
    def update_network_wireless_billing(
        network_id: str,
        currency: Optional[str] = None,
        plans: Optional[str] = None
    ):
        """Update network wireless billing settings."""
        try:
            kwargs = {}
            
            if currency:
                kwargs['currency'] = currency
            if plans:
                kwargs['plans'] = json.loads(plans) if isinstance(plans, str) else plans
            
            result = meraki_client.dashboard.wireless.updateNetworkWirelessBilling(
                network_id, **kwargs
            )
            
            return f"✅ Updated billing settings - Currency: {result.get('currency')}"
            
        except Exception as e:
            return f"❌ Error updating billing settings: {str(e)}"

# ==================== FIREWALL ISOLATION ALLOWLIST ====================

def register_isolation_allowlist_tools():
    """Register firewall isolation allowlist tools."""
    
    @app.tool(
        name="get_organization_wireless_ssids_firewall_isolation_allowlist",
        description="📡🔥 Get SSID firewall isolation allowlist for organization"
    )
    def get_organization_wireless_ssids_firewall_isolation_allowlist(
        organization_id: str,
        per_page: Optional[int] = 1000
    ):
        """Get organization SSID firewall isolation allowlist."""
        try:
            result = meraki_client.dashboard.wireless.getOrganizationWirelessSsidsFirewallIsolationAllowlistEntries(
                organization_id,
                perPage=per_page
            )
            
            response = f"# 🔥 SSID Firewall Isolation Allowlist\n\n"
            
            entries = result
            if entries:
                response += f"**Total Entries**: {len(entries)}\n\n"
                for entry in entries[:20]:  # Show first 20
                    response += f"- **{entry.get('mac')}**: {entry.get('comment', 'No comment')}\n"
            else:
                response += "No isolation allowlist entries configured\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error getting isolation allowlist: {str(e)}"
    
    @app.tool(
        name="create_org_wireless_isolation_allowlist_entry",
        description="📡🔥 Create SSID firewall isolation allowlist entry"
    )
    def create_organization_wireless_ssids_firewall_isolation_allowlist_entry(
        organization_id: str,
        mac: str,
        comment: Optional[str] = None
    ):
        """Create organization SSID firewall isolation allowlist entry."""
        try:
            kwargs = {'mac': mac}
            
            if comment:
                kwargs['comment'] = comment
            
            result = meraki_client.dashboard.wireless.createOrganizationWirelessSsidsFirewallIsolationAllowlistEntry(
                organization_id, **kwargs
            )
            
            return f"✅ Created isolation allowlist entry for {result.get('mac')}"
            
        except Exception as e:
            return f"❌ Error creating isolation allowlist entry: {str(e)}"
    
    @app.tool(
        name="update_org_wireless_isolation_allowlist_entry",
        description="📡🔥 Update SSID firewall isolation allowlist entry"
    )
    def update_organization_wireless_ssids_firewall_isolation_allowlist_entry(
        organization_id: str,
        entry_id: str,
        mac: Optional[str] = None,
        comment: Optional[str] = None
    ):
        """Update organization SSID firewall isolation allowlist entry."""
        try:
            kwargs = {}
            
            if mac:
                kwargs['mac'] = mac
            if comment:
                kwargs['comment'] = comment
            
            result = meraki_client.dashboard.wireless.updateOrganizationWirelessSsidsFirewallIsolationAllowlistEntry(
                organization_id, entry_id, **kwargs
            )
            
            return f"✅ Updated isolation allowlist entry {entry_id}"
            
        except Exception as e:
            return f"❌ Error updating isolation allowlist entry: {str(e)}"
    
    @app.tool(
        name="delete_org_wireless_isolation_allowlist_entry",
        description="📡🔥 Delete SSID firewall isolation allowlist entry"
    )
    def delete_organization_wireless_ssids_firewall_isolation_allowlist_entry(
        organization_id: str,
        entry_id: str
    ):
        """Delete organization SSID firewall isolation allowlist entry."""
        try:
            meraki_client.dashboard.wireless.deleteOrganizationWirelessSsidsFirewallIsolationAllowlistEntry(
                organization_id, entry_id
            )
            
            return f"✅ Deleted isolation allowlist entry {entry_id}"
            
        except Exception as e:
            return f"❌ Error deleting isolation allowlist entry: {str(e)}"