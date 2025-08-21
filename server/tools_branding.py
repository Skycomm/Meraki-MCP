"""
Branding Tools for Cisco Meraki MCP Server
Configure custom branding for dashboard and splash pages
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


def get_organization_branding_policies(org_id: str) -> str:
    """
    🎨 Get branding policies for organization.
    
    Shows custom branding configurations for dashboard and splash pages.
    
    Args:
        org_id: Organization ID
    
    Returns:
        Branding policy list
    """
    try:
        with safe_api_call("get branding policies"):
            policies = meraki.dashboard.organizations.getOrganizationBrandingPolicies(org_id)
            
            output = ["🎨 Branding Policies", "=" * 50, ""]
            output.append(f"Organization: {org_id}")
            output.append("")
            
            if not policies:
                output.append("No branding policies configured")
                output.append("\n💡 Use create_organization_branding_policy() to add")
                return "\n".join(output)
            
            output.append(f"Total Policies: {len(policies)}")
            output.append("")
            
            # Show each policy
            for i, policy in enumerate(policies, 1):
                policy_id = policy.get('id', 'Unknown')
                name = policy.get('name', 'Unnamed Policy')
                enabled = policy.get('enabled', False)
                
                output.append(f"{i}. 🖼️ {name}")
                output.append(f"   ID: {policy_id}")
                output.append(f"   Status: {'✅ Enabled' if enabled else '❌ Disabled'}")
                
                # Admin settings
                admin_settings = policy.get('adminSettings', {})
                if admin_settings:
                    applies_to = admin_settings.get('appliesTo', 'All admins')
                    output.append(f"   Applies to: {applies_to}")
                    
                    if admin_settings.get('values'):
                        output.append("   Applied to:")
                        for value in admin_settings['values'][:3]:
                            output.append(f"      • {value}")
                        if len(admin_settings['values']) > 3:
                            output.append(f"      ... and {len(admin_settings['values']) - 3} more")
                
                # Custom logo
                custom_logo = policy.get('customLogo', {})
                if custom_logo.get('enabled'):
                    output.append("   📷 Custom Logo: Enabled")
                    if custom_logo.get('image', {}).get('preview', {}).get('expiresAt'):
                        output.append(f"      Preview expires: {custom_logo['image']['preview']['expiresAt']}")
                
                # Help settings
                help_settings = policy.get('helpSettings', {})
                if help_settings:
                    output.append("   📚 Help Customization:")
                    
                    if help_settings.get('helpTab'):
                        output.append(f"      Help tab: {help_settings['helpTab']}")
                    
                    if help_settings.get('getHelpSubtab'):
                        output.append(f"      Get help: {help_settings['getHelpSubtab']}")
                    
                    if help_settings.get('communitySubtab'):
                        output.append(f"      Community: {help_settings['communitySubtab']}")
                    
                    if help_settings.get('casesSubtab'):
                        output.append(f"      Cases: {help_settings['casesSubtab']}")
                    
                    if help_settings.get('dataProtectionRequestsSubtab'):
                        output.append(f"      Data protection: {help_settings['dataProtectionRequestsSubtab']}")
                    
                    if help_settings.get('universalSearchKnowledgeBaseSearch'):
                        output.append(f"      KB search: {help_settings['universalSearchKnowledgeBaseSearch']}")
                    
                    if help_settings.get('ciscoMerakiProductDocumentation'):
                        output.append(f"      Product docs: {help_settings['ciscoMerakiProductDocumentation']}")
                    
                    if help_settings.get('supportContactInfo'):
                        output.append(f"      Support info: {help_settings['supportContactInfo']}")
                    
                    if help_settings.get('newFeaturesSubtab'):
                        output.append(f"      New features: {help_settings['newFeaturesSubtab']}")
                    
                    if help_settings.get('firewallInfoSubtab'):
                        output.append(f"      Firewall info: {help_settings['firewallInfoSubtab']}")
                    
                    if help_settings.get('apiDocsSubtab'):
                        output.append(f"      API docs: {help_settings['apiDocsSubtab']}")
                    
                    if help_settings.get('hardwareReplacementsSubtab'):
                        output.append(f"      Hardware replacements: {help_settings['hardwareReplacementsSubtab']}")
                    
                    if help_settings.get('smForums'):
                        output.append(f"      SM forums: {help_settings['smForums']}")
                
                output.append("")
            
            # Branding capabilities
            output.append("🎨 Branding Capabilities:")
            output.append("• Custom logo upload")
            output.append("• Help menu customization")
            output.append("• Support contact info")
            output.append("• API documentation links")
            output.append("• Targeted admin groups")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("get branding policies", e)


def create_organization_branding_policy(
    org_id: str,
    name: str,
    enabled: bool = True,
    admin_settings: Optional[Dict[str, Any]] = None,
    help_settings: Optional[Dict[str, Any]] = None
) -> str:
    """
    ➕ Create branding policy.
    
    Configure custom branding for dashboard experience.
    
    Args:
        org_id: Organization ID
        name: Policy name
        enabled: Enable policy
        admin_settings: Admin targeting settings
        help_settings: Help menu customization
    
    Returns:
        Created branding policy details
    """
    try:
        with safe_api_call("create branding policy"):
            # Build policy data
            policy_data = {
                "name": name,
                "enabled": enabled
            }
            
            if admin_settings:
                policy_data["adminSettings"] = admin_settings
            
            if help_settings:
                policy_data["helpSettings"] = help_settings
            
            # Create the policy
            policy = meraki.dashboard.organizations.createOrganizationBrandingPolicy(
                org_id,
                **policy_data
            )
            
            output = ["✅ Branding Policy Created", "=" * 50, ""]
            output.append(f"Name: {policy.get('name', name)}")
            output.append(f"ID: {policy.get('id', 'N/A')}")
            output.append(f"Status: {'Enabled' if policy.get('enabled') else 'Disabled'}")
            output.append("")
            
            # Admin settings summary
            if admin_settings:
                output.append("👥 Target Admins:")
                output.append(f"   Applies to: {admin_settings.get('appliesTo', 'All')}")
                if admin_settings.get('values'):
                    output.append(f"   Count: {len(admin_settings['values'])}")
            
            # Help settings summary  
            if help_settings:
                output.append("\n📚 Help Customization:")
                custom_count = sum(1 for v in help_settings.values() if v == 'custom')
                hidden_count = sum(1 for v in help_settings.values() if v == 'hide')
                output.append(f"   Custom items: {custom_count}")
                output.append(f"   Hidden items: {hidden_count}")
            
            output.append("\n🚀 Next Steps:")
            output.append("1. Upload custom logo")
            output.append("2. Configure help links")
            output.append("3. Test with target admins")
            output.append("4. Enable policy")
            output.append("5. Gather feedback")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("create branding policy", e)


def update_organization_branding_policy(
    org_id: str,
    branding_policy_id: str,
    name: Optional[str] = None,
    enabled: Optional[bool] = None,
    admin_settings: Optional[Dict[str, Any]] = None,
    help_settings: Optional[Dict[str, Any]] = None
) -> str:
    """
    ✏️ Update branding policy.
    
    Modify existing branding policy configuration.
    
    Args:
        org_id: Organization ID
        branding_policy_id: Branding policy ID
        name: New policy name
        enabled: Enable/disable policy
        admin_settings: New admin targeting
        help_settings: New help customization
    
    Returns:
        Updated branding policy details
    """
    try:
        with safe_api_call("update branding policy"):
            # Build update data
            update_data = {}
            
            if name is not None:
                update_data["name"] = name
            
            if enabled is not None:
                update_data["enabled"] = enabled
            
            if admin_settings is not None:
                update_data["adminSettings"] = admin_settings
            
            if help_settings is not None:
                update_data["helpSettings"] = help_settings
            
            # Update the policy
            policy = meraki.dashboard.organizations.updateOrganizationBrandingPolicy(
                org_id,
                branding_policy_id,
                **update_data
            )
            
            output = ["✏️ Branding Policy Updated", "=" * 50, ""]
            output.append(f"Policy ID: {branding_policy_id}")
            output.append(f"Name: {policy.get('name', 'Unknown')}")
            output.append(f"Status: {'Enabled' if policy.get('enabled') else 'Disabled'}")
            output.append("")
            
            output.append("✅ Changes Applied")
            
            output.append("\n⚠️ Important:")
            output.append("• Changes take effect immediately")
            output.append("• Admins may need to refresh")
            output.append("• Test with sample admin first")
            output.append("• Monitor for issues")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("update branding policy", e)


def delete_organization_branding_policy(
    org_id: str,
    branding_policy_id: str
) -> str:
    """
    🗑️ Delete branding policy.
    
    Remove branding policy from organization.
    
    Args:
        org_id: Organization ID
        branding_policy_id: Branding policy ID
    
    Returns:
        Deletion confirmation
    """
    try:
        with safe_api_call("delete branding policy"):
            meraki.dashboard.organizations.deleteOrganizationBrandingPolicy(
                org_id,
                branding_policy_id
            )
            
            output = ["🗑️ Branding Policy Deleted", "=" * 50, ""]
            output.append(f"Policy ID: {branding_policy_id}")
            output.append(f"Organization: {org_id}")
            output.append("")
            output.append("✅ Policy removed successfully")
            output.append("")
            output.append("⚠️ Impact:")
            output.append("• Affected admins see default branding")
            output.append("• Custom logos removed")
            output.append("• Help menu reverts to default")
            output.append("• Changes immediate")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("delete branding policy", e)


def branding_configuration_examples() -> str:
    """
    📚 Show branding configuration examples.
    
    Provides example configurations for common branding scenarios.
    
    Returns:
        Branding configuration examples
    """
    output = ["📚 Branding Configuration Examples", "=" * 50, ""]
    
    output.append("1️⃣ MSP Custom Branding:")
    output.append("""
