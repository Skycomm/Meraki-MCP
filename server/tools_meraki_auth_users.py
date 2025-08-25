"""
Meraki Auth Users management tools for the Cisco Meraki MCP Server - COMPLETE v1.61 IMPLEMENTATION.
"""

# Global variables to store app and meraki client
app = None
meraki_client = None

def register_meraki_auth_users_tools(mcp_app, meraki):
    """
    Register Meraki Auth Users-related tools with the MCP server.
    
    Args:
        mcp_app: MCP server instance
        meraki: Meraki client instance
    """
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    
    # Register all Meraki Auth Users tools
    register_meraki_auth_users_tool_handlers()

def register_meraki_auth_users_tool_handlers():
    """Register all Meraki Auth Users-related tool handlers using the decorator pattern."""
    
    # Meraki Auth Users Management
    @app.tool(
        name="get_network_meraki_auth_users",
        description="🔐 Get Meraki auth users"
    )
    def get_network_meraki_auth_users(network_id: str):
        """List Meraki auth users for a network."""
        try:
            users = meraki_client.dashboard.networks.getNetworkMerakiAuthUsers(network_id)
            
            if not users:
                return f"No Meraki auth users found for network {network_id}."
            
            result = f"# 🔐 Meraki Auth Users\n\n"
            result += f"**Total Users**: {len(users)}\n\n"
            
            for user in users[:20]:
                result += f"- **{user.get('name', 'Unknown')}**\n"
                result += f"  - Email: {user.get('email', 'Not set')}\n"
                result += f"  - Account Type: {user.get('accountType', 'Unknown')}\n"
                result += f"  - Authorized: {'✅' if user.get('isAuthorized') else '❌'}\n\n"
            
            if len(users) > 20:
                result += f"... and {len(users) - 20} more users\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving Meraki auth users: {str(e)}"
    
    @app.tool(
        name="create_network_meraki_auth_user",
        description="🔐 Create Meraki auth user"
    )
    def create_network_meraki_auth_user(network_id: str, email: str, name: str, password: str, **kwargs):
        """Create a Meraki auth user."""
        try:
            result = meraki_client.dashboard.networks.createNetworkMerakiAuthUser(
                network_id, email, name, password, **kwargs
            )
            
            return f"✅ Meraki auth user '{name}' created successfully!\n\nUser ID: {result.get('id')}"
            
        except Exception as e:
            return f"Error creating Meraki auth user: {str(e)}"
    
    @app.tool(
        name="get_network_meraki_auth_user",
        description="🔐 Get Meraki auth user details"
    )
    def get_network_meraki_auth_user(network_id: str, merakiAuthUserId: str):
        """Get details of a Meraki auth user."""
        try:
            user = meraki_client.dashboard.networks.getNetworkMerakiAuthUser(
                network_id, merakiAuthUserId
            )
            
            result = f"# 🔐 Meraki Auth User Details\n\n"
            result += f"**Name**: {user.get('name')}\n"
            result += f"**Email**: {user.get('email')}\n"
            result += f"**Account Type**: {user.get('accountType')}\n"
            result += f"**Authorized**: {'✅' if user.get('isAuthorized') else '❌'}\n"
            result += f"**Created At**: {user.get('createdAt')}\n"
            
            if user.get('authorizations'):
                result += f"\n**Authorizations**: {len(user['authorizations'])}\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving Meraki auth user: {str(e)}"
    
    @app.tool(
        name="delete_network_meraki_auth_user",
        description="🔐 Delete Meraki auth user"
    )
    def delete_network_meraki_auth_user(network_id: str, merakiAuthUserId: str):
        """Delete a Meraki auth user."""
        try:
            meraki_client.dashboard.networks.deleteNetworkMerakiAuthUser(
                network_id, merakiAuthUserId
            )
            
            return f"✅ Meraki auth user deleted successfully!"
            
        except Exception as e:
            return f"Error deleting Meraki auth user: {str(e)}"
    
    @app.tool(
        name="update_network_meraki_auth_user",
        description="🔐 Update Meraki auth user"
    )
    def update_network_meraki_auth_user(network_id: str, merakiAuthUserId: str, **kwargs):
        """Update a Meraki auth user."""
        try:
            result = meraki_client.dashboard.networks.updateNetworkMerakiAuthUser(
                network_id, merakiAuthUserId, **kwargs
            )
            
            return f"✅ Meraki auth user updated successfully!"
            
        except Exception as e:
            return f"Error updating Meraki auth user: {str(e)}"