"""
Login Security management tools for Cisco Meraki MCP Server.
Handles organization-wide login security settings.
"""

# Global variables to store app and meraki client
app = None
meraki_client = None

def register_login_security_tools(mcp_app, meraki):
    """Register login security tools with the MCP server."""
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    
    # Register all login security tools
    register_login_security_handlers()

def register_login_security_handlers():
    """Register all login security tool handlers using the decorator pattern."""
    
    @app.tool(
        name="get_organization_login_security",
        description="🔐 Get organization login security settings"
    )
    def get_organization_login_security(organization_id: str):
        """Get the login security settings for an organization."""
        try:
            settings = meraki_client.dashboard.organizations.getOrganizationLoginSecurity(organization_id)
            
            result = f"# 🔐 Organization Login Security Settings\n\n"
            
            # Account lockout settings
            result += "## Account Lockout\n"
            result += f"- **Enabled**: {'✅' if settings.get('accountLockoutAttempts') else '❌'}\n"
            if settings.get('accountLockoutAttempts'):
                result += f"- **Failed Attempts**: {settings.get('accountLockoutAttempts')} attempts\n"
                result += f"- **Lockout Duration**: {settings.get('accountLockoutDuration')} minutes\n"
            
            # Idle timeout
            result += "\n## Idle Timeout\n"
            result += f"- **Enabled**: {'✅' if settings.get('idleTimeoutMinutes') else '❌'}\n"
            if settings.get('idleTimeoutMinutes'):
                result += f"- **Timeout**: {settings.get('idleTimeoutMinutes')} minutes\n"
            
            # Two-factor authentication
            result += "\n## Two-Factor Authentication\n"
            result += f"- **Enforced**: {'✅' if settings.get('enforceTwoFactorAuth') else '❌'}\n"
            
            # Password requirements
            result += "\n## Password Requirements\n"
            result += f"- **Strong Passwords**: {'✅' if settings.get('enforceStrongPasswords') else '❌'}\n"
            result += f"- **Password Expiration**: {settings.get('passwordExpirationDays', 'Never')} days\n"
            result += f"- **Different Passwords**: {'✅' if settings.get('enforceDifferentPasswords') else '❌'}\n"
            if settings.get('numDifferentPasswords'):
                result += f"- **Number of Different Passwords**: {settings.get('numDifferentPasswords')}\n"
            
            # Login IP ranges
            if settings.get('loginIpRanges'):
                result += "\n## Allowed Login IP Ranges\n"
                for ip_range in settings['loginIpRanges']:
                    result += f"- {ip_range}\n"
            
            # API authentication
            result += "\n## API Authentication\n"
            api_auth = settings.get('apiAuthentication', {})
            if api_auth:
                result += f"- **IP Restrictions Enforced**: {'✅' if api_auth.get('ipRestrictionsForKeys', {}).get('enabled') else '❌'}\n"
                if api_auth.get('ipRestrictionsForKeys', {}).get('ranges'):
                    result += "- **Allowed API IP Ranges**:\n"
                    for ip_range in api_auth['ipRestrictionsForKeys']['ranges']:
                        result += f"  - {ip_range}\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving login security settings: {str(e)}"
    
    @app.tool(
        name="update_organization_login_security",
        description="🔐 Update organization login security settings"
    )
    def update_organization_login_security(organization_id: str, **kwargs):
        """
        Update the login security settings for an organization.
        
        Args:
            organization_id: Organization ID
            **kwargs: Security settings to update:
                - accountLockoutAttempts: Number of failed attempts before lockout
                - accountLockoutDuration: Lockout duration in minutes
                - idleTimeoutMinutes: Idle timeout in minutes
                - enforceTwoFactorAuth: Require 2FA for all admins
                - enforceStrongPasswords: Require strong passwords
                - passwordExpirationDays: Days before password expires
                - enforceDifferentPasswords: Prevent password reuse
                - numDifferentPasswords: Number of unique passwords required
                - loginIpRanges: List of allowed IP ranges for login
        """
        try:
            result = meraki_client.dashboard.organizations.updateOrganizationLoginSecurity(
                organization_id,
                **kwargs
            )
            
            response = "✅ Login security settings updated successfully!\n\n"
            response += "## Updated Settings\n"
            
            if 'accountLockoutAttempts' in kwargs:
                response += f"- Account lockout after {kwargs['accountLockoutAttempts']} failed attempts\n"
            
            if 'idleTimeoutMinutes' in kwargs:
                response += f"- Idle timeout set to {kwargs['idleTimeoutMinutes']} minutes\n"
            
            if 'enforceTwoFactorAuth' in kwargs:
                response += f"- Two-factor authentication: {'Enforced' if kwargs['enforceTwoFactorAuth'] else 'Optional'}\n"
            
            if 'enforceStrongPasswords' in kwargs:
                response += f"- Strong passwords: {'Required' if kwargs['enforceStrongPasswords'] else 'Optional'}\n"
            
            if 'passwordExpirationDays' in kwargs:
                response += f"- Password expiration: {kwargs['passwordExpirationDays']} days\n"
            
            if 'loginIpRanges' in kwargs:
                response += f"- Login restricted to {len(kwargs['loginIpRanges'])} IP ranges\n"
            
            response += "\n⚠️ **Note**: These changes affect all administrators in the organization."
            
            return response
            
        except Exception as e:
            return f"Error updating login security settings: {str(e)}"