# Target specific customer admins
admin_settings = {
    "appliesTo": "A list of network IDs",
    "values": ["N_123456", "N_789012"]
}

# Customize help menu
help_settings = {
    "helpTab": "default",
    "getHelpSubtab": "custom",
    "customGetHelpSubtabText": "Contact MSP Support",
    "supportContactInfo": "custom",
    "customSupportContactInfoText": "support@msp.com | 1-800-MSP-HELP"
}

create_organization_branding_policy(
    org_id,
    name="Customer ABC Branding",
    enabled=True,
    admin_settings=admin_settings,
    help_settings=help_settings
)
""")
    
    output.append("\n2️⃣ Enterprise IT Branding:")
    output.append("""
# Apply to all admins
admin_settings = {
    "appliesTo": "All organization admins"
}

# Hide external links, add internal
help_settings = {
    "helpTab": "show",
    "getHelpSubtab": "custom",
    "customGetHelpSubtabText": "IT Service Desk",
    "communitySubtab": "hide",
    "casesSubtab": "hide",
    "supportContactInfo": "custom",
    "customSupportContactInfoText": "Internal ext: 4357",
    "apiDocsSubtab": "custom",
    "customApiDocsSubtabUrl": "https://wiki.company.com/meraki-api"
}
""")
    
    output.append("\n3️⃣ Education Institution:")
    output.append("""
