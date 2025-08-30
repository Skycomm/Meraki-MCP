"""
Appliance Firewall tools for Cisco Meraki MCP server.

This module provides firewall management tools for MX appliances.
"""

from typing import Optional, Dict, Any, List
from datetime import datetime
import json

# Global references to be set by register function
app = None
meraki_client = None

def register_appliance_firewall_tools(mcp_app, meraki):
    """
    Register appliance firewall tools with the MCP server.
    
    Args:
        mcp_app: MCP server instance
        meraki: Meraki client instance
    """
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    
    # ==================== INBOUND FIREWALL RULES ====================
    
    @app.tool(
        name="get_network_appliance_firewall_inbound_firewall_rules",
        description="🔥🔒 Get inbound firewall rules (L3 rules)"
    )
    def get_network_appliance_firewall_inbound_firewall_rules(
        network_id: str
    ):
        """Get inbound firewall rules."""
        try:
            result = meraki_client.dashboard.appliance.getNetworkApplianceFirewallInboundFirewallRules(network_id)
            
            response = f"# 🔒 Inbound Firewall Rules\n\n"
            
            if result and 'rules' in result:
                rules = result['rules']
                response += f"**Total Rules**: {len(rules)}\n"
                response += f"**Syslog Enabled**: {'✅' if result.get('syslogEnabled') else '❌'}\n\n"
                
                for i, rule in enumerate(rules, 1):
                    response += f"## Rule {i}: {rule.get('comment', 'No comment')}\n"
                    response += f"- Policy: {rule.get('policy', 'N/A')}\n"
                    response += f"- Protocol: {rule.get('protocol', 'any')}\n"
                    response += f"- Source: {rule.get('srcCidr', 'any')}\n"
                    
                    if rule.get('srcPort'):
                        response += f"- Source Port: {rule.get('srcPort')}\n"
                    
                    response += f"- Destination: {rule.get('destCidr', 'any')}\n"
                    
                    if rule.get('destPort'):
                        response += f"- Destination Port: {rule.get('destPort')}\n"
                    
                    response += "\n"
            else:
                response += "*No inbound firewall rules configured*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting inbound firewall rules: {str(e)}"
    
    @app.tool(
        name="update_network_appliance_firewall_inbound_firewall_rules",
        description="🔥🔒 Update inbound firewall rules (rules: JSON array, syslog_enabled: bool)"
    )
    def update_network_appliance_firewall_inbound_firewall_rules(
        network_id: str,
        rules: str,
        syslog_enabled: Optional[bool] = False
    ):
        """
        Update inbound firewall rules.
        
        Args:
            network_id: Network ID
            rules: JSON array of rule objects
            syslog_enabled: Enable syslog for denied connections
        """
        try:
            try:
                rules_list = json.loads(rules)
            except:
                return "❌ Invalid JSON format for rules parameter"
            
            kwargs = {
                'rules': rules_list,
                'syslogEnabled': syslog_enabled
            }
            
            result = meraki_client.dashboard.appliance.updateNetworkApplianceFirewallInboundFirewallRules(
                network_id, **kwargs
            )
            
            response = f"# ✅ Inbound Firewall Rules Updated\n\n"
            response += f"**Rules Count**: {len(rules_list)}\n"
            response += f"**Syslog**: {'Enabled' if syslog_enabled else 'Disabled'}\n"
            
            return response
        except Exception as e:
            return f"❌ Error updating inbound firewall rules: {str(e)}"
    
    # ==================== INBOUND CELLULAR FIREWALL RULES ====================
    
    @app.tool(
        name="get_network_appliance_firewall_inbound_cellular_rules",
        description="🔥📱 Get inbound cellular firewall rules"
    )
    def get_network_appliance_firewall_inbound_cellular_rules(
        network_id: str
    ):
        """Get inbound cellular firewall rules."""
        try:
            result = meraki_client.dashboard.appliance.getNetworkApplianceFirewallInboundCellularFirewallRules(network_id)
            
            response = f"# 📱 Inbound Cellular Firewall Rules\n\n"
            
            if result and 'rules' in result:
                rules = result['rules']
                response += f"**Total Rules**: {len(rules)}\n\n"
                
                for i, rule in enumerate(rules, 1):
                    response += f"## Rule {i}: {rule.get('comment', 'No comment')}\n"
                    response += f"- Policy: {rule.get('policy', 'N/A')}\n"
                    response += f"- Protocol: {rule.get('protocol', 'any')}\n"
                    response += f"- Source: {rule.get('srcCidr', 'any')}\n"
                    response += f"- Source Port: {rule.get('srcPort', 'any')}\n"
                    response += f"- Destination: {rule.get('destCidr', 'any')}\n"
                    response += f"- Destination Port: {rule.get('destPort', 'any')}\n\n"
            else:
                response += "*No cellular firewall rules configured*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting cellular firewall rules: {str(e)}"
    
    @app.tool(
        name="update_network_appliance_firewall_inbound_cellular_rules",
        description="🔥📱 Update inbound cellular firewall rules (rules: JSON array)"
    )
    def update_network_appliance_firewall_inbound_cellular_rules(
        network_id: str,
        rules: str
    ):
        """Update inbound cellular firewall rules."""
        try:
            try:
                rules_list = json.loads(rules)
            except:
                return "❌ Invalid JSON format for rules parameter"
            
            result = meraki_client.dashboard.appliance.updateNetworkApplianceFirewallInboundCellularFirewallRules(
                network_id, rules=rules_list
            )
            
            response = f"# ✅ Cellular Firewall Rules Updated\n\n"
            response += f"**Rules Count**: {len(rules_list)}\n"
            
            return response
        except Exception as e:
            return f"❌ Error updating cellular firewall rules: {str(e)}"
    
    # ==================== L3 FIREWALL RULES ====================
    
    @app.tool(
        name="get_network_appliance_firewall_l3_firewall_rules",
        description="🔥🌐 Get L3 outbound firewall rules"
    )
    def get_network_appliance_firewall_l3_firewall_rules(
        network_id: str
    ):
        """Get L3 firewall rules."""
        try:
            result = meraki_client.dashboard.appliance.getNetworkApplianceFirewallL3FirewallRules(network_id)
            
            response = f"# 🌐 L3 Firewall Rules (Outbound)\n\n"
            
            if result and 'rules' in result:
                rules = result['rules']
                response += f"**Total Rules**: {len(rules)}\n\n"
                
                for i, rule in enumerate(rules, 1):
                    response += f"## Rule {i}: {rule.get('comment', 'No comment')}\n"
                    response += f"- Policy: {rule.get('policy', 'N/A')}\n"
                    response += f"- Protocol: {rule.get('protocol', 'any')}\n"
                    response += f"- Source: {rule.get('srcCidr', 'any')}\n"
                    response += f"- Source Port: {rule.get('srcPort', 'any')}\n"
                    response += f"- Destination: {rule.get('destCidr', 'any')}\n"
                    response += f"- Destination Port: {rule.get('destPort', 'any')}\n"
                    response += f"- Syslog: {'✅' if rule.get('syslogEnabled') else '❌'}\n\n"
            else:
                response += "*Default allow all rule in effect*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting L3 firewall rules: {str(e)}"
    
    @app.tool(
        name="update_network_appliance_firewall_l3_firewall_rules",
        description="🔥🌐 Update L3 outbound firewall rules (rules: JSON array)"
    )
    def update_network_appliance_firewall_l3_firewall_rules(
        network_id: str,
        rules: str
    ):
        """Update L3 firewall rules."""
        try:
            try:
                rules_list = json.loads(rules)
            except:
                return "❌ Invalid JSON format for rules parameter"
            
            result = meraki_client.dashboard.appliance.updateNetworkApplianceFirewallL3FirewallRules(
                network_id, rules=rules_list
            )
            
            response = f"# ✅ L3 Firewall Rules Updated\n\n"
            response += f"**Rules Count**: {len(rules_list)}\n"
            
            return response
        except Exception as e:
            return f"❌ Error updating L3 firewall rules: {str(e)}"
    
    # ==================== L7 FIREWALL RULES ====================
    
    @app.tool(
        name="get_network_appliance_firewall_l7_firewall_rules",
        description="🔥🔍 Get L7 application firewall rules"
    )
    def get_network_appliance_firewall_l7_firewall_rules(
        network_id: str
    ):
        """Get L7 firewall rules."""
        try:
            result = meraki_client.dashboard.appliance.getNetworkApplianceFirewallL7FirewallRules(network_id)
            
            response = f"# 🔍 L7 Application Firewall Rules\n\n"
            
            if result and 'rules' in result:
                rules = result['rules']
                response += f"**Total Rules**: {len(rules)}\n\n"
                
                for i, rule in enumerate(rules, 1):
                    response += f"## Rule {i}\n"
                    response += f"- Policy: {rule.get('policy', 'N/A')}\n"
                    response += f"- Type: {rule.get('type', 'N/A')}\n"
                    
                    if rule.get('value'):
                        if isinstance(rule['value'], dict):
                            response += f"- Application: {rule['value'].get('name', 'N/A')}\n"
                            response += f"  ID: {rule['value'].get('id', 'N/A')}\n"
                        else:
                            response += f"- Value: {rule.get('value')}\n"
                    
                    response += "\n"
            else:
                response += "*No L7 firewall rules configured*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting L7 firewall rules: {str(e)}"
    
    @app.tool(
        name="update_network_appliance_firewall_l7_firewall_rules",
        description="🔥🔍 Update L7 application firewall rules (rules: JSON array)"
    )
    def update_network_appliance_firewall_l7_firewall_rules(
        network_id: str,
        rules: str
    ):
        """Update L7 firewall rules."""
        try:
            try:
                rules_list = json.loads(rules)
            except:
                return "❌ Invalid JSON format for rules parameter"
            
            result = meraki_client.dashboard.appliance.updateNetworkApplianceFirewallL7FirewallRules(
                network_id, rules=rules_list
            )
            
            response = f"# ✅ L7 Firewall Rules Updated\n\n"
            response += f"**Rules Count**: {len(rules_list)}\n"
            
            return response
        except Exception as e:
            return f"❌ Error updating L7 firewall rules: {str(e)}"
    
    @app.tool(
        name="get_network_appliance_firewall_l7_app_categories",
        description="🔥📋 Get available L7 application categories"
    )
    def get_network_appliance_firewall_l7_app_categories(
        network_id: str
    ):
        """Get L7 application categories."""
        try:
            result = meraki_client.dashboard.appliance.getNetworkApplianceFirewallL7FirewallRulesApplicationCategories(
                network_id
            )
            
            response = f"# 📋 L7 Application Categories\n\n"
            
            if result and 'applicationCategories' in result:
                categories = result['applicationCategories']
                response += f"**Total Categories**: {len(categories)}\n\n"
                
                # Group by category type
                by_type = {}
                for cat in categories:
                    cat_name = cat.get('name', 'Unknown')
                    cat_id = cat.get('id', 'N/A')
                    
                    # Extract category type from name
                    if '.' in cat_name:
                        cat_type = cat_name.split('.')[0]
                    else:
                        cat_type = 'Other'
                    
                    if cat_type not in by_type:
                        by_type[cat_type] = []
                    by_type[cat_type].append((cat_name, cat_id))
                
                for cat_type, items in sorted(by_type.items()):
                    response += f"## {cat_type}\n"
                    for name, cat_id in items[:5]:
                        response += f"- {name} ({cat_id})\n"
                    if len(items) > 5:
                        response += f"  ...and {len(items)-5} more\n"
                    response += "\n"
            else:
                response += "*No application categories available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting L7 categories: {str(e)}"
    
    # ==================== FIREWALLED SERVICES ====================
    
    @app.tool(
        name="get_network_appliance_firewall_firewalled_services",
        description="🔥🛡️ Get all firewalled services settings"
    )
    def get_network_appliance_firewall_firewalled_services(
        network_id: str
    ):
        """Get firewalled services."""
        try:
            result = meraki_client.dashboard.appliance.getNetworkApplianceFirewallFirewalledServices(network_id)
            
            response = f"# 🛡️ Firewalled Services\n\n"
            
            if result and isinstance(result, list):
                response += f"**Total Services**: {len(result)}\n\n"
                
                for service in result:
                    response += f"## {service.get('service', 'Unknown')}\n"
                    response += f"- Access: {service.get('access', 'N/A')}\n"
                    
                    allowed = service.get('allowedIps', [])
                    if allowed:
                        response += f"- Allowed IPs: {', '.join(allowed)}\n"
                    
                    response += "\n"
            else:
                response += "*No firewalled services configured*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting firewalled services: {str(e)}"
    
    @app.tool(
        name="get_network_appliance_firewall_firewalled_service",
        description="🔥🛡️ Get specific firewalled service (ICMP, SNMP, web)"
    )
    def get_network_appliance_firewall_firewalled_service(
        network_id: str,
        service: str
    ):
        """Get specific firewalled service."""
        try:
            result = meraki_client.dashboard.appliance.getNetworkApplianceFirewallFirewalledService(
                network_id, service
            )
            
            response = f"# 🛡️ Firewalled Service: {service.upper()}\n\n"
            response += f"**Access**: {result.get('access', 'N/A')}\n"
            
            allowed = result.get('allowedIps', [])
            if allowed:
                response += f"**Allowed IPs**:\n"
                for ip in allowed:
                    response += f"- {ip}\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting firewalled service: {str(e)}"
    
    @app.tool(
        name="update_network_appliance_firewall_firewalled_service",
        description="🔥🛡️ Update firewalled service (service: ICMP/SNMP/web, access: blocked/restricted/unrestricted)"
    )
    def update_network_appliance_firewall_firewalled_service(
        network_id: str,
        service: str,
        access: str,
        allowed_ips: Optional[str] = None
    ):
        """
        Update firewalled service.
        
        Args:
            network_id: Network ID
            service: Service name (ICMP, SNMP, web)
            access: Access policy (blocked, restricted, unrestricted)
            allowed_ips: Comma-separated IPs for restricted access
        """
        try:
            kwargs = {'access': access}
            
            if access == 'restricted' and allowed_ips:
                kwargs['allowedIps'] = [ip.strip() for ip in allowed_ips.split(',')]
            
            result = meraki_client.dashboard.appliance.updateNetworkApplianceFirewallFirewalledService(
                network_id, service, **kwargs
            )
            
            response = f"# ✅ Firewalled Service Updated\n\n"
            response += f"**Service**: {service.upper()}\n"
            response += f"**Access**: {access}\n"
            if allowed_ips:
                response += f"**Allowed IPs**: {allowed_ips}\n"
            
            return response
        except Exception as e:
            return f"❌ Error updating firewalled service: {str(e)}"
    
    # ==================== PORT FORWARDING ====================
    
    @app.tool(
        name="get_network_appliance_firewall_port_forwarding",
        description="🔥🔀 Get port forwarding rules"
    )
    def get_network_appliance_firewall_port_forwarding(
        network_id: str
    ):
        """Get port forwarding rules."""
        try:
            result = meraki_client.dashboard.appliance.getNetworkApplianceFirewallPortForwardingRules(network_id)
            
            response = f"# 🔀 Port Forwarding Rules\n\n"
            
            if result and 'rules' in result:
                rules = result['rules']
                response += f"**Total Rules**: {len(rules)}\n\n"
                
                for i, rule in enumerate(rules, 1):
                    response += f"## Rule {i}: {rule.get('name', 'Unnamed')}\n"
                    response += f"- LAN IP: {rule.get('lanIp', 'N/A')}\n"
                    response += f"- Public Port: {rule.get('publicPort', 'N/A')}\n"
                    response += f"- Local Port: {rule.get('localPort', 'N/A')}\n"
                    response += f"- Protocol: {rule.get('protocol', 'tcp')}\n"
                    
                    allowed = rule.get('allowedIps', [])
                    if allowed:
                        response += f"- Allowed IPs: {', '.join(allowed)}\n"
                    else:
                        response += f"- Allowed IPs: Any\n"
                    
                    response += f"- Uplink: {rule.get('uplink', 'both')}\n\n"
            else:
                response += "*No port forwarding rules configured*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting port forwarding rules: {str(e)}"
    
    @app.tool(
        name="update_network_appliance_firewall_port_forwarding",
        description="🔥🔀 Update port forwarding rules (rules: JSON array)"
    )
    def update_network_appliance_firewall_port_forwarding(
        network_id: str,
        rules: str
    ):
        """Update port forwarding rules."""
        try:
            try:
                rules_list = json.loads(rules)
            except:
                return "❌ Invalid JSON format for rules parameter"
            
            result = meraki_client.dashboard.appliance.updateNetworkApplianceFirewallPortForwardingRules(
                network_id, rules=rules_list
            )
            
            response = f"# ✅ Port Forwarding Rules Updated\n\n"
            response += f"**Rules Count**: {len(rules_list)}\n"
            
            return response
        except Exception as e:
            return f"❌ Error updating port forwarding rules: {str(e)}"
    
    # ==================== ONE-TO-ONE NAT ====================
    
    @app.tool(
        name="get_network_appliance_firewall_one_to_one_nat",
        description="🔥🔄 Get one-to-one NAT rules"
    )
    def get_network_appliance_firewall_one_to_one_nat(
        network_id: str
    ):
        """Get one-to-one NAT rules."""
        try:
            result = meraki_client.dashboard.appliance.getNetworkApplianceFirewallOneToOneNatRules(network_id)
            
            response = f"# 🔄 One-to-One NAT Rules\n\n"
            
            if result and 'rules' in result:
                rules = result['rules']
                response += f"**Total Rules**: {len(rules)}\n\n"
                
                for i, rule in enumerate(rules, 1):
                    response += f"## Rule {i}: {rule.get('name', 'Unnamed')}\n"
                    response += f"- Public IP: {rule.get('publicIp', 'N/A')}\n"
                    response += f"- LAN IP: {rule.get('lanIp', 'N/A')}\n"
                    response += f"- Uplink: {rule.get('uplink', 'both')}\n"
                    
                    allowed = rule.get('allowedInboundPorts', [])
                    if allowed:
                        response += f"- Allowed Inbound: {allowed}\n"
                    
                    response += "\n"
            else:
                response += "*No one-to-one NAT rules configured*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting one-to-one NAT rules: {str(e)}"
    
    @app.tool(
        name="update_network_appliance_firewall_one_to_one_nat",
        description="🔥🔄 Update one-to-one NAT rules (rules: JSON array)"
    )
    def update_network_appliance_firewall_one_to_one_nat(
        network_id: str,
        rules: str
    ):
        """Update one-to-one NAT rules."""
        try:
            try:
                rules_list = json.loads(rules)
            except:
                return "❌ Invalid JSON format for rules parameter"
            
            result = meraki_client.dashboard.appliance.updateNetworkApplianceFirewallOneToOneNatRules(
                network_id, rules=rules_list
            )
            
            response = f"# ✅ One-to-One NAT Rules Updated\n\n"
            response += f"**Rules Count**: {len(rules_list)}\n"
            
            return response
        except Exception as e:
            return f"❌ Error updating one-to-one NAT rules: {str(e)}"
    
    # ==================== ONE-TO-MANY NAT ====================
    
    @app.tool(
        name="get_network_appliance_firewall_one_to_many_nat",
        description="🔥🔄 Get one-to-many NAT rules (outbound NAT)"
    )
    def get_network_appliance_firewall_one_to_many_nat(
        network_id: str
    ):
        """Get one-to-many NAT rules."""
        try:
            result = meraki_client.dashboard.appliance.getNetworkApplianceFirewallOneToManyNatRules(network_id)
            
            response = f"# 🔄 One-to-Many NAT Rules (Outbound)\n\n"
            
            if result and 'rules' in result:
                rules = result['rules']
                response += f"**Total Rules**: {len(rules)}\n\n"
                
                for i, rule in enumerate(rules, 1):
                    response += f"## Rule {i}\n"
                    response += f"- Public IP: {rule.get('publicIp', 'N/A')}\n"
                    response += f"- Uplink: {rule.get('uplink', 'both')}\n"
                    
                    port_rules = rule.get('portRules', [])
                    if port_rules:
                        response += f"- Port Rules:\n"
                        for pr in port_rules:
                            response += f"  - {pr.get('name', 'Unnamed')}: "
                            response += f"{pr.get('protocol', 'tcp')} "
                            response += f"port {pr.get('publicPort', 'N/A')} → "
                            response += f"{pr.get('localIp', 'N/A')}:{pr.get('localPort', 'N/A')}\n"
                    
                    response += "\n"
            else:
                response += "*No one-to-many NAT rules configured*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting one-to-many NAT rules: {str(e)}"
    
    @app.tool(
        name="update_network_appliance_firewall_one_to_many_nat",
        description="🔥🔄 Update one-to-many NAT rules (rules: JSON array)"
    )
    def update_network_appliance_firewall_one_to_many_nat(
        network_id: str,
        rules: str
    ):
        """Update one-to-many NAT rules."""
        try:
            try:
                rules_list = json.loads(rules)
            except:
                return "❌ Invalid JSON format for rules parameter"
            
            result = meraki_client.dashboard.appliance.updateNetworkApplianceFirewallOneToManyNatRules(
                network_id, rules=rules_list
            )
            
            response = f"# ✅ One-to-Many NAT Rules Updated\n\n"
            response += f"**Rules Count**: {len(rules_list)}\n"
            
            return response
        except Exception as e:
            return f"❌ Error updating one-to-many NAT rules: {str(e)}"
    
    # ==================== FIREWALL SETTINGS ====================
    
    @app.tool(
        name="get_network_appliance_firewall_settings",
        description="🔥⚙️ Get firewall spoofing protection settings"
    )
    def get_network_appliance_firewall_settings(
        network_id: str
    ):
        """Get firewall settings."""
        try:
            result = meraki_client.dashboard.appliance.getNetworkApplianceFirewallSettings(network_id)
            
            response = f"# ⚙️ Firewall Settings\n\n"
            
            # Spoofing protection
            spoofing = result.get('spoofingProtection', {})
            if spoofing:
                response += "## Spoofing Protection\n"
                
                ip_source_guard = spoofing.get('ipSourceGuard', {})
                response += f"- IP Source Guard: {ip_source_guard.get('mode', 'N/A')}\n\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting firewall settings: {str(e)}"
    
    @app.tool(
        name="update_network_appliance_firewall_settings",
        description="🔥⚙️ Update firewall settings (ip_source_guard: none/dhcp)"
    )
    def update_network_appliance_firewall_settings(
        network_id: str,
        ip_source_guard_mode: Optional[str] = None
    ):
        """
        Update firewall settings.
        
        Args:
            network_id: Network ID
            ip_source_guard_mode: IP source guard mode ('none' or 'dhcp')
        """
        try:
            kwargs = {}
            
            if ip_source_guard_mode:
                kwargs['spoofingProtection'] = {
                    'ipSourceGuard': {
                        'mode': ip_source_guard_mode
                    }
                }
            
            result = meraki_client.dashboard.appliance.updateNetworkApplianceFirewallSettings(
                network_id, **kwargs
            )
            
            response = f"# ✅ Firewall Settings Updated\n\n"
            if ip_source_guard_mode:
                response += f"**IP Source Guard**: {ip_source_guard_mode}\n"
            
            return response
        except Exception as e:
            return f"❌ Error updating firewall settings: {str(e)}"