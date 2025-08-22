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
        try:
            # Get device details first
            device = meraki_client.get_device(serial)
            
            # Import helper function
            from utils.helpers import require_confirmation
            
            # Require confirmation
            if not require_confirmation(
                operation_type="reboot",
                resource_type="device",
                resource_name=device.get('name', f'Device {serial}'),
                resource_id=serial
            ):
                return "❌ Device reboot cancelled by user"
            
            # Perform reboot
            result = meraki_client.reboot_device(serial)
            
            return f"""✅ REBOOT INITIATED

**Device**: {device.get('name', serial)}
**Serial**: {serial}
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
    
    @app.tool(
        name="claim_device_into_network", 
        description="Claim/assign an organization device into a network"
    )
    def claim_device_into_network(network_id: str, serial: str):
        """
        Claim a device from organization inventory into a specific network.
        
        Args:
            network_id: ID of the network to claim the device into
            serial: Serial number of the device to claim
            
        Returns:
            Success message or error details
        """
        try:
            # The Meraki API endpoint for this is:
            # POST /networks/{networkId}/devices/claim
            result = meraki_client.dashboard.networks.claimNetworkDevices(
                network_id, 
                serials=[serial]
            )
            return f"✅ Successfully claimed device {serial} into network {network_id}"
        except Exception as e:
            return f"❌ Failed to claim device {serial}: {str(e)}"
    
    @app.tool(
        name="claim_devices_into_network",
        description="Claim multiple devices into a network at once"
    )
    def claim_devices_into_network(network_id: str, serials: str):
        """
        Claim multiple devices into a network.
        
        Args:
            network_id: ID of the network to claim devices into
            serials: Comma-separated list of device serial numbers
            
        Returns:
            Success message with results
        """
        serial_list = [s.strip() for s in serials.split(',')]
        
        try:
            result = meraki_client.dashboard.networks.claimNetworkDevices(
                network_id,
                serials=serial_list
            )
            return f"✅ Successfully claimed {len(serial_list)} devices into network"
        except Exception as e:
            return f"❌ Failed to claim devices: {str(e)}"
    
    @app.tool(
        name="list_unassigned_devices",
        description="List all devices in organization not assigned to any network"  
    )
    def list_unassigned_devices(organization_id: str):
        """
        List devices in organization inventory not assigned to networks.
        
        Args:
            organization_id: ID of the organization
            
        Returns:
            Formatted list of unassigned devices
        """
        try:
            # Get all devices in organization
            all_devices = meraki_client.dashboard.organizations.getOrganizationDevices(organization_id)
            
            # Filter for devices without networkId
            unassigned = [d for d in all_devices if not d.get('networkId')]
            
            if not unassigned:
                return "No unassigned devices found in organization"
                
            result = f"# Unassigned Devices ({len(unassigned)} total)\n\n"
            for device in unassigned:
                result += f"- **{device.get('model', 'Unknown')}** - Serial: `{device['serial']}`\n"
                if device.get('name'):
                    result += f"  - Name: {device['name']}\n"
                if device.get('mac'):
                    result += f"  - MAC: {device['mac']}\n"
                    
            return result
        except Exception as e:
            return f"Failed to list unassigned devices: {str(e)}"
