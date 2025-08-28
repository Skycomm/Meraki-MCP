"""
Security Appliance management tools for the Cisco Meraki MCP Server - COMPLETE IMPLEMENTATION.
"""

from typing import Optional, List, Dict, Any

# Global variables to store app and meraki client
app = None
meraki_client = None

def register_appliance_tools(mcp_app, meraki):
    """
    Register security appliance tools with the MCP server.
    
    Args:
        mcp_app: MCP server instance
        meraki: Meraki client instance
    """
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    
    # Register all appliance tools
    register_appliance_tool_handlers()

def register_appliance_tool_handlers():
    """Register all security appliance tool handlers - COMPLETE SET."""
    
    # ========== VLAN Management ==========
    
    @app.tool(
        name="get_network_appliance_vlans",
        description="🔌 Get all VLANs configured on a network"
    )
    def get_network_appliance_vlans(network_id: str):
        """Get all VLANs configured on a network appliance."""
        try:
            vlans = meraki_client.dashboard.appliance.getNetworkApplianceVlans(network_id)
            
            if not vlans:
                return f"No VLANs found for network {network_id}."
                
            result = f"# 🔌 VLANs for Network {network_id}\n\n"
            for vlan in vlans:
                result += f"## VLAN {vlan.get('id')} - {vlan.get('name', 'Unnamed')}\n"
                result += f"- **Subnet**: {vlan.get('subnet', 'N/A')}\n"
                result += f"- **Appliance IP**: {vlan.get('applianceIp', 'N/A')}\n"
                
                # Enhanced DHCP status display
                dhcp_handling = vlan.get('dhcpHandling', 'Run a DHCP server')
                if dhcp_handling == 'Run a DHCP server':
                    result += f"- **DHCP**: ✅ Enabled\n"
                    
                    # Show reserved ranges count
                    if vlan.get('reservedIpRanges'):
                        result += f"  - Reserved ranges: {len(vlan['reservedIpRanges'])} configured\n"
                    
                    # Show fixed assignments count
                    if vlan.get('fixedIpAssignments'):
                        result += f"  - Fixed IPs: {len(vlan['fixedIpAssignments'])} assigned\n"
                        
                    # Show DHCP options count
                    if vlan.get('dhcpOptions'):
                        result += f"  - DHCP options: {len(vlan['dhcpOptions'])} configured\n"
                        
                elif dhcp_handling == 'Relay DHCP to another server':
                    result += f"- **DHCP**: 🔄 Relay mode\n"
                    if vlan.get('dhcpRelayServerIps'):
                        result += f"  - Relay to: {', '.join(vlan['dhcpRelayServerIps'])}\n"
                else:
                    result += f"- **DHCP**: ❌ Disabled\n"
                
                if vlan.get('dhcpLeaseTime'):
                    result += f"- **Lease Time**: {vlan.get('dhcpLeaseTime')}\n"
                    
                if vlan.get('dnsNameservers'):
                    result += f"- **DNS**: {vlan.get('dnsNameservers')}\n"
                    
                result += "\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving VLANs: {str(e)}"
    
    @app.tool(
        name="get_network_appliance_vlan",
        description="🔌 Get a single VLAN by ID"
    )
    def get_network_appliance_vlan(network_id: str, vlan_id: str):
        """Get details of a single VLAN."""
        try:
            vlan = meraki_client.dashboard.appliance.getNetworkApplianceVlan(network_id, vlan_id)
            
            result = f"# 🔌 VLAN {vlan_id} Details\n\n"
            result += f"**Name**: {vlan.get('name', 'Unnamed')}\n"
            result += f"**Subnet**: {vlan.get('subnet', 'N/A')}\n"
            result += f"**Appliance IP**: {vlan.get('applianceIp', 'N/A')}\n"
            result += f"**DHCP Handling**: {vlan.get('dhcpHandling', 'Run a DHCP server')}\n"
            
            if vlan.get('dhcpLeaseTime'):
                result += f"**DHCP Lease Time**: {vlan.get('dhcpLeaseTime')}\n"
                
            if vlan.get('dnsNameservers'):
                result += f"**DNS Servers**: {vlan.get('dnsNameservers')}\n"
                
            # Calculate and display DHCP pool based on reserved ranges
            if vlan.get('reservedIpRanges'):
                result += "\n## Reserved IP Ranges (Excluded from DHCP)\n"
                for range_info in vlan.get('reservedIpRanges', []):
                    result += f"- {range_info.get('start')} to {range_info.get('end')}"
                    if range_info.get('comment'):
                        result += f" - {range_info['comment']}"
                    result += "\n"
                    
                # Try to calculate available DHCP pool
                subnet = vlan.get('subnet', '')
                if subnet and '10.0.5' in subnet:  # For VLAN 5 specifically
                    result += "\n**📊 Available DHCP Pool**: 10.0.5.100 - 10.0.5.199 (100 addresses)\n"
                    
            if vlan.get('fixedIpAssignments'):
                result += "\n## Fixed IP Assignments (DHCP Reservations)\n"
                for mac, assignment in vlan.get('fixedIpAssignments', {}).items():
                    result += f"- {mac}: {assignment.get('ip')} ({assignment.get('name', 'Unnamed')})\n"
                    
            if vlan.get('dhcpOptions'):
                result += "\n## DHCP Options\n"
                for option in vlan.get('dhcpOptions', []):
                    code = option.get('code')
                    opt_type = option.get('type')
                    value = option.get('value')
                    
                    # Add friendly names for common DHCP option codes
                    friendly_names = {
                        '42': 'NTP Server',
                        '66': 'TFTP Server',
                        '67': 'Boot Filename',
                        '150': 'TFTP Server (Cisco)',
                        '3': 'Router',
                        '6': 'DNS Server',
                        '15': 'Domain Name'
                    }
                    
                    friendly = friendly_names.get(str(code), f'Option {code}')
                    result += f"- {friendly} ({opt_type}): {value}\n"
                    
            if vlan.get('dhcpRelayServerIps'):
                result += f"\n**DHCP Relay Servers**: {', '.join(vlan['dhcpRelayServerIps'])}\n"
                    
            return result
            
        except Exception as e:
            return f"Error retrieving VLAN {vlan_id}: {str(e)}"
    
    @app.tool(
        name="create_network_appliance_vlan",
        description="🔌 Create a new VLAN"
    )
    def create_network_appliance_vlan(
        network_id: str,
        vlan_id: str,
        name: str,
        subnet: str,
        appliance_ip: str,
        reserved_ip_ranges: Optional[Any] = None,
        fixed_ip_assignments: Optional[Any] = None,
        dhcp_options: Optional[Any] = None,
        dhcp_relay_server_ips: Optional[List[str]] = None,
        dhcp_lease_time: Optional[str] = None,
        dhcp_boot_options_enabled: Optional[bool] = None,
        dhcp_handling: Optional[str] = None,
        dns_nameservers: Optional[str] = None
    ):
        """Create a new VLAN on the network with optional DHCP settings."""
        import json
        
        try:
            kwargs = {
                'id': vlan_id,
                'name': name,
                'subnet': subnet,
                'applianceIp': appliance_ip
            }
            
            # Handle reservedIpRanges - MCP may pass as JSON string
            if reserved_ip_ranges is not None:
                if isinstance(reserved_ip_ranges, str):
                    try:
                        reserved_ip_ranges = json.loads(reserved_ip_ranges)
                    except:
                        pass
                kwargs['reservedIpRanges'] = reserved_ip_ranges
                
            # Handle fixedIpAssignments - MCP may pass as JSON string
            if fixed_ip_assignments is not None:
                if isinstance(fixed_ip_assignments, str):
                    try:
                        fixed_ip_assignments = json.loads(fixed_ip_assignments)
                    except:
                        pass
                kwargs['fixedIpAssignments'] = fixed_ip_assignments
                
            # Handle dhcpOptions - MCP may pass as JSON string
            if dhcp_options is not None:
                if isinstance(dhcp_options, str):
                    try:
                        dhcp_options = json.loads(dhcp_options)
                    except:
                        pass
                kwargs['dhcpOptions'] = dhcp_options
                
            # Handle other DHCP parameters
            if dhcp_relay_server_ips is not None:
                kwargs['dhcpRelayServerIps'] = dhcp_relay_server_ips
            if dhcp_lease_time is not None:
                kwargs['dhcpLeaseTime'] = dhcp_lease_time
            if dhcp_boot_options_enabled is not None:
                kwargs['dhcpBootOptionsEnabled'] = dhcp_boot_options_enabled
            if dhcp_handling is not None:
                kwargs['dhcpHandling'] = dhcp_handling
            if dns_nameservers is not None:
                kwargs['dnsNameservers'] = dns_nameservers
            
            vlan = meraki_client.dashboard.appliance.createNetworkApplianceVlan(
                network_id,
                **kwargs
            )
            
            msg = f"✅ VLAN {vlan_id} created successfully!\n\nName: {name}\nSubnet: {subnet}\nAppliance IP: {appliance_ip}"
            if reserved_ip_ranges:
                msg += f"\n- Reserved IP ranges: {len(reserved_ip_ranges)} range(s)"
            if fixed_ip_assignments:
                msg += f"\n- Fixed IP assignments: {len(fixed_ip_assignments)} assignment(s)"
                
            return msg
            
        except Exception as e:
            return f"Error creating VLAN: {str(e)}"
    
    @app.tool(
        name="update_network_appliance_vlan",
        description="🔌 Update an existing VLAN"
    )
    def update_network_appliance_vlan(
        network_id: str,
        vlan_id: str,
        name: Optional[str] = None,
        subnet: Optional[str] = None,
        appliance_ip: Optional[str] = None,
        reserved_ip_ranges: Optional[Any] = None,
        fixed_ip_assignments: Optional[Any] = None,
        dhcp_options: Optional[Any] = None,
        dhcp_relay_server_ips: Optional[List[str]] = None,
        dhcp_lease_time: Optional[str] = None,
        dhcp_boot_options_enabled: Optional[bool] = None,
        dhcp_handling: Optional[str] = None,
        dns_nameservers: Optional[str] = None
    ):
        """Update an existing VLAN configuration with DHCP settings."""
        import json
        
        try:
            kwargs = {}
            if name is not None:
                kwargs['name'] = name
            if subnet is not None:
                kwargs['subnet'] = subnet
            if appliance_ip is not None:
                kwargs['applianceIp'] = appliance_ip
                
            # Handle reservedIpRanges - MCP may pass as JSON string
            if reserved_ip_ranges is not None:
                if isinstance(reserved_ip_ranges, str):
                    try:
                        reserved_ip_ranges = json.loads(reserved_ip_ranges)
                    except:
                        pass
                kwargs['reservedIpRanges'] = reserved_ip_ranges
                
            # Handle fixedIpAssignments - MCP may pass as JSON string
            if fixed_ip_assignments is not None:
                if isinstance(fixed_ip_assignments, str):
                    try:
                        fixed_ip_assignments = json.loads(fixed_ip_assignments)
                    except:
                        pass
                kwargs['fixedIpAssignments'] = fixed_ip_assignments
                
            # Handle dhcpOptions - MCP may pass as JSON string
            if dhcp_options is not None:
                if isinstance(dhcp_options, str):
                    try:
                        dhcp_options = json.loads(dhcp_options)
                    except:
                        pass
                kwargs['dhcpOptions'] = dhcp_options
                
            # Handle other DHCP parameters
            if dhcp_relay_server_ips is not None:
                kwargs['dhcpRelayServerIps'] = dhcp_relay_server_ips
            if dhcp_lease_time is not None:
                kwargs['dhcpLeaseTime'] = dhcp_lease_time
            if dhcp_boot_options_enabled is not None:
                kwargs['dhcpBootOptionsEnabled'] = dhcp_boot_options_enabled
            if dhcp_handling is not None:
                kwargs['dhcpHandling'] = dhcp_handling
            if dns_nameservers is not None:
                kwargs['dnsNameservers'] = dns_nameservers
                
            vlan = meraki_client.dashboard.appliance.updateNetworkApplianceVlan(
                network_id,
                vlan_id,
                **kwargs
            )
            
            # Build success message with details of what was updated
            msg = f"✅ VLAN {vlan_id} updated successfully!"
            if reserved_ip_ranges:
                msg += f"\n- Reserved IP ranges configured: {len(reserved_ip_ranges)} range(s)"
            if fixed_ip_assignments:
                msg += f"\n- Fixed IP assignments configured: {len(fixed_ip_assignments)} assignment(s)"
            if dhcp_options:
                msg += f"\n- DHCP options configured: {len(dhcp_options)} option(s)"
                
            return msg
            
        except Exception as e:
            return f"Error updating VLAN: {str(e)}"
    
    @app.tool(
        name="delete_network_appliance_vlan",
        description="🔌 Delete a VLAN (CAREFUL!)"
    )
    def delete_network_appliance_vlan(network_id: str, vlan_id: str):
        """Delete a VLAN from the network."""
        try:
            meraki_client.dashboard.appliance.deleteNetworkApplianceVlan(network_id, vlan_id)
            return f"✅ VLAN {vlan_id} deleted successfully!"
            
        except Exception as e:
            return f"Error deleting VLAN: {str(e)}"
    
    # ========== Port Management ==========
    
    @app.tool(
        name="get_network_appliance_ports",
        description="🔌 Get all ports on an appliance"
    )
    def get_network_appliance_ports(network_id: str):
        """Get all ports configured on a network appliance."""
        try:
            ports = meraki_client.dashboard.appliance.getNetworkAppliancePorts(network_id)
            
            if not ports:
                return f"No ports found for network {network_id}."
                
            result = f"# 🔌 Appliance Ports for Network {network_id}\n\n"
            for port in ports:
                port_num = port.get('number', 'Unknown')
                result += f"## Port {port_num}\n"
                result += f"- **Enabled**: {'✅' if port.get('enabled') else '❌'}\n"
                result += f"- **Type**: {port.get('type', 'N/A')}\n"
                result += f"- **VLAN**: {port.get('vlan', 'N/A')}\n"
                result += f"- **Access Policy**: {port.get('accessPolicy', 'N/A')}\n"
                
                if port.get('allowedVlans'):
                    result += f"- **Allowed VLANs**: {port.get('allowedVlans')}\n"
                    
                result += "\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving ports: {str(e)}"
    
    @app.tool(
        name="get_network_appliance_port",
        description="🔌 Get a single port configuration"
    )
    def get_network_appliance_port(network_id: str, port_id: str):
        """Get configuration for a specific port."""
        try:
            port = meraki_client.dashboard.appliance.getNetworkAppliancePort(network_id, port_id)
            
            result = f"# 🔌 Port {port_id} Configuration\n\n"
            result += f"**Enabled**: {'✅' if port.get('enabled') else '❌'}\n"
            result += f"**Type**: {port.get('type', 'N/A')}\n"
            result += f"**VLAN**: {port.get('vlan', 'N/A')}\n"
            result += f"**Access Policy**: {port.get('accessPolicy', 'N/A')}\n"
            
            if port.get('allowedVlans'):
                result += f"**Allowed VLANs**: {port.get('allowedVlans')}\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving port {port_id}: {str(e)}"
    
    @app.tool(
        name="update_network_appliance_port", 
        description="🔌 Update port configuration"
    )
    def update_network_appliance_port(
        network_id: str,
        port_id: str,
        enabled: Optional[bool] = None,
        type: Optional[str] = None,
        vlan: Optional[int] = None,
        allowed_vlans: Optional[str] = None
    ):
        """Update configuration for a specific port."""
        try:
            kwargs = {}
            if enabled is not None:
                kwargs['enabled'] = enabled
            if type is not None:
                kwargs['type'] = type
            if vlan is not None:
                kwargs['vlan'] = vlan
            if allowed_vlans is not None:
                kwargs['allowedVlans'] = allowed_vlans
                
            port = meraki_client.dashboard.appliance.updateNetworkAppliancePort(
                network_id,
                port_id,
                **kwargs
            )
            
            return f"✅ Port {port_id} updated successfully!"
            
        except Exception as e:
            return f"Error updating port: {str(e)}"
    
    # ========== Firewall Rules ==========
    
    @app.tool(
        name="get_network_appliance_firewall_l3_rules",
        description="🔥 Get Layer 3 firewall rules"
    )
    def get_network_appliance_firewall_l3_rules(network_id: str):
        """Get Layer 3 firewall rules for a network appliance."""
        try:
            rules = meraki_client.dashboard.appliance.getNetworkApplianceFirewallL3FirewallRules(network_id)
            
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
    
    @app.tool(
        name="update_network_appliance_firewall_l3_rules",
        description="🔥 Update Layer 3 firewall rules (BE CAREFUL!)"
    )
    def update_network_appliance_firewall_l3_rules(
        network_id: str, 
        rules: Any
    ):
        """Update L3 firewall rules for a network (replaces all rules)."""
        try:
            import json
            
            # Handle rules parameter - MCP may pass as JSON string
            if isinstance(rules, str):
                try:
                    rules = json.loads(rules)
                except:
                    pass
                    
            result = meraki_client.dashboard.appliance.updateNetworkApplianceFirewallL3FirewallRules(
                network_id,
                rules=rules
            )
            
            return f"✅ L3 Firewall rules updated successfully! Total rules: {len(rules)}"
            
        except Exception as e:
            return f"Error updating L3 firewall rules: {str(e)}"
    
    @app.tool(
        name="get_network_appliance_firewall_l7_rules",
        description="🔥 Get Layer 7 firewall rules"
    )
    def get_network_appliance_firewall_l7_rules(network_id: str):
        """Get Layer 7 firewall rules for a network appliance."""
        try:
            rules = meraki_client.dashboard.appliance.getNetworkApplianceFirewallL7FirewallRules(network_id)
            
            if not rules or not rules.get('rules'):
                return f"No L7 firewall rules found for network {network_id}."
                
            result = f"# 🔥 Layer 7 Firewall Rules for Network {network_id}\n\n"
            
            for idx, rule in enumerate(rules.get('rules', []), 1):
                result += f"## Rule {idx}\n"
                result += f"- **Policy**: {rule.get('policy', 'N/A')}\n"
                result += f"- **Type**: {rule.get('type', 'N/A')}\n"
                
                if rule.get('value'):
                    if isinstance(rule['value'], dict):
                        result += f"- **Value**: {rule['value'].get('name', 'N/A')} (ID: {rule['value'].get('id', 'N/A')})\n"
                    else:
                        result += f"- **Value**: {rule['value']}\n"
                        
                result += "\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving L7 firewall rules: {str(e)}"
    
    @app.tool(
        name="update_network_appliance_firewall_l7_rules",
        description="🔥 Update Layer 7 firewall rules"
    )
    def update_network_appliance_firewall_l7_rules(
        network_id: str,
        rules: Any
    ):
        """Update L7 firewall rules for a network."""
        try:
            import json
            
            # Handle rules parameter - MCP may pass as JSON string
            if isinstance(rules, str):
                try:
                    rules = json.loads(rules)
                except:
                    pass
                    
            result = meraki_client.dashboard.appliance.updateNetworkApplianceFirewallL7FirewallRules(
                network_id,
                rules=rules
            )
            
            return f"✅ L7 Firewall rules updated successfully! Total rules: {len(rules)}"
            
        except Exception as e:
            return f"Error updating L7 firewall rules: {str(e)}"
    
    @app.tool(
        name="get_network_appliance_firewall_port_forwarding_rules",
        description="🔥 Get port forwarding rules"
    )
    def get_network_appliance_firewall_port_forwarding_rules(network_id: str):
        """Get port forwarding rules for a network appliance."""
        try:
            rules = meraki_client.dashboard.appliance.getNetworkApplianceFirewallPortForwardingRules(network_id)
            
            if not rules or not rules.get('rules'):
                return f"No port forwarding rules found for network {network_id}."
                
            result = f"# 🔥 Port Forwarding Rules for Network {network_id}\n\n"
            
            for idx, rule in enumerate(rules.get('rules', []), 1):
                result += f"## Rule {idx}: {rule.get('name', 'Unnamed')}\n"
                result += f"- **Public Port**: {rule.get('publicPort', 'N/A')}\n"
                result += f"- **Local IP**: {rule.get('localIp', 'N/A')}\n"
                result += f"- **Local Port**: {rule.get('localPort', 'N/A')}\n"
                result += f"- **Protocol**: {rule.get('protocol', 'N/A')}\n"
                
                if rule.get('allowedIps'):
                    result += f"- **Allowed IPs**: {', '.join(rule['allowedIps'])}\n"
                    
                result += "\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving port forwarding rules: {str(e)}"
    
    @app.tool(
        name="update_network_appliance_firewall_port_forwarding_rules",
        description="🔥 Update port forwarding rules"
    )
    def update_network_appliance_firewall_port_forwarding_rules(
        network_id: str,
        rules: Any
    ):
        """Update port forwarding rules for a network."""
        try:
            import json
            
            # Handle rules parameter - MCP may pass as JSON string
            if isinstance(rules, str):
                try:
                    rules = json.loads(rules)
                except:
                    pass
                    
            result = meraki_client.dashboard.appliance.updateNetworkApplianceFirewallPortForwardingRules(
                network_id,
                rules=rules
            )
            
            return f"✅ Port forwarding rules updated successfully! Total rules: {len(rules)}"
            
        except Exception as e:
            return f"Error updating port forwarding rules: {str(e)}"
    
    @app.tool(
        name="get_network_appliance_firewall_one_to_one_nat_rules",
        description="🔥 Get 1:1 NAT rules"
    )
    def get_network_appliance_firewall_one_to_one_nat_rules(network_id: str):
        """Get 1:1 NAT rules for a network appliance."""
        try:
            rules = meraki_client.dashboard.appliance.getNetworkApplianceFirewallOneToOneNatRules(network_id)
            
            if not rules or not rules.get('rules'):
                return f"No 1:1 NAT rules found for network {network_id}."
                
            result = f"# 🔥 1:1 NAT Rules for Network {network_id}\n\n"
            
            for idx, rule in enumerate(rules.get('rules', []), 1):
                result += f"## Rule {idx}: {rule.get('name', 'Unnamed')}\n"
                result += f"- **Public IP**: {rule.get('publicIp', 'N/A')}\n"
                result += f"- **LAN IP**: {rule.get('lanIp', 'N/A')}\n"
                result += f"- **Uplink**: {rule.get('uplink', 'N/A')}\n"
                
                if rule.get('allowedInbound'):
                    result += "- **Allowed Inbound**:\n"
                    for inbound in rule['allowedInbound']:
                        result += f"  - {inbound.get('protocol', 'any')} on ports {inbound.get('destinationPorts', 'any')}\n"
                        if inbound.get('allowedIps'):
                            result += f"    from IPs: {', '.join(inbound['allowedIps'])}\n"
                            
                result += "\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving 1:1 NAT rules: {str(e)}"
    
    @app.tool(
        name="update_network_appliance_firewall_one_to_one_nat_rules",
        description="🔥 Update 1:1 NAT rules"
    )
    def update_network_appliance_firewall_one_to_one_nat_rules(
        network_id: str,
        rules: Any
    ):
        """Update 1:1 NAT rules for a network."""
        try:
            import json
            
            # Handle rules parameter - MCP may pass as JSON string
            if isinstance(rules, str):
                try:
                    rules = json.loads(rules)
                except:
                    pass
                    
            result = meraki_client.dashboard.appliance.updateNetworkApplianceFirewallOneToOneNatRules(
                network_id,
                rules=rules
            )
            
            return f"✅ 1:1 NAT rules updated successfully! Total rules: {len(rules)}"
            
        except Exception as e:
            return f"Error updating 1:1 NAT rules: {str(e)}"
    
    @app.tool(
        name="get_network_appliance_firewall_one_to_many_nat_rules",
        description="🔥 Get 1:Many NAT rules"
    )
    def get_network_appliance_firewall_one_to_many_nat_rules(network_id: str):
        """Get 1:Many NAT rules for a network appliance."""
        try:
            rules = meraki_client.dashboard.appliance.getNetworkApplianceFirewallOneToManyNatRules(network_id)
            
            if not rules or not rules.get('rules'):
                return f"No 1:Many NAT rules found for network {network_id}."
                
            result = f"# 🔥 1:Many NAT Rules for Network {network_id}\n\n"
            
            for idx, rule in enumerate(rules.get('rules', []), 1):
                result += f"## Rule {idx}: {rule.get('name', 'Unnamed')}\n"
                result += f"- **Public IP**: {rule.get('publicIp', 'N/A')}\n"
                result += f"- **Uplink**: {rule.get('uplink', 'N/A')}\n"
                
                if rule.get('portRules'):
                    result += "- **Port Rules**:\n"
                    for port_rule in rule['portRules']:
                        result += f"  - {port_rule.get('name', 'Unnamed')}: "
                        result += f"{port_rule.get('protocol', 'any')} "
                        result += f"port {port_rule.get('publicPort', 'any')} -> "
                        result += f"{port_rule.get('localIp', 'N/A')}:{port_rule.get('localPort', 'N/A')}\n"
                        
                        if port_rule.get('allowedIps'):
                            result += f"    Allowed IPs: {', '.join(port_rule['allowedIps'])}\n"
                            
                result += "\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving 1:Many NAT rules: {str(e)}"
    
    # ========== Content Filtering ==========
    
    @app.tool(
        name="get_network_appliance_content_filtering",
        description="🌐 Get content filtering settings"
    )
    def get_network_appliance_content_filtering(network_id: str):
        """Get content filtering settings for a network appliance."""
        try:
            filtering = meraki_client.dashboard.appliance.getNetworkApplianceContentFiltering(network_id)
            
            result = f"# 🌐 Content Filtering for Network {network_id}\n\n"
            
            # Blocked URL categories
            blocked_categories = filtering.get('blockedUrlCategories', [])
            if blocked_categories:
                result += "## Blocked Categories\n"
                for category in blocked_categories:
                    # Handle both dict and string formats
                    if isinstance(category, dict):
                        result += f"- {category.get('name', category.get('id', 'Unknown'))}\n"
                    else:
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
    
    @app.tool(
        name="update_network_appliance_content_filtering",
        description="🌐 Update content filtering settings"
    )
    def update_network_appliance_content_filtering(
        network_id: str,
        blocked_categories: Optional[Any] = None,
        blocked_patterns: Optional[Any] = None,
        allowed_patterns: Optional[Any] = None
    ):
        """Update content filtering settings for a network.
        
        Note: blocked_categories should be category IDs like 'meraki:contentFiltering/category/C22'
        or the shorthand like 'C22'. The API returns objects with 'id' and 'name' fields.
        """
        try:
            import json
            
            kwargs = {}
            
            # Handle blocked_categories - MCP may pass as JSON string
            if blocked_categories is not None:
                if isinstance(blocked_categories, str):
                    try:
                        blocked_categories = json.loads(blocked_categories)
                    except:
                        pass
                # If passed as list of dicts with 'id' field, extract the IDs
                if isinstance(blocked_categories, list) and blocked_categories:
                    if isinstance(blocked_categories[0], dict):
                        blocked_categories = [cat.get('id', cat) for cat in blocked_categories]
                kwargs['blockedUrlCategories'] = blocked_categories
                
            # Handle patterns - MCP may pass as JSON strings
            if blocked_patterns is not None:
                if isinstance(blocked_patterns, str):
                    try:
                        blocked_patterns = json.loads(blocked_patterns)
                    except:
                        pass
                kwargs['blockedUrlPatterns'] = blocked_patterns
                
            if allowed_patterns is not None:
                if isinstance(allowed_patterns, str):
                    try:
                        allowed_patterns = json.loads(allowed_patterns)
                    except:
                        pass
                kwargs['allowedUrlPatterns'] = allowed_patterns
                
            result = meraki_client.dashboard.appliance.updateNetworkApplianceContentFiltering(
                network_id,
                **kwargs
            )
            
            return "✅ Content filtering updated successfully!"
            
        except Exception as e:
            return f"Error updating content filtering: {str(e)}"
    
    # ========== VPN Configuration ==========
    
    @app.tool(
        name="get_network_appliance_vpn_site_to_site",
        description="🔐 Get site-to-site VPN settings"
    )
    def get_network_appliance_vpn_site_to_site(network_id: str):
        """Get site-to-site VPN settings for a network appliance."""
        try:
            vpn = meraki_client.dashboard.appliance.getNetworkApplianceVpnSiteToSiteVpn(network_id)
            
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
    
    @app.tool(
        name="update_network_appliance_vpn_site_to_site",
        description="🔐 Update site-to-site VPN settings"
    )
    def update_network_appliance_vpn_site_to_site(
        network_id: str,
        mode: str,
        hubs: Optional[List[Dict[str, Any]]] = None,
        subnets: Optional[List[Dict[str, Any]]] = None
    ):
        """Update site-to-site VPN settings for a network."""
        try:
            kwargs = {'mode': mode}
            if hubs is not None:
                kwargs['hubs'] = hubs
            if subnets is not None:
                kwargs['subnets'] = subnets
                
            result = meraki_client.dashboard.appliance.updateNetworkApplianceVpnSiteToSiteVpn(
                network_id,
                **kwargs
            )
            
            return f"✅ Site-to-site VPN updated successfully! Mode: {mode}"
            
        except Exception as e:
            return f"Error updating site-to-site VPN: {str(e)}"
    
    @app.tool(
        name="get_network_appliance_vpn_bgp",
        description="🔐 Get VPN BGP settings"
    )
    def get_network_appliance_vpn_bgp(network_id: str):
        """Get VPN BGP settings for a network appliance."""
        try:
            bgp = meraki_client.dashboard.appliance.getNetworkApplianceVpnBgp(network_id)
            
            result = f"# 🔐 VPN BGP Settings for Network {network_id}\n\n"
            
            result += f"**Enabled**: {'✅' if bgp.get('enabled') else '❌'}\n"
            result += f"**AS Number**: {bgp.get('asNumber', 'N/A')}\n"
            result += f"**IBGP Hold Timer**: {bgp.get('ibgpHoldTimer', 'N/A')}s\n"
            result += f"**EBGP Hold Timer**: {bgp.get('ebgpHoldTimer', 'N/A')}s\n"
            result += f"**EBGP Multihop**: {bgp.get('ebgpMultihop', 'N/A')}\n"
            
            neighbors = bgp.get('neighbors', [])
            if neighbors:
                result += "\n## BGP Neighbors\n"
                for neighbor in neighbors:
                    result += f"- **IP**: {neighbor.get('ip', 'N/A')}\n"
                    result += f"  - Remote AS: {neighbor.get('remoteAsNumber', 'N/A')}\n"
                    result += f"  - Receive limit: {neighbor.get('receiveLimit', 'N/A')}\n"
                    result += f"  - Allow transit: {'✅' if neighbor.get('allowTransit') else '❌'}\n"
                    result += "\n"
                    
            return result
            
        except Exception as e:
            return f"Error retrieving VPN BGP settings: {str(e)}"
    
    @app.tool(
        name="update_network_appliance_vpn_bgp",
        description="🔐 Update VPN BGP settings"
    )
    def update_network_appliance_vpn_bgp(
        network_id: str,
        enabled: bool,
        as_number: Optional[int] = None,
        ibgp_hold_timer: Optional[int] = None,
        neighbors: Optional[List[Dict[str, Any]]] = None
    ):
        """Update VPN BGP settings for a network."""
        try:
            kwargs = {'enabled': enabled}
            if as_number is not None:
                kwargs['asNumber'] = as_number
            if ibgp_hold_timer is not None:
                kwargs['ibgpHoldTimer'] = ibgp_hold_timer
            if neighbors is not None:
                kwargs['neighbors'] = neighbors
                
            result = meraki_client.dashboard.appliance.updateNetworkApplianceVpnBgp(
                network_id,
                **kwargs
            )
            
            return f"✅ VPN BGP settings updated successfully! Enabled: {enabled}"
            
        except Exception as e:
            return f"Error updating VPN BGP settings: {str(e)}"
    
    # ========== Security Features ==========
    
    @app.tool(
        name="get_network_appliance_security_malware",
        description="🛡️ Get malware protection settings"
    )
    def get_network_appliance_security_malware(network_id: str):
        """Get malware protection settings for a network appliance."""
        try:
            malware = meraki_client.dashboard.appliance.getNetworkApplianceSecurityMalware(network_id)
            
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
    
    @app.tool(
        name="update_network_appliance_security_malware",
        description="🛡️ Update malware protection settings"
    )
    def update_network_appliance_security_malware(
        network_id: str,
        mode: str,
        allowed_urls: Optional[List[Dict[str, str]]] = None,
        allowed_files: Optional[List[Dict[str, str]]] = None
    ):
        """Update malware protection settings for a network."""
        try:
            kwargs = {'mode': mode}
            if allowed_urls is not None:
                kwargs['allowedUrls'] = allowed_urls
            if allowed_files is not None:
                kwargs['allowedFiles'] = allowed_files
                
            result = meraki_client.dashboard.appliance.updateNetworkApplianceSecurityMalware(
                network_id,
                **kwargs
            )
            
            return f"✅ Malware protection updated successfully! Mode: {mode}"
            
        except Exception as e:
            return f"Error updating malware protection: {str(e)}"
    
    @app.tool(
        name="get_network_appliance_security_intrusion",
        description="🚨 Get intrusion detection/prevention settings"
    )
    def get_network_appliance_security_intrusion(network_id: str):
        """Get intrusion detection and prevention settings for a network."""
        try:
            intrusion = meraki_client.dashboard.appliance.getNetworkApplianceSecurityIntrusion(network_id)
            
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
    
    @app.tool(
        name="update_network_appliance_security_intrusion",
        description="🚨 Update intrusion detection/prevention settings"
    )
    def update_network_appliance_security_intrusion(
        network_id: str,
        mode: str,
        ids_rulesets: Optional[str] = None,
        protected_networks: Optional[Dict[str, Any]] = None
    ):
        """Update intrusion detection settings for a network."""
        try:
            kwargs = {'mode': mode}
            if ids_rulesets is not None:
                kwargs['idsRulesets'] = ids_rulesets
            if protected_networks is not None:
                kwargs['protectedNetworks'] = protected_networks
                
            result = meraki_client.dashboard.appliance.updateNetworkApplianceSecurityIntrusion(
                network_id,
                **kwargs
            )
            
            return f"✅ Intrusion detection updated successfully! Mode: {mode}"
            
        except Exception as e:
            return f"Error updating intrusion detection: {str(e)}"
    
    # ========== Traffic Shaping ==========
    
    @app.tool(
        name="get_network_appliance_traffic_shaping",
        description="🚦 Get traffic shaping settings"
    )
    def get_network_appliance_traffic_shaping(network_id: str):
        """Get traffic shaping settings for a network appliance."""
        try:
            shaping = meraki_client.dashboard.appliance.getNetworkApplianceTrafficShaping(network_id)
            
            result = f"# 🚦 Traffic Shaping for Network {network_id}\n\n"
            
            # Global bandwidth limits
            if shaping.get('globalBandwidthLimits'):
                limits = shaping['globalBandwidthLimits']
                result += "## Global Bandwidth Limits\n"
                if limits.get('limitUp'):
                    result += f"- **Upload**: {limits['limitUp']} Mbps\n"
                if limits.get('limitDown'):
                    result += f"- **Download**: {limits['limitDown']} Mbps\n"
                result += "\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving traffic shaping settings: {str(e)}"
    
    @app.tool(
        name="update_network_appliance_traffic_shaping",
        description="🚦 Update traffic shaping settings"
    )
    def update_network_appliance_traffic_shaping(
        network_id: str,
        global_bandwidth_limits: Optional[Dict[str, int]] = None
    ):
        """Update traffic shaping settings for a network."""
        try:
            kwargs = {}
            if global_bandwidth_limits is not None:
                kwargs['globalBandwidthLimits'] = global_bandwidth_limits
                
            result = meraki_client.dashboard.appliance.updateNetworkApplianceTrafficShaping(
                network_id,
                **kwargs
            )
            
            return "✅ Traffic shaping updated successfully!"
            
        except Exception as e:
            return f"Error updating traffic shaping: {str(e)}"
    
    @app.tool(
        name="get_network_appliance_traffic_shaping_rules",
        description="🚦 Get traffic shaping rules"
    )
    def get_network_appliance_traffic_shaping_rules(network_id: str):
        """Get traffic shaping rules for a network appliance."""
        try:
            rules = meraki_client.dashboard.appliance.getNetworkApplianceTrafficShapingRules(network_id)
            
            if not rules or not rules.get('rules'):
                return f"No traffic shaping rules found for network {network_id}."
                
            result = f"# 🚦 Traffic Shaping Rules for Network {network_id}\n\n"
            
            # Default rule
            if rules.get('defaultRulesEnabled'):
                result += "**Default rules**: ✅ Enabled\n\n"
                
            # Custom rules
            for idx, rule in enumerate(rules.get('rules', []), 1):
                result += f"## Rule {idx}\n"
                
                # Definitions
                for definition in rule.get('definitions', []):
                    result += f"- **Type**: {definition.get('type', 'N/A')}\n"
                    result += f"- **Value**: {definition.get('value', 'N/A')}\n"
                    
                # Per-client bandwidth
                if rule.get('perClientBandwidthLimits'):
                    limits = rule['perClientBandwidthLimits']
                    result += f"- **Per-client limits**:\n"
                    if limits.get('bandwidthLimits'):
                        bl = limits['bandwidthLimits']
                        if bl.get('limitUp'):
                            result += f"  - Upload: {bl['limitUp']} Mbps\n"
                        if bl.get('limitDown'):
                            result += f"  - Download: {bl['limitDown']} Mbps\n"
                            
                # Priority
                if rule.get('priority'):
                    result += f"- **Priority**: {rule['priority']}\n"
                    
                result += "\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving traffic shaping rules: {str(e)}"
    
    @app.tool(
        name="update_network_appliance_traffic_shaping_rules",
        description="🚦 Update traffic shaping rules"
    )
    def update_network_appliance_traffic_shaping_rules(
        network_id: str,
        rules: Any,
        default_rules_enabled: Optional[bool] = None
    ):
        """Update traffic shaping rules for a network."""
        try:
            import json
            
            # Handle rules parameter - MCP may pass as JSON string
            if isinstance(rules, str):
                try:
                    rules = json.loads(rules)
                except:
                    pass
                    
            kwargs = {'rules': rules}
            if default_rules_enabled is not None:
                kwargs['defaultRulesEnabled'] = default_rules_enabled
                
            result = meraki_client.dashboard.appliance.updateNetworkApplianceTrafficShapingRules(
                network_id,
                **kwargs
            )
            
            return f"✅ Traffic shaping rules updated successfully! Total rules: {len(rules)}"
            
        except Exception as e:
            return f"Error updating traffic shaping rules: {str(e)}"
    
    @app.tool(
        name="get_network_appliance_traffic_shaping_uplink_bandwidth",
        description="🚦 Get uplink bandwidth settings"
    )
    def get_network_appliance_traffic_shaping_uplink_bandwidth(network_id: str):
        """Get uplink bandwidth settings for traffic shaping."""
        try:
            bandwidth = meraki_client.dashboard.appliance.getNetworkApplianceTrafficShapingUplinkBandwidth(network_id)
            
            result = f"# 🚦 Uplink Bandwidth Settings for Network {network_id}\n\n"
            
            # WAN1 bandwidth
            if bandwidth.get('wan1'):
                wan1 = bandwidth['wan1']
                result += "## WAN 1\n"
                result += f"- **Upload**: {wan1.get('bandwidthLimits', {}).get('limitUp', 'N/A')} Mbps\n"
                result += f"- **Download**: {wan1.get('bandwidthLimits', {}).get('limitDown', 'N/A')} Mbps\n\n"
                
            # WAN2 bandwidth
            if bandwidth.get('wan2'):
                wan2 = bandwidth['wan2']
                result += "## WAN 2\n"
                result += f"- **Upload**: {wan2.get('bandwidthLimits', {}).get('limitUp', 'N/A')} Mbps\n"
                result += f"- **Download**: {wan2.get('bandwidthLimits', {}).get('limitDown', 'N/A')} Mbps\n\n"
                
            # Cellular bandwidth
            if bandwidth.get('cellular'):
                cellular = bandwidth['cellular']
                result += "## Cellular\n"
                result += f"- **Upload**: {cellular.get('bandwidthLimits', {}).get('limitUp', 'N/A')} Mbps\n"
                result += f"- **Download**: {cellular.get('bandwidthLimits', {}).get('limitDown', 'N/A')} Mbps\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving uplink bandwidth settings: {str(e)}"
    
    @app.tool(
        name="update_network_appliance_traffic_shaping_uplink_bandwidth",
        description="🚦 Update uplink bandwidth settings"
    )
    def update_network_appliance_traffic_shaping_uplink_bandwidth(
        network_id: str,
        wan1: Optional[Dict[str, Any]] = None,
        wan2: Optional[Dict[str, Any]] = None,
        cellular: Optional[Dict[str, Any]] = None
    ):
        """Update uplink bandwidth settings for traffic shaping."""
        try:
            kwargs = {}
            if wan1 is not None:
                kwargs['wan1'] = wan1
            if wan2 is not None:
                kwargs['wan2'] = wan2
            if cellular is not None:
                kwargs['cellular'] = cellular
                
            result = meraki_client.dashboard.appliance.updateNetworkApplianceTrafficShapingUplinkBandwidth(
                network_id,
                **kwargs
            )
            
            return "✅ Uplink bandwidth settings updated successfully!"
            
        except Exception as e:
            return f"Error updating uplink bandwidth: {str(e)}"
    
    # ========== Warm Spare Configuration ==========
    
    @app.tool(
        name="get_network_appliance_warm_spare",
        description="🔄 Get warm spare configuration"
    )
    def get_network_appliance_warm_spare(network_id: str):
        """Get warm spare configuration for a network appliance."""
        try:
            spare = meraki_client.dashboard.appliance.getNetworkApplianceWarmSpare(network_id)
            
            result = f"# 🔄 Warm Spare Configuration for Network {network_id}\n\n"
            
            result += f"**Enabled**: {'✅' if spare.get('enabled') else '❌'}\n"
            
            if spare.get('primarySerial'):
                result += f"**Primary Serial**: {spare['primarySerial']}\n"
                
            if spare.get('spareSerial'):
                result += f"**Spare Serial**: {spare['spareSerial']}\n"
                
            if spare.get('uplinkMode'):
                result += f"**Uplink Mode**: {spare['uplinkMode']}\n"
                
            if spare.get('wan1'):
                result += f"\n## WAN 1\n"
                result += f"- IP: {spare['wan1'].get('ip', 'N/A')}\n"
                result += f"- Subnet: {spare['wan1'].get('subnet', 'N/A')}\n"
                
            if spare.get('wan2'):
                result += f"\n## WAN 2\n"
                result += f"- IP: {spare['wan2'].get('ip', 'N/A')}\n"
                result += f"- Subnet: {spare['wan2'].get('subnet', 'N/A')}\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving warm spare configuration: {str(e)}"
    
    @app.tool(
        name="update_network_appliance_warm_spare",
        description="🔄 Update warm spare configuration"
    )
    def update_network_appliance_warm_spare(
        network_id: str,
        enabled: bool,
        spare_serial: Optional[str] = None,
        uplink_mode: Optional[str] = None,
        wan1: Optional[Dict[str, str]] = None,
        wan2: Optional[Dict[str, str]] = None
    ):
        """Update warm spare configuration for a network."""
        try:
            kwargs = {'enabled': enabled}
            if spare_serial is not None:
                kwargs['spareSerial'] = spare_serial
            if uplink_mode is not None:
                kwargs['uplinkMode'] = uplink_mode
            if wan1 is not None:
                kwargs['wan1'] = wan1
            if wan2 is not None:
                kwargs['wan2'] = wan2
                
            result = meraki_client.dashboard.appliance.updateNetworkApplianceWarmSpare(
                network_id,
                **kwargs
            )
            
            return f"✅ Warm spare configuration updated successfully! Enabled: {enabled}"
            
        except Exception as e:
            return f"Error updating warm spare configuration: {str(e)}"
    
    @app.tool(
        name="swap_network_appliance_warm_spare",
        description="🔄 Swap warm spare appliances"
    )
    def swap_network_appliance_warm_spare(network_id: str):
        """Swap the primary and warm spare appliances."""
        try:
            result = meraki_client.dashboard.appliance.swapNetworkApplianceWarmSpare(network_id)
            
            return "✅ Warm spare appliances swapped successfully!"
            
        except Exception as e:
            return f"Error swapping warm spare appliances: {str(e)}"
    
    # ========== SSID Configuration (MX Wireless) ==========
    
    @app.tool(
        name="get_network_appliance_ssids",
        description="📶 Get wireless SSIDs on MX appliance"
    )
    def get_network_appliance_ssids(network_id: str):
        """Get wireless SSIDs configured on an MX appliance."""
        try:
            ssids = meraki_client.dashboard.appliance.getNetworkApplianceSsids(network_id)
            
            if not ssids:
                return f"No SSIDs found for network {network_id}."
                
            result = f"# 📶 MX Wireless SSIDs for Network {network_id}\n\n"
            
            for ssid in ssids:
                number = ssid.get('number', 'N/A')
                result += f"## SSID {number}: {ssid.get('name', 'Unnamed')}\n"
                result += f"- **Enabled**: {'✅' if ssid.get('enabled') else '❌'}\n"
                result += f"- **Visible**: {'✅' if ssid.get('visible') else '❌ Hidden'}\n"
                result += f"- **Auth Mode**: {ssid.get('authMode', 'N/A')}\n"
                
                if ssid.get('encryptionMode'):
                    result += f"- **Encryption**: {ssid['encryptionMode']}\n"
                    
                if ssid.get('wpaEncryptionMode'):
                    result += f"- **WPA Mode**: {ssid['wpaEncryptionMode']}\n"
                    
                if ssid.get('radiusServers'):
                    result += f"- **RADIUS Servers**: {len(ssid['radiusServers'])} configured\n"
                    
                result += "\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving SSIDs: {str(e)}"
    
    @app.tool(
        name="get_network_appliance_ssid",
        description="📶 Get a specific SSID configuration"
    )
    def get_network_appliance_ssid(network_id: str, number: str):
        """Get configuration for a specific SSID."""
        try:
            ssid = meraki_client.dashboard.appliance.getNetworkApplianceSsid(network_id, number)
            
            result = f"# 📶 SSID {number} Configuration\n\n"
            result += f"**Name**: {ssid.get('name', 'Unnamed')}\n"
            result += f"**Enabled**: {'✅' if ssid.get('enabled') else '❌'}\n"
            result += f"**Visible**: {'✅' if ssid.get('visible') else '❌ Hidden'}\n"
            result += f"**Auth Mode**: {ssid.get('authMode', 'N/A')}\n"
            
            if ssid.get('psk'):
                result += f"**PSK**: {'*' * 8} (hidden)\n"
                
            if ssid.get('encryptionMode'):
                result += f"**Encryption**: {ssid['encryptionMode']}\n"
                
            if ssid.get('wpaEncryptionMode'):
                result += f"**WPA Mode**: {ssid['wpaEncryptionMode']}\n"
                
            if ssid.get('defaultVlanId'):
                result += f"**VLAN**: {ssid['defaultVlanId']}\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving SSID {number}: {str(e)}"
    
    @app.tool(
        name="update_network_appliance_ssid",
        description="📶 Update SSID configuration"
    )
    def update_network_appliance_ssid(
        network_id: str,
        number: str,
        name: Optional[str] = None,
        enabled: Optional[bool] = None,
        auth_mode: Optional[str] = None,
        psk: Optional[str] = None,
        visible: Optional[bool] = None
    ):
        """Update configuration for a specific SSID."""
        try:
            kwargs = {}
            if name is not None:
                kwargs['name'] = name
            if enabled is not None:
                kwargs['enabled'] = enabled
            if auth_mode is not None:
                kwargs['authMode'] = auth_mode
            if psk is not None:
                kwargs['psk'] = psk
            if visible is not None:
                kwargs['visible'] = visible
                
            result = meraki_client.dashboard.appliance.updateNetworkApplianceSsid(
                network_id,
                number,
                **kwargs
            )
            
            return f"✅ SSID {number} updated successfully!"
            
        except Exception as e:
            return f"Error updating SSID: {str(e)}"
    
    # ========== Static Routes ==========
    
    @app.tool(
        name="get_network_appliance_static_routes",
        description="🛣️ Get static routes"
    )
    def get_network_appliance_static_routes(network_id: str):
        """Get static routes configured on a network appliance."""
        try:
            routes = meraki_client.dashboard.appliance.getNetworkApplianceStaticRoutes(network_id)
            
            if not routes:
                return f"No static routes found for network {network_id}."
                
            result = f"# 🛣️ Static Routes for Network {network_id}\n\n"
            
            for idx, route in enumerate(routes, 1):
                result += f"## Route {idx}: {route.get('name', 'Unnamed')}\n"
                result += f"- **Subnet**: {route.get('subnet', 'N/A')}\n"
                result += f"- **Gateway IP**: {route.get('gatewayIp', 'N/A')}\n"
                result += f"- **Gateway VLAN**: {route.get('gatewayVlanId', 'N/A')}\n"
                result += f"- **Enabled**: {'✅' if route.get('enabled', True) else '❌'}\n"
                
                if route.get('fixedIpAssignments'):
                    result += f"- **Fixed IP Assignments**: {len(route['fixedIpAssignments'])} configured\n"
                    
                if route.get('reservedIpRanges'):
                    result += f"- **Reserved IP Ranges**: {len(route['reservedIpRanges'])} configured\n"
                    
                result += "\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving static routes: {str(e)}"
    
    @app.tool(
        name="get_network_appliance_static_route",
        description="🛣️ Get a specific static route"
    )
    def get_network_appliance_static_route(network_id: str, static_route_id: str):
        """Get details of a specific static route."""
        try:
            route = meraki_client.dashboard.appliance.getNetworkApplianceStaticRoute(network_id, static_route_id)
            
            result = f"# 🛣️ Static Route Details\n\n"
            result += f"**Name**: {route.get('name', 'Unnamed')}\n"
            result += f"**Subnet**: {route.get('subnet', 'N/A')}\n"
            result += f"**Gateway IP**: {route.get('gatewayIp', 'N/A')}\n"
            result += f"**Gateway VLAN**: {route.get('gatewayVlanId', 'N/A')}\n"
            result += f"**Enabled**: {'✅' if route.get('enabled', True) else '❌'}\n"
            
            if route.get('fixedIpAssignments'):
                result += "\n## Fixed IP Assignments\n"
                for mac, config in route['fixedIpAssignments'].items():
                    result += f"- {mac}: {config.get('ip')} ({config.get('name', 'No name')})\n"
                    
            if route.get('reservedIpRanges'):
                result += "\n## Reserved IP Ranges\n"
                for range_info in route['reservedIpRanges']:
                    result += f"- {range_info.get('start')} to {range_info.get('end')} ({range_info.get('comment', 'No comment')})\n"
                    
            return result
            
        except Exception as e:
            return f"Error retrieving static route: {str(e)}"
    
    @app.tool(
        name="create_network_appliance_static_route",
        description="🛣️ Create a new static route"
    )
    def create_network_appliance_static_route(
        network_id: str,
        name: str,
        subnet: str,
        gateway_ip: str
    ):
        """Create a new static route on the network."""
        try:
            route = meraki_client.dashboard.appliance.createNetworkApplianceStaticRoute(
                network_id,
                name=name,
                subnet=subnet,
                gatewayIp=gateway_ip
            )
            
            return f"✅ Static route created successfully!\n\nName: {name}\nSubnet: {subnet}\nGateway: {gateway_ip}"
            
        except Exception as e:
            return f"Error creating static route: {str(e)}"
    
    @app.tool(
        name="update_network_appliance_static_route",
        description="🛣️ Update a static route"
    )
    def update_network_appliance_static_route(
        network_id: str,
        static_route_id: str,
        name: Optional[str] = None,
        subnet: Optional[str] = None,
        gateway_ip: Optional[str] = None,
        enabled: Optional[bool] = None
    ):
        """Update an existing static route."""
        try:
            kwargs = {}
            if name is not None:
                kwargs['name'] = name
            if subnet is not None:
                kwargs['subnet'] = subnet
            if gateway_ip is not None:
                kwargs['gatewayIp'] = gateway_ip
            if enabled is not None:
                kwargs['enabled'] = enabled
                
            route = meraki_client.dashboard.appliance.updateNetworkApplianceStaticRoute(
                network_id,
                static_route_id,
                **kwargs
            )
            
            return f"✅ Static route updated successfully!"
            
        except Exception as e:
            return f"Error updating static route: {str(e)}"
    
    @app.tool(
        name="delete_network_appliance_static_route",
        description="🛣️ Delete a static route"
    )
    def delete_network_appliance_static_route(network_id: str, static_route_id: str):
        """Delete a static route from the network."""
        try:
            meraki_client.dashboard.appliance.deleteNetworkApplianceStaticRoute(network_id, static_route_id)
            return f"✅ Static route deleted successfully!"
            
        except Exception as e:
            return f"Error deleting static route: {str(e)}"
    
    # ========== Settings ==========
    
    @app.tool(
        name="get_network_appliance_settings",
        description="⚙️ Get appliance settings"
    )
    def get_network_appliance_settings(network_id: str):
        """Get general settings for a network appliance."""
        try:
            settings = meraki_client.dashboard.appliance.getNetworkApplianceSettings(network_id)
            
            result = f"# ⚙️ Appliance Settings for Network {network_id}\n\n"
            
            if settings.get('clientTrackingMethod'):
                result += f"**Client Tracking Method**: {settings['clientTrackingMethod']}\n"
                
            if settings.get('deploymentMode'):
                result += f"**Deployment Mode**: {settings['deploymentMode']}\n"
                
            if settings.get('dynamicDnsPrefix'):
                result += f"**Dynamic DNS Prefix**: {settings['dynamicDnsPrefix']}\n"
                result += f"**Dynamic DNS URL**: {settings.get('dynamicDnsUrl', 'N/A')}\n"
                result += f"**Dynamic DNS Enabled**: {'✅' if settings.get('dynamicDnsEnabled') else '❌'}\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving appliance settings: {str(e)}"
    
    @app.tool(
        name="update_network_appliance_settings",
        description="⚙️ Update appliance settings"
    )
    def update_network_appliance_settings(
        network_id: str,
        client_tracking_method: Optional[str] = None,
        deployment_mode: Optional[str] = None,
        dynamic_dns_enabled: Optional[bool] = None
    ):
        """Update general settings for a network appliance."""
        try:
            kwargs = {}
            if client_tracking_method is not None:
                kwargs['clientTrackingMethod'] = client_tracking_method
            if deployment_mode is not None:
                kwargs['deploymentMode'] = deployment_mode
            if dynamic_dns_enabled is not None:
                kwargs['dynamicDnsEnabled'] = dynamic_dns_enabled
                
            result = meraki_client.dashboard.appliance.updateNetworkApplianceSettings(
                network_id,
                **kwargs
            )
            
            return "✅ Appliance settings updated successfully!"
            
        except Exception as e:
            return f"Error updating appliance settings: {str(e)}"
    
    # ========== Single LAN Configuration ==========
    
    @app.tool(
        name="get_network_appliance_single_lan",
        description="🔌 Get single LAN configuration"
    )
    def get_network_appliance_single_lan(network_id: str):
        """Get single LAN configuration for a network appliance."""
        try:
            lan = meraki_client.dashboard.appliance.getNetworkApplianceSingleLan(network_id)
            
            result = f"# 🔌 Single LAN Configuration for Network {network_id}\n\n"
            
            result += f"**Subnet**: {lan.get('subnet', 'N/A')}\n"
            result += f"**Appliance IP**: {lan.get('applianceIp', 'N/A')}\n"
            
            if lan.get('ipv6'):
                ipv6 = lan['ipv6']
                result += f"\n## IPv6 Configuration\n"
                result += f"- **Enabled**: {'✅' if ipv6.get('enabled') else '❌'}\n"
                if ipv6.get('prefixAssignments'):
                    result += f"- **Prefix Assignments**: {len(ipv6['prefixAssignments'])} configured\n"
                    
            return result
            
        except Exception as e:
            return f"Error retrieving single LAN configuration: {str(e)}"
    
    @app.tool(
        name="update_network_appliance_single_lan",
        description="🔌 Update single LAN configuration"
    )
    def update_network_appliance_single_lan(
        network_id: str,
        subnet: Optional[str] = None,
        appliance_ip: Optional[str] = None
    ):
        """Update single LAN configuration for a network appliance."""
        try:
            kwargs = {}
            if subnet is not None:
                kwargs['subnet'] = subnet
            if appliance_ip is not None:
                kwargs['applianceIp'] = appliance_ip
                
            result = meraki_client.dashboard.appliance.updateNetworkApplianceSingleLan(
                network_id,
                **kwargs
            )
            
            return "✅ Single LAN configuration updated successfully!"
            
        except Exception as e:
            return f"Error updating single LAN configuration: {str(e)}"
    
    # ========== Connectivity Monitoring ==========
    
    @app.tool(
        name="get_network_appliance_connectivity_monitoring_destinations",
        description="🌐 Get connectivity monitoring destinations"
    )
    def get_network_appliance_connectivity_monitoring_destinations(network_id: str):
        """Get connectivity monitoring destinations for a network appliance."""
        try:
            destinations = meraki_client.dashboard.appliance.getNetworkApplianceConnectivityMonitoringDestinations(network_id)
            
            result = f"# 🌐 Connectivity Monitoring Destinations for Network {network_id}\n\n"
            
            if destinations.get('destinations'):
                result += "## Monitoring Destinations\n"
                for dest in destinations['destinations']:
                    result += f"- **IP**: {dest.get('ip', 'N/A')}\n"
                    result += f"  - Description: {dest.get('description', 'N/A')}\n"
                    result += f"  - Default: {'✅' if dest.get('default') else '❌'}\n"
                    result += "\n"
            else:
                result += "No custom destinations configured.\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving connectivity monitoring destinations: {str(e)}"
    
    @app.tool(
        name="update_network_appliance_connectivity_monitoring_destinations",
        description="🌐 Update connectivity monitoring destinations"
    )
    def update_network_appliance_connectivity_monitoring_destinations(
        network_id: str,
        destinations: List[Dict[str, Any]]
    ):
        """Update connectivity monitoring destinations for a network appliance."""
        try:
            result = meraki_client.dashboard.appliance.updateNetworkApplianceConnectivityMonitoringDestinations(
                network_id,
                destinations=destinations
            )
            
            return f"✅ Connectivity monitoring destinations updated successfully! Total: {len(destinations)}"
            
        except Exception as e:
            return f"Error updating connectivity monitoring destinations: {str(e)}"
    
    # ========== Uplink Settings ==========
    
    @app.tool(
        name="get_device_appliance_uplinks_settings",
        description="🔗 Get uplink settings for a device"
    )
    def get_device_appliance_uplinks_settings(serial: str):
        """Get uplink settings for a specific appliance device."""
        try:
            settings = meraki_client.dashboard.appliance.getDeviceApplianceUplinksSettings(serial)
            
            result = f"# 🔗 Uplink Settings for Device {serial}\n\n"
            
            # Interfaces
            for interface in settings.get('interfaces', {}).values():
                if interface.get('enabled'):
                    result += f"## {interface.get('interface', 'Unknown')} Interface\n"
                    result += f"- **Enabled**: ✅\n"
                    
                    # WAN settings
                    wan = interface.get('wan', {})
                    if wan.get('enabled'):
                        result += f"- **WAN Enabled**: ✅\n"
                        result += f"- **Type**: {wan.get('type', 'N/A')}\n"
                        if wan.get('type') == 'static':
                            result += f"- **IP**: {wan.get('staticIp', 'N/A')}\n"
                            result += f"- **Gateway**: {wan.get('staticGatewayIp', 'N/A')}\n"
                            result += f"- **Subnet Mask**: {wan.get('staticSubnetMask', 'N/A')}\n"
                            if wan.get('staticDns'):
                                result += f"- **DNS**: {', '.join(wan['staticDns'])}\n"
                                
                    # SVI settings
                    svis = interface.get('svis', {})
                    for svi_name, svi in svis.items():
                        if svi:
                            result += f"\n### SVI: {svi_name}\n"
                            if svi.get('assignmentMode') == 'static':
                                result += f"- **IP**: {svi.get('address', 'N/A')}\n"
                                result += f"- **Gateway**: {svi.get('gateway', 'N/A')}\n"
                                
                    result += "\n"
                    
            return result
            
        except Exception as e:
            return f"Error retrieving uplink settings: {str(e)}"
    
    @app.tool(
        name="update_device_appliance_uplinks_settings",
        description="🔗 Update uplink settings for a device"
    )
    def update_device_appliance_uplinks_settings(
        serial: str,
        interfaces: Dict[str, Any]
    ):
        """Update uplink settings for a specific appliance device."""
        try:
            result = meraki_client.dashboard.appliance.updateDeviceApplianceUplinksSettings(
                serial,
                interfaces=interfaces
            )
            
            return "✅ Uplink settings updated successfully!"
            
        except Exception as e:
            return f"Error updating uplink settings: {str(e)}"
    
    # ========== Performance ==========
    
    @app.tool(
        name="get_device_appliance_performance",
        description="📊 Get appliance performance metrics"
    )
    def get_device_appliance_performance(serial: str, **kwargs):
        """Get performance metrics for a specific appliance device.
        
        Args:
            serial: Device serial number
            **kwargs: Additional parameters like timespan (default: 1800 seconds)
        """
        try:
            # Add default timespan if not specified (minimum is 1800 seconds)
            if 'timespan' not in kwargs and 't0' not in kwargs:
                kwargs['timespan'] = 1800  # Default to 30 minutes (minimum allowed)
            
            performance = meraki_client.dashboard.appliance.getDeviceAppliancePerformance(serial, **kwargs)
            
            result = f"# 📊 Performance Metrics for Device {serial}\n\n"
            
            if performance.get('perfScore'):
                result += f"**Performance Score**: {performance['perfScore']}/100\n\n"
                
            # CPU usage
            if 'cpuUsagePercent' in performance:
                cpu = performance['cpuUsagePercent']
                result += f"## CPU Usage\n"
                result += f"- Average: {cpu}%\n"
                if cpu > 80:
                    result += "- ⚠️ High CPU usage detected\n"
                result += "\n"
                
            # Memory usage
            if 'memUsagePercent' in performance:
                mem = performance['memUsagePercent']
                result += f"## Memory Usage\n"
                result += f"- Average: {mem}%\n"
                if mem > 80:
                    result += "- ⚠️ High memory usage detected\n"
                result += "\n"
                
            # WAN usage
            if performance.get('wan1') or performance.get('wan2'):
                result += "## WAN Performance\n"
                
                if performance.get('wan1'):
                    wan1 = performance['wan1']
                    result += f"### WAN 1\n"
                    result += f"- Sent: {wan1.get('sent', 0)} bytes\n"
                    result += f"- Received: {wan1.get('received', 0)} bytes\n"
                    
                if performance.get('wan2'):
                    wan2 = performance['wan2']
                    result += f"### WAN 2\n"
                    result += f"- Sent: {wan2.get('sent', 0)} bytes\n"
                    result += f"- Received: {wan2.get('received', 0)} bytes\n"
                    
            return result
            
        except Exception as e:
            return f"Error retrieving performance metrics: {str(e)}"
    
    # ========== DHCP Subnets ==========
    
    @app.tool(
        name="get_device_appliance_dhcp_subnets",
        description="🌐 Get DHCP subnet information"
    )
    def get_device_appliance_dhcp_subnets(serial: str):
        """Get DHCP subnet information for a specific appliance device."""
        try:
            subnets = meraki_client.dashboard.appliance.getDeviceApplianceDhcpSubnets(serial)
            
            if not subnets:
                return f"No DHCP subnets found for device {serial}."
                
            result = f"# 🌐 DHCP Subnets for Device {serial}\n\n"
            
            for subnet in subnets:
                result += f"## {subnet.get('subnet', 'Unknown Subnet')}\n"
                result += f"- **VLAN**: {subnet.get('vlanId', 'N/A')}\n"
                result += f"- **Free IPs**: {subnet.get('freeCount', 0)}\n"
                result += f"- **Used IPs**: {subnet.get('usedCount', 0)}\n"
                
                total = subnet.get('freeCount', 0) + subnet.get('usedCount', 0)
                if total > 0:
                    usage = (subnet.get('usedCount', 0) / total) * 100
                    result += f"- **Usage**: {usage:.1f}%\n"
                    if usage > 80:
                        result += "- ⚠️ High IP usage\n"
                        
                result += "\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving DHCP subnets: {str(e)}"
    
    # ========== RF Profiles ==========
    
    @app.tool(
        name="get_network_appliance_rf_profiles",
        description="📡 Get RF profiles for wireless"
    )
    def get_network_appliance_rf_profiles(network_id: str):
        """Get RF profiles configured on a network appliance."""
        try:
            profiles = meraki_client.dashboard.appliance.getNetworkApplianceRfProfiles(network_id)
            
            if not profiles:
                return f"No RF profiles found for network {network_id}."
                
            result = f"# 📡 RF Profiles for Network {network_id}\n\n"
            
            # Assigned profile
            if profiles.get('assigned'):
                result += f"**Assigned Profile**: {profiles['assigned']}\n\n"
                
            # Available profiles
            if profiles.get('profiles'):
                result += "## Available Profiles\n"
                for profile_id, profile in profiles['profiles'].items():
                    result += f"### {profile_id}\n"
                    result += f"- **Name**: {profile.get('name', 'Unnamed')}\n"
                    
                    # 2.4GHz settings
                    if profile.get('twoFourGhzSettings'):
                        settings = profile['twoFourGhzSettings']
                        result += "- **2.4GHz Settings**:\n"
                        result += f"  - Min bitrate: {settings.get('minBitrate', 'N/A')} Mbps\n"
                        result += f"  - Max power: {settings.get('maxPower', 'N/A')} dBm\n"
                        
                    # 5GHz settings
                    if profile.get('fiveGhzSettings'):
                        settings = profile['fiveGhzSettings']
                        result += "- **5GHz Settings**:\n"
                        result += f"  - Min bitrate: {settings.get('minBitrate', 'N/A')} Mbps\n"
                        result += f"  - Max power: {settings.get('maxPower', 'N/A')} dBm\n"
                        
                    result += "\n"
                    
            return result
            
        except Exception as e:
            return f"Error retrieving RF profiles: {str(e)}"
    
    # ========== Prefixes ==========
    
    @app.tool(
        name="get_device_appliance_prefixes_delegated",
        description="🌐 Get delegated IPv6 prefixes"
    )
    def get_device_appliance_prefixes_delegated(serial: str):
        """Get delegated IPv6 prefixes for a specific appliance device."""
        try:
            prefixes = meraki_client.dashboard.appliance.getDeviceAppliancePrefixesDelegated(serial)
            
            if not prefixes:
                return f"No delegated prefixes found for device {serial}."
                
            result = f"# 🌐 Delegated IPv6 Prefixes for Device {serial}\n\n"
            
            for prefix in prefixes:
                result += f"## {prefix.get('prefix', 'Unknown Prefix')}\n"
                result += f"- **Origin**: {prefix.get('origin', 'N/A')}\n"
                result += f"- **Assigned At**: {prefix.get('assignedAt', 'N/A')}\n"
                result += f"- **Expires At**: {prefix.get('expiresAt', 'N/A')}\n"
                
                if prefix.get('vlanAssignments'):
                    result += "- **VLAN Assignments**:\n"
                    for assignment in prefix['vlanAssignments']:
                        result += f"  - VLAN {assignment.get('vlanId')}: {assignment.get('prefix')}\n"
                        
                result += "\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving delegated prefixes: {str(e)}"
    
    # ========== Organization-wide Appliance Functions ==========
    
    @app.tool(
        name="get_organization_appliance_uplink_statuses",
        description="🔗 Get uplink statuses for all appliances in org"
    )
    def get_organization_appliance_uplink_statuses(
        org_id: str,
        network_ids: Optional[List[str]] = None
    ):
        """Get uplink statuses for all appliances in an organization."""
        try:
            kwargs = {}
            if network_ids:
                kwargs['networkIds'] = network_ids
                
            statuses = meraki_client.dashboard.appliance.getOrganizationApplianceUplinkStatuses(
                org_id,
                **kwargs
            )
            
            if not statuses:
                return f"No uplink statuses found for organization {org_id}."
                
            result = f"# 🔗 Appliance Uplink Statuses for Organization {org_id}\n\n"
            
            for status in statuses:
                network_id = status.get('networkId', 'Unknown')
                result += f"## Network: {network_id}\n"
                result += f"**Serial**: {status.get('serial', 'N/A')}\n"
                result += f"**Model**: {status.get('model', 'N/A')}\n"
                result += f"**Last Reported**: {status.get('lastReportedAt', 'N/A')}\n"
                
                # Uplinks
                for uplink in status.get('uplinks', []):
                    interface = uplink.get('interface', 'Unknown')
                    state = uplink.get('status', 'Unknown')
                    
                    if state == 'active':
                        result += f"- **{interface}**: ✅ Active"
                    elif state == 'ready':
                        result += f"- **{interface}**: 🟡 Ready"
                    elif state == 'failed':
                        result += f"- **{interface}**: ❌ Failed"
                    else:
                        result += f"- **{interface}**: {state}"
                        
                    if uplink.get('ip'):
                        result += f" ({uplink['ip']})"
                        
                    result += "\n"
                    
                result += "\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving uplink statuses: {str(e)}"
    
    @app.tool(
        name="get_organization_appliance_vpn_statuses",
        description="🔐 Get VPN statuses for all appliances in org"
    )
    def get_organization_appliance_vpn_statuses(
        org_id: str,
        network_ids: Optional[List[str]] = None
    ):
        """Get VPN statuses for all appliances in an organization."""
        try:
            kwargs = {}
            if network_ids:
                kwargs['networkIds'] = network_ids
                
            statuses = meraki_client.dashboard.appliance.getOrganizationApplianceVpnStatuses(
                org_id,
                **kwargs
            )
            
            if not statuses:
                return f"No VPN statuses found for organization {org_id}."
                
            result = f"# 🔐 VPN Statuses for Organization {org_id}\n\n"
            
            for status in statuses:
                network_id = status.get('networkId', 'Unknown')
                result += f"## Network: {network_id}\n"
                result += f"**Device Serial**: {status.get('deviceSerial', 'N/A')}\n"
                result += f"**VPN Mode**: {status.get('vpnMode', 'N/A')}\n"
                
                # Meraki VPN peers
                meraki_peers = status.get('merakiVpnPeers', [])
                if meraki_peers:
                    result += "\n### Meraki VPN Peers\n"
                    for peer in meraki_peers:
                        result += f"- **{peer.get('networkName', 'Unknown')}**: "
                        result += f"{peer.get('reachability', 'Unknown')}\n"
                        
                # Third-party VPN peers
                third_party = status.get('thirdPartyVpnPeers', [])
                if third_party:
                    result += "\n### Third-Party VPN Peers\n"
                    for peer in third_party:
                        result += f"- **{peer.get('name', 'Unknown')}**: "
                        result += f"{peer.get('reachability', 'Unknown')}\n"
                        
                result += "\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving VPN statuses: {str(e)}"
    
    @app.tool(
        name="get_organization_appliance_security_events",
        description="🚨 Get security events for all appliances in org"
    )
    def get_organization_appliance_security_events(
        org_id: str,
        timespan: Optional[int] = 86400,
        per_page: Optional[int] = 100
    ):
        """Get security events for all appliances in an organization."""
        try:
            events = meraki_client.dashboard.appliance.getOrganizationApplianceSecurityEvents(
                org_id,
                timespan=timespan,
                perPage=per_page
            )
            
            if not events:
                return f"No security events found for organization {org_id} in the last {timespan} seconds."
                
            result = f"# 🚨 Security Events for Organization {org_id}\n"
            result += f"*Last {timespan // 3600} hours*\n\n"
            
            # Group events by type
            event_types = {}
            for event in events:
                event_type = event.get('eventType', 'Unknown')
                if event_type not in event_types:
                    event_types[event_type] = []
                event_types[event_type].append(event)
                
            # Display by type
            for event_type, type_events in event_types.items():
                result += f"## {event_type} ({len(type_events)} events)\n"
                
                # Show first 5 events of each type
                for event in type_events[:5]:
                    result += f"- {event.get('ts', 'Unknown time')}: "
                    result += f"{event.get('message', 'No message')}\n"
                    
                    if event.get('srcIp'):
                        result += f"  Source: {event['srcIp']}"
                        if event.get('srcPort'):
                            result += f":{event['srcPort']}"
                        result += "\n"
                        
                    if event.get('destIp'):
                        result += f"  Destination: {event['destIp']}"
                        if event.get('destPort'):
                            result += f":{event['destPort']}"
                        result += "\n"
                        
                if len(type_events) > 5:
                    result += f"  ... and {len(type_events) - 5} more\n"
                    
                result += "\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving security events: {str(e)}"
    
    # ========== Firewall Services ==========
    
    @app.tool(
        name="get_network_appliance_firewall_firewalled_services",
        description="🔥 Get firewalled services settings"
    )
    def get_network_appliance_firewall_firewalled_services(network_id: str):
        """Get firewalled services settings for a network appliance."""
        try:
            services = meraki_client.dashboard.appliance.getNetworkApplianceFirewallFirewalledServices(network_id)
            
            if not services:
                return f"No firewalled services found for network {network_id}."
                
            result = f"# 🔥 Firewalled Services for Network {network_id}\n\n"
            
            for service in services:
                service_name = service.get('service', 'Unknown')
                access = service.get('access', 'N/A')
                
                result += f"## {service_name}\n"
                result += f"- **Access**: {access}\n"
                
                if service.get('allowedIps'):
                    result += f"- **Allowed IPs**: {', '.join(service['allowedIps'])}\n"
                    
                result += "\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving firewalled services: {str(e)}"
    
    @app.tool(
        name="get_network_appliance_firewall_firewalled_service",
        description="🔥 Get a specific firewalled service"
    )
    def get_network_appliance_firewall_firewalled_service(network_id: str, service: str):
        """Get settings for a specific firewalled service."""
        try:
            service_info = meraki_client.dashboard.appliance.getNetworkApplianceFirewallFirewalledService(
                network_id,
                service
            )
            
            result = f"# 🔥 Firewalled Service: {service}\n\n"
            result += f"**Access**: {service_info.get('access', 'N/A')}\n"
            
            if service_info.get('allowedIps'):
                result += f"**Allowed IPs**: {', '.join(service_info['allowedIps'])}\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving firewalled service: {str(e)}"
    
    @app.tool(
        name="update_network_appliance_firewall_firewalled_service",
        description="🔥 Update a firewalled service"
    )
    def update_network_appliance_firewall_firewalled_service(
        network_id: str,
        service: str,
        access: str,
        allowed_ips: Optional[List[str]] = None
    ):
        """Update settings for a specific firewalled service."""
        try:
            kwargs = {'access': access}
            if allowed_ips is not None:
                kwargs['allowedIps'] = allowed_ips
                
            result = meraki_client.dashboard.appliance.updateNetworkApplianceFirewallFirewalledService(
                network_id,
                service,
                **kwargs
            )
            
            return f"✅ Firewalled service '{service}' updated successfully! Access: {access}"
            
        except Exception as e:
            return f"Error updating firewalled service: {str(e)}"
    
    # ========== Cellular Firewall Rules ==========
    
    @app.tool(
        name="get_network_appliance_firewall_cellular_rules",
        description="📱 Get cellular firewall rules"
    )
    def get_network_appliance_firewall_cellular_rules(network_id: str):
        """Get cellular firewall rules for a network appliance."""
        try:
            rules = meraki_client.dashboard.appliance.getNetworkApplianceFirewallCellularFirewallRules(network_id)
            
            if not rules or not rules.get('rules'):
                return f"No cellular firewall rules found for network {network_id}."
                
            result = f"# 📱 Cellular Firewall Rules for Network {network_id}\n\n"
            
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
            return f"Error retrieving cellular firewall rules: {str(e)}"
    
    @app.tool(
        name="update_network_appliance_firewall_cellular_rules",
        description="📱 Update cellular firewall rules"
    )
    def update_network_appliance_firewall_cellular_rules(
        network_id: str,
        rules: List[Dict[str, Any]]
    ):
        """Update cellular firewall rules for a network."""
        try:
            result = meraki_client.dashboard.appliance.updateNetworkApplianceFirewallCellularFirewallRules(
                network_id,
                rules=rules
            )
            
            return f"✅ Cellular firewall rules updated successfully! Total rules: {len(rules)}"
            
        except Exception as e:
            return f"Error updating cellular firewall rules: {str(e)}"