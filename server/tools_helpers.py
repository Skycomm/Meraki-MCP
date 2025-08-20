"""
Helper tools for better tool discovery and usage guidance.
Provides context-aware tool selection and category helpers.
"""

from mcp.server import FastMCP
from typing import Optional, Dict, Any, List
from meraki_client import MerakiClient

# This will be set by register function
mcp_app = None
meraki = None


def check_network_capabilities(network_id: str) -> str:
    """
    🔍 Check network capabilities to determine available tool categories.
    
    Shows which device types are present and which tools can be used.
    
    Args:
        network_id: Network ID to check
        
    Returns:
        Network capabilities and available tool categories
    """
    try:
        # Get network info
        network = meraki.dashboard.networks.getNetwork(networkId=network_id)
        devices = meraki.dashboard.networks.getNetworkDevices(networkId=network_id)
        
        result = f"""🔍 Network Capabilities Check
==================================================

Network: {network['name']}
Product Types: {', '.join(network.get('productTypes', []))}

"""
        
        # Check each product type
        capabilities = {
            'appliance': False,
            'switch': False,
            'wireless': False,
            'camera': False,
            'cellularGateway': False,
            'sensor': False
        }
        
        for product in network.get('productTypes', []):
            if product in capabilities:
                capabilities[product] = True
        
        # Show available capabilities
        result += "✅ Available Capabilities:\n"
        
        if capabilities['appliance']:
            result += "\n🔐 Security Appliance (MX):\n"
            result += "   • Firewall management\n"
            result += "   • VPN configuration\n"
            result += "   • Traffic shaping\n"
            result += "   • DHCP services\n"
            result += "   • Uplink monitoring\n"
            result += "   • Content filtering\n"
            
        if capabilities['switch']:
            result += "\n🔌 Switches (MS):\n"
            result += "   • Port configuration\n"
            result += "   • VLAN management\n"
            result += "   • STP settings\n"
            result += "   • Cable testing\n"
            result += "   • PoE control\n"
            
        if capabilities['wireless']:
            result += "\n📡 Wireless (MR):\n"
            result += "   • SSID configuration\n"
            result += "   • RF optimization\n"
            result += "   • Client analytics\n"
            result += "   • Mesh networking\n"
            result += "   • Bluetooth settings\n"
            
        if capabilities['camera']:
            result += "\n📹 Cameras (MV):\n"
            result += "   • Video settings\n"
            result += "   • Motion detection\n"
            result += "   • Analytics zones\n"
            result += "   • Snapshot capture\n"
            
        # Show device inventory
        result += f"\n📊 Device Inventory ({len(devices)} devices):\n"
        
        device_types = {}
        for device in devices:
            model_prefix = device['model'][:2]
            if model_prefix not in device_types:
                device_types[model_prefix] = []
            device_types[model_prefix].append(device)
        
        for prefix, device_list in sorted(device_types.items()):
            result += f"\n{prefix} Devices ({len(device_list)}):\n"
            for device in device_list[:3]:  # Show first 3
                status = '🟢' if device.get('status') == 'online' else '🔴'
                result += f"   {status} {device.get('name', device['serial'])} ({device['model']})\n"
            if len(device_list) > 3:
                result += f"   ... and {len(device_list) - 3} more\n"
        
        # Tool recommendations
        result += "\n💡 Recommended Tool Categories:\n"
        
        if capabilities['appliance']:
            result += "\n   For Security (MX):\n"
            result += "   • firewall_help() - Firewall management\n"
            result += "   • vpn_configuration_help() - VPN setup\n"
            result += "   • traffic_shaping_help() - QoS control\n"
            result += "   • check_dhcp_network_type() - DHCP tools\n"
            
        if capabilities['switch']:
            result += "\n   For Switching (MS):\n"
            result += "   • get_switch_ports() - Port status\n"
            result += "   • configure_switch_port() - Port config\n"
            result += "   • create_switch_cable_test() - Cable testing\n"
            
        if capabilities['wireless']:
            result += "\n   For Wireless (MR):\n"
            result += "   • get_network_wireless_ssids() - WiFi networks\n"
            result += "   • update_network_wireless_ssid() - SSID config\n"
            result += "   • get_network_wireless_rf_profiles() - RF settings\n"
        
        return result
        
    except Exception as e:
        return f"❌ Error checking network capabilities: {str(e)}"


