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
                
                # Add IP assignment mode
                ip_mode = ssid.get('ipAssignmentMode', 'Unknown')
                result += f"- IP Assignment Mode: {ip_mode}\n"
                
                # Add VLAN settings if in bridge mode
                if ip_mode == 'Bridge mode':
                    use_vlan = ssid.get('useVlanTagging', False)
                    if use_vlan:
                        result += f"- VLAN Tagging: Enabled\n"
                        result += f"- VLAN ID: {ssid.get('vlanId', 'Not set')}\n"
                
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
        name="get_network_wireless_client_count_history",
        description="📊 Get historical client count data - See WiFi client trends over time"
    )
    def get_network_wireless_client_count_history(network_id: str, timespan: int = 86400, 
                                                  band: str = None, ssid_number: int = None,
                                                  device_serial: str = None, ap_tag: str = None):
        """
        Get wireless client count history over time.
        
        Args:
            network_id: Network ID
            timespan: Time period in seconds (default: 86400 = 24 hours)
            band: Filter by frequency band ('2.4', '5', or '6')
            ssid_number: Filter by SSID number
            device_serial: Filter by specific AP serial
            ap_tag: Filter by AP tag
            
        Returns:
            Client count trends over time
        """
        try:
            history = meraki_client.get_network_wireless_client_count_history(
                network_id, timespan=timespan, band=band, ssid=ssid_number,
                device_serial=device_serial, ap_tag=ap_tag
            )
            
            if not history:
                return f"No client count history available for network {network_id}."
            
            result = f"# 📊 Wireless Client Count History\n\n"
            result += f"**Network**: {network_id}\n"
            result += f"**Time Period**: Last {timespan // 3600} hours\n"
            
            if band:
                result += f"**Band**: {band} GHz\n"
            if ssid_number:
                result += f"**SSID**: {ssid_number}\n"
            if device_serial:
                result += f"**Device**: {device_serial}\n"
            if ap_tag:
                result += f"**AP Tag**: {ap_tag}\n"
            
            result += "\n## Client Count Over Time\n\n"
            
            # Calculate statistics
            counts = [entry.get('clientCount', 0) for entry in history]
            if counts:
                max_clients = max(counts)
                min_clients = min(counts)
                avg_clients = sum(counts) / len(counts)
                
                result += f"**Peak Clients**: {max_clients}\n"
                result += f"**Minimum Clients**: {min_clients}\n"
                result += f"**Average Clients**: {avg_clients:.1f}\n\n"
            
            # Show recent history
            result += "### Recent Data Points\n\n"
            
            # Determine if this is a new network
            if len(history) < 10:
                result += f"ℹ️ **Note**: Showing all {len(history)} available data points (network may be new)\n\n"
                
            for entry in history[-10:]:  # Last 10 entries
                start_time = entry.get('startTs', 'Unknown')
                end_time = entry.get('endTs', 'Unknown')
                count = entry.get('clientCount', 0)
                
                # Simple visualization
                bar = '█' * min(count, 50)
                result += f"**{start_time[:16]}**: {count} clients {bar}\n"
            
            # If very limited data, provide guidance
            if len(history) <= 2:
                result += "\n⚠️ **Limited Historical Data**\n"
                result += "This appears to be a recently created network. Historical data will accumulate over time.\n"
                result += "For immediate insights, consider using:\n"
                result += "- Current client snapshots\n"
                result += "- Real-time monitoring\n"
                result += "- Connection statistics\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving client count history: {str(e)}"
    
    @app.tool(
        name="get_network_wireless_clients_health_scores",
        description="🏥 Get health scores for all wireless clients - Identify problematic clients"
    )
    def get_network_wireless_clients_health_scores(network_id: str):
        """
        Get health scores for all wireless clients.
        
        Args:
            network_id: Network ID
            
        Returns:
            Health scores for all clients
        """
        try:
            scores = meraki_client.get_network_wireless_clients_health_scores(network_id)
            
            if not scores:
                return f"No client health scores available for network {network_id}."
            
            result = f"# 🏥 Wireless Client Health Scores\n\n"
            result += f"**Network**: {network_id}\n"
            result += f"**Total Clients**: {len(scores)}\n\n"
            
            # Categorize clients by health
            excellent = []
            good = []
            fair = []
            poor = []
            
            for client in scores:
                mac = client.get('mac', 'Unknown')
                client_id = client.get('clientId', '')
                performance = client.get('performance', {})
                onboarding = client.get('onboarding', {})
                
                perf_score = performance.get('latest', 0)
                onboard_score = onboarding.get('latest', 100)
                
                # Overall score (average of performance and onboarding)
                overall = (perf_score + onboard_score) / 2
                
                client_info = {
                    'mac': mac,
                    'id': client_id,
                    'performance': perf_score,
                    'onboarding': onboard_score,
                    'overall': overall
                }
                
                if overall >= 90:
                    excellent.append(client_info)
                elif overall >= 70:
                    good.append(client_info)
                elif overall >= 50:
                    fair.append(client_info)
                else:
                    poor.append(client_info)
            
            # Summary
            result += "## Health Summary\n\n"
            result += f"- 🟢 **Excellent** (90-100): {len(excellent)} clients\n"
            result += f"- 🟡 **Good** (70-89): {len(good)} clients\n"
            result += f"- 🟠 **Fair** (50-69): {len(fair)} clients\n"
            result += f"- 🔴 **Poor** (0-49): {len(poor)} clients\n\n"
            
            # Show problematic clients
            if poor or fair:
                result += "## ⚠️ Clients Needing Attention\n\n"
                
                for client in poor[:10]:  # Show up to 10 poor clients
                    result += f"### 🔴 {client['mac']}\n"
                    result += f"- Performance: {client['performance']}%\n"
                    result += f"- Onboarding: {client['onboarding']}%\n"
                    result += f"- Overall: {client['overall']:.1f}%\n\n"
                
                for client in fair[:5]:  # Show up to 5 fair clients
                    result += f"### 🟠 {client['mac']}\n"
                    result += f"- Performance: {client['performance']}%\n"
                    result += f"- Onboarding: {client['onboarding']}%\n"
                    result += f"- Overall: {client['overall']:.1f}%\n\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving client health scores: {str(e)}"
    
    @app.tool(
        name="get_network_wireless_connection_stats",
        description="📈 Get wireless connection statistics - Success/failure rates for troubleshooting"
    )
    def get_network_wireless_connection_stats(network_id: str, timespan: int = 86400,
                                             band: str = None, ssid_number: int = None,
                                             vlan: int = None, ap_tag: str = None):
        """
        Get aggregated wireless connection statistics.
        
        Args:
            network_id: Network ID
            timespan: Time period in seconds (default: 86400 = 24 hours)
            band: Filter by frequency band ('2.4', '5', or '6')
            ssid_number: Filter by SSID number
            vlan: Filter by VLAN
            ap_tag: Filter by AP tag
            
        Returns:
            Connection success/failure statistics
        """
        try:
            stats = meraki_client.get_network_wireless_connection_stats(
                network_id, timespan=timespan, band=band, ssid=ssid_number,
                vlan=vlan, ap_tag=ap_tag
            )
            
            if not stats:
                return f"No connection statistics available for network {network_id}."
            
            result = f"# 📈 Wireless Connection Statistics\n\n"
            result += f"**Network**: {network_id}\n"
            result += f"**Time Period**: Last {timespan // 3600} hours\n"
            
            if band:
                result += f"**Band**: {band} GHz\n"
            if ssid_number:
                result += f"**SSID**: {ssid_number}\n"
            if vlan:
                result += f"**VLAN**: {vlan}\n"
            if ap_tag:
                result += f"**AP Tag**: {ap_tag}\n"
            
            result += "\n## Connection Metrics\n\n"
            
            # Extract stats
            assoc = stats.get('assoc', 0)
            auth = stats.get('auth', 0)
            dhcp = stats.get('dhcp', 0)
            dns = stats.get('dns', 0)
            success = stats.get('success', 0)
            
            total_attempts = assoc + success if assoc > 0 else success
            
            # Calculate success rates
            if assoc > 0:
                auth_rate = (auth / assoc) * 100 if assoc > 0 else 0
                dhcp_rate = (dhcp / auth) * 100 if auth > 0 else 0
                dns_rate = (dns / dhcp) * 100 if dhcp > 0 else 0
                overall_rate = (success / (assoc + success)) * 100 if (assoc + success) > 0 else 0
            else:
                auth_rate = dhcp_rate = dns_rate = overall_rate = 100
            
            # Connection funnel
            result += "### Connection Funnel\n\n"
            result += f"1. **Association Attempts**: {assoc + success} total\n"
            result += f"   - ✅ Successful: {success}\n"
            result += f"   - ❌ Failed: {assoc}\n\n"
            
            if assoc > 0:
                result += f"2. **Authentication**: {auth_rate:.1f}% success rate\n"
                result += f"   - ✅ Passed: {auth}\n"
                result += f"   - ❌ Failed: {assoc - auth}\n\n"
                
                result += f"3. **DHCP**: {dhcp_rate:.1f}% success rate\n"
                result += f"   - ✅ Obtained IP: {dhcp}\n"
                result += f"   - ❌ Failed: {auth - dhcp}\n\n"
                
                result += f"4. **DNS**: {dns_rate:.1f}% success rate\n"
                result += f"   - ✅ Resolved: {dns}\n"
                result += f"   - ❌ Failed: {dhcp - dns}\n\n"
            
            result += f"### Overall Success Rate: {overall_rate:.1f}%\n\n"
            
            # Troubleshooting guidance
            if overall_rate < 90:
                result += "## ⚠️ Troubleshooting Recommendations\n\n"
                
                if auth_rate < 90:
                    result += "- **Authentication Issues**: Check PSK, RADIUS server, certificates\n"
                if dhcp_rate < 90:
                    result += "- **DHCP Issues**: Check DHCP pool, server availability\n"
                if dns_rate < 90:
                    result += "- **DNS Issues**: Check DNS server configuration\n"
                if assoc > success * 0.1:
                    result += "- **High Failure Rate**: Check RF interference, AP coverage\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving connection statistics: {str(e)}"
    
    @app.tool(
        name="get_network_wireless_failed_connections",
        description="❌ Get failed wireless connection attempts - Troubleshoot connection issues"
    )
    def get_network_wireless_failed_connections(network_id: str, timespan: int = 3600,
                                               band: str = None, ssid_number: int = None,
                                               vlan: int = None, ap_tag: str = None):
        """
        Get details about failed wireless connection attempts.
        
        Args:
            network_id: Network ID
            timespan: Time period in seconds (default: 3600 = 1 hour)
            band: Filter by frequency band
            ssid_number: Filter by SSID number
            vlan: Filter by VLAN
            ap_tag: Filter by AP tag
            
        Returns:
            Failed connection details
        """
        try:
            failures = meraki_client.get_network_wireless_failed_connections(
                network_id, timespan=timespan, band=band, ssid=ssid_number,
                vlan=vlan, ap_tag=ap_tag
            )
            
            if not failures:
                return f"No failed connections found for network {network_id} in the last {timespan // 3600} hours. 🎉"
            
            result = f"# ❌ Failed Wireless Connections\n\n"
            result += f"**Network**: {network_id}\n"
            result += f"**Time Period**: Last {timespan // 3600} hours\n"
            result += f"**Total Failures**: {len(failures)}\n\n"
            
            # Categorize failures
            failure_types = {}
            failure_by_ssid = {}
            failure_by_ap = {}
            
            for failure in failures:
                # Count by failure type
                fail_type = failure.get('failureStep', 'Unknown')
                failure_types[fail_type] = failure_types.get(fail_type, 0) + 1
                
                # Count by SSID
                ssid_name = failure.get('ssidName', 'Unknown')
                failure_by_ssid[ssid_name] = failure_by_ssid.get(ssid_name, 0) + 1
                
                # Count by AP
                ap_name = failure.get('apName', 'Unknown')
                failure_by_ap[ap_name] = failure_by_ap.get(ap_name, 0) + 1
            
            # Show failure breakdown
            result += "## Failure Analysis\n\n"
            
            result += "### By Failure Type\n"
            for fail_type, count in sorted(failure_types.items(), key=lambda x: x[1], reverse=True):
                percentage = (count / len(failures)) * 100
                result += f"- **{fail_type}**: {count} ({percentage:.1f}%)\n"
            
            result += "\n### By SSID\n"
            for ssid, count in sorted(failure_by_ssid.items(), key=lambda x: x[1], reverse=True)[:5]:
                percentage = (count / len(failures)) * 100
                result += f"- **{ssid}**: {count} failures ({percentage:.1f}%)\n"
            
            result += "\n### By Access Point\n"
            for ap, count in sorted(failure_by_ap.items(), key=lambda x: x[1], reverse=True)[:5]:
                percentage = (count / len(failures)) * 100
                result += f"- **{ap}**: {count} failures ({percentage:.1f}%)\n"
            
            # Show recent failures
            result += "\n## Recent Failures (Last 10)\n\n"
            for failure in failures[:10]:
                result += f"### {failure.get('ts', 'Unknown time')}\n"
                result += f"- **Client**: {failure.get('clientMac', 'Unknown')}\n"
                result += f"- **SSID**: {failure.get('ssidName', 'Unknown')}\n"
                result += f"- **AP**: {failure.get('apName', 'Unknown')}\n"
                result += f"- **Step**: {failure.get('failureStep', 'Unknown')}\n"
                result += f"- **Type**: {failure.get('type', 'Unknown')}\n\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving failed connections: {str(e)}"
    
    @app.tool(
        name="get_network_wireless_latency_history",
        description="⏱️ Get wireless latency history - Monitor network performance over time"
    )
    def get_network_wireless_latency_history(network_id: str, timespan: int = 3600,
                                            client_id: str = None, device_serial: str = None,
                                            ap_tag: str = None, band: str = None, 
                                            ssid_number: int = None):
        """
        Get wireless latency history.
        
        Args:
            network_id: Network ID
            timespan: Time period in seconds (default: 3600 = 1 hour)
            client_id: Filter by specific client
            device_serial: Filter by specific AP
            ap_tag: Filter by AP tag
            band: Filter by frequency band
            ssid_number: Filter by SSID
            
        Returns:
            Latency metrics over time
        """
        try:
            history = meraki_client.get_network_wireless_clients_latency_history(
                network_id, timespan=timespan, client_id=client_id,
                device_serial=device_serial, ap_tag=ap_tag, band=band, ssid=ssid_number
            )
            
            if not history:
                return f"No latency history available for network {network_id}."
            
            result = f"# ⏱️ Wireless Latency History\n\n"
            result += f"**Network**: {network_id}\n"
            result += f"**Time Period**: Last {timespan // 3600} hours\n\n"
            
            # Calculate statistics
            latencies = []
            for entry in history:
                if 'latencyMs' in entry:
                    latencies.append(entry['latencyMs'])
            
            if latencies:
                avg_latency = sum(latencies) / len(latencies)
                max_latency = max(latencies)
                min_latency = min(latencies)
                
                result += "## Latency Statistics\n\n"
                result += f"- **Average**: {avg_latency:.1f} ms\n"
                result += f"- **Maximum**: {max_latency} ms\n"
                result += f"- **Minimum**: {min_latency} ms\n\n"
                
                # Performance assessment
                if avg_latency < 50:
                    result += "✅ **Performance**: Excellent\n"
                elif avg_latency < 100:
                    result += "🟡 **Performance**: Good\n"
                elif avg_latency < 200:
                    result += "🟠 **Performance**: Fair\n"
                else:
                    result += "🔴 **Performance**: Poor\n"
            
            # Show recent data
            result += "\n## Recent Measurements\n\n"
            for entry in history[-20:]:  # Last 20 entries
                time = entry.get('ts', 'Unknown')
                latency = entry.get('latencyMs', 0)
                
                # Visual indicator
                if latency < 50:
                    indicator = '🟢'
                elif latency < 100:
                    indicator = '🟡'
                elif latency < 200:
                    indicator = '🟠'
                else:
                    indicator = '🔴'
                
                result += f"{indicator} **{time[:16]}**: {latency} ms\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving latency history: {str(e)}"
    
    @app.tool(
        name="get_organization_wireless_channel_utilization",
        description="📡 Get organization-wide channel utilization - Identify congested channels"
    )
    def get_organization_wireless_channel_utilization(org_id: str, network_id: str, 
                                                     timespan: int = 3600):
        """
        Get channel utilization across all APs in the organization.
        
        Args:
            org_id: Organization ID
            network_id: Network ID to filter
            timespan: Time period in seconds (default: 3600 = 1 hour)
            
        Returns:
            Channel utilization by device
        """
        try:
            # Get network info for context
            network = meraki_client.get_network(network_id)
            
            utilization = meraki_client.get_organization_wireless_devices_channel_utilization_by_device(
                org_id, timespan=timespan, network_ids=[network_id]
            )
            
            if not utilization:
                return f"No channel utilization data available for organization {org_id}."
            
            result = f"# 📡 Channel Utilization Report\n\n"
            result += f"**Organization**: {org_id}\n"
            result += f"**Network**: {network.get('name', network_id)}\n"
            result += f"**Time Period**: Last {timespan // 3600} hours\n\n"
            
            # Analyze by band
            band_2_4_utils = []
            band_5_utils = []
            band_6_utils = []
            
            for device in utilization:
                serial = device.get('serial', 'Unknown')
                name = device.get('name', 'Unnamed')
                
                result += f"## 📡 {name} ({serial})\n\n"
                
                by_band = device.get('byBand', [])
                for band_data in by_band:
                    band = band_data.get('band', 'Unknown')
                    wifi_util = band_data.get('wifi', {}).get('percentage', 0)
                    non_wifi_util = band_data.get('nonWifi', {}).get('percentage', 0)
                    total_util = band_data.get('total', {}).get('percentage', 0)
                    
                    # Collect for summary
                    if '2.4' in str(band):
                        band_2_4_utils.append(total_util)
                    elif '5' in str(band):
                        band_5_utils.append(total_util)
                    elif '6' in str(band):
                        band_6_utils.append(total_util)
                    
                    # Status indicator
                    if total_util > 80:
                        status = '🔴 Congested'
                    elif total_util > 60:
                        status = '🟠 Busy'
                    elif total_util > 40:
                        status = '🟡 Moderate'
                    else:
                        status = '🟢 Clear'
                    
                    result += f"### Band: {band} GHz - {status}\n"
                    result += f"- WiFi Traffic: {wifi_util}%\n"
                    result += f"- Interference: {non_wifi_util}%\n"
                    result += f"- **Total Usage**: {total_util}%\n\n"
            
            # Summary
            result += "## 📊 Network-Wide Summary\n\n"
            
            if band_2_4_utils:
                avg_2_4 = sum(band_2_4_utils) / len(band_2_4_utils)
                result += f"### 2.4 GHz Band\n"
                result += f"- Average Utilization: {avg_2_4:.1f}%\n"
                result += f"- Max Utilization: {max(band_2_4_utils)}%\n\n"
            
            if band_5_utils:
                avg_5 = sum(band_5_utils) / len(band_5_utils)
                result += f"### 5 GHz Band\n"
                result += f"- Average Utilization: {avg_5:.1f}%\n"
                result += f"- Max Utilization: {max(band_5_utils)}%\n\n"
            
            # Recommendations
            result += "## 💡 Recommendations\n\n"
            
            high_util_2_4 = [u for u in band_2_4_utils if u > 70]
            high_util_5 = [u for u in band_5_utils if u > 70]
            
            if high_util_2_4:
                result += f"- ⚠️ {len(high_util_2_4)} APs have high 2.4 GHz utilization\n"
                result += "  - Consider moving clients to 5 GHz\n"
                result += "  - Check for non-WiFi interference\n\n"
            
            if high_util_5:
                result += f"- ⚠️ {len(high_util_5)} APs have high 5 GHz utilization\n"
                result += "  - Consider adding more APs\n"
                result += "  - Enable band steering\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving channel utilization: {str(e)}"
