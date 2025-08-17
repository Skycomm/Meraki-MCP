"""
Alert and Webhook management tools for the Cisco Meraki MCP Server - ONLY REAL API METHODS.
"""

# Global variables to store app and meraki client
app = None
meraki_client = None

def register_alert_tools(mcp_app, meraki):
    """
    Register alert and webhook tools with the MCP server.
    
    Args:
        mcp_app: MCP server instance
        meraki: Meraki client instance
    """
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    
    # Register all alert tools
    register_alert_tool_handlers()

def register_alert_tool_handlers():
    """Register all alert and webhook tool handlers using ONLY REAL API methods."""
    
    @app.tool(
        name="get_organization_webhooks",
        description="🔔 Get all webhooks for an organization"
    )
    def get_organization_webhooks(org_id: str):
        """
        Get all webhooks configured for an organization.
        
        Args:
            org_id: Organization ID
            
        Returns:
            List of webhooks with their configurations
        """
        try:
            webhooks = meraki_client.get_organization_webhooks(org_id)
            
            if not webhooks:
                return f"No webhooks found for organization {org_id}."
                
            result = f"# 🔔 Webhooks for Organization {org_id}\n\n"
            
            for webhook in webhooks:
                result += f"## {webhook.get('name', 'Unnamed Webhook')}\n"
                result += f"- **URL**: {webhook.get('url', 'N/A')}\n"
                result += f"- **Shared Secret**: {'***' if webhook.get('sharedSecret') else 'Not set'}\n"
                result += f"- **Network ID**: {webhook.get('networkId', 'All Networks')}\n"
                
                # Alert types
                alert_types = webhook.get('alertTypeIds', [])
                if alert_types:
                    result += f"- **Alert Types**: {', '.join(alert_types)}\n"
                
                result += "\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving webhooks: {str(e)}"
    
    @app.tool(
        name="create_organization_webhook", 
        description="🔔 Create a new webhook for an organization"
    )
    def create_organization_webhook(org_id: str, name: str, url: str, shared_secret: str = None):
        """
        Create a new webhook HTTP server for an organization.
        
        Args:
            org_id: Organization ID
            name: Name of the webhook
            url: URL to send webhooks to
            shared_secret: Optional shared secret for security
            
        Returns:
            Created webhook details
        """
        try:
            webhook_data = {
                'name': name,
                'url': url
            }
            
            if shared_secret:
                webhook_data['sharedSecret'] = shared_secret
                
            webhook = meraki_client.create_organization_webhook(org_id, **webhook_data)
            
            result = f"# ✅ Webhook Created Successfully\n\n"
            result += f"- **Name**: {webhook.get('name')}\n"
            result += f"- **ID**: {webhook.get('id')}\n"
            result += f"- **URL**: {webhook.get('url')}\n"
            result += f"- **Shared Secret**: {'Set' if webhook.get('sharedSecret') else 'Not set'}\n"
            
            return result
            
        except Exception as e:
            return f"Error creating webhook: {str(e)}"
    
    @app.tool(
        name="get_network_webhook_http_servers",
        description="🌐 Get webhook HTTP servers for a network"
    )
    def get_network_webhook_http_servers(network_id: str):
        """
        Get webhook HTTP servers configured for a network.
        
        Args:
            network_id: Network ID
            
        Returns:
            List of webhook HTTP servers
        """
        try:
            servers = meraki_client.get_network_webhook_http_servers(network_id)
            
            if not servers:
                return f"No webhook HTTP servers found for network {network_id}."
                
            result = f"# 🌐 Webhook HTTP Servers for Network {network_id}\n\n"
            
            for server in servers:
                result += f"## {server.get('name', 'Unnamed Server')}\n"
                result += f"- **ID**: {server.get('id')}\n"
                result += f"- **URL**: {server.get('url', 'N/A')}\n"
                result += f"- **Shared Secret**: {'***' if server.get('sharedSecret') else 'Not set'}\n"
                
                payload_template = server.get('payloadTemplate')
                if payload_template:
                    result += f"- **Payload Template**: {payload_template.get('name', 'Custom')}\n"
                    
                result += "\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving webhook HTTP servers: {str(e)}"
    
    @app.tool(
        name="create_network_webhook_http_server",
        description="🌐 Create a webhook HTTP server for a network"
    )
    def create_network_webhook_http_server(network_id: str, name: str, url: str, shared_secret: str = None):
        """
        Create a webhook HTTP server for a network.
        
        Args:
            network_id: Network ID
            name: Name of the webhook server
            url: URL to send webhooks to
            shared_secret: Optional shared secret
            
        Returns:
            Created webhook server details
        """
        try:
            server_data = {
                'name': name,
                'url': url
            }
            
            if shared_secret:
                server_data['sharedSecret'] = shared_secret
                
            server = meraki_client.create_network_webhook_http_server(network_id, **server_data)
            
            result = f"# ✅ Webhook HTTP Server Created\n\n"
            result += f"- **Name**: {server.get('name')}\n"
            result += f"- **ID**: {server.get('id')}\n"
            result += f"- **URL**: {server.get('url')}\n"
            
            return result
            
        except Exception as e:
            return f"Error creating webhook HTTP server: {str(e)}"
    
    @app.tool(
        name="get_network_alerts_settings",
        description="⚠️ Get alert settings for a network"
    )
    def get_network_alerts_settings(network_id: str):
        """
        Get alert settings for a network.
        
        Args:
            network_id: Network ID
            
        Returns:
            Network alert settings
        """
        try:
            settings = meraki_client.get_network_alerts_settings(network_id)
            
            result = f"# ⚠️ Alert Settings for Network {network_id}\n\n"
            
            # Default destinations
            default_dest = settings.get('defaultDestinations', {})
            if default_dest:
                result += "## Default Alert Destinations\n"
                
                emails = default_dest.get('emails', [])
                if emails:
                    result += f"- **Emails**: {', '.join(emails)}\n"
                    
                webhooks = default_dest.get('httpServerIds', [])
                if webhooks:
                    result += f"- **Webhook Servers**: {len(webhooks)} configured\n"
                    
                if default_dest.get('allAdmins'):
                    result += "- **All Admins**: ✅ Enabled\n"
                    
                if default_dest.get('snmp'):
                    result += "- **SNMP**: ✅ Enabled\n"
                    
                result += "\n"
            
            # Alert type settings
            alerts = settings.get('alerts', [])
            if alerts:
                result += "## Alert Types Configuration\n"
                for alert in alerts:
                    alert_type = alert.get('type', 'Unknown')
                    enabled = alert.get('enabled', False)
                    result += f"### {alert_type}: {'✅ Enabled' if enabled else '❌ Disabled'}\n"
                    
                    filters = alert.get('filters', {})
                    if filters:
                        result += "  Filters:\n"
                        for key, value in filters.items():
                            result += f"  - {key}: {value}\n"
                            
                    alert_dest = alert.get('alertDestinations', {})
                    if alert_dest:
                        if alert_dest.get('emails'):
                            result += f"  - Emails: {', '.join(alert_dest['emails'])}\n"
                        if alert_dest.get('httpServerIds'):
                            result += f"  - Webhooks: {len(alert_dest['httpServerIds'])} servers\n"
                            
                    result += "\n"
                    
            return result
            
        except Exception as e:
            return f"Error retrieving alert settings: {str(e)}"
    
    @app.tool(
        name="update_network_alerts_settings",
        description="⚠️ Update alert settings for a network"
    )
    def update_network_alerts_settings(network_id: str, emails: str = None, all_admins: bool = None):
        """
        Update alert settings for a network.
        
        Args:
            network_id: Network ID
            emails: Comma-separated email addresses for alerts
            all_admins: Send alerts to all admins
            
        Returns:
            Updated alert settings
        """
        try:
            update_data = {}
            
            if emails is not None or all_admins is not None:
                default_dest = {}
                
                if emails:
                    default_dest['emails'] = [e.strip() for e in emails.split(',')]
                    
                if all_admins is not None:
                    default_dest['allAdmins'] = all_admins
                    
                update_data['defaultDestinations'] = default_dest
                
            settings = meraki_client.update_network_alerts_settings(network_id, **update_data)
            
            return "✅ Alert settings updated successfully!"
            
        except Exception as e:
            return f"Error updating alert settings: {str(e)}"