def suggest_tools_for_task(task_description: str) -> str:
    """
    🎯 Suggest appropriate tools based on task description.
    
    Natural language tool discovery helper.
    
    Args:
        task_description: What you want to accomplish
        
    Returns:
        Suggested tools and examples
    """
    task_lower = task_description.lower()
    
    result = f"""🎯 Tool Suggestions for: "{task_description}"
==================================================

"""
    
    suggestions = []
    
    # Firewall related
    if any(word in task_lower for word in ['firewall', 'block', 'allow', 'port', 'rule']):
        suggestions.append({
            'category': 'Firewall Management',
            'tools': [
                ('get_firewall_l3_rules(network_id)', 'View current firewall rules'),
                ('add_firewall_l3_rule(network_id, ...)', 'Add new firewall rule'),
                ('add_port_forwarding_rule(network_id, ...)', 'Forward ports'),
                ('firewall_help()', 'Get firewall management help')
            ]
        })
    
    # VPN related
    if any(word in task_lower for word in ['vpn', 'remote', 'tunnel', 'ipsec']):
        suggestions.append({
            'category': 'VPN Configuration',
            'tools': [
                ('get_vpn_status(network_id)', 'Check VPN status'),
                ('configure_site_to_site_vpn(network_id, ...)', 'Set up site VPN'),
                ('configure_client_vpn(network_id, ...)', 'Enable remote access'),
                ('vpn_configuration_help()', 'Get VPN help')
            ]
        })
    
    # Client/WiFi issues
    if any(word in task_lower for word in ['client', 'wifi', 'wireless', 'connect', 'user']):
        suggestions.append({
            'category': 'Client Troubleshooting',
            'tools': [
                ('diagnose_client_connection(network_id, mac)', 'Diagnose issues'),
                ('get_client_details(network_id, mac)', 'Get client info'),
                ('analyze_client_performance(network_id, mac)', 'Check performance'),
                ('client_troubleshooting_help()', 'Get troubleshooting help')
            ]
        })
    
    # Monitoring/Performance
    if any(word in task_lower for word in ['monitor', 'performance', 'slow', 'bandwidth', 'usage']):
        suggestions.append({
            'category': 'Performance Monitoring',
            'tools': [
                ('get_network_health_summary(network_id)', 'Overall health check'),
                ('analyze_performance_bottlenecks(network_id)', 'Find issues'),
                ('get_uplink_bandwidth_history(network_id)', 'WAN usage'),
                ('monitoring_help()', 'Get monitoring help')
            ]
        })
    
    # DHCP related
    if any(word in task_lower for word in ['dhcp', 'ip', 'address', 'reservation', 'lease']):
        suggestions.append({
            'category': 'DHCP Management',
            'tools': [
                ('check_dhcp_network_type(network_id)', 'IMPORTANT: Run this first!'),
                ('list_single_lan_fixed_ips(network_id)', 'For non-VLAN networks'),
                ('get_vlan_dhcp_settings(network_id, vlan_id)', 'For VLAN networks'),
                ('dhcp_help()', 'Get DHCP help')
            ]
        })
    
    # Traffic Shaping/QoS
    if any(word in task_lower for word in ['qos', 'bandwidth', 'limit', 'shape', 'priority']):
        suggestions.append({
            'category': 'Traffic Shaping',
            'tools': [
                ('check_traffic_shaping_prerequisites(network_id)', 'Check if available'),
                ('get_traffic_shaping_rules(network_id)', 'View current rules'),
                ('set_bandwidth_limit(network_id, ...)', 'Limit bandwidth'),
                ('traffic_shaping_help()', 'Get QoS help')
            ]
        })
    
    # Alerts/Notifications
    if any(word in task_lower for word in ['alert', 'notify', 'email', 'webhook', 'snmp']):
        suggestions.append({
            'category': 'Alert Configuration',
            'tools': [
                ('get_alert_settings(network_id)', 'View alert config'),
                ('configure_email_alerts(network_id, ...)', 'Set up emails'),
                ('configure_snmp(network_id, ...)', 'Enable SNMP'),
                ('alert_configuration_help()', 'Get alert help')
            ]
        })
    
    # Changes/Audit
    if any(word in task_lower for word in ['change', 'audit', 'who', 'when', 'history']):
        suggestions.append({
            'category': 'Change Tracking',
            'tools': [
                ('get_configuration_changes(org_id)', 'Recent changes'),
                ('generate_change_report(org_id, ...)', 'Audit report'),
                ('track_specific_changes(org_id, ...)', 'Filter changes'),
                ('change_tracking_help()', 'Get tracking help')
            ]
        })
    
    if suggestions:
        for suggestion in suggestions:
            result += f"\n📁 {suggestion['category']}:\n"
            for tool, desc in suggestion['tools']:
                result += f"   • {tool}\n"
                result += f"     {desc}\n"
    else:
        result += "No specific tool suggestions found. Try:\n"
        result += "   • help() - List all available tools\n"
        result += "   • check_network_capabilities(network_id) - See what's available\n"
        result += "   • Use more specific keywords in your task description\n"
    
    result += "\n💡 Tips:\n"
    result += "   • Always check prerequisites first\n"
    result += "   • Use help() functions for detailed guidance\n"
    result += "   • Test in lab environment when possible\n"
    
    return result


