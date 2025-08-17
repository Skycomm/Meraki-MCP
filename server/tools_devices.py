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
        description="⚠️ REBOOT a Meraki device - REQUIRES CONFIRMATION"
    )
    def reboot_device(serial: str):
        """
        Reboot a Meraki device.
        
        ⚠️ WARNING: This will disconnect all users and interrupt service!
        
        Args:
            serial: Serial number of the device to reboot
            
        Returns:
            Success/failure information
        """
        # Return a warning message instead of directly rebooting
        warning_msg = f"""# ⚠️ REBOOT CONFIRMATION REQUIRED

**Device Serial**: {serial}

**WARNING**: Rebooting this device will:
- 🔴 Disconnect ALL users
- 🔴 Interrupt network services
- 🔴 Take 2-5 minutes to come back online

**To proceed with reboot**:
If you really want to reboot this device, please confirm by saying:
"Yes, reboot device {serial}"

**Alternative solutions to try first**:
1. Check device status and logs
2. Verify cable connections
3. Check for firmware updates
4. Review recent configuration changes

⚠️ This action cannot be undone!"""
        
        return warning_msg
    
    @app.tool(
        name="confirm_reboot_device",
        description="🔴 CONFIRM and execute device reboot (use with extreme caution)"
    )
    def confirm_reboot_device(serial: str, confirmation: str):
        """
        Actually reboot a device after explicit confirmation.
        
        Args:
            serial: Serial number of the device to reboot
            confirmation: Must be exactly "YES-REBOOT-[serial]" to proceed
            
        Returns:
            Reboot status
        """
        expected_confirmation = f"YES-REBOOT-{serial}"
        
        if confirmation != expected_confirmation:
            return f"""❌ Confirmation failed!

You provided: "{confirmation}"
Expected: "{expected_confirmation}"

The device was NOT rebooted. Please use exact confirmation text if you really want to proceed."""
        
        try:
            result = meraki_client.reboot_device(serial)
            
            return f"""✅ REBOOT INITIATED

**Device**: {serial}
**Status**: Reboot command sent successfully
**Expected downtime**: 2-5 minutes

The device is now rebooting. Monitor its status to confirm it comes back online."""
            
        except Exception as e:
            return f"❌ Error rebooting device: {str(e)}"
    
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
            # Get device details
            device = meraki_client.get_device_status(serial)
            
            if not device:
                return f"No device found with serial {serial}."
                
            # Format the output for readability
            result = f"# Device Status: {device.get('name') or serial}\n\n"
            
            # Basic Information
            result += "## Device Information\n"
            result += f"- **Model**: {device.get('model', 'Unknown')}\n"
            result += f"- **Serial**: {device.get('serial', serial)}\n"
            result += f"- **MAC Address**: {device.get('mac', 'Unknown')}\n"
            result += f"- **Firmware**: {device.get('firmware', 'Unknown')}\n"
            result += f"- **Network ID**: {device.get('networkId', 'Unknown')}\n"
            
            # Location
            if device.get('address') or device.get('lat'):
                result += "\n## Location\n"
                if device.get('address'):
                    result += f"- **Address**: {device['address']}\n"
                if device.get('lat') and device.get('lng'):
                    result += f"- **Coordinates**: {device['lat']}, {device['lng']}\n"
            
            # WAN IPs (for MX/Z devices)
            if device.get('wan1Ip') or device.get('wan2Ip'):
                result += "\n## WAN Status\n"
                if device.get('wan1Ip'):
                    result += f"- **WAN 1**: {device['wan1Ip']}\n"
                if device.get('wan2Ip'):
                    result += f"- **WAN 2**: {device['wan2Ip']}\n"
            
            # LAN IP (for devices with management IP)
            if device.get('lanIp'):
                result += f"\n## Management\n"
                result += f"- **LAN IP**: {device['lanIp']}\n"
            
            # Configuration
            if device.get('configurationUpdatedAt'):
                result += f"\n## Configuration\n"
                result += f"- **Last Updated**: {device['configurationUpdatedAt']}\n"
            
            # Tags
            if device.get('tags'):
                result += f"\n## Tags\n"
                result += f"- {device['tags']}\n"
            
            # Dashboard URL
            if device.get('url'):
                result += f"\n## Dashboard\n"
                result += f"- **URL**: {device['url']}\n"
            
            # Notes
            if device.get('notes'):
                result += f"\n## Notes\n"
                result += f"{device['notes']}\n"
            
            return result
            
        except Exception as e:
            return f"Failed to get status for device {serial}: {str(e)}"
