"""
SAML Tools for Cisco Meraki MCP Server
Configure SAML Single Sign-On for dashboard access
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


def get_organization_saml(org_id: str) -> str:
    """
    🔐 Get SAML configuration for organization.
    
    Shows SAML SSO settings for dashboard authentication.
    
    Args:
        org_id: Organization ID
    
    Returns:
        SAML configuration details
    """
    try:
        with safe_api_call("get SAML configuration"):
            saml = meraki.dashboard.organizations.getOrganizationSaml(org_id)
            
            output = ["🔐 SAML Configuration", "=" * 50, ""]
            output.append(f"Organization: {org_id}")
            output.append("")
            
            # SAML enabled status
            enabled = saml.get('enabled', False)
            if enabled:
                output.append("✅ SAML SSO: Enabled")
            else:
                output.append("❌ SAML SSO: Disabled")
                output.append("\n💡 Use update_organization_saml() to enable")
            
            output.append("")
            
            # IdP settings
            output.append("🏢 Identity Provider (IdP) Settings:")
            
            # Consumer URL (Meraki side)
            if saml.get('consumerUrl'):
                output.append(f"   ACS URL: {saml['consumerUrl']}")
            
            # IdP metadata
            if saml.get('idpId'):
                output.append(f"   IdP ID: {saml['idpId']}")
            
            # Login URL
            if saml.get('sloLogoutUrl'):
                output.append(f"   Logout URL: {saml['sloLogoutUrl']}")
            
            # X.509 certificate
            if saml.get('x509certSha1Fingerprint'):
                output.append(f"   Cert Fingerprint: {saml['x509certSha1Fingerprint']}")
            
            output.append("")
            
            # SAML roles
            roles = saml.get('samlRoles', [])
            if roles:
                output.append("👥 SAML Role Mappings:")
                for i, role in enumerate(roles, 1):
                    role_name = role.get('role', 'Unknown')
                    org_access = role.get('orgAccess', 'none')
                    
                    output.append(f"\n{i}. Role: {role_name}")
                    output.append(f"   Organization Access: {org_access}")
                    
                    # Network access
                    networks = role.get('networks', [])
                    if networks:
                        output.append(f"   Networks: {len(networks)} configured")
                        for net in networks[:3]:
                            access = net.get('access', 'none')
                            net_id = net.get('id', 'Unknown')
                            output.append(f"      • {net_id}: {access}")
                        if len(networks) > 3:
                            output.append(f"      ... and {len(networks) - 3} more")
                    
                    # Tags
                    tags = role.get('tags', [])
                    if tags:
                        output.append(f"   Tags: {len(tags)} configured")
                        for tag in tags[:3]:
                            access = tag.get('access', 'none')
                            tag_name = tag.get('tag', 'Unknown')
                            output.append(f"      • {tag_name}: {access}")
            else:
                output.append("⚠️ No SAML role mappings configured")
            
            # URLs for IdP configuration
            output.append("\n🔗 Meraki SAML URLs:")
            output.append(f"• SP Entity ID: https://dashboard.meraki.com")
            output.append(f"• ACS URL: {saml.get('consumerUrl', 'Not available')}")
            
            # Common IdP providers
            output.append("\n🏢 Common Identity Providers:")
            output.append("• Okta")
            output.append("• Azure AD")
            output.append("• Google Workspace")
            output.append("• OneLogin")
            output.append("• Ping Identity")
            output.append("• ADFS")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("get SAML configuration", e)


def update_organization_saml(
    org_id: str,
    enabled: bool,
    idp_id: Optional[str] = None,
    consumer_url: Optional[str] = None,
    slo_logout_url: Optional[str] = None,
    x509_cert_sha1_fingerprint: Optional[str] = None
) -> str:
    """
    ✏️ Update SAML configuration.
    
    Configure SAML SSO settings for dashboard authentication.
    
    Args:
        org_id: Organization ID
        enabled: Enable/disable SAML
        idp_id: Identity Provider entity ID
        consumer_url: Assertion Consumer Service URL
        slo_logout_url: Single Logout URL
        x509_cert_sha1_fingerprint: X.509 certificate fingerprint
    
    Returns:
        Updated SAML configuration
    """
    try:
        with safe_api_call("update SAML configuration"):
            # Build update data
            update_data = {
                "enabled": enabled
            }
            
            if idp_id is not None:
                update_data["idpId"] = idp_id
            
            if consumer_url is not None:
                update_data["consumerUrl"] = consumer_url
            
            if slo_logout_url is not None:
                update_data["sloLogoutUrl"] = slo_logout_url
            
            if x509_cert_sha1_fingerprint is not None:
                update_data["x509certSha1Fingerprint"] = x509_cert_sha1_fingerprint
            
            # Update SAML configuration
            result = meraki.dashboard.organizations.updateOrganizationSaml(
                org_id,
                **update_data
            )
            
            output = ["✏️ SAML Configuration Updated", "=" * 50, ""]
            output.append(f"Organization: {org_id}")
            output.append(f"Status: {'✅ Enabled' if result.get('enabled') else '❌ Disabled'}")
            output.append("")
            
            if result.get('enabled'):
                output.append("🔧 Configuration Summary:")
                if result.get('idpId'):
                    output.append(f"   IdP ID: {result['idpId']}")
                if result.get('consumerUrl'):
                    output.append(f"   ACS URL: {result['consumerUrl']}")
                if result.get('x509certSha1Fingerprint'):
                    output.append(f"   Cert: {result['x509certSha1Fingerprint'][:16]}...")
                
                output.append("\n⚠️ Important Next Steps:")
                output.append("1. Configure SAML roles")
                output.append("2. Test SSO login")
                output.append("3. Verify role mappings")
                output.append("4. Enable for users")
                output.append("5. Disable local auth (optional)")
                
                output.append("\n🔐 Security Notes:")
                output.append("• Keep certificate updated")
                output.append("• Use HTTPS endpoints only")
                output.append("• Test thoroughly before enforcing")
                output.append("• Have break-glass accounts")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("update SAML configuration", e)


def get_organization_saml_roles(org_id: str) -> str:
    """
    👥 Get SAML role mappings.
    
    Shows detailed SAML role configurations and permissions.
    
    Args:
        org_id: Organization ID
    
    Returns:
        SAML role mapping details
    """
    try:
        with safe_api_call("get SAML roles"):
            roles = meraki.dashboard.organizations.getOrganizationSamlRoles(org_id)
            
            output = ["👥 SAML Role Mappings", "=" * 50, ""]
            output.append(f"Organization: {org_id}")
            output.append("")
            
            if not roles:
                output.append("No SAML roles configured")
                output.append("\n💡 Use create_organization_saml_role() to add")
                return "\n".join(output)
            
            output.append(f"Total Roles: {len(roles)}")
            output.append("")
            
            # Show each role
            for i, role in enumerate(roles, 1):
                role_id = role.get('id', 'Unknown')
                role_name = role.get('role', 'Unknown')
                org_access = role.get('orgAccess', 'none')
                
                output.append(f"{i}. 🎭 {role_name}")
                output.append(f"   ID: {role_id}")
                output.append(f"   Org Access: {org_access}")
                
                # Network access
                networks = role.get('networks', [])
                if networks:
                    output.append(f"   Networks: {len(networks)}")
                    
                    # Group by access level
                    access_groups = {}
                    for net in networks:
                        access = net.get('access', 'none')
                        if access not in access_groups:
                            access_groups[access] = []
                        access_groups[access].append(net.get('id', 'Unknown'))
                    
                    for access, net_ids in access_groups.items():
                        output.append(f"      {access}: {len(net_ids)} networks")
                
                # Tag access
                tags = role.get('tags', [])
                if tags:
                    output.append(f"   Tags: {len(tags)}")
                    for tag in tags[:3]:
                        tag_name = tag.get('tag', 'Unknown')
                        access = tag.get('access', 'none')
                        output.append(f"      • {tag_name}: {access}")
                    if len(tags) > 3:
                        output.append(f"      ... and {len(tags) - 3} more")
                
                output.append("")
            
            # Access levels explained
            output.append("📊 Access Levels:")
            output.append("• full - Full admin access")
            output.append("• read-only - View only")
            output.append("• monitor-only - Limited view")
            output.append("• guest-ambassador - AP config only")
            output.append("• none - No access")
            
            # Best practices
            output.append("\n💡 Role Mapping Best Practices:")
            output.append("• Use groups from IdP")
            output.append("• Principle of least privilege")
            output.append("• Regular access reviews")
            output.append("• Document role purposes")
            output.append("• Test before deployment")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("get SAML roles", e)


def create_organization_saml_role(
    org_id: str,
    role: str,
    org_access: str,
    networks: Optional[List[Dict[str, str]]] = None,
    tags: Optional[List[Dict[str, str]]] = None
) -> str:
    """
    ➕ Create SAML role mapping.
    
    Define permissions for SAML authenticated users.
    
    Args:
        org_id: Organization ID
        role: SAML role/group name from IdP
        org_access: Organization access level
        networks: Network access configurations
        tags: Tag-based access configurations
    
    Returns:
        Created SAML role details
    """
    try:
        with safe_api_call("create SAML role"):
            # Build role data
            role_data = {
                "role": role,
                "orgAccess": org_access
            }
            
            if networks:
                role_data["networks"] = networks
            
            if tags:
                role_data["tags"] = tags
            
            # Create the role
            result = meraki.dashboard.organizations.createOrganizationSamlRole(
                org_id,
                **role_data
            )
            
            output = ["✅ SAML Role Created", "=" * 50, ""]
            output.append(f"Role Name: {result.get('role', role)}")
            output.append(f"Role ID: {result.get('id', 'N/A')}")
            output.append(f"Org Access: {result.get('orgAccess', org_access)}")
            output.append("")
            
            # Network access summary
            if networks:
                output.append(f"Network Access: {len(networks)} networks configured")
            
            # Tag access summary
            if tags:
                output.append(f"Tag Access: {len(tags)} tags configured")
            
            output.append("\n🚀 Next Steps:")
            output.append("1. Configure IdP group mapping")
            output.append("2. Add users to IdP group")
            output.append("3. Test authentication")
            output.append("4. Verify permissions")
            output.append("5. Monitor access logs")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("create SAML role", e)


def update_organization_saml_role(
    org_id: str,
    saml_role_id: str,
    role: Optional[str] = None,
    org_access: Optional[str] = None,
    networks: Optional[List[Dict[str, str]]] = None,
    tags: Optional[List[Dict[str, str]]] = None
) -> str:
    """
    ✏️ Update SAML role mapping.
    
    Modify permissions for existing SAML role.
    
    Args:
        org_id: Organization ID
        saml_role_id: SAML role ID
        role: New role/group name
        org_access: New organization access level
        networks: New network access configurations
        tags: New tag-based access configurations
    
    Returns:
        Updated SAML role details
    """
    try:
        with safe_api_call("update SAML role"):
            # Build update data
            update_data = {}
            
            if role is not None:
                update_data["role"] = role
            
            if org_access is not None:
                update_data["orgAccess"] = org_access
            
            if networks is not None:
                update_data["networks"] = networks
            
            if tags is not None:
                update_data["tags"] = tags
            
            # Update the role
            result = meraki.dashboard.organizations.updateOrganizationSamlRole(
                org_id,
                saml_role_id,
                **update_data
            )
            
            output = ["✏️ SAML Role Updated", "=" * 50, ""]
            output.append(f"Role ID: {saml_role_id}")
            output.append(f"Role Name: {result.get('role', 'Unknown')}")
            output.append(f"Org Access: {result.get('orgAccess', 'Unknown')}")
            output.append("")
            
            output.append("✅ Changes Applied")
            
            output.append("\n⚠️ Important:")
            output.append("• Changes affect all users with this role")
            output.append("• Active sessions continue with old permissions")
            output.append("• Users must re-authenticate for changes")
            output.append("• Test with a sample user first")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("update SAML role", e)


def get_organization_saml_role(
    org_id: str,
    saml_role_id: str
) -> str:
    """
    Get a specific SAML role by ID.
    
    Args:
        org_id: Organization ID
        saml_role_id: SAML role ID
    
    Returns:
        SAML role details
    """
    try:
        with safe_api_call("get SAML role"):
            role = meraki.dashboard.organizations.getOrganizationSamlRole(
                org_id,
                saml_role_id
            )
            
            output = ["🎭 SAML Role Details", "=" * 50, ""]
            output.append(f"Role ID: {role.get('id', 'Unknown')}")
            output.append(f"Role Name: {role.get('role', 'Unknown')}")
            output.append(f"Organization Access: {role.get('orgAccess', 'none')}")
            output.append("")
            
            # Network access details
            networks = role.get('networks', [])
            if networks:
                output.append(f"📡 Network Access ({len(networks)} networks):")
                
                # Group by access level
                access_groups = {}
                for net in networks:
                    access = net.get('access', 'none')
                    if access not in access_groups:
                        access_groups[access] = []
                    access_groups[access].append(net.get('id', 'Unknown'))
                
                for access, net_ids in sorted(access_groups.items()):
                    output.append(f"  {access}: {len(net_ids)} networks")
                    for net_id in net_ids[:3]:
                        output.append(f"    • {net_id}")
                    if len(net_ids) > 3:
                        output.append(f"    ... and {len(net_ids) - 3} more")
            else:
                output.append("📡 Network Access: None configured")
            
            output.append("")
            
            # Tag access details
            tags = role.get('tags', [])
            if tags:
                output.append(f"🏷️ Tag Access ({len(tags)} tags):")
                for tag in tags[:5]:
                    tag_name = tag.get('tag', 'Unknown')
                    access = tag.get('access', 'none')
                    output.append(f"  • {tag_name}: {access}")
                if len(tags) > 5:
                    output.append(f"  ... and {len(tags) - 5} more")
            else:
                output.append("🏷️ Tag Access: None configured")
            
            output.append("")
            output.append("💡 To modify this role, use update_organization_saml_role()")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("get SAML role", e)


def delete_organization_saml_role(
    org_id: str,
    saml_role_id: str
) -> str:
    """
    Delete a SAML role mapping.
    
    Args:
        org_id: Organization ID
        saml_role_id: SAML role ID to delete
    
    Returns:
        Deletion confirmation
    """
    try:
        # Get role details first for confirmation
        try:
            role = meraki.dashboard.organizations.getOrganizationSamlRole(
                org_id,
                saml_role_id
            )
            role_name = role.get('role', 'Unknown')
        except:
            role_name = saml_role_id
        
        # Confirmation prompt
        confirmation = input(f"⚠️ Are you sure you want to delete SAML role '{role_name}'? Type 'DELETE' to confirm: ")
        if confirmation != "DELETE":
            return "❌ Deletion cancelled"
        
        with safe_api_call("delete SAML role"):
            meraki.dashboard.organizations.deleteOrganizationSamlRole(
                org_id,
                saml_role_id
            )
            
            output = ["🗑️ SAML Role Deleted", "=" * 50, ""]
            output.append(f"✅ Successfully deleted SAML role: {role_name}")
            output.append(f"   Role ID: {saml_role_id}")
            output.append("")
            output.append("⚠️ Impact:")
            output.append("• Users with this role will lose access")
            output.append("• Active sessions may continue temporarily")
            output.append("• Consider creating replacement role first")
            output.append("")
            output.append("💡 Next Steps:")
            output.append("• Review remaining SAML roles")
            output.append("• Update IdP group mappings")
            output.append("• Notify affected users")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("delete SAML role", e)


def saml_configuration_guide() -> str:
    """
    📚 SAML configuration guide.
    
    Comprehensive guide for setting up SAML SSO.
    
    Returns:
        SAML setup guide with examples
    """
    output = ["📚 SAML Configuration Guide", "=" * 50, ""]
    
    output.append("🚀 Setup Overview:")
    output.append("1. Configure IdP application")
    output.append("2. Enable SAML in Meraki")
    output.append("3. Create role mappings")
    output.append("4. Test authentication")
    output.append("5. Roll out to users")
    output.append("")
    
    output.append("1️⃣ Okta Configuration:")
    output.append("""
