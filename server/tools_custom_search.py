"""
Search tools for finding devices across organizations.
"""

from typing import Optional

app = None
meraki_client = None

def register_search_tools(mcp_app, meraki):
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    """Register search tools with the MCP server."""
    
    @app.tool(
        name="search_device_by_serial",
        description="🔍 Search for a device by serial number across all organizations"
    )
    def search_device_by_serial(serial: str):
        """
        Search for a device by serial number across all organizations.
        
        Args:
            serial: Device serial number to search for
            
        Returns:
            Device details and location if found
        """
        try:
            # Normalize serial to uppercase
            serial = serial.upper()
            
            # Get all organizations
            orgs = meraki_client.get_organizations()
            
            result = f"# 🔍 Searching for device: {serial}\n\n"
            
            for org in orgs:
                org_id = org['id']
                org_name = org.get('name', 'Unknown')
                
                try:
                    # Check organization inventory for the device
                    devices = meraki_client.get_organization_devices(org_id)
                    
                    for device in devices:
                        if device.get('serial', '').upper() == serial:
                            # Found the device!
                            result = f"# ✅ Device Found!\n\n"
                            result += f"## Organization\n"
                            result += f"- **Name**: {org_name}\n"
                            result += f"- **ID**: {org_id}\n\n"
                            
                            result += f"## Device Details\n"
                            result += f"- **Serial**: {device.get('serial')}\n"
                            result += f"- **Name**: {device.get('name', 'Unnamed')}\n"
                            result += f"- **Model**: {device.get('model')}\n"
                            result += f"- **MAC**: {device.get('mac')}\n"
                            
                            # Check if claimed to a network
                            network_id = device.get('networkId')
                            if network_id:
                                try:
                                    network = meraki_client.get_network(network_id)
                                    result += f"\n## Network\n"
                                    result += f"- **Name**: {network.get('name')}\n"
                                    result += f"- **ID**: {network_id}\n"
                                except:
                                    result += f"\n## Network\n"
                                    result += f"- **ID**: {network_id}\n"
                            else:
                                result += f"\n## Status\n"
                                result += f"- **Unclaimed** (not assigned to any network)\n"
                            
                            # Add location info if available
                            if device.get('address'):
                                result += f"\n## Location\n"
                                result += f"- **Address**: {device.get('address')}\n"
                            if device.get('lat') and device.get('lng'):
                                result += f"- **Coordinates**: {device.get('lat')}, {device.get('lng')}\n"
                            
                            return result
                            
                except Exception as e:
                    # Skip organizations we can't access
                    continue
            
            # Device not found
            result += f"❌ Device with serial **{serial}** not found in any accessible organization.\n\n"
            result += "Possible reasons:\n"
            result += "- Serial number is incorrect\n"
            result += "- Device is not claimed to any organization\n"
            result += "- You don't have API access to the organization containing this device\n"
            
            return result
            
        except Exception as e:
            return f"❌ Error searching for device: {str(e)}"
    
    @app.tool(
        name="search_devices_by_model",
        description="🔍 Search for all devices of a specific model across organizations"
    )
    def search_devices_by_model(model: str, org_id: Optional[str] = None):
        """
        Search for devices by model across organizations.
        
        Args:
            model: Device model to search for (e.g., MR33, MS120-8LP)
            org_id: Optional - limit search to specific organization
            
        Returns:
            List of matching devices
        """
        try:
            result = f"# 🔍 Searching for devices: Model {model}\n\n"
            total_found = 0
            
            if org_id:
                # Search specific organization
                orgs = [meraki_client.get_organization(org_id)]
            else:
                # Search all organizations
                orgs = meraki_client.get_organizations()
            
            for org in orgs:
                org_id = org['id'] if isinstance(org, dict) else org
                org_name = org.get('name', 'Unknown') if isinstance(org, dict) else 'Unknown'
                org_found = []
                
                try:
                    devices = meraki_client.get_organization_devices(org_id)
                    
                    for device in devices:
                        if model.upper() in device.get('model', '').upper():
                            org_found.append(device)
                            total_found += 1
                    
                    if org_found:
                        result += f"## {org_name} ({len(org_found)} devices)\n"
                        for device in org_found[:10]:  # Limit to first 10 per org
                            result += f"- **{device.get('name', 'Unnamed')}** "
                            result += f"({device.get('serial')})\n"
                            if device.get('networkId'):
                                result += f"  - Network: {device.get('networkId')}\n"
                        if len(org_found) > 10:
                            result += f"  - *...and {len(org_found) - 10} more*\n"
                        result += "\n"
                        
                except:
                    continue
            
            if total_found == 0:
                result += f"❌ No devices found with model matching '{model}'\n"
            else:
                result += f"## Summary\n"
                result += f"**Total devices found**: {total_found}\n"
            
            return result
            
        except Exception as e:
            return f"❌ Error searching devices: {str(e)}"
    
    @app.tool(
        name="find_unclaimed_devices",
        description="🔍 Find all unclaimed devices across all organizations"
    )
    def find_unclaimed_devices():
        """
        Find all unclaimed devices across all organizations.
        
        Returns:
            List of unclaimed devices
        """
        try:
            result = f"# 🔍 Finding Unclaimed Devices\n\n"
            total_unclaimed = 0
            
            orgs = meraki_client.get_organizations()
            
            for org in orgs:
                org_id = org['id']
                org_name = org.get('name', 'Unknown')
                
                try:
                    devices = meraki_client.get_organization_devices(org_id)
                    unclaimed = [d for d in devices if not d.get('networkId')]
                    
                    if unclaimed:
                        result += f"## {org_name}\n"
                        for device in unclaimed:
                            result += f"- **{device.get('model')}** - {device.get('serial')}\n"
                            result += f"  - Name: {device.get('name', 'Unnamed')}\n"
                            result += f"  - MAC: {device.get('mac')}\n"
                            total_unclaimed += 1
                        result += "\n"
                        
                except:
                    continue
            
            if total_unclaimed == 0:
                result += "✅ No unclaimed devices found in any organization\n"
            else:
                result += f"## Summary\n"
                result += f"**Total unclaimed devices**: {total_unclaimed}\n"
                result += "\nThese devices are in inventory but not assigned to any network.\n"
            
            return result
            
        except Exception as e:
            return f"❌ Error finding unclaimed devices: {str(e)}"