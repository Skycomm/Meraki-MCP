"""
Webhook Management Tools for Cisco Meraki MCP Server
Configure webhooks, manage payload templates, and monitor webhook delivery
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


def get_organization_webhooks_alert_types(org_id: str) -> str:
    """
    🚨 Get available webhook alert types.
    
    Lists all alert types that can trigger webhooks in the organization.
    
    Args:
        org_id: Organization ID
    
    Returns:
        List of available alert types with descriptions
    """
    try:
        with safe_api_call("get webhook alert types"):
            alert_types = meraki.dashboard.organizations.getOrganizationWebhooksAlertTypes(org_id)
            
            output = ["🚨 Webhook Alert Types", "=" * 50, ""]
            
            if not alert_types:
                output.append("No alert types available")
                return "\n".join(output)
            
            # Group alert types by category
            by_category = {}
            for alert in alert_types:
                # Try to categorize based on alert type name
                alert_type = alert.get('alertType', 'Unknown')
                
                # Determine category
                if any(x in alert_type.lower() for x in ['appliance', 'mx', 'firewall', 'vpn']):
                    category = 'Appliance/Security'
                elif any(x in alert_type.lower() for x in ['switch', 'port', 'stp']):
                    category = 'Switching'
                elif any(x in alert_type.lower() for x in ['wireless', 'ap', 'ssid', 'client']):
                    category = 'Wireless'
                elif any(x in alert_type.lower() for x in ['camera', 'mv', 'motion']):
                    category = 'Camera'
                elif any(x in alert_type.lower() for x in ['sensor', 'temperature', 'humidity']):
                    category = 'Sensors'
                else:
                    category = 'Other'
                
                if category not in by_category:
                    by_category[category] = []
                by_category[category].append(alert)
            
            # Show summary
            output.append(f"Total Alert Types: {len(alert_types)}")
            output.append("")
            
            # Show by category
            for category, alerts in sorted(by_category.items()):
                output.append(f"📂 {category} ({len(alerts)} alerts):")
                
                for alert in sorted(alerts, key=lambda x: x.get('alertType', '')):
                    alert_type = alert.get('alertType', 'Unknown')
                    
                    # Get appropriate icon
                    if 'down' in alert_type.lower() or 'fail' in alert_type.lower():
                        icon = '🔴'
                    elif 'up' in alert_type.lower() or 'online' in alert_type.lower():
                        icon = '🟢'
                    elif 'motion' in alert_type.lower():
                        icon = '🏃'
                    elif 'temperature' in alert_type.lower():
                        icon = '🌡️'
                    else:
                        icon = '📍'
                    
                    output.append(f"   {icon} {alert_type}")
                    
                    # Show example if available
                    if alert.get('example'):
                        output.append(f"      Example: {json.dumps(alert['example'], indent=10)[:100]}...")
                
                output.append("")
            
            # Popular alert types
            output.append("💡 Popular Alert Types:")
            output.append("• Device down/up notifications")
            output.append("• Security events and threats")
            output.append("• Environmental sensor alerts")
            output.append("• Client connectivity issues")
            output.append("• Configuration changes")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("get webhook alert types", e)


def get_organization_webhooks_logs(
    org_id: str,
    t0: Optional[str] = None,
    t1: Optional[str] = None,
    timespan: Optional[int] = 3600,
    per_page: Optional[int] = None,
    url: Optional[str] = None
) -> str:
    """
    📋 Get webhook delivery logs.
    
    Shows the history of webhook POST attempts with status and response info.
    
    Args:
        org_id: Organization ID
        t0: Start time (ISO 8601)
        t1: End time (ISO 8601)
        timespan: Time period in seconds (default: 3600 = 1 hour)
        per_page: Number of entries per page
        url: Filter by webhook URL
    
    Returns:
        Webhook delivery log with status information
    """
    try:
        with safe_api_call("get webhook logs"):
            # Build parameters
            params = {}
            if t0:
                params['t0'] = t0
            if t1:
                params['t1'] = t1
            elif timespan:
                params['timespan'] = timespan
            if per_page:
                params['perPage'] = per_page
            if url:
                params['url'] = url
            
            logs = meraki.dashboard.organizations.getOrganizationWebhooksLogs(
                org_id,
                **params
            )
            
            output = ["📋 Webhook Delivery Logs", "=" * 50, ""]
            output.append(f"Time Period: Last {timespan // 60} minutes")
            
            if not logs:
                output.append("\nNo webhook deliveries in this time period")
                return "\n".join(output)
            
            # Calculate statistics
            total = len(logs)
            successful = sum(1 for log in logs if 200 <= log.get('responseCode', 0) < 300)
            failed = total - successful
            success_rate = (successful / total * 100) if total > 0 else 0
            
            output.append(f"\n📊 Delivery Statistics:")
            output.append(f"   Total Attempts: {total}")
            output.append(f"   ✅ Successful: {successful}")
            output.append(f"   ❌ Failed: {failed}")
            output.append(f"   Success Rate: {success_rate:.1f}%")
            output.append("")
            
            # Group by URL
            by_url = {}
            for log in logs:
                log_url = log.get('url', 'Unknown')
                if log_url not in by_url:
                    by_url[log_url] = []
                by_url[log_url].append(log)
            
            # Show logs by URL
            for webhook_url, url_logs in by_url.items():
                output.append(f"🔗 Webhook: {webhook_url}")
                output.append(f"   Deliveries: {len(url_logs)}")
                
                # Show recent deliveries
                for log in url_logs[:5]:  # Show last 5
                    alert_type = log.get('alertType', 'Unknown')
                    response_code = log.get('responseCode', 0)
                    response_duration = log.get('responseDuration', 0)
                    sent_at = log.get('sentAt', 'Unknown')
                    
                    # Status icon
                    if 200 <= response_code < 300:
                        status = '✅'
                    elif response_code == 0:
                        status = '⏳'
                    else:
                        status = '❌'
                    
                    output.append(f"\n   {status} {alert_type}")
                    output.append(f"      Response: {response_code} ({response_duration}ms)")
                    output.append(f"      Sent: {sent_at}")
                    
                    if log.get('networkId'):
                        output.append(f"      Network: {log['networkId']}")
                
                if len(url_logs) > 5:
                    output.append(f"\n   ... and {len(url_logs) - 5} more deliveries")
                
                output.append("")
            
            # Error analysis
            errors = [log for log in logs if log.get('responseCode', 0) >= 400 or log.get('responseCode', 0) == 0]
            if errors:
                output.append("⚠️ Error Analysis:")
                error_codes = {}
                for error in errors:
                    code = error.get('responseCode', 0)
                    error_codes[code] = error_codes.get(code, 0) + 1
                
                for code, count in sorted(error_codes.items()):
                    if code == 0:
                        output.append(f"   Timeout/No Response: {count}")
                    else:
                        output.append(f"   HTTP {code}: {count}")
            
            # Performance analysis
            if logs:
                durations = [log.get('responseDuration', 0) for log in logs if log.get('responseDuration')]
                if durations:
                    avg_duration = sum(durations) / len(durations)
                    max_duration = max(durations)
                    output.append(f"\n⏱️ Performance:")
                    output.append(f"   Average Response: {avg_duration:.0f}ms")
                    output.append(f"   Slowest Response: {max_duration:.0f}ms")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("get webhook logs", e)


def get_organization_webhooks_http_servers(org_id: str) -> str:
    """
    🌐 Get configured webhook HTTP servers.
    
    Lists all webhook receivers configured for the organization.
    
    Args:
        org_id: Organization ID
    
    Returns:
        List of webhook HTTP servers with configuration
    """
    try:
        with safe_api_call("get webhook HTTP servers"):
            servers = meraki.dashboard.organizations.getOrganizationWebhooksHttpServers(org_id)
            
            output = ["🌐 Webhook HTTP Servers", "=" * 50, ""]
            
            if not servers:
                output.append("No webhook servers configured")
                output.append("\n💡 Use create_organization_webhooks_http_server() to add one")
                return "\n".join(output)
            
            output.append(f"Total Servers: {len(servers)}")
            output.append("")
            
            # Show each server
            for i, server in enumerate(servers, 1):
                server_id = server.get('id', 'Unknown')
                name = server.get('name', 'Unnamed Server')
                url = server.get('url', 'No URL')
                
                output.append(f"{i}. 🖥️ {name}")
                output.append(f"   ID: {server_id}")
                output.append(f"   URL: {url}")
                
                # Shared secret status
                if server.get('sharedSecret'):
                    output.append("   🔐 Shared Secret: Configured")
                else:
                    output.append("   ⚠️ Shared Secret: Not set")
                
                # Payload template
                if server.get('payloadTemplate'):
                    template = server['payloadTemplate']
                    template_name = template.get('name', 'Custom')
                    output.append(f"   📄 Template: {template_name}")
                
                # Network alerts
                network_ids = server.get('networkIds', [])
                if network_ids:
                    output.append(f"   📡 Networks: {len(network_ids)}")
                else:
                    output.append("   📡 Networks: All")
                
                output.append("")
            
            # Security reminder
            output.append("🔒 Security Requirements:")
            output.append("• HTTPS with valid SSL certificate required")
            output.append("• Self-signed certificates not supported")
            output.append("• Use shared secret for verification")
            output.append("• Implement request validation")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("get webhook HTTP servers", e)


def create_organization_webhooks_http_server(
    org_id: str,
    name: str,
    url: str,
    shared_secret: Optional[str] = None,
    payload_template_id: Optional[str] = None,
    payload_template_name: Optional[str] = None,
    network_ids: Optional[List[str]] = None
) -> str:
    """
    ➕ Create a webhook HTTP server.
    
    Configures a new webhook receiver endpoint.
    
    Args:
        org_id: Organization ID
        name: Server name
        url: HTTPS webhook URL
        shared_secret: Secret for request verification
        payload_template_id: ID of custom payload template
        payload_template_name: Name of payload template
        network_ids: Specific networks to monitor (None = all)
    
    Returns:
        Created webhook server details
    """
    try:
        with safe_api_call("create webhook HTTP server"):
            # Build request
            server_data = {
                "name": name,
                "url": url
            }
            
            if shared_secret:
                server_data["sharedSecret"] = shared_secret
            
            if payload_template_id or payload_template_name:
                server_data["payloadTemplate"] = {}
                if payload_template_id:
                    server_data["payloadTemplate"]["payloadTemplateId"] = payload_template_id
                if payload_template_name:
                    server_data["payloadTemplate"]["name"] = payload_template_name
            
            if network_ids:
                server_data["networkIds"] = network_ids
            
            # Create the server
            server = meraki.dashboard.organizations.createOrganizationWebhooksHttpServer(
                org_id,
                **server_data
            )
            
            output = ["✅ Webhook Server Created", "=" * 50, ""]
            output.append(f"Name: {server.get('name', name)}")
            output.append(f"ID: {server.get('id', 'N/A')}")
            output.append(f"URL: {server.get('url', url)}")
            
            if server.get('sharedSecret'):
                output.append("🔐 Shared Secret: Set")
            
            if server.get('payloadTemplate'):
                output.append(f"📄 Template: {server['payloadTemplate'].get('name', 'Custom')}")
            
            output.append("\n🚀 Next Steps:")
            output.append("1. Configure alert settings in Dashboard")
            output.append("2. Test webhook delivery")
            output.append("3. Monitor webhook logs")
            output.append("4. Implement error handling")
            
            output.append("\n💡 Testing Tips:")
            output.append("• Use test_organization_webhooks_webhook_test()")
            output.append("• Check logs with get_organization_webhooks_logs()")
            output.append("• Verify SSL certificate is valid")
            output.append("• Ensure endpoint responds quickly (<5s)")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("create webhook HTTP server", e)


def test_organization_webhooks_webhook_test(
    org_id: str,
    url: str,
    shared_secret: Optional[str] = None,
    payload_template_id: Optional[str] = None,
    payload_template_name: Optional[str] = None
) -> str:
    """
    🧪 Test webhook delivery.
    
    Sends a test webhook to verify endpoint configuration.
    
    Args:
        org_id: Organization ID
        url: Webhook URL to test
        shared_secret: Secret for verification
        payload_template_id: Custom template ID
        payload_template_name: Template name
    
    Returns:
        Test results with response details
    """
    try:
        with safe_api_call("test webhook"):
            # Build test request
            test_data = {
                "url": url
            }
            
            if shared_secret:
                test_data["sharedSecret"] = shared_secret
            
            if payload_template_id or payload_template_name:
                test_data["payloadTemplate"] = {}
                if payload_template_id:
                    test_data["payloadTemplate"]["payloadTemplateId"] = payload_template_id
                if payload_template_name:
                    test_data["payloadTemplate"]["name"] = payload_template_name
            
            # Create the test
            test = meraki.dashboard.organizations.createOrganizationWebhooksWebhookTest(
                org_id,
                **test_data
            )
            
            test_id = test.get('id', 'Unknown')
            
            output = ["🧪 Webhook Test Created", "=" * 50, ""]
            output.append(f"Test ID: {test_id}")
            output.append(f"URL: {url}")
            output.append("")
            
            # Check test status
            output.append("⏳ Test Status: Created")
            output.append("")
            output.append("To check results:")
            output.append(f"1. Use get_organization_webhooks_webhook_test('{org_id}', '{test_id}')")
            output.append("2. Check webhook logs for delivery status")
            output.append("3. Verify your endpoint received the test")
            
            output.append("\n📋 Test Webhook Payload:")
            output.append("• Alert Type: 'Test webhook'")
            output.append("• Organization info included")
            output.append("• Timestamp of test")
            output.append("• Shared secret (if configured)")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("test webhook", e)


def get_organization_webhooks_webhook_test(
    org_id: str,
    webhook_test_id: str
) -> str:
    """
    🔍 Get webhook test status.
    
    Checks the results of a webhook test.
    
    Args:
        org_id: Organization ID
        webhook_test_id: Test ID from create test
    
    Returns:
        Test results and delivery status
    """
    try:
        with safe_api_call("get webhook test status"):
            test = meraki.dashboard.organizations.getOrganizationWebhooksWebhookTest(
                org_id,
                webhook_test_id
            )
            
            output = ["🔍 Webhook Test Results", "=" * 50, ""]
            output.append(f"Test ID: {webhook_test_id}")
            output.append("")
            
            # Test details
            output.append(f"URL: {test.get('url', 'Unknown')}")
            
            # Status
            status = test.get('status', 'Unknown')
            if status == 'completed':
                output.append("✅ Status: Completed")
            elif status == 'pending':
                output.append("⏳ Status: Pending")
            else:
                output.append(f"📊 Status: {status}")
            
            # Results
            if test.get('result'):
                result = test['result']
                response_code = result.get('responseCode', 0)
                response_duration = result.get('responseDuration', 0)
                
                output.append("\n📋 Delivery Results:")
                
                if 200 <= response_code < 300:
                    output.append(f"   ✅ Success: HTTP {response_code}")
                else:
                    output.append(f"   ❌ Failed: HTTP {response_code}")
                
                output.append(f"   Response Time: {response_duration}ms")
                
                # Response body preview
                if result.get('responseBody'):
                    body = result['responseBody']
                    output.append(f"   Response: {body[:100]}...")
            
            # Recommendations based on results
            if test.get('result'):
                response_code = test['result'].get('responseCode', 0)
                
                output.append("\n💡 Analysis:")
                if response_code == 0:
                    output.append("• No response - check URL accessibility")
                    output.append("• Verify SSL certificate is valid")
                    output.append("• Check firewall rules")
                elif response_code >= 500:
                    output.append("• Server error - check endpoint logs")
                    output.append("• Verify webhook handler code")
                elif response_code >= 400:
                    output.append("• Client error - check request format")
                    output.append("• Verify authentication if used")
                elif 200 <= response_code < 300:
                    output.append("• Webhook working correctly!")
                    output.append("• Ready for production use")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("get webhook test status", e)


def get_organization_webhooks_payload_templates(org_id: str) -> str:
    """
    📄 Get webhook payload templates.
    
    Lists custom payload templates for webhook formatting.
    
    Args:
        org_id: Organization ID
    
    Returns:
        List of available payload templates
    """
    try:
        with safe_api_call("get payload templates"):
            templates = meraki.dashboard.organizations.getOrganizationWebhooksPayloadTemplates(org_id)
            
            output = ["📄 Webhook Payload Templates", "=" * 50, ""]
            
            if not templates:
                output.append("No custom templates configured")
                output.append("\n💡 Use create_organization_webhooks_payload_template() to add one")
                return "\n".join(output)
            
            output.append(f"Total Templates: {len(templates)}")
            output.append("")
            
            # Show each template
            for i, template in enumerate(templates, 1):
                template_id = template.get('payloadTemplateId', 'Unknown')
                name = template.get('name', 'Unnamed Template')
                template_type = template.get('type', 'custom')
                
                output.append(f"{i}. 📝 {name}")
                output.append(f"   ID: {template_id}")
                output.append(f"   Type: {template_type}")
                
                # Sharing status
                if template.get('sharing'):
                    sharing = template['sharing']
                    if sharing.get('byNetwork'):
                        output.append(f"   Shared with: {len(sharing['byNetwork'])} networks")
                
                # Headers if defined
                if template.get('headers'):
                    output.append(f"   Headers: {len(template['headers'])} custom headers")
                
                # Body preview
                if template.get('body'):
                    body = template['body']
                    if isinstance(body, str):
                        preview = body.replace('\n', ' ')[:100]
                        output.append(f"   Body: {preview}...")
                
                output.append("")
            
            # Template tips
            output.append("💡 Template Features:")
            output.append("• Liquid template syntax")
            output.append("• Access to all alert variables")
            output.append("• Custom headers support")
            output.append("• JSON output format")
            output.append("• Direct API integration")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("get payload templates", e)


def webhook_template_examples() -> str:
    """
    📚 Show webhook template examples.
    
    Provides example Liquid templates for common integrations.
    
    Returns:
        Example webhook templates
    """
    output = ["📚 Webhook Template Examples", "=" * 50, ""]
    
    output.append("1️⃣ Slack Integration:")
    output.append("""
{
  "text": "Meraki Alert: {{alertType}}",
  "attachments": [{
    "color": "{% if alertLevel == 'critical' %}danger{% else %}warning{% endif %}",
    "fields": [
      {"title": "Network", "value": "{{networkName}}", "short": true},
      {"title": "Device", "value": "{{deviceName}}", "short": true},
      {"title": "Time", "value": "{{occurredAt}}", "short": false}
    ]
  }]
}
""")
    
    output.append("\n2️⃣ Microsoft Teams:")
    output.append("""
{
  "@type": "MessageCard",
  "@context": "https://schema.org/extensions",
  "summary": "{{alertType}}",
  "sections": [{
    "activityTitle": "Meraki Alert",
    "activitySubtitle": "{{networkName}}",
    "facts": [
      {"name": "Alert", "value": "{{alertType}}"},
      {"name": "Device", "value": "{{deviceSerial}}"},
      {"name": "Time", "value": "{{occurredAt}}"}
    ]
  }]
}
""")
    
    output.append("\n3️⃣ Generic JSON:")
    output.append("""
{
  "alert": {
    "type": "{{alertType}}",
    "level": "{{alertLevel}}",
    "network": {
      "id": "{{networkId}}",
      "name": "{{networkName}}"
    },
    "device": {
      "serial": "{{deviceSerial}}",
      "name": "{{deviceName}}",
      "model": "{{deviceModel}}"
    },
    "timestamp": "{{occurredAt}}",
    "details": {{alertData | json}}
  }
}
""")
    
    output.append("\n4️⃣ Custom Headers Example:")
    output.append("""
