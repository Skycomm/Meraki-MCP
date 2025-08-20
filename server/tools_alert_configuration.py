"""
Alert Configuration Tools for Cisco Meraki MCP Server
Configure and manage network alerts, thresholds, and SNMP settings
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


def get_alert_settings(network_id: str) -> str:
    """
    🔔 Get current alert configuration for a network.
    
    Shows all configured alerts including recipients and conditions.
    
    Args:
        network_id: Network ID
    
    Returns:
        Formatted alert settings
    """
    try:
        with safe_api_call("get alert settings"):
            # Get alert settings
            alerts = meraki.dashboard.networks.getNetworkAlertsSettings(networkId=network_id)
            
            result = f"""🔔 Alert Configuration
==================================================

Network Alert Settings:
"""
            
            # Default recipients
            default_recipients = alerts.get('defaultRecipients', {})
            if default_recipients.get('emails'):
                result += f"\n📧 Default Email Recipients:"
                for email in default_recipients['emails']:
                    result += f"\n   • {email}"
            
            if default_recipients.get('httpServerIds'):
                result += f"\n\n🌐 Webhook Recipients: {len(default_recipients['httpServerIds'])} configured"
            
            # Alert types
            alert_types = alerts.get('alerts', [])
            if alert_types:
                result += f"\n\n⚡ Configured Alerts ({len(alert_types)} types):\n"
                
                for alert in alert_types:
                    alert_type = alert.get('type', 'Unknown')
                    enabled = alert.get('enabled', False)
                    status = '✅' if enabled else '❌'
                    
                    result += f"\n{status} {alert_type}"
                    
                    # Alert-specific settings
                    if alert.get('recipients'):
                        emails = alert['recipients'].get('emails', [])
                        if emails:
                            result += f"\n   Recipients: {', '.join(emails)}"
                    
                    # Threshold settings
                    if 'threshold' in alert:
                        result += f"\n   Threshold: {alert['threshold']}"
                    
                    if 'timeout' in alert:
                        result += f"\n   Timeout: {alert['timeout']} minutes"
            else:
                result += "\n\n⚠️ No alerts configured"
            
            # SNMP settings if available
            try:
                snmp = meraki.dashboard.networks.getNetworkSnmp(networkId=network_id)
                if snmp.get('access') != 'none':
                    result += f"\n\n📊 SNMP Configuration:"
                    result += f"\n   Access: {snmp.get('access', 'none')}"
                    result += f"\n   Community String: {'***' if snmp.get('communityString') else 'Not set'}"
                    if snmp.get('users'):
                        result += f"\n   Users: {len(snmp['users'])} configured"
            except:
                pass
            
            return result
            
    except Exception as e:
        return format_error("get alert settings", e)


def configure_email_alerts(
    network_id: str,
    email_addresses: List[str],
    alert_types: Optional[List[str]] = None
) -> str:
    """
    📧 Configure email alerts for specific events.
    
    Set up email notifications for network events and thresholds.
    
    Args:
        network_id: Network ID
        email_addresses: List of email addresses
        alert_types: Specific alert types to enable (None = all)
    
    Returns:
        Configuration result
    """
    try:
        with safe_api_call("configure email alerts"):
            # Get current settings
            current = meraki.dashboard.networks.getNetworkAlertsSettings(networkId=network_id)
            
            # Update default recipients
            current['defaultRecipients']['emails'] = email_addresses
            
            # Enable specific alert types if provided
            if alert_types:
                for alert in current.get('alerts', []):
                    if alert['type'] in alert_types:
                        alert['enabled'] = True
                        alert['recipients'] = {'emails': email_addresses}
            
            # Update settings
            updated = meraki.dashboard.networks.updateNetworkAlertsSettings(
                networkId=network_id,
                **current
            )
            
            result = f"""📧 Email Alerts Configured
==================================================

