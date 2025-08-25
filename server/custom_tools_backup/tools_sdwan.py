"""
SD-WAN Policy Tools for Cisco Meraki MCP Server
Manage SD-WAN policies, traffic steering, and VPN configurations
"""

from mcp.server import FastMCP
from typing import Optional, Dict, Any, List
import json
from datetime import datetime
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


def get_network_appliance_sdwan_internet_policies(network_id: str) -> str:
    """
    🌐 Get SD-WAN internet traffic policies.
    
    Shows policies for steering internet-bound traffic across WAN uplinks.
    
    Args:
        network_id: Network ID
    
    Returns:
        SD-WAN internet traffic policies
    """
    try:
        with safe_api_call("get SD-WAN internet policies"):
            # Get general uplink settings first
            try:
                uplink_settings = meraki.dashboard.appliance.getNetworkApplianceTrafficShapingUplinkSelection(network_id)
            except:
                uplink_settings = None
            
            output = ["🌐 SD-WAN Internet Policies", "=" * 50, ""]
            output.append(f"Network: {network_id}")
            output.append("")
            
            # Show uplink selection settings
            if uplink_settings:
                # Active uplink
                active_uplink = uplink_settings.get('activeActiveAutoVpnEnabled', False)
                output.append(f"Active-Active Auto VPN: {'✅ Enabled' if active_uplink else '❌ Disabled'}")
                
                # Default uplink
                default_uplink = uplink_settings.get('defaultUplink', 'wan1')
                output.append(f"Default Uplink: {default_uplink.upper()}")
                
                # Load balancing
                load_balancing = uplink_settings.get('loadBalancingEnabled', False)
                output.append(f"Load Balancing: {'✅ Enabled' if load_balancing else '❌ Disabled'}")
                
                # Failover and failback
                failover = uplink_settings.get('failoverAndFailback', {})
                if failover:
                    output.append("\n⚡ Failover Settings:")
                    output.append(f"   Immediate Failback: {'Yes' if failover.get('immediate', {}).get('enabled') else 'No'}")
                
                output.append("")
                
                # WAN traffic preferences
                wan_preferences = uplink_settings.get('wanTrafficUplinkPreferences', [])
                if wan_preferences:
                    output.append("📋 Traffic Preferences:")
                    
                    for i, pref in enumerate(wan_preferences, 1):
                        traffic_filters = pref.get('trafficFilters', [])
                        preferred_uplink = pref.get('preferredUplink', 'default')
                        
                        output.append(f"\n{i}. Policy:")
                        output.append(f"   Preferred Uplink: {preferred_uplink.upper()}")
                        
                        # Show traffic filters
                        if traffic_filters:
                            output.append("   Traffic Filters:")
                            for filter_item in traffic_filters:
                                filter_type = filter_item.get('type', 'custom')
                                value = filter_item.get('value', {})
                                
                                if filter_type == 'application':
                                    output.append(f"      • Application: {value.get('name', 'Unknown')}")
                                elif filter_type == 'custom':
                                    protocol = value.get('protocol', 'any')
                                    output.append(f"      • Custom: {protocol}")
                                    if value.get('source'):
                                        output.append(f"        Source: {value['source'].get('cidr', 'any')}")
                                    if value.get('destination'):
                                        output.append(f"        Dest: {value['destination'].get('cidr', 'any')}")
                
                # VPN traffic preferences
                vpn_preferences = uplink_settings.get('vpnTrafficUplinkPreferences', [])
                if vpn_preferences:
                    output.append("\n🔒 VPN Traffic Preferences:")
                    
                    for i, pref in enumerate(vpn_preferences, 1):
                        traffic_filters = pref.get('trafficFilters', [])
                        preferred_uplink = pref.get('preferredUplink', 'default')
                        failover_preset = pref.get('failOverCriterion', 'poorPerformance')
                        performance_class = pref.get('performanceClass', {})
                        
                        output.append(f"\n{i}. VPN Policy:")
                        output.append(f"   Preferred Uplink: {preferred_uplink.upper()}")
                        output.append(f"   Failover: {failover_preset}")
                        
                        if performance_class.get('type') == 'custom':
                            output.append("   Performance Thresholds:")
                            criteria = performance_class.get('customPerformanceClass', {}).get('criteria', {})
                            if criteria.get('latency'):
                                output.append(f"      Latency: {criteria['latency']}ms")
                            if criteria.get('jitter'):
                                output.append(f"      Jitter: {criteria['jitter']}ms")
                            if criteria.get('packetLoss'):
                                output.append(f"      Packet Loss: {criteria['packetLoss']}%")
            
            # SD-WAN benefits
            output.append("\n💡 SD-WAN Benefits:")
            output.append("• Automatic failover")
            output.append("• Load balancing")
            output.append("• Application steering")
            output.append("• Performance-based routing")
            output.append("• VPN optimization")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("get SD-WAN internet policies", e)


