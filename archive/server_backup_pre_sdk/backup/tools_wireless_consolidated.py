"""
Wireless tools for Cisco Meraki MCP server.
Consolidated from multiple modules to match SDK structure.
"""

from typing import Any
from typing import Optional, List, Dict, Any
import json

# Global references to be set by register function
app = None
meraki_client = None

def register_wireless_tools(mcp_app, meraki):
    """
    Register wireless tools with the MCP server.
    
    Args:
        mcp_app: MCP server instance
        meraki: Meraki client instance
    """
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    
    @app.tool(
            name="get_network_wireless_ssids",
            description="List wireless SSIDs for a Meraki network"
        )
        def get_network_wireless_ssids(network_id: str):
            """
            List wireless SSIDs for a Meraki network.
            
            Args:
                network_id: ID of the network
                
            Returns:
                Formatted list of SSIDs
            """
            try:
                ssids = meraki_client.get_network_wireless_ssids(network_id)
                
                if not ssids:
                    return f"No wireless SSIDs found for network {network_id}."
                    
                # Format the output for readability
                result = f"# Wireless SSIDs in Network ({network_id})\n\n"
                for ssid in ssids:
                    result += f"## SSID {ssid.get('number', 'Unknown')}: {ssid.get('name', 'Unnamed')}\n"
                    result += f"- Enabled: {ssid.get('enabled', False)}\n"
                    result += f"- Visible: {ssid.get('visible', False)}\n"
                    
                    # Add security settings
                    auth_mode = ssid.get('authMode', 'Unknown')
                    result += f"- Authentication: {auth_mode}\n"
                    
                    if auth_mode != 'open':
                        encryption_mode = ssid.get('encryptionMode', 'Unknown')
                        result += f"- Encryption: {encryption_mode}\n"
                    
                    # Add IP assignment mode
                    ip_mode = ssid.get('ipAssignmentMode', 'Unknown')
                    result += f"- IP Assignment Mode: {ip_mode}\n"
                    
                    # Add VLAN settings if in bridge mode
                    if ip_mode == 'Bridge mode':
                        use_vlan = ssid.get('useVlanTagging', False)
                        if use_vlan:
                            result += f"- VLAN Tagging: Enabled\n"
                            result += f"- VLAN ID: {ssid.get('defaultVlanId', 'Not set')}\n"
                    
                    # Add additional settings
                    result += f"- Band Selection: {ssid.get('bandSelection', 'Unknown')}\n"
                    result += f"- Minimum Bitrate: {ssid.get('minBitrate', 'Unknown')}\n"
                    
                    # LAN isolation
                    if ssid.get('lanIsolationEnabled'):
                        result += f"- LAN Isolation: Enabled\n"
                    
                    result += "\n"
                    
                return result
                
            except Exception as e:
                return f"Failed to list wireless SSIDs for network {network_id}: {str(e)}"
        
        
    @app.tool(
            name="get_network_wireless_passwords",
            description="🔑 Get WiFi passwords/PSK - retrieve for security audits, password complexity checks, credential sharing"
        )
        def get_network_wireless_passwords(network_id: str):
            """
            Get WiFi passwords/PSK for wireless networks.
            
            Args:
                network_id: ID of the network
                
            Returns:
                Formatted list of SSIDs with passwords where available
            """
            try:
                ssids = meraki_client.get_network_wireless_passwords(network_id)
                
                if not ssids:
                    return f"No wireless SSIDs found for network {network_id}."
                    
                result = f"# 🔑 WiFi Passwords for Network ({network_id})\n\n"
                
                for ssid in ssids:
                    ssid_name = ssid.get('name', 'Unnamed')
                    ssid_number = ssid.get('number', 'Unknown')
                    enabled = ssid.get('enabled', False)
                    
                    result += f"## SSID {ssid_number}: {ssid_name}\n"
                    result += f"- **Status**: {'🟢 Enabled' if enabled else '🔴 Disabled'}\n"
                    
                    auth_mode = ssid.get('authMode', 'Unknown')
                    result += f"- **Security**: {auth_mode}\n"
                    
                    # Show password/PSK if available
                    if auth_mode in ['psk', 'wpa', 'wpa-eap', '8021x-radius']:
                        psk = ssid.get('psk')
                        if psk:
                            result += f"- **🔑 Password/PSK**: `{psk}`\n"
                        else:
                            result += f"- **🔑 Password/PSK**: Not available via API\n"
                    elif auth_mode == 'open':
                        result += f"- **🔑 Password/PSK**: Open network (no password required)\n"
                    else:
                        result += f"- **🔑 Password/PSK**: Enterprise authentication\n"
                    
                    # Add RADIUS settings if available
                    if ssid.get('radiusServers'):
                        result += f"- **RADIUS Servers**: {len(ssid['radiusServers'])} configured\n"
                    
                    result += "\n"
                    
                return result
                
            except Exception as e:
                return f"Error retrieving WiFi passwords for network {network_id}: {str(e)}"
        
        
    @app.tool(
            name="update_network_wireless_ssid",
            description="🔐 Update wireless SSID - security, bridge mode, VLAN tagging, and more"
        )
        def update_network_wireless_ssid(network_id: str, ssid_number: int, name: str = None, enabled: bool = None,
                                       auth_mode: str = None, psk: str = None, encryption_mode: str = None,
                                       wpa_encryption_mode: str = None, visible: bool = None,
                                       ip_assignment_mode: str = None, use_vlan_tagging: bool = None,
                                       vlan_id: int = None, default_vlan_id: int = None,
                                       lan_isolation_enabled: bool = None):
            """
            Update a wireless SSID for a Meraki network with full configuration support.
            
            Args:
                network_id: ID of the network
                ssid_number: Number of the SSID to update (0-14)
                name: New name for the SSID (optional)
                enabled: Whether the SSID should be enabled (optional)
                auth_mode: Authentication mode - 'open', 'psk', '8021x-radius', etc (optional)
                psk: Pre-shared key (password) - only valid when auth_mode is 'psk' (optional)
                encryption_mode: Encryption mode - 'open', 'wep', 'wpa' (required if auth_mode is 'psk')
                wpa_encryption_mode: WPA mode - 'WPA2 only', 'WPA3 only', etc (optional)
                visible: Whether SSID is broadcast (optional)
                ip_assignment_mode: 'NAT mode' or 'Bridge mode' or 'Layer 3 roaming' (optional)
                use_vlan_tagging: Enable VLAN tagging (required for Bridge mode with VLANs) (optional)
                vlan_id: The VLAN ID to use when use_vlan_tagging is true (optional)
                default_vlan_id: Default VLAN ID for the SSID (optional)
                lan_isolation_enabled: Prevent wireless clients from communicating with each other (optional)
                
            Returns:
                Updated SSID details
                
            Examples:
                1. WPA2-PSK with password:
                   auth_mode='psk', psk='YourPassword', encryption_mode='wpa', wpa_encryption_mode='WPA2 only'
                
                2. Bridge mode to local network:
                   ip_assignment_mode='Bridge mode'
                
                3. Bridge mode with VLAN 100:
                   ip_assignment_mode='Bridge mode', use_vlan_tagging=True, vlan_id=100
            """
            try:
                # Convert snake_case to camelCase for API
                result = meraki_client.update_network_wireless_ssid(
                    network_id, 
                    ssid_number, 
                    name=name, 
                    enabled=enabled,
                    authMode=auth_mode,
                    psk=psk,
                    encryptionMode=encryption_mode,
                    wpaEncryptionMode=wpa_encryption_mode,
                    visible=visible,
                    ipAssignmentMode=ip_assignment_mode,
                    useVlanTagging=use_vlan_tagging,
                    vlanId=vlan_id,
                    defaultVlanId=default_vlan_id,
                    lanIsolationEnabled=lan_isolation_enabled
                )
                
                # Format success message
                updates = []
                if name is not None:
                    updates.append(f"name='{name}'")
                if enabled is not None:
                    updates.append(f"enabled={enabled}")
                if auth_mode is not None:
                    updates.append(f"auth='{auth_mode}'")
                if psk is not None:
                    updates.append(f"password='***'")
                if encryption_mode is not None:
                    updates.append(f"encryption='{encryption_mode}'")
                if wpa_encryption_mode is not None:
                    updates.append(f"wpa='{wpa_encryption_mode}'")
                if visible is not None:
                    updates.append(f"visible={visible}")
                if ip_assignment_mode is not None:
                    updates.append(f"IP mode='{ip_assignment_mode}'")
                if use_vlan_tagging is not None:
                    updates.append(f"VLAN tagging={use_vlan_tagging}")
                if vlan_id is not None:
                    updates.append(f"VLAN ID={vlan_id}")
                if default_vlan_id is not None:
                    updates.append(f"default VLAN={default_vlan_id}")
                if lan_isolation_enabled is not None:
                    updates.append(f"LAN isolation={lan_isolation_enabled}")
                    
                return f"✅ SSID {ssid_number} updated successfully: {', '.join(updates)}"
                
            except Exception as e:
                return f"❌ Failed to update SSID: {str(e)}"
        
        # DUPLICATE: Commented out - using version at line 805 which has timespan parameter
        # 
    @app.tool(
            name="get_network_wireless_client",
            description="Get details for a specific wireless client"
        )
        def get_network_wireless_client(network_id: str, client_id: str):
            """
            Get details for a specific wireless client.
            
            Args:
                network_id: ID of the network
                client_id: ID of the client (MAC address)
                
            Returns:
                Detailed information about the wireless client
            """
            try:
                client = meraki_client.dashboard.networks.getNetworkClient(network_id, client_id)
                
                result = f"# Wireless Client Details\n\n"
                result += f"**MAC Address**: {client.get('mac', 'N/A')}\n"
                result += f"**Description**: {client.get('description', 'N/A')}\n"
                result += f"**IP**: {client.get('ip', 'N/A')}\n"
                result += f"**IPv6**: {client.get('ip6', 'N/A')}\n"
                result += f"**User**: {client.get('user', 'N/A')}\n"
                result += f"**VLAN**: {client.get('vlan', 'N/A')}\n"
                result += f"**Manufacturer**: {client.get('manufacturer', 'N/A')}\n"
                result += f"**OS**: {client.get('os', 'N/A')}\n"
                result += f"**SSID**: {client.get('ssid', 'N/A')}\n"
                result += f"**Status**: {client.get('status', 'N/A')}\n"
                result += f"**Last Seen**: {client.get('lastSeen', 'N/A')}\n"
                result += f"**Switch Port**: {client.get('switchport', 'N/A')}\n"
                
                usage = client.get('usage', {})
                if usage:
                    result += f"\n## Usage\n"
                    result += f"- Sent: {usage.get('sent', 0):,} bytes\n"
                    result += f"- Received: {usage.get('recv', 0):,} bytes\n"
                
                return result
                
            except Exception as e:
                return f"Failed to get wireless client {client_id}: {str(e)}"
        
        
    @app.tool(
            name="get_network_wireless_rf_profiles",
            description="📡 Get RF profiles for a wireless network"
        )
        def get_network_wireless_rf_profiles(network_id: str):
            """
            Get RF profiles for a wireless network.
            
            Args:
                network_id: ID of the network
                
            Returns:
                RF profiles configuration
            """
            try:
                profiles = meraki_client.get_network_wireless_rf_profiles(network_id)
                
                if not profiles:
                    return f"No RF profiles found for network {network_id}."
                    
                result = f"# 📡 RF Profiles for Network {network_id}\n\n"
                
                for profile in profiles:
                    result += f"## {profile.get('name', 'Unnamed Profile')}\n"
                    result += f"- **ID**: {profile.get('id')}\n"
                    result += f"- **Band Selection**: {profile.get('bandSelectionType', 'N/A')}\n"
                    result += f"- **Min Bitrate (2.4GHz)**: {profile.get('minBitrate', 'N/A')}\n"
                    result += f"- **Min Bitrate (5GHz)**: {profile.get('minBitrate5', 'N/A')}\n"
                    
                    # Client balancing
                    client_balancing = profile.get('clientBalancingEnabled')
                    if client_balancing is not None:
                        result += f"- **Client Balancing**: {'✅ Enabled' if client_balancing else '❌ Disabled'}\n"
                        
                    result += "\n"
                    
                return result
                
            except Exception as e:
                return f"Error retrieving RF profiles: {str(e)}"
        # DUPLICATE: Commented out - better implementation in tools_wireless_client_analytics.py
        '''
        
    @app.tool(
            name="get_network_wireless_air_marshal",
            description="🛡️ Get Air Marshal security scan results"
        )
        def get_network_wireless_air_marshal(network_id: str, timespan: int = 3600):
            """
            Get Air Marshal (rogue AP detection) results for a network.
            
            Args:
                network_id: ID of the network
                timespan: Timespan in seconds (default: 1 hour)
                
            Returns:
                Air Marshal security scan results
            """
            try:
                air_marshal = meraki_client.get_network_wireless_air_marshal(network_id, timespan)
                
                if not air_marshal:
                    return f"No Air Marshal data found for network {network_id}."
                    
                result = f"# 🛡️ Air Marshal Security Scan - Network {network_id}\n"
                result += f"**Time Period**: Last {timespan/3600:.1f} hours\n\n"
                
                # Group by classification
                rogues = []
                neighbors = []
                others = []
                
                for ap in air_marshal:
                    classification = ap.get('wiredMacClassification', 'Unknown')
                    if 'Rogue' in classification:
                        rogues.append(ap)
                    elif 'Neighbor' in classification:
                        neighbors.append(ap)
                    else:
                        others.append(ap)
                        
                if rogues:
                    result += f"## 🚨 ROGUE APs DETECTED ({len(rogues)})\n"
                    for ap in rogues[:5]:  # Show first 5
                        result += f"- **SSID**: {ap.get('ssid', 'Hidden')}\n"
                        result += f"  - MAC: {ap.get('bssid')}\n"
                        result += f"  - Channel: {ap.get('channel')}\n"
                        result += f"  - RSSI: {ap.get('rssi')} dBm\n"
                        result += f"  - First Seen: {ap.get('firstSeen')}\n"
                        result += f"  - Last Seen: {ap.get('lastSeen')}\n\n"
                        
                if neighbors:
                    result += f"## 📶 Neighbor APs ({len(neighbors)})\n"
                    result += f"Detected {len(neighbors)} neighboring networks.\n\n"
                    
                return result
                
            except Exception as e:
                return f"Error retrieving Air Marshal data: {str(e)}"
        '''
        
        
    @app.tool(
            name="get_network_wireless_bluetooth_clients", 
            description="📱 Get Bluetooth clients in a wireless network"
        )
        def get_network_wireless_bluetooth_clients(network_id: str):
            """
            Get Bluetooth clients detected in a wireless network.
            
            Args:
                network_id: ID of the network
                
            Returns:
                List of Bluetooth clients
            """
            try:
                bt_clients = meraki_client.get_network_wireless_bluetooth_clients(network_id)
                
                if not bt_clients:
                    return f"No Bluetooth clients found in network {network_id}."
                    
                result = f"# 📱 Bluetooth Clients in Network {network_id}\n\n"
                result += f"**Total Clients**: {len(bt_clients)}\n\n"
                
                for client in bt_clients[:20]:  # Show first 20
                    result += f"- **{client.get('name', 'Unknown Device')}**\n"
                    result += f"  - MAC: {client.get('mac')}\n"
                    result += f"  - Manufacturer: {client.get('manufacturer', 'Unknown')}\n"
                    result += f"  - RSSI: {client.get('rssi')} dBm\n"
                    result += f"  - Last Seen: {client.get('lastSeen')}\n"
                    
                    tags = client.get('tags', [])
                    if tags:
                        result += f"  - Tags: {', '.join(tags)}\n"
                        
                    result += "\n"
                    
                if len(bt_clients) > 20:
                    result += f"... and {len(bt_clients) - 20} more clients\n"
                    
                return result
                
            except Exception as e:
                return f"Error retrieving Bluetooth clients: {str(e)}"
        
        
    @app.tool(
            name="configure_ssid_bridge_mode",
            description="🌉 Quick setup for WiFi bridge mode - connects wireless clients to local network"
        )
        def configure_ssid_bridge_mode(network_id: str, ssid_number: int, vlan_id: int = None):
            """
            Configure an SSID for bridge mode to connect wireless clients to the local network.
            
            Args:
                network_id: ID of the network
                ssid_number: Number of the SSID to configure (0-14)
                vlan_id: Optional VLAN ID for tagged traffic (omit for untagged/native VLAN)
                
            Returns:
                Configuration result
                
            Example:
                - Bridge to native VLAN: configure_ssid_bridge_mode(network_id, 0)
                - Bridge to VLAN 100: configure_ssid_bridge_mode(network_id, 0, vlan_id=100)
            """
            try:
                # Get current SSID config first
                ssids = meraki_client.get_network_wireless_ssids(network_id)
                current_ssid = next((s for s in ssids if s.get('number') == ssid_number), None)
                
                if not current_ssid:
                    return f"❌ SSID {ssid_number} not found"
                
                ssid_name = current_ssid.get('name', f'SSID {ssid_number}')
                
                # Configure bridge mode
                kwargs = {
                    'ipAssignmentMode': 'Bridge mode',
                    'useVlanTagging': vlan_id is not None
                }
                
                if vlan_id:
                    kwargs['vlanId'] = vlan_id
                
                result = meraki_client.update_network_wireless_ssid(
                    network_id,
                    ssid_number,
                    **kwargs
                )
                
                # Format response
                if vlan_id:
                    return f"""✅ Bridge Mode Configured for {ssid_name}!
                    
    **Configuration:**
    - IP Assignment: Bridge mode
    - VLAN Tagging: Enabled
    - VLAN ID: {vlan_id}
    
    **Result:** Wireless clients will now:
    - Receive IP addresses from VLAN {vlan_id}'s DHCP server
    - Be on the same network as wired devices in VLAN {vlan_id}
    - Have direct access to local network resources"""
                else:
                    return f"""✅ Bridge Mode Configured for {ssid_name}!
                    
    **Configuration:**
    - IP Assignment: Bridge mode
    - VLAN Tagging: Disabled (native/untagged VLAN)
    
    **Result:** Wireless clients will now:
    - Receive IP addresses from your main network's DHCP server
    - Be on the same network as wired devices
    - Have direct access to all local network resources"""
                
            except Exception as e:
                return f"❌ Error configuring bridge mode: {str(e)}"
        
        
    @app.tool(
            name="get_composite_wireless_health",
            description="Get comprehensive wireless health check for a network"
        )
        def get_composite_wireless_health(
            network_id: str,
            check_ssids: bool = True,
            check_clients: bool = True,
            check_aps: bool = True,
            check_rf: bool = True
        ):
            """
            Perform a comprehensive wireless health check.
            
            Args:
                network_id: Network ID
                check_ssids: Check SSID configurations
                check_clients: Check client connections
                check_aps: Check access point status
                check_rf: Check RF health
                
            Returns:
                Comprehensive health report
            """
            try:
                result = "# 📊 Wireless Health Check Report\n\n"
                
                # Check SSIDs
                if check_ssids:
                    try:
                        ssids = meraki_client.dashboard.wireless.getNetworkWirelessSsids(network_id)
                        enabled_ssids = [s for s in ssids if s.get('enabled')]
                        result += f"## SSIDs\n"
                        result += f"- Total SSIDs: {len(ssids)}\n"
                        result += f"- Enabled SSIDs: {len(enabled_ssids)}\n"
                        for ssid in enabled_ssids:
                            result += f"  - **{ssid.get('name', 'Unnamed')}** (#{ssid.get('number')})\n"
                    except Exception as e:
                        result += f"## SSIDs\n- ⚠️ Error checking SSIDs: {str(e)}\n"
                
                # Check Access Points
                if check_aps:
                    try:
                        devices = meraki_client.dashboard.networks.getNetworkDevices(network_id)
                        aps = [d for d in devices if d.get('model', '').startswith('MR')]
                        
                        # Better status detection
                        online_aps = []
                        offline_aps = []
                        unknown_aps = []
                        
                        for ap in aps:
                            status = ap.get('status', 'unknown')
                            if status == 'online' or (status == 'unknown' and ap.get('lanIp')):
                                online_aps.append(ap)
                            elif status == 'offline':
                                offline_aps.append(ap)
                            else:
                                unknown_aps.append(ap)
                        
                        result += f"\n## Access Points\n"
                        result += f"- Total APs: {len(aps)}\n"
                        result += f"- Online APs: {len(online_aps)}\n"
                        result += f"- Offline APs: {len(offline_aps)}\n"
                        if unknown_aps:
                            result += f"- Unknown Status: {len(unknown_aps)}\n"
                        
                        for ap in aps:
                            status = ap.get('status', 'unknown')
                            if status == 'online' or (status == 'unknown' and ap.get('lanIp')):
                                status_icon = "✅"
                            elif status == 'offline':
                                status_icon = "❌"
                            else:
                                status_icon = "⚠️"
                            
                            ap_info = f"**{ap.get('name', ap.get('serial'))}** ({ap.get('model')})"
                            if ap.get('lanIp'):
                                ap_info += f" - IP: {ap.get('lanIp')}"
                            result += f"  - {status_icon} {ap_info}\n"
                    except Exception as e:
                        result += f"\n## Access Points\n- ⚠️ Error checking APs: {str(e)}\n"
                
                # Check Clients
                if check_clients:
                    try:
                        clients = meraki_client.dashboard.networks.getNetworkClients(
                            network_id, 
                            timespan=300,
                            perPage=100
                        )
                        wireless_clients = [c for c in clients if c.get('ssid')]
                        result += f"\n## Connected Clients\n"
                        result += f"- Total wireless clients: {len(wireless_clients)}\n"
                        if wireless_clients:
                            ssid_counts = {}
                            for client in wireless_clients:
                                ssid = client.get('ssid', 'Unknown')
                                ssid_counts[ssid] = ssid_counts.get(ssid, 0) + 1
                            result += "- Clients per SSID:\n"
                            for ssid, count in ssid_counts.items():
                                result += f"  - {ssid}: {count} clients\n"
                    except Exception as e:
                        result += f"\n## Connected Clients\n- ⚠️ Error checking clients: {str(e)}\n"
                
                # Check RF Health
                if check_rf:
                    try:
                        rf_profiles = meraki_client.dashboard.wireless.getNetworkWirelessRfProfiles(network_id)
                        result += f"\n## RF Configuration\n"
                        result += f"- RF Profiles configured: {len(rf_profiles)}\n"
                        for profile in rf_profiles:
                            result += f"  - **{profile.get('name')}** ({profile.get('bandSelectionType')})\n"
                    except Exception as e:
                        result += f"\n## RF Configuration\n- ⚠️ Error checking RF: {str(e)}\n"
                
                result += "\n---\n✅ Health check complete!"
                return result
                
            except Exception as e:
                return f"❌ Error performing health check: {str(e)}"
        
        
    @app.tool(
            name="get_network_wireless_access_points",
            description="Get wireless access points in a network"
        )
        def get_network_wireless_access_points(network_id: str):
            """
            Get wireless access points in a network.
            Maps to getNetworkDevices filtered for wireless APs.
            
            Args:
                network_id: Network ID
                
            Returns:
                List of wireless access points
            """
            try:
                devices = meraki_client.dashboard.networks.getNetworkDevices(network_id)
                
                # Filter for wireless APs (models starting with MR)
                aps = [d for d in devices if d.get('model', '').startswith('MR')]
                
                if not aps:
                    return f"No wireless access points found in network {network_id}"
                
                result = f"# Wireless Access Points\n\n"
                for ap in aps:
                    # Determine status with fallback
                    status = ap.get('status', 'unknown')
                    if status == 'online':
                        status_icon = "✅"
                    elif status == 'offline':
                        status_icon = "❌"
                    else:
                        status_icon = "⚠️"
                        # If no status field, check other indicators
                        if ap.get('lanIp'):
                            status = 'online'
                            status_icon = "✅"
                    
                    result += f"## {ap.get('name', ap.get('serial'))}\n"
                    result += f"- Model: {ap.get('model')}\n"
                    result += f"- Serial: {ap.get('serial')}\n"
                    result += f"- Status: {status_icon} {status}\n"
                    result += f"- MAC: {ap.get('mac')}\n"
                    if ap.get('lanIp'):
                        result += f"- IP: {ap.get('lanIp')}\n"
                    if ap.get('tags'):
                        result += f"- Tags: {', '.join(ap.get('tags'))}\n"
                    if ap.get('firmware'):
                        result += f"- Firmware: {ap.get('firmware')}\n"
                    result += "\n"
                
                return result
                
            except Exception as e:
                return f"Error getting access points: {str(e)}"
        
        
    @app.tool(
            name="get_network_wireless_clients",
            description="Get wireless clients connected to a network"
        )
        def get_network_wireless_clients(network_id: str, timespan: int = 300):
            """
            Get wireless clients connected to a network.
            
            Args:
                network_id: Network ID
                timespan: Time span in seconds (default 300 = 5 minutes)
                
            Returns:
                List of wireless clients
            """
            try:
                clients = meraki_client.dashboard.networks.getNetworkClients(
                    network_id,
                    timespan=timespan,
                    perPage=1000
                )
                
                # Filter for wireless clients (those with SSID)
                wireless_clients = [c for c in clients if c.get('ssid')]
                
                if not wireless_clients:
                    return f"No wireless clients found in network {network_id} (last {timespan} seconds)"
                
                result = f"# Wireless Clients (Last {timespan} seconds)\n\n"
                result += f"Total wireless clients: {len(wireless_clients)}\n\n"
                
                # Group by SSID
                by_ssid = {}
                for client in wireless_clients:
                    ssid = client.get('ssid', 'Unknown')
                    if ssid not in by_ssid:
                        by_ssid[ssid] = []
                    by_ssid[ssid].append(client)
                
                for ssid, ssid_clients in by_ssid.items():
                    result += f"## SSID: {ssid} ({len(ssid_clients)} clients)\n"
                    for client in ssid_clients[:10]:  # Show first 10 per SSID
                        result += f"- {client.get('description', client.get('mac'))}\n"
                        result += f"  - IP: {client.get('ip', 'N/A')}\n"
                        result += f"  - MAC: {client.get('mac')}\n"
                        result += f"  - Usage: {client.get('usage', {}).get('sent', 0)} sent, {client.get('usage', {}).get('recv', 0)} recv\n"
                    if len(ssid_clients) > 10:
                        result += f"  ... and {len(ssid_clients) - 10} more\n"
                    result += "\n"
                
                return result
                
            except Exception as e:
                return f"Error getting wireless clients: {str(e)}"
        
        # DUPLICATE: Commented out - using version in tools_wireless_advanced.py
        # 
    @app.tool(
        #     name="get_network_wireless_failed_connections", 
        #     description="Get failed wireless connection attempts"
        # )
        def get_network_wireless_failed_connections_redirect(network_id: str, timespan: int = 86400):
            """
            Get failed wireless connection attempts.
            Wrapper for the SDK method in tools_wireless_advanced.
            
            Args:
                network_id: Network ID
                timespan: Time span in seconds (default 86400 = 24 hours)
                
            Returns:
                Failed connection events
            """
            try:
                # Call the SDK method
                failures = meraki_client.dashboard.wireless.getNetworkWirelessFailedConnections(
                    network_id,
                    timespan=timespan
                )
                
                if not failures:
                    return f"No failed connections in the last {timespan} seconds"
                
                result = f"# Failed Wireless Connections (Last {timespan} seconds)\n\n"
                result += f"Total failures: {len(failures)}\n\n"
                
                # Get all unique client MACs for name resolution
                all_client_macs = list(set(f.get('clientMac', '') for f in failures if f.get('clientMac')))
                
                # Try to fetch client details for name resolution
                client_names = {}
                try:
                    # Get current wireless clients to map MAC to names
                    # Use a longer timespan to catch clients that may have failed to connect
                    current_clients = meraki_client.dashboard.wireless.getNetworkWirelessClients(
                        network_id, 
                        timespan=max(86400, timespan)  # Look back at least 24 hours for client info
                    )
                    for client in current_clients:
                        mac = client.get('mac')
                        if mac:
                            # Use description (device name) if available, otherwise manufacturer
                            name = client.get('description')
                            if not name:
                                name = client.get('manufacturer')
                            if name:
                                client_names[mac] = name
                except:
                    # If we can't get client names, continue without them
                    pass
                
                # Group by failure type
                by_type = {}
                for failure in failures:
                    fail_type = failure.get('failureStep', 'Unknown')
                    if fail_type not in by_type:
                        by_type[fail_type] = []
                    by_type[fail_type].append(failure)
                
                for fail_type, type_failures in by_type.items():
                    result += f"## {fail_type} Failures ({len(type_failures)})\n"
                    for failure in type_failures[:5]:  # Show first 5 per type
                        client_mac = failure.get('clientMac', 'Unknown')
                        client_name = client_names.get(client_mac)
                        
                        # Show name with MAC in parentheses if we have a name
                        if client_name:
                            result += f"- Client: **{client_name}** ({client_mac})\n"
                        else:
                            result += f"- Client: {client_mac}\n"
                        
                        result += f"  - SSID: {failure.get('ssidNumber')}\n"
                        result += f"  - Time: {failure.get('ts')}\n"
                        result += f"  - Type: {failure.get('type')}\n"
                    if len(type_failures) > 5:
                        result += f"  ... and {len(type_failures) - 5} more\n"
                    result += "\n"
                
                return result
                
            except Exception as e:
                return f"Error getting failed connections: {str(e)}"
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
        # 
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
        # 
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
                
                # Try to get client names
                client_names = {}
                try:
                    wireless_clients = meraki_client.dashboard.wireless.getNetworkWirelessClients(
                        network_id, timespan=max(86400, timespan or 86400)
                    )
                    for wc in wireless_clients:
                        mac = wc.get('mac')
                        if mac:
                            name = wc.get('description') or wc.get('manufacturer')
                            if name:
                                client_names[mac] = name
                except:
                    pass
                
                response = f"# 📊 Clients Connection Stats\n\n"
                
                if isinstance(result, list):
                    response += f"**Total Clients**: {len(result)}\n\n"
                    
                    for client in result[:5]:  # Show first 5
                        client_mac = client.get('mac', 'Unknown')
                        client_name = client_names.get(client_mac)
                        
                        if client_name:
                            response += f"## Client: **{client_name}**\n"
                            response += f"   MAC: {client_mac}\n"
                        else:
                            response += f"## Client: {client_mac}\n"
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
                
                # Try to get client names
                client_names = {}
                try:
                    wireless_clients = meraki_client.dashboard.wireless.getNetworkWirelessClients(
                        network_id, timespan=max(86400, timespan or 86400)
                    )
                    for wc in wireless_clients:
                        mac = wc.get('mac')
                        if mac:
                            name = wc.get('description') or wc.get('manufacturer')
                            if name:
                                client_names[mac] = name
                except:
                    pass
                
                response = f"# 📊 Clients Latency Stats\n\n"
                
                if isinstance(result, list):
                    response += f"**Total Clients**: {len(result)}\n\n"
                    
                    # Sort by average latency
                    sorted_clients = sorted(result, 
                        key=lambda x: x.get('latencyStats', {}).get('backgroundTraffic', {}).get('avg', 0),
                        reverse=True)
                    
                    response += "## Clients with Highest Latency\n"
                    for client in sorted_clients[:5]:
                        client_mac = client.get('mac', 'Unknown')
                        client_name = client_names.get(client_mac)
                        
                        if client_name:
                            response += f"- **{client_name}** ({client_mac})\n"
                        else:
                            response += f"- **{client_mac}**\n"
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
        # 
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
        
        # 
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
            """This API doesn't exist at network level - redirect to org level."""
            return ("❌ This network-level API doesn't exist in the Meraki SDK.\n\n"
                    "✅ **Use the organization-level tool instead:**\n"
                    "Tool name: `get_organization_wireless_rf_profiles_assignments_by_device`\n\n"
                    "**Example usage:**\n"
                    "```\n"
                    "get_organization_wireless_rf_profiles_assignments_by_device(\n"
                    "    organization_id='686470',\n"
                    f"    network_ids='{network_id}'  # Filter for specific network\n"
                    ")\n"
                    "```\n\n"
                    "This tool provides RF profile assignments for all devices in the organization,\n"
                    "and you can filter by specific networks using the network_ids parameter.")
        
        
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
                            ssid_name = ssid.get('ssid', '(Hidden)')
                            response += f"- **{ssid_name if ssid_name else '(Empty SSID)'}**\n"
                            
                            # Get channels at SSID level
                            channels = ssid.get('channels', [])
                            if channels:
                                response += f"  - Channels: {', '.join(map(str, channels[:5]))}\n"
                            
                            # Get BSSIDs and their details
                            bssids = ssid.get('bssids', [])
                            if bssids:
                                # Show first BSSID with best RSSI
                                best_bssid = None
                                best_rssi = -200
                                
                                for bssid_info in bssids[:3]:  # Check first 3 BSSIDs
                                    bssid_mac = bssid_info.get('bssid')
                                    detected_by = bssid_info.get('detectedBy', [])
                                    
                                    for detector in detected_by:
                                        rssi = detector.get('rssi', -200)
                                        if rssi > best_rssi:
                                            best_rssi = rssi
                                            best_bssid = bssid_mac
                                
                                if best_bssid:
                                    response += f"  - BSSID: {best_bssid}\n"
                                    if best_rssi > -200:
                                        response += f"  - Best RSSI: {best_rssi} dBm\n"
                                
                                response += f"  - Total BSSIDs: {len(bssids)}\n"
                
                return response
                
            except Exception as e:
                return f"❌ Error getting Air Marshal data: {str(e)}"
        
        
    @app.tool(
            name="get_network_wireless_ssid_l3_firewall_rules",
            description="📡🔥 Get L3 firewall rules for a wireless SSID"
        )
        def get_network_wireless_ssid_l3_firewall_rules(
            network_id: str,
            number: str
        ):
            """
            Get L3 firewall rules for a wireless SSID.
            
            Args:
                network_id: Network ID
                number: SSID number (0-14)
                
            Returns:
                L3 firewall rules for the SSID
            """
            try:
                result = meraki_client.dashboard.wireless.getNetworkWirelessSsidFirewallL3FirewallRules(
                    network_id,
                    number
                )
                
                rules = result.get('rules', [])
                
                response = f"# 📡 Wireless SSID {number} - L3 Firewall Rules\n\n"
                
                if not rules:
                    response += "No L3 firewall rules configured (default: allow all)\n"
                else:
                    response += f"**Total Rules**: {len(rules)}\n\n"
                    
                    for i, rule in enumerate(rules, 1):
                        policy = rule.get('policy', 'allow')
                        icon = "✅" if policy == 'allow' else "🚫"
                        
                        response += f"## Rule {i}: {icon} {policy.upper()}\n"
                        
                        comment = rule.get('comment')
                        if comment:
                            response += f"**Comment**: {comment}\n"
                        
                        response += f"- **Protocol**: {rule.get('protocol', 'any')}\n"
                        response += f"- **Source**: {rule.get('srcCidr', 'any')}\n"
                        response += f"- **Source Port**: {rule.get('srcPort', 'any')}\n"
                        response += f"- **Destination**: {rule.get('destCidr', 'any')}\n"
                        response += f"- **Dest Port**: {rule.get('destPort', 'any')}\n\n"
                
                response += "\n💡 **Note**: Rules are evaluated top to bottom. First match wins."
                
                return response
                
            except Exception as e:
                return f"❌ Error getting L3 firewall rules: {str(e)}"
        
        
    @app.tool(
            name="get_network_wireless_ssid_traffic_shaping",
            description="📡🚦 Get traffic shaping rules for a wireless SSID"
        )
        def get_network_wireless_ssid_traffic_shaping(
            network_id: str,
            number: str
        ):
            """
            Get traffic shaping configuration for a wireless SSID.
            
            Args:
                network_id: Network ID
                number: SSID number (0-14)
                
            Returns:
                Traffic shaping configuration
            """
            try:
                result = meraki_client.dashboard.wireless.getNetworkWirelessSsidTrafficShapingRules(
                    network_id,
                    number
                )
                
                response = f"# 📡 Wireless SSID {number} - Traffic Shaping\n\n"
                
                # Overall settings
                enabled = result.get('trafficShapingEnabled', False)
                response += f"**Traffic Shaping**: {'Enabled ✅' if enabled else 'Disabled ❌'}\n"
                
                if enabled:
                    # Default per-client limits
                    default_limits = result.get('defaultRulesEnabled', False)
                    if default_limits:
                        response += f"\n## Default Per-Client Limits\n"
                        response += f"- **Upload**: {result.get('perClientBandwidthLimits', {}).get('limitUp', 'Unlimited')} Mbps\n"
                        response += f"- **Download**: {result.get('perClientBandwidthLimits', {}).get('limitDown', 'Unlimited')} Mbps\n"
                    
                    # SSID bandwidth limits
                    ssid_limits = result.get('bandwidthLimits', {})
                    if ssid_limits:
                        response += f"\n## SSID Total Bandwidth Limits\n"
                        response += f"- **Upload**: {ssid_limits.get('limitUp', 'Unlimited')} Mbps\n"
                        response += f"- **Download**: {ssid_limits.get('limitDown', 'Unlimited')} Mbps\n"
                    
                    # Traffic shaping rules
                    rules = result.get('rules', [])
                    if rules:
                        response += f"\n## Traffic Shaping Rules ({len(rules)} total)\n"
                        for i, rule in enumerate(rules, 1):
                            response += f"\n### Rule {i}\n"
                            
                            # Definition
                            definitions = rule.get('definitions', [])
                            if definitions:
                                response += "**Matches**:\n"
                                for definition in definitions:
                                    def_type = definition.get('type')
                                    value = definition.get('value')
                                    response += f"  - {def_type}: {value}\n"
                            
                            # Limits
                            per_client = rule.get('perClientBandwidthLimits', {})
                            if per_client:
                                response += f"**Per-Client Limits**:\n"
                                response += f"  - Upload: {per_client.get('limitUp', 'Unlimited')} Mbps\n"
                                response += f"  - Download: {per_client.get('limitDown', 'Unlimited')} Mbps\n"
                            
                            # DSCP tagging
                            dscp = rule.get('dscpTagValue')
                            if dscp is not None:
                                response += f"**DSCP Tag**: {dscp}\n"
                            
                            # PCP tagging
                            pcp = rule.get('pcpTagValue')
                            if pcp is not None:
                                response += f"**PCP Tag**: {pcp}\n"
                
                return response
                
            except Exception as e:
                return f"❌ Error getting traffic shaping rules: {str(e)}"
        
        
    @app.tool(
            name="update_network_wireless_ssid_traffic_shaping",
            description="📡🚦 Update traffic shaping rules for a wireless SSID"
        )
        def update_network_wireless_ssid_traffic_shaping(
            network_id: str,
            number: str,
            enabled: Optional[bool] = None,
            per_client_bandwidth_up: Optional[int] = None,
            per_client_bandwidth_down: Optional[int] = None,
            ssid_bandwidth_up: Optional[int] = None,
            ssid_bandwidth_down: Optional[int] = None
        ):
            """
            Update traffic shaping configuration for a wireless SSID.
            
            Args:
                network_id: Network ID
                number: SSID number (0-14)
                enabled: Enable/disable traffic shaping
                per_client_bandwidth_up: Per-client upload limit in Mbps
                per_client_bandwidth_down: Per-client download limit in Mbps
                ssid_bandwidth_up: Total SSID upload limit in Mbps
                ssid_bandwidth_down: Total SSID download limit in Mbps
                
            Returns:
                Updated traffic shaping configuration
            """
            try:
                kwargs = {}
                
                if enabled is not None:
                    kwargs['trafficShapingEnabled'] = enabled
                
                # Per-client limits
                if per_client_bandwidth_up is not None or per_client_bandwidth_down is not None:
                    kwargs['defaultRulesEnabled'] = True
                    kwargs['perClientBandwidthLimits'] = {}
                    if per_client_bandwidth_up is not None:
                        kwargs['perClientBandwidthLimits']['limitUp'] = per_client_bandwidth_up
                    if per_client_bandwidth_down is not None:
                        kwargs['perClientBandwidthLimits']['limitDown'] = per_client_bandwidth_down
                
                # SSID total limits
                if ssid_bandwidth_up is not None or ssid_bandwidth_down is not None:
                    kwargs['bandwidthLimits'] = {}
                    if ssid_bandwidth_up is not None:
                        kwargs['bandwidthLimits']['limitUp'] = ssid_bandwidth_up
                    if ssid_bandwidth_down is not None:
                        kwargs['bandwidthLimits']['limitDown'] = ssid_bandwidth_down
                
                # Update traffic shaping
                result = meraki_client.dashboard.wireless.updateNetworkWirelessSsidTrafficShapingRules(
                    network_id,
                    number,
                    **kwargs
                )
                
                response = f"# ✅ Updated SSID {number} Traffic Shaping\n\n"
                
                if result.get('trafficShapingEnabled'):
                    response += "**Status**: Enabled ✅\n\n"
                    
                    if result.get('defaultRulesEnabled'):
                        limits = result.get('perClientBandwidthLimits', {})
                        response += "## Per-Client Limits\n"
                        response += f"- Upload: {limits.get('limitUp', 'Unlimited')} Mbps\n"
                        response += f"- Download: {limits.get('limitDown', 'Unlimited')} Mbps\n"
                    
                    ssid_limits = result.get('bandwidthLimits', {})
                    if ssid_limits:
                        response += "\n## SSID Total Limits\n"
                        response += f"- Upload: {ssid_limits.get('limitUp', 'Unlimited')} Mbps\n"
                        response += f"- Download: {ssid_limits.get('limitDown', 'Unlimited')} Mbps\n"
                else:
                    response += "**Status**: Disabled ❌\n"
                
                return response
                
            except Exception as e:
                return f"❌ Error updating traffic shaping: {str(e)}"
    @app.tool(
            name="get_device_wireless_alternate_management_interface",
            description="📡🔧 Get alternate management interface settings for wireless device"
        )
        def get_device_wireless_alternate_management_interface(serial: str):
            """Get device alternate management interface settings."""
            try:
                result = meraki_client.dashboard.wireless.getDeviceWirelessAlternateManagementInterface(serial)
                
                response = f"# 📡 Device {serial} - Alternate Management Interface\n\n"
                response += f"**Enabled**: {result.get('enabled', False)}\n"
                
                if result.get('enabled'):
                    response += f"**VLAN ID**: {result.get('vlanId', 'N/A')}\n"
                    protocols = result.get('protocols', [])
                    if protocols:
                        response += f"**Protocols**: {', '.join(protocols)}\n"
                        
                    aps = result.get('accessPoints', [])
                    if aps:
                        response += f"\n## Access Points ({len(aps)})\n"
                        for ap in aps[:5]:  # Show first 5
                            response += f"- {ap.get('serial', 'Unknown')}: {ap.get('alternateManagementIp', 'N/A')}\n"
                
                return response
                
            except Exception as e:
                return f"❌ Error getting alternate management interface: {str(e)}"
        
        
    @app.tool(
            name="update_device_wireless_alternate_management_interface",
            description="📡🔧 Update alternate management interface settings for wireless device"
        )
        def update_device_wireless_alternate_management_interface(
            serial: str,
            enabled: bool,
            vlan_id: Optional[int] = None,
            protocols: Optional[str] = None
        ):
            """Update device alternate management interface settings."""
            try:
                kwargs = {'enabled': enabled}
                
                if enabled and vlan_id:
                    kwargs['vlanId'] = vlan_id
                
                if enabled and protocols:
                    kwargs['protocols'] = json.loads(protocols) if isinstance(protocols, str) else protocols
                
                result = meraki_client.dashboard.wireless.updateDeviceWirelessAlternateManagementInterface(
                    serial, **kwargs
                )
                
                status = "Enabled ✅" if result.get('enabled') else "Disabled ❌"
                return f"✅ Updated alternate management interface for device {serial} - {status}"
                
            except Exception as e:
                return f"❌ Error updating alternate management interface: {str(e)}"
        
        
    @app.tool(
            name="get_device_wireless_alternate_management_interface_ipv6",
            description="📡🔧 Get IPv6 alternate management interface for wireless device"
        )
        def get_device_wireless_alternate_management_interface_ipv6(serial: str):
            """Get device IPv6 alternate management interface."""
            try:
                result = meraki_client.dashboard.wireless.getDeviceWirelessAlternateManagementInterfaceIpv6(serial)
                
                response = f"# 📡 Device {serial} - IPv6 Alternate Management\n\n"
                addresses = result.get('addresses', [])
                
                if addresses:
                    response += f"## IPv6 Addresses ({len(addresses)})\n"
                    for addr in addresses:
                        response += f"- **Address**: {addr.get('address', 'N/A')}\n"
                        response += f"  - Protocol: {addr.get('protocol', 'N/A')}\n"
                        response += f"  - Assignment: {addr.get('assignmentMode', 'N/A')}\n"
                        response += f"  - Gateway: {addr.get('gateway', 'N/A')}\n"
                        response += f"  - Prefix: {addr.get('prefix', 'N/A')}\n\n"
                else:
                    response += "No IPv6 addresses configured\n"
                
                return response
                
            except Exception as e:
                return f"❌ Error getting IPv6 alternate management: {str(e)}"
        
        
    @app.tool(
            name="update_device_wireless_alternate_management_interface_ipv6",
            description="📡🔧 Update IPv6 alternate management interface for wireless device"
        )
        def update_device_wireless_alternate_management_interface_ipv6(
            serial: str,
            addresses: Optional[str] = None
        ):
            """Update device IPv6 alternate management interface."""
            try:
                kwargs = {}
                if addresses:
                    kwargs['addresses'] = json.loads(addresses) if isinstance(addresses, str) else addresses
                
                result = meraki_client.dashboard.wireless.updateDeviceWirelessAlternateManagementInterfaceIpv6(
                    serial, **kwargs
                )
                
                return f"✅ Updated IPv6 alternate management for device {serial}"
                
            except Exception as e:
                return f"❌ Error updating IPv6 alternate management: {str(e)}"
        
        
    @app.tool(
            name="get_device_wireless_latency_stats",
            description="📡📊 Get latency statistics for a wireless device"
        )
        def get_device_wireless_latency_stats(
            serial: str,
            t0: Optional[str] = None,
            t1: Optional[str] = None,
            timespan: Optional[float] = 86400,
            band: Optional[str] = None,
            ssid: Optional[int] = None,
            vlan: Optional[int] = None,
            ap_tag: Optional[str] = None,
            fields: Optional[str] = None
        ):
            """Get device wireless latency statistics."""
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
                
                result = meraki_client.dashboard.wireless.getDeviceWirelessLatencyStats(serial, **kwargs)
                
                response = f"# 📊 Device {serial} - Latency Stats\n\n"
                if isinstance(result, dict):
                    response += f"**Background Traffic**: {result.get('backgroundTraffic', {}).get('avg', 0):.1f} ms avg\n"
                    response += f"**Best Effort**: {result.get('bestEffortTraffic', {}).get('avg', 0):.1f} ms avg\n"
                    response += f"**Video**: {result.get('videoTraffic', {}).get('avg', 0):.1f} ms avg\n"
                    response += f"**Voice**: {result.get('voiceTraffic', {}).get('avg', 0):.1f} ms avg\n"
                
                return response
                
            except Exception as e:
                return f"❌ Error getting device latency stats: {str(e)}"
    
    # ==================== MISSING NETWORK TOOLS (5) ====================
    
    def register_missing_network_tools():
        """Register missing network wireless tools."""
        
        
    @app.tool(
            name="get_network_wireless_electronic_shelf_label_configured_devices",
            description="📡🏷️ Get ESL configured devices for network"
        )
        def get_network_wireless_electronic_shelf_label_configured_devices(network_id: str):
            """Get ESL configured devices."""
            try:
                result = meraki_client.dashboard.wireless.getNetworkWirelessElectronicShelfLabelConfiguredDevices(
                    network_id
                )
                
                response = f"# 🏷️ ESL Configured Devices\n\n"
                if isinstance(result, list):
                    response += f"**Total Devices**: {len(result)}\n\n"
                    for device in result:
                        response += f"- **{device.get('name')}** ({device.get('serial')})\n"
                        response += f"  - Enabled: {device.get('enabled')}\n"
                        response += f"  - Provider: {device.get('provider')}\n"
                
                return response
                
            except Exception as e:
                return f"❌ Error getting ESL configured devices: {str(e)}"
        
        
    @app.tool(
            name="set_network_wireless_ethernet_ports_profiles_default",
            description="📡🔌 Set default Ethernet ports profile for network"
        )
        def set_network_wireless_ethernet_ports_profiles_default(
            network_id: str,
            profile_id: str
        ):
            """Set default Ethernet ports profile."""
            try:
                result = meraki_client.dashboard.wireless.setNetworkWirelessEthernetPortsProfilesDefault(
                    network_id,
                    profileId=profile_id
                )
                
                return f"✅ Set default Ethernet ports profile to {profile_id}"
                
            except Exception as e:
                return f"❌ Error setting default profile: {str(e)}"
        
        
    @app.tool(
            name="get_network_wireless_ethernet_ports_profile",
            description="📡🔌 Get a specific Ethernet ports profile"
        )
        def get_network_wireless_ethernet_ports_profile(
            network_id: str,
            profile_id: str
        ):
            """Get specific Ethernet ports profile."""
            try:
                result = meraki_client.dashboard.wireless.getNetworkWirelessEthernetPortsProfile(
                    network_id, profile_id
                )
                
                response = f"# 🔌 Ethernet Ports Profile\n\n"
                response += f"**Name**: {result.get('name')}\n"
                response += f"**ID**: {result.get('profileId')}\n"
                response += f"**Is Default**: {result.get('isDefault', False)}\n"
                
                ports = result.get('ports', [])
                if ports:
                    response += f"\n## Ports ({len(ports)})\n"
                    for port in ports:
                        response += f"- **{port.get('name')}**: "
                        response += f"VLAN {port.get('vlan')}, "
                        response += f"{'Enabled' if port.get('enabled') else 'Disabled'}\n"
                
                return response
                
            except Exception as e:
                return f"❌ Error getting Ethernet ports profile: {str(e)}"
        
        
    @app.tool(
            name="get_network_wireless_latency_history",
            description="📡📈 Get latency history for wireless network"
        )
        def get_network_wireless_latency_history(
            network_id: str,
            t0: Optional[str] = None,
            t1: Optional[str] = None,
            timespan: Optional[float] = 86400,
            resolution: Optional[int] = 300,
            auto_resolution: Optional[bool] = True,
            client_id: Optional[str] = None,
            device_serial: Optional[str] = None,
            ap_tag: Optional[str] = None,
            band: Optional[str] = None,
            ssid: Optional[int] = None
        ):
            """Get latency history for network."""
            try:
                kwargs = {}
                if t0:
                    kwargs['t0'] = t0
                if t1:
                    kwargs['t1'] = t1
                if timespan:
                    kwargs['timespan'] = timespan
                if resolution:
                    kwargs['resolution'] = resolution
                if auto_resolution is not None:
                    kwargs['autoResolution'] = auto_resolution
                if client_id:
                    kwargs['clientId'] = client_id
                if device_serial:
                    kwargs['deviceSerial'] = device_serial
                if ap_tag:
                    kwargs['apTag'] = ap_tag
                if band:
                    kwargs['band'] = band
                if ssid is not None:
                    kwargs['ssid'] = ssid
                
                result = meraki_client.dashboard.wireless.getNetworkWirelessLatencyHistory(
                    network_id, **kwargs
                )
                
                response = f"# 📈 Latency History\n\n"
                response += f"**Timespan**: {timespan/3600:.1f} hours\n"
                
                if isinstance(result, list) and result:
                    response += f"**Data Points**: {len(result)}\n\n"
                    
                    # Calculate averages
                    avg_bg = sum(d.get('backgroundTraffic', {}).get('avg', 0) for d in result) / len(result)
                    avg_be = sum(d.get('bestEffortTraffic', {}).get('avg', 0) for d in result) / len(result)
                    
                    response += f"## Average Latency\n"
                    response += f"- Background: {avg_bg:.1f} ms\n"
                    response += f"- Best Effort: {avg_be:.1f} ms\n"
                
                return response
                
            except Exception as e:
                return f"❌ Error getting latency history: {str(e)}"
    
    # ==================== MISSING ORGANIZATION TOOLS (13) ====================
    
    def register_missing_organization_tools():
        """Register missing organization wireless tools."""
        
        
    @app.tool(
            name="get_org_wireless_channel_util_history_by_device",
            description="📡📊 Get channel utilization history by device and interval"
        )
        def get_organization_wireless_devices_channel_utilization_history_by_device_by_interval(
            organization_id: str,
            network_ids: Optional[str] = None,
            serials: Optional[str] = None,
            t0: Optional[str] = None,
            t1: Optional[str] = None,
            timespan: Optional[float] = 86400,
            interval: Optional[int] = 300
        ):
            """Get channel utilization history by device and interval."""
            try:
                kwargs = {}
                if network_ids:
                    kwargs['networkIds'] = json.loads(network_ids) if isinstance(network_ids, str) else network_ids
                if serials:
                    kwargs['serials'] = json.loads(serials) if isinstance(serials, str) else serials
                if t0:
                    kwargs['t0'] = t0
                if t1:
                    kwargs['t1'] = t1
                if timespan:
                    kwargs['timespan'] = timespan
                if interval:
                    kwargs['interval'] = interval
                
                result = meraki_client.dashboard.wireless.getOrganizationWirelessDevicesChannelUtilizationHistoryByDeviceByInterval(
                    organization_id, **kwargs
                )
                
                response = f"# 📊 Channel Utilization History by Device\n\n"
                response += f"**Timespan**: {timespan/3600:.1f} hours\n"
                response += f"**Interval**: {interval} seconds\n\n"
                
                if isinstance(result, list) and result:
                    response += f"**Total Devices**: {len(result)}\n"
                    for device in result[:3]:
                        response += f"\n## Device: {device.get('serial')}\n"
                        by_interval = device.get('byInterval', [])
                        if by_interval:
                            recent = by_interval[0]
                            response += f"- Latest Total Utilization: {recent.get('utilization', {}).get('total', 0):.1f}%\n"
                
                return response
                
            except Exception as e:
                return f"❌ Error getting channel utilization history: {str(e)}"
        
        
    @app.tool(
            name="get_org_wireless_channel_util_history_by_network",
            description="📡📊 Get channel utilization history by network and interval"
        )
        def get_organization_wireless_devices_channel_utilization_history_by_network_by_interval(
            organization_id: str,
            network_ids: Optional[str] = None,
            serials: Optional[str] = None,
            t0: Optional[str] = None,
            t1: Optional[str] = None,
            timespan: Optional[float] = 86400,
            interval: Optional[int] = 300
        ):
            """Get channel utilization history by network and interval."""
            try:
                kwargs = {}
                if network_ids:
                    kwargs['networkIds'] = json.loads(network_ids) if isinstance(network_ids, str) else network_ids
                if serials:
                    kwargs['serials'] = json.loads(serials) if isinstance(serials, str) else serials
                if t0:
                    kwargs['t0'] = t0
                if t1:
                    kwargs['t1'] = t1
                if timespan:
                    kwargs['timespan'] = timespan
                if interval:
                    kwargs['interval'] = interval
                
                result = meraki_client.dashboard.wireless.getOrganizationWirelessDevicesChannelUtilizationHistoryByNetworkByInterval(
                    organization_id, **kwargs
                )
                
                response = f"# 📊 Channel Utilization History by Network\n\n"
                response += f"**Timespan**: {timespan/3600:.1f} hours\n"
                response += f"**Interval**: {interval} seconds\n\n"
                
                if isinstance(result, list) and result:
                    response += f"**Total Networks**: {len(result)}\n"
                    for network in result[:3]:
                        response += f"\n## Network: {network.get('network', {}).get('name')}\n"
                        by_interval = network.get('byInterval', [])
                        if by_interval:
                            recent = by_interval[0]
                            response += f"- Latest Utilization: {recent.get('utilization', {}).get('total', 0):.1f}%\n"
                
                return response
                
            except Exception as e:
                return f"❌ Error getting channel utilization by network: {str(e)}"
        
        
    @app.tool(
            name="get_organization_wireless_devices_power_mode_history",
            description="📡⚡ Get power mode history for wireless devices"
        )
        def get_organization_wireless_devices_power_mode_history(
            organization_id: str,
            network_ids: Optional[str] = None,
            serials: Optional[str] = None,
            t0: Optional[str] = None,
            t1: Optional[str] = None,
            timespan: Optional[float] = 86400
        ):
            """Get power mode history for wireless devices."""
            try:
                kwargs = {}
                if network_ids:
                    kwargs['networkIds'] = json.loads(network_ids) if isinstance(network_ids, str) else network_ids
                if serials:
                    kwargs['serials'] = json.loads(serials) if isinstance(serials, str) else serials
                if t0:
                    kwargs['t0'] = t0
                if t1:
                    kwargs['t1'] = t1
                if timespan:
                    kwargs['timespan'] = timespan
                
                result = meraki_client.dashboard.wireless.getOrganizationWirelessDevicesPowerModeHistory(
                    organization_id, **kwargs
                )
                
                response = f"# ⚡ Power Mode History\n\n"
                response += f"**Timespan**: {timespan/3600:.1f} hours\n\n"
                
                if isinstance(result, list):
                    response += f"**Total Devices**: {len(result)}\n"
                    for device in result[:5]:
                        response += f"\n## Device: {device.get('serial')}\n"
                        response += f"- Network: {device.get('network', {}).get('name')}\n"
                        response += f"- Power Mode: {device.get('powerMode')}\n"
                
                return response
                
            except Exception as e:
                return f"❌ Error getting power mode history: {str(e)}"
        
        
    @app.tool(
            name="get_org_wireless_radsec_authorities",
            description="📡🔒 Get RADSEC certificate authorities"
        )
        def get_organization_wireless_devices_radsec_certificates_authorities(
            organization_id: str
        ):
            """Get RADSEC certificate authorities."""
            try:
                result = meraki_client.dashboard.wireless.getOrganizationWirelessDevicesRadsecCertificatesAuthorities(
                    organization_id
                )
                
                response = f"# 🔒 RADSEC Certificate Authorities\n\n"
                if isinstance(result, list):
                    response += f"**Total CAs**: {len(result)}\n\n"
                    for ca in result:
                        response += f"## CA: {ca.get('name')}\n"
                        response += f"- ID: {ca.get('certificateId')}\n"
                        response += f"- Root: {ca.get('root', False)}\n\n"
                
                return response
                
            except Exception as e:
                return f"❌ Error getting RADSEC CAs: {str(e)}"
        
        
    @app.tool(
            name="create_org_wireless_radsec_authority",
            description="📡🔒 Create a RADSEC certificate authority"
        )
        def create_organization_wireless_devices_radsec_certificates_authority(
            organization_id: str,
            name: str,
            contents: str,
            root: Optional[bool] = False
        ):
            """Create RADSEC certificate authority."""
            try:
                result = meraki_client.dashboard.wireless.createOrganizationWirelessDevicesRadsecCertificatesAuthority(
                    organization_id,
                    name=name,
                    contents=contents,
                    root=root
                )
                
                return f"✅ Created RADSEC CA '{result.get('name')}' - ID: {result.get('certificateId')}"
                
            except Exception as e:
                return f"❌ Error creating RADSEC CA: {str(e)}"
        
        
    @app.tool(
            name="update_org_wireless_radsec_authorities",
            description="📡🔒 Update RADSEC certificate authorities"
        )
        def update_organization_wireless_devices_radsec_certificates_authorities(
            organization_id: str,
            certificate_ids: str
        ):
            """Update RADSEC certificate authorities."""
            try:
                ids = json.loads(certificate_ids) if isinstance(certificate_ids, str) else certificate_ids
                
                result = meraki_client.dashboard.wireless.updateOrganizationWirelessDevicesRadsecCertificatesAuthorities(
                    organization_id,
                    certificateIds=ids
                )
                
                return f"✅ Updated RADSEC certificate authorities"
                
            except Exception as e:
                return f"❌ Error updating RADSEC CAs: {str(e)}"
        
        
    @app.tool(
            name="get_org_wireless_radsec_crls",
            description="📡🔒 Get RADSEC certificate revocation lists"
        )
        def get_organization_wireless_devices_radsec_certificates_authorities_crls(
            organization_id: str
        ):
            """Get RADSEC CRLs."""
            try:
                result = meraki_client.dashboard.wireless.getOrganizationWirelessDevicesRadsecCertificatesAuthoritiesCrls(
                    organization_id
                )
                
                response = f"# 🔒 RADSEC Certificate Revocation Lists\n\n"
                if isinstance(result, list):
                    response += f"**Total CRLs**: {len(result)}\n"
                    for crl in result:
                        response += f"- CRL ID: {crl.get('id')}\n"
                
                return response
                
            except Exception as e:
                return f"❌ Error getting RADSEC CRLs: {str(e)}"
        
        
    @app.tool(
            name="get_org_wireless_radsec_crl_deltas",
            description="📡🔒 Get RADSEC CRL deltas"
        )
        def get_organization_wireless_devices_radsec_certificates_authorities_crls_deltas(
            organization_id: str
        ):
            """Get RADSEC CRL deltas."""
            try:
                result = meraki_client.dashboard.wireless.getOrganizationWirelessDevicesRadsecCertificatesAuthoritiesCrlsDeltas(
                    organization_id
                )
                
                response = f"# 🔒 RADSEC CRL Deltas\n\n"
                if isinstance(result, list):
                    response += f"**Total Deltas**: {len(result)}\n"
                
                return response
                
            except Exception as e:
                return f"❌ Error getting RADSEC CRL deltas: {str(e)}"
        
        
    @app.tool(
            name="get_organization_wireless_devices_system_cpu_load_history",
            description="📡💻 Get CPU load history for wireless devices"
        )
        def get_organization_wireless_devices_system_cpu_load_history(
            organization_id: str,
            network_ids: Optional[str] = None,
            serials: Optional[str] = None,
            t0: Optional[str] = None,
            t1: Optional[str] = None,
            timespan: Optional[float] = 86400
        ):
            """Get CPU load history for wireless devices."""
            try:
                kwargs = {}
                if network_ids:
                    kwargs['networkIds'] = json.loads(network_ids) if isinstance(network_ids, str) else network_ids
                if serials:
                    kwargs['serials'] = json.loads(serials) if isinstance(serials, str) else serials
                if t0:
                    kwargs['t0'] = t0
                if t1:
                    kwargs['t1'] = t1
                if timespan:
                    kwargs['timespan'] = timespan
                
                result = meraki_client.dashboard.wireless.getOrganizationWirelessDevicesSystemCpuLoadHistory(
                    organization_id, **kwargs
                )
                
                response = f"# 💻 CPU Load History\n\n"
                response += f"**Timespan**: {timespan/3600:.1f} hours\n\n"
                
                if isinstance(result, list):
                    response += f"**Total Devices**: {len(result)}\n"
                    for device in result[:5]:
                        response += f"- {device.get('serial')}: {device.get('cpuPercentage', 0):.1f}% CPU\n"
                
                return response
                
            except Exception as e:
                return f"❌ Error getting CPU load history: {str(e)}"
        
        
    @app.tool(
            name="get_organization_wireless_devices_wireless_controllers_by_device",
            description="📡🎮 Get wireless controllers by device"
        )
        def get_organization_wireless_devices_wireless_controllers_by_device(
            organization_id: str,
            network_ids: Optional[str] = None,
            serials: Optional[str] = None,
            per_page: Optional[int] = 1000
        ):
            """Get wireless controllers by device."""
            try:
                kwargs = {'perPage': per_page}
                if network_ids:
                    kwargs['networkIds'] = json.loads(network_ids) if isinstance(network_ids, str) else network_ids
                if serials:
                    kwargs['serials'] = json.loads(serials) if isinstance(serials, str) else serials
                
                result = meraki_client.dashboard.wireless.getOrganizationWirelessDevicesWirelessControllersByDevice(
                    organization_id, **kwargs
                )
                
                response = f"# 🎮 Wireless Controllers by Device\n\n"
                if isinstance(result, list):
                    response += f"**Total Devices**: {len(result)}\n"
                    for device in result[:5]:
                        response += f"- {device.get('serial')}: {device.get('controller', {}).get('name', 'N/A')}\n"
                
                return response
                
            except Exception as e:
                return f"❌ Error getting wireless controllers: {str(e)}"
        
        
    @app.tool(
            name="recalculate_organization_wireless_radio_auto_rf_channels",
            description="📡📻 Recalculate auto RF channels for organization"
        )
        def recalculate_organization_wireless_radio_auto_rf_channels(
            organization_id: str,
            serials: str
        ):
            """Recalculate auto RF channels."""
            try:
                serial_list = json.loads(serials) if isinstance(serials, str) else serials
                
                result = meraki_client.dashboard.wireless.recalculateOrganizationWirelessRadioAutoRfChannels(
                    organization_id,
                    serials=serial_list
                )
                
                return f"✅ Recalculated auto RF channels for {len(serial_list)} devices"
                
            except Exception as e:
                return f"❌ Error recalculating RF channels: {str(e)}"
        
        
    @app.tool(
            name="get_organization_wireless_rf_profiles_assignments_by_device",
            description="📡📻 Get RF profile assignments by device"
        )
        def get_organization_wireless_rf_profiles_assignments_by_device(
            organization_id: str,
            per_page: Optional[int] = 1000,
            network_ids: Optional[str] = None,
            product_types: Optional[str] = None
        ):
            """Get RF profile assignments by device."""
            try:
                kwargs = {'perPage': per_page}
                if network_ids:
                    kwargs['networkIds'] = json.loads(network_ids) if isinstance(network_ids, str) else network_ids
                if product_types:
                    kwargs['productTypes'] = json.loads(product_types) if isinstance(product_types, str) else product_types
                
                result = meraki_client.dashboard.wireless.getOrganizationWirelessRfProfilesAssignmentsByDevice(
                    organization_id, **kwargs
                )
                
                response = f"# 📻 RF Profile Assignments\n\n"
                if isinstance(result, list):
                    response += f"**Total Devices**: {len(result)}\n"
                    
                    # Group by profile
                    profiles = {}
                    for device in result:
                        profile_name = device.get('rfProfile', {}).get('name', 'Default')
                        if profile_name not in profiles:
                            profiles[profile_name] = 0
                        profiles[profile_name] += 1
                    
                    response += f"\n## Profile Distribution\n"
                    for profile, count in profiles.items():
                        response += f"- {profile}: {count} devices\n"
                
                return response
                
            except Exception as e:
                return f"❌ Error getting RF profile assignments: {str(e)}"
        
        
    @app.tool(
            name="get_org_wireless_isolation_allowlist",
            description="📡🔥 Get SSID firewall isolation allowlist entries"
        )
        def get_organization_wireless_ssids_firewall_isolation_allowlist_entries(
            organization_id: str,
            per_page: Optional[int] = 1000
        ):
            """Get SSID firewall isolation allowlist entries."""
            try:
                result = meraki_client.dashboard.wireless.getOrganizationWirelessSsidsFirewallIsolationAllowlistEntries(
                    organization_id,
                    perPage=per_page
                )
                
                response = f"# 🔥 SSID Firewall Isolation Allowlist\n\n"
                if isinstance(result, list):
                    response += f"**Total Entries**: {len(result)}\n\n"
                    for entry in result[:10]:
                        response += f"- **{entry.get('mac')}**: {entry.get('comment', 'No comment')}\n"
                
                return response
                
            except Exception as e:
                return f"❌ Error getting isolation allowlist: {str(e)}"
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
    
    # ==================== DEVICE TYPE GROUP POLICIES ====================
    
    def register_device_type_policies_tools():
        """Register additional device type group policy tools."""
        
        
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
    
    # ==================== LOCATION SCANNING RECEIVERS ====================
    
    def register_location_receivers_tools():
        """Register location scanning receiver tools."""
        
        
    @app.tool(
            name="get_organization_wireless_location_scanning_receivers",
            description="📡📍 Get location scanning receivers for organization"
        )
        def get_organization_wireless_location_scanning_receivers(
            organization_id: str
        ):
            """Get organization location scanning receivers."""
            try:
                result = meraki_client.dashboard.wireless.getOrganizationWirelessLocationScanningReceivers(
                    organization_id
                )
                
                response = f"# 📍 Location Scanning Receivers\n\n"
                
                receivers = result
                if receivers:
                    response += f"**Total Receivers**: {len(receivers)}\n\n"
                    for receiver in receivers:
                        response += f"## Receiver: {receiver.get('name')}\n"
                        response += f"- **ID**: {receiver.get('receiverId')}\n"
                        response += f"- **URL**: {receiver.get('url')}\n"
                        response += f"- **Networks**: {len(receiver.get('networks', []))}\n"
                else:
                    response += "No location scanning receivers configured\n"
                
                return response
                
            except Exception as e:
                return f"❌ Error getting location receivers: {str(e)}"
        
        
    @app.tool(
            name="create_organization_wireless_location_scanning_receiver",
            description="📡📍 Create a location scanning receiver for organization"
        )
        def create_organization_wireless_location_scanning_receiver(
            organization_id: str,
            name: str,
            url: str,
            secret: str,
            networks: Optional[str] = None
        ):
            """Create organization location scanning receiver."""
            try:
                kwargs = {
                    'name': name,
                    'url': url,
                    'secret': secret
                }
                
                if networks:
                    kwargs['networks'] = json.loads(networks) if isinstance(networks, str) else networks
                
                result = meraki_client.dashboard.wireless.createOrganizationWirelessLocationScanningReceiver(
                    organization_id, **kwargs
                )
                
                return f"✅ Created location receiver '{result.get('name')}' - ID: {result.get('receiverId')}"
                
            except Exception as e:
                return f"❌ Error creating location receiver: {str(e)}"
        
        
    @app.tool(
            name="update_organization_wireless_location_scanning_receiver",
            description="📡📍 Update a location scanning receiver for organization"
        )
        def update_organization_wireless_location_scanning_receiver(
            organization_id: str,
            receiver_id: str,
            name: Optional[str] = None,
            url: Optional[str] = None,
            secret: Optional[str] = None,
            networks: Optional[str] = None
        ):
            """Update organization location scanning receiver."""
            try:
                kwargs = {}
                
                if name:
                    kwargs['name'] = name
                if url:
                    kwargs['url'] = url
                if secret:
                    kwargs['secret'] = secret
                if networks:
                    kwargs['networks'] = json.loads(networks) if isinstance(networks, str) else networks
                
                result = meraki_client.dashboard.wireless.updateOrganizationWirelessLocationScanningReceiver(
                    organization_id, receiver_id, **kwargs
                )
                
                return f"✅ Updated location receiver {receiver_id}"
                
            except Exception as e:
                return f"❌ Error updating location receiver: {str(e)}"
        
        
    @app.tool(
            name="delete_organization_wireless_location_scanning_receiver",
            description="📡📍 Delete a location scanning receiver from organization"
        )
        def delete_organization_wireless_location_scanning_receiver(
            organization_id: str,
            receiver_id: str
        ):
            """Delete organization location scanning receiver."""
            try:
                meraki_client.dashboard.wireless.deleteOrganizationWirelessLocationScanningReceiver(
                    organization_id, receiver_id
                )
                
                return f"✅ Deleted location receiver {receiver_id}"
                
            except Exception as e:
                return f"❌ Error deleting location receiver: {str(e)}"
        
        
    @app.tool(
            name="get_organization_wireless_location_scanning_by_network",
            description="📡📍 Get location scanning settings by network for organization"
        )
        def get_organization_wireless_location_scanning_by_network(
            organization_id: str,
            per_page: Optional[int] = 1000
        ):
            """Get organization location scanning settings by network."""
            try:
                result = meraki_client.dashboard.wireless.getOrganizationWirelessLocationScanningByNetwork(
                    organization_id,
                    perPage=per_page
                )
                
                response = f"# 📍 Location Scanning by Network\n\n"
                
                networks = result
                if networks:
                    response += f"**Total Networks**: {len(networks)}\n\n"
                    for network in networks[:10]:  # Show first 10
                        response += f"- **{network.get('name')}**\n"
                        response += f"  - Analytics: {network.get('analyticsEnabled')}\n"
                        response += f"  - Scanning API: {network.get('scanningApiEnabled')}\n"
                else:
                    response += "No network location scanning configured\n"
                
                return response
                
            except Exception as e:
                return f"❌ Error getting location scanning by network: {str(e)}"
    
    # ==================== AIR MARSHAL SETTINGS BY NETWORK ====================
    
    def register_air_marshal_settings_tools():
        """Register Air Marshal settings by network tools."""
        
        
    @app.tool(
            name="get_organization_wireless_air_marshal_settings_by_network",
            description="📡🛡️ Get Air Marshal settings by network for organization"
        )
        def get_organization_wireless_air_marshal_settings_by_network(
            organization_id: str,
            network_ids: Optional[str] = None,
            per_page: Optional[int] = 1000
        ):
            """Get organization Air Marshal settings by network."""
            try:
                kwargs = {'perPage': per_page}
                
                if network_ids:
                    kwargs['networkIds'] = json.loads(network_ids) if isinstance(network_ids, str) else network_ids
                
                result = meraki_client.dashboard.wireless.getOrganizationWirelessAirMarshalSettingsByNetwork(
                    organization_id, **kwargs
                )
                
                response = f"# 🛡️ Air Marshal Settings by Network\n\n"
                
                items = result.get('items', [])
                if items:
                    response += f"**Total Networks**: {len(items)}\n\n"
                    for network in items[:10]:  # Show first 10
                        response += f"## Network: {network.get('network', {}).get('name')}\n"
                        response += f"- **Default Policy**: {network.get('defaultPolicy')}\n"
                        response += f"- **Whitelist**: {len(network.get('whitelist', []))} entries\n"
                        response += f"- **Rules**: {len(network.get('rules', []))} configured\n\n"
                else:
                    response += "No Air Marshal settings configured\n"
                
                return response
                
            except Exception as e:
                return f"❌ Error getting Air Marshal settings by network: {str(e)}"
    
    # ==================== ORGANIZATION PACKET LOSS ====================
    
    def register_organization_packet_loss_tools():
        """Register organization packet loss analysis tools."""
        
        
    @app.tool(
            name="get_organization_wireless_devices_packet_loss_by_client",
            description="📡📉 Get packet loss by client for organization wireless devices"
        )
        def get_organization_wireless_devices_packet_loss_by_client(
            organization_id: str,
            network_ids: Optional[str] = None,
            ssids: Optional[str] = None,
            bands: Optional[str] = None,
            per_page: Optional[int] = 1000,
            timespan: Optional[int] = 86400
        ):
            """Get organization wireless packet loss by client."""
            try:
                kwargs = {'perPage': per_page}
                
                if network_ids:
                    kwargs['networkIds'] = json.loads(network_ids) if isinstance(network_ids, str) else network_ids
                if ssids:
                    kwargs['ssids'] = json.loads(ssids) if isinstance(ssids, str) else ssids
                if bands:
                    kwargs['bands'] = json.loads(bands) if isinstance(bands, str) else bands
                if timespan:
                    kwargs['timespan'] = timespan
                
                result = meraki_client.dashboard.wireless.getOrganizationWirelessDevicesPacketLossByClient(
                    organization_id, **kwargs
                )
                
                response = f"# 📉 Packet Loss by Client\n\n"
                response += f"**Timespan**: {timespan/3600:.1f} hours\n\n"
                
                clients = result
                if clients:
                    response += f"**Total Clients**: {len(clients)}\n\n"
                    
                    # Show top 10 clients with highest packet loss
                    sorted_clients = sorted(clients, key=lambda x: x.get('lossPercentage', 0), reverse=True)
                    response += "## Top 10 Clients with Packet Loss\n"
                    for client in sorted_clients[:10]:
                        response += f"- **{client.get('mac')}**\n"
                        response += f"  - Loss: {client.get('lossPercentage', 0):.1f}%\n"
                        response += f"  - Network: {client.get('network', {}).get('name')}\n"
                        response += f"  - Device: {client.get('device', {}).get('name')}\n"
                else:
                    response += "No packet loss data available\n"
                
                return response
                
            except Exception as e:
                return f"❌ Error getting packet loss by client: {str(e)}"
        
        
    @app.tool(
            name="get_organization_wireless_devices_packet_loss_by_device",
            description="📡📉 Get packet loss by device for organization wireless"
        )
        def get_organization_wireless_devices_packet_loss_by_device(
            organization_id: str,
            network_ids: Optional[str] = None,
            serials: Optional[str] = None,
            bands: Optional[str] = None,
            ssids: Optional[str] = None,
            per_page: Optional[int] = 1000,
            timespan: Optional[int] = 86400
        ):
            """Get organization wireless packet loss by device."""
            try:
                kwargs = {'perPage': per_page}
                
                if network_ids:
                    kwargs['networkIds'] = json.loads(network_ids) if isinstance(network_ids, str) else network_ids
                if serials:
                    kwargs['serials'] = json.loads(serials) if isinstance(serials, str) else serials
                if bands:
                    kwargs['bands'] = json.loads(bands) if isinstance(bands, str) else bands
                if ssids:
                    kwargs['ssids'] = json.loads(ssids) if isinstance(ssids, str) else ssids
                if timespan:
                    kwargs['timespan'] = timespan
                
                result = meraki_client.dashboard.wireless.getOrganizationWirelessDevicesPacketLossByDevice(
                    organization_id, **kwargs
                )
                
                response = f"# 📉 Packet Loss by Device\n\n"
                response += f"**Timespan**: {timespan/3600:.1f} hours\n\n"
                
                devices = result
                if devices:
                    response += f"**Total Devices**: {len(devices)}\n\n"
                    
                    # Sort devices by downstream packet loss
                    sorted_devices = sorted(devices, 
                        key=lambda x: x.get('downstream', {}).get('lossPercentage', 0), 
                        reverse=True)
                    
                    response += "## Devices with Packet Loss\n"
                    for device_data in sorted_devices[:10]:
                        device_info = device_data.get('device', {})
                        network_info = device_data.get('network', {})
                        downstream = device_data.get('downstream', {})
                        upstream = device_data.get('upstream', {})
                        
                        response += f"- **{device_info.get('name', 'Unknown')}** ({device_info.get('serial', 'N/A')})\n"
                        response += f"  - Network: {network_info.get('name', 'Unknown')}\n"
                        
                        # Downstream stats
                        if downstream:
                            response += f"  - Downstream Loss: {downstream.get('lossPercentage', 0):.1f}% "
                            response += f"({downstream.get('lost', 0):,}/{downstream.get('total', 0):,})\n"
                        
                        # Upstream stats  
                        if upstream:
                            response += f"  - Upstream Loss: {upstream.get('lossPercentage', 0):.1f}% "
                            response += f"({upstream.get('lost', 0):,}/{upstream.get('total', 0):,})\n"
                        
                        response += "\n"
                else:
                    response += "No packet loss data available\n"
                
                return response
                
            except Exception as e:
                return f"❌ Error getting packet loss by device: {str(e)}"
        
        
    @app.tool(
            name="get_organization_wireless_devices_packet_loss_by_network",
            description="📡📉 Get packet loss by network for organization wireless"
        )
        def get_organization_wireless_devices_packet_loss_by_network(
            organization_id: str,
            network_ids: Optional[str] = None,
            serials: Optional[str] = None,
            bands: Optional[str] = None,
            ssids: Optional[str] = None,
            per_page: Optional[int] = 1000,
            timespan: Optional[int] = 86400
        ):
            """Get organization wireless packet loss by network."""
            try:
                kwargs = {'perPage': per_page}
                
                if network_ids:
                    kwargs['networkIds'] = json.loads(network_ids) if isinstance(network_ids, str) else network_ids
                if serials:
                    kwargs['serials'] = json.loads(serials) if isinstance(serials, str) else serials
                if bands:
                    kwargs['bands'] = json.loads(bands) if isinstance(bands, str) else bands
                if ssids:
                    kwargs['ssids'] = json.loads(ssids) if isinstance(ssids, str) else ssids
                if timespan:
                    kwargs['timespan'] = timespan
                
                result = meraki_client.dashboard.wireless.getOrganizationWirelessDevicesPacketLossByNetwork(
                    organization_id, **kwargs
                )
                
                response = f"# 📉 Packet Loss by Network\n\n"
                response += f"**Timespan**: {timespan/3600:.1f} hours\n\n"
                
                networks = result
                if networks:
                    response += f"**Total Networks**: {len(networks)}\n\n"
                    
                    # Show networks with packet loss data
                    response += "## Packet Loss by Network\n"
                    for network_data in networks:
                        network_info = network_data.get('network', {})
                        downstream = network_data.get('downstream', {})
                        upstream = network_data.get('upstream', {})
                        
                        response += f"- **{network_info.get('name', 'Unknown')}**\n"
                        response += f"  - Network ID: {network_info.get('id', 'N/A')}\n"
                        
                        # Downstream stats
                        if downstream:
                            response += f"  - Downstream Loss: {downstream.get('lossPercentage', 0):.1f}% "
                            response += f"({downstream.get('lost', 0):,}/{downstream.get('total', 0):,} packets)\n"
                        
                        # Upstream stats
                        if upstream:
                            response += f"  - Upstream Loss: {upstream.get('lossPercentage', 0):.1f}% "
                            response += f"({upstream.get('lost', 0):,}/{upstream.get('total', 0):,} packets)\n"
                        
                        response += "\n"
                else:
                    response += "No packet loss data available\n"
                
                return response
                
            except Exception as e:
                return f"❌ Error getting packet loss by network: {str(e)}"
    
    # ==================== ORGANIZATION OVERVIEW ====================
    
    def register_organization_overview_tools():
        """Register organization wireless overview tools."""
        
        
    @app.tool(
            name="get_organization_wireless_clients_overview_by_device",
            description="📡👥 Get wireless clients overview by device for organization"
        )
        def get_organization_wireless_clients_overview_by_device(
            organization_id: str,
            network_ids: Optional[str] = None,
            serials: Optional[str] = None,
            per_page: Optional[int] = 1000,
            timespan: Optional[int] = 86400
        ):
            """Get organization wireless clients overview by device."""
            try:
                kwargs = {'perPage': per_page}
                
                if network_ids:
                    kwargs['networkIds'] = json.loads(network_ids) if isinstance(network_ids, str) else network_ids
                if serials:
                    kwargs['serials'] = json.loads(serials) if isinstance(serials, str) else serials
                if timespan:
                    kwargs['timespan'] = timespan
                
                result = meraki_client.dashboard.wireless.getOrganizationWirelessClientsOverviewByDevice(
                    organization_id, **kwargs
                )
                
                response = f"# 👥 Wireless Clients Overview by Device\n\n"
                response += f"**Timespan**: {timespan/3600:.1f} hours\n\n"
                
                items = result.get('items', [])
                if items:
                    response += f"**Total Devices**: {len(items)}\n\n"
                    
                    # Sort by client count
                    sorted_devices = sorted(items, key=lambda x: x.get('usage', {}).get('clientCount', 0), reverse=True)
                    response += "## Top Devices by Client Count\n"
                    for device in sorted_devices[:10]:
                        response += f"- **{device.get('device', {}).get('name')}**\n"
                        response += f"  - Serial: {device.get('device', {}).get('serial')}\n"
                        response += f"  - Clients: {device.get('usage', {}).get('clientCount', 0)}\n"
                        response += f"  - Usage: {device.get('usage', {}).get('totalMbps', 0):.1f} Mbps\n"
                        response += f"  - Network: {device.get('network', {}).get('name')}\n"
                else:
                    response += "No client overview data available\n"
                
                return response
                
            except Exception as e:
                return f"❌ Error getting clients overview by device: {str(e)}"
        
        
    @app.tool(
            name="get_organization_wireless_ssids_statuses_by_device",
            description="📡📶 Get SSID statuses by device for organization"
        )
        def get_organization_wireless_ssids_statuses_by_device(
            organization_id: str,
            network_ids: Optional[str] = None,
            serials: Optional[str] = None,
            bssids: Optional[str] = None,
            per_page: Optional[int] = 500  # API limit: must be between 3 and 500
        ):
            """Get organization SSID statuses by device."""
            try:
                kwargs = {'perPage': per_page}
                
                if network_ids:
                    kwargs['networkIds'] = json.loads(network_ids) if isinstance(network_ids, str) else network_ids
                if serials:
                    kwargs['serials'] = json.loads(serials) if isinstance(serials, str) else serials
                if bssids:
                    kwargs['bssids'] = json.loads(bssids) if isinstance(bssids, str) else bssids
                
                result = meraki_client.dashboard.wireless.getOrganizationWirelessSsidsStatusesByDevice(
                    organization_id, **kwargs
                )
                
                response = f"# 📶 SSID Statuses by Device\n\n"
                
                items = result.get('items', [])
                if items:
                    response += f"**Total Device SSIDs**: {len(items)}\n\n"
                    
                    # Group by device
                    devices = {}
                    for item in items:
                        device_name = item.get('device', {}).get('name', 'Unknown')
                        if device_name not in devices:
                            devices[device_name] = []
                        devices[device_name].append(item)
                    
                    response += f"## Devices ({len(devices)})\n"
                    for device_name, ssids in list(devices.items())[:5]:  # Show first 5 devices
                        response += f"\n### {device_name}\n"
                        for ssid in ssids[:3]:  # Show first 3 SSIDs per device
                            response += f"- **{ssid.get('ssid', {}).get('name')}**\n"
                            response += f"  - Enabled: {ssid.get('basicServiceSet', {}).get('enabled')}\n"
                            response += f"  - Visible: {ssid.get('basicServiceSet', {}).get('visible')}\n"
                            response += f"  - Band: {ssid.get('basicServiceSet', {}).get('band')}\n"
                            response += f"  - Channel: {ssid.get('basicServiceSet', {}).get('channel')}\n"
                else:
                    response += "No SSID status data available\n"
                
                return response
                
            except Exception as e:
                return f"❌ Error getting SSID statuses by device: {str(e)}"
        
        
    @app.tool(
            name="get_organization_wireless_devices_channel_utilization_by_device",
            description="📡📊 Get channel utilization by device for organization"
        )
        def get_organization_wireless_devices_channel_utilization_by_device(
            organization_id: str,
            network_ids: Optional[str] = None,
            serials: Optional[str] = None,
            per_page: Optional[int] = 1000,
            timespan: Optional[int] = 86400
        ):
            """Get organization wireless channel utilization by device."""
            try:
                kwargs = {'perPage': per_page}
                
                if network_ids:
                    kwargs['networkIds'] = json.loads(network_ids) if isinstance(network_ids, str) else network_ids
                if serials:
                    kwargs['serials'] = json.loads(serials) if isinstance(serials, str) else serials
                if timespan:
                    kwargs['timespan'] = timespan
                
                result = meraki_client.dashboard.wireless.getOrganizationWirelessDevicesChannelUtilizationByDevice(
                    organization_id, **kwargs
                )
                
                response = f"# 📊 Channel Utilization by Device\n\n"
                response += f"**Timespan**: {timespan/3600:.1f} hours\n\n"
                
                devices = result
                if devices:
                    response += f"**Total Devices**: {len(devices)}\n\n"
                    
                    # Sort by total utilization
                    sorted_devices = sorted(devices, 
                        key=lambda x: x.get('byBand', [{}])[0].get('utilization', {}).get('total', 0) if x.get('byBand') else 0, 
                        reverse=True)
                    
                    response += "## Devices with Highest Channel Utilization\n"
                    for device in sorted_devices[:10]:
                        response += f"- **{device.get('device', {}).get('name')}** ({device.get('device', {}).get('serial')})\n"
                        response += f"  - Network: {device.get('network', {}).get('name')}\n"
                        
                        by_band = device.get('byBand', [])
                        for band_data in by_band:
                            band = band_data.get('band')
                            util = band_data.get('utilization', {})
                            response += f"  - **{band} Band**:\n"
                            response += f"    - Total: {util.get('total', 0):.1f}%\n"
                            response += f"    - WiFi: {util.get('wifi', 0):.1f}%\n"
                            response += f"    - Non-WiFi: {util.get('nonWifi', 0):.1f}%\n"
                else:
                    response += "No channel utilization data available\n"
                
                return response
                
            except Exception as e:
                return f"❌ Error getting channel utilization by device: {str(e)}"
        
        
    @app.tool(
            name="get_organization_wireless_devices_channel_utilization_by_network",
            description="📡📊 Get channel utilization by network for organization"
        )
        def get_organization_wireless_devices_channel_utilization_by_network(
            organization_id: str,
            network_ids: Optional[str] = None,
            serials: Optional[str] = None,
            per_page: Optional[int] = 1000,
            timespan: Optional[int] = 86400
        ):
            """Get organization wireless channel utilization by network."""
            try:
                kwargs = {'perPage': per_page}
                
                if network_ids:
                    kwargs['networkIds'] = json.loads(network_ids) if isinstance(network_ids, str) else network_ids
                if serials:
                    kwargs['serials'] = json.loads(serials) if isinstance(serials, str) else serials
                if timespan:
                    kwargs['timespan'] = timespan
                
                result = meraki_client.dashboard.wireless.getOrganizationWirelessDevicesChannelUtilizationByNetwork(
                    organization_id, **kwargs
                )
                
                response = f"# 📊 Channel Utilization by Network\n\n"
                response += f"**Timespan**: {timespan/3600:.1f} hours\n\n"
                
                networks = result
                if networks:
                    response += f"**Total Networks**: {len(networks)}\n\n"
                    
                    # Sort by average utilization
                    sorted_networks = sorted(networks, 
                        key=lambda x: x.get('byBand', [{}])[0].get('utilization', {}).get('total', 0) if x.get('byBand') else 0,
                        reverse=True)
                    
                    response += "## Networks with Highest Channel Utilization\n"
                    for network in sorted_networks:
                        response += f"- **{network.get('network', {}).get('name')}**\n"
                        
                        by_band = network.get('byBand', [])
                        for band_data in by_band:
                            band = band_data.get('band')
                            util = band_data.get('utilization', {})
                            response += f"  - **{band} Band**:\n"
                            response += f"    - Total: {util.get('total', 0):.1f}%\n"
                            response += f"    - WiFi: {util.get('wifi', 0):.1f}%\n"
                            response += f"    - Non-WiFi: {util.get('nonWifi', 0):.1f}%\n"
                else:
                    response += "No channel utilization data available\n"
                
                return response
                
            except Exception as e:
                return f"❌ Error getting channel utilization by network: {str(e)}"
    @app.tool(
            name="get_network_wireless_rf_profile",
            description="📡📻 Get details of a specific RF profile"
        )
        def get_network_wireless_rf_profile(
            network_id: str,
            rf_profile_id: str
        ):
            """Get details of a specific RF profile."""
            try:
                result = meraki_client.dashboard.wireless.getNetworkWirelessRfProfile(
                    network_id, rf_profile_id
                )
                
                response = f"# 📻 RF Profile Details\n\n"
                response += f"**Name**: {result.get('name', 'Unknown')}\n"
                response += f"**ID**: {result.get('id', 'Unknown')}\n"
                response += f"**Client Balancing**: {'Enabled ✅' if result.get('clientBalancingEnabled') else 'Disabled ❌'}\n\n"
                
                # Band selection
                band_selection = result.get('bandSelectionType', 'ap')
                response += f"**Band Selection**: {band_selection}\n"
                
                # AP Band Settings
                ap_band = result.get('apBandSettings', {})
                if ap_band:
                    response += "\n## AP Band Settings:\n"
                    response += f"- **Mode**: {ap_band.get('mode', 'Unknown')}\n"
                    if ap_band.get('bands', {}).get('enabled'):
                        response += f"- **Enabled Bands**: {', '.join(ap_band['bands']['enabled'])}\n"
                
                # Two-four GHz settings
                two_four = result.get('twoFourGhzSettings', {})
                if two_four:
                    response += "\n## 2.4 GHz Settings:\n"
                    response += f"- **Max Power**: {two_four.get('maxPower', 'Auto')} dBm\n"
                    response += f"- **Min Power**: {two_four.get('minPower', 'Auto')} dBm\n"
                    response += f"- **Min Bitrate**: {two_four.get('minBitrate', 'Auto')} Mbps\n"
                    response += f"- **Valid Channels**: {two_four.get('validAutoChannels', [])}\n"
                    response += f"- **Ax Enabled**: {two_four.get('axEnabled', False)}\n"
                    response += f"- **RX-SOP**: {two_four.get('rxsop', 'Auto')}\n"
                
                # Five GHz settings
                five = result.get('fiveGhzSettings', {})
                if five:
                    response += "\n## 5 GHz Settings:\n"
                    response += f"- **Max Power**: {five.get('maxPower', 'Auto')} dBm\n"
                    response += f"- **Min Power**: {five.get('minPower', 'Auto')} dBm\n"
                    response += f"- **Min Bitrate**: {five.get('minBitrate', 'Auto')} Mbps\n"
                    response += f"- **Valid Channels**: {five.get('validAutoChannels', [])}\n"
                    response += f"- **Channel Width**: {five.get('channelWidth', 'Auto')}\n"
                    response += f"- **RX-SOP**: {five.get('rxsop', 'Auto')}\n"
                
                # Six GHz settings
                six = result.get('sixGhzSettings', {})
                if six:
                    response += "\n## 6 GHz Settings:\n"
                    response += f"- **Max Power**: {six.get('maxPower', 'Auto')} dBm\n"
                    response += f"- **Min Power**: {six.get('minPower', 'Auto')} dBm\n"
                    response += f"- **Min Bitrate**: {six.get('minBitrate', 'Auto')} Mbps\n"
                    response += f"- **Valid Channels**: {six.get('validAutoChannels', [])}\n"
                    response += f"- **Channel Width**: {six.get('channelWidth', 'Auto')}\n"
                
                # Transmission settings
                transmission = result.get('transmission', {})
                if transmission:
                    response += "\n## Transmission Settings:\n"
                    response += f"- **Enabled**: {transmission.get('enabled', False)}\n"
                
                return response
            except Exception as e:
                return f"❌ Error: {str(e)}"
        
        
    @app.tool(
            name="create_network_wireless_rf_profile",
            description="📡📻 Create a new RF profile"
        )
        def create_network_wireless_rf_profile(
            network_id: str,
            name: str,
            band_selection_type: Optional[str] = 'ap',
            client_balancing_enabled: Optional[bool] = None,
            min_bitrate_2_4: Optional[float] = None,
            min_bitrate_5: Optional[float] = None
        ):
            """Create a new RF profile."""
            try:
                kwargs = {
                    'name': name,
                    'bandSelectionType': band_selection_type
                }
                
                if client_balancing_enabled is not None:
                    kwargs['clientBalancingEnabled'] = client_balancing_enabled
                
                # 2.4 GHz settings
                if min_bitrate_2_4 is not None:
                    kwargs['twoFourGhzSettings'] = {'minBitrate': min_bitrate_2_4}
                
                # 5 GHz settings
                if min_bitrate_5 is not None:
                    kwargs['fiveGhzSettings'] = {'minBitrate': min_bitrate_5}
                
                result = meraki_client.dashboard.wireless.createNetworkWirelessRfProfile(
                    network_id, **kwargs
                )
                
                response = f"# ✅ Created RF Profile\n\n"
                response += f"**Name**: {result.get('name', 'Unknown')}\n"
                response += f"**ID**: {result.get('id', 'Unknown')}\n"
                response += f"**Band Selection**: {result.get('bandSelectionType', 'Unknown')}\n"
                
                return response
            except Exception as e:
                return f"❌ Error: {str(e)}"
        
        
    @app.tool(
            name="update_network_wireless_rf_profile",
            description="📡📻 Update an existing RF profile"
        )
        def update_network_wireless_rf_profile(
            network_id: str,
            rf_profile_id: str,
            name: Optional[str] = None,
            client_balancing_enabled: Optional[bool] = None,
            min_bitrate_2_4: Optional[float] = None,
            min_bitrate_5: Optional[float] = None,
            max_power_2_4: Optional[int] = None,
            max_power_5: Optional[int] = None
        ):
            """Update an existing RF profile."""
            try:
                kwargs = {}
                
                if name:
                    kwargs['name'] = name
                
                if client_balancing_enabled is not None:
                    kwargs['clientBalancingEnabled'] = client_balancing_enabled
                
                # 2.4 GHz settings
                two_four_settings = {}
                if min_bitrate_2_4 is not None:
                    two_four_settings['minBitrate'] = min_bitrate_2_4
                if max_power_2_4 is not None:
                    two_four_settings['maxPower'] = max_power_2_4
                if two_four_settings:
                    kwargs['twoFourGhzSettings'] = two_four_settings
                
                # 5 GHz settings
                five_settings = {}
                if min_bitrate_5 is not None:
                    five_settings['minBitrate'] = min_bitrate_5
                if max_power_5 is not None:
                    five_settings['maxPower'] = max_power_5
                if five_settings:
                    kwargs['fiveGhzSettings'] = five_settings
                
                result = meraki_client.dashboard.wireless.updateNetworkWirelessRfProfile(
                    network_id, rf_profile_id, **kwargs
                )
                
                response = f"# ✅ Updated RF Profile\n\n"
                response += f"**Name**: {result.get('name', 'Unknown')}\n"
                response += f"**ID**: {rf_profile_id}\n"
                
                return response
            except Exception as e:
                return f"❌ Error: {str(e)}"
        
        
    @app.tool(
            name="delete_network_wireless_rf_profile",
            description="📡📻 Delete an RF profile"
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
                
                return f"# ✅ Deleted RF Profile\n\n**ID**: {rf_profile_id}"
            except Exception as e:
                return f"❌ Error: {str(e)}"
        
        
    @app.tool(
            name="get_organization_wireless_rf_profiles_assignments",
            description="📡📻 Get RF profile assignments by device"
        )
        def get_organization_wireless_rf_profiles_assignments(
            organization_id: str,
            include_templates: Optional[bool] = False,
            network_ids: Optional[str] = None,
            product_types: Optional[str] = None,
            per_page: Optional[int] = 1000
        ):
            """Get RF profile assignments by device."""
            try:
                kwargs = {
                    'includeTemplates': include_templates,
                    'perPage': per_page
                }
                if network_ids:
                    kwargs['networkIds'] = network_ids.split(',')
                if product_types:
                    kwargs['productTypes'] = product_types.split(',')
                
                result = meraki_client.dashboard.wireless.getOrganizationWirelessRfProfilesAssignmentsByDevice(
                    organization_id, **kwargs
                )
                
                response = f"# 📻 RF Profile Assignments\n\n"
                
                if isinstance(result, list):
                    response += f"**Total Devices**: {len(result)}\n\n"
                    
                    # Group by RF profile
                    profile_groups = {}
                    for device in result:
                        profile_id = device.get('rfProfile', {}).get('id', 'None')
                        profile_name = device.get('rfProfile', {}).get('name', 'Default')
                        
                        if profile_id not in profile_groups:
                            profile_groups[profile_id] = {
                                'name': profile_name,
                                'devices': []
                            }
                        profile_groups[profile_id]['devices'].append(device.get('serial'))
                    
                    response += "## Profile Distribution:\n"
                    for profile_id, data in profile_groups.items():
                        response += f"- **{data['name']}**: {len(data['devices'])} devices\n"
                        if len(data['devices']) <= 5:
                            for serial in data['devices']:
                                response += f"  - {serial}\n"
                
                return response
            except Exception as e:
                return f"❌ Error: {str(e)}"
    
    # ==================== AIR MARSHAL SECURITY ====================
    
    def register_air_marshal_tools():
        """Register Air Marshal security tools."""
        
        
    @app.tool(
            name="get_organization_wireless_air_marshal_rules",
            description="📡🚨 Get Air Marshal rules for organization"
        )
        def get_organization_wireless_air_marshal_rules(
            organization_id: str,
            network_ids: Optional[str] = None,
            per_page: Optional[int] = 1000
        ):
            """Get Air Marshal rules for organization."""
            try:
                kwargs = {'perPage': per_page}
                if network_ids:
                    kwargs['networkIds'] = network_ids.split(',')
                
                result = meraki_client.dashboard.wireless.getOrganizationWirelessAirMarshalRules(
                    organization_id, **kwargs
                )
                
                response = f"# 🚨 Air Marshal Rules\n\n"
                
                if isinstance(result, list):
                    response += f"**Total Rules**: {len(result)}\n\n"
                    
                    for i, rule in enumerate(result[:10], 1):  # Show first 10
                        response += f"## Rule {i}: {rule.get('ruleId', 'Unknown')}\n"
                        response += f"- **Type**: {rule.get('type', 'Unknown')}\n"
                        
                        match_rule = rule.get('match', {})
                        if match_rule:
                            response += f"- **Match String**: {match_rule.get('string', 'Any')}\n"
                            response += f"- **Match Type**: {match_rule.get('type', 'Any')}\n"
                        
                        # Networks
                        networks = rule.get('networks', [])
                        if networks:
                            response += f"- **Applied to**: {len(networks)} networks\n"
                        
                        response += "\n"
                
                return response
            except Exception as e:
                return f"❌ Error: {str(e)}"
        
        
    @app.tool(
            name="create_network_wireless_air_marshal_rule",
            description="📡🚨 Create a new Air Marshal rule"
        )
        def create_network_wireless_air_marshal_rule(
            network_id: str,
            type: str,
            match_string: str,
            match_type: str = 'contains'
        ):
            """Create a new Air Marshal rule."""
            try:
                result = meraki_client.dashboard.wireless.createNetworkWirelessAirMarshalRule(
                    network_id,
                    type=type,
                    match={
                        'string': match_string,
                        'type': match_type
                    }
                )
                
                response = f"# ✅ Created Air Marshal Rule\n\n"
                response += f"**Type**: {result.get('type', 'Unknown')}\n"
                response += f"**Rule ID**: {result.get('ruleId', 'Unknown')}\n"
                response += f"**Match**: {result.get('match', {}).get('string', 'Unknown')}\n"
                
                return response
            except Exception as e:
                return f"❌ Error: {str(e)}"
        
        
    @app.tool(
            name="update_network_wireless_air_marshal_rule",
            description="📡🚨 Update an Air Marshal rule"
        )
        def update_network_wireless_air_marshal_rule(
            network_id: str,
            rule_id: str,
            type: Optional[str] = None,
            match_string: Optional[str] = None,
            match_type: Optional[str] = None
        ):
            """Update an Air Marshal rule."""
            try:
                kwargs = {}
                if type:
                    kwargs['type'] = type
                if match_string or match_type:
                    kwargs['match'] = {}
                    if match_string:
                        kwargs['match']['string'] = match_string
                    if match_type:
                        kwargs['match']['type'] = match_type
                
                result = meraki_client.dashboard.wireless.updateNetworkWirelessAirMarshalRule(
                    network_id, rule_id, **kwargs
                )
                
                response = f"# ✅ Updated Air Marshal Rule\n\n"
                response += f"**Rule ID**: {rule_id}\n"
                response += f"**Type**: {result.get('type', 'Unknown')}\n"
                
                return response
            except Exception as e:
                return f"❌ Error: {str(e)}"
        
        
    @app.tool(
            name="delete_network_wireless_air_marshal_rule",
            description="📡🚨 Delete an Air Marshal rule"
        )
        def delete_network_wireless_air_marshal_rule(
            network_id: str,
            rule_id: str
        ):
            """Delete an Air Marshal rule."""
            try:
                meraki_client.dashboard.wireless.deleteNetworkWirelessAirMarshalRule(
                    network_id, rule_id
                )
                
                return f"# ✅ Deleted Air Marshal Rule\n\n**Rule ID**: {rule_id}"
            except Exception as e:
                return f"❌ Error: {str(e)}"
        
        
    @app.tool(
            name="update_network_wireless_air_marshal_settings",
            description="📡🚨 Update Air Marshal settings for network"
        )
        def update_network_wireless_air_marshal_settings(
            network_id: str,
            default_policy: str = 'allow'
        ):
            """Update Air Marshal settings for network."""
            try:
                result = meraki_client.dashboard.wireless.updateNetworkWirelessAirMarshalSettings(
                    network_id,
                    defaultPolicy=default_policy
                )
                
                response = f"# ✅ Updated Air Marshal Settings\n\n"
                response += f"**Default Policy**: {result.get('defaultPolicy', 'Unknown')}\n"
                
                return response
            except Exception as e:
                return f"❌ Error: {str(e)}"
        
        
    @app.tool(
            name="create_organization_wireless_air_marshal_rule",
            description="📡🚨 Create a new Air Marshal rule"
        )
        def create_organization_wireless_air_marshal_rule(
            organization_id: str,
            type: str,
            match_string: Optional[str] = None,
            match_type: Optional[str] = None,
            network_ids: Optional[str] = None
        ):
            """Create a new Air Marshal rule."""
            try:
                kwargs = {'type': type}
                
                if match_string or match_type:
                    kwargs['match'] = {}
                    if match_string:
                        kwargs['match']['string'] = match_string
                    if match_type:
                        kwargs['match']['type'] = match_type
                
                if network_ids:
                    kwargs['networkIds'] = json.loads(network_ids) if isinstance(network_ids, str) else network_ids
                
                result = meraki_client.dashboard.wireless.createOrganizationWirelessAirMarshalRule(
                    organization_id, **kwargs
                )
                
                response = f"# ✅ Created Air Marshal Rule\n\n"
                response += f"**Rule ID**: {result.get('ruleId', 'Unknown')}\n"
                response += f"**Type**: {result.get('type', 'Unknown')}\n"
                
                match_rule = result.get('match', {})
                if match_rule:
                    response += f"**Match String**: {match_rule.get('string', 'N/A')}\n"
                    response += f"**Match Type**: {match_rule.get('type', 'N/A')}\n"
                
                networks = result.get('networks', [])
                if networks:
                    response += f"\n**Applied to {len(networks)} networks**\n"
                
                return response
                
            except Exception as e:
                return f"❌ Error creating Air Marshal rule: {str(e)}"
        
        
    @app.tool(
            name="update_organization_wireless_air_marshal_rule",
            description="📡🚨 Update an existing Air Marshal rule"
        )
        def update_organization_wireless_air_marshal_rule(
            organization_id: str,
            rule_id: str,
            type: Optional[str] = None,
            match_string: Optional[str] = None,
            match_type: Optional[str] = None,
            network_ids: Optional[str] = None
        ):
            """Update an existing Air Marshal rule."""
            try:
                kwargs = {}
                
                if type:
                    kwargs['type'] = type
                
                if match_string or match_type:
                    kwargs['match'] = {}
                    if match_string:
                        kwargs['match']['string'] = match_string
                    if match_type:
                        kwargs['match']['type'] = match_type
                
                if network_ids:
                    kwargs['networkIds'] = json.loads(network_ids) if isinstance(network_ids, str) else network_ids
                
                result = meraki_client.dashboard.wireless.updateOrganizationWirelessAirMarshalRule(
                    organization_id, rule_id, **kwargs
                )
                
                response = f"# ✅ Updated Air Marshal Rule\n\n"
                response += f"**Rule ID**: {result.get('ruleId', 'Unknown')}\n"
                response += f"**Type**: {result.get('type', 'Unknown')}\n"
                
                match_rule = result.get('match', {})
                if match_rule:
                    response += f"**Match String**: {match_rule.get('string', 'N/A')}\n"
                    response += f"**Match Type**: {match_rule.get('type', 'N/A')}\n"
                
                return response
                
            except Exception as e:
                return f"❌ Error updating Air Marshal rule: {str(e)}"
        
        
    @app.tool(
            name="delete_organization_wireless_air_marshal_rule",
            description="📡🚨 Delete an Air Marshal rule"
        )
        def delete_organization_wireless_air_marshal_rule(
            organization_id: str,
            rule_id: str
        ):
            """Delete an Air Marshal rule."""
            try:
                meraki_client.dashboard.wireless.deleteOrganizationWirelessAirMarshalRule(
                    organization_id, rule_id
                )
                
                return f"✅ Successfully deleted Air Marshal rule {rule_id}"
                
            except Exception as e:
                return f"❌ Error deleting Air Marshal rule: {str(e)}"
        
        
    @app.tool(
            name="get_organization_wireless_air_marshal_settings_by_network",
            description="📡🚨 Get Air Marshal settings for all networks"
        )
        def get_organization_wireless_air_marshal_settings_by_network(
            organization_id: str,
            network_ids: Optional[str] = None,
            per_page: Optional[int] = 1000
        ):
            """Get Air Marshal settings for all networks."""
            try:
                kwargs = {'perPage': per_page}
                if network_ids:
                    kwargs['networkIds'] = network_ids.split(',')
                
                result = meraki_client.dashboard.wireless.getOrganizationWirelessAirMarshalSettingsByNetwork(
                    organization_id, **kwargs
                )
                
                response = f"# 🚨 Air Marshal Settings by Network\n\n"
                
                if isinstance(result, list):
                    response += f"**Total Networks**: {len(result)}\n\n"
                    
                    # Group by default policy
                    allow_networks = [n for n in result if n.get('defaultPolicy') == 'allow']
                    block_networks = [n for n in result if n.get('defaultPolicy') == 'block']
                    
                    response += f"## Policy Distribution:\n"
                    response += f"- **Allow by default**: {len(allow_networks)} networks\n"
                    response += f"- **Block by default**: {len(block_networks)} networks\n"
                    
                    if block_networks:
                        response += f"\n## Networks with Block Policy:\n"
                        for network in block_networks[:5]:
                            response += f"- {network.get('network', {}).get('name', 'Unknown')} ({network.get('networkId', 'Unknown')})\n"
                
                return response
            except Exception as e:
                return f"❌ Error: {str(e)}"
    
    # ==================== CLIENT CONNECTIVITY TOOLS ====================
    
    def register_client_connectivity_tools():
        """Register client connectivity analysis tools."""
        
        
    @app.tool(
            name="get_network_wireless_client_connectivity_events",
            description="📡📊 Get client connectivity events"
        )
        def get_network_wireless_client_connectivity_events(
            network_id: str,
            client_id: str,
            per_page: Optional[int] = 1000,
            starting_after: Optional[str] = None,
            ending_before: Optional[str] = None
        ):
            """Get client connectivity events."""
            try:
                kwargs = {'perPage': per_page}
                if starting_after:
                    kwargs['startingAfter'] = starting_after
                if ending_before:
                    kwargs['endingBefore'] = ending_before
                
                result = meraki_client.dashboard.wireless.getNetworkWirelessClientConnectivityEvents(
                    network_id, client_id, **kwargs
                )
                
                response = f"# 📊 Client Connectivity Events\n\n"
                response += f"**Client**: {client_id}\n\n"
                
                if isinstance(result, list):
                    response += f"**Total Events**: {len(result)}\n\n"
                    
                    # Group by event type
                    event_types = {}
                    for event in result:
                        event_type = event.get('type', 'Unknown')
                        if event_type not in event_types:
                            event_types[event_type] = 0
                        event_types[event_type] += 1
                    
                    response += "## Event Distribution:\n"
                    for event_type, count in event_types.items():
                        response += f"- **{event_type}**: {count} events\n"
                    
                    # Show recent events
                    response += "\n## Recent Events:\n"
                    for event in result[:5]:
                        response += f"- **{event.get('type', 'Unknown')}** at {event.get('occurredAt', 'Unknown')}\n"
                        response += f"  - SSID: {event.get('ssidNumber', 'Unknown')}\n"
                        response += f"  - AP: {event.get('deviceSerial', 'Unknown')}\n"
                        response += f"  - Band: {event.get('band', 'Unknown')}\n"
                        response += f"  - Channel: {event.get('channel', 'Unknown')}\n\n"
                
                return response
            except Exception as e:
                return f"❌ Error: {str(e)}"
        
        
    @app.tool(
            name="get_network_wireless_client_connection_stats",
            description="📡📈 Get aggregated client connection statistics"
        )
        def get_network_wireless_client_connection_stats(
            network_id: str,
            client_id: str,
            t0: Optional[str] = None,
            t1: Optional[str] = None,
            timespan: Optional[float] = 86400,
            ssid: Optional[int] = None,
            vlan: Optional[int] = None,
            ap_tag: Optional[str] = None
        ):
            """Get aggregated client connection statistics."""
            try:
                kwargs = {'timespan': timespan}
                if t0: kwargs['t0'] = t0
                if t1: kwargs['t1'] = t1
                if ssid is not None: kwargs['ssid'] = ssid
                if vlan is not None: kwargs['vlan'] = vlan
                if ap_tag: kwargs['apTag'] = ap_tag
                
                result = meraki_client.dashboard.wireless.getNetworkWirelessClientConnectionStats(
                    network_id, client_id, **kwargs
                )
                
                response = f"# 📈 Client Connection Statistics\n\n"
                response += f"**Client**: {client_id}\n\n"
                
                if isinstance(result, dict):
                    connection_stats = result.get('connectionStats', {})
                    
                    response += "## Connection Success Rates:\n"
                    response += f"- **Overall**: {connection_stats.get('success', 0)}%\n"
                    response += f"- **Authentication**: {connection_stats.get('auth', 0)}%\n"
                    response += f"- **Association**: {connection_stats.get('assoc', 0)}%\n"
                    response += f"- **DHCP**: {connection_stats.get('dhcp', 0)}%\n"
                    response += f"- **DNS**: {connection_stats.get('dns', 0)}%\n"
                
                return response
            except Exception as e:
                return f"❌ Error: {str(e)}"
        
        
    @app.tool(
            name="get_network_wireless_client_latency_stats",
            description="📡⏱️ Get client latency statistics"
        )
        def get_network_wireless_client_latency_stats(
            network_id: str,
            client_id: str,
            t0: Optional[str] = None,
            t1: Optional[str] = None,
            timespan: Optional[float] = 86400,
            ssid: Optional[int] = None,
            vlan: Optional[int] = None,
            ap_tag: Optional[str] = None
        ):
            """Get client latency statistics."""
            try:
                kwargs = {'timespan': timespan}
                if t0: kwargs['t0'] = t0
                if t1: kwargs['t1'] = t1
                if ssid is not None: kwargs['ssid'] = ssid
                if vlan is not None: kwargs['vlan'] = vlan
                if ap_tag: kwargs['apTag'] = ap_tag
                
                result = meraki_client.dashboard.wireless.getNetworkWirelessClientLatencyStats(
                    network_id, client_id, **kwargs
                )
                
                response = f"# ⏱️ Client Latency Statistics\n\n"
                response += f"**Client**: {client_id}\n\n"
                
                if isinstance(result, dict):
                    response += "## Latency by Traffic Type:\n"
                    
                    for traffic_type in ['backgroundTraffic', 'bestEffortTraffic', 'videoTraffic', 'voiceTraffic']:
                        traffic_data = result.get(traffic_type, {})
                        if traffic_data:
                            response += f"\n### {traffic_type.replace('Traffic', ' Traffic').title()}:\n"
                            response += f"- **Average**: {traffic_data.get('avg', 0)}ms\n"
                            response += f"- **Min**: {traffic_data.get('min', 0)}ms\n"
                            response += f"- **Max**: {traffic_data.get('max', 0)}ms\n"
                
                return response
            except Exception as e:
                return f"❌ Error: {str(e)}"
        
        
    @app.tool(
            name="get_network_wireless_client_latency_history",
            description="📡📉 Get historical client latency data"
        )
        def get_network_wireless_client_latency_history(
            network_id: str,
            client_id: str,
            t0: Optional[str] = None,
            t1: Optional[str] = None,
            timespan: Optional[float] = 86400,
            resolution: Optional[int] = None,
            ssid: Optional[int] = None,
            ap_tag: Optional[str] = None
        ):
            """Get historical client latency data."""
            try:
                kwargs = {'timespan': timespan}
                if t0: kwargs['t0'] = t0
                if t1: kwargs['t1'] = t1
                if resolution: kwargs['resolution'] = resolution
                if ssid is not None: kwargs['ssid'] = ssid
                if ap_tag: kwargs['apTag'] = ap_tag
                
                result = meraki_client.dashboard.wireless.getNetworkWirelessClientLatencyHistory(
                    network_id, client_id, **kwargs
                )
                
                response = f"# 📉 Client Latency History\n\n"
                response += f"**Client**: {client_id}\n\n"
                
                if isinstance(result, list):
                    response += f"**Data Points**: {len(result)}\n\n"
                    
                    if result:
                        # Calculate averages
                        latencies = [point.get('latencyMs', 0) for point in result if point.get('latencyMs')]
                        if latencies:
                            response += f"## Latency Summary:\n"
                            response += f"- **Average**: {sum(latencies) // len(latencies)}ms\n"
                            response += f"- **Min**: {min(latencies)}ms\n"
                            response += f"- **Max**: {max(latencies)}ms\n\n"
                        
                        # Show recent data
                        response += "## Recent Measurements:\n"
                        for point in result[-5:]:
                            response += f"- {point.get('t', 'Unknown')}: {point.get('latencyMs', 0)}ms\n"
                
                return response
            except Exception as e:
                return f"❌ Error: {str(e)}"
    
    # ==================== SSID DEVICE TYPE GROUP POLICIES ====================
    
    def register_ssid_device_policy_tools():
        """Register SSID device type group policy tools."""
        
        
    @app.tool(
            name="get_network_wireless_ssid_device_type_group_policies",
            description="📡📱 Get device type group policies for SSID"
        )
        def get_network_wireless_ssid_device_type_group_policies(
            network_id: str,
            number: str
        ):
            """Get device type group policies for SSID."""
            try:
                result = meraki_client.dashboard.wireless.getNetworkWirelessSsidDeviceTypeGroupPolicies(
                    network_id, number
                )
                
                response = f"# 📱 SSID {number} Device Type Policies\n\n"
                
                if isinstance(result, dict):
                    enabled = result.get('enabled', False)
                    response += f"**Status**: {'Enabled ✅' if enabled else 'Disabled ❌'}\n"
                    
                    if enabled:
                        policies = result.get('deviceTypePolicies', [])
                        if policies:
                            response += f"\n## Device Type Policies ({len(policies)}):\n"
                            for policy in policies:
                                response += f"- **{policy.get('deviceType', 'Unknown')}**\n"
                                response += f"  - Policy: {policy.get('devicePolicy', 'Unknown')}\n"
                                response += f"  - Group Policy ID: {policy.get('groupPolicyId', 'None')}\n"
                
                return response
            except Exception as e:
                return f"❌ Error: {str(e)}"
        
        
    @app.tool(
            name="update_network_wireless_ssid_device_type_group_policies",
            description="📡📱 Update device type group policies for SSID"
        )
        def update_network_wireless_ssid_device_type_group_policies(
            network_id: str,
            number: str,
            enabled: Optional[bool] = None,
            device_type_policies: Optional[str] = None
        ):
            """Update device type group policies for SSID."""
            try:
                kwargs = {}
                if enabled is not None:
                    kwargs['enabled'] = enabled
                if device_type_policies:
                    kwargs['deviceTypePolicies'] = json.loads(device_type_policies)
                
                result = meraki_client.dashboard.wireless.updateNetworkWirelessSsidDeviceTypeGroupPolicies(
                    network_id, number, **kwargs
                )
                
                response = f"# ✅ Updated Device Type Policies\n\n"
                response += f"**Status**: {'Enabled ✅' if result.get('enabled') else 'Disabled ❌'}\n"
                
                policies = result.get('deviceTypePolicies', [])
                if policies:
                    response += f"**Configured Policies**: {len(policies)}\n"
                
                return response
            except Exception as e:
                return f"❌ Error: {str(e)}"
        
        
    @app.tool(
            name="get_organization_wireless_clients_overview_by_device",
            description="📡📊 Get wireless client overview by device"
        )
        def get_organization_wireless_clients_overview_by_device(
            organization_id: str,
            t0: Optional[str] = None,
            t1: Optional[str] = None,
            timespan: Optional[float] = 86400,
            per_page: Optional[int] = 1000
        ):
            """Get wireless client overview by device."""
            try:
                kwargs = {'timespan': timespan, 'perPage': per_page}
                if t0: kwargs['t0'] = t0
                if t1: kwargs['t1'] = t1
                
                result = meraki_client.dashboard.wireless.getOrganizationWirelessClientsOverviewByDevice(
                    organization_id, **kwargs
                )
                
                response = f"# 📊 Wireless Clients Overview by Device\n\n"
                
                if isinstance(result, list):
                    response += f"**Total Devices**: {len(result)}\n\n"
                    
                    # Find busiest APs
                    sorted_devices = sorted(result, key=lambda x: x.get('counts', {}).get('total', 0), reverse=True)
                    
                    response += "## Top 10 Busiest APs:\n"
                    for device in sorted_devices[:10]:
                        counts = device.get('counts', {})
                        response += f"- **{device.get('serial', 'Unknown')}**\n"
                        response += f"  - Total Clients: {counts.get('total', 0)}\n"
                        response += f"  - By Status: {counts.get('byStatus', {})}\n"
                    
                    # Usage statistics
                    total_usage = sum(d.get('usage', {}).get('total', 0) for d in result)
                    response += f"\n## Total Usage: {total_usage / (1024*1024*1024):.2f} GB\n"
                
                return response
            except Exception as e:
                return f"❌ Error: {str(e)}"
        
        
    @app.tool(
            name="get_organization_wireless_ssids_statuses_by_device",
            description="📡📊 Get SSID statuses by device"
        )
        def get_organization_wireless_ssids_statuses_by_device(
            organization_id: str,
            network_ids: Optional[str] = None,
            serials: Optional[str] = None,
            bssids: Optional[str] = None,
            per_page: Optional[int] = 500  # API limit: must be between 3 and 500
        ):
            """Get SSID statuses by device."""
            try:
                kwargs = {'perPage': per_page}
                if network_ids: kwargs['networkIds'] = network_ids.split(',')
                if serials: kwargs['serials'] = serials.split(',')
                if bssids: kwargs['bssids'] = bssids.split(',')
                
                result = meraki_client.dashboard.wireless.getOrganizationWirelessSsidsStatusesByDevice(
                    organization_id, **kwargs
                )
                
                response = f"# 📊 SSID Statuses by Device\n\n"
                
                if isinstance(result, list):
                    response += f"**Total Devices**: {len(result)}\n\n"
                    
                    # Count enabled SSIDs
                    for device in result[:5]:
                        response += f"## Device: {device.get('serial', 'Unknown')}\n"
                        
                        basic_service_sets = device.get('basicServiceSets', [])
                        if basic_service_sets:
                            enabled_count = sum(1 for bss in basic_service_sets if bss.get('enabled'))
                            response += f"- **Enabled SSIDs**: {enabled_count}/{len(basic_service_sets)}\n"
                            
                            for bss in basic_service_sets[:3]:
                                if bss.get('enabled'):
                                    response += f"  - SSID {bss.get('ssidNumber', '?')}: {bss.get('ssidName', 'Unknown')}\n"
                                    response += f"    Band: {bss.get('band', 'Unknown')}, Channel: {bss.get('channel', 'Unknown')}\n"
                        response += "\n"
                
                return response
            except Exception as e:
                return f"❌ Error: {str(e)}"
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
        
        # 
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
        
        # 
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
