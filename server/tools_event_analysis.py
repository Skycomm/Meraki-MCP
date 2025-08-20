"""
Event Log Analysis Tools for Cisco Meraki MCP Server
Analyze event patterns, identify root causes, and correlate related events
"""

from mcp.server import FastMCP
from typing import Optional, Dict, Any, List, Tuple
import json
from datetime import datetime, timedelta
from collections import defaultdict, Counter
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


def search_event_logs(
    network_id: str,
    search_term: Optional[str] = None,
    event_types: Optional[List[str]] = None,
    timespan: Optional[int] = 86400,
    device_serial: Optional[str] = None,
    client_mac: Optional[str] = None
) -> str:
    """
    🔍 Search event logs for specific patterns or errors.
    
    Search and filter network events by various criteria.
    
    Args:
        network_id: Network ID to search
        search_term: Text to search for in event descriptions
        event_types: List of event types to filter (e.g., ['auth_fail', 'dhcp_no_lease'])
        timespan: Time period in seconds (default: 86400 = 24 hours)
        device_serial: Filter by specific device
        client_mac: Filter by specific client
        
    Returns:
        Filtered event log results
    """
    try:
        output = ["🔍 Event Log Search Results", "=" * 50, ""]
        
        # Build parameters
        params = {
            'perPage': 1000,
            'timespan': timespan
        }
        
        if event_types:
            params['includedEventTypes'] = event_types
        if device_serial:
            params['deviceSerial'] = device_serial
        if client_mac:
            params['clientMac'] = client_mac
        
        # Get events
        with safe_api_call("search events"):
            events_response = meraki.dashboard.networks.getNetworkEvents(
                network_id,
                **params
            )
            
            events = events_response.get('events', []) if isinstance(events_response, dict) else []
            
            # Filter by search term if provided
            if search_term and events:
                search_lower = search_term.lower()
                filtered_events = []
                for event in events:
                    if (search_lower in event.get('description', '').lower() or
                        search_lower in event.get('type', '').lower() or
                        search_lower in event.get('category', '').lower()):
                        filtered_events.append(event)
                events = filtered_events
            
            # Display results
            output.append(f"Found {len(events)} matching events")
            
            if search_term:
                output.append(f"Search term: '{search_term}'")
            if event_types:
                output.append(f"Event types: {', '.join(event_types)}")
            if device_serial:
                output.append(f"Device: {device_serial}")
            if client_mac:
                output.append(f"Client: {client_mac}")
            
            output.append(f"Time range: Last {timespan//3600} hours")
            output.append("")
            
            if events:
                # Group events by type
                events_by_type = defaultdict(list)
                for event in events:
                    event_type = event.get('type', 'unknown')
                    events_by_type[event_type].append(event)
                
                # Display grouped events
                for event_type, type_events in sorted(events_by_type.items()):
                    output.append(f"\n📌 {event_type} ({len(type_events)} events)")
                    output.append("-" * 40)
                    
                    # Show first 5 events of each type
                    for event in type_events[:5]:
                        timestamp = event.get('occurredAt', 'Unknown time')
                        description = event.get('description', 'No description')
                        category = event.get('category', 'Unknown')
                        device_name = event.get('deviceName', '')
                        client_name = event.get('clientName', event.get('clientMac', ''))
                        
                        output.append(f"⏰ {timestamp}")
                        output.append(f"   Category: {category}")
                        if device_name:
                            output.append(f"   Device: {device_name}")
                        if client_name:
                            output.append(f"   Client: {client_name}")
                        output.append(f"   {description}")
                        output.append("")
                    
                    if len(type_events) > 5:
                        output.append(f"   ... and {len(type_events) - 5} more {event_type} events")
                        output.append("")
                
                # Summary statistics
                output.append("\n📊 Event Summary:")
                output.append("-" * 40)
                for event_type, count in Counter(e.get('type', 'unknown') for e in events).most_common(10):
                    output.append(f"   {event_type}: {count}")
            else:
                output.append("No events found matching your criteria")
                
                # Suggest broader search
                output.extend([
                    "",
                    "💡 Try:",
                    "• Expanding the timespan",
                    "• Using broader search terms",
                    "• Removing specific filters",
                    "• Checking different event types"
                ])
        
        return "\n".join(output)
        
    except Exception as e:
        return format_error("search event logs", e)


