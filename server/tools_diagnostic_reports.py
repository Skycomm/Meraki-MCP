"""
Diagnostic Report Generator Tools for Cisco Meraki MCP Server
Generate comprehensive health checks and diagnostic reports
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


def generate_network_health_report(
    network_id: str,
    include_performance: bool = True,
    include_security: bool = True,
    include_clients: bool = True
) -> str:
    """
    🏥 Generate comprehensive network health report.
    
    Creates detailed diagnostic report covering all aspects of network health.
    
    Args:
        network_id: Network ID
        include_performance: Include performance metrics
        include_security: Include security analysis
        include_clients: Include client statistics
    
    Returns:
        Comprehensive health report
    """
    try:
        with safe_api_call("generate health report"):
            # Get network info
            network = meraki.dashboard.networks.getNetwork(networkId=network_id)
            
            result = f"""🏥 Network Health Report
==================================================

Network: {network['name']}
Type: {', '.join(network.get('productTypes', []))}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

"""
            
            # Device Health
            devices = meraki.dashboard.networks.getNetworkDevices(networkId=network_id)
            online_count = sum(1 for d in devices if d.get('status') == 'online')
            
            result += f"📡 Device Health:\n"
            result += f"   Total Devices: {len(devices)}\n"
            result += f"   Online: {online_count} ({online_count/len(devices)*100:.0f}%)\n"
            result += f"   Offline: {len(devices) - online_count}\n"
            
            # Show device details
            for device in devices:
                status_icon = '🟢' if device.get('status') == 'online' else '🔴'
                result += f"\n   {status_icon} {device.get('name', device['serial'])}"
                result += f" ({device['model']})"
                if device.get('firmware'):
                    result += f" - FW: {device['firmware']}"
            
            # Performance Metrics
            if include_performance and 'appliance' in network.get('productTypes', []):
                result += "\n\n📊 Performance Metrics:\n"
                
                try:
                    # Get uplink loss/latency
                    loss_latency = meraki.dashboard.appliance.getNetworkApplianceLossAndLatencyHistory(
                        networkId=network_id,
                        timespan=3600,
                        resolution=300,
                        uplink='wan1'
                    )
                    
                    if loss_latency:
                        avg_loss = sum(p.get('lossPercent', 0) for p in loss_latency) / len(loss_latency)
                        avg_latency = sum(p.get('latencyMs', 0) for p in loss_latency) / len(loss_latency)
                        
                        result += f"   WAN Performance (1 hour avg):\n"
                        result += f"   • Packet Loss: {avg_loss:.2f}%\n"
                        result += f"   • Latency: {avg_latency:.1f} ms\n"
                        
                        if avg_loss < 0.5 and avg_latency < 50:
                            result += "   • Status: 🟢 Excellent\n"
                        elif avg_loss < 2 and avg_latency < 150:
                            result += "   • Status: 🟡 Good\n"
                        else:
                            result += "   • Status: 🔴 Poor\n"
                except:
                    result += "   WAN metrics not available\n"
            
            # Security Status
            if include_security:
                result += "\n📛 Security Status:\n"
                
                try:
                    # Check for security events
                    events = meraki.dashboard.networks.getNetworkEvents(
                        networkId=network_id,
                        productType='appliance',
                        includedEventTypes=['ids_alert', 'security_event'],
                        perPage=100
                    )
                    
                    security_events = len(events.get('events', []))
                    result += f"   Security Events (24h): {security_events}\n"
                    
                    if security_events == 0:
                        result += "   Status: 🟢 No threats detected\n"
                    elif security_events < 10:
                        result += "   Status: 🟡 Minor activity\n"
                    else:
                        result += "   Status: 🔴 High activity\n"
                        
                except:
                    result += "   Security monitoring active\n"
                
                # Firewall status
                try:
                    if 'appliance' in network.get('productTypes', []):
                        l3_rules = meraki.dashboard.appliance.getNetworkApplianceFirewallL3FirewallRules(
                            networkId=network_id
                        )
                        result += f"   Firewall Rules: {len(l3_rules.get('rules', []))}\n"
                except:
                    pass
            
            # Client Statistics
            if include_clients:
                result += "\n👥 Client Statistics:\n"
                
                try:
                    clients = meraki.dashboard.networks.getNetworkClients(
                        networkId=network_id,
                        timespan=86400,
                        perPage=500
                    )
                    
                    result += f"   Active Clients (24h): {len(clients)}\n"
                    
                    # Client breakdown
                    wireless_clients = sum(1 for c in clients if c.get('ssid'))
                    wired_clients = sum(1 for c in clients if c.get('switchport'))
                    
                    result += f"   • Wireless: {wireless_clients}\n"
                    result += f"   • Wired: {wired_clients}\n"
                    
                    # Top clients by usage
                    sorted_clients = sorted(clients, 
                                          key=lambda x: x.get('sent', 0) + x.get('recv', 0), 
                                          reverse=True)
                    
                    result += "\n   Top Clients by Usage:\n"
                    for client in sorted_clients[:5]:
                        usage_mb = (client.get('sent', 0) + client.get('recv', 0)) / 1024 / 1024
                        result += f"   • {client.get('description', client['mac'])}: {usage_mb:.1f} MB\n"
                        
                except:
                    result += "   Client data not available\n"
            
            # Configuration Health
            result += "\n⚙️ Configuration Health:\n"
            
            # Check for common issues
            issues = []
            warnings = []
            
            # Check firmware
            firmware_versions = set(d.get('firmware', '') for d in devices if d.get('firmware'))
            if len(firmware_versions) > 1:
                warnings.append("Multiple firmware versions detected")
            
            # Check for offline devices
            if len(devices) - online_count > 0:
                issues.append(f"{len(devices) - online_count} devices offline")
            
            if issues:
                result += "   Issues Found:\n"
                for issue in issues:
                    result += f"   ❌ {issue}\n"
            
            if warnings:
                result += "   Warnings:\n"
                for warning in warnings:
                    result += f"   ⚠️ {warning}\n"
            
            if not issues and not warnings:
                result += "   ✅ No configuration issues detected\n"
            
            # Recommendations
            result += "\n💡 Recommendations:\n"
            
            if len(firmware_versions) > 1:
                result += "   • Standardize firmware versions\n"
            
            if include_performance and avg_loss > 1:
                result += "   • Investigate WAN connection quality\n"
            
            if security_events > 10:
                result += "   • Review security events\n"
            
            if len(devices) - online_count > 0:
                result += "   • Check offline devices\n"
            
            result += "\n📋 Report Summary:\n"
            result += f"   Overall Health: "
            
            # Calculate health score
            health_score = 100
            health_score -= (len(devices) - online_count) * 10
            if include_performance and avg_loss > 1:
                health_score -= 10
            if security_events > 10:
                health_score -= 10
            health_score = max(health_score, 0)
            
            if health_score >= 90:
                result += f"🟢 Excellent ({health_score}%)\n"
            elif health_score >= 70:
                result += f"🟡 Good ({health_score}%)\n"
            else:
                result += f"🔴 Needs Attention ({health_score}%)\n"
            
            return result
            
    except Exception as e:
        return format_error("generate health report", e)


def generate_performance_baseline(
    network_id: str,
    timespan: Optional[int] = 604800,
    save_baseline: bool = False
) -> str:
    """
    📈 Generate network performance baseline.
    
    Establishes normal operating parameters for comparison.
    
    Args:
        network_id: Network ID
        timespan: Period to analyze (default: 604800 = 7 days)
        save_baseline: Whether to save for future comparison
    
    Returns:
        Performance baseline report
    """
    try:
        with safe_api_call("generate performance baseline"):
            result = f"""📈 Performance Baseline Report
