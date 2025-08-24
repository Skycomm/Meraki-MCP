"""
Wireless-related tools for the Cisco Meraki MCP Server - Modern implementation.
"""

# Global variables to store app and meraki client
app = None
meraki_client = None

def register_wireless_tools(mcp_app, meraki):
    """
    Register wireless-related tools with the MCP server.
    
    Args:
        mcp_app: MCP server instance
        meraki: Meraki client instance
    """
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    
    # Register all wireless tools
    register_wireless_tool_handlers()

def register_wireless_tool_handlers():
    """Register all wireless-related tool handlers using the decorator pattern."""
    
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
                
                # Add additional settings
                result += f"- Band Selection: {ssid.get('bandSelection', 'Unknown')}\n"
                result += f"- Minimum Bitrate: {ssid.get('minBitrate', 'Unknown')}\n"
                
                result += "\n"
                
            return result
            
        except Exception as e:
            return f"Failed to list wireless SSIDs for network {network_id}: {str(e)}"
    
    @app.tool(
        name="get_network_wireless_passwords",
        description="🔑 Get WiFi passwords/PSK for wireless networks"
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
                                   lan_isolation_enabled: bool = None, min_bitrate: float = None,
                                   band_selection: str = None):
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
            min_bitrate: Minimum bitrate in Mbps - 1, 2, 5.5, 6, 9, 11, 12, 18, 24, 36, 48, 54 (optional)
            band_selection: 'Dual band operation', '5 GHz band only', '2.4 GHz band only' (optional)
            
        Returns:
            Updated SSID details
            
        Examples:
            1. WPA2-PSK with password:
               auth_mode='psk', psk='YourPassword', encryption_mode='wpa', wpa_encryption_mode='WPA2 only'
            
            2. Bridge mode to local network:
               ip_assignment_mode='Bridge mode'
            
            3. Bridge mode with VLAN 100:
               ip_assignment_mode='Bridge mode', use_vlan_tagging=True, vlan_id=100
               
            4. IoT optimized (2.4GHz only, 2 Mbps):
               band_selection='2.4 GHz band only', min_bitrate=2
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
                lanIsolationEnabled=lan_isolation_enabled,
                minBitrate=min_bitrate,
                bandSelection=band_selection
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
            if min_bitrate is not None:
                updates.append(f"min bitrate={min_bitrate} Mbps")
            if band_selection is not None:
                updates.append(f"band='{band_selection}'")
                
            return f"✅ SSID {ssid_number} updated successfully: {', '.join(updates)}"
            
        except Exception as e:
            return f"❌ Failed to update SSID: {str(e)}"
    
    @app.tool(
        name="get_network_wireless_clients",
        description="List wireless clients for a Meraki network"
    )
    def get_network_wireless_clients(network_id: str):
        """
        List wireless clients for a Meraki network.
        
        Args:
            network_id: ID of the network
            
        Returns:
            Formatted list of wireless clients
        """
        try:
            clients = meraki_client.get_network_wireless_clients(network_id)
            
            if not clients:
                return f"No wireless clients found for network {network_id}."
                
            # Format the output for readability
            result = f"# Wireless Clients in Network ({network_id})\n\n"
            for client in clients:
                result += f"- **{client.get('description', 'Unknown Device')}**\n"
                result += f"  - MAC: `{client.get('mac', 'Unknown')}`\n"
                result += f"  - IP: `{client.get('ip', 'Unknown')}`\n"
                result += f"  - SSID: {client.get('ssid', 'Unknown')}\n"
                result += f"  - RSSI: {client.get('rssi', 'Unknown')} dBm\n"
                result += f"  - Connection: {client.get('status', 'Unknown')}\n"
                
                # Add usage if available
                usage = client.get('usage')
                if usage:
                    result += f"  - Usage: {usage.get('sent', 0)} sent, {usage.get('recv', 0)} received\n"
                
                result += "\n"
                
            return result
            
        except Exception as e:
            return f"Failed to list wireless clients for network {network_id}: {str(e)}"
    
    @app.tool(
        name="get_network_wireless_usage",
        description="Get wireless usage statistics for a Meraki network"
    )
    def get_network_wireless_usage(network_id: str, ssid_number: int = None, device_serial: str = None):
        """
        Get wireless usage statistics for a Meraki network.
        
        Args:
            network_id: ID of the network
            ssid_number: Optional SSID number to filter (0-14)
            device_serial: Optional device serial to filter by specific AP
            
        Returns:
            Formatted wireless usage statistics
        """
        try:
            usage = meraki_client.get_network_wireless_usage(
                network_id, 
                ssid_number=ssid_number,
                device_serial=device_serial
            )
            
            if not usage:
                return f"No wireless usage statistics found for network {network_id}."
                
            # Format the output for readability
            result = f"# Wireless Usage Statistics for Network ({network_id})\n\n"
            
            if isinstance(usage, dict):
                for ssid, stats in usage.items():
                    result += f"## SSID: {ssid}\n"
                    result += f"- Total Traffic: {stats.get('total', 0)} bytes\n"
                    result += f"- Sent: {stats.get('sent', 0)} bytes\n"
                    result += f"- Received: {stats.get('recv', 0)} bytes\n"
                    result += f"- Clients: {stats.get('numClients', 0)}\n"
                    result += "\n"
            else:
                result += str(usage)
                
            return result
            
        except Exception as e:
            return f"Failed to get wireless usage statistics for network {network_id}: {str(e)}"
    
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
        name="get_network_wireless_channel_utilization",
        description="📊 Get channel utilization history"
    )
    def get_network_wireless_channel_utilization(network_id: str, timespan: int = 3600, ssid_number: int = None, device_serial: str = None):
        """
        Get wireless channel utilization history for a network.
        
        Args:
            network_id: ID of the network
            timespan: Timespan in seconds (default: 1 hour)
            ssid_number: Optional SSID number to filter (0-14)
            device_serial: Optional device serial to filter by specific AP
            
        Returns:
            Channel utilization statistics
        """
        try:
            utilization = meraki_client.get_network_wireless_channel_utilization(
                network_id, 
                timespan,
                ssid_number=ssid_number,
                device_serial=device_serial
            )
            
            if not utilization:
                return f"No channel utilization data found for network {network_id}."
                
            result = f"# 📊 Channel Utilization - Network {network_id}\n"
            result += f"**Time Period**: Last {timespan/3600:.1f} hours\n\n"
            
            for entry in utilization:
                timestamp = entry.get('startTs', 'Unknown')
                result += f"## {timestamp}\n"
                
                # WiFi utilization
                wifi = entry.get('wifi', {})
                if wifi:
                    result += f"- **WiFi Utilization**: {wifi.get('utilization', 0)}%\n"
                    
                # Non-WiFi utilization  
                non_wifi = entry.get('nonWifi', {})
                if non_wifi:
                    result += f"- **Non-WiFi Interference**: {non_wifi.get('utilization', 0)}%\n"
                    
                # Total utilization
                total = entry.get('total', {})
                if total:
                    result += f"- **Total Utilization**: {total.get('utilization', 0)}%\n"
                    
                result += "\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving channel utilization: {str(e)}"
