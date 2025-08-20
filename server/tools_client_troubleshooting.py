"""
Client Connectivity Troubleshooting Tools for Cisco Meraki MCP Server
Specialized tools for diagnosing and resolving client connection issues
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


def get_client_details(
    network_id: str,
    client_id_or_mac: str,
    timespan: Optional[int] = 86400
) -> str:
    """
    👤 Get detailed client information and connection history.
    
    Comprehensive client details including device info, connection status, and usage.
    
    Args:
        network_id: Network ID
        client_id_or_mac: Client ID or MAC address
        timespan: Time period in seconds (default: 86400 = 24 hours)
    
    Returns:
        Formatted client details with connection history
    """
    try:
        with safe_api_call("get client details"):
            # Get client details
            client = meraki.dashboard.networks.getNetworkClient(
                networkId=network_id,
                clientId=client_id_or_mac
            )
            
            # Format the response
            result = f"""👤 Client Details
==================================================

Device Information:
   Description: {client.get('description', 'Unknown Device')}
   MAC Address: {client.get('mac', 'N/A')}
   IP Address: {client.get('ip', 'No IP assigned')}
   Manufacturer: {client.get('manufacturer', 'Unknown')}
   OS: {client.get('os', 'Unknown OS')}

Connection Status:
   Status: {'🟢 Connected' if client.get('status') == 'Online' else '🔴 Offline'}
   SSID: {client.get('ssid', 'Not connected to WiFi')}
   Access Point: {client.get('apMac', 'N/A')}
   Switch Port: {client.get('switchport', 'N/A')}
   VLAN: {client.get('vlan', 'N/A')}

Network Usage:
   Data Sent: {client.get('sent', 0) / 1024 / 1024:.2f} MB
   Data Received: {client.get('recv', 0) / 1024 / 1024:.2f} MB
   
Recent Activity:
   First Seen: {client.get('firstSeen', 'Never')}
   Last Seen: {client.get('lastSeen', 'Never')}"""
            
            # Add security info if available
            if '802.1x' in client:
                result += f"\n\nSecurity:\n   802.1X Status: {client.get('802.1x', 'N/A')}"
            
            return result
            
    except Exception as e:
        return format_error("get client details", e)


def diagnose_client_connection(
    network_id: str,
    client_mac: str,
    timespan: Optional[int] = 3600
) -> str:
    """
    🔧 Diagnose client connection issues with detailed analysis.
    
    Analyzes authentication, DHCP, and connectivity problems for a specific client.
    
    Args:
        network_id: Network ID
        client_mac: Client MAC address
        timespan: Time period in seconds (default: 3600 = 1 hour)
    
    Returns:
        Detailed diagnosis with recommendations
    """
    try:
        with safe_api_call("diagnose client connection"):
            diagnosis = f"""🔧 Client Connection Diagnosis
==================================================

