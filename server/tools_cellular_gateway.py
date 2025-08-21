"""
Cellular Gateway Tools for Cisco Meraki MCP Server
Manage cellular gateways, eSIMs, and LTE/5G connectivity
"""

from mcp.server import FastMCP
from typing import Optional, Dict, Any, List
import json
from datetime import datetime, timedelta
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


def get_device_cellular_gateway_lan(serial: str) -> str:
    """
    🌐 Get cellular gateway LAN configuration.
    
    Shows LAN settings for a cellular gateway device.
    
    Args:
        serial: Device serial number
    
    Returns:
        LAN configuration details
    """
    try:
        with safe_api_call("get cellular gateway LAN"):
            lan = meraki.dashboard.cellularGateway.getDeviceCellularGatewayLan(serial)
            
            output = ["🌐 Cellular Gateway LAN Configuration", "=" * 50, ""]
            output.append(f"Device: {serial}")
            output.append("")
            
            # Reserved subnets
            reserved = lan.get('reservedIpRanges', [])
            if reserved:
                output.append("📍 Reserved IP Ranges:")
                for range_info in reserved:
                    start = range_info.get('start', 'N/A')
                    end = range_info.get('end', 'N/A')
                    comment = range_info.get('comment', '')
                    output.append(f"   • {start} - {end}")
                    if comment:
                        output.append(f"     Comment: {comment}")
                output.append("")
            
            # Fixed IP assignments
            fixed_ips = lan.get('fixedIpAssignments', [])
            if fixed_ips:
                output.append("🔧 Fixed IP Assignments:")
                for assignment in fixed_ips:
                    name = assignment.get('name', 'Unknown')
                    ip = assignment.get('ip', 'N/A')
                    mac = assignment.get('mac', 'N/A')
                    output.append(f"   • {name}: {ip} ({mac})")
                output.append("")
            
            # Device LAN IP
            if lan.get('deviceLanIp'):
                output.append(f"🔌 Device LAN IP: {lan['deviceLanIp']}")
            
            # Device subnet
            if lan.get('deviceSubnet'):
                output.append(f"🌐 Device Subnet: {lan['deviceSubnet']}")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("get cellular gateway LAN", e)


def get_device_cellular_gateway_port_forwarding_rules(serial: str) -> str:
    """
    🔀 Get port forwarding rules for cellular gateway.
    
    Shows configured port forwarding rules.
    
    Args:
        serial: Device serial number
    
    Returns:
        Port forwarding configuration
    """
    try:
        with safe_api_call("get port forwarding rules"):
            rules = meraki.dashboard.cellularGateway.getDeviceCellularGatewayPortForwardingRules(serial)
            
            output = ["🔀 Port Forwarding Rules", "=" * 50, ""]
            output.append(f"Device: {serial}")
            
            rule_list = rules.get('rules', [])
            if not rule_list:
                output.append("\nNo port forwarding rules configured")
                return "\n".join(output)
            
            output.append(f"\nTotal Rules: {len(rule_list)}")
            output.append("")
            
            for i, rule in enumerate(rule_list, 1):
                output.append(f"📋 Rule {i}: {rule.get('name', 'Unnamed')}")
                output.append(f"   LAN IP: {rule.get('lanIp', 'N/A')}")
                output.append(f"   Public Port: {rule.get('publicPort', 'N/A')}")
                output.append(f"   Local Port: {rule.get('localPort', 'N/A')}")
                output.append(f"   Protocol: {rule.get('protocol', 'N/A')}")
                
                allowed = rule.get('allowedIps', [])
                if allowed:
                    output.append(f"   Allowed IPs: {', '.join(allowed)}")
                else:
                    output.append("   Allowed IPs: Any")
                
                output.append("")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("get port forwarding rules", e)


