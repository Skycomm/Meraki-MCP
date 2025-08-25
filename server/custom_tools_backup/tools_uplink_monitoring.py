"""
Uplink Monitoring Tools for Cisco Meraki MCP Server
Monitor WAN uplinks, bandwidth usage, and failover events
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


def get_uplink_status(network_id: str) -> str:
    """
    🌐 Get current WAN uplink status and configuration.
    
    Shows all WAN interfaces, their status, and current utilization.
    
    Args:
        network_id: Network ID
    
    Returns:
        Formatted uplink status overview
    """
    try:
        output = ["🌐 WAN Uplink Status", "=" * 50, ""]
        
        # Get network info
        try:
            network = meraki.dashboard.networks.getNetwork(network_id)
            org_id = network.get('organizationId')
            output.append(f"Network: {network['name']}")
            output.append("")
        except:
            return "❌ Could not retrieve network information"
        
        # Get devices
        devices = meraki.dashboard.networks.getNetworkDevices(network_id)
        mx_device = next((d for d in devices if d['model'].startswith('MX')), None)
        
        if mx_device:
            output.append(f"Device: {mx_device.get('name', mx_device['serial'])} ({mx_device['model']})")
            output.append("")
            
            # Get uplink configuration from device
            try:
                settings = meraki.dashboard.appliance.getDeviceApplianceUplinksSettings(
                    mx_device['serial']
                )
                
                # WAN 1
                wan1 = settings.get('interfaces', {}).get('wan1', {})
                if wan1.get('enabled'):
                    output.append("WAN 1: Enabled ✅")
                    output.append(f"   Assignment: {wan1.get('svis', {}).get('ipv4', {}).get('assignmentMode', 'Unknown')}")
                    if wan1.get('pppoe', {}).get('enabled'):
                        output.append("   PPPoE: Enabled")
                else:
                    output.append("WAN 1: Disabled ❌")
                output.append("")
                
                # WAN 2  
                wan2 = settings.get('interfaces', {}).get('wan2', {})
                if wan2.get('enabled'):
                    output.append("WAN 2: Enabled ✅")
                    output.append(f"   Assignment: {wan2.get('svis', {}).get('ipv4', {}).get('assignmentMode', 'Unknown')}")
                    if wan2.get('pppoe', {}).get('enabled'):
                        output.append("   PPPoE: Enabled")
                else:
                    output.append("WAN 2: Disabled ❌")
                output.append("")
                    
            except Exception as e:
                output.append(f"⚠️ Could not get uplink configuration: {str(e)}")
                output.append("")
        
        # Try to get actual uplink status from organization API
        try:
            uplink_statuses = meraki.dashboard.appliance.getOrganizationApplianceUplinkStatuses(org_id)
            
            for status in uplink_statuses:
                if status.get('networkId') == network_id:
                    output.append("📡 Current Uplink Status:")
                    
                    for uplink in status.get('uplinks', []):
                        interface = uplink.get('interface', 'Unknown')
                        is_active = uplink.get('status') == 'active'
                        status_icon = '🟢' if is_active else '🔴'
                        
                        output.append(f"\n{interface.upper()}: {status_icon} {uplink.get('status', 'Unknown').title()}")
                        if uplink.get('ip'):
                            output.append(f"   IP: {uplink['ip']}")
                        if uplink.get('gateway'):
                            output.append(f"   Gateway: {uplink['gateway']}")
                        if uplink.get('dns'):
                            output.append(f"   DNS: {uplink['dns']}")
                    break
        except:
            # Fallback - just show basic info
            pass
        
        # Get recent loss and latency metrics to 8.8.8.8
        try:
            output.append("\n📊 Link Quality to 8.8.8.8 (Last 5 minutes):")
            
            # Try to get loss/latency data using the device-specific API that tests to 8.8.8.8
            if mx_device:
                try:
                    loss_data = meraki.dashboard.devices.getDeviceLossAndLatencyHistory(
                        mx_device['serial'],
                        timespan=300,  # 5 minutes
                        ip='8.8.8.8'
                    )
                    
                    if loss_data:
                        # Calculate averages from the time series data
                        losses = [item.get('lossPercent', 0) for item in loss_data if item.get('lossPercent') is not None]
                        latencies = [item.get('latencyMs', 0) for item in loss_data if item.get('latencyMs', 0) > 0]
                        
                        if losses:
                            avg_loss = sum(losses) / len(losses)
                            max_loss = max(losses)
                            current_loss = losses[-1] if losses else 0
                        else:
                            avg_loss = max_loss = current_loss = 0
                            
                        if latencies:
                            avg_latency = sum(latencies) / len(latencies)
                            max_latency = max(latencies)
                            current_latency = latencies[-1] if latencies else 0
                        else:
                            avg_latency = max_latency = current_latency = None
                        
                        # Current status with indicators
                        loss_icon = '🔴' if current_loss > 5 else '🟡' if current_loss > 1 else '🟢'
                        
                        output.append(f"\n🌐 Current Status:")
                        output.append(f"   📉 Packet Loss: {loss_icon} {current_loss:.1f}%")
                        
                        if current_latency is not None:
                            lat_icon = '🟢' if current_latency < 50 else '🟡' if current_latency < 100 else '🔴'
                            quality = "Excellent" if current_latency < 20 else "Good" if current_latency < 50 else "Fair" if current_latency < 100 else "Poor"
                            output.append(f"   ⏱️ Latency: {lat_icon} {current_latency:.1f} ms ({quality})")
                        else:
                            output.append(f"   ⏱️ Latency: Measuring...")
                        
                        # Show averages if we have enough data
                        if len(losses) > 1:
                            output.append(f"\n📊 5-Minute Averages:")
                            output.append(f"   📉 Avg Loss: {avg_loss:.1f}% (Max: {max_loss:.1f}%)")
                            if avg_latency is not None:
                                output.append(f"   ⏱️ Avg Latency: {avg_latency:.1f} ms (Max: {max_latency:.1f} ms)")
                            output.append(f"   📈 Data Points: {len(loss_data)}")
                    else:
                        output.append("   ⚠️ No loss/latency data available")
                        output.append("   💡 Tip: Wait a few minutes for data to populate")
                except Exception as e:
                    # Fallback to organization-level API
                    try:
                        output.append("   ℹ️ Using organization-wide metrics...")
                        perf_data = meraki.dashboard.organizations.getOrganizationDevicesUplinksLossAndLatency(
                            org_id,
                            timespan=300,
                            networkId=network_id
                        )
                        if perf_data:
                            # Average the recent samples
                            recent = perf_data[-5:] if len(perf_data) > 5 else perf_data
                            avg_loss = sum(p.get('lossPercent', 0) for p in recent) / len(recent) if recent else 0
                            
                            # Calculate average latency, excluding zeros
                            latencies = [p.get('latencyMs', 0) for p in recent if p.get('latencyMs', 0) > 0]
                            avg_latency = sum(latencies) / len(latencies) if latencies else None
                            
                            loss_icon = '🟢' if avg_loss < 1 else '🟡' if avg_loss < 5 else '🔴'
                            output.append(f"   📉 Packet Loss: {loss_icon} {avg_loss:.1f}%")
                            
                            if avg_latency is not None:
                                lat_icon = '🟢' if avg_latency < 50 else '🟡' if avg_latency < 100 else '🔴'
                                quality = "Excellent" if avg_latency < 20 else "Good" if avg_latency < 50 else "Fair" if avg_latency < 100 else "Poor"
                                output.append(f"   ⏱️ Latency: {lat_icon} {avg_latency:.1f} ms ({quality})")
                            else:
                                output.append(f"   ⏱️ Latency: Measuring...")
                    except:
                        output.append("   ⚠️ Could not retrieve loss/latency metrics")
        except Exception as e:
            output.append(f"\n⚠️ Could not retrieve link quality metrics: {str(e)}")
        
        # If we didn't get latency data, suggest running a ping test
        need_ping_test = True
        for line in output:
            if "Latency:" in line and "Measuring..." not in line and "ms" in line:
                need_ping_test = False
                break
        
        if need_ping_test and mx_device:
            output.append("\n💡 Tip: Run a ping test for real-time latency measurement:")
            output.append(f"   create_device_ping_test(serial='{mx_device['serial']}', target='8.8.8.8')")
        
        # Show quick actions
        output.extend([
            "",
            "💡 Quick Actions:",
            "• Run get_realtime_bandwidth_usage() for current bandwidth",
            "• Run get_uplink_bandwidth_history() for historical data",
            "• Run analyze_uplink_health() for health analysis",
            "• Run run_throughput_test() to test speeds"
        ])
        
        return "\n".join(output)
        
    except Exception as e:
        return format_error("get uplink status", e)


def get_uplink_bandwidth_history(
    network_id: str,
    timespan: Optional[int] = 7200,
    resolution: Optional[int] = 300
) -> str:
    """
    📊 Get historical bandwidth usage for WAN uplinks.
    
    Shows upload/download rates over time for each uplink.
    
    Args:
        network_id: Network ID
        timespan: Time period in seconds (default: 7200 = 2 hours)
        resolution: Data resolution in seconds (300, 600, 3600, 86400)
    
    Returns:
        Bandwidth usage history and statistics
    """
    try:
        with safe_api_call("get bandwidth history"):
            # Get loss and latency history
            history = meraki.dashboard.appliance.getNetworkApplianceLossAndLatencyHistory(
                network_id,
                timespan=timespan,
                resolution=resolution,
                uplink='wan1'
            )
            
            result = f"""📊 Uplink Bandwidth History
