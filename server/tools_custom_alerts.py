"""
Alert and Webhook management tools for the Cisco Meraki MCP Server - ONLY REAL API METHODS.
"""

# Global variables to store app and meraki client
app = None
meraki_client = None

def register_alert_tools(mcp_app, meraki):
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    """
    Register alert and webhook tools with the MCP server.
    
    Args:
        mcp_app: MCP server instance
        meraki: Meraki client instance
    """
    
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
            result += f"**Total Webhooks**: {len(webhooks)}\n\n"
            
            for i, webhook in enumerate(webhooks, 1):
                result += f"## {i}. {webhook.get('name', 'Unnamed Webhook')}\n"
                result += f"- **ID**: `{webhook.get('id', 'N/A')}`\n"
                result += f"- **URL**: {webhook.get('url', 'N/A')}\n"
                result += f"- **Shared Secret**: {'***' if webhook.get('sharedSecret') else 'Not set'}\n"
                
                # Payload template
                template = webhook.get('payloadTemplate')
                if template:
                    result += f"- **Payload Template**: {template.get('name', 'Default')}\n"
                
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
        name="delete_organization_webhook",
        description="🗑️ Delete a webhook from an organization"
    )
    def delete_organization_webhook(org_id: str, webhook_id: str, network_id: str = None):
        """
        Delete a webhook HTTP server from an organization.
        
        Args:
            org_id: Organization ID
            webhook_id: Webhook HTTP server ID
            network_id: Network ID (optional - if known, makes deletion faster)
            
        Returns:
            Success or error message
        """
        try:
            meraki_client.delete_organization_webhook(org_id, webhook_id, network_id)
            if network_id:
                return f"✅ Successfully deleted webhook {webhook_id} from network {network_id}"
            else:
                return f"✅ Successfully deleted webhook {webhook_id} from organization {org_id}"
            
        except Exception as e:
            return f"❌ Error deleting webhook: {str(e)}"
    
    @app.tool(
        name="delete_network_webhook",
        description="🗑️ Delete a webhook HTTP server from a network"
    )
    def delete_network_webhook(network_id: str, webhook_id: str):
        """
        Delete a webhook HTTP server from a network.
        
        Args:
            network_id: Network ID
            webhook_id: Webhook HTTP server ID
            
        Returns:
            Success or error message
        """
        try:
            meraki_client.delete_network_webhook(network_id, webhook_id)
            return f"✅ Successfully deleted webhook {webhook_id} from network {network_id}"
            
        except Exception as e:
            return f"❌ Error deleting webhook: {str(e)}"
    
    @app.tool(
        name="delete_all_organization_webhooks",
        description="🗑️ Delete ALL webhooks from an organization (use with caution!)"
    )
    def delete_all_organization_webhooks(org_id: str, confirm: bool = False):
        """
        Delete all webhook HTTP servers from an organization.
        
        Args:
            org_id: Organization ID
            confirm: Must be True to proceed (safety check)
            
        Returns:
            Summary of deleted webhooks
        """
        if not confirm:
            return "❌ Safety check: Set confirm=True to delete all webhooks"
            
        try:
            # Get all webhooks
            webhooks = meraki_client.get_organization_webhooks(org_id)
            
            if not webhooks:
                return f"No webhooks found for organization {org_id}"
            
            result = f"# 🗑️ Deleting All Webhooks from Organization {org_id}\n\n"
            result += f"**Total webhooks to delete**: {len(webhooks)}\n\n"
            
            deleted = 0
            failed = 0
            
            for webhook in webhooks:
                webhook_id = webhook.get('id')
                webhook_name = webhook.get('name', 'Unnamed')
                
                if not webhook_id:
                    result += f"⚠️ Skipped {webhook_name} - No ID found\n"
                    failed += 1
                    continue
                    
                try:
                    # Pass network_id if available
                    network_id = webhook.get('networkId')
                    meraki_client.delete_organization_webhook(org_id, webhook_id, network_id)
                    result += f"✅ Deleted: {webhook_name} (ID: {webhook_id}) from network {webhook.get('networkName', 'Unknown')}\n"
                    deleted += 1
                except Exception as e:
                    result += f"❌ Failed to delete {webhook_name}: {str(e)}\n"
                    failed += 1
            
            result += f"\n## Summary\n"
            result += f"- **Deleted**: {deleted} webhooks\n"
            result += f"- **Failed**: {failed} webhooks\n"
            
            return result
            
        except Exception as e:
            return f"❌ Error deleting webhooks: {str(e)}"
    
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
                            if key == 'timeout':
                                result += f"  - {key}: {value} seconds\n"
                            else:
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
    def update_network_alerts_settings(network_id: str, emails: str = None, all_admins: bool = None, 
                                     enable_device_down: bool = None, enable_gateway_down: bool = None,
                                     enable_dhcp_failure: bool = None, enable_high_usage: bool = None,
                                     enable_ip_conflict: bool = None, enable_security_events: bool = None,
                                     enable_rogue_ap: bool = None, enable_client_connectivity: bool = None):
        """
        Update alert settings for a network.
        
        Args:
            network_id: Network ID
            emails: Comma-separated email addresses for alerts
            all_admins: Send alerts to all admins
            enable_device_down: Enable device down alerts (MX, camera, switch, AP)
            enable_gateway_down: Enable gateway connectivity alerts (VPN, uplink)
            enable_dhcp_failure: Enable DHCP failure alerts
            enable_high_usage: Enable high wireless usage alerts
            enable_ip_conflict: Enable IP conflict detection alerts
            enable_security_events: Enable security event alerts (IDS/IPS, malware)
            enable_rogue_ap: Enable rogue access point detection alerts
            enable_client_connectivity: Enable client connectivity failure alerts
            
        Returns:
            Updated alert settings
        """
        try:
            update_data = {}
            
            # Set default destinations
            if emails is not None or all_admins is not None:
                default_dest = {}
                
                if emails:
                    default_dest['emails'] = [e.strip() for e in emails.split(',')]
                    
                if all_admins is not None:
                    default_dest['allAdmins'] = all_admins
                    
                update_data['defaultDestinations'] = default_dest
            
            # Configure specific alerts
            alerts = []
            
            # Device down alerts
            if enable_device_down is not None:
                # MX/Security appliance down
                alerts.append({
                    'type': 'applianceDown',
                    'enabled': enable_device_down,
                    'alertDestinations': {
                        'allAdmins': True
                    }
                })
                # Camera down
                alerts.append({
                    'type': 'cameraDown',
                    'enabled': enable_device_down,
                    'alertDestinations': {
                        'allAdmins': True
                    }
                })
                # Gateway down (for gateway devices)
                alerts.append({
                    'type': 'gatewayDown',
                    'enabled': enable_device_down,
                    'alertDestinations': {
                        'allAdmins': True
                    }
                })
                # Repeater down
                alerts.append({
                    'type': 'repeaterDown',
                    'enabled': enable_device_down,
                    'alertDestinations': {
                        'allAdmins': True
                    }
                })
                # Cellular backup up/down
                alerts.append({
                    'type': 'cellularUpDown',
                    'enabled': enable_device_down,
                    'alertDestinations': {
                        'allAdmins': True
                    }
                })
                # Node hardware failure (covers switches and APs)
                alerts.append({
                    'type': 'nodeHardwareFailure',
                    'enabled': enable_device_down,
                    'alertDestinations': {
                        'allAdmins': True
                    }
                })
            
            # Gateway connectivity issues
            if enable_gateway_down is not None:
                alerts.append({
                    'type': 'vpnConnectivityChange',
                    'enabled': enable_gateway_down,
                    'alertDestinations': {
                        'allAdmins': True
                    }
                })
                alerts.append({
                    'type': 'failoverEvent',
                    'enabled': enable_gateway_down,
                    'alertDestinations': {
                        'allAdmins': True
                    }
                })
            
            # DHCP failures
            if enable_dhcp_failure is not None:
                alerts.append({
                    'type': 'dhcpNoLeases',
                    'enabled': enable_dhcp_failure,
                    'alertDestinations': {
                        'allAdmins': True
                    }
                })
                alerts.append({
                    'type': 'rogueDhcp',
                    'enabled': enable_dhcp_failure,
                    'alertDestinations': {
                        'allAdmins': True
                    }
                })
            
            # High wireless usage
            if enable_high_usage is not None:
                alerts.append({
                    'type': 'usageAlert',
                    'enabled': enable_high_usage,
                    'alertDestinations': {
                        'allAdmins': True
                    }
                })
            
            # IP conflict detection
            if enable_ip_conflict is not None:
                alerts.append({
                    'type': 'ipConflict',
                    'enabled': enable_ip_conflict,
                    'alertDestinations': {
                        'allAdmins': True
                    }
                })
            
            # Security events (IDS/IPS, malware)
            if enable_security_events is not None:
                # AMP malware detected
                alerts.append({
                    'type': 'ampMalwareDetected',
                    'enabled': enable_security_events,
                    'alertDestinations': {
                        'allAdmins': True
                    }
                })
                # AMP malware blocked
                alerts.append({
                    'type': 'ampMalwareBlocked',
                    'enabled': enable_security_events,
                    'alertDestinations': {
                        'allAdmins': True
                    }
                })
            
            # Rogue AP detection
            if enable_rogue_ap is not None:
                alerts.append({
                    'type': 'rogueAp',
                    'enabled': enable_rogue_ap,
                    'alertDestinations': {
                        'allAdmins': True
                    }
                })
            
            # Client connectivity failures
            if enable_client_connectivity is not None:
                alerts.append({
                    'type': 'clientConnectivity',
                    'enabled': enable_client_connectivity,
                    'alertDestinations': {
                        'allAdmins': True
                    }
                })
            
            if alerts:
                update_data['alerts'] = alerts
                
            settings = meraki_client.update_network_alerts_settings(network_id, **update_data)
            
            result = "✅ Alert settings updated successfully!\n\n"
            result += "Enabled alerts:\n"
            if enable_device_down:
                result += "- Device down alerts (MX/appliance, camera, gateway, repeater, cellular, hardware failures)\n"
            if enable_gateway_down:
                result += "- Gateway connectivity issues (VPN changes, failover events)\n"
            if enable_dhcp_failure:
                result += "- DHCP issues (no leases available, rogue DHCP servers)\n"
            if enable_high_usage:
                result += "- High wireless usage alerts\n"
            if enable_ip_conflict:
                result += "- IP conflict detection\n"
            if enable_security_events:
                result += "- Security events (malware detected/blocked)\n"
            if enable_rogue_ap:
                result += "- Rogue access point detection\n"
            if enable_client_connectivity:
                result += "- Client connectivity monitoring\n"
            
            return result
            
        except Exception as e:
            return f"Error updating alert settings: {str(e)}"