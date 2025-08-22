"""
Organization-related tools for the Cisco Meraki MCP Server - Modern implementation.
"""

# Global variables to store app and meraki client
app = None
meraki_client = None

def register_organization_tools(mcp_app, meraki):
    """
    Register organization-related tools with the MCP server.
    
    Args:
        mcp_app: MCP server instance
        meraki: Meraki client instance
    """
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    
    # Register all organization tools
    register_organization_tool_handlers()

def register_organization_tool_handlers():
    """Register all organization-related tool handlers using the decorator pattern."""
    
    @app.tool(
        name="list_organizations",
        description="List all Meraki organizations the API key has access to"
    )
    def list_organizations():
        """
        List all Meraki organizations the API key has access to.
        
        Returns:
            Formatted list of organizations
        """
        try:
            organizations = meraki_client.get_organizations()
            
            if not organizations:
                return "No organizations found for this API key."
                
            # Format the output for readability
            result = "# Meraki Organizations\n\n"
            for org in organizations:
                result += f"- **{org['name']}** (ID: `{org['id']}`)\n"
                
            return result
            
        except Exception as e:
            return f"Failed to list organizations: {str(e)}"
    
    @app.tool(
        name="get_organization",
        description="Get details about a specific Meraki organization"
    )
    def get_organization(organization_id: str):
        """
        Get details about a specific Meraki organization.
        
        Args:
            organization_id: ID of the organization to retrieve
            
        Returns:
            Organization details
        """
        return meraki_client.get_organization(organization_id)
    
    @app.tool(
        name="get_organization_networks",
        description="List networks in a Meraki organization"
    )
    def get_organization_networks(org_id: str):
        """
        List networks in a Meraki organization.
        
        Args:
            org_id: ID of the organization
            
        Returns:
            Formatted list of networks
        """
        try:
            networks = meraki_client.get_organization_networks(org_id)
            
            if not networks:
                return f"No networks found for organization {org_id}."
                
            # Format the output for readability
            result = f"# Networks in Organization ({org_id})\n\n"
            for net in networks:
                result += f"- **{net['name']}** (ID: `{net['id']}`)\n"
                result += f"  - Type: {net.get('type', 'Unknown')}\n"
                result += f"  - Tags: {', '.join(net.get('tags', []) or ['None'])}\n"
                
            return result
            
        except Exception as e:
            return f"Failed to list networks for organization {org_id}: {str(e)}"
    
    @app.tool(
        name="get_organization_alerts",
        description="Get alert settings for a Meraki organization"
    )
    def get_organization_alerts(org_id: str):
        """
        Get alert settings for a Meraki organization.
        
        Args:
            org_id: ID of the organization
            
        Returns:
            Formatted alert settings
        """
        try:
            alerts = meraki_client.get_organization_alerts(org_id)
            
            if not alerts:
                return f"No alert settings found for organization {org_id}."
                
            # Format the output for readability
            result = f"# Alert Settings for Organization ({org_id})\n\n"
            
            # Add default destinations if present
            if 'defaultDestinations' in alerts:
                result += "## Default Destinations\n"
                destinations = alerts['defaultDestinations']
                result += f"- Email: {destinations.get('emails', [])}\n"
                result += f"- Webhook URLs: {destinations.get('httpServerIds', [])}\n"
                result += f"- SMS Numbers: {destinations.get('smsNumbers', [])}\n"
                result += "\n"
            
            # Add alert types
            if 'alerts' in alerts:
                result += "## Alert Types\n"
                for alert in alerts['alerts']:
                    result += f"### {alert.get('type', 'Unknown')}\n"
                    result += f"- Enabled: {alert.get('enabled', False)}\n"
                    
                    # Add alert-specific destinations
                    if 'destinations' in alert:
                        alert_dest = alert['destinations']
                        result += "- Destinations:\n"
                        result += f"  - Email: {alert_dest.get('emails', [])}\n"
                        result += f"  - Webhook URLs: {alert_dest.get('httpServerIds', [])}\n"
                        result += f"  - SMS Numbers: {alert_dest.get('smsNumbers', [])}\n"
                    
                    result += "\n"
                
            return result
            
        except Exception as e:
            return f"Failed to get alert settings for organization {org_id}: {str(e)}"
    
    @app.tool(
        name="create_organization",
        description="Create a new Meraki organization"
    )
    def create_organization(name: str):
        """
        Create a new Meraki organization.
        
        Args:
            name: Name for the new organization
            
        Returns:
            New organization details
        """
        return meraki_client.create_organization(name)
    
    @app.tool(
        name="update_organization",
        description="Update a Meraki organization"
    )
    def update_organization(organization_id: str, name: str = None):
        """
        Update a Meraki organization.
        
        Args:
            organization_id: ID of the organization to update
            name: New name for the organization (optional)
            
        Returns:
            Updated organization details
        """
        try:
            # Get current organization
            org = meraki_client.get_organization(organization_id)
            current_name = org.get('name', 'Unknown')
            
            # If renaming, require confirmation
            if name and name != current_name:
                from utils.helpers import require_confirmation
                
                if not require_confirmation(
                    operation_type="rename",
                    resource_type="organization",
                    resource_name=f"{current_name} → {name}",
                    resource_id=organization_id
                ):
                    return "❌ Organization rename cancelled by user"
            
            # Perform update
            result = meraki_client.update_organization(organization_id, name)
            return f"✅ Organization updated successfully"
            
        except Exception as e:
            return f"Failed to update organization: {str(e)}"
    
    @app.tool(
        name="delete_organization",
        description="Delete a Meraki organization - REQUIRES CONFIRMATION - DANGEROUS!"
    )
    def delete_organization(organization_id: str):
        """
        Delete a Meraki organization.
        
        Args:
            organization_id: ID of the organization to delete
            
        Returns:
            Success/failure information
        """
        try:
            # Get organization details
            org = meraki_client.get_organization(organization_id)
            
            from utils.helpers import require_confirmation
            
            # Double confirmation for organization deletion
            print("\n⚠️  EXTREME CAUTION: Organization deletion will delete ALL networks and devices!")
            
            if not require_confirmation(
                operation_type="delete",
                resource_type="organization",
                resource_name=org.get('name', 'Unknown'),
                resource_id=organization_id
            ):
                return "❌ Organization deletion cancelled by user"
            
            # Second confirmation
            print(f"\n🚨 FINAL WARNING: This will delete organization '{org['name']}' and ALL its contents!")
            print("Type 'DELETE EVERYTHING' to confirm:")
            
            final_confirm = input("> ").strip()
            if final_confirm != "DELETE EVERYTHING":
                return "❌ Organization deletion cancelled - final confirmation failed"
            
            # Perform deletion
            meraki_client.delete_organization(organization_id)
            return f"✅ Organization '{org['name']}' deleted permanently"
            
        except Exception as e:
            return f"Failed to delete organization: {str(e)}"
    
    @app.tool(
        name="get_organization_firmware",
        description="Get firmware upgrades for a Meraki organization"
    )
    def get_organization_firmware(org_id: str):
        """
        Get firmware upgrades for a Meraki organization.
        
        Args:
            org_id: ID of the organization
            
        Returns:
            Formatted firmware upgrade information
        """
        try:
            upgrades = meraki_client.get_organization_firmware_upgrades(org_id)
            
            if not upgrades:
                return f"No firmware upgrades found for organization {org_id}."
                
            # Format the output for readability
            result = f"# Firmware Upgrades for Organization ({org_id})\n\n"
            
            if isinstance(upgrades, list):
                for upgrade in upgrades:
                    result += f"## Upgrade ID: {upgrade.get('id', 'Unknown')}\n"
                    result += f"- Status: {upgrade.get('status', 'Unknown')}\n"
                    result += f"- Time: {upgrade.get('time', 'Unknown')}\n"
                    result += f"- Products: {', '.join(upgrade.get('products', []) or ['None'])}\n"
                    result += "\n"
            else:
                result += str(upgrades)
                
            return result
            
        except Exception as e:
            return f"Failed to get firmware upgrades for organization {org_id}: {str(e)}"
