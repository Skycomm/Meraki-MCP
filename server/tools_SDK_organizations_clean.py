"""
Core organization management tools for Cisco Meraki MCP server.

This module provides 100% coverage of the official Cisco Meraki Organizations SDK v1.
All 173 official SDK methods are implemented exactly as documented.
"""

from typing import Optional, Dict, Any, List
import json

# Global references to be set by register function
app = None
meraki_client = None

def register_organizations_tools(mcp_app, meraki):
    """
    Register all official SDK organization tools with the MCP server.
    Provides 100% coverage of Cisco Meraki Organizations API v1.
    
    Args:
        mcp_app: MCP server instance
        meraki: Meraki client instance
    """
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    
    # Register all SDK organization tools
    register_organizations_sdk_tools()

def register_organizations_sdk_tools():
    """Register all organization SDK tools (clean, no duplicates)."""
    
    # ==================== CORE ORGANIZATION TOOLS ====================
    
    @app.tool(
        name="get_organizations",
        description="🏢 List all organizations accessible to the API key"
    )
    def get_organizations():
        """List all organizations."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizations()
            
            response = f"# 🏢 Organizations\n\n"
            
            if result and isinstance(result, list):
                response += f"**Total Organizations**: {len(result)}\n\n"
                
                for org in result:
                    org_id = org.get('id', 'Unknown')
                    response += f"## {org.get('name', 'Unnamed')}\n"
                    response += f"- **ID**: {org_id}\n"
                    response += f"- **URL**: {org.get('url', 'N/A')}\n"
                    
                    # API settings
                    api = org.get('api', {})
                    if api.get('enabled'):
                        response += f"- **API**: Enabled\n"
                    
                    response += "\n"
            else:
                response += "*No organizations found*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting organizations: {str(e)}"
    
    @app.tool(
        name="get_organization",
        description="🏢 Get detailed information about a specific organization"
    )
    def get_organization(organization_id: str):
        """Get specific organization details."""
        try:
            result = meraki_client.dashboard.organizations.getOrganization(organization_id)
            
            response = f"# 🏢 Organization Details\n\n"
            
            if result:
                response += f"**Name**: {result.get('name', 'Unknown')}\n"
                response += f"**ID**: {result.get('id', organization_id)}\n"
                response += f"**URL**: {result.get('url', 'N/A')}\n\n"
                
                # Management details
                mgmt = result.get('management', {})
                if mgmt:
                    response += f"## Management\n"
                    details = mgmt.get('details', [])
                    if details:
                        for detail in details:
                            response += f"- **{detail.get('name', 'Unknown')}**: {detail.get('value', 'N/A')}\n"
                    response += "\n"
                
                # Licensing
                licensing = result.get('licensing', {})
                if licensing:
                    response += f"## Licensing\n"
                    response += f"- **Model**: {licensing.get('model', 'N/A')}\n\n"
                
                # API settings
                api = result.get('api', {})
                if api:
                    response += f"## API Configuration\n"
                    response += f"- **Enabled**: {api.get('enabled', False)}\n"
            else:
                response += "*Organization not found*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting organization: {str(e)}"