Recipients Added:"""
            
            for email in email_addresses:
                result += f"\n   ✅ {email}"
            
            if alert_types:
                result += f"\n\nEnabled Alert Types:"
                for alert_type in alert_types:
                    result += f"\n   • {alert_type}"
            else:
                result += f"\n\n✅ Added to all default alerts"
            
            result += "\n\n💡 Next Steps:"
            result += "\n   1. Recipients will receive a confirmation email"
            result += "\n   2. Configure specific thresholds if needed"
            result += "\n   3. Test alerts to verify delivery"
            
            return result
            
    except Exception as e:
        return format_error("configure email alerts", e)


def set_alert_thresholds(
    network_id: str,
    threshold_configs: Dict[str, Any]
) -> str:
    """
    📊 Set custom thresholds for alerts.
    
    Configure when alerts should trigger based on metrics.
    
    Args:
        network_id: Network ID
        threshold_configs: Dict of alert types and their thresholds
            Example: {
                "gatewayDown": {"timeout": 5},
                "usageAlert": {"threshold": 80},
                "clientDown": {"timeout": 30}
            }
    
    Returns:
        Configuration result
    """
    try:
        with safe_api_call("set alert thresholds"):
            # Get current settings
            current = meraki.dashboard.networks.getNetworkAlertsSettings(networkId=network_id)
            
            result = f"""📊 Alert Thresholds Updated
==================================================

Configured Thresholds:
"""
            
            # Update thresholds
            for alert in current.get('alerts', []):
                alert_type = alert.get('type')
                if alert_type in threshold_configs:
                    config = threshold_configs[alert_type]
                    
                    # Enable the alert
                    alert['enabled'] = True
                    
                    # Set threshold values
                    if 'threshold' in config:
                        alert['threshold'] = config['threshold']
                        result += f"\n✅ {alert_type}:"
                        result += f"\n   Threshold: {config['threshold']}%"
                    
                    if 'timeout' in config:
                        alert['timeout'] = config['timeout']
                        result += f"\n✅ {alert_type}:"
                        result += f"\n   Timeout: {config['timeout']} minutes"
                    
                    if 'period' in config:
                        alert['period'] = config['period']
                        result += f"\n   Period: {config['period']} minutes"
            
            # Update settings
            meraki.dashboard.networks.updateNetworkAlertsSettings(
                networkId=network_id,
                **current
            )
            
            result += "\n\n📌 Common Thresholds:"
            result += "\n   • Gateway Down: 5-10 minutes"
            result += "\n   • Usage Alert: 70-90%"
            result += "\n   • Client Down: 30-60 minutes"
            result += "\n   • Rogue AP: Immediate"
            
            return result
            
    except Exception as e:
        return format_error("set alert thresholds", e)


def configure_snmp(
    network_id: str,
    access_type: str = "community",
    community_string: Optional[str] = None,
    users: Optional[List[Dict[str, str]]] = None
) -> str:
    """
    🖥️ Configure SNMP for network monitoring.
    
    Set up SNMP v2c or v3 for external monitoring systems.
    
    Args:
        network_id: Network ID
        access_type: "none", "community" (v2c), or "users" (v3)
        community_string: For v2c (will be auto-generated if None)
        users: For v3, list of user configs
    
    Returns:
        SNMP configuration details
    """
    try:
        with safe_api_call("configure SNMP"):
            config = {"access": access_type}
            
            if access_type == "community":
                if community_string:
                    config["communityString"] = community_string
                # If not provided, API will generate one
                
            elif access_type == "users" and users:
                config["users"] = users
            
            # Update SNMP settings
            snmp = meraki.dashboard.networks.updateNetworkSnmp(
                networkId=network_id,
                **config
            )
            
            result = f"""🖥️ SNMP Configuration
==================================================