def update_network_appliance_sdwan_internet_policies(
    network_id: str,
    wan_traffic_preferences: List[Dict[str, Any]],
    vpn_traffic_preferences: Optional[List[Dict[str, Any]]] = None
) -> str:
    """
    ✏️ Update SD-WAN internet traffic policies.
    
    Configure how traffic is steered across WAN uplinks.
    
    Args:
        network_id: Network ID
        wan_traffic_preferences: WAN traffic steering rules
        vpn_traffic_preferences: VPN traffic steering rules
    
    Returns:
        Updated policy configuration
    """
    try:
        with safe_api_call("update SD-WAN internet policies"):
            # Build update data
            update_data = {
                "wanTrafficUplinkPreferences": wan_traffic_preferences
            }
            
            if vpn_traffic_preferences is not None:
                update_data["vpnTrafficUplinkPreferences"] = vpn_traffic_preferences
            
            # Update the policies
            result = meraki.dashboard.appliance.updateNetworkApplianceTrafficShapingUplinkSelection(
                network_id,
                **update_data
            )
            
            output = ["✏️ SD-WAN Policies Updated", "=" * 50, ""]
            output.append(f"Network: {network_id}")
            output.append("")
            
            # Show updated WAN preferences
            if wan_traffic_preferences:
                output.append(f"📋 WAN Traffic Policies: {len(wan_traffic_preferences)}")
                
                for i, pref in enumerate(wan_traffic_preferences[:3], 1):
                    output.append(f"\n{i}. Uplink: {pref.get('preferredUplink', 'default').upper()}")
                    
                    filters = pref.get('trafficFilters', [])
                    if filters:
                        output.append("   Matches:")
                        for f in filters[:2]:
                            if f.get('type') == 'application':
                                output.append(f"      • App: {f.get('value', {}).get('name', 'Unknown')}")
                            elif f.get('type') == 'custom':
                                output.append("      • Custom filter")
                
                if len(wan_traffic_preferences) > 3:
                    output.append(f"\n... and {len(wan_traffic_preferences) - 3} more policies")
            
            # Show updated VPN preferences
            if vpn_traffic_preferences:
                output.append(f"\n🔒 VPN Traffic Policies: {len(vpn_traffic_preferences)}")
            
            output.append("\n✅ Configuration Applied")
            output.append("\n⚠️ Note: Changes may take a few minutes to propagate")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("update SD-WAN internet policies", e)


