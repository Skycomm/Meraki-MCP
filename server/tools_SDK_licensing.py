"""
Licensing tools for Cisco Meraki MCP server.

This module provides 100% coverage of the official Cisco Meraki Licensing SDK v1.
All 8 official SDK methods are implemented exactly as documented.
"""

from typing import Optional, Dict, Any, List
import json

# Global references to be set by register function
app = None
meraki_client = None

def register_licensing_tools(mcp_app, meraki):
    """
    Register all official SDK licensing tools with the MCP server.
    Provides 100% coverage of Cisco Meraki Licensing API v1.
    
    Args:
        mcp_app: MCP server instance
        meraki: Meraki client instance
    """
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    
    # Register all licensing SDK tools
    register_licensing_sdk_tools()

def register_licensing_sdk_tools():
    """Register all licensing SDK tools (100% coverage)."""
    
    # ==================== ALL 8 LICENSING SDK TOOLS ====================
    
    @app.tool(
        name="bind_administered_licensing_subscription_subscription",
        description="🔗 Bind administered licensing subscription subscription"
    )
    def bind_administered_licensing_subscription_subscription(subscription_id: str, networks: str):
        """Bind bind administered licensing subscription subscription."""
        try:
            kwargs = {}
            
            if 'subscription_id' in locals():
                kwargs['subscriptionId'] = subscription_id
            if 'networks' in locals():
                kwargs['networks'] = [n.strip() for n in networks.split(',')]
            
            result = meraki_client.dashboard.licensing.bindAdministeredLicensingSubscriptionSubscription(**kwargs)
            
            response = f"# 🔗 Bind Administered Licensing Subscription Subscription\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with licensing-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('claimKey', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key licensing-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'expirationDate' in item:
                                response += f"   - Expires: {item.get('expirationDate')}\n"
                            if 'productType' in item:
                                response += f"   - Product: {item.get('productType')}\n"
                            if 'subscription' in item:
                                sub = item.get('subscription', {})
                                if isinstance(sub, dict):
                                    response += f"   - Subscription: {sub.get('name', 'N/A')}\n"
                            if 'counts' in item:
                                counts = item.get('counts', [])
                                if counts:
                                    response += f"   - Counts: {len(counts)} models\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show licensing-relevant fields
                    licensing_fields = ['name', 'claimKey', 'status', 'expirationDate', 'productType', 
                                      'subscription', 'counts', 'productTypes', 'networks']
                    
                    for field in licensing_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'counts' and value:
                                    response += f"- **Counts**: {len(value)} models\n"
                                elif field == 'networks' and value:
                                    response += f"- **Networks**: {len(value)} networks\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in licensing_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in bind_administered_licensing_subscription_subscription: {str(e)}"
    
    @app.tool(
        name="claim_administered_licensing_subscription_subscriptions",
        description="🔑 Claim administered licensing subscription subscriptions"
    )
    def claim_administered_licensing_subscription_subscriptions(claim_key: str, name: str):
        """Claim claim administered licensing subscription subscriptions."""
        try:
            kwargs = {}
            
            if 'claim_key' in locals():
                kwargs['claimKey'] = claim_key
            if 'name' in locals():
                kwargs['name'] = name
            
            result = meraki_client.dashboard.licensing.claimAdministeredLicensingSubscriptionSubscriptions(**kwargs)
            
            response = f"# 🔑 Claim Administered Licensing Subscription Subscriptions\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with licensing-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('claimKey', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key licensing-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'expirationDate' in item:
                                response += f"   - Expires: {item.get('expirationDate')}\n"
                            if 'productType' in item:
                                response += f"   - Product: {item.get('productType')}\n"
                            if 'subscription' in item:
                                sub = item.get('subscription', {})
                                if isinstance(sub, dict):
                                    response += f"   - Subscription: {sub.get('name', 'N/A')}\n"
                            if 'counts' in item:
                                counts = item.get('counts', [])
                                if counts:
                                    response += f"   - Counts: {len(counts)} models\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show licensing-relevant fields
                    licensing_fields = ['name', 'claimKey', 'status', 'expirationDate', 'productType', 
                                      'subscription', 'counts', 'productTypes', 'networks']
                    
                    for field in licensing_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'counts' and value:
                                    response += f"- **Counts**: {len(value)} models\n"
                                elif field == 'networks' and value:
                                    response += f"- **Networks**: {len(value)} networks\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in licensing_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in claim_administered_licensing_subscription_subscriptions: {str(e)}"
    
    @app.tool(
        name="get_administered_licensing_subscription_entitlements",
        description="📄 Get administered licensing subscriptionEntitlements"
    )
    def get_administered_licensing_subscription_entitlements(per_page: int = 100):
        """Get get administered licensing subscriptionentitlements."""
        try:
            kwargs = {}
            
            if 'per_page' in locals() and per_page:
                kwargs['perPage'] = min(per_page, 1000)
            
            result = meraki_client.dashboard.licensing.getAdministeredLicensingSubscriptionEntitlements(**kwargs)
            
            response = f"# 📄 Get Administered Licensing Subscriptionentitlements\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with licensing-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('claimKey', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key licensing-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'expirationDate' in item:
                                response += f"   - Expires: {item.get('expirationDate')}\n"
                            if 'productType' in item:
                                response += f"   - Product: {item.get('productType')}\n"
                            if 'subscription' in item:
                                sub = item.get('subscription', {})
                                if isinstance(sub, dict):
                                    response += f"   - Subscription: {sub.get('name', 'N/A')}\n"
                            if 'counts' in item:
                                counts = item.get('counts', [])
                                if counts:
                                    response += f"   - Counts: {len(counts)} models\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show licensing-relevant fields
                    licensing_fields = ['name', 'claimKey', 'status', 'expirationDate', 'productType', 
                                      'subscription', 'counts', 'productTypes', 'networks']
                    
                    for field in licensing_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'counts' and value:
                                    response += f"- **Counts**: {len(value)} models\n"
                                elif field == 'networks' and value:
                                    response += f"- **Networks**: {len(value)} networks\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in licensing_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_administered_licensing_subscription_entitlements: {str(e)}"
    
    @app.tool(
        name="get_administered_licensing_subscription_subscriptions",
        description="📄 Get administered licensing subscription subscriptions"
    )
    def get_administered_licensing_subscription_subscriptions(per_page: int = 100):
        """Get get administered licensing subscription subscriptions."""
        try:
            kwargs = {}
            
            if 'per_page' in locals() and per_page:
                kwargs['perPage'] = min(per_page, 1000)
            
            result = meraki_client.dashboard.licensing.getAdministeredLicensingSubscriptionSubscriptions(**kwargs)
            
            response = f"# 📄 Get Administered Licensing Subscription Subscriptions\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with licensing-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('claimKey', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key licensing-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'expirationDate' in item:
                                response += f"   - Expires: {item.get('expirationDate')}\n"
                            if 'productType' in item:
                                response += f"   - Product: {item.get('productType')}\n"
                            if 'subscription' in item:
                                sub = item.get('subscription', {})
                                if isinstance(sub, dict):
                                    response += f"   - Subscription: {sub.get('name', 'N/A')}\n"
                            if 'counts' in item:
                                counts = item.get('counts', [])
                                if counts:
                                    response += f"   - Counts: {len(counts)} models\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show licensing-relevant fields
                    licensing_fields = ['name', 'claimKey', 'status', 'expirationDate', 'productType', 
                                      'subscription', 'counts', 'productTypes', 'networks']
                    
                    for field in licensing_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'counts' and value:
                                    response += f"- **Counts**: {len(value)} models\n"
                                elif field == 'networks' and value:
                                    response += f"- **Networks**: {len(value)} networks\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in licensing_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_administered_licensing_subscription_subscriptions: {str(e)}"
    
    @app.tool(
        name="get_administered_licensing_subscription_subscriptions_compliance_statuses",
        description="📄 Get administered licensing subscription subscriptionsComplianceStatuses"
    )
    def get_administered_licensing_subscription_subscriptions_compliance_statuses(per_page: int = 100):
        """Get get administered licensing subscription subscriptionscompliancestatuses."""
        try:
            kwargs = {}
            
            if 'per_page' in locals() and per_page:
                kwargs['perPage'] = min(per_page, 1000)
            
            result = meraki_client.dashboard.licensing.getAdministeredLicensingSubscriptionSubscriptionsComplianceStatuses(**kwargs)
            
            response = f"# 📄 Get Administered Licensing Subscription Subscriptionscompliancestatuses\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with licensing-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('claimKey', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key licensing-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'expirationDate' in item:
                                response += f"   - Expires: {item.get('expirationDate')}\n"
                            if 'productType' in item:
                                response += f"   - Product: {item.get('productType')}\n"
                            if 'subscription' in item:
                                sub = item.get('subscription', {})
                                if isinstance(sub, dict):
                                    response += f"   - Subscription: {sub.get('name', 'N/A')}\n"
                            if 'counts' in item:
                                counts = item.get('counts', [])
                                if counts:
                                    response += f"   - Counts: {len(counts)} models\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show licensing-relevant fields
                    licensing_fields = ['name', 'claimKey', 'status', 'expirationDate', 'productType', 
                                      'subscription', 'counts', 'productTypes', 'networks']
                    
                    for field in licensing_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'counts' and value:
                                    response += f"- **Counts**: {len(value)} models\n"
                                elif field == 'networks' and value:
                                    response += f"- **Networks**: {len(value)} networks\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in licensing_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_administered_licensing_subscription_subscriptions_compliance_statuses: {str(e)}"
    
    @app.tool(
        name="get_organization_licensing_coterm_licenses",
        description="📄 Get organization licensing co-termLicenses"
    )
    def get_organization_licensing_coterm_licenses(organization_id: str, per_page: int = 100):
        """Get get organization licensing co-termlicenses."""
        try:
            kwargs = {}
            
            if 'per_page' in locals() and per_page:
                kwargs['perPage'] = min(per_page, 1000)
            
            result = meraki_client.dashboard.licensing.getOrganizationLicensingCotermLicenses(organization_id, **kwargs)
            
            response = f"# 📄 Get Organization Licensing Co-Termlicenses\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with licensing-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('claimKey', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key licensing-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'expirationDate' in item:
                                response += f"   - Expires: {item.get('expirationDate')}\n"
                            if 'productType' in item:
                                response += f"   - Product: {item.get('productType')}\n"
                            if 'subscription' in item:
                                sub = item.get('subscription', {})
                                if isinstance(sub, dict):
                                    response += f"   - Subscription: {sub.get('name', 'N/A')}\n"
                            if 'counts' in item:
                                counts = item.get('counts', [])
                                if counts:
                                    response += f"   - Counts: {len(counts)} models\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show licensing-relevant fields
                    licensing_fields = ['name', 'claimKey', 'status', 'expirationDate', 'productType', 
                                      'subscription', 'counts', 'productTypes', 'networks']
                    
                    for field in licensing_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'counts' and value:
                                    response += f"- **Counts**: {len(value)} models\n"
                                elif field == 'networks' and value:
                                    response += f"- **Networks**: {len(value)} networks\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in licensing_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_organization_licensing_coterm_licenses: {str(e)}"
    
    @app.tool(
        name="move_organization_licensing_coterm_licenses",
        description="🔄 Move organization licensing co-termLicenses"
    )
    def move_organization_licensing_coterm_licenses(organization_id: str, destination_organization_id: str, licenses: str):
        """Move move organization licensing co-termlicenses."""
        try:
            kwargs = {}
            
            if 'destination_organization_id' in locals():
                kwargs['destinationOrganizationId'] = destination_organization_id
            if 'licenses' in locals():
                kwargs['licenses'] = [l.strip() for l in licenses.split(',')]
            
            result = meraki_client.dashboard.licensing.moveOrganizationLicensingCotermLicenses(organization_id, **kwargs)
            
            response = f"# 🔄 Move Organization Licensing Co-Termlicenses\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with licensing-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('claimKey', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key licensing-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'expirationDate' in item:
                                response += f"   - Expires: {item.get('expirationDate')}\n"
                            if 'productType' in item:
                                response += f"   - Product: {item.get('productType')}\n"
                            if 'subscription' in item:
                                sub = item.get('subscription', {})
                                if isinstance(sub, dict):
                                    response += f"   - Subscription: {sub.get('name', 'N/A')}\n"
                            if 'counts' in item:
                                counts = item.get('counts', [])
                                if counts:
                                    response += f"   - Counts: {len(counts)} models\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show licensing-relevant fields
                    licensing_fields = ['name', 'claimKey', 'status', 'expirationDate', 'productType', 
                                      'subscription', 'counts', 'productTypes', 'networks']
                    
                    for field in licensing_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'counts' and value:
                                    response += f"- **Counts**: {len(value)} models\n"
                                elif field == 'networks' and value:
                                    response += f"- **Networks**: {len(value)} networks\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in licensing_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in move_organization_licensing_coterm_licenses: {str(e)}"
    
    @app.tool(
        name="validate_administered_licensing_subscription_subscriptions_claim_key",
        description="🔑 Claim administered licensing subscription subscriptionsClaimKey"
    )
    def validate_administered_licensing_subscription_subscriptions_claim_key(claim_key: str, name: str):
        """Claim claim administered licensing subscription subscriptionsclaimkey."""
        try:
            kwargs = {}
            
            if 'claim_key' in locals():
                kwargs['claimKey'] = claim_key
            if 'name' in locals():
                kwargs['name'] = name
            
            result = meraki_client.dashboard.licensing.validateAdministeredLicensingSubscriptionSubscriptionsClaimKey(**kwargs)
            
            response = f"# 🔑 Claim Administered Licensing Subscription Subscriptionsclaimkey\n\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    # Show first 10 items with licensing-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('claimKey', item.get('id', f'Item {idx}')))
                            response += f"**{idx}. {name}**\n"
                            
                            # Show key licensing-specific fields
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                            if 'expirationDate' in item:
                                response += f"   - Expires: {item.get('expirationDate')}\n"
                            if 'productType' in item:
                                response += f"   - Product: {item.get('productType')}\n"
                            if 'subscription' in item:
                                sub = item.get('subscription', {})
                                if isinstance(sub, dict):
                                    response += f"   - Subscription: {sub.get('name', 'N/A')}\n"
                            if 'counts' in item:
                                counts = item.get('counts', [])
                                if counts:
                                    response += f"   - Counts: {len(counts)} models\n"
                                    
                        else:
                            response += f"**{idx}. {item}**\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show licensing-relevant fields
                    licensing_fields = ['name', 'claimKey', 'status', 'expirationDate', 'productType', 
                                      'subscription', 'counts', 'productTypes', 'networks']
                    
                    for field in licensing_fields:
                        if field in result:
                            value = result[field]
                            if isinstance(value, dict):
                                response += f"- **{field}**: {', '.join(f'{k}: {v}' for k, v in list(value.items())[:3])}\n"
                            elif isinstance(value, list):
                                if field == 'counts' and value:
                                    response += f"- **Counts**: {len(value)} models\n"
                                elif field == 'networks' and value:
                                    response += f"- **Networks**: {len(value)} networks\n"
                                else:
                                    response += f"- **{field}**: {len(value)} items\n"
                            else:
                                response += f"- **{field}**: {value}\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in licensing_fields}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key}**: {value}\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key}**: {len(value)} items\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\n"
                        
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in validate_administered_licensing_subscription_subscriptions_claim_key: {str(e)}"
    
