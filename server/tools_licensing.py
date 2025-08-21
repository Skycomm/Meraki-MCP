"""
Licensing tools for the Cisco Meraki MCP Server - ONLY REAL API METHODS.
"""

# Global variables to store app and meraki client
app = None
meraki_client = None

def register_licensing_tools(mcp_app, meraki):
    """
    Register licensing tools with the MCP server.
    
    Args:
        mcp_app: MCP server instance
        meraki: Meraki client instance
    """
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    
    # Register all licensing tools
    register_licensing_tool_handlers()

def register_licensing_tool_handlers():
    """Register all licensing tool handlers using ONLY REAL API methods."""
    
    @app.tool(
        name="get_organization_licensing_overview",
        description="📊 Get comprehensive licensing overview for an organization"
    )
    def get_organization_licensing_overview(org_id: str):
        """
        Get a comprehensive overview of organization licensing.
        Supports both co-termination and per-device licensing models.
        
        Args:
            org_id: Organization ID
            
        Returns:
            Comprehensive licensing overview
        """
        try:
            # First check what type of licensing model
            try:
                # Try to get the licensing coterm overview
                coterm = meraki_client.dashboard.organizations.getOrganizationLicensingCotermLicenses(org_id)
                
                # This is a co-termination org
                result = f"# 📊 Organization Licensing Overview\n\n"
                result += f"**Organization ID**: {org_id}\n"
                result += f"**Licensing Model**: Co-Termination\n\n"
                
                # Show co-term licenses
                result += "## 📅 Co-Termination Licenses\n\n"
                
                for license in coterm:
                    editions = license.get('editions', [])
                    for edition in editions:
                        result += f"### {edition.get('edition', 'Unknown Edition')}\n"
                        result += f"- **Product Type**: {edition.get('productType', 'N/A')}\n"
                        result += f"- **License Count**: {edition.get('licenseCount', 0)}\n"
                        
                    counts = license.get('counts', [])
                    for count in counts:
                        model = count.get('model', 'Unknown')
                        count_val = count.get('count', 0)
                        if count_val > 0:
                            result += f"- **{model}**: {count_val} devices\n"
                    
                    result += f"\n**Expiration Date**: {license.get('expirationDate', 'N/A')}\n"
                    
                    # Calculate days remaining
                    exp_date = license.get('expirationDate')
                    if exp_date:
                        from datetime import datetime
                        try:
                            exp_dt = datetime.fromisoformat(exp_date.replace('Z', '+00:00'))
                            days_left = (exp_dt - datetime.now(exp_dt.tzinfo)).days
                            if days_left < 30:
                                result += f"⚠️ **Days Remaining**: {days_left} days\n"
                            else:
                                result += f"✅ **Days Remaining**: {days_left} days\n"
                        except:
                            pass
                    
                    result += "\n"
                
            except Exception as e:
                if "404" in str(e) or "does not support" in str(e):
                    # Try per-device licensing
                    licenses = meraki_client.dashboard.organizations.getOrganizationLicenses(org_id)
                    
                    result = f"# 📊 Organization Licensing Overview\n\n"
                    result += f"**Organization ID**: {org_id}\n"
                    result += f"**Licensing Model**: Per-Device\n"
                    result += f"**Total Licenses**: {len(licenses)}\n\n"
                    
                    # Count by state
                    states = {}
                    device_types = {}
                    
                    for license in licenses:
                        state = license.get('state', 'unknown')
                        states[state] = states.get(state, 0) + 1
                        
                        device_type = license.get('deviceType', 'Unknown')
                        if device_type not in device_types:
                            device_types[device_type] = {'active': 0, 'expired': 0, 'unused': 0}
                        device_types[device_type][state] = device_types[device_type].get(state, 0) + 1
                    
                    # Overall summary
                    result += "## 📈 License Status Summary\n"
                    result += f"- ✅ **Active**: {states.get('active', 0)}\n"
                    result += f"- 📦 **Unused**: {states.get('unused', 0)}\n"
                    result += f"- ⏰ **Expired**: {states.get('expired', 0)}\n\n"
                    
                    # By device type
                    result += "## 📱 Licenses by Device Type\n"
                    for device_type, counts in device_types.items():
                        total = sum(counts.values())
                        result += f"\n### {device_type} ({total} licenses)\n"
                        result += f"- Active: {counts['active']}\n"
                        result += f"- Unused: {counts['unused']}\n"
                        result += f"- Expired: {counts['expired']}\n"
                else:
                    raise e
                    
            # Get organization info for more context
            try:
                org_info = meraki_client.dashboard.organizations.getOrganization(org_id)
                result += f"\n## 🏢 Organization Details\n"
                result += f"- **Name**: {org_info.get('name', 'N/A')}\n"
                
                # Check if licensing info is in org details
                licensing = org_info.get('licensing', {})
                if licensing:
                    result += f"- **Licensing Model**: {licensing.get('model', 'N/A')}\n"
            except:
                pass
                
            result += "\n## 💡 Licensing Tips\n"
            result += "- Renew licenses before expiration to avoid service interruption\n"
            result += "- Unused licenses can be assigned to new devices\n"
            result += "- Contact your Meraki sales rep for bulk renewals\n"
            
            return result
            
        except Exception as e:
            return f"Error getting licensing overview: {str(e)}"
    
    @app.tool(
        name="get_organization_licenses",
        description="📄 List all licenses in an organization"
    )
    def get_organization_licenses(org_id: str):
        """
        List all licenses for an organization.
        
        Args:
            org_id: Organization ID
            
        Returns:
            List of licenses with details
        """
        try:
            licenses = meraki_client.get_organization_licenses(org_id)
            
            if not licenses:
                return f"No licenses found for organization {org_id}."
                
            result = f"# 📄 Organization Licenses - Org {org_id}\n\n"
            result += f"**Total Licenses**: {len(licenses)}\n\n"
            
            # Group by device type
            device_types = {}
            for license in licenses:
                device_type = license.get('deviceType', 'Unknown')
                if device_type not in device_types:
                    device_types[device_type] = []
                device_types[device_type].append(license)
            
            # Display by device type
            for device_type, type_licenses in device_types.items():
                result += f"## {device_type} Licenses ({len(type_licenses)})\n"
                
                # Count active vs expired
                active = sum(1 for lic in type_licenses if lic.get('state') == 'active')
                expired = sum(1 for lic in type_licenses if lic.get('state') == 'expired')
                unused = sum(1 for lic in type_licenses if lic.get('state') == 'unused')
                
                result += f"- **Active**: {active}\n"
                result += f"- **Expired**: {expired}\n"
                result += f"- **Unused**: {unused}\n\n"
                
                # Show details for first few
                for license in type_licenses[:5]:
                    lic_key = license.get('licenseKey', 'Unknown')
                    state = license.get('state', 'unknown')
                    state_icon = "✅" if state == 'active' else "⏰" if state == 'expired' else "📦"
                    
                    result += f"### {state_icon} License {lic_key[-8:]}\n"
                    result += f"- **State**: {state}\n"
                    result += f"- **Order Number**: {license.get('orderNumber', 'N/A')}\n"
                    
                    # Expiration info
                    expiration = license.get('expirationDate')
                    if expiration:
                        result += f"- **Expires**: {expiration}\n"
                    
                    # Device assignment
                    device_serial = license.get('deviceSerial')
                    if device_serial:
                        result += f"- **Assigned to**: {device_serial}\n"
                    
                    # Duration
                    duration = license.get('durationInDays')
                    if duration:
                        result += f"- **Duration**: {duration} days\n"
                    
                    result += "\n"
                
                if len(type_licenses) > 5:
                    result += f"... and {len(type_licenses) - 5} more {device_type} licenses\n\n"
                    
            return result
            
        except Exception as e:
            return f"Error retrieving licenses: {str(e)}"
    
    @app.tool(
        name="get_organization_licensing_coterm",
        description="📊 Get co-termination licensing info for organization"
    )
    def get_organization_licensing_coterm(org_id: str):
        """
        Get co-termination licensing model information.
        
        Args:
            org_id: Organization ID
            
        Returns:
            Co-term licensing details
        """
        try:
            coterm = meraki_client.get_organization_licensing_coterm_licenses(org_id)
            
            result = f"# 📊 Co-Termination Licensing - Org {org_id}\n\n"
            
            # Check if expired
            expired = coterm.get('expired', False)
            if expired:
                result += "⚠️ **WARNING: Co-term licenses are expired!**\n\n"
            
            # Overall counts
            counts = coterm.get('counts', [])
            if counts:
                result += "## License Counts by Model\n"
                total_count = 0
                for count in counts:
                    model = count.get('model', 'Unknown')
                    qty = count.get('count', 0)
                    total_count += qty
                    result += f"- **{model}**: {qty} licenses\n"
                result += f"\n**Total Devices**: {total_count}\n\n"
            
            # Expiration dates
            expiration_date = coterm.get('expirationDate')
            if expiration_date:
                result += f"## Expiration\n"
                result += f"**All licenses expire on**: {expiration_date}\n\n"
            
            # Invalid devices
            invalid = coterm.get('invalidSerials', [])
            if invalid:
                result += f"## ⚠️ Invalid Devices ({len(invalid)})\n"
                result += "These devices have invalid licenses:\n"
                for serial in invalid[:10]:
                    result += f"- {serial}\n"
                if len(invalid) > 10:
                    result += f"... and {len(invalid) - 10} more\n"
                result += "\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving co-term licensing info: {str(e)}"
    
    @app.tool(
        name="claim_organization_license",
        description="🔑 Claim a license key for an organization"
    )
    def claim_organization_license(org_id: str, license_key: str):
        """
        Claim a new license key for an organization.
        
        Args:
            org_id: Organization ID
            license_key: License key to claim
            
        Returns:
            Claim result
        """
        try:
            result = meraki_client.claim_organization_license(org_id, licenseKey=license_key)
            
            response = f"# 🔑 License Claimed Successfully\n\n"
            response += f"**License Key**: {license_key}\n"
            response += f"**Organization**: {org_id}\n\n"
            
            # Display claimed license info if returned
            if isinstance(result, dict):
                if result.get('licenseKey'):
                    response += f"## License Details\n"
                    response += f"- **Type**: {result.get('deviceType', 'Unknown')}\n"
                    response += f"- **State**: {result.get('state', 'Unknown')}\n"
                    response += f"- **Duration**: {result.get('durationInDays', 'N/A')} days\n"
                    
                    expiration = result.get('expirationDate')
                    if expiration:
                        response += f"- **Expires**: {expiration}\n"
            
            return response
            
        except Exception as e:
            return f"Error claiming license: {str(e)}"
    
    @app.tool(
        name="update_organization_license",
        description="📝 Update license assignment (assign to device)"
    )
    def update_organization_license(org_id: str, license_id: str, device_serial: str = None):
        """
        Update a license (typically to assign/unassign to a device).
        
        Args:
            org_id: Organization ID
            license_id: License ID to update
            device_serial: Device serial to assign to (or empty to unassign)
            
        Returns:
            Update result
        """
        try:
            kwargs = {}
            if device_serial:
                kwargs['deviceSerial'] = device_serial
            else:
                # Unassign by setting to empty string
                kwargs['deviceSerial'] = ""
                
            result = meraki_client.update_organization_license(org_id, license_id, **kwargs)
            
            response = f"# 📝 License Updated\n\n"
            response += f"**License ID**: {license_id}\n"
            
            if device_serial:
                response += f"**Assigned to**: {device_serial}\n"
            else:
                response += "**Status**: Unassigned from device\n"
                
            return response
            
        except Exception as e:
            return f"Error updating license: {str(e)}"
    
    @app.tool(
        name="move_organization_licenses",
        description="🔄 Move licenses between organizations"
    )
    def move_organization_licenses(source_org_id: str, dest_org_id: str, license_ids: str):
        """
        Move licenses from one organization to another.
        
        Args:
            source_org_id: Source organization ID
            dest_org_id: Destination organization ID
            license_ids: Comma-separated license IDs to move
            
        Returns:
            Move result
        """
        try:
            ids_list = [id.strip() for id in license_ids.split(',')]
            
            result = meraki_client.move_organization_licenses(
                source_org_id,
                destOrganizationId=dest_org_id,
                licenseIds=ids_list
            )
            
            response = f"# 🔄 Licenses Moved\n\n"
            response += f"**From Organization**: {source_org_id}\n"
            response += f"**To Organization**: {dest_org_id}\n"
            response += f"**Number of Licenses**: {len(ids_list)}\n\n"
            
            response += "✅ Licenses successfully transferred to the destination organization.\n"
            
            return response
            
        except Exception as e:
            return f"Error moving licenses: {str(e)}"
    
    @app.tool(
        name="renew_organization_licenses_seats",
        description="🔄 Renew SM seats for an organization"
    )
    def renew_organization_licenses_seats(org_id: str, license_id_to_renew: str, unused_license_id: str):
        """
        Renew Systems Manager seats by combining licenses.
        
        Args:
            org_id: Organization ID
            license_id_to_renew: License ID that needs renewal
            unused_license_id: Unused license ID to apply for renewal
            
        Returns:
            Renewal result
        """
        try:
            result = meraki_client.renew_organization_licenses_seats(
                org_id,
                licenseIdToRenew=license_id_to_renew,
                unusedLicenseId=unused_license_id
            )
            
            response = f"# 🔄 SM Seats Renewed\n\n"
            response += f"**Renewed License**: {license_id_to_renew}\n"
            response += f"**Using License**: {unused_license_id}\n\n"
            
            if isinstance(result, dict):
                response += f"## Result\n"
                response += f"- **New Expiration**: {result.get('expirationDate', 'N/A')}\n"
                response += f"- **Seat Count**: {result.get('seatCount', 'N/A')}\n"
            
            return response
            
        except Exception as e:
            return f"Error renewing SM seats: {str(e)}"