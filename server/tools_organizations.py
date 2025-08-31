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
        name="search_organizations_by_name",
        description="Search for Meraki organizations by name (case-insensitive)"
    )
    def search_organizations_by_name(name: str):
        """
        Search for Meraki organizations by name.
        
        Args:
            name: Name to search for (case-insensitive partial match)
            
        Returns:
            Formatted list of matching organizations
        """
        try:
            organizations = meraki_client.get_organizations()
            
            # Filter organizations by name (case-insensitive)
            search_term = name.lower()
            matching_orgs = [
                org for org in organizations 
                if search_term in org['name'].lower()
            ]
            
            if not matching_orgs:
                return f"No organizations found matching '{name}'."
                
            # Format the output
            result = f"# Organizations matching '{name}'\n\n"
            for org in matching_orgs:
                result += f"- **{org['name']}** (ID: `{org['id']}`)\n"
                if org.get('url'):
                    result += f"  - URL: {org['url']}\n"
                    
            return result
            
        except Exception as e:
            return f"Failed to search organizations: {str(e)}"
    
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
    def get_organization_networks(organization_id: str):
        """
        List networks in a Meraki organization.
        
        Args:
            organization_id: ID of the organization
            
        Returns:
            Formatted list of networks
        """
        try:
            networks = meraki_client.get_organization_networks(organization_id)
            
            if not networks:
                return f"No networks found for organization {organization_id}."
                
            # Format the output for readability
            result = f"# Networks in Organization ({organization_id})\n\n"
            for net in networks:
                result += f"- **{net['name']}** (ID: `{net['id']}`)\n"
                result += f"  - Type: {net.get('type', 'Unknown')}\n"
                result += f"  - Tags: {', '.join(net.get('tags', []) or ['None'])}\n"
                
            return result
            
        except Exception as e:
            return f"Failed to list networks for organization {organization_id}: {str(e)}"
    
    @app.tool(
        name="get_organization_alerts",
        description="Get alert settings for a Meraki organization"
    )
    def get_organization_alerts(organization_id: str):
        """
        Get alert settings for a Meraki organization.
        
        Args:
            organization_id: ID of the organization
            
        Returns:
            Formatted alert settings
        """
        try:
            alerts = meraki_client.get_organization_alerts(organization_id)
            
            if not alerts:
                return f"No alert settings found for organization {organization_id}."
                
            # Format the output for readability
            result = f"# Alert Settings for Organization ({organization_id})\n\n"
            
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
            return f"Failed to get alert settings for organization {organization_id}: {str(e)}"
    
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
    def get_organization_firmware(organization_id: str):
        """
        Get firmware upgrades for a Meraki organization.
        
        Args:
            organization_id: ID of the organization
            
        Returns:
            Formatted firmware upgrade information
        """
        try:
            upgrades = meraki_client.get_organization_firmware_upgrades(organization_id)
            
            if not upgrades:
                return f"No firmware upgrades found for organization {organization_id}."
                
            # Format the output for readability
            result = f"# Firmware Upgrades for Organization ({organization_id})\n\n"
            
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
            return f"Failed to get firmware upgrades for organization {organization_id}: {str(e)}"
    
    @app.tool(
        name="get_organization_admins",
        description="Get dashboard administrators for a Meraki organization"
    )
    def get_organization_admins(organization_id: str, network_ids: str = None):
        """
        Get dashboard administrators for a Meraki organization.
        
        Args:
            organization_id: ID of the organization
            network_ids: Comma-separated list of network IDs to filter by (optional)
            
        Returns:
            Formatted list of administrators
        """
        try:
            # Parse network IDs if provided
            network_id_list = None
            if network_ids:
                network_id_list = [id.strip() for id in network_ids.split(',')]
            
            admins = meraki_client.get_organization_admins(organization_id, network_id_list)
            
            if not admins:
                return f"No administrators found for organization {organization_id}."
                
            # Format the output for readability
            result = f"# Administrators for Organization ({organization_id})\n\n"
            
            for admin in admins:
                result += f"## {admin.get('name', 'Unknown')}\n"
                result += f"- Email: {admin.get('email', 'Unknown')}\n"
                result += f"- ID: {admin.get('id', 'Unknown')}\n"
                result += f"- Auth Method: {admin.get('authenticationMethod', 'Unknown')}\n"
                result += f"- Two Factor Auth: {admin.get('twoFactorAuthEnabled', False)}\n"
                result += f"- Account Status: {admin.get('accountStatus', 'Unknown')}\n"
                result += f"- Has API Key: {admin.get('hasApiKey', False)}\n"
                result += f"- Last Active: {admin.get('lastActive', 'Unknown')}\n"
                
                # Add organization access details
                if 'orgAccess' in admin:
                    result += f"- Organization Access: {admin['orgAccess']}\n"
                
                # Add network privileges if available
                if 'networks' in admin and admin['networks']:
                    result += "- Network Privileges:\n"
                    for network in admin['networks']:
                        result += f"  - {network.get('id', 'Unknown')}: {network.get('access', 'Unknown')}\n"
                
                # Add tags if available
                if 'tags' in admin and admin['tags']:
                    result += "- Tags:\n"
                    for tag in admin['tags']:
                        result += f"  - {tag.get('tag', 'Unknown')}: {tag.get('access', 'Unknown')}\n"
                
                result += "\n"
                
            return result
            
        except Exception as e:
            return f"Failed to get administrators for organization {organization_id}: {str(e)}"
    
    @app.tool(
        name="check_organization_comprehensive",
        description="Perform a comprehensive check of a Meraki organization including all settings, policies, webhooks, licenses, devices, and configurations"
    )
    def check_organization_comprehensive(organization_id: str, check_type: str = "all"):
        """
        Perform a comprehensive check of a Meraki organization.
        
        Args:
            organization_id: ID of the organization
            check_type: Type of check to perform - 'all', 'settings', 'devices', 'policies', 'webhooks', 'licenses' (default: 'all')
            
        Returns:
            Comprehensive report on the organization
        """
        try:
            result = f"# Comprehensive Organization Check\n"
            result += f"## Organization ID: {organization_id}\n\n"
            
            # Get basic organization info
            try:
                org = meraki_client.get_organization(organization_id)
                result += f"### Organization Details\n"
                result += f"- Name: {org.get('name', 'Unknown')}\n"
                result += f"- URL: {org.get('url', 'Unknown')}\n"
                result += f"- API Enabled: {org.get('api', {}).get('enabled', 'Unknown')}\n"
                result += f"- Cloud Region: {org.get('cloud', {}).get('region', {}).get('name', 'Unknown')}\n"
                result += f"- Management Details: {org.get('management', {}).get('details', [])}\n\n"
            except Exception as e:
                result += f"### Organization Details\n"
                result += f"- Error fetching details: {str(e)}\n\n"
            
            # Check networks
            if check_type in ['all', 'settings']:
                result += "### Networks\n"
                try:
                    networks = meraki_client.get_organization_networks(organization_id)
                    result += f"- Total Networks: {len(networks)}\n"
                    if networks:
                        result += "- Network List:\n"
                        for net in networks[:5]:  # Show first 5
                            result += f"  - {net.get('name', 'Unknown')} (ID: {net.get('id', 'Unknown')}, Type: {net.get('productTypes', [])})\n"
                        if len(networks) > 5:
                            result += f"  - ... and {len(networks) - 5} more networks\n"
                    else:
                        result += "- **No networks found**\n"
                except Exception as e:
                    result += f"- Error fetching networks: {str(e)}\n"
                result += "\n"
            
            # Check devices
            if check_type in ['all', 'devices']:
                result += "### Devices\n"
                try:
                    devices = meraki_client.get_organization_devices(organization_id)
                    result += f"- Total Devices: {len(devices)}\n"
                    if devices:
                        # Group by model
                        models = {}
                        for device in devices:
                            model = device.get('model', 'Unknown')
                            models[model] = models.get(model, 0) + 1
                        result += "- Device Models:\n"
                        for model, count in models.items():
                            result += f"  - {model}: {count}\n"
                except Exception as e:
                    result += f"- Error fetching devices: {str(e)}\n"
                result += "\n"
            
            # Check alerts
            if check_type in ['all', 'settings']:
                result += "### Alert Settings\n"
                try:
                    alerts = meraki_client.get_organization_alerts(organization_id)
                    if alerts and 'alerts' in alerts:
                        enabled_alerts = [a['type'] for a in alerts['alerts'] if a.get('enabled', False)]
                        result += f"- Enabled Alerts: {len(enabled_alerts)}\n"
                        if enabled_alerts:
                            result += f"- Alert Types: {', '.join(enabled_alerts[:5])}"
                            if len(enabled_alerts) > 5:
                                result += f" ... and {len(enabled_alerts) - 5} more"
                            result += "\n"
                    else:
                        result += "- No alert settings configured\n"
                except Exception as e:
                    result += f"- Error fetching alerts: {str(e)}\n"
                result += "\n"
            
            # Check webhooks
            if check_type in ['all', 'webhooks']:
                result += "### Webhooks\n"
                try:
                    webhooks = meraki_client.get_organization_webhooks(organization_id)
                    if webhooks:
                        result += f"- Total Webhooks: {len(webhooks)}\n"
                        for webhook in webhooks[:3]:  # Show first 3
                            result += f"  - {webhook.get('name', 'Unknown')} ({webhook.get('url', 'Unknown')})\n"
                        if len(webhooks) > 3:
                            result += f"  - ... and {len(webhooks) - 3} more webhooks\n"
                    else:
                        result += "- No webhooks configured\n"
                except Exception as e:
                    result += f"- Error fetching webhooks: {str(e)}\n"
                result += "\n"
            
            # Check firmware settings
            if check_type in ['all', 'settings']:
                result += "### Firmware Settings\n"
                try:
                    firmware = meraki_client.get_organization_firmware_upgrades(organization_id)
                    if firmware:
                        result += f"- Firmware upgrade information available\n"
                    else:
                        result += "- No firmware upgrades configured\n"
                except Exception as e:
                    result += f"- Error fetching firmware settings: {str(e)}\n"
                result += "\n"
            
            # Check licenses
            if check_type in ['all', 'licenses']:
                result += "### Licensing\n"
                try:
                    licenses = meraki_client.get_organization_licenses(organization_id)
                    if licenses:
                        result += f"- Total Licenses: {len(licenses)}\n"
                        # Group by state
                        states = {}
                        for lic in licenses:
                            state = lic.get('state', 'Unknown')
                            states[state] = states.get(state, 0) + 1
                        result += "- License States:\n"
                        for state, count in states.items():
                            result += f"  - {state}: {count}\n"
                    else:
                        result += "- No licenses found\n"
                except Exception as e:
                    result += f"- Error fetching licenses: {str(e)}\n"
                result += "\n"
            
            # Check policy objects
            if check_type in ['all', 'policies']:
                result += "### Policy Objects\n"
                try:
                    policies = meraki_client.get_organization_policy_objects(organization_id)
                    if policies:
                        result += f"- Total Policy Objects: {len(policies)}\n"
                        # Group by category
                        categories = {}
                        for policy in policies:
                            cat = policy.get('category', 'Unknown')
                            categories[cat] = categories.get(cat, 0) + 1
                        result += "- Policy Categories:\n"
                        for cat, count in categories.items():
                            result += f"  - {cat}: {count}\n"
                    else:
                        result += "- No policy objects configured\n"
                except Exception as e:
                    result += f"- Error fetching policy objects: {str(e)}\n"
                    
                # Check policy groups
                try:
                    groups = meraki_client.get_organization_policy_objects_groups(organization_id)
                    if groups:
                        result += f"- Policy Groups: {len(groups)}\n"
                except Exception as e:
                    pass  # Silent fail for groups
                result += "\n"
            
            # Check early access features
            if check_type in ['all', 'settings']:
                result += "### Early Access Features\n"
                try:
                    features = meraki_client.get_organization_early_access_features(organization_id)
                    opt_ins = meraki_client.get_organization_early_access_features_opt_ins(organization_id)
                    if opt_ins:
                        result += f"- Opted-in Features: {len(opt_ins)}\n"
                        for opt_in in opt_ins[:3]:
                            result += f"  - {opt_in.get('shortName', 'Unknown')}\n"
                        if len(opt_ins) > 3:
                            result += f"  - ... and {len(opt_ins) - 3} more features\n"
                    else:
                        result += "- No early access features enabled\n"
                except Exception as e:
                    result += f"- Error fetching early access features: {str(e)}\n"
                result += "\n"
            
            # Check administrators
            if check_type in ['all', 'settings']:
                result += "### Administrators\n"
                try:
                    admins = meraki_client.get_organization_admins(organization_id)
                    result += f"- Total Admins: {len(admins)}\n"
                    if admins:
                        # Group by access level
                        access_levels = {}
                        for admin in admins:
                            access = admin.get('orgAccess', 'Unknown')
                            access_levels[access] = access_levels.get(access, 0) + 1
                        result += "- Access Levels:\n"
                        for access, count in access_levels.items():
                            result += f"  - {access}: {count}\n"
                except Exception as e:
                    result += f"- Error fetching administrators: {str(e)}\n"
                result += "\n"
            
            # Check API usage (if available)
            if check_type in ['all', 'settings']:
                result += "### API Usage\n"
                try:
                    # Get recent API requests (last 5 minutes)
                    api_requests = meraki_client.get_organization_api_requests(organization_id, timespan=300)
                    if api_requests:
                        result += f"- Recent API Requests (last 5 min): {len(api_requests)}\n"
                    else:
                        result += "- No recent API activity\n"
                except Exception as e:
                    result += f"- Error fetching API usage: {str(e)}\n"
                result += "\n"
            
            result += "\n### Summary\n"
            result += "This organization appears to be "
            
            # Determine if it's a clone based on findings
            try:
                networks = meraki_client.get_organization_networks(organization_id)
                devices = meraki_client.get_organization_devices(organization_id)
                
                if not networks and not devices:
                    result += "**a clone or empty organization** with no networks or devices configured."
                else:
                    result += "an active organization with configured resources."
            except:
                result += "difficult to assess due to API errors."
                
            return result
            
        except Exception as e:
            return f"Failed to perform comprehensive check for organization {organization_id}: {str(e)}"
    
    @app.tool(
        name="compare_organizations",
        description="Compare two Meraki organizations to identify similarities and differences"
    )
    def compare_organizations(org_id_1: str, org_id_2: str):
        """
        Compare two Meraki organizations to identify similarities and differences.
        
        Args:
            org_id_1: ID of the first organization
            org_id_2: ID of the second organization
            
        Returns:
            Comparison report
        """
        try:
            result = f"# Organization Comparison\n"
            result += f"## Comparing Organizations:\n"
            result += f"- Organization 1: {org_id_1}\n"
            result += f"- Organization 2: {org_id_2}\n\n"
            
            # Get basic organization info
            try:
                org1 = meraki_client.get_organization(org_id_1)
                org2 = meraki_client.get_organization(org_id_2)
                
                result += "### Basic Information\n"
                result += f"| Property | Org 1 ({org1.get('name', 'Unknown')}) | Org 2 ({org2.get('name', 'Unknown')}) |\n"
                result += f"|----------|---------|----------|\n"
                result += f"| ID | {org_id_1} | {org_id_2} |\n"
                result += f"| Name | {org1.get('name', 'N/A')} | {org2.get('name', 'N/A')} |\n"
                result += f"| URL | {org1.get('url', 'N/A')} | {org2.get('url', 'N/A')} |\n"
                result += f"| API Enabled | {org1.get('api', {}).get('enabled', 'N/A')} | {org2.get('api', {}).get('enabled', 'N/A')} |\n"
                result += f"| Cloud Region | {org1.get('cloud', {}).get('region', {}).get('name', 'N/A')} | {org2.get('cloud', {}).get('region', {}).get('name', 'N/A')} |\n\n"
            except Exception as e:
                result += f"### Basic Information\n"
                result += f"Error fetching organization details: {str(e)}\n\n"
            
            # Compare networks
            try:
                networks1 = meraki_client.get_organization_networks(org_id_1)
                networks2 = meraki_client.get_organization_networks(org_id_2)
                
                result += "### Networks\n"
                result += f"| Metric | Org 1 | Org 2 |\n"
                result += f"|--------|-------|-------|\n"
                result += f"| Total Networks | {len(networks1)} | {len(networks2)} |\n"
                
                # Get network types
                types1 = {}
                types2 = {}
                for net in networks1:
                    for ptype in net.get('productTypes', []):
                        types1[ptype] = types1.get(ptype, 0) + 1
                for net in networks2:
                    for ptype in net.get('productTypes', []):
                        types2[ptype] = types2.get(ptype, 0) + 1
                
                all_types = set(types1.keys()) | set(types2.keys())
                for ptype in sorted(all_types):
                    result += f"| {ptype} Networks | {types1.get(ptype, 0)} | {types2.get(ptype, 0)} |\n"
                result += "\n"
            except Exception as e:
                result += f"### Networks\n"
                result += f"Error comparing networks: {str(e)}\n\n"
            
            # Compare devices
            try:
                devices1 = meraki_client.get_organization_devices(org_id_1)
                devices2 = meraki_client.get_organization_devices(org_id_2)
                
                result += "### Devices\n"
                result += f"| Metric | Org 1 | Org 2 |\n"
                result += f"|--------|-------|-------|\n"
                result += f"| Total Devices | {len(devices1)} | {len(devices2)} |\n"
                
                # Group by model
                models1 = {}
                models2 = {}
                for device in devices1:
                    model = device.get('model', 'Unknown')
                    models1[model] = models1.get(model, 0) + 1
                for device in devices2:
                    model = device.get('model', 'Unknown')
                    models2[model] = models2.get(model, 0) + 1
                
                all_models = set(models1.keys()) | set(models2.keys())
                for model in sorted(all_models):
                    result += f"| {model} | {models1.get(model, 0)} | {models2.get(model, 0)} |\n"
                result += "\n"
            except Exception as e:
                result += f"### Devices\n"
                result += f"Error comparing devices: {str(e)}\n\n"
            
            # Compare administrators
            try:
                admins1 = meraki_client.get_organization_admins(org_id_1)
                admins2 = meraki_client.get_organization_admins(org_id_2)
                
                result += "### Administrators\n"
                result += f"| Metric | Org 1 | Org 2 |\n"
                result += f"|--------|-------|-------|\n"
                result += f"| Total Admins | {len(admins1)} | {len(admins2)} |\n"
                
                # Check for common admins
                emails1 = {admin.get('email', '').lower() for admin in admins1}
                emails2 = {admin.get('email', '').lower() for admin in admins2}
                common_admins = emails1 & emails2
                
                if common_admins:
                    result += f"| Common Admins | {len(common_admins)} | {len(common_admins)} |\n"
                    result += f"\nCommon administrators:\n"
                    for email in sorted(common_admins):
                        result += f"- {email}\n"
                result += "\n"
            except Exception as e:
                result += f"### Administrators\n"
                result += f"Error comparing administrators: {str(e)}\n\n"
            
            # Compare licenses
            try:
                licenses1 = meraki_client.get_organization_licenses(org_id_1)
                licenses2 = meraki_client.get_organization_licenses(org_id_2)
                
                result += "### Licenses\n"
                result += f"| Metric | Org 1 | Org 2 |\n"
                result += f"|--------|-------|-------|\n"
                result += f"| Total Licenses | {len(licenses1)} | {len(licenses2)} |\n"
                
                # Group by state
                states1 = {}
                states2 = {}
                for lic in licenses1:
                    state = lic.get('state', 'Unknown')
                    states1[state] = states1.get(state, 0) + 1
                for lic in licenses2:
                    state = lic.get('state', 'Unknown')
                    states2[state] = states2.get(state, 0) + 1
                
                all_states = set(states1.keys()) | set(states2.keys())
                for state in sorted(all_states):
                    result += f"| {state} Licenses | {states1.get(state, 0)} | {states2.get(state, 0)} |\n"
                result += "\n"
            except Exception as e:
                result += f"### Licenses\n"
                result += f"Error comparing licenses: {str(e)}\n\n"
            
            # Summary
            result += "### Summary\n"
            
            # Determine if they might be clones
            clone_indicators = []
            
            try:
                # Check if both have no networks/devices
                if not networks1 and not networks2 and not devices1 and not devices2:
                    clone_indicators.append("Both organizations have no networks or devices")
                
                # Check for similar names
                if 'clone' in org1.get('name', '').lower() and 'clone' in org2.get('name', '').lower():
                    clone_indicators.append("Both organizations have 'clone' in their names")
                
                # Check for common administrators
                if common_admins:
                    clone_indicators.append(f"Organizations share {len(common_admins)} common administrator(s)")
                
                # Check for same cloud region
                if org1.get('cloud', {}).get('region', {}).get('name') == org2.get('cloud', {}).get('region', {}).get('name'):
                    clone_indicators.append("Both organizations are in the same cloud region")
            except:
                pass
            
            if clone_indicators:
                result += "**Potential Clone Indicators:**\n"
                for indicator in clone_indicators:
                    result += f"- {indicator}\n"
            else:
                result += "No obvious clone indicators found.\n"
            
            return result
            
        except Exception as e:
            return f"Failed to compare organizations: {str(e)}"