def list_tool_categories() -> str:
    """
    📚 List all available tool categories with descriptions.
    
    Overview of all tool categories in the MCP server.
    
    Returns:
        Formatted list of tool categories
    """
    return """📚 Meraki MCP Tool Categories
==================================================

## 🔐 Security & Access Control
• **Firewall Management** - L3/L7 rules, port forwarding, NAT
• **VPN Configuration** - Site-to-site, client VPN, third-party peers
• **Traffic Shaping** - QoS, bandwidth control, application priorities
• **Content Filtering** - Web filtering, malware protection

## 🌐 Network Configuration
• **DHCP Services** - IP management, reservations, options
• **VLAN Management** - VLAN configuration, inter-VLAN routing
• **Wireless Settings** - SSID, security, RF optimization
• **Switch Configuration** - Ports, STP, storm control

## 📊 Monitoring & Analytics
• **Health Monitoring** - Real-time status, performance metrics
• **Event Analysis** - Log analysis, pattern detection, root cause
• **Client Analytics** - Usage patterns, performance tracking
• **Uplink Monitoring** - WAN performance, failover tracking

## 🔧 Troubleshooting
• **Client Troubleshooting** - Connection issues, performance
• **Network Diagnostics** - Connectivity tests, bottlenecks
• **Live Tools** - Ping, traceroute, cable test
• **Performance Analysis** - Latency, packet loss, throughput

## 📋 Management & Compliance
• **Change Tracking** - Audit logs, configuration history
• **Alert Configuration** - Email, webhooks, SNMP
• **Firmware Management** - Updates, compliance, rollback
• **Report Generation** - Health reports, compliance audits

## 🏢 Organization Tools
• **Organization Management** - Networks, admins, licenses
• **Policy Management** - Group policies, templates
• **License Management** - Usage, compliance, renewal

## 🎯 Quick Access by Device Type

### [MX] Security Appliances
- Firewall, VPN, Traffic Shaping, DHCP, Uplink Monitoring

### [MS] Switches  
- Port Config, VLANs, STP, Cable Test, PoE Control

### [MR] Wireless
- SSIDs, RF Settings, Client Analytics, Mesh Config

### [MV] Cameras
- Video Settings, Motion Detection, Analytics, Snapshots

### [SM] Systems Manager
- Device Policies, App Management, Security Profiles

## 💡 Getting Started
1. Use `check_network_capabilities(network_id)` to see available features
2. Use category-specific help functions (e.g., `firewall_help()`)
3. Check prerequisites before configuration changes
4. Test in lab environment when possible

## 🔍 Tool Discovery
- By task: `suggest_tools_for_task("block port 80")`
- By category: `firewall_help()`, `vpn_help()`, etc.
- All tools: `help()` in the MCP interface
"""