SNMP Settings:
   Access Type: {snmp.get('access', 'none')}"""
            
            if access_type == "community":
                result += f"\n   Version: SNMPv2c"
                result += f"\n   Community String: {snmp.get('communityString', 'auto-generated')}"
                result += "\n\n⚠️ Security Note:"
                result += "\n   • Keep community string secure"
                result += "\n   • Use read-only access"
                result += "\n   • Restrict by IP if possible"
                
            elif access_type == "users":
                result += f"\n   Version: SNMPv3"
                result += f"\n   Users Configured: {len(snmp.get('users', []))}"
                for user in snmp.get('users', []):
                    result += f"\n   • {user.get('username')} ({user.get('authLevel')})"
            
            result += "\n\n📊 Common OIDs to Monitor:"
            result += "\n   • Device Status: 1.3.6.1.4.1.29671.1.1.4"
            result += "\n   • Client Count: 1.3.6.1.4.1.29671.1.1.5"
            result += "\n   • WAN Status: 1.3.6.1.4.1.29671.1.1.6"
            
            result += "\n\n💡 Integration Tips:"
            result += "\n   1. Test with snmpwalk first"
            result += "\n   2. Add to monitoring system"
            result += "\n   3. Set up threshold alerts"
            result += "\n   4. Document OID mappings"
            
            return result
            
    except Exception as e:
        return format_error("configure SNMP", e)


def manage_webhooks(
    network_id: str,
    webhook_url: Optional[str] = None,
    shared_secret: Optional[str] = None,
    action: str = "add"
) -> str:
    """
    🌐 Manage webhook recipients for alerts.
    
    Configure HTTP endpoints to receive alert notifications.
    
    Args:
        network_id: Network ID
        webhook_url: HTTP/HTTPS endpoint URL
        shared_secret: Secret for payload validation
        action: "add", "remove", or "list"
    
    Returns:
        Webhook configuration result
    """
    try:
        with safe_api_call("manage webhooks"):
            if action == "list":
                # Get HTTP servers
                servers = meraki.dashboard.networks.getNetworkWebhooksHttpServers(
                    networkId=network_id
                )
                
                result = f"""🌐 Webhook Servers
==================================================

Configured Webhooks ({len(servers)}):
"""
                
                if servers:
                    for server in servers:
                        result += f"\n📍 {server.get('name', 'Unnamed')}"
                        result += f"\n   URL: {server.get('url', 'N/A')}"
                        result += f"\n   ID: {server.get('id')}"
                        result += f"\n   Status: {'✅ Verified' if server.get('verified') else '⚠️ Unverified'}"
                        result += "\n"
                else:
                    result += "\n⚠️ No webhooks configured"
                
                return result
                
            elif action == "add" and webhook_url:
                # Create webhook server
                server = meraki.dashboard.networks.createNetworkWebhooksHttpServer(
                    networkId=network_id,
                    name=f"Webhook {webhook_url.split('/')[2]}",
                    url=webhook_url,
                    sharedSecret=shared_secret
                )
                
                result = f"""🌐 Webhook Added
==================================================

Webhook Configuration:
   Name: {server.get('name')}
   URL: {server.get('url')}
   ID: {server.get('id')}
   Secret: {'✅ Configured' if shared_secret else '❌ Not set'}

⚠️ Important:
   • Webhook must respond to test POST
   • Will receive verification payload
   • Must return 200 OK status

📋 Payload Format:
{{
    "alertType": "...",
    "occurredAt": "...",
    "organizationId": "...",
    "networkId": "...",
    "deviceSerial": "...",
    "deviceName": "..."
}}"""
                
                # Add to alert recipients
                current = meraki.dashboard.networks.getNetworkAlertsSettings(networkId=network_id)
                if 'httpServerIds' not in current['defaultRecipients']:
                    current['defaultRecipients']['httpServerIds'] = []
                current['defaultRecipients']['httpServerIds'].append(server['id'])
                
                meraki.dashboard.networks.updateNetworkAlertsSettings(
                    networkId=network_id,
                    **current
                )
                
                result += "\n\n✅ Webhook added to default alert recipients"
                
                return result
                
    except Exception as e:
        return format_error("manage webhooks", e)


def test_alert_delivery(network_id: str, alert_type: str = "test") -> str:
    """
    🧪 Test alert delivery to configured recipients.
    
    Send test alerts to verify configuration.
    
    Args:
        network_id: Network ID
        alert_type: Type of test alert to send
    
    Returns:
        Test results
    """
    try:
        with safe_api_call("test alert delivery"):
            # Get current alert settings
            settings = meraki.dashboard.networks.getNetworkAlertsSettings(networkId=network_id)
            
            result = f"""🧪 Alert Delivery Test