def get_organization_appliance_vpn_third_party_vpn_peers(org_id: str) -> str:
    """
    🔐 Get third-party VPN peers.
    
    Lists non-Meraki VPN peers for SD-WAN integration.
    
    Args:
        org_id: Organization ID
    
    Returns:
        Third-party VPN peer configurations
    """
    try:
        with safe_api_call("get third-party VPN peers"):
            peers = meraki.dashboard.appliance.getOrganizationApplianceVpnThirdPartyVPNPeers(org_id)
            
            output = ["🔐 Third-Party VPN Peers", "=" * 50, ""]
            output.append(f"Organization: {org_id}")
            output.append("")
            
            peer_list = peers.get('peers', [])
            if not peer_list:
                output.append("No third-party VPN peers configured")
                output.append("\n💡 Use update_organization_appliance_vpn_third_party_vpn_peers() to add")
                return "\n".join(output)
            
            output.append(f"Total Peers: {len(peer_list)}")
            output.append("")
            
            # Show each peer
            for i, peer in enumerate(peer_list, 1):
                name = peer.get('name', 'Unnamed Peer')
                public_ip = peer.get('publicIp', 'Unknown')
                ike_version = peer.get('ikeVersion', '1')
                
                output.append(f"{i}. 🏢 {name}")
                output.append(f"   Public IP: {public_ip}")
                output.append(f"   IKE Version: {ike_version}")
                
                # Remote networks
                remote_networks = peer.get('privateSubnets', [])
                if remote_networks:
                    output.append("   Remote Networks:")
                    for subnet in remote_networks[:3]:
                        output.append(f"      • {subnet}")
                    if len(remote_networks) > 3:
                        output.append(f"      ... and {len(remote_networks) - 3} more")
                
                # IPsec policies
                ipsec_policies = peer.get('ipsecPolicies', {})
                if ipsec_policies:
                    output.append("   IPsec Settings:")
                    
                    # IKE (Phase 1)
                    ike = ipsec_policies.get('ikeCipherAlgo', [])
                    if ike:
                        output.append(f"      Phase 1: {', '.join(ike)}")
                    
                    # ESP (Phase 2)
                    esp = ipsec_policies.get('espCipherAlgo', [])
                    if esp:
                        output.append(f"      Phase 2: {', '.join(esp)}")
                
                # Tags
                if peer.get('networkTags'):
                    output.append(f"   Tags: {', '.join(peer['networkTags'])}")
                
                output.append("")
            
            # IPsec settings
            output.append("🔧 Global IPsec Settings:")
            if peers.get('ipsecPoliciesPreset'):
                output.append(f"   Preset: {peers['ipsecPoliciesPreset']}")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("get third-party VPN peers", e)


def update_organization_appliance_vpn_third_party_vpn_peers(
    org_id: str,
    peers: List[Dict[str, Any]]
) -> str:
    """
    ✏️ Update third-party VPN peers.
    
    Configure non-Meraki VPN peers for hybrid SD-WAN.
    
    Args:
        org_id: Organization ID
        peers: List of VPN peer configurations
    
    Returns:
        Updated VPN peer configuration
    """
    try:
        with safe_api_call("update third-party VPN peers"):
            # Update the peers
            result = meraki.dashboard.appliance.updateOrganizationApplianceVpnThirdPartyVPNPeers(
                org_id,
                peers=peers
            )
            
            output = ["✏️ Third-Party VPN Peers Updated", "=" * 50, ""]
            output.append(f"Organization: {org_id}")
            output.append("")
            
            # Show updated peers
            updated_peers = result.get('peers', [])
            output.append(f"Total Peers: {len(updated_peers)}")
            
            for i, peer in enumerate(updated_peers[:5], 1):
                output.append(f"\n{i}. {peer.get('name', 'Unnamed')}")
                output.append(f"   IP: {peer.get('publicIp', 'Unknown')}")
                output.append(f"   IKE: v{peer.get('ikeVersion', '1')}")
                
                # Count subnets
                subnets = peer.get('privateSubnets', [])
                if subnets:
                    output.append(f"   Subnets: {len(subnets)}")
            
            if len(updated_peers) > 5:
                output.append(f"\n... and {len(updated_peers) - 5} more peers")
            
            output.append("\n✅ Configuration Applied")
            output.append("\n🔄 Next Steps:")
            output.append("• Configure matching settings on peer device")
            output.append("• Verify IPsec policies match")
            output.append("• Test VPN connectivity")
            output.append("• Monitor VPN status")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("update third-party VPN peers", e)


