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
        description="Update a Meraki device - name, tags, address, or coordinates"
    )
    def update_device(serial: str, name: str = None, tags: list = None, address: str = None,
                     lat: float = None, lng: float = None):
        """
        Update a Meraki device.
        
        Args:
            serial: Serial number of the device to update
            name: New name for the device (optional)
            tags: New tags for the device (optional)
            address: New address for the device (optional)
            lat: Latitude coordinate (optional)
            lng: Longitude coordinate (optional)
            
        Returns:
            Updated device details
        """
        try:
            result = meraki_client.update_device(serial, name, tags, address, lat, lng)
            
            # Build response message
            updates = []
            if name:
                updates.append(f"name: {name}")
            if tags:
                updates.append(f"tags: {tags}")
            if address:
                updates.append(f"address: {address}")
            if lat is not None and lng is not None:
                updates.append(f"coordinates: ({lat}, {lng})")
            
            return f"✅ Device updated successfully - {', '.join(updates)}"
            
        except Exception as e:
            return f"❌ Failed to update device: {str(e)}"
    
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
        name="claim_device_direct",
        description="Directly claim a device into a network without checking if it exists first"
    )
    def claim_device_direct(network_id: str, serial: str):
        """
        Directly claim a device into a network without existence check.
        Use this when get_device returns 404 for unclaimed devices.
        
        Args:
            network_id: ID of the network to claim the device into
            serial: Serial number of the device to claim
            
        Returns:
            Success message or error details
        """
        try:
            # Get network info for better error message
            network = meraki_client.get_network(network_id)
            network_name = network.get('name', 'Unknown')
            
            # Directly attempt to claim without checking existence
            result = meraki_client.dashboard.networks.claimNetworkDevices(
                network_id, 
                serials=[serial]
            )
            
            # Check if there were any errors in the result
            if result.get('errors'):
                return f"⚠️ Claim completed with errors: {result['errors']}"
            
            return f"✅ Successfully claimed device {serial} into network '{network_name}' (ID: {network_id})"
            
        except Exception as e:
            error_msg = str(e)
            
            # Provide helpful error messages
            if "400" in error_msg:
                if "already claimed" in error_msg.lower():
                    return f"❌ Device {serial} is already claimed to another network"
                elif "invalid" in error_msg.lower():
                    return f"❌ Invalid device serial: {serial}"
                else:
                    return f"❌ Bad request: {error_msg}"
            elif "404" in error_msg:
                return f"❌ Network {network_id} not found"
            else:
                return f"❌ Failed to claim device {serial}: {error_msg}"
    
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
    
    @app.tool(
        name="unclaim_device_from_network",
        description="Remove/unclaim a device from a network (returns it to organization inventory)"
    )
    def unclaim_device_from_network(network_id: str, serial: str):
        """
        Remove a device from a network and return it to organization inventory.
        This is a non-destructive operation - the device remains in the org.
        
        Args:
            network_id: ID of the network containing the device
            serial: Serial number of the device to unclaim
            
        Returns:
            Success message or error details
        """
        try:
            # Get network and device info for better messages
            network = meraki_client.get_network(network_id)
            network_name = network.get('name', 'Unknown')
            
            # Get device info
            try:
                device = meraki_client.get_device(serial)
                device_name = device.get('name', serial)
                device_model = device.get('model', 'Unknown')
            except:
                device_name = serial
                device_model = 'Unknown'
            
            # Remove device from network
            result = meraki_client.dashboard.networks.removeNetworkDevices(
                network_id,
                serial=serial
            )
            
            return f"""✅ Successfully unclaimed device from network!

**Device**: {device_name} ({device_model})
**Serial**: {serial}
**Removed from**: {network_name} (ID: {network_id})
**Status**: Returned to organization inventory

The device is now unassigned and can be:
- Added to a different network
- Left in inventory as a spare
- Transferred to another organization"""
            
        except Exception as e:
            error_msg = str(e)
            
            # Provide helpful error messages
            if "404" in error_msg:
                if "network" in error_msg.lower():
                    return f"❌ Network {network_id} not found"
                else:
                    return f"❌ Device {serial} not found in network {network_id}"
            elif "400" in error_msg:
                return f"❌ Bad request: {error_msg}\n\nDevice might not be in this network."
            else:
                return f"❌ Failed to unclaim device {serial}: {error_msg}"