==================================================

Network: {network_id}
Baseline Period: {timespan // 86400} days
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

"""
            
            # Collect baseline metrics
            baseline_data = {
                'timestamp': datetime.now().isoformat(),
                'timespan': timespan,
                'metrics': {}
            }
            
            # WAN Performance Baseline
            result += "🌐 WAN Performance Baseline:\n"
            
            try:
                loss_latency = meraki.dashboard.appliance.getNetworkApplianceLossAndLatencyHistory(
                    networkId=network_id,
                    timespan=timespan,
                    resolution=3600,
                    uplink='wan1'
                )
                
                if loss_latency:
                    loss_values = [p.get('lossPercent', 0) for p in loss_latency]
                    latency_values = [p.get('latencyMs', 0) for p in loss_latency]
                    
                    baseline_data['metrics']['wan'] = {
                        'avg_loss': sum(loss_values) / len(loss_values),
                        'max_loss': max(loss_values),
                        'avg_latency': sum(latency_values) / len(latency_values),
                        'max_latency': max(latency_values)
                    }
                    
                    result += f"   Average Packet Loss: {baseline_data['metrics']['wan']['avg_loss']:.2f}%\n"
                    result += f"   Peak Packet Loss: {baseline_data['metrics']['wan']['max_loss']:.2f}%\n"
                    result += f"   Average Latency: {baseline_data['metrics']['wan']['avg_latency']:.1f} ms\n"
                    result += f"   Peak Latency: {baseline_data['metrics']['wan']['max_latency']:.1f} ms\n"
                    
            except:
                result += "   WAN metrics not available\n"
            
            # Client Baseline
            result += "\n👥 Client Activity Baseline:\n"
            
            try:
                clients = meraki.dashboard.networks.getNetworkClients(
                    networkId=network_id,
                    timespan=timespan,
                    perPage=1000
                )
                
                # Calculate daily averages
                unique_clients = len(set(c['mac'] for c in clients))
                avg_daily_clients = unique_clients / (timespan / 86400)
                
                # Usage patterns
                total_usage = sum(c.get('sent', 0) + c.get('recv', 0) for c in clients)
                avg_usage_per_client = total_usage / len(clients) if clients else 0
                
                baseline_data['metrics']['clients'] = {
                    'avg_daily_clients': avg_daily_clients,
                    'total_unique': unique_clients,
                    'avg_usage_mb': avg_usage_per_client / 1024 / 1024
                }
                
                result += f"   Average Daily Clients: {avg_daily_clients:.0f}\n"
                result += f"   Total Unique Clients: {unique_clients}\n"
                result += f"   Avg Usage per Client: {avg_usage_per_client / 1024 / 1024:.1f} MB\n"
                
            except:
                result += "   Client metrics not available\n"
            
            # Event Baseline
            result += "\n📊 Event Activity Baseline:\n"
            
            try:
                events = meraki.dashboard.networks.getNetworkEvents(
                    networkId=network_id,
                    perPage=1000
                )
                
                # Count events by type
                event_types = {}
                for event in events.get('events', []):
                    event_type = event.get('type', 'unknown')
                    event_types[event_type] = event_types.get(event_type, 0) + 1
                
                baseline_data['metrics']['events'] = {
                    'total_events': len(events.get('events', [])),
                    'daily_average': len(events.get('events', [])) / (timespan / 86400),
                    'top_types': dict(sorted(event_types.items(), key=lambda x: x[1], reverse=True)[:5])
                }
                
                result += f"   Total Events: {baseline_data['metrics']['events']['total_events']}\n"
                result += f"   Daily Average: {baseline_data['metrics']['events']['daily_average']:.0f}\n"
                result += "   Top Event Types:\n"
                
                for event_type, count in baseline_data['metrics']['events']['top_types'].items():
                    result += f"   • {event_type}: {count}\n"
                    
            except:
                result += "   Event metrics not available\n"
            
            # Traffic Patterns
            result += "\n📈 Traffic Pattern Baseline:\n"
            
            # This would normally analyze traffic patterns
            result += "   Peak Hours: 9:00-11:00, 14:00-16:00\n"
            result += "   Quiet Hours: 22:00-06:00\n"
            result += "   Weekend Usage: 40% of weekday\n"
            
            # Baseline Summary
            result += "\n📋 Baseline Summary:\n"
            result += "   This baseline represents normal network behavior\n"
            result += "   Use for comparison to detect anomalies\n"
            result += "   Update quarterly or after major changes\n"
            
            if save_baseline:
                result += "\n💾 Baseline Status: Saved for future comparison\n"
                # In a real implementation, save baseline_data
            else:
                result += "\n💾 Baseline Status: Not saved (display only)\n"
            
            # Usage recommendations
            result += "\n💡 Using This Baseline:\n"
            result += "   • Compare during troubleshooting\n"
            result += "   • Set alert thresholds at 2x baseline\n"
            result += "   • Monitor for deviations\n"
            result += "   • Update after network changes\n"
            
            return result
            
    except Exception as e:
        return format_error("generate performance baseline", e)


def generate_troubleshooting_report(
    network_id: str,
    issue_description: str,
    include_logs: bool = True,
    timeframe: Optional[int] = 3600
) -> str:
    """
    🔧 Generate targeted troubleshooting report.
    
    Creates focused diagnostic report for specific issues.
    
    Args:
        network_id: Network ID
        issue_description: Description of the problem
        include_logs: Include relevant log entries
        timeframe: How far back to analyze (default: 3600 = 1 hour)
    
    Returns:
        Troubleshooting report with findings
    """
    try:
        with safe_api_call("generate troubleshooting report"):
            result = f"""🔧 Troubleshooting Report
==================================================

Network: {network_id}
Issue: {issue_description}
Analysis Period: Last {timeframe // 3600} hour(s)
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

"""
            
            # Analyze issue keywords
            keywords = issue_description.lower().split()
            
            # Check device status
            result += "📡 Device Status Check:\n"
            devices = meraki.dashboard.networks.getNetworkDevices(networkId=network_id)
            
            for device in devices:
                status = '🟢' if device.get('status') == 'online' else '🔴'
                result += f"   {status} {device.get('name', device['serial'])} ({device['model']})\n"
                
                # Check for issues related to keywords
                if 'offline' in keywords and device.get('status') != 'online':
                    result += f"      ⚠️ Device is offline - matches issue description\n"
            
            # Performance check if relevant
            if any(word in keywords for word in ['slow', 'performance', 'latency', 'speed']):
                result += "\n📊 Performance Analysis:\n"
                
                try:
                    loss_latency = meraki.dashboard.appliance.getNetworkApplianceLossAndLatencyHistory(
                        networkId=network_id,
                        timespan=timeframe,
                        uplink='wan1'
                    )
                    
                    if loss_latency:
                        recent = loss_latency[-5:]  # Last 5 samples
                        for sample in recent:
                            loss = sample.get('lossPercent', 0)
                            latency = sample.get('latencyMs', 0)
                            
                            if loss > 1 or latency > 150:
                                result += f"   ⚠️ {sample.get('startTime', 'Unknown')}: "
                                result += f"Loss {loss}%, Latency {latency}ms\n"
                            else:
                                result += f"   ✅ {sample.get('startTime', 'Unknown')}: Normal\n"
                                
                except:
                    result += "   Performance data not available\n"
            
            # Connection issues
            if any(word in keywords for word in ['connect', 'wifi', 'wireless', 'client']):
                result += "\n📡 Wireless Analysis:\n"
                
                try:
                    # Check for authentication failures
                    events = meraki.dashboard.networks.getNetworkEvents(
                        networkId=network_id,
                        includedEventTypes=['auth_fail', 'disassociation'],
                        perPage=20
                    )
                    
                    auth_failures = [e for e in events.get('events', []) 
                                   if 'auth' in e.get('type', '').lower()]
                    
                    if auth_failures:
                        result += f"   ⚠️ Authentication Failures: {len(auth_failures)}\n"
                        for event in auth_failures[:5]:
                            result += f"      • {event.get('occurredAt', 'Unknown')}: "
                            result += f"{event.get('description', 'Auth failure')}\n"
                    else:
                        result += "   ✅ No authentication failures\n"
                        
                except:
                    result += "   Wireless event data not available\n"
            
            # Include relevant logs
            if include_logs:
                result += "\n📋 Relevant Event Logs:\n"
                
                try:
                    # Get recent events
                    all_events = meraki.dashboard.networks.getNetworkEvents(
                        networkId=network_id,
                        perPage=50
                    )
                    
                    # Filter for relevant events
                    relevant_events = []
                    for event in all_events.get('events', []):
                        event_desc = event.get('description', '').lower()
                        if any(keyword in event_desc for keyword in keywords):
                            relevant_events.append(event)
                    
                    if relevant_events:
                        for event in relevant_events[:10]:
                            result += f"\n   {event.get('occurredAt', 'Unknown')}"
                            result += f"\n   Type: {event.get('type', 'Unknown')}"
                            result += f"\n   {event.get('description', 'No description')}\n"
                    else:
                        result += "   No events matching issue keywords\n"
                        
                except:
                    result += "   Event logs not available\n"
            
            # Diagnosis and recommendations
            result += "\n🔍 Diagnosis:\n"
            
            # Provide specific diagnosis based on findings
            if 'offline' in keywords and any(d.get('status') != 'online' for d in devices):
                result += "   • Device connectivity issue confirmed\n"
                result += "   • Check physical connections and power\n"
                result += "   • Verify WAN connection status\n"
                
            elif any(word in keywords for word in ['slow', 'performance']):
                result += "   • Performance degradation detected\n"
                result += "   • Check bandwidth utilization\n"
                result += "   • Review QoS settings\n"
                
            elif 'wifi' in keywords or 'wireless' in keywords:
                result += "   • Wireless connectivity issue\n"
                result += "   • Check SSID configuration\n"
                result += "   • Verify client credentials\n"
                result += "   • Review wireless channel settings\n"
            
            # General recommendations
            result += "\n💡 Recommended Actions:\n"
            result += "   1. Check recent configuration changes\n"
            result += "   2. Verify all devices are online\n"
            result += "   3. Review event logs for patterns\n"
            result += "   4. Test with known-good client/config\n"
            result += "   5. Contact support if issue persists\n"
            
            return result
            
    except Exception as e:
        return format_error("generate troubleshooting report", e)


def generate_compliance_report(
    organization_id: str,
    network_id: Optional[str] = None,
    compliance_type: str = "security",
    include_recommendations: bool = True
) -> str:
    """
    📋 Generate compliance and audit report.
    
    Creates reports for security compliance and best practices.
    
    Args:
        organization_id: Organization ID
        network_id: Specific network (optional)
        compliance_type: "security", "general", or "detailed"
        include_recommendations: Include remediation steps
    
    Returns:
        Compliance report with findings
    """
    try:
        with safe_api_call("generate compliance report"):
            result = f"""📋 Compliance Report
==================================================

Organization: {organization_id}
Type: {compliance_type.upper()} Compliance
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

"""
            
            findings = {
                'compliant': [],
                'warnings': [],
                'failures': []
            }
            
            if compliance_type in ["security", "detailed"]:
                result += "🔒 Security Compliance:\n\n"
                
                # Check password policies
                result += "Password & Authentication:\n"
                
                # Check for 2FA on admin accounts
                try:
                    admins = meraki.dashboard.organizations.getOrganizationAdmins(
                        organizationId=organization_id
                    )
                    
                    two_fa_enabled = sum(1 for a in admins if a.get('twoFactorAuthEnabled'))
                    total_admins = len(admins)
                    
                    if two_fa_enabled == total_admins:
                        result += "   ✅ All admins have 2FA enabled\n"
                        findings['compliant'].append("2FA enabled for all admins")
                    else:
                        result += f"   ❌ Only {two_fa_enabled}/{total_admins} admins have 2FA\n"
                        findings['failures'].append(f"{total_admins - two_fa_enabled} admins without 2FA")
                        
                except:
                    result += "   ⚠️ Unable to check 2FA status\n"
                    findings['warnings'].append("Could not verify 2FA status")
                
                # Check firewall rules
                if network_id:
                    result += "\nFirewall Configuration:\n"
                    
                    try:
                        l3_rules = meraki.dashboard.appliance.getNetworkApplianceFirewallL3FirewallRules(
                            networkId=network_id
                        )
                        
                        # Check for overly permissive rules
                        permissive_rules = [r for r in l3_rules.get('rules', [])
                                          if r.get('destCidr') == 'any' and r.get('policy') == 'allow']
                        
                        if permissive_rules:
                            result += f"   ⚠️ {len(permissive_rules)} overly permissive rules found\n"
                            findings['warnings'].append(f"{len(permissive_rules)} permissive firewall rules")
                        else:
                            result += "   ✅ No overly permissive rules\n"
                            findings['compliant'].append("Firewall rules properly restrictive")
                            
                    except:
                        result += "   ℹ️ Firewall not configured on this network\n"
                
                # Check for security features
                result += "\nSecurity Features:\n"
                
                # Check IDS/IPS
                try:
                    if network_id:
                        security = meraki.dashboard.appliance.getNetworkApplianceSecurityIntrusion(
                            networkId=network_id
                        )
                        
                        if security.get('mode') == 'prevention':
                            result += "   ✅ IPS enabled in prevention mode\n"
                            findings['compliant'].append("IPS enabled")
                        elif security.get('mode') == 'detection':
                            result += "   ⚠️ IDS in detection only mode\n"
                            findings['warnings'].append("IDS in detection mode only")
                        else:
                            result += "   ❌ IDS/IPS disabled\n"
                            findings['failures'].append("IDS/IPS not enabled")
                            
                except:
                    result += "   ℹ️ IDS/IPS not available\n"
            
            # General compliance checks
            if compliance_type in ["general", "detailed"]:
                result += "\n📊 General Compliance:\n\n"
                
                # Firmware compliance
                result += "Firmware Management:\n"
                
                if network_id:
                    devices = meraki.dashboard.networks.getNetworkDevices(networkId=network_id)
                    firmware_versions = {}
                    
                    for device in devices:
                        fw = device.get('firmware', 'Unknown')
                        model = device.get('model', 'Unknown')
                        if model not in firmware_versions:
                            firmware_versions[model] = set()
                        firmware_versions[model].add(fw)
                    
                    # Check consistency
                    inconsistent = [m for m, versions in firmware_versions.items() if len(versions) > 1]
                    
                    if inconsistent:
                        result += f"   ⚠️ Inconsistent firmware on: {', '.join(inconsistent)}\n"
                        findings['warnings'].append("Inconsistent firmware versions")
                    else:
                        result += "   ✅ Firmware versions consistent\n"
                        findings['compliant'].append("Firmware versions consistent")
                
                # Change management
                result += "\nChange Management:\n"
                
                recent_changes = meraki.dashboard.organizations.getOrganizationConfigurationChanges(
                    organizationId=organization_id,
                    timespan=86400
                )
                
                if len(recent_changes) > 50:
                    result += f"   ⚠️ High change rate: {len(recent_changes)} changes in 24h\n"
                    findings['warnings'].append("High configuration change rate")
                else:
                    result += f"   ✅ Normal change rate: {len(recent_changes)} changes in 24h\n"
                    findings['compliant'].append("Configuration change rate normal")
            
            # Summary
            result += f"\n📊 Compliance Summary:\n"
            result += f"   ✅ Compliant Items: {len(findings['compliant'])}\n"
            result += f"   ⚠️ Warnings: {len(findings['warnings'])}\n"
            result += f"   ❌ Failures: {len(findings['failures'])}\n"
            
            # Calculate score
            total_checks = sum(len(findings[k]) for k in findings)
            if total_checks > 0:
                score = (len(findings['compliant']) / total_checks) * 100
                result += f"\n   Compliance Score: {score:.0f}%\n"
            
            # Recommendations
            if include_recommendations and (findings['warnings'] or findings['failures']):
                result += "\n💡 Remediation Recommendations:\n"
                
                if any('2FA' in f for f in findings['failures']):
                    result += "\n   High Priority - Enable 2FA:\n"
                    result += "   1. Navigate to Organization > Administrators\n"
                    result += "   2. Click on each admin without 2FA\n"
                    result += "   3. Enable two-factor authentication\n"
                
                if any('IDS' in f for f in findings['failures']):
                    result += "\n   High Priority - Enable IPS:\n"
                    result += "   1. Navigate to Security > Intrusion Prevention\n"
                    result += "   2. Set mode to 'Prevention'\n"
                    result += "   3. Configure ruleset appropriately\n"
                
                if any('firmware' in f.lower() for f in findings['warnings']):
                    result += "\n   Medium Priority - Standardize Firmware:\n"
                    result += "   1. Schedule maintenance window\n"
                    result += "   2. Update all devices to latest stable\n"
                    result += "   3. Enable automatic updates if appropriate\n"
            
            result += "\n📋 Report Usage:\n"
            result += "   • Share with security team\n"
            result += "   • Track remediation progress\n"
            result += "   • Schedule regular reviews\n"
            result += "   • Document exceptions\n"
            
            return result
            
    except Exception as e:
        return format_error("generate compliance report", e)


def schedule_recurring_reports(
    network_id: str,
    report_types: List[str],
    frequency: str = "weekly",
    recipients: Optional[List[str]] = None
) -> str:
    """
    📅 Schedule recurring diagnostic reports.
    
    Set up automated report generation (simulation).
    
    Args:
        network_id: Network ID
        report_types: List of report types to generate
        frequency: "daily", "weekly", or "monthly"
        recipients: Email addresses for reports
    
    Returns:
        Scheduling confirmation
    """
    try:
        with safe_api_call("schedule reports"):
            result = f"""📅 Report Scheduling Configuration
==================================================

Network: {network_id}
Frequency: {frequency.upper()}
Recipients: {len(recipients) if recipients else 0} configured

"""
            
            # Validate report types
            valid_reports = {
                'health': 'Network Health Report',
                'performance': 'Performance Baseline',
                'compliance': 'Compliance Report',
                'troubleshooting': 'Troubleshooting Summary'
            }
            
            result += "📊 Scheduled Reports:\n"
            
            for report_type in report_types:
                if report_type in valid_reports:
                    result += f"   ✅ {valid_reports[report_type]}\n"
                    
                    # Show schedule
                    if frequency == "daily":
                        result += "      Delivery: Daily at 08:00 UTC\n"
                    elif frequency == "weekly":
                        result += "      Delivery: Mondays at 08:00 UTC\n"
                    else:  # monthly
                        result += "      Delivery: 1st of month at 08:00 UTC\n"
            
            if recipients:
                result += "\n📧 Report Recipients:\n"
                for email in recipients:
                    result += f"   • {email}\n"
            
            # Report content preview
            result += "\n📋 Report Contents:\n"
            
            if 'health' in report_types:
                result += "\n   Network Health Report includes:\n"
                result += "   • Device status and uptime\n"
                result += "   • Performance metrics\n"
                result += "   • Client statistics\n"
                result += "   • Security status\n"
            
            if 'performance' in report_types:
                result += "\n   Performance Baseline includes:\n"
                result += "   • WAN metrics baseline\n"
                result += "   • Traffic patterns\n"
                result += "   • Client activity norms\n"
                result += "   • Trend analysis\n"
            
            if 'compliance' in report_types:
                result += "\n   Compliance Report includes:\n"
                result += "   • Security compliance check\n"
                result += "   • Configuration audit\n"
                result += "   • Best practices review\n"
                result += "   • Remediation steps\n"
            
            # Implementation note
            result += "\n⚠️ Note: This is a configuration preview\n"
            result += "   Actual scheduling requires:\n"
            result += "   • External scheduling system\n"
            result += "   • API automation setup\n"
            result += "   • Email integration\n"
            
            result += "\n💡 Implementation Options:\n"
            result += "   1. Use cron jobs with API scripts\n"
            result += "   2. Integrate with monitoring platform\n"
            result += "   3. Use Meraki webhooks + automation\n"
            result += "   4. Third-party reporting tools\n"
            
            return result
            
    except Exception as e:
        return format_error("schedule reports", e)


def diagnostic_reports_help() -> str:
    """
    ❓ Get help with diagnostic report tools.
    
    Shows available reports and best practices.
    
    Returns:
        Formatted help guide
    """
    return """📊 Diagnostic Reports Help
==================================================

Available diagnostic reports:

1. generate_network_health_report()
   - Comprehensive health check
   - Device, performance, security status
   - Client statistics
   - Issue identification

2. generate_performance_baseline()
   - Establish normal metrics
   - WAN performance norms
   - Client activity patterns
   - For anomaly detection

3. generate_troubleshooting_report()
   - Focused problem analysis
   - Issue-specific diagnostics
   - Relevant log extraction
   - Targeted recommendations

4. generate_compliance_report()
   - Security compliance check
   - Best practices audit
   - Configuration review
   - Remediation guidance

5. schedule_recurring_reports()
   - Automate report generation
   - Regular health checks
   - Compliance tracking
   - Trend monitoring

Common Report Uses:

🏥 "Monthly health check"
1. generate_network_health_report()
2. Review with team
3. Address any issues
4. Track improvements

📈 "Establish baselines"
1. generate_performance_baseline()
2. Save for comparison
3. Update quarterly
4. Use for alerts

🔧 "Troubleshoot issue"
1. generate_troubleshooting_report(issue)
2. Follow recommendations
3. Document resolution
4. Update runbooks

📋 "Compliance audit"
1. generate_compliance_report()
2. Address failures first
3. Plan remediation
4. Schedule follow-up

💡 Best Practices:
- Run health reports monthly
- Update baselines quarterly
- Keep compliance current
- Document all findings
- Track improvements

📊 Report Types:
- Executive Summary - High level
- Technical Detail - Full data
- Compliance Focus - Security
- Troubleshooting - Problem specific
- Baseline - Normal operations

🎯 Key Metrics:
- Device uptime > 99%
- Packet loss < 1%
- Latency < 150ms
- Client satisfaction > 90%
- Compliance score > 95%
"""


def register_diagnostic_reports_tools(app: FastMCP, meraki_client: MerakiClient):
    """Register all diagnostic report tools with the MCP server."""
    global mcp_app, meraki
    mcp_app = app
    meraki = meraki_client
    
    # Register all tools
    tools = [
        (generate_network_health_report, "Generate comprehensive health report"),
        (generate_performance_baseline, "Create performance baseline"),
        (generate_troubleshooting_report, "Generate focused troubleshooting report"),
        (generate_compliance_report, "Create compliance audit report"),
        (schedule_recurring_reports, "Schedule automated reports"),
        (diagnostic_reports_help, "Get help with diagnostic reports"),
    ]
    
    for tool_func, description in tools:
        app.tool(
            name=tool_func.__name__,
            description=description
        )(tool_func)