Headers:
  X-Meraki-Alert-Type: {{alertType}}
  X-Meraki-Network: {{networkId}}
  Authorization: Bearer {{sharedSecret}}

Body:
{
  "event": "meraki.{{alertType | downcase | replace: ' ', '_'}}",
  "data": {{alertData | json}}
}
""")
    
    output.append("\n💡 Liquid Template Tips:")
    output.append("• Use {{variable}} for values")
    output.append("• Conditionals: {% if condition %}")
    output.append("• Filters: {{value | json}}")
    output.append("• Loops: {% for item in array %}")
    output.append("• Default values: {{var | default: 'N/A'}}")
    
    output.append("\n📋 Common Variables:")
    output.append("• alertType - Type of alert")
    output.append("• alertLevel - Severity level")
    output.append("• networkName/networkId - Network info")
    output.append("• deviceName/deviceSerial - Device info")
    output.append("• occurredAt - Timestamp")
    output.append("• alertData - Full alert payload")
    
    return "\n".join(output)


def webhooks_help() -> str:
    """
    ❓ Get help with webhook management tools.
    
    Shows available tools and best practices.
    
    Returns:
        Formatted help guide
    """
    return """🔔 Webhook Management Tools Help
==================================================

Available tools for webhook configuration:

1. get_organization_webhooks_alert_types()
   - List available alert types
   - Grouped by category
   - Shows example payloads
   - Plan webhook strategy