def analyze_error_patterns(
    network_id: str,
    timespan: Optional[int] = 86400,
    min_occurrences: Optional[int] = 5
) -> str:
    """
    📊 Analyze error event patterns to identify recurring issues.
    
    Identifies patterns in error events and their frequency.
    
    Args:
        network_id: Network ID to analyze
        timespan: Time period in seconds (default: 86400 = 24 hours)
        min_occurrences: Minimum occurrences to report (default: 5)
        
    Returns:
        Error pattern analysis report
    """
    try:
        output = ["📊 Error Pattern Analysis", "=" * 50, ""]
        
        # Define error event types to analyze
        error_event_types = [
            'auth_fail',
            'association_reject',
            'dhcp_no_lease',
            'dns_lookup_fail',
            'arp_poisoning',
            'port_cycle',
            'device_down',
            'vpn_connectivity_issue',
            'client_connectivity_issue',
            'wired_8021x_auth_fail',
            'wireless_auth_fail'
        ]
        
        # Get error events
        with safe_api_call("get error events"):
            events_response = meraki.dashboard.networks.getNetworkEvents(
                network_id,
                perPage=1000,
                timespan=timespan,
                includedEventTypes=error_event_types
            )
            
            events = events_response.get('events', []) if isinstance(events_response, dict) else []
            
            if not events:
                output.append("✅ No error events found in the specified time period")
                output.append(f"   Analyzed: Last {timespan//3600} hours")
                return "\n".join(output)
            
            output.append(f"Analyzing {len(events)} error events from the last {timespan//3600} hours")
            output.append("")
            
            # Analyze patterns
            patterns = {
                'by_type': defaultdict(int),
                'by_device': defaultdict(lambda: defaultdict(int)),
                'by_client': defaultdict(lambda: defaultdict(int)),
                'by_hour': defaultdict(int),
                'by_error_detail': defaultdict(int),
                'temporal_patterns': defaultdict(list)
            }
            
            # Process events
            for event in events:
                event_type = event.get('type', 'unknown')
                device_name = event.get('deviceName', event.get('deviceSerial', 'Unknown'))
                client_id = event.get('clientName', event.get('clientMac', 'Unknown'))
                description = event.get('description', '')
                
                # Count by type
                patterns['by_type'][event_type] += 1
                
                # Count by device
                if device_name != 'Unknown':
                    patterns['by_device'][device_name][event_type] += 1
                
                # Count by client
                if client_id != 'Unknown':
                    patterns['by_client'][client_id][event_type] += 1
                
                # Extract hour for temporal analysis
                try:
                    timestamp = event.get('occurredAt', '')
                    if timestamp:
                        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                        hour = dt.hour
                        patterns['by_hour'][hour] += 1
                        patterns['temporal_patterns'][event_type].append(dt)
                except:
                    pass
                
                # Extract error details from description
                if 'fail' in description.lower():
                    # Extract reason if present
                    if 'reason:' in description.lower():
                        reason = description.lower().split('reason:')[1].split('.')[0].strip()
                        patterns['by_error_detail'][f"{event_type}: {reason}"] += 1
                    else:
                        patterns['by_error_detail'][event_type] += 1
            
            # Display analysis results
            
            # 1. Most common error types
            output.append("🔴 Most Common Error Types:")
            output.append("-" * 40)
            for error_type, count in sorted(patterns['by_type'].items(), key=lambda x: x[1], reverse=True)[:10]:
                if count >= min_occurrences:
                    percentage = (count / len(events)) * 100
                    output.append(f"   {error_type}: {count} ({percentage:.1f}%)")
            output.append("")
            
            # 2. Devices with most errors
            device_errors = []
            for device, errors in patterns['by_device'].items():
                total_errors = sum(errors.values())
                if total_errors >= min_occurrences:
                    device_errors.append((device, total_errors, errors))
            
            if device_errors:
                output.append("🖥️ Devices with Recurring Errors:")
                output.append("-" * 40)
                for device, total, errors in sorted(device_errors, key=lambda x: x[1], reverse=True)[:5]:
                    output.append(f"   {device}: {total} errors")
                    # Show top error types for this device
                    for error_type, count in sorted(errors.items(), key=lambda x: x[1], reverse=True)[:3]:
                        output.append(f"      - {error_type}: {count}")
                output.append("")
            
            # 3. Clients with most errors
            client_errors = []
            for client, errors in patterns['by_client'].items():
                total_errors = sum(errors.values())
                if total_errors >= min_occurrences:
                    client_errors.append((client, total_errors, errors))
            
            if client_errors:
                output.append("👤 Clients with Recurring Errors:")
                output.append("-" * 40)
                for client, total, errors in sorted(client_errors, key=lambda x: x[1], reverse=True)[:5]:
                    output.append(f"   {client}: {total} errors")
                    # Show top error types for this client
                    for error_type, count in sorted(errors.items(), key=lambda x: x[1], reverse=True)[:2]:
                        output.append(f"      - {error_type}: {count}")
                output.append("")
            
            # 4. Temporal patterns
            if patterns['by_hour']:
                output.append("🕐 Temporal Patterns (Errors by Hour):")
                output.append("-" * 40)
                peak_hours = sorted(patterns['by_hour'].items(), key=lambda x: x[1], reverse=True)[:5]
                for hour, count in peak_hours:
                    output.append(f"   {hour:02d}:00 - {count} errors")
                output.append("")
            
            # 5. Error clustering detection
            output.append("🔍 Error Clustering Analysis:")
            output.append("-" * 40)
            
            for event_type, timestamps in patterns['temporal_patterns'].items():
                if len(timestamps) >= min_occurrences:
                    # Check for clusters (multiple errors within 5 minutes)
                    timestamps.sort()
                    clusters = []
                    current_cluster = [timestamps[0]]
                    
                    for i in range(1, len(timestamps)):
                        if (timestamps[i] - timestamps[i-1]).seconds < 300:  # 5 minutes
                            current_cluster.append(timestamps[i])
                        else:
                            if len(current_cluster) >= 3:
                                clusters.append(current_cluster)
                            current_cluster = [timestamps[i]]
                    
                    if len(current_cluster) >= 3:
                        clusters.append(current_cluster)
                    
                    if clusters:
                        output.append(f"   {event_type}:")
                        output.append(f"      Found {len(clusters)} error clusters")
                        for cluster in clusters[:3]:
                            output.append(f"      - {len(cluster)} errors between {cluster[0].strftime('%H:%M')} - {cluster[-1].strftime('%H:%M')}")
            
            # 6. Root cause indicators
            output.append("\n🎯 Potential Root Causes:")
            output.append("-" * 40)
            
            # Authentication failures
            auth_errors = patterns['by_type'].get('auth_fail', 0) + patterns['by_type'].get('wireless_auth_fail', 0)
            if auth_errors > min_occurrences:
                output.append(f"   🔐 Authentication Issues ({auth_errors} failures):")
                output.append("      • Check RADIUS server connectivity")
                output.append("      • Verify credentials and certificates")
                output.append("      • Review authentication policies")
            
            # DHCP failures
            dhcp_errors = patterns['by_type'].get('dhcp_no_lease', 0)
            if dhcp_errors > min_occurrences:
                output.append(f"   📡 DHCP Issues ({dhcp_errors} failures):")
                output.append("      • Check DHCP pool exhaustion")
                output.append("      • Verify VLAN configuration")
                output.append("      • Review DHCP server settings")
            
            # Network connectivity
            conn_errors = patterns['by_type'].get('device_down', 0) + patterns['by_type'].get('port_cycle', 0)
            if conn_errors > min_occurrences:
                output.append(f"   🌐 Connectivity Issues ({conn_errors} events):")
                output.append("      • Check physical connections")
                output.append("      • Review spanning tree")
                output.append("      • Verify power and cabling")
            
            # Recommendations
            output.extend([
                "",
                "💡 Recommendations:",
                "1. Focus on devices/clients with highest error rates",
                "2. Investigate temporal patterns for scheduled issues",
                "3. Check error clusters for systemic problems",
                "4. Review configuration for top error types",
                "5. Set up alerts for recurring patterns"
            ])
        
        return "\n".join(output)
        
    except Exception as e:
        return format_error("analyze error patterns", e)


