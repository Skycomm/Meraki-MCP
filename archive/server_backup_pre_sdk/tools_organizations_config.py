"""
Configuration templates and branding tools for Cisco Meraki MCP server.

This module provides tools for managing organization config templates and branding policies.
"""

from typing import Optional, Dict, Any, List
import json

# Global references
app = None
meraki_client = None

def register_config_tools(mcp_app, meraki):
    """Register configuration tools with the MCP server."""
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    
    # ==================== CONFIG TEMPLATES ====================
    
    @app.tool(
        name="get_org_config_templates",
        description="📋 List all configuration templates in an organization"
    )
    def get_org_config_templates(
        organization_id: str
    ):
        """Get all configuration templates."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationConfigTemplates(
                organization_id
            )
            
            response = f"# 📋 Configuration Templates\n\n"
            
            if result and isinstance(result, list):
                response += f"**Total Templates**: {len(result)}\n\n"
                
                for template in result:
                    response += f"## {template.get('name', 'Unnamed')}\n"
                    response += f"- **ID**: {template.get('id', 'N/A')}\n"
                    response += f"- **Product Types**: {', '.join(template.get('productTypes', []))}\n"
                    response += f"- **Time Zone**: {template.get('timeZone', 'N/A')}\n"
                    
                    # Bound networks count
                    if 'isBoundToConfigTemplate' in template:
                        response += f"- **Is Bound**: {template['isBoundToConfigTemplate']}\n"
                    
                    response += "\n"
            else:
                response += "*No configuration templates found*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting templates: {str(e)}"
    
    @app.tool(
        name="get_org_config_template",
        description="📋 Get details of a specific configuration template"
    )
    def get_org_config_template(
        organization_id: str,
        config_template_id: str
    ):
        """Get specific configuration template details."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationConfigTemplate(
                organization_id, config_template_id
            )
            
            response = f"# 📋 Configuration Template Details\n\n"
            
            if result:
                response += f"**Name**: {result.get('name', 'Unnamed')}\n"
                response += f"**ID**: {result.get('id', 'N/A')}\n"
                response += f"**Product Types**: {', '.join(result.get('productTypes', []))}\n"
                response += f"**Time Zone**: {result.get('timeZone', 'N/A')}\n\n"
                
                # Copy from networks
                if result.get('copyFromNetworkId'):
                    response += f"## Source Network\n"
                    response += f"- **Network ID**: {result['copyFromNetworkId']}\n\n"
            else:
                response += "*Template not found*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting template: {str(e)}"
    
    @app.tool(
        name="create_org_config_template",
        description="📋➕ Create a new configuration template"
    )
    def create_org_config_template(
        organization_id: str,
        name: str,
        time_zone: str,
        copy_from_network_id: Optional[str] = None
    ):
        """
        Create a new configuration template.
        
        Args:
            organization_id: Organization ID
            name: Template name
            time_zone: Time zone (e.g., 'America/Los_Angeles')
            copy_from_network_id: Network ID to copy settings from
        """
        try:
            kwargs = {
                'name': name,
                'timeZone': time_zone
            }
            
            if copy_from_network_id:
                kwargs['copyFromNetworkId'] = copy_from_network_id
            
            result = meraki_client.dashboard.organizations.createOrganizationConfigTemplate(
                organization_id, **kwargs
            )
            
            response = f"# ✅ Created Configuration Template\n\n"
            response += f"**Name**: {name}\n"
            response += f"**ID**: {result.get('id', 'N/A')}\n"
            response += f"**Time Zone**: {time_zone}\n"
            
            return response
        except Exception as e:
            return f"❌ Error creating template: {str(e)}"
    
    @app.tool(
        name="update_org_config_template",
        description="📋✏️ Update a configuration template"
    )
    def update_org_config_template(
        organization_id: str,
        config_template_id: str,
        name: Optional[str] = None,
        time_zone: Optional[str] = None
    ):
        """Update a configuration template."""
        try:
            kwargs = {}
            
            if name:
                kwargs['name'] = name
            if time_zone:
                kwargs['timeZone'] = time_zone
            
            result = meraki_client.dashboard.organizations.updateOrganizationConfigTemplate(
                organization_id, config_template_id, **kwargs
            )
            
            response = f"# ✅ Updated Configuration Template\n\n"
            response += f"**Template ID**: {config_template_id}\n"
            
            return response
        except Exception as e:
            return f"❌ Error updating template: {str(e)}"
    
    @app.tool(
        name="delete_org_config_template",
        description="📋❌ Delete a configuration template"
    )
    def delete_org_config_template(
        organization_id: str,
        config_template_id: str
    ):
        """Delete a configuration template."""
        try:
            meraki_client.dashboard.organizations.deleteOrganizationConfigTemplate(
                organization_id, config_template_id
            )
            
            response = f"# ✅ Deleted Configuration Template\n\n"
            response += f"**Template ID**: {config_template_id}\n"
            
            return response
        except Exception as e:
            return f"❌ Error deleting template: {str(e)}"
    
    @app.tool(
        name="get_org_config_template_switch_profiles",
        description="📋 Get switch profiles for a configuration template"
    )
    def get_org_config_template_switch_profiles(
        organization_id: str,
        config_template_id: str
    ):
        """Get switch profiles for a template."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationConfigTemplateSwitchProfiles(
                organization_id, config_template_id
            )
            
            response = f"# 📋 Switch Profiles\n\n"
            
            if result and isinstance(result, list):
                response += f"**Total Profiles**: {len(result)}\n\n"
                
                for profile in result:
                    response += f"## {profile.get('name', 'Unnamed')}\n"
                    response += f"- **Model**: {profile.get('model', 'N/A')}\n"
                    
                    # Switch ports
                    ports = profile.get('switchPorts', [])
                    if ports:
                        response += f"- **Ports**: {len(ports)}\n"
                    
                    response += "\n"
            else:
                response += "*No switch profiles found*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting switch profiles: {str(e)}"
    
    # ==================== BRANDING POLICIES ====================
    
    @app.tool(
        name="get_org_branding_policies",
        description="🎨 List all branding policies in an organization"
    )
    def get_org_branding_policies(
        organization_id: str
    ):
        """Get all branding policies."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationBrandingPolicies(
                organization_id
            )
            
            response = f"# 🎨 Branding Policies\n\n"
            
            if result and isinstance(result, list):
                response += f"**Total Policies**: {len(result)}\n\n"
                
                for policy in result:
                    response += f"## {policy.get('name', 'Unnamed')}\n"
                    response += f"- **ID**: {policy.get('id', 'N/A')}\n"
                    response += f"- **Enabled**: {policy.get('enabled', False)}\n"
                    
                    # Admin settings
                    admin_settings = policy.get('adminSettings', {})
                    if admin_settings:
                        response += f"- **Applies to**: {admin_settings.get('appliesTo', 'N/A')}\n"
                    
                    # Help settings
                    help_settings = policy.get('helpSettings', {})
                    if help_settings:
                        help_text = help_settings.get('helpText')
                        if help_text:
                            response += f"- **Help Text**: {help_text[:50]}...\n"
                    
                    response += "\n"
            else:
                response += "*No branding policies found*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting branding policies: {str(e)}"
    
    @app.tool(
        name="get_org_branding_policy",
        description="🎨 Get details of a specific branding policy"
    )
    def get_org_branding_policy(
        organization_id: str,
        branding_policy_id: str
    ):
        """Get specific branding policy details."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationBrandingPolicy(
                organization_id, branding_policy_id
            )
            
            response = f"# 🎨 Branding Policy Details\n\n"
            
            if result:
                response += f"**Name**: {result.get('name', 'Unnamed')}\n"
                response += f"**ID**: {result.get('id', 'N/A')}\n"
                response += f"**Enabled**: {result.get('enabled', False)}\n\n"
                
                # Admin settings
                admin_settings = result.get('adminSettings', {})
                if admin_settings:
                    response += f"## Admin Settings\n"
                    response += f"- **Applies to**: {admin_settings.get('appliesTo', 'N/A')}\n"
                    response += f"- **Values**: {admin_settings.get('values', [])}\n\n"
                
                # Custom logo
                custom_logo = result.get('customLogo', {})
                if custom_logo and custom_logo.get('enabled'):
                    response += f"## Custom Logo\n"
                    response += f"- **Enabled**: {custom_logo.get('enabled', False)}\n\n"
                
                # Help settings
                help_settings = result.get('helpSettings', {})
                if help_settings:
                    response += f"## Help Settings\n"
                    if help_settings.get('helpText'):
                        response += f"- **Custom Help**: Yes\n"
                    if help_settings.get('supportContactEmail'):
                        response += f"- **Support Email**: {help_settings['supportContactEmail']}\n"
            else:
                response += "*Policy not found*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting policy: {str(e)}"
    
    @app.tool(
        name="create_org_branding_policy",
        description="🎨➕ Create a new branding policy"
    )
    def create_org_branding_policy(
        organization_id: str,
        name: str,
        enabled: bool = True,
        admin_settings: Optional[str] = None,
        help_settings: Optional[str] = None,
        custom_logo: Optional[str] = None
    ):
        """
        Create a new branding policy.
        
        Args:
            organization_id: Organization ID
            name: Policy name
            enabled: Enable/disable policy
            admin_settings: JSON string of admin settings
            help_settings: JSON string of help settings
            custom_logo: JSON string of custom logo settings
        """
        try:
            kwargs = {
                'name': name,
                'enabled': enabled
            }
            
            if admin_settings:
                kwargs['adminSettings'] = json.loads(admin_settings) if isinstance(admin_settings, str) else admin_settings
            if help_settings:
                kwargs['helpSettings'] = json.loads(help_settings) if isinstance(help_settings, str) else help_settings
            if custom_logo:
                kwargs['customLogo'] = json.loads(custom_logo) if isinstance(custom_logo, str) else custom_logo
            
            result = meraki_client.dashboard.organizations.createOrganizationBrandingPolicy(
                organization_id, **kwargs
            )
            
            response = f"# ✅ Created Branding Policy\n\n"
            response += f"**Name**: {name}\n"
            response += f"**ID**: {result.get('id', 'N/A')}\n"
            response += f"**Enabled**: {enabled}\n"
            
            return response
        except Exception as e:
            return f"❌ Error creating policy: {str(e)}"
    
    @app.tool(
        name="update_org_branding_policy",
        description="🎨✏️ Update a branding policy"
    )
    def update_org_branding_policy(
        organization_id: str,
        branding_policy_id: str,
        name: Optional[str] = None,
        enabled: Optional[bool] = None,
        admin_settings: Optional[str] = None,
        help_settings: Optional[str] = None,
        custom_logo: Optional[str] = None
    ):
        """Update a branding policy."""
        try:
            kwargs = {}
            
            if name:
                kwargs['name'] = name
            if enabled is not None:
                kwargs['enabled'] = enabled
            if admin_settings:
                kwargs['adminSettings'] = json.loads(admin_settings) if isinstance(admin_settings, str) else admin_settings
            if help_settings:
                kwargs['helpSettings'] = json.loads(help_settings) if isinstance(help_settings, str) else help_settings
            if custom_logo:
                kwargs['customLogo'] = json.loads(custom_logo) if isinstance(custom_logo, str) else custom_logo
            
            result = meraki_client.dashboard.organizations.updateOrganizationBrandingPolicy(
                organization_id, branding_policy_id, **kwargs
            )
            
            response = f"# ✅ Updated Branding Policy\n\n"
            response += f"**Policy ID**: {branding_policy_id}\n"
            
            return response
        except Exception as e:
            return f"❌ Error updating policy: {str(e)}"
    
    @app.tool(
        name="delete_org_branding_policy",
        description="🎨❌ Delete a branding policy"
    )
    def delete_org_branding_policy(
        organization_id: str,
        branding_policy_id: str
    ):
        """Delete a branding policy."""
        try:
            meraki_client.dashboard.organizations.deleteOrganizationBrandingPolicy(
                organization_id, branding_policy_id
            )
            
            response = f"# ✅ Deleted Branding Policy\n\n"
            response += f"**Policy ID**: {branding_policy_id}\n"
            
            return response
        except Exception as e:
            return f"❌ Error deleting policy: {str(e)}"
    
    @app.tool(
        name="get_org_branding_policies_priorities",
        description="🎨 Get branding policy priorities"
    )
    def get_org_branding_policies_priorities(
        organization_id: str
    ):
        """Get branding policy priorities."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationBrandingPoliciesPriorities(
                organization_id
            )
            
            response = f"# 🎨 Branding Policy Priorities\n\n"
            
            if result and isinstance(result, dict):
                priorities = result.get('brandingPolicyIds', [])
                if priorities:
                    response += "**Priority Order**:\n"
                    for i, policy_id in enumerate(priorities, 1):
                        response += f"{i}. {policy_id}\n"
            else:
                response += "*No priorities set*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting priorities: {str(e)}"
    
    @app.tool(
        name="update_org_branding_policies_priorities",
        description="🎨✏️ Update branding policy priorities"
    )
    def update_org_branding_policies_priorities(
        organization_id: str,
        branding_policy_ids: str
    ):
        """
        Update branding policy priorities.
        
        Args:
            organization_id: Organization ID
            branding_policy_ids: Comma-separated policy IDs in priority order
        """
        try:
            policy_list = [p.strip() for p in branding_policy_ids.split(',')]
            
            result = meraki_client.dashboard.organizations.updateOrganizationBrandingPoliciesPriorities(
                organization_id,
                brandingPolicyIds=policy_list
            )
            
            response = f"# ✅ Updated Policy Priorities\n\n"
            response += f"**New Order**: {', '.join(policy_list)}\n"
            
            return response
        except Exception as e:
            return f"❌ Error updating priorities: {str(e)}"