2. get_organization_webhooks_logs()
   - View delivery history
   - Check success rates
   - Debug failures
   - Performance metrics

3. get_organization_webhooks_http_servers()
   - List webhook receivers
   - View configurations
   - Check templates
   - Security settings

4. create_organization_webhooks_http_server()
   - Add webhook endpoint
   - Configure security
   - Set custom templates
   - Network filtering

5. test_organization_webhooks_webhook_test()
   - Test webhook delivery
   - Verify SSL/TLS
   - Check response times
   - Validate endpoint

6. get_organization_webhooks_webhook_test()
   - Check test results
   - View response codes
   - Debug issues
   - Performance data

7. get_organization_webhooks_payload_templates()
   - List custom templates
   - Liquid syntax support
   - Integration ready
   - Reusable formats

8. webhook_template_examples()
   - Slack templates
   - Teams templates
   - Generic JSON
   - Custom headers

Security Requirements:
🔒 HTTPS with valid certificate
🔐 Shared secret for verification
⏱️ <5 second response time
📋 Request validation

Common Alert Types:
• Device up/down
• Security events
• Environmental alerts
• Client issues
• Config changes
• Performance alerts

Best Practices:
• Use shared secrets
• Implement retries
• Log all webhooks
• Monitor delivery
• Handle duplicates
• Validate payloads