def helper_tools_info() -> str:
    """
    ❓ Get information about helper tools and patterns.
    
    Explains context-aware tool selection and best practices.
    
    Returns:
        Helper tools guide
    """
    return """❓ Helper Tools & Patterns Guide
==================================================

## 🎯 Context-Aware Tool Selection

The MCP server uses helper patterns to guide you to the right tools:

### 1. Capability Checking
Always start by understanding what's available:
```
check_network_capabilities(network_id)
```
This shows:
- Device types in the network
- Available features
- Recommended tools

### 2. Task-Based Discovery
Describe what you want to do:
```
suggest_tools_for_task("limit Netflix bandwidth")
```
Returns:
- Relevant tool categories
- Specific tool suggestions
- Usage examples

### 3. Category-Specific Helpers
Each major category has a help function:
- `firewall_help()` - Firewall tools
- `vpn_configuration_help()` - VPN tools
- `traffic_shaping_help()` - QoS tools
- `client_troubleshooting_help()` - Client tools
- And many more...

## 🔍 The DHCP Pattern

DHCP tools pioneered the helper pattern:

1. **Check First**: `check_dhcp_network_type(network_id)`
2. **Understand Context**: Single LAN vs VLAN-enabled
3. **Use Appropriate Tools**: Different tools for each type

This pattern prevents common errors like:
- Using VLAN tools on non-VLAN networks
- Assuming subnet numbers indicate VLAN IDs
- Missing network type requirements

## 💡 Best Practices

### Always Check Prerequisites
```
# Before traffic shaping:
check_traffic_shaping_prerequisites(network_id)

# Before DHCP changes:
check_dhcp_network_type(network_id)

# Before any changes:
check_network_capabilities(network_id)
```

### Use Natural Language
```
# Instead of memorizing tool names:
suggest_tools_for_task("monitor bandwidth usage")
suggest_tools_for_task("block social media")
suggest_tools_for_task("setup remote access")
```

### Follow the Workflow
1. Check capabilities/prerequisites
2. Use help function for guidance
3. Execute specific tools
4. Verify results

## 🏷️ Tool Naming Patterns

Tools follow consistent naming:
- `get_*` - Retrieve information
- `update_*` - Modify existing
- `create_*` - Create new
- `delete_*` - Remove
- `configure_*` - Complex setup
- `analyze_*` - Deep analysis
- `diagnose_*` - Troubleshooting
- `generate_*` - Create reports

## 🔧 Helper Tools Available

- `check_network_capabilities()` - What can this network do?
- `suggest_tools_for_task()` - What tools for this task?
- `list_tool_categories()` - Overview of all categories
- `helper_tools_info()` - This guide

## 📚 Category Helpers

Each category has its own helper:
- Alert Configuration
- Change Tracking  
- Client Troubleshooting
- DHCP Management
- Diagnostic Reports
- Event Analysis
- Firewall Management
- Firmware Management
- Monitoring Dashboard
- Traffic Shaping
- Troubleshooting
- Uplink Monitoring
- VPN Configuration
- Wireless Management
- And more...

## 🎓 Learning Path

1. Start with `check_network_capabilities()`
2. Explore category helps
3. Try task-based discovery
4. Use specific tools
5. Check results

The helper pattern makes the 200+ tools discoverable and usable without memorizing everything!
"""


def register_helper_tools(app: FastMCP, meraki_client: MerakiClient):
    """Register helper tools with the MCP server."""
    global mcp_app, meraki
    mcp_app = app
    meraki = meraki_client
    
    # Register all tools
    tools = [
        (check_network_capabilities, "[ALL] Check what tools are available for a network"),
        (suggest_tools_for_task, "[ALL] Get tool suggestions for a specific task"),
        (list_tool_categories, "[ALL] List all available tool categories"),
        (helper_tools_info, "[ALL] Learn about helper patterns and best practices"),
    ]
    
    for tool_func, description in tools:
        app.tool(
            name=tool_func.__name__,
            description=description
        )(tool_func)