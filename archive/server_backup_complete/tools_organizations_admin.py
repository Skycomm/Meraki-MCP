"""
Admin and SAML management tools for Cisco Meraki MCP server.

This module provides tools for managing organization admins and SAML/SSO configuration.
"""

from typing import Optional, Dict, Any, List
from datetime import datetime
import json

# Global references to be set by register function
app = None
meraki_client = None

def register_admin_tools(mcp_app, meraki):
    """
    Register admin tools with the MCP server.
    
    Args:
        mcp_app: MCP server instance
        meraki: Meraki client instance
    """
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    
    # ==================== ADMIN MANAGEMENT ====================
    
    @app.tool(
        name="get_org_admins",
        description="👤 List all dashboard administrators in an organization"
    )
    def get_org_admins(
        organization_id: str
    ):
        """Get all organization admins."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationAdmins(
                organization_id
            )
            
            response = f"# 👤 Organization Administrators\n\n"
            
            if result and isinstance(result, list):
                response += f"**Total Admins**: {len(result)}\n\n"
                
                for admin in result:
                    response += f"## {admin.get('name', 'Unknown')}\n"
                    response += f"- **Email**: {admin.get('email', 'N/A')}\n"
                    response += f"- **ID**: {admin.get('id', 'N/A')}\n"
                    response += f"- **Org Access**: {admin.get('orgAccess', 'N/A')}\n"
                    
                    # Networks
                    networks = admin.get('networks', [])
                    if networks:
                        response += f"- **Network Access**: {len(networks)} networks\n"
                        for net in networks[:3]:
                            response += f"  - {net.get('id', 'N/A')}: {net.get('access', 'N/A')}\n"
                        if len(networks) > 3:
                            response += f"  ... and {len(networks)-3} more\n"
                    
                    # Tags
                    tags = admin.get('tags', [])
                    if tags:
                        response += f"- **Tag Access**: {len(tags)} tags\n"
                        for tag in tags[:3]:
                            response += f"  - {tag.get('tag', 'N/A')}: {tag.get('access', 'N/A')}\n"
                        if len(tags) > 3:
                            response += f"  ... and {len(tags)-3} more\n"
                    
                    response += f"- **Two-Factor Auth**: {admin.get('twoFactorAuthEnabled', False)}\n"
                    response += f"- **API Key**: {'Yes' if admin.get('hasApiKey', False) else 'No'}\n"
                    response += f"- **Last Active**: {admin.get('lastActive', 'N/A')}\n\n"
            else:
                response += "*No admins found*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting admins: {str(e)}"
    
    @app.tool(
        name="create_org_admin",
        description="👤➕ Create a new dashboard administrator"
    )
    def create_org_admin(
        organization_id: str,
        email: str,
        name: str,
        org_access: str,
        networks: Optional[str] = None,
        tags: Optional[str] = None,
        authentication_method: str = "Email"
    ):
        """
        Create a new organization admin.
        
        Args:
            organization_id: Organization ID
            email: Admin email
            name: Admin name
            org_access: Organization access level (full, read-only, none)
            networks: JSON string of network access array
            tags: JSON string of tag access array
            authentication_method: Authentication method (Email, Cisco SecureX Sign-On)
        """
        try:
            kwargs = {
                'email': email,
                'name': name,
                'orgAccess': org_access,
                'authenticationMethod': authentication_method
            }
            
            if networks:
                kwargs['networks'] = json.loads(networks) if isinstance(networks, str) else networks
            if tags:
                kwargs['tags'] = json.loads(tags) if isinstance(tags, str) else tags
            
            result = meraki_client.dashboard.organizations.createOrganizationAdmin(
                organization_id, **kwargs
            )
            
            response = f"# ✅ Created Admin\n\n"
            response += f"**Name**: {result.get('name', name)}\n"
            response += f"**Email**: {result.get('email', email)}\n"
            response += f"**ID**: {result.get('id', 'N/A')}\n"
            response += f"**Org Access**: {org_access}\n"
            
            return response
        except Exception as e:
            return f"❌ Error creating admin: {str(e)}"
    
    @app.tool(
        name="update_org_admin",
        description="👤✏️ Update a dashboard administrator"
    )
    def update_org_admin(
        organization_id: str,
        admin_id: str,
        name: Optional[str] = None,
        org_access: Optional[str] = None,
        networks: Optional[str] = None,
        tags: Optional[str] = None
    ):
        """Update an organization admin."""
        try:
            kwargs = {}
            
            if name:
                kwargs['name'] = name
            if org_access:
                kwargs['orgAccess'] = org_access
            if networks:
                kwargs['networks'] = json.loads(networks) if isinstance(networks, str) else networks
            if tags:
                kwargs['tags'] = json.loads(tags) if isinstance(tags, str) else tags
            
            result = meraki_client.dashboard.organizations.updateOrganizationAdmin(
                organization_id, admin_id, **kwargs
            )
            
            response = f"# ✅ Updated Admin\n\n"
            response += f"**Name**: {result.get('name', 'Unknown')}\n"
            response += f"**ID**: {admin_id}\n"
            
            return response
        except Exception as e:
            return f"❌ Error updating admin: {str(e)}"
    
    @app.tool(
        name="delete_org_admin",
        description="👤❌ Delete a dashboard administrator"
    )
    def delete_org_admin(
        organization_id: str,
        admin_id: str
    ):
        """Delete an organization admin."""
        try:
            meraki_client.dashboard.organizations.deleteOrganizationAdmin(
                organization_id, admin_id
            )
            
            response = f"# ✅ Deleted Admin\n\n"
            response += f"**Admin ID**: {admin_id}\n"
            
            return response
        except Exception as e:
            return f"❌ Error deleting admin: {str(e)}"
    
    @app.tool(
        name="revoke_org_admin_api_key",
        description="🔑❌ Revoke an admin's API key"
    )
    def revoke_org_admin_api_key(
        organization_id: str,
        admin_id: str
    ):
        """Revoke an admin's API key."""
        try:
            meraki_client.dashboard.organizations.revokeOrganizationAdminApiKey(
                organization_id, admin_id
            )
            
            response = f"# ✅ Revoked API Key\n\n"
            response += f"**Admin ID**: {admin_id}\n"
            response += "The admin's API key has been revoked.\n"
            
            return response
        except Exception as e:
            return f"❌ Error revoking API key: {str(e)}"
    
    # ==================== SAML CONFIGURATION ====================
    
    @app.tool(
        name="get_org_saml",
        description="🔐 Get SAML SSO configuration for an organization"
    )
    def get_org_saml(
        organization_id: str
    ):
        """Get SAML configuration."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationSaml(
                organization_id
            )
            
            response = f"# 🔐 SAML Configuration\n\n"
            
            if result:
                response += f"**Enabled**: {result.get('enabled', False)}\n\n"
                
                if result.get('enabled'):
                    response += "## Configuration\n"
                    
                    # Consumer URL
                    response += f"- **Consumer URL**: {result.get('consumerUrl', 'N/A')}\n"
                    
                    # IdPs
                    idps = result.get('idps', [])
                    if idps:
                        response += f"\n## Identity Providers ({len(idps)})\n"
                        for idp in idps:
                            response += f"### {idp.get('name', 'Unknown')}\n"
                            response += f"- **SSO URL**: {idp.get('ssoUrl', 'N/A')}\n"
                            response += f"- **Certificate**: {'Present' if idp.get('certificate') else 'Not configured'}\n"
                            response += f"- **Sign-On URL**: {idp.get('signOnUrl', 'N/A')}\n"
                            response += f"- **Logout URL**: {idp.get('logoutUrl', 'N/A')}\n\n"
            else:
                response += "*SAML not configured*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting SAML configuration: {str(e)}"
    
    @app.tool(
        name="update_org_saml",
        description="🔐✏️ Update SAML SSO configuration"
    )
    def update_org_saml(
        organization_id: str,
        enabled: Optional[bool] = None
    ):
        """
        Update SAML configuration.
        
        Args:
            organization_id: Organization ID
            enabled: Enable/disable SAML
        """
        try:
            kwargs = {}
            
            if enabled is not None:
                kwargs['enabled'] = enabled
            
            result = meraki_client.dashboard.organizations.updateOrganizationSaml(
                organization_id, **kwargs
            )
            
            response = f"# ✅ Updated SAML Configuration\n\n"
            response += f"**Enabled**: {result.get('enabled', False)}\n"
            
            return response
        except Exception as e:
            return f"❌ Error updating SAML: {str(e)}"
    
    @app.tool(
        name="get_org_saml_roles",
        description="🔐👥 List SAML roles for an organization"
    )
    def get_org_saml_roles(
        organization_id: str
    ):
        """Get SAML roles."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationSamlRoles(
                organization_id
            )
            
            response = f"# 🔐 SAML Roles\n\n"
            
            if result and isinstance(result, list):
                response += f"**Total Roles**: {len(result)}\n\n"
                
                for role in result:
                    response += f"## {role.get('role', 'Unknown')}\n"
                    response += f"- **ID**: {role.get('id', 'N/A')}\n"
                    response += f"- **Org Access**: {role.get('orgAccess', 'N/A')}\n"
                    
                    # Networks
                    networks = role.get('networks', [])
                    if networks:
                        response += f"- **Network Access**: {len(networks)} networks\n"
                    
                    # Tags
                    tags = role.get('tags', [])
                    if tags:
                        response += f"- **Tag Access**: {len(tags)} tags\n"
                    
                    response += "\n"
            else:
                response += "*No SAML roles found*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting SAML roles: {str(e)}"
    
    @app.tool(
        name="get_org_saml_role",
        description="🔐👥 Get details of a specific SAML role"
    )
    def get_org_saml_role(
        organization_id: str,
        role_id: str
    ):
        """Get specific SAML role details."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationSamlRole(
                organization_id, role_id
            )
            
            response = f"# 🔐 SAML Role Details\n\n"
            
            if result:
                response += f"**Role**: {result.get('role', 'Unknown')}\n"
                response += f"**ID**: {result.get('id', 'N/A')}\n"
                response += f"**Org Access**: {result.get('orgAccess', 'N/A')}\n\n"
                
                # Networks
                networks = result.get('networks', [])
                if networks:
                    response += f"## Network Access ({len(networks)})\n"
                    for net in networks:
                        response += f"- **{net.get('id', 'N/A')}**: {net.get('access', 'N/A')}\n"
                
                # Tags
                tags = result.get('tags', [])
                if tags:
                    response += f"\n## Tag Access ({len(tags)})\n"
                    for tag in tags:
                        response += f"- **{tag.get('tag', 'N/A')}**: {tag.get('access', 'N/A')}\n"
            else:
                response += "*Role not found*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting role: {str(e)}"
    
    @app.tool(
        name="create_org_saml_role",
        description="🔐👥➕ Create a new SAML role"
    )
    def create_org_saml_role(
        organization_id: str,
        role: str,
        org_access: str,
        networks: Optional[str] = None,
        tags: Optional[str] = None
    ):
        """
        Create a new SAML role.
        
        Args:
            organization_id: Organization ID
            role: Role name
            org_access: Organization access level
            networks: JSON string of network access array
            tags: JSON string of tag access array
        """
        try:
            kwargs = {
                'role': role,
                'orgAccess': org_access
            }
            
            if networks:
                kwargs['networks'] = json.loads(networks) if isinstance(networks, str) else networks
            if tags:
                kwargs['tags'] = json.loads(tags) if isinstance(tags, str) else tags
            
            result = meraki_client.dashboard.organizations.createOrganizationSamlRole(
                organization_id, **kwargs
            )
            
            response = f"# ✅ Created SAML Role\n\n"
            response += f"**Role**: {result.get('role', role)}\n"
            response += f"**ID**: {result.get('id', 'N/A')}\n"
            response += f"**Org Access**: {org_access}\n"
            
            return response
        except Exception as e:
            return f"❌ Error creating SAML role: {str(e)}"
    
    @app.tool(
        name="update_org_saml_role",
        description="🔐👥✏️ Update a SAML role"
    )
    def update_org_saml_role(
        organization_id: str,
        role_id: str,
        role: Optional[str] = None,
        org_access: Optional[str] = None,
        networks: Optional[str] = None,
        tags: Optional[str] = None
    ):
        """Update a SAML role."""
        try:
            kwargs = {}
            
            if role:
                kwargs['role'] = role
            if org_access:
                kwargs['orgAccess'] = org_access
            if networks:
                kwargs['networks'] = json.loads(networks) if isinstance(networks, str) else networks
            if tags:
                kwargs['tags'] = json.loads(tags) if isinstance(tags, str) else tags
            
            result = meraki_client.dashboard.organizations.updateOrganizationSamlRole(
                organization_id, role_id, **kwargs
            )
            
            response = f"# ✅ Updated SAML Role\n\n"
            response += f"**Role**: {result.get('role', 'Unknown')}\n"
            response += f"**ID**: {role_id}\n"
            
            return response
        except Exception as e:
            return f"❌ Error updating SAML role: {str(e)}"
    
    @app.tool(
        name="delete_org_saml_role",
        description="🔐👥❌ Delete a SAML role"
    )
    def delete_org_saml_role(
        organization_id: str,
        role_id: str
    ):
        """Delete a SAML role."""
        try:
            meraki_client.dashboard.organizations.deleteOrganizationSamlRole(
                organization_id, role_id
            )
            
            response = f"# ✅ Deleted SAML Role\n\n"
            response += f"**Role ID**: {role_id}\n"
            
            return response
        except Exception as e:
            return f"❌ Error deleting SAML role: {str(e)}"
    
    @app.tool(
        name="get_org_saml_idps",
        description="🔐🏢 List SAML Identity Providers for an organization"
    )
    def get_org_saml_idps(
        organization_id: str
    ):
        """Get SAML Identity Providers."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationSamlIdps(
                organization_id
            )
            
            response = f"# 🔐 SAML Identity Providers\n\n"
            
            if result and isinstance(result, list):
                response += f"**Total IdPs**: {len(result)}\n\n"
                
                for idp in result:
                    response += f"## {idp.get('name', 'Unknown')}\n"
                    response += f"- **ID**: {idp.get('idpId', 'N/A')}\n"
                    response += f"- **SSO URL**: {idp.get('ssoUrl', 'N/A')}\n"
                    response += f"- **Sign-On URL**: {idp.get('signOnUrl', 'N/A')}\n"
                    response += f"- **Logout URL**: {idp.get('logoutUrl', 'N/A')}\n"
                    response += f"- **Certificate**: {'Present' if idp.get('x509certSha1Fingerprint') else 'Not configured'}\n\n"
            else:
                response += "*No SAML IdPs found*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting SAML IdPs: {str(e)}"
    
    @app.tool(
        name="create_org_saml_idp",
        description="🔐🏢➕ Create a new SAML Identity Provider"
    )
    def create_org_saml_idp(
        organization_id: str,
        x509cert_sha1_fingerprint: str,
        consumer_url: Optional[str] = None,
        idp_entity_id: Optional[str] = None,
        sso_url: Optional[str] = None
    ):
        """
        Create a new SAML IdP.
        
        Args:
            organization_id: Organization ID
            x509cert_sha1_fingerprint: X.509 certificate SHA1 fingerprint
            consumer_url: SAML consumer URL
            idp_entity_id: IdP entity ID
            sso_url: SSO URL
        """
        try:
            kwargs = {
                'x509certSha1Fingerprint': x509cert_sha1_fingerprint
            }
            
            if consumer_url:
                kwargs['consumerUrl'] = consumer_url
            if idp_entity_id:
                kwargs['idpEntityId'] = idp_entity_id
            if sso_url:
                kwargs['ssoUrl'] = sso_url
            
            result = meraki_client.dashboard.organizations.createOrganizationSamlIdp(
                organization_id, **kwargs
            )
            
            response = f"# ✅ Created SAML IdP\n\n"
            response += f"**ID**: {result.get('idpId', 'N/A')}\n"
            response += f"**Certificate**: {x509cert_sha1_fingerprint[:20]}...\n"
            
            return response
        except Exception as e:
            return f"❌ Error creating SAML IdP: {str(e)}"
    
    @app.tool(
        name="update_org_saml_idp",
        description="🔐🏢✏️ Update a SAML Identity Provider"
    )
    def update_org_saml_idp(
        organization_id: str,
        idp_id: str,
        x509cert_sha1_fingerprint: Optional[str] = None,
        consumer_url: Optional[str] = None,
        idp_entity_id: Optional[str] = None,
        sso_url: Optional[str] = None
    ):
        """Update a SAML IdP."""
        try:
            kwargs = {}
            
            if x509cert_sha1_fingerprint:
                kwargs['x509certSha1Fingerprint'] = x509cert_sha1_fingerprint
            if consumer_url:
                kwargs['consumerUrl'] = consumer_url
            if idp_entity_id:
                kwargs['idpEntityId'] = idp_entity_id
            if sso_url:
                kwargs['ssoUrl'] = sso_url
            
            result = meraki_client.dashboard.organizations.updateOrganizationSamlIdp(
                organization_id, idp_id, **kwargs
            )
            
            response = f"# ✅ Updated SAML IdP\n\n"
            response += f"**ID**: {idp_id}\n"
            
            return response
        except Exception as e:
            return f"❌ Error updating SAML IdP: {str(e)}"
    
    @app.tool(
        name="delete_org_saml_idp",
        description="🔐🏢❌ Delete a SAML Identity Provider"
    )
    def delete_org_saml_idp(
        organization_id: str,
        idp_id: str
    ):
        """Delete a SAML IdP."""
        try:
            meraki_client.dashboard.organizations.deleteOrganizationSamlIdp(
                organization_id, idp_id
            )
            
            response = f"# ✅ Deleted SAML IdP\n\n"
            response += f"**IdP ID**: {idp_id}\n"
            
            return response
        except Exception as e:
            return f"❌ Error deleting SAML IdP: {str(e)}"