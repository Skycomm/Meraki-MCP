"""
Alternate Management Interface tools for Cisco Meraki MCP Server.
Handles alternate management interfaces for switches and wireless devices.
"""

# Global variables to store app and meraki client
app = None
meraki_client = None

def register_alternate_management_tools(mcp_app, meraki):
    """Register alternate management interface tools with the MCP server."""
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    
    # Register all alternate management tools
    register_alternate_management_handlers()

def register_alternate_management_handlers():
    """Register all alternate management tool handlers using the decorator pattern."""
    
    @app.tool(
        name="get_network_switch_alternate_mgmt_interface",
        description="🔧 Get switch alternate management interface settings"
    )
    def get_network_switch_alternate_mgmt_interface(network_id: str):
        """Get alternate management interface settings for switches."""
        try:
            settings = meraki_client.dashboard.switch.getNetworkSwitchAlternateManagementInterface(network_id)
            
            result = f"# 🔧 Switch Alternate Management Interface\n\n"
            
            # Check if enabled
            enabled = settings.get('enabled', False)
            result += f"**Status**: {'✅ Enabled' if enabled else '❌ Disabled'}\n\n"
            
            if enabled:
                # VLAN settings
                result += "## VLAN Configuration\n"
                result += f"- **VLAN ID**: {settings.get('vlanId', 'Not set')}\n"
                
                # Protocols
                protocols = settings.get('protocols', [])
                if protocols:
                    result += f"\n## Enabled Protocols\n"
                    for protocol in protocols:
                        result += f"- {protocol.upper()}\n"
                
                # Switches
                switches = settings.get('switches', [])
                if switches:
                    result += f"\n## Configured Switches ({len(switches)})\n"
                    for switch in switches[:10]:
                        result += f"\n### {switch.get('name', switch.get('serial'))}\n"
                        result += f"- **Serial**: {switch.get('serial')}\n"
                        result += f"- **Alternate Gateway**: {switch.get('alternateGateway', 'Auto')}\n"
                        result += f"- **Subnet Mask**: {switch.get('subnetMask', 'Auto')}\n"
                        result += f"- **Gateway**: {switch.get('gateway', 'Auto')}\n"
                    
                    if len(switches) > 10:
                        result += f"\n... and {len(switches) - 10} more switches\n"
            else:
                result += "Alternate management interface is currently disabled.\n"
                result += "\n## 💡 Benefits of Enabling\n"
                result += "- Separate management traffic from data traffic\n"
                result += "- Maintain access during network issues\n"
                result += "- Enhanced security through isolation\n"
                result += "- Better traffic management\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving switch alternate management interface: {str(e)}"
    
    @app.tool(
        name="update_network_switch_alternate_mgmt_interface",
        description="🔧 Update switch alternate management interface"
    )
    def update_network_switch_alternate_mgmt_interface(network_id: str, **kwargs):
        """
        Update alternate management interface settings for switches.
        
        Args:
            network_id: Network ID
            **kwargs: Settings to update:
                - enabled: Enable/disable alternate management
                - vlanId: VLAN ID for management
                - protocols: List of protocols to enable
                - switches: Switch-specific configurations
        """
        try:
            result = meraki_client.dashboard.switch.updateNetworkSwitchAlternateManagementInterface(
                network_id,
                **kwargs
            )
            
            response = "✅ Switch alternate management interface updated!\n\n"
            
            if 'enabled' in kwargs:
                response += f"## Status\n"
                response += f"- {'Enabled' if kwargs['enabled'] else 'Disabled'}\n"
            
            if 'vlanId' in kwargs:
                response += f"\n## VLAN Configuration\n"
                response += f"- VLAN ID: {kwargs['vlanId']}\n"
            
            if 'protocols' in kwargs:
                response += f"\n## Protocols\n"
                for protocol in kwargs['protocols']:
                    response += f"- {protocol.upper()} enabled\n"
            
            response += "\n⚠️ **Important**: Changes may require switch reboot to take effect."
            
            return response
            
        except Exception as e:
            return f"Error updating switch alternate management interface: {str(e)}"
    
    @app.tool(
        name="get_network_wireless_alternate_mgmt_interface",
        description="📡 Get wireless alternate management interface settings"
    )
    def get_network_wireless_alternate_mgmt_interface(network_id: str):
        """Get alternate management interface settings for wireless."""
        try:
            settings = meraki_client.dashboard.wireless.getNetworkWirelessAlternateManagementInterface(network_id)
            
            result = f"# 📡 Wireless Alternate Management Interface\n\n"
            
            # Check if enabled
            enabled = settings.get('enabled', False)
            result += f"**Status**: {'✅ Enabled' if enabled else '❌ Disabled'}\n\n"
            
            if enabled:
                # VLAN settings
                result += "## VLAN Configuration\n"
                result += f"- **VLAN ID**: {settings.get('vlanId', 'Not set')}\n"
                
                # Protocols
                protocols = settings.get('protocols', [])
                if protocols:
                    result += f"\n## Enabled Protocols\n"
                    for protocol in protocols:
                        result += f"- {protocol.upper()}\n"
                
                # Access Points
                access_points = settings.get('accessPoints', [])
                if access_points:
                    result += f"\n## Configured Access Points ({len(access_points)})\n"
                    for ap in access_points[:10]:
                        result += f"\n### {ap.get('name', ap.get('serial'))}\n"
                        result += f"- **Serial**: {ap.get('serial')}\n"
                        result += f"- **Alternate Gateway**: {ap.get('alternateGateway', 'Auto')}\n"
                        result += f"- **DNS 1**: {ap.get('dns1', 'Auto')}\n"
                        result += f"- **DNS 2**: {ap.get('dns2', 'Auto')}\n"
                    
                    if len(access_points) > 10:
                        result += f"\n... and {len(access_points) - 10} more access points\n"
            else:
                result += "Alternate management interface is currently disabled.\n"
                result += "\n## 💡 Benefits of Enabling\n"
                result += "- Separate AP management from client traffic\n"
                result += "- Maintain AP access during client network issues\n"
                result += "- Enhanced security through traffic isolation\n"
                result += "- Better QoS for management traffic\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving wireless alternate management interface: {str(e)}"
    
    @app.tool(
        name="update_network_wireless_alternate_mgmt_interface",
        description="📡 Update wireless alternate management interface"
    )
    def update_network_wireless_alternate_mgmt_interface(network_id: str, **kwargs):
        """
        Update alternate management interface settings for wireless.
        
        Args:
            network_id: Network ID
            **kwargs: Settings to update:
                - enabled: Enable/disable alternate management
                - vlanId: VLAN ID for management
                - protocols: List of protocols to enable
                - accessPoints: AP-specific configurations
        """
        try:
            result = meraki_client.dashboard.wireless.updateNetworkWirelessAlternateManagementInterface(
                network_id,
                **kwargs
            )
            
            response = "✅ Wireless alternate management interface updated!\n\n"
            
            if 'enabled' in kwargs:
                response += f"## Status\n"
                response += f"- {'Enabled' if kwargs['enabled'] else 'Disabled'}\n"
            
            if 'vlanId' in kwargs:
                response += f"\n## VLAN Configuration\n"
                response += f"- VLAN ID: {kwargs['vlanId']}\n"
            
            if 'protocols' in kwargs:
                response += f"\n## Protocols\n"
                for protocol in kwargs['protocols']:
                    response += f"- {protocol.upper()} enabled\n"
            
            response += "\n⚠️ **Important**: Access points may briefly disconnect during reconfiguration."
            
            return response
            
        except Exception as e:
            return f"Error updating wireless alternate management interface: {str(e)}"
    
    @app.tool(
        name="update_device_wireless_alternate_mgmt_ipv6",
        description="📡 Update device wireless alternate management IPv6"
    )
    def update_device_wireless_alternate_mgmt_ipv6(
        serial: str,
        **kwargs
    ):
        """
        Update IPv6 alternate management interface for a wireless device.
        
        Args:
            serial: Device serial number
            **kwargs: IPv6 configuration parameters
        """
        try:
            result = meraki_client.dashboard.wireless.updateDeviceWirelessAlternateManagementInterfaceIpv6(
                serial,
                **kwargs
            )
            
            response = f"✅ IPv6 alternate management updated for device {serial}!\n\n"
            
            # Show configuration
            if result:
                response += "## IPv6 Configuration\n"
                
                addresses = result.get('addresses', [])
                if addresses:
                    response += "### Addresses\n"
                    for addr in addresses:
                        response += f"- {addr.get('address')}\n"
                        response += f"  Protocol: {addr.get('protocol')}\n"
                        response += f"  Assignment: {addr.get('assignmentMode')}\n"
                
                nameservers = result.get('nameservers', {})
                if nameservers.get('addresses'):
                    response += "\n### DNS Servers\n"
                    for dns in nameservers['addresses']:
                        response += f"- {dns}\n"
            
            response += "\n💡 IPv6 provides enhanced addressing and routing capabilities."
            
            return response
            
        except Exception as e:
            return f"Error updating device wireless alternate management IPv6: {str(e)}"