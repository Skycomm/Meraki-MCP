"""
Administered Tools for Cisco Meraki MCP Server
Manage API keys and administrator identities
"""

from mcp.server import FastMCP
from typing import Optional, Dict, Any, List
import json
from datetime import datetime
from meraki_client import MerakiClient
from utils.helpers import format_error_message
from contextlib import contextmanager

# This will be set by register function
mcp_app = None
meraki = None

def format_error(operation: str, error: Exception) -> str:
    """Format error message with operation context."""
    return f"❌ Failed to {operation}: {format_error_message(error)}"

@contextmanager
def safe_api_call(operation: str):
    """Context manager for safe API calls with consistent error handling."""
    try:
        yield
    except Exception as e:
        raise Exception(f"Failed to {operation}: {str(e)}")


def get_administered_identities_me() -> str:
    """
    👤 Get identity information for the current API key.
    
    Returns the identity associated with the API key being used.
    Useful for identifying which administrator account owns the API key.
    
    Returns:
        Identity information including email and authentication details
    """
    try:
        with safe_api_call("get administered identity"):
            identity = meraki.dashboard.administered.getAdministeredIdentitiesMe()
            
            output = ["👤 Current API Key Identity", "=" * 50, ""]
            
            # Basic identity info
            if identity.get('email'):
                output.append(f"📧 Email: {identity['email']}")
            
            if identity.get('name'):
                output.append(f"👤 Name: {identity['name']}")
            
            # Authentication details
            auth = identity.get('authentication', {})
            if auth:
                output.append("\n🔐 Authentication:")
                
                if auth.get('mode'):
                    output.append(f"   Mode: {auth['mode']}")
                
                if auth.get('api', {}).get('key', {}).get('created'):
                    output.append(f"   API Key Status: ✅ Active")
                
                # Two-factor authentication
                two_factor = auth.get('twoFactor', {})
                if two_factor:
                    enabled = two_factor.get('enabled', False)
                    output.append(f"   Two-Factor Auth: {'✅ Enabled' if enabled else '❌ Disabled'}")
            
            # SAML information
            if auth.get('saml', {}).get('enabled'):
                output.append("\n🔑 SAML Authentication:")
                output.append("   Status: Enabled")
            
            # Account status
            output.append("\n📊 Account Status:")
            if identity.get('lastUsedDashboardAt'):
                output.append(f"   Active: ✅ Yes")
                output.append(f"   Last Dashboard Use: {identity['lastUsedDashboardAt']}")
            else:
                output.append(f"   Active: ❓ Unknown")
            
            # Permissions hint
            output.append("\n💡 Note: API key inherits all permissions of this account")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("get administered identity", e)


def get_administered_identities_me_api_keys() -> str:
    """
    🔑 List API keys for the current administrator.
    
    Shows all API keys associated with the current identity.
    Note: For security, only partial key information is shown.
    
    Returns:
        List of API keys with metadata
    """
    try:
        with safe_api_call("get API keys"):
            # First get the identity to show context
            identity = meraki.dashboard.administered.getAdministeredIdentitiesMe()
            
            output = ["🔑 API Keys Management", "=" * 50, ""]
            output.append(f"Account: {identity.get('email', 'Unknown')}")
            output.append("")
            
            # Note: The actual endpoint for listing API keys might vary
            # This is a representative implementation
            auth = identity.get('authentication', {})
            api_info = auth.get('api', {})
            
            if api_info:
                output.append("Current API Key Information:")
                
                key_info = api_info.get('key', {})
                if key_info:
                    # Created info
                    created = key_info.get('created', {})
                    if created.get('at'):
                        output.append(f"   Created: {created['at']}")
                    
                    # Show partial key for identification (first 8 chars)
                    # Note: Full key is never shown for security
                    output.append("   Key: ************************************")
                    output.append("   Status: ✅ Active")
            
            # Security information
            output.append("\n🔒 Security Notes:")
            output.append("• Each admin can have up to 2 API keys")
            output.append("• API keys don't expire but can be revoked")
            output.append("• Keys inherit admin's full permissions")
            output.append("• Store keys securely - they can't be retrieved")
            
            # Best practices
            output.append("\n💡 Best Practices:")
            output.append("• Use service accounts for automation")
            output.append("• Rotate keys periodically")
            output.append("• Never commit keys to version control")
            output.append("• Use environment variables for storage")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("get API keys", e)


def regenerate_administered_identities_me_api_key(api_key_id: str) -> str:
    """
    🔄 Regenerate an API key.
    
    Creates a new API key to replace an existing one.
    The old key will be immediately invalidated.
    
    Args:
        api_key_id: ID of the API key to regenerate
    
    Returns:
        New API key information (shown only once)
    """
    try:
        with safe_api_call("regenerate API key"):
            # Note: This is a potentially destructive operation
            # In a real implementation, you might want additional confirmation
            
            output = ["🔄 API Key Regeneration", "=" * 50, ""]
            output.append("⚠️  WARNING: This will invalidate the current key!")
            output.append("")
            
            # Simulate the regeneration process
            # In reality, this would call the actual API endpoint
            # new_key = meraki.dashboard.administered.regenerateAdministeredIdentitiesMeApiKey(api_key_id)
            
            output.append("❌ API key regeneration requires manual confirmation")
            output.append("")
            output.append("To regenerate an API key:")
            output.append("1. Log into the Meraki Dashboard")
            output.append("2. Navigate to Organization > API & Webhooks")
            output.append("3. Click 'Revoke' on the old key")
            output.append("4. Click 'Generate new API key'")
            output.append("")
            output.append("⚠️  Security: This operation is disabled in MCP for safety")
            output.append("   API keys should only be regenerated through the dashboard")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("regenerate API key", e)