def identify_root_causes(
    network_id: str,
    issue_description: str,
    timespan: Optional[int] = 7200
) -> str:
    """
    🔬 Identify potential root causes for specific issues.
    
    Analyzes events around a specific issue to determine root cause.
    
    Args:
        network_id: Network ID to analyze
        issue_description: Description of the issue (e.g., "users can't connect", "slow network")
        timespan: Time period to analyze in seconds (default: 7200 = 2 hours)
        
    Returns:
        Root cause analysis report
    """
    try:
        output = ["🔬 Root Cause Analysis", "=" * 50, ""]
        output.append(f"Issue: {issue_description}")
        output.append(f"Analyzing last {timespan//3600} hours of events")
        output.append("")
        
        # Map issue descriptions to relevant event types
        issue_event_mapping = {
            "connect": ["auth_fail", "association_reject", "dhcp_no_lease", "client_connectivity_issue"],
            "auth": ["auth_fail", "wireless_auth_fail", "wired_8021x_auth_fail", "radius_auth_fail"],
            "slow": ["port_cycle", "high_collision_rate", "high_channel_utilization", "vpn_connectivity_issue"],
            "dhcp": ["dhcp_no_lease", "dhcp_release", "dhcp_conflict", "dhcp_server_unreachable"],
            "internet": ["dns_lookup_fail", "gateway_down", "uplink_down", "wan_link_down"],
            "vpn": ["vpn_connectivity_issue", "vpn_tunnel_down", "vpn_peer_unreachable"],
            "wireless": ["association_reject", "deauth", "disassociation", "high_channel_utilization"]
        }
        
        # Determine relevant event types based on issue description
        issue_lower = issue_description.lower()
        relevant_events = []
        
        for keyword, event_types in issue_event_mapping.items():
            if keyword in issue_lower:
                relevant_events.extend(event_types)
        
        # If no specific match, use common problem events
        if not relevant_events:
            relevant_events = [
                "auth_fail", "association_reject", "dhcp_no_lease",
                "device_down", "port_cycle", "client_connectivity_issue"
            ]
        
        # Remove duplicates
        relevant_events = list(set(relevant_events))
        
        # Get events
        with safe_api_call("get events for analysis"):
            events_response = meraki.dashboard.networks.getNetworkEvents(
                network_id,
                perPage=1000,
                timespan=timespan,
                includedEventTypes=relevant_events
            )
            
            events = events_response.get('events', []) if isinstance(events_response, dict) else []
            
            if not events:
                output.append("ℹ️ No relevant events found in the specified time period")
                output.append("")
                output.append("This could mean:")
                output.append("• The issue occurred outside the analysis window")
                output.append("• The issue is not generating logged events")
                output.append("• Different event types need to be analyzed")
                return "\n".join(output)
            
            output.append(f"Found {len(events)} relevant events")
            output.append("")
            
            # Analyze event timeline
            output.append("📅 Event Timeline Analysis:")
            output.append("-" * 40)
            
            # Group events by time windows (5-minute buckets)
            time_buckets = defaultdict(list)
            event_sequence = []
            
            for event in sorted(events, key=lambda x: x.get('occurredAt', '')):
                try:
                    timestamp = event.get('occurredAt', '')
                    if timestamp:
                        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                        bucket = dt.replace(minute=(dt.minute // 5) * 5, second=0, microsecond=0)
                        time_buckets[bucket].append(event)
                        event_sequence.append((dt, event))
                except:
                    pass
            
            # Find the time bucket with most events (likely when issue occurred)
            if time_buckets:
                peak_bucket = max(time_buckets.items(), key=lambda x: len(x[1]))
                peak_time, peak_events = peak_bucket
                
                output.append(f"🔴 Peak activity at {peak_time.strftime('%H:%M')} ({len(peak_events)} events)")
                output.append("")
                
                # Analyze events around peak time
                output.append("Events during peak period:")
                event_types_at_peak = defaultdict(int)
                devices_affected = set()
                clients_affected = set()
                
                for event in peak_events:
                    event_type = event.get('type', 'unknown')
                    event_types_at_peak[event_type] += 1
                    
                    if event.get('deviceName'):
                        devices_affected.add(event['deviceName'])
                    if event.get('clientMac'):
                        clients_affected.add(event.get('clientName', event['clientMac']))
                
                for event_type, count in sorted(event_types_at_peak.items(), key=lambda x: x[1], reverse=True):
                    output.append(f"   • {event_type}: {count}")
                
                output.append(f"\nDevices affected: {len(devices_affected)}")
                output.append(f"Clients affected: {len(clients_affected)}")
            
            # Identify event chains (cascade analysis)
            output.append("\n🔗 Event Chain Analysis:")
            output.append("-" * 40)
            
            # Look for common failure patterns
            failure_chains = {
                "Authentication Cascade": ["radius_auth_fail", "auth_fail", "association_reject"],
                "DHCP Failure Chain": ["dhcp_server_unreachable", "dhcp_no_lease", "client_connectivity_issue"],
                "Network Outage": ["device_down", "gateway_down", "client_connectivity_issue"],
                "Wireless Issues": ["high_channel_utilization", "association_reject", "deauth"]
            }
            
            detected_chains = []
            event_type_list = [e.get('type', '') for e in events]
            
            for chain_name, chain_events in failure_chains.items():
                # Check if events in chain occurred
                chain_found = all(event in event_type_list for event in chain_events)
                if chain_found:
                    detected_chains.append(chain_name)
            
            if detected_chains:
                output.append("Detected failure patterns:")
                for chain in detected_chains:
                    output.append(f"   ⚠️ {chain}")
            else:
                output.append("No specific failure chains detected")
            
            # Root cause determination
            output.append("\n🎯 Probable Root Causes:")
            output.append("-" * 40)
            
            root_causes = []
            
            # Analyze based on event patterns
            total_events = len(events)
            event_type_counts = Counter(e.get('type', 'unknown') for e in events)
            
            # Authentication root causes
            auth_percentage = (event_type_counts.get('auth_fail', 0) + 
                             event_type_counts.get('wireless_auth_fail', 0)) / total_events * 100
            
            if auth_percentage > 30:
                root_causes.append({
                    'cause': 'Authentication System Failure',
                    'confidence': min(90, int(auth_percentage * 1.5)),
                    'evidence': f'{int(auth_percentage)}% of events are auth failures',
                    'fix': 'Check RADIUS server, verify credentials, review certificates'
                })
            
            # DHCP root causes
            dhcp_percentage = event_type_counts.get('dhcp_no_lease', 0) / total_events * 100
            
            if dhcp_percentage > 20:
                root_causes.append({
                    'cause': 'DHCP Service Issue',
                    'confidence': min(85, int(dhcp_percentage * 2)),
                    'evidence': f'{int(dhcp_percentage)}% of events are DHCP failures',
                    'fix': 'Check DHCP pool, verify server status, review VLAN config'
                })
            
            # Infrastructure root causes
            infra_events = (event_type_counts.get('device_down', 0) + 
                           event_type_counts.get('port_cycle', 0))
            infra_percentage = infra_events / total_events * 100
            
            if infra_percentage > 15:
                root_causes.append({
                    'cause': 'Infrastructure/Hardware Issue',
                    'confidence': min(80, int(infra_percentage * 2.5)),
                    'evidence': f'{int(infra_percentage)}% of events indicate hardware problems',
                    'fix': 'Check device status, verify cabling, review power supply'
                })
            
            # Client-side root causes
            if len(clients_affected) < 5 and len(clients_affected) > 0:
                root_causes.append({
                    'cause': 'Client-Specific Issue',
                    'confidence': 70,
                    'evidence': f'Only {len(clients_affected)} clients affected',
                    'fix': 'Check client configuration, update drivers, verify credentials'
                })
            
            # Display root causes
            if root_causes:
                # Sort by confidence
                root_causes.sort(key=lambda x: x['confidence'], reverse=True)
                
                for i, cause in enumerate(root_causes, 1):
                    output.append(f"\n{i}. {cause['cause']} (Confidence: {cause['confidence']}%)")
                    output.append(f"   Evidence: {cause['evidence']}")
                    output.append(f"   Recommended Fix: {cause['fix']}")
            else:
                output.append("\n❓ Unable to determine specific root cause")
                output.append("   Consider:")
                output.append("   • Expanding the analysis timeframe")
                output.append("   • Checking additional event types")
                output.append("   • Reviewing configuration changes")
            
            # Next steps
            output.extend([
                "",
                "📋 Next Steps:",
                "1. Address highest confidence root cause first",
                "2. Check devices/clients with most errors",
                "3. Review events immediately before issue",
                "4. Verify recent configuration changes",
                "5. Run diagnostics on affected components"
            ])
        
        return "\n".join(output)
        
    except Exception as e:
        return format_error("identify root causes", e)


def correlate_events(
    network_id: str,
    reference_time: str,
    correlation_window: Optional[int] = 300,
    event_types: Optional[List[str]] = None
) -> str:
    """
    🔗 Correlate related events around a specific time.
    
    Finds events that occurred near a reference time to understand relationships.
    
    Args:
        network_id: Network ID to analyze
        reference_time: ISO format time to correlate around (e.g., "2024-01-20T15:30:00Z")
        correlation_window: Seconds before/after reference time (default: 300 = 5 minutes)
        event_types: Specific event types to include (optional)
        
    Returns:
        Correlated events analysis
    """
    try:
        output = ["🔗 Event Correlation Analysis", "=" * 50, ""]
        
        # Parse reference time
        try:
            ref_dt = datetime.fromisoformat(reference_time.replace('Z', '+00:00'))
        except:
            return "❌ Invalid reference time. Use ISO format: YYYY-MM-DDTHH:MM:SSZ"
        
        output.append(f"Reference time: {ref_dt.strftime('%Y-%m-%d %H:%M:%S')} UTC")
        output.append(f"Correlation window: ±{correlation_window} seconds")
        output.append("")
        
        # Calculate time range
        start_time = ref_dt - timedelta(seconds=correlation_window)
        end_time = ref_dt + timedelta(seconds=correlation_window)
        total_timespan = correlation_window * 2
        
        # Get events
        params = {
            'perPage': 1000,
            'startingAfter': start_time.isoformat() + 'Z',
            'endingBefore': end_time.isoformat() + 'Z'
        }
        
        if event_types:
            params['includedEventTypes'] = event_types
        
        with safe_api_call("get correlated events"):
            events_response = meraki.dashboard.networks.getNetworkEvents(
                network_id,
                **params
            )
            
            events = events_response.get('events', []) if isinstance(events_response, dict) else []
            
            if not events:
                output.append("No events found in the correlation window")
                return "\n".join(output)
            
            output.append(f"Found {len(events)} events in correlation window")
            output.append("")
            
            # Process and sort events by time
            processed_events = []
            for event in events:
                try:
                    event_time = datetime.fromisoformat(event['occurredAt'].replace('Z', '+00:00'))
                    time_diff = (event_time - ref_dt).total_seconds()
                    processed_events.append({
                        'event': event,
                        'time': event_time,
                        'diff_seconds': time_diff,
                        'before_reference': time_diff < 0
                    })
                except:
                    continue
            
            # Sort by time
            processed_events.sort(key=lambda x: x['time'])
            
            # Display timeline
            output.append("📅 Event Timeline:")
            output.append("-" * 40)
            
            for pe in processed_events:
                event = pe['event']
                diff = pe['diff_seconds']
                
                # Format time difference
                if abs(diff) < 60:
                    time_str = f"{int(diff):+d}s"
                else:
                    time_str = f"{int(diff/60):+d}m {int(abs(diff)%60)}s"
                
                # Mark reference point
                if abs(diff) < 1:
                    time_str = "REF →"
                
                event_type = event.get('type', 'unknown')
                description = event.get('description', 'No description')[:80]
                device = event.get('deviceName', '')
                client = event.get('clientName', event.get('clientMac', ''))
                
                output.append(f"{time_str:>8} | {event_type:<25} | {description}")
                
                if device:
                    output.append(f"{'':>8} | Device: {device}")
                if client:
                    output.append(f"{'':>8} | Client: {client}")
                output.append("")
            
            # Analyze correlations
            output.append("🔍 Correlation Analysis:")
            output.append("-" * 40)
            
            # Events immediately before reference
            before_events = [pe for pe in processed_events if pe['before_reference']]
            after_events = [pe for pe in processed_events if not pe['before_reference']]
            
            if before_events:
                output.append("\n📌 Potential Triggers (events before reference):")
                
                # Group by device/client
                triggers_by_device = defaultdict(list)
                triggers_by_client = defaultdict(list)
                
                for pe in before_events[-10:]:  # Last 10 events before reference
                    event = pe['event']
                    if event.get('deviceName'):
                        triggers_by_device[event['deviceName']].append(event)
                    if event.get('clientMac'):
                        client_id = event.get('clientName', event['clientMac'])
                        triggers_by_client[client_id].append(event)
                
                # Find devices/clients with multiple events
                for device, device_events in triggers_by_device.items():
                    if len(device_events) > 1:
                        output.append(f"   • {device}: {len(device_events)} events")
                        for e in device_events[-3:]:
                            output.append(f"     - {e.get('type', 'unknown')}")
                
                for client, client_events in triggers_by_client.items():
                    if len(client_events) > 1:
                        output.append(f"   • {client}: {len(client_events)} events")
                        for e in client_events[-3:]:
                            output.append(f"     - {e.get('type', 'unknown')}")
            
            if after_events:
                output.append("\n📌 Cascade Effects (events after reference):")
                
                # Count event types that occurred after
                cascade_types = Counter(pe['event'].get('type', 'unknown') for pe in after_events[:20])
                
                for event_type, count in cascade_types.most_common(5):
                    output.append(f"   • {event_type}: {count} occurrences")
            
            # Identify patterns
            output.append("\n🎯 Correlation Patterns:")
            output.append("-" * 40)
            
            # Check for auth → dhcp → connectivity pattern
            event_types_list = [pe['event'].get('type', '') for pe in processed_events]
            
            patterns_found = []
            
            if 'auth_fail' in event_types_list and 'dhcp_no_lease' in event_types_list:
                patterns_found.append("Authentication → DHCP failure chain detected")
            
            if 'device_down' in event_types_list and 'client_connectivity_issue' in event_types_list:
                patterns_found.append("Device failure → Client impact correlation")
            
            if 'high_channel_utilization' in event_types_list and 'association_reject' in event_types_list:
                patterns_found.append("Wireless congestion → Connection failures")
            
            if patterns_found:
                for pattern in patterns_found:
                    output.append(f"   ⚠️ {pattern}")
            else:
                output.append("   No specific correlation patterns detected")
            
            # Summary
            output.extend([
                "",
                "📊 Summary:",
                f"• Total events in window: {len(events)}",
                f"• Events before reference: {len(before_events)}",
                f"• Events after reference: {len(after_events)}",
                f"• Unique event types: {len(set(event_types_list))}",
                f"• Devices involved: {len(set(e['event'].get('deviceName', '') for e in processed_events if e['event'].get('deviceName')))}",
                f"• Clients involved: {len(set(e['event'].get('clientMac', '') for e in processed_events if e['event'].get('clientMac')))}"
            ])
        
        return "\n".join(output)
        
    except Exception as e:
        return format_error("correlate events", e)


def generate_incident_timeline(
    network_id: str,
    start_time: str,
    end_time: str,
    affected_device: Optional[str] = None,
    affected_client: Optional[str] = None
) -> str:
    """
    📝 Generate a detailed incident timeline for documentation.
    
    Creates a comprehensive timeline of events for incident reporting.
    
    Args:
        network_id: Network ID where incident occurred
        start_time: Incident start time (ISO format)
        end_time: Incident end time (ISO format)
        affected_device: Specific device serial if applicable
        affected_client: Specific client MAC if applicable
        
    Returns:
        Formatted incident timeline report
    """
    try:
        output = ["📝 Incident Timeline Report", "=" * 50, ""]
        
        # Parse times
        try:
            start_dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
            end_dt = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
        except:
            return "❌ Invalid time format. Use ISO format: YYYY-MM-DDTHH:MM:SSZ"
        
        if end_dt <= start_dt:
            return "❌ End time must be after start time"
        
        duration = end_dt - start_dt
        
        # Header information
        output.extend([
            "📋 Incident Details:",
            f"   Start: {start_dt.strftime('%Y-%m-%d %H:%M:%S')} UTC",
            f"   End: {end_dt.strftime('%Y-%m-%d %H:%M:%S')} UTC", 
            f"   Duration: {duration}",
            f"   Network ID: {network_id}"
        ])
        
        if affected_device:
            output.append(f"   Affected Device: {affected_device}")
        if affected_client:
            output.append(f"   Affected Client: {affected_client}")
        
        output.append("")
        
        # Get all events during incident
        params = {
            'perPage': 1000,
            'startingAfter': start_time,
            'endingBefore': end_time
        }
        
        if affected_device:
            params['deviceSerial'] = affected_device
        if affected_client:
            params['clientMac'] = affected_client
        
        with safe_api_call("get incident events"):
            events_response = meraki.dashboard.networks.getNetworkEvents(
                network_id,
                **params
            )
            
            events = events_response.get('events', []) if isinstance(events_response, dict) else []
            
            if not events:
                output.append("No events found during the incident timeframe")
                return "\n".join(output)
            
            # Process events
            processed_events = []
            event_categories = defaultdict(int)
            affected_devices = set()
            affected_clients = set()
            
            for event in events:
                try:
                    event_time = datetime.fromisoformat(event['occurredAt'].replace('Z', '+00:00'))
                    processed_events.append({
                        'time': event_time,
                        'type': event.get('type', 'unknown'),
                        'category': event.get('category', 'unknown'),
                        'description': event.get('description', 'No description'),
                        'device': event.get('deviceName', event.get('deviceSerial', '')),
                        'client': event.get('clientName', event.get('clientMac', '')),
                        'details': event
                    })
                    
                    event_categories[event.get('category', 'unknown')] += 1
                    
                    if event.get('deviceName'):
                        affected_devices.add(event['deviceName'])
                    if event.get('clientMac'):
                        affected_clients.add(event.get('clientName', event['clientMac']))
                except:
                    continue
            
            # Sort by time
            processed_events.sort(key=lambda x: x['time'])
            
            # Executive Summary
            output.extend([
                "📊 Executive Summary:",
                "-" * 40,
                f"Total Events: {len(events)}",
                f"Event Categories: {', '.join(f'{k} ({v})' for k, v in event_categories.items())}",
                f"Devices Affected: {len(affected_devices)}",
                f"Clients Affected: {len(affected_clients)}",
                ""
            ])
            
            # Timeline phases
            output.append("🕐 Incident Phases:")
            output.append("-" * 40)
            
            # Divide timeline into phases
            phase_duration = duration / 3
            phase1_end = start_dt + phase_duration
            phase2_end = start_dt + (phase_duration * 2)
            
            phase1_events = [e for e in processed_events if e['time'] <= phase1_end]
            phase2_events = [e for e in processed_events if phase1_end < e['time'] <= phase2_end]
            phase3_events = [e for e in processed_events if e['time'] > phase2_end]
            
            # Initial phase
            if phase1_events:
                output.append(f"\n🔴 Initial Phase ({start_dt.strftime('%H:%M')} - {phase1_end.strftime('%H:%M')})")
                output.append(f"   {len(phase1_events)} events")
                
                # Most common events in this phase
                phase1_types = Counter(e['type'] for e in phase1_events)
                for event_type, count in phase1_types.most_common(3):
                    output.append(f"   • {event_type}: {count}")
            
            # Development phase
            if phase2_events:
                output.append(f"\n🟡 Development Phase ({phase1_end.strftime('%H:%M')} - {phase2_end.strftime('%H:%M')})")
                output.append(f"   {len(phase2_events)} events")
                
                phase2_types = Counter(e['type'] for e in phase2_events)
                for event_type, count in phase2_types.most_common(3):
                    output.append(f"   • {event_type}: {count}")
            
            # Resolution phase
            if phase3_events:
                output.append(f"\n🟢 Resolution Phase ({phase2_end.strftime('%H:%M')} - {end_dt.strftime('%H:%M')})")
                output.append(f"   {len(phase3_events)} events")
                
                phase3_types = Counter(e['type'] for e in phase3_events)
                for event_type, count in phase3_types.most_common(3):
                    output.append(f"   • {event_type}: {count}")
            
            # Detailed Timeline
            output.extend([
                "",
                "📜 Detailed Event Timeline:",
                "-" * 40
            ])
            
            # Show key events (first, last, and critical ones)
            key_events = []
            
            # First event
            if processed_events:
                key_events.append(('FIRST', processed_events[0]))
            
            # Critical events
            critical_types = ['device_down', 'auth_fail', 'dhcp_no_lease', 'vpn_connectivity_issue']
            for event in processed_events:
                if event['type'] in critical_types and len(key_events) < 10:
                    key_events.append(('CRITICAL', event))
            
            # Last event
            if processed_events:
                key_events.append(('LAST', processed_events[-1]))
            
            for label, event in key_events:
                time_str = event['time'].strftime('%H:%M:%S')
                output.append(f"\n[{label}] {time_str}")
                output.append(f"Type: {event['type']}")
                output.append(f"Description: {event['description']}")
                if event['device']:
                    output.append(f"Device: {event['device']}")
                if event['client']:
                    output.append(f"Client: {event['client']}")
            
            # Impact Summary
            output.extend([
                "",
                "💥 Impact Analysis:",
                "-" * 40
            ])
            
            if affected_devices:
                output.append(f"\nAffected Devices ({len(affected_devices)}):")
                for device in sorted(affected_devices)[:10]:
                    output.append(f"   • {device}")
                if len(affected_devices) > 10:
                    output.append(f"   ... and {len(affected_devices) - 10} more")
            
            if affected_clients:
                output.append(f"\nAffected Clients ({len(affected_clients)}):")
                for client in sorted(affected_clients)[:10]:
                    output.append(f"   • {client}")
                if len(affected_clients) > 10:
                    output.append(f"   ... and {len(affected_clients) - 10} more")
            
            # Root Cause Indicators
            output.extend([
                "",
                "🎯 Root Cause Indicators:",
                "-" * 40
            ])
            
            # Find the event type that appeared most in the first phase
            if phase1_events:
                initial_cause = Counter(e['type'] for e in phase1_events).most_common(1)[0]
                output.append(f"Most frequent initial event: {initial_cause[0]} ({initial_cause[1]} occurrences)")
            
            # Event cascade analysis
            event_sequence = [e['type'] for e in processed_events[:20]]
            if 'device_down' in event_sequence:
                output.append("⚠️ Infrastructure failure detected")
            if 'auth_fail' in event_sequence:
                output.append("⚠️ Authentication system issues detected")
            if 'dhcp_no_lease' in event_sequence:
                output.append("⚠️ DHCP service issues detected")
            
            # Recommendations
            output.extend([
                "",
                "📋 Post-Incident Recommendations:",
                "-" * 40,
                "1. Review events in the initial phase for root cause",
                "2. Check configuration changes before incident",
                "3. Analyze affected devices for common factors",
                "4. Implement monitoring for detected patterns",
                "5. Create runbook for similar incidents",
                "",
                "📎 Report generated for incident documentation",
                "   Save this timeline for post-mortem analysis"
            ])
        
        return "\n".join(output)
        
    except Exception as e:
        return format_error("generate incident timeline", e)


# Helper tool
def event_analysis_help() -> str:
    """
    ❓ Get help on using event log analysis tools.
    
    Provides guidance on analyzing events and finding patterns.
    
    Returns:
        Help guide for event analysis tools
    """
    try:
        output = ["❓ Event Log Analysis Help Guide", "=" * 50, ""]
        
        output.extend([
            "🔧 Available Event Analysis Tools:",
            "",
            "1. **search_event_logs()**",
            "   Use when: Looking for specific events or errors",
            "   Features: Search by text, filter by type, device, or client",
            "   Example: search_event_logs(network_id, search_term='auth fail', timespan=3600)",
            "",
            "2. **analyze_error_patterns()**", 
            "   Use when: Need to find recurring issues",
            "   Features: Pattern detection, frequency analysis, clustering",
            "   Example: analyze_error_patterns(network_id, timespan=86400, min_occurrences=5)",
            "",
            "3. **identify_root_causes()**",
            "   Use when: Investigating why something happened",
            "   Features: Analyzes events around an issue, suggests causes",
            "   Example: identify_root_causes(network_id, 'users cannot connect to wifi')",
            "",
            "4. **correlate_events()**",
            "   Use when: Understanding what happened at specific time",
            "   Features: Shows related events in time window",
            "   Example: correlate_events(network_id, '2024-01-20T15:30:00Z', correlation_window=300)",
            "",
            "5. **generate_incident_timeline()**",
            "   Use when: Documenting an incident",
            "   Features: Creates detailed timeline for reports",
            "   Example: generate_incident_timeline(network_id, start_time, end_time)",
            "",
            "🔍 Common Event Types:",
            "",
            "**Authentication Events:**",
            "• auth_fail - General authentication failure",
            "• wireless_auth_fail - WiFi authentication failure", 
            "• wired_8021x_auth_fail - Wired 802.1X failure",
            "• radius_auth_fail - RADIUS server failure",
            "",
            "**Connectivity Events:**",
            "• association_reject - Client association rejected",
            "• dhcp_no_lease - DHCP lease not obtained",
            "• client_connectivity_issue - General connectivity problem",
            "• dns_lookup_fail - DNS resolution failure",
            "",
            "**Infrastructure Events:**",
            "• device_down - Device went offline",
            "• port_cycle - Switch port flapped",
            "• vpn_connectivity_issue - VPN tunnel problem",
            "• gateway_down - Gateway unreachable",
            "",
            "**Wireless Events:**",
            "• deauth - Client deauthenticated",
            "• disassociation - Client disassociated",
            "• high_channel_utilization - Channel congestion",
            "",
            "💡 Analysis Tips:",
            "",
            "**For Authentication Issues:**",
            "1. search_event_logs(network_id, event_types=['auth_fail', 'radius_auth_fail'])",
            "2. Look for patterns by client or time",
            "3. Check RADIUS server connectivity",
            "",
            "**For Connectivity Problems:**",
            "1. identify_root_causes(network_id, 'connectivity issues')",
            "2. Check DHCP and DNS events",
            "3. Look for infrastructure problems",
            "",
            "**For Performance Issues:**",
            "1. analyze_error_patterns(network_id, timespan=7200)",
            "2. Look for port cycles or high utilization",
            "3. Check for correlated device events",
            "",
            "**For Incident Investigation:**",
            "1. Note the approximate time of issue",
            "2. Use correlate_events() around that time",
            "3. Generate timeline for documentation",
            "",
            "📊 Time Ranges:",
            "• 300 = 5 minutes (correlation)",
            "• 3600 = 1 hour (recent issues)",
            "• 7200 = 2 hours (root cause)",
            "• 86400 = 24 hours (patterns)",
            "• 604800 = 7 days (trends)"
        ])
        
        return "\n".join(output)
        
    except Exception as e:
        return format_error("event analysis help", e)


def register_event_analysis_tools(app: FastMCP, client: MerakiClient):
    """Register event analysis tools with the MCP server."""
    global mcp_app, meraki
    mcp_app = app
    meraki = client
    
    # Register all tools
    app.tool()(search_event_logs)
    app.tool()(analyze_error_patterns)
    app.tool()(identify_root_causes)
    app.tool()(correlate_events)
    app.tool()(generate_incident_timeline)
    app.tool()(event_analysis_help)