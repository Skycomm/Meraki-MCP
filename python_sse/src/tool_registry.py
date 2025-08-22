"""
Auto-generated tool registry from stdio server.
Contains all 97 MCP tools with implementations.
"""

from typing import Dict, Any, List, Optional
import json

# Import meraki_client - will be set by the server
meraki_client = None

def set_meraki_client(client):
    """Set the global meraki_client."""
    global meraki_client
    meraki_client = client


# From tools_organizations.py
async def list_organizations():
        """
        List all Meraki organizations the API key has access to.
        
        Returns:
            Formatted list of organizations
        """
        try:
            organizations = await meraki_client.get_organizations()
            
            if not organizations:
                return "No organizations found for this API key."
                
            # Format the output for readability
            result = "# Meraki Organizations\n\n"
            for org in organizations:
                result += f"- **{org['name']}** (ID: `{org['id']}`)\n"
                
            return result
            
        except Exception as e:
            return f"Failed to list organizations: {str(e)}"


# From tools_organizations.py
async def get_organization(organization_id: str):
        """
        Get details about a specific Meraki organization.
        
        Args:
            organization_id: ID of the organization to retrieve
            
        Returns:
            Organization details
        """
        return await meraki_client.get_organization(organization_id)


# From tools_organizations.py
async def get_organization_networks(org_id: str):
        """
        List networks in a Meraki organization.
        
        Args:
            org_id: ID of the organization
            
        Returns:
            Formatted list of networks
        """
        try:
            networks = await meraki_client.get_organization_networks(org_id)
            
            if not networks:
                return f"No networks found for organization {org_id}."
                
            # Format the output for readability
            result = f"# Networks in Organization ({org_id})\n\n"
            for net in networks:
                result += f"- **{net['name']}** (ID: `{net['id']}`)\n"
                result += f"  - Type: {net.get('type', 'Unknown')}\n"
                result += f"  - Tags: {', '.join(net.get('tags', []) or ['None'])}\n"
                
            return result
            
        except Exception as e:
            return f"Failed to list networks for organization {org_id}: {str(e)}"


# From tools_organizations.py
async def get_organization_alerts(org_id: str):
        """
        Get alert settings for a Meraki organization.
        
        Args:
            org_id: ID of the organization
            
        Returns:
            Formatted alert settings
        """
        try:
            alerts = await meraki_client.get_organization_alerts(org_id)
            
            if not alerts:
                return f"No alert settings found for organization {org_id}."
                
            # Format the output for readability
            result = f"# Alert Settings for Organization ({org_id})\n\n"
            
            # Add default destinations if present
            if 'defaultDestinations' in alerts:
                result += "## Default Destinations\n"
                destinations = alerts['defaultDestinations']
                result += f"- Email: {destinations.get('emails', [])}\n"
                result += f"- Webhook URLs: {destinations.get('httpServerIds', [])}\n"
                result += f"- SMS Numbers: {destinations.get('smsNumbers', [])}\n"
                result += "\n"
            
            # Add alert types
            if 'alerts' in alerts:
                result += "## Alert Types\n"
                for alert in alerts['alerts']:
                    result += f"### {alert.get('type', 'Unknown')}\n"
                    result += f"- Enabled: {alert.get('enabled', False)}\n"
                    
                    # Add alert-specific destinations
                    if 'destinations' in alert:
                        alert_dest = alert['destinations']
                        result += "- Destinations:\n"
                        result += f"  - Email: {alert_dest.get('emails', [])}\n"
                        result += f"  - Webhook URLs: {alert_dest.get('httpServerIds', [])}\n"
                        result += f"  - SMS Numbers: {alert_dest.get('smsNumbers', [])}\n"
                    
                    result += "\n"
                
            return result
            
        except Exception as e:
            return f"Failed to get alert settings for organization {org_id}: {str(e)}"


# From tools_organizations.py
async def create_organization(name: str):
        """
        Create a new Meraki organization.
        
        Args:
            name: Name for the new organization
            
        Returns:
            New organization details
        """
        return await meraki_client.create_organization(name)


# From tools_organizations.py
async def update_organization(organization_id: str, name: str = None):
        """
        Update a Meraki organization.
        
        Args:
            organization_id: ID of the organization to update
            name: New name for the organization (optional)
            
        Returns:
            Updated organization details
        """
        try:
            # Get current organization
            org = await meraki_client.get_organization(organization_id)
            current_name = org.get('name', 'Unknown')
            
            # If renaming, require confirmation
            if name and name != current_name:
                from utils.helpers import require_confirmation
                
                if not require_confirmation(
                    operation_type="rename",
                    resource_type="organization",
                    resource_name=f"{current_name} → {name}",
                    resource_id=organization_id
                ):
                    return "❌ Organization rename cancelled by user"
            
            # Perform update
            result = await meraki_client.update_organization(organization_id, name)
            return f"✅ Organization updated successfully"
            
        except Exception as e:
            return f"Failed to update organization: {str(e)}"


# From tools_organizations.py
async def delete_organization(organization_id: str):
        """
        Delete a Meraki organization.
        
        Args:
            organization_id: ID of the organization to delete
            
        Returns:
            Success/failure information
        """
        try:
            # Get organization details
            org = await meraki_client.get_organization(organization_id)
            
            # Import helper functions
            import os
            from utils.helpers import require_confirmation, get_read_only_message
            
            # Check if in read-only mode first
            if os.getenv("MCP_READ_ONLY_MODE", "false").lower() == "true":
                return get_read_only_message(
                    operation_type="delete",
                    resource_type="organization (⚠️ EXTREME DANGER)",
                    resource_name=org.get('name', 'Unknown'),
                    resource_id=organization_id
                )
            
            # Double confirmation for organization deletion
            print("\n⚠️  EXTREME CAUTION: Organization deletion will delete ALL networks and devices!")
            
            if not require_confirmation(
                operation_type="delete",
                resource_type="organization",
                resource_name=org.get('name', 'Unknown'),
                resource_id=organization_id
            ):
                return "❌ Organization deletion cancelled by user"
            
            # Second confirmation
            print(f"\n🚨 FINAL WARNING: This will delete organization '{org['name']}' and ALL its contents!")
            print("Type 'DELETE EVERYTHING' to confirm:")
            
            final_confirm = input("> ").strip()
            if final_confirm != "DELETE EVERYTHING":
                return "❌ Organization deletion cancelled - final confirmation failed"
            
            # Perform deletion
            await meraki_client.delete_organization(organization_id)
            return f"✅ Organization '{org['name']}' deleted permanently"
            
        except Exception as e:
            return f"Failed to delete organization: {str(e)}"


# From tools_organizations.py
async def get_organization_firmware(org_id: str):
        """
        Get firmware upgrades for a Meraki organization.
        
        Args:
            org_id: ID of the organization
            
        Returns:
            Formatted firmware upgrade information
        """
        try:
            upgrades = await meraki_client.get_organization_firmware_upgrades(org_id)
            
            if not upgrades:
                return f"No firmware upgrades found for organization {org_id}."
                
            # Format the output for readability
            result = f"# Firmware Upgrades for Organization ({org_id})\n\n"
            
            if isinstance(upgrades, list):
                for upgrade in upgrades:
                    result += f"## Upgrade ID: {upgrade.get('id', 'Unknown')}\n"
                    result += f"- Status: {upgrade.get('status', 'Unknown')}\n"
                    result += f"- Time: {upgrade.get('time', 'Unknown')}\n"
                    result += f"- Products: {', '.join(upgrade.get('products', []) or ['None'])}\n"
                    result += "\n"
            else:
                result += str(upgrades)
                
            return result
            
        except Exception as e:
            return f"Failed to get firmware upgrades for organization {org_id}: {str(e)}"


# From tools_networks.py
async def get_network(network_id: str):
        """
        Get details about a specific Meraki network.
        
        Args:
            network_id: ID of the network to retrieve
            
        Returns:
            Network details
        """
        return await meraki_client.get_network(network_id)


# From tools_networks.py
async def update_network(network_id: str, name: str = None, tags: list = None):
        """
        Update a Meraki network.
        
        Args:
            network_id: ID of the network to update
            name: New name for the network (optional)
            tags: New tags for the network (optional)
            
        Returns:
            Updated network details
        """
        try:
            # Get current network details
            network = await meraki_client.get_network(network_id)
            current_name = network.get('name', 'Unknown')
            
            # If renaming, require confirmation
            if name and name != current_name:
                from utils.helpers import require_confirmation
                
                if not require_confirmation(
                    operation_type="rename",
                    resource_type="network",
                    resource_name=f"{current_name} → {name}",
                    resource_id=network_id
                ):
                    return "❌ Network rename cancelled by user"
            
            # Perform update
            result = await meraki_client.update_network(network_id, name, tags)
            return f"✅ Network updated successfully"
            
        except Exception as e:
            return f"Failed to update network: {str(e)}"


# From tools_networks.py
async def get_network_devices(network_id: str):
        """
        List devices in a Meraki network.
        
        Args:
            network_id: ID of the network
            
        Returns:
            Formatted list of devices
        """
        try:
            devices = await meraki_client.get_network_devices(network_id)
            
            if not devices:
                return f"No devices found for network {network_id}."
                
            # Format the output for readability
            result = f"# Devices in Network ({network_id})\n\n"
            for device in devices:
                result += f"- **{device.get('name', 'Unnamed')}** (Model: {device.get('model', 'Unknown')})\n"
                result += f"  - Serial: `{device.get('serial', 'Unknown')}`\n"
                result += f"  - MAC: `{device.get('mac', 'Unknown')}`\n"
                result += f"  - Status: {device.get('status', 'Unknown')}\n"
                
                # Add location if available
                lat = device.get('lat')
                lng = device.get('lng')
                address = device.get('address')
                
                if lat and lng:
                    result += f"  - Location: ({lat}, {lng})\n"
                if address:
                    result += f"  - Address: {address}\n"
                
                result += "\n"
                
            return result
            
        except Exception as e:
            return f"Failed to list devices for network {network_id}: {str(e)}"


# From tools_networks.py
async def get_network_clients(network_id: str):
        """
        List clients in a Meraki network.
        
        Args:
            network_id: ID of the network
            
        Returns:
            Formatted list of clients
        """
        try:
            clients = await meraki_client.get_network_clients(network_id)
            
            if not clients:
                return f"No clients found for network {network_id}."
                
            # Format the output for readability
            result = f"# Clients in Network ({network_id})\n\n"
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
            return f"Failed to list clients for network {network_id}: {str(e)}"


# From tools_networks.py
async def create_network(organization_id: str, name: str, product_types: str = "wireless"):
        """
        Create a new Meraki network in an organization.
        
        Args:
            organization_id: ID of the organization to create the network in
            name: Name for the new network
            product_types: Comma-separated product types (appliance,switch,wireless,camera,sensor)
            
        Returns:
            New network details
        """
        # Convert comma-separated string to list
        types_list = [t.strip() for t in product_types.split(',')]
        # BUGFIX: Pass productTypes as named parameter instead of positional
        return await meraki_client.create_network(organization_id, name, productTypes=types_list)


# From tools_networks.py
async def delete_network(network_id: str):
        """
        Delete a Meraki network.
        
        Args:
            network_id: ID of the network to delete
            
        Returns:
            Success/failure information
        """
        try:
            # Get network details first
            network = await meraki_client.get_network(network_id)
            
            # Import helper functions
            import os
            from utils.helpers import require_confirmation, get_read_only_message
            
            # Check if in read-only mode first
            if os.getenv("MCP_READ_ONLY_MODE", "false").lower() == "true":
                return get_read_only_message(
                    operation_type="delete",
                    resource_type="network",
                    resource_name=network.get('name', 'Unknown'),
                    resource_id=network_id
                )
            
            # Require confirmation
            if not require_confirmation(
                operation_type="delete",
                resource_type="network", 
                resource_name=network.get('name', 'Unknown'),
                resource_id=network_id
            ):
                return "❌ Network deletion cancelled by user"
            
            # Perform deletion
            await meraki_client.delete_network(network_id)
            return f"✅ Network '{network['name']}' deleted successfully"
            
        except Exception as e:
            return f"Failed to delete network: {str(e)}"


# From tools_devices.py
async def get_device(serial: str):
        """
        Get details about a specific Meraki device.
        
        Args:
            serial: Serial number of the device to retrieve
            
        Returns:
            Device details
        """
        return await meraki_client.get_device(serial)


# From tools_devices.py
async def update_device(serial: str, name: str = None, tags: list = None, address: str = None):
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
        return await meraki_client.update_device(serial, name, tags, address)


# From tools_devices.py
async def reboot_device(serial: str):
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
            device = await meraki_client.get_device(serial)
            
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
            result = await meraki_client.reboot_device(serial)
            
            return f"""✅ REBOOT INITIATED

**Device**: {device.get('name', serial)}
**Serial**: {serial}
**Status**: Reboot command sent successfully
**Expected downtime**: 2-5 minutes

The device is now rebooting. Monitor its status to confirm it comes back online."""
            
        except Exception as e:
            return f"❌ Error rebooting device: {str(e)}"




# From tools_devices.py
async def get_device_clients(serial: str):
        """
        List clients connected to a specific Meraki device.
        
        Args:
            serial: Serial number of the device
            
        Returns:
            Formatted list of clients
        """
        try:
            clients = await meraki_client.get_device_clients(serial)
            
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


# From tools_devices.py
async def get_device_status(serial: str):
        """
        Get status information for a specific Meraki device.
        
        Args:
            serial: Serial number of the device
            
        Returns:
            Formatted status information
        """
        try:
            # Get device details
            device = await meraki_client.get_device_status(serial)
            
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


# From tools_devices.py
async def claim_device_into_network(network_id: str, serial: str):
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
            result = await meraki_client.dashboard.networks.claimNetworkDevices(
                network_id, 
                serials=[serial]
            )
            return f"✅ Successfully claimed device {serial} into network {network_id}"
        except Exception as e:
            return f"❌ Failed to claim device {serial}: {str(e)}"


# From tools_devices.py
async def claim_devices_into_network(network_id: str, serials: str):
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
            result = await meraki_client.dashboard.networks.claimNetworkDevices(
                network_id,
                serials=serial_list
            )
            return f"✅ Successfully claimed {len(serial_list)} devices into network"
        except Exception as e:
            return f"❌ Failed to claim devices: {str(e)}"


# From tools_devices.py
async def list_unassigned_devices(organization_id: str):
        """
        List devices in organization inventory not assigned to networks.
        
        Args:
            organization_id: ID of the organization
            
        Returns:
            Formatted list of unassigned devices
        """
        try:
            # Get all devices in organization
            all_devices = await meraki_client.dashboard.organizations.getOrganizationDevices(organization_id)
            
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


# From tools_wireless.py
async def get_network_wireless_ssids(network_id: str):
        """
        List wireless SSIDs for a Meraki network.
        
        Args:
            network_id: ID of the network
            
        Returns:
            Formatted list of SSIDs
        """
        try:
            ssids = await meraki_client.get_network_wireless_ssids(network_id)
            
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


# From tools_wireless.py
async def get_network_wireless_passwords(network_id: str):
        """
        Get WiFi passwords/PSK for wireless networks.
        
        Args:
            network_id: ID of the network
            
        Returns:
            Formatted list of SSIDs with passwords where available
        """
        try:
            ssids = await meraki_client.get_network_wireless_passwords(network_id)
            
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


# From tools_wireless.py
async def update_network_wireless_ssid(network_id: str, ssid_number: int, name: str = None, enabled: bool = None):
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
        return await meraki_client.update_network_wireless_ssid(network_id, ssid_number, name, enabled)


# From tools_wireless.py
async def get_network_wireless_clients(network_id: str):
        """
        List wireless clients for a Meraki network.
        
        Args:
            network_id: ID of the network
            
        Returns:
            Formatted list of wireless clients
        """
        try:
            clients = await meraki_client.get_network_wireless_clients(network_id)
            
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


