"""
DHCP configuration tools for Single LAN networks.
Provides DHCP management for networks without VLANs enabled.
"""

from typing import Optional
import logging

logger = logging.getLogger(__name__)

def register_single_lan_dhcp_tools(mcp_app, meraki):
    """Register Single LAN DHCP tools that use the correct Single LAN API endpoints."""
    
    @mcp_app.tool()
    def get_single_lan_dhcp_settings(network_id: str) -> str:
        """
        🔧 [Single LAN] Get DHCP settings for Single LAN network.
        
        ⚠️ For Single LAN networks only (no VLANs)! Use check_dhcp_network_type first.
        
        Args:
            network_id: Network ID
            
        Returns:
            Formatted DHCP configuration details
        """
        try:
            # Use the correct Single LAN endpoint
            config = meraki.get_network_appliance_single_lan(network_id)
            
            result = f"# DHCP Settings for Single LAN Network\n\n"
            result += f"**Network**: {network_id}\n"
            result += f"**Subnet**: {config.get('subnet', 'Unknown')}\n"
            result += f"**Appliance IP**: {config.get('applianceIp', 'Unknown')}\n\n"
            
            # DHCP Handling Mode
            dhcp_handling = config.get('dhcpHandling', 'Not configured')
            result += f"## DHCP Mode\n"
            result += f"- **Handling**: {dhcp_handling}\n"
            
            if dhcp_handling == 'Run a DHCP server':
                # DHCP Server Settings
                result += f"\n## DHCP Server Configuration\n"
                result += f"- **Lease Time**: {config.get('dhcpLeaseTime', 'Default')}\n"
                result += f"- **DNS Nameservers**: {config.get('dnsNameservers', 'Default')}\n"
                
                # Custom DNS servers
                custom_dns = config.get('dnsCustomNameservers', [])
                if custom_dns:
                    result += f"- **Custom DNS Servers**: {', '.join(custom_dns)}\n"
                
                # Fixed IP Assignments
                fixed_ips = config.get('fixedIpAssignments', {})
                if fixed_ips:
                    result += f"\n### Fixed IP Assignments ({len(fixed_ips)} total)\n"
                    for mac, assignment in fixed_ips.items():
                        result += f"- **{mac}**: {assignment['ip']}"
                        if assignment.get('name'):
                            result += f" ({assignment['name']})"
                        result += "\n"
                
                # Reserved IP Ranges
                reserved_ranges = config.get('reservedIpRanges', [])
                if reserved_ranges:
                    result += f"\n### Reserved IP Ranges\n"
                    for range_item in reserved_ranges:
                        result += f"- **{range_item['start']} - {range_item['end']}**"
                        if range_item.get('comment'):
                            result += f" ({range_item['comment']})"
                        result += "\n"
                
                # Custom DHCP Options
                dhcp_options = config.get('dhcpOptions', [])
                if dhcp_options:
                    result += f"\n### Custom DHCP Options\n"
                    for option in dhcp_options:
                        result += f"- **Option {option['code']}**: {option['value']} (Type: {option['type']})\n"
                
                # DHCP Boot Options
                if config.get('dhcpBootOptionsEnabled'):
                    result += f"\n### Boot Options\n"
                    result += f"- **Enabled**: ✅\n"
                    result += f"- **Next Server**: {config.get('dhcpBootNextServer', 'Not set')}\n"
                    result += f"- **Boot Filename**: {config.get('dhcpBootFilename', 'Not set')}\n"
            
            return result
            
        except Exception as e:
            logger.error(f"Error getting Single LAN DHCP settings: {e}")
            error_msg = str(e)
            
            # Provide helpful guidance
            if "vlans" in error_msg.lower() and "enabled" in error_msg.lower():
                return f"""❌ This network has VLANs enabled!

You're using Single LAN tools on a VLAN-enabled network.
→ Use `check_dhcp_network_type(network_id="{network_id}")` to see available VLANs
→ Use VLAN DHCP tools like `get_vlan_dhcp_settings` instead

Original error: {error_msg}"""
            
            return f"❌ Error getting Single LAN DHCP settings: {error_msg}"
    
    @mcp_app.tool()
    def add_single_lan_fixed_ip(network_id: str, mac_address: str, 
                               ip_address: str, name: Optional[str] = None) -> str:
        """
        🔧 [Single LAN] Add a fixed IP assignment to Single LAN network.
        
        ⚠️ For Single LAN networks only (no VLANs)! Use check_dhcp_network_type first.
        For VLAN networks, use add_dhcp_fixed_assignment instead.
        
        Args:
            network_id: Network ID
            mac_address: MAC address (format: XX:XX:XX:XX:XX:XX)
            ip_address: IP address to assign (must be within network subnet)
            name: Optional name for the assignment
            
        Returns:
            Configuration result
        """
        try:
            # Get current Single LAN config
            config = meraki.get_network_appliance_single_lan(network_id)
            
            # Get existing fixed assignments or create new dict
            fixed_assignments = config.get('fixedIpAssignments', {})
            
            # Add new assignment
            assignment = {"ip": ip_address}
            if name:
                assignment["name"] = name
            
            fixed_assignments[mac_address] = assignment
            
            # Update Single LAN configuration
            # API requires at least one of: subnet, applianceIp, ipv6, or mandatoryDhcp
            update_data = {
                "subnet": config.get('subnet'),
                "applianceIp": config.get('applianceIp'),
                "fixedIpAssignments": fixed_assignments
            }
            meraki.update_network_appliance_single_lan(network_id, **update_data)
            
            result = f"✅ Fixed IP assignment added for Single LAN\n\n"
            result += f"- **MAC Address**: {mac_address}\n"
            result += f"- **IP Address**: {ip_address}\n"
            if name:
                result += f"- **Name**: {name}\n"
            
            return result
            
        except Exception as e:
            logger.error(f"Error adding fixed IP assignment: {e}")
            error_msg = str(e)
            
            # Provide helpful guidance
            if "vlans" in error_msg.lower() and "enabled" in error_msg.lower():
                return f"""❌ This network has VLANs enabled!

You're using Single LAN tools on a VLAN-enabled network.
→ Use `check_dhcp_network_type(network_id="{network_id}")` to see available VLANs
→ Use `add_dhcp_fixed_assignment` with the appropriate VLAN ID instead

Original error: {error_msg}"""
            elif "400" in error_msg:
                return f"""❌ API Error - This might be a configuration issue.

Possible solutions:
1. Verify the MAC address format (XX:XX:XX:XX:XX:XX)
2. Ensure the IP address is within the network subnet
3. Check if the IP is already assigned to another device

Original error: {error_msg}"""
            
            return f"❌ Error adding fixed IP assignment: {error_msg}"
    
    @mcp_app.tool()
    def add_single_lan_dhcp_option(network_id: str, code: int, 
                                  type: str, value: str) -> str:
        """
        🔧 Add a custom DHCP option to Single LAN network.
        
        Args:
            network_id: Network ID
            code: DHCP option code (1-254)
            type: Option type (text, ip, hex, integer)
            value: Option value
            
        Returns:
            Configuration result
        """
        try:
            # Get current Single LAN config
            config = meraki.get_network_appliance_single_lan(network_id)
            
            # Get existing DHCP options or create new list
            dhcp_options = config.get('dhcpOptions', [])
            
            # Check if option already exists
            existing_option = next((opt for opt in dhcp_options if opt['code'] == str(code)), None)
            if existing_option:
                return f"⚠️ DHCP option {code} already exists. Remove it first to update."
            
            # Add new option
            new_option = {
                "code": str(code),
                "type": type,
                "value": value
            }
            dhcp_options.append(new_option)
            
            # Update Single LAN configuration
            # API requires at least one of: subnet, applianceIp, ipv6, or mandatoryDhcp
            update_data = {
                "subnet": config.get('subnet'),
                "applianceIp": config.get('applianceIp'),
                "dhcpOptions": dhcp_options
            }
            meraki.update_network_appliance_single_lan(network_id, **update_data)
            
            result = f"✅ Custom DHCP option added for Single LAN\n\n"
            result += f"- **Option Code**: {code}\n"
            result += f"- **Type**: {type}\n"
            result += f"- **Value**: {value}\n"
            
            return result
            
        except Exception as e:
            logger.error(f"Error adding custom DHCP option: {e}")
            return f"❌ Error adding custom DHCP option: {str(e)}"
    
    @mcp_app.tool()
    def remove_single_lan_fixed_ip(network_id: str, mac_address: str) -> str:
        """
        🔧 Remove a fixed IP assignment from Single LAN network.
        
        Args:
            network_id: Network ID
            mac_address: MAC address to remove
            
        Returns:
            Configuration result
        """
        try:
            # Get current Single LAN config
            config = meraki.get_network_appliance_single_lan(network_id)
            
            # Get existing fixed assignments
            fixed_assignments = config.get('fixedIpAssignments', {})
            
            if mac_address not in fixed_assignments:
                return f"⚠️ MAC address {mac_address} not found in fixed assignments"
            
            # Remove assignment
            del fixed_assignments[mac_address]
            
            # Update Single LAN configuration
            # API requires at least one of: subnet, applianceIp, ipv6, or mandatoryDhcp
            update_data = {
                "subnet": config.get('subnet'),
                "applianceIp": config.get('applianceIp'),
                "fixedIpAssignments": fixed_assignments
            }
            meraki.update_network_appliance_single_lan(network_id, **update_data)
            
            return f"✅ Fixed IP assignment removed for MAC {mac_address}"
            
        except Exception as e:
            logger.error(f"Error removing fixed IP assignment: {e}")
            return f"❌ Error removing fixed IP assignment: {str(e)}"
    
    @mcp_app.tool()
    def list_single_lan_fixed_ips(network_id: str) -> str:
        """
        🔧 [Single LAN] List all fixed IP assignments in Single LAN network.
        
        ⚠️ For Single LAN networks only (no VLANs)! Use check_dhcp_network_type first.
        
        Args:
            network_id: Network ID
            
        Returns:
            List of fixed IP assignments with details
        """
        try:
            # Get current Single LAN config
            config = meraki.get_network_appliance_single_lan(network_id)
            
            fixed_ips = config.get('fixedIpAssignments', {})
            
            result = f"# Fixed IP Assignments for Single LAN\n\n"
            result += f"**Network**: {network_id}\n"
            result += f"**Subnet**: {config.get('subnet', 'Unknown')}\n"
            result += f"**Total Reservations**: {len(fixed_ips)}\n\n"
            
            if not fixed_ips:
                result += "No fixed IP assignments configured.\n"
            else:
                result += "| MAC Address | IP Address | Name |\n"
                result += "|-------------|------------|------|\n"
                for mac, assignment in sorted(fixed_ips.items(), key=lambda x: x[1]['ip']):
                    name = assignment.get('name', '-')
                    result += f"| {mac} | {assignment['ip']} | {name} |\n"
            
            # Show DHCP options if any
            dhcp_options = config.get('dhcpOptions', [])
            if dhcp_options:
                result += f"\n## Custom DHCP Options\n"
                for option in dhcp_options:
                    result += f"- **Option {option['code']}**: {option['value']} (Type: {option['type']})\n"
            
            return result
            
        except Exception as e:
            logger.error(f"Error listing fixed IP assignments: {e}")
            return f"❌ Error listing fixed IP assignments: {str(e)}"
    
    @mcp_app.tool()
    def remove_single_lan_dhcp_option(network_id: str, code: int) -> str:
        """
        🔧 Remove a custom DHCP option from Single LAN network.
        
        Args:
            network_id: Network ID
            code: DHCP option code to remove
            
        Returns:
            Configuration result
        """
        try:
            # Get current Single LAN config
            config = meraki.get_network_appliance_single_lan(network_id)
            
            # Get existing DHCP options
            dhcp_options = config.get('dhcpOptions', [])
            
            # Find and remove the option
            new_options = [opt for opt in dhcp_options if opt['code'] != str(code)]
            
            if len(new_options) == len(dhcp_options):
                return f"⚠️ DHCP option {code} not found"
            
            # Update Single LAN configuration
            # API requires at least one of: subnet, applianceIp, ipv6, or mandatoryDhcp
            update_data = {
                "subnet": config.get('subnet'),
                "applianceIp": config.get('applianceIp'),
                "dhcpOptions": new_options
            }
            meraki.update_network_appliance_single_lan(network_id, **update_data)
            
            return f"✅ DHCP option {code} removed successfully"
            
        except Exception as e:
            logger.error(f"Error removing DHCP option: {e}")
            return f"❌ Error removing DHCP option: {str(e)}"