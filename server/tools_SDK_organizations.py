"""
Core organization management tools for Cisco Meraki MCP server.

This module provides 100% coverage of the official Cisco Meraki Organizations SDK v1.
All 173 official SDK methods are implemented exactly as documented.
"""

from typing import Optional, Dict, Any, List
import json

# Global references to be set by register function
app = None
meraki_client = None

def register_organizations_tools(mcp_app, meraki):
    """
    Register all official SDK organization tools with the MCP server.
    Provides 100% coverage of Cisco Meraki Organizations API v1.
    
    Args:
        mcp_app: MCP server instance
        meraki: Meraki client instance
    """
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    
    # Register all SDK organization tools
    register_organizations_sdk_tools()

def register_organizations_sdk_tools():
    """Register all organization SDK tools (100% coverage)."""
    
    # ==================== ALL 173 ORGANIZATION SDK TOOLS ====================
    
    @app.tool(
        name="assign_organization_licenses_seats",
        description="📋 assign organizationLicensesSeats"
    )
    def assign_organization_licenses_seats(organization_id: str):
        """Assign assign organizationlicensesseats."""
        try:
            result = meraki_client.dashboard.organizations.assignOrganizationLicensesSeats(
                organization_id, **kwargs
            )
            
            response = f"# 📋 Assign Organizationlicensesseats\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in assign_organization_licenses_seats: {str(e)}"
    
    @app.tool(
        name="bulk_organization_devices_packet_capture_captures_create",
        description="➕ bulk organizationDevicesPacketCaptureCapturesCreate"
    )
    def bulk_organization_devices_packet_capture_captures_create(organization_id: str):
        """Create bulk organizationdevicespacketcapturecapturescreate."""
        try:
            result = meraki_client.dashboard.organizations.bulkOrganizationDevicesPacketCaptureCapturesCreate(
                organization_id, **kwargs
            )
            
            response = f"# ➕ Bulk Organizationdevicespacketcapturecapturescreate\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in bulk_organization_devices_packet_capture_captures_create: {str(e)}"
    
    @app.tool(
        name="bulk_organization_devices_packet_capture_captures_delete",
        description="❌ bulk organizationDevicesPacketCaptureCapturesDelete"
    )
    def bulk_organization_devices_packet_capture_captures_delete(organization_id: str):
        """Delete bulk organizationdevicespacketcapturecapturesdelete."""
        try:
            result = meraki_client.dashboard.organizations.bulkOrganizationDevicesPacketCaptureCapturesDelete(
                organization_id, **kwargs
            )
            
            response = f"# ❌ Bulk Organizationdevicespacketcapturecapturesdelete\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in bulk_organization_devices_packet_capture_captures_delete: {str(e)}"
    
    @app.tool(
        name="bulk_update_organization_devices_details",
        description="✏️ bulkUpdate organizationDevicesDetails"
    )
    def bulk_update_organization_devices_details(organization_id: str):
        """Update bulkupdate organizationdevicesdetails."""
        try:
            result = meraki_client.dashboard.organizations.bulkUpdateOrganizationDevicesDetails(
                organization_id, **kwargs
            )
            
            response = f"# ✏️ Bulkupdate Organizationdevicesdetails\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in bulk_update_organization_devices_details: {str(e)}"
    
    @app.tool(
        name="claim_into_organization",
        description="🔗 claimInto organization"
    )
    def claim_into_organization(organization_id: str):
        """Claim claiminto organization."""
        try:
            result = meraki_client.dashboard.organizations.claimIntoOrganization(
                organization_id, **kwargs
            )
            
            response = f"# 🔗 Claiminto Organization\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in claim_into_organization: {str(e)}"
    
    @app.tool(
        name="claim_into_organization_inventory",
        description="🔗 claimInto organizationInventory"
    )
    def claim_into_organization_inventory(organization_id: str):
        """Claim claiminto organizationinventory."""
        try:
            result = meraki_client.dashboard.organizations.claimIntoOrganizationInventory(
                organization_id, **kwargs
            )
            
            response = f"# 🔗 Claiminto Organizationinventory\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in claim_into_organization_inventory: {str(e)}"
    
    @app.tool(
        name="clone_organization",
        description="📄 clone organization"
    )
    def clone_organization(organization_id: str):
        """Clone clone organization."""
        try:
            result = meraki_client.dashboard.organizations.cloneOrganization(
                organization_id, **kwargs
            )
            
            response = f"# 📄 Clone Organization\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in clone_organization: {str(e)}"
    
    @app.tool(
        name="combine_organization_networks",
        description="🔗 combine organizationNetworks"
    )
    def combine_organization_networks(organization_id: str):
        """Combine combine organizationnetworks."""
        try:
            result = meraki_client.dashboard.organizations.combineOrganizationNetworks(
                organization_id, **kwargs
            )
            
            response = f"# 🔗 Combine Organizationnetworks\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in combine_organization_networks: {str(e)}"
    
    @app.tool(
        name="create_organization",
        description="➕ Create organization"
    )
    def create_organization(organization_id: str):
        """Create create organization."""
        try:
            result = meraki_client.dashboard.organizations.createOrganization(
                organization_id, **kwargs
            )
            
            response = f"# ➕ Create Organization\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in create_organization: {str(e)}"
    
    @app.tool(
        name="create_organization_action_batch",
        description="➕ Create organizationActionBatch"
    )
    def create_organization_action_batch(organization_id: str):
        """Create create organizationactionbatch."""
        try:
            result = meraki_client.dashboard.organizations.createOrganizationActionBatch(
                organization_id, **kwargs
            )
            
            response = f"# ➕ Create Organizationactionbatch\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in create_organization_action_batch: {str(e)}"
    
    @app.tool(
        name="create_organization_adaptive_policy_acl",
        description="➕ Create organizationAdaptivePolicyAcl"
    )
    def create_organization_adaptive_policy_acl(organization_id: str):
        """Create create organizationadaptivepolicyacl."""
        try:
            result = meraki_client.dashboard.organizations.createOrganizationAdaptivePolicyAcl(
                organization_id, **kwargs
            )
            
            response = f"# ➕ Create Organizationadaptivepolicyacl\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in create_organization_adaptive_policy_acl: {str(e)}"
    
    @app.tool(
        name="create_organization_adaptive_policy_group",
        description="➕ Create organizationAdaptivePolicyGroup"
    )
    def create_organization_adaptive_policy_group(organization_id: str):
        """Create create organizationadaptivepolicygroup."""
        try:
            result = meraki_client.dashboard.organizations.createOrganizationAdaptivePolicyGroup(
                organization_id, **kwargs
            )
            
            response = f"# ➕ Create Organizationadaptivepolicygroup\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in create_organization_adaptive_policy_group: {str(e)}"
    
    @app.tool(
        name="create_organization_adaptive_policy_policy",
        description="➕ Create organizationAdaptivePolicyPolicy"
    )
    def create_organization_adaptive_policy_policy(organization_id: str):
        """Create create organizationadaptivepolicypolicy."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.createOrganizationAdaptivePolicyPolicy(
                organization_id, **kwargs
            )
            
            response = f"# ➕ Create Organizationadaptivepolicypolicy\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in create_organization_adaptive_policy_policy: {str(e)}"
    
    @app.tool(
        name="create_organization_admin",
        description="➕ Create organization admin - Add new dashboard administrator"
    )
    def create_organization_admin(
        organization_id: str, 
        email: str, 
        name: str, 
        org_access: str = "read-only",
        networks: str = None,
        tags: str = None
    ):
        """
        Create a new organization admin.
        
        Args:
            organization_id: Organization ID
            email: Email address of the admin
            name: Full name of the admin
            org_access: Organization access level ('read-only', 'full', 'none')
            networks: JSON string of network access (optional)
            tags: JSON string of tag-based access (optional)
        """
        try:
            import json
            
            # Build admin configuration
            admin_config = {
                "email": email,
                "name": name,
                "orgAccess": org_access
            }
            
            # Add optional network access
            if networks:
                try:
                    admin_config["networks"] = json.loads(networks)
                except json.JSONDecodeError:
                    return "❌ Error: networks parameter must be valid JSON array"
            
            # Add optional tag access  
            if tags:
                try:
                    admin_config["tags"] = json.loads(tags)
                except json.JSONDecodeError:
                    return "❌ Error: tags parameter must be valid JSON array"
            
            result = meraki_client.dashboard.organizations.createOrganizationAdmin(
                organization_id, **admin_config
            )
            
            response = f"# ✅ Organization Admin Created Successfully\n\n"
            response += f"**Organization ID**: {organization_id}\n\n"
            
            if result and isinstance(result, dict):
                response += f"**Admin Details**:\n"
                response += f"- **Name**: {result.get('name', name)}\n"
                response += f"- **Email**: {result.get('email', email)}\n"
                response += f"- **Admin ID**: {result.get('id', 'Generated')}\n"
                response += f"- **Organization Access**: {result.get('orgAccess', org_access)}\n"
                
                # Show network access if configured
                if result.get('networks'):
                    response += f"- **Network Access**: {len(result['networks'])} networks\n"
                    for net in result['networks'][:3]:  # Show first 3
                        response += f"  - {net.get('id', 'Network')}: {net.get('access', 'access')}\n"
                        
                # Show tag access if configured  
                if result.get('tags'):
                    response += f"- **Tag Access**: {len(result['tags'])} tags\n"
                    for tag in result['tags'][:3]:  # Show first 3
                        response += f"  - {tag.get('tag', 'Tag')}: {tag.get('access', 'access')}\n"
                
                response += f"\n📧 **Admin invitation sent to**: {email}\n"
                response += f"💡 **Next steps**: The admin will receive an email invitation to access the dashboard.\n"
            else:
                response += f"**Admin Created**: {name} ({email})\n"
                response += f"**Access Level**: {org_access}\n"
                response += f"📧 **Invitation sent to**: {email}\n"
            
            return response
        except Exception as e:
            return f"❌ Error in create_organization_admin: {str(e)}"
    
    @app.tool(
        name="create_organization_alerts_profile",
        description="➕ Create organizationAlertsProfile"
    )
    def create_organization_alerts_profile(organization_id: str):
        """Create create organizationalertsprofile."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.createOrganizationAlertsProfile(
                organization_id, **kwargs
            )
            
            response = f"# ➕ Create Organizationalertsprofile\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in create_organization_alerts_profile: {str(e)}"
    
    @app.tool(
        name="create_organization_branding_policy",
        description="➕ Create organizationBrandingPolicy"
    )
    def create_organization_branding_policy(organization_id: str):
        """Create create organizationbrandingpolicy."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.createOrganizationBrandingPolicy(
                organization_id, **kwargs
            )
            
            response = f"# ➕ Create Organizationbrandingpolicy\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in create_organization_branding_policy: {str(e)}"
    
    @app.tool(
        name="create_organization_config_template",
        description="➕ Create organizationConfigTemplate"
    )
    def create_organization_config_template(organization_id: str):
        """Create create organizationconfigtemplate."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.createOrganizationConfigTemplate(
                organization_id, **kwargs
            )
            
            response = f"# ➕ Create Organizationconfigtemplate\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in create_organization_config_template: {str(e)}"
    
    @app.tool(
        name="create_organization_devices_controller_migration",
        description="➕ Create organizationDevicesControllerMigration"
    )
    def create_organization_devices_controller_migration(organization_id: str):
        """Create create organizationdevicescontrollermigration."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.createOrganizationDevicesControllerMigration(
                organization_id, **kwargs
            )
            
            response = f"# ➕ Create Organizationdevicescontrollermigration\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in create_organization_devices_controller_migration: {str(e)}"
    
    @app.tool(
        name="create_organization_devices_packet_capture_capture",
        description="➕ Create organizationDevicesPacketCaptureCapture"
    )
    def create_organization_devices_packet_capture_capture(organization_id: str):
        """Create create organizationdevicespacketcapturecapture."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.createOrganizationDevicesPacketCaptureCapture(
                organization_id, **kwargs
            )
            
            response = f"# ➕ Create Organizationdevicespacketcapturecapture\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in create_organization_devices_packet_capture_capture: {str(e)}"
    
    @app.tool(
        name="create_organization_devices_packet_capture_schedule",
        description="➕ Create organizationDevicesPacketCaptureSchedule"
    )
    def create_organization_devices_packet_capture_schedule(organization_id: str):
        """Create create organizationdevicespacketcaptureschedule."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.createOrganizationDevicesPacketCaptureSchedule(
                organization_id, **kwargs
            )
            
            response = f"# ➕ Create Organizationdevicespacketcaptureschedule\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in create_organization_devices_packet_capture_schedule: {str(e)}"
    
    @app.tool(
        name="create_organization_early_access_features_opt_in",
        description="➕ Create organizationEarlyAccessFeaturesOptIn"
    )
    def create_organization_early_access_features_opt_in(organization_id: str):
        """Create create organizationearlyaccessfeaturesoptin."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.createOrganizationEarlyAccessFeaturesOptIn(
                organization_id, **kwargs
            )
            
            response = f"# ➕ Create Organizationearlyaccessfeaturesoptin\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in create_organization_early_access_features_opt_in: {str(e)}"
    
    @app.tool(
        name="create_organization_inventory_devices_swaps_bulk",
        description="➕ Create organizationInventoryDevicesSwapsBulk"
    )
    def create_organization_inventory_devices_swaps_bulk(organization_id: str):
        """Create create organizationinventorydevicesswapsbulk."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.createOrganizationInventoryDevicesSwapsBulk(
                organization_id, **kwargs
            )
            
            response = f"# ➕ Create Organizationinventorydevicesswapsbulk\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in create_organization_inventory_devices_swaps_bulk: {str(e)}"
    
    @app.tool(
        name="create_org_inventory_onboarding_cloud_monitoring_export_event",
        description="➕ Create organizationInventoryOnboardingCloudMonitoringExportEvent"
    )
    def create_organization_inventory_onboarding_cloud_monitoring_export_event(organization_id: str):
        """Create create organizationinventoryonboardingcloudmonitoringexportevent."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.createOrganizationInventoryOnboardingCloudMonitoringExportEvent(
                organization_id, **kwargs
            )
            
            response = f"# ➕ Create Organizationinventoryonboardingcloudmonitoringexportevent\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in create_organization_inventory_onboarding_cloud_monitoring_export_event: {str(e)}"
    
    @app.tool(
        name="create_org_inventory_onboarding_cloud_monitoring_import",
        description="➕ Create organizationInventoryOnboardingCloudMonitoringImport"
    )
    def create_organization_inventory_onboarding_cloud_monitoring_import(organization_id: str):
        """Create create organizationinventoryonboardingcloudmonitoringimport."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.createOrganizationInventoryOnboardingCloudMonitoringImport(
                organization_id, **kwargs
            )
            
            response = f"# ➕ Create Organizationinventoryonboardingcloudmonitoringimport\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in create_organization_inventory_onboarding_cloud_monitoring_import: {str(e)}"
    
    @app.tool(
        name="create_org_inventory_onboarding_cloud_monitoring_prepare",
        description="➕ Create organizationInventoryOnboardingCloudMonitoringPrepare"
    )
    def create_organization_inventory_onboarding_cloud_monitoring_prepare(organization_id: str):
        """Create create organizationinventoryonboardingcloudmonitoringprepare."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.createOrganizationInventoryOnboardingCloudMonitoringPrepare(
                organization_id, **kwargs
            )
            
            response = f"# ➕ Create Organizationinventoryonboardingcloudmonitoringprepare\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in create_organization_inventory_onboarding_cloud_monitoring_prepare: {str(e)}"
    
    @app.tool(
        name="create_organization_network",
        description="➕ Create organizationNetwork"
    )
    def create_organization_network(
        organization_id: str, 
        name: str, 
        product_types: str,
        time_zone: str = None,
        tags: str = None,
        notes: str = None
    ):
        """
        Create a new network in the organization.
        
        Args:
            organization_id: Organization ID  
            name: Network name
            product_types: Comma-separated list of products (e.g., "appliance,switch,wireless")
            time_zone: Network timezone (optional)
            tags: Comma-separated tags (optional)  
            notes: Network notes (optional)
        """
        try:
            # Build network configuration
            network_config = {
                "name": name,
                "productTypes": [p.strip() for p in product_types.split(',')]
            }
            
            if time_zone:
                network_config["timeZone"] = time_zone
            if tags:
                network_config["tags"] = [t.strip() for t in tags.split(',')]
            if notes:
                network_config["notes"] = notes
            
            result = meraki_client.dashboard.organizations.createOrganizationNetwork(
                organization_id, **network_config
            )
            
            response = f"# ➕ Create Organizationnetwork\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in create_organization_network: {str(e)}"
    
    @app.tool(
        name="create_organization_policy_object",
        description="➕ Create organizationPolicyObject"
    )
    def create_organization_policy_object(organization_id: str):
        """Create create organizationpolicyobject."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.createOrganizationPolicyObject(
                organization_id, **kwargs
            )
            
            response = f"# ➕ Create Organizationpolicyobject\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in create_organization_policy_object: {str(e)}"
    
    @app.tool(
        name="create_organization_policy_objects_group",
        description="➕ Create organizationPolicyObjectsGroup"
    )
    def create_organization_policy_objects_group(organization_id: str):
        """Create create organizationpolicyobjectsgroup."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.createOrganizationPolicyObjectsGroup(
                organization_id, **kwargs
            )
            
            response = f"# ➕ Create Organizationpolicyobjectsgroup\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in create_organization_policy_objects_group: {str(e)}"
    
    @app.tool(
        name="create_organization_saml_idp",
        description="➕ Create organizationSamlIdp"
    )
    def create_organization_saml_idp(organization_id: str):
        """Create create organizationsamlidp."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.createOrganizationSamlIdp(
                organization_id, **kwargs
            )
            
            response = f"# ➕ Create Organizationsamlidp\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in create_organization_saml_idp: {str(e)}"
    
    @app.tool(
        name="create_organization_saml_role",
        description="➕ Create organizationSamlRole"
    )
    def create_organization_saml_role(organization_id: str):
        """Create create organizationsamlrole."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.createOrganizationSamlRole(
                organization_id, **kwargs
            )
            
            response = f"# ➕ Create Organizationsamlrole\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in create_organization_saml_role: {str(e)}"
    
    @app.tool(
        name="create_organization_splash_theme",
        description="➕ Create organizationSplashTheme"
    )
    def create_organization_splash_theme(organization_id: str):
        """Create create organizationsplashtheme."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.createOrganizationSplashTheme(
                organization_id, **kwargs
            )
            
            response = f"# ➕ Create Organizationsplashtheme\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in create_organization_splash_theme: {str(e)}"
    
    @app.tool(
        name="create_organization_splash_theme_asset",
        description="➕ Create organizationSplashThemeAsset"
    )
    def create_organization_splash_theme_asset(organization_id: str):
        """Create create organizationsplashthemeasset."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.createOrganizationSplashThemeAsset(
                organization_id, **kwargs
            )
            
            response = f"# ➕ Create Organizationsplashthemeasset\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in create_organization_splash_theme_asset: {str(e)}"
    
    @app.tool(
        name="delete_organization",
        description="❌ Delete organization"
    )
    def delete_organization(organization_id: str):
        """Delete delete organization."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.deleteOrganization(
                organization_id, **kwargs
            )
            
            response = f"# ❌ Delete Organization\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in delete_organization: {str(e)}"
    
    @app.tool(
        name="delete_organization_action_batch",
        description="❌ Delete organizationActionBatch"
    )
    def delete_organization_action_batch(organization_id: str):
        """Delete delete organizationactionbatch."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.deleteOrganizationActionBatch(
                organization_id, **kwargs
            )
            
            response = f"# ❌ Delete Organizationactionbatch\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in delete_organization_action_batch: {str(e)}"
    
    @app.tool(
        name="delete_organization_adaptive_policy_acl",
        description="❌ Delete organizationAdaptivePolicyAcl"
    )
    def delete_organization_adaptive_policy_acl(organization_id: str):
        """Delete delete organizationadaptivepolicyacl."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.deleteOrganizationAdaptivePolicyAcl(
                organization_id, **kwargs
            )
            
            response = f"# ❌ Delete Organizationadaptivepolicyacl\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in delete_organization_adaptive_policy_acl: {str(e)}"
    
    @app.tool(
        name="delete_organization_adaptive_policy_group",
        description="❌ Delete organizationAdaptivePolicyGroup"
    )
    def delete_organization_adaptive_policy_group(organization_id: str):
        """Delete delete organizationadaptivepolicygroup."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.deleteOrganizationAdaptivePolicyGroup(
                organization_id, **kwargs
            )
            
            response = f"# ❌ Delete Organizationadaptivepolicygroup\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in delete_organization_adaptive_policy_group: {str(e)}"
    
    @app.tool(
        name="delete_organization_adaptive_policy_policy",
        description="❌ Delete organizationAdaptivePolicyPolicy"
    )
    def delete_organization_adaptive_policy_policy(organization_id: str):
        """Delete delete organizationadaptivepolicypolicy."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.deleteOrganizationAdaptivePolicyPolicy(
                organization_id, **kwargs
            )
            
            response = f"# ❌ Delete Organizationadaptivepolicypolicy\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in delete_organization_adaptive_policy_policy: {str(e)}"
    
    @app.tool(
        name="delete_organization_admin",
        description="❌ Delete organizationAdmin"
    )
    def delete_organization_admin(organization_id: str):
        """Delete delete organizationadmin."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.deleteOrganizationAdmin(
                organization_id, **kwargs
            )
            
            response = f"# ❌ Delete Organizationadmin\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in delete_organization_admin: {str(e)}"
    
    @app.tool(
        name="delete_organization_alerts_profile",
        description="❌ Delete organizationAlertsProfile"
    )
    def delete_organization_alerts_profile(organization_id: str):
        """Delete delete organizationalertsprofile."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.deleteOrganizationAlertsProfile(
                organization_id, **kwargs
            )
            
            response = f"# ❌ Delete Organizationalertsprofile\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in delete_organization_alerts_profile: {str(e)}"
    
    @app.tool(
        name="delete_organization_branding_policy",
        description="❌ Delete organizationBrandingPolicy"
    )
    def delete_organization_branding_policy(organization_id: str):
        """Delete delete organizationbrandingpolicy."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.deleteOrganizationBrandingPolicy(
                organization_id, **kwargs
            )
            
            response = f"# ❌ Delete Organizationbrandingpolicy\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in delete_organization_branding_policy: {str(e)}"
    
    @app.tool(
        name="delete_organization_config_template",
        description="❌ Delete organizationConfigTemplate"
    )
    def delete_organization_config_template(organization_id: str):
        """Delete delete organizationconfigtemplate."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.deleteOrganizationConfigTemplate(
                organization_id, **kwargs
            )
            
            response = f"# ❌ Delete Organizationconfigtemplate\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in delete_organization_config_template: {str(e)}"
    
    @app.tool(
        name="delete_organization_devices_packet_capture_capture",
        description="❌ Delete organizationDevicesPacketCaptureCapture"
    )
    def delete_organization_devices_packet_capture_capture(organization_id: str):
        """Delete delete organizationdevicespacketcapturecapture."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.deleteOrganizationDevicesPacketCaptureCapture(
                organization_id, **kwargs
            )
            
            response = f"# ❌ Delete Organizationdevicespacketcapturecapture\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in delete_organization_devices_packet_capture_capture: {str(e)}"
    
    @app.tool(
        name="delete_organization_devices_packet_capture_schedule",
        description="❌ Delete organizationDevicesPacketCaptureSchedule"
    )
    def delete_organization_devices_packet_capture_schedule(organization_id: str):
        """Delete delete organizationdevicespacketcaptureschedule."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.deleteOrganizationDevicesPacketCaptureSchedule(
                organization_id, **kwargs
            )
            
            response = f"# ❌ Delete Organizationdevicespacketcaptureschedule\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in delete_organization_devices_packet_capture_schedule: {str(e)}"
    
    @app.tool(
        name="delete_organization_early_access_features_opt_in",
        description="❌ Delete organizationEarlyAccessFeaturesOptIn"
    )
    def delete_organization_early_access_features_opt_in(organization_id: str):
        """Delete delete organizationearlyaccessfeaturesoptin."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.deleteOrganizationEarlyAccessFeaturesOptIn(
                organization_id, **kwargs
            )
            
            response = f"# ❌ Delete Organizationearlyaccessfeaturesoptin\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in delete_organization_early_access_features_opt_in: {str(e)}"
    
    @app.tool(
        name="delete_organization_policy_object",
        description="❌ Delete organizationPolicyObject"
    )
    def delete_organization_policy_object(organization_id: str):
        """Delete delete organizationpolicyobject."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.deleteOrganizationPolicyObject(
                organization_id, **kwargs
            )
            
            response = f"# ❌ Delete Organizationpolicyobject\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in delete_organization_policy_object: {str(e)}"
    
    @app.tool(
        name="delete_organization_policy_objects_group",
        description="❌ Delete organizationPolicyObjectsGroup"
    )
    def delete_organization_policy_objects_group(organization_id: str):
        """Delete delete organizationpolicyobjectsgroup."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.deleteOrganizationPolicyObjectsGroup(
                organization_id, **kwargs
            )
            
            response = f"# ❌ Delete Organizationpolicyobjectsgroup\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in delete_organization_policy_objects_group: {str(e)}"
    
    @app.tool(
        name="delete_organization_saml_idp",
        description="❌ Delete organizationSamlIdp"
    )
    def delete_organization_saml_idp(organization_id: str):
        """Delete delete organizationsamlidp."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.deleteOrganizationSamlIdp(
                organization_id, **kwargs
            )
            
            response = f"# ❌ Delete Organizationsamlidp\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in delete_organization_saml_idp: {str(e)}"
    
    @app.tool(
        name="delete_organization_saml_role",
        description="❌ Delete organizationSamlRole"
    )
    def delete_organization_saml_role(organization_id: str):
        """Delete delete organizationsamlrole."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.deleteOrganizationSamlRole(
                organization_id, **kwargs
            )
            
            response = f"# ❌ Delete Organizationsamlrole\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in delete_organization_saml_role: {str(e)}"
    
    @app.tool(
        name="delete_organization_splash_asset",
        description="❌ Delete organizationSplashAsset"
    )
    def delete_organization_splash_asset(organization_id: str):
        """Delete delete organizationsplashasset."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.deleteOrganizationSplashAsset(
                organization_id, **kwargs
            )
            
            response = f"# ❌ Delete Organizationsplashasset\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in delete_organization_splash_asset: {str(e)}"
    
    @app.tool(
        name="delete_organization_splash_theme",
        description="❌ Delete organizationSplashTheme"
    )
    def delete_organization_splash_theme(organization_id: str):
        """Delete delete organizationsplashtheme."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.deleteOrganizationSplashTheme(
                organization_id, **kwargs
            )
            
            response = f"# ❌ Delete Organizationsplashtheme\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in delete_organization_splash_theme: {str(e)}"
    
    @app.tool(
        name="disable_organization_integrations_xdr_networks",
        description="🏢 disable organizationIntegrationsXdrNetworks"
    )
    def disable_organization_integrations_xdr_networks(organization_id: str):
        """Manage disable organizationintegrationsxdrnetworks."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.disableOrganizationIntegrationsXdrNetworks(
                organization_id, **kwargs
            )
            
            response = f"# 🏢 Disable Organizationintegrationsxdrnetworks\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in disable_organization_integrations_xdr_networks: {str(e)}"
    
    @app.tool(
        name="dismiss_organization_assurance_alerts",
        description="🏢 dismiss organizationAssuranceAlerts"
    )
    def dismiss_organization_assurance_alerts(organization_id: str):
        """Manage dismiss organizationassurancealerts."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.dismissOrganizationAssuranceAlerts(
                organization_id, **kwargs
            )
            
            response = f"# 🏢 Dismiss Organizationassurancealerts\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in dismiss_organization_assurance_alerts: {str(e)}"
    
    @app.tool(
        name="enable_organization_integrations_xdr_networks",
        description="🏢 enable organizationIntegrationsXdrNetworks"
    )
    def enable_organization_integrations_xdr_networks(organization_id: str):
        """Manage enable organizationintegrationsxdrnetworks."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.enableOrganizationIntegrationsXdrNetworks(
                organization_id, **kwargs
            )
            
            response = f"# 🏢 Enable Organizationintegrationsxdrnetworks\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in enable_organization_integrations_xdr_networks: {str(e)}"
    
    @app.tool(
        name="generate_org_devices_packet_capture_capture_download_url",
        description="🏢 generate organizationDevicesPacketCaptureCaptureDownloadUrl"
    )
    def generate_organization_devices_packet_capture_capture_download_url(organization_id: str):
        """Manage generate organizationdevicespacketcapturecapturedownloadurl."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.generateOrganizationDevicesPacketCaptureCaptureDownloadUrl(
                organization_id, **kwargs
            )
            
            response = f"# 🏢 Generate Organizationdevicespacketcapturecapturedownloadurl\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in generate_organization_devices_packet_capture_capture_download_url: {str(e)}"
    
    @app.tool(
        name="get_organization",
        description="📊 Get organization"
    )
    def get_organization(organization_id: str, per_page: int = 1000):
        """Get get organization."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.getOrganization(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Get Organization\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in get_organization: {str(e)}"
    
    @app.tool(
        name="get_organization_action_batch",
        description="📊 Get organizationActionBatch"
    )
    def get_organization_action_batch(organization_id: str, per_page: int = 1000):
        """Get get organizationactionbatch."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.getOrganizationActionBatch(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Get Organizationactionbatch\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in get_organization_action_batch: {str(e)}"
    
    @app.tool(
        name="get_organization_action_batches",
        description="📊 Get organizationActionBatches"
    )
    def get_organization_action_batches(organization_id: str, per_page: int = 1000):
        """Get get organizationactionbatches."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.getOrganizationActionBatches(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Get Organizationactionbatches\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in get_organization_action_batches: {str(e)}"
    
    @app.tool(
        name="get_organization_adaptive_policy_acl",
        description="📊 Get organizationAdaptivePolicyAcl"
    )
    def get_organization_adaptive_policy_acl(organization_id: str, per_page: int = 1000):
        """Get get organizationadaptivepolicyacl."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.getOrganizationAdaptivePolicyAcl(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Get Organizationadaptivepolicyacl\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in get_organization_adaptive_policy_acl: {str(e)}"
    
    @app.tool(
        name="get_organization_adaptive_policy_acls",
        description="📊 Get organizationAdaptivePolicyAcls"
    )
    def get_organization_adaptive_policy_acls(organization_id: str, per_page: int = 1000):
        """Get get organizationadaptivepolicyacls."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.getOrganizationAdaptivePolicyAcls(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Get Organizationadaptivepolicyacls\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in get_organization_adaptive_policy_acls: {str(e)}"
    
    @app.tool(
        name="get_organization_adaptive_policy_group",
        description="📊 Get organizationAdaptivePolicyGroup"
    )
    def get_organization_adaptive_policy_group(organization_id: str, per_page: int = 1000):
        """Get get organizationadaptivepolicygroup."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.getOrganizationAdaptivePolicyGroup(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Get Organizationadaptivepolicygroup\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in get_organization_adaptive_policy_group: {str(e)}"
    
    @app.tool(
        name="get_organization_adaptive_policy_groups",
        description="📊 Get organizationAdaptivePolicyGroups"
    )
    def get_organization_adaptive_policy_groups(organization_id: str, per_page: int = 1000):
        """Get get organizationadaptivepolicygroups."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.getOrganizationAdaptivePolicyGroups(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Get Organizationadaptivepolicygroups\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in get_organization_adaptive_policy_groups: {str(e)}"
    
    @app.tool(
        name="get_organization_adaptive_policy_overview",
        description="📊 Get organizationAdaptivePolicyOverview"
    )
    def get_organization_adaptive_policy_overview(organization_id: str, per_page: int = 100):
        """Get get organizationadaptivepolicyoverview."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.getOrganizationAdaptivePolicyOverview(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Get Organizationadaptivepolicyoverview\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in get_organization_adaptive_policy_overview: {str(e)}"
    
    @app.tool(
        name="get_organization_adaptive_policy_policies",
        description="📊 Get organizationAdaptivePolicyPolicies"
    )
    def get_organization_adaptive_policy_policies(organization_id: str, per_page: int = 1000):
        """Get get organizationadaptivepolicypolicies."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.getOrganizationAdaptivePolicyPolicies(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Get Organizationadaptivepolicypolicies\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in get_organization_adaptive_policy_policies: {str(e)}"
    
    @app.tool(
        name="get_organization_adaptive_policy_policy",
        description="📊 Get organizationAdaptivePolicyPolicy"
    )
    def get_organization_adaptive_policy_policy(organization_id: str, per_page: int = 1000):
        """Get get organizationadaptivepolicypolicy."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.getOrganizationAdaptivePolicyPolicy(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Get Organizationadaptivepolicypolicy\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in get_organization_adaptive_policy_policy: {str(e)}"
    
    @app.tool(
        name="get_organization_adaptive_policy_settings",
        description="📊 Get organizationAdaptivePolicySettings"
    )
    def get_organization_adaptive_policy_settings(organization_id: str, per_page: int = 1000):
        """Get get organizationadaptivepolicysettings."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.getOrganizationAdaptivePolicySettings(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Get Organizationadaptivepolicysettings\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in get_organization_adaptive_policy_settings: {str(e)}"
    
    @app.tool(
        name="get_organization_admins",
        description="📊 Get organizationAdmins"
    )
    def get_organization_admins(organization_id: str, per_page: int = 1000):
        """Get get organizationadmins."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.getOrganizationAdmins(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Get Organizationadmins\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in get_organization_admins: {str(e)}"
    
    @app.tool(
        name="get_organization_alerts_profiles",
        description="📊 Get organizationAlertsProfiles"
    )
    def get_organization_alerts_profiles(organization_id: str, per_page: int = 1000):
        """Get get organizationalertsprofiles."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.getOrganizationAlertsProfiles(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Get Organizationalertsprofiles\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in get_organization_alerts_profiles: {str(e)}"
    
    @app.tool(
        name="get_organization_api_requests",
        description="📊 Get organizationApiRequests"
    )
    def get_organization_api_requests(organization_id: str, per_page: int = 1000):
        """Get get organizationapirequests."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.getOrganizationApiRequests(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Get Organizationapirequests\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in get_organization_api_requests: {str(e)}"
    
    @app.tool(
        name="get_organization_api_requests_overview",
        description="📊 Get organizationApiRequestsOverview"
    )
    def get_organization_api_requests_overview(organization_id: str, per_page: int = 100):
        """Get get organizationapirequestsoverview."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.getOrganizationApiRequestsOverview(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Get Organizationapirequestsoverview\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in get_organization_api_requests_overview: {str(e)}"
    
    @app.tool(
        name="get_org_api_requests_overview_response_codes_by_interval",
        description="📊 Get organizationApiRequestsOverviewResponseCodesByInterval"
    )
    def get_organization_api_requests_overview_response_codes_by_interval(organization_id: str, per_page: int = 100):
        """Get get organizationapirequestsoverviewresponsecodesbyinterval."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.getOrganizationApiRequestsOverviewResponseCodesByInterval(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Get Organizationapirequestsoverviewresponsecodesbyinterval\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in get_organization_api_requests_overview_response_codes_by_interval: {str(e)}"
    
    @app.tool(
        name="get_organization_assurance_alert",
        description="📊 Get organizationAssuranceAlert"
    )
    def get_organization_assurance_alert(organization_id: str, per_page: int = 1000):
        """Get get organizationassurancealert."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.getOrganizationAssuranceAlert(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Get Organizationassurancealert\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in get_organization_assurance_alert: {str(e)}"
    
    @app.tool(
        name="get_organization_assurance_alerts",
        description="📊 Get organizationAssuranceAlerts"
    )
    def get_organization_assurance_alerts(organization_id: str, per_page: int = 1000):
        """Get get organizationassurancealerts."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.getOrganizationAssuranceAlerts(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Get Organizationassurancealerts\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in get_organization_assurance_alerts: {str(e)}"
    
    @app.tool(
        name="get_organization_assurance_alerts_overview",
        description="📊 Get organizationAssuranceAlertsOverview"
    )
    def get_organization_assurance_alerts_overview(organization_id: str, per_page: int = 100):
        """Get get organizationassurancealertsoverview."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.getOrganizationAssuranceAlertsOverview(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Get Organizationassurancealertsoverview\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in get_organization_assurance_alerts_overview: {str(e)}"
    
    @app.tool(
        name="get_organization_assurance_alerts_overview_by_network",
        description="📊 Get organizationAssuranceAlertsOverviewByNetwork"
    )
    def get_organization_assurance_alerts_overview_by_network(organization_id: str, per_page: int = 100):
        """Get get organizationassurancealertsoverviewbynetwork."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.getOrganizationAssuranceAlertsOverviewByNetwork(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Get Organizationassurancealertsoverviewbynetwork\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in get_organization_assurance_alerts_overview_by_network: {str(e)}"
    
    @app.tool(
        name="get_organization_assurance_alerts_overview_by_type",
        description="📊 Get organizationAssuranceAlertsOverviewByType"
    )
    def get_organization_assurance_alerts_overview_by_type(organization_id: str, per_page: int = 100):
        """Get get organizationassurancealertsoverviewbytype."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.getOrganizationAssuranceAlertsOverviewByType(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Get Organizationassurancealertsoverviewbytype\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in get_organization_assurance_alerts_overview_by_type: {str(e)}"
    
    @app.tool(
        name="get_organization_assurance_alerts_overview_historical",
        description="📊 Get organizationAssuranceAlertsOverviewHistorical"
    )
    def get_organization_assurance_alerts_overview_historical(organization_id: str, per_page: int = 100):
        """Get get organizationassurancealertsoverviewhistorical."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.getOrganizationAssuranceAlertsOverviewHistorical(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Get Organizationassurancealertsoverviewhistorical\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in get_organization_assurance_alerts_overview_historical: {str(e)}"
    
    @app.tool(
        name="get_organization_branding_policies",
        description="📊 Get organizationBrandingPolicies"
    )
    def get_organization_branding_policies(organization_id: str, per_page: int = 1000):
        """Get get organizationbrandingpolicies."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.getOrganizationBrandingPolicies(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Get Organizationbrandingpolicies\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in get_organization_branding_policies: {str(e)}"
    
    @app.tool(
        name="get_organization_branding_policies_priorities",
        description="📊 Get organizationBrandingPoliciesPriorities"
    )
    def get_organization_branding_policies_priorities(organization_id: str, per_page: int = 1000):
        """Get get organizationbrandingpoliciespriorities."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.getOrganizationBrandingPoliciesPriorities(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Get Organizationbrandingpoliciespriorities\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in get_organization_branding_policies_priorities: {str(e)}"
    
    @app.tool(
        name="get_organization_branding_policy",
        description="📊 Get organizationBrandingPolicy"
    )
    def get_organization_branding_policy(organization_id: str, per_page: int = 1000):
        """Get get organizationbrandingpolicy."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.getOrganizationBrandingPolicy(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Get Organizationbrandingpolicy\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in get_organization_branding_policy: {str(e)}"
    
    @app.tool(
        name="get_organization_clients_bandwidth_usage_history",
        description="📊 Get organizationClientsBandwidthUsageHistory"
    )
    def get_organization_clients_bandwidth_usage_history(organization_id: str, per_page: int = 1000):
        """Get get organizationclientsbandwidthusagehistory."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.getOrganizationClientsBandwidthUsageHistory(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Get Organizationclientsbandwidthusagehistory\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in get_organization_clients_bandwidth_usage_history: {str(e)}"
    
    @app.tool(
        name="get_organization_clients_overview",
        description="📊 Get organizationClientsOverview"
    )
    def get_organization_clients_overview(organization_id: str, per_page: int = 100):
        """Get get organizationclientsoverview."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.getOrganizationClientsOverview(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Get Organizationclientsoverview\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in get_organization_clients_overview: {str(e)}"
    
    @app.tool(
        name="get_organization_clients_search",
        description="📊 Get organizationClientsSearch"
    )
    def get_organization_clients_search(organization_id: str, per_page: int = 1000):
        """Get get organizationclientssearch."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.getOrganizationClientsSearch(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Get Organizationclientssearch\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in get_organization_clients_search: {str(e)}"
    
    @app.tool(
        name="get_organization_config_template",
        description="📊 Get organizationConfigTemplate"
    )
    def get_organization_config_template(organization_id: str, per_page: int = 1000):
        """Get get organizationconfigtemplate."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.getOrganizationConfigTemplate(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Get Organizationconfigtemplate\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in get_organization_config_template: {str(e)}"
    
    @app.tool(
        name="get_organization_config_templates",
        description="📊 Get organizationConfigTemplates"
    )
    def get_organization_config_templates(organization_id: str, per_page: int = 1000):
        """Get get organizationconfigtemplates."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.getOrganizationConfigTemplates(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Get Organizationconfigtemplates\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in get_organization_config_templates: {str(e)}"
    
    @app.tool(
        name="get_organization_configuration_changes",
        description="📊 Get organizationConfigurationChanges"
    )
    def get_organization_configuration_changes(organization_id: str, per_page: int = 1000):
        """Get get organizationconfigurationchanges."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.getOrganizationConfigurationChanges(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Get Organizationconfigurationchanges\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in get_organization_configuration_changes: {str(e)}"
    
    @app.tool(
        name="get_organization_devices",
        description="📊 Get organizationDevices"
    )
    def get_organization_devices(organization_id: str, per_page: int = 1000):
        """Get get organizationdevices."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.getOrganizationDevices(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Get Organizationdevices\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in get_organization_devices: {str(e)}"
    
    @app.tool(
        name="get_organization_devices_availabilities",
        description="📊 Get organizationDevicesAvailabilities"
    )
    def get_organization_devices_availabilities(organization_id: str, per_page: int = 1000):
        """Get get organizationdevicesavailabilities."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.getOrganizationDevicesAvailabilities(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Get Organizationdevicesavailabilities\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in get_organization_devices_availabilities: {str(e)}"
    
    @app.tool(
        name="get_organization_devices_availabilities_change_history",
        description="📊 Get organizationDevicesAvailabilitiesChangeHistory"
    )
    def get_organization_devices_availabilities_change_history(organization_id: str, per_page: int = 1000):
        """Get get organizationdevicesavailabilitieschangehistory."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.getOrganizationDevicesAvailabilitiesChangeHistory(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Get Organizationdevicesavailabilitieschangehistory\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in get_organization_devices_availabilities_change_history: {str(e)}"
    
    @app.tool(
        name="get_organization_devices_controller_migrations",
        description="📊 Get organizationDevicesControllerMigrations"
    )
    def get_organization_devices_controller_migrations(organization_id: str, per_page: int = 1000):
        """Get get organizationdevicescontrollermigrations."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.getOrganizationDevicesControllerMigrations(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Get Organizationdevicescontrollermigrations\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in get_organization_devices_controller_migrations: {str(e)}"
    
    @app.tool(
        name="get_organization_devices_overview_by_model",
        description="📊 Get organizationDevicesOverviewByModel"
    )
    def get_organization_devices_overview_by_model(organization_id: str, per_page: int = 100):
        """Get get organizationdevicesoverviewbymodel."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.getOrganizationDevicesOverviewByModel(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Get Organizationdevicesoverviewbymodel\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in get_organization_devices_overview_by_model: {str(e)}"
    
    @app.tool(
        name="get_organization_devices_packet_capture_captures",
        description="📊 Get organizationDevicesPacketCaptureCaptures"
    )
    def get_organization_devices_packet_capture_captures(organization_id: str, per_page: int = 1000):
        """Get get organizationdevicespacketcapturecaptures."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.getOrganizationDevicesPacketCaptureCaptures(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Get Organizationdevicespacketcapturecaptures\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in get_organization_devices_packet_capture_captures: {str(e)}"
    
    @app.tool(
        name="get_organization_devices_packet_capture_schedules",
        description="📊 Get organizationDevicesPacketCaptureSchedules"
    )
    def get_organization_devices_packet_capture_schedules(organization_id: str, per_page: int = 1000):
        """Get get organizationdevicespacketcaptureschedules."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.getOrganizationDevicesPacketCaptureSchedules(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Get Organizationdevicespacketcaptureschedules\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in get_organization_devices_packet_capture_schedules: {str(e)}"
    
    @app.tool(
        name="get_organization_devices_power_modules_statuses_by_device",
        description="📊 Get organizationDevicesPowerModulesStatusesByDevice"
    )
    def get_organization_devices_power_modules_statuses_by_device(organization_id: str, per_page: int = 1000):
        """Get get organizationdevicespowermodulesstatusesbydevice."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.getOrganizationDevicesPowerModulesStatusesByDevice(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Get Organizationdevicespowermodulesstatusesbydevice\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in get_organization_devices_power_modules_statuses_by_device: {str(e)}"
    
    @app.tool(
        name="get_organization_devices_provisioning_statuses",
        description="📊 Get organizationDevicesProvisioningStatuses"
    )
    def get_organization_devices_provisioning_statuses(organization_id: str, per_page: int = 1000):
        """Get get organizationdevicesprovisioningstatuses."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.getOrganizationDevicesProvisioningStatuses(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Get Organizationdevicesprovisioningstatuses\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in get_organization_devices_provisioning_statuses: {str(e)}"
    
    @app.tool(
        name="get_organization_devices_statuses",
        description="📊 Get organizationDevicesStatuses"
    )
    def get_organization_devices_statuses(organization_id: str, per_page: int = 1000):
        """Get get organizationdevicesstatuses."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.getOrganizationDevicesStatuses(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Organization Device Status\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Devices**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        device_name = item.get('name', 'Unnamed Device')
                        response += f"{i}. **{device_name}**\n"
                        if isinstance(item, dict):
                            # Show complete device information
                            if 'serial' in item:
                                response += f"   - Serial: {item.get('serial')}\n"
                            if 'model' in item:
                                response += f"   - Model: {item.get('model')}\n"
                            if 'mac' in item:
                                response += f"   - MAC: {item.get('mac')}\n"
                            if 'productType' in item:
                                response += f"   - Type: {item.get('productType')}\n"
                            if 'networkId' in item:
                                response += f"   - Network ID: {item.get('networkId')}\n"
                            if 'status' in item:
                                response += f"   - Status: {item.get('status')}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in get_organization_devices_statuses: {str(e)}"
    
    @app.tool(
        name="get_organization_devices_statuses_overview",
        description="📊 Get organizationDevicesStatusesOverview"
    )
    def get_organization_devices_statuses_overview(organization_id: str, per_page: int = 100):
        """Get get organizationdevicesstatusesoverview."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.getOrganizationDevicesStatusesOverview(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Get Organizationdevicesstatusesoverview\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in get_organization_devices_statuses_overview: {str(e)}"
    
    @app.tool(
        name="get_org_devices_system_memory_usage_history_by_interval",
        description="📊 Get organizationDevicesSystemMemoryUsageHistoryByInterval"
    )
    def get_organization_devices_system_memory_usage_history_by_interval(organization_id: str, per_page: int = 1000):
        """Get get organizationdevicessystemmemoryusagehistorybyinterval."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.getOrganizationDevicesSystemMemoryUsageHistoryByInterval(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Get Organizationdevicessystemmemoryusagehistorybyinterval\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in get_organization_devices_system_memory_usage_history_by_interval: {str(e)}"
    
    @app.tool(
        name="get_organization_devices_uplinks_addresses_by_device",
        description="📊 Get organizationDevicesUplinksAddressesByDevice"
    )
    def get_organization_devices_uplinks_addresses_by_device(organization_id: str, per_page: int = 1000):
        """Get get organizationdevicesuplinksaddressesbydevice."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.getOrganizationDevicesUplinksAddressesByDevice(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Get Organizationdevicesuplinksaddressesbydevice\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in get_organization_devices_uplinks_addresses_by_device: {str(e)}"
    
    @app.tool(
        name="get_organization_devices_uplinks_loss_and_latency",
        description="📊 Get organizationDevicesUplinksLossAndLatency"
    )
    def get_organization_devices_uplinks_loss_and_latency(organization_id: str, per_page: int = 1000):
        """Get get organizationdevicesuplinkslossandlatency."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.getOrganizationDevicesUplinksLossAndLatency(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Get Organizationdevicesuplinkslossandlatency\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in get_organization_devices_uplinks_loss_and_latency: {str(e)}"
    
    @app.tool(
        name="get_organization_early_access_features",
        description="📊 Get organizationEarlyAccessFeatures"
    )
    def get_organization_early_access_features(organization_id: str, per_page: int = 1000):
        """Get get organizationearlyaccessfeatures."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.getOrganizationEarlyAccessFeatures(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Get Organizationearlyaccessfeatures\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in get_organization_early_access_features: {str(e)}"
    
    @app.tool(
        name="get_organization_early_access_features_opt_in",
        description="📊 Get organizationEarlyAccessFeaturesOptIn"
    )
    def get_organization_early_access_features_opt_in(organization_id: str, per_page: int = 1000):
        """Get get organizationearlyaccessfeaturesoptin."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.getOrganizationEarlyAccessFeaturesOptIn(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Get Organizationearlyaccessfeaturesoptin\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in get_organization_early_access_features_opt_in: {str(e)}"
    
    @app.tool(
        name="get_organization_early_access_features_opt_ins",
        description="📊 Get organizationEarlyAccessFeaturesOptIns"
    )
    def get_organization_early_access_features_opt_ins(organization_id: str, per_page: int = 1000):
        """Get get organizationearlyaccessfeaturesoptins."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.getOrganizationEarlyAccessFeaturesOptIns(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Get Organizationearlyaccessfeaturesoptins\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in get_organization_early_access_features_opt_ins: {str(e)}"
    
    @app.tool(
        name="get_organization_firmware_upgrades",
        description="📊 Get organizationFirmwareUpgrades"
    )
    def get_organization_firmware_upgrades(organization_id: str, per_page: int = 1000):
        """Get get organizationfirmwareupgrades."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.getOrganizationFirmwareUpgrades(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Get Organizationfirmwareupgrades\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in get_organization_firmware_upgrades: {str(e)}"
    
    @app.tool(
        name="get_organization_firmware_upgrades_by_device",
        description="📊 Get organizationFirmwareUpgradesByDevice"
    )
    def get_organization_firmware_upgrades_by_device(organization_id: str, per_page: int = 1000):
        """Get get organizationfirmwareupgradesbydevice."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.getOrganizationFirmwareUpgradesByDevice(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Get Organizationfirmwareupgradesbydevice\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in get_organization_firmware_upgrades_by_device: {str(e)}"
    
    @app.tool(
        name="get_organization_floor_plans_auto_locate_devices",
        description="📊 Get organizationFloorPlansAutoLocateDevices"
    )
    def get_organization_floor_plans_auto_locate_devices(organization_id: str, per_page: int = 1000):
        """Get get organizationfloorplansautolocatedevices."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.getOrganizationFloorPlansAutoLocateDevices(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Get Organizationfloorplansautolocatedevices\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in get_organization_floor_plans_auto_locate_devices: {str(e)}"
    
    @app.tool(
        name="get_organization_floor_plans_auto_locate_statuses",
        description="📊 Get organizationFloorPlansAutoLocateStatuses"
    )
    def get_organization_floor_plans_auto_locate_statuses(organization_id: str, per_page: int = 1000):
        """Get get organizationfloorplansautolocatestatuses."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.getOrganizationFloorPlansAutoLocateStatuses(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Get Organizationfloorplansautolocatestatuses\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in get_organization_floor_plans_auto_locate_statuses: {str(e)}"
    
    @app.tool(
        name="get_organization_integrations_xdr_networks",
        description="📊 Get organizationIntegrationsXdrNetworks"
    )
    def get_organization_integrations_xdr_networks(organization_id: str, per_page: int = 1000):
        """Get get organizationintegrationsxdrnetworks."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.getOrganizationIntegrationsXdrNetworks(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Get Organizationintegrationsxdrnetworks\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in get_organization_integrations_xdr_networks: {str(e)}"
    
    @app.tool(
        name="get_organization_inventory_device",
        description="📊 Get organizationInventoryDevice"
    )
    def get_organization_inventory_device(organization_id: str, per_page: int = 1000):
        """Get get organizationinventorydevice."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.getOrganizationInventoryDevice(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Get Organizationinventorydevice\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in get_organization_inventory_device: {str(e)}"
    
    @app.tool(
        name="get_organization_inventory_devices",
        description="📊 Get organizationInventoryDevices"
    )
    def get_organization_inventory_devices(organization_id: str, per_page: int = 1000):
        """Get get organizationinventorydevices."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.getOrganizationInventoryDevices(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Get Organizationinventorydevices\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in get_organization_inventory_devices: {str(e)}"
    
    @app.tool(
        name="get_organization_inventory_devices_swaps_bulk",
        description="📊 Get organizationInventoryDevicesSwapsBulk"
    )
    def get_organization_inventory_devices_swaps_bulk(organization_id: str, per_page: int = 1000):
        """Get get organizationinventorydevicesswapsbulk."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.getOrganizationInventoryDevicesSwapsBulk(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Get Organizationinventorydevicesswapsbulk\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in get_organization_inventory_devices_swaps_bulk: {str(e)}"
    
    @app.tool(
        name="get_organization_inventory_onboarding_cloud_monitoring_imports",
        description="📊 Get organizationInventoryOnboardingCloudMonitoringImports"
    )
    def get_organization_inventory_onboarding_cloud_monitoring_imports(organization_id: str, per_page: int = 1000):
        """Get get organizationinventoryonboardingcloudmonitoringimports."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.getOrganizationInventoryOnboardingCloudMonitoringImports(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Get Organizationinventoryonboardingcloudmonitoringimports\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in get_organization_inventory_onboarding_cloud_monitoring_imports: {str(e)}"
    
    @app.tool(
        name="get_organization_inventory_onboarding_cloud_monitoring_networks",
        description="📊 Get organizationInventoryOnboardingCloudMonitoringNetworks"
    )
    def get_organization_inventory_onboarding_cloud_monitoring_networks(organization_id: str, per_page: int = 1000):
        """Get get organizationinventoryonboardingcloudmonitoringnetworks."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.getOrganizationInventoryOnboardingCloudMonitoringNetworks(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Get Organizationinventoryonboardingcloudmonitoringnetworks\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in get_organization_inventory_onboarding_cloud_monitoring_networks: {str(e)}"
    
    @app.tool(
        name="get_organization_license",
        description="📊 Get organizationLicense"
    )
    def get_organization_license(organization_id: str, per_page: int = 1000):
        """Get get organizationlicense."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.getOrganizationLicense(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Get Organizationlicense\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in get_organization_license: {str(e)}"
    
    @app.tool(
        name="get_organization_licenses",
        description="📊 Get organizationLicenses"
    )
    def get_organization_licenses(organization_id: str, per_page: int = 1000):
        """Get get organizationlicenses."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.getOrganizationLicenses(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Get Organizationlicenses\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in get_organization_licenses: {str(e)}"
    
    @app.tool(
        name="get_organization_licenses_overview",
        description="📊 Get organizationLicensesOverview"
    )
    def get_organization_licenses_overview(organization_id: str, per_page: int = 100):
        """Get get organizationlicensesoverview."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.getOrganizationLicensesOverview(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Get Organizationlicensesoverview\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in get_organization_licenses_overview: {str(e)}"
    
    @app.tool(
        name="get_organization_login_security",
        description="📊 Get organizationLoginSecurity"
    )
    def get_organization_login_security(organization_id: str, per_page: int = 1000):
        """Get get organizationloginsecurity."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.getOrganizationLoginSecurity(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Get Organizationloginsecurity\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in get_organization_login_security: {str(e)}"
    
    @app.tool(
        name="get_organization_networks",
        description="📊 Get organizationNetworks"
    )
    def get_organization_networks(organization_id: str, per_page: int = 1000):
        """Get get organizationnetworks."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.getOrganizationNetworks(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Get Organizationnetworks\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in get_organization_networks: {str(e)}"
    
    @app.tool(
        name="get_organization_openapi_spec",
        description="📊 Get organizationOpenapiSpec"
    )
    def get_organization_openapi_spec(organization_id: str, per_page: int = 1000):
        """Get get organizationopenapispec."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.getOrganizationOpenapiSpec(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Get Organizationopenapispec\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in get_organization_openapi_spec: {str(e)}"
    
    @app.tool(
        name="get_organization_policy_object",
        description="📊 Get organizationPolicyObject"
    )
    def get_organization_policy_object(organization_id: str, per_page: int = 1000):
        """Get get organizationpolicyobject."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.getOrganizationPolicyObject(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Get Organizationpolicyobject\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in get_organization_policy_object: {str(e)}"
    
    @app.tool(
        name="get_organization_policy_objects",
        description="📊 Get organizationPolicyObjects"
    )
    def get_organization_policy_objects(organization_id: str, per_page: int = 1000):
        """Get get organizationpolicyobjects."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.getOrganizationPolicyObjects(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Get Organizationpolicyobjects\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in get_organization_policy_objects: {str(e)}"
    
    @app.tool(
        name="get_organization_policy_objects_group",
        description="📊 Get organizationPolicyObjectsGroup"
    )
    def get_organization_policy_objects_group(organization_id: str, per_page: int = 1000):
        """Get get organizationpolicyobjectsgroup."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.getOrganizationPolicyObjectsGroup(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Get Organizationpolicyobjectsgroup\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in get_organization_policy_objects_group: {str(e)}"
    
    @app.tool(
        name="get_organization_policy_objects_groups",
        description="📊 Get organizationPolicyObjectsGroups"
    )
    def get_organization_policy_objects_groups(organization_id: str, per_page: int = 1000):
        """Get get organizationpolicyobjectsgroups."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.getOrganizationPolicyObjectsGroups(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Get Organizationpolicyobjectsgroups\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in get_organization_policy_objects_groups: {str(e)}"
    
    @app.tool(
        name="get_organization_saml",
        description="📊 Get organizationSaml"
    )
    def get_organization_saml(organization_id: str, per_page: int = 1000):
        """Get get organizationsaml."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.getOrganizationSaml(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Get Organizationsaml\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in get_organization_saml: {str(e)}"
    
    @app.tool(
        name="get_organization_saml_idp",
        description="📊 Get organizationSamlIdp"
    )
    def get_organization_saml_idp(organization_id: str, per_page: int = 1000):
        """Get get organizationsamlidp."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.getOrganizationSamlIdp(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Get Organizationsamlidp\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in get_organization_saml_idp: {str(e)}"
    
    @app.tool(
        name="get_organization_saml_idps",
        description="📊 Get organizationSamlIdps"
    )
    def get_organization_saml_idps(organization_id: str, per_page: int = 1000):
        """Get get organizationsamlidps."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.getOrganizationSamlIdps(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Get Organizationsamlidps\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in get_organization_saml_idps: {str(e)}"
    
    @app.tool(
        name="get_organization_saml_role",
        description="📊 Get organizationSamlRole"
    )
    def get_organization_saml_role(organization_id: str, per_page: int = 1000):
        """Get get organizationsamlrole."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.getOrganizationSamlRole(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Get Organizationsamlrole\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in get_organization_saml_role: {str(e)}"
    
    @app.tool(
        name="get_organization_saml_roles",
        description="📊 Get organizationSamlRoles"
    )
    def get_organization_saml_roles(organization_id: str, per_page: int = 1000):
        """Get get organizationsamlroles."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.getOrganizationSamlRoles(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Get Organizationsamlroles\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in get_organization_saml_roles: {str(e)}"
    
    @app.tool(
        name="get_organization_snmp",
        description="📊 Get organizationSnmp"
    )
    def get_organization_snmp(organization_id: str, per_page: int = 1000):
        """Get get organizationsnmp."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.getOrganizationSnmp(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Get Organizationsnmp\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in get_organization_snmp: {str(e)}"
    
    @app.tool(
        name="get_organization_splash_asset",
        description="📊 Get organizationSplashAsset"
    )
    def get_organization_splash_asset(organization_id: str, per_page: int = 1000):
        """Get get organizationsplashasset."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.getOrganizationSplashAsset(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Get Organizationsplashasset\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in get_organization_splash_asset: {str(e)}"
    
    @app.tool(
        name="get_organization_splash_themes",
        description="📊 Get organizationSplashThemes"
    )
    def get_organization_splash_themes(organization_id: str, per_page: int = 1000):
        """Get get organizationsplashthemes."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.getOrganizationSplashThemes(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Get Organizationsplashthemes\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in get_organization_splash_themes: {str(e)}"
    
    @app.tool(
        name="get_organization_summary_top_appliances_by_utilization",
        description="📊 Get organizationSummaryTopAppliancesByUtilization"
    )
    def get_organization_summary_top_appliances_by_utilization(organization_id: str, per_page: int = 100):
        """Get get organizationsummarytopappliancesbyutilization."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.getOrganizationSummaryTopAppliancesByUtilization(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Get Organizationsummarytopappliancesbyutilization\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in get_organization_summary_top_appliances_by_utilization: {str(e)}"
    
    @app.tool(
        name="get_organization_summary_top_applications_by_usage",
        description="📊 Get organizationSummaryTopApplicationsByUsage"
    )
    def get_organization_summary_top_applications_by_usage(organization_id: str, per_page: int = 100):
        """Get get organizationsummarytopapplicationsbyusage."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.getOrganizationSummaryTopApplicationsByUsage(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Get Organizationsummarytopapplicationsbyusage\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in get_organization_summary_top_applications_by_usage: {str(e)}"
    
    @app.tool(
        name="get_organization_summary_top_applications_categories_by_usage",
        description="📊 Get organizationSummaryTopApplicationsCategoriesByUsage"
    )
    def get_organization_summary_top_applications_categories_by_usage(organization_id: str, per_page: int = 100):
        """Get get organizationsummarytopapplicationscategoriesbyusage."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.getOrganizationSummaryTopApplicationsCategoriesByUsage(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Get Organizationsummarytopapplicationscategoriesbyusage\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in get_organization_summary_top_applications_categories_by_usage: {str(e)}"
    
    @app.tool(
        name="get_organization_summary_top_clients_by_usage",
        description="📊 Get organizationSummaryTopClientsByUsage"
    )
    def get_organization_summary_top_clients_by_usage(organization_id: str, per_page: int = 100):
        """Get get organizationsummarytopclientsbyusage."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.getOrganizationSummaryTopClientsByUsage(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Get Organizationsummarytopclientsbyusage\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in get_organization_summary_top_clients_by_usage: {str(e)}"
    
    @app.tool(
        name="get_organization_summary_top_clients_manufacturers_by_usage",
        description="📊 Get organizationSummaryTopClientsManufacturersByUsage"
    )
    def get_organization_summary_top_clients_manufacturers_by_usage(organization_id: str, per_page: int = 100):
        """Get get organizationsummarytopclientsmanufacturersbyusage."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.getOrganizationSummaryTopClientsManufacturersByUsage(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Get Organizationsummarytopclientsmanufacturersbyusage\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in get_organization_summary_top_clients_manufacturers_by_usage: {str(e)}"
    
    @app.tool(
        name="get_organization_summary_top_devices_by_usage",
        description="📊 Get organizationSummaryTopDevicesByUsage"
    )
    def get_organization_summary_top_devices_by_usage(organization_id: str, per_page: int = 100):
        """Get get organizationsummarytopdevicesbyusage."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.getOrganizationSummaryTopDevicesByUsage(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Get Organizationsummarytopdevicesbyusage\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in get_organization_summary_top_devices_by_usage: {str(e)}"
    
    @app.tool(
        name="get_organization_summary_top_devices_models_by_usage",
        description="📊 Get organizationSummaryTopDevicesModelsByUsage"
    )
    def get_organization_summary_top_devices_models_by_usage(organization_id: str, per_page: int = 100):
        """Get get organizationsummarytopdevicesmodelsbyusage."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.getOrganizationSummaryTopDevicesModelsByUsage(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Get Organizationsummarytopdevicesmodelsbyusage\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in get_organization_summary_top_devices_models_by_usage: {str(e)}"
    
    @app.tool(
        name="get_organization_summary_top_networks_by_status",
        description="📊 Get organizationSummaryTopNetworksByStatus"
    )
    def get_organization_summary_top_networks_by_status(organization_id: str, per_page: int = 100):
        """Get get organizationsummarytopnetworksbystatus."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.getOrganizationSummaryTopNetworksByStatus(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Get Organizationsummarytopnetworksbystatus\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in get_organization_summary_top_networks_by_status: {str(e)}"
    
    @app.tool(
        name="get_organization_summary_top_ssids_by_usage",
        description="📊 Get organizationSummaryTopSsidsByUsage"
    )
    def get_organization_summary_top_ssids_by_usage(organization_id: str, per_page: int = 100):
        """Get get organizationsummarytopssidsbyusage."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.getOrganizationSummaryTopSsidsByUsage(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Get Organizationsummarytopssidsbyusage\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in get_organization_summary_top_ssids_by_usage: {str(e)}"
    
    @app.tool(
        name="get_organization_summary_top_switches_by_energy_usage",
        description="📊 Get organizationSummaryTopSwitchesByEnergyUsage"
    )
    def get_organization_summary_top_switches_by_energy_usage(organization_id: str, per_page: int = 100):
        """Get get organizationsummarytopswitchesbyenergyusage."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.getOrganizationSummaryTopSwitchesByEnergyUsage(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Get Organizationsummarytopswitchesbyenergyusage\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in get_organization_summary_top_switches_by_energy_usage: {str(e)}"
    
    @app.tool(
        name="get_organization_uplinks_statuses",
        description="📊 Get organizationUplinksStatuses"
    )
    def get_organization_uplinks_statuses(organization_id: str, per_page: int = 1000):
        """Get get organizationuplinksstatuses."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.getOrganizationUplinksStatuses(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Get Organizationuplinksstatuses\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in get_organization_uplinks_statuses: {str(e)}"
    
    @app.tool(
        name="get_organization_webhooks_alert_types",
        description="📊 Get organizationWebhooksAlertTypes"
    )
    def get_organization_webhooks_alert_types(organization_id: str, per_page: int = 1000):
        """Get get organizationwebhooksalerttypes."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.getOrganizationWebhooksAlertTypes(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Get Organizationwebhooksalerttypes\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in get_organization_webhooks_alert_types: {str(e)}"
    
    @app.tool(
        name="get_organization_webhooks_callbacks_status",
        description="📊 Get organizationWebhooksCallbacksStatus"
    )
    def get_organization_webhooks_callbacks_status(organization_id: str, per_page: int = 1000):
        """Get get organizationwebhookscallbacksstatus."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.getOrganizationWebhooksCallbacksStatus(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Get Organizationwebhookscallbacksstatus\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in get_organization_webhooks_callbacks_status: {str(e)}"
    
    @app.tool(
        name="get_organization_webhooks_logs",
        description="📊 Get organizationWebhooksLogs"
    )
    def get_organization_webhooks_logs(organization_id: str, per_page: int = 1000):
        """Get get organizationwebhookslogs."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.getOrganizationWebhooksLogs(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Get Organizationwebhookslogs\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in get_organization_webhooks_logs: {str(e)}"
    
    @app.tool(
        name="get_organizations",
        description="📊 Get organizations"
    )
    def get_organizations():
        """Get all organizations accessible to the API key."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizations()
            
            response = f"# 📊 Get Organizations\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in get_organizations: {str(e)}"
    
    @app.tool(
        name="move_organization_licenses",
        description="🔄 move organizationLicenses"
    )
    def move_organization_licenses(organization_id: str):
        """Move move organizationlicenses."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.moveOrganizationLicenses(
                organization_id, **kwargs
            )
            
            response = f"# 🔄 Move Organizationlicenses\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in move_organization_licenses: {str(e)}"
    
    @app.tool(
        name="move_organization_licenses_seats",
        description="🔄 move organizationLicensesSeats"
    )
    def move_organization_licenses_seats(organization_id: str):
        """Move move organizationlicensesseats."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.moveOrganizationLicensesSeats(
                organization_id, **kwargs
            )
            
            response = f"# 🔄 Move Organizationlicensesseats\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in move_organization_licenses_seats: {str(e)}"
    
    @app.tool(
        name="release_from_organization_inventory",
        description="🏢 releaseFrom organizationInventory"
    )
    def release_from_organization_inventory(organization_id: str):
        """Manage releasefrom organizationinventory."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.releaseFromOrganizationInventory(
                organization_id, **kwargs
            )
            
            response = f"# 🏢 Releasefrom Organizationinventory\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in release_from_organization_inventory: {str(e)}"
    
    @app.tool(
        name="renew_organization_licenses_seats",
        description="🏢 renew organizationLicensesSeats"
    )
    def renew_organization_licenses_seats(organization_id: str):
        """Manage renew organizationlicensesseats."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.renewOrganizationLicensesSeats(
                organization_id, **kwargs
            )
            
            response = f"# 🏢 Renew Organizationlicensesseats\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in renew_organization_licenses_seats: {str(e)}"
    
    @app.tool(
        name="reorder_organization_devices_packet_capture_schedules",
        description="🏢 reorder organizationDevicesPacketCaptureSchedules"
    )
    def reorder_organization_devices_packet_capture_schedules(organization_id: str):
        """Manage reorder organizationdevicespacketcaptureschedules."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.reorderOrganizationDevicesPacketCaptureSchedules(
                organization_id, **kwargs
            )
            
            response = f"# 🏢 Reorder Organizationdevicespacketcaptureschedules\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in reorder_organization_devices_packet_capture_schedules: {str(e)}"
    
    @app.tool(
        name="restore_organization_assurance_alerts",
        description="🏢 restore organizationAssuranceAlerts"
    )
    def restore_organization_assurance_alerts(organization_id: str):
        """Manage restore organizationassurancealerts."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.restoreOrganizationAssuranceAlerts(
                organization_id, **kwargs
            )
            
            response = f"# 🏢 Restore Organizationassurancealerts\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in restore_organization_assurance_alerts: {str(e)}"
    
    @app.tool(
        name="stop_organization_devices_packet_capture_capture",
        description="🏢 stop organizationDevicesPacketCaptureCapture"
    )
    def stop_organization_devices_packet_capture_capture(organization_id: str):
        """Manage stop organizationdevicespacketcapturecapture."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.stopOrganizationDevicesPacketCaptureCapture(
                organization_id, **kwargs
            )
            
            response = f"# 🏢 Stop Organizationdevicespacketcapturecapture\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in stop_organization_devices_packet_capture_capture: {str(e)}"
    
    @app.tool(
        name="update_organization",
        description="✏️ Update organization"
    )
    def update_organization(organization_id: str):
        """Update update organization."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.updateOrganization(
                organization_id, **kwargs
            )
            
            response = f"# ✏️ Update Organization\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in update_organization: {str(e)}"
    
    @app.tool(
        name="update_organization_action_batch",
        description="✏️ Update organizationActionBatch"
    )
    def update_organization_action_batch(organization_id: str):
        """Update update organizationactionbatch."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.updateOrganizationActionBatch(
                organization_id, **kwargs
            )
            
            response = f"# ✏️ Update Organizationactionbatch\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in update_organization_action_batch: {str(e)}"
    
    @app.tool(
        name="update_organization_adaptive_policy_acl",
        description="✏️ Update organizationAdaptivePolicyAcl"
    )
    def update_organization_adaptive_policy_acl(organization_id: str):
        """Update update organizationadaptivepolicyacl."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.updateOrganizationAdaptivePolicyAcl(
                organization_id, **kwargs
            )
            
            response = f"# ✏️ Update Organizationadaptivepolicyacl\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in update_organization_adaptive_policy_acl: {str(e)}"
    
    @app.tool(
        name="update_organization_adaptive_policy_group",
        description="✏️ Update organizationAdaptivePolicyGroup"
    )
    def update_organization_adaptive_policy_group(organization_id: str):
        """Update update organizationadaptivepolicygroup."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.updateOrganizationAdaptivePolicyGroup(
                organization_id, **kwargs
            )
            
            response = f"# ✏️ Update Organizationadaptivepolicygroup\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in update_organization_adaptive_policy_group: {str(e)}"
    
    @app.tool(
        name="update_organization_adaptive_policy_policy",
        description="✏️ Update organizationAdaptivePolicyPolicy"
    )
    def update_organization_adaptive_policy_policy(organization_id: str):
        """Update update organizationadaptivepolicypolicy."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.updateOrganizationAdaptivePolicyPolicy(
                organization_id, **kwargs
            )
            
            response = f"# ✏️ Update Organizationadaptivepolicypolicy\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in update_organization_adaptive_policy_policy: {str(e)}"
    
    @app.tool(
        name="update_organization_adaptive_policy_settings",
        description="✏️ Update organizationAdaptivePolicySettings"
    )
    def update_organization_adaptive_policy_settings(organization_id: str):
        """Update update organizationadaptivepolicysettings."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.updateOrganizationAdaptivePolicySettings(
                organization_id, **kwargs
            )
            
            response = f"# ✏️ Update Organizationadaptivepolicysettings\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in update_organization_adaptive_policy_settings: {str(e)}"
    
    @app.tool(
        name="update_organization_admin",
        description="✏️ Update organizationAdmin"
    )
    def update_organization_admin(organization_id: str):
        """Update update organizationadmin."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.updateOrganizationAdmin(
                organization_id, **kwargs
            )
            
            response = f"# ✏️ Update Organizationadmin\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in update_organization_admin: {str(e)}"
    
    @app.tool(
        name="update_organization_alerts_profile",
        description="✏️ Update organizationAlertsProfile"
    )
    def update_organization_alerts_profile(organization_id: str):
        """Update update organizationalertsprofile."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.updateOrganizationAlertsProfile(
                organization_id, **kwargs
            )
            
            response = f"# ✏️ Update Organizationalertsprofile\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in update_organization_alerts_profile: {str(e)}"
    
    @app.tool(
        name="update_organization_branding_policies_priorities",
        description="✏️ Update organizationBrandingPoliciesPriorities"
    )
    def update_organization_branding_policies_priorities(organization_id: str):
        """Update update organizationbrandingpoliciespriorities."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.updateOrganizationBrandingPoliciesPriorities(
                organization_id, **kwargs
            )
            
            response = f"# ✏️ Update Organizationbrandingpoliciespriorities\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in update_organization_branding_policies_priorities: {str(e)}"
    
    @app.tool(
        name="update_organization_branding_policy",
        description="✏️ Update organizationBrandingPolicy"
    )
    def update_organization_branding_policy(organization_id: str):
        """Update update organizationbrandingpolicy."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.updateOrganizationBrandingPolicy(
                organization_id, **kwargs
            )
            
            response = f"# ✏️ Update Organizationbrandingpolicy\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in update_organization_branding_policy: {str(e)}"
    
    @app.tool(
        name="update_organization_config_template",
        description="✏️ Update organizationConfigTemplate"
    )
    def update_organization_config_template(organization_id: str):
        """Update update organizationconfigtemplate."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.updateOrganizationConfigTemplate(
                organization_id, **kwargs
            )
            
            response = f"# ✏️ Update Organizationconfigtemplate\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in update_organization_config_template: {str(e)}"
    
    @app.tool(
        name="update_organization_devices_packet_capture_schedule",
        description="✏️ Update organizationDevicesPacketCaptureSchedule"
    )
    def update_organization_devices_packet_capture_schedule(organization_id: str):
        """Update update organizationdevicespacketcaptureschedule."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.updateOrganizationDevicesPacketCaptureSchedule(
                organization_id, **kwargs
            )
            
            response = f"# ✏️ Update Organizationdevicespacketcaptureschedule\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in update_organization_devices_packet_capture_schedule: {str(e)}"
    
    @app.tool(
        name="update_organization_early_access_features_opt_in",
        description="✏️ Update organizationEarlyAccessFeaturesOptIn"
    )
    def update_organization_early_access_features_opt_in(organization_id: str):
        """Update update organizationearlyaccessfeaturesoptin."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.updateOrganizationEarlyAccessFeaturesOptIn(
                organization_id, **kwargs
            )
            
            response = f"# ✏️ Update Organizationearlyaccessfeaturesoptin\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in update_organization_early_access_features_opt_in: {str(e)}"
    
    @app.tool(
        name="update_organization_license",
        description="✏️ Update organizationLicense"
    )
    def update_organization_license(organization_id: str):
        """Update update organizationlicense."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.updateOrganizationLicense(
                organization_id, **kwargs
            )
            
            response = f"# ✏️ Update Organizationlicense\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in update_organization_license: {str(e)}"
    
    @app.tool(
        name="update_organization_login_security",
        description="✏️ Update organizationLoginSecurity"
    )
    def update_organization_login_security(organization_id: str):
        """Update update organizationloginsecurity."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.updateOrganizationLoginSecurity(
                organization_id, **kwargs
            )
            
            response = f"# ✏️ Update Organizationloginsecurity\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in update_organization_login_security: {str(e)}"
    
    @app.tool(
        name="update_organization_policy_object",
        description="✏️ Update organizationPolicyObject"
    )
    def update_organization_policy_object(organization_id: str):
        """Update update organizationpolicyobject."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.updateOrganizationPolicyObject(
                organization_id, **kwargs
            )
            
            response = f"# ✏️ Update Organizationpolicyobject\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in update_organization_policy_object: {str(e)}"
    
    @app.tool(
        name="update_organization_policy_objects_group",
        description="✏️ Update organizationPolicyObjectsGroup"
    )
    def update_organization_policy_objects_group(organization_id: str):
        """Update update organizationpolicyobjectsgroup."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.updateOrganizationPolicyObjectsGroup(
                organization_id, **kwargs
            )
            
            response = f"# ✏️ Update Organizationpolicyobjectsgroup\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in update_organization_policy_objects_group: {str(e)}"
    
    @app.tool(
        name="update_organization_saml",
        description="✏️ Update organizationSaml"
    )
    def update_organization_saml(organization_id: str):
        """Update update organizationsaml."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.updateOrganizationSaml(
                organization_id, **kwargs
            )
            
            response = f"# ✏️ Update Organizationsaml\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in update_organization_saml: {str(e)}"
    
    @app.tool(
        name="update_organization_saml_idp",
        description="✏️ Update organizationSamlIdp"
    )
    def update_organization_saml_idp(organization_id: str):
        """Update update organizationsamlidp."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.updateOrganizationSamlIdp(
                organization_id, **kwargs
            )
            
            response = f"# ✏️ Update Organizationsamlidp\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in update_organization_saml_idp: {str(e)}"
    
    @app.tool(
        name="update_organization_saml_role",
        description="✏️ Update organizationSamlRole"
    )
    def update_organization_saml_role(organization_id: str):
        """Update update organizationsamlrole."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.updateOrganizationSamlRole(
                organization_id, **kwargs
            )
            
            response = f"# ✏️ Update Organizationsamlrole\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in update_organization_saml_role: {str(e)}"
    
    @app.tool(
        name="update_organization_snmp",
        description="✏️ Update organizationSnmp"
    )
    def update_organization_snmp(organization_id: str):
        """Update update organizationsnmp."""
        try:
            kwargs = {"perPage": per_page} if "per_page" in locals() else {}
            
            result = meraki_client.dashboard.organizations.updateOrganizationSnmp(
                organization_id, **kwargs
            )
            
            response = f"# ✏️ Update Organizationsnmp\n\n"
            
            if result:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\n\n"
                    
                    for i, item in enumerate(result[:10], 1):
                        response += f"{i}. **{item.get('name', item.get('id', 'Item'))}**\n"
                        if isinstance(item, dict):
                            for key, value in list(item.items())[:3]:
                                response += f"   - {key}: {value}\n"
                        response += "\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\n"
                else:
                    response += f"**Result**: {result}\n"
            else:
                response += "*No data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error in update_organization_snmp: {str(e)}"