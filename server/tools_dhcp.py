"""
DHCP configuration tools for Cisco Meraki networks.
Provides comprehensive DHCP management capabilities.
"""

from typing import Optional, Dict, Any, List
import logging

logger = logging.getLogger(__name__)

def register_dhcp_tools(mcp_app, meraki):
    """Register all DHCP-related tools with the MCP application."""
    
    @mcp_app.tool()
    async def get_vlan_dhcp_settings(network_id: str, vlan_id: str) -> str:
        """
        🔧 Get DHCP settings for a specific VLAN.
        
        Args:
            network_id: Network ID
            vlan_id: VLAN ID
            
        Returns:
            Formatted DHCP configuration details
        """
        try:
            # Get VLAN configuration including DHCP settings
            vlan = await meraki.get(f"/networks/{network_id}/appliance/vlans/{vlan_id}")
            
            result = f"# DHCP Settings for VLAN {vlan_id}\n\n"
            result += f"**Network**: {network_id}\n"
            result += f"**VLAN**: {vlan.get('name', 'Unknown')} (ID: {vlan_id})\n\n"
            
            # DHCP Handling Mode
            dhcp_handling = vlan.get('dhcpHandling', 'Not configured')
            result += f"## DHCP Mode\n"
            result += f"- **Handling**: {dhcp_handling}\n"
            
            if dhcp_handling == 'Run a DHCP server':
                # DHCP Server Settings
                result += f"\n## DHCP Server Configuration\n"
                result += f"- **Lease Time**: {vlan.get('dhcpLeaseTime', 'Default')}\n"
                result += f"- **DNS Nameservers**: {vlan.get('dnsNameservers', 'Default')}\n"
                
                # DHCP Boot Options
                if vlan.get('dhcpBootOptionsEnabled'):
                    result += f"\n### Boot Options\n"
                    result += f"- **Enabled**: ✅\n"
                    result += f"- **Next Server**: {vlan.get('dhcpBootNextServer', 'Not set')}\n"
                    result += f"- **Boot Filename**: {vlan.get('dhcpBootFilename', 'Not set')}\n"
                
                # Reserved IP Ranges
                reserved_ranges = vlan.get('reservedIpRanges', [])
                if reserved_ranges:
                    result += f"\n### Reserved IP Ranges\n"
                    for range_item in reserved_ranges:
                        result += f"- **{range_item['start']} - {range_item['end']}**"
                        if range_item.get('comment'):
                            result += f" ({range_item['comment']})"
                        result += "\n"
                
                # Fixed IP Assignments
                fixed_ips = vlan.get('fixedIpAssignments', {})
                if fixed_ips:
                    result += f"\n### Fixed IP Assignments\n"
                    for mac, assignment in fixed_ips.items():
                        result += f"- **{mac}**: {assignment['ip']}"
                        if assignment.get('name'):
                            result += f" ({assignment['name']})"
                        result += "\n"
                
                # Custom DHCP Options
                dhcp_options = vlan.get('dhcpOptions', [])
                if dhcp_options:
                    result += f"\n### Custom DHCP Options\n"
                    for option in dhcp_options:
                        result += f"- **Option {option['code']}**: {option['value']} (Type: {option['type']})\n"
                
                # Mandatory DHCP
                if vlan.get('mandatoryDhcp', {}).get('enabled'):
                    result += f"\n### Mandatory DHCP\n"
                    result += f"- **Enabled**: ✅ (Clients must use DHCP)\n"
                    
            elif dhcp_handling == 'Relay DHCP to another server':
                # DHCP Relay Settings
                result += f"\n## DHCP Relay Configuration\n"
                relay_servers = vlan.get('dhcpRelayServerIps', [])
                if relay_servers:
                    result += f"### Relay Servers\n"
                    for server in relay_servers:
                        result += f"- {server}\n"
                else:
                    result += "- No relay servers configured\n"
            
            return result
            
        except Exception as e:
            logger.error(f"Error getting DHCP settings: {e}")
            return f"❌ Error getting DHCP settings: {str(e)}"
    
    @mcp_app.tool()
    async def update_vlan_dhcp_server(network_id: str, vlan_id: str, 
                                     lease_time: str = "1 day",
                                     dns_nameservers: str = "upstream_dns") -> str:
        """
        🔧 Configure VLAN to run DHCP server with basic settings.
        
        Args:
            network_id: Network ID
            vlan_id: VLAN ID
            lease_time: DHCP lease time (30 minutes, 1 hour, 4 hours, 12 hours, 1 day, 1 week)
            dns_nameservers: DNS servers (upstream_dns, google_dns, opendns, or comma-separated IPs)
            
        Returns:
            Configuration result
        """
        try:
            data = {
                "dhcpHandling": "Run a DHCP server",
                "dhcpLeaseTime": lease_time,
                "dnsNameservers": dns_nameservers
            }
            
            await meraki.put(f"/networks/{network_id}/appliance/vlans/{vlan_id}", data)
            
            result = f"✅ DHCP Server configured for VLAN {vlan_id}\n\n"
            result += f"- **Mode**: Run a DHCP server\n"
            result += f"- **Lease Time**: {lease_time}\n"
            result += f"- **DNS Servers**: {dns_nameservers}\n"
            
            return result
            
        except Exception as e:
            logger.error(f"Error configuring DHCP server: {e}")
            return f"❌ Error configuring DHCP server: {str(e)}"
    
    @mcp_app.tool()
    async def configure_dhcp_relay(network_id: str, vlan_id: str, 
                                  relay_server_ips: str) -> str:
        """
        🔧 Configure VLAN to relay DHCP to another server.
        
        Args:
            network_id: Network ID
            vlan_id: VLAN ID
            relay_server_ips: Comma-separated list of DHCP relay server IPs
            
        Returns:
            Configuration result
        """
        try:
            servers = [ip.strip() for ip in relay_server_ips.split(",")]
            
            data = {
                "dhcpHandling": "Relay DHCP to another server",
                "dhcpRelayServerIps": servers
            }
            
            await meraki.put(f"/networks/{network_id}/appliance/vlans/{vlan_id}", data)
            
            result = f"✅ DHCP Relay configured for VLAN {vlan_id}\n\n"
            result += f"- **Mode**: Relay DHCP to another server\n"
            result += f"- **Relay Servers**:\n"
            for server in servers:
                result += f"  - {server}\n"
            
            return result
            
        except Exception as e:
            logger.error(f"Error configuring DHCP relay: {e}")
            return f"❌ Error configuring DHCP relay: {str(e)}"
    
    @mcp_app.tool()
    async def disable_vlan_dhcp(network_id: str, vlan_id: str) -> str:
        """
        🔧 Disable DHCP on a VLAN.
        
        Args:
            network_id: Network ID
            vlan_id: VLAN ID
            
        Returns:
            Configuration result
        """
        try:
            data = {
                "dhcpHandling": "Do not respond to DHCP requests"
            }
            
            await meraki.put(f"/networks/{network_id}/appliance/vlans/{vlan_id}", data)
            
            return f"✅ DHCP disabled for VLAN {vlan_id}\n\nThe VLAN will not respond to DHCP requests."
            
        except Exception as e:
            logger.error(f"Error disabling DHCP: {e}")
            return f"❌ Error disabling DHCP: {str(e)}"
    
    @mcp_app.tool()
    async def add_dhcp_fixed_assignment(network_id: str, vlan_id: str,
                                       mac_address: str, ip_address: str,
                                       name: Optional[str] = None) -> str:
        """
        🔧 Add a fixed IP assignment (DHCP reservation) for a MAC address.
        
        Args:
            network_id: Network ID
            vlan_id: VLAN ID
            mac_address: MAC address (format: XX:XX:XX:XX:XX:XX)
            ip_address: IP address to assign
            name: Optional name for the assignment
            
        Returns:
            Configuration result
        """
        try:
            # Get current VLAN config
            vlan = await meraki.get(f"/networks/{network_id}/appliance/vlans/{vlan_id}")
            
            # Get existing fixed assignments or create new dict
            fixed_assignments = vlan.get('fixedIpAssignments', {})
            
            # Add new assignment
            assignment = {"ip": ip_address}
            if name:
                assignment["name"] = name
            
            fixed_assignments[mac_address] = assignment
            
            # Update VLAN
            data = {"fixedIpAssignments": fixed_assignments}
            await meraki.put(f"/networks/{network_id}/appliance/vlans/{vlan_id}", data)
            
            result = f"✅ Fixed IP assignment added for VLAN {vlan_id}\n\n"
            result += f"- **MAC Address**: {mac_address}\n"
            result += f"- **IP Address**: {ip_address}\n"
            if name:
                result += f"- **Name**: {name}\n"
            
            return result
            
        except Exception as e:
            logger.error(f"Error adding fixed IP assignment: {e}")
            return f"❌ Error adding fixed IP assignment: {str(e)}"
    
    @mcp_app.tool()
    async def remove_dhcp_fixed_assignment(network_id: str, vlan_id: str,
                                          mac_address: str) -> str:
        """
        🔧 Remove a fixed IP assignment (DHCP reservation).
        
        Args:
            network_id: Network ID
            vlan_id: VLAN ID
            mac_address: MAC address to remove
            
        Returns:
            Configuration result
        """
        try:
            # Get current VLAN config
            vlan = await meraki.get(f"/networks/{network_id}/appliance/vlans/{vlan_id}")
            
            # Get existing fixed assignments
            fixed_assignments = vlan.get('fixedIpAssignments', {})
            
            if mac_address not in fixed_assignments:
                return f"⚠️ MAC address {mac_address} not found in fixed assignments"
            
            # Remove assignment
            del fixed_assignments[mac_address]
            
            # Update VLAN
            data = {"fixedIpAssignments": fixed_assignments}
            await meraki.put(f"/networks/{network_id}/appliance/vlans/{vlan_id}", data)
            
            return f"✅ Fixed IP assignment removed for MAC {mac_address}"
            
        except Exception as e:
            logger.error(f"Error removing fixed IP assignment: {e}")
            return f"❌ Error removing fixed IP assignment: {str(e)}"
    
    @mcp_app.tool()
    async def add_dhcp_reserved_range(network_id: str, vlan_id: str,
                                     start_ip: str, end_ip: str,
                                     comment: Optional[str] = None) -> str:
        """
        🔧 Add a reserved IP range to exclude from DHCP pool.
        
        Args:
            network_id: Network ID
            vlan_id: VLAN ID
            start_ip: Start IP of the range
            end_ip: End IP of the range
            comment: Optional comment for the range
            
        Returns:
            Configuration result
        """
        try:
            # Get current VLAN config
            vlan = await meraki.get(f"/networks/{network_id}/appliance/vlans/{vlan_id}")
            
            # Get existing reserved ranges or create new list
            reserved_ranges = vlan.get('reservedIpRanges', [])
            
            # Add new range
            new_range = {
                "start": start_ip,
                "end": end_ip
            }
            if comment:
                new_range["comment"] = comment
            
            reserved_ranges.append(new_range)
            
            # Update VLAN
            data = {"reservedIpRanges": reserved_ranges}
            await meraki.put(f"/networks/{network_id}/appliance/vlans/{vlan_id}", data)
            
            result = f"✅ Reserved IP range added for VLAN {vlan_id}\n\n"
            result += f"- **Range**: {start_ip} - {end_ip}\n"
            if comment:
                result += f"- **Comment**: {comment}\n"
            
            return result
            
        except Exception as e:
            logger.error(f"Error adding reserved IP range: {e}")
            return f"❌ Error adding reserved IP range: {str(e)}"
    
    @mcp_app.tool()
    async def configure_dhcp_boot_options(network_id: str, vlan_id: str,
                                         next_server: str, boot_filename: str) -> str:
        """
        🔧 Configure DHCP boot options for PXE booting.
        
        Args:
            network_id: Network ID
            vlan_id: VLAN ID
            next_server: TFTP server IP address
            boot_filename: Boot filename
            
        Returns:
            Configuration result
        """
        try:
            data = {
                "dhcpBootOptionsEnabled": True,
                "dhcpBootNextServer": next_server,
                "dhcpBootFilename": boot_filename
            }
            
            await meraki.put(f"/networks/{network_id}/appliance/vlans/{vlan_id}", data)
            
            result = f"✅ DHCP boot options configured for VLAN {vlan_id}\n\n"
            result += f"- **Boot Options**: Enabled\n"
            result += f"- **Next Server**: {next_server}\n"
            result += f"- **Boot Filename**: {boot_filename}\n"
            
            return result
            
        except Exception as e:
            logger.error(f"Error configuring DHCP boot options: {e}")
            return f"❌ Error configuring DHCP boot options: {str(e)}"
    
    @mcp_app.tool()
    async def add_custom_dhcp_option(network_id: str, vlan_id: str,
                                    code: int, type: str, value: str) -> str:
        """
        🔧 Add a custom DHCP option.
        
        Args:
            network_id: Network ID
            vlan_id: VLAN ID
            code: DHCP option code (1-254)
            type: Option type (text, ip, hex, integer)
            value: Option value
            
        Returns:
            Configuration result
        """
        try:
            # Get current VLAN config
            vlan = await meraki.get(f"/networks/{network_id}/appliance/vlans/{vlan_id}")
            
            # Get existing DHCP options or create new list
            dhcp_options = vlan.get('dhcpOptions', [])
            
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
            
            # Update VLAN
            data = {"dhcpOptions": dhcp_options}
            await meraki.put(f"/networks/{network_id}/appliance/vlans/{vlan_id}", data)
            
            result = f"✅ Custom DHCP option added for VLAN {vlan_id}\n\n"
            result += f"- **Option Code**: {code}\n"
            result += f"- **Type**: {type}\n"
            result += f"- **Value**: {value}\n"
            
            return result
            
        except Exception as e:
            logger.error(f"Error adding custom DHCP option: {e}")
            return f"❌ Error adding custom DHCP option: {str(e)}"
    
    @mcp_app.tool()
    async def enable_mandatory_dhcp(network_id: str, vlan_id: str) -> str:
        """
        🔧 Enable mandatory DHCP (clients must use DHCP-assigned IPs).
        
        Args:
            network_id: Network ID
            vlan_id: VLAN ID
            
        Returns:
            Configuration result
        """
        try:
            data = {
                "mandatoryDhcp": {
                    "enabled": True
                }
            }
            
            await meraki.put(f"/networks/{network_id}/appliance/vlans/{vlan_id}", data)
            
            result = f"✅ Mandatory DHCP enabled for VLAN {vlan_id}\n\n"
            result += "Clients connecting to this VLAN must use the IP address assigned by the DHCP server.\n"
            result += "Clients using static IP addresses will not be able to connect."
            
            return result
            
        except Exception as e:
            logger.error(f"Error enabling mandatory DHCP: {e}")
            return f"❌ Error enabling mandatory DHCP: {str(e)}"
    
    @mcp_app.tool()
    async def get_appliance_dhcp_subnets(serial: str) -> str:
        """
        🔧 Get DHCP subnet information for an appliance.
        
        Args:
            serial: Device serial number
            
        Returns:
            DHCP subnet information
        """
        try:
            subnets = await meraki.get(f"/devices/{serial}/appliance/dhcp/subnets")
            
            result = f"# DHCP Subnets for Device {serial}\n\n"
            
            if not subnets:
                result += "No DHCP subnets configured.\n"
                return result
            
            for subnet in subnets:
                result += f"## Subnet: {subnet.get('subnet', 'Unknown')}\n"
                result += f"- **VLAN ID**: {subnet.get('vlanId', 'N/A')}\n"
                result += f"- **Interface**: {subnet.get('interfaceId', 'N/A')}\n"
                result += f"- **Free Addresses**: {subnet.get('freeCount', 0)}\n"
                result += f"- **Used Addresses**: {subnet.get('usedCount', 0)}\n"
                result += f"- **Total Addresses**: {subnet.get('totalCount', 0)}\n\n"
            
            return result
            
        except Exception as e:
            logger.error(f"Error getting DHCP subnets: {e}")
            return f"❌ Error getting DHCP subnets: {str(e)}"


def register_dhcp_tool_handlers():
    """Register handlers for DHCP tools - placeholder for future extensions."""
    pass