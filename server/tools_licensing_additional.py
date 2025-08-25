"""
Additional Licensing endpoints for Cisco Meraki MCP Server.
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

def register_licensing_additional_tools(mcp_app, meraki):
    """Register additional licensing tools with the MCP server."""
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    
    # Register all additional tools
    register_licensing_additional_handlers()

def register_licensing_additional_handlers():
    """Register additional licensing tool handlers."""

    @app.tool(
        name="bind_administered_licensing_subscription_subscription",
        description="⚡ Execute administered licensing subscription subscription"
    )
    def bind_administered_licensing_subscription_subscription():
        """Execute administered licensing subscription subscription."""
        try:
            result = meraki_client.dashboard.licensing.bindAdministeredLicensingSubscriptionSubscription(
                
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Administered Licensing Subscription Subscription")
            elif isinstance(result, list):
                return format_list_response(result, "Administered Licensing Subscription Subscription")
            else:
                return f"✅ Execute administered licensing subscription subscription completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="claim_administered_licensing_subscription_subscriptions",
        description="📥 Claim administered licensing subscription subscriptions"
    )
    def claim_administered_licensing_subscription_subscriptions():
        """Claim administered licensing subscription subscriptions."""
        try:
            result = meraki_client.dashboard.licensing.claimAdministeredLicensingSubscriptionSubscriptions(
                
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Administered Licensing Subscription Subscriptions")
            elif isinstance(result, list):
                return format_list_response(result, "Administered Licensing Subscription Subscriptions")
            else:
                return f"✅ Claim administered licensing subscription subscriptions completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_administered_licensing_subscription_entitlements",
        description="📊 Get administered licensing subscription entitlements"
    )
    def get_administered_licensing_subscription_entitlements():
        """Get administered licensing subscription entitlements."""
        try:
            result = meraki_client.dashboard.licensing.getAdministeredLicensingSubscriptionEntitlements(
                
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Administered Licensing Subscription Entitlements")
            elif isinstance(result, list):
                return format_list_response(result, "Administered Licensing Subscription Entitlements")
            else:
                return f"✅ Get administered licensing subscription entitlements completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_administered_licensing_subscription_subscriptions",
        description="📊 Get administered licensing subscription subscriptions"
    )
    def get_administered_licensing_subscription_subscriptions():
        """Get administered licensing subscription subscriptions."""
        try:
            result = meraki_client.dashboard.licensing.getAdministeredLicensingSubscriptionSubscriptions(
                
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Administered Licensing Subscription Subscriptions")
            elif isinstance(result, list):
                return format_list_response(result, "Administered Licensing Subscription Subscriptions")
            else:
                return f"✅ Get administered licensing subscription subscriptions completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_admin_licensing_compliance_status",
        description="📊 Get administered licensing subscription subscriptions compliance statuses"
    )
    def get_administered_licensing_subscription_subscriptions_compliance_statuses():
        """Get administered licensing subscription subscriptions compliance statuses."""
        try:
            result = meraki_client.dashboard.licensing.getAdministeredLicensingSubscriptionSubscriptionsComplianceStatuses(
                
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Administered Licensing Subscription Subscriptions Compliance Statuses")
            elif isinstance(result, list):
                return format_list_response(result, "Administered Licensing Subscription Subscriptions Compliance Statuses")
            else:
                return f"✅ Get administered licensing subscription subscriptions compliance statuses completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="validate_admin_licensing_claim_key",
        description="📥 Claim administered licensing subscription subscriptions claim key"
    )
    def validate_administered_licensing_subscription_subscriptions_claim_key():
        """Claim administered licensing subscription subscriptions claim key."""
        try:
            result = meraki_client.dashboard.licensing.validateAdministeredLicensingSubscriptionSubscriptionsClaimKey(
                
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Administered Licensing Subscription Subscriptions Claim Key")
            elif isinstance(result, list):
                return format_list_response(result, "Administered Licensing Subscription Subscriptions Claim Key")
            else:
                return f"✅ Claim administered licensing subscription subscriptions claim key completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"