def get_traffic_shaping_performance_classes(network_id: str) -> str:
    """
    📊 Get custom performance classes.
    
    Shows custom performance thresholds for SD-WAN traffic steering.
    
    Args:
        network_id: Network ID
    
    Returns:
        Custom performance class definitions
    """
    try:
        with safe_api_call("get custom performance classes"):
            classes = meraki.dashboard.appliance.getNetworkApplianceTrafficShapingCustomPerformanceClasses(network_id)
            
            output = ["📊 Custom Performance Classes", "=" * 50, ""]
            output.append(f"Network: {network_id}")
            output.append("")
            
            if not classes:
                output.append("No custom performance classes defined")
                output.append("\n💡 Custom classes allow fine-tuned SD-WAN failover")
                return "\n".join(output)
            
            # Show each class
            for i, perf_class in enumerate(classes, 1):
                class_id = perf_class.get('id', 'Unknown')
                name = perf_class.get('name', 'Unnamed Class')
                
                output.append(f"{i}. 🎯 {name}")
                output.append(f"   ID: {class_id}")
                
                # Thresholds
                criteria = perf_class.get('criteria', {})
                if criteria:
                    output.append("   Thresholds:")
                    
                    if criteria.get('latency'):
                        output.append(f"      Latency: ≤ {criteria['latency']}ms")
                    
                    if criteria.get('jitter'):
                        output.append(f"      Jitter: ≤ {criteria['jitter']}ms")
                    
                    if criteria.get('packetLoss'):
                        output.append(f"      Packet Loss: ≤ {criteria['packetLoss']}%")
                
                output.append("")
            
            # Usage guide
            output.append("💡 Performance Class Usage:")
            output.append("• Assign to VPN traffic policies")
            output.append("• Define failover thresholds")
            output.append("• Create SLA-based routing")
            output.append("• Monitor performance metrics")
            
            output.append("\n📈 Common Profiles:")
            output.append("• VoIP: Latency <150ms, Jitter <30ms, Loss <1%")
            output.append("• Video: Latency <200ms, Jitter <50ms, Loss <2%")
            output.append("• Data: Latency <500ms, Loss <5%")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("get custom performance classes", e)


def create_traffic_shaping_performance_class(
    network_id: str,
    name: str,
    max_latency: Optional[int] = None,
    max_jitter: Optional[int] = None,
    max_packet_loss: Optional[float] = None
) -> str:
    """
    ➕ Create custom performance class.
    
    Define performance thresholds for SD-WAN failover decisions.
    
    Args:
        network_id: Network ID
        name: Class name
        max_latency: Maximum latency in ms
        max_jitter: Maximum jitter in ms
        max_packet_loss: Maximum packet loss percentage
    
    Returns:
        Created performance class details
    """
    try:
        with safe_api_call("create custom performance class"):
            # Build criteria
            criteria = {}
            if max_latency is not None:
                criteria['latency'] = max_latency
            if max_jitter is not None:
                criteria['jitter'] = max_jitter
            if max_packet_loss is not None:
                criteria['packetLoss'] = max_packet_loss
            
            if not criteria:
                return "❌ At least one threshold must be specified"
            
            # Create the class
            perf_class = meraki.dashboard.appliance.createNetworkApplianceTrafficShapingCustomPerformanceClass(
                network_id,
                name=name,
                criteria=criteria
            )
            
            output = ["✅ Performance Class Created", "=" * 50, ""]
            output.append(f"Name: {perf_class.get('name', name)}")
            output.append(f"ID: {perf_class.get('id', 'N/A')}")
            output.append("")
            
            output.append("📊 Thresholds:")
            result_criteria = perf_class.get('criteria', {})
            if result_criteria.get('latency'):
                output.append(f"   Latency: ≤ {result_criteria['latency']}ms")
            if result_criteria.get('jitter'):
                output.append(f"   Jitter: ≤ {result_criteria['jitter']}ms")
            if result_criteria.get('packetLoss'):
                output.append(f"   Packet Loss: ≤ {result_criteria['packetLoss']}%")
            
            output.append("\n🚀 Next Steps:")
            output.append("1. Apply to VPN traffic policies")
            output.append("2. Configure uplink preferences")
            output.append("3. Test failover behavior")
            output.append("4. Monitor performance metrics")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("create custom performance class", e)


