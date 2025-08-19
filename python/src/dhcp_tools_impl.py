"""
DHCP tools implementation for SSE version.
Full DHCP functionality for Meraki networks.
"""

# Global meraki_client will be set by the server
meraki_client = None

async def get_vlan_dhcp_settings(network_id: str, vlan_id: str) -> str:
    """🔧 Get DHCP settings for a specific VLAN."""
    if not meraki_client:
        return "Error: Meraki client not initialized"
    
    try:
        vlan = await meraki_client.get(f"/networks/{network_id}/appliance/vlans/{vlan_id}")
        
        result = f"# DHCP Settings for VLAN {vlan_id}\n\n"
        result += f"**Network**: {network_id}\n"
        result += f"**VLAN**: {vlan.get('name', 'Unknown')} (ID: {vlan_id})\n\n"
        
        dhcp_handling = vlan.get('dhcpHandling', 'Not configured')
        result += f"## DHCP Mode\n"
        result += f"- **Handling**: {dhcp_handling}\n"
        
        if dhcp_handling == 'Run a DHCP server':
            result += f"\n## DHCP Server Configuration\n"
            result += f"- **Lease Time**: {vlan.get('dhcpLeaseTime', 'Default')}\n"
            result += f"- **DNS Nameservers**: {vlan.get('dnsNameservers', 'Default')}\n"
            
            if vlan.get('dhcpBootOptionsEnabled'):
                result += f"\n### Boot Options\n"
                result += f"- **Enabled**: ✅\n"
                result += f"- **Next Server**: {vlan.get('dhcpBootNextServer', 'Not set')}\n"
                result += f"- **Boot Filename**: {vlan.get('dhcpBootFilename', 'Not set')}\n"
            
            reserved_ranges = vlan.get('reservedIpRanges', [])
            if reserved_ranges:
                result += f"\n### Reserved IP Ranges\n"
                for range_item in reserved_ranges:
                    result += f"- **{range_item['start']} - {range_item['end']}**"
                    if range_item.get('comment'):
                        result += f" ({range_item['comment']})"
                    result += "\n"
            
            fixed_ips = vlan.get('fixedIpAssignments', {})
            if fixed_ips:
                result += f"\n### Fixed IP Assignments\n"
                for mac, assignment in fixed_ips.items():
                    result += f"- **{mac}**: {assignment['ip']}"
                    if assignment.get('name'):
                        result += f" ({assignment['name']})"
                    result += "\n"
            
            dhcp_options = vlan.get('dhcpOptions', [])
            if dhcp_options:
                result += f"\n### Custom DHCP Options\n"
                for option in dhcp_options:
                    result += f"- **Option {option['code']}**: {option['value']} (Type: {option['type']})\n"
            
            if vlan.get('mandatoryDhcp', {}).get('enabled'):
                result += f"\n### Mandatory DHCP\n"
                result += f"- **Enabled**: ✅ (Clients must use DHCP)\n"
                
        elif dhcp_handling == 'Relay DHCP to another server':
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
        return f"❌ Error getting DHCP settings: {str(e)}"

async def update_vlan_dhcp_server(network_id: str, vlan_id: str, 
                                 lease_time: str = "1 day",
                                 dns_nameservers: str = "upstream_dns") -> str:
    """🔧 Configure VLAN to run DHCP server with basic settings."""
    if not meraki_client:
        return "Error: Meraki client not initialized"
    
    try:
        data = {
            "dhcpHandling": "Run a DHCP server",
            "dhcpLeaseTime": lease_time,
            "dnsNameservers": dns_nameservers
        }
        
        await meraki_client.put(f"/networks/{network_id}/appliance/vlans/{vlan_id}", data)
        
        result = f"✅ DHCP Server configured for VLAN {vlan_id}\n\n"
        result += f"- **Mode**: Run a DHCP server\n"
        result += f"- **Lease Time**: {lease_time}\n"
        result += f"- **DNS Servers**: {dns_nameservers}\n"
        
        return result
        
    except Exception as e:
        return f"❌ Error configuring DHCP server: {str(e)}"

