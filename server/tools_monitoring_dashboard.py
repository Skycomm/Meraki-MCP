"""
Enhanced Monitoring Dashboard for Cisco Meraki MCP Server
Combine multiple APIs for comprehensive network health monitoring
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


def get_network_health_summary(network_id: str, timespan: Optional[int] = 300) -> str:
    """
    🏥 Get comprehensive network health summary.
    
    Combines multiple health metrics into a single dashboard view.
    
    Args:
        network_id: Network ID to monitor
        timespan: Time period in seconds (default: 300 = 5 minutes, max: 2592000 = 30 days)
        
    Returns:
        Comprehensive health summary
    """
    try:
        output = ["🏥 Network Health Summary", "=" * 50, ""]
        
        # Initialize counters
        online_count = 0
        alerting_count = 0
        offline_count = 0
        client_count = 0
        
        # Network info
        try:
            network = meraki.get_network(network_id)
            output.append(f"Network: {network['name']}")
            output.append(f"Type: {', '.join(network.get('productTypes', []))}")
            output.append("")
        except:
            pass
        
        # Device statuses
        try:
            with safe_api_call("get device statuses"):
                statuses = meraki.get_organization_devices_statuses(
                    network['organizationId'],
                    network_ids=[network_id]
                )
                
                if statuses:
                    output.append("📡 Infrastructure Device Status (Switches, APs, Firewalls):")
                    output.append("   ℹ️  These are Meraki hardware devices, not user devices")
                    online_count = sum(1 for s in statuses if s.get('status') == 'online')
                    alerting_count = sum(1 for s in statuses if s.get('status') == 'alerting')
                    offline_count = sum(1 for s in statuses if s.get('status') == 'offline')
                    
                    output.append(f"   ✅ Online: {online_count}")
                    if alerting_count > 0:
                        output.append(f"   ⚠️ Alerting: {alerting_count}")
                    if offline_count > 0:
                        output.append(f"   ❌ Offline: {offline_count}")
                    
                    # Show problem devices
                    for device in statuses:
                        if device.get('status') != 'online':
                            output.append(f"   - {device.get('name', 'Unknown')} ({device.get('model', '')}): {device.get('status', 'unknown').upper()}")
                    output.append("")
        except:
            output.append("⚠️ Could not retrieve device statuses\n")
        
        # Connection stats (clients)
        try:
            with safe_api_call("get connection stats"):
                conn_stats = meraki.get_network_clients_connection_stats(
                    network_id,
                    timespan=timespan
                )
                
                if conn_stats:
                    output.append("👥 Connected Client Devices (Computers, Phones, Tablets, etc.):")
                    output.append("   ℹ️  These are end-user devices connected to the network")
                    client_count = conn_stats.get('totalCount', 0)
                    output.append(f"   Connected Devices: {client_count}")
                    
                    # Connection success rate
                    assoc = conn_stats.get('assoc', 0)
                    auth = conn_stats.get('auth', 0) 
                    dhcp = conn_stats.get('dhcp', 0)
                    dns = conn_stats.get('dns', 0)
                    success = conn_stats.get('success', 0)
                    
                    if assoc > 0:
                        output.append(f"   Association Success: {(auth/assoc*100):.1f}%")
                    if auth > 0:
                        output.append(f"   Authentication Success: {(dhcp/auth*100):.1f}%")
                    if dhcp > 0:
                        output.append(f"   DHCP Success: {(dns/dhcp*100):.1f}%")
                    if dns > 0:
                        output.append(f"   DNS Success: {(success/dns*100):.1f}%")
                    
                    output.append("")
        except:
            pass
        
        # Uplink status with packet loss
        try:
            with safe_api_call("get uplink status"):
                devices = meraki.get_network_devices(network_id)
                mx_devices = [d for d in devices if d.get('model', '').startswith('MX')]
                
                if mx_devices:
                    for mx in mx_devices:
                        try:
                            uplinks = meraki.get_device_appliance_uplinks_settings(mx['serial'])
                            output.append(f"🌐 WAN Status ({mx['name']}):")
                            
                            # Get uplink statuses with loss/latency
                            try:
                                org_uplinks = meraki.dashboard.appliance.getOrganizationApplianceUplinkStatuses(
                                    network.get('organizationId')
                                )
                                network_uplinks = next((u for u in org_uplinks if u.get('networkId') == network_id), None)
                                
                                if network_uplinks:
                                    for uplink in network_uplinks.get('uplinks', []):
                                        interface = uplink.get('interface', '').upper()
                                        status = uplink.get('status', 'unknown')
                                        
                                        status_icon = '🟢' if status == 'active' else '🔴'
                                        output.append(f"   {interface}: {status_icon} {status.title()}")
                                        
                                        # Try to get recent loss/latency
                                        try:
                                            perf_data = meraki.dashboard.organizations.getOrganizationDevicesUplinksLossAndLatency(
                                                network.get('organizationId'),
                                                networkId=network_id,
                                                timespan=300,  # Last 5 minutes
                                                uplink=interface.lower()
                                            )
                                            if perf_data:
                                                recent = perf_data[-5:] if len(perf_data) > 5 else perf_data
                                                avg_loss = sum(p.get('lossPercent', 0) for p in recent) / len(recent) if recent else 0
                                                
                                                # Calculate average latency, excluding zeros
                                                latencies = [p.get('latencyMs', 0) for p in recent if p.get('latencyMs', 0) > 0]
                                                avg_latency = sum(latencies) / len(latencies) if latencies else None
                                                
                                                loss_icon = '🟢' if avg_loss < 1 else '🟡' if avg_loss < 5 else '🔴'
                                                output.append(f"     Packet Loss: {loss_icon} {avg_loss:.1f}%")
                                                
                                                if avg_latency is not None:
                                                    lat_icon = '🟢' if avg_latency < 50 else '🟡' if avg_latency < 100 else '🔴'
                                                    output.append(f"     Latency: {lat_icon} {avg_latency:.1f} ms")
                                                else:
                                                    output.append(f"     Latency: Checking...")
                                        except:
                                            pass
                            except:
                                # Fallback to just showing enabled/disabled
                                for interface in uplinks.get('interfaces', {}).values():
                                    if interface.get('enabled'):
                                        wan = interface.get('wan', {})
                                        output.append(f"   {wan.get('interface', 'Unknown')}:")
                                        output.append(f"     Status: {'✅ Enabled' if wan.get('enabled') else '❌ Disabled'}")
                            output.append("")
                        except:
                            pass
        except:
            pass
        
        # Recent alerts
        try:
            with safe_api_call("get alerts"):
                end_time = datetime.utcnow()
                start_time = end_time - timedelta(seconds=timespan)
                
                alerts = meraki.get_organization_alerts(
                    network['organizationId']
                )
                
                # Note: This would need actual alerts history API
                output.append("🚨 Recent Alerts:")
                output.append("   (Alert history requires specific API endpoint)")
                output.append("")
        except:
            pass
        
        # Performance metrics
        try:
            with safe_api_call("get performance"):
                # Try to get latency stats if available
                output.append("📊 Performance Metrics:")
                output.append(f"   Time Range: Last {timespan//60} minutes")
                
                # For MX devices, check if we can get latency stats
                if mx_devices:
                    try:
                        for mx in mx_devices[:1]:  # Just first MX
                            loss_and_latency = meraki.get_device_loss_and_latency_history(
                                mx['serial'],
                                timespan=min(timespan, 300),  # Max 5 minutes
                                ip='8.8.8.8'
                            )
                            
                            if loss_and_latency:
                                avg_latency = sum(item.get('latencyMs', 0) for item in loss_and_latency) / len(loss_and_latency)
                                avg_loss = sum(item.get('lossPercent', 0) for item in loss_and_latency) / len(loss_and_latency)
                                
                                output.append(f"   WAN to 8.8.8.8:")
                                output.append(f"     Avg Latency: {avg_latency:.1f} ms")
                                output.append(f"     Avg Loss: {avg_loss:.1f}%")
                    except:
                        output.append("   (Performance data limited to 5 minutes)")
                
                output.append("")
        except:
            pass
        
        # Device Summary Box
        output.append("📊 Device Summary:")
        output.append("=" * 50)
        output.append(f"Infrastructure Devices: {online_count} online")
        output.append(f"Client Devices: {client_count} connected")
        output.append("=" * 50)
        output.append("")
        
        # Overall health status
        output.append("📈 Network Health:")
        # Simple health calculation based on infrastructure devices
        health_score = 100
        if offline_count > 0:
            health_score -= (offline_count * 20)
        if alerting_count > 0:
            health_score -= (alerting_count * 10)
        
        health_icon = "🟢" if health_score >= 80 else "🟡" if health_score >= 60 else "🔴"
        output.append(f"   Health Score: {health_icon} {max(0, health_score)}%")
        output.append("   ℹ️  Score based on infrastructure device status")
        
        return "\n".join(output)
        
    except Exception as e:
        return format_error("get network health summary", e)


def get_uplink_bandwidth_summary(
    network_id: str,
    timespan: Optional[int] = 3600,
    resolution: Optional[int] = 300
) -> str:
    """
    📈 Get bandwidth usage summary for WAN uplinks.
    
    Shows bandwidth trends overview.
    
    Args:
        network_id: Network ID to monitor
        timespan: Time period in seconds (default: 3600 = 1 hour, max: 2592000 = 30 days)
        resolution: Data resolution in seconds (300, 600, 1800, 3600, 86400)
        
    Returns:
        Bandwidth usage summary
    """
    try:
        output = ["📈 Uplink Bandwidth History", "=" * 50, ""]
        
        # Get MX devices
        devices = meraki.dashboard.networks.getNetworkDevices(network_id)
        mx_devices = [d for d in devices if d.get('model', '').startswith('MX')]
        
        if not mx_devices:
            return "❌ No MX devices found in this network"
        
        # Add time range header
        hours = timespan // 3600
        minutes = (timespan % 3600) // 60
        if hours > 0:
            output.append(f"⏰ Time Range: Last {hours} hour{'s' if hours > 1 else ''}")
        else:
            output.append(f"⏰ Time Range: Last {minutes} minutes")
        output.append(f"📊 Resolution: {resolution // 60} minute intervals")
        
        for mx in mx_devices:
            output.append(f"\n🔧 Device: {mx['name']} ({mx['model']})")
            
            try:
                with safe_api_call(f"get bandwidth for {mx['name']}"):
                    # Get uplink bandwidth usage
                    bandwidth = meraki.dashboard.appliance.getNetworkApplianceUplinksUsageHistory(
                        network_id,
                        timespan=timespan,
                        resolution=resolution
                    )
                    
                    if bandwidth:
                        # Group by interface
                        by_interface = {}
                        for entry in bandwidth:
                            # Each entry has a byInterface array
                            for iface_data in entry.get('byInterface', []):
                                interface = iface_data.get('interface', 'Unknown')
                                if interface not in by_interface:
                                    by_interface[interface] = {
                                        'sent': [],
                                        'received': [],
                                        'timestamps': []
                                    }
                                
                                by_interface[interface]['sent'].append(iface_data.get('sent', 0))
                                by_interface[interface]['received'].append(iface_data.get('received', 0))
                                by_interface[interface]['timestamps'].append(entry.get('startTime', ''))
                        
                        # Display summary for each interface
                        for interface, data in by_interface.items():
                            output.append(f"\n   {interface}:")
                            
                            if data['sent']:
                                avg_sent = sum(data['sent']) / len(data['sent'])
                                max_sent = max(data['sent'])
                                avg_received = sum(data['received']) / len(data['received'])
                                max_received = max(data['received'])
                                
                                # Convert bytes to Mbps: (bytes * 8) / 1_000_000 / time_period_seconds
                                # Resolution is in seconds, so divide by it to get rate
                                time_divisor = resolution  # Time period in seconds
                                
                                output.append(f"     📤 Upload:")
                                output.append(f"        Average: {(avg_sent * 8)/1000000/time_divisor:.2f} Mbps")
                                output.append(f"        Peak: {(max_sent * 8)/1000000/time_divisor:.2f} Mbps")
                                
                                output.append(f"     📥 Download:")
                                output.append(f"        Average: {(avg_received * 8)/1000000/time_divisor:.2f} Mbps")
                                output.append(f"        Peak: {(max_received * 8)/1000000/time_divisor:.2f} Mbps")
                                
                                # Show recent trend
                                if len(data['sent']) >= 3:
                                    recent = data['sent'][-3:]
                                    trend = "📈" if recent[-1] > recent[0] else "📉" if recent[-1] < recent[0] else "➡️"
                                    output.append(f"     Trend: {trend}")
                    else:
                        output.append("   No bandwidth data available")
            except Exception as e:
                output.append(f"   ⚠️ Could not get bandwidth data: {str(e)}")
        
        # Time range info
        output.append(f"\n⏱️ Time Range: {timespan//3600} hours" if timespan >= 3600 else f"\n⏱️ Time Range: {timespan//60} minutes")
        output.append(f"📊 Resolution: {resolution//60} minutes")
        
        return "\n".join(output)
        
    except Exception as e:
        return format_error("get uplink bandwidth history", e)


def get_critical_alerts(
    network_id: str,
    timespan: Optional[int] = 86400,
    product_type: Optional[str] = None
) -> str:
    """
    🚨 Get critical alerts and events for a network.
    
    Shows high-priority network issues.
    
    Args:
        network_id: Network ID to check
        timespan: Time period in seconds (default: 86400 = 24 hours)
        product_type: Filter by product type (appliance, wireless, switch, camera, etc.)
                     If not specified, will try to get events for all product types
        
    Returns:
        Critical alerts and events
    """
    try:
        output = ["🚨 Critical Alerts & Events", "=" * 50, ""]
        
        # Get network info for display and to determine product types
        network_info = None
        network_types = []
        try:
            network_info = meraki.dashboard.networks.getNetwork(network_id)
            output.append(f"Network: {network_info.get('name', network_id)}")
            
            # Parse product types from network
            if 'productTypes' in network_info:
                network_types = network_info['productTypes']
            else:
                # Fall back to checking devices if productTypes not available
                devices = meraki.dashboard.networks.getNetworkDevices(network_id)
                device_types = set()
                for device in devices:
                    model = device.get('model', '')
                    if model.startswith('MX'):
                        device_types.add('appliance')
                    elif model.startswith('MS'):
                        device_types.add('switch')
                    elif model.startswith('MR'):
                        device_types.add('wireless')
                    elif model.startswith('MV'):
                        device_types.add('camera')
                network_types = list(device_types)
        except:
            output.append(f"Network: {network_id}")
        
        # Display time range
        hours = timespan // 3600
        if hours >= 24:
            time_desc = f"{hours // 24} day{'s' if hours // 24 > 1 else ''}"
        elif hours > 0:
            time_desc = f"{hours} hour{'s' if hours > 1 else ''}"
        else:
            time_desc = f"{timespan // 60} minutes"
        
        output.append(f"Time Range: Last {time_desc}")
        output.append("")
        
        # Get network events
        all_events = []
        errors = []
        
        # If specific product type requested, use that
        if product_type:
            types_to_check = [product_type]
        # If we have multiple network types, check each
        elif len(network_types) > 1:
            types_to_check = network_types
        # Otherwise try without productType first
        else:
            types_to_check = [None]
        
        for ptype in types_to_check:
            try:
                with safe_api_call("get network events"):
                    params = {
                        'perPage': 100
                    }
                    if ptype:
                        params['productType'] = ptype
                    
                    events = meraki.dashboard.networks.getNetworkEvents(
                        network_id,
                        **params
                    )
                    
                    if events and 'events' in events:
                        all_events.extend(events['events'])
            except Exception as e:
                error_msg = str(e)
                # If we get productType required error, try with product types
                if 'productType is required' in error_msg and not ptype and len(network_types) == 0:
                    # Try common product types
                    for common_type in ['appliance', 'wireless', 'switch', 'camera']:
                        try:
                            events = meraki.dashboard.networks.getNetworkEvents(
                                network_id,
                                productType=common_type,
                                perPage=100
                            )
                            if events and 'events' in events:
                                all_events.extend(events['events'])
                        except:
                            continue
                elif ptype:
                    errors.append(f"Could not get {ptype} events: {error_msg}")
        
        # Process all collected events
        if all_events:
            # Filter critical events
            critical_types = [
                'went_down', 'came_up', 'reboot', 'failover',
                'critical', 'alert', 'error', 'warning'
            ]
            
            critical_events = []
            # Note: Since we can't filter by time in the API call, we get recent events
            # The API returns the most recent events by default
            for event in all_events:
                event_type = event.get('type', '').lower()
                if any(crit in event_type for crit in critical_types):
                    critical_events.append(event)
            
            if critical_events:
                output.append(f"Found {len(critical_events)} critical events:")
                
                # Group by category
                by_category = {}
                for event in critical_events[:20]:  # Show max 20
                    category = event.get('category', 'Other')
                    if category not in by_category:
                        by_category[category] = []
                    by_category[category].append(event)
                
                for category, cat_events in by_category.items():
                    output.append(f"\n📁 {category}:")
                    for event in cat_events:
                        timestamp = event.get('occurredAt', 'Unknown time')
                        event_type = event.get('type', 'Unknown')
                        description = event.get('description', 'No description')
                        device_name = event.get('deviceName', '')
                        
                        # Event icon
                        icon = "🔴" if 'down' in event_type.lower() else "🟢" if 'up' in event_type.lower() else "⚠️"
                        
                        output.append(f"   {icon} {timestamp}")
                        if device_name:
                            output.append(f"      Device: {device_name}")
                        output.append(f"      Type: {event_type}")
                        output.append(f"      {description}")
            else:
                output.append("✅ No critical events in the specified time range")
        else:
            output.append("⚠️ No events data available")
            
        # Show any errors encountered
        if errors:
            output.append("\n⚠️ Some event types could not be retrieved:")
            for error in errors:
                output.append(f"   • {error}")
        
        # Check current device alerts
        try:
            devices = meraki.get_network_devices(network_id)
            alerting_devices = []
            
            # Get org_id from network
            try:
                network = meraki.dashboard.networks.getNetwork(network_id)
                org_id = network.get('organizationId')
            except:
                org_id = None
            
            if org_id:
                for device in devices:
                    try:
                        status = meraki.dashboard.organizations.getOrganizationDevicesStatuses(
                            org_id,
                            serials=[device['serial']]
                        )
                        if status and status[0].get('status') == 'alerting':
                            alerting_devices.append(device)
                    except:
                        pass
                
                if alerting_devices:
                    output.append(f"\n⚠️ Currently Alerting Devices:")
                    for device in alerting_devices:
                        output.append(f"   • {device['name']} ({device['model']})")
        except:
            pass
        
        return "\n".join(output)
        
    except Exception as e:
        return format_error("get critical alerts", e)


def get_device_utilization(network_id: str, timespan: Optional[int] = 300) -> str:
    """
    💻 Get device CPU and memory utilization.
    
    Shows resource usage for network devices.
    
    Args:
        network_id: Network ID to monitor
        timespan: Time period in seconds (default: 300 = 5 minutes)
        
    Returns:
        Device utilization metrics
    """
    try:
        output = ["💻 Device Utilization", "=" * 50, ""]
        
        # Get all devices
        devices = meraki.dashboard.networks.getNetworkDevices(network_id)
        
        if not devices:
            return "❌ No devices found in this network"
        
        # Check each device type
        for device in devices:
            output.append(f"\n🔧 {device['name']} ({device['model']})")
            device_serial = device['serial']
            
            # MX devices - Performance scores
            if device['model'].startswith('MX'):
                try:
                    with safe_api_call(f"get MX performance for {device['name']}"):
                        # Get performance score
                        perf = meraki.dashboard.appliance.getDeviceAppliancePerformance(device_serial)
                        
                        if perf:
                            output.append("   Performance Score:")
                            if 'perfScore' in perf:
                                score = perf['perfScore']
                                score_icon = "🟢" if score >= 80 else "🟡" if score >= 60 else "🔴"
                                output.append(f"     Overall: {score_icon} {score}/100")
                            
                            # Show any performance issues
                            if 'alerts' in perf and perf['alerts']:
                                output.append("   ⚠️ Performance Alerts:")
                                for alert in perf['alerts']:
                                    output.append(f"     • {alert}")
                except:
                    output.append("   Performance data not available")
            
            # MS switches - Port utilization
            elif device['model'].startswith('MS'):
                try:
                    with safe_api_call(f"get switch stats for {device['name']}"):
                        # Get switch port statuses
                        port_statuses = meraki.switch.getDeviceSwitchPortsStatuses(
                            device_serial,
                            timespan=timespan
                        )
                        
                        if port_statuses:
                            total_ports = len(port_statuses)
                            active_ports = sum(1 for p in port_statuses if p.get('status') == 'Connected')
                            
                            output.append(f"   Port Utilization:")
                            output.append(f"     Active Ports: {active_ports}/{total_ports}")
                            output.append(f"     Utilization: {(active_ports/total_ports*100):.1f}%")
                            
                            # Check for errors
                            error_ports = [p for p in port_statuses if p.get('errors', [])]
                            if error_ports:
                                output.append(f"     ⚠️ Ports with errors: {len(error_ports)}")
                except:
                    output.append("   Port statistics not available")
            
            # MR access points - Client load
            elif device['model'].startswith('MR'):
                try:
                    with safe_api_call(f"get AP stats for {device['name']}"):
                        # Get wireless status
                        status = meraki.dashboard.wireless.getDeviceWirelessStatus(device_serial)
                        
                        if status:
                            output.append("   Wireless Status:")
                            
                            # Basic info
                            for ssid in status.get('basicServiceSets', []):
                                ssid_name = ssid.get('ssidName', 'Unknown')
                                if ssid.get('enabled'):
                                    output.append(f"     SSID: {ssid_name}")
                                    output.append(f"       Band: {ssid.get('band', 'Unknown')}")
                                    output.append(f"       Channel: {ssid.get('channel', 'Unknown')}")
                                    output.append(f"       Power: {ssid.get('power', 'Unknown')} dBm")
                except:
                    output.append("   Wireless statistics not available")
            
            # General device info
            try:
                # Try to get uptime
                status = meraki.dashboard.organizations.getOrganizationDevicesStatuses(
                    device.get('organizationId', network_id),
                    serials=[device_serial]
                )
                
                if status and status[0]:
                    device_status = status[0]
                    output.append(f"   Status: {device_status.get('status', 'Unknown').upper()}")
                    
                    # Last reported
                    if 'lastReportedAt' in device_status:
                        output.append(f"   Last Seen: {device_status['lastReportedAt']}")
            except:
                pass
        
        return "\n".join(output)
        
    except Exception as e:
        return format_error("get device utilization", e)


def get_vpn_performance_stats(network_id: str, timespan: Optional[int] = 3600) -> str:
    """
    🔒 Get VPN tunnel performance statistics.
    
    Shows VPN connectivity and performance metrics.
    
    Args:
        network_id: Network ID to monitor
        timespan: Time period in seconds (default: 3600 = 1 hour)
        
    Returns:
        VPN performance statistics
    """
    try:
        output = ["🔒 VPN Performance Statistics", "=" * 50, ""]
        
        # Get VPN stats
        try:
            with safe_api_call("get VPN stats"):
                vpn_stats = meraki.dashboard.appliance.getNetworkApplianceVpnStats(
                    network_id,
                    timespan=timespan
                )
                
                if vpn_stats:
                    # Site-to-site VPN stats
                    if 'merakiVpnPeers' in vpn_stats:
                        output.append("🏢 Site-to-Site VPN:")
                        
                        for peer in vpn_stats['merakiVpnPeers']:
                            peer_name = peer.get('networkName', 'Unknown')
                            output.append(f"\n   Peer: {peer_name}")
                            
                            # Connection status
                            if 'usageSummary' in peer:
                                summary = peer['usageSummary']
                                sent_kb = summary.get('sentKilobytes', 0)
                                recv_kb = summary.get('receivedKilobytes', 0)
                                
                                output.append(f"     📤 Sent: {sent_kb/1024:.2f} MB")
                                output.append(f"     📥 Received: {recv_kb/1024:.2f} MB")
                            
                            # Latency stats
                            if 'latencySummary' in peer:
                                latency = peer['latencySummary']
                                avg_ms = latency.get('averageMs', 0)
                                min_ms = latency.get('minimumMs', 0)
                                max_ms = latency.get('maximumMs', 0)
                                
                                output.append(f"     ⏱️ Latency:")
                                output.append(f"        Avg: {avg_ms:.1f} ms")
                                output.append(f"        Min/Max: {min_ms:.1f}/{max_ms:.1f} ms")
                            
                            # Loss stats
                            if 'lossSummary' in peer:
                                loss = peer['lossSummary']
                                avg_loss = loss.get('averagePercentage', 0)
                                
                                loss_icon = "🟢" if avg_loss < 1 else "🟡" if avg_loss < 5 else "🔴"
                                output.append(f"     {loss_icon} Loss: {avg_loss:.1f}%")
                            
                            # Jitter stats
                            if 'jitterSummary' in peer:
                                jitter = peer['jitterSummary']
                                avg_jitter = jitter.get('averageMs', 0)
                                
                                output.append(f"     📊 Jitter: {avg_jitter:.1f} ms")
                    
                    # Non-Meraki VPN peers
                    if 'nonMerakiVpnPeers' in vpn_stats:
                        output.append("\n🌐 Non-Meraki VPN Peers:")
                        
                        for peer in vpn_stats['nonMerakiVpnPeers']:
                            peer_name = peer.get('peerName', 'Unknown')
                            peer_ip = peer.get('peerIp', 'Unknown')
                            
                            output.append(f"\n   Peer: {peer_name} ({peer_ip})")
                            
                            # Connection status
                            if 'connectionStatus' in peer:
                                status = peer['connectionStatus']
                                status_icon = "🟢" if status == 'connected' else "🔴"
                                output.append(f"     Status: {status_icon} {status.upper()}")
                            
                            # Usage
                            if 'usageSummary' in peer:
                                summary = peer['usageSummary']
                                sent_kb = summary.get('sentKilobytes', 0)
                                recv_kb = summary.get('receivedKilobytes', 0)
                                
                                output.append(f"     📤 Sent: {sent_kb/1024:.2f} MB")
                                output.append(f"     📥 Received: {recv_kb/1024:.2f} MB")
                    
                    # Client VPN stats
                    if 'clientVpn' in vpn_stats:
                        client_vpn = vpn_stats['clientVpn']
                        output.append("\n👤 Client VPN:")
                        
                        active_users = client_vpn.get('activeUsers', 0)
                        total_usage_kb = client_vpn.get('totalUsageKilobytes', 0)
                        
                        output.append(f"   Active Users: {active_users}")
                        output.append(f"   Total Usage: {total_usage_kb/1024:.2f} MB")
                else:
                    output.append("No VPN statistics available")
                    
        except Exception as e:
            if "404" in str(e):
                output.append("VPN not configured on this network")
            else:
                output.append(f"Could not retrieve VPN stats: {str(e)}")
        
        return "\n".join(output)
        
    except Exception as e:
        return format_error("get VPN performance stats", e)


def generate_monitoring_dashboard_report(
    network_id: str,
    include_bandwidth: bool = True,
    include_vpn: bool = True,
    include_devices: bool = True,
    timespan: Optional[int] = 3600
) -> str:
    """
    📊 Generate comprehensive monitoring dashboard report.
    
    Combines all monitoring data into a single report.
    
    Args:
        network_id: Network ID to report on
        include_bandwidth: Include bandwidth history
        include_vpn: Include VPN statistics  
        include_devices: Include device utilization
        timespan: Time period in seconds (default: 3600 = 1 hour)
        
    Returns:
        Comprehensive monitoring report
    """
    try:
        output = ["📊 COMPREHENSIVE NETWORK HEALTH REPORT", "=" * 60, ""]
        
        # Header with timestamp
        output.append(f"Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")
        output.append(f"Time Range: Last {timespan//3600} hours" if timespan >= 3600 else f"Time Range: Last {timespan//60} minutes")
        output.append("")
        
        # Executive Summary
        output.append("📋 EXECUTIVE SUMMARY")
        output.append("-" * 40)
        summary = get_network_health_summary(network_id, timespan)
        output.append(summary)
        output.append("")
        
        # Device Utilization
        if include_devices:
            output.append("\n📟 DEVICE UTILIZATION")
            output.append("-" * 40)
            device_util = get_device_utilization(network_id, min(timespan, 300))
            output.append(device_util)
            output.append("")
        
        # Bandwidth Analysis
        if include_bandwidth:
            output.append("\n📈 BANDWIDTH ANALYSIS")
            output.append("-" * 40)
            bandwidth = get_uplink_bandwidth_summary(network_id, timespan)
            output.append(bandwidth)
            output.append("")
        
        # VPN Performance
        if include_vpn:
            output.append("\n🔒 VPN PERFORMANCE")
            output.append("-" * 40)
            vpn_stats = get_vpn_performance_stats(network_id, timespan)
            output.append(vpn_stats)
            output.append("")
        
        # Recommendations
        output.extend([
            "\n💡 RECOMMENDATIONS",
            "-" * 40,
            "Based on the analysis:",
            "• Monitor devices showing alerting status",
            "• Review bandwidth peaks for capacity planning",
            "• Check VPN peers with high latency or loss",
            "• Investigate any authentication failures",
            "",
            "📅 Next Steps:",
            "1. Schedule regular health checks",
            "2. Set up alerts for critical thresholds",
            "3. Plan maintenance for underperforming devices",
            "4. Review and optimize traffic shaping rules"
        ])
        
        return "\n".join(output)
        
    except Exception as e:
        return format_error("generate health report", e)


# Helper tool
def check_monitoring_prerequisites(network_id: str) -> str:
    """
    🔍 Check monitoring capabilities for this network.
    
    ALWAYS RUN THIS FIRST to understand available metrics!
    
    Args:
        network_id: Network ID to check
        
    Returns:
        Available monitoring features
    """
    try:
        output = ["🔍 Monitoring Prerequisites Check", "=" * 50, ""]
        
        # Get network info
        try:
            network = meraki.dashboard.networks.getNetwork(network_id)
            output.append(f"Network: {network['name']}")
            output.append(f"Product Types: {', '.join(network.get('productTypes', []))}")
            output.append("")
        except:
            output.append("⚠️ Could not retrieve network info")
            return "\n".join(output)
        
        # Check device types
        devices = meraki.dashboard.networks.getNetworkDevices(network_id)
        device_types = {}
        for device in devices:
            model_prefix = device['model'][:2]
            if model_prefix not in device_types:
                device_types[model_prefix] = 0
            device_types[model_prefix] += 1
        
        output.append("📡 Device Inventory:")
        for dev_type, count in device_types.items():
            type_name = {
                'MX': 'Security Appliances',
                'MS': 'Switches',
                'MR': 'Access Points',
                'MV': 'Cameras',
                'MG': 'Cellular Gateways'
            }.get(dev_type, 'Other')
            output.append(f"   {dev_type}: {count} {type_name}")
        
        # Check available features
        output.append("\n✅ Available Monitoring Features:")
        
        features_to_check = [
            ("Device Status", lambda: meraki.dashboard.organizations.getOrganizationDevicesStatuses(network['organizationId'], networkIds=[network_id])),
            ("Client Stats", lambda: meraki.dashboard.networks.getNetworkClientsConnectionStats(network_id, timespan=300)),
            ("Events", lambda: meraki.dashboard.networks.getNetworkEvents(network_id, perPage=1)),
        ]
        
        if 'MX' in device_types:
            features_to_check.extend([
                ("Bandwidth History", lambda: meraki.dashboard.appliance.getNetworkApplianceUplinksUsageHistory(network_id, timespan=300)),
                ("VPN Stats", lambda: meraki.dashboard.appliance.getNetworkApplianceVpnStats(network_id, timespan=300)),
                ("Performance", lambda: meraki.dashboard.appliance.getDeviceAppliancePerformance(devices[0]['serial']))
            ])
        
        for feature_name, check_func in features_to_check:
            try:
                check_func()
                output.append(f"   ✅ {feature_name}")
            except:
                output.append(f"   ❌ {feature_name}")
        
        # Recommendations
        output.extend([
            "\n💡 Usage Tips:",
            "1. Start with get_network_health_summary() for overview",
            "2. Use specific tools for detailed analysis",
            "3. Generate reports for documentation",
            "",
            "⚠️ Limitations:",
            "• Packet loss monitoring: 5 minutes max",
            "• Some metrics require specific device types",
            "• Historical data varies by metric type"
        ])
        
        return "\n".join(output)
        
    except Exception as e:
        return format_error("check prerequisites", e)


def register_monitoring_dashboard_tools(app: FastMCP, client: MerakiClient):
    """Register enhanced monitoring dashboard tools with the MCP server."""
    global mcp_app, meraki
    mcp_app = app
    meraki = client
    
    # Register all tools
    app.tool()(get_network_health_summary)
    app.tool()(get_uplink_bandwidth_summary)
    app.tool()(get_critical_alerts)
    app.tool()(get_device_utilization)
    app.tool()(get_vpn_performance_stats)
    app.tool()(generate_monitoring_dashboard_report)
    app.tool()(check_monitoring_prerequisites)