"""
Traffic Shaping Tools for Cisco Meraki MCP Server
Manage QoS, bandwidth limits, and traffic prioritization
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


def get_network_traffic_shaping_rules(network_id: str) -> str:
    """
    📊 Get traffic shaping rules for a network.
    
    Shows bandwidth limits and QoS settings for applications.
    
    Args:
        network_id: Network ID to query
        
    Returns:
        Current traffic shaping configuration
    """
    try:
        with safe_api_call("get traffic shaping rules"):
            rules = meraki.dashboard.appliance.getNetworkApplianceTrafficShapingRules(network_id)
            
            output = ["📊 Traffic Shaping Rules", "=" * 50, ""]
            
            # Default rules
            if 'defaultRulesEnabled' in rules:
                output.append(f"Default Rules Enabled: {'✅' if rules['defaultRulesEnabled'] else '❌'}")
                output.append("")
            
            # Custom rules
            if 'rules' in rules and rules['rules']:
                output.append("🎯 Custom Rules:")
                for i, rule in enumerate(rules['rules'], 1):
                    output.append(f"\n{i}. {rule.get('description', 'Unnamed Rule')}")
                    
                    # Definitions (what traffic this applies to)
                    if 'definitions' in rule:
                        defs = rule['definitions']
                        for def_item in defs:
                            if def_item['type'] == 'application':
                                output.append(f"   Application: {def_item['value']}")
                            elif def_item['type'] == 'applicationCategory':
                                output.append(f"   Category: {def_item['value']}")
                            elif def_item['type'] == 'ipRange':
                                output.append(f"   IP Range: {def_item['value']}")
                            elif def_item['type'] == 'port':
                                output.append(f"   Port: {def_item['value']}")
                    
                    # Per-client bandwidth limits
                    if 'perClientBandwidthLimits' in rule:
                        limits = rule['perClientBandwidthLimits']
                        settings = limits.get('settings', 'custom')
                        output.append(f"   Per-Client Limits: {settings}")
                        
                        if settings == 'custom':
                            if 'bandwidthLimits' in limits:
                                bw = limits['bandwidthLimits']
                                down = bw.get('limitDown', 'Unlimited')
                                up = bw.get('limitUp', 'Unlimited')
                                output.append(f"     ↓ Down: {down} Kbps")
                                output.append(f"     ↑ Up: {up} Kbps")
                    
                    # DSCP tagging
                    if 'dscpTagValue' in rule:
                        output.append(f"   DSCP Tag: {rule['dscpTagValue']}")
                    
                    # Priority
                    if 'priority' in rule:
                        priority = rule['priority']
                        priority_icon = {
                            'low': '🔵',
                            'normal': '🟢', 
                            'high': '🟡'
                        }.get(priority, '⚪')
                        output.append(f"   Priority: {priority_icon} {priority}")
            else:
                output.append("No custom traffic shaping rules configured")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("get traffic shaping rules", e)


def update_network_traffic_shaping_rules(
    network_id: str,
    default_rules_enabled: Optional[bool] = None,
    rules: Optional[str] = None
) -> str:
    """
    🎛️ Update traffic shaping rules for a network.
    
    Configure bandwidth limits and QoS for applications.
    
    Args:
        network_id: Network ID to update
        default_rules_enabled: Enable/disable default Meraki rules
        rules: JSON array of custom rules (see examples below)
        
    Examples:
        Basic bandwidth limit for streaming:
        rules='[{
            "description": "Limit Netflix streaming",
            "definitions": [{
                "type": "application",
                "value": "Netflix"
            }],
            "perClientBandwidthLimits": {
                "settings": "custom",
                "bandwidthLimits": {
                    "limitDown": 5000,
                    "limitUp": 1000
                }
            }
        }]'
        
        Prioritize video conferencing:
        rules='[{
            "description": "Prioritize Zoom",
            "definitions": [{
                "type": "application", 
                "value": "Zoom"
            }],
            "priority": "high",
            "dscpTagValue": 46
        }]'
        
    Returns:
        Update status
    """
    try:
        with safe_api_call("update traffic shaping rules"):
            update_data = {}
            
            if default_rules_enabled is not None:
                update_data['defaultRulesEnabled'] = default_rules_enabled
            
            if rules:
                update_data['rules'] = json.loads(rules)
            
            if not update_data:
                return "❌ No changes specified. Provide default_rules_enabled or rules."
            
            meraki.dashboard.appliance.updateNetworkApplianceTrafficShapingRules(
                network_id, 
                **update_data
            )
            
            return "✅ Traffic shaping rules updated successfully"
            
    except json.JSONDecodeError as e:
        return f"❌ Invalid JSON in rules parameter: {e}"
    except Exception as e:
        return format_error("update traffic shaping rules", e)


def get_network_traffic_shaping_uplink_selection(network_id: str) -> str:
    """
    🔄 Get uplink selection settings for traffic shaping.
    
    Shows WAN failover preferences and VPN traffic rules.
    
    Args:
        network_id: Network ID to query
        
    Returns:
        Uplink selection configuration
    """
    try:
        with safe_api_call("get uplink selection"):
            config = meraki.dashboard.appliance.getNetworkApplianceTrafficShapingUplinkSelection(network_id)
            
            output = ["🔄 Uplink Selection Settings", "=" * 50, ""]
            
            # Active uplink
            if 'activeActiveAutoVpnEnabled' in config:
                output.append(f"Active-Active AutoVPN: {'✅' if config['activeActiveAutoVpnEnabled'] else '❌'}")
            
            # Default uplink
            if 'defaultUplink' in config:
                output.append(f"Default Uplink: {config['defaultUplink']}")
            
            # Load balancing
            if 'loadBalancingEnabled' in config:
                output.append(f"Load Balancing: {'✅' if config['loadBalancingEnabled'] else '❌'}")
            
            # Failover and failback
            if 'failoverAndFailback' in config:
                ff = config['failoverAndFailback']
                output.append("\n⚡ Failover & Failback:")
                output.append(f"  Immediate Failback: {'✅' if ff.get('immediate', {}).get('enabled', False) else '❌'}")
            
            # WAN traffic preferences
            if 'wanTrafficUplinkPreferences' in config:
                output.append("\n🌐 WAN Traffic Preferences:")
                for i, pref in enumerate(config['wanTrafficUplinkPreferences'], 1):
                    output.append(f"\n{i}. Preference:")
                    
                    # Traffic filters
                    if 'trafficFilters' in pref:
                        for filter in pref['trafficFilters']:
                            filter_type = filter['type']
                            value = filter['value']
                            
                            if filter_type == 'application':
                                output.append(f"   Application: {value}")
                            elif filter_type == 'custom':
                                custom = value
                                if 'protocol' in custom:
                                    output.append(f"   Protocol: {custom['protocol']}")
                                if 'source' in custom:
                                    output.append(f"   Source: {custom['source'].get('cidr', 'Any')}")
                                if 'destination' in custom:
                                    output.append(f"   Destination: {custom['destination'].get('cidr', 'Any')}")
                    
                    # Preferred uplink
                    if 'preferredUplink' in pref:
                        output.append(f"   Preferred Uplink: {pref['preferredUplink']}")
            
            # VPN traffic preferences  
            if 'vpnTrafficUplinkPreferences' in config:
                output.append("\n🔒 VPN Traffic Preferences:")
                for i, pref in enumerate(config['vpnTrafficUplinkPreferences'], 1):
                    output.append(f"\n{i}. VPN Preference:")
                    
                    if 'trafficFilters' in pref:
                        for filter in pref['trafficFilters']:
                            filter_type = filter['type']
                            if filter_type == 'applicationCategory':
                                output.append(f"   Category: {filter['value']}")
                            elif filter_type == 'application':
                                output.append(f"   Application: {filter['value']}")
                    
                    if 'preferredUplink' in pref:
                        output.append(f"   Preferred Uplink: {pref['preferredUplink']}")
                    
                    if 'performanceClass' in pref:
                        output.append(f"   Performance Class: {pref['performanceClass']}")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("get uplink selection", e)


def update_network_traffic_shaping_uplink_selection(
    network_id: str,
    default_uplink: Optional[str] = None,
    load_balancing_enabled: Optional[bool] = None,
    wan_traffic_preferences: Optional[str] = None,
    vpn_traffic_preferences: Optional[str] = None
) -> str:
    """
    🎛️ Update uplink selection for traffic shaping.
    
    Configure WAN failover and load balancing.
    
    Args:
        network_id: Network ID to update
        default_uplink: Default WAN uplink ('wan1' or 'wan2')
        load_balancing_enabled: Enable/disable load balancing
        wan_traffic_preferences: JSON array of WAN preferences
        vpn_traffic_preferences: JSON array of VPN preferences
        
    Examples:
        Prefer WAN1 for video streaming:
        wan_traffic_preferences='[{
            "trafficFilters": [{
                "type": "applicationCategory",
                "value": "Video & music"
            }],
            "preferredUplink": "wan1"
        }]'
        
        Route VoIP over WAN2:
        wan_traffic_preferences='[{
            "trafficFilters": [{
                "type": "application",
                "value": "VoIP"
            }],
            "preferredUplink": "wan2"
        }]'
        
    Returns:
        Update status
    """
    try:
        with safe_api_call("update uplink selection"):
            update_data = {}
            
            if default_uplink:
                update_data['defaultUplink'] = default_uplink
            
            if load_balancing_enabled is not None:
                update_data['loadBalancingEnabled'] = load_balancing_enabled
            
            if wan_traffic_preferences:
                update_data['wanTrafficUplinkPreferences'] = json.loads(wan_traffic_preferences)
            
            if vpn_traffic_preferences:
                update_data['vpnTrafficUplinkPreferences'] = json.loads(vpn_traffic_preferences)
            
            if not update_data:
                return "❌ No changes specified"
            
            meraki.dashboard.appliance.updateNetworkApplianceTrafficShapingUplinkSelection(
                network_id,
                **update_data
            )
            
            return "✅ Uplink selection updated successfully"
            
    except json.JSONDecodeError as e:
        return f"❌ Invalid JSON: {e}"
    except Exception as e:
        return format_error("update uplink selection", e)


def get_network_traffic_shaping_dscp_tagging(network_id: str) -> str:
    """
    🏷️ Get DSCP tagging options for traffic shaping.
    
    Shows available DSCP values for QoS marking.
    
    Args:
        network_id: Network ID to query
        
    Returns:
        DSCP tagging options
    """
    try:
        with safe_api_call("get DSCP tagging options"):
            options = meraki.dashboard.appliance.getNetworkApplianceTrafficShapingDscpTaggingOptions(network_id)
            
            output = ["🏷️ DSCP Tagging Options", "=" * 50, ""]
            
            if options:
                for option in options:
                    output.append(f"• {option.get('description', 'Unknown')}")
                    output.append(f"  DSCP Value: {option.get('dscpTagValue', 'N/A')}")
                    output.append("")
            else:
                output.append("No DSCP tagging options available")
            
            # Common DSCP values reference
            output.extend([
                "📋 Common DSCP Values:",
                "  • 0  - Best Effort (default)",
                "  • 8  - Class Selector 1",  
                "  • 10 - Assured Forwarding 11",
                "  • 18 - Assured Forwarding 21",
                "  • 26 - Assured Forwarding 31",
                "  • 34 - Assured Forwarding 41",
                "  • 46 - Expedited Forwarding (VoIP)",
                "  • 48 - Network Control"
            ])
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("get DSCP tagging options", e)


def get_network_traffic_shaping_custom_performance_classes(network_id: str) -> str:
    """
    ⚡ Get custom performance classes for traffic shaping.
    
    Shows QoS profiles for different traffic types.
    
    Args:
        network_id: Network ID to query
        
    Returns:
        Custom performance class configuration
    """
    try:
        with safe_api_call("get custom performance classes"):
            classes = meraki.dashboard.appliance.getNetworkApplianceTrafficShapingCustomPerformanceClasses(network_id)
            
            output = ["⚡ Custom Performance Classes", "=" * 50, ""]
            
            if classes:
                for pc in classes:
                    output.append(f"🎯 {pc.get('name', 'Unnamed Class')}")
                    
                    if 'maxJitter' in pc:
                        output.append(f"  Max Jitter: {pc['maxJitter']} ms")
                    
                    if 'maxLatency' in pc:
                        output.append(f"  Max Latency: {pc['maxLatency']} ms")
                    
                    if 'maxLossPercentage' in pc:
                        output.append(f"  Max Loss: {pc['maxLossPercentage']}%")
                    
                    if 'type' in pc:
                        output.append(f"  Type: {pc['type']}")
                    
                    output.append("")
            else:
                output.append("No custom performance classes configured")
            
            # Suggested classes
            output.extend([
                "💡 Suggested Performance Classes:",
                "  • VoIP: Jitter < 30ms, Latency < 150ms, Loss < 1%",
                "  • Video: Jitter < 50ms, Latency < 200ms, Loss < 1%",
                "  • Gaming: Jitter < 20ms, Latency < 100ms, Loss < 0.5%",
                "  • Business Apps: Latency < 300ms, Loss < 2%"
            ])
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("get custom performance classes", e)


def create_traffic_shaping_custom_performance_class(
    network_id: str,
    name: str,
    max_jitter: Optional[int] = None,
    max_latency: Optional[int] = None,
    max_loss_percentage: Optional[float] = None
) -> str:
    """
    ➕ Create a custom performance class for traffic shaping.
    
    Define QoS requirements for specific applications.
    
    Args:
        network_id: Network ID
        name: Name for the performance class
        max_jitter: Maximum jitter in milliseconds
        max_latency: Maximum latency in milliseconds
        max_loss_percentage: Maximum packet loss percentage
        
    Examples:
        Create VoIP class:
        name="VoIP Traffic" max_jitter=30 max_latency=150 max_loss_percentage=1.0
        
        Create gaming class:
        name="Gaming" max_jitter=20 max_latency=100 max_loss_percentage=0.5
        
    Returns:
        Creation status
    """
    try:
        with safe_api_call("create custom performance class"):
            class_data = {"name": name}
            
            if max_jitter is not None:
                class_data['maxJitter'] = max_jitter
            
            if max_latency is not None:
                class_data['maxLatency'] = max_latency
            
            if max_loss_percentage is not None:
                class_data['maxLossPercentage'] = max_loss_percentage
            
            result = meraki.dashboard.appliance.createNetworkApplianceTrafficShapingCustomPerformanceClass(
                network_id,
                **class_data
            )
            
            return f"✅ Created performance class '{name}' (ID: {result.get('id', 'Unknown')})"
            
    except Exception as e:
        return format_error("create custom performance class", e)


def update_traffic_shaping_vpn_exclusions(
    network_id: str,
    custom_exclusions: Optional[str] = None,
    major_applications: Optional[str] = None
) -> str:
    """
    🚫 Update VPN exclusion rules for split tunneling.
    
    Exclude specific traffic from VPN tunnel.
    
    Args:
        network_id: Network ID
        custom_exclusions: JSON array of custom exclusions
        major_applications: JSON array of major apps to exclude
        
    Examples:
        Exclude Microsoft 365:
        major_applications='[{
            "name": "Office 365",
            "id": "meraki:application/205"
        }]'
        
        Exclude custom IPs:
        custom_exclusions='[{
            "protocol": "tcp",
            "destination": "192.168.100.0/24",
            "port": "443"
        }]'
        
    Returns:
        Update status
    """
    try:
        with safe_api_call("update VPN exclusions"):
            update_data = {}
            
            if custom_exclusions:
                update_data['custom'] = json.loads(custom_exclusions)
            
            if major_applications:
                update_data['majorApplications'] = json.loads(major_applications)
            
            if not update_data:
                return "❌ No exclusions specified"
            
            meraki.dashboard.appliance.updateNetworkApplianceTrafficShapingVpnExclusions(
                network_id,
                **update_data
            )
            
            return "✅ VPN exclusions updated successfully"
            
    except json.JSONDecodeError as e:
        return f"❌ Invalid JSON: {e}"
    except Exception as e:
        return format_error("update VPN exclusions", e)


def get_traffic_shaping_application_categories() -> str:
    """
    📱 Get all available application categories for traffic shaping.
    
    Lists categories that can be used in traffic rules.
    
    Returns:
        Available application categories
    """
    try:
        with safe_api_call("get application categories"):
            # Note: Application categories are shared with L7 firewall
            # This is a helper that shows which apps can be used in traffic shaping
            categories = {'applicationCategories': [
                {'id': 'meraki:layer7/category/1', 'name': 'Blogging'},
                {'id': 'meraki:layer7/category/2', 'name': 'Business and economy'},
                {'id': 'meraki:layer7/category/3', 'name': 'Education'},
                {'id': 'meraki:layer7/category/4', 'name': 'File sharing'},
                {'id': 'meraki:layer7/category/5', 'name': 'Games'},
                {'id': 'meraki:layer7/category/6', 'name': 'Instant messaging'},
                {'id': 'meraki:layer7/category/7', 'name': 'Social web & photo sharing'},
                {'id': 'meraki:layer7/category/8', 'name': 'Video & music'},
                {'id': 'meraki:layer7/category/9', 'name': 'Web and email'},
                {'id': 'meraki:layer7/category/10', 'name': 'Network protocols'},
                {'id': 'meraki:layer7/category/11', 'name': 'Proxy avoidance'},
                {'id': 'meraki:layer7/category/12', 'name': 'Software updates'},
            ]}
            
            output = ["📱 Application Categories", "=" * 50, ""]
            
            if categories and 'applicationCategories' in categories:
                # Group by type for better organization
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
            else:
                output.append("No application categories available")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("get application categories", e)


# Helper tool
def check_traffic_shaping_prerequisites(network_id: str) -> str:
    """
    🔍 Check if traffic shaping is supported on this network.
    
    ALWAYS RUN THIS FIRST before using traffic shaping tools!
    
    Args:
        network_id: Network ID to check
        
    Returns:
        Prerequisites status and guidance
    """
    try:
        output = ["🔍 Traffic Shaping Prerequisites Check", "=" * 50, ""]
        
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
                output.append("   Traffic shaping requires an MX device")
                return "\n".join(output)
        except:
            output.append("⚠️ Could not verify MX appliance")
        
        # Check current rules
        try:
            rules = meraki.dashboard.appliance.getNetworkApplianceTrafficShapingRules(network_id)
            output.append("\n✅ Traffic shaping is available")
            
            rule_count = len(rules.get('rules', []))
            output.append(f"   Current rules: {rule_count}")
            
            if rules.get('defaultRulesEnabled'):
                output.append("   Default rules: Enabled")
        except Exception as e:
            if "404" in str(e):
                output.append("\n❌ Traffic shaping not available")
                output.append("   This network may not support traffic shaping")
            else:
                output.append(f"\n⚠️ Could not check rules: {str(e)}")
        
        # License check
        output.extend([
            "\n📋 License Requirements:",
            "   • Enterprise or Advanced Security license required",
            "   • SD-WAN Plus license for advanced features"
        ])
        
        # Recommendations
        output.extend([
            "\n💡 Next Steps:",
            "1. Use get_network_traffic_shaping_rules() to view current config",
            "2. Use get_traffic_shaping_application_categories() to see available apps",
            "3. Create rules with update_network_traffic_shaping_rules()"
        ])
        
        return "\n".join(output)
        
    except Exception as e:
        return format_error("check prerequisites", e)


def register_traffic_shaping_tools(app: FastMCP, client: MerakiClient):
    """Register traffic shaping tools with the MCP server."""
    global mcp_app, meraki
    mcp_app = app
    meraki = client
    
    # Register all tools
    app.tool()(get_network_traffic_shaping_rules)
    app.tool()(update_network_traffic_shaping_rules)
    app.tool()(get_network_traffic_shaping_uplink_selection)
    app.tool()(update_network_traffic_shaping_uplink_selection)
    app.tool()(get_network_traffic_shaping_dscp_tagging)
    app.tool()(get_network_traffic_shaping_custom_performance_classes)
    app.tool()(create_traffic_shaping_custom_performance_class)
    app.tool()(update_traffic_shaping_vpn_exclusions)
    app.tool()(get_traffic_shaping_application_categories)
    app.tool()(check_traffic_shaping_prerequisites)