"""
Firewall Management Tools for Cisco Meraki MCP Server
Manage L3/L7 firewall rules, port forwarding, and security policies
"""

from mcp.server import FastMCP
from typing import Optional, Dict, Any, List
import json
from meraki_client import MerakiClient
from utils.helpers import format_error_message
from contextlib import contextmanager

# This will be set by register function
mcp_app = None
meraki = None

def format_error(operation: str, error: Exception) -> str:
    """Format error message with operation context."""
    return f"❌ Failed to {operation}: {format_error_message(error)}"

@contextmanager
def safe_api_call(operation: str):
    """Context manager for safe API calls with consistent error handling."""
    try:
        yield
    except Exception as e:
        raise Exception(f"Failed to {operation}: {str(e)}")


def get_firewall_l3_rules(network_id: str) -> str:
    """
    🔥 Get Layer 3 firewall rules for a network.
    
    Shows inbound/outbound traffic rules based on IP addresses and ports.
    
    Args:
        network_id: Network ID to query
        
    Returns:
        Current L3 firewall rules
    """
    try:
        with safe_api_call("get L3 firewall rules"):
            rules = meraki.dashboard.appliance.getNetworkApplianceFirewallL3FirewallRules(network_id)
            
            output = ["🔥 Layer 3 Firewall Rules", "=" * 50, ""]
            
            if 'rules' in rules and rules['rules']:
                for i, rule in enumerate(rules['rules'], 1):
                    output.append(f"{i}. {rule.get('comment', 'Unnamed Rule')}")
                    output.append(f"   Policy: {'✅ Allow' if rule.get('policy') == 'allow' else '❌ Deny'}")
                    output.append(f"   Protocol: {rule.get('protocol', 'any').upper()}")
                    
                    # Source
                    src_port = rule.get('srcPort', 'Any')
                    src_cidr = rule.get('srcCidr', 'Any')
                    output.append(f"   Source: {src_cidr}:{src_port}")
                    
                    # Destination  
                    dest_port = rule.get('destPort', 'Any')
                    dest_cidr = rule.get('destCidr', 'Any')
                    output.append(f"   Destination: {dest_cidr}:{dest_port}")
                    
                    # Syslog
                    if rule.get('syslogEnabled'):
                        output.append("   📝 Syslog: Enabled")
                    
                    output.append("")
            
            # Default rule
            output.append("Default Rule:")
            output.append(f"   Policy: {rules.get('syslogDefaultRule', 'Not configured')}")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("get L3 firewall rules", e)


def update_firewall_l3_rules(
    network_id: str,
    rules: str,
    syslog_default_rule: Optional[bool] = None
) -> str:
    """
    🛡️ Update Layer 3 firewall rules for a network.
    
    Configure IP-based traffic filtering.
    
    Args:
        network_id: Network ID to update
        rules: JSON array of firewall rules
        syslog_default_rule: Enable syslog for default rule
        
    Examples:
        Block traffic from specific IP:
        rules='[{
            "comment": "Block malicious IP",
            "policy": "deny",
            "protocol": "any",
            "srcCidr": "192.168.100.50/32",
            "destCidr": "Any"
        }]'
        
        Allow HTTPS from subnet:
        rules='[{
            "comment": "Allow HTTPS from office",
            "policy": "allow", 
            "protocol": "tcp",
            "srcCidr": "10.0.0.0/24",
            "destPort": "443",
            "destCidr": "Any"
        }]'
        
        Block outbound to specific port:
        rules='[{
            "comment": "Block Telnet",
            "policy": "deny",
            "protocol": "tcp",
            "srcCidr": "Any",
            "destPort": "23",
            "destCidr": "Any",
            "syslogEnabled": true
        }]'
        
    Returns:
        Update status
    """
    try:
        with safe_api_call("update L3 firewall rules"):
            update_data = {}
            
            if rules:
                update_data['rules'] = json.loads(rules)
            
            if syslog_default_rule is not None:
                update_data['syslogDefaultRule'] = syslog_default_rule
            
            if not update_data:
                return "❌ No changes specified"
            
            meraki.dashboard.appliance.updateNetworkApplianceFirewallL3FirewallRules(
                network_id,
                **update_data
            )
            
            return "✅ L3 firewall rules updated successfully"
            
    except json.JSONDecodeError as e:
        return f"❌ Invalid JSON: {e}"
    except Exception as e:
        return format_error("update L3 firewall rules", e)


