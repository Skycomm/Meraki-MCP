"""
Troubleshooting Dashboard for Cisco Meraki MCP Server
Diagnose connectivity issues, performance problems, and configuration conflicts
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


def diagnose_connectivity_issues(
    network_id: str,
    client_mac: Optional[str] = None,
    timespan: Optional[int] = 3600
) -> str:
    """
    🔍 Diagnose network connectivity issues.
    
    Analyzes common connectivity problems and provides recommendations.
    
    Args:
        network_id: Network ID to diagnose
        client_mac: Specific client MAC to diagnose (optional)
        timespan: Time period in seconds (default: 3600 = 1 hour)
        
    Returns:
        Connectivity diagnosis report
    """
    try:
        output = ["🔍 Connectivity Diagnosis", "=" * 50, ""]
        issues_found = []
        
        # 1. Check device connectivity
        try:
            with safe_api_call("check device status"):
                devices = meraki.dashboard.networks.getNetworkDevices(network_id)
                offline_devices = []
                
                for device in devices:
                    try:
                        status = meraki.dashboard.organizations.getOrganizationDevicesStatuses(
                            device.get('organizationId', network_id),
                            serials=[device['serial']]
                        )
                        if status and status[0].get('status') != 'online':
                            offline_devices.append(device)
                    except:
                        pass
                
                if offline_devices:
                    issues_found.append("offline_devices")
                    output.append("⚠️ OFFLINE DEVICES DETECTED:")
                    for dev in offline_devices:
                        output.append(f"   - {dev.get('name', 'Unknown')} ({dev['model']})")
                        output.append(f"     Serial: {dev['serial']}")
                    output.append("")
                else:
                    output.append("✅ All devices online")
                    output.append("")
        except:
            output.append("⚠️ Could not check device status")
            output.append("")
        
        # 2. Check client connectivity stats
        if not client_mac:
            try:
                with safe_api_call("check connection stats"):
                    conn_stats = meraki.dashboard.networks.getNetworkConnectionStats(
                        network_id,
                        timespan=timespan
                    )
                    
                    if conn_stats:
                        output.append("📊 Connection Statistics:")
                        
                        # Calculate success rates
                        assoc = conn_stats.get('assoc', 0)
                        auth = conn_stats.get('auth', 0)
                        dhcp = conn_stats.get('dhcp', 0)
                        dns = conn_stats.get('dns', 0)
                        success = conn_stats.get('success', 0)
                        
                        # Check for issues at each stage
                        if assoc > 0:
                            auth_rate = (auth/assoc*100) if assoc > 0 else 0
                            dhcp_rate = (dhcp/auth*100) if auth > 0 else 0
                            dns_rate = (dns/dhcp*100) if dhcp > 0 else 0
                            success_rate = (success/dns*100) if dns > 0 else 0
                            
                            output.append(f"   Association → Auth: {auth_rate:.1f}%")
                            output.append(f"   Auth → DHCP: {dhcp_rate:.1f}%")
                            output.append(f"   DHCP → DNS: {dns_rate:.1f}%")
                            output.append(f"   DNS → Success: {success_rate:.1f}%")
                            
                            # Identify bottlenecks
                            if auth_rate < 90:
                                issues_found.append("auth_failures")
                                output.append("   ⚠️ Authentication issues detected")
                            if dhcp_rate < 95:
                                issues_found.append("dhcp_failures")
                                output.append("   ⚠️ DHCP issues detected")
                            if dns_rate < 95:
                                issues_found.append("dns_failures")
                                output.append("   ⚠️ DNS resolution issues detected")
                        
                        output.append("")
            except:
                pass
        
        # 3. Check specific client if provided
        if client_mac:
            try:
                with safe_api_call("check client details"):
                    clients = meraki.dashboard.networks.getNetworkClients(
                        network_id,
                        mac=client_mac,
                        timespan=timespan
                    )
                    
                    if clients:
                        client = clients[0]
                        output.append(f"📱 Client Analysis: {client.get('description', client_mac)}")
                        output.append(f"   Status: {client.get('status', 'Unknown')}")
                        output.append(f"   IP: {client.get('ip', 'No IP assigned')}")
                        output.append(f"   VLAN: {client.get('vlan', 'None')}")
                        output.append(f"   Connected to: {client.get('recentDeviceName', 'Unknown')}")
                        
                        # Check for issues
                        if not client.get('ip'):
                            issues_found.append("no_ip")
                            output.append("   ⚠️ No IP address assigned")
                        
                        if client.get('status') != 'Online':
                            issues_found.append("client_offline")
                            output.append("   ⚠️ Client not online")
                        
                        output.append("")
            except:
                output.append(f"⚠️ Could not find client {client_mac}")
                output.append("")
        
        # 4. Check network health indicators
        try:
            with safe_api_call("check network events"):
                events = meraki.dashboard.networks.getNetworkEvents(
                    network_id,
                    perPage=50,
                    includedEventTypes=['association_reject', 'auth_fail', 'dhcp_no_lease']
                )
                
                if events and 'events' in events:
                    error_events = events['events'][:10]
                    if error_events:
                        issues_found.append("error_events")
                        output.append("🚨 Recent Error Events:")
                        for event in error_events[:5]:
                            output.append(f"   - {event.get('type', 'Unknown')}")
                            output.append(f"     {event.get('description', '')}")
                            output.append(f"     Time: {event.get('occurredAt', '')}")
                        output.append("")
        except:
            pass
        
        # 5. Generate recommendations
        output.append("💡 DIAGNOSIS & RECOMMENDATIONS:")
        output.append("=" * 50)
        
        if not issues_found:
            output.append("✅ No connectivity issues detected")
            output.append("   Network appears to be functioning normally")
        else:
            if "offline_devices" in issues_found:
                output.append("\n🔧 Offline Devices:")
                output.append("   1. Check device power and cabling")
                output.append("   2. Verify WAN/Internet connectivity")
                output.append("   3. Check for firmware issues")
                output.append("   4. Review device event logs")
            
            if "auth_failures" in issues_found:
                output.append("\n🔐 Authentication Failures:")
                output.append("   1. Verify RADIUS server connectivity")
                output.append("   2. Check WiFi passwords/PSK")
                output.append("   3. Review 802.1X certificates")
                output.append("   4. Check group policies")
            
            if "dhcp_failures" in issues_found:
                output.append("\n📡 DHCP Issues:")
                output.append("   1. Check DHCP pool exhaustion")
                output.append("   2. Verify VLAN configuration")
                output.append("   3. Review DHCP reservations")
                output.append("   4. Check DHCP relay settings")
            
            if "dns_failures" in issues_found:
                output.append("\n🌐 DNS Resolution Issues:")
                output.append("   1. Verify DNS server settings")
                output.append("   2. Check content filtering")
                output.append("   3. Test external connectivity")
                output.append("   4. Review firewall rules")
            
            if "no_ip" in issues_found:
                output.append("\n🏷️ No IP Assignment:")
                output.append("   1. Check DHCP server status")
                output.append("   2. Verify VLAN assignment")
                output.append("   3. Check for IP conflicts")
                output.append("   4. Review client isolation")
        
        # Add general tips
        output.extend([
            "\n📋 General Troubleshooting Steps:",
            "1. Run packet capture on affected devices",
            "2. Check switch port status and errors",
            "3. Review wireless channel utilization",
            "4. Verify upstream ISP connectivity",
            "5. Check for recent configuration changes"
        ])
        
        return "\n".join(output)
        
    except Exception as e:
        return format_error("diagnose connectivity", e)


def analyze_performance_bottlenecks(
    network_id: str,
    timespan: Optional[int] = 3600
) -> str:
    """
    🚀 Analyze network performance bottlenecks.
    
    Identifies performance issues and their potential causes.
    
    Args:
        network_id: Network ID to analyze
        timespan: Time period in seconds (default: 3600 = 1 hour)
        
    Returns:
        Performance analysis report
    """
    try:
        output = ["🚀 Performance Bottleneck Analysis", "=" * 50, ""]
        bottlenecks = []
        
        # 1. Check bandwidth utilization
        try:
            with safe_api_call("check bandwidth"):
                devices = meraki.dashboard.networks.getNetworkDevices(network_id)
                mx_devices = [d for d in devices if d.get('model', '').startswith('MX')]
                
                if mx_devices:
                    for mx in mx_devices[:1]:  # Check first MX
                        try:
                            usage = meraki.dashboard.appliance.getNetworkApplianceUplinksUsageHistory(
                                network_id,
                                timespan=min(timespan, 3600),
                                resolution=300
                            )
                            
                            if usage:
                                output.append("📊 WAN Bandwidth Analysis:")
                                
                                # Analyze each interface
                                by_interface = {}
                                for entry in usage:
                                    interface = entry.get('interface', 'Unknown')
                                    if interface not in by_interface:
                                        by_interface[interface] = {
                                            'sent': [],
                                            'received': []
                                        }
                                    by_interface[interface]['sent'].append(entry.get('sent', 0))
                                    by_interface[interface]['received'].append(entry.get('received', 0))
                                
                                for interface, data in by_interface.items():
                                    if data['sent']:
                                        max_sent = max(data['sent'])
                                        max_recv = max(data['received'])
                                        avg_sent = sum(data['sent']) / len(data['sent'])
                                        avg_recv = sum(data['received']) / len(data['received'])
                                        
                                        output.append(f"\n   {interface}:")
                                        output.append(f"     Peak Upload: {max_sent/1000000:.1f} Mbps")
                                        output.append(f"     Peak Download: {max_recv/1000000:.1f} Mbps")
                                        output.append(f"     Avg Upload: {avg_sent/1000000:.1f} Mbps")
                                        output.append(f"     Avg Download: {avg_recv/1000000:.1f} Mbps")
                                        
                                        # Check for saturation (>80% of typical speeds)
                                        if max_sent > 80_000_000:  # 80 Mbps
                                            bottlenecks.append("upload_saturation")
                                            output.append("     ⚠️ High upload utilization detected")
                                        if max_recv > 400_000_000:  # 400 Mbps
                                            bottlenecks.append("download_saturation")
                                            output.append("     ⚠️ High download utilization detected")
                                
                                output.append("")
                        except:
                            pass
        except:
            output.append("⚠️ Could not analyze bandwidth utilization")
            output.append("")
        
        # 2. Check switch port utilization
        try:
            with safe_api_call("check switch ports"):
                switches = [d for d in devices if d.get('model', '').startswith('MS')]
                high_util_ports = []
                
                for switch in switches[:2]:  # Check first 2 switches
                    try:
                        port_statuses = meraki.dashboard.switch.getDeviceSwitchPortStatuses(
                            switch['serial'],
                            timespan=timespan
                        )
                        
                        for port in port_statuses:
                            if port.get('trafficInKbps', {}).get('total', 0) > 800000:  # 800 Mbps
                                high_util_ports.append({
                                    'switch': switch.get('name', switch['serial']),
                                    'port': port.get('portId'),
                                    'traffic': port['trafficInKbps']['total']
                                })
                    except:
                        pass
                
                if high_util_ports:
                    bottlenecks.append("switch_port_saturation")
                    output.append("⚠️ HIGH UTILIZATION SWITCH PORTS:")
                    for port_info in high_util_ports[:5]:
                        output.append(f"   - {port_info['switch']} Port {port_info['port']}")
                        output.append(f"     Traffic: {port_info['traffic']/1000:.1f} Mbps")
                    output.append("")
        except:
            pass
        
        # 3. Check wireless performance
        try:
            with safe_api_call("check wireless"):
                # Channel utilization
                channel_util = meraki.dashboard.networks.getNetworkWirelessChannelUtilizationHistory(
                    network_id,
                    timespan=min(timespan, 3600),
                    resolution=300
                )
                
                if channel_util:
                    output.append("📡 Wireless Performance:")
                    high_util_aps = []
                    
                    for entry in channel_util[-10:]:  # Last 10 entries
                        for ap_data in entry.get('byBand', []):
                            for band_data in ap_data.get('byChannel', []):
                                util = band_data.get('utilization', 0)
                                if util > 70:  # 70% channel utilization
                                    high_util_aps.append({
                                        'channel': band_data.get('channel'),
                                        'utilization': util
                                    })
                    
                    if high_util_aps:
                        bottlenecks.append("wireless_congestion")
                        output.append("   ⚠️ High channel utilization detected:")
                        channels = {}
                        for ap in high_util_aps:
                            ch = ap['channel']
                            if ch not in channels:
                                channels[ch] = []
                            channels[ch].append(ap['utilization'])
                        
                        for ch, utils in channels.items():
                            avg_util = sum(utils) / len(utils)
                            output.append(f"     Channel {ch}: {avg_util:.1f}% average")
                    else:
                        output.append("   ✅ Wireless channels operating normally")
                    output.append("")
        except:
            pass
        
        # 4. Check for packet loss
        try:
            with safe_api_call("check packet loss"):
                # Get loss data for MX devices
                if mx_devices:
                    loss_data = meraki.dashboard.devices.getDeviceLossAndLatencyHistory(
                        mx_devices[0]['serial'],
                        timespan=min(timespan, 300),  # Max 5 minutes
                        ip='8.8.8.8'
                    )
                    
                    if loss_data:
                        losses = [item.get('lossPercent', 0) for item in loss_data]
                        latencies = [item.get('latencyMs', 0) for item in loss_data]
                        
                        if losses:
                            avg_loss = sum(losses) / len(losses)
                            max_loss = max(losses)
                            avg_latency = sum(latencies) / len(latencies) if latencies else 0
                            max_latency = max(latencies) if latencies else 0
                            
                            output.append("🌐 WAN Performance (to 8.8.8.8):")
                            output.append(f"   Packet Loss: {avg_loss:.1f}% avg, {max_loss:.1f}% max")
                            output.append(f"   Latency: {avg_latency:.1f}ms avg, {max_latency:.1f}ms max")
                            
                            if avg_loss > 1:
                                bottlenecks.append("packet_loss")
                                output.append("   ⚠️ Significant packet loss detected")
                            if avg_latency > 100:
                                bottlenecks.append("high_latency")
                                output.append("   ⚠️ High latency detected")
                            
                            output.append("")
        except:
            pass
        
        # 5. Generate performance recommendations
        output.append("🎯 PERFORMANCE RECOMMENDATIONS:")
        output.append("=" * 50)
        
        if not bottlenecks:
            output.append("✅ No significant performance issues detected")
        else:
            if "upload_saturation" in bottlenecks or "download_saturation" in bottlenecks:
                output.append("\n📈 Bandwidth Saturation:")
                output.append("   1. Consider upgrading WAN bandwidth")
                output.append("   2. Implement traffic shaping/QoS")
                output.append("   3. Identify bandwidth-heavy applications")
                output.append("   4. Schedule large transfers off-peak")
            
            if "switch_port_saturation" in bottlenecks:
                output.append("\n🔌 Switch Port Congestion:")
                output.append("   1. Consider link aggregation (LACP)")
                output.append("   2. Upgrade to 10G connections")
                output.append("   3. Review VLAN segmentation")
                output.append("   4. Balance traffic across ports")
            
            if "wireless_congestion" in bottlenecks:
                output.append("\n📡 Wireless Congestion:")
                output.append("   1. Add more access points")
                output.append("   2. Enable band steering (5GHz)")
                output.append("   3. Adjust channel width (20/40/80MHz)")
                output.append("   4. Review RF profiles and power")
            
            if "packet_loss" in bottlenecks:
                output.append("\n📉 Packet Loss Issues:")
                output.append("   1. Contact ISP for line quality")
                output.append("   2. Check WAN cable/fiber connection")
                output.append("   3. Review WAN interface errors")
                output.append("   4. Test with alternate DNS")
            
            if "high_latency" in bottlenecks:
                output.append("\n⏱️ High Latency:")
                output.append("   1. Check for routing loops")
                output.append("   2. Optimize WAN failover settings")
                output.append("   3. Consider SD-WAN optimization")
                output.append("   4. Review VPN overhead")
        
        # Performance optimization tips
        output.extend([
            "\n💡 Performance Optimization Tips:",
            "• Enable adaptive policy for dynamic QoS",
            "• Use local DHCP instead of relay when possible",
            "• Implement broadcast storm control",
            "• Regular firmware updates for performance fixes",
            "• Monitor and optimize client density per AP"
        ])
        
        return "\n".join(output)
        
    except Exception as e:
        return format_error("analyze performance", e)


def check_configuration_conflicts(network_id: str) -> str:
    """
    ⚙️ Check for configuration conflicts and misconfigurations.
    
    Identifies common configuration issues that may cause problems.
    
    Args:
        network_id: Network ID to check
        
    Returns:
        Configuration analysis report
    """
    try:
        output = ["⚙️ Configuration Conflict Check", "=" * 50, ""]
        conflicts = []
        
        # 1. Check VLAN configuration
        try:
            with safe_api_call("check VLAN config"):
                # Try to get VLANs
                vlans = None
                single_lan = None
                
                try:
                    vlans = meraki.dashboard.appliance.getNetworkApplianceVlans(network_id)
                except:
                    # Might be single LAN
                    try:
                        single_lan = meraki.dashboard.appliance.getNetworkApplianceSingleLan(network_id)
                    except:
                        pass
                
                if vlans:
                    output.append("📋 VLAN Configuration:")
                    vlan_subnets = {}
                    
                    for vlan in vlans:
                        vlan_id = vlan['id']
                        subnet = vlan.get('subnet', '')
                        
                        output.append(f"   VLAN {vlan_id}: {vlan.get('name', 'Unnamed')}")
                        output.append(f"     Subnet: {subnet}")
                        output.append(f"     DHCP: {'Enabled' if vlan.get('dhcpHandling') != 'Do not respond to DHCP requests' else 'Disabled'}")
                        
                        # Check for subnet conflicts
                        if subnet in vlan_subnets.values():
                            conflicts.append("subnet_overlap")
                            output.append("     ⚠️ Subnet overlap detected!")
                        vlan_subnets[vlan_id] = subnet
                    
                    output.append("")
                elif single_lan:
                    output.append("📋 Single LAN Configuration:")
                    output.append(f"   Subnet: {single_lan.get('subnet', 'Not configured')}")
                    output.append(f"   Appliance IP: {single_lan.get('applianceIp', 'Not set')}")
                    output.append("")
        except Exception as e:
            output.append(f"⚠️ Could not check VLAN configuration: {str(e)[:50]}")
            output.append("")
        
        # 2. Check firewall rules for conflicts
        try:
            with safe_api_call("check firewall rules"):
                l3_rules = meraki.dashboard.appliance.getNetworkApplianceFirewallL3FirewallRules(network_id)
                
                if l3_rules and 'rules' in l3_rules:
                    output.append("🔥 Firewall Rule Analysis:")
                    
                    # Check for overly permissive rules
                    for i, rule in enumerate(l3_rules['rules']):
                        if (rule.get('policy') == 'allow' and 
                            rule.get('srcCidr') == 'Any' and 
                            rule.get('destCidr') == 'Any' and
                            rule.get('destPort') == 'Any'):
                            conflicts.append("permissive_firewall")
                            output.append(f"   ⚠️ Rule {i+1}: Overly permissive (allows all traffic)")
                    
                    # Check for deny rules after allow all
                    found_allow_all = False
                    for i, rule in enumerate(l3_rules['rules']):
                        if found_allow_all and rule.get('policy') == 'deny':
                            conflicts.append("unreachable_rule")
                            output.append(f"   ⚠️ Rule {i+1}: Unreachable (after allow-all rule)")
                        
                        if (rule.get('policy') == 'allow' and 
                            rule.get('srcCidr') == 'Any' and 
                            rule.get('destCidr') == 'Any'):
                            found_allow_all = True
                    
                    if not conflicts:
                        output.append("   ✅ No obvious firewall conflicts")
                    output.append("")
        except:
            pass
        
        # 3. Check DHCP configuration
        try:
            with safe_api_call("check DHCP config"):
                if vlans:
                    output.append("📡 DHCP Configuration Check:")
                    dhcp_pools = []
                    
                    for vlan in vlans:
                        if vlan.get('dhcpHandling') == 'Run a DHCP server':
                            # Check for reasonable pool size
                            subnet = vlan.get('subnet', '')
                            if subnet:
                                # Simple check - could be improved
                                if '/30' in subnet or '/31' in subnet:
                                    conflicts.append("small_dhcp_pool")
                                    output.append(f"   ⚠️ VLAN {vlan['id']}: Very small DHCP pool")
                    
                    output.append("")
        except:
            pass
        
        # 4. Check wireless configuration
        try:
            with safe_api_call("check wireless config"):
                ssids = meraki.dashboard.wireless.getNetworkWirelessSsids(network_id)
                
                if ssids:
                    output.append("📶 Wireless Configuration:")
                    ssid_names = []
                    open_networks = []
                    
                    for ssid in ssids:
                        if ssid.get('enabled'):
                            name = ssid.get('name', f"SSID {ssid.get('number')}")
                            
                            # Check for duplicate names
                            if name in ssid_names:
                                conflicts.append("duplicate_ssid")
                                output.append(f"   ⚠️ Duplicate SSID name: {name}")
                            ssid_names.append(name)
                            
                            # Check for open networks
                            if ssid.get('encryptionMode') == 'open':
                                open_networks.append(name)
                                conflicts.append("open_network")
                    
                    if open_networks:
                        output.append("   ⚠️ Open (unencrypted) networks:")
                        for net in open_networks:
                            output.append(f"     - {net}")
                    
                    output.append("")
        except:
            pass
        
        # 5. Generate recommendations
        output.append("🔧 CONFIGURATION RECOMMENDATIONS:")
        output.append("=" * 50)
        
        if not conflicts:
            output.append("✅ No configuration conflicts detected")
        else:
            if "subnet_overlap" in conflicts:
                output.append("\n🔄 Subnet Overlap:")
                output.append("   1. Review VLAN subnet assignments")
                output.append("   2. Ensure unique subnets per VLAN")
                output.append("   3. Update routing tables if needed")
                output.append("   4. Check for static route conflicts")
            
            if "permissive_firewall" in conflicts:
                output.append("\n🔓 Overly Permissive Firewall:")
                output.append("   1. Implement least-privilege rules")
                output.append("   2. Define specific source/destination")
                output.append("   3. Restrict ports to required services")
                output.append("   4. Add deny rules for untrusted sources")
            
            if "unreachable_rule" in conflicts:
                output.append("\n📑 Unreachable Firewall Rules:")
                output.append("   1. Reorder rules (most specific first)")
                output.append("   2. Remove redundant rules")
                output.append("   3. Place deny rules before allow-all")
                output.append("   4. Use rule comments for clarity")
            
            if "small_dhcp_pool" in conflicts:
                output.append("\n🎯 Small DHCP Pool:")
                output.append("   1. Increase subnet size if possible")
                output.append("   2. Use DHCP reservations efficiently")
                output.append("   3. Reduce lease time for guest networks")
                output.append("   4. Monitor pool utilization")
            
            if "open_network" in conflicts:
                output.append("\n🔒 Open Wireless Networks:")
                output.append("   1. Enable WPA2/WPA3 encryption")
                output.append("   2. Use enterprise auth for corporate")
                output.append("   3. Implement splash page for guest")
                output.append("   4. Enable client isolation")
            
            if "duplicate_ssid" in conflicts:
                output.append("\n📡 Duplicate SSID Names:")
                output.append("   1. Use unique names per SSID")
                output.append("   2. Follow naming conventions")
                output.append("   3. Document SSID purposes")
                output.append("   4. Regular SSID audit")
        
        # Best practices
        output.extend([
            "\n📋 Configuration Best Practices:",
            "• Regular configuration backups",
            "• Change control documentation",
            "• Test changes in lab first",
            "• Use configuration templates",
            "• Regular security audits"
        ])
        
        return "\n".join(output)
        
    except Exception as e:
        return format_error("check configuration", e)


def generate_troubleshooting_report(
    network_id: str,
    include_connectivity: bool = True,
    include_performance: bool = True,
    include_configuration: bool = True,
    client_mac: Optional[str] = None
) -> str:
    """
    📊 Generate comprehensive troubleshooting report.
    
    Combines all diagnostic tools into a single report.
    
    Args:
        network_id: Network ID to analyze
        include_connectivity: Include connectivity diagnosis
        include_performance: Include performance analysis
        include_configuration: Include configuration check
        client_mac: Specific client to analyze (optional)
        
    Returns:
        Comprehensive troubleshooting report
    """
    try:
        output = ["📊 COMPREHENSIVE TROUBLESHOOTING REPORT", "=" * 60, ""]
        
        # Header
        output.append(f"Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")
        
        try:
            network = meraki.dashboard.networks.getNetwork(network_id)
            output.append(f"Network: {network['name']}")
            output.append(f"Type: {', '.join(network.get('productTypes', []))}")
        except:
            output.append(f"Network ID: {network_id}")
        
        if client_mac:
            output.append(f"Client Analysis: {client_mac}")
        
        output.append("")
        
        # Section 1: Connectivity
        if include_connectivity:
            output.append("\n" + "="*60)
            output.append("SECTION 1: CONNECTIVITY DIAGNOSIS")
            output.append("="*60)
            connectivity = diagnose_connectivity_issues(network_id, client_mac, 3600)
            output.append(connectivity)
            output.append("")
        
        # Section 2: Performance
        if include_performance:
            output.append("\n" + "="*60)
            output.append("SECTION 2: PERFORMANCE ANALYSIS")
            output.append("="*60)
            performance = analyze_performance_bottlenecks(network_id, 3600)
            output.append(performance)
            output.append("")
        
        # Section 3: Configuration
        if include_configuration:
            output.append("\n" + "="*60)
            output.append("SECTION 3: CONFIGURATION CHECK")
            output.append("="*60)
            configuration = check_configuration_conflicts(network_id)
            output.append(configuration)
            output.append("")
        
        # Summary and next steps
        output.extend([
            "\n" + "="*60,
            "SUMMARY & NEXT STEPS",
            "="*60,
            "",
            "🎯 Priority Actions:",
            "1. Address any offline devices immediately",
            "2. Resolve authentication/DHCP failures",
            "3. Fix configuration conflicts",
            "4. Optimize performance bottlenecks",
            "5. Schedule maintenance window for changes",
            "",
            "📞 Escalation Path:",
            "• Collect this report for support tickets",
            "• Run packet captures for deep analysis",
            "• Contact ISP for WAN issues",
            "• Engage Meraki support for hardware issues",
            "",
            "📊 Report saved: Use for documentation and tracking"
        ])
        
        return "\n".join(output)
        
    except Exception as e:
        return format_error("generate report", e)


def suggest_remediation_steps(
    network_id: str,
    issue_type: str
) -> str:
    """
    💊 Suggest specific remediation steps for common issues.
    
    Provides detailed fix instructions for identified problems.
    
    Args:
        network_id: Network ID with issues
        issue_type: Type of issue (connectivity, performance, dhcp, wireless, etc.)
        
    Returns:
        Detailed remediation steps
    """
    try:
        output = ["💊 Remediation Steps", "=" * 50, ""]
        
        issue_type = issue_type.lower()
        
        remediation_guides = {
            "connectivity": {
                "title": "Connectivity Issue Remediation",
                "steps": [
                    "1. **Device Connectivity Check**",
                    "   - Navigate to Organization > Devices",
                    "   - Filter for offline devices",
                    "   - For each offline device:",
                    "     a) Check physical connections",
                    "     b) Verify power status",
                    "     c) Test WAN connectivity",
                    "     d) Review device event log",
                    "",
                    "2. **Client Connection Issues**",
                    "   - Go to Network > Clients",
                    "   - Filter for disconnected clients",
                    "   - Check client details:",
                    "     a) Authentication status",
                    "     b) DHCP lease status",
                    "     c) Signal strength (wireless)",
                    "     d) VLAN assignment",
                    "",
                    "3. **Authentication Failures**",
                    "   - Wireless > Access Control",
                    "   - Verify authentication method",
                    "   - For 802.1X:",
                    "     a) Test RADIUS connectivity",
                    "     b) Verify certificates",
                    "     c) Check NPS/ISE logs",
                    "   - For PSK: Verify password",
                    "",
                    "4. **DHCP Troubleshooting**",
                    "   - Security & SD-WAN > DHCP",
                    "   - Check pool utilization",
                    "   - Verify scope settings",
                    "   - Clear stale leases",
                    "   - Test with static IP"
                ]
            },
            
            "performance": {
                "title": "Performance Issue Remediation",
                "steps": [
                    "1. **Bandwidth Optimization**",
                    "   - Security & SD-WAN > Traffic Shaping",
                    "   - Create bandwidth limits for:",
                    "     a) Streaming applications",
                    "     b) File sharing",
                    "     c) Software updates",
                    "   - Enable SD-WAN policies",
                    "",
                    "2. **Wireless Optimization**",
                    "   - Wireless > Radio Settings",
                    "   - Adjust channel width",
                    "   - Enable band steering",
                    "   - Set minimum bitrate",
                    "   - Review RF profiles",
                    "",
                    "3. **Switch Performance**",
                    "   - Switch > Switch Ports",
                    "   - Check port utilization",
                    "   - Enable flow control",
                    "   - Configure port aggregation",
                    "   - Review spanning tree",
                    "",
                    "4. **WAN Optimization**",
                    "   - Test with multiple DNS servers",
                    "   - Enable WAN optimization",
                    "   - Configure load balancing",
                    "   - Review MTU settings"
                ]
            },
            
            "dhcp": {
                "title": "DHCP Issue Remediation",
                "steps": [
                    "1. **DHCP Server Configuration**",
                    "   - Security & SD-WAN > DHCP",
                    "   - For each VLAN/subnet:",
                    "     a) Verify DHCP enabled",
                    "     b) Check IP pool size",
                    "     c) Review reservations",
                    "     d) Set appropriate lease time",
                    "",
                    "2. **DHCP Relay Setup**",
                    "   - Configure DHCP relay if needed",
                    "   - Verify helper address",
                    "   - Check VLAN settings",
                    "   - Test relay function",
                    "",
                    "3. **Troubleshooting Steps**",
                    "   - Clear DHCP bindings",
                    "   - Check for IP conflicts",
                    "   - Verify VLAN tagging",
                    "   - Review firewall rules",
                    "",
                    "4. **Client-Specific Issues**",
                    "   - Release/renew on client",
                    "   - Check MAC filtering",
                    "   - Verify group policy",
                    "   - Test with different VLAN"
                ]
            },
            
            "wireless": {
                "title": "Wireless Issue Remediation",
                "steps": [
                    "1. **RF Optimization**",
                    "   - Wireless > Radio Settings",
                    "   - Run RF spectrum analysis",
                    "   - Adjust channel assignments",
                    "   - Set appropriate power levels",
                    "   - Enable DFS channels if needed",
                    "",
                    "2. **SSID Configuration**",
                    "   - Wireless > SSIDs",
                    "   - Enable band steering",
                    "   - Set minimum bitrate (12 Mbps)",
                    "   - Configure load balancing",
                    "   - Enable 802.11r for roaming",
                    "",
                    "3. **Client Density**",
                    "   - Review client limits per AP",
                    "   - Add APs in high-density areas",
                    "   - Enable client balancing",
                    "   - Configure broadcast filtering",
                    "",
                    "4. **Security Settings**",
                    "   - Use WPA3 where supported",
                    "   - Enable management frame protection",
                    "   - Configure client isolation",
                    "   - Review guest access policies"
                ]
            },
            
            "security": {
                "title": "Security Issue Remediation",
                "steps": [
                    "1. **Firewall Hardening**",
                    "   - Security & SD-WAN > Firewall",
                    "   - Review and tighten rules",
                    "   - Enable IDS/IPS",
                    "   - Configure geo-blocking",
                    "   - Enable advanced malware protection",
                    "",
                    "2. **Access Control**",
                    "   - Implement 802.1X",
                    "   - Configure MAB for devices",
                    "   - Set up guest isolation",
                    "   - Enable posture assessment",
                    "",
                    "3. **Monitoring Setup**",
                    "   - Configure security alerts",
                    "   - Enable syslog forwarding",
                    "   - Set up webhook notifications",
                    "   - Review security events regularly",
                    "",
                    "4. **Best Practices**",
                    "   - Regular firmware updates",
                    "   - Strong admin passwords",
                    "   - Two-factor authentication",
                    "   - Regular security audits"
                ]
            }
        }
        
        if issue_type in remediation_guides:
            guide = remediation_guides[issue_type]
            output.append(f"📋 {guide['title']}")
            output.append("")
            output.extend(guide['steps'])
        else:
            # Generic remediation
            output.extend([
                "📋 General Remediation Steps",
                "",
                "1. **Immediate Actions**",
                "   - Check device status dashboard",
                "   - Review recent events/alerts",
                "   - Verify no recent changes",
                "   - Test with known-good config",
                "",
                "2. **Diagnostic Steps**",
                "   - Run ping tests from devices",
                "   - Perform packet captures",
                "   - Check upstream connectivity",
                "   - Review client connection logs",
                "",
                "3. **Common Fixes**",
                "   - Reboot affected devices",
                "   - Clear ARP/MAC tables",
                "   - Update firmware if needed",
                "   - Reset to factory if corrupted",
                "",
                "4. **Escalation**",
                "   - Document all findings",
                "   - Open Meraki support case",
                "   - Provide diagnostic outputs",
                "   - Schedule maintenance window"
            ])
        
        # Add commands reference
        output.extend([
            "",
            "🔧 Useful Dashboard Locations:",
            "• Device Status: Organization > Summary",
            "• Event Log: Network > Event Log",
            "• Traffic Analytics: Network > Analytics",
            "• Client Details: Network > Clients",
            "• Wireless Health: Wireless > Health",
            "",
            "📞 Support Information:",
            "• Meraki Support: https://meraki.cisco.com/support",
            "• API Status: https://api.meraki.com/api/v1/status",
            "• Documentation: https://documentation.meraki.com"
        ])
        
        return "\n".join(output)
        
    except Exception as e:
        return format_error("suggest remediation", e)


# Helper tool
def troubleshooting_help() -> str:
    """
    ❓ Get help on using troubleshooting tools.
    
    Provides guidance on which tool to use for different issues.
    
    Returns:
        Help guide for troubleshooting tools
    """
    try:
        output = ["❓ Troubleshooting Tools Help Guide", "=" * 50, ""]
        
        output.extend([
            "🔧 Available Troubleshooting Tools:",
            "",
            "1. **diagnose_connectivity_issues()**",
            "   Use when: Clients can't connect or stay connected",
            "   Checks: Device status, auth failures, DHCP issues",
            "   Example: diagnose_connectivity_issues(network_id, client_mac='AA:BB:CC:DD:EE:FF')",
            "",
            "2. **analyze_performance_bottlenecks()**",
            "   Use when: Network is slow or laggy",
            "   Checks: Bandwidth usage, port saturation, wireless congestion",
            "   Example: analyze_performance_bottlenecks(network_id, timespan=3600)",
            "",
            "3. **check_configuration_conflicts()**",
            "   Use when: Things stopped working after changes",
            "   Checks: VLAN conflicts, firewall rules, DHCP settings",
            "   Example: check_configuration_conflicts(network_id)",
            "",
            "4. **generate_troubleshooting_report()**",
            "   Use when: Need comprehensive analysis",
            "   Includes: All diagnostics in one report",
            "   Example: generate_troubleshooting_report(network_id)",
            "",
            "5. **suggest_remediation_steps()**",
            "   Use when: Need fixing instructions",
            "   Types: connectivity, performance, dhcp, wireless, security",
            "   Example: suggest_remediation_steps(network_id, 'connectivity')",
            "",
            "🎯 Quick Troubleshooting Guide:",
            "",
            "**Client Can't Connect?**",
            "1. Run: diagnose_connectivity_issues(network_id, client_mac)",
            "2. Check authentication method and credentials",
            "3. Verify VLAN and DHCP settings",
            "4. Review wireless signal strength",
            "",
            "**Network Running Slow?**",
            "1. Run: analyze_performance_bottlenecks(network_id)",
            "2. Check bandwidth utilization graphs",
            "3. Look for high channel utilization",
            "4. Review traffic shaping rules",
            "",
            "**Recent Changes Broke Something?**",
            "1. Run: check_configuration_conflicts(network_id)",
            "2. Review change log/audit trail",
            "3. Compare before/after configs",
            "4. Test rollback in lab",
            "",
            "**Need Help for Support?**",
            "1. Run: generate_troubleshooting_report(network_id)",
            "2. Save report output",
            "3. Include in support ticket",
            "4. Follow remediation steps",
            "",
            "💡 Pro Tips:",
            "• Always check device status first",
            "• Use specific client MAC when possible",
            "• Longer timespan = more historical data",
            "• Save reports for comparison",
            "• Test fixes in maintenance window"
        ])
        
        return "\n".join(output)
        
    except Exception as e:
        return format_error("troubleshooting help", e)


def register_troubleshooting_tools(app: FastMCP, client: MerakiClient):
    """Register troubleshooting tools with the MCP server."""
    global mcp_app, meraki
    mcp_app = app
    meraki = client
    
    # Register all tools
    app.tool()(diagnose_connectivity_issues)
    app.tool()(analyze_performance_bottlenecks)
    app.tool()(check_configuration_conflicts)
    app.tool()(generate_troubleshooting_report)
    app.tool()(suggest_remediation_steps)
    app.tool()(troubleshooting_help)