def get_organization_cellular_gateway_esims_inventory(org_id: str) -> str:
    """
    📱 Get eSIM inventory for the organization.
    
    Shows all eSIMs and their status across the organization.
    
    Args:
        org_id: Organization ID
    
    Returns:
        eSIM inventory details
    """
    try:
        with safe_api_call("get eSIM inventory"):
            esims = meraki.dashboard.cellularGateway.getOrganizationCellularGatewayEsimsInventory(org_id)
            
            output = ["📱 eSIM Inventory", "=" * 50, ""]
            
            if not esims:
                output.append("No eSIMs in inventory")
                return "\n".join(output)
            
            # Group by status
            by_status = {}
            for esim in esims:
                status = esim.get('status', 'Unknown')
                if status not in by_status:
                    by_status[status] = []
                by_status[status].append(esim)
            
            # Show summary
            output.append(f"Total eSIMs: {len(esims)}")
            for status, sims in by_status.items():
                output.append(f"   {status}: {len(sims)}")
            output.append("")
            
            # Show details by status
            for status, sims in by_status.items():
                output.append(f"📊 {status} eSIMs ({len(sims)}):")
                
                for sim in sims[:5]:  # Show first 5 of each status
                    eid = sim.get('eid', 'Unknown')
                    output.append(f"\n   eSIM ID: {eid[:20]}...")
                    
                    if sim.get('deviceSerial'):
                        output.append(f"   Device: {sim['deviceSerial']}")
                    
                    if sim.get('carrier'):
                        output.append(f"   Carrier: {sim['carrier']}")
                    
                    if sim.get('iccid'):
                        output.append(f"   ICCID: {sim['iccid'][:10]}...")
                    
                    if sim.get('activationDate'):
                        output.append(f"   Activated: {sim['activationDate']}")
                
                if len(sims) > 5:
                    output.append(f"\n   ... and {len(sims) - 5} more")
                
                output.append("")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("get eSIM inventory", e)


def get_organization_cellular_gateway_esims_service_providers(org_id: str) -> str:
    """
    📡 Get eSIM service providers.
    
    Shows available eSIM service providers and accounts.
    
    Args:
        org_id: Organization ID
    
    Returns:
        Service provider information
    """
    try:
        with safe_api_call("get eSIM service providers"):
            providers = meraki.dashboard.cellularGateway.getOrganizationCellularGatewayEsimsServiceProviders(org_id)
            
            output = ["📡 eSIM Service Providers", "=" * 50, ""]
            
            accounts = providers.get('accounts', [])
            if not accounts:
                output.append("No service provider accounts configured")
                output.append("\n💡 Add accounts to enable eSIM provisioning")
                return "\n".join(output)
            
            output.append(f"Total Accounts: {len(accounts)}")
            output.append("")
            
            for account in accounts:
                account_id = account.get('accountId', 'Unknown')
                title = account.get('title', 'Unnamed Account')
                provider = account.get('serviceProvider', {})
                
                output.append(f"📱 {title}")
                output.append(f"   Account ID: {account_id}")
                output.append(f"   Provider: {provider.get('name', 'Unknown')}")
                
                if account.get('lastUpdatedAt'):
                    output.append(f"   Last Updated: {account['lastUpdatedAt']}")
                
                # API integration status
                if account.get('apiKey'):
                    output.append("   🔑 API Integration: Active")
                else:
                    output.append("   ⚠️ API Integration: Not configured")
                
                output.append("")
            
            # Show available providers
            available_providers = providers.get('providers', [])
            if available_providers:
                output.append("📋 Available Providers:")
                for provider in available_providers:
                    output.append(f"   • {provider.get('name', 'Unknown')}")
                    if provider.get('countries'):
                        output.append(f"     Countries: {', '.join(provider['countries'][:5])}")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("get eSIM service providers", e)