Integration Tips:
• Start with test webhooks
• Use templates for consistency
• Monitor success rates
• Implement error handling
• Document webhook flows
• Regular endpoint health checks

Troubleshooting:
• Check SSL certificate
• Verify firewall rules
• Monitor response times
• Check webhook logs
• Test with curl
• Validate JSON format
"""


def register_webhooks_tools(app: FastMCP, meraki_client: MerakiClient):
    """Register all webhook management tools with the MCP server."""
    global mcp_app, meraki
    mcp_app = app
    meraki = meraki_client
    
    # Register all tools
    tools = [
        (get_organization_webhooks_alert_types, "Get available webhook alert types"),
        (get_organization_webhooks_logs, "View webhook delivery logs"),
        (get_organization_webhooks_http_servers, "List webhook HTTP servers"),
        (create_organization_webhooks_http_server, "Create webhook HTTP server"),
        (test_organization_webhooks_webhook_test, "Test webhook delivery"),
        (get_organization_webhooks_webhook_test, "Get webhook test results"),
        (get_organization_webhooks_payload_templates, "List payload templates"),
        (webhook_template_examples, "Show webhook template examples"),
        (webhooks_help, "Get help with webhooks"),
    ]
    
    for tool_func, description in tools:
        app.tool(
            name=tool_func.__name__,
            description=description
        )(tool_func)