def get_firewall_l7_rules(network_id: str) -> str:
    """
    🌐 Get Layer 7 firewall rules for a network.
    
    Shows application-based traffic filtering rules.
    
    Args:
        network_id: Network ID to query
        
    Returns:
        Current L7 firewall rules
    """
    try:
        with safe_api_call("get L7 firewall rules"):
            rules = meraki.dashboard.appliance.getNetworkApplianceFirewallL7FirewallRules(network_id)
            
            output = ["🌐 Layer 7 Firewall Rules", "=" * 50, ""]
            
            if 'rules' in rules and rules['rules']:
                for rule in rules['rules']:
                    # Rule type
                    rule_type = rule.get('type', 'unknown')
                    type_icon = {
                        'application': '📱',
                        'applicationCategory': '📂',
                        'ipRange': '🌐',
                        'host': '💻',
                        'port': '🔌',
                        'allowedUrlPatterns': '✅',
                        'blockedUrlPatterns': '❌'
                    }.get(rule_type, '❓')
                    
                    output.append(f"{type_icon} {rule_type.upper()}")
                    
                    # Policy
                    policy = rule.get('policy', 'deny')
                    output.append(f"   Policy: {'✅ Allow' if policy == 'allow' else '❌ Deny'}")
                    
                    # Value
                    value = rule.get('value')
                    if isinstance(value, dict):
                        # For complex values like application objects
                        output.append(f"   Name: {value.get('name', 'Unknown')}")
                        if 'id' in value:
                            output.append(f"   ID: {value['id']}")
                    elif isinstance(value, list):
                        # For URL patterns
                        output.append("   Patterns:")
                        for pattern in value[:5]:  # Show first 5
                            output.append(f"     • {pattern}")
                        if len(value) > 5:
                            output.append(f"     ... and {len(value) - 5} more")
                    else:
                        output.append(f"   Value: {value}")
                    
                    output.append("")
            else:
                output.append("No L7 firewall rules configured")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("get L7 firewall rules", e)


def update_firewall_l7_rules(
    network_id: str,
    rules: str
) -> str:
    """
    🛡️ Update Layer 7 firewall rules for a network.
    
    Configure application-based traffic filtering.
    
    Args:
        network_id: Network ID to update
        rules: JSON array of L7 firewall rules
        
    Examples:
        Block social media:
        rules='[{
            "type": "applicationCategory",
            "policy": "deny",
            "value": {
                "id": "meraki:layer7/category/7",
                "name": "Social web & photo sharing"
            }
        }]'
        
        Allow specific application:
        rules='[{
            "type": "application", 
            "policy": "allow",
            "value": {
                "id": "meraki:layer7/application/205",
                "name": "Office 365"
            }
        }]'
        
        Block URL patterns:
        rules='[{
            "type": "blockedUrlPatterns",
            "value": [
                "*.gambling.com",
                "*.casino.*",
                "*poker*"
            ]
        }]'
        
    Returns:
        Update status
    """
    try:
        with safe_api_call("update L7 firewall rules"):
            rules_data = json.loads(rules)
            
            meraki.dashboard.appliance.updateNetworkApplianceFirewallL7FirewallRules(
                network_id,
                rules=rules_data
            )
            
            return "✅ L7 firewall rules updated successfully"
            
    except json.JSONDecodeError as e:
        return f"❌ Invalid JSON: {e}"
    except Exception as e:
        return format_error("update L7 firewall rules", e)


