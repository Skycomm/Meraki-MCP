"""
Cellular Gateway management tools for Cisco Meraki MCP server.

This module provides tools for managing cellular gateways, eSIMs, uplinks, and related configurations.
"""

from typing import Optional, Dict, Any, List
from datetime import datetime
import json

# Global references to be set by register function
app = None
meraki_client = None

def register_cellular_gateway_tools(mcp_app, meraki):
    """
    Register cellular gateway tools with the MCP server.
    
    Args:
        mcp_app: MCP server instance
        meraki: Meraki client instance
    """
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    
    # ==================== DEVICE LAN CONFIGURATION ====================
    
    @app.tool(
        name="get_device_cellular_gateway_lan",
        description="📱🔌 Get LAN settings for a cellular gateway device"
    )
    def get_device_cellular_gateway_lan(
        serial: str
    ):
        """Get cellular gateway LAN configuration."""
        try:
            result = meraki_client.dashboard.cellularGateway.getDeviceCellularGatewayLan(serial)
            
            response = f"# 📱 Cellular Gateway LAN Configuration\n\n"
            response += f"**Device**: {serial}\n\n"
            
            if result:
                # Reserved IP ranges
                reserved = result.get('reservedIpRanges', [])
                if reserved:
                    response += "## Reserved IP Ranges\n"
                    for range_info in reserved:
                        response += f"- {range_info.get('start')} - {range_info.get('end')}\n"
                        response += f"  Comment: {range_info.get('comment', 'N/A')}\n"
                
                # Fixed IP assignments
                fixed = result.get('fixedIpAssignments', {})
                if fixed:
                    response += "\n## Fixed IP Assignments\n"
                    for mac, ip_info in fixed.items():
                        response += f"- MAC: {mac}\n"
                        response += f"  IP: {ip_info.get('ip')}\n"
                        response += f"  Name: {ip_info.get('name', 'N/A')}\n"
            else:
                response += "*No LAN configuration found*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting LAN settings: {str(e)}"
    
    @app.tool(
        name="update_device_cellular_gateway_lan",
        description="📱✏️ Update LAN settings (reserved IPs, fixed assignments)"
    )
    def update_device_cellular_gateway_lan(
        serial: str,
        reserved_ip_start: Optional[str] = None,
        reserved_ip_end: Optional[str] = None,
        reserved_comment: Optional[str] = None,
        fixed_ip_mac: Optional[str] = None,
        fixed_ip_address: Optional[str] = None,
        fixed_ip_name: Optional[str] = None
    ):
        """
        Update cellular gateway LAN configuration.
        
        Args:
            serial: Device serial number
            reserved_ip_start: Start of reserved IP range
            reserved_ip_end: End of reserved IP range
            reserved_comment: Comment for reserved range
            fixed_ip_mac: MAC address for fixed IP assignment
            fixed_ip_address: IP address to assign
            fixed_ip_name: Name for fixed assignment
        """
        try:
            kwargs = {}
            
            # Build reserved IP ranges
            if reserved_ip_start and reserved_ip_end:
                kwargs['reservedIpRanges'] = [{
                    'start': reserved_ip_start,
                    'end': reserved_ip_end,
                    'comment': reserved_comment or 'Reserved'
                }]
            
            # Build fixed IP assignments
            if fixed_ip_mac and fixed_ip_address:
                kwargs['fixedIpAssignments'] = {
                    fixed_ip_mac: {
                        'ip': fixed_ip_address,
                        'name': fixed_ip_name or 'Fixed Device'
                    }
                }
            
            result = meraki_client.dashboard.cellularGateway.updateDeviceCellularGatewayLan(
                serial, **kwargs
            )
            
            response = f"# ✅ LAN Configuration Updated\n\n"
            response += f"**Device**: {serial}\n"
            
            if reserved_ip_start:
                response += f"**Reserved Range**: {reserved_ip_start} - {reserved_ip_end}\n"
            if fixed_ip_mac:
                response += f"**Fixed IP**: {fixed_ip_mac} → {fixed_ip_address}\n"
            
            return response
        except Exception as e:
            return f"❌ Error updating LAN settings: {str(e)}"
    
    # ==================== PORT FORWARDING ====================
    
    @app.tool(
        name="get_device_cellular_gateway_port_forwarding",
        description="📱🔀 Get port forwarding rules for cellular gateway"
    )
    def get_device_cellular_gateway_port_forwarding(
        serial: str
    ):
        """Get port forwarding rules."""
        try:
            result = meraki_client.dashboard.cellularGateway.getDeviceCellularGatewayPortForwardingRules(serial)
            
            response = f"# 🔀 Port Forwarding Rules\n\n"
            response += f"**Device**: {serial}\n\n"
            
            if result and 'rules' in result:
                rules = result['rules']
                if rules:
                    response += f"**Total Rules**: {len(rules)}\n\n"
                    for i, rule in enumerate(rules, 1):
                        response += f"## Rule {i}: {rule.get('name', 'Unnamed')}\n"
                        response += f"- LAN IP: {rule.get('lanIp')}\n"
                        response += f"- Public Port: {rule.get('publicPort')}\n"
                        response += f"- Local Port: {rule.get('localPort')}\n"
                        response += f"- Protocol: {rule.get('protocol', 'tcp')}\n"
                        response += f"- Access: {rule.get('access', 'any')}\n"
                        
                        allowed = rule.get('allowedIps', [])
                        if allowed:
                            response += f"- Allowed IPs: {', '.join(allowed)}\n"
                        response += "\n"
                else:
                    response += "*No port forwarding rules configured*\n"
            else:
                response += "*No port forwarding data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting port forwarding rules: {str(e)}"
    
    @app.tool(
        name="update_device_cellular_gateway_port_forwarding",
        description="📱🔀 Update port forwarding rules (name, lan_ip, ports, protocol: tcp/udp/both)"
    )
    def update_device_cellular_gateway_port_forwarding(
        serial: str,
        rule_name: str,
        lan_ip: str,
        public_port: str,
        local_port: str,
        protocol: Optional[str] = "tcp",
        allowed_ips: Optional[str] = None
    ):
        """
        Update port forwarding rules.
        
        Args:
            serial: Device serial number
            rule_name: Name for the rule
            lan_ip: Internal IP address
            public_port: Public port or range (e.g., "8080" or "8080-8090")
            local_port: Local port or range
            protocol: Protocol (tcp/udp/both)
            allowed_ips: Comma-separated allowed IPs (optional)
        """
        try:
            rule = {
                'name': rule_name,
                'lanIp': lan_ip,
                'publicPort': public_port,
                'localPort': local_port,
                'protocol': protocol
            }
            
            if allowed_ips:
                rule['allowedIps'] = [ip.strip() for ip in allowed_ips.split(',')]
                rule['access'] = 'restricted'
            else:
                rule['access'] = 'any'
            
            kwargs = {'rules': [rule]}
            
            result = meraki_client.dashboard.cellularGateway.updateDeviceCellularGatewayPortForwardingRules(
                serial, **kwargs
            )
            
            response = f"# ✅ Port Forwarding Updated\n\n"
            response += f"**Device**: {serial}\n"
            response += f"**Rule**: {rule_name}\n"
            response += f"**Forwarding**: {public_port} → {lan_ip}:{local_port} ({protocol})\n"
            
            return response
        except Exception as e:
            return f"❌ Error updating port forwarding: {str(e)}"
    
    # ==================== NETWORK CONFIGURATION ====================
    
    @app.tool(
        name="get_network_cellular_gateway_uplink",
        description="📱📡 Get cellular gateway uplink configuration"
    )
    def get_network_cellular_gateway_uplink(
        network_id: str
    ):
        """Get uplink configuration."""
        try:
            result = meraki_client.dashboard.cellularGateway.getNetworkCellularGatewayUplink(network_id)
            
            response = f"# 📡 Cellular Uplink Configuration\n\n"
            
            if result:
                # Bandwidth limits
                bandwidth = result.get('bandwidthLimits', {})
                if bandwidth:
                    response += "## Bandwidth Limits\n"
                    response += f"- Download: {bandwidth.get('limitDown', 'Unlimited')} Mbps\n"
                    response += f"- Upload: {bandwidth.get('limitUp', 'Unlimited')} Mbps\n\n"
            else:
                response += "*No uplink configuration found*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting uplink config: {str(e)}"
    
    @app.tool(
        name="update_network_cellular_gateway_uplink",
        description="📱📡 Update uplink bandwidth limits (Mbps)"
    )
    def update_network_cellular_gateway_uplink(
        network_id: str,
        limit_down_mbps: Optional[int] = None,
        limit_up_mbps: Optional[int] = None
    ):
        """Update uplink configuration."""
        try:
            kwargs = {}
            
            if limit_down_mbps is not None or limit_up_mbps is not None:
                kwargs['bandwidthLimits'] = {}
                if limit_down_mbps is not None:
                    kwargs['bandwidthLimits']['limitDown'] = limit_down_mbps
                if limit_up_mbps is not None:
                    kwargs['bandwidthLimits']['limitUp'] = limit_up_mbps
            
            result = meraki_client.dashboard.cellularGateway.updateNetworkCellularGatewayUplink(
                network_id, **kwargs
            )
            
            response = f"# ✅ Uplink Configuration Updated\n\n"
            if limit_down_mbps:
                response += f"**Download Limit**: {limit_down_mbps} Mbps\n"
            if limit_up_mbps:
                response += f"**Upload Limit**: {limit_up_mbps} Mbps\n"
            
            return response
        except Exception as e:
            return f"❌ Error updating uplink: {str(e)}"
    
    @app.tool(
        name="get_network_cellular_gateway_dhcp",
        description="📱🌐 Get cellular gateway DHCP settings"
    )
    def get_network_cellular_gateway_dhcp(
        network_id: str
    ):
        """Get DHCP configuration."""
        try:
            result = meraki_client.dashboard.cellularGateway.getNetworkCellularGatewayDhcp(network_id)
            
            response = f"# 🌐 Cellular Gateway DHCP Settings\n\n"
            
            if result:
                response += f"**DHCP Lease Time**: {result.get('dhcpLeaseTime', 'N/A')}\n"
                response += f"**DNS Nameservers**: {result.get('dnsNameservers', 'N/A')}\n"
                
                # Custom DNS
                custom_dns = result.get('dnsCustomNameservers', [])
                if custom_dns:
                    response += f"**Custom DNS Servers**: {', '.join(custom_dns)}\n"
            else:
                response += "*No DHCP configuration found*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting DHCP settings: {str(e)}"
    
    @app.tool(
        name="update_network_cellular_gateway_dhcp",
        description="📱🌐 Update DHCP settings (lease_time: seconds, dns_servers: comma-separated IPs)"
    )
    def update_network_cellular_gateway_dhcp(
        network_id: str,
        dhcp_lease_time: Optional[int] = None,
        dns_custom_nameservers: Optional[str] = None
    ):
        """
        Update DHCP configuration.
        
        Args:
            network_id: Network ID
            dhcp_lease_time: DHCP lease time in seconds
            dns_custom_nameservers: Comma-separated custom DNS servers
        """
        try:
            kwargs = {}
            
            if dhcp_lease_time:
                kwargs['dhcpLeaseTime'] = dhcp_lease_time
            
            if dns_custom_nameservers:
                kwargs['dnsCustomNameservers'] = [
                    dns.strip() for dns in dns_custom_nameservers.split(',')
                ]
            
            result = meraki_client.dashboard.cellularGateway.updateNetworkCellularGatewayDhcp(
                network_id, **kwargs
            )
            
            response = f"# ✅ DHCP Configuration Updated\n\n"
            if dhcp_lease_time:
                response += f"**Lease Time**: {dhcp_lease_time} seconds\n"
            if dns_custom_nameservers:
                response += f"**Custom DNS**: {dns_custom_nameservers}\n"
            
            return response
        except Exception as e:
            return f"❌ Error updating DHCP: {str(e)}"
    
    @app.tool(
        name="get_network_cellular_gateway_subnet_pool",
        description="📱🔢 Get cellular gateway subnet pool configuration"
    )
    def get_network_cellular_gateway_subnet_pool(
        network_id: str
    ):
        """Get subnet pool configuration."""
        try:
            result = meraki_client.dashboard.cellularGateway.getNetworkCellularGatewaySubnetPool(network_id)
            
            response = f"# 🔢 Subnet Pool Configuration\n\n"
            
            if result:
                response += f"**Mask**: /{result.get('mask', 'N/A')}\n"
                response += f"**CIDR**: {result.get('cidr', 'N/A')}\n"
                
                # Subnets
                subnets = result.get('subnets', [])
                if subnets:
                    response += f"\n## Configured Subnets ({len(subnets)})\n"
                    for subnet in subnets:
                        response += f"- Serial: {subnet.get('serial')}\n"
                        response += f"  Name: {subnet.get('name')}\n"
                        response += f"  App URL: {subnet.get('applianceIp')}\n"
                        response += f"  Subnet: {subnet.get('subnet')}\n\n"
            else:
                response += "*No subnet pool configured*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting subnet pool: {str(e)}"
    
    @app.tool(
        name="update_network_cellular_gateway_subnet_pool",
        description="📱🔢 Update subnet pool (mask: 24-32, cidr: e.g., 192.168.0.0/24)"
    )
    def update_network_cellular_gateway_subnet_pool(
        network_id: str,
        mask: int,
        cidr: str
    ):
        """
        Update subnet pool configuration.
        
        Args:
            network_id: Network ID
            mask: Subnet mask (24-32)
            cidr: CIDR notation (e.g., 192.168.0.0/24)
        """
        try:
            kwargs = {
                'mask': mask,
                'cidr': cidr
            }
            
            result = meraki_client.dashboard.cellularGateway.updateNetworkCellularGatewaySubnetPool(
                network_id, **kwargs
            )
            
            response = f"# ✅ Subnet Pool Updated\n\n"
            response += f"**Mask**: /{mask}\n"
            response += f"**CIDR**: {cidr}\n"
            
            return response
        except Exception as e:
            return f"❌ Error updating subnet pool: {str(e)}"
    
    @app.tool(
        name="get_network_cellular_gateway_connectivity_monitoring",
        description="📱🔍 Get connectivity monitoring destinations"
    )
    def get_network_cellular_gateway_connectivity_monitoring(
        network_id: str
    ):
        """Get connectivity monitoring destinations."""
        try:
            result = meraki_client.dashboard.cellularGateway.getNetworkCellularGatewayConnectivityMonitoringDestinations(
                network_id
            )
            
            response = f"# 🔍 Connectivity Monitoring\n\n"
            
            if result and 'destinations' in result:
                destinations = result['destinations']
                if destinations:
                    response += f"**Total Destinations**: {len(destinations)}\n\n"
                    for dest in destinations:
                        response += f"- **{dest.get('description', 'Unknown')}**\n"
                        response += f"  IP: {dest.get('ip')}\n"
                        response += f"  Default: {'✅' if dest.get('default') else '❌'}\n\n"
                else:
                    response += "*No monitoring destinations configured*\n"
            else:
                response += "*No monitoring data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting monitoring destinations: {str(e)}"
    
    @app.tool(
        name="update_network_cellular_gateway_connectivity_monitoring",
        description="📱🔍 Update connectivity monitoring (destinations: comma-separated IPs)"
    )
    def update_network_cellular_gateway_connectivity_monitoring(
        network_id: str,
        destination_ips: str,
        destination_descriptions: Optional[str] = None
    ):
        """
        Update connectivity monitoring destinations.
        
        Args:
            network_id: Network ID
            destination_ips: Comma-separated IP addresses to monitor
            destination_descriptions: Comma-separated descriptions (optional)
        """
        try:
            ips = [ip.strip() for ip in destination_ips.split(',')]
            descriptions = []
            if destination_descriptions:
                descriptions = [d.strip() for d in destination_descriptions.split(',')]
            
            destinations = []
            for i, ip in enumerate(ips):
                dest = {'ip': ip}
                if i < len(descriptions):
                    dest['description'] = descriptions[i]
                else:
                    dest['description'] = f"Monitor {ip}"
                dest['default'] = (i == 0)  # First is default
                destinations.append(dest)
            
            kwargs = {'destinations': destinations}
            
            result = meraki_client.dashboard.cellularGateway.updateNetworkCellularGatewayConnectivityMonitoringDestinations(
                network_id, **kwargs
            )
            
            response = f"# ✅ Monitoring Destinations Updated\n\n"
            response += f"**Monitoring**: {destination_ips}\n"
            
            return response
        except Exception as e:
            return f"❌ Error updating monitoring: {str(e)}"
    
    # ==================== ESIM MANAGEMENT ====================
    
    @app.tool(
        name="get_organization_cellular_gateway_esims_inventory",
        description="📱💳 Get eSIM inventory for organization"
    )
    def get_organization_cellular_gateway_esims_inventory(
        organization_id: str,
        eids: Optional[str] = None
    ):
        """
        Get eSIM inventory.
        
        Args:
            organization_id: Organization ID
            eids: Comma-separated eSIM EIDs to filter (optional)
        """
        try:
            kwargs = {}
            if eids:
                kwargs['eids'] = [eid.strip() for eid in eids.split(',')]
            
            result = meraki_client.dashboard.cellularGateway.getOrganizationCellularGatewayEsimsInventory(
                organization_id, **kwargs
            )
            
            response = f"# 💳 eSIM Inventory\n\n"
            
            if result and isinstance(result, list):
                response += f"**Total eSIMs**: {len(result)}\n\n"
                
                for esim in result[:10]:  # Show first 10
                    response += f"## eSIM: {esim.get('eid', 'Unknown')[:8]}...\n"
                    response += f"- Status: {esim.get('status', 'N/A')}\n"
                    response += f"- Device: {esim.get('device', {}).get('name', 'Unassigned')}\n"
                    response += f"- Serial: {esim.get('device', {}).get('serial', 'N/A')}\n"
                    response += f"- Carrier: {esim.get('carrier', 'N/A')}\n\n"
                
                if len(result) > 10:
                    response += f"*...and {len(result)-10} more eSIMs*\n"
            else:
                response += "*No eSIMs found*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting eSIM inventory: {str(e)}"
    
    @app.tool(
        name="update_organization_cellular_gateway_esims_inventory",
        description="📱💳 Update eSIM inventory status"
    )
    def update_organization_cellular_gateway_esims_inventory(
        organization_id: str,
        eid: str,
        status: Optional[str] = None
    ):
        """
        Update eSIM inventory.
        
        Args:
            organization_id: Organization ID
            eid: eSIM EID
            status: New status for the eSIM
        """
        try:
            kwargs = {}
            if status:
                kwargs['status'] = status
            
            result = meraki_client.dashboard.cellularGateway.updateOrganizationCellularGatewayEsimsInventory(
                organization_id, eid=eid, **kwargs
            )
            
            response = f"# ✅ eSIM Updated\n\n"
            response += f"**EID**: {eid[:12]}...\n"
            if status:
                response += f"**Status**: {status}\n"
            
            return response
        except Exception as e:
            return f"❌ Error updating eSIM: {str(e)}"
    
    @app.tool(
        name="get_organization_cellular_gateway_esims_providers",
        description="📱📡 Get available eSIM service providers"
    )
    def get_organization_cellular_gateway_esims_providers(
        organization_id: str
    ):
        """Get eSIM service providers."""
        try:
            result = meraki_client.dashboard.cellularGateway.getOrganizationCellularGatewayEsimsServiceProviders(
                organization_id
            )
            
            response = f"# 📡 eSIM Service Providers\n\n"
            
            if result and isinstance(result, list):
                response += f"**Available Providers**: {len(result)}\n\n"
                
                for provider in result:
                    response += f"## {provider.get('name', 'Unknown')}\n"
                    response += f"- Provider ID: {provider.get('providerId')}\n"
                    response += f"- Logo: {provider.get('logo', 'N/A')}\n\n"
            else:
                response += "*No service providers available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting providers: {str(e)}"
    
    @app.tool(
        name="get_organization_cellular_gateway_esims_accounts",
        description="📱💼 Get eSIM service provider accounts"
    )
    def get_organization_cellular_gateway_esims_accounts(
        organization_id: str,
        account_ids: Optional[str] = None
    ):
        """
        Get eSIM service provider accounts.
        
        Args:
            organization_id: Organization ID
            account_ids: Comma-separated account IDs to filter (optional)
        """
        try:
            kwargs = {}
            if account_ids:
                kwargs['accountIds'] = [aid.strip() for aid in account_ids.split(',')]
            
            result = meraki_client.dashboard.cellularGateway.getOrganizationCellularGatewayEsimsServiceProvidersAccounts(
                organization_id, **kwargs
            )
            
            response = f"# 💼 Service Provider Accounts\n\n"
            
            if result and isinstance(result, list):
                response += f"**Total Accounts**: {len(result)}\n\n"
                
                for account in result:
                    response += f"## {account.get('accountName', 'Unknown')}\n"
                    response += f"- Account ID: {account.get('accountId')}\n"
                    response += f"- Provider: {account.get('serviceProvider', {}).get('name')}\n"
                    response += f"- Status: {account.get('status')}\n"
                    response += f"- Added: {account.get('addedOn')}\n\n"
            else:
                response += "*No accounts configured*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting accounts: {str(e)}"
    
    @app.tool(
        name="create_organization_cellular_gateway_esims_account",
        description="📱➕ Add new eSIM service provider account"
    )
    def create_organization_cellular_gateway_esims_account(
        organization_id: str,
        account_name: str,
        provider_id: str,
        username: str,
        api_key: Optional[str] = None
    ):
        """
        Create eSIM service provider account.
        
        Args:
            organization_id: Organization ID
            account_name: Name for the account
            provider_id: Service provider ID
            username: Account username
            api_key: API key for the account (if required)
        """
        try:
            kwargs = {
                'accountName': account_name,
                'providerId': provider_id,
                'username': username
            }
            
            if api_key:
                kwargs['apiKey'] = api_key
            
            result = meraki_client.dashboard.cellularGateway.createOrganizationCellularGatewayEsimsServiceProvidersAccount(
                organization_id, **kwargs
            )
            
            response = f"# ✅ Service Provider Account Created\n\n"
            response += f"**Account**: {account_name}\n"
            response += f"**Provider ID**: {provider_id}\n"
            response += f"**Username**: {username}\n"
            
            return response
        except Exception as e:
            return f"❌ Error creating account: {str(e)}"
    
    @app.tool(
        name="update_organization_cellular_gateway_esims_account",
        description="📱✏️ Update eSIM service provider account"
    )
    def update_organization_cellular_gateway_esims_account(
        organization_id: str,
        account_id: str,
        account_name: Optional[str] = None,
        is_password_updated: Optional[bool] = None
    ):
        """Update eSIM service provider account."""
        try:
            kwargs = {}
            if account_name:
                kwargs['accountName'] = account_name
            if is_password_updated is not None:
                kwargs['isPasswordUpdated'] = is_password_updated
            
            result = meraki_client.dashboard.cellularGateway.updateOrganizationCellularGatewayEsimsServiceProvidersAccount(
                organization_id, account_id, **kwargs
            )
            
            response = f"# ✅ Account Updated\n\n"
            response += f"**Account ID**: {account_id}\n"
            if account_name:
                response += f"**New Name**: {account_name}\n"
            
            return response
        except Exception as e:
            return f"❌ Error updating account: {str(e)}"
    
    @app.tool(
        name="delete_organization_cellular_gateway_esims_account",
        description="📱❌ Delete eSIM service provider account"
    )
    def delete_organization_cellular_gateway_esims_account(
        organization_id: str,
        account_id: str
    ):
        """Delete eSIM service provider account."""
        try:
            meraki_client.dashboard.cellularGateway.deleteOrganizationCellularGatewayEsimsServiceProvidersAccount(
                organization_id, account_id
            )
            
            response = f"# ✅ Account Deleted\n\n"
            response += f"**Account ID**: {account_id}\n"
            
            return response
        except Exception as e:
            return f"❌ Error deleting account: {str(e)}"
    
    @app.tool(
        name="get_organization_cellular_gateway_esims_rate_plans",
        description="📱📊 Get available eSIM rate plans"
    )
    def get_organization_cellular_gateway_esims_rate_plans(
        organization_id: str,
        account_id: str
    ):
        """Get eSIM rate plans for an account."""
        try:
            result = meraki_client.dashboard.cellularGateway.getOrganizationCellularGatewayEsimsServiceProvidersAccountsRatePlans(
                organization_id, account_id
            )
            
            response = f"# 📊 Available Rate Plans\n\n"
            response += f"**Account ID**: {account_id}\n\n"
            
            if result and isinstance(result, list):
                response += f"**Total Plans**: {len(result)}\n\n"
                
                for plan in result:
                    response += f"## {plan.get('name', 'Unknown')}\n"
                    response += f"- Plan ID: {plan.get('ratePlanId')}\n"
                    response += f"- Data Limit: {plan.get('dataLimit', 'N/A')}\n"
                    response += f"- Price: {plan.get('price', 'N/A')}\n\n"
            else:
                response += "*No rate plans available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting rate plans: {str(e)}"
    
    @app.tool(
        name="get_organization_cellular_gateway_esims_comm_plans",
        description="📱📞 Get eSIM communication plans"
    )
    def get_organization_cellular_gateway_esims_comm_plans(
        organization_id: str,
        account_id: str
    ):
        """Get eSIM communication plans."""
        try:
            result = meraki_client.dashboard.cellularGateway.getOrganizationCellularGatewayEsimsServiceProvidersAccountsCommunicationPlans(
                organization_id, account_id
            )
            
            response = f"# 📞 Communication Plans\n\n"
            response += f"**Account ID**: {account_id}\n\n"
            
            if result and isinstance(result, list):
                response += f"**Total Plans**: {len(result)}\n\n"
                
                for plan in result:
                    response += f"## {plan.get('name', 'Unknown')}\n"
                    response += f"- Plan ID: {plan.get('communicationPlanId')}\n"
                    response += f"- APNs: {plan.get('apns', 'N/A')}\n\n"
            else:
                response += "*No communication plans available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting communication plans: {str(e)}"
    
    @app.tool(
        name="create_organization_cellular_gateway_esims_swap",
        description="📱🔄 Initiate eSIM swap between devices"
    )
    def create_organization_cellular_gateway_esims_swap(
        organization_id: str,
        swap_id: str,
        old_esims: str,
        new_esims: str
    ):
        """
        Create eSIM swap operation.
        
        Args:
            organization_id: Organization ID
            swap_id: Unique swap ID
            old_esims: Comma-separated old eSIM EIDs
            new_esims: Comma-separated new eSIM EIDs
        """
        try:
            old_list = [{'eid': eid.strip()} for eid in old_esims.split(',')]
            new_list = [{'eid': eid.strip()} for eid in new_esims.split(',')]
            
            swaps = [{
                'swapId': swap_id,
                'oldEsims': old_list,
                'newEsims': new_list
            }]
            
            result = meraki_client.dashboard.cellularGateway.createOrganizationCellularGatewayEsimsSwap(
                organization_id, swaps=swaps
            )
            
            response = f"# ✅ eSIM Swap Initiated\n\n"
            response += f"**Swap ID**: {swap_id}\n"
            response += f"**Old eSIMs**: {old_esims}\n"
            response += f"**New eSIMs**: {new_esims}\n"
            
            return response
        except Exception as e:
            return f"❌ Error creating swap: {str(e)}"
    
    @app.tool(
        name="update_organization_cellular_gateway_esims_swap",
        description="📱🔄 Update eSIM swap status"
    )
    def update_organization_cellular_gateway_esims_swap(
        organization_id: str,
        swap_id: str,
        status: str
    ):
        """
        Update eSIM swap operation.
        
        Args:
            organization_id: Organization ID
            swap_id: Swap ID to update
            status: New status (e.g., 'confirmed', 'cancelled')
        """
        try:
            result = meraki_client.dashboard.cellularGateway.updateOrganizationCellularGatewayEsimsSwap(
                organization_id, swap_id, status=status
            )
            
            response = f"# ✅ eSIM Swap Updated\n\n"
            response += f"**Swap ID**: {swap_id}\n"
            response += f"**Status**: {status}\n"
            
            return response
        except Exception as e:
            return f"❌ Error updating swap: {str(e)}"
    
    @app.tool(
        name="get_organization_cellular_gateway_uplink_statuses",
        description="📱📊 Get uplink statuses for all cellular gateways"
    )
    def get_organization_cellular_gateway_uplink_statuses(
        organization_id: str,
        per_page: Optional[int] = 10,
        network_ids: Optional[str] = None,
        serials: Optional[str] = None,
        iccids: Optional[str] = None
    ):
        """
        Get uplink statuses for cellular gateways.
        
        Args:
            organization_id: Organization ID
            per_page: Results per page
            network_ids: Comma-separated network IDs to filter
            serials: Comma-separated device serials to filter
            iccids: Comma-separated ICCIDs to filter
        """
        try:
            kwargs = {}
            if per_page:
                kwargs['perPage'] = per_page
            if network_ids:
                kwargs['networkIds'] = [n.strip() for n in network_ids.split(',')]
            if serials:
                kwargs['serials'] = [s.strip() for s in serials.split(',')]
            if iccids:
                kwargs['iccids'] = [i.strip() for i in iccids.split(',')]
            
            result = meraki_client.dashboard.cellularGateway.getOrganizationCellularGatewayUplinkStatuses(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Cellular Gateway Uplink Statuses\n\n"
            
            if result and 'items' in result:
                items = result['items']
                response += f"**Total Devices**: {len(items)}\n\n"
                
                for item in items[:5]:  # Show first 5
                    uplinks = item.get('uplinks', [])
                    response += f"## Device: {item.get('serial', 'Unknown')}\n"
                    response += f"**Network**: {item.get('networkId')}\n"
                    response += f"**Last Reported**: {item.get('lastReportedAt')}\n"
                    
                    for uplink in uplinks:
                        response += f"\n### Uplink: {uplink.get('interface', 'Unknown')}\n"
                        response += f"- Status: {uplink.get('status', 'unknown')}\n"
                        response += f"- IP: {uplink.get('ip', 'N/A')}\n"
                        response += f"- Provider: {uplink.get('provider', 'N/A')}\n"
                        response += f"- Signal: {uplink.get('signalStat', {}).get('rsrp', 'N/A')} dBm\n"
                        response += f"- Connection: {uplink.get('connectionType', 'N/A')}\n"
                        response += f"- APN: {uplink.get('apn', 'N/A')}\n"
                        response += f"- ICCID: {uplink.get('iccid', 'N/A')[:10]}...\n"
                    
                    response += "\n"
                
                if len(items) > 5:
                    response += f"*...and {len(items)-5} more devices*\n"
            else:
                response += "*No uplink status data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting uplink statuses: {str(e)}"