# Target by admin tags
admin_settings = {
    "appliesTo": "A list of SAML role IDs",
    "values": ["samlRole_123", "samlRole_456"]
}

help_settings = {
    "helpTab": "show",
    "newFeaturesSubtab": "default",
    "firewallInfoSubtab": "custom",
    "customFirewallInfoSubtabUrl": "https://it.university.edu/firewall-rules",
    "hardwareReplacementsSubtab": "custom",
    "customHardwareReplacementsSubtabText": "Submit IT Ticket"
}
""")
    
    output.append("\n4️⃣ Minimal Branding:")
    output.append("""
# Hide most help options
help_settings = {
    "helpTab": "show",
    "getHelpSubtab": "hide",
    "communitySubtab": "hide", 
    "casesSubtab": "hide",
    "dataProtectionRequestsSubtab": "hide",
    "universalSearchKnowledgeBaseSearch": "hide",
    "supportContactInfo": "custom",
    "customSupportContactInfoText": "Contact your administrator"
}
""")
    
    output.append("\n🎨 Logo Requirements:")
    output.append("• Format: PNG, JPG, or GIF")
    output.append("• Max size: 1 MB")
    output.append("• Recommended: 150x150px")
    output.append("• Transparent background preferred")
    output.append("• High contrast for visibility")
    
    output.append("\n💡 Best Practices:")
    output.append("• Test with small admin group first")
    output.append("• Keep branding professional")
    output.append("• Provide useful help links")
    output.append("• Update contact info regularly")
    output.append("• Document customizations")
    
    return "\n".join(output)


def branding_help() -> str:
    """
    ❓ Get help with branding tools.
    
    Shows available tools and best practices.
    
    Returns:
        Formatted help guide
    """
    return """🎨 Branding Tools Help
