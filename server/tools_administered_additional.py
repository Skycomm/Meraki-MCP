"""
Additional Administered endpoints for Cisco Meraki MCP Server.
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

def register_administered_additional_tools(mcp_app, meraki):
    """Register additional administered tools with the MCP server."""
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    
    # Register all additional tools
    register_administered_additional_handlers()

def register_administered_additional_handlers():
    """Register additional administered tool handlers."""

    @app.tool(
        name="generate_administered_identities_me_api_keys",
        description="⚡ Execute administered identities me api keys"
    )
    def generate_administered_identities_me_api_keys():
        """Execute administered identities me api keys."""
        try:
            result = meraki_client.dashboard.administered.generateAdministeredIdentitiesMeApiKeys(
                
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Administered Identities Me Api Keys")
            elif isinstance(result, list):
                return format_list_response(result, "Administered Identities Me Api Keys")
            else:
                return f"✅ Execute administered identities me api keys completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="revoke_administered_identities_me_api_keys",
        description="⚡ Execute administered identities me api keys"
    )
    def revoke_administered_identities_me_api_keys():
        """Execute administered identities me api keys."""
        try:
            result = meraki_client.dashboard.administered.revokeAdministeredIdentitiesMeApiKeys(
                
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Administered Identities Me Api Keys")
            elif isinstance(result, list):
                return format_list_response(result, "Administered Identities Me Api Keys")
            else:
                return f"✅ Execute administered identities me api keys completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"
