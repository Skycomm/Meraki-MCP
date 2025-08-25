"""
PII (Personally Identifiable Information) management tools for the Cisco Meraki MCP Server - COMPLETE v1.61 IMPLEMENTATION.
"""

# Global variables to store app and meraki client
app = None
meraki_client = None

def register_pii_tools(mcp_app, meraki):
    """
    Register PII-related tools with the MCP server.
    
    Args:
        mcp_app: MCP server instance
        meraki: Meraki client instance
    """
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    
    # Register all PII tools
    register_pii_tool_handlers()

def register_pii_tool_handlers():
    """Register all PII-related tool handlers using the decorator pattern."""
    
    # PII Management
    @app.tool(
        name="get_network_pii_pii_keys",
        description="🔑 Get PII keys"
    )
    def get_network_pii_pii_keys(network_id: str, **kwargs):
        """List personally identifiable information keys."""
        try:
            keys = meraki_client.dashboard.networks.getNetworkPiiPiiKeys(network_id, **kwargs)
            
            result = f"# 🔑 PII Keys\n\n"
            
            if not keys:
                return result + "No PII keys found."
            
            for key in keys:
                result += f"- **{key}**\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving PII keys: {str(e)}"
    
    @app.tool(
        name="get_network_pii_requests",
        description="📋 Get PII requests"
    )
    def get_network_pii_requests(network_id: str):
        """List PII requests for a network."""
        try:
            requests = meraki_client.dashboard.networks.getNetworkPiiRequests(network_id)
            
            if not requests:
                return f"No PII requests found for network {network_id}."
            
            result = f"# 📋 PII Requests\n\n"
            result += f"**Total Requests**: {len(requests)}\n\n"
            
            for request in requests[:10]:
                result += f"## Request {request.get('id')}\n"
                result += f"- Type: {request.get('type')}\n"
                result += f"- Status: {request.get('status')}\n"
                result += f"- Created At: {request.get('createdAt')}\n\n"
            
            if len(requests) > 10:
                result += f"... and {len(requests) - 10} more requests\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving PII requests: {str(e)}"
    
    @app.tool(
        name="create_network_pii_request",
        description="📋 Create PII request"
    )
    def create_network_pii_request(network_id: str, type: str, **kwargs):
        """Create a new PII request."""
        try:
            result = meraki_client.dashboard.networks.createNetworkPiiRequest(
                network_id, type, **kwargs
            )
            
            return f"✅ PII request created successfully!\n\nRequest ID: {result.get('id')}"
            
        except Exception as e:
            return f"Error creating PII request: {str(e)}"
    
    @app.tool(
        name="get_network_pii_request",
        description="📋 Get PII request details"
    )
    def get_network_pii_request(network_id: str, requestId: str):
        """Get details of a PII request."""
        try:
            request = meraki_client.dashboard.networks.getNetworkPiiRequest(
                network_id, requestId
            )
            
            result = f"# 📋 PII Request Details\n\n"
            result += f"**ID**: {request.get('id')}\n"
            result += f"**Type**: {request.get('type')}\n"
            result += f"**Status**: {request.get('status')}\n"
            result += f"**Created At**: {request.get('createdAt')}\n"
            
            if request.get('completedAt'):
                result += f"**Completed At**: {request['completedAt']}\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving PII request: {str(e)}"
    
    @app.tool(
        name="delete_network_pii_request",
        description="📋 Delete PII request"
    )
    def delete_network_pii_request(network_id: str, requestId: str):
        """Delete a PII request."""
        try:
            meraki_client.dashboard.networks.deleteNetworkPiiRequest(network_id, requestId)
            
            return f"✅ PII request deleted successfully!"
            
        except Exception as e:
            return f"Error deleting PII request: {str(e)}"
    
    @app.tool(
        name="get_network_pii_sm_devices_for_key",
        description="📱 Get SM devices for PII key"
    )
    def get_network_pii_sm_devices_for_key(network_id: str, **kwargs):
        """Get Systems Manager devices for a PII key."""
        try:
            devices = meraki_client.dashboard.networks.getNetworkPiiSmDevicesForKey(
                network_id, **kwargs
            )
            
            if not devices:
                return f"No SM devices found for the specified PII key."
            
            result = f"# 📱 SM Devices for PII Key\n\n"
            result += f"**Total Devices**: {len(devices)}\n\n"
            
            for device in devices[:20]:
                result += f"- {device.get('name', 'Unknown')} ({device.get('id')})\n"
            
            if len(devices) > 20:
                result += f"... and {len(devices) - 20} more devices\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving SM devices: {str(e)}"
    
    @app.tool(
        name="get_network_pii_sm_owners_for_key",
        description="👤 Get SM owners for PII key"
    )
    def get_network_pii_sm_owners_for_key(network_id: str, **kwargs):
        """Get Systems Manager owners for a PII key."""
        try:
            owners = meraki_client.dashboard.networks.getNetworkPiiSmOwnersForKey(
                network_id, **kwargs
            )
            
            if not owners:
                return f"No SM owners found for the specified PII key."
            
            result = f"# 👤 SM Owners for PII Key\n\n"
            result += f"**Total Owners**: {len(owners)}\n\n"
            
            for owner in owners[:20]:
                result += f"- {owner.get('name', 'Unknown')} ({owner.get('email', 'No email')})\n"
            
            if len(owners) > 20:
                result += f"... and {len(owners) - 20} more owners\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving SM owners: {str(e)}"