"""
Early Access features management tools for Cisco Meraki MCP server.

This module provides tools for managing early access features and opt-ins.
"""

from typing import Optional, Dict, Any, List
from datetime import datetime
import json

# Global references to be set by register function
app = None
meraki_client = None

def register_early_access_tools(mcp_app, meraki):
    """
    Register early access tools with the MCP server.
    
    Args:
        mcp_app: MCP server instance
        meraki: Meraki client instance
    """
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    
    # ==================== EARLY ACCESS FEATURES ====================
    
    @app.tool(
        name="get_organization_early_access_features",
        description="🧪📋 List all available early access features for an organization"
    )
    def get_organization_early_access_features(
        organization_id: str
    ):
        """Get all available early access features."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationEarlyAccessFeatures(
                organization_id
            )
            
            response = f"# 🧪 Available Early Access Features\n\n"
            
            if result and isinstance(result, list):
                response += f"**Total Features**: {len(result)}\n\n"
                
                for feature in result:
                    # Status icon
                    status = feature.get('status', 'unknown')
                    status_icon = "✅" if status == 'available' else "🔒" if status == 'restricted' else "⏳"
                    
                    response += f"## {status_icon} {feature.get('name', 'Unknown')}\n"
                    response += f"- **ID**: {feature.get('shortName', feature.get('id', 'N/A'))}\n"
                    response += f"- **Status**: {status}\n"
                    response += f"- **Description**: {feature.get('description', 'No description')}\n"
                    
                    # Documentation
                    doc_link = feature.get('documentationLink')
                    if doc_link:
                        response += f"- **Documentation**: {doc_link}\n"
                    
                    # Supported products
                    products = feature.get('supportedProducts', [])
                    if products:
                        response += f"- **Products**: {', '.join(products)}\n"
                    
                    response += "\n"
            else:
                response += "*No early access features available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting early access features: {str(e)}"
    
    @app.tool(
        name="get_organization_early_access_features_opt_ins",
        description="🧪✅ List all early access features the organization has opted into"
    )
    def get_organization_early_access_features_opt_ins(
        organization_id: str
    ):
        """Get all early access feature opt-ins."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationEarlyAccessFeaturesOptIns(
                organization_id
            )
            
            response = f"# 🧪 Active Early Access Opt-Ins\n\n"
            
            if result and isinstance(result, list):
                response += f"**Total Opt-Ins**: {len(result)}\n\n"
                response += "⚠️ **Note**: Early access features may have breaking changes\n\n"
                
                for opt_in in result:
                    response += f"## ✅ {opt_in.get('shortName', 'Unknown Feature')}\n"
                    response += f"- **Opt-In ID**: {opt_in.get('id', 'N/A')}\n"
                    response += f"- **Created**: {opt_in.get('createdAt', 'N/A')}\n"
                    
                    # Limited access networks
                    limited = opt_in.get('limitScopeToNetworks', [])
                    if limited:
                        response += f"- **Limited to {len(limited)} networks**:\n"
                        for net_id in limited[:5]:
                            response += f"  - {net_id}\n"
                        if len(limited) > 5:
                            response += f"  - ...and {len(limited)-5} more\n"
                    else:
                        response += "- **Scope**: All networks\n"
                    
                    response += "\n"
            else:
                response += "*No early access features opted into*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting opt-ins: {str(e)}"
    
    @app.tool(
        name="get_organization_early_access_features_opt_in",
        description="🧪🔍 Get details of a specific early access feature opt-in"
    )
    def get_organization_early_access_features_opt_in(
        organization_id: str,
        opt_in_id: str
    ):
        """Get details of a specific opt-in."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationEarlyAccessFeaturesOptIn(
                organization_id, opt_in_id
            )
            
            response = f"# 🧪 Early Access Opt-In Details\n\n"
            
            if result:
                response += f"**Feature**: {result.get('shortName', 'Unknown')}\n"
                response += f"**Opt-In ID**: {result.get('id', 'N/A')}\n"
                response += f"**Created**: {result.get('createdAt', 'N/A')}\n\n"
                
                # Scope
                limited = result.get('limitScopeToNetworks', [])
                if limited:
                    response += f"## Limited Scope ({len(limited)} networks)\n\n"
                    for net_id in limited:
                        response += f"- {net_id}\n"
                else:
                    response += "## Scope: All Networks\n"
            else:
                response += "*Opt-in not found*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting opt-in details: {str(e)}"
    
    @app.tool(
        name="create_organization_early_access_features_opt_in",
        description="🧪➕ Opt into an early access feature"
    )
    def create_organization_early_access_features_opt_in(
        organization_id: str,
        short_name: str,
        limit_scope_to_networks: Optional[str] = None
    ):
        """
        Opt into an early access feature.
        
        Args:
            organization_id: Organization ID
            short_name: Short name/ID of the feature
            limit_scope_to_networks: Comma-separated network IDs to limit scope (optional)
        """
        try:
            kwargs = {'shortName': short_name}
            
            if limit_scope_to_networks:
                # Convert comma-separated string to list
                network_ids = [n.strip() for n in limit_scope_to_networks.split(',')]
                kwargs['limitScopeToNetworks'] = network_ids
            
            result = meraki_client.dashboard.organizations.createOrganizationEarlyAccessFeaturesOptIn(
                organization_id, **kwargs
            )
            
            response = f"# ✅ Opted Into Early Access Feature\n\n"
            
            if result:
                response += f"**Feature**: {result.get('shortName', short_name)}\n"
                response += f"**Opt-In ID**: {result.get('id', 'N/A')}\n"
                response += f"**Created**: {result.get('createdAt', 'Now')}\n\n"
                
                if limit_scope_to_networks:
                    response += f"**Limited to**: {limit_scope_to_networks}\n\n"
                
                response += "⚠️ **Warning**: Early access features may change or be removed\n"
            
            return response
        except Exception as e:
            error_msg = str(e)
            if '400' in error_msg:
                return f"❌ Invalid feature or already opted in: {short_name}"
            return f"❌ Error opting into feature: {error_msg}"
    
    @app.tool(
        name="update_organization_early_access_features_opt_in",
        description="🧪✏️ Update the scope of an early access feature opt-in"
    )
    def update_organization_early_access_features_opt_in(
        organization_id: str,
        opt_in_id: str,
        limit_scope_to_networks: Optional[str] = None
    ):
        """
        Update an early access opt-in scope.
        
        Args:
            organization_id: Organization ID
            opt_in_id: Opt-in ID to update
            limit_scope_to_networks: Comma-separated network IDs or 'all' for all networks
        """
        try:
            kwargs = {}
            
            if limit_scope_to_networks:
                if limit_scope_to_networks.lower() == 'all':
                    # Empty list means all networks
                    kwargs['limitScopeToNetworks'] = []
                else:
                    # Convert comma-separated string to list
                    network_ids = [n.strip() for n in limit_scope_to_networks.split(',')]
                    kwargs['limitScopeToNetworks'] = network_ids
            
            result = meraki_client.dashboard.organizations.updateOrganizationEarlyAccessFeaturesOptIn(
                organization_id, opt_in_id, **kwargs
            )
            
            response = f"# ✅ Updated Early Access Opt-In\n\n"
            
            if result:
                response += f"**Feature**: {result.get('shortName', 'Unknown')}\n"
                response += f"**Opt-In ID**: {opt_in_id}\n\n"
                
                limited = result.get('limitScopeToNetworks', [])
                if limited:
                    response += f"**Limited to {len(limited)} networks**\n"
                else:
                    response += "**Scope**: All networks\n"
            
            return response
        except Exception as e:
            return f"❌ Error updating opt-in: {str(e)}"
    
    @app.tool(
        name="delete_organization_early_access_features_opt_in",
        description="🧪❌ Opt out of an early access feature"
    )
    def delete_organization_early_access_features_opt_in(
        organization_id: str,
        opt_in_id: str
    ):
        """
        Delete an early access feature opt-in (opt out).
        
        Args:
            organization_id: Organization ID
            opt_in_id: Opt-in ID to delete
        """
        try:
            meraki_client.dashboard.organizations.deleteOrganizationEarlyAccessFeaturesOptIn(
                organization_id, opt_in_id
            )
            
            response = f"# ✅ Opted Out of Early Access Feature\n\n"
            response += f"**Opt-In ID**: {opt_in_id}\n\n"
            response += "The early access feature has been disabled for this organization.\n"
            
            return response
        except Exception as e:
            error_msg = str(e)
            if '404' in error_msg:
                return f"❌ Opt-in not found: {opt_in_id}\n\n💡 Use get_organization_early_access_features_opt_ins to list valid opt-in IDs"
            return f"❌ Error deleting opt-in: {error_msg}"