# Okta App Settings
- App Type: SAML 2.0
- Single Sign-On URL: https://n1.meraki.com/saml/login/[org_id]/[unique_id]
- Audience URI: https://dashboard.meraki.com
- Name ID Format: EmailAddress
- Application Username: Email

# Attribute Mappings
- username → user.email
- role → groups (filter for Meraki groups)

# Get metadata XML and extract:
- X.509 Certificate
- IdP Issuer
- SSO URL
""")
    
    output.append("\n2️⃣ Azure AD Configuration:")
    output.append("""
# Enterprise App Settings
- Identifier: https://dashboard.meraki.com
- Reply URL: https://n1.meraki.com/saml/login/[org_id]/[unique_id]
- Sign-on URL: Same as Reply URL

# User Attributes
- user.mail → username
- user.groups → role

# Download Federation Metadata XML
""")
    
    output.append("\n3️⃣ Google Workspace:")
    output.append("""
# SAML App Settings
- ACS URL: https://n1.meraki.com/saml/login/[org_id]/[unique_id]
- Entity ID: https://dashboard.meraki.com
- Start URL: https://dashboard.meraki.com
- Name ID: Basic Information > Primary email

# Google Groups for role mapping
""")
    
    output.append("\n4️⃣ Role Mapping Examples:")
    output.append("""