# From tools_wireless.py
async def get_network_wireless_usage(network_id: str, ssid_number: int = None, device_serial: str = None):
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
            usage = await meraki_client.get_network_wireless_usage(
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


# From tools_wireless.py
async def get_network_wireless_rf_profiles(network_id: str):
        """
        Get RF profiles for a wireless network.
        
        Args:
            network_id: ID of the network
            
        Returns:
            RF profiles configuration
        """
        try:
            profiles = await meraki_client.get_network_wireless_rf_profiles(network_id)
            
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


# From tools_wireless.py
async def get_network_wireless_air_marshal(network_id: str, timespan: int = 3600):
        """
        Get Air Marshal (rogue AP detection) results for a network.
        
        Args:
            network_id: ID of the network
            timespan: Timespan in seconds (default: 1 hour)
            
        Returns:
            Air Marshal security scan results
        """
        try:
            air_marshal = await meraki_client.get_network_wireless_air_marshal(network_id, timespan)
            
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


# From tools_wireless.py
async def get_network_wireless_bluetooth_clients(network_id: str):
        """
        Get Bluetooth clients detected in a wireless network.
        
        Args:
            network_id: ID of the network
            
        Returns:
            List of Bluetooth clients
        """
        try:
            bt_clients = await meraki_client.get_network_wireless_bluetooth_clients(network_id)
            
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


# From tools_wireless.py
async def get_network_wireless_channel_utilization(network_id: str, timespan: int = 3600, ssid_number: int = None, device_serial: str = None):
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
            utilization = await meraki_client.get_network_wireless_channel_utilization(
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


# From tools_switch.py
async def get_device_switch_ports(serial: str):
        """
        List switch ports for a Meraki switch.
        
        Args:
            serial: Serial number of the switch
            
        Returns:
            Formatted list of switch ports
        """
        try:
            ports = await meraki_client.get_device_switch_ports(serial)
            
            if not ports:
                return f"No switch ports found for device {serial}."
                
            # Format the output for readability
            result = f"# Switch Ports for Device ({serial})\n\n"
            for port in ports:
                port_num = port.get('portId', 'Unknown')
                port_name = port.get('name', f'Port {port_num}')
                
                result += f"## {port_name} (Port {port_num})\n"
                result += f"- Enabled: {port.get('enabled', False)}\n"
                result += f"- Type: {port.get('type', 'Unknown')}\n"
                result += f"- VLAN: {port.get('vlan', 'Unknown')}\n"
                
                # Add additional settings
                poe_enabled = port.get('poeEnabled', False)
                result += f"- PoE Enabled: {poe_enabled}\n"
                
                if poe_enabled:
                    result += f"- PoE Type: {port.get('poeType', 'Unknown')}\n"
                
                stp_enabled = port.get('stpEnabled', False)
                result += f"- STP Enabled: {stp_enabled}\n"
                
                # Add access policy if available
                access_policy = port.get('accessPolicy', 'Open')
                result += f"- Access Policy: {access_policy}\n"
                
                result += "\n"
                
            return result
            
        except Exception as e:
            return f"Failed to list switch ports for device {serial}: {str(e)}"


# From tools_switch.py
async def update_device_switch_port(serial: str, port_number: int, name: str = None, enabled: bool = None, 
                                 vlan: int = None, poe_enabled: bool = None):
        """
        Update a switch port for a Meraki switch.
        
        Args:
            serial: Serial number of the switch
            port_number: Number of the port to update
            name: New name for the port (optional)
            enabled: Whether the port should be enabled (optional)
            vlan: VLAN ID for the port (optional)
            poe_enabled: Whether PoE should be enabled (optional)
            
        Returns:
            Updated port details
        """
        return await meraki_client.update_device_switch_port(serial, port_number, name, enabled, vlan, poe_enabled)


# From tools_switch.py
async def get_device_switch_port_statuses(serial: str):
        """
        Get status information for switch ports.
        
        Args:
            serial: Serial number of the switch
            
        Returns:
            Formatted switch port status information
        """
        try:
            statuses = await meraki_client.get_device_switch_port_statuses(serial)
            
            if not statuses:
                return f"No switch port status information found for device {serial}."
                
            # Format the output for readability
            result = f"# Switch Port Statuses for Device ({serial})\n\n"
            for status in statuses:
                port_num = status.get('portId', 'Unknown')
                
                result += f"## Port {port_num}\n"
                result += f"- Status: {status.get('status', 'Unknown')}\n"
                result += f"- Speed: {status.get('speed', 'Unknown')}\n"
                result += f"- Duplex: {status.get('duplex', 'Unknown')}\n"
                
                # Add client details if available
                client = status.get('clientId')
                if client:
                    result += f"- Connected Client: `{client}`\n"
                
                # Add errors if available
                errors = status.get('errors', [])
                if errors:
                    result += "- Errors:\n"
                    for error in errors:
                        result += f"  - {error}\n"
                
                result += "\n"
                
            return result
            
        except Exception as e:
            return f"Failed to get switch port statuses for device {serial}: {str(e)}"


# From tools_switch.py
async def get_device_switch_vlans(serial: str):
        """
        List VLANs for a Meraki switch.
        
        Args:
            serial: Serial number of the switch
            
        Returns:
            Formatted list of VLANs
        """
        try:
            vlans = await meraki_client.get_device_switch_vlans(serial)
            
            if not vlans:
                return f"No VLANs found for device {serial}."
                
            # Format the output for readability
            result = f"# VLANs for Switch ({serial})\n\n"
            for vlan in vlans:
                vlan_id = vlan.get('id', 'Unknown')
                vlan_name = vlan.get('name', f'VLAN {vlan_id}')
                
                result += f"## {vlan_name} (ID: {vlan_id})\n"
                result += f"- Subnet: {vlan.get('subnet', 'Unknown')}\n"
                result += f"- IP Assignment Mode: {vlan.get('ipAssignmentMode', 'Unknown')}\n"
                
                dhcp_options = vlan.get('dhcpOptions', {})
                if dhcp_options:
                    result += "- DHCP Options:\n"
                    for key, value in dhcp_options.items():
                        result += f"  - {key}: {value}\n"
                
                result += "\n"
                
            return result
            
        except Exception as e:
            return f"Failed to list VLANs for device {serial}: {str(e)}"


# From tools_switch.py
async def create_device_switch_vlan(serial: str, vlan_id: int, name: str, subnet: str = None):
        """
        Create a new VLAN for a Meraki switch.
        
        Args:
            serial: Serial number of the switch
            vlan_id: ID for the new VLAN
            name: Name for the new VLAN
            subnet: Subnet for the new VLAN (optional)
            
        Returns:
            New VLAN details
        """
        return await meraki_client.create_device_switch_vlan(serial, vlan_id, name, subnet)


# From tools_analytics.py
async def get_organization_uplinks_loss_and_latency(org_id: str, timespan: int = 300):
        """
        Get REAL packet loss and latency data for all uplinks in organization.
        
        Args:
            org_id: Organization ID
            timespan: Timespan in seconds (default: 300 = 5 minutes, max: 300)
            
        Returns:
            Formatted uplink loss and latency data
        """
        try:
            # Validate and ensure timespan doesn't exceed API limit
            if not isinstance(timespan, (int, float)):
                return "❌ Error: timespan must be a number (seconds)"
            
            if timespan <= 0:
                return "❌ Error: timespan must be positive"
                
            if timespan > 300:
                timespan = 300
                # Note: API limit is 300 seconds (5 minutes)
                
            loss_latency = await meraki_client.get_organization_devices_uplinks_loss_and_latency(org_id, timespan)
            
            if not loss_latency:
                return f"No uplink loss/latency data found for organization {org_id}."
            
            # Build result
            result = f"# 🚨 UPLINK LOSS & LATENCY REPORT\n\n"
            result += f"**Organization**: {org_id}\n"
            result += f"**Time Period**: Last {timespan//60} minutes\n"
            result += f"**Total Uplinks**: {len(loss_latency)}\n\n"
            
            # Group by device serial for easier reading
            devices = {}
            for entry in loss_latency:
                serial = entry.get('serial', 'Unknown')
                if serial not in devices:
                    devices[serial] = {
                        'network_id': entry.get('networkId', 'Unknown'),
                        'uplinks': []
                    }
                devices[serial]['uplinks'].append(entry)
            
            # Format output by device
            for serial, device_data in devices.items():
                result += f"## 📱 Device: {serial}\n"
                result += f"Network: {device_data['network_id']}\n\n"
                
                for uplink in device_data['uplinks']:
                    uplink_name = uplink.get('uplink', 'Unknown')
                    ip = uplink.get('ip', 'N/A')
                    
                    # Check if uplink_name exists before calling upper()
                    if uplink_name:
                        result += f"### 🔗 {uplink_name.upper()} ({ip})\n"
                    else:
                        result += f"### 🔗 Unknown Uplink ({ip})\n"
                    
                    # Get time series data
                    time_series = uplink.get('timeSeries', [])
                    
                    if time_series:
                        # Get latest reading
                        latest = time_series[-1]
                        current_loss = latest.get('lossPercent', 0)
                        current_latency = latest.get('latencyMs', 0)
                        
                        # Calculate statistics
                        losses = [p.get('lossPercent', 0) for p in time_series if p.get('lossPercent') is not None]
                        latencies = [p.get('latencyMs', 0) for p in time_series if p.get('latencyMs') is not None]
                        
                        if losses:
                            avg_loss = sum(losses) / len(losses)
                            max_loss = max(losses)
                            min_loss = min(losses)
                        else:
                            avg_loss = max_loss = min_loss = 0
                            
                        if latencies:
                            avg_latency = sum(latencies) / len(latencies)
                            max_latency = max(latencies)
                            min_latency = min(latencies)
                        else:
                            avg_latency = max_latency = min_latency = 0
                        
                        # Current status with indicators
                        loss_indicator = "🔴" if current_loss > 5 else "🟡" if current_loss > 1 else "🟢"
                        latency_indicator = "🔴" if current_latency > 150 else "🟡" if current_latency > 50 else "🟢"
                        
                        result += f"**Current Status:**\n"
                        result += f"- Packet Loss: {current_loss:.1f}% {loss_indicator}\n"
                        result += f"- Latency: {current_latency:.0f}ms {latency_indicator}\n\n"
                        
                        result += f"**5-Minute Statistics:**\n"
                        result += f"- Avg Loss: {avg_loss:.1f}% (Min: {min_loss:.1f}%, Max: {max_loss:.1f}%)\n"
                        result += f"- Avg Latency: {avg_latency:.0f}ms (Min: {min_latency:.0f}ms, Max: {max_latency:.0f}ms)\n"
                        result += f"- Data Points: {len(time_series)}\n\n"
                        
                        # Show last 5 readings
                        result += f"**Recent Readings:**\n"
                        for reading in time_series[-5:]:
                            ts = reading.get('ts', 'Unknown').split('T')[1].split('Z')[0]
                            loss = reading.get('lossPercent', 0)
                            lat = reading.get('latencyMs', 0)
                            result += f"- {ts}: Loss={loss:.1f}%, Latency={lat:.0f}ms\n"
                        
                        # Alert on issues
                        if avg_loss > 1:
                            result += f"\n⚠️ **WARNING**: Average packet loss above 1%!\n"
                        if avg_latency > 100:
                            result += f"\n⚠️ **WARNING**: High average latency detected!\n"
                            
                    else:
                        result += "- **Status**: No data available\n"
                    
                    result += "\n"
                    
            return result
            
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            return f"Error retrieving uplink loss/latency data:\n{str(e)}\n\nDetails:\n{error_details}"


# From tools_analytics.py
async def get_organization_appliance_uplink_statuses(org_id: str):
        """
        Get REAL uplink status for all appliances in organization.
        
        Args:
            org_id: Organization ID
            
        Returns:
            Formatted appliance uplink status data
        """
        try:
            uplink_statuses = await meraki_client.get_organization_appliance_uplink_statuses(org_id)
            
            if not uplink_statuses:
                return f"No appliance uplink status data found for organization {org_id}."
                
            result = f"# 🔗 APPLIANCE UPLINK STATUS - Organization {org_id}\n\n"
            
            # Group by network
            networks = {}
            for status in uplink_statuses:
                network_id = status.get('networkId', 'Unknown')
                network_name = status.get('networkName', network_id)
                if network_name not in networks:
                    networks[network_name] = []
                networks[network_name].append(status)
            
            for network_name, statuses in networks.items():
                result += f"## 🌐 {network_name}\n"
                
                for status in statuses:
                    serial = status.get('serial', 'Unknown')
                    model = status.get('model', 'Unknown')
                    result += f"### 📱 {model} ({serial})\n"
                    
                    uplinks = status.get('uplinks', [])
                    if not uplinks:
                        result += "- **Status**: No uplink data available\n"
                        continue
                        
                    for uplink in uplinks:
                        interface = uplink.get('interface', 'Unknown')
                        uplink_status = uplink.get('status', 'Unknown')
                        
                        # Status indicators
                        if uplink_status.lower() == 'active':
                            status_icon = "✅"
                        elif uplink_status.lower() == 'ready':
                            status_icon = "🟡"
                        elif uplink_status.lower() in ['failed', 'down']:
                            status_icon = "❌"
                        else:
                            status_icon = "⚠️"
                            
                        result += f"#### 🔗 {interface}: {uplink_status} {status_icon}\n"
                        
                        if uplink.get('ip'):
                            result += f"- **IP**: {uplink['ip']}\n"
                        if uplink.get('gateway'):
                            result += f"- **Gateway**: {uplink['gateway']}\n"
                        if uplink.get('publicIp'):
                            result += f"- **Public IP**: {uplink['publicIp']}\n"
                        if uplink.get('dns'):
                            result += f"- **DNS**: {uplink['dns']}\n"
                        if uplink.get('usingStaticIp'):
                            result += f"- **Static IP**: {uplink['usingStaticIp']}\n"
                        
                        result += "\n"
                        
            return result
            
        except Exception as e:
            error_msg = str(e)
            
            if "404" in error_msg:
                return f"""❌ Error: Organization not found or API not accessible.
                
Organization ID: {org_id}

Possible causes:
- Invalid organization ID
- No API access to this organization
- Organization doesn't have appliances
- API endpoint not available for your license"""
            elif "403" in error_msg:
                return f"""❌ Error: Permission denied.

Possible causes:
- API key doesn't have permission for this organization
- Feature not available for your license tier"""
            else:
                return f"❌ Error retrieving appliance uplink statuses: {error_msg}"


# From tools_analytics.py
async def get_network_connection_stats(network_id: str, timespan: int = 86400):
        """
        Get REAL network connection statistics.
        
        Args:
            network_id: Network ID
            timespan: Timespan in seconds (default: 86400 = 24 hours)
            
        Returns:
            Formatted connection statistics
        """
        try:
            conn_stats = await meraki_client.get_network_connection_stats(network_id, timespan)
            
            if not conn_stats:
                return f"No connection statistics found for network {network_id}."
                
            result = f"# 📊 Connection Statistics for Network {network_id}\n\n"
            result += f"**Time Period**: Last {timespan/3600:.1f} hours\n\n"
            
            # Handle both dict and list responses
            if isinstance(conn_stats, dict):
                # Single summary object
                result += f"## Summary Statistics\n"
                result += f"- **Total Associations**: {conn_stats.get('assoc', 0)}\n"
                result += f"- **Successful Authentications**: {conn_stats.get('auth', 0)}\n"
                result += f"- **DHCP Success**: {conn_stats.get('dhcp', 0)}\n"
                result += f"- **DNS Success**: {conn_stats.get('dns', 0)}\n"
                result += f"- **Overall Success**: {conn_stats.get('success', 0)}\n"
                
                # Check if all values are zero
                total_activity = sum([
                    conn_stats.get('assoc', 0),
                    conn_stats.get('auth', 0),
                    conn_stats.get('dhcp', 0),
                    conn_stats.get('dns', 0),
                    conn_stats.get('success', 0)
                ])
                
                if total_activity == 0:
                    result += f"\n📌 **Note**: No wireless client activity in the specified time period.\n"
                    result += "This could mean:\n"
                    result += "- No wireless clients connected\n"
                    result += "- All clients are wired\n"
                    result += "- The network is idle\n"
                    result += "- Try a longer timespan for more data\n"
                else:
                    # Calculate success rate if possible
                    if conn_stats.get('assoc', 0) > 0:
                        success_rate = (conn_stats.get('success', 0) / conn_stats.get('assoc', 0)) * 100
                        result += f"- **Success Rate**: {success_rate:.1f}%\n"
                        
                        if success_rate < 95:
                            result += f"\n⚠️ **WARNING**: Success rate below 95%!\n"
                        
            elif isinstance(conn_stats, list):
                # Time series data
                for entry in conn_stats:
                    result += f"## {entry.get('startTs', 'Unknown Time')}\n"
                    result += f"- **Successful Connections**: {entry.get('assoc', 'N/A')}\n"
                    result += f"- **Authentication Failures**: {entry.get('authFailures', 'N/A')}\n"
                    result += f"- **DHCP Failures**: {entry.get('dhcpFailures', 'N/A')}\n"
                    result += f"- **DNS Failures**: {entry.get('dnsFailures', 'N/A')}\n"
                    result += f"- **Success Rate**: {entry.get('successRate', 'N/A')}%\n"
                    result += "\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving connection statistics: {str(e)}"


# From tools_analytics.py
async def get_network_latency_stats(network_id: str, timespan: int = 86400):
        """
        Get REAL network latency statistics.
        
        Args:
            network_id: Network ID
            timespan: Timespan in seconds (default: 86400 = 24 hours)
            
        Returns:
            Formatted latency statistics
        """
        try:
            latency_data = await meraki_client.get_network_latency_stats(network_id, timespan)
            
            if not latency_data:
                return f"No latency statistics found for network {network_id}."
                
            result = f"# ⚡ Network Latency Statistics for {network_id}\n\n"
            result += f"**Time Period**: Last {timespan/3600:.1f} hours\n\n"
            
            for entry in latency_data:
                result += f"## {entry.get('startTs', 'Unknown Time')}\n"
                result += f"- **Average Latency**: {entry.get('avgLatencyMs', 'N/A')} ms\n"
                result += f"- **Loss Percentage**: {entry.get('lossPercent', 'N/A')}%\n"
                result += f"- **Jitter**: {entry.get('jitterMs', 'N/A')} ms\n"
                if entry.get('uplink'):
                    result += f"- **Uplink**: {entry['uplink']}\n"
                result += "\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving latency statistics: {str(e)}"


# From tools_alerts.py
async def get_organization_webhooks(org_id: str):
        """
        Get all webhooks configured for an organization.
        
        Args:
            org_id: Organization ID
            
        Returns:
            List of webhooks with their configurations
        """
        try:
            webhooks = await meraki_client.get_organization_webhooks(org_id)
            
            if not webhooks:
                return f"No webhooks found for organization {org_id}."
                
            result = f"# 🔔 Webhooks for Organization {org_id}\n\n"
            
            for webhook in webhooks:
                result += f"## {webhook.get('name', 'Unnamed Webhook')}\n"
                result += f"- **URL**: {webhook.get('url', 'N/A')}\n"
                result += f"- **Shared Secret**: {'***' if webhook.get('sharedSecret') else 'Not set'}\n"
                result += f"- **Network ID**: {webhook.get('networkId', 'All Networks')}\n"
                
                # Alert types
                alert_types = webhook.get('alertTypeIds', [])
                if alert_types:
                    result += f"- **Alert Types**: {', '.join(alert_types)}\n"
                
                result += "\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving webhooks: {str(e)}"


# From tools_alerts.py
async def create_organization_webhook(org_id: str, name: str, url: str, shared_secret: str = None):
        """
        Create a new webhook HTTP server for an organization.
        
        Args:
            org_id: Organization ID
            name: Name of the webhook
            url: URL to send webhooks to
            shared_secret: Optional shared secret for security
            
        Returns:
            Created webhook details
        """
        try:
            webhook_data = {
                'name': name,
                'url': url
            }
            
            if shared_secret:
                webhook_data['sharedSecret'] = shared_secret
                
            webhook = await meraki_client.create_organization_webhook(org_id, **webhook_data)
            
            result = f"# ✅ Webhook Created Successfully\n\n"
            result += f"- **Name**: {webhook.get('name')}\n"
            result += f"- **ID**: {webhook.get('id')}\n"
            result += f"- **URL**: {webhook.get('url')}\n"
            result += f"- **Shared Secret**: {'Set' if webhook.get('sharedSecret') else 'Not set'}\n"
            
            return result
            
        except Exception as e:
            return f"Error creating webhook: {str(e)}"


# From tools_alerts.py
async def get_network_webhook_http_servers(network_id: str):
        """
        Get webhook HTTP servers configured for a network.
        
        Args:
            network_id: Network ID
            
        Returns:
            List of webhook HTTP servers
        """
        try:
            servers = await meraki_client.get_network_webhook_http_servers(network_id)
            
            if not servers:
                return f"No webhook HTTP servers found for network {network_id}."
                
            result = f"# 🌐 Webhook HTTP Servers for Network {network_id}\n\n"
            
            for server in servers:
                result += f"## {server.get('name', 'Unnamed Server')}\n"
                result += f"- **ID**: {server.get('id')}\n"
                result += f"- **URL**: {server.get('url', 'N/A')}\n"
                result += f"- **Shared Secret**: {'***' if server.get('sharedSecret') else 'Not set'}\n"
                
                payload_template = server.get('payloadTemplate')
                if payload_template:
                    result += f"- **Payload Template**: {payload_template.get('name', 'Custom')}\n"
                    
                result += "\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving webhook HTTP servers: {str(e)}"


# From tools_alerts.py
async def create_network_webhook_http_server(network_id: str, name: str, url: str, shared_secret: str = None):
        """
        Create a webhook HTTP server for a network.
        
        Args:
            network_id: Network ID
            name: Name of the webhook server
            url: URL to send webhooks to
            shared_secret: Optional shared secret
            
        Returns:
            Created webhook server details
        """
        try:
            server_data = {
                'name': name,
                'url': url
            }
            
            if shared_secret:
                server_data['sharedSecret'] = shared_secret
                
            server = await meraki_client.create_network_webhook_http_server(network_id, **server_data)
            
            result = f"# ✅ Webhook HTTP Server Created\n\n"
            result += f"- **Name**: {server.get('name')}\n"
            result += f"- **ID**: {server.get('id')}\n"
            result += f"- **URL**: {server.get('url')}\n"
            
            return result
            
        except Exception as e:
            return f"Error creating webhook HTTP server: {str(e)}"


# From tools_alerts.py
async def get_network_alerts_settings(network_id: str):
        """
        Get alert settings for a network.
        
        Args:
            network_id: Network ID
            
        Returns:
            Network alert settings
        """
        try:
            settings = await meraki_client.get_network_alerts_settings(network_id)
            
            result = f"# ⚠️ Alert Settings for Network {network_id}\n\n"
            
            # Default destinations
            default_dest = settings.get('defaultDestinations', {})
            if default_dest:
                result += "## Default Alert Destinations\n"
                
                emails = default_dest.get('emails', [])
                if emails:
                    result += f"- **Emails**: {', '.join(emails)}\n"
                    
                webhooks = default_dest.get('httpServerIds', [])
                if webhooks:
                    result += f"- **Webhook Servers**: {len(webhooks)} configured\n"
                    
                if default_dest.get('allAdmins'):
                    result += "- **All Admins**: ✅ Enabled\n"
                    
                if default_dest.get('snmp'):
                    result += "- **SNMP**: ✅ Enabled\n"
                    
                result += "\n"
            
            # Alert type settings
            alerts = settings.get('alerts', [])
            if alerts:
                result += "## Alert Types Configuration\n"
                for alert in alerts:
                    alert_type = alert.get('type', 'Unknown')
                    enabled = alert.get('enabled', False)
                    result += f"### {alert_type}: {'✅ Enabled' if enabled else '❌ Disabled'}\n"
                    
                    filters = alert.get('filters', {})
                    if filters:
                        result += "  Filters:\n"
                        for key, value in filters.items():
                            result += f"  - {key}: {value}\n"
                            
                    alert_dest = alert.get('alertDestinations', {})
                    if alert_dest:
                        if alert_dest.get('emails'):
                            result += f"  - Emails: {', '.join(alert_dest['emails'])}\n"
                        if alert_dest.get('httpServerIds'):
                            result += f"  - Webhooks: {len(alert_dest['httpServerIds'])} servers\n"
                            
                    result += "\n"
                    
            return result
            
        except Exception as e:
            return f"Error retrieving alert settings: {str(e)}"


# From tools_alerts.py
async def update_network_alerts_settings(network_id: str, emails: str = None, all_admins: bool = None, 
                                     enable_device_down: bool = None, enable_gateway_down: bool = None,
                                     enable_dhcp_failure: bool = None, enable_high_usage: bool = None,
                                     enable_ip_conflict: bool = None):
        """
        Update alert settings for a network.
        
        Args:
            network_id: Network ID
            emails: Comma-separated email addresses for alerts
            all_admins: Send alerts to all admins
            enable_device_down: Enable device down alerts
            enable_gateway_down: Enable gateway connectivity alerts
            enable_dhcp_failure: Enable DHCP failure alerts
            enable_high_usage: Enable high wireless usage alerts
            enable_ip_conflict: Enable IP conflict detection alerts
            
        Returns:
            Updated alert settings
        """
        try:
            update_data = {}
            
            # Set default destinations
            if emails is not None or all_admins is not None:
                default_dest = {}
                
                if emails:
                    default_dest['emails'] = [e.strip() for e in emails.split(',')]
                    
                if all_admins is not None:
                    default_dest['allAdmins'] = all_admins
                    
                update_data['defaultDestinations'] = default_dest
            
            # Configure specific alerts
            alerts = []
            
            # Device down alerts
            if enable_device_down is not None:
                alerts.append({
                    'type': 'gatewayDown',
                    'enabled': enable_device_down,
                    'alertDestinations': {
                        'allAdmins': True
                    }
                })
                alerts.append({
                    'type': 'repeaterDown',
                    'enabled': enable_device_down,
                    'alertDestinations': {
                        'allAdmins': True
                    }
                })
                alerts.append({
                    'type': 'switchDown',
                    'enabled': enable_device_down,
                    'alertDestinations': {
                        'allAdmins': True
                    }
                })
                alerts.append({
                    'type': 'wirelessDown',
                    'enabled': enable_device_down,
                    'alertDestinations': {
                        'allAdmins': True
                    }
                })
            
            # Gateway connectivity issues
            if enable_gateway_down is not None:
                alerts.append({
                    'type': 'vpnConnectivityChange',
                    'enabled': enable_gateway_down,
                    'alertDestinations': {
                        'allAdmins': True
                    }
                })
                alerts.append({
                    'type': 'uplinkStatusChange',
                    'enabled': enable_gateway_down,
                    'alertDestinations': {
                        'allAdmins': True
                    }
                })
            
            # DHCP failures
            if enable_dhcp_failure is not None:
                alerts.append({
                    'type': 'dhcpNoLeases',
                    'enabled': enable_dhcp_failure,
                    'alertDestinations': {
                        'allAdmins': True
                    }
                })
                alerts.append({
                    'type': 'dhcpServerProblem',
                    'enabled': enable_dhcp_failure,
                    'alertDestinations': {
                        'allAdmins': True
                    }
                })
            
            # High wireless usage
            if enable_high_usage is not None:
                alerts.append({
                    'type': 'usageAlert',
                    'enabled': enable_high_usage,
                    'alertDestinations': {
                        'allAdmins': True
                    }
                })
            
            # IP conflict detection
            if enable_ip_conflict is not None:
                alerts.append({
                    'type': 'ipConflict',
                    'enabled': enable_ip_conflict,
                    'alertDestinations': {
                        'allAdmins': True
                    }
                })
            
            if alerts:
                update_data['alerts'] = alerts
                
            settings = await meraki_client.update_network_alerts_settings(network_id, **update_data)
            
            result = "✅ Alert settings updated successfully!\n\n"
            result += "Enabled alerts:\n"
            if enable_device_down:
                result += "- Device down alerts (gateway, repeater, switch, wireless)\n"
            if enable_gateway_down:
                result += "- Gateway connectivity issues (VPN, uplink status)\n"
            if enable_dhcp_failure:
                result += "- DHCP failures (no leases, server problems)\n"
            if enable_high_usage:
                result += "- High wireless usage\n"
            if enable_ip_conflict:
                result += "- IP conflict detection\n"
            
            return result
            
        except Exception as e:
            return f"Error updating alert settings: {str(e)}"


# From tools_appliance.py
async def get_network_appliance_firewall_l3_rules(network_id: str):
        """
        Get Layer 3 firewall rules for a network appliance.
        
        Args:
            network_id: Network ID
            
        Returns:
            Formatted L3 firewall rules
        """
        try:
            rules = await meraki_client.get_network_appliance_firewall_l3_rules(network_id)
            
            if not rules or not rules.get('rules'):
                return f"No L3 firewall rules found for network {network_id}."
                
            result = f"# 🔥 Layer 3 Firewall Rules for Network {network_id}\n\n"
            
            for idx, rule in enumerate(rules.get('rules', []), 1):
                result += f"## Rule {idx}: {rule.get('comment', 'No comment')}\n"
                result += f"- **Policy**: {rule.get('policy', 'N/A')}\n"
                result += f"- **Protocol**: {rule.get('protocol', 'any')}\n"
                result += f"- **Source**: {rule.get('srcCidr', 'any')}\n"
                
                if rule.get('srcPort'):
                    result += f"- **Source Port**: {rule['srcPort']}\n"
                    
                result += f"- **Destination**: {rule.get('destCidr', 'any')}\n"
                
                if rule.get('destPort'):
                    result += f"- **Destination Port**: {rule['destPort']}\n"
                    
                result += f"- **Syslog**: {'✅ Enabled' if rule.get('syslogEnabled') else '❌ Disabled'}\n"
                result += "\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving L3 firewall rules: {str(e)}"


# From tools_appliance.py
async def update_network_appliance_firewall_l3_rules(
        network_id: str, 
        comment: str,
        policy: str,
        protocol: str = "any",
        src_cidr: str = "any",
        dest_cidr: str = "any",
        dest_port: str = None,
        syslog_enabled: bool = False
    ):
        """
        Add a new L3 firewall rule to a network (existing rules are preserved).
        
        Args:
            network_id: Network ID
            comment: Description of the rule
            policy: 'allow' or 'deny'
            protocol: 'tcp', 'udp', 'icmp', or 'any'
            src_cidr: Source CIDR (e.g., '192.168.1.0/24')
            dest_cidr: Destination CIDR
            dest_port: Destination port (optional)
            syslog_enabled: Enable syslog for this rule
            
        Returns:
            Updated firewall rules
        """
        try:
            # Get existing rules first
            current = await meraki_client.get_network_appliance_firewall_l3_rules(network_id)
            existing_rules = current.get('rules', [])
            
            # Create new rule
            new_rule = {
                'comment': comment,
                'policy': policy,
                'protocol': protocol,
                'srcCidr': src_cidr,
                'destCidr': dest_cidr,
                'syslogEnabled': syslog_enabled
            }
            
            if dest_port:
                new_rule['destPort'] = dest_port
                
            # Add new rule to beginning (processed first)
            updated_rules = [new_rule] + existing_rules
            
            # Update firewall rules
            result = await meraki_client.update_network_appliance_firewall_l3_rules(
                network_id,
                rules=updated_rules
            )
            
            return f"✅ Firewall rule added successfully!\n\nNew rule: {comment}\nPolicy: {policy}\nTotal rules: {len(updated_rules)}"
            
        except Exception as e:
            return f"Error updating L3 firewall rules: {str(e)}"


# From tools_appliance.py
async def get_network_appliance_content_filtering(network_id: str):
        """
        Get content filtering settings for a network appliance.
        
        Args:
            network_id: Network ID
            
        Returns:
            Content filtering configuration
        """
        try:
            filtering = await meraki_client.get_network_appliance_content_filtering(network_id)
            
            result = f"# 🌐 Content Filtering for Network {network_id}\n\n"
            
            # Blocked URL categories
            blocked_categories = filtering.get('blockedUrlCategories', [])
            if blocked_categories:
                result += "## Blocked Categories\n"
                for category in blocked_categories:
                    result += f"- {category}\n"
                result += "\n"
                
            # Blocked URL patterns
            blocked_patterns = filtering.get('blockedUrlPatterns', [])
            if blocked_patterns:
                result += "## Blocked URL Patterns\n"
                for pattern in blocked_patterns:
                    result += f"- {pattern}\n"
                result += "\n"
                
            # Allowed URL patterns
            allowed_patterns = filtering.get('allowedUrlPatterns', [])
            if allowed_patterns:
                result += "## Allowed URL Patterns\n"
                for pattern in allowed_patterns:
                    result += f"- {pattern}\n"
                result += "\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving content filtering settings: {str(e)}"


# From tools_appliance.py
async def get_network_appliance_vpn_site_to_site(network_id: str):
        """
        Get site-to-site VPN settings for a network appliance.
        
        Args:
            network_id: Network ID
            
        Returns:
            Site-to-site VPN configuration
        """
        try:
            vpn = await meraki_client.get_network_appliance_vpn_site_to_site(network_id)
            
            result = f"# 🔐 Site-to-Site VPN for Network {network_id}\n\n"
            
            mode = vpn.get('mode', 'none')
            result += f"**Mode**: {mode}\n\n"
            
            if mode != 'none':
                # Hubs (for spoke mode)
                hubs = vpn.get('hubs', [])
                if hubs:
                    result += "## VPN Hubs\n"
                    for hub in hubs:
                        result += f"- Hub ID: {hub.get('hubId')}\n"
                        result += f"  Default route: {'✅' if hub.get('useDefaultRoute') else '❌'}\n"
                    result += "\n"
                    
                # Subnets
                subnets = vpn.get('subnets', [])
                if subnets:
                    result += "## Local Subnets in VPN\n"
                    for subnet in subnets:
                        result += f"- {subnet.get('localSubnet')}"
                        if subnet.get('useVpn'):
                            result += " ✅ In VPN"
                        else:
                            result += " ❌ Not in VPN"
                        result += "\n"
                    result += "\n"
                    
            return result
            
        except Exception as e:
            return f"Error retrieving site-to-site VPN settings: {str(e)}"


# From tools_appliance.py
async def get_network_appliance_security_malware(network_id: str):
        """
        Get malware protection settings for a network appliance.
        
        Args:
            network_id: Network ID
            
        Returns:
            Malware protection configuration
        """
        try:
            malware = await meraki_client.get_network_appliance_security_malware(network_id)
            
            result = f"# 🛡️ Malware Protection for Network {network_id}\n\n"
            
            mode = malware.get('mode', 'disabled')
            result += f"**Mode**: {mode}\n"
            
            if mode == 'enabled':
                result += "✅ Malware protection is ACTIVE\n"
                
                # Allowed URLs
                allowed_urls = malware.get('allowedUrls', [])
                if allowed_urls:
                    result += "\n## Allowed URLs (Whitelist)\n"
                    for url in allowed_urls:
                        result += f"- {url.get('url')} - {url.get('comment', 'No comment')}\n"
                        
                # Allowed files
                allowed_files = malware.get('allowedFiles', [])
                if allowed_files:
                    result += "\n## Allowed Files (by SHA256)\n"
                    for file in allowed_files:
                        result += f"- {file.get('sha256')[:16]}... - {file.get('comment', 'No comment')}\n"
            else:
                result += "❌ Malware protection is DISABLED\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving malware protection settings: {str(e)}"


# From tools_appliance.py
async def get_network_appliance_security_intrusion(network_id: str):
        """
        Get intrusion detection and prevention settings for a network.
        
        Args:
            network_id: Network ID
            
        Returns:
            IDS/IPS configuration
        """
        try:
            intrusion = await meraki_client.get_network_appliance_security_intrusion(network_id)
            
            result = f"# 🚨 Intrusion Detection/Prevention for Network {network_id}\n\n"
            
            mode = intrusion.get('mode', 'disabled')
            result += f"**Mode**: {mode}\n"
            
            if mode != 'disabled':
                result += f"✅ IDS/IPS is ACTIVE in {mode.upper()} mode\n"
                
                # IDS rulesets
                ids_rulesets = intrusion.get('idsRulesets', 'balanced')
                result += f"\n**Ruleset**: {ids_rulesets}\n"
                
                # Protected networks
                protected = intrusion.get('protectedNetworks', {})
                use_default = protected.get('useDefault', True)
                
                if use_default:
                    result += "\n**Protected Networks**: Using default (all local networks)\n"
                else:
                    included = protected.get('includedCidr', [])
                    excluded = protected.get('excludedCidr', [])
                    
                    if included:
                        result += "\n**Protected Networks**:\n"
                        for cidr in included:
                            result += f"- ✅ {cidr}\n"
                            
                    if excluded:
                        result += "\n**Excluded Networks**:\n"
                        for cidr in excluded:
                            result += f"- ❌ {cidr}\n"
            else:
                result += "❌ IDS/IPS is DISABLED\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving intrusion detection settings: {str(e)}"


# From tools_camera.py
async def get_device_camera_video_link(serial: str, timestamp: str = None):
        """
        Get video link for a camera device.
        
        Args:
            serial: Device serial number
            timestamp: Optional timestamp (ISO 8601) for historical footage
            
        Returns:
            Video link URL
        """
        try:
            link_info = await meraki_client.get_device_camera_video_link(serial, timestamp)
            
            result = f"# 📹 Camera Video Link for {serial}\n\n"
            result += f"**Video URL**: {link_info.get('url', 'Not available')}\n"
            
            if timestamp:
                result += f"**Timestamp**: {timestamp}\n"
            else:
                result += "**Type**: Live stream\n"
                
            expiry = link_info.get('expiresAt')
            if expiry:
                result += f"**Expires**: {expiry}\n"
                
            result += "\n⚠️ This link is temporary and will expire. Do not share publicly."
            
            return result
            
        except Exception as e:
            return f"Error retrieving camera video link: {str(e)}"


# From tools_camera.py
async def get_device_camera_snapshot(serial: str, timestamp: str = None):
        """
        Generate a snapshot from a camera.
        
        Args:
            serial: Device serial number
            timestamp: Optional timestamp (ISO 8601) for historical snapshot
            
        Returns:
            Snapshot URL
        """
        try:
            snapshot = await meraki_client.get_device_camera_snapshot(serial, timestamp)
            
            result = f"# 📸 Camera Snapshot for {serial}\n\n"
            result += f"**Snapshot URL**: {snapshot.get('url', 'Not available')}\n"
            
            if timestamp:
                result += f"**Timestamp**: {timestamp}\n"
            else:
                result += "**Type**: Current snapshot\n"
                
            expiry = snapshot.get('expiresAt')
            if expiry:
                result += f"**Expires**: {expiry}\n"
                
            result += "\n⚠️ This link is temporary and will expire. Download promptly if needed."
            
            return result
            
        except Exception as e:
            return f"Error generating camera snapshot: {str(e)}"


# From tools_camera.py
async def get_device_camera_video_settings(serial: str):
        """
        Get video settings for a camera device.
        
        Args:
            serial: Device serial number
            
        Returns:
            Camera video settings
        """
        try:
            settings = await meraki_client.get_device_camera_video_settings(serial)
            
            result = f"# ⚙️ Video Settings for Camera {serial}\n\n"
            
            # External RTSP
            external_rtsp = settings.get('externalRtspEnabled')
            if external_rtsp is not None:
                result += f"**External RTSP**: {'✅ Enabled' if external_rtsp else '❌ Disabled'}\n"
                
            # RTSP URL if enabled
            rtsp_url = settings.get('rtspUrl')
            if rtsp_url:
                result += f"**RTSP URL**: `{rtsp_url}`\n"
                
            result += "\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving camera video settings: {str(e)}"


# From tools_camera.py
async def update_device_camera_video_settings(serial: str, external_rtsp_enabled: bool):
        """
        Update video settings for a camera device.
        
        Args:
            serial: Device serial number
            external_rtsp_enabled: Enable/disable external RTSP access
            
        Returns:
            Updated video settings
        """
        try:
            settings = await meraki_client.update_device_camera_video_settings(
                serial,
                externalRtspEnabled=external_rtsp_enabled
            )
            
            result = f"# ✅ Video Settings Updated for Camera {serial}\n\n"
            result += f"**External RTSP**: {'✅ Enabled' if external_rtsp_enabled else '❌ Disabled'}\n"
            
            if external_rtsp_enabled and settings.get('rtspUrl'):
                result += f"\n**RTSP URL**: `{settings['rtspUrl']}`\n"
                result += "\n⚠️ Use this URL with VLC or other RTSP-compatible video players."
                
            return result
            
        except Exception as e:
            return f"Error updating camera video settings: {str(e)}"


# From tools_camera.py
async def get_device_camera_analytics_zones(serial: str):
        """
        Get analytics zones configured on a camera.
        
        Args:
            serial: Device serial number
            
        Returns:
            Camera analytics zones configuration
        """
        try:
            zones = await meraki_client.get_device_camera_analytics_zones(serial)
            
            if not zones:
                return f"No analytics zones configured for camera {serial}."
                
            result = f"# 📊 Analytics Zones for Camera {serial}\n\n"
            
            for idx, zone in enumerate(zones, 1):
                zone_id = zone.get('zoneId', f'Zone {idx}')
                zone_type = zone.get('type', 'Unknown')
                label = zone.get('label', 'Unlabeled')
                
                result += f"## {label} (ID: {zone_id})\n"
                result += f"- **Type**: {zone_type}\n"
                
                # Region vertices
                region = zone.get('regionOfInterest', {})
                vertices = region.get('vertices', [])
                if vertices:
                    result += f"- **Vertices**: {len(vertices)} points\n"
                    
                result += "\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving camera analytics zones: {str(e)}"


# From tools_camera.py
async def get_device_camera_sense(serial: str):
        """
        Get motion detection (sense) settings for a camera.
        
        Args:
            serial: Device serial number
            
        Returns:
            Camera motion detection settings
        """
        try:
            sense = await meraki_client.get_device_camera_sense(serial)
            
            result = f"# 🎯 Motion Detection Settings for Camera {serial}\n\n"
            
            # Motion detection enabled
            detection_enabled = sense.get('detectionEnabled')
            if detection_enabled is not None:
                result += f"**Motion Detection**: {'✅ Enabled' if detection_enabled else '❌ Disabled'}\n"
                
            # Audio detection
            audio_detection = sense.get('audioDetection', {})
            if audio_detection:
                audio_enabled = audio_detection.get('enabled', False)
                result += f"**Audio Detection**: {'✅ Enabled' if audio_enabled else '❌ Disabled'}\n"
                
            # MQTT broker
            mqtt_broker_id = sense.get('mqttBrokerId')
            if mqtt_broker_id:
                result += f"**MQTT Broker ID**: {mqtt_broker_id}\n"
                
            result += "\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving camera sense settings: {str(e)}"


# From tools_sm.py
async def get_network_sm_devices(network_id: str):
        """
        List all devices enrolled in Systems Manager for a network.
        
        Args:
            network_id: Network ID
            
        Returns:
            List of SM devices with details
        """
        try:
            devices = await meraki_client.get_network_sm_devices(network_id)
            
            if not devices:
                return f"No Systems Manager devices found in network {network_id}."
                
            result = f"# 📱 Systems Manager Devices - Network {network_id}\n\n"
            result += f"**Total Devices**: {len(devices)}\n\n"
            
            # Group by OS
            os_groups = {}
            for device in devices:
                os_name = device.get('osName', 'Unknown')
                if os_name not in os_groups:
                    os_groups[os_name] = []
                os_groups[os_name].append(device)
            
            for os_name, os_devices in os_groups.items():
                result += f"## {os_name} ({len(os_devices)} devices)\n"
                
                for device in os_devices[:10]:  # Show first 10 per OS
                    name = device.get('name', 'Unnamed')
                    serial = device.get('serialNumber', device.get('id', 'Unknown'))
                    model = device.get('systemModel', 'Unknown')
                    
                    result += f"### 📱 {name}\n"
                    result += f"- **Serial/ID**: {serial}\n"
                    result += f"- **Model**: {model}\n"
                    result += f"- **User**: {device.get('ownerEmail', device.get('ownerUsername', 'Unknown'))}\n"
                    
                    # Status indicators
                    wifi_mac = device.get('wifiMac')
                    if wifi_mac:
                        result += f"- **WiFi MAC**: {wifi_mac}\n"
                        result += f"- **Last SSID**: {device.get('ssid', 'Not connected')}\n"
                    
                    # Battery if available
                    battery = device.get('batteryEstCharge')
                    if battery:
                        battery_icon = "🔋" if battery > 50 else "🪫" if battery > 20 else "🔴"
                        result += f"- **Battery**: {battery_icon} {battery}%\n"
                    
                    # Tags
                    tags = device.get('tags', [])
                    if tags:
                        result += f"- **Tags**: {', '.join(tags)}\n"
                        
                    result += "\n"
                
                if len(os_devices) > 10:
                    result += f"... and {len(os_devices) - 10} more {os_name} devices\n\n"
                    
            return result
            
        except Exception as e:
            return f"Error retrieving SM devices: {str(e)}"


# From tools_sm.py
async def get_network_sm_device_detail(network_id: str, device_id: str):
        """
        Get detailed information for a specific Systems Manager device.
        
        Args:
            network_id: Network ID
            device_id: Device ID or serial number
            
        Returns:
            Detailed device information
        """
        try:
            device = await meraki_client.get_network_sm_device(network_id, device_id)
            
            result = f"# 📱 SM Device Details: {device.get('name', 'Unknown')}\n\n"
            
            # Basic Info
            result += "## Device Information\n"
            result += f"- **Serial/ID**: {device.get('serialNumber', device.get('id'))}\n"
            result += f"- **Model**: {device.get('systemModel', 'Unknown')}\n"
            result += f"- **OS**: {device.get('osName', 'Unknown')} {device.get('systemVersion', '')}\n"
            result += f"- **UUID**: {device.get('uuid', 'N/A')}\n"
            
            # User Info
            result += "\n## User Information\n"
            result += f"- **Owner**: {device.get('ownerEmail', device.get('ownerUsername', 'Unknown'))}\n"
            result += f"- **User Email**: {device.get('userEmail', 'N/A')}\n"
            
            # Network Info
            result += "\n## Network Status\n"
            result += f"- **WiFi MAC**: {device.get('wifiMac', 'N/A')}\n"
            result += f"- **Last SSID**: {device.get('ssid', 'Not connected')}\n"
            result += f"- **IP**: {device.get('ip', 'N/A')}\n"
            result += f"- **Has Cellular**: {'✅' if device.get('hasCellular') else '❌'}\n"
            
            # Security Status
            result += "\n## Security Status\n"
            result += f"- **Managed**: {'✅' if device.get('managed') else '❌'}\n"
            result += f"- **Supervised**: {'✅' if device.get('isSupervised') else '❌'}\n"
            
            # Battery if available
            battery = device.get('batteryEstCharge')
            if battery:
                battery_icon = "🔋" if battery > 50 else "🪫" if battery > 20 else "🔴"
                result += f"- **Battery**: {battery_icon} {battery}%\n"
            
            # Storage
            disk_info = device.get('diskInfo')
            if disk_info:
                result += f"\n## Storage\n"
                for disk in disk_info:
                    used = disk.get('used', 0)
                    size = disk.get('size', 1)
                    percent = (used / size * 100) if size > 0 else 0
                    result += f"- **{disk.get('name', 'Disk')}**: {percent:.1f}% used ({used}GB/{size}GB)\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving SM device details: {str(e)}"


# From tools_sm.py
async def get_network_sm_device_apps(network_id: str, device_id: str):
        """
        List all apps installed on a Systems Manager device.
        
        Args:
            network_id: Network ID
            device_id: Device ID or serial number
            
        Returns:
            List of installed applications
        """
        try:
            apps = await meraki_client.get_network_sm_device_apps(network_id, device_id)
            
            if not apps:
                return f"No apps found on device {device_id}."
                
            result = f"# 📲 Installed Apps on Device {device_id}\n\n"
            result += f"**Total Apps**: {len(apps)}\n\n"
            
            # Group by app status
            managed_apps = [app for app in apps if app.get('isManaged')]
            other_apps = [app for app in apps if not app.get('isManaged')]
            
            if managed_apps:
                result += "## 🏢 Managed Apps\n"
                for app in managed_apps[:20]:
                    result += f"- **{app.get('name', 'Unknown')}** v{app.get('version', '?')}\n"
                    result += f"  - Bundle ID: {app.get('bundleId', 'N/A')}\n"
                    result += f"  - Size: {app.get('bundleSize', 0) / 1024 / 1024:.1f} MB\n"
                    if app.get('isVppApp'):
                        result += "  - VPP App ✅\n"
                    result += "\n"
                    
            if other_apps:
                result += "## 📱 Other Apps\n"
                for app in other_apps[:20]:
                    result += f"- **{app.get('name', 'Unknown')}** v{app.get('version', '?')}\n"
                    
            if len(apps) > 40:
                result += f"\n... and {len(apps) - 40} more apps\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving device apps: {str(e)}"


# From tools_sm.py
async def reboot_network_sm_devices(network_id: str, device_ids: str):
        """
        Reboot one or more Systems Manager devices.
        
        ⚠️ WARNING: This will force devices to restart!
        
        Args:
            network_id: Network ID
            device_ids: Comma-separated device IDs to reboot
            
        Returns:
            Reboot command status
        """
        try:
            ids_list = [id.strip() for id in device_ids.split(',')]
            device_count = len(ids_list)
            
            # Import helper function
            from utils.helpers import require_confirmation
            
            # Require confirmation
            if not require_confirmation(
                operation_type="reboot",
                resource_type="SM devices",
                resource_name=f"{device_count} device(s) in network {network_id}",
                resource_id=f"Network: {network_id}"
            ):
                return "❌ SM device reboot cancelled by user"
            
            # Perform reboot
            result = await meraki_client.reboot_network_sm_devices(network_id, ids=ids_list)
            
            response = f"""✅ SM REBOOT COMMAND SENT

**Network**: {network_id}
**Devices rebooted**: {len(ids_list)}
**Device IDs**: {', '.join(ids_list)}
**Command ID**: {result.get('id', 'N/A')}

The reboot command has been sent to all devices. They will restart shortly."""
            
            return response
            
        except Exception as e:
            return f"❌ Error sending reboot command: {str(e)}"




# From tools_sm.py
async def get_network_sm_profiles(network_id: str):
        """
        List all Systems Manager profiles for a network.
        
        Args:
            network_id: Network ID
            
        Returns:
            List of SM profiles
        """
        try:
            profiles = await meraki_client.get_network_sm_profiles(network_id)
            
            if not profiles:
                return f"No SM profiles found in network {network_id}."
                
            result = f"# 📋 Systems Manager Profiles - Network {network_id}\n\n"
            
            for profile in profiles:
                result += f"## {profile.get('name', 'Unnamed Profile')}\n"
                result += f"- **ID**: {profile.get('id')}\n"
                result += f"- **Description**: {profile.get('description', 'No description')}\n"
                result += f"- **Scope**: {profile.get('scope', 'Unknown')}\n"
                
                # Tags targeted
                tags = profile.get('tags', [])
                if tags:
                    result += f"- **Target Tags**: {', '.join(tags)}\n"
                    
                # Payload count
                payloads = profile.get('payloadTypes', [])
                if payloads:
                    result += f"- **Payload Types**: {', '.join(payloads)}\n"
                    
                result += "\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving SM profiles: {str(e)}"


# From tools_sm.py
async def get_network_sm_performance_history(network_id: str, device_id: str):
        """
        Get performance history for a Systems Manager device.
        
        Args:
            network_id: Network ID
            device_id: Device ID
            
        Returns:
            Device performance metrics over time
        """
        try:
            history = await meraki_client.get_network_sm_device_performance_history(network_id, device_id)
            
            if not history:
                return f"No performance history found for device {device_id}."
                
            result = f"# 📊 Performance History - Device {device_id}\n\n"
            
            for entry in history[-10:]:  # Last 10 entries
                timestamp = entry.get('ts', 'Unknown time')
                result += f"## {timestamp}\n"
                
                # CPU usage
                cpu_percent = entry.get('cpuPercentUsed')
                if cpu_percent is not None:
                    cpu_icon = "🟢" if cpu_percent < 50 else "🟡" if cpu_percent < 80 else "🔴"
                    result += f"- **CPU Usage**: {cpu_icon} {cpu_percent}%\n"
                
                # Memory usage
                mem_free = entry.get('memFree', 0)
                mem_active = entry.get('memActive', 0)
                mem_inactive = entry.get('memInactive', 0)
                mem_wired = entry.get('memWired', 0)
                
                if mem_free or mem_active:
                    total_mem = mem_free + mem_active + mem_inactive + mem_wired
                    if total_mem > 0:
                        mem_percent = ((mem_active + mem_wired) / total_mem) * 100
                        mem_icon = "🟢" if mem_percent < 70 else "🟡" if mem_percent < 90 else "🔴"
                        result += f"- **Memory**: {mem_icon} {mem_percent:.1f}% used\n"
                        result += f"  - Free: {mem_free}MB\n"
                        result += f"  - Active: {mem_active}MB\n"
                
                # Disk usage
                disk_usage = entry.get('diskUsage', {})
                if disk_usage:
                    for disk, usage in disk_usage.items():
                        used = usage.get('used', 0)
                        total = usage.get('total', 1)
                        percent = (used / total * 100) if total > 0 else 0
                        disk_icon = "🟢" if percent < 80 else "🟡" if percent < 90 else "🔴"
                        result += f"- **Disk {disk}**: {disk_icon} {percent:.1f}% used\n"
                
                # Network usage
                network_sent = entry.get('networkSent', 0)
                network_recv = entry.get('networkReceived', 0)
                if network_sent or network_recv:
                    result += f"- **Network**: ↑{network_sent}KB ↓{network_recv}KB\n"
                
                result += "\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving performance history: {str(e)}"


# From tools_licensing.py
async def get_organization_licenses(org_id: str):
        """
        List all licenses for an organization.
        
        Args:
            org_id: Organization ID
            
        Returns:
            List of licenses with details
        """
        try:
            licenses = await meraki_client.get_organization_licenses(org_id)
            
            if not licenses:
                return f"No licenses found for organization {org_id}."
                
            result = f"# 📄 Organization Licenses - Org {org_id}\n\n"
            result += f"**Total Licenses**: {len(licenses)}\n\n"
            
            # Group by device type
            device_types = {}
            for license in licenses:
                device_type = license.get('deviceType', 'Unknown')
                if device_type not in device_types:
                    device_types[device_type] = []
                device_types[device_type].append(license)
            
            # Display by device type
            for device_type, type_licenses in device_types.items():
                result += f"## {device_type} Licenses ({len(type_licenses)})\n"
                
                # Count active vs expired
                active = sum(1 for lic in type_licenses if lic.get('state') == 'active')
                expired = sum(1 for lic in type_licenses if lic.get('state') == 'expired')
                unused = sum(1 for lic in type_licenses if lic.get('state') == 'unused')
                
                result += f"- **Active**: {active}\n"
                result += f"- **Expired**: {expired}\n"
                result += f"- **Unused**: {unused}\n\n"
                
                # Show details for first few
                for license in type_licenses[:5]:
                    lic_key = license.get('licenseKey', 'Unknown')
                    state = license.get('state', 'unknown')
                    state_icon = "✅" if state == 'active' else "⏰" if state == 'expired' else "📦"
                    
                    result += f"### {state_icon} License {lic_key[-8:]}\n"
                    result += f"- **State**: {state}\n"
                    result += f"- **Order Number**: {license.get('orderNumber', 'N/A')}\n"
                    
                    # Expiration info
                    expiration = license.get('expirationDate')
                    if expiration:
                        result += f"- **Expires**: {expiration}\n"
                    
                    # Device assignment
                    device_serial = license.get('deviceSerial')
                    if device_serial:
                        result += f"- **Assigned to**: {device_serial}\n"
                    
                    # Duration
                    duration = license.get('durationInDays')
                    if duration:
                        result += f"- **Duration**: {duration} days\n"
                    
                    result += "\n"
                
                if len(type_licenses) > 5:
                    result += f"... and {len(type_licenses) - 5} more {device_type} licenses\n\n"
                    
            return result
            
        except Exception as e:
            return f"Error retrieving licenses: {str(e)}"


# From tools_licensing.py
async def get_organization_licensing_coterm(org_id: str):
        """
        Get co-termination licensing model information.
        
        Args:
            org_id: Organization ID
            
        Returns:
            Co-term licensing details
        """
        try:
            coterm = await meraki_client.get_organization_licensing_coterm_licenses(org_id)
            
            result = f"# 📊 Co-Termination Licensing - Org {org_id}\n\n"
            
            # Check if expired
            expired = coterm.get('expired', False)
            if expired:
                result += "⚠️ **WARNING: Co-term licenses are expired!**\n\n"
            
            # Overall counts
            counts = coterm.get('counts', [])
            if counts:
                result += "## License Counts by Model\n"
                total_count = 0
                for count in counts:
                    model = count.get('model', 'Unknown')
                    qty = count.get('count', 0)
                    total_count += qty
                    result += f"- **{model}**: {qty} licenses\n"
                result += f"\n**Total Devices**: {total_count}\n\n"
            
            # Expiration dates
            expiration_date = coterm.get('expirationDate')
            if expiration_date:
                result += f"## Expiration\n"
                result += f"**All licenses expire on**: {expiration_date}\n\n"
            
            # Invalid devices
            invalid = coterm.get('invalidSerials', [])
            if invalid:
                result += f"## ⚠️ Invalid Devices ({len(invalid)})\n"
                result += "These devices have invalid licenses:\n"
                for serial in invalid[:10]:
                    result += f"- {serial}\n"
                if len(invalid) > 10:
                    result += f"... and {len(invalid) - 10} more\n"
                result += "\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving co-term licensing info: {str(e)}"


# From tools_licensing.py
async def claim_organization_license(org_id: str, license_key: str):
        """
        Claim a new license key for an organization.
        
        Args:
            org_id: Organization ID
            license_key: License key to claim
            
        Returns:
            Claim result
        """
        try:
            result = await meraki_client.claim_organization_license(org_id, licenseKey=license_key)
            
            response = f"# 🔑 License Claimed Successfully\n\n"
            response += f"**License Key**: {license_key}\n"
            response += f"**Organization**: {org_id}\n\n"
            
            # Display claimed license info if returned
            if isinstance(result, dict):
                if result.get('licenseKey'):
                    response += f"## License Details\n"
                    response += f"- **Type**: {result.get('deviceType', 'Unknown')}\n"
                    response += f"- **State**: {result.get('state', 'Unknown')}\n"
                    response += f"- **Duration**: {result.get('durationInDays', 'N/A')} days\n"
                    
                    expiration = result.get('expirationDate')
                    if expiration:
                        response += f"- **Expires**: {expiration}\n"
            
            return response
            
        except Exception as e:
            return f"Error claiming license: {str(e)}"


# From tools_licensing.py
async def update_organization_license(org_id: str, license_id: str, device_serial: str = None):
        """
        Update a license (typically to assign/unassign to a device).
        
        Args:
            org_id: Organization ID
            license_id: License ID to update
            device_serial: Device serial to assign to (or empty to unassign)
            
        Returns:
            Update result
        """
        try:
            kwargs = {}
            if device_serial:
                kwargs['deviceSerial'] = device_serial
            else:
                # Unassign by setting to empty string
                kwargs['deviceSerial'] = ""
                
            result = await meraki_client.update_organization_license(org_id, license_id, **kwargs)
            
            response = f"# 📝 License Updated\n\n"
            response += f"**License ID**: {license_id}\n"
            
            if device_serial:
                response += f"**Assigned to**: {device_serial}\n"
            else:
                response += "**Status**: Unassigned from device\n"
                
            return response
            
        except Exception as e:
            return f"Error updating license: {str(e)}"


# From tools_licensing.py
async def move_organization_licenses(source_org_id: str, dest_org_id: str, license_ids: str):
        """
        Move licenses from one organization to another.
        
        Args:
            source_org_id: Source organization ID
            dest_org_id: Destination organization ID
            license_ids: Comma-separated license IDs to move
            
        Returns:
            Move result
        """
        try:
            ids_list = [id.strip() for id in license_ids.split(',')]
            
            result = await meraki_client.move_organization_licenses(
                source_org_id,
                destOrganizationId=dest_org_id,
                licenseIds=ids_list
            )
            
            response = f"# 🔄 Licenses Moved\n\n"
            response += f"**From Organization**: {source_org_id}\n"
            response += f"**To Organization**: {dest_org_id}\n"
            response += f"**Number of Licenses**: {len(ids_list)}\n\n"
            
            response += "✅ Licenses successfully transferred to the destination organization.\n"
            
            return response
            
        except Exception as e:
            return f"Error moving licenses: {str(e)}"


# From tools_licensing.py
async def renew_organization_licenses_seats(org_id: str, license_id_to_renew: str, unused_license_id: str):
        """
        Renew Systems Manager seats by combining licenses.
        
        Args:
            org_id: Organization ID
            license_id_to_renew: License ID that needs renewal
            unused_license_id: Unused license ID to apply for renewal
            
        Returns:
            Renewal result
        """
        try:
            result = await meraki_client.renew_organization_licenses_seats(
                org_id,
                licenseIdToRenew=license_id_to_renew,
                unusedLicenseId=unused_license_id
            )
            
            response = f"# 🔄 SM Seats Renewed\n\n"
            response += f"**Renewed License**: {license_id_to_renew}\n"
            response += f"**Using License**: {unused_license_id}\n\n"
            
            if isinstance(result, dict):
                response += f"## Result\n"
                response += f"- **New Expiration**: {result.get('expirationDate', 'N/A')}\n"
                response += f"- **Seat Count**: {result.get('seatCount', 'N/A')}\n"
            
            return response
            
        except Exception as e:
            return f"Error renewing SM seats: {str(e)}"


# From tools_policy.py
async def get_organization_policy_objects(org_id: str):
        """
        List all policy objects for an organization.
        
        Args:
            org_id: Organization ID
            
        Returns:
            List of policy objects
        """
        try:
            objects = await meraki_client.get_organization_policy_objects(org_id)
            
            if not objects:
                return f"No policy objects found for organization {org_id}."
                
            result = f"# 🛡️ Policy Objects - Organization {org_id}\n\n"
            result += f"**Total Objects**: {len(objects)}\n\n"
            
            # Group by category
            categories = {}
            for obj in objects:
                category = obj.get('category', 'uncategorized')
                if category not in categories:
                    categories[category] = []
                categories[category].append(obj)
            
            # Display by category
            for category, cat_objects in categories.items():
                result += f"## {category.title()} ({len(cat_objects)} objects)\n"
                
                for obj in cat_objects[:10]:
                    obj_id = obj.get('id', 'Unknown')
                    name = obj.get('name', 'Unnamed')
                    obj_type = obj.get('type', 'unknown')
                    
                    result += f"### 🔸 {name}\n"
                    result += f"- **ID**: {obj_id}\n"
                    result += f"- **Type**: {obj_type}\n"
                    
                    # Type-specific details
                    if obj_type == 'ipv4':
                        cidr = obj.get('cidr')
                        if cidr:
                            result += f"- **CIDR**: {cidr}\n"
                    elif obj_type == 'fqdn':
                        fqdn = obj.get('fqdn')
                        if fqdn:
                            result += f"- **FQDN**: {fqdn}\n"
                    elif obj_type == 'applicationCategory':
                        app_category_id = obj.get('applicationCategoryId')
                        if app_category_id:
                            result += f"- **App Category ID**: {app_category_id}\n"
                    
                    # Group associations
                    group_ids = obj.get('groupIds', [])
                    if group_ids:
                        result += f"- **Groups**: {len(group_ids)} groups\n"
                    
                    # Network associations
                    network_ids = obj.get('networkIds', [])
                    if network_ids:
                        result += f"- **Networks**: {len(network_ids)} networks\n"
                    
                    result += "\n"
                
                if len(cat_objects) > 10:
                    result += f"... and {len(cat_objects) - 10} more {category} objects\n\n"
                    
            return result
            
        except Exception as e:
            return f"Error retrieving policy objects: {str(e)}"


# From tools_policy.py
async def create_organization_policy_object(org_id: str, name: str, category: str, type: str, cidr: str = None, fqdn: str = None, ip: str = None):
        """
        Create a new policy object.
        
        Args:
            org_id: Organization ID
            name: Object name
            category: Category (e.g., 'network', 'application')
            type: Type (e.g., 'ipv4', 'fqdn', 'ipv4Range')
            cidr: CIDR notation for IP objects (e.g., '10.0.0.0/24')
            fqdn: Fully qualified domain name for FQDN objects
            ip: Single IP address
            
        Returns:
            Created policy object
        """
        try:
            # Map our type names to Meraki API type names
            type_mapping = {
                'ipv4': 'cidr',
                'fqdn': 'fqdn',
                'ipv4Range': 'ipAndMask'
            }
            
            meraki_type = type_mapping.get(type, type)
            
            kwargs = {
                'name': name,
                'category': category,
                'type': meraki_type
            }
            
            # Add type-specific parameters
            if type == 'ipv4' and cidr:
                kwargs['cidr'] = cidr
            elif type == 'fqdn' and fqdn:
                kwargs['fqdn'] = fqdn
            elif type == 'ipv4' and ip:
                # Convert single IP to CIDR
                kwargs['cidr'] = f"{ip}/32"
            else:
                return f"Error: Missing required parameter for type {type}"
            
            result = await meraki_client.create_organization_policy_object(org_id, **kwargs)
            
            response = f"# 🛡️ Policy Object Created\n\n"
            response += f"**Name**: {result.get('name', name)}\n"
            response += f"**ID**: {result.get('id', 'N/A')}\n"
            response += f"**Category**: {result.get('category', category)}\n"
            response += f"**Type**: {result.get('type', type)}\n"
            
            if result.get('cidr'):
                response += f"**CIDR**: {result.get('cidr')}\n"
            if result.get('fqdn'):
                response += f"**FQDN**: {result.get('fqdn')}\n"
                
            return response
            
        except Exception as e:
            return f"Error creating policy object: {str(e)}"


# From tools_policy.py
async def update_organization_policy_object(org_id: str, policy_object_id: str, name: str = None, cidr: str = None, fqdn: str = None):
        """
        Update an existing policy object.
        
        Args:
            org_id: Organization ID
            policy_object_id: Policy object ID
            name: New name (optional)
            cidr: New CIDR for IP objects (optional)
            fqdn: New FQDN for domain objects (optional)
            
        Returns:
            Updated policy object
        """
        try:
            kwargs = {}
            if name:
                kwargs['name'] = name
            if cidr:
                kwargs['cidr'] = cidr
            if fqdn:
                kwargs['fqdn'] = fqdn
                
            result = await meraki_client.update_organization_policy_object(org_id, policy_object_id, **kwargs)
            
            response = f"# 📝 Policy Object Updated\n\n"
            response += f"**ID**: {policy_object_id}\n"
            response += f"**Name**: {result.get('name', 'N/A')}\n"
            
            if result.get('cidr'):
                response += f"**CIDR**: {result.get('cidr')}\n"
            if result.get('fqdn'):
                response += f"**FQDN**: {result.get('fqdn')}\n"
                
            return response
            
        except Exception as e:
            return f"Error updating policy object: {str(e)}"


# From tools_policy.py
async def delete_organization_policy_object(org_id: str, policy_object_id: str):
        """
        Delete a policy object.
        
        Args:
            org_id: Organization ID
            policy_object_id: Policy object ID to delete
            
        Returns:
            Deletion confirmation
        """
        try:
            # Get policy object details first
            objects = await meraki_client.get_organization_policy_objects(org_id)
            policy_obj = None
            for obj in objects:
                if obj.get('id') == policy_object_id:
                    policy_obj = obj
                    break
            
            if not policy_obj:
                return f"❌ Policy object {policy_object_id} not found"
            
            # Import helper function
            from utils.helpers import require_confirmation
            
            # Require confirmation
            if not require_confirmation(
                operation_type="delete",
                resource_type="policy object",
                resource_name=policy_obj.get('name', 'Unknown'),
                resource_id=policy_object_id
            ):
                return "❌ Policy object deletion cancelled by user"
            
            # Perform deletion
            await meraki_client.delete_organization_policy_object(org_id, policy_object_id)
            
            return f"✅ Policy object '{policy_obj.get('name', policy_object_id)}' deleted successfully"
            
        except Exception as e:
            return f"Error deleting policy object: {str(e)}"


# From tools_policy.py
async def get_organization_policy_objects_groups(org_id: str):
        """
        List all policy object groups for an organization.
        
        Args:
            org_id: Organization ID
            
        Returns:
            List of policy object groups
        """
        try:
            groups = await meraki_client.get_organization_policy_objects_groups(org_id)
            
            if not groups:
                return f"No policy object groups found for organization {org_id}."
                
            result = f"# 📁 Policy Object Groups - Organization {org_id}\n\n"
            result += f"**Total Groups**: {len(groups)}\n\n"
            
            for group in groups:
                group_id = group.get('id', 'Unknown')
                name = group.get('name', 'Unnamed')
                category = group.get('category', 'uncategorized')
                
                result += f"## 📂 {name}\n"
                result += f"- **ID**: {group_id}\n"
                result += f"- **Category**: {category}\n"
                
                # Object IDs in this group
                object_ids = group.get('objectIds', [])
                if object_ids:
                    result += f"- **Objects**: {len(object_ids)} objects\n"
                    # Show first few
                    for obj_id in object_ids[:5]:
                        result += f"  - {obj_id}\n"
                    if len(object_ids) > 5:
                        result += f"  - ... and {len(object_ids) - 5} more\n"
                
                # Network associations
                network_ids = group.get('networkIds', [])
                if network_ids:
                    result += f"- **Networks**: {len(network_ids)} networks\n"
                
                result += "\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving policy object groups: {str(e)}"


# From tools_policy.py
async def create_organization_policy_objects_group(org_id: str, name: str, category: str, object_ids: str = None):
        """
        Create a new policy object group.
        
        Args:
            org_id: Organization ID
            name: Group name
            category: Category (must match objects' category)
            object_ids: Comma-separated policy object IDs to include
            
        Returns:
            Created policy object group
        """
        try:
            kwargs = {
                'name': name,
                'category': category
            }
            
            if object_ids:
                ids_list = [id.strip() for id in object_ids.split(',')]
                kwargs['objectIds'] = ids_list
            
            result = await meraki_client.create_organization_policy_objects_group(org_id, **kwargs)
            
            response = f"# 📁 Policy Object Group Created\n\n"
            response += f"**Name**: {result.get('name', name)}\n"
            response += f"**ID**: {result.get('id', 'N/A')}\n"
            response += f"**Category**: {result.get('category', category)}\n"
            
            obj_ids = result.get('objectIds', [])
            if obj_ids:
                response += f"**Objects**: {len(obj_ids)} objects included\n"
                
            return response
            
        except Exception as e:
            return f"Error creating policy object group: {str(e)}"


# From tools_monitoring.py
async def get_device_memory_history(serial: str, timespan: int = 3600):
        """
        Get memory utilization history for a device.
        
        Args:
            serial: Device serial number
            timespan: Time span in seconds (default 1 hour)
            
        Returns:
            Memory utilization history
        """
        try:
            history = await meraki_client.get_device_memory_history(serial, timespan=timespan)
            
            if not history:
                return f"No memory history available for device {serial}."
                
            result = f"# 💾 Memory History - Device {serial}\n\n"
            result += f"**Time Period**: Last {timespan/3600:.1f} hours\n\n"
            
            # Show recent data points
            for entry in history[-10:]:
                timestamp = entry.get('ts', 'Unknown')
                used_mb = entry.get('memoryUsedMb', 0)
                total_mb = entry.get('memoryTotalMb', 1)
                percent = (used_mb / total_mb * 100) if total_mb > 0 else 0
                
                # Status icon based on usage
                icon = "🟢" if percent < 70 else "🟡" if percent < 90 else "🔴"
                
                result += f"## {timestamp}\n"
                result += f"- **Usage**: {icon} {percent:.1f}% ({used_mb}MB / {total_mb}MB)\n"
                result += f"- **Free**: {total_mb - used_mb}MB\n\n"
            
            # Calculate average
            if history:
                avg_percent = sum((e.get('memoryUsedMb', 0) / e.get('memoryTotalMb', 1) * 100) 
                                for e in history if e.get('memoryTotalMb', 0) > 0) / len(history)
                result += f"### Average Usage: {avg_percent:.1f}%\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving memory history: {str(e)}"


# From tools_monitoring.py
async def get_device_cpu_power_mode_history(serial: str, timespan: int = 3600):
        """
        Get CPU power mode history for a wireless device.
        
        Args:
            serial: Device serial number
            timespan: Time span in seconds (default 1 hour)
            
        Returns:
            CPU power mode history
        """
        try:
            history = await meraki_client.get_device_cpu_power_mode_history(serial, timespan=timespan)
            
            if not history:
                return f"No CPU power mode history available for device {serial}."
                
            result = f"# ⚡ CPU Power Mode History - Device {serial}\n\n"
            result += f"**Time Period**: Last {timespan/3600:.1f} hours\n\n"
            
            # Count modes
            mode_counts = {}
            for entry in history:
                mode = entry.get('powerMode', 'unknown')
                mode_counts[mode] = mode_counts.get(mode, 0) + 1
            
            result += "## Power Mode Distribution\n"
            for mode, count in mode_counts.items():
                percent = (count / len(history) * 100) if history else 0
                icon = "🟢" if mode == 'low' else "🟡" if mode == 'medium' else "🔴"
                result += f"- **{mode.title()}**: {icon} {percent:.1f}% ({count} samples)\n"
            
            result += f"\n## Recent History\n"
            for entry in history[-10:]:
                timestamp = entry.get('ts', 'Unknown')
                mode = entry.get('powerMode', 'unknown')
                icon = "🟢" if mode == 'low' else "🟡" if mode == 'medium' else "🔴"
                
                result += f"- {timestamp}: {icon} {mode}\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving CPU power mode history: {str(e)}"


# From tools_monitoring.py
async def get_device_wireless_cpu_load(serial: str):
        """
        Get current CPU load for a wireless device.
        
        Args:
            serial: Device serial number
            
        Returns:
            Current CPU load information
        """
        try:
            cpu_load = await meraki_client.get_device_wireless_cpu_load(serial)
            
            result = f"# 📊 CPU Load - Wireless Device {serial}\n\n"
            
            # Overall CPU load
            overall = cpu_load.get('overall', {})
            if overall:
                load_percent = overall.get('percentage', 0)
                icon = "🟢" if load_percent < 50 else "🟡" if load_percent < 80 else "🔴"
                
                result += f"## Overall CPU Load\n"
                result += f"- **Current Load**: {icon} {load_percent}%\n"
                result += f"- **1 Min Average**: {overall.get('avg1Min', 0)}%\n"
                result += f"- **5 Min Average**: {overall.get('avg5Min', 0)}%\n"
                result += f"- **15 Min Average**: {overall.get('avg15Min', 0)}%\n\n"
            
            # Per-core information
            cores = cpu_load.get('perCore', [])
            if cores:
                result += f"## Per-Core Load ({len(cores)} cores)\n"
                for i, core in enumerate(cores):
                    core_percent = core.get('percentage', 0)
                    icon = "🟢" if core_percent < 50 else "🟡" if core_percent < 80 else "🔴"
                    result += f"- **Core {i}**: {icon} {core_percent}%\n"
            
            # Process information
            top_processes = cpu_load.get('topProcesses', [])
            if top_processes:
                result += f"\n## Top Processes\n"
                for proc in top_processes[:5]:
                    result += f"- **{proc.get('name', 'Unknown')}**: {proc.get('cpuPercentage', 0)}%\n"
                    
            return result
            
        except Exception as e:
            return f"Error retrieving CPU load: {str(e)}"


# From tools_monitoring.py
async def get_organization_switch_ports_history(org_id: str, timespan: int = 3600):
        """
        Get aggregated switch port statistics history for entire organization.
        
        Args:
            org_id: Organization ID
            timespan: Time span in seconds (default 1 hour)
            
        Returns:
            Organization-wide switch port history
        """
        try:
            history = await meraki_client.get_organization_switch_ports_history(org_id, timespan=timespan)
            
            if not history:
                return f"No switch port history available for organization {org_id}."
                
            result = f"# 🔌 Organization Switch Ports History - Org {org_id}\n\n"
            result += f"**Time Period**: Last {timespan/3600:.1f} hours\n\n"
            
            # Aggregate statistics
            total_ports = 0
            active_ports = 0
            error_ports = 0
            
            for entry in history:
                stats = entry.get('stats', {})
                total_ports = max(total_ports, stats.get('totalPorts', 0))
                active_ports = max(active_ports, stats.get('activePorts', 0))
                error_ports = max(error_ports, stats.get('errorPorts', 0))
            
            result += f"## Summary\n"
            result += f"- **Total Ports**: {total_ports}\n"
            result += f"- **Active Ports**: {active_ports} ({(active_ports/total_ports*100) if total_ports else 0:.1f}%)\n"
            result += f"- **Error Ports**: {error_ports}\n\n"
            
            # Recent history
            result += f"## Recent Activity\n"
            for entry in history[-10:]:
                timestamp = entry.get('ts', 'Unknown')
                stats = entry.get('stats', {})
                
                result += f"### {timestamp}\n"
                result += f"- Active: {stats.get('activePorts', 0)}/{stats.get('totalPorts', 0)}\n"
                result += f"- Errors: {stats.get('errorPorts', 0)}\n"
                result += f"- Power Usage: {stats.get('totalPowerWatts', 0)}W\n\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving switch ports history: {str(e)}"


# From tools_monitoring.py
async def get_organization_devices_migration_status(org_id: str):
        """
        Get migration status for devices being migrated in the organization.
        
        Args:
            org_id: Organization ID
            
        Returns:
            Device migration status
        """
        try:
            migrations = await meraki_client.get_organization_devices_migration_status(org_id)
            
            if not migrations:
                return f"No device migrations in progress for organization {org_id}."
                
            result = f"# 🔄 Device Migration Status - Org {org_id}\n\n"
            result += f"**Total Migrations**: {len(migrations)}\n\n"
            
            # Group by status
            status_groups = {}
            for migration in migrations:
                status = migration.get('status', 'unknown')
                if status not in status_groups:
                    status_groups[status] = []
                status_groups[status].append(migration)
            
            # Display by status
            for status, devices in status_groups.items():
                icon = "✅" if status == 'completed' else "🔄" if status == 'in_progress' else "⚠️"
                result += f"## {icon} {status.title()} ({len(devices)} devices)\n"
                
                for device in devices[:5]:
                    serial = device.get('serial', 'Unknown')
                    name = device.get('name', 'Unnamed')
                    from_network = device.get('fromNetwork', {}).get('name', 'Unknown')
                    to_network = device.get('toNetwork', {}).get('name', 'Unknown')
                    
                    result += f"### {name} ({serial})\n"
                    result += f"- **From**: {from_network}\n"
                    result += f"- **To**: {to_network}\n"
                    
                    # Progress percentage
                    progress = device.get('progressPercent')
                    if progress is not None:
                        progress_bar = "█" * (progress // 10) + "░" * (10 - progress // 10)
                        result += f"- **Progress**: [{progress_bar}] {progress}%\n"
                    
                    # Start time
                    started = device.get('startedAt')
                    if started:
                        result += f"- **Started**: {started}\n"
                    
                    result += "\n"
                
                if len(devices) > 5:
                    result += f"... and {len(devices) - 5} more {status} migrations\n\n"
                    
            return result
            
        except Exception as e:
            return f"Error retrieving migration status: {str(e)}"


# From tools_monitoring.py
async def get_organization_api_usage(org_id: str, timespan: int = 86400):
        """
        Get API usage statistics for monitoring API consumption.
        
        Args:
            org_id: Organization ID
            timespan: Time span in seconds (default 24 hours)
            
        Returns:
            API usage analytics
        """
        try:
            usage = await meraki_client.get_organization_api_requests(org_id, timespan=timespan)
            
            if not usage:
                return f"No API usage data available for organization {org_id}."
                
            result = f"# 📈 API Usage Analytics - Org {org_id}\n\n"
            result += f"**Time Period**: Last {timespan/3600:.0f} hours\n"
            result += f"**Total Requests**: {len(usage)}\n\n"
            
            # Group by admin
            admin_usage = {}
            for req in usage:
                admin = req.get('adminId', 'Unknown')
                if admin not in admin_usage:
                    admin_usage[admin] = 0
                admin_usage[admin] += 1
            
            result += "## Usage by Admin\n"
            for admin, count in sorted(admin_usage.items(), key=lambda x: x[1], reverse=True)[:5]:
                result += f"- **{admin}**: {count} requests\n"
            
            # Group by path
            path_usage = {}
            for req in usage:
                path = req.get('path', 'Unknown')
                # Simplify path to endpoint
                path_parts = path.split('/')
                if len(path_parts) > 3:
                    endpoint = f"/{path_parts[1]}/{path_parts[2]}/..."
                else:
                    endpoint = path
                    
                if endpoint not in path_usage:
                    path_usage[endpoint] = 0
                path_usage[endpoint] += 1
            
            result += "\n## Top Endpoints\n"
            for endpoint, count in sorted(path_usage.items(), key=lambda x: x[1], reverse=True)[:10]:
                result += f"- **{endpoint}**: {count} requests\n"
            
            # Response codes
            response_codes = {}
            for req in usage:
                code = req.get('responseCode', 0)
                if code not in response_codes:
                    response_codes[code] = 0
                response_codes[code] += 1
            
            result += "\n## Response Codes\n"
            for code, count in sorted(response_codes.items()):
                icon = "✅" if 200 <= code < 300 else "⚠️" if 400 <= code < 500 else "🔴"
                result += f"- **{code}**: {icon} {count} responses\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving API usage: {str(e)}"


# From tools_beta.py
async def get_organization_early_access_features(org_id: str):
        """
        List all available early access features for an organization.
        
        Args:
            org_id: Organization ID
            
        Returns:
            List of available early access features
        """
        try:
            features = await meraki_client.get_organization_early_access_features(org_id)
            
            if not features:
                return f"No early access features available for organization {org_id}."
                
            result = f"# 🧪 Early Access Features - Organization {org_id}\n\n"
            result += f"**Total Features**: {len(features)}\n\n"
            
            for feature in features:
                feature_id = feature.get('id', 'Unknown')
                name = feature.get('name', 'Unnamed')
                description = feature.get('description', 'No description')
                status = feature.get('status', 'unknown')
                
                # Status icon
                status_icon = "✅" if status == 'available' else "🔒" if status == 'restricted' else "⏳"
                
                result += f"## {status_icon} {name}\n"
                result += f"- **ID**: {feature_id}\n"
                result += f"- **Status**: {status}\n"
                result += f"- **Description**: {description}\n"
                
                # Documentation link
                doc_link = feature.get('documentationLink')
                if doc_link:
                    result += f"- **Documentation**: {doc_link}\n"
                
                # Privacy link
                privacy_link = feature.get('privacyLink')
                if privacy_link:
                    result += f"- **Privacy Policy**: {privacy_link}\n"
                
                # Supported products
                products = feature.get('supportedProducts', [])
                if products:
                    result += f"- **Supported Products**: {', '.join(products)}\n"
                
                result += "\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving early access features: {str(e)}"


# From tools_beta.py
async def get_organization_early_access_opt_ins(org_id: str):
        """
        List all early access features that the organization has opted into.
        
        Args:
            org_id: Organization ID
            
        Returns:
            List of opted-in early access features
        """
        try:
            opt_ins = await meraki_client.get_organization_early_access_features_opt_ins(org_id)
            
            if not opt_ins:
                return f"Organization {org_id} has not opted into any early access features."
                
            result = f"# 🧪 Early Access Opt-Ins - Organization {org_id}\n\n"
            result += f"**Total Opt-Ins**: {len(opt_ins)}\n\n"
            
            result += "⚠️ **WARNING**: Early access features may have breaking changes!\n\n"
            
            for opt_in in opt_ins:
                opt_in_id = opt_in.get('optInId', 'Unknown')
                feature_id = opt_in.get('shortName', opt_in.get('id', 'Unknown'))
                created_at = opt_in.get('createdAt', 'Unknown')
                
                result += f"## ✅ {feature_id}\n"
                result += f"- **Opt-In ID**: {opt_in_id}\n"
                result += f"- **Enabled At**: {created_at}\n"
                
                # Limit access to specific networks
                limited_access = opt_in.get('limitedAccess', [])
                if limited_access:
                    result += f"- **Limited to Networks**: {len(limited_access)} networks\n"
                    for network in limited_access[:5]:
                        result += f"  - {network.get('name', 'Unknown')} ({network.get('id')})\n"
                    if len(limited_access) > 5:
                        result += f"  - ... and {len(limited_access) - 5} more\n"
                        
                result += "\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving early access opt-ins: {str(e)}"


# From tools_beta.py
async def enable_organization_early_access_feature(org_id: str, feature_id: str, limit_to_networks: str = None):
        """
        Opt into an early access feature for the organization.
        
        Args:
            org_id: Organization ID
            feature_id: Early access feature ID or short name
            limit_to_networks: Comma-separated network IDs to limit access (optional)
            
        Returns:
            Opt-in confirmation
        """
        try:
            kwargs = {}
            
            if limit_to_networks:
                network_ids = [id.strip() for id in limit_to_networks.split(',')]
                kwargs['limitedAccessNetworkIds'] = network_ids
            
            result = await meraki_client.create_organization_early_access_features_opt_in(
                org_id,
                shortName=feature_id,
                **kwargs
            )
            
            response = f"# 🧪 Early Access Feature Enabled\n\n"
            response += f"**Feature**: {feature_id}\n"
            response += f"**Organization**: {org_id}\n"
            response += f"**Opt-In ID**: {result.get('optInId', 'N/A')}\n\n"
            
            response += "⚠️ **IMPORTANT**: This feature is in beta and may have breaking changes!\n"
            response += "All API users for this organization will now use the beta API spec.\n\n"
            
            if 'limitedAccessNetworkIds' in kwargs:
                response += f"**Limited to**: {len(kwargs['limitedAccessNetworkIds'])} specific networks\n"
            else:
                response += "**Access**: Organization-wide\n"
                
            return response
            
        except Exception as e:
            return f"Error enabling early access feature: {str(e)}"


# From tools_beta.py
async def disable_organization_early_access_feature(org_id: str, opt_in_id: str):
        """
        Opt out of an early access feature for the organization.
        
        Args:
            org_id: Organization ID
            opt_in_id: Opt-in ID to disable
            
        Returns:
            Opt-out confirmation
        """
        try:
            await meraki_client.delete_organization_early_access_features_opt_in(org_id, opt_in_id)
            
            response = f"# 🧪 Early Access Feature Disabled\n\n"
            response += f"**Opt-In ID**: {opt_in_id}\n"
            response += f"**Organization**: {org_id}\n\n"
            
            response += "✅ Successfully opted out of the early access feature.\n"
            response += "The organization will now use the stable API spec.\n"
            
            return response
            
        except Exception as e:
            return f"Error disabling early access feature: {str(e)}"


# From tools_beta.py
async def get_organization_api_analytics(org_id: str, timespan: int = 86400):
        """
        Get API analytics for the organization (new 2025 feature).
        
        Args:
            org_id: Organization ID
            timespan: Time span in seconds (default 24 hours)
            
        Returns:
            API analytics data
        """
        try:
            # This uses the existing API requests endpoint
            requests = await meraki_client.get_organization_api_requests(org_id, timespan=timespan)
            
            if not requests:
                return f"No API usage data available for organization {org_id}."
                
            result = f"# 📊 API Analytics - Organization {org_id}\n\n"
            result += f"**Time Period**: Last {timespan/3600:.0f} hours\n"
            result += f"**Total API Calls**: {len(requests)}\n\n"
            
            # Analyze by response code
            response_codes = {}
            for req in requests:
                code = req.get('responseCode', 0)
                response_codes[code] = response_codes.get(code, 0) + 1
            
            result += "## Response Code Distribution\n"
            total_calls = len(requests)
            for code, count in sorted(response_codes.items()):
                percent = (count / total_calls * 100) if total_calls else 0
                if 200 <= code < 300:
                    icon = "✅"
                    status = "Success"
                elif code == 429:
                    icon = "⚠️"
                    status = "Rate Limited"
                elif 400 <= code < 500:
                    icon = "❌"
                    status = "Client Error"
                else:
                    icon = "🔴"
                    status = "Server Error"
                    
                result += f"- **{code} {status}**: {icon} {count} calls ({percent:.1f}%)\n"
            
            # Top endpoints
            endpoints = {}
            for req in requests:
                path = req.get('path', '')
                # Simplify path
                parts = path.split('/')
                if len(parts) > 3:
                    endpoint = f"/{parts[1]}/{parts[2]}"
                else:
                    endpoint = path
                endpoints[endpoint] = endpoints.get(endpoint, 0) + 1
            
            result += "\n## Top API Endpoints\n"
            for endpoint, count in sorted(endpoints.items(), key=lambda x: x[1], reverse=True)[:10]:
                result += f"- **{endpoint}**: {count} calls\n"
            
            # Rate limit analysis
            rate_limited = sum(1 for req in requests if req.get('responseCode') == 429)
            if rate_limited > 0:
                result += f"\n## ⚠️ Rate Limiting\n"
                result += f"- **Rate Limited Calls**: {rate_limited}\n"
                result += f"- **Percentage**: {(rate_limited/total_calls*100):.1f}%\n"
                result += "- **Recommendation**: Consider implementing request throttling\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving API analytics: {str(e)}"


# From tools_beta.py
async def check_beta_apis_status():
        """
        Check the status of beta APIs mentioned in the 2025 documentation.
        
        Returns:
            Status of various beta APIs
        """
        result = f"# 🧪 Beta APIs Status Check\n\n"
        result += "Based on the 2025 Meraki API documentation, here are potentially available beta features:\n\n"
        
        result += "## 1. 💾 Device Memory History API\n"
        result += "- **Endpoint**: `/devices/{serial}/memory/history`\n"
        result += "- **Status**: Planned/Beta - Not in current SDK\n"
        result += "- **Alternative**: Use SNMP or device status APIs\n\n"
        
        result += "## 2. ⚡ CPU Power Mode History API\n"
        result += "- **Endpoint**: `/devices/{serial}/wireless/cpuPowerMode/history`\n"
        result += "- **Status**: May be early access only\n"
        result += "- **Current**: Using radio settings as proxy\n\n"
        
        result += "## 3. 🔧 MAC Table Live Tools\n"
        result += "- **Endpoint**: `/devices/{serial}/liveTools/macTable`\n"
        result += "- **Status**: New 2025 feature - likely beta\n"
        result += "- **Purpose**: Real-time MAC table queries\n\n"
        
        result += "## 4. 🔐 OAuth 2.0 Support\n"
        result += "- **Status**: Released in 2025\n"
        result += "- **Implementation**: Available but requires setup\n"
        result += "- **Benefit**: More secure than API keys\n\n"
        
        result += "## 5. 📊 API Analytics Dashboard\n"
        result += "- **Status**: Released in 2025\n"
        result += "- **Access**: Via Dashboard UI and API\n"
        result += "- **Tool**: `get_organization_api_analytics`\n\n"
        
        result += "## How to Enable Beta Features\n"
        result += "1. Use `get_organization_early_access_features` to see available features\n"
        result += "2. Use `enable_organization_early_access_feature` to opt in\n"
        result += "3. Test carefully - beta APIs can have breaking changes!\n\n"
        
        result += "⚠️ **Note**: Once enabled for an org, ALL API users get beta access!"
        
        return result


# From tools_live.py
async def create_device_ping_test(serial: str, target: str, count: int = 5):
        """
        Create a ping test from a device.
        
        Args:
            serial: Device serial number
            target: Target IP or hostname to ping
            count: Number of pings (default 5, max 5)
            
        Returns:
            Ping test job details
        """
        try:
            # Ensure count doesn't exceed maximum
            if count > 5:
                count = 5
                
            result = await meraki_client.create_device_live_tools_ping(
                serial,
                target=target,
                count=count
            )
            
            # Check if we got a valid response
            if not result:
                return "❌ Error: No response from API. The device may be offline or Live Tools may not be enabled."
            
            # Get the job ID - it might be 'id' or 'pingId'
            job_id = result.get('pingId') or result.get('id')
            
            if not job_id:
                return f"""❌ Error: Ping test creation failed.
                
API Response: {result}

Possible causes:
- Device is offline or unreachable
- Live Tools not enabled for this organization
- Invalid target address
- Device doesn't support Live Tools"""
            
            response = f"# 🏓 Ping Test Started Successfully\n\n"
            response += f"**Device**: {serial}\n"
            response += f"**Target**: {target}\n"
            response += f"**Count**: {count}\n"
            response += f"**Job ID**: `{job_id}`\n"
            response += f"**Status**: {result.get('status', 'Unknown')}\n\n"
            
            response += "⏳ Test in progress. Use `get_device_ping_test` with the job ID to check results.\n"
            response += f"\nExample: `get_device_ping_test serial=\"{serial}\" ping_id=\"{job_id}\"`\n"
            
            return response
            
        except Exception as e:
            return f"Error creating ping test: {str(e)}"


# From tools_live.py
async def get_device_ping_test(serial: str, ping_id: str):
        """
        Get results of a ping test.
        
        Args:
            serial: Device serial number
            ping_id: Ping test job ID
            
        Returns:
            Ping test results
        """
        try:
            result = await meraki_client.get_device_live_tools_ping(serial, ping_id)
            
            response = f"# 🏓 Ping Test Results\n\n"
            response += f"**Status**: {result.get('status', 'Unknown')}\n"
            
            # Results
            results = result.get('results', {})
            if results:
                response += f"\n## Results\n"
                response += f"- **Sent**: {results.get('sent', 0)} packets\n"
                response += f"- **Received**: {results.get('received', 0)} packets\n"
                response += f"- **Loss**: {results.get('loss', {}).get('percentage', 0)}%\n"
                
                # Latency stats
                latency = results.get('latency', {})
                if latency:
                    response += f"\n## Latency\n"
                    response += f"- **Min**: {latency.get('minimum', 0)}ms\n"
                    response += f"- **Avg**: {latency.get('average', 0)}ms\n"
                    response += f"- **Max**: {latency.get('maximum', 0)}ms\n"
                
                # Individual replies
                replies = results.get('replies', [])
                if replies:
                    response += f"\n## Replies\n"
                    for i, reply in enumerate(replies[:5], 1):
                        response += f"{i}. Seq {reply.get('sequenceId')}: {reply.get('size')} bytes, {reply.get('latency')}ms\n"
                        
            return response
            
        except Exception as e:
            return f"Error getting ping test results: {str(e)}"


# From tools_live.py
async def create_device_throughput_test(serial: str, target_serial: str):
        """
        Create a throughput test between two devices.
        
        Args:
            serial: Source device serial
            target_serial: Target device serial
            
        Returns:
            Throughput test job details
        """
        try:
            result = await meraki_client.create_device_live_tools_throughput_test(
                serial,
                targetSerial=target_serial
            )
            
            # Check if we got a valid response
            if not result:
                return "❌ Error: No response from API. Live Tools may not be enabled."
            
            # Get the job ID - it might be 'id' or 'throughputTestId'
            job_id = result.get('throughputTestId') or result.get('id')
            
            if not job_id:
                return f"""❌ Error: Throughput test creation failed.
                
API Response: {result}

Possible causes:
- Devices must be on the same network
- Both devices must support Live Tools
- Devices must be compatible (e.g., switch to switch, MX to MX)
- Live Tools not enabled for this organization
- One or both devices may be offline"""
            
            response = f"# 🚀 Throughput Test Started Successfully\n\n"
            response += f"**Source Device**: {serial}\n"
            response += f"**Target Device**: {target_serial}\n"
            response += f"**Job ID**: `{job_id}`\n"
            response += f"**Status**: {result.get('status', 'Unknown')}\n\n"
            
            response += "⏳ Test in progress. This may take 1-3 minutes.\n"
            response += f"\nExample: `get_device_throughput_test serial=\"{serial}\" test_id=\"{job_id}\"`\n"
            
            return response
            
        except Exception as e:
            error_msg = str(e)
            
            # Provide helpful error messages for common issues
            if "400" in error_msg:
                return f"""❌ Error: {error_msg}

Common causes:
- Devices must be on the same network
- Device types must be compatible
- Both devices must support Live Tools throughput testing"""
            elif "404" in error_msg:
                return f"""❌ Error: {error_msg}

Device not found or Live Tools not available."""
            else:
                return f"❌ Error creating throughput test: {error_msg}"


# From tools_live.py
async def get_device_throughput_test(serial: str, test_id: str):
        """
        Get results of a throughput test.
        
        Args:
            serial: Device serial number
            test_id: Test job ID
            
        Returns:
            Throughput test results
        """
        try:
            result = await meraki_client.get_device_live_tools_throughput_test(serial, test_id)
            
            response = f"# 🚀 Throughput Test Results\n\n"
            response += f"**Status**: {result.get('status', 'Unknown')}\n"
            
            # Results
            results = result.get('results', {})
            if results:
                speeds = results.get('speeds', {})
                if speeds:
                    response += f"\n## Speed Results\n"
                    response += f"- **Download**: {speeds.get('downstream', 0)} Mbps\n"
                    response += f"- **Upload**: {speeds.get('upstream', 0)} Mbps\n"
                    
            return response
            
        except Exception as e:
            return f"Error getting throughput test results: {str(e)}"


# From tools_live.py
async def create_switch_cable_test(serial: str, port: str):
        """
        Run cable diagnostic test on a switch port.
        
        Args:
            serial: Switch serial number
            port: Port ID (e.g., "1", "5")
            
        Returns:
            Cable test job details
        """
        try:
            result = await meraki_client.create_device_live_tools_cable_test(
                serial,
                ports=[port]
            )
            
            response = f"# 🔌 Cable Test Started\n\n"
            response += f"**Switch**: {serial}\n"
            response += f"**Port**: {port}\n"
            response += f"**Job ID**: {result.get('id', 'N/A')}\n\n"
            
            response += "⏳ Testing cable. Use `get_switch_cable_test` to check results.\n"
            
            return response
            
        except Exception as e:
            return f"Error creating cable test: {str(e)}"


# From tools_live.py
async def get_switch_cable_test(serial: str, test_id: str):
        """
        Get results of a cable test.
        
        Args:
            serial: Switch serial number
            test_id: Test job ID
            
        Returns:
            Cable test results
        """
        try:
            result = await meraki_client.get_device_live_tools_cable_test(serial, test_id)
            
            response = f"# 🔌 Cable Test Results\n\n"
            response += f"**Status**: {result.get('status', 'Unknown')}\n"
            
            # Results
            results = result.get('results', {})
            if results:
                ports = results.get('ports', {})
                for port_id, port_data in ports.items():
                    response += f"\n## Port {port_id}\n"
                    response += f"- **Status**: {port_data.get('status', 'Unknown')}\n"
                    response += f"- **Speed**: {port_data.get('speedMbps', 'N/A')} Mbps\n"
                    
                    # Pairs (cable pairs)
                    pairs = port_data.get('pairs', [])
                    if pairs:
                        response += "- **Cable Pairs**:\n"
                        for pair in pairs:
                            status = pair.get('status', 'Unknown')
                            length = pair.get('lengthMeters', 'N/A')
                            icon = "✅" if status == 'ok' else "❌"
                            response += f"  - Pair {pair.get('index')}: {icon} {status} ({length}m)\n"
                            
            return response
            
        except Exception as e:
            return f"Error getting cable test results: {str(e)}"


# From tools_live.py
async def create_device_wake_on_lan(serial: str, vlan_id: int, mac_address: str):
        """
        Send Wake-on-LAN packet to wake up a device.
        
        Args:
            serial: Device serial to send WOL from
            vlan_id: VLAN ID
            mac_address: Target MAC address to wake
            
        Returns:
            WOL job details
        """
        try:
            result = await meraki_client.create_device_live_tools_wake_on_lan(
                serial,
                vlanId=vlan_id,
                mac=mac_address
            )
            
            response = f"# ⏰ Wake-on-LAN Sent\n\n"
            response += f"**From Device**: {serial}\n"
            response += f"**Target MAC**: {mac_address}\n"
            response += f"**VLAN**: {vlan_id}\n"
            response += f"**Job ID**: {result.get('id', 'N/A')}\n\n"
            
            response += "✅ Magic packet sent to wake the device.\n"
            
            return response
            
        except Exception as e:
            return f"Error sending Wake-on-LAN: {str(e)}"


# From tools_live.py
async def create_switch_mac_table(serial: str):
        """
        Request MAC address table from a switch.
        
        Args:
            serial: Switch serial number
            
        Returns:
            MAC table job details
        """
        try:
            result = await meraki_client.create_device_live_tools_mac_table(serial)
            
            response = f"# 📋 MAC Table Request Started\n\n"
            response += f"**Switch**: {serial}\n"
            response += f"**Job ID**: {result.get('id', 'N/A')}\n\n"
            
            response += "⏳ Retrieving MAC table. Use `get_switch_mac_table` to view results.\n"
            
            return response
            
        except Exception as e:
            return f"Error creating MAC table request: {str(e)}"


# From tools_live.py
async def get_switch_mac_table(serial: str, request_id: str):
        """
        Get MAC address table results.
        
        Args:
            serial: Switch serial number
            request_id: MAC table request ID
            
        Returns:
            MAC table entries
        """
        try:
            result = await meraki_client.get_device_live_tools_mac_table(serial, request_id)
            
            response = f"# 📋 MAC Address Table\n\n"
            response += f"**Status**: {result.get('status', 'Unknown')}\n"
            
            # Entries
            entries = result.get('entries', [])
            if entries:
                response += f"\n**Total Entries**: {len(entries)}\n\n"
                
                # Group by VLAN
                vlan_groups = {}
                for entry in entries:
                    vlan = entry.get('vlanId', 'Unknown')
                    if vlan not in vlan_groups:
                        vlan_groups[vlan] = []
                    vlan_groups[vlan].append(entry)
                
                for vlan, vlan_entries in sorted(vlan_groups.items()):
                    response += f"## VLAN {vlan} ({len(vlan_entries)} entries)\n"
                    
                    for entry in vlan_entries[:10]:  # Show first 10 per VLAN
                        mac = entry.get('mac', 'Unknown')
                        port = entry.get('port', 'Unknown')
                        response += f"- **{mac}** → Port {port}\n"
                    
                    if len(vlan_entries) > 10:
                        response += f"... and {len(vlan_entries) - 10} more entries\n"
                    response += "\n"
                    
            return response
            
        except Exception as e:
            return f"Error getting MAC table results: {str(e)}"


# From tools_live.py
async def blink_device_leds(serial: str, duration: int = 30):
        """
        Blink device LEDs to help identify it physically.
        
        Args:
            serial: Device serial number
            duration: Duration in seconds (default 30)
            
        Returns:
            LED blink job details
        """
        try:
            result = await meraki_client.create_device_live_tools_leds_blink(
                serial,
                duration=duration
            )
            
            response = f"# 💡 LED Blink Started\n\n"
            response += f"**Device**: {serial}\n"
            response += f"**Duration**: {duration} seconds\n"
            response += f"**Job ID**: {result.get('id', 'N/A')}\n\n"
            
            response += "✨ Device LEDs are now blinking to help identify it!\n"
            
            return response
            
        except Exception as e:
            return f"Error blinking LEDs: {str(e)}"


# Tool registry
ALL_TOOLS = {
    "list_organizations": list_organizations,
    "get_organization": get_organization,
    "get_organization_networks": get_organization_networks,
    "get_organization_alerts": get_organization_alerts,
    "create_organization": create_organization,
    "update_organization": update_organization,
    "delete_organization": delete_organization,
    "get_organization_firmware": get_organization_firmware,
    "get_network": get_network,
    "update_network": update_network,
    "get_network_devices": get_network_devices,
    "get_network_clients": get_network_clients,
    "create_network": create_network,
    "delete_network": delete_network,
    "get_device": get_device,
    "update_device": update_device,
    "reboot_device": reboot_device,
    "get_device_clients": get_device_clients,
    "get_device_status": get_device_status,
    "claim_device_into_network": claim_device_into_network,
    "claim_devices_into_network": claim_devices_into_network,
    "list_unassigned_devices": list_unassigned_devices,
    "get_network_wireless_ssids": get_network_wireless_ssids,
    "get_network_wireless_passwords": get_network_wireless_passwords,
    "update_network_wireless_ssid": update_network_wireless_ssid,
    "get_network_wireless_clients": get_network_wireless_clients,
    "get_network_wireless_usage": get_network_wireless_usage,
    "get_network_wireless_rf_profiles": get_network_wireless_rf_profiles,
    "get_network_wireless_air_marshal": get_network_wireless_air_marshal,
    "get_network_wireless_bluetooth_clients": get_network_wireless_bluetooth_clients,
    "get_network_wireless_channel_utilization": get_network_wireless_channel_utilization,
    "get_device_switch_ports": get_device_switch_ports,
    "update_device_switch_port": update_device_switch_port,
    "get_device_switch_port_statuses": get_device_switch_port_statuses,
    "get_device_switch_vlans": get_device_switch_vlans,
    "create_device_switch_vlan": create_device_switch_vlan,
    "get_organization_uplinks_loss_and_latency": get_organization_uplinks_loss_and_latency,
    "get_organization_appliance_uplink_statuses": get_organization_appliance_uplink_statuses,
    "get_network_connection_stats": get_network_connection_stats,
    "get_network_latency_stats": get_network_latency_stats,
    "get_organization_webhooks": get_organization_webhooks,
    "create_organization_webhook": create_organization_webhook,
    "get_network_webhook_http_servers": get_network_webhook_http_servers,
    "create_network_webhook_http_server": create_network_webhook_http_server,
    "get_network_alerts_settings": get_network_alerts_settings,
    "update_network_alerts_settings": update_network_alerts_settings,
    "get_network_appliance_firewall_l3_rules": get_network_appliance_firewall_l3_rules,
    "update_network_appliance_firewall_l3_rules": update_network_appliance_firewall_l3_rules,
    "get_network_appliance_content_filtering": get_network_appliance_content_filtering,
    "get_network_appliance_vpn_site_to_site": get_network_appliance_vpn_site_to_site,
    "get_network_appliance_security_malware": get_network_appliance_security_malware,
    "get_network_appliance_security_intrusion": get_network_appliance_security_intrusion,
    "get_device_camera_video_link": get_device_camera_video_link,
    "get_device_camera_snapshot": get_device_camera_snapshot,
    "get_device_camera_video_settings": get_device_camera_video_settings,
    "update_device_camera_video_settings": update_device_camera_video_settings,
    "get_device_camera_analytics_zones": get_device_camera_analytics_zones,
    "get_device_camera_sense": get_device_camera_sense,
    "get_network_sm_devices": get_network_sm_devices,
    "get_network_sm_device_detail": get_network_sm_device_detail,
    "get_network_sm_device_apps": get_network_sm_device_apps,
    "reboot_network_sm_devices": reboot_network_sm_devices,
    "get_network_sm_profiles": get_network_sm_profiles,
    "get_network_sm_performance_history": get_network_sm_performance_history,
    "get_organization_licenses": get_organization_licenses,
    "get_organization_licensing_coterm": get_organization_licensing_coterm,
    "claim_organization_license": claim_organization_license,
    "update_organization_license": update_organization_license,
    "move_organization_licenses": move_organization_licenses,
    "renew_organization_licenses_seats": renew_organization_licenses_seats,
    "get_organization_policy_objects": get_organization_policy_objects,
    "create_organization_policy_object": create_organization_policy_object,
    "update_organization_policy_object": update_organization_policy_object,
    "delete_organization_policy_object": delete_organization_policy_object,
    "get_organization_policy_objects_groups": get_organization_policy_objects_groups,
    "create_organization_policy_objects_group": create_organization_policy_objects_group,
    "get_device_memory_history": get_device_memory_history,
    "get_device_cpu_power_mode_history": get_device_cpu_power_mode_history,
    "get_device_wireless_cpu_load": get_device_wireless_cpu_load,
    "get_organization_switch_ports_history": get_organization_switch_ports_history,
    "get_organization_devices_migration_status": get_organization_devices_migration_status,
    "get_organization_api_usage": get_organization_api_usage,
    "get_organization_early_access_features": get_organization_early_access_features,
    "get_organization_early_access_opt_ins": get_organization_early_access_opt_ins,
    "enable_organization_early_access_feature": enable_organization_early_access_feature,
    "disable_organization_early_access_feature": disable_organization_early_access_feature,
    "get_organization_api_analytics": get_organization_api_analytics,
    "check_beta_apis_status": check_beta_apis_status,
    "create_device_ping_test": create_device_ping_test,
    "get_device_ping_test": get_device_ping_test,
    "create_device_throughput_test": create_device_throughput_test,
    "get_device_throughput_test": get_device_throughput_test,
    "create_switch_cable_test": create_switch_cable_test,
    "get_switch_cable_test": get_switch_cable_test,
    "create_device_wake_on_lan": create_device_wake_on_lan,
    "create_switch_mac_table": create_switch_mac_table,
    "get_switch_mac_table": get_switch_mac_table,
    "blink_device_leds": blink_device_leds,
}

# Tool metadata for MCP protocol
TOOL_METADATA = {
    "list_organizations": {
        "description": "List all Meraki organizations the API key has access to.\n        \n        Returns:\n            Formatted list of organizations",
        "parameters": []
    },
    "get_organization": {
        "description": "Get details about a specific Meraki organization.\n        \n        Args:\n            organization_id: ID of the organization to retrieve\n            \n        Returns:\n            Organization details",
        "parameters": [{"name": "organization_id", "type": "str", "default": null, "required": true}]
    },
    "get_organization_networks": {
        "description": "List networks in a Meraki organization.\n        \n        Args:\n            org_id: ID of the organization\n            \n        Returns:\n            Formatted list of networks",
        "parameters": [{"name": "org_id", "type": "str", "default": null, "required": true}]
    },
    "get_organization_alerts": {
        "description": "Get alert settings for a Meraki organization.\n        \n        Args:\n            org_id: ID of the organization\n            \n        Returns:\n            Formatted alert settings",
        "parameters": [{"name": "org_id", "type": "str", "default": null, "required": true}]
    },
    "create_organization": {
        "description": "Create a new Meraki organization.\n        \n        Args:\n            name: Name for the new organization\n            \n        Returns:\n            New organization details",
        "parameters": [{"name": "name", "type": "str", "default": null, "required": true}]
    },
    "update_organization": {
        "description": "Update a Meraki organization.\n        \n        Args:\n            organization_id: ID of the organization to update\n            name: New name for the organization (optional)\n            \n        Returns:\n            Updated organization details",
        "parameters": [{"name": "organization_id", "type": "str", "default": null, "required": true}, {"name": "name", "type": "str", "default": "None", "required": false}]
    },
    "delete_organization": {
        "description": "Delete a Meraki organization.\n        \n        Args:\n            organization_id: ID of the organization to delete\n            \n        Returns:\n            Success/failure information",
        "parameters": [{"name": "organization_id", "type": "str", "default": null, "required": true}]
    },
    "get_organization_firmware": {
        "description": "Get firmware upgrades for a Meraki organization.\n        \n        Args:\n            org_id: ID of the organization\n            \n        Returns:\n            Formatted firmware upgrade information",
        "parameters": [{"name": "org_id", "type": "str", "default": null, "required": true}]
    },
    "get_network": {
        "description": "Get details about a specific Meraki network.\n        \n        Args:\n            network_id: ID of the network to retrieve\n            \n        Returns:\n            Network details",
        "parameters": [{"name": "network_id", "type": "str", "default": null, "required": true}]
    },
    "update_network": {
        "description": "Update a Meraki network.\n        \n        Args:\n            network_id: ID of the network to update\n            name: New name for the network (optional)\n            tags: New tags for the network (optional)\n            \n        Returns:\n            Updated network details",
        "parameters": [{"name": "network_id", "type": "str", "default": null, "required": true}, {"name": "name", "type": "str", "default": "None", "required": false}, {"name": "tags", "type": "list", "default": "None", "required": false}]
    },
    "get_network_devices": {
        "description": "List devices in a Meraki network.\n        \n        Args:\n            network_id: ID of the network\n            \n        Returns:\n            Formatted list of devices",
        "parameters": [{"name": "network_id", "type": "str", "default": null, "required": true}]
    },
    "get_network_clients": {
        "description": "List clients in a Meraki network.\n        \n        Args:\n            network_id: ID of the network\n            \n        Returns:\n            Formatted list of clients",
        "parameters": [{"name": "network_id", "type": "str", "default": null, "required": true}]
    },
    "create_network": {
        "description": "Create a new Meraki network in an organization.\n        \n        Args:\n            organization_id: ID of the organization to create the network in\n            name: Name for the new network\n            product_types: Comma-separated product types (appliance,switch,wireless,camera,sensor)\n            \n        Returns:\n            New network details",
        "parameters": [{"name": "organization_id", "type": "str", "default": null, "required": true}, {"name": "name", "type": "str", "default": null, "required": true}, {"name": "product_types", "type": "str", "default": "\"wireless\"", "required": false}]
    },
    "delete_network": {
        "description": "Delete a Meraki network.\n        \n        Args:\n            network_id: ID of the network to delete\n            \n        Returns:\n            Success/failure information",
        "parameters": [{"name": "network_id", "type": "str", "default": null, "required": true}]
    },
    "get_device": {
        "description": "Get details about a specific Meraki device.\n        \n        Args:\n            serial: Serial number of the device to retrieve\n            \n        Returns:\n            Device details",
        "parameters": [{"name": "serial", "type": "str", "default": null, "required": true}]
    },
    "update_device": {
        "description": "Update a Meraki device.\n        \n        Args:\n            serial: Serial number of the device to update\n            name: New name for the device (optional)\n            tags: New tags for the device (optional)\n            address: New address for the device (optional)\n            \n        Returns:\n            Updated device details",
        "parameters": [{"name": "serial", "type": "str", "default": null, "required": true}, {"name": "name", "type": "str", "default": "None", "required": false}, {"name": "tags", "type": "list", "default": "None", "required": false}, {"name": "address", "type": "str", "default": "None", "required": false}]
    },
    "reboot_device": {
        "description": "Reboot a Meraki device.\n        \n        ⚠️ WARNING: This will disconnect all users and interrupt service!\n        \n        Args:\n            serial: Serial number of the device to reboot\n            \n        Returns:\n            Success/failure information",
        "parameters": [{"name": "serial", "type": "str", "default": null, "required": true}]
    },
    "get_device_clients": {
        "description": "List clients connected to a specific Meraki device.\n        \n        Args:\n            serial: Serial number of the device\n            \n        Returns:\n            Formatted list of clients",
        "parameters": [{"name": "serial", "type": "str", "default": null, "required": true}]
    },
    "get_device_status": {
        "description": "Get status information for a specific Meraki device.\n        \n        Args:\n            serial: Serial number of the device\n            \n        Returns:\n            Formatted status information",
        "parameters": [{"name": "serial", "type": "str", "default": null, "required": true}]
    },
    "claim_device_into_network": {
        "description": "Claim a device from organization inventory into a specific network.\n        \n        Args:\n            network_id: ID of the network to claim the device into\n            serial: Serial number of the device to claim\n            \n        Returns:\n            Success message or error details",
        "parameters": [{"name": "network_id", "type": "str", "default": null, "required": true}, {"name": "serial", "type": "str", "default": null, "required": true}]
    },
    "claim_devices_into_network": {
        "description": "Claim multiple devices into a network.\n        \n        Args:\n            network_id: ID of the network to claim devices into\n            serials: Comma-separated list of device serial numbers\n            \n        Returns:\n            Success message with results",
        "parameters": [{"name": "network_id", "type": "str", "default": null, "required": true}, {"name": "serials", "type": "str", "default": null, "required": true}]
    },
    "list_unassigned_devices": {
        "description": "List devices in organization inventory not assigned to networks.\n        \n        Args:\n            organization_id: ID of the organization\n            \n        Returns:\n            Formatted list of unassigned devices",
        "parameters": [{"name": "organization_id", "type": "str", "default": null, "required": true}]
    },
    "get_network_wireless_ssids": {
        "description": "List wireless SSIDs for a Meraki network.\n        \n        Args:\n            network_id: ID of the network\n            \n        Returns:\n            Formatted list of SSIDs",
        "parameters": [{"name": "network_id", "type": "str", "default": null, "required": true}]
    },
    "get_network_wireless_passwords": {
        "description": "Get WiFi passwords/PSK for wireless networks.\n        \n        Args:\n            network_id: ID of the network\n            \n        Returns:\n            Formatted list of SSIDs with passwords where available",
        "parameters": [{"name": "network_id", "type": "str", "default": null, "required": true}]
    },
    "update_network_wireless_ssid": {
        "description": "Update a wireless SSID for a Meraki network.\n        \n        Args:\n            network_id: ID of the network\n            ssid_number: Number of the SSID to update\n            name: New name for the SSID (optional)\n            enabled: Whether the SSID should be enabled (optional)\n            \n        Returns:\n            Updated SSID details",
        "parameters": [{"name": "network_id", "type": "str", "default": null, "required": true}, {"name": "ssid_number", "type": "int", "default": null, "required": true}, {"name": "name", "type": "str", "default": "None", "required": false}, {"name": "enabled", "type": "bool", "default": "None", "required": false}]
    },
    "get_network_wireless_clients": {
        "description": "List wireless clients for a Meraki network.\n        \n        Args:\n            network_id: ID of the network\n            \n        Returns:\n            Formatted list of wireless clients",
        "parameters": [{"name": "network_id", "type": "str", "default": null, "required": true}]
    },
    "get_network_wireless_usage": {
        "description": "Get wireless usage statistics for a Meraki network.\n        \n        Args:\n            network_id: ID of the network\n            ssid_number: Optional SSID number to filter (0-14)\n            device_serial: Optional device serial to filter by specific AP\n            \n        Returns:\n            Formatted wireless usage statistics",
        "parameters": [{"name": "network_id", "type": "str", "default": null, "required": true}, {"name": "ssid_number", "type": "int", "default": "None", "required": false}, {"name": "device_serial", "type": "str", "default": "None", "required": false}]
    },
    "get_network_wireless_rf_profiles": {
        "description": "Get RF profiles for a wireless network.\n        \n        Args:\n            network_id: ID of the network\n            \n        Returns:\n            RF profiles configuration",
        "parameters": [{"name": "network_id", "type": "str", "default": null, "required": true}]
    },
    "get_network_wireless_air_marshal": {
        "description": "Get Air Marshal (rogue AP detection) results for a network.\n        \n        Args:\n            network_id: ID of the network\n            timespan: Timespan in seconds (default: 1 hour)\n            \n        Returns:\n            Air Marshal security scan results",
        "parameters": [{"name": "network_id", "type": "str", "default": null, "required": true}, {"name": "timespan", "type": "int", "default": "3600", "required": false}]
    },
    "get_network_wireless_bluetooth_clients": {
        "description": "Get Bluetooth clients detected in a wireless network.\n        \n        Args:\n            network_id: ID of the network\n            \n        Returns:\n            List of Bluetooth clients",
        "parameters": [{"name": "network_id", "type": "str", "default": null, "required": true}]
    },
    "get_network_wireless_channel_utilization": {
        "description": "Get wireless channel utilization history for a network.\n        \n        Args:\n            network_id: ID of the network\n            timespan: Timespan in seconds (default: 1 hour)\n            ssid_number: Optional SSID number to filter (0-14)\n            device_serial: Optional device serial to filter by specific AP\n            \n        Returns:\n            Channel utilization statistics",
        "parameters": [{"name": "network_id", "type": "str", "default": null, "required": true}, {"name": "timespan", "type": "int", "default": "3600", "required": false}, {"name": "ssid_number", "type": "int", "default": "None", "required": false}, {"name": "device_serial", "type": "str", "default": "None", "required": false}]
    },
    "get_device_switch_ports": {
        "description": "List switch ports for a Meraki switch.\n        \n        Args:\n            serial: Serial number of the switch\n            \n        Returns:\n            Formatted list of switch ports",
        "parameters": [{"name": "serial", "type": "str", "default": null, "required": true}]
    },
    "update_device_switch_port": {
        "description": "Update a switch port for a Meraki switch.\n        \n        Args:\n            serial: Serial number of the switch\n            port_number: Number of the port to update\n            name: New name for the port (optional)\n            enabled: Whether the port should be enabled (optional)\n            vlan: VLAN ID for the port (optional)\n            poe_enabled: Whether PoE should be enabled (optional)\n            \n        Returns:\n            Updated port details",
        "parameters": [{"name": "serial", "type": "str", "default": null, "required": true}, {"name": "port_number", "type": "int", "default": null, "required": true}, {"name": "name", "type": "str", "default": "None", "required": false}, {"name": "enabled", "type": "bool", "default": "None", "required": false}, {"name": "vlan", "type": "int", "default": "None", "required": false}, {"name": "poe_enabled", "type": "bool", "default": "None", "required": false}]
    },
    "get_device_switch_port_statuses": {
        "description": "Get status information for switch ports.\n        \n        Args:\n            serial: Serial number of the switch\n            \n        Returns:\n            Formatted switch port status information",
        "parameters": [{"name": "serial", "type": "str", "default": null, "required": true}]
    },
    "get_device_switch_vlans": {
        "description": "List VLANs for a Meraki switch.\n        \n        Args:\n            serial: Serial number of the switch\n            \n        Returns:\n            Formatted list of VLANs",
        "parameters": [{"name": "serial", "type": "str", "default": null, "required": true}]
    },
    "create_device_switch_vlan": {
        "description": "Create a new VLAN for a Meraki switch.\n        \n        Args:\n            serial: Serial number of the switch\n            vlan_id: ID for the new VLAN\n            name: Name for the new VLAN\n            subnet: Subnet for the new VLAN (optional)\n            \n        Returns:\n            New VLAN details",
        "parameters": [{"name": "serial", "type": "str", "default": null, "required": true}, {"name": "vlan_id", "type": "int", "default": null, "required": true}, {"name": "name", "type": "str", "default": null, "required": true}, {"name": "subnet", "type": "str", "default": "None", "required": false}]
    },
    "get_organization_uplinks_loss_and_latency": {
        "description": "Get REAL packet loss and latency data for all uplinks in organization.\n        \n        Args:\n            org_id: Organization ID\n            timespan: Timespan in seconds (default: 300 = 5 minutes, max: 300)\n            \n        Returns:\n            Formatted uplink loss and latency data",
        "parameters": [{"name": "org_id", "type": "str", "default": null, "required": true}, {"name": "timespan", "type": "int", "default": "300", "required": false}]
    },
    "get_organization_appliance_uplink_statuses": {
        "description": "Get REAL uplink status for all appliances in organization.\n        \n        Args:\n            org_id: Organization ID\n            \n        Returns:\n            Formatted appliance uplink status data",
        "parameters": [{"name": "org_id", "type": "str", "default": null, "required": true}]
    },
    "get_network_connection_stats": {
        "description": "Get REAL network connection statistics.\n        \n        Args:\n            network_id: Network ID\n            timespan: Timespan in seconds (default: 86400 = 24 hours)\n            \n        Returns:\n            Formatted connection statistics",
        "parameters": [{"name": "network_id", "type": "str", "default": null, "required": true}, {"name": "timespan", "type": "int", "default": "86400", "required": false}]
    },
    "get_network_latency_stats": {
        "description": "Get REAL network latency statistics.\n        \n        Args:\n            network_id: Network ID\n            timespan: Timespan in seconds (default: 86400 = 24 hours)\n            \n        Returns:\n            Formatted latency statistics",
        "parameters": [{"name": "network_id", "type": "str", "default": null, "required": true}, {"name": "timespan", "type": "int", "default": "86400", "required": false}]
    },
    "get_organization_webhooks": {
        "description": "Get all webhooks configured for an organization.\n        \n        Args:\n            org_id: Organization ID\n            \n        Returns:\n            List of webhooks with their configurations",
        "parameters": [{"name": "org_id", "type": "str", "default": null, "required": true}]
    },
    "create_organization_webhook": {
        "description": "Create a new webhook HTTP server for an organization.\n        \n        Args:\n            org_id: Organization ID\n            name: Name of the webhook\n            url: URL to send webhooks to\n            shared_secret: Optional shared secret for security\n            \n        Returns:\n            Created webhook details",
        "parameters": [{"name": "org_id", "type": "str", "default": null, "required": true}, {"name": "name", "type": "str", "default": null, "required": true}, {"name": "url", "type": "str", "default": null, "required": true}, {"name": "shared_secret", "type": "str", "default": "None", "required": false}]
    },
    "get_network_webhook_http_servers": {
        "description": "Get webhook HTTP servers configured for a network.\n        \n        Args:\n            network_id: Network ID\n            \n        Returns:\n            List of webhook HTTP servers",
        "parameters": [{"name": "network_id", "type": "str", "default": null, "required": true}]
    },
    "create_network_webhook_http_server": {
        "description": "Create a webhook HTTP server for a network.\n        \n        Args:\n            network_id: Network ID\n            name: Name of the webhook server\n            url: URL to send webhooks to\n            shared_secret: Optional shared secret\n            \n        Returns:\n            Created webhook server details",
        "parameters": [{"name": "network_id", "type": "str", "default": null, "required": true}, {"name": "name", "type": "str", "default": null, "required": true}, {"name": "url", "type": "str", "default": null, "required": true}, {"name": "shared_secret", "type": "str", "default": "None", "required": false}]
    },
    "get_network_alerts_settings": {
        "description": "Get alert settings for a network.\n        \n        Args:\n            network_id: Network ID\n            \n        Returns:\n            Network alert settings",
        "parameters": [{"name": "network_id", "type": "str", "default": null, "required": true}]
    },
    "update_network_alerts_settings": {
        "description": "Update alert settings for a network.\n        \n        Args:\n            network_id: Network ID\n            emails: Comma-separated email addresses for alerts\n            all_admins: Send alerts to all admins\n            enable_device_down: Enable device down alerts\n            enable_gateway_down: Enable gateway connectivity alerts\n            enable_dhcp_failure: Enable DHCP failure alerts\n            enable_high_usage: Enable high wireless usage alerts\n            enable_ip_conflict: Enable IP conflict detection alerts\n            \n        Returns:\n            Updated alert settings",
        "parameters": [{"name": "network_id", "type": "str", "default": null, "required": true}, {"name": "emails", "type": "str", "default": "None", "required": false}, {"name": "all_admins", "type": "bool", "default": "None", "required": false}, {"name": "enable_device_down", "type": "bool", "default": "None", "required": false}, {"name": "enable_gateway_down", "type": "bool", "default": "None", "required": false}, {"name": "enable_dhcp_failure", "type": "bool", "default": "None", "required": false}, {"name": "enable_high_usage", "type": "bool", "default": "None", "required": false}, {"name": "enable_ip_conflict", "type": "bool", "default": "None", "required": false}]
    },
    "get_network_appliance_firewall_l3_rules": {
        "description": "Get Layer 3 firewall rules for a network appliance.\n        \n        Args:\n            network_id: Network ID\n            \n        Returns:\n            Formatted L3 firewall rules",
        "parameters": [{"name": "network_id", "type": "str", "default": null, "required": true}]
    },
    "update_network_appliance_firewall_l3_rules": {
        "description": "Add a new L3 firewall rule to a network (existing rules are preserved).\n        \n        Args:\n            network_id: Network ID\n            comment: Description of the rule\n            policy: 'allow' or 'deny'\n            protocol: 'tcp', 'udp', 'icmp', or 'any'\n            src_cidr: Source CIDR (e.g., '192.168.1.0/24')\n            dest_cidr: Destination CIDR\n            dest_port: Destination port (optional)\n            syslog_enabled: Enable syslog for this rule\n            \n        Returns:\n            Updated firewall rules",
        "parameters": [{"name": "network_id", "type": "str", "default": null, "required": true}, {"name": "comment", "type": "str", "default": null, "required": true}, {"name": "policy", "type": "str", "default": null, "required": true}, {"name": "protocol", "type": "str", "default": "\"any\"", "required": false}, {"name": "src_cidr", "type": "str", "default": "\"any\"", "required": false}, {"name": "dest_cidr", "type": "str", "default": "\"any\"", "required": false}, {"name": "dest_port", "type": "str", "default": "None", "required": false}, {"name": "syslog_enabled", "type": "bool", "default": "False", "required": false}]
    },
    "get_network_appliance_content_filtering": {
        "description": "Get content filtering settings for a network appliance.\n        \n        Args:\n            network_id: Network ID\n            \n        Returns:\n            Content filtering configuration",
        "parameters": [{"name": "network_id", "type": "str", "default": null, "required": true}]
    },
    "get_network_appliance_vpn_site_to_site": {
        "description": "Get site-to-site VPN settings for a network appliance.\n        \n        Args:\n            network_id: Network ID\n            \n        Returns:\n            Site-to-site VPN configuration",
        "parameters": [{"name": "network_id", "type": "str", "default": null, "required": true}]
    },
    "get_network_appliance_security_malware": {
        "description": "Get malware protection settings for a network appliance.\n        \n        Args:\n            network_id: Network ID\n            \n        Returns:\n            Malware protection configuration",
        "parameters": [{"name": "network_id", "type": "str", "default": null, "required": true}]
    },
    "get_network_appliance_security_intrusion": {
        "description": "Get intrusion detection and prevention settings for a network.\n        \n        Args:\n            network_id: Network ID\n            \n        Returns:\n            IDS/IPS configuration",
        "parameters": [{"name": "network_id", "type": "str", "default": null, "required": true}]
    },
    "get_device_camera_video_link": {
        "description": "Get video link for a camera device.\n        \n        Args:\n            serial: Device serial number\n            timestamp: Optional timestamp (ISO 8601) for historical footage\n            \n        Returns:\n            Video link URL",
        "parameters": [{"name": "serial", "type": "str", "default": null, "required": true}, {"name": "timestamp", "type": "str", "default": "None", "required": false}]
    },
    "get_device_camera_snapshot": {
        "description": "Generate a snapshot from a camera.\n        \n        Args:\n            serial: Device serial number\n            timestamp: Optional timestamp (ISO 8601) for historical snapshot\n            \n        Returns:\n            Snapshot URL",
        "parameters": [{"name": "serial", "type": "str", "default": null, "required": true}, {"name": "timestamp", "type": "str", "default": "None", "required": false}]
    },
    "get_device_camera_video_settings": {
        "description": "Get video settings for a camera device.\n        \n        Args:\n            serial: Device serial number\n            \n        Returns:\n            Camera video settings",
        "parameters": [{"name": "serial", "type": "str", "default": null, "required": true}]
    },
    "update_device_camera_video_settings": {
        "description": "Update video settings for a camera device.\n        \n        Args:\n            serial: Device serial number\n            external_rtsp_enabled: Enable/disable external RTSP access\n            \n        Returns:\n            Updated video settings",
        "parameters": [{"name": "serial", "type": "str", "default": null, "required": true}, {"name": "external_rtsp_enabled", "type": "bool", "default": null, "required": true}]
    },
    "get_device_camera_analytics_zones": {
        "description": "Get analytics zones configured on a camera.\n        \n        Args:\n            serial: Device serial number\n            \n        Returns:\n            Camera analytics zones configuration",
        "parameters": [{"name": "serial", "type": "str", "default": null, "required": true}]
    },
    "get_device_camera_sense": {
        "description": "Get motion detection (sense) settings for a camera.\n        \n        Args:\n            serial: Device serial number\n            \n        Returns:\n            Camera motion detection settings",
        "parameters": [{"name": "serial", "type": "str", "default": null, "required": true}]
    },
    "get_network_sm_devices": {
        "description": "List all devices enrolled in Systems Manager for a network.\n        \n        Args:\n            network_id: Network ID\n            \n        Returns:\n            List of SM devices with details",
        "parameters": [{"name": "network_id", "type": "str", "default": null, "required": true}]
    },
    "get_network_sm_device_detail": {
        "description": "Get detailed information for a specific Systems Manager device.\n        \n        Args:\n            network_id: Network ID\n            device_id: Device ID or serial number\n            \n        Returns:\n            Detailed device information",
        "parameters": [{"name": "network_id", "type": "str", "default": null, "required": true}, {"name": "device_id", "type": "str", "default": null, "required": true}]
    },
    "get_network_sm_device_apps": {
        "description": "List all apps installed on a Systems Manager device.\n        \n        Args:\n            network_id: Network ID\n            device_id: Device ID or serial number\n            \n        Returns:\n            List of installed applications",
        "parameters": [{"name": "network_id", "type": "str", "default": null, "required": true}, {"name": "device_id", "type": "str", "default": null, "required": true}]
    },
    "reboot_network_sm_devices": {
        "description": "Reboot one or more Systems Manager devices.\n        \n        ⚠️ WARNING: This will force devices to restart!\n        \n        Args:\n            network_id: Network ID\n            device_ids: Comma-separated device IDs to reboot\n            \n        Returns:\n            Reboot command status",
        "parameters": [{"name": "network_id", "type": "str", "default": null, "required": true}, {"name": "device_ids", "type": "str", "default": null, "required": true}]
    },
    "get_network_sm_profiles": {
        "description": "List all Systems Manager profiles for a network.\n        \n        Args:\n            network_id: Network ID\n            \n        Returns:\n            List of SM profiles",
        "parameters": [{"name": "network_id", "type": "str", "default": null, "required": true}]
    },
    "get_network_sm_performance_history": {
        "description": "Get performance history for a Systems Manager device.\n        \n        Args:\n            network_id: Network ID\n            device_id: Device ID\n            \n        Returns:\n            Device performance metrics over time",
        "parameters": [{"name": "network_id", "type": "str", "default": null, "required": true}, {"name": "device_id", "type": "str", "default": null, "required": true}]
    },
    "get_organization_licenses": {
        "description": "List all licenses for an organization.\n        \n        Args:\n            org_id: Organization ID\n            \n        Returns:\n            List of licenses with details",
        "parameters": [{"name": "org_id", "type": "str", "default": null, "required": true}]
    },
    "get_organization_licensing_coterm": {
        "description": "Get co-termination licensing model information.\n        \n        Args:\n            org_id: Organization ID\n            \n        Returns:\n            Co-term licensing details",
        "parameters": [{"name": "org_id", "type": "str", "default": null, "required": true}]
    },
    "claim_organization_license": {
        "description": "Claim a new license key for an organization.\n        \n        Args:\n            org_id: Organization ID\n            license_key: License key to claim\n            \n        Returns:\n            Claim result",
        "parameters": [{"name": "org_id", "type": "str", "default": null, "required": true}, {"name": "license_key", "type": "str", "default": null, "required": true}]
    },
    "update_organization_license": {
        "description": "Update a license (typically to assign/unassign to a device).\n        \n        Args:\n            org_id: Organization ID\n            license_id: License ID to update\n            device_serial: Device serial to assign to (or empty to unassign)\n            \n        Returns:\n            Update result",
        "parameters": [{"name": "org_id", "type": "str", "default": null, "required": true}, {"name": "license_id", "type": "str", "default": null, "required": true}, {"name": "device_serial", "type": "str", "default": "None", "required": false}]
    },
    "move_organization_licenses": {
        "description": "Move licenses from one organization to another.\n        \n        Args:\n            source_org_id: Source organization ID\n            dest_org_id: Destination organization ID\n            license_ids: Comma-separated license IDs to move\n            \n        Returns:\n            Move result",
        "parameters": [{"name": "source_org_id", "type": "str", "default": null, "required": true}, {"name": "dest_org_id", "type": "str", "default": null, "required": true}, {"name": "license_ids", "type": "str", "default": null, "required": true}]
    },
    "renew_organization_licenses_seats": {
        "description": "Renew Systems Manager seats by combining licenses.\n        \n        Args:\n            org_id: Organization ID\n            license_id_to_renew: License ID that needs renewal\n            unused_license_id: Unused license ID to apply for renewal\n            \n        Returns:\n            Renewal result",
        "parameters": [{"name": "org_id", "type": "str", "default": null, "required": true}, {"name": "license_id_to_renew", "type": "str", "default": null, "required": true}, {"name": "unused_license_id", "type": "str", "default": null, "required": true}]
    },
    "get_organization_policy_objects": {
        "description": "List all policy objects for an organization.\n        \n        Args:\n            org_id: Organization ID\n            \n        Returns:\n            List of policy objects",
        "parameters": [{"name": "org_id", "type": "str", "default": null, "required": true}]
    },
    "create_organization_policy_object": {
        "description": "Create a new policy object.\n        \n        Args:\n            org_id: Organization ID\n            name: Object name\n            category: Category (e.g., 'network', 'application')\n            type: Type (e.g., 'ipv4', 'fqdn', 'ipv4Range')\n            cidr: CIDR notation for IP objects (e.g., '10.0.0.0/24')\n            fqdn: Fully qualified domain name for FQDN objects\n            ip: Single IP address\n            \n        Returns:\n            Created policy object",
        "parameters": [{"name": "org_id", "type": "str", "default": null, "required": true}, {"name": "name", "type": "str", "default": null, "required": true}, {"name": "category", "type": "str", "default": null, "required": true}, {"name": "type", "type": "str", "default": null, "required": true}, {"name": "cidr", "type": "str", "default": "None", "required": false}, {"name": "fqdn", "type": "str", "default": "None", "required": false}, {"name": "ip", "type": "str", "default": "None", "required": false}]
    },
    "update_organization_policy_object": {
        "description": "Update an existing policy object.\n        \n        Args:\n            org_id: Organization ID\n            policy_object_id: Policy object ID\n            name: New name (optional)\n            cidr: New CIDR for IP objects (optional)\n            fqdn: New FQDN for domain objects (optional)\n            \n        Returns:\n            Updated policy object",
        "parameters": [{"name": "org_id", "type": "str", "default": null, "required": true}, {"name": "policy_object_id", "type": "str", "default": null, "required": true}, {"name": "name", "type": "str", "default": "None", "required": false}, {"name": "cidr", "type": "str", "default": "None", "required": false}, {"name": "fqdn", "type": "str", "default": "None", "required": false}]
    },
    "delete_organization_policy_object": {
        "description": "Delete a policy object.\n        \n        Args:\n            org_id: Organization ID\n            policy_object_id: Policy object ID to delete\n            \n        Returns:\n            Deletion confirmation",
        "parameters": [{"name": "org_id", "type": "str", "default": null, "required": true}, {"name": "policy_object_id", "type": "str", "default": null, "required": true}]
    },
    "get_organization_policy_objects_groups": {
        "description": "List all policy object groups for an organization.\n        \n        Args:\n            org_id: Organization ID\n            \n        Returns:\n            List of policy object groups",
        "parameters": [{"name": "org_id", "type": "str", "default": null, "required": true}]
    },
    "create_organization_policy_objects_group": {
        "description": "Create a new policy object group.\n        \n        Args:\n            org_id: Organization ID\n            name: Group name\n            category: Category (must match objects' category)\n            object_ids: Comma-separated policy object IDs to include\n            \n        Returns:\n            Created policy object group",
        "parameters": [{"name": "org_id", "type": "str", "default": null, "required": true}, {"name": "name", "type": "str", "default": null, "required": true}, {"name": "category", "type": "str", "default": null, "required": true}, {"name": "object_ids", "type": "str", "default": "None", "required": false}]
    },
    "get_device_memory_history": {
        "description": "Get memory utilization history for a device.\n        \n        Args:\n            serial: Device serial number\n            timespan: Time span in seconds (default 1 hour)\n            \n        Returns:\n            Memory utilization history",
        "parameters": [{"name": "serial", "type": "str", "default": null, "required": true}, {"name": "timespan", "type": "int", "default": "3600", "required": false}]
    },
    "get_device_cpu_power_mode_history": {
        "description": "Get CPU power mode history for a wireless device.\n        \n        Args:\n            serial: Device serial number\n            timespan: Time span in seconds (default 1 hour)\n            \n        Returns:\n            CPU power mode history",
        "parameters": [{"name": "serial", "type": "str", "default": null, "required": true}, {"name": "timespan", "type": "int", "default": "3600", "required": false}]
    },
    "get_device_wireless_cpu_load": {
        "description": "Get current CPU load for a wireless device.\n        \n        Args:\n            serial: Device serial number\n            \n        Returns:\n            Current CPU load information",
        "parameters": [{"name": "serial", "type": "str", "default": null, "required": true}]
    },
    "get_organization_switch_ports_history": {
        "description": "Get aggregated switch port statistics history for entire organization.\n        \n        Args:\n            org_id: Organization ID\n            timespan: Time span in seconds (default 1 hour)\n            \n        Returns:\n            Organization-wide switch port history",
        "parameters": [{"name": "org_id", "type": "str", "default": null, "required": true}, {"name": "timespan", "type": "int", "default": "3600", "required": false}]
    },
    "get_organization_devices_migration_status": {
        "description": "Get migration status for devices being migrated in the organization.\n        \n        Args:\n            org_id: Organization ID\n            \n        Returns:\n            Device migration status",
        "parameters": [{"name": "org_id", "type": "str", "default": null, "required": true}]
    },
    "get_organization_api_usage": {
        "description": "Get API usage statistics for monitoring API consumption.\n        \n        Args:\n            org_id: Organization ID\n            timespan: Time span in seconds (default 24 hours)\n            \n        Returns:\n            API usage analytics",
        "parameters": [{"name": "org_id", "type": "str", "default": null, "required": true}, {"name": "timespan", "type": "int", "default": "86400", "required": false}]
    },
    "get_organization_early_access_features": {
        "description": "List all available early access features for an organization.\n        \n        Args:\n            org_id: Organization ID\n            \n        Returns:\n            List of available early access features",
        "parameters": [{"name": "org_id", "type": "str", "default": null, "required": true}]
    },
    "get_organization_early_access_opt_ins": {
        "description": "List all early access features that the organization has opted into.\n        \n        Args:\n            org_id: Organization ID\n            \n        Returns:\n            List of opted-in early access features",
        "parameters": [{"name": "org_id", "type": "str", "default": null, "required": true}]
    },
    "enable_organization_early_access_feature": {
        "description": "Opt into an early access feature for the organization.\n        \n        Args:\n            org_id: Organization ID\n            feature_id: Early access feature ID or short name\n            limit_to_networks: Comma-separated network IDs to limit access (optional)\n            \n        Returns:\n            Opt-in confirmation",
        "parameters": [{"name": "org_id", "type": "str", "default": null, "required": true}, {"name": "feature_id", "type": "str", "default": null, "required": true}, {"name": "limit_to_networks", "type": "str", "default": "None", "required": false}]
    },
    "disable_organization_early_access_feature": {
        "description": "Opt out of an early access feature for the organization.\n        \n        Args:\n            org_id: Organization ID\n            opt_in_id: Opt-in ID to disable\n            \n        Returns:\n            Opt-out confirmation",
        "parameters": [{"name": "org_id", "type": "str", "default": null, "required": true}, {"name": "opt_in_id", "type": "str", "default": null, "required": true}]
    },
    "get_organization_api_analytics": {
        "description": "Get API analytics for the organization (new 2025 feature).\n        \n        Args:\n            org_id: Organization ID\n            timespan: Time span in seconds (default 24 hours)\n            \n        Returns:\n            API analytics data",
        "parameters": [{"name": "org_id", "type": "str", "default": null, "required": true}, {"name": "timespan", "type": "int", "default": "86400", "required": false}]
    },
    "check_beta_apis_status": {
        "description": "Check the status of beta APIs mentioned in the 2025 documentation.\n        \n        Returns:\n            Status of various beta APIs",
        "parameters": []
    },
    "create_device_ping_test": {
        "description": "Create a ping test from a device.\n        \n        Args:\n            serial: Device serial number\n            target: Target IP or hostname to ping\n            count: Number of pings (default 5, max 5)\n            \n        Returns:\n            Ping test job details",
        "parameters": [{"name": "serial", "type": "str", "default": null, "required": true}, {"name": "target", "type": "str", "default": null, "required": true}, {"name": "count", "type": "int", "default": "5", "required": false}]
    },
    "get_device_ping_test": {
        "description": "Get results of a ping test.\n        \n        Args:\n            serial: Device serial number\n            ping_id: Ping test job ID\n            \n        Returns:\n            Ping test results",
        "parameters": [{"name": "serial", "type": "str", "default": null, "required": true}, {"name": "ping_id", "type": "str", "default": null, "required": true}]
    },
    "create_device_throughput_test": {
        "description": "Create a throughput test between two devices.\n        \n        Args:\n            serial: Source device serial\n            target_serial: Target device serial\n            \n        Returns:\n            Throughput test job details",
        "parameters": [{"name": "serial", "type": "str", "default": null, "required": true}, {"name": "target_serial", "type": "str", "default": null, "required": true}]
    },
    "get_device_throughput_test": {
        "description": "Get results of a throughput test.\n        \n        Args:\n            serial: Device serial number\n            test_id: Test job ID\n            \n        Returns:\n            Throughput test results",
        "parameters": [{"name": "serial", "type": "str", "default": null, "required": true}, {"name": "test_id", "type": "str", "default": null, "required": true}]
    },
    "create_switch_cable_test": {
        "description": "Run cable diagnostic test on a switch port.\n        \n        Args:\n            serial: Switch serial number\n            port: Port ID (e.g., \"1\", \"5\")\n            \n        Returns:\n            Cable test job details",
        "parameters": [{"name": "serial", "type": "str", "default": null, "required": true}, {"name": "port", "type": "str", "default": null, "required": true}]
    },
    "get_switch_cable_test": {
        "description": "Get results of a cable test.\n        \n        Args:\n            serial: Switch serial number\n            test_id: Test job ID\n            \n        Returns:\n            Cable test results",
        "parameters": [{"name": "serial", "type": "str", "default": null, "required": true}, {"name": "test_id", "type": "str", "default": null, "required": true}]
    },
    "create_device_wake_on_lan": {
        "description": "Send Wake-on-LAN packet to wake up a device.\n        \n        Args:\n            serial: Device serial to send WOL from\n            vlan_id: VLAN ID\n            mac_address: Target MAC address to wake\n            \n        Returns:\n            WOL job details",
        "parameters": [{"name": "serial", "type": "str", "default": null, "required": true}, {"name": "vlan_id", "type": "int", "default": null, "required": true}, {"name": "mac_address", "type": "str", "default": null, "required": true}]
    },
    "create_switch_mac_table": {
        "description": "Request MAC address table from a switch.\n        \n        Args:\n            serial: Switch serial number\n            \n        Returns:\n            MAC table job details",
        "parameters": [{"name": "serial", "type": "str", "default": null, "required": true}]
    },
    "get_switch_mac_table": {
        "description": "Get MAC address table results.\n        \n        Args:\n            serial: Switch serial number\n            request_id: MAC table request ID\n            \n        Returns:\n            MAC table entries",
        "parameters": [{"name": "serial", "type": "str", "default": null, "required": true}, {"name": "request_id", "type": "str", "default": null, "required": true}]
    },
    "blink_device_leds": {
        "description": "Blink device LEDs to help identify it physically.\n        \n        Args:\n            serial: Device serial number\n            duration: Duration in seconds (default 30)\n            \n        Returns:\n            LED blink job details",
        "parameters": [{"name": "serial", "type": "str", "default": null, "required": true}, {"name": "duration", "type": "int", "default": "30", "required": false}]
    },
}
