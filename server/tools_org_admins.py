"""
Organization Admins management tools for Cisco Meraki MCP Server.
Handles administrator accounts and permissions.
"""

# Global variables to store app and meraki client
app = None
meraki_client = None

def register_org_admins_tools(mcp_app, meraki):
    """Register organization admins tools with the MCP server."""
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    
    # Register all org admins tools
    register_org_admins_handlers()

def register_org_admins_handlers():
    """Register all organization admins tool handlers using the decorator pattern."""
    
    @app.tool(
        name="get_organization_admins",
        description="👤 List all administrators for an organization"
    )
    def get_organization_admins(organization_id: str):
        """List all administrators for an organization."""
        try:
            admins = meraki_client.dashboard.organizations.getOrganizationAdmins(organization_id)
            
            if not admins:
                return f"No administrators found for organization {organization_id}."
            
            result = f"# 👤 Organization Administrators\n\n"
            result += f"**Total Admins**: {len(admins)}\n\n"
            
            for admin in admins:
                result += f"## {admin.get('name', 'Unknown')}\n"
                result += f"- **Email**: {admin.get('email')}\n"
                result += f"- **ID**: {admin.get('id')}\n"
                result += f"- **Org Access**: {admin.get('orgAccess', 'none')}\n"
                
                if admin.get('networks'):
                    result += f"- **Network Access**:\n"
                    for network in admin['networks'][:5]:
                        result += f"  - {network.get('name')} ({network.get('access')})\n"
                    if len(admin['networks']) > 5:
                        result += f"  ... and {len(admin['networks']) - 5} more networks\n"
                
                if admin.get('tags'):
                    result += f"- **Tag Access**:\n"
                    for tag in admin['tags'][:5]:
                        result += f"  - {tag.get('tag')} ({tag.get('access')})\n"
                
                result += f"- **Two Factor Auth**: {'✅' if admin.get('twoFactorAuthEnabled') else '❌'}\n"
                result += f"- **Account Status**: {admin.get('accountStatus', 'active')}\n"
                result += f"- **Last Active**: {admin.get('lastActive', 'Unknown')}\n\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving organization admins: {str(e)}"
    
    @app.tool(
        name="create_organization_admin",
        description="👤 Create a new organization administrator"
    )
    def create_organization_admin(
        organization_id: str, 
        email: str, 
        name: str, 
        orgAccess: str,
        **kwargs
    ):
        """
        Create a new organization administrator.
        
        Args:
            organization_id: Organization ID
            email: Admin email address
            name: Admin name
            orgAccess: Access level ('full', 'read-only', 'none')
            **kwargs: Additional parameters (networks, tags, etc.)
        """
        try:
            result = meraki_client.dashboard.organizations.createOrganizationAdmin(
                organization_id,
                email=email,
                name=name,
                orgAccess=orgAccess,
                **kwargs
            )
            
            return f"""✅ Administrator created successfully!

**Name**: {result.get('name')}
**Email**: {result.get('email')}
**Access Level**: {result.get('orgAccess')}
**ID**: {result.get('id')}

The administrator will receive an email invitation to activate their account."""
            
        except Exception as e:
            return f"Error creating organization admin: {str(e)}"
    
    @app.tool(
        name="update_organization_admin",
        description="👤 Update an organization administrator"
    )
    def update_organization_admin(
        organization_id: str,
        admin_id: str,
        **kwargs
    ):
        """
        Update an organization administrator.
        
        Args:
            organization_id: Organization ID
            admin_id: Administrator ID
            **kwargs: Parameters to update (name, orgAccess, networks, tags)
        """
        try:
            result = meraki_client.dashboard.organizations.updateOrganizationAdmin(
                organization_id,
                admin_id,
                **kwargs
            )
            
            return f"""✅ Administrator updated successfully!

**Name**: {result.get('name')}
**Email**: {result.get('email')}
**Access Level**: {result.get('orgAccess')}
**Last Updated**: Now"""
            
        except Exception as e:
            return f"Error updating organization admin: {str(e)}"
    
    @app.tool(
        name="delete_organization_admin",
        description="👤 Delete an organization administrator"
    )
    def delete_organization_admin(organization_id: str, admin_id: str):
        """Delete an organization administrator."""
        try:
            meraki_client.dashboard.organizations.deleteOrganizationAdmin(
                organization_id,
                admin_id
            )
            
            return f"✅ Administrator deleted successfully!"
            
        except Exception as e:
            return f"Error deleting organization admin: {str(e)}"
    
    @app.tool(
        name="revoke_organization_admin",
        description="👤 Revoke an organization administrator's access"
    )
    def revoke_organization_admin(organization_id: str, admin_id: str):
        """Revoke an organization administrator's access without deleting the account."""
        try:
            # Revoke by setting orgAccess to 'none'
            result = meraki_client.dashboard.organizations.updateOrganizationAdmin(
                organization_id,
                admin_id,
                orgAccess='none'
            )
            
            return f"""✅ Administrator access revoked!

**Name**: {result.get('name')}
**Email**: {result.get('email')}
**Access Level**: Revoked (none)

The administrator account still exists but has no access to the organization."""
            
        except Exception as e:
            return f"Error revoking organization admin access: {str(e)}"