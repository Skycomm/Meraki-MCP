"""
Filtered Alert and Webhook management tools - ONLY UNIQUE TOOLS (no SDK duplicates).
Contains 7 unique webhook management tools not available in SDK.
"""

# Global variables to store app and meraki client
app = None
meraki_client = None

def register_alerts_tools_filtered(mcp_app, meraki):
    """
    Register ONLY unique alert and webhook tools (7 tools).
    Excludes tools that duplicate SDK functionality.
    
    Args:
        mcp_app: MCP server instance
        meraki: Meraki client instance
    """
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    
    # Register only unique webhook management tools
    register_unique_webhook_tools()

def register_unique_webhook_tools():
    """Register unique webhook management tools (7 tools)."""
    
    @app.tool(
        name="get_organization_webhooks",
        description="📡 Get all webhooks for an organization"
    )
    def get_organization_webhooks(organization_id: str):
        """Get organization webhooks."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationWebhooks(organization_id)
            
            response = "# 📡 Organization Webhooks\\n\\n"
            
            if result and isinstance(result, list):
                response += f"**Total Webhooks**: {len(result)}\\n\\n"
                
                for idx, webhook in enumerate(result[:10], 1):
                    if isinstance(webhook, dict):
                        name = webhook.get('name', webhook.get('id', f'Webhook {idx}'))
                        response += f"**{idx}. {name}**\\n"
                        response += f"   - URL: {webhook.get('url', 'N/A')}\\n"
                        response += f"   - Status: {webhook.get('status', 'N/A')}\\n"
                        response += f"   - Network ID: {webhook.get('networkId', 'Organization-wide')}\\n"
                        if 'httpServer' in webhook:
                            response += f"   - HTTP Server: {webhook['httpServer'].get('name', 'N/A')}\\n"
                        response += "\\n"
                
                if len(result) > 10:
                    response += f"... and {len(result)-10} more webhooks\\n"
            else:
                response += "*No webhooks configured*\\n"
                
            return response
            
        except Exception as e:
            return f"❌ Error getting organization webhooks: {str(e)}"
    
    @app.tool(
        name="create_organization_webhook",
        description="➕ Create a new webhook for an organization"
    )
    def create_organization_webhook(organization_id: str, name: str, url: str, 
                                  shared_secret: str, network_id: str = None):
        """Create organization webhook."""
        try:
            webhook_data = {
                'name': name,
                'url': url,
                'sharedSecret': shared_secret
            }
            
            if network_id:
                webhook_data['networkId'] = network_id
            
            result = meraki_client.dashboard.organizations.createOrganizationWebhook(
                organization_id, **webhook_data
            )
            
            response = "# ➕ Created Organization Webhook\\n\\n"
            
            if result:
                response += f"**Webhook Created Successfully**\\n"
                response += f"- **Name**: {result.get('name')}\\n"
                response += f"- **URL**: {result.get('url')}\\n"
                response += f"- **ID**: {result.get('id')}\\n"
                response += f"- **Status**: {result.get('status', 'Active')}\\n"
                if result.get('networkId'):
                    response += f"- **Network ID**: {result.get('networkId')}\\n"
                else:
                    response += f"- **Scope**: Organization-wide\\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error creating webhook: {str(e)}"
    
    @app.tool(
        name="delete_organization_webhook",
        description="🗑️ Delete a specific organization webhook"
    )
    def delete_organization_webhook(organization_id: str, webhook_id: str, confirmed: bool = False):
        """Delete organization webhook."""
        if not confirmed:
            return "⚠️ This operation requires confirmed=true to execute"
            
        try:
            meraki_client.dashboard.organizations.deleteOrganizationWebhook(
                organization_id, webhook_id
            )
            
            return f"# 🗑️ Webhook Deleted\\n\\n✅ Successfully deleted webhook {webhook_id} from organization {organization_id}"
            
        except Exception as e:
            return f"❌ Error deleting webhook: {str(e)}"
    
    @app.tool(
        name="delete_all_organization_webhooks",
        description="🗑️ Delete ALL webhooks for an organization"
    )
    def delete_all_organization_webhooks(organization_id: str, confirmed: bool = False):
        """Delete all organization webhooks."""
        if not confirmed:
            return "⚠️ This operation requires confirmed=true to execute"
            
        try:
            # Get all webhooks first
            webhooks = meraki_client.dashboard.organizations.getOrganizationWebhooks(organization_id)
            
            if not webhooks:
                return f"# 🗑️ No Webhooks to Delete\\n\\n*Organization {organization_id} has no webhooks configured*"
            
            deleted_count = 0
            errors = []
            
            for webhook in webhooks:
                try:
                    meraki_client.dashboard.organizations.deleteOrganizationWebhook(
                        organization_id, webhook['id']
                    )
                    deleted_count += 1
                except Exception as e:
                    errors.append(f"Failed to delete {webhook.get('name', webhook['id'])}: {str(e)}")
            
            response = f"# 🗑️ Bulk Webhook Deletion\\n\\n"
            response += f"✅ Successfully deleted {deleted_count}/{len(webhooks)} webhooks\\n"
            
            if errors:
                response += f"\\n❌ **Errors encountered**:\\n"
                for error in errors[:5]:
                    response += f"- {error}\\n"
                if len(errors) > 5:
                    response += f"... and {len(errors)-5} more errors\\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in bulk webhook deletion: {str(e)}"
    
    @app.tool(
        name="get_network_webhook_http_servers",
        description="🌐 Get HTTP servers for network webhooks"
    )
    def get_network_webhook_http_servers(network_id: str):
        """Get network webhook HTTP servers."""
        try:
            result = meraki_client.dashboard.networks.getNetworkWebhooksHttpServers(network_id)
            
            response = "# 🌐 Network Webhook HTTP Servers\\n\\n"
            
            if result and isinstance(result, list):
                response += f"**Total HTTP Servers**: {len(result)}\\n\\n"
                
                for idx, server in enumerate(result, 1):
                    if isinstance(server, dict):
                        name = server.get('name', f'Server {idx}')
                        response += f"**{idx}. {name}**\\n"
                        response += f"   - URL: {server.get('url', 'N/A')}\\n"
                        response += f"   - ID: {server.get('id', 'N/A')}\\n"
                        if 'payloadTemplate' in server:
                            template = server['payloadTemplate']
                            response += f"   - Payload Template: {template.get('name', 'Custom')}\\n"
                        response += "\\n"
            else:
                response += "*No HTTP servers configured*\\n"
                
            return response
            
        except Exception as e:
            return f"❌ Error getting network webhook HTTP servers: {str(e)}"
    
    @app.tool(
        name="create_network_webhook_http_server",
        description="➕ Create HTTP server for network webhooks"
    )
    def create_network_webhook_http_server(network_id: str, name: str, url: str,
                                         shared_secret: str = None):
        """Create network webhook HTTP server."""
        try:
            server_data = {
                'name': name,
                'url': url
            }
            
            if shared_secret:
                server_data['sharedSecret'] = shared_secret
            
            result = meraki_client.dashboard.networks.createNetworkWebhooksHttpServer(
                network_id, **server_data
            )
            
            response = "# ➕ Created Network Webhook HTTP Server\\n\\n"
            
            if result:
                response += f"**HTTP Server Created Successfully**\\n"
                response += f"- **Name**: {result.get('name')}\\n"
                response += f"- **URL**: {result.get('url')}\\n"
                response += f"- **ID**: {result.get('id')}\\n"
                response += f"- **Network ID**: {network_id}\\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error creating HTTP server: {str(e)}"
    
    @app.tool(
        name="delete_network_webhook",
        description="🗑️ Delete a network webhook configuration"
    )
    def delete_network_webhook(network_id: str, http_server_id: str, confirmed: bool = False):
        """Delete network webhook HTTP server."""
        if not confirmed:
            return "⚠️ This operation requires confirmed=true to execute"
            
        try:
            meraki_client.dashboard.networks.deleteNetworkWebhooksHttpServer(
                network_id, http_server_id
            )
            
            return f"# 🗑️ Network Webhook Deleted\\n\\n✅ Successfully deleted HTTP server {http_server_id} from network {network_id}"
            
        except Exception as e:
            return f"❌ Error deleting network webhook: {str(e)}"