# Full Admin Role
create_organization_saml_role(
    org_id,
    role="meraki-full-admins",  # IdP group name
    org_access="full"
)

# Network-Specific Role
create_organization_saml_role(
    org_id,
    role="meraki-network-admins",
    org_access="none",
    networks=[
        {"id": "L_123456", "access": "full"},
        {"id": "L_789012", "access": "read-only"}
    ]
)

# Tag-Based Role
create_organization_saml_role(
    org_id,
    role="meraki-store-managers",
    org_access="none",
    tags=[
        {"tag": "store", "access": "full"},
        {"tag": "corporate", "access": "read-only"}
    ]
)
""")
    
    output.append("\n5️⃣ Testing Process:")
    output.append("1. Create test IdP user")
    output.append("2. Assign to test group")
    output.append("3. Navigate to dashboard.meraki.com")
    output.append("4. Click 'Log in with SSO'")
    output.append("5. Verify redirect to IdP")
    output.append("6. Authenticate and verify access")
    output.append("7. Check audit logs")
    
    output.append("\n🔧 Troubleshooting:")
    output.append("• Invalid SAML response → Check time sync")
    output.append("• No role match → Verify attribute mapping")
    output.append("• Access denied → Check role permissions")
    output.append("• Cert error → Update fingerprint")
    output.append("• Redirect loop → Clear cookies")
    
    return "\n".join(output)


def saml_help() -> str:
    """
    ❓ Get help with SAML tools.
    
    Shows available tools and best practices.
    
    Returns:
        Formatted help guide
    """
    return """🔐 SAML Tools Help
