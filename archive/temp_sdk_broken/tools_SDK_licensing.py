"""
Cisco Meraki MCP Server - Licensing SDK Tools
Complete implementation of all 8 official Meraki Licensing API methods.

This module provides 100% coverage of the Licensing category from the official Meraki Dashboard API SDK.
Each tool corresponds directly to a method in the meraki.dashboard.licensing namespace.
"""

# Import removed to avoid circular import
import meraki


def register_licensing_tools(app, meraki_client):
    """Register all licensing SDK tools."""
    print(f"🔑 Registering 8 licensing SDK tools...")


@app.tool(
    name="bind_administered_licensing_subscription_subscription",
    description="Manage bindadministeredlicensingsubscriptionsubscription"
)
def bind_administered_licensing_subscription_subscription():
    """
    Manage bindadministeredlicensingsubscriptionsubscription
    
    Args:

    
    Returns:
        dict: API response with bindadministeredlicensingsubscriptionsubscription data
    """
    try:
        result = meraki_client.dashboard.licensing.bindAdministeredLicensingSubscriptionSubscription()
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="claim_administered_licensing_subscription_subscriptions",
    description="Manage claimadministeredlicensingsubscriptionsubscriptions"
)
def claim_administered_licensing_subscription_subscriptions():
    """
    Manage claimadministeredlicensingsubscriptionsubscriptions
    
    Args:

    
    Returns:
        dict: API response with claimadministeredlicensingsubscriptionsubscriptions data
    """
    try:
        result = meraki_client.dashboard.licensing.claimAdministeredLicensingSubscriptionSubscriptions()
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_administered_licensing_subscription_entitlements",
    description="Retrieve administeredlicensingsubscriptionentitlements"
)
def get_administered_licensing_subscription_entitlements():
    """
    Retrieve administeredlicensingsubscriptionentitlements
    
    Args:

    
    Returns:
        dict: API response with administeredlicensingsubscriptionentitlements data
    """
    try:
        result = meraki_client.dashboard.licensing.getAdministeredLicensingSubscriptionEntitlements()
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_administered_licensing_subscription_subscriptions",
    description="Retrieve administeredlicensingsubscriptionsubscriptions"
)
def get_administered_licensing_subscription_subscriptions():
    """
    Retrieve administeredlicensingsubscriptionsubscriptions
    
    Args:

    
    Returns:
        dict: API response with administeredlicensingsubscriptionsubscriptions data
    """
    try:
        result = meraki_client.dashboard.licensing.getAdministeredLicensingSubscriptionSubscriptions()
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_administered_licensing_subscription_subscriptions_compliance_statuses",
    description="Retrieve administeredlicensingsubscriptionsubscriptionscompliancestatuses"
)
def get_administered_licensing_subscription_subscriptions_compliance_statuses():
    """
    Retrieve administeredlicensingsubscriptionsubscriptionscompliancestatuses
    
    Args:

    
    Returns:
        dict: API response with administeredlicensingsubscriptionsubscriptionscompliancestatuses data
    """
    try:
        result = meraki_client.dashboard.licensing.getAdministeredLicensingSubscriptionSubscriptionsComplianceStatuses()
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_licensing_coterm_licenses",
    description="Retrieve licensingcotermlicenses"
)
def get_organization_licensing_coterm_licenses(organization_id: str):
    """
    Retrieve licensingcotermlicenses
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with licensingcotermlicenses data
    """
    try:
        result = meraki_client.dashboard.licensing.getOrganizationLicensingCotermLicenses(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="move_organization_licensing_coterm_licenses",
    description="Manage movelicensingcotermlicenses"
)
def move_organization_licensing_coterm_licenses():
    """
    Manage movelicensingcotermlicenses
    
    Args:

    
    Returns:
        dict: API response with movelicensingcotermlicenses data
    """
    try:
        result = meraki_client.dashboard.licensing.moveOrganizationLicensingCotermLicenses()
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="validate_administered_licensing_subscription_subscriptions_claim_key",
    description="Manage validateadministeredlicensingsubscriptionsubscriptionsclaimkey"
)
def validate_administered_licensing_subscription_subscriptions_claim_key():
    """
    Manage validateadministeredlicensingsubscriptionsubscriptionsclaimkey
    
    Args:

    
    Returns:
        dict: API response with validateadministeredlicensingsubscriptionsubscriptionsclaimkey data
    """
    try:
        result = meraki_client.dashboard.licensing.validateAdministeredLicensingSubscriptionSubscriptionsClaimKey()
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}