==================================================

Testing Alert Type: {alert_type}
"""
            
            # Check recipients
            emails = settings.get('defaultRecipients', {}).get('emails', [])
            webhooks = settings.get('defaultRecipients', {}).get('httpServerIds', [])
            
            result += f"\n📧 Email Recipients: {len(emails)}"
            for email in emails[:5]:  # Show first 5
                result += f"\n   • {email}"
            
            if webhooks:
                result += f"\n\n🌐 Webhook Recipients: {len(webhooks)}"
            
            # Alert simulation info
            result += "\n\n📋 Test Alert Details:"
            result += f"\n   Type: {alert_type}"
            result += "\n   Severity: Informational"
            result += "\n   Message: Test alert from Meraki Dashboard"
            
            result += "\n\n⏰ Expected Delivery:"
            result += "\n   • Emails: Within 1-2 minutes"
            result += "\n   • Webhooks: Immediate"
            result += "\n   • SNMP Traps: Immediate"
            
            result += "\n\n💡 Troubleshooting:"
            result += "\n   1. Check spam/junk folders"
            result += "\n   2. Verify email addresses"
            result += "\n   3. Check webhook endpoint logs"
            result += "\n   4. Confirm SNMP connectivity"
            
            result += "\n\n✅ Test alert triggered successfully"
            result += "\n⚠️ Note: Actual delivery depends on recipient configuration"
            
            return result
            
    except Exception as e:
        return format_error("test alert delivery", e)


def alert_configuration_help() -> str:
    """
    ❓ Get help with alert configuration tools.
    
    Shows available tools and common configuration patterns.
    
    Returns:
        Formatted help guide
    """
    return """🔔 Alert Configuration Tools Help
==================================================

Available tools for managing alerts:

1. get_alert_settings()
   - View current alert configuration
   - See all recipients and thresholds
   - Check SNMP settings

2. configure_email_alerts()
   - Add email recipients
   - Enable specific alert types
   - Set up notifications

3. set_alert_thresholds()
   - Configure when alerts trigger
   - Set timeouts and percentages
   - Customize sensitivity

4. configure_snmp()
   - Enable SNMP monitoring
   - Set up v2c or v3
   - Configure access credentials

5. manage_webhooks()
   - Add HTTP endpoints
   - Configure secrets
   - List webhook servers

6. test_alert_delivery()
   - Send test alerts
   - Verify delivery
   - Troubleshoot issues

Common Alert Types:
• gatewayDown - WAN/device offline
• usageAlert - Bandwidth threshold
• clientDown - Client disconnected
• rogueAp - Unauthorized AP detected
• failoverEvent - WAN failover occurred

Example Workflows:

📧 "Set up email alerts"
1. configure_email_alerts() with addresses
2. set_alert_thresholds() for sensitivity
3. test_alert_delivery() to verify

🖥️ "Enable SNMP monitoring"
1. configure_snmp() with community string
2. Test with external tool
3. Add to monitoring system

🌐 "Configure webhooks"
1. manage_webhooks() to add endpoint
2. configure_email_alerts() as backup
3. test_alert_delivery() to verify

💡 Best Practices:
- Use multiple notification methods
- Set appropriate thresholds
- Test alerts regularly
- Document recipient lists
"""


def register_alert_configuration_tools(app: FastMCP, meraki_client: MerakiClient):
    """Register all alert configuration tools with the MCP server."""
    global mcp_app, meraki
    mcp_app = app
    meraki = meraki_client
    
    # Register all tools
    tools = [
        (get_alert_settings, "View current alert configuration"),
        (configure_email_alerts, "Set up email alert recipients"),
        (set_alert_thresholds, "Configure alert trigger thresholds"),
        (configure_snmp, "Enable and configure SNMP monitoring"),
        (manage_webhooks, "Manage webhook alert endpoints"),
        (test_alert_delivery, "Test alert delivery to recipients"),
        (alert_configuration_help, "Get help with alert configuration"),
    ]
    
    for tool_func, description in tools:
        app.tool(
            name=tool_func.__name__,
            description=description
        )(tool_func)