def analyze_cellular_performance(network_id: str) -> str:
    """
    📊 Analyze cellular gateway performance.
    
    Provides insights on cellular connectivity and usage.
    
    Args:
        network_id: Network ID
    
    Returns:
        Performance analysis and recommendations
    """
    try:
        with safe_api_call("analyze cellular performance"):
            output = ["📊 Cellular Gateway Performance Analysis", "=" * 50, ""]
            
            # Get cellular gateway devices
            devices = meraki.dashboard.networks.getNetworkDevices(network_id)
            mg_devices = [d for d in devices if d.get('model', '').startswith('MG')]
            
            if not mg_devices:
                output.append("No cellular gateway devices found in this network")
                return "\n".join(output)
            
            output.append(f"Cellular Gateways: {len(mg_devices)}")
            output.append("")
            
            for device in mg_devices:
                serial = device['serial']
                name = device.get('name', serial)
                model = device['model']
                
                output.append(f"📱 {name} ({model})")
                
                # Get uplink status
                try:
                    org_id = meraki.dashboard.networks.getNetwork(network_id).get('organizationId')
                    uplink_statuses = meraki.dashboard.appliance.getOrganizationApplianceUplinkStatuses(org_id)
                    
                    device_status = next((s for s in uplink_statuses 
                                        if s.get('serial') == serial), None)
                    
                    if device_status:
                        for uplink in device_status.get('uplinks', []):
                            if uplink.get('interface', '').lower() == 'cellular':
                                status = uplink.get('status', 'Unknown')
                                status_icon = '🟢' if status == 'active' else '🔴'
                                
                                output.append(f"   Status: {status_icon} {status}")
                                
                                if uplink.get('signalType'):
                                    output.append(f"   Signal: {uplink['signalType']}")
                                
                                if uplink.get('signalStat'):
                                    signal = uplink['signalStat']
                                    if signal.get('rsrp'):
                                        rsrp = signal['rsrp']
                                        # RSRP signal strength interpretation
                                        if rsrp > -80:
                                            strength = "Excellent 📶"
                                        elif rsrp > -90:
                                            strength = "Good 📶"
                                        elif rsrp > -100:
                                            strength = "Fair 📶"
                                        else:
                                            strength = "Poor 📶"
                                        output.append(f"   Signal Strength: {strength} ({rsrp} dBm)")
                                
                                if uplink.get('publicIp'):
                                    output.append(f"   Public IP: {uplink['publicIp']}")
                                
                                if uplink.get('provider'):
                                    output.append(f"   Provider: {uplink['provider']}")
                except:
                    output.append("   Status: Unable to retrieve")
                
                output.append("")
            
            # Recommendations
            output.append("💡 Cellular Optimization Tips:")
            output.append("• Position gateway near windows for better signal")
            output.append("• Use external antennas in weak signal areas")
            output.append("• Monitor data usage to avoid overage charges")
            output.append("• Configure failover to cellular for critical apps")
            output.append("• Test cellular failover monthly")
            output.append("• Consider 5G models for higher speeds")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("analyze cellular performance", e)


def cellular_gateway_help() -> str:
    """
    ❓ Get help with cellular gateway tools.
    
    Shows available tools and best practices.
    
    Returns:
        Formatted help guide
    """
    return """📱 Cellular Gateway Tools Help
==================================================

Available tools for cellular gateway management:

1. get_device_cellular_gateway_lan()
   - View LAN configuration
   - Reserved IP ranges
   - Fixed IP assignments

2. get_device_cellular_gateway_port_forwarding_rules()
   - Port forwarding setup
   - NAT traversal rules
   - Security settings

3. get_organization_cellular_gateway_esims_inventory()
   - eSIM inventory status
   - Device assignments
   - Activation status

4. get_organization_cellular_gateway_esims_service_providers()
   - Service provider accounts
   - Available carriers
   - API integration status

5. analyze_cellular_performance()
   - Signal strength analysis
   - Connection status
   - Optimization tips

Cellular Gateway Models:
• MG21: LTE Cat 6, compact design
• MG41: LTE Cat 12, higher speeds
• MG51: 5G support, future-proof

Signal Strength Guide:
📶 RSRP (Reference Signal Received Power):
   • > -80 dBm: Excellent
   • -80 to -90 dBm: Good
   • -90 to -100 dBm: Fair
   • < -100 dBm: Poor

Best Practices:
- Use cellular as backup WAN
- Monitor data usage closely
- Place near windows/high locations
- Use external antennas if needed
- Test failover scenarios
- Keep firmware updated

eSIM Benefits:
• Remote provisioning
• Easy carrier switching
• No physical SIM handling
• Multiple profiles support
• Better security
"""


def register_cellular_gateway_tools(app: FastMCP, meraki_client: MerakiClient):
    """Register all cellular gateway tools with the MCP server."""
    global mcp_app, meraki
    mcp_app = app
    meraki = meraki_client
    
    # Register all tools
    tools = [
        (get_device_cellular_gateway_lan, "Get cellular gateway LAN configuration"),
        (get_device_cellular_gateway_port_forwarding_rules, "View port forwarding rules"),
        (get_organization_cellular_gateway_esims_inventory, "Get eSIM inventory"),
        (get_organization_cellular_gateway_esims_service_providers, "View eSIM service providers"),
        (analyze_cellular_performance, "Analyze cellular gateway performance"),
        (cellular_gateway_help, "Get help with cellular gateway tools"),
    ]
    
    for tool_func, description in tools:
        app.tool(
            name=tool_func.__name__,
            description=description
        )(tool_func)