Client MAC: {client_mac}
Analysis Period: Last {timespan // 3600} hour(s)
"""
            
            # Get client info
            try:
                client = meraki.dashboard.networks.getNetworkClient(
                    networkId=network_id,
                    clientId=client_mac
                )
                
                diagnosis += f"\n📱 Device Info:\n   {client.get('description', 'Unknown')} ({client.get('os', 'Unknown OS')})"
                diagnosis += f"\n   Current Status: {'🟢 Online' if client.get('status') == 'Online' else '🔴 Offline'}"
                
                # Connection details
                if client.get('ssid'):
                    diagnosis += f"\n\n📡 Wireless Connection:\n   SSID: {client['ssid']}"
                    diagnosis += f"\n   AP: {client.get('apMac', 'N/A')}"
                    diagnosis += f"\n   Signal: {client.get('rssi', 'N/A')} dBm"
                
            except:
                diagnosis += "\n⚠️ Client not currently connected"
            
            # Get events for this client
            try:
                events = meraki.dashboard.networks.getNetworkEvents(
                    networkId=network_id,
                    clientMac=client_mac,
                    perPage=100
                )
                
                # Analyze events
                auth_failures = 0
                dhcp_failures = 0
                disassociations = 0
                
                diagnosis += "\n\n📊 Recent Events:"
                for event in events.get('events', [])[:10]:
                    event_type = event.get('type', '')
                    if 'auth' in event_type.lower() and 'fail' in event_type.lower():
                        auth_failures += 1
                    elif 'dhcp' in event_type.lower() and ('fail' in event_type.lower() or 'no lease' in event_type.lower()):
                        dhcp_failures += 1
                    elif 'disassociat' in event_type.lower():
                        disassociations += 1
                
                # Summary
                diagnosis += f"\n   Authentication Failures: {auth_failures}"
                diagnosis += f"\n   DHCP Failures: {dhcp_failures}"
                diagnosis += f"\n   Disassociations: {disassociations}"
                
                # Diagnosis
                diagnosis += "\n\n🔍 Diagnosis:"
                if auth_failures > 0:
                    diagnosis += "\n   ❌ Authentication Issues Detected"
                    diagnosis += "\n      - Check WiFi password/credentials"
                    diagnosis += "\n      - Verify RADIUS server (if 802.1X)"
                    diagnosis += "\n      - Check certificate validity"
                    
                if dhcp_failures > 0:
                    diagnosis += "\n   ❌ DHCP Issues Detected"
                    diagnosis += "\n      - Check DHCP pool availability"
                    diagnosis += "\n      - Verify VLAN configuration"
                    diagnosis += "\n      - Check for IP conflicts"
                    
                if disassociations > 2:
                    diagnosis += "\n   ⚠️ Frequent Disconnections"
                    diagnosis += "\n      - Check signal strength"
                    diagnosis += "\n      - Look for interference"
                    diagnosis += "\n      - Verify roaming settings"
                
                if auth_failures == 0 and dhcp_failures == 0 and disassociations < 2:
                    diagnosis += "\n   ✅ No major connection issues found"
                    
            except:
                diagnosis += "\n\n⚠️ Unable to retrieve event history"
            
            # Recommendations
            diagnosis += "\n\n💡 Recommendations:"
            diagnosis += "\n   1. Check client WiFi settings"
            diagnosis += "\n   2. Verify network access policies"
            diagnosis += "\n   3. Test with a different device"
            diagnosis += "\n   4. Check for MAC filtering or ACLs"
            
            return diagnosis
            
    except Exception as e:
        return format_error("diagnose client connection", e)


def get_client_connection_history(
    network_id: str,
    client_mac: str,
    timespan: Optional[int] = 86400
) -> str:
    """
    📈 Get client connection history and patterns.
    
    Shows connection timeline, roaming history, and usage patterns.
    
    Args:
        network_id: Network ID
        client_mac: Client MAC address
        timespan: Time period in seconds (default: 86400 = 24 hours)
    
    Returns:
        Connection history with patterns analysis
    """
    try:
        with safe_api_call("get client connection history"):
            # Get connection events
            events = meraki.dashboard.networks.getNetworkEvents(
                networkId=network_id,
                clientMac=client_mac,
                includedEventTypes=["association", "disassociation", "client_connect", "client_disconnect"],
                perPage=1000
            )
            
            result = f"""📈 Client Connection History
==================================================

Client MAC: {client_mac}
Time Period: Last {timespan // 3600} hour(s)

📊 Connection Timeline:
"""
            
            # Process events chronologically
            connection_events = []
            for event in events.get('events', []):
                event_time = event.get('occurredAt', 'Unknown time')
                event_type = event.get('type', 'Unknown')
                description = event.get('description', '')
                
                if 'association' in event_type or 'connect' in event_type:
                    emoji = '🟢'
                else:
                    emoji = '🔴'
                    
                connection_events.append(f"{emoji} {event_time[:19]} - {description}")
            
            # Show recent events
            if connection_events:
                for event in connection_events[:20]:  # Show last 20 events
                    result += f"\n{event}"
            else:
                result += "\n📊 No connection events found in this period"
            
            # Get usage statistics
            try:
                client = meraki.dashboard.networks.getNetworkClient(
                    networkId=network_id,
                    clientId=client_mac
                )
                
                result += f"\n\n📊 Usage Statistics:"
                result += f"\n   Total Sent: {client.get('sent', 0) / 1024 / 1024:.2f} MB"
                result += f"\n   Total Received: {client.get('recv', 0) / 1024 / 1024:.2f} MB"
                result += f"\n   Usage Trend: {'Heavy' if (client.get('sent', 0) + client.get('recv', 0)) > 1073741824 else 'Normal'}"
                
            except:
                pass
            
            # Connection patterns
            result += "\n\n🔍 Connection Patterns:"
            if len(connection_events) > 5:
                result += "\n   ⚠️ Frequent connection changes detected"
                result += "\n   - May indicate roaming or stability issues"
            else:
                result += "\n   ✅ Stable connection pattern"
            
            return result
            
    except Exception as e:
        return format_error("get client connection history", e)


def analyze_client_performance(
    network_id: str,
    client_mac: str,
    timespan: Optional[int] = 3600
) -> str:
    """
    📊 Analyze client performance metrics and issues.
    
    Examines latency, packet loss, signal strength, and data rates.
    
    Args:
        network_id: Network ID
        client_mac: Client MAC address
        timespan: Time period in seconds (default: 3600 = 1 hour)
    
    Returns:
        Performance analysis with optimization suggestions
    """
    try:
        with safe_api_call("analyze client performance"):
            # Get client details
            client = meraki.dashboard.networks.getNetworkClient(
                networkId=network_id,
                clientId=client_mac
            )
            
            result = f"""📊 Client Performance Analysis
==================================================

Client: {client.get('description', client_mac)}
Device Type: {client.get('os', 'Unknown')} - {client.get('manufacturer', 'Unknown')}

📡 Wireless Performance:
"""
            
            # Signal strength analysis
            rssi = client.get('rssi')
            if rssi:
                result += f"\n   Signal Strength: {rssi} dBm"
                if rssi > -67:
                    result += " (🟢 Excellent)"
                elif rssi > -75:
                    result += " (🟡 Good)"
                elif rssi > -80:
                    result += " (🟠 Fair)"
                else:
                    result += " (🔴 Poor)"
            
            # SNR analysis
            snr = client.get('snr')
            if snr:
                result += f"\n   Signal-to-Noise Ratio: {snr} dB"
                if snr > 25:
                    result += " (🟢 Excellent)"
                elif snr > 15:
                    result += " (🟡 Good)"
                else:
                    result += " (🔴 Poor)"
            
            # Data rates
            result += f"\n   Associated SSID: {client.get('ssid', 'N/A')}"
            result += f"\n   Access Point: {client.get('apMac', 'N/A')}"
            
            # Usage analysis
            sent_mb = client.get('sent', 0) / 1024 / 1024
            recv_mb = client.get('recv', 0) / 1024 / 1024
            
            result += f"\n\n📈 Data Usage:"
            result += f"\n   Uploaded: {sent_mb:.2f} MB"
            result += f"\n   Downloaded: {recv_mb:.2f} MB"
            result += f"\n   Total: {(sent_mb + recv_mb):.2f} MB"
            
            # Performance issues
            result += "\n\n🔍 Performance Assessment:"
            
            issues_found = False
            
            if rssi and rssi < -75:
                result += "\n   ⚠️ Weak signal strength detected"
                result += "\n      - Move closer to access point"
                result += "\n      - Check for obstacles/interference"
                issues_found = True
                
            if snr and snr < 15:
                result += "\n   ⚠️ Poor signal quality (high noise)"
                result += "\n      - Check for interference sources"
                result += "\n      - Consider changing WiFi channel"
                issues_found = True
            
            if client.get('vlan') and client.get('vlan') > 1:
                result += f"\n   ℹ️ Client on VLAN {client['vlan']}"
                result += "\n      - Verify VLAN performance settings"
            
            if not issues_found:
                result += "\n   ✅ No major performance issues detected"
            
            # Optimization suggestions
            result += "\n\n💡 Optimization Suggestions:"
            result += "\n   1. Enable band steering to 5GHz"
            result += "\n   2. Check QoS/traffic shaping rules"
            result += "\n   3. Verify client power save settings"
            result += "\n   4. Update client device drivers"
            
            return result
            
    except Exception as e:
        return format_error("analyze client performance", e)


def compare_client_behavior(
    network_id: str,
    client_mac: str,
    timespan: Optional[int] = 604800
) -> str:
    """
    🔄 Compare client behavior against network baseline.
    
    Identifies if client issues are unique or network-wide.
    
    Args:
        network_id: Network ID
        client_mac: Client MAC address
        timespan: Time period in seconds (default: 604800 = 7 days)
    
    Returns:
        Comparative analysis with insights
    """
    try:
        with safe_api_call("compare client behavior"):
            # Get target client info
            client = meraki.dashboard.networks.getNetworkClient(
                networkId=network_id,
                clientId=client_mac
            )
            
            # Get all clients for comparison
            all_clients = meraki.dashboard.networks.getNetworkClients(
                networkId=network_id,
                timespan=timespan,
                perPage=100
            )
            
            result = f"""🔄 Client Behavior Comparison
==================================================

Target Client: {client.get('description', client_mac)}
Comparing against: {len(all_clients)} network clients

📊 Comparative Analysis:
"""
            
            # Calculate averages
            total_usage = 0
            total_clients = len(all_clients)
            same_ssid_count = 0
            same_os_count = 0
            
            for c in all_clients:
                total_usage += c.get('sent', 0) + c.get('recv', 0)
                if c.get('ssid') == client.get('ssid'):
                    same_ssid_count += 1
                if c.get('os') == client.get('os'):
                    same_os_count += 1
            
            avg_usage = total_usage / total_clients if total_clients > 0 else 0
            client_usage = client.get('sent', 0) + client.get('recv', 0)
            
            # Usage comparison
            result += f"\n\nData Usage Comparison:"
            result += f"\n   Client Usage: {client_usage / 1024 / 1024:.2f} MB"
            result += f"\n   Network Average: {avg_usage / 1024 / 1024:.2f} MB"
            
            if client_usage > avg_usage * 2:
                result += "\n   📈 Status: Heavy user (>2x average)"
            elif client_usage < avg_usage * 0.5:
                result += "\n   📉 Status: Light user (<0.5x average)"
            else:
                result += "\n   ✅ Status: Normal usage"
            
            # Connection comparison
            result += f"\n\nConnection Profile:"
            result += f"\n   SSID: {client.get('ssid', 'N/A')}"
            result += f"\n   Others on same SSID: {same_ssid_count - 1}"
            result += f"\n   Same OS type: {same_os_count - 1}"
            
            # Signal comparison (if wireless)
            if client.get('rssi'):
                rssi_values = [c.get('rssi', 0) for c in all_clients if c.get('rssi')]
                avg_rssi = sum(rssi_values) / len(rssi_values) if rssi_values else 0
                
                result += f"\n\nSignal Strength Comparison:"
                result += f"\n   Client RSSI: {client['rssi']} dBm"
                result += f"\n   Network Average: {avg_rssi:.1f} dBm"
                
                if client['rssi'] < avg_rssi - 10:
                    result += "\n   ⚠️ Below average signal strength"
                else:
                    result += "\n   ✅ Normal signal strength"
            
            # Insights
            result += "\n\n🔍 Insights:"
            
            if client_usage > avg_usage * 3:
                result += "\n   • Client is a very heavy bandwidth user"
                result += "\n   • Consider QoS rules if affecting others"
            
            if same_ssid_count < 5:
                result += f"\n   • Few clients on '{client.get('ssid')}' SSID"
                result += "\n   • Issues may be SSID-specific"
            
            if same_os_count < 3:
                result += f"\n   • Few {client.get('os')} devices on network"
                result += "\n   • Check for OS-specific issues"
            
            result += "\n\n💡 Recommendations:"
            result += "\n   1. Compare with similar device types"
            result += "\n   2. Check if issues are location-specific"
            result += "\n   3. Review client-specific policies"
            result += "\n   4. Test with different user account"
            
            return result
            
    except Exception as e:
        return format_error("compare client behavior", e)


def client_troubleshooting_help() -> str:
    """
    ❓ Get help with client troubleshooting tools.
    
    Shows available tools and common troubleshooting workflows.
    
    Returns:
        Formatted help guide for client troubleshooting
    """
    return """🔧 Client Troubleshooting Tools Help
==================================================

Available tools for diagnosing client issues:

1. get_client_details()
   - View comprehensive client information
   - Check current connection status
   - See device details and usage

2. diagnose_client_connection()
   - Analyze authentication failures
   - Check DHCP issues
   - Find connection problems

3. get_client_connection_history()
   - View connection timeline
   - Track roaming patterns
   - Identify disconnect events

4. analyze_client_performance()
   - Check signal strength and quality
   - Analyze data usage patterns
   - Get optimization suggestions

5. compare_client_behavior()
   - Compare against network baseline
   - Identify unique vs common issues
   - Get comparative insights

Common Workflows:

🔍 "Client Can't Connect"
1. get_client_details() - Check current status
2. diagnose_client_connection() - Find root cause
3. get_client_connection_history() - Review patterns

📊 "Client Has Poor Performance"
1. analyze_client_performance() - Check metrics
2. compare_client_behavior() - Is it just this client?
3. get_client_connection_history() - Look for patterns

💡 Pro Tips:
- Always start with get_client_details()
- Use MAC address format: AA:BB:CC:DD:EE:FF
- Check multiple time periods for patterns
- Compare against similar clients

Need specific help? Try:
- "Why can't this client connect?"
- "Is this client's performance normal?"
- "Show me this client's connection history"
"""


def register_client_troubleshooting_tools(app: FastMCP, meraki_client: MerakiClient):
    """Register all client troubleshooting tools with the MCP server."""
    global mcp_app, meraki
    mcp_app = app
    meraki = meraki_client
    
    # Register all tools
    tools = [
        (get_client_details, "Get detailed client information and status"),
        (diagnose_client_connection, "Diagnose client connection issues"),
        (get_client_connection_history, "View client connection history"),
        (analyze_client_performance, "Analyze client performance metrics"),
        (compare_client_behavior, "Compare client against network baseline"),
        (client_troubleshooting_help, "Get help with client troubleshooting"),
    ]
    
    for tool_func, description in tools:
        app.tool(
            name=tool_func.__name__,
            description=description
        )(tool_func)