==================================================

Available tools for SAML configuration:

1. get_organization_saml()
   - View SAML settings
   - Check enabled status
   - See IdP configuration
   - List role mappings

2. update_organization_saml()
   - Enable/disable SAML
   - Configure IdP settings
   - Update certificates
   - Set SSO URLs

3. get_organization_saml_roles()
   - List all roles
   - View permissions
   - Check access levels
   - See assignments

4. create_organization_saml_role()
   - Add role mapping
   - Set permissions
   - Configure access
   - Define scope

5. update_organization_saml_role()
   - Modify roles
   - Change permissions
   - Update access
   - Adjust scope

6. saml_configuration_guide()
   - Setup instructions
   - IdP examples
   - Role templates
   - Testing steps

SAML Concepts:
🏢 IdP - Identity Provider
🎫 SP - Service Provider
📜 Assertion - Auth token
🔐 SSO - Single Sign-On
👤 Principal - User
🎭 Role - Permission set

Common IdPs:
• Okta
• Azure AD
• Google Workspace
• OneLogin
• Ping Identity
• ADFS

Access Levels:
• full - Complete admin
• read-only - View only
• monitor-only - Limited
• guest-ambassador - AP only
• none - No access

Role Scopes:
• Organization-wide
• Specific networks
• Tag-based access
• Combined permissions