==================================================

Time Period: Last {timespan // 3600} hours
Resolution: {resolution // 60} minutes

"""
            
            # Try to get actual bandwidth data
            devices = meraki.dashboard.networks.getNetworkDevices(network_id)
            mx_device = next((d for d in devices if d['model'].startswith('MX')), None)
            
            if mx_device:
                try:
                    # Get uplink bandwidth
                    bandwidth = meraki.dashboard.appliance.getDeviceApplianceThroughputTest(
                        serial=mx_device['serial']
                    )
                    
                    if bandwidth:
                        result += "📈 Recent Throughput Tests:\n"
                        for test in bandwidth[:5]:
                            result += f"\n   {test.get('testTime', 'Unknown time')}"
                            result += f"\n   ↓ {test.get('downstream', 0)} Mbps"
                            result += f"\n   ↑ {test.get('upstream', 0)} Mbps\n"
                            
                except:
                    pass
            
            # Show loss and latency data
            if history:
                result += "\n📊 Performance Metrics:\n"
                
                # Calculate averages
                total_loss = 0
                total_latency = 0
                count = 0
                
                for point in history:
                    loss = point.get('lossPercent', 0)
                    latency = point.get('latencyMs', 0)
                    total_loss += loss
                    total_latency += latency
                    count += 1
                
                if count > 0:
                    avg_loss = total_loss / count
                    avg_latency = total_latency / count
                    
                    result += f"\nWAN 1 Averages:"
                    result += f"\n   Packet Loss: {avg_loss:.2f}%"
                    result += f"\n   Latency: {avg_latency:.1f} ms"
                    
                    # Status assessment
                    if avg_loss < 0.1:
                        result += "\n   Status: 🟢 Excellent"
                    elif avg_loss < 1:
                        result += "\n   Status: 🟡 Good"
                    else:
                        result += "\n   Status: 🔴 Poor"
                
                # Show recent samples
                result += "\n\n📈 Recent Samples:"
                for point in history[-5:]:
                    time_str = point.get('startTime', 'Unknown')
                    loss = point.get('lossPercent', 0)
                    latency = point.get('latencyMs', 0)
                    
                    result += f"\n   {time_str[-8:-3]}: "
                    result += f"Loss {loss:.1f}%, Latency {latency:.0f}ms"
            
            result += "\n\n💡 Performance Guidelines:"
            result += "\n   • Loss < 1% for VoIP quality"
            result += "\n   • Latency < 150ms for real-time apps"
            result += "\n   • Jitter < 30ms for video calls"
            
            result += "\n\n📋 Bandwidth Management:"
            result += "\n   • Enable traffic shaping"
            result += "\n   • Set bandwidth limits"
            result += "\n   • Configure QoS rules"
            result += "\n   • Monitor peak usage times"
            
            return result
            
    except Exception as e:
        return format_error("get bandwidth history", e)


def get_realtime_bandwidth_usage(network_id: str) -> str:
    """
    📊 Get real-time bandwidth usage for all uplinks.
    
    Shows current bandwidth utilization in real-time.
    
    Args:
        network_id: Network ID
        
    Returns:
        Real-time bandwidth usage
    """
    try:
        with safe_api_call("get real-time bandwidth"):
            # Get the last 2 minutes of data with 1-minute resolution
            usage = meraki.dashboard.appliance.getNetworkApplianceUplinksUsageHistory(
                network_id,
                timespan=120,  # 2 minutes
                resolution=60  # 1 minute
            )
            
            output = ["📊 Real-Time Bandwidth Usage", "=" * 50, ""]
            
            if usage:
                # Get the most recent data point
                latest = usage[-1] if usage else None
                
                if latest and 'byInterface' in latest:
                    output.append(f"⏰ Time Period: {latest.get('startTime', '')} to {latest.get('endTime', '')}")
                    output.append("")
                    
                    # Process each interface
                    total_sent = 0
                    total_recv = 0
                    active_interfaces = []
                    
                    for iface_data in latest.get('byInterface', []):
                        interface = iface_data.get('interface', 'Unknown')
                        sent_bytes = iface_data.get('sent', 0)
                        recv_bytes = iface_data.get('received', 0)
                        
                        # Skip interfaces with no traffic
                        if sent_bytes == 0 and recv_bytes == 0:
                            continue
                        
                        # Convert bytes to Mbps (bytes * 8 / 1,000,000)
                        # Also divide by time period (60 seconds) to get rate
                        sent_mbps = (sent_bytes * 8) / 1_000_000 / 60
                        recv_mbps = (recv_bytes * 8) / 1_000_000 / 60
                        
                        total_sent += sent_mbps
                        total_recv += recv_mbps
                        active_interfaces.append((interface, sent_mbps, recv_mbps))
                        
                    # Show active interfaces first
                    for interface, sent_mbps, recv_mbps in active_interfaces:
                        output.append(f"🔌 Interface: {interface}")
                        
                        # Create visual bandwidth bars
                        upload_bar = "█" * min(int(sent_mbps / 2), 20)  # 1 block = 2 Mbps, max 20 blocks
                        download_bar = "█" * min(int(recv_mbps / 2), 20)
                        
                        output.append(f"📤 Upload: {sent_mbps:.2f} Mbps")
                        output.append(f"   [{upload_bar:<20}]")
                        output.append(f"📥 Download: {recv_mbps:.2f} Mbps")
                        output.append(f"   [{download_bar:<20}]")
                        output.append("")
                    
                    if total_sent > 0 or total_recv > 0:
                        output.append("📊 Total Bandwidth Summary:")
                        output.append(f"   📤 Total Upload: {total_sent:.2f} Mbps")
                        output.append(f"   📥 Total Download: {total_recv:.2f} Mbps")
                        output.append(f"   🔗 Combined: {(total_sent + total_recv):.2f} Mbps")
                        
                        # Add usage interpretation
                        total_mbps = total_sent + total_recv
                        if total_mbps < 10:
                            output.append(f"   📊 Usage: Light")
                        elif total_mbps < 50:
                            output.append(f"   📊 Usage: Moderate")
                        elif total_mbps < 100:
                            output.append(f"   📊 Usage: Heavy")
                        else:
                            output.append(f"   📊 Usage: Very Heavy")
                else:
                    output.append("No recent bandwidth data available")
            else:
                output.append("No bandwidth monitoring data available")
                output.append("\n💡 Troubleshooting:")
                output.append("• Ensure the device has been online for at least 2 minutes")
                output.append("• Check if traffic analytics is enabled")
                output.append("• Verify WAN connections are active")
                
            return "\n".join(output)
            
    except Exception as e:
        return format_error("get real-time bandwidth", e)


def get_failover_events(
    network_id: str,
    timespan: Optional[int] = 604800
) -> str:
    """
    🔄 Get WAN failover event history.
    
    Shows when uplinks failed over and why.
    
    Args:
        network_id: Network ID
        timespan: Time period in seconds (default: 604800 = 7 days)
    
    Returns:
        Failover event history and analysis
    """
    try:
        with safe_api_call("get failover events"):
            # Get network events filtered for failover
            events = meraki.dashboard.networks.getNetworkEvents(
                networkId=network_id,
                includedEventTypes=["failover", "failback", "primary_uplink_change"],
                perPage=100
            )
            
            result = f"""🔄 WAN Failover Events
==================================================

Time Period: Last {timespan // 86400} days
"""
            
            failover_events = []
            for event in events.get('events', []):
                if any(term in event.get('type', '').lower() for term in ['failover', 'uplink', 'wan']):
                    failover_events.append(event)
            
            if failover_events:
                result += f"\nFailover Events Found: {len(failover_events)}\n"
                
                # Analyze patterns
                failover_count = {}
                for event in failover_events:
                    event_type = event.get('type', 'Unknown')
                    failover_count[event_type] = failover_count.get(event_type, 0) + 1
                
                result += "\n📊 Event Summary:"
                for event_type, count in failover_count.items():
                    result += f"\n   • {event_type}: {count} times"
                
                # Show recent events
                result += "\n\n📋 Recent Failover Events:"
                for event in failover_events[:10]:
                    time_str = event.get('occurredAt', 'Unknown time')
                    desc = event.get('description', 'No description')
                    
                    result += f"\n\n🔄 {time_str}"
                    result += f"\n   {desc}"
                    
                    # Determine cause if possible
                    if 'timeout' in desc.lower():
                        result += "\n   Cause: Connection timeout"
                    elif 'packet loss' in desc.lower():
                        result += "\n   Cause: Excessive packet loss"
                    elif 'latency' in desc.lower():
                        result += "\n   Cause: High latency"
                
                # Recommendations based on frequency
                if len(failover_events) > 10:
                    result += "\n\n⚠️ High Failover Frequency Detected!"
                    result += "\n\n🔧 Recommendations:"
                    result += "\n   1. Check WAN 1 connection stability"
                    result += "\n   2. Review ISP service quality"
                    result += "\n   3. Adjust failover sensitivity"
                    result += "\n   4. Consider redundant ISPs"
                    
            else:
                result += "\n✅ No failover events in this period"
                result += "\n   • Uplinks have been stable"
                result += "\n   • No WAN outages detected"
            
            result += "\n\n💡 Failover Configuration:"
            result += "\n   • Set appropriate thresholds"
            result += "\n   • Test failover regularly"
            result += "\n   • Configure email alerts"
            result += "\n   • Document ISP contacts"
            
            return result
            
    except Exception as e:
        return format_error("get failover events", e)


def configure_uplink_settings(
    network_id: str,
    load_balancing_mode: str = "failover",
    wan1_weight: Optional[int] = None,
    wan2_weight: Optional[int] = None,
    primary_uplink: Optional[str] = None
) -> str:
    """
    ⚙️ Configure WAN uplink settings.
    
    Set load balancing, failover, and bandwidth settings.
    
    Args:
        network_id: Network ID
        load_balancing_mode: "failover" or "loadBalance"
        wan1_weight: Weight for WAN1 (1-100, for load balance mode)
        wan2_weight: Weight for WAN2 (1-100, for load balance mode)
        primary_uplink: "wan1" or "wan2" for failover mode
    
    Returns:
        Configuration result
    """
    try:
        with safe_api_call("configure uplink settings"):
            # Get current settings
            current = meraki.dashboard.appliance.getNetworkApplianceUplinksSettings(
                networkId=network_id
            )
            
            # Update configuration
            config = {
                "loadBalancingMode": load_balancing_mode
            }
            
            if load_balancing_mode == "loadBalance":
                if wan1_weight and wan2_weight:
                    config["wan1"] = {"weight": wan1_weight}
                    config["wan2"] = {"weight": wan2_weight}
            elif primary_uplink:
                config["primaryUplink"] = primary_uplink
            
            # Apply settings
            updated = meraki.dashboard.appliance.updateNetworkApplianceUplinksSettings(
                networkId=network_id,
                **config
            )
            
            result = f"""⚙️ Uplink Configuration Updated
==================================================

Load Balancing Mode: {updated['loadBalancingMode']}
"""
            
            if load_balancing_mode == "loadBalance":
                result += "\n⚖️ Load Balance Settings:"
                wan1_w = updated.get('wan1', {}).get('weight', 50)
                wan2_w = updated.get('wan2', {}).get('weight', 50)
                result += f"\n   WAN 1: {wan1_w}% of traffic"
                result += f"\n   WAN 2: {wan2_w}% of traffic"
                
                result += "\n\n📊 How it works:"
                result += "\n   • Traffic distributed by weight"
                result += "\n   • Both links active simultaneously"
                result += "\n   • Automatic failover if one fails"
                result += "\n   • Best for bandwidth aggregation"
                
            else:  # failover mode
                primary = updated.get('primaryUplink', 'wan1')
                result += f"\n🔄 Failover Settings:"
                result += f"\n   Primary: {primary.upper()}"
                result += f"\n   Backup: {'WAN2' if primary == 'wan1' else 'WAN1'}"
                
                result += "\n\n📋 How it works:"
                result += "\n   • All traffic uses primary"
                result += "\n   • Switches on primary failure"
                result += "\n   • Returns when primary recovers"
                result += "\n   • Best for reliability"
            
            result += "\n\n🔍 Failover Detection:"
            result += "\n   • ICMP to multiple targets"
            result += "\n   • DNS resolution tests"
            result += "\n   • HTTP connectivity checks"
            result += "\n   • Configurable thresholds"
            
            result += "\n\n💡 Next Steps:"
            result += "\n   1. Test failover behavior"
            result += "\n   2. Monitor bandwidth usage"
            result += "\n   3. Set up alert notifications"
            result += "\n   4. Document configuration"
            
            return result
            
    except Exception as e:
        return format_error("configure uplink settings", e)


def set_bandwidth_limits(
    network_id: str,
    wan_interface: str,
    limit_up: Optional[int] = None,
    limit_down: Optional[int] = None
) -> str:
    """
    📏 Set bandwidth limits for WAN interfaces.
    
    Configure upload/download speed limits per WAN interface.
    
    Args:
        network_id: Network ID
        wan_interface: "wan1" or "wan2"
        limit_up: Upload limit in Mbps (None = unlimited)
        limit_down: Download limit in Mbps (None = unlimited)
    
    Returns:
        Configuration result
    """
    try:
        with safe_api_call("set bandwidth limits"):
            # Get current settings
            current = meraki.dashboard.appliance.getNetworkApplianceUplinksSettings(
                networkId=network_id
            )
            
            # Update bandwidth limits
            if wan_interface not in current:
                current[wan_interface] = {}
            
            if limit_up is not None or limit_down is not None:
                current[wan_interface]['bandwidthLimits'] = {}
                if limit_up is not None:
                    current[wan_interface]['bandwidthLimits']['limitUp'] = limit_up
                if limit_down is not None:
                    current[wan_interface]['bandwidthLimits']['limitDown'] = limit_down
            else:
                # Remove limits
                if 'bandwidthLimits' in current[wan_interface]:
                    del current[wan_interface]['bandwidthLimits']
            
            # Apply settings
            updated = meraki.dashboard.appliance.updateNetworkApplianceUplinksSettings(
                networkId=network_id,
                **current
            )
            
            result = f"""📏 Bandwidth Limits Configured
==================================================

Interface: {wan_interface.upper()}
"""
            
            if limit_up is not None or limit_down is not None:
                result += "\n🚦 Speed Limits Set:"
                if limit_up:
                    result += f"\n   Upload: {limit_up} Mbps"
                if limit_down:
                    result += f"\n   Download: {limit_down} Mbps"
                
                result += "\n\n📊 Why use bandwidth limits?"
                result += "\n   • Prevent ISP overage charges"
                result += "\n   • Match actual ISP speeds"
                result += "\n   • Improve QoS accuracy"
                result += "\n   • Control bandwidth costs"
                
                result += "\n\n⚠️ Important Notes:"
                result += "\n   • Set to 95% of ISP speed"
                result += "\n   • Test actual throughput first"
                result += "\n   • Affects all traffic on interface"
                result += "\n   • QoS rules work within these limits"
                
            else:
                result += "\n✅ Bandwidth limits removed"
                result += "\n   • No speed restrictions"
                result += "\n   • Using full ISP bandwidth"
            
            result += "\n\n💡 Optimization Tips:"
            result += "\n   1. Run speed tests first"
            result += "\n   2. Monitor actual usage"
            result += "\n   3. Adjust based on performance"
            result += "\n   4. Consider time-based limits"
            
            return result
            
    except Exception as e:
        return format_error("set bandwidth limits", e)


def analyze_uplink_health(
    network_id: str,
    timespan: Optional[int] = 86400
) -> str:
    """
    🏥 Analyze overall uplink health and reliability.
    
    Comprehensive analysis of WAN performance and recommendations.
    
    Args:
        network_id: Network ID
        timespan: Analysis period in seconds (default: 86400 = 24 hours)
    
    Returns:
        Health analysis and recommendations
    """
    try:
        with safe_api_call("analyze uplink health"):
            result = f"""🏥 Uplink Health Analysis
==================================================

Analysis Period: Last {timespan // 3600} hours
"""
            
            # Get network info first
            try:
                network = meraki.dashboard.networks.getNetwork(network_id)
            except Exception as e:
                return f"❌ Failed to get network information: {str(e)}"
            
            # Get uplink status
            uplinks = meraki.dashboard.appliance.getNetworkApplianceUplinksSettings(
                networkId=network_id
            )
            
            # Get performance history with error handling
            wan1_history = None
            wan2_history = None
            
            try:
                # Note: This API might have timespan limitations
                actual_timespan = min(timespan, 86400)  # Limit to 24 hours max
                wan1_history = meraki.dashboard.organizations.getOrganizationDevicesUplinksLossAndLatency(
                    network.get('organizationId'),
                    networkId=network_id,
                    timespan=actual_timespan,
                    uplink='wan1'
                )
            except Exception as e:
                # Try alternative API
                try:
                    devices = meraki.dashboard.networks.getNetworkDevices(network_id)
                    mx_device = next((d for d in devices if d.get('model', '').startswith('MX')), None)
                    if mx_device:
                        wan1_history = meraki.dashboard.devices.getDeviceLossAndLatencyHistory(
                            mx_device['serial'],
                            timespan=min(timespan, 300),  # This API may be limited to 5 minutes
                            ip='8.8.8.8'
                        )
                except:
                    pass
            
            # Analyze WAN 1
            if wan1_history:
                total_loss = sum(p.get('lossPercent', 0) for p in wan1_history)
                total_latency = sum(p.get('latencyMs', 0) for p in wan1_history)
                count = len(wan1_history)
                
                avg_loss = total_loss / count if count > 0 else 0
                avg_latency = total_latency / count if count > 0 else 0
                
                result += f"\n📊 WAN 1 Health (to 8.8.8.8):"
                result += f"\n   Avg Packet Loss: {avg_loss:.2f}%"
                result += f"\n   Avg Latency: {avg_latency:.1f} ms"
                
                # Health score
                health_score = 100
                if avg_loss > 0.1:
                    health_score -= min(avg_loss * 10, 30)
                if avg_latency > 50:
                    health_score -= min((avg_latency - 50) / 10, 20)
                
                result += f"\n   Health Score: {health_score:.0f}/100"
                
                if health_score >= 90:
                    result += " 🟢 Excellent"
                elif health_score >= 70:
                    result += " 🟡 Good"
                else:
                    result += " 🔴 Poor"
            
            # Check for failover events
            events = meraki.dashboard.networks.getNetworkEvents(
                networkId=network_id,
                includedEventTypes=["failover"],
                perPage=50
            )
            
            failover_count = len([e for e in events.get('events', []) 
                                if 'failover' in e.get('type', '').lower()])
            
            result += f"\n\n🔄 Stability Metrics:"
            result += f"\n   Failover Events: {failover_count}"
            
            if failover_count == 0:
                result += " ✅ Very Stable"
            elif failover_count < 5:
                result += " 🟡 Mostly Stable"
            else:
                result += " 🔴 Unstable"
            
            # Recommendations
            result += "\n\n💡 Recommendations:"
            
            if avg_loss > 1:
                result += "\n\n🔧 High Packet Loss Detected:"
                result += "\n   1. Contact ISP about line quality"
                result += "\n   2. Check physical connections"
                result += "\n   3. Test with different modem"
                result += "\n   4. Consider backup connection"
            
            if avg_latency > 100:
                result += "\n\n⏱️ High Latency Detected:"
                result += "\n   1. Check for bandwidth saturation"
                result += "\n   2. Enable traffic shaping"
                result += "\n   3. Optimize routing paths"
                result += "\n   4. Consider closer servers"
            
            if failover_count > 5:
                result += "\n\n🔄 Frequent Failovers:"
                result += "\n   1. Increase failover threshold"
                result += "\n   2. Check primary WAN stability"
                result += "\n   3. Review power/environmental issues"
                result += "\n   4. Enable load balancing mode"
            
            # Best practices
            result += "\n\n📋 Best Practices:"
            result += "\n   • Monitor both uplinks regularly"
            result += "\n   • Test failover monthly"
            result += "\n   • Keep firmware updated"
            result += "\n   • Document ISP support contacts"
            result += "\n   • Set up proactive alerts"
            
            return result
            
    except Exception as e:
        return format_error("analyze uplink health", e)


def run_throughput_test(network_id: str) -> str:
    """
    🚀 Run a throughput test on WAN uplinks.
    
    Performs active bandwidth testing to measure actual speeds.
    
    Args:
        network_id: Network ID
        
    Returns:
        Throughput test results or status
    """
    try:
        with safe_api_call("run throughput test"):
            devices = meraki.dashboard.networks.getNetworkDevices(network_id)
            mx_device = next((d for d in devices if d.get('model', '').startswith('MX')), None)
            
            if not mx_device:
                return "❌ No MX device found in this network"
            
            output = ["🚀 Throughput Test", "=" * 50, ""]
            
            try:
                # Trigger throughput test
                try:
                    # Try newer live tools API
                    result = meraki.dashboard.devices.createDeviceLiveToolsThroughputTest(
                        mx_device['serial']
                    )
                except:
                    # Fallback to legacy API
                    result = meraki.dashboard.appliance.createDeviceApplianceThroughputTest(
                        mx_device['serial']
                    )
                
                output.append(f"✅ Throughput test initiated on {mx_device.get('name', mx_device['serial'])}")
                output.append(f"   Model: {mx_device['model']}")
                output.append("")
                output.append("⏱️ Test Status:")
                output.append("   • Test duration: 30-60 seconds")
                output.append("   • Testing both upload and download speeds")
                output.append("   • Results will be available shortly")
                output.append("")
                output.append("💡 Next Steps:")
                output.append("   1. Wait 60 seconds for test completion")
                output.append("   2. Run 'get_throughput_test_results' to see results")
                output.append("   3. Compare with ISP provisioned speeds")
                
            except Exception as e:
                # Try to get existing test results instead
                try:
                    # Try newer API
                    existing_results = meraki.dashboard.devices.getDeviceLiveToolsThroughputTest(
                        mx_device['serial'],
                        id=""  # Empty ID might return latest
                    )
                    if isinstance(existing_results, dict) and 'results' in existing_results:
                        existing_results = existing_results.get('results', [])
                except:
                    # Fallback to legacy API
                    try:
                        existing_results = meraki.dashboard.appliance.getDeviceApplianceThroughputTest(
                            mx_device['serial']
                        )
                    except:
                        existing_results = None
                    
                if existing_results:
                    output.append("📊 Previous Test Results:")
                    for test in existing_results[:3]:  # Show last 3 tests
                        output.append(f"\n   Test Time: {test.get('testTime', 'Unknown')}")
                        output.append(f"   ↓ Download: {test.get('downstream', 0)} Mbps")
                        output.append(f"   ↑ Upload: {test.get('upstream', 0)} Mbps")
                    output.append("\n⚠️ Could not start new test - showing previous results")
                else:
                    output.append(f"⚠️ Could not start test: {str(e)}")
                    output.append("\nPossible reasons:")
                    output.append("• Test already in progress")
                    output.append("• Device offline or unreachable")
                    output.append("• Insufficient permissions")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("run throughput test", e)


def get_throughput_test_results(network_id: str) -> str:
    """
    📈 Get results from throughput tests.
    
    Shows bandwidth test results for WAN connections.
    
    Args:
        network_id: Network ID
        
    Returns:
        Throughput test results
    """
    try:
        with safe_api_call("get throughput test results"):
            devices = meraki.dashboard.networks.getNetworkDevices(network_id)
            mx_device = next((d for d in devices if d.get('model', '').startswith('MX')), None)
            
            if not mx_device:
                return "❌ No MX device found in this network"
            
            output = ["📈 Throughput Test Results", "=" * 50, ""]
            
            # Get test results
            try:
                # Try the live tools API first (newer)
                test_id = ""  # Would need to get from createDeviceLiveToolsThroughputTest
                results = meraki.dashboard.devices.getDeviceLiveToolsThroughputTest(
                    mx_device['serial'],
                    id=test_id
                )
                # Convert to list format if needed
                if isinstance(results, dict) and 'results' in results:
                    results = results.get('results', [])
            except:
                # Fallback to legacy API
                try:
                    results = meraki.dashboard.appliance.getDeviceApplianceThroughputTest(
                        mx_device['serial']
                    )
                except:
                    results = None
            
            if results:
                output.append(f"Device: {mx_device.get('name', mx_device['serial'])} ({mx_device['model']})")
                output.append("")
                
                for i, test in enumerate(results[:5]):  # Show last 5 tests
                    output.append(f"Test #{i+1}:")
                    output.append(f"   Time: {test.get('testTime', 'Unknown')}")
                    output.append(f"   📥 Download: {test.get('downstream', 0)} Mbps")
                    output.append(f"   📤 Upload: {test.get('upstream', 0)} Mbps")
                    output.append("")
                
                # Calculate averages if multiple tests
                if len(results) > 1:
                    avg_down = sum(t.get('downstream', 0) for t in results) / len(results)
                    avg_up = sum(t.get('upstream', 0) for t in results) / len(results)
                    output.append("📊 Average Speeds:")
                    output.append(f"   Download: {avg_down:.2f} Mbps")
                    output.append(f"   Upload: {avg_up:.2f} Mbps")
                    
            else:
                output.append("No throughput test results available")
                output.append("\n💡 Run 'run_throughput_test' first to measure speeds")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("get throughput test results", e)


def uplink_monitoring_help() -> str:
    """
    ❓ Get help with uplink monitoring tools.
    
    Shows available tools and monitoring best practices.
    
    Returns:
        Formatted help guide
    """
    return """🌐 Uplink Monitoring Tools Help
==================================================

Available tools for WAN monitoring:

1. get_uplink_status()
   - View current WAN status
   - Check active interfaces
   - See load balancing mode

2. get_uplink_bandwidth_history()
   - Historical bandwidth usage
   - Performance metrics over time
   - Loss and latency trends

3. get_failover_events()
   - WAN failover history
   - Identify failure patterns
   - Analyze stability issues

4. configure_uplink_settings()
   - Set load balancing mode
   - Configure failover behavior
   - Adjust traffic weights

5. set_bandwidth_limits()
   - Configure speed limits
   - Match ISP speeds
   - Control bandwidth usage

6. analyze_uplink_health()
   - Comprehensive health check
   - Performance analysis
   - Get recommendations

7. get_realtime_bandwidth_usage()
   - Real-time bandwidth monitoring
   - Current upload/download speeds
   - Per-interface usage

8. run_throughput_test()
   - Active bandwidth testing
   - Measure actual WAN speeds
   - Test upload and download

9. get_throughput_test_results()
   - View test results
   - Historical test data
   - Average speeds

Common Monitoring Tasks:

📊 "Check WAN performance"
1. get_uplink_bandwidth_history()
2. analyze_uplink_health()
3. Review recommendations

🔄 "Investigate failovers"
1. get_failover_events()
2. Check event patterns
3. Adjust thresholds if needed

⚖️ "Set up load balancing"
1. configure_uplink_settings("loadBalance")
2. Set appropriate weights
3. Monitor bandwidth distribution

💡 Monitoring Best Practices:
- Check uplinks daily
- Review failover events weekly
- Test failover monthly
- Update bandwidth limits quarterly
- Document ISP information

🚨 Alert Recommendations:
- WAN failover events
- High packet loss (>1%)
- High latency (>150ms)
- Bandwidth saturation (>90%)
- Extended downtime
"""


def register_uplink_monitoring_tools(app: FastMCP, meraki_client: MerakiClient):
    """Register all uplink monitoring tools with the MCP server."""
    global mcp_app, meraki
    mcp_app = app
    meraki = meraki_client
    
    # Register all tools
    tools = [
        (get_uplink_status, "View current WAN uplink status"),
        (get_uplink_bandwidth_history, "Get historical bandwidth usage"),
        (get_realtime_bandwidth_usage, "Get real-time bandwidth usage"),
        (get_failover_events, "View WAN failover event history"),
        (configure_uplink_settings, "Configure load balancing and failover"),
        (set_bandwidth_limits, "Set bandwidth limits per interface"),
        (analyze_uplink_health, "Analyze overall uplink health"),
        (run_throughput_test, "Run active bandwidth speed test"),
        (get_throughput_test_results, "Get throughput test results"),
        (uplink_monitoring_help, "Get help with uplink monitoring"),
    ]
    
    for tool_func, description in tools:
        app.tool(
            name=tool_func.__name__,
            description=description
        )(tool_func)