def get_firewall_port_forwarding_rules(network_id: str) -> str:
    """
    ↗️ Get port forwarding rules for a network.
    
    Shows NAT rules for inbound traffic.
    
    Args:
        network_id: Network ID to query
        
    Returns:
        Current port forwarding rules
    """
    try:
        with safe_api_call("get port forwarding rules"):
            rules = meraki.dashboard.appliance.getNetworkApplianceFirewallPortForwardingRules(network_id)
            
            output = ["↗️ Port Forwarding Rules", "=" * 50, ""]
            
            if 'rules' in rules and rules['rules']:
                for i, rule in enumerate(rules['rules'], 1):
                    output.append(f"{i}. {rule.get('name', 'Unnamed Rule')}")
                    
                    # Public port
                    output.append(f"   Public Port: {rule.get('publicPort', 'Any')}")
                    
                    # Local IP and port
                    output.append(f"   Local IP: {rule.get('localIp', 'Unknown')}")
                    output.append(f"   Local Port: {rule.get('localPort', 'Unknown')}")
                    
                    # Protocol
                    output.append(f"   Protocol: {rule.get('protocol', 'tcp').upper()}")
                    
                    # Allowed IPs
                    allowed_ips = rule.get('allowedIps', [])
                    if allowed_ips:
                        output.append("   Allowed IPs:")
                        for ip in allowed_ips[:5]:
                            output.append(f"     • {ip}")
                        if len(allowed_ips) > 5:
                            output.append(f"     ... and {len(allowed_ips) - 5} more")
                    else:
                        output.append("   Allowed IPs: Any")
                    
                    output.append("")
            else:
                output.append("No port forwarding rules configured")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("get port forwarding rules", e)


def update_firewall_port_forwarding_rules(
    network_id: str,
    rules: str
) -> str:
    """
    🔄 Update port forwarding rules for a network.
    
    Configure NAT rules for inbound services.
    
    Args:
        network_id: Network ID to update
        rules: JSON array of port forwarding rules
        
    Examples:
        Forward web server:
        rules='[{
            "name": "Web Server",
            "publicPort": "80",
            "localIp": "192.168.1.100",
            "localPort": "80",
            "protocol": "tcp",
            "allowedIps": ["any"]
        }]'
        
        Forward RDP with restrictions:
        rules='[{
            "name": "RDP Access",
            "publicPort": "3389",
            "localIp": "192.168.1.50",
            "localPort": "3389",
            "protocol": "tcp",
            "allowedIps": ["203.0.113.0/24", "198.51.100.14"]
        }]'
        
        Forward custom port:
        rules='[{
            "name": "Game Server",
            "publicPort": "25565",
            "localIp": "192.168.1.200",
            "localPort": "25565",
            "protocol": "both",
            "allowedIps": ["any"]
        }]'
        
    Returns:
        Update status
    """
    try:
        with safe_api_call("update port forwarding rules"):
            rules_data = json.loads(rules)
            
            meraki.dashboard.appliance.updateNetworkApplianceFirewallPortForwardingRules(
                network_id,
                rules=rules_data
            )
            
            return "✅ Port forwarding rules updated successfully"
            
    except json.JSONDecodeError as e:
        return f"❌ Invalid JSON: {e}"
    except Exception as e:
        return format_error("update port forwarding rules", e)