Best Practices:
• Use groups from IdP
• Least privilege principle
• Regular access reviews
• Test before enforcing
• Keep break-glass accounts
• Monitor login activity

Security Notes:
• HTTPS only
• Valid certificates
• Time synchronization
• Secure metadata
• Audit logging
• MFA recommended

Troubleshooting:
• Check SAML response
• Verify attributes
• Test role matching
• Review audit logs
• Clear browser cache
• Check time sync

Common Issues:
• No role match
• Invalid response
• Certificate mismatch
• Attribute missing
• Time skew
• Redirect loops
"""


def register_saml_tools(app: FastMCP, meraki_client: MerakiClient):
    """Register all SAML tools with the MCP server."""
    global mcp_app, meraki
    mcp_app = app
    meraki = meraki_client
    
    # Register all tools
    tools = [
        (get_organization_saml, "Get SAML configuration"),
        (update_organization_saml, "Update SAML settings"),
        (get_organization_saml_roles, "List SAML role mappings"),
        (create_organization_saml_role, "Create SAML role"),
        (get_organization_saml_role, "Get specific SAML role"),
        (update_organization_saml_role, "Update SAML role"),
        (delete_organization_saml_role, "Delete SAML role"),
        (saml_configuration_guide, "SAML setup guide"),
        (saml_help, "Get help with SAML tools"),
    ]
    
    for tool_func, description in tools:
        app.tool(
            name=tool_func.__name__,
            description=description
        )(tool_func)