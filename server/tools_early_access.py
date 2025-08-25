"""
Early Access Features management tools for Cisco Meraki MCP Server.
Handles opt-in/opt-out for beta and early access features.
"""

# Global variables to store app and meraki client
app = None
meraki_client = None

def register_early_access_tools(mcp_app, meraki):
    """Register early access tools with the MCP server."""
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    
    # Register all early access tools
    register_early_access_handlers()

def register_early_access_handlers():
    """Register all early access tool handlers using the decorator pattern."""
    
    @app.tool(
        name="get_organization_early_access_features",
        description="🚀 Get early access features opt-in status"
    )
    def get_organization_early_access_features(organization_id: str):
        """Get early access features opt-in status for an organization."""
        try:
            features = meraki_client.dashboard.organizations.getOrganizationEarlyAccessFeaturesOptIns(organization_id)
            
            if not features:
                return f"No early access features available for organization {organization_id}."
            
            result = f"# 🚀 Early Access Features\n\n"
            result += f"**Total Features**: {len(features)}\n\n"
            
            # Group by opt-in status
            opted_in = []
            available = []
            
            for feature in features:
                if feature.get('isOptedIn'):
                    opted_in.append(feature)
                else:
                    available.append(feature)
            
            if opted_in:
                result += "## ✅ Opted-In Features\n"
                for feature in opted_in:
                    result += f"\n### {feature.get('name', 'Unknown Feature')}\n"
                    result += f"- **ID**: {feature.get('id')}\n"
                    result += f"- **Short Name**: {feature.get('shortName')}\n"
                    
                    if feature.get('description'):
                        result += f"- **Description**: {feature['description']}\n"
                    
                    if feature.get('documentationLink'):
                        result += f"- **Documentation**: {feature['documentationLink']}\n"
                    
                    if feature.get('supportLink'):
                        result += f"- **Support**: {feature['supportLink']}\n"
                    
                    result += f"- **Opted In Since**: {feature.get('optedInAt', 'Unknown')}\n"
            
            if available:
                result += "\n## 🆕 Available Features (Not Opted In)\n"
                for feature in available:
                    result += f"\n### {feature.get('name', 'Unknown Feature')}\n"
                    result += f"- **ID**: {feature.get('id')}\n"
                    result += f"- **Short Name**: {feature.get('shortName')}\n"
                    
                    if feature.get('description'):
                        result += f"- **Description**: {feature['description']}\n"
                    
                    if feature.get('documentationLink'):
                        result += f"- **Documentation**: {feature['documentationLink']}\n"
            
            result += "\n## 💡 How to Opt In\n"
            result += "Use `update_organization_early_access_feature()` with the feature ID to opt in.\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving early access features: {str(e)}"
    
    @app.tool(
        name="update_organization_early_access_feature",
        description="🚀 Opt in/out of an early access feature"
    )
    def update_organization_early_access_feature(
        organization_id: str,
        feature_id: str,
        opt_in: bool = True
    ):
        """
        Update early access feature opt-in status.
        
        Args:
            organization_id: Organization ID
            feature_id: Early access feature ID
            opt_in: True to opt in, False to opt out
        """
        try:
            result = meraki_client.dashboard.organizations.updateOrganizationEarlyAccessFeaturesOptIn(
                organization_id,
                feature_id,
                limitScopeToNetworks=[]  # Apply to all networks
            )
            
            action = "opted in to" if opt_in else "opted out of"
            
            response = f"✅ Successfully {action} early access feature!\n\n"
            response += f"**Feature**: {result.get('shortName', feature_id)}\n"
            response += f"**Status**: {'Enabled' if opt_in else 'Disabled'}\n"
            
            if result.get('documentationLink'):
                response += f"\n📚 **Documentation**: {result['documentationLink']}\n"
            
            if opt_in:
                response += "\n⚠️ **Important Notes**:\n"
                response += "- Early access features may be unstable\n"
                response += "- Features may change or be removed\n"
                response += "- Not recommended for production networks\n"
                response += "- Test thoroughly before widespread deployment\n"
            
            return response
            
        except Exception as e:
            return f"Error updating early access feature: {str(e)}"