"""
Additional Insight endpoints for Cisco Meraki MCP Server.
Auto-generated to achieve 100% API coverage.
"""

# Global variables to store app and meraki client
app = None
meraki_client = None

def format_dict_response(data: dict, resource_name: str) -> str:
    """Format dictionary response."""
    result = f"# {resource_name}\n\n"
    for key, value in data.items():
        if value is not None:
            result += f"**{key}**: {value}\n"
    return result

def format_list_response(data: list, resource_name: str) -> str:
    """Format list response."""
    if not data:
        return f"No {resource_name.lower()} found."
    
    result = f"# {resource_name}\n\n"
    result += f"**Total**: {len(data)}\n\n"
    
    for idx, item in enumerate(data[:10], 1):
        if isinstance(item, dict):
            name = item.get('name', item.get('id', f'Item {idx}'))
            result += f"## {name}\n"
            for key, value in item.items():
                if value is not None and key not in ['name']:
                    result += f"- **{key}**: {value}\n"
            result += "\n"
        else:
            result += f"- {item}\n"
    
    if len(data) > 10:
        result += f"\n... and {len(data) - 10} more items"
    
    return result

def register_insight_additional_tools(mcp_app, meraki):
    """Register additional insight tools with the MCP server."""
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    
    # Register all additional tools
    register_insight_additional_handlers()

def register_insight_additional_handlers():
    """Register additional insight tool handlers."""

    @app.tool(
        name="create_organization_insight_monitored_media_server",
        description="➕ Create organization insight monitored media server"
    )
    def create_organization_insight_monitored_media_server(organization_id: str, **kwargs):
        """Create organization insight monitored media server."""
        try:
            result = meraki_client.dashboard.insight.createOrganizationInsightMonitoredMediaServer(
                organization_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Insight Monitored Media Server")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Insight Monitored Media Server")
            else:
                return f"✅ Create organization insight monitored media server completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="delete_organization_insight_monitored_media_server",
        description="🗑️ Delete organization insight monitored media server"
    )
    def delete_organization_insight_monitored_media_server(organization_id: str):
        """Delete organization insight monitored media server."""
        try:
            result = meraki_client.dashboard.insight.deleteOrganizationInsightMonitoredMediaServer(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Insight Monitored Media Server")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Insight Monitored Media Server")
            else:
                return f"✅ Delete organization insight monitored media server completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_insight_monitored_media_server",
        description="📊 Get organization insight monitored media server"
    )
    def get_organization_insight_monitored_media_server(organization_id: str):
        """Get organization insight monitored media server."""
        try:
            result = meraki_client.dashboard.insight.getOrganizationInsightMonitoredMediaServer(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Insight Monitored Media Server")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Insight Monitored Media Server")
            else:
                return f"✅ Get organization insight monitored media server completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="update_organization_insight_monitored_media_server",
        description="✏️ Update organization insight monitored media server"
    )
    def update_organization_insight_monitored_media_server(organization_id: str, **kwargs):
        """Update organization insight monitored media server."""
        try:
            result = meraki_client.dashboard.insight.updateOrganizationInsightMonitoredMediaServer(
                organization_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Insight Monitored Media Server")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Insight Monitored Media Server")
            else:
                return f"✅ Update organization insight monitored media server completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"
