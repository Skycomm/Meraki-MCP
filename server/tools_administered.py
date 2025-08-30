"""
Administered identity and API key management tools for Cisco Meraki MCP server.

This module provides tools for managing administered identities and API keys.
"""

from typing import Optional, Dict, Any, List
from datetime import datetime
import json

# Global references to be set by register function
app = None
meraki_client = None

def register_administered_tools(mcp_app, meraki):
    """
    Register administered tools with the MCP server.
    
    Args:
        mcp_app: MCP server instance
        meraki: Meraki client instance
    """
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    
    # ==================== IDENTITY MANAGEMENT ====================
    
    @app.tool(
        name="get_administered_identities_me",
        description="🔑👤 Get the identity of the current API user"
    )
    def get_administered_identities_me():
        """Get the identity of the current administrator/API user."""
        try:
            result = meraki_client.administered.getAdministeredIdentitiesMe()
            
            response = f"# 👤 Current Administrator Identity\n\n"
            
            if result:
                response += f"**Name**: {result.get('name', 'N/A')}\n"
                response += f"**Email**: {result.get('email', 'N/A')}\n"
                response += f"**Authentication**: {result.get('authentication', {}).get('mode', 'N/A')}\n"
                
                # Show organizations
                orgs = result.get('organizations', [])
                if orgs:
                    response += f"\n## Organizations ({len(orgs)})\n\n"
                    for org in orgs:
                        response += f"### {org.get('name', 'Unknown')}\n"
                        response += f"- ID: {org.get('id')}\n"
                        response += f"- Access: {org.get('access', 'N/A')}\n"
                        response += f"- Status: {org.get('status', 'N/A')}\n\n"
                
                # Show permissions
                permissions = result.get('permissions', [])
                if permissions:
                    response += f"\n## Permissions\n\n"
                    for perm in permissions:
                        response += f"- {perm}\n"
            else:
                response += "*No identity information available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting identity: {str(e)}"
    
    @app.tool(
        name="get_administered_identities_me_api_keys",
        description="🔑🔐 Get all API keys for the current user"
    )
    def get_administered_identities_me_api_keys():
        """Get all API keys associated with the current user."""
        try:
            result = meraki_client.administered.getAdministeredIdentitiesMeApiKeys()
            
            response = f"# 🔐 API Keys\n\n"
            
            if result and isinstance(result, list):
                response += f"**Total Keys**: {len(result)}\n\n"
                
                for i, key in enumerate(result, 1):
                    response += f"## Key {i}\n"
                    response += f"- ID: {key.get('id', 'N/A')}\n"
                    response += f"- Name: {key.get('name', 'Unnamed')}\n"
                    response += f"- Created: {key.get('createdAt', 'N/A')}\n"
                    response += f"- Last Used: {key.get('lastUsedAt', 'Never')}\n"
                    
                    # Don't show the actual key for security
                    if key.get('key'):
                        response += f"- Key: {'*' * 8}...{key['key'][-4:]}\n"
                    
                    response += "\n"
            else:
                response += "*No API keys found*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting API keys: {str(e)}"
    
    @app.tool(
        name="generate_administered_identities_me_api_keys",
        description="🔑➕ Generate a new API key for the current user"
    )
    def generate_administered_identities_me_api_keys(
        name: Optional[str] = None
    ):
        """
        Generate a new API key for the current user.
        
        Args:
            name: Optional name for the API key
        """
        try:
            kwargs = {}
            if name:
                kwargs['name'] = name
            
            result = meraki_client.administered.generateAdministeredIdentitiesMeApiKeys(**kwargs)
            
            response = f"# ✅ New API Key Generated\n\n"
            
            if result:
                response += f"**ID**: {result.get('id', 'N/A')}\n"
                response += f"**Name**: {result.get('name', 'Unnamed')}\n"
                response += f"**Created**: {result.get('createdAt', 'N/A')}\n\n"
                
                # Show the key with a security warning
                if result.get('key'):
                    response += "⚠️ **IMPORTANT**: Save this key securely. It won't be shown again!\n\n"
                    response += f"```\n{result['key']}\n```\n\n"
                    response += "This key provides full API access to your Meraki dashboard.\n"
            else:
                response += "*Key generation failed*\n"
            
            return response
        except Exception as e:
            return f"❌ Error generating API key: {str(e)}"
    
    @app.tool(
        name="revoke_administered_identities_me_api_keys",
        description="🔑❌ Revoke an API key for the current user"
    )
    def revoke_administered_identities_me_api_keys(
        api_key_id: str
    ):
        """
        Revoke an existing API key.
        
        Args:
            api_key_id: The ID of the API key to revoke
        """
        try:
            # This typically returns 204 No Content on success
            meraki_client.administered.revokeAdministeredIdentitiesMeApiKeys(api_key_id)
            
            response = f"# ✅ API Key Revoked\n\n"
            response += f"**Key ID**: {api_key_id}\n\n"
            response += "The API key has been successfully revoked and can no longer be used.\n"
            
            return response
        except Exception as e:
            error_msg = str(e)
            if '404' in error_msg:
                return f"❌ API key not found: {api_key_id}\n\n💡 Use get_administered_identities_me_api_keys to list valid key IDs"
            return f"❌ Error revoking API key: {error_msg}"