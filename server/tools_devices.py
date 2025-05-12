"""
Device-related tools for the Cisco Meraki MCP Server - Modern implementation.
"""

# Global variables to store app and meraki client
app = None
meraki_client = None

def register_device_tools(mcp_app, meraki):
    """
    Register device-related tools with the MCP server.
    
    Args:
        mcp_app: MCP server instance
        meraki: Meraki client instance
    """
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    
    # Register all device tools
    register_device_tool_handlers()

def register_device_tool_handlers():
    """Register all device-related tool handlers using the decorator pattern."""
    
    @app.tool(
        name="get_device",
        description="Get details about a specific Meraki device"
    )
    def get_device(serial: str):
        """
        Get details about a specific Meraki device.
        
        Args:
            serial: Serial number of the device to retrieve
            
        Returns:
            Device details
        """
        return meraki_client.get_device(serial)
    
    @app.tool(
        name="update_device",
        description="Update a Meraki device"
    )
    def update_device(serial: str, name: str = None, tags: list = None, address: str = None):
        """
        Update a Meraki device.
        
        Args:
            serial: Serial number of the device to update
            name: New name for the device (optional)
            tags: New tags for the device (optional)
            address: New address for the device (optional)
            
        Returns:
            Updated device details
        """
        return meraki_client.update_device(serial, name, tags, address)
    
    @app.tool(
        name="reboot_device",
        description="Reboot a Meraki device"
    )
    def reboot_device(serial: str):
        """
        Reboot a Meraki device.
        
        Args:
            serial: Serial number of the device to reboot
            
        Returns:
            Success/failure information
        """
        return meraki_client.reboot_device(serial)
    
    @app.tool(
        name="get_device_clients",
        description="List clients connected to a specific Meraki device"
    )
    def get_device_clients(serial: str):
        """
        List clients connected to a specific Meraki device.
        
        Args:
            serial: Serial number of the device
            
        Returns:
            Formatted list of clients
        """
        try:
            clients = meraki_client.get_device_clients(serial)
            
            if not clients:
                return f"No clients found for device {serial}."
                
            # Format the output for readability
            result = f"# Clients Connected to Device ({serial})\n\n"
            for client in clients:
                result += f"- **{client.get('description', 'Unknown Device')}**\n"
                result += f"  - MAC: `{client.get('mac', 'Unknown')}`\n"
                result += f"  - IP: `{client.get('ip', 'Unknown')}`\n"
                result += f"  - VLAN: {client.get('vlan', 'Unknown')}\n"
                result += f"  - Connection: {client.get('status', 'Unknown')}\n"
                
                # Add usage if available
                usage = client.get('usage')
                if usage:
                    result += f"  - Usage: {usage.get('sent', 0)} sent, {usage.get('recv', 0)} received\n"
                
                result += "\n"
                
            return result
            
        except Exception as e:
            return f"Failed to list clients for device {serial}: {str(e)}"
    
    @app.tool(
        name="get_device_status",
        description="Get status information for a specific Meraki device"
    )
    def get_device_status(serial: str):
        """
        Get status information for a specific Meraki device.
        
        Args:
            serial: Serial number of the device
            
        Returns:
            Formatted status information
        """
        try:
            status = meraki_client.get_device_status(serial)
            
            if not status:
                return f"No status information found for device {serial}."
                
            # Format the output for readability
            result = f"# Status for Device ({serial})\n\n"
            
            # Connection
            result += "## Connection\n"
            result += f"- Status: {status.get('status', 'Unknown')}\n"
            result += f"- Last Reported: {status.get('lastReportedAt', 'Unknown')}\n"
            
            # Performance
            result += "\n## Performance\n"
            result += f"- CPU: {status.get('cpu', 'Unknown')}%\n"
            result += f"- Memory: {status.get('memory', 'Unknown')}%\n"
            
            # WAN
            wan = status.get('wan', {})
            if wan:
                result += "\n## WAN Interface\n"
                result += f"- IP: {wan.get('ip', 'Unknown')}\n"
                result += f"- Gateway: {wan.get('gateway', 'Unknown')}\n"
                result += f"- DNS: {wan.get('dns', 'Unknown')}\n"
                result += f"- Upload: {wan.get('uplink', {}).get('status', 'Unknown')}\n"
            
            return result
            
        except Exception as e:
            return f"Failed to get status for device {serial}: {str(e)}"
