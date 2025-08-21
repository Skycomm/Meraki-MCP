"""
Configuration Templates Tools for Cisco Meraki MCP Server
Manage and deploy configuration templates across networks
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


def get_organization_config_templates(org_id: str) -> str:
    """
    📋 Get configuration templates.
    
    Lists all configuration templates in organization.
    
    Args:
        org_id: Organization ID
    
    Returns:
        List of configuration templates
    """
    try:
        with safe_api_call("get config templates"):
            templates = meraki.dashboard.organizations.getOrganizationConfigTemplates(org_id)
            
            output = ["📋 Configuration Templates", "=" * 50, ""]
            output.append(f"Organization: {org_id}")
            output.append(f"Total Templates: {len(templates)}")
            output.append("")
            
            if not templates:
                output.append("No configuration templates found")
                output.append("\n💡 Use create_organization_config_template() to add")
                return "\n".join(output)
            
            # Group by product type
            by_product = {}
            for template in templates:
                product_types = template.get('productTypes', ['Unknown'])
                for product in product_types:
                    if product not in by_product:
                        by_product[product] = []
                    by_product[product].append(template)
            
            # Show templates by product
            for product, templates in sorted(by_product.items()):
                output.append(f"\n🔧 {product.upper()} Templates:")
                for template in templates[:5]:
                    template_id = template.get('id', 'Unknown')
                    name = template.get('name', 'Unnamed')
                    
                    output.append(f"\n   📄 {name}")
                    output.append(f"      ID: {template_id}")
                    
                    # Time zone
                    if template.get('timeZone'):
                        output.append(f"      Timezone: {template['timeZone']}")
                    
                if len(templates) > 5:
                    output.append(f"\n   ... and {len(templates) - 5} more {product} templates")
            
            output.append("\n💡 Template Benefits:")
            output.append("• Consistent configuration")
            output.append("• Rapid deployment")
            output.append("• Reduced errors")
            output.append("• Version control")
            output.append("• Bulk updates")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("get config templates", e)


def create_organization_config_template(
    org_id: str,
    name: str,
    timezone: str,
    copy_from_network_id: Optional[str] = None
) -> str:
    """
    ➕ Create configuration template.
    
    Create new template optionally from existing network.
    
    Args:
        org_id: Organization ID
        name: Template name
        timezone: Template timezone
        copy_from_network_id: Source network ID
    
    Returns:
        Created template details
    """
    try:
        with safe_api_call("create config template"):
            template_data = {
                "name": name,
                "timeZone": timezone
            }
            
            if copy_from_network_id:
                template_data["copyFromNetworkId"] = copy_from_network_id
            
            template = meraki.dashboard.organizations.createOrganizationConfigTemplate(
                org_id,
                **template_data
            )
            
            output = ["➕ Configuration Template Created", "=" * 50, ""]
            output.append(f"Name: {template.get('name', name)}")
            output.append(f"ID: {template.get('id', 'N/A')}")
            output.append(f"Timezone: {template.get('timeZone', timezone)}")
            
            if copy_from_network_id:
                output.append(f"\n📋 Copied from: {copy_from_network_id}")
                output.append("• All settings copied")
                output.append("• Review configuration")
                output.append("• Adjust as needed")
            
            output.append("\n🚀 Next Steps:")
            output.append("1. Configure template settings")
            output.append("2. Test on single network")
            output.append("3. Bind to networks")
            output.append("4. Monitor deployment")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("create config template", e)


def bind_network_to_template(
    network_id: str,
    template_id: str,
    auto_bind: bool = True
) -> str:
    """
    🔗 Bind network to template.
    
    Apply template configuration to network.
    
    Args:
        network_id: Network ID
        template_id: Template ID
        auto_bind: Auto-bind new devices
    
    Returns:
        Binding status
    """
    try:
        with safe_api_call("bind network to template"):
            result = meraki.dashboard.networks.bindNetwork(
                network_id,
                configTemplateId=template_id,
                autoBind=auto_bind
            )
            
            output = ["🔗 Network Bound to Template", "=" * 50, ""]
            output.append(f"Network: {network_id}")
            output.append(f"Template: {template_id}")
            output.append(f"Auto-bind: {'Yes' if auto_bind else 'No'}")
            output.append("")
            
            output.append("✅ Template Applied Successfully")
            
            output.append("\n⚠️ Important Notes:")
            output.append("• Settings overwritten")
            output.append("• Local changes lost")
            output.append("• Template controls config")
            output.append("• Updates propagate")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("bind network to template", e)


def template_deployment_guide() -> str:
    """
    📚 Template deployment guide.
    
    Best practices for template management.
    
    Returns:
        Deployment guide
    """
    output = ["📚 Template Deployment Guide", "=" * 50, ""]
    
    output.append("🎯 Template Strategy:")
    output.append("1. Design template hierarchy")
    output.append("2. Create base templates")
    output.append("3. Test thoroughly")
    output.append("4. Document changes")
    output.append("5. Plan rollout")
    
    output.append("\n📋 Common Templates:")
    output.append("• Branch office standard")
    output.append("• Retail store config")
    output.append("• Campus wireless")
    output.append("• Security baseline")
    output.append("• Guest network")
    
    output.append("\n🚀 Deployment Process:")
    output.append("1. Create template")
    output.append("2. Configure all settings")
    output.append("3. Test on lab network")
    output.append("4. Pilot deployment")
    output.append("5. Full rollout")
    
    output.append("\n💡 Best Practices:")
    output.append("• Version templates")
    output.append("• Use descriptive names")
    output.append("• Document exceptions")
    output.append("• Regular reviews")
    output.append("• Change control")
    
    return "\n".join(output)


def config_templates_help() -> str:
    """
    ❓ Get help with config template tools.
    
    Shows available tools and concepts.
    
    Returns:
        Formatted help guide
    """
    return """📋 Configuration Templates Help
==================================================

Available tools:

1. get_organization_config_templates()
   - List all templates
   - View by product type
   - Check bindings

2. create_organization_config_template()
   - Create new template
   - Copy from network
   - Set timezone

3. bind_network_to_template()
   - Apply template
   - Auto-bind devices
   - Override settings

4. template_deployment_guide()
   - Best practices
   - Deployment process
   - Common patterns

Benefits:
• Consistency
• Scalability
• Error reduction
• Time savings
• Version control

Use Cases:
• Multi-site deployment
• Standard configs
• Quick provisioning
• Change management
• Disaster recovery
"""


def register_config_template_tools(app: FastMCP, meraki_client: MerakiClient):
    """Register all config template tools with the MCP server."""
    global mcp_app, meraki
    mcp_app = app
    meraki = meraki_client
    
    # Register all tools
    tools = [
        (get_organization_config_templates, "List configuration templates"),
        (create_organization_config_template, "Create config template"),
        (bind_network_to_template, "Bind network to template"),
        (template_deployment_guide, "Template deployment guide"),
        (config_templates_help, "Get help with templates"),
    ]
    
    for tool_func, description in tools:
        app.tool(
            name=tool_func.__name__,
            description=description
        )(tool_func)