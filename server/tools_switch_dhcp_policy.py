"""
Switch DHCP Server Policy management tools for Cisco Meraki MCP Server.
Handles DHCP server policies and ARP inspection for switches.
"""

# Global variables to store app and meraki client
app = None
meraki_client = None

def register_switch_dhcp_policy_tools(mcp_app, meraki):
    """Register switch DHCP policy tools with the MCP server."""
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    
    # Register all switch DHCP policy tools
    register_switch_dhcp_policy_handlers()

def register_switch_dhcp_policy_handlers():
    """Register all switch DHCP policy tool handlers using the decorator pattern."""
    
    @app.tool(
        name="get_network_switch_dhcp_server_policy",
        description="🔌 Get DHCP server policy for a switch network"
    )
    def get_network_switch_dhcp_server_policy(network_id: str):
        """Get the DHCP server policy for a switch network."""
        try:
            policy = meraki_client.dashboard.switch.getNetworkSwitchDhcpServerPolicy(network_id)
            
            result = f"# 🔌 Switch DHCP Server Policy\n\n"
            
            # DHCP Server Policy
            result += "## DHCP Server Settings\n"
            result += f"- **Alerts Enabled**: {'✅' if policy.get('alerts', {}).get('email', {}).get('enabled') else '❌'}\n"
            
            # Default Policy
            default_policy = policy.get('defaultPolicy', 'allow')
            result += f"\n## Default Policy\n"
            result += f"- **Action**: {default_policy}\n"
            
            if default_policy == 'block':
                result += "  ⚠️ Blocking unknown DHCP servers by default\n"
            else:
                result += "  ✅ Allowing DHCP servers by default\n"
            
            # Allowed Servers
            allowed_servers = policy.get('allowedServers', [])
            if allowed_servers:
                result += f"\n## Allowed DHCP Servers ({len(allowed_servers)})\n"
                for server in allowed_servers:
                    result += f"- **{server.get('comment', 'No description')}**\n"
                    result += f"  - MAC: {server.get('mac')}\n"
                    result += f"  - VLAN: {server.get('vlan', 'Any')}\n"
                    result += f"  - IPv4: {server.get('ipv4', {}).get('address', 'Any')}\n"
            
            # Blocked Servers
            blocked_servers = policy.get('blockedServers', [])
            if blocked_servers:
                result += f"\n## Blocked DHCP Servers ({len(blocked_servers)})\n"
                for server in blocked_servers:
                    result += f"- **{server.get('comment', 'No description')}**\n"
                    result += f"  - MAC: {server.get('mac')}\n"
                    result += f"  - VLAN: {server.get('vlan', 'Any')}\n"
            
            # ARP Inspection
            arp_inspection = policy.get('arpInspection', {})
            if arp_inspection.get('enabled'):
                result += f"\n## ARP Inspection\n"
                result += f"- **Enabled**: ✅\n"
                
                unsupported_models = arp_inspection.get('unsupportedModels', [])
                if unsupported_models:
                    result += f"- **Unsupported Models**: {', '.join(unsupported_models)}\n"
            else:
                result += f"\n## ARP Inspection\n"
                result += f"- **Enabled**: ❌\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving DHCP server policy: {str(e)}"
    
    @app.tool(
        name="update_network_switch_dhcp_server_policy",
        description="🔌 Update DHCP server policy for a switch network"
    )
    def update_network_switch_dhcp_server_policy(network_id: str, **kwargs):
        """
        Update the DHCP server policy for a switch network.
        
        Args:
            network_id: Network ID
            **kwargs: Policy settings to update:
                - defaultPolicy: 'allow' or 'block'
                - allowedServers: List of allowed DHCP servers
                - blockedServers: List of blocked DHCP servers
                - arpInspection: ARP inspection settings
                - alerts: Alert settings
        """
        try:
            result = meraki_client.dashboard.switch.updateNetworkSwitchDhcpServerPolicy(
                network_id,
                **kwargs
            )
            
            response = "✅ DHCP server policy updated successfully!\n\n"
            
            if 'defaultPolicy' in kwargs:
                response += f"## Default Policy\n"
                response += f"- Action: {kwargs['defaultPolicy']}\n"
                if kwargs['defaultPolicy'] == 'block':
                    response += "- ⚠️ Now blocking unknown DHCP servers\n"
                else:
                    response += "- ✅ Now allowing DHCP servers\n"
            
            if 'allowedServers' in kwargs:
                response += f"\n## Allowed Servers\n"
                response += f"- Updated {len(kwargs['allowedServers'])} allowed servers\n"
            
            if 'blockedServers' in kwargs:
                response += f"\n## Blocked Servers\n"
                response += f"- Updated {len(kwargs['blockedServers'])} blocked servers\n"
            
            if 'arpInspection' in kwargs:
                enabled = kwargs['arpInspection'].get('enabled', False)
                response += f"\n## ARP Inspection\n"
                response += f"- {'Enabled' if enabled else 'Disabled'}\n"
            
            response += "\n💡 **Note**: Changes may take a few minutes to propagate to all switches."
            
            return response
            
        except Exception as e:
            return f"Error updating DHCP server policy: {str(e)}"
    
    @app.tool(
        name="get_network_switch_dhcp_arp_inspection_trusted",
        description="🔍 Get ARP inspection trusted servers"
    )
    def get_network_switch_dhcp_arp_inspection_trusted(network_id: str):
        """Get ARP inspection trusted servers for a network."""
        try:
            servers = meraki_client.dashboard.switch.getNetworkSwitchDhcpServerPolicyArpInspectionTrustedServers(
                network_id
            )
            
            if not servers:
                return f"No ARP inspection trusted servers configured for network {network_id}."
            
            result = f"# 🔍 ARP Inspection Trusted Servers\n\n"
            result += f"**Total Trusted Servers**: {len(servers)}\n\n"
            
            for server in servers:
                result += f"## Server {server.get('trustedServerId')}\n"
                result += f"- **MAC**: {server.get('mac')}\n"
                result += f"- **VLAN**: {server.get('vlan', 'Any')}\n"
                
                ipv4 = server.get('ipv4', {})
                if ipv4.get('address'):
                    result += f"- **IPv4**: {ipv4['address']}\n"
                
                result += f"- **Comment**: {server.get('comment', 'No description')}\n\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving ARP inspection trusted servers: {str(e)}"
    
    @app.tool(
        name="create_switch_dhcp_arp_inspection_trusted",
        description="🔍 Add ARP inspection trusted server"
    )
    def create_switch_dhcp_arp_inspection_trusted(
        network_id: str,
        mac: str,
        vlan: int,
        **kwargs
    ):
        """
        Add a trusted server for ARP inspection.
        
        Args:
            network_id: Network ID
            mac: MAC address of the trusted server
            vlan: VLAN ID
            **kwargs: Additional parameters (ipv4, comment)
        """
        try:
            result = meraki_client.dashboard.switch.createNetworkSwitchDhcpServerPolicyArpInspectionTrustedServer(
                network_id,
                mac=mac,
                vlan=vlan,
                **kwargs
            )
            
            return f"""✅ ARP inspection trusted server added!

**Server ID**: {result.get('trustedServerId')}
**MAC**: {result.get('mac')}
**VLAN**: {result.get('vlan')}
**Comment**: {result.get('comment', 'No description')}

The server is now trusted for ARP inspection on this network."""
            
        except Exception as e:
            return f"Error adding ARP inspection trusted server: {str(e)}"
    
    @app.tool(
        name="update_switch_dhcp_arp_inspection_trusted",
        description="🔍 Update ARP inspection trusted server"
    )
    def update_switch_dhcp_arp_inspection_trusted(
        network_id: str,
        trusted_server_id: str,
        **kwargs
    ):
        """
        Update a trusted server for ARP inspection.
        
        Args:
            network_id: Network ID
            trusted_server_id: Trusted server ID
            **kwargs: Parameters to update (mac, vlan, ipv4, comment)
        """
        try:
            result = meraki_client.dashboard.switch.updateNetworkSwitchDhcpServerPolicyArpInspectionTrustedServer(
                network_id,
                trusted_server_id,
                **kwargs
            )
            
            return f"""✅ ARP inspection trusted server updated!

**Server ID**: {result.get('trustedServerId')}
**MAC**: {result.get('mac')}
**VLAN**: {result.get('vlan')}

Changes have been applied to the trusted server configuration."""
            
        except Exception as e:
            return f"Error updating ARP inspection trusted server: {str(e)}"
    
    @app.tool(
        name="delete_switch_dhcp_arp_inspection_trusted",
        description="🔍 Remove ARP inspection trusted server"
    )
    def delete_switch_dhcp_arp_inspection_trusted(
        network_id: str,
        trusted_server_id: str
    ):
        """Remove a trusted server from ARP inspection."""
        try:
            meraki_client.dashboard.switch.deleteNetworkSwitchDhcpServerPolicyArpInspectionTrustedServer(
                network_id,
                trusted_server_id
            )
            
            return f"✅ ARP inspection trusted server removed successfully!"
            
        except Exception as e:
            return f"Error removing ARP inspection trusted server: {str(e)}"
    
    @app.tool(
        name="get_switch_dhcp_arp_inspection_warnings",
        description="⚠️ Get ARP inspection warnings by device"
    )
    def get_switch_dhcp_arp_inspection_warnings(network_id: str):
        """Get ARP inspection warnings grouped by device."""
        try:
            warnings = meraki_client.dashboard.switch.getNetworkSwitchDhcpServerPolicyArpInspectionWarningsByDevice(
                network_id
            )
            
            if not warnings:
                return f"No ARP inspection warnings for network {network_id}. ✅"
            
            result = f"# ⚠️ ARP Inspection Warnings\n\n"
            result += f"**Devices with Warnings**: {len(warnings)}\n\n"
            
            for device in warnings[:10]:  # Limit to first 10 devices
                result += f"## Device: {device.get('name', device.get('serial'))}\n"
                result += f"- **Serial**: {device.get('serial')}\n"
                result += f"- **URL**: {device.get('url')}\n"
                
                has_trusted_port = device.get('hasTrustedPort', False)
                result += f"- **Has Trusted Port**: {'✅' if has_trusted_port else '❌'}\n"
                
                if not has_trusted_port:
                    result += "  ⚠️ This device needs a trusted port configured\n"
                
                result += "\n"
            
            if len(warnings) > 10:
                result += f"... and {len(warnings) - 10} more devices with warnings\n"
            
            result += "\n## 💡 Recommendations\n"
            result += "1. Configure trusted ports on switches with warnings\n"
            result += "2. Add legitimate DHCP servers to trusted list\n"
            result += "3. Enable ARP inspection on critical VLANs\n"
            result += "4. Monitor for rogue DHCP servers regularly\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving ARP inspection warnings: {str(e)}"