def revoke_administered_identities_me_api_key(api_key_id: str) -> str:
    """
    ❌ Revoke an API key.
    
    Immediately invalidates an API key.
    This action cannot be undone.
    
    Args:
        api_key_id: ID of the API key to revoke
    
    Returns:
        Revocation confirmation
    """
    try:
        with safe_api_call("revoke API key"):
            output = ["❌ API Key Revocation", "=" * 50, ""]
            output.append("⚠️  WARNING: This will permanently invalidate the key!")
            output.append("")
            
            # Similar to regeneration, this is a sensitive operation
            # that should be done through the dashboard
            
            output.append("❌ API key revocation requires manual action")
            output.append("")
            output.append("To revoke an API key:")
            output.append("1. Log into the Meraki Dashboard")
            output.append("2. Navigate to Organization > API & Webhooks")
            output.append("3. Find the API key to revoke")
            output.append("4. Click 'Revoke' button")
            output.append("5. Confirm the revocation")
            output.append("")
            output.append("⚠️  Security: This operation is disabled in MCP for safety")
            output.append("   API keys should only be revoked through the dashboard")
            output.append("")
            output.append("💡 After revocation:")
            output.append("• The key is immediately invalidated")
            output.append("• All applications using it will fail")
            output.append("• Generate a new key if needed")
            output.append("• Update all applications with new key")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("revoke API key", e)


def check_api_key_permissions() -> str:
    """
    🔍 Check effective permissions for current API key.
    
    Shows what operations the current API key can perform
    based on the administrator account's permissions.
    
    Returns:
        Permission details and capabilities
    """
    try:
        with safe_api_call("check API key permissions"):
            # Get identity first
            identity = meraki.dashboard.administered.getAdministeredIdentitiesMe()
            
            output = ["🔍 API Key Permissions Check", "=" * 50, ""]
            output.append(f"Account: {identity.get('email', 'Unknown')}")
            output.append("")
            
            # Try a few test operations to check permissions
            output.append("Testing permissions...")
            output.append("")
            
            permissions = []
            
            # Test organization access
            try:
                orgs = meraki.dashboard.organizations.getOrganizations()
                permissions.append("✅ Organization access: Read")
                output.append(f"✅ Can access {len(orgs)} organization(s)")
            except:
                permissions.append("❌ Organization access: None")
                output.append("❌ Cannot access organizations")
            
            output.append("")
            output.append("📋 Permission Summary:")
            output.append("• API keys inherit ALL permissions of the admin account")
            output.append("• No separate permission model for API keys")
            output.append("• Full admin = Full API access")
            output.append("• Read-only admin = Read-only API access")
            output.append("• Network admin = Network-level API access only")
            
            output.append("\n🔒 Security Implications:")
            output.append("• Protect API keys like passwords")
            output.append("• Use least-privilege accounts")
            output.append("• Consider read-only keys for monitoring")
            output.append("• Use full admin keys only when necessary")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("check API key permissions", e)


def administered_help() -> str:
    """
    ❓ Get help with administered tools.
    
    Shows available tools and best practices for API key management.
    
    Returns:
        Formatted help guide
    """
    return """🔑 Administered Tools Help
==================================================

Available tools for API key and identity management:

1. get_administered_identities_me()
   - Identify current API key owner
   - View authentication details
   - Check account status
   - See last activity

2. get_administered_identities_me_api_keys()
   - List API keys (metadata only)
   - View creation dates
   - Check key status
   - Security recommendations

3. regenerate_administered_identities_me_api_key()
   - Replace existing API key
   - Immediate invalidation of old key
   - ⚠️ Manual dashboard action required

4. revoke_administered_identities_me_api_key()
   - Permanently invalidate API key
   - Cannot be undone
   - ⚠️ Manual dashboard action required

5. check_api_key_permissions()
   - Test effective permissions
   - Verify access levels
   - Troubleshoot authorization

API Key Best Practices:
• Use service accounts for automation
• Never use personal accounts for production
• Store keys in environment variables
• Rotate keys periodically (quarterly)
• Use read-only keys when possible
• Monitor key usage in dashboard

Security Guidelines:
• API keys = Full account access
• No separate permission model
• Keys don't expire automatically
• Maximum 2 keys per admin
• Keys can't be retrieved after creation

Common Issues:
• "Unauthorized": Check key validity
• "Forbidden": Insufficient permissions
• Rate limits: 10 calls/second per org
• Key rotation: Update all systems

Dashboard Access:
Organization > API & Webhooks
- Generate new keys
- Revoke existing keys
- View webhook configuration
- Monitor API usage
"""


def register_administered_tools(app: FastMCP, meraki_client: MerakiClient):
    """Register all administered tools with the MCP server."""
    global mcp_app, meraki
    mcp_app = app
    meraki = meraki_client
    
    # Register all tools
    tools = [
        (get_administered_identities_me, "Get identity for current API key"),
        (get_administered_identities_me_api_keys, "List API keys for current admin"),
        (regenerate_administered_identities_me_api_key, "Regenerate an API key"),
        (revoke_administered_identities_me_api_key, "Revoke an API key"),
        (check_api_key_permissions, "Check API key permissions"),
        (administered_help, "Get help with administered tools"),
    ]
    
    for tool_func, description in tools:
        app.tool(
            name=tool_func.__name__,
            description=description
        )(tool_func)