async def configure_dhcp_relay(network_id: str, vlan_id: str, 
                              relay_server_ips: str) -> str:
    """🔧 Configure VLAN to relay DHCP to another server."""
    if not meraki_client:
        return "Error: Meraki client not initialized"
    
    try:
        servers = [ip.strip() for ip in relay_server_ips.split(",")]
        
        data = {
            "dhcpHandling": "Relay DHCP to another server",
            "dhcpRelayServerIps": servers
        }
        
        await meraki_client.put(f"/networks/{network_id}/appliance/vlans/{vlan_id}", data)
        
        result = f"✅ DHCP Relay configured for VLAN {vlan_id}\n\n"
        result += f"- **Mode**: Relay DHCP to another server\n"
        result += f"- **Relay Servers**:\n"
        for server in servers:
            result += f"  - {server}\n"
        
        return result
        
    except Exception as e:
        return f"❌ Error configuring DHCP relay: {str(e)}"

async def disable_vlan_dhcp(network_id: str, vlan_id: str) -> str:
    """🔧 Disable DHCP on a VLAN."""
    if not meraki_client:
        return "Error: Meraki client not initialized"
    
    try:
        data = {
            "dhcpHandling": "Do not respond to DHCP requests"
        }
        
        await meraki_client.put(f"/networks/{network_id}/appliance/vlans/{vlan_id}", data)
        
        return f"✅ DHCP disabled for VLAN {vlan_id}\n\nThe VLAN will not respond to DHCP requests."
        
    except Exception as e:
        return f"❌ Error disabling DHCP: {str(e)}"

async def add_dhcp_fixed_assignment(network_id: str, vlan_id: str,
                                   mac_address: str, ip_address: str,
                                   name: str = None) -> str:
    """🔧 Add a fixed IP assignment (DHCP reservation) for a MAC address."""
    if not meraki_client:
        return "Error: Meraki client not initialized"
    
    try:
        vlan = await meraki_client.get(f"/networks/{network_id}/appliance/vlans/{vlan_id}")
        
        fixed_assignments = vlan.get('fixedIpAssignments', {})
        
        assignment = {"ip": ip_address}
        if name:
            assignment["name"] = name
        
        fixed_assignments[mac_address] = assignment
        
        data = {"fixedIpAssignments": fixed_assignments}
        await meraki_client.put(f"/networks/{network_id}/appliance/vlans/{vlan_id}", data)
        
        result = f"✅ Fixed IP assignment added for VLAN {vlan_id}\n\n"
        result += f"- **MAC Address**: {mac_address}\n"
        result += f"- **IP Address**: {ip_address}\n"
        if name:
            result += f"- **Name**: {name}\n"
        
        return result
        
    except Exception as e:
        return f"❌ Error adding fixed IP assignment: {str(e)}"

async def remove_dhcp_fixed_assignment(network_id: str, vlan_id: str,
                                      mac_address: str) -> str:
    """🔧 Remove a fixed IP assignment (DHCP reservation)."""
    if not meraki_client:
        return "Error: Meraki client not initialized"
    
    try:
        vlan = await meraki_client.get(f"/networks/{network_id}/appliance/vlans/{vlan_id}")
        
        fixed_assignments = vlan.get('fixedIpAssignments', {})
        
        if mac_address not in fixed_assignments:
            return f"⚠️ MAC address {mac_address} not found in fixed assignments"
        
        del fixed_assignments[mac_address]
        
        data = {"fixedIpAssignments": fixed_assignments}
        await meraki_client.put(f"/networks/{network_id}/appliance/vlans/{vlan_id}", data)
        
        return f"✅ Fixed IP assignment removed for MAC {mac_address}"
        
    except Exception as e:
        return f"❌ Error removing fixed IP assignment: {str(e)}"

