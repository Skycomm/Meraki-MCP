"""
Wireless management tools for the Cisco Meraki MCP Server - COMPLETE v1.61 IMPLEMENTATION.
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
    
    # SSID Management
    @app.tool(
        name="get_network_wireless_ssids",
        description="📶 List wireless SSIDs for a network"
    )
    def get_network_wireless_ssids(network_id: str):
        """List all SSIDs in a wireless network."""
        try:
            ssids = meraki_client.dashboard.wireless.getNetworkWirelessSsids(network_id)
            
            if not ssids:
                return f"No wireless SSIDs found for network {network_id}."
                
            result = f"# 📶 Wireless SSIDs in Network {network_id}\n\n"
            for ssid in ssids:
                result += f"## SSID {ssid.get('number', 'Unknown')}: {ssid.get('name', 'Unnamed')}\n"
                result += f"- Enabled: {'✅' if ssid.get('enabled') else '❌'}\n"
                result += f"- Visible: {'✅' if ssid.get('visible') else '❌'}\n"
                result += f"- Auth Mode: {ssid.get('authMode', 'Unknown')}\n"
                result += f"- IP Assignment: {ssid.get('ipAssignmentMode', 'Unknown')}\n"
                
                if ssid.get('useVlanTagging'):
                    result += f"- VLAN ID: {ssid.get('vlanId', 'Not set')}\n"
                
                result += "\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving wireless SSIDs: {str(e)}"
    
    @app.tool(
        name="get_network_wireless_ssid",
        description="📶 Get details of a specific SSID"
    )
    def get_network_wireless_ssid(network_id: str, number: str):
        """Get configuration for a specific SSID."""
        try:
            ssid = meraki_client.dashboard.wireless.getNetworkWirelessSsid(network_id, number)
            
            result = f"# 📶 SSID {number} Configuration\n\n"
            result += f"**Name**: {ssid.get('name', 'Unnamed')}\n"
            result += f"**Enabled**: {'✅' if ssid.get('enabled') else '❌'}\n"
            result += f"**Visible**: {'✅' if ssid.get('visible') else '❌'}\n"
            result += f"**Auth Mode**: {ssid.get('authMode', 'Unknown')}\n"
            
            if ssid.get('encryptionMode'):
                result += f"**Encryption**: {ssid['encryptionMode']}\n"
            
            result += f"**IP Assignment**: {ssid.get('ipAssignmentMode', 'Unknown')}\n"
            
            if ssid.get('useVlanTagging'):
                result += f"**VLAN Tagging**: Enabled (VLAN {ssid.get('vlanId')})\n"
            
            if ssid.get('radiusServers'):
                result += f"**RADIUS Servers**: {len(ssid['radiusServers'])} configured\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving SSID {number}: {str(e)}"
    
    @app.tool(
        name="update_network_wireless_ssid",
        description="🔧 Update wireless SSID configuration"
    )
    def update_network_wireless_ssid(network_id: str, number: str, **kwargs):
        """Update configuration for a specific SSID."""
        try:
            result = meraki_client.dashboard.wireless.updateNetworkWirelessSsid(
                network_id, number, **kwargs
            )
            
            return f"✅ SSID {number} updated successfully!\n\nUpdated settings applied."
            
        except Exception as e:
            return f"Error updating SSID {number}: {str(e)}"
    
    # RF Profiles
    @app.tool(
        name="get_network_wireless_rf_profiles",
        description="📡 Get RF profiles for a network"
    )
    def get_network_wireless_rf_profiles(network_id: str):
        """List RF profiles for optimizing wireless performance."""
        try:
            profiles = meraki_client.dashboard.wireless.getNetworkWirelessRfProfiles(network_id)
            
            if not profiles:
                return f"No RF profiles found for network {network_id}."
                
            result = f"# 📡 RF Profiles for Network {network_id}\n\n"
            
            for profile in profiles:
                result += f"## {profile.get('name', 'Unnamed Profile')}\n"
                result += f"- **ID**: {profile.get('id')}\n"
                result += f"- **Band Selection**: {profile.get('bandSelectionType', 'N/A')}\n"
                result += f"- **Client Balancing**: {'✅' if profile.get('clientBalancingEnabled') else '❌'}\n"
                
                if profile.get('minBitrate'):
                    result += f"- **Min Bitrate (2.4GHz)**: {profile['minBitrate']} Mbps\n"
                if profile.get('minBitrate5'):
                    result += f"- **Min Bitrate (5GHz)**: {profile['minBitrate5']} Mbps\n"
                if profile.get('minBitrate6'):
                    result += f"- **Min Bitrate (6GHz)**: {profile['minBitrate6']} Mbps\n"
                    
                result += "\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving RF profiles: {str(e)}"
    
    @app.tool(
        name="create_network_wireless_rf_profile",
        description="📡 Create a new RF profile"
    )
    def create_network_wireless_rf_profile(network_id: str, name: str, bandSelectionType: str, **kwargs):
        """Create a new RF profile for wireless optimization."""
        try:
            profile = meraki_client.dashboard.wireless.createNetworkWirelessRfProfile(
                network_id, name, bandSelectionType, **kwargs
            )
            
            return f"✅ RF Profile '{name}' created successfully!\n\nProfile ID: {profile.get('id')}"
            
        except Exception as e:
            return f"Error creating RF profile: {str(e)}"
    
    @app.tool(
        name="update_network_wireless_rf_profile",
        description="📡 Update an RF profile"
    )
    def update_network_wireless_rf_profile(network_id: str, rf_profile_id: str, **kwargs):
        """Update an existing RF profile."""
        try:
            result = meraki_client.dashboard.wireless.updateNetworkWirelessRfProfile(
                network_id, rf_profile_id, **kwargs
            )
            
            return f"✅ RF Profile {rf_profile_id} updated successfully!"
            
        except Exception as e:
            return f"Error updating RF profile: {str(e)}"
    
    @app.tool(
        name="delete_network_wireless_rf_profile",
        description="📡 Delete an RF profile"
    )
    def delete_network_wireless_rf_profile(network_id: str, rf_profile_id: str):
        """Delete an RF profile."""
        try:
            meraki_client.dashboard.wireless.deleteNetworkWirelessRfProfile(network_id, rf_profile_id)
            return f"✅ RF Profile {rf_profile_id} deleted successfully!"
            
        except Exception as e:
            return f"Error deleting RF profile: {str(e)}"
    
    # Bluetooth Settings
    @app.tool(
        name="get_network_wireless_bluetooth_settings",
        description="📱 Get Bluetooth settings for a network"
    )
    def get_network_wireless_bluetooth_settings(network_id: str):
        """Get Bluetooth settings for the wireless network."""
        try:
            settings = meraki_client.dashboard.wireless.getNetworkWirelessBluetoothSettings(network_id)
            
            result = f"# 📱 Bluetooth Settings for Network {network_id}\n\n"
            result += f"**Scanning Enabled**: {'✅' if settings.get('scanningEnabled') else '❌'}\n"
            result += f"**Advertising Enabled**: {'✅' if settings.get('advertisingEnabled') else '❌'}\n"
            
            if settings.get('uuid'):
                result += f"**UUID**: {settings['uuid']}\n"
            
            if settings.get('major'):
                result += f"**Major**: {settings['major']}\n"
                
            if settings.get('minor'):
                result += f"**Minor**: {settings['minor']}\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving Bluetooth settings: {str(e)}"
    
    @app.tool(
        name="update_network_wireless_bluetooth_settings",
        description="📱 Update Bluetooth settings"
    )
    def update_network_wireless_bluetooth_settings(network_id: str, **kwargs):
        """Update Bluetooth settings for the wireless network."""
        try:
            result = meraki_client.dashboard.wireless.updateNetworkWirelessBluetoothSettings(
                network_id, **kwargs
            )
            
            return f"✅ Bluetooth settings updated successfully!"
            
        except Exception as e:
            return f"Error updating Bluetooth settings: {str(e)}"
    
    # Client Management
    @app.tool(
        name="get_network_wireless_clients",
        description="👥 List wireless clients in a network"
    )
    def get_network_wireless_clients(network_id: str, **kwargs):
        """List wireless clients connected to the network."""
        try:
            clients = meraki_client.dashboard.wireless.getNetworkWirelessClients(network_id, **kwargs)
            
            if not clients:
                return f"No wireless clients found for network {network_id}."
                
            result = f"# 👥 Wireless Clients in Network {network_id}\n\n"
            result += f"**Total Clients**: {len(clients)}\n\n"
            
            for client in clients[:20]:  # Show first 20
                result += f"## {client.get('description', 'Unknown Device')}\n"
                result += f"- MAC: `{client.get('mac', 'Unknown')}`\n"
                result += f"- IP: `{client.get('ip', 'Unknown')}`\n"
                result += f"- SSID: {client.get('ssid', 'Unknown')}\n"
                result += f"- RSSI: {client.get('rssi', 'Unknown')} dBm\n"
                result += f"- Status: {client.get('status', 'Unknown')}\n"
                
                usage = client.get('usage')
                if usage:
                    sent_mb = usage.get('sent', 0) / 1024 / 1024
                    recv_mb = usage.get('recv', 0) / 1024 / 1024
                    result += f"- Usage: {sent_mb:.1f} MB sent, {recv_mb:.1f} MB received\n"
                
                result += "\n"
                
            if len(clients) > 20:
                result += f"... and {len(clients) - 20} more clients\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving wireless clients: {str(e)}"
    
    @app.tool(
        name="get_network_wireless_client_count_history",
        description="📊 Get wireless client count history"
    )
    def get_network_wireless_client_count_history(network_id: str, **kwargs):
        """Get historical client count data over time."""
        try:
            # Add default timespan if not specified
            if 'timespan' not in kwargs and 't0' not in kwargs:
                kwargs['timespan'] = 604800  # Default to 7 days
            
            history = meraki_client.dashboard.wireless.getNetworkWirelessClientCountHistory(
                network_id, **kwargs
            )
            
            if not history:
                return f"No client count history available for network {network_id}."
            
            result = f"# 📊 Client Count History for Network {network_id}\n\n"
            
            # Calculate statistics
            counts = [entry.get('clientCount', 0) for entry in history]
            if counts:
                result += f"**Peak Clients**: {max(counts)}\n"
                result += f"**Average Clients**: {sum(counts) / len(counts):.1f}\n"
                result += f"**Minimum Clients**: {min(counts)}\n\n"
            
            result += "## Recent History\n\n"
            for entry in history[-10:]:  # Last 10 entries
                time = entry.get('startTs', 'Unknown')
                count = entry.get('clientCount', 0)
                bar = '█' * min(count, 50)
                result += f"**{time[:16]}**: {count} clients {bar}\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving client count history: {str(e)}"
    
    # Connection Stats
    @app.tool(
        name="get_network_wireless_connection_stats",
        description="📈 Get wireless connection statistics"
    )
    def get_network_wireless_connection_stats(network_id: str, **kwargs):
        """Get aggregated wireless connection statistics."""
        try:
            # Default to timespan if no time parameters specified
            if 'timespan' not in kwargs and 't0' not in kwargs:
                kwargs['timespan'] = 86400  # Default to 1 day
            
            # If both t0 and t1 are specified together, remove t1 and use timespan
            if 't0' in kwargs and 't1' in kwargs:
                # Calculate timespan from t0 and t1 if possible, otherwise use default
                kwargs.pop('t0', None)
                kwargs.pop('t1', None)
                kwargs['timespan'] = 86400  # Default to 1 day
            
            stats = meraki_client.dashboard.wireless.getNetworkWirelessConnectionStats(
                network_id, **kwargs
            )
            
            if not stats:
                return f"No connection statistics available for network {network_id}."
            
            result = f"# 📈 Wireless Connection Statistics\n\n"
            
            # Extract stats
            assoc = stats.get('assoc', 0)
            auth = stats.get('auth', 0)
            dhcp = stats.get('dhcp', 0)
            dns = stats.get('dns', 0)
            success = stats.get('success', 0)
            
            total = assoc + success if assoc > 0 else success
            
            if total > 0:
                result += f"**Total Connection Attempts**: {total}\n"
                result += f"**Successful Connections**: {success}\n"
                result += f"**Overall Success Rate**: {(success / total * 100):.1f}%\n\n"
                
                if assoc > 0:
                    result += "## Connection Funnel\n\n"
                    result += f"1. **Association**: {assoc} attempts\n"
                    result += f"2. **Authentication**: {auth} ({(auth/assoc*100):.1f}% success)\n"
                    result += f"3. **DHCP**: {dhcp} ({(dhcp/auth*100 if auth > 0 else 0):.1f}% success)\n"
                    result += f"4. **DNS**: {dns} ({(dns/dhcp*100 if dhcp > 0 else 0):.1f}% success)\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving connection statistics: {str(e)}"
    
    @app.tool(
        name="get_network_wireless_failed_connections",
        description="❌ Get failed wireless connection attempts"
    )
    def get_network_wireless_failed_connections(network_id: str, **kwargs):
        """Get details about failed wireless connection attempts."""
        try:
            # Default to timespan if no time parameters specified
            if 'timespan' not in kwargs and 't0' not in kwargs:
                kwargs['timespan'] = 86400  # Default to 1 day
            
            # If both t0 and t1 are specified together, remove them and use timespan
            if 't0' in kwargs and 't1' in kwargs:
                kwargs.pop('t0', None)
                kwargs.pop('t1', None)
                kwargs['timespan'] = 86400  # Default to 1 day
            
            failures = meraki_client.dashboard.wireless.getNetworkWirelessFailedConnections(
                network_id, **kwargs
            )
            
            if not failures:
                return f"No failed connections found for network {network_id}. 🎉"
            
            result = f"# ❌ Failed Wireless Connections\n\n"
            result += f"**Total Failures**: {len(failures)}\n\n"
            
            # Categorize failures
            failure_types = {}
            for failure in failures:
                fail_type = failure.get('failureStep', 'Unknown')
                failure_types[fail_type] = failure_types.get(fail_type, 0) + 1
            
            result += "## Failure Breakdown\n\n"
            for fail_type, count in sorted(failure_types.items(), key=lambda x: x[1], reverse=True):
                percentage = (count / len(failures)) * 100
                result += f"- **{fail_type}**: {count} ({percentage:.1f}%)\n"
            
            result += "\n## Recent Failures\n\n"
            for failure in failures[:10]:
                result += f"- **{failure.get('ts', 'Unknown')}**\n"
                result += f"  - Client: {failure.get('clientMac')}\n"
                result += f"  - SSID: {failure.get('ssidName')}\n"
                result += f"  - AP: {failure.get('apName')}\n"
                result += f"  - Step: {failure.get('failureStep')}\n\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving failed connections: {str(e)}"
    
    # Data Rate History
    @app.tool(
        name="get_network_wireless_data_rate_history",
        description="📊 Get wireless data rate history"
    )
    def get_network_wireless_data_rate_history(network_id: str, **kwargs):
        """Get historical data rate information."""
        try:
            # Add default timespan if not specified
            if 'timespan' not in kwargs and 't0' not in kwargs:
                kwargs['timespan'] = 604800  # Default to 7 days
            
            history = meraki_client.dashboard.wireless.getNetworkWirelessDataRateHistory(
                network_id, **kwargs
            )
            
            if not history:
                return f"No data rate history available for network {network_id}."
            
            result = f"# 📊 Data Rate History for Network {network_id}\n\n"
            
            for entry in history[-20:]:  # Last 20 entries
                time = entry.get('startTs', 'Unknown')
                result += f"## {time[:16]}\n"
                
                # Average data rates
                if 'averageKbps' in entry:
                    avg_mbps = entry['averageKbps'] / 1000
                    result += f"- Average: {avg_mbps:.1f} Mbps\n"
                
                if 'downloadKbps' in entry:
                    dl_mbps = entry['downloadKbps'] / 1000
                    result += f"- Download: {dl_mbps:.1f} Mbps\n"
                    
                if 'uploadKbps' in entry:
                    ul_mbps = entry['uploadKbps'] / 1000
                    result += f"- Upload: {ul_mbps:.1f} Mbps\n"
                
                result += "\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving data rate history: {str(e)}"
    
    # Usage History
    @app.tool(
        name="get_network_wireless_usage_history",
        description="📊 Get wireless usage history"
    )
    def get_network_wireless_usage_history(network_id: str, **kwargs):
        """Get historical wireless usage data."""
        try:
            # Add default timespan if not specified
            if 'timespan' not in kwargs and 't0' not in kwargs:
                kwargs['timespan'] = 604800  # Default to 7 days
            
            history = meraki_client.dashboard.wireless.getNetworkWirelessUsageHistory(
                network_id, **kwargs
            )
            
            if not history:
                return f"No usage history available for network {network_id}."
            
            result = f"# 📊 Wireless Usage History for Network {network_id}\n\n"
            
            total_sent = 0
            total_recv = 0
            
            for entry in history:
                total_sent += entry.get('sentKbps', 0)
                total_recv += entry.get('receivedKbps', 0)
            
            if len(history) > 0:
                avg_sent = total_sent / len(history) / 1000  # Convert to Mbps
                avg_recv = total_recv / len(history) / 1000
                
                result += f"**Average Sent**: {avg_sent:.1f} Mbps\n"
                result += f"**Average Received**: {avg_recv:.1f} Mbps\n\n"
            
            result += "## Recent Usage\n\n"
            for entry in history[-10:]:  # Last 10 entries
                time = entry.get('startTs', 'Unknown')
                sent_mbps = entry.get('sentKbps', 0) / 1000
                recv_mbps = entry.get('receivedKbps', 0) / 1000
                
                result += f"**{time[:16]}**\n"
                result += f"- Sent: {sent_mbps:.1f} Mbps\n"
                result += f"- Received: {recv_mbps:.1f} Mbps\n\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving usage history: {str(e)}"
    
    # Latency Stats
    @app.tool(
        name="get_network_wireless_latency_stats",
        description="⏱️ Get wireless latency statistics"
    )
    def get_network_wireless_latency_stats(network_id: str, **kwargs):
        """Get aggregated wireless latency statistics."""
        try:
            # Add default timespan if not specified
            if 'timespan' not in kwargs and 't0' not in kwargs:
                kwargs['timespan'] = 86400  # Default to 1 day
            
            stats = meraki_client.dashboard.wireless.getNetworkWirelessLatencyStats(
                network_id, **kwargs
            )
            
            if not stats:
                return f"No latency statistics available for network {network_id}."
            
            result = f"# ⏱️ Wireless Latency Statistics\n\n"
            
            # Background traffic stats
            if 'backgroundTraffic' in stats:
                bg = stats['backgroundTraffic']
                result += "## Background Traffic Latency\n"
                result += f"- Average: {bg.get('avg', 0):.1f} ms\n"
                result += f"- Minimum: {bg.get('min', 0)} ms\n"
                result += f"- Maximum: {bg.get('max', 0)} ms\n\n"
            
            # Best effort traffic
            if 'bestEffortTraffic' in stats:
                be = stats['bestEffortTraffic']
                result += "## Best Effort Traffic Latency\n"
                result += f"- Average: {be.get('avg', 0):.1f} ms\n"
                result += f"- Minimum: {be.get('min', 0)} ms\n"
                result += f"- Maximum: {be.get('max', 0)} ms\n\n"
            
            # Video traffic
            if 'videoTraffic' in stats:
                video = stats['videoTraffic']
                result += "## Video Traffic Latency\n"
                result += f"- Average: {video.get('avg', 0):.1f} ms\n"
                result += f"- Minimum: {video.get('min', 0)} ms\n"
                result += f"- Maximum: {video.get('max', 0)} ms\n\n"
            
            # Voice traffic
            if 'voiceTraffic' in stats:
                voice = stats['voiceTraffic']
                result += "## Voice Traffic Latency\n"
                result += f"- Average: {voice.get('avg', 0):.1f} ms\n"
                result += f"- Minimum: {voice.get('min', 0)} ms\n"
                result += f"- Maximum: {voice.get('max', 0)} ms\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving latency statistics: {str(e)}"
    
    @app.tool(
        name="get_network_wireless_latency_history",
        description="⏱️ Get wireless latency history"
    )
    def get_network_wireless_latency_history(network_id: str, **kwargs):
        """Get historical wireless latency data."""
        try:
            # Add default timespan if not specified
            if 'timespan' not in kwargs and 't0' not in kwargs:
                kwargs['timespan'] = 604800  # Default to 7 days
            
            history = meraki_client.dashboard.wireless.getNetworkWirelessLatencyHistory(
                network_id, **kwargs
            )
            
            if not history:
                return f"No latency history available for network {network_id}."
            
            result = f"# ⏱️ Wireless Latency History\n\n"
            
            # Calculate overall stats
            all_latencies = []
            for entry in history:
                if 'latencyMs' in entry:
                    all_latencies.append(entry['latencyMs'])
            
            if all_latencies:
                result += f"**Average Latency**: {sum(all_latencies)/len(all_latencies):.1f} ms\n"
                result += f"**Max Latency**: {max(all_latencies)} ms\n"
                result += f"**Min Latency**: {min(all_latencies)} ms\n\n"
            
            result += "## Recent Measurements\n\n"
            for entry in history[-20:]:  # Last 20
                time = entry.get('t', 'Unknown')
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
    
    # Mesh Status
    @app.tool(
        name="get_network_wireless_mesh_statuses",
        description="🔗 Get wireless mesh status"
    )
    def get_network_wireless_mesh_statuses(network_id: str, **kwargs):
        """Get the mesh status for wireless devices."""
        try:
            statuses = meraki_client.dashboard.wireless.getNetworkWirelessMeshStatuses(
                network_id, **kwargs
            )
            
            if not statuses:
                return f"No mesh status information available for network {network_id}."
            
            result = f"# 🔗 Wireless Mesh Status for Network {network_id}\n\n"
            
            gateways = []
            repeaters = []
            
            for device in statuses:
                if device.get('meshRole') == 'gateway':
                    gateways.append(device)
                else:
                    repeaters.append(device)
            
            result += f"**Mesh Gateways**: {len(gateways)}\n"
            result += f"**Mesh Repeaters**: {len(repeaters)}\n\n"
            
            if gateways:
                result += "## 🌐 Gateways\n\n"
                for gw in gateways:
                    result += f"- **{gw.get('name', 'Unknown')}** ({gw.get('serial')})\n"
                    result += f"  - Status: {gw.get('status', 'Unknown')}\n"
                    
            if repeaters:
                result += "\n## 📡 Repeaters\n\n"
                for rep in repeaters:
                    result += f"- **{rep.get('name', 'Unknown')}** ({rep.get('serial')})\n"
                    result += f"  - Status: {rep.get('status', 'Unknown')}\n"
                    result += f"  - Uplink: {rep.get('uplinkDevice', 'Unknown')}\n"
                    result += f"  - Hop Count: {rep.get('hopCount', 'Unknown')}\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving mesh status: {str(e)}"
    
    # Device Usage History
    @app.tool(
        name="get_network_wireless_devices_latency_stats",
        description="⏱️ Get latency stats for wireless devices"
    )
    def get_network_wireless_devices_latency_stats(network_id: str, **kwargs):
        """Get latency statistics for wireless devices."""
        try:
            # Add default timespan if not specified
            if 'timespan' not in kwargs and 't0' not in kwargs:
                kwargs['timespan'] = 86400  # Default to 1 day
            
            stats = meraki_client.dashboard.wireless.getNetworkWirelessDevicesLatencyStats(
                network_id, **kwargs
            )
            
            if not stats:
                return f"No device latency statistics available for network {network_id}."
            
            result = f"# ⏱️ Wireless Device Latency Statistics\n\n"
            
            for device in stats:
                serial = device.get('serial', 'Unknown')
                name = device.get('name', 'Unknown Device')
                
                result += f"## {name} ({serial})\n"
                
                # Get latency stats
                latency = device.get('latencyStats', {})
                if latency:
                    result += f"- Average: {latency.get('avg', 0):.1f} ms\n"
                    result += f"- Minimum: {latency.get('min', 0)} ms\n"
                    result += f"- Maximum: {latency.get('max', 0)} ms\n"
                
                result += "\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving device latency statistics: {str(e)}"
    
    # Channel Utilization
    @app.tool(
        name="get_network_wireless_channel_utilization_history",
        description="📡 Get channel utilization history"
    )
    def get_network_wireless_channel_utilization_history(network_id: str, **kwargs):
        """Get historical channel utilization data."""
        try:
            # Set default timespan if no time parameters specified
            if 'timespan' not in kwargs and 't0' not in kwargs:
                kwargs['timespan'] = 604800  # Default to 7 days
            
            # Set default resolution if not specified
            if 'resolution' not in kwargs:
                kwargs['resolution'] = 86400  # Default to 1 day resolution
            
            history = meraki_client.dashboard.wireless.getNetworkWirelessChannelUtilizationHistory(
                network_id, **kwargs
            )
            
            if not history:
                return f"No channel utilization history available for network {network_id}."
            
            result = f"# 📡 Channel Utilization History\n\n"
            
            for entry in history[-10:]:  # Last 10 entries
                time = entry.get('startTs', 'Unknown')
                result += f"## {time[:16]}\n"
                
                # WiFi utilization
                wifi = entry.get('wifi', {})
                if wifi:
                    result += f"- WiFi Utilization: {wifi.get('percentage', 0)}%\n"
                
                # Non-WiFi utilization
                non_wifi = entry.get('nonWifi', {})
                if non_wifi:
                    result += f"- Non-WiFi Interference: {non_wifi.get('percentage', 0)}%\n"
                
                # Total utilization
                total = entry.get('total', {})
                if total:
                    result += f"- Total Utilization: {total.get('percentage', 0)}%\n"
                
                result += "\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving channel utilization history: {str(e)}"
    
    # Signal Quality History
    @app.tool(
        name="get_network_wireless_signal_quality_history",
        description="📶 Get signal quality history"
    )
    def get_network_wireless_signal_quality_history(network_id: str, **kwargs):
        """Get historical signal quality data."""
        try:
            # Add default timespan if not specified
            if 'timespan' not in kwargs and 't0' not in kwargs:
                kwargs['timespan'] = 604800  # Default to 7 days
            
            history = meraki_client.dashboard.wireless.getNetworkWirelessSignalQualityHistory(
                network_id, **kwargs
            )
            
            if not history:
                return f"No signal quality history available for network {network_id}."
            
            result = f"# 📶 Signal Quality History\n\n"
            
            for entry in history[-20:]:  # Last 20 entries
                time = entry.get('startTs', 'Unknown')
                rssi = entry.get('rssi', 0)
                snr = entry.get('snr', 0)
                
                # Quality indicator
                if rssi > -67:
                    quality = '🟢 Excellent'
                elif rssi > -70:
                    quality = '🟡 Good'
                elif rssi > -80:
                    quality = '🟠 Fair'
                else:
                    quality = '🔴 Poor'
                
                result += f"**{time[:16]}** - {quality}\n"
                result += f"- RSSI: {rssi} dBm\n"
                result += f"- SNR: {snr} dB\n\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving signal quality history: {str(e)}"
    
    # Air Marshal
    @app.tool(
        name="get_network_wireless_air_marshal",
        description="🛡️ Get Air Marshal security scan results"
    )
    def get_network_wireless_air_marshal(network_id: str, **kwargs):
        """Get Air Marshal (rogue AP detection) results."""
        try:
            air_marshal = meraki_client.dashboard.wireless.getNetworkWirelessAirMarshal(
                network_id, **kwargs
            )
            
            if not air_marshal:
                return f"No Air Marshal data found for network {network_id}."
            
            result = f"# 🛡️ Air Marshal Security Scan\n\n"
            
            # Group by classification
            rogues = []
            neighbors = []
            others = []
            
            for ap in air_marshal:
                if 'Rogue' in ap.get('wiredVendor', ''):
                    rogues.append(ap)
                elif 'Neighbor' in ap.get('wiredVendor', ''):
                    neighbors.append(ap)
                else:
                    others.append(ap)
            
            result += f"**Rogue APs**: {len(rogues)}\n"
            result += f"**Neighbor APs**: {len(neighbors)}\n"
            result += f"**Other APs**: {len(others)}\n\n"
            
            if rogues:
                result += "## 🚨 Rogue APs Detected\n\n"
                for ap in rogues[:10]:
                    result += f"- **SSID**: {ap.get('ssid', 'Hidden')}\n"
                    result += f"  - BSSID: {ap.get('bssid')}\n"
                    result += f"  - Channel: {ap.get('channel')}\n"
                    result += f"  - RSSI: {ap.get('rssi')} dBm\n"
                    result += f"  - First Seen: {ap.get('firstSeen')}\n"
                    result += f"  - Last Seen: {ap.get('lastSeen')}\n\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving Air Marshal data: {str(e)}"
    
    # Settings
    @app.tool(
        name="get_network_wireless_settings",
        description="⚙️ Get wireless network settings"
    )
    def get_network_wireless_settings(network_id: str):
        """Get wireless network settings."""
        try:
            settings = meraki_client.dashboard.wireless.getNetworkWirelessSettings(network_id)
            
            result = f"# ⚙️ Wireless Settings for Network {network_id}\n\n"
            
            result += f"**Meshing Enabled**: {'✅' if settings.get('meshingEnabled') else '❌'}\n"
            result += f"**IPv6 Bridge Mode**: {'✅' if settings.get('ipv6BridgeEnabled') else '❌'}\n"
            result += f"**LED Lights On**: {'✅' if settings.get('ledLightsOn') else '❌'}\n"
            
            if settings.get('locationAnalyticsEnabled') is not None:
                result += f"**Location Analytics**: {'✅' if settings['locationAnalyticsEnabled'] else '❌'}\n"
            
            if settings.get('upgradeStrategy'):
                result += f"**Upgrade Strategy**: {settings['upgradeStrategy']}\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving wireless settings: {str(e)}"
    
    @app.tool(
        name="update_network_wireless_settings",
        description="⚙️ Update wireless network settings"
    )
    def update_network_wireless_settings(network_id: str, **kwargs):
        """Update wireless network settings."""
        try:
            result = meraki_client.dashboard.wireless.updateNetworkWirelessSettings(
                network_id, **kwargs
            )
            
            return f"✅ Wireless settings updated successfully!"
            
        except Exception as e:
            return f"Error updating wireless settings: {str(e)}"
    
    # Alternate Management Interface
    @app.tool(
        name="get_network_wireless_alternate_management_interface",
        description="🔧 Get alternate management interface settings"
    )
    def get_network_wireless_alternate_management_interface(network_id: str):
        """Get alternate management interface settings for wireless devices."""
        try:
            ami = meraki_client.dashboard.wireless.getNetworkWirelessAlternateManagementInterface(network_id)
            
            result = f"# 🔧 Alternate Management Interface\n\n"
            result += f"**Enabled**: {'✅' if ami.get('enabled') else '❌'}\n"
            
            if ami.get('enabled'):
                result += f"**VLAN ID**: {ami.get('vlanId', 'Not set')}\n"
                
                protocols = ami.get('protocols', [])
                if protocols:
                    result += f"**Protocols**: {', '.join(protocols)}\n"
                
                access_points = ami.get('accessPoints', [])
                if access_points:
                    result += f"**Configured APs**: {len(access_points)}\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving alternate management interface: {str(e)}"
    
    @app.tool(
        name="update_network_wireless_alternate_management_interface",
        description="🔧 Update alternate management interface"
    )
    def update_network_wireless_alternate_management_interface(network_id: str, **kwargs):
        """Update alternate management interface settings."""
        try:
            result = meraki_client.dashboard.wireless.updateNetworkWirelessAlternateManagementInterface(
                network_id, **kwargs
            )
            
            return f"✅ Alternate management interface updated successfully!"
            
        except Exception as e:
            return f"Error updating alternate management interface: {str(e)}"
    
    # Billing
    @app.tool(
        name="get_network_wireless_billing",
        description="💳 Get wireless billing settings"
    )
    def get_network_wireless_billing(network_id: str):
        """Get wireless billing configuration."""
        try:
            billing = meraki_client.dashboard.wireless.getNetworkWirelessBilling(network_id)
            
            result = f"# 💳 Wireless Billing Settings\n\n"
            
            if billing.get('currency'):
                result += f"**Currency**: {billing['currency']}\n"
            
            plans = billing.get('plans', [])
            if plans:
                result += f"\n**Billing Plans**: {len(plans)} configured\n\n"
                
                for plan in plans:
                    result += f"## Plan: {plan.get('name', 'Unnamed')}\n"
                    result += f"- ID: {plan.get('id')}\n"
                    result += f"- Price: {plan.get('price', 0)}\n"
                    result += f"- Time Limit: {plan.get('timeLimit', 'None')}\n"
                    result += f"- Bandwidth Limit: {plan.get('bandwidthLimit', 'None')}\n\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving billing settings: {str(e)}"
    
    @app.tool(
        name="update_network_wireless_billing",
        description="💳 Update wireless billing settings"
    )
    def update_network_wireless_billing(network_id: str, **kwargs):
        """Update wireless billing configuration."""
        try:
            result = meraki_client.dashboard.wireless.updateNetworkWirelessBilling(
                network_id, **kwargs
            )
            
            return f"✅ Billing settings updated successfully!"
            
        except Exception as e:
            return f"Error updating billing settings: {str(e)}"
    
    # SSID Specific Tools
    @app.tool(
        name="get_network_wireless_ssid_eap_override",
        description="🔐 Get RADIUS override settings for SSID"
    )
    def get_network_wireless_ssid_eap_override(network_id: str, number: str):
        """Get EAP override settings for an SSID."""
        try:
            eap = meraki_client.dashboard.wireless.getNetworkWirelessSsidEapOverride(
                network_id, number
            )
            
            result = f"# 🔐 EAP Override for SSID {number}\n\n"
            
            result += f"**Timeout**: {eap.get('timeout', 'Default')} seconds\n"
            result += f"**Max Retries**: {eap.get('maxRetries', 'Default')}\n"
            result += f"**Identity**: {eap.get('identity', 'Not set')}\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving EAP override settings: {str(e)}"
    
    @app.tool(
        name="update_network_wireless_ssid_eap_override",
        description="🔐 Update RADIUS override settings for SSID"
    )
    def update_network_wireless_ssid_eap_override(network_id: str, number: str, **kwargs):
        """Update EAP override settings for an SSID."""
        try:
            result = meraki_client.dashboard.wireless.updateNetworkWirelessSsidEapOverride(
                network_id, number, **kwargs
            )
            
            return f"✅ EAP override settings updated for SSID {number}!"
            
        except Exception as e:
            return f"Error updating EAP override settings: {str(e)}"
    
    @app.tool(
        name="get_network_wireless_ssid_firewall_l3_firewall_rules",
        description="🔥 Get Layer 3 firewall rules for SSID"
    )
    def get_network_wireless_ssid_firewall_l3_firewall_rules(network_id: str, number: str):
        """Get Layer 3 firewall rules for a specific SSID."""
        try:
            rules = meraki_client.dashboard.wireless.getNetworkWirelessSsidFirewallL3FirewallRules(
                network_id, number
            )
            
            result = f"# 🔥 L3 Firewall Rules for SSID {number}\n\n"
            
            if not rules or not rules.get('rules'):
                return result + "No firewall rules configured."
            
            for idx, rule in enumerate(rules.get('rules', []), 1):
                result += f"## Rule {idx}: {rule.get('comment', 'No comment')}\n"
                result += f"- Policy: {rule.get('policy')}\n"
                result += f"- Protocol: {rule.get('protocol')}\n"
                result += f"- Source: {rule.get('srcCidr')}\n"
                result += f"- Destination: {rule.get('destCidr')}\n"
                
                if rule.get('destPort'):
                    result += f"- Dest Port: {rule['destPort']}\n"
                
                result += "\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving L3 firewall rules: {str(e)}"
    
    @app.tool(
        name="update_network_wireless_ssid_firewall_l3_firewall_rules",
        description="🔥 Update Layer 3 firewall rules for SSID"
    )
    def update_network_wireless_ssid_firewall_l3_firewall_rules(network_id: str, number: str, rules: list):
        """Update Layer 3 firewall rules for a specific SSID."""
        try:
            result = meraki_client.dashboard.wireless.updateNetworkWirelessSsidFirewallL3FirewallRules(
                network_id, number, rules=rules
            )
            
            return f"✅ L3 firewall rules updated for SSID {number}!"
            
        except Exception as e:
            return f"Error updating L3 firewall rules: {str(e)}"
    
    @app.tool(
        name="get_network_wireless_ssid_firewall_l7_firewall_rules",
        description="🔥 Get Layer 7 firewall rules for SSID"
    )
    def get_network_wireless_ssid_firewall_l7_firewall_rules(network_id: str, number: str):
        """Get Layer 7 application firewall rules for a specific SSID."""
        try:
            rules = meraki_client.dashboard.wireless.getNetworkWirelessSsidFirewallL7FirewallRules(
                network_id, number
            )
            
            result = f"# 🔥 L7 Firewall Rules for SSID {number}\n\n"
            
            if not rules or not rules.get('rules'):
                return result + "No L7 firewall rules configured."
            
            for idx, rule in enumerate(rules.get('rules', []), 1):
                result += f"## Rule {idx}\n"
                result += f"- Policy: {rule.get('policy')}\n"
                result += f"- Type: {rule.get('type')}\n"
                
                if rule.get('value'):
                    result += f"- Value: {rule['value']}\n"
                
                result += "\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving L7 firewall rules: {str(e)}"
    
    @app.tool(
        name="update_network_wireless_ssid_firewall_l7_firewall_rules",
        description="🔥 Update Layer 7 firewall rules for SSID"
    )
    def update_network_wireless_ssid_firewall_l7_firewall_rules(network_id: str, number: str, rules: list):
        """Update Layer 7 application firewall rules for a specific SSID."""
        try:
            result = meraki_client.dashboard.wireless.updateNetworkWirelessSsidFirewallL7FirewallRules(
                network_id, number, rules=rules
            )
            
            return f"✅ L7 firewall rules updated for SSID {number}!"
            
        except Exception as e:
            return f"Error updating L7 firewall rules: {str(e)}"
    
    @app.tool(
        name="get_network_wireless_ssid_splash_settings",
        description="🎨 Get splash page settings for SSID"
    )
    def get_network_wireless_ssid_splash_settings(network_id: str, number: str):
        """Get splash page settings for a specific SSID."""
        try:
            splash = meraki_client.dashboard.wireless.getNetworkWirelessSsidSplashSettings(
                network_id, number
            )
            
            result = f"# 🎨 Splash Page Settings for SSID {number}\n\n"
            
            result += f"**Splash Page**: {splash.get('splashPage', 'None')}\n"
            
            if splash.get('splashUrl'):
                result += f"**Custom URL**: {splash['splashUrl']}\n"
            
            if splash.get('splashTimeout'):
                result += f"**Timeout**: {splash['splashTimeout']} seconds\n"
            
            if splash.get('welcomeMessage'):
                result += f"**Welcome Message**: {splash['welcomeMessage']}\n"
            
            if splash.get('splashLogo'):
                result += "**Custom Logo**: Configured\n"
            
            if splash.get('blockAllTrafficBeforeSignOn') is not None:
                result += f"**Block Traffic Before Sign-On**: {'✅' if splash['blockAllTrafficBeforeSignOn'] else '❌'}\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving splash settings: {str(e)}"
    
    @app.tool(
        name="update_network_wireless_ssid_splash_settings",
        description="🎨 Update splash page settings for SSID"
    )
    def update_network_wireless_ssid_splash_settings(network_id: str, number: str, **kwargs):
        """Update splash page settings for a specific SSID."""
        try:
            result = meraki_client.dashboard.wireless.updateNetworkWirelessSsidSplashSettings(
                network_id, number, **kwargs
            )
            
            return f"✅ Splash settings updated for SSID {number}!"
            
        except Exception as e:
            return f"Error updating splash settings: {str(e)}"
    
    @app.tool(
        name="get_network_wireless_ssid_hotspot20",
        description="📶 Get Hotspot 2.0 settings for SSID"
    )
    def get_network_wireless_ssid_hotspot20(network_id: str, number: str):
        """Get Hotspot 2.0 settings for a specific SSID."""
        try:
            hotspot = meraki_client.dashboard.wireless.getNetworkWirelessSsidHotspot20(
                network_id, number
            )
            
            result = f"# 📶 Hotspot 2.0 Settings for SSID {number}\n\n"
            
            result += f"**Enabled**: {'✅' if hotspot.get('enabled') else '❌'}\n"
            
            if hotspot.get('enabled'):
                if hotspot.get('operator'):
                    op = hotspot['operator']
                    result += f"\n**Operator Name**: {op.get('name', 'Not set')}\n"
                
                if hotspot.get('venue'):
                    venue = hotspot['venue']
                    result += f"\n**Venue Name**: {venue.get('name', 'Not set')}\n"
                    result += f"**Venue Type**: {venue.get('type', 'Not set')}\n"
                
                domains = hotspot.get('domains', [])
                if domains:
                    result += f"\n**Domains**: {', '.join(domains)}\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving Hotspot 2.0 settings: {str(e)}"
    
    @app.tool(
        name="update_network_wireless_ssid_hotspot20",
        description="📶 Update Hotspot 2.0 settings for SSID"
    )
    def update_network_wireless_ssid_hotspot20(network_id: str, number: str, **kwargs):
        """Update Hotspot 2.0 settings for a specific SSID."""
        try:
            result = meraki_client.dashboard.wireless.updateNetworkWirelessSsidHotspot20(
                network_id, number, **kwargs
            )
            
            return f"✅ Hotspot 2.0 settings updated for SSID {number}!"
            
        except Exception as e:
            return f"Error updating Hotspot 2.0 settings: {str(e)}"
    
    @app.tool(
        name="get_network_wireless_ssid_identity_psks",
        description="🔑 Get identity PSKs for SSID"
    )
    def get_network_wireless_ssid_identity_psks(network_id: str, number: str):
        """Get identity PSKs (individual passwords) for a specific SSID."""
        try:
            psks = meraki_client.dashboard.wireless.getNetworkWirelessSsidIdentityPsks(
                network_id, number
            )
            
            result = f"# 🔑 Identity PSKs for SSID {number}\n\n"
            
            if not psks:
                return result + "No identity PSKs configured."
            
            result += f"**Total PSKs**: {len(psks)}\n\n"
            
            for psk in psks[:20]:  # Show first 20
                result += f"## {psk.get('name', 'Unnamed')}\n"
                result += f"- ID: {psk.get('id')}\n"
                result += f"- Email: {psk.get('email', 'Not set')}\n"
                result += f"- Passphrase: {'Set' if psk.get('passphrase') else 'Not set'}\n"
                
                if psk.get('groupPolicyId'):
                    result += f"- Group Policy: {psk['groupPolicyId']}\n"
                
                result += "\n"
            
            if len(psks) > 20:
                result += f"... and {len(psks) - 20} more PSKs\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving identity PSKs: {str(e)}"
    
    @app.tool(
        name="create_network_wireless_ssid_identity_psk",
        description="🔑 Create a new identity PSK"
    )
    def create_network_wireless_ssid_identity_psk(network_id: str, number: str, name: str, passphrase: str, **kwargs):
        """Create a new identity PSK for a specific SSID."""
        try:
            psk = meraki_client.dashboard.wireless.createNetworkWirelessSsidIdentityPsk(
                network_id, number, name, passphrase, **kwargs
            )
            
            return f"✅ Identity PSK '{name}' created successfully!\n\nPSK ID: {psk.get('id')}"
            
        except Exception as e:
            return f"Error creating identity PSK: {str(e)}"
    
    @app.tool(
        name="update_network_wireless_ssid_identity_psk",
        description="🔑 Update an identity PSK"
    )
    def update_network_wireless_ssid_identity_psk(network_id: str, number: str, identityPskId: str, **kwargs):
        """Update an existing identity PSK."""
        try:
            result = meraki_client.dashboard.wireless.updateNetworkWirelessSsidIdentityPsk(
                network_id, number, identityPskId, **kwargs
            )
            
            return f"✅ Identity PSK {identityPskId} updated successfully!"
            
        except Exception as e:
            return f"Error updating identity PSK: {str(e)}"
    
    @app.tool(
        name="delete_network_wireless_ssid_identity_psk",
        description="🔑 Delete an identity PSK"
    )
    def delete_network_wireless_ssid_identity_psk(network_id: str, number: str, identityPskId: str):
        """Delete an identity PSK."""
        try:
            meraki_client.dashboard.wireless.deleteNetworkWirelessSsidIdentityPsk(
                network_id, number, identityPskId
            )
            
            return f"✅ Identity PSK {identityPskId} deleted successfully!"
            
        except Exception as e:
            return f"Error deleting identity PSK: {str(e)}"
    
    @app.tool(
        name="get_network_wireless_ssid_schedules",
        description="📅 Get SSID schedules"
    )
    def get_network_wireless_ssid_schedules(network_id: str, number: str):
        """Get scheduling settings for a specific SSID."""
        try:
            schedules = meraki_client.dashboard.wireless.getNetworkWirelessSsidSchedules(
                network_id, number
            )
            
            result = f"# 📅 SSID {number} Schedules\n\n"
            
            result += f"**Scheduling Enabled**: {'✅' if schedules.get('enabled') else '❌'}\n"
            
            if schedules.get('enabled') and schedules.get('ranges'):
                result += "\n## Schedule Ranges\n\n"
                
                for range_item in schedules['ranges']:
                    result += f"- **{range_item.get('day', 'Unknown')}**\n"
                    result += f"  - Start: {range_item.get('startTime', 'Unknown')}\n"
                    result += f"  - End: {range_item.get('endTime', 'Unknown')}\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving SSID schedules: {str(e)}"
    
    @app.tool(
        name="update_network_wireless_ssid_schedules",
        description="📅 Update SSID schedules"
    )
    def update_network_wireless_ssid_schedules(network_id: str, number: str, **kwargs):
        """Update scheduling settings for a specific SSID."""
        try:
            result = meraki_client.dashboard.wireless.updateNetworkWirelessSsidSchedules(
                network_id, number, **kwargs
            )
            
            return f"✅ SSID {number} schedules updated successfully!"
            
        except Exception as e:
            return f"Error updating SSID schedules: {str(e)}"
    
    @app.tool(
        name="get_network_wireless_ssid_vpn",
        description="🔐 Get SSID VPN settings"
    )
    def get_network_wireless_ssid_vpn(network_id: str, number: str):
        """Get VPN settings for a specific SSID."""
        try:
            vpn = meraki_client.dashboard.wireless.getNetworkWirelessSsidVpn(
                network_id, number
            )
            
            result = f"# 🔐 VPN Settings for SSID {number}\n\n"
            
            concentrator = vpn.get('concentrator', {})
            if concentrator:
                result += f"**Network ID**: {concentrator.get('networkId', 'Not set')}\n"
                result += f"**VLAN ID**: {concentrator.get('vlanId', 'Not set')}\n"
            
            split_tunnel = vpn.get('splitTunnel', {})
            if split_tunnel:
                result += f"\n**Split Tunnel Enabled**: {'✅' if split_tunnel.get('enabled') else '❌'}\n"
                
                rules = split_tunnel.get('rules', [])
                if rules:
                    result += "\n**Split Tunnel Rules**:\n"
                    for rule in rules:
                        result += f"- {rule.get('destCidr')} ({rule.get('policy')})\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving VPN settings: {str(e)}"
    
    @app.tool(
        name="update_network_wireless_ssid_vpn",
        description="🔐 Update SSID VPN settings"
    )
    def update_network_wireless_ssid_vpn(network_id: str, number: str, concentrator: dict, **kwargs):
        """Update VPN settings for a specific SSID."""
        try:
            result = meraki_client.dashboard.wireless.updateNetworkWirelessSsidVpn(
                network_id, number, concentrator=concentrator, **kwargs
            )
            
            return f"✅ VPN settings updated for SSID {number}!"
            
        except Exception as e:
            return f"Error updating VPN settings: {str(e)}"
    
    @app.tool(
        name="get_network_wireless_ssid_device_type_group_policies",
        description="📱 Get device type group policies for SSID"
    )
    def get_network_wireless_ssid_device_type_group_policies(network_id: str, number: str):
        """Get device type group policy mappings for a specific SSID."""
        try:
            policies = meraki_client.dashboard.wireless.getNetworkWirelessSsidDeviceTypeGroupPolicies(
                network_id, number
            )
            
            result = f"# 📱 Device Type Group Policies for SSID {number}\n\n"
            
            result += f"**Enabled**: {'✅' if policies.get('enabled') else '❌'}\n"
            
            device_policies = policies.get('deviceTypePolicies', [])
            if device_policies:
                result += f"\n**Device Policies**: {len(device_policies)} configured\n\n"
                
                for policy in device_policies:
                    result += f"- **{policy.get('deviceType', 'Unknown')}**\n"
                    result += f"  - Policy: {policy.get('devicePolicy', 'Unknown')}\n"
                    result += f"  - Group Policy ID: {policy.get('groupPolicyId', 'Not set')}\n\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving device type policies: {str(e)}"
    
    @app.tool(
        name="update_network_wireless_ssid_device_type_group_policies",
        description="📱 Update device type group policies for SSID"
    )
    def update_network_wireless_ssid_device_type_group_policies(network_id: str, number: str, **kwargs):
        """Update device type group policy mappings for a specific SSID."""
        try:
            result = meraki_client.dashboard.wireless.updateNetworkWirelessSsidDeviceTypeGroupPolicies(
                network_id, number, **kwargs
            )
            
            return f"✅ Device type policies updated for SSID {number}!"
            
        except Exception as e:
            return f"Error updating device type policies: {str(e)}"
    
    @app.tool(
        name="get_network_wireless_ssid_bonjour_forwarding",
        description="🍎 Get Bonjour forwarding settings for SSID"
    )
    def get_network_wireless_ssid_bonjour_forwarding(network_id: str, number: str):
        """Get Bonjour forwarding settings for a specific SSID."""
        try:
            bonjour = meraki_client.dashboard.wireless.getNetworkWirelessSsidBonjourForwarding(
                network_id, number
            )
            
            result = f"# 🍎 Bonjour Forwarding for SSID {number}\n\n"
            
            result += f"**Enabled**: {'✅' if bonjour.get('enabled') else '❌'}\n"
            
            if bonjour.get('enabled'):
                rules = bonjour.get('rules', [])
                if rules:
                    result += f"\n**Rules**: {len(rules)} configured\n\n"
                    
                    for rule in rules:
                        result += f"- **{rule.get('description', 'No description')}**\n"
                        result += f"  - VLAN ID: {rule.get('vlanId')}\n"
                        result += f"  - Services: {', '.join(rule.get('services', []))}\n\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving Bonjour forwarding settings: {str(e)}"
    
    @app.tool(
        name="update_network_wireless_ssid_bonjour_forwarding",
        description="🍎 Update Bonjour forwarding settings for SSID"
    )
    def update_network_wireless_ssid_bonjour_forwarding(network_id: str, number: str, **kwargs):
        """Update Bonjour forwarding settings for a specific SSID."""
        try:
            result = meraki_client.dashboard.wireless.updateNetworkWirelessSsidBonjourForwarding(
                network_id, number, **kwargs
            )
            
            return f"✅ Bonjour forwarding updated for SSID {number}!"
            
        except Exception as e:
            return f"Error updating Bonjour forwarding: {str(e)}"
    
    # Traffic Shaping
    @app.tool(
        name="get_network_wireless_ssid_traffic_shaping_rules",
        description="🚦 Get traffic shaping rules for SSID"
    )
    def get_network_wireless_ssid_traffic_shaping_rules(network_id: str, number: str):
        """Get traffic shaping rules for a specific SSID."""
        try:
            rules = meraki_client.dashboard.wireless.getNetworkWirelessSsidTrafficShapingRules(
                network_id, number
            )
            
            result = f"# 🚦 Traffic Shaping for SSID {number}\n\n"
            
            result += f"**Enabled**: {'✅' if rules.get('trafficShapingEnabled') else '❌'}\n"
            
            if rules.get('defaultRulesEnabled'):
                result += "**Default Rules**: Enabled\n"
            
            # Per-client bandwidth limits
            if rules.get('perClientBandwidthLimits'):
                limits = rules['perClientBandwidthLimits']
                result += f"\n**Per-Client Limits**:\n"
                result += f"- Download: {limits.get('limitDown', 'Unlimited')} Mbps\n"
                result += f"- Upload: {limits.get('limitUp', 'Unlimited')} Mbps\n"
            
            # Application rules
            app_rules = rules.get('rules', [])
            if app_rules:
                result += f"\n**Application Rules**: {len(app_rules)} configured\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving traffic shaping rules: {str(e)}"
    
    @app.tool(
        name="update_network_wireless_ssid_traffic_shaping_rules",
        description="🚦 Update traffic shaping rules for SSID"
    )
    def update_network_wireless_ssid_traffic_shaping_rules(network_id: str, number: str, **kwargs):
        """Update traffic shaping rules for a specific SSID."""
        try:
            result = meraki_client.dashboard.wireless.updateNetworkWirelessSsidTrafficShapingRules(
                network_id, number, **kwargs
            )
            
            return f"✅ Traffic shaping rules updated for SSID {number}!"
            
        except Exception as e:
            return f"Error updating traffic shaping rules: {str(e)}"
    
    # Organization-wide Wireless Functions
    @app.tool(
        name="get_organization_wireless_devices_channel_utilization_by_device",
        description="📡 Get channel utilization by device (org-wide)"
    )
    def get_organization_wireless_devices_channel_utilization_by_device(organization_id: str, **kwargs):
        """Get channel utilization for all wireless devices in the organization."""
        try:
            utilization = meraki_client.dashboard.wireless.getOrganizationWirelessDevicesChannelUtilizationByDevice(
                organization_id, **kwargs
            )
            
            if not utilization:
                return f"No channel utilization data available for organization {organization_id}."
            
            result = f"# 📡 Organization-Wide Channel Utilization\n\n"
            
            high_util_devices = []
            
            for device in utilization:
                name = device.get('name', 'Unknown')
                serial = device.get('serial')
                
                by_band = device.get('byBand', [])
                for band_data in by_band:
                    band = band_data.get('band')
                    total_util = band_data.get('total', {}).get('percentage', 0)
                    
                    if total_util > 70:
                        high_util_devices.append({
                            'name': name,
                            'serial': serial,
                            'band': band,
                            'utilization': total_util
                        })
            
            if high_util_devices:
                result += f"## ⚠️ High Utilization Devices ({len(high_util_devices)})\n\n"
                
                for device in high_util_devices:
                    result += f"- **{device['name']}** ({device['serial']})\n"
                    result += f"  - Band: {device['band']} GHz\n"
                    result += f"  - Utilization: {device['utilization']}%\n\n"
            else:
                result += "✅ All devices have normal channel utilization.\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving channel utilization: {str(e)}"
    
    @app.tool(
        name="get_organization_wireless_devices_channel_utilization_by_network",
        description="📡 Get channel utilization by network (org-wide)"
    )
    def get_organization_wireless_devices_channel_utilization_by_network(organization_id: str, **kwargs):
        """Get channel utilization summary by network."""
        try:
            utilization = meraki_client.dashboard.wireless.getOrganizationWirelessDevicesChannelUtilizationByNetwork(
                organization_id, **kwargs
            )
            
            if not utilization:
                return f"No channel utilization data available for organization {organization_id}."
            
            result = f"# 📡 Channel Utilization by Network\n\n"
            
            for network in utilization:
                network_name = network.get('name', 'Unknown')
                network_id = network.get('networkId')
                
                result += f"## {network_name}\n"
                result += f"Network ID: {network_id}\n\n"
                
                by_band = network.get('byBand', [])
                for band_data in by_band:
                    band = band_data.get('band')
                    wifi_util = band_data.get('wifi', {}).get('percentage', 0)
                    non_wifi_util = band_data.get('nonWifi', {}).get('percentage', 0)
                    total_util = band_data.get('total', {}).get('percentage', 0)
                    
                    # Status
                    if total_util > 80:
                        status = '🔴 Critical'
                    elif total_util > 60:
                        status = '🟠 High'
                    elif total_util > 40:
                        status = '🟡 Moderate'
                    else:
                        status = '🟢 Good'
                    
                    result += f"- **{band} GHz Band** - {status}\n"
                    result += f"  - WiFi: {wifi_util}%\n"
                    result += f"  - Interference: {non_wifi_util}%\n"
                    result += f"  - Total: {total_util}%\n\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving network utilization: {str(e)}"
    
    @app.tool(
        name="get_org_wireless_channel_util_history_by_device",
        description="📡 Get detailed channel utilization history by device"
    )
    def get_organization_wireless_devices_channel_utilization_history_by_device_by_interval(
        organization_id: str, **kwargs
    ):
        """Get detailed channel utilization history with intervals."""
        try:
            history = meraki_client.dashboard.wireless.getOrganizationWirelessDevicesChannelUtilizationHistoryByDeviceByInterval(
                organization_id, **kwargs
            )
            
            if not history:
                return f"No utilization history available for organization {organization_id}."
            
            result = f"# 📡 Channel Utilization History (Detailed)\n\n"
            
            # Show recent data for first few devices
            for device in history[:5]:
                name = device.get('name', 'Unknown')
                serial = device.get('serial')
                
                result += f"## {name} ({serial})\n\n"
                
                by_band = device.get('byBand', [])
                for band_data in by_band[:2]:  # First 2 bands
                    band = band_data.get('band')
                    result += f"### {band} GHz Band\n"
                    
                    by_interval = band_data.get('byInterval', [])
                    for interval in by_interval[-5:]:  # Last 5 intervals
                        time = interval.get('startTs', 'Unknown')
                        total = interval.get('total', {}).get('percentage', 0)
                        
                        # Visual bar
                        bar_length = int(total / 5)
                        bar = '█' * bar_length + '░' * (20 - bar_length)
                        
                        result += f"{time[:16]}: [{bar}] {total}%\n"
                    
                    result += "\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving utilization history: {str(e)}"
    
    @app.tool(
        name="get_org_wireless_channel_util_history_by_network",
        description="📡 Get network channel utilization history by interval"
    )
    def get_organization_wireless_devices_channel_utilization_history_by_network_by_interval(
        organization_id: str, **kwargs
    ):
        """Get channel utilization history grouped by network."""
        try:
            history = meraki_client.dashboard.wireless.getOrganizationWirelessDevicesChannelUtilizationHistoryByNetworkByInterval(
                organization_id, **kwargs
            )
            
            if not history:
                return f"No utilization history available for organization {organization_id}."
            
            result = f"# 📡 Network Channel Utilization Trends\n\n"
            
            for network in history[:10]:  # First 10 networks
                network_name = network.get('name', 'Unknown')
                
                result += f"## {network_name}\n"
                
                by_band = network.get('byBand', [])
                for band_data in by_band:
                    band = band_data.get('band')
                    
                    by_interval = band_data.get('byInterval', [])
                    if by_interval:
                        # Get trend
                        recent_utils = [i.get('total', {}).get('percentage', 0) for i in by_interval[-5:]]
                        if len(recent_utils) >= 2:
                            trend = recent_utils[-1] - recent_utils[0]
                            if trend > 10:
                                trend_icon = '📈 Increasing'
                            elif trend < -10:
                                trend_icon = '📉 Decreasing'
                            else:
                                trend_icon = '➡️ Stable'
                            
                            current = recent_utils[-1]
                            result += f"- {band} GHz: {current}% {trend_icon}\n"
                
                result += "\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving network utilization history: {str(e)}"
    
    @app.tool(
        name="get_organization_wireless_devices_packet_loss_by_client",
        description="📉 Get packet loss statistics by client"
    )
    def get_organization_wireless_devices_packet_loss_by_client(organization_id: str, **kwargs):
        """Get packet loss statistics for wireless clients."""
        try:
            packet_loss = meraki_client.dashboard.wireless.getOrganizationWirelessDevicesPacketLossByClient(
                organization_id, **kwargs
            )
            
            if not packet_loss:
                return f"No packet loss data available for organization {organization_id}."
            
            result = f"# 📉 Packet Loss by Client\n\n"
            
            # Categorize clients
            high_loss_clients = []
            moderate_loss_clients = []
            
            for client in packet_loss:
                client_id = client.get('clientId')
                mac = client.get('mac')
                name = client.get('name', 'Unknown')
                
                # Get packet loss percentages
                upstream = client.get('upstream', {})
                downstream = client.get('downstream', {})
                
                up_loss = upstream.get('lossPercentage', 0)
                down_loss = downstream.get('lossPercentage', 0)
                
                max_loss = max(up_loss, down_loss)
                
                if max_loss > 5:
                    high_loss_clients.append({
                        'name': name,
                        'mac': mac,
                        'up_loss': up_loss,
                        'down_loss': down_loss
                    })
                elif max_loss > 1:
                    moderate_loss_clients.append({
                        'name': name,
                        'mac': mac,
                        'up_loss': up_loss,
                        'down_loss': down_loss
                    })
            
            if high_loss_clients:
                result += f"## 🔴 High Packet Loss Clients ({len(high_loss_clients)})\n\n"
                for client in high_loss_clients[:10]:
                    result += f"- **{client['name']}** ({client['mac']})\n"
                    result += f"  - Upstream Loss: {client['up_loss']:.1f}%\n"
                    result += f"  - Downstream Loss: {client['down_loss']:.1f}%\n\n"
            
            if moderate_loss_clients:
                result += f"## 🟡 Moderate Packet Loss Clients ({len(moderate_loss_clients)})\n\n"
                for client in moderate_loss_clients[:5]:
                    result += f"- **{client['name']}** ({client['mac']})\n"
                    result += f"  - Upstream Loss: {client['up_loss']:.1f}%\n"
                    result += f"  - Downstream Loss: {client['down_loss']:.1f}%\n\n"
            
            if not high_loss_clients and not moderate_loss_clients:
                result += "✅ No significant packet loss detected for any clients.\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving packet loss data: {str(e)}"
    
    @app.tool(
        name="get_organization_wireless_devices_packet_loss_by_device",
        description="📉 Get packet loss statistics by device"
    )
    def get_organization_wireless_devices_packet_loss_by_device(organization_id: str, **kwargs):
        """Get packet loss statistics for wireless devices."""
        try:
            packet_loss = meraki_client.dashboard.wireless.getOrganizationWirelessDevicesPacketLossByDevice(
                organization_id, **kwargs
            )
            
            if not packet_loss:
                return f"No packet loss data available for organization {organization_id}."
            
            result = f"# 📉 Packet Loss by Device\n\n"
            
            problematic_devices = []
            
            for device in packet_loss:
                name = device.get('name', 'Unknown')
                serial = device.get('serial')
                network = device.get('network', {})
                
                # Get packet loss percentages
                upstream = device.get('upstream', {})
                downstream = device.get('downstream', {})
                
                up_loss = upstream.get('lossPercentage', 0)
                down_loss = downstream.get('lossPercentage', 0)
                
                if up_loss > 1 or down_loss > 1:
                    problematic_devices.append({
                        'name': name,
                        'serial': serial,
                        'network': network.get('name', 'Unknown'),
                        'up_loss': up_loss,
                        'down_loss': down_loss
                    })
            
            if problematic_devices:
                result += f"## ⚠️ Devices with Packet Loss ({len(problematic_devices)})\n\n"
                
                for device in problematic_devices:
                    result += f"### {device['name']} ({device['serial']})\n"
                    result += f"- Network: {device['network']}\n"
                    result += f"- Upstream Loss: {device['up_loss']:.1f}%\n"
                    result += f"- Downstream Loss: {device['down_loss']:.1f}%\n\n"
            else:
                result += "✅ No significant packet loss detected on any devices.\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving device packet loss data: {str(e)}"
    
    @app.tool(
        name="get_organization_wireless_devices_packet_loss_by_network",
        description="📉 Get packet loss statistics by network"
    )
    def get_organization_wireless_devices_packet_loss_by_network(organization_id: str, **kwargs):
        """Get packet loss statistics aggregated by network."""
        try:
            packet_loss = meraki_client.dashboard.wireless.getOrganizationWirelessDevicesPacketLossByNetwork(
                organization_id, **kwargs
            )
            
            if not packet_loss:
                return f"No packet loss data available for organization {organization_id}."
            
            result = f"# 📉 Packet Loss by Network\n\n"
            
            # Sort networks by packet loss
            networks_with_loss = []
            
            for network in packet_loss:
                name = network.get('name', 'Unknown')
                network_id = network.get('networkId')
                
                upstream = network.get('upstream', {})
                downstream = network.get('downstream', {})
                
                up_loss = upstream.get('lossPercentage', 0)
                down_loss = downstream.get('lossPercentage', 0)
                
                avg_loss = (up_loss + down_loss) / 2
                
                if avg_loss > 0.1:
                    networks_with_loss.append({
                        'name': name,
                        'id': network_id,
                        'up_loss': up_loss,
                        'down_loss': down_loss,
                        'avg_loss': avg_loss
                    })
            
            # Sort by average loss
            networks_with_loss.sort(key=lambda x: x['avg_loss'], reverse=True)
            
            if networks_with_loss:
                result += "## Networks Ranked by Packet Loss\n\n"
                
                for idx, network in enumerate(networks_with_loss[:20], 1):
                    # Status indicator
                    if network['avg_loss'] > 5:
                        status = '🔴'
                    elif network['avg_loss'] > 2:
                        status = '🟠'
                    elif network['avg_loss'] > 0.5:
                        status = '🟡'
                    else:
                        status = '🟢'
                    
                    result += f"{idx}. {status} **{network['name']}**\n"
                    result += f"   - Average Loss: {network['avg_loss']:.2f}%\n"
                    result += f"   - Upstream: {network['up_loss']:.2f}%\n"
                    result += f"   - Downstream: {network['down_loss']:.2f}%\n\n"
            else:
                result += "✅ Excellent! No measurable packet loss across any networks.\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving network packet loss data: {str(e)}"
    
    # Ethernet Over Power (EoP)
    @app.tool(
        name="get_network_wireless_ethernet_ports_profiles",
        description="🔌 Get Ethernet port profiles for wireless devices"
    )
    def get_network_wireless_ethernet_ports_profiles(network_id: str):
        """Get Ethernet port profiles for wireless devices."""
        try:
            profiles = meraki_client.dashboard.wireless.getNetworkWirelessEthernetPortsProfiles(network_id)
            
            if not profiles:
                return f"No Ethernet port profiles found for network {network_id}."
            
            result = f"# 🔌 Ethernet Port Profiles\n\n"
            
            for profile in profiles:
                result += f"## {profile.get('name', 'Unnamed Profile')}\n"
                result += f"- **ID**: {profile.get('profileId')}\n"
                result += f"- **Default**: {'✅' if profile.get('isDefault') else '❌'}\n"
                
                ports = profile.get('ports', [])
                if ports:
                    result += f"- **Ports**: {len(ports)} configured\n"
                    
                    for port in ports:
                        result += f"\n  ### Port {port.get('name', 'Unknown')}\n"
                        result += f"  - Enabled: {'✅' if port.get('enabled') else '❌'}\n"
                        
                        if port.get('vlanId'):
                            result += f"  - VLAN: {port['vlanId']}\n"
                        
                        if port.get('poeEnabled') is not None:
                            result += f"  - PoE: {'✅' if port['poeEnabled'] else '❌'}\n"
                
                result += "\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving Ethernet port profiles: {str(e)}"
    
    @app.tool(
        name="create_network_wireless_ethernet_ports_profile",
        description="🔌 Create Ethernet port profile"
    )
    def create_network_wireless_ethernet_ports_profile(network_id: str, name: str, ports: list, **kwargs):
        """Create a new Ethernet port profile for wireless devices."""
        try:
            profile = meraki_client.dashboard.wireless.createNetworkWirelessEthernetPortsProfile(
                network_id, name, ports, **kwargs
            )
            
            return f"✅ Ethernet port profile '{name}' created successfully!\n\nProfile ID: {profile.get('profileId')}"
            
        except Exception as e:
            return f"Error creating Ethernet port profile: {str(e)}"
    
    @app.tool(
        name="update_network_wireless_ethernet_ports_profile",
        description="🔌 Update Ethernet port profile"
    )
    def update_network_wireless_ethernet_ports_profile(network_id: str, profileId: str, **kwargs):
        """Update an existing Ethernet port profile."""
        try:
            result = meraki_client.dashboard.wireless.updateNetworkWirelessEthernetPortsProfile(
                network_id, profileId, **kwargs
            )
            
            return f"✅ Ethernet port profile {profileId} updated successfully!"
            
        except Exception as e:
            return f"Error updating Ethernet port profile: {str(e)}"
    
    @app.tool(
        name="delete_network_wireless_ethernet_ports_profile",
        description="🔌 Delete Ethernet port profile"
    )
    def delete_network_wireless_ethernet_ports_profile(network_id: str, profileId: str):
        """Delete an Ethernet port profile."""
        try:
            meraki_client.dashboard.wireless.deleteNetworkWirelessEthernetPortsProfile(
                network_id, profileId
            )
            
            return f"✅ Ethernet port profile {profileId} deleted successfully!"
            
        except Exception as e:
            return f"Error deleting Ethernet port profile: {str(e)}"
    
    @app.tool(
        name="assign_network_wireless_ethernet_ports_profiles",
        description="🔌 Assign Ethernet profiles to APs"
    )
    def assign_network_wireless_ethernet_ports_profiles(network_id: str, serials: list, profileId: str):
        """Assign an Ethernet port profile to specific access points."""
        try:
            result = meraki_client.dashboard.wireless.assignNetworkWirelessEthernetPortsProfiles(
                network_id, serials, profileId
            )
            
            return f"✅ Ethernet profile {profileId} assigned to {len(serials)} access points!"
            
        except Exception as e:
            return f"Error assigning Ethernet profiles: {str(e)}"
    
    # Electronic Shelf Labels
    @app.tool(
        name="get_network_wireless_electronic_shelf_label",
        description="🏷️ Get electronic shelf label settings"
    )
    def get_network_wireless_electronic_shelf_label(network_id: str):
        """Get electronic shelf label (ESL) settings."""
        try:
            esl = meraki_client.dashboard.wireless.getNetworkWirelessElectronicShelfLabel(network_id)
            
            result = f"# 🏷️ Electronic Shelf Label Settings\n\n"
            
            result += f"**Enabled**: {'✅' if esl.get('enabled') else '❌'}\n"
            
            if esl.get('hostname'):
                result += f"**Hostname**: {esl['hostname']}\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving ESL settings: {str(e)}"
    
    @app.tool(
        name="update_network_wireless_electronic_shelf_label",
        description="🏷️ Update electronic shelf label settings"
    )
    def update_network_wireless_electronic_shelf_label(network_id: str, **kwargs):
        """Update electronic shelf label (ESL) settings."""
        try:
            result = meraki_client.dashboard.wireless.updateNetworkWirelessElectronicShelfLabel(
                network_id, **kwargs
            )
            
            return f"✅ Electronic shelf label settings updated successfully!"
            
        except Exception as e:
            return f"Error updating ESL settings: {str(e)}"
    
    # Bluetooth Clients
    @app.tool(
        name="get_network_wireless_bluetooth_clients",
        description="📱 Get Bluetooth clients"
    )
    def get_network_wireless_bluetooth_clients(network_id: str, **kwargs):
        """Get Bluetooth clients detected in the network."""
        try:
            clients = meraki_client.dashboard.wireless.getNetworkWirelessBluetoothClients(
                network_id, **kwargs
            )
            
            if not clients:
                return f"No Bluetooth clients found in network {network_id}."
            
            result = f"# 📱 Bluetooth Clients\n\n"
            result += f"**Total Clients**: {len(clients)}\n\n"
            
            # Group by manufacturer
            by_manufacturer = {}
            for client in clients:
                manufacturer = client.get('manufacturer', 'Unknown')
                if manufacturer not in by_manufacturer:
                    by_manufacturer[manufacturer] = []
                by_manufacturer[manufacturer].append(client)
            
            # Show top manufacturers
            for manufacturer, devices in sorted(by_manufacturer.items(), key=lambda x: len(x[1]), reverse=True)[:5]:
                result += f"## {manufacturer} ({len(devices)} devices)\n"
                
                for device in devices[:5]:  # Show first 5 of each
                    result += f"- **{device.get('name', 'Unknown')}**\n"
                    result += f"  - MAC: {device.get('mac')}\n"
                    result += f"  - RSSI: {device.get('rssi')} dBm\n"
                    result += f"  - Last Seen: {device.get('lastSeen')}\n\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving Bluetooth clients: {str(e)}"
    
    # Client Health Scores
    @app.tool(
        name="get_network_wireless_clients_health_scores",
        description="🏥 Get health scores for wireless clients"
    )
    def get_network_wireless_clients_health_scores(network_id: str, **kwargs):
        """Get health scores for wireless clients."""
        try:
            scores = meraki_client.dashboard.wireless.getNetworkWirelessClientsHealthScores(
                network_id, **kwargs
            )
            
            if not scores:
                return f"No client health scores available for network {network_id}."
            
            result = f"# 🏥 Wireless Client Health Scores\n\n"
            result += f"**Total Clients**: {len(scores)}\n\n"
            
            # Categorize by health
            excellent = []
            good = []
            fair = []
            poor = []
            
            for client in scores:
                mac = client.get('mac')
                performance = client.get('performance', {})
                
                # Get latest score
                latest_score = performance.get('latest', 0)
                
                if latest_score >= 90:
                    excellent.append((mac, latest_score))
                elif latest_score >= 70:
                    good.append((mac, latest_score))
                elif latest_score >= 50:
                    fair.append((mac, latest_score))
                else:
                    poor.append((mac, latest_score))
            
            # Summary
            result += "## Health Distribution\n\n"
            result += f"- 🟢 Excellent (90-100): {len(excellent)} clients\n"
            result += f"- 🟡 Good (70-89): {len(good)} clients\n"
            result += f"- 🟠 Fair (50-69): {len(fair)} clients\n"
            result += f"- 🔴 Poor (0-49): {len(poor)} clients\n\n"
            
            # Show poor performers
            if poor:
                result += "## ⚠️ Clients with Poor Health\n\n"
                for mac, score in poor[:10]:
                    result += f"- {mac}: {score}%\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving client health scores: {str(e)}"
    
    # Client Onboarding
    @app.tool(
        name="get_network_wireless_clients_onboarding_history",
        description="🚀 Get client onboarding history"
    )
    def get_network_wireless_clients_onboarding_history(network_id: str, **kwargs):
        """Get onboarding history for wireless clients."""
        try:
            history = meraki_client.dashboard.wireless.getNetworkWirelessClientsOnboardingHistory(
                network_id, **kwargs
            )
            
            if not history:
                return f"No onboarding history available for network {network_id}."
            
            result = f"# 🚀 Client Onboarding History\n\n"
            
            # Analyze onboarding times
            times = []
            failures = []
            
            for entry in history:
                onboarding_time = entry.get('onboardingTime', 0)
                if onboarding_time > 0:
                    times.append(onboarding_time)
                else:
                    failures.append(entry)
            
            if times:
                avg_time = sum(times) / len(times)
                result += f"**Average Onboarding Time**: {avg_time:.1f} seconds\n"
                result += f"**Fastest**: {min(times)} seconds\n"
                result += f"**Slowest**: {max(times)} seconds\n"
                result += f"**Failed Attempts**: {len(failures)}\n\n"
            
            # Recent onboarding events
            result += "## Recent Onboarding Events\n\n"
            for entry in history[:10]:
                time = entry.get('timestamp', 'Unknown')
                mac = entry.get('mac', 'Unknown')
                onboarding_time = entry.get('onboardingTime', 0)
                
                if onboarding_time > 0:
                    result += f"- **{time[:16]}** - {mac}\n"
                    result += f"  - Time: {onboarding_time} seconds\n"
                    result += f"  - SSID: {entry.get('ssid', 'Unknown')}\n\n"
                else:
                    result += f"- **{time[:16]}** - {mac} ❌ FAILED\n\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving onboarding history: {str(e)}"
    
    # Usage Utilities
    @app.tool(
        name="get_network_wireless_clients_connection_events",
        description="📡 Get wireless client connection events"
    )
    def get_network_wireless_clients_connection_events(network_id: str, clientId: str, **kwargs):
        """Get connection events for a specific wireless client."""
        try:
            events = meraki_client.dashboard.wireless.getNetworkWirelessClientsConnectionEvents(
                network_id, clientId, **kwargs
            )
            
            if not events:
                return f"No connection events found for client {clientId}."
            
            result = f"# 📡 Connection Events for Client {clientId}\n\n"
            result += f"**Total Events**: {len(events)}\n\n"
            
            # Count event types
            event_types = {}
            for event in events:
                event_type = event.get('type', 'Unknown')
                event_types[event_type] = event_types.get(event_type, 0) + 1
            
            result += "## Event Summary\n\n"
            for event_type, count in sorted(event_types.items(), key=lambda x: x[1], reverse=True):
                result += f"- {event_type}: {count} events\n"
            
            result += "\n## Recent Events\n\n"
            for event in events[:20]:
                time = event.get('occurredAt', 'Unknown')
                event_type = event.get('type', 'Unknown')
                ssid = event.get('ssid', 'Unknown')
                
                # Icon based on event type
                if 'success' in event_type.lower() or 'connect' in event_type.lower():
                    icon = '✅'
                elif 'fail' in event_type.lower() or 'disconnect' in event_type.lower():
                    icon = '❌'
                else:
                    icon = '📍'
                
                result += f"{icon} **{time[:16]}** - {event_type}\n"
                result += f"   - SSID: {ssid}\n"
                
                if event.get('eventData'):
                    result += f"   - Details: {event['eventData']}\n"
                
                result += "\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving connection events: {str(e)}"
    
    @app.tool(
        name="get_network_wireless_ssid_connection_stats",
        description="📊 Get connection stats for a specific SSID"
    )
    def get_network_wireless_ssid_connection_stats(network_id: str, number: str, **kwargs):
        """Get connection statistics for a specific SSID."""
        try:
            stats = meraki_client.dashboard.wireless.getNetworkWirelessSsidConnectionStats(
                network_id, number, **kwargs
            )
            
            if not stats:
                return f"No connection statistics available for SSID {number}."
            
            result = f"# 📊 Connection Stats for SSID {number}\n\n"
            
            # Overall stats
            total_attempts = stats.get('totalAttempts', 0)
            successful = stats.get('successfulConnections', 0)
            
            if total_attempts > 0:
                success_rate = (successful / total_attempts) * 100
                result += f"**Success Rate**: {success_rate:.1f}%\n"
                result += f"**Total Attempts**: {total_attempts}\n"
                result += f"**Successful**: {successful}\n"
                result += f"**Failed**: {total_attempts - successful}\n\n"
                
                # Connection funnel
                result += "## Connection Funnel\n\n"
                
                assoc = stats.get('associationAttempts', 0)
                auth = stats.get('authenticationAttempts', 0)
                dhcp = stats.get('dhcpAttempts', 0)
                dns = stats.get('dnsAttempts', 0)
                
                if assoc > 0:
                    result += f"1. Association: {assoc} attempts\n"
                    result += f"2. Authentication: {auth} ({(auth/assoc*100):.1f}% of assoc)\n"
                    result += f"3. DHCP: {dhcp} ({(dhcp/auth*100 if auth > 0 else 0):.1f}% of auth)\n"
                    result += f"4. DNS: {dns} ({(dns/dhcp*100 if dhcp > 0 else 0):.1f}% of DHCP)\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving SSID connection stats: {str(e)}"
    
    # Helper/Utility Functions
    @app.tool(
        name="get_network_wireless_passwords",
        description="🔑 Get WiFi passwords for all SSIDs"
    )
    def get_network_wireless_passwords(network_id: str):
        """Get WiFi passwords/PSK for all SSIDs in a network."""
        try:
            ssids = meraki_client.dashboard.wireless.getNetworkWirelessSsids(network_id)
            
            if not ssids:
                return f"No wireless SSIDs found for network {network_id}."
            
            result = f"# 🔑 WiFi Passwords for Network {network_id}\n\n"
            
            for ssid in ssids:
                if not ssid.get('enabled'):
                    continue
                    
                ssid_name = ssid.get('name', 'Unnamed')
                ssid_number = ssid.get('number', 'Unknown')
                auth_mode = ssid.get('authMode', 'Unknown')
                
                result += f"## SSID {ssid_number}: {ssid_name}\n"
                result += f"- **Status**: 🟢 Enabled\n"
                result += f"- **Security**: {auth_mode}\n"
                
                # Show password/PSK if available
                if auth_mode in ['psk', 'wpa', 'wpa-eap']:
                    psk = ssid.get('psk')
                    if psk:
                        result += f"- **🔑 Password**: `{psk}`\n"
                    else:
                        result += f"- **🔑 Password**: Not available (Enterprise auth)\n"
                elif auth_mode == 'open':
                    result += f"- **🔑 Password**: Open network (no password)\n"
                else:
                    result += f"- **🔑 Password**: Enterprise authentication\n"
                
                result += "\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving WiFi passwords: {str(e)}"