def analyze_sdwan_performance(network_id: str) -> str:
    """
    📈 Analyze SD-WAN performance and recommendations.
    
    Provides insights on WAN link usage and optimization opportunities.
    
    Args:
        network_id: Network ID
    
    Returns:
        SD-WAN performance analysis
    """
    try:
        with safe_api_call("analyze SD-WAN performance"):
            output = ["📈 SD-WAN Performance Analysis", "=" * 50, ""]
            output.append(f"Network: {network_id}")
            output.append("")
            
            # Get uplink status
            try:
                device_statuses = meraki.dashboard.appliance.getOrganizationApplianceUplinkStatuses(
                    meraki.dashboard.networks.getNetwork(network_id).get('organizationId')
                )
                
                # Find devices in this network
                network_devices = [d for d in device_statuses 
                                 if d.get('networkId') == network_id]
                
                if network_devices:
                    output.append("🔗 WAN Uplink Status:")
                    
                    for device in network_devices:
                        serial = device.get('serial', 'Unknown')
                        
                        for uplink in device.get('uplinks', []):
                            interface = uplink.get('interface', 'Unknown')
                            status = uplink.get('status', 'Unknown')
                            
                            # Status icon
                            if status == 'active':
                                icon = '🟢'
                            elif status == 'ready':
                                icon = '🟡'
                            else:
                                icon = '🔴'
                            
                            output.append(f"\n{icon} {interface.upper()}")
                            output.append(f"   Status: {status}")
                            
                            if uplink.get('ip'):
                                output.append(f"   IP: {uplink['ip']}")
                            
                            if uplink.get('provider'):
                                output.append(f"   ISP: {uplink['provider']}")
                            
                            # Performance metrics if available
                            if uplink.get('latencyMs'):
                                output.append(f"   Latency: {uplink['latencyMs']}ms")
                            
                            if uplink.get('lossPercent') is not None:
                                output.append(f"   Loss: {uplink['lossPercent']}%")
            except:
                output.append("Unable to retrieve uplink status")
            
            # Get traffic shaping settings
            try:
                uplink_selection = meraki.dashboard.appliance.getNetworkApplianceTrafficShapingUplinkSelection(network_id)
                
                output.append("\n⚙️ SD-WAN Configuration:")
                
                # Active-active
                if uplink_selection.get('activeActiveAutoVpnEnabled'):
                    output.append("   ✅ Active-Active VPN enabled")
                
                # Load balancing
                if uplink_selection.get('loadBalancingEnabled'):
                    output.append("   ✅ Load balancing enabled")
                else:
                    output.append("   ❌ Load balancing disabled")
                
                # Policy count
                wan_prefs = uplink_selection.get('wanTrafficUplinkPreferences', [])
                vpn_prefs = uplink_selection.get('vpnTrafficUplinkPreferences', [])
                
                output.append(f"   📋 WAN policies: {len(wan_prefs)}")
                output.append(f"   🔒 VPN policies: {len(vpn_prefs)}")
            except:
                pass
            
            # Recommendations
            output.append("\n💡 SD-WAN Optimization Tips:")
            output.append("• Enable load balancing for better utilization")
            output.append("• Create policies for critical applications")
            output.append("• Use custom performance classes for SLAs")
            output.append("• Monitor uplink performance regularly")
            output.append("• Configure automatic failover")
            output.append("• Test failover scenarios monthly")
            
            output.append("\n📊 Best Practices:")
            output.append("• VoIP → Low latency uplink")
            output.append("• Backup → Secondary uplink")
            output.append("• General traffic → Load balanced")
            output.append("• Critical apps → Primary with quick failover")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("analyze SD-WAN performance", e)


def sdwan_policy_examples() -> str:
    """
    📚 Show SD-WAN policy examples.
    
    Provides example configurations for common SD-WAN scenarios.
    
    Returns:
        SD-WAN policy examples
    """
    output = ["📚 SD-WAN Policy Examples", "=" * 50, ""]
    
    output.append("1️⃣ VoIP Traffic Steering:")
    output.append("""
wan_traffic_preferences = [{
    "preferredUplink": "wan1",
    "trafficFilters": [{
        "type": "application",
        "value": {
            "id": "voip",
            "name": "VoIP & Video Conferencing"
        }
    }]
}]
""")
    
    output.append("\n2️⃣ Guest Traffic to Secondary WAN:")
    output.append("""
wan_traffic_preferences = [{
    "preferredUplink": "wan2",
    "trafficFilters": [{
        "type": "custom",
        "value": {
            "protocol": "any",
            "source": {
                "cidr": "192.168.100.0/24",
                "description": "Guest VLAN"
            }
        }
    }]
}]
""")
    
    output.append("\n3️⃣ VPN with Custom Performance:")
    output.append("""
vpn_traffic_preferences = [{
    "preferredUplink": "wan1",
    "failOverCriterion": "custom",
    "performanceClass": {
        "type": "custom",
        "customPerformanceClass": {
            "criteria": {
                "latency": 150,
                "jitter": 30,
                "packetLoss": 1.0
            }
        }
    },
    "trafficFilters": [{
        "type": "custom",
        "value": {
            "protocol": "any",
            "destination": {
                "cidr": "10.0.0.0/8"
            }
        }
    }]
}]
""")
    
    output.append("\n4️⃣ Application-Based Load Balancing:")
    output.append("""
# Streaming to WAN1
{
    "preferredUplink": "wan1",
    "trafficFilters": [{
        "type": "application",
        "value": {"name": "Video Streaming"}
    }]
},
# Cloud apps to WAN2
{
    "preferredUplink": "wan2",
    "trafficFilters": [{
        "type": "application",
        "value": {"name": "Cloud Storage"}
    }]
}
""")
    
    output.append("\n💡 Policy Guidelines:")
    output.append("• Order matters - first match wins")
    output.append("• Be specific with filters")
    output.append("• Test failover behavior")
    output.append("• Monitor policy hits")
    output.append("• Document policy purpose")
    
    return "\n".join(output)