def get_firewall_inbound_cellular_rules(network_id: str) -> str:
    """
    📶 Get inbound cellular firewall rules.
    
    Shows rules for traffic coming through cellular uplinks.
    
    Args:
        network_id: Network ID to query
        
    Returns:
        Cellular firewall rules
    """
    try:
        with safe_api_call("get inbound cellular rules"):
            rules = meraki.dashboard.appliance.getNetworkApplianceFirewallInboundCellularFirewallRules(network_id)
            
            output = ["📶 Inbound Cellular Firewall Rules", "=" * 50, ""]
            
            if 'rules' in rules and rules['rules']:
                for i, rule in enumerate(rules['rules'], 1):
                    output.append(f"{i}. {rule.get('comment', 'Unnamed Rule')}")
                    output.append(f"   Policy: {'✅ Allow' if rule.get('policy') == 'allow' else '❌ Deny'}")
                    output.append(f"   Protocol: {rule.get('protocol', 'any').upper()}")
                    
                    # Source
                    src_port = rule.get('srcPort', 'Any')
                    src_cidr = rule.get('srcCidr', 'Any')
                    output.append(f"   Source: {src_cidr}:{src_port}")
                    
                    # Destination
                    dest_port = rule.get('destPort', 'Any') 
                    dest_cidr = rule.get('destCidr', 'Any')
                    output.append(f"   Destination: {dest_cidr}:{dest_port}")
                    
                    # Syslog
                    if rule.get('syslogEnabled'):
                        output.append("   📝 Syslog: Enabled")
                    
                    output.append("")
            else:
                output.append("No inbound cellular firewall rules configured")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("get inbound cellular rules", e)


def get_firewall_services(network_id: str) -> str:
    """
    🔧 Get firewall service settings.
    
    Shows allowed services like ICMP, SNMP, and web access.
    
    Args:
        network_id: Network ID to query
        
    Returns:
        Firewall service configuration
    """
    try:
        with safe_api_call("get firewall services"):
            services = meraki.dashboard.appliance.getNetworkApplianceFirewallFirewalledServices(network_id)
            
            output = ["🔧 Firewall Services", "=" * 50, ""]
            
            if services:
                for service in services:
                    service_name = service.get('service', 'Unknown')
                    access = service.get('access', 'restricted')
                    
                    # Service icon
                    icon = {
                        'ICMP': '🏓',
                        'SNMP': '📊',
                        'web': '🌐'
                    }.get(service_name, '🔧')
                    
                    output.append(f"{icon} {service_name}")
                    output.append(f"   Access: {access}")
                    
                    # Allowed IPs
                    if access == 'restricted' and 'allowedIps' in service:
                        output.append("   Allowed IPs:")
                        for ip in service['allowedIps'][:5]:
                            output.append(f"     • {ip}")
                        if len(service['allowedIps']) > 5:
                            output.append(f"     ... and {len(service['allowedIps']) - 5} more")
                    
                    output.append("")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("get firewall services", e)


def update_firewall_services(
    network_id: str,
    service: str,
    access: str,
    allowed_ips: Optional[str] = None
) -> str:
    """
    🔧 Update firewall service settings.
    
    Configure access to ICMP, SNMP, or web services.
    
    Args:
        network_id: Network ID to update
        service: Service name ('ICMP', 'SNMP', or 'web')
        access: Access policy ('blocked', 'restricted', or 'unrestricted')
        allowed_ips: JSON array of allowed IPs (for 'restricted' access)
        
    Examples:
        Allow ping from specific IPs:
        service="ICMP" access="restricted" allowed_ips='["10.0.0.0/8", "192.168.1.100"]'
        
        Block SNMP completely:
        service="SNMP" access="blocked"
        
        Allow web access from anywhere:
        service="web" access="unrestricted"
        
    Returns:
        Update status
    """
    try:
        with safe_api_call("update firewall service"):
            update_data = {
                "service": service,
                "access": access
            }
            
            if access == "restricted" and allowed_ips:
                update_data["allowedIps"] = json.loads(allowed_ips)
            
            meraki.dashboard.appliance.updateNetworkApplianceFirewallFirewalledService(
                network_id,
                service,
                **update_data
            )
            
            return f"✅ {service} firewall service updated successfully"
            
    except json.JSONDecodeError as e:
        return f"❌ Invalid JSON in allowed_ips: {e}"
    except Exception as e:
        return format_error("update firewall service", e)