async def add_dhcp_reserved_range(network_id: str, vlan_id: str,
                                 start_ip: str, end_ip: str,
                                 comment: str = None) -> str:
    """🔧 Add a reserved IP range to exclude from DHCP pool."""
    if not meraki_client:
        return "Error: Meraki client not initialized"
    
    try:
        vlan = await meraki_client.get(f"/networks/{network_id}/appliance/vlans/{vlan_id}")
        
        reserved_ranges = vlan.get('reservedIpRanges', [])
        
        new_range = {
            "start": start_ip,
            "end": end_ip
        }
        if comment:
            new_range["comment"] = comment
        
        reserved_ranges.append(new_range)
        
        data = {"reservedIpRanges": reserved_ranges}
        await meraki_client.put(f"/networks/{network_id}/appliance/vlans/{vlan_id}", data)
        
        result = f"✅ Reserved IP range added for VLAN {vlan_id}\n\n"
        result += f"- **Range**: {start_ip} - {end_ip}\n"
        if comment:
            result += f"- **Comment**: {comment}\n"
        
        return result
        
    except Exception as e:
        return f"❌ Error adding reserved IP range: {str(e)}"

async def configure_dhcp_boot_options(network_id: str, vlan_id: str,
                                     next_server: str, boot_filename: str) -> str:
    """🔧 Configure DHCP boot options for PXE booting."""
    if not meraki_client:
        return "Error: Meraki client not initialized"
    
    try:
        data = {
            "dhcpBootOptionsEnabled": True,
            "dhcpBootNextServer": next_server,
            "dhcpBootFilename": boot_filename
        }
        
        await meraki_client.put(f"/networks/{network_id}/appliance/vlans/{vlan_id}", data)
        
        result = f"✅ DHCP boot options configured for VLAN {vlan_id}\n\n"
        result += f"- **Boot Options**: Enabled\n"
        result += f"- **Next Server**: {next_server}\n"
        result += f"- **Boot Filename**: {boot_filename}\n"
        
        return result
        
    except Exception as e:
        return f"❌ Error configuring DHCP boot options: {str(e)}"

async def add_custom_dhcp_option(network_id: str, vlan_id: str,
                                code: int, type: str, value: str) -> str:
    """🔧 Add a custom DHCP option."""
    if not meraki_client:
        return "Error: Meraki client not initialized"
    
    try:
        vlan = await meraki_client.get(f"/networks/{network_id}/appliance/vlans/{vlan_id}")
        
        dhcp_options = vlan.get('dhcpOptions', [])
        
        existing_option = next((opt for opt in dhcp_options if opt['code'] == str(code)), None)
        if existing_option:
            return f"⚠️ DHCP option {code} already exists. Remove it first to update."
        
        new_option = {
            "code": str(code),
            "type": type,
            "value": value
        }
        dhcp_options.append(new_option)
        
        data = {"dhcpOptions": dhcp_options}
        await meraki_client.put(f"/networks/{network_id}/appliance/vlans/{vlan_id}", data)
        
        result = f"✅ Custom DHCP option added for VLAN {vlan_id}\n\n"
        result += f"- **Option Code**: {code}\n"
        result += f"- **Type**: {type}\n"
        result += f"- **Value**: {value}\n"
        
        return result
        
    except Exception as e:
        return f"❌ Error adding custom DHCP option: {str(e)}"

async def enable_mandatory_dhcp(network_id: str, vlan_id: str) -> str:
    """🔧 Enable mandatory DHCP (clients must use DHCP-assigned IPs)."""
    if not meraki_client:
        return "Error: Meraki client not initialized"
    
    try:
        data = {
            "mandatoryDhcp": {
                "enabled": True
            }
        }
        
        await meraki_client.put(f"/networks/{network_id}/appliance/vlans/{vlan_id}", data)
        
        result = f"✅ Mandatory DHCP enabled for VLAN {vlan_id}\n\n"
        result += "Clients connecting to this VLAN must use the IP address assigned by the DHCP server.\n"
        result += "Clients using static IP addresses will not be able to connect."
        
        return result
        
    except Exception as e:
        return f"❌ Error enabling mandatory DHCP: {str(e)}"

async def get_appliance_dhcp_subnets(serial: str) -> str:
    """🔧 Get DHCP subnet information for an appliance."""
    if not meraki_client:
        return "Error: Meraki client not initialized"
    
    try:
        subnets = await meraki_client.get(f"/devices/{serial}/appliance/dhcp/subnets")
        
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
        return f"❌ Error getting DHCP subnets: {str(e)}"