def sdwan_help() -> str:
    """
    ❓ Get help with SD-WAN tools.
    
    Shows available tools and best practices.
    
    Returns:
        Formatted help guide
    """
    return """🌐 SD-WAN Policy Tools Help
==================================================

Available tools for SD-WAN configuration:

1. get_network_appliance_sdwan_internet_policies()
   - View current policies
   - Traffic preferences
   - Failover settings
   - Load balancing status

2. update_network_appliance_sdwan_internet_policies()
   - Configure traffic steering
   - Set uplink preferences
   - Define failover criteria
   - Application routing

3. get_organization_appliance_vpn_third_party_vpn_peers()
   - List non-Meraki VPN peers
   - IPsec configurations
   - Remote networks
   - Hybrid connectivity

4. update_organization_appliance_vpn_third_party_vpn_peers()
   - Add VPN peers
   - Configure IPsec
   - Set remote subnets
   - Enable hybrid WAN

5. get_traffic_shaping_performance_classes()
   - View SLA definitions
   - Performance thresholds
   - Failover criteria
   - Custom classes

6. create_traffic_shaping_performance_class()
   - Define SLA thresholds
   - Set performance metrics
   - Create failover rules
   - Custom routing logic

7. analyze_sdwan_performance()
   - WAN link status
   - Performance metrics
   - Configuration review
   - Optimization tips

8. sdwan_policy_examples()
   - Common configurations
   - Best practices
   - Policy templates
   - Use case examples

SD-WAN Features:
• Automatic failover
• Load balancing
• Application steering
• Performance routing
• VPN optimization
• Hybrid WAN support

Policy Types:
• WAN traffic policies
• VPN traffic policies
• Custom performance
• Application-based
• Source-based
• Destination-based

Performance Metrics:
• Latency (ms)
• Jitter (ms)
• Packet loss (%)
• Bandwidth usage
• Connection state

Best Practices:
• Enable load balancing
• Define clear policies
• Test failover regularly
• Monitor performance
• Document changes
• Use custom classes

Common Use Cases:
• VoIP prioritization
• Guest segregation
• Cloud app steering
• Backup optimization
• Branch connectivity
• Disaster recovery

Troubleshooting:
• Check uplink status
• Verify policy order
• Test with traceroute
• Monitor statistics
• Review event logs
• Validate IPsec
"""


def register_sdwan_tools(app: FastMCP, meraki_client: MerakiClient):
    """Register all SD-WAN policy tools with the MCP server."""
    global mcp_app, meraki
    mcp_app = app
    meraki = meraki_client
    
    # Register all tools
    tools = [
        (get_network_appliance_sdwan_internet_policies, "Get SD-WAN internet policies"),
        (update_network_appliance_sdwan_internet_policies, "Update SD-WAN policies"),
        (get_organization_appliance_vpn_third_party_vpn_peers, "Get third-party VPN peers"),
        (update_organization_appliance_vpn_third_party_vpn_peers, "Update VPN peers"),
        (get_traffic_shaping_performance_classes, "Get custom performance classes"),
        (create_traffic_shaping_performance_class, "Create performance class"),
        (analyze_sdwan_performance, "Analyze SD-WAN performance"),
        (sdwan_policy_examples, "Show SD-WAN policy examples"),
        (sdwan_help, "Get help with SD-WAN tools"),
    ]
    
    for tool_func, description in tools:
        app.tool(
            name=tool_func.__name__,
            description=description
        )(tool_func)