def get_layer7_application_categories(network_id: str) -> str:
    """
    📱 Get all available Layer 7 application categories.
    
    Lists categories for use in L7 firewall rules.
    
    Args:
        network_id: Network ID to query
    
    Returns:
        Available L7 application categories
    """
    try:
        with safe_api_call("get L7 application categories"):
            categories = meraki.dashboard.appliance.getNetworkApplianceFirewallL7FirewallRulesApplicationCategories(network_id)
            
            output = ["📱 Layer 7 Application Categories", "=" * 50, ""]
            
            if 'applicationCategories' in categories:
                # Group by type
                by_type = {}
                for cat in categories['applicationCategories']:
                    cat_type = cat.get('type', 'Other')
                    if cat_type not in by_type:
                        by_type[cat_type] = []
                    by_type[cat_type].append(cat)
                
                for cat_type, cats in sorted(by_type.items()):
                    output.append(f"\n{cat_type}:")
                    for cat in sorted(cats, key=lambda x: x.get('name', '')):
                        output.append(f"  • {cat.get('name')} (ID: {cat.get('id')})")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("get L7 application categories", e)


# Helper tool
def check_firewall_prerequisites(network_id: str) -> str:
    """
    🔍 Check firewall configuration prerequisites.
    
    ALWAYS RUN THIS FIRST before configuring firewall rules!
    
    Args:
        network_id: Network ID to check
        
    Returns:
        Prerequisites status and guidance
    """
    try:
        output = ["🔍 Firewall Prerequisites Check", "=" * 50, ""]
        
        # Check if network has MX appliance
        try:
            devices = meraki.dashboard.networks.getNetworkDevices(network_id)
            has_mx = any(d.get('model', '').startswith('MX') for d in devices)
            
            if has_mx:
                output.append("✅ MX Security Appliance detected")
                mx_models = [d.get('model') for d in devices if d.get('model', '').startswith('MX')]
                output.append(f"   Models: {', '.join(mx_models)}")
            else:
                output.append("❌ No MX Security Appliance found")
                output.append("   Firewall features require an MX device")
                return "\n".join(output)
        except:
            output.append("⚠️ Could not verify MX appliance")
        
        # Check current rules
        checks = [
            ("L3 Firewall", lambda: meraki.dashboard.appliance.getNetworkApplianceFirewallL3FirewallRules(network_id)),
            ("L7 Firewall", lambda: meraki.dashboard.appliance.getNetworkApplianceFirewallL7FirewallRules(network_id)),
            ("Port Forwarding", lambda: meraki.dashboard.appliance.getNetworkApplianceFirewallPortForwardingRules(network_id))
        ]
        
        output.append("\n📋 Feature Availability:")
        for feature_name, check_func in checks:
            try:
                check_func()
                output.append(f"   ✅ {feature_name}: Available")
            except Exception as e:
                if "404" in str(e):
                    output.append(f"   ❌ {feature_name}: Not available")
                else:
                    output.append(f"   ⚠️ {feature_name}: Error checking")
        
        # Recommendations
        output.extend([
            "\n💡 Best Practices:",
            "1. Always backup current rules before making changes",
            "2. Test rules in a maintenance window",
            "3. Use descriptive comments for all rules",
            "4. Enable syslog for security-critical rules",
            "",
            "🔐 Security Tips:",
            "• Deny by default, allow by exception",
            "• Use most specific rules first",
            "• Regularly review and audit rules",
            "• Document all port forwarding rules"
        ])
        
        return "\n".join(output)
        
    except Exception as e:
        return format_error("check prerequisites", e)


def register_firewall_tools(app: FastMCP, client: MerakiClient):
    """Register firewall tools with the MCP server."""
    global mcp_app, meraki
    mcp_app = app
    meraki = client
    
    # Register all tools
    app.tool()(get_firewall_l3_rules)
    app.tool()(update_firewall_l3_rules)
    app.tool()(get_firewall_l7_rules)
    app.tool()(update_firewall_l7_rules)
    app.tool()(get_firewall_port_forwarding_rules)
    app.tool()(update_firewall_port_forwarding_rules)
    app.tool()(get_firewall_inbound_cellular_rules)
    app.tool()(get_firewall_services)
    app.tool()(update_firewall_services)
    app.tool()(get_layer7_application_categories)
    app.tool()(check_firewall_prerequisites)