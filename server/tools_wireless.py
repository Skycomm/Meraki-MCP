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
        description="Update a wireless SSID for a Meraki network"
    )
    def update_network_wireless_ssid(network_id: str, ssid_number: int, name: str = None, enabled: bool = None):
        """
        Update a wireless SSID for a Meraki network.
        
        Args:
            network_id: ID of the network
            ssid_number: Number of the SSID to update
            name: New name for the SSID (optional)
            enabled: Whether the SSID should be enabled (optional)
            
        Returns:
            Updated SSID details
        """
        return meraki_client.update_network_wireless_ssid(network_id, ssid_number, name, enabled)
    
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
    def get_network_wireless_usage(network_id: str):
        """
        Get wireless usage statistics for a Meraki network.
        
        Args:
            network_id: ID of the network
            
        Returns:
            Formatted wireless usage statistics
        """
        try:
            usage = meraki_client.get_network_wireless_usage(network_id)
            
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
