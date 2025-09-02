"""
Device-related tools for the Cisco Meraki MCP Server - Complete SDK coverage.
Organized to match the official Meraki Dashboard API structure.
"""

import json
from typing import Optional, List, Dict, Any

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
    
    # ========== MANAGEMENT INTERFACE SDK METHODS ==========
    @app.tool(
        name="get_device_management_interface",
        description="🔧 Get management interface settings for a device"
    )
    def get_device_management_interface(serial: str):
        """
        Get management interface settings for a device.
        
        Args:
            serial: Device serial number
            
        Returns:
            Management interface configuration
        """
        try:
            interface = meraki_client.get_device_management_interface(serial)
            
            result = f"# 🔧 Management Interface for {serial}\n\n"
            
            # WAN configuration
            if interface.get('wan1'):
                wan1 = interface['wan1']
                result += "## WAN1 Configuration\n"
                result += f"- **Using DHCP**: {'✅' if wan1.get('usingStaticIp') == False else '❌'}\n"
                if wan1.get('staticIp'):
                    result += f"- **Static IP**: {wan1['staticIp']}\n"
                if wan1.get('staticSubnetMask'):
                    result += f"- **Subnet Mask**: {wan1['staticSubnetMask']}\n"
                if wan1.get('staticGatewayIp'):
                    result += f"- **Gateway**: {wan1['staticGatewayIp']}\n"
                if wan1.get('staticDns'):
                    result += f"- **DNS Servers**: {', '.join(wan1['staticDns'])}\n"
                if wan1.get('vlan'):
                    result += f"- **VLAN**: {wan1['vlan']}\n"
                    
            if interface.get('wan2'):
                wan2 = interface['wan2']
                result += "\n## WAN2 Configuration\n"
                result += f"- **Using DHCP**: {'✅' if wan2.get('usingStaticIp') == False else '❌'}\n"
                if wan2.get('staticIp'):
                    result += f"- **Static IP**: {wan2['staticIp']}\n"
                if wan2.get('staticSubnetMask'):
                    result += f"- **Subnet Mask**: {wan2['staticSubnetMask']}\n"
                if wan2.get('staticGatewayIp'):
                    result += f"- **Gateway**: {wan2['staticGatewayIp']}\n"
                if wan2.get('staticDns'):
                    result += f"- **DNS Servers**: {', '.join(wan2['staticDns'])}\n"
                if wan2.get('vlan'):
                    result += f"- **VLAN**: {wan2['vlan']}\n"
                    
            return result
            
        except Exception as e:
            return f"Error retrieving management interface: {str(e)}"
    
    @app.tool(
        name="update_device_management_interface",
        description="🔧 Update management interface settings for a device"
    )
    def update_device_management_interface(
        serial: str,
        wan1_settings: Optional[str] = None,
        wan2_settings: Optional[str] = None
    ):
        """
        Update management interface settings for a device.
        
        Args:
            serial: Device serial number
            wan1_settings: JSON WAN1 settings {usingStaticIp: bool, staticIp: "...", ...}
            wan2_settings: JSON WAN2 settings {usingStaticIp: bool, staticIp: "...", ...}
            
        Returns:
            Updated management interface settings
        """
        try:
            kwargs = {}
            if wan1_settings:
                kwargs['wan1'] = json.loads(wan1_settings)
            if wan2_settings:
                kwargs['wan2'] = json.loads(wan2_settings)
                
            result = meraki_client.update_device_management_interface(serial, **kwargs)
            return "✅ Management interface updated successfully"
            
        except Exception as e:
            return f"Error updating management interface: {str(e)}"
    
    # ========== LOSS AND LATENCY SDK METHODS ==========
    @app.tool(
        name="get_device_loss_and_latency_history",
        description="📊 Get historical loss and latency data for a device"
    )
    def get_device_loss_and_latency_history(
        serial: str,
        ip: str,
        timespan: Optional[int] = 86400,
        resolution: Optional[int] = 60,
        uplink: Optional[str] = None
    ):
        """
        Get loss and latency history for a device.
        
        Args:
            serial: Device serial number
            ip: Target IP to test connectivity to
            timespan: Time span in seconds (default: 24 hours)
            resolution: Resolution in seconds (60, 600, 3600, 86400)
            uplink: Uplink to test (wan1, wan2, cellular)
            
        Returns:
            Historical loss and latency data
        """
        try:
            kwargs = {
                'ip': ip,
                'timespan': timespan,
                'resolution': resolution
            }
            if uplink:
                kwargs['uplink'] = uplink
                
            history = meraki_client.dashboard.devices.getDeviceLossAndLatencyHistory(serial, **kwargs)
            
            if not history:
                return f"No loss/latency data available for {ip}"
                
            result = f"# 📊 Loss & Latency History to {ip}\n\n"
            result += f"**Device**: {serial}\n"
            result += f"**Time Span**: {timespan} seconds\n"
            if uplink:
                result += f"**Uplink**: {uplink}\n"
            result += "\n"
            
            # Show recent data points
            for data_point in history[-10:]:  # Last 10 data points
                result += f"## {data_point.get('startTs', 'Unknown')}\n"
                result += f"- **Loss**: {data_point.get('lossPercent', 0)}%\n"
                result += f"- **Latency**: {data_point.get('latencyMs', 0)} ms\n\n"
                
            if len(history) > 10:
                result += f"*Showing last 10 of {len(history)} data points*\n"
                
            return result
            
        except Exception as e:
            error_msg = str(e)
            if "only supports MX, MG and Z devices" in error_msg:
                return f"⚠️ Loss/latency history is only available for MX (security appliances), MG (cellular gateways), and Z (teleworker gateways) devices.\n\nDevice {serial} appears to be a different type (e.g., MR wireless AP or MS switch).\n\nFor wireless APs, use 'get_network_wireless_latency_stats' instead."
            return f"Error retrieving loss/latency history: {error_msg}"
    
    # ========== LLDP/CDP SDK METHODS ==========
    @app.tool(
        name="get_device_lldp_cdp",
        description="🔗 Get LLDP and CDP neighbor information for a device"
    )
    def get_device_lldp_cdp(serial: str):
        """
        Get LLDP and CDP neighbor information for a device.
        
        Args:
            serial: Device serial number
            
        Returns:
            LLDP/CDP neighbor details
        """
        try:
            neighbors = meraki_client.dashboard.devices.getDeviceLldpCdp(serial)
            
            if not neighbors:
                return f"No LLDP/CDP neighbors found for device {serial}"
                
            result = f"# 🔗 LLDP/CDP Neighbors for {serial}\n\n"
            
            # CDP neighbors
            if neighbors.get('cdp'):
                result += "## CDP Neighbors\n"
                for neighbor in neighbors['cdp']:
                    result += f"- **{neighbor.get('deviceId', 'Unknown')}**\n"
                    result += f"  - Port: {neighbor.get('portId', 'Unknown')}\n"
                    result += f"  - Address: {neighbor.get('address', 'N/A')}\n"
                    result += f"  - Platform: {neighbor.get('platform', 'N/A')}\n\n"
                    
            # LLDP neighbors
            if neighbors.get('lldp'):
                result += "## LLDP Neighbors\n"
                for neighbor in neighbors['lldp']:
                    result += f"- **{neighbor.get('systemName', 'Unknown')}**\n"
                    result += f"  - Port: {neighbor.get('portId', 'Unknown')}\n"
                    result += f"  - Description: {neighbor.get('portDescription', 'N/A')}\n"
                    result += f"  - Chassis ID: {neighbor.get('chassisId', 'N/A')}\n\n"
                    
            return result
            
        except Exception as e:
            return f"Error retrieving LLDP/CDP info: {str(e)}"
    
    # ========== CELLULAR SIMS SDK METHODS ==========
    @app.tool(
        name="get_device_cellular_sims",
        description="📱 Get SIM card information for a cellular device"
    )
    def get_device_cellular_sims(serial: str):
        """
        Get SIM card information for a cellular device.
        
        Args:
            serial: Device serial number
            
        Returns:
            SIM card details
        """
        try:
            sims = meraki_client.get_device_cellular_sims(serial)
            
            result = f"# 📱 Cellular SIM Information\n\n"
            
            for sim in sims.get('sims', []):
                slot = sim.get('slot', 'Unknown')
                result += f"## SIM Slot {slot}\n"
                result += f"- **Status**: {sim.get('status', 'Unknown')}\n"
                result += f"- **ICCID**: {sim.get('iccid', 'N/A')}\n"
                result += f"- **Carrier**: {sim.get('carrier', 'N/A')}\n"
                result += f"- **APN**: {sim.get('apn', 'N/A')}\n"
                
                if sim.get('isPrimary'):
                    result += "- **Primary SIM**: ✅\n"
                    
                result += "\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving SIM information: {str(e)}"
    
    @app.tool(
        name="update_device_cellular_sims",
        description="📱 Update SIM card settings for a cellular device"
    )
    def update_device_cellular_sims(
        serial: str,
        sims: str,
        sim_failover: Optional[str] = None,
        sim_failover_timeout: Optional[int] = None
    ):
        """
        Update SIM card settings for a cellular device.
        
        Args:
            serial: Device serial number
            sims: JSON array of SIM configurations [{slot: "sim1", isPrimary: true, apn: "..."}]
            sim_failover: Failover settings JSON
            sim_failover_timeout: Failover timeout in seconds
            
        Returns:
            Updated SIM settings
        """
        try:
            kwargs = {
                'sims': json.loads(sims)
            }
            if sim_failover:
                kwargs['simFailover'] = json.loads(sim_failover)
            if sim_failover_timeout:
                kwargs['simFailoverTimeout'] = sim_failover_timeout
                
            result = meraki_client.update_device_cellular_sims(serial, **kwargs)
            return "✅ SIM settings updated successfully"
            
        except Exception as e:
            return f"Error updating SIM settings: {str(e)}"
    
    # ========== LED BLINKING SDK METHOD ==========
    @app.tool(
        name="blink_device_leds",
        description="💡 Blink LEDs on a device for identification"
    )
    def blink_device_leds(
        serial: str,
        duration: Optional[int] = 20,
        duty: Optional[int] = 50,
        period: Optional[int] = 100
    ):
        """
        Blink LEDs on a device for identification.
        
        Args:
            serial: Device serial number
            duration: Duration in seconds (default: 20)
            duty: Duty cycle percentage (default: 50)
            period: Period in milliseconds (default: 100)
            
        Returns:
            LED blink status
        """
        try:
            result = meraki_client.blink_device_leds(
                serial,
                duration=duration,
                duty=duty,
                period=period
            )
            
            return f"""✅ LED Blink Initiated

**Device**: {serial}
**Duration**: {duration} seconds
**Pattern**: {duty}% on, {100-duty}% off
**Period**: {period} ms

The device LEDs are now blinking to help identify it physically."""
            
        except Exception as e:
            return f"Error blinking LEDs: {str(e)}"
    
    # ========== SENSOR SDK METHODS ==========
    # DUPLICATE: Commented out - using version in tools_sensor.py
    # @app.tool(
    #     name="get_device_sensor_relationships",
    #     description="📊 Get sensor relationships for a device"
    # )
    def get_device_sensor_relationships(serial: str):
        """
        Get sensor relationships for a device.
        
        Args:
            serial: Device serial number
            
        Returns:
            Sensor relationship information
        """
        try:
            result = meraki_client.dashboard.devices.getDeviceSensorRelationships(serial)
            
            if not result:
                return "No sensor relationships found for this device."
                
            formatted = "# 📊 Sensor Relationships\n\n"
            
            if 'livestream' in result:
                formatted += "## Livestream\n"
                for item in result['livestream'].get('relatedDevices', []):
                    formatted += f"- {item.get('serial', 'Unknown')}: {item.get('productType', 'Unknown')}\n"
                    
            return formatted
            
        except Exception as e:
            return f"Error retrieving sensor relationships: {str(e)}"
    
    # DUPLICATE: Commented out - using version in tools_sensor.py
    # @app.tool(
    #     name="update_device_sensor_relationships",
    #     description="📊 Update sensor relationships for a device"
    # )
    def update_device_sensor_relationships(
        serial: str,
        livestream: Optional[str] = None
    ):
        """
        Update sensor relationships for a device.
        
        Args:
            serial: Device serial number
            livestream: JSON object with relatedDevices array
            
        Returns:
            Updated sensor relationships
        """
        try:
            kwargs = {}
            if livestream:
                kwargs['livestream'] = json.loads(livestream)
                
            result = meraki_client.dashboard.devices.updateDeviceSensorRelationships(
                serial, **kwargs
            )
            return "✅ Sensor relationships updated successfully"
            
        except Exception as e:
            return f"Error updating sensor relationships: {str(e)}"
    
    # ========== SWITCH PORT SDK METHODS ==========
    # DUPLICATE: Commented out - using version in tools_switch.py
    # @app.tool(
    #     name="cycle_device_switch_ports",
    #     description="🔄 Cycle (restart) switch ports on a device - REQUIRES CONFIRMATION"
    # )
    def cycle_device_switch_ports(
        serial: str,
        ports: str,
        confirmed: bool = False
    ):
        """
        Cycle (restart) switch ports on a device.
        
        ⚠️ WARNING: This will disconnect devices on these ports!
        
        Args:
            serial: Device serial number
            ports: JSON array of port IDs to cycle ["1", "2", "3"]
            confirmed: Must be True to execute this operation
            
        Returns:
            Port cycling status
        """
        if not confirmed:
            return "⚠️ Port cycling requires confirmation. Set confirmed=true to proceed."
            
        try:
            ports_list = json.loads(ports)
            result = meraki_client.dashboard.devices.cycleDeviceSwitchPorts(
                serial,
                ports=ports_list
            )
            
            return f"✅ Successfully initiated port cycling for ports: {', '.join(ports_list)}"
            
        except Exception as e:
            return f"Error cycling ports: {str(e)}"
    
    # ========== PING SDK METHODS ==========
    @app.tool(
        name="create_device_live_tools_ping",
        description="🏓 Create a ping test from a device"
    )
    def create_device_live_tools_ping(
        serial: str,
        target: str,
        count: Optional[int] = 5
    ):
        """
        Create a ping test from a device.
        
        Args:
            serial: Device serial number
            target: IP address or hostname to ping
            count: Number of pings to send (default: 5)
            
        Returns:
            Ping test ID and status
        """
        try:
            result = meraki_client.dashboard.devices.createDeviceLiveToolsPing(
                serial,
                target=target,
                count=count
            )
            
            # Check for different possible ID field names
            test_id = result.get('pingId') or result.get('id') or result.get('testId', 'Unknown')
            
            return f"""✅ Ping Test Initiated

**Test ID**: {test_id}
**Target**: {target}
**Count**: {count}
**Status**: {result.get('status', 'new')}

Use get_device_live_tools_ping with the test ID to check results."""
            
        except Exception as e:
            return f"Error creating ping test: {str(e)}"
    
    # DUPLICATE: Commented out - using async version in tools_live.py
    # @app.tool(
    #     name="get_device_live_tools_ping",
    #     description="🏓 Get results of a ping test"
    # )
    def get_device_live_tools_ping(serial: str, id: str):
        """
        Get results of a ping test.
        
        Args:
            serial: Device serial number
            id: Ping test ID
            
        Returns:
            Ping test results
        """
        try:
            result = meraki_client.dashboard.devices.getDeviceLiveToolsPing(serial, id)
            
            formatted = f"# 🏓 Ping Test Results\n\n"
            formatted += f"**Status**: {result.get('status', 'Unknown')}\n"
            formatted += f"**Target**: {result.get('target', 'Unknown')}\n\n"
            
            if 'results' in result:
                formatted += "## Results\n"
                stats = result['results']
                formatted += f"- **Sent**: {stats.get('sent', 0)}\n"
                formatted += f"- **Received**: {stats.get('received', 0)}\n"
                formatted += f"- **Loss**: {stats.get('loss', 0)}%\n"
                
                if 'latencies' in stats:
                    lat = stats['latencies']
                    formatted += f"- **Min Latency**: {lat.get('minimum', 0)} ms\n"
                    formatted += f"- **Avg Latency**: {lat.get('average', 0)} ms\n"
                    formatted += f"- **Max Latency**: {lat.get('maximum', 0)} ms\n"
                    
            return formatted
            
        except Exception as e:
            return f"Error retrieving ping results: {str(e)}"

    
    # ========== CABLE TEST SDK METHODS ==========
    # DUPLICATE: Commented out - using async version in tools_live.py
    # @app.tool(
    #     name="create_device_live_tools_cable_test",
    #     description="🔌 Create a cable test on switch ports"
    # )
    def create_device_live_tools_cable_test(
        serial: str,
        ports: str
    ):
        """
        Create a cable test on switch ports.
        
        Args:
            serial: Device serial number
            ports: JSON array of port IDs to test ["1", "2", "3"]
            
        Returns:
            Cable test ID and status
        """
        try:
            ports_list = json.loads(ports)
            result = meraki_client.dashboard.devices.createDeviceLiveToolsCableTest(
                serial,
                ports=ports_list
            )
            
            return f"""✅ Cable Test Initiated

**Test ID**: {result.get("id", "Unknown")}
**Ports**: {", ".join(ports_list)}
**Status**: {result.get("status", "Unknown")}

Use get_device_live_tools_cable_test with the test ID to check results."""
            
        except Exception as e:
            return f"Error creating cable test: {str(e)}"
    
    # DUPLICATE: Commented out - using async version in tools_live.py
    # @app.tool(
    #     name="get_device_live_tools_cable_test",
    #     description="🔌 Get results of a cable test"
    # )
    def get_device_live_tools_cable_test(serial: str, id: str):
        """
        Get results of a cable test.
        
        Args:
            serial: Device serial number
            id: Cable test ID
            
        Returns:
            Cable test results
        """
        try:
            result = meraki_client.dashboard.devices.getDeviceLiveToolsCableTest(serial, id)
            
            formatted = f"# 🔌 Cable Test Results\n\n"
            formatted += f"**Status**: {result.get('status', 'Unknown')}\n\n"
            
            if "results" in result:
                formatted += "## Port Results\n"
                for port_result in result["results"]:
                    port = port_result.get("port", "Unknown")
                    status = port_result.get("status", "Unknown")
                    formatted += f"\n### Port {port}\n"
                    formatted += f"- **Status**: {status}\n"
                    
                    if "pairs" in port_result:
                        for pair in port_result["pairs"]:
                            formatted += f"- **Pair {pair.get('index', '?')}**: "
                            formatted += f"{pair.get('status', 'Unknown')} "
                            if "lengthMeters" in pair:
                                formatted += f"({pair['lengthMeters']} meters)"
                            formatted += "\n"
                            
            return formatted
            
        except Exception as e:
            return f"Error retrieving cable test results: {str(e)}"
    
    # ========== WAKE ON LAN SDK METHOD ==========
    # DUPLICATE: Commented out - using async version in tools_live.py
    # @app.tool(
    #     name="create_device_live_tools_wake_on_lan",
    #     description="⏰ Send Wake-on-LAN packet to wake up a device"
    # )
    def create_device_live_tools_wake_on_lan(
        serial: str,
        vlan_id: int,
        mac: str
    ):
        """
        Send Wake-on-LAN packet to wake up a device.
        
        Args:
            serial: Device serial number (switch/AP to send from)
            vlan_id: VLAN ID to send the packet on
            mac: MAC address of the device to wake
            
        Returns:
            Wake-on-LAN status
        """
        try:
            result = meraki_client.dashboard.devices.createDeviceLiveToolsWakeOnLan(
                serial,
                vlanId=vlan_id,
                mac=mac
            )
            
            return f"""✅ Wake-on-LAN Sent

**Target MAC**: {mac}
**VLAN**: {vlan_id}
**Status**: {result.get("status", "Unknown")}

The magic packet has been sent to wake the device."""
            
        except Exception as e:
            return f"Error sending Wake-on-LAN: {str(e)}"
    
    # ========== THROUGHPUT TEST SDK METHODS ==========
    # DUPLICATE: Commented out - using async version in tools_live.py
    # @app.tool(
    #     name="create_device_live_tools_throughput_test",
    #     description="📊 Create a throughput test from a device"
    # )
    def create_device_live_tools_throughput_test(serial: str):
        """
        Create a throughput test from a device.
        
        Args:
            serial: Device serial number
            
        Returns:
            Throughput test ID and status
        """
        try:
            result = meraki_client.dashboard.devices.createDeviceLiveToolsThroughputTest(serial)
            
            return f"""✅ Throughput Test Initiated

**Test ID**: {result.get("id", "Unknown")}
**Status**: {result.get("status", "Unknown")}

Use get_device_live_tools_throughput_test with the test ID to check results."""
            
        except Exception as e:
            return f"Error creating throughput test: {str(e)}"
    
    # DUPLICATE: Commented out - using async version in tools_live.py
    # @app.tool(
    #     name="get_device_live_tools_throughput_test",
    #     description="📊 Get results of a throughput test"
    # )
    def get_device_live_tools_throughput_test(serial: str, id: str):
        """
        Get results of a throughput test.
        
        Args:
            serial: Device serial number
            id: Throughput test ID
            
        Returns:
            Throughput test results
        """
        try:
            result = meraki_client.dashboard.devices.getDeviceLiveToolsThroughputTest(serial, id)
            
            formatted = f"# 📊 Throughput Test Results\n\n"
            formatted += f"**Status**: {result.get('status', 'Unknown')}\n\n"
            
            if "results" in result:
                results = result["results"]
                formatted += "## Test Results\n"
                
                if "speeds" in results:
                    speeds = results["speeds"]
                    formatted += f"- **Download**: {speeds.get('downstream', 0)} Mbps\n"
                    formatted += f"- **Upload**: {speeds.get('upstream', 0)} Mbps\n"
                    
            return formatted
            
        except Exception as e:
            return f"Error retrieving throughput test results: {str(e)}"
    
    # ==================== MISSING LIVE TOOLS ====================
    
    @app.tool(
        name="create_device_live_tools_ping_device",
        description="🏓 Enqueue a job to check connectivity status to the device"
    )
    def create_device_live_tools_ping_device(serial: str):
        """
        Create a ping test TO the device itself.
        
        Args:
            serial: Device serial number
            
        Returns:
            Ping device job details including id
        """
        try:
            result = meraki_client.dashboard.devices.createDeviceLiveToolsPingDevice(serial)
            
            response = f"# 🏓 Ping Device Test Started\n\n"
            response += f"**Device**: {serial}\n"
            response += f"**Job ID**: {result.get('id', 'N/A')}\n"
            response += f"**Status**: {result.get('status', 'N/A')}\n"
            
            if result.get('url'):
                response += f"**Check URL**: {result['url']}\n"
                
            return response
            
        except Exception as e:
            return f"❌ Error creating ping device test: {str(e)}"
    
    @app.tool(
        name="get_device_live_tools_ping_device",
        description="🏓 Return a ping device job result"
    )
    def get_device_live_tools_ping_device(serial: str, id: str):
        """
        Get results of a ping device test.
        
        Args:
            serial: Device serial number
            id: Ping test job ID
            
        Returns:
            Ping device test results
        """
        try:
            result = meraki_client.dashboard.devices.getDeviceLiveToolsPingDevice(serial, id)
            
            response = f"# 🏓 Ping Device Results\n\n"
            response += f"**Device**: {serial}\n"
            response += f"**Job ID**: {id}\n"
            response += f"**Status**: {result.get('status', 'N/A')}\n"
            
            if result.get('results'):
                results = result['results']
                response += f"**Sent**: {results.get('sent', 0)} packets\n"
                response += f"**Received**: {results.get('received', 0)} packets\n"
                response += f"**Loss**: {results.get('loss', {}).get('percentage', 0)}%\n"
                
                latencies = results.get('latencies', {})
                if latencies:
                    response += f"**Latency**: {latencies.get('average', 0)}ms avg\n"
                    
            return response
            
        except Exception as e:
            return f"❌ Error getting ping device results: {str(e)}"
    
    @app.tool(
        name="create_device_live_tools_trace_route",
        description="🛣️ Enqueue a job for running traceroute from the device"
    )
    def create_device_live_tools_trace_route(serial: str, target: str):
        """
        Create a traceroute test from a device.
        
        Args:
            serial: Device serial number
            target: Target IP or hostname for traceroute
            
        Returns:
            Traceroute job details including traceRouteId
        """
        try:
            result = meraki_client.dashboard.devices.createDeviceLiveToolsTraceRoute(
                serial, target=target
            )
            
            response = f"# 🛣️ Traceroute Test Started\n\n"
            response += f"**Device**: {serial}\n"
            response += f"**Target**: {target}\n"
            response += f"**Job ID**: {result.get('id', 'N/A')}\n"
            response += f"**Status**: {result.get('status', 'N/A')}\n"
            
            if result.get('url'):
                response += f"**Check URL**: {result['url']}\n"
                
            return response
            
        except Exception as e:
            return f"❌ Error creating traceroute test: {str(e)}"
    
    @app.tool(
        name="get_device_live_tools_trace_route",
        description="🛣️ Return a traceroute job result"
    )
    def get_device_live_tools_trace_route(serial: str, id: str):
        """
        Get results of a traceroute test.
        
        Args:
            serial: Device serial number
            id: Traceroute job ID
            
        Returns:
            Traceroute results with hop details
        """
        try:
            result = meraki_client.dashboard.devices.getDeviceLiveToolsTraceRoute(serial, id)
            
            response = f"# 🛣️ Traceroute Results\n\n"
            response += f"**Device**: {serial}\n"
            response += f"**Job ID**: {id}\n"
            response += f"**Status**: {result.get('status', 'N/A')}\n"
            
            if result.get('results') and result['results'].get('hops'):
                response += f"\n## Hops\n"
                for i, hop in enumerate(result['results']['hops'], 1):
                    response += f"{i}. {hop.get('ip', 'N/A')} - {hop.get('rtt', 'N/A')}ms\n"
                    
            return response
            
        except Exception as e:
            return f"❌ Error getting traceroute results: {str(e)}"
    
    @app.tool(
        name="create_device_live_tools_arp_table",
        description="📋 Enqueue a job to retrieve the ARP table from the device"
    )
    def create_device_live_tools_arp_table(serial: str):
        """
        Create an ARP table retrieval job for a device.
        
        Args:
            serial: Device serial number
            
        Returns:
            ARP table job details including arpTableId
        """
        try:
            result = meraki_client.dashboard.devices.createDeviceLiveToolsArpTable(serial)
            
            response = f"# 📋 ARP Table Retrieval Started\n\n"
            response += f"**Device**: {serial}\n"
            response += f"**Job ID**: {result.get('id', 'N/A')}\n"
            response += f"**Status**: {result.get('status', 'N/A')}\n"
            
            if result.get('url'):
                response += f"**Check URL**: {result['url']}\n"
                
            return response
            
        except Exception as e:
            return f"❌ Error creating ARP table job: {str(e)}"
    
    @app.tool(
        name="get_device_live_tools_arp_table",
        description="📋 Return an ARP table job result"
    )
    def get_device_live_tools_arp_table(serial: str, id: str):
        """
        Get the ARP table job results from a device.
        
        Args:
            serial: Device serial number
            id: ARP table job ID
            
        Returns:
            ARP table entries
        """
        try:
            result = meraki_client.dashboard.devices.getDeviceLiveToolsArpTable(serial, id)
            
            response = f"# 📋 ARP Table Results\n\n"
            response += f"**Device**: {serial}\n"
            response += f"**Job ID**: {id}\n"
            response += f"**Status**: {result.get('status', 'N/A')}\n"
            
            if result.get('results') and result['results'].get('entries'):
                response += f"\n## ARP Entries ({len(result['results']['entries'])})\n"
                for entry in result['results']['entries']:
                    response += f"- **IP**: {entry.get('ip', 'N/A')} → "
                    response += f"**MAC**: {entry.get('mac', 'N/A')}\n"
                    
            return response
            
        except Exception as e:
            return f"❌ Error getting ARP table results: {str(e)}"