==================================================

Available tools for branding configuration:

1. get_organization_branding_policies()
   - List all policies
   - View configurations
   - Check targeting
   - See customizations

2. create_organization_branding_policy()
   - Add new policy
   - Set targeting rules
   - Configure help menu
   - Enable/disable

3. update_organization_branding_policy()
   - Modify existing
   - Change targeting
   - Update help links
   - Toggle status

4. delete_organization_branding_policy()
   - Remove policy
   - Revert to default
   - Clean up old

5. branding_configuration_examples()
   - MSP scenarios
   - Enterprise setups
   - Education configs
   - Best practices

Branding Elements:
🖼️ Custom logo
📚 Help menu
📞 Support info
🔗 Custom links
📖 Documentation
🎯 Admin targeting

Admin Targeting:
• All organization admins
• Specific networks
• SAML role IDs
• Admin tags
• Email addresses

Help Menu Options:
• default - Show standard
• custom - Custom content
• hide - Remove item

Customizable Items:
• Get Help tab
• Community forum
• Support cases
• Data protection
• Knowledge base
• Product docs
• Support contact
• New features
• Firewall info
• API docs
• Hardware RMA
• SM forums

Logo Guidelines:
• PNG/JPG/GIF format
• Max 1 MB size
• 150x150px recommended
• High contrast
• Professional look

Use Cases:
🏢 MSP white-labeling
🎓 Education branding
🏥 Healthcare compliance
🏭 Enterprise standards
🏪 Retail chains
🌐 Global organizations

Best Practices:
• Test before deploying
• Document customizations
• Keep info updated
• Professional appearance
• Useful help links
• Monitor feedback

Common Scenarios:
• White-label for MSPs
• Internal IT branding
• Department isolation
• Compliance requirements
• Simplified interface
• Custom documentation

Tips:
• Start with one policy
• Target small group
• Gather feedback
• Iterate design
• Document changes
• Train admins
"""


def register_branding_tools(app: FastMCP, meraki_client: MerakiClient):
    """Register all branding tools with the MCP server."""
    global mcp_app, meraki
    mcp_app = app
    meraki = meraki_client
    
    # Register all tools
    tools = [
        (get_organization_branding_policies, "List branding policies"),
        (create_organization_branding_policy, "Create branding policy"),
        (update_organization_branding_policy, "Update branding policy"),
        (delete_organization_branding_policy, "Delete branding policy"),
        (branding_configuration_examples, "Show branding examples"),
        (branding_help, "Get help with branding tools"),
    ]
    
    for tool_func, description in tools:
        app.tool(
            name=tool_func.__name__,
            description=description
        )(tool_func)