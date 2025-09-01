"""
Licensing management tools for Cisco Meraki MCP server.

This module provides tools for managing organization licenses and seats.
"""

from typing import Optional, Dict, Any, List
from datetime import datetime
import json

# Global references to be set by register function
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
    
    # ==================== LICENSE MANAGEMENT ====================
    
    @app.tool(
        name="get_org_licenses",
        description="📜 List all licenses in an organization"
    )
    def get_org_licenses(
        organization_id: str,
        per_page: int = 100,
        starting_after: Optional[str] = None,
        ending_before: Optional[str] = None,
        device_serial: Optional[str] = None,
        network_id: Optional[str] = None,
        state: Optional[str] = None
    ):
        """Get organization licenses."""
        try:
            kwargs = {"perPage": per_page}
            
            if starting_after:
                kwargs["startingAfter"] = starting_after
            if ending_before:
                kwargs["endingBefore"] = ending_before
            if device_serial:
                kwargs["deviceSerial"] = device_serial
            if network_id:
                kwargs["networkId"] = network_id
            if state:
                kwargs["state"] = state
            
            result = meraki_client.dashboard.organizations.getOrganizationLicenses(
                organization_id, **kwargs
            )
            
            response = f"# 📜 Organization Licenses\n\n"
            
            if result and isinstance(result, list):
                response += f"**Total Licenses**: {len(result)}\n\n"
                
                # Group by state
                by_state = {}
                for license in result:
                    state = license.get('state', 'Unknown')
                    if state not in by_state:
                        by_state[state] = []
                    by_state[state].append(license)
                
                for state, licenses in by_state.items():
                    icon = "✅" if state == "active" else "⏳" if state == "unused" else "❌"
                    response += f"## {icon} {state.title()} ({len(licenses)})\n"
                    
                    for lic in licenses[:5]:
                        response += f"- **{lic.get('licenseType', 'Unknown')}**\n"
                        response += f"  - ID: {lic.get('id', 'N/A')}\n"
                        
                        if lic.get('deviceSerial'):
                            response += f"  - Device: {lic['deviceSerial']}\n"
                        
                        if lic.get('expirationDate'):
                            response += f"  - Expires: {lic['expirationDate']}\n"
                        
                        if lic.get('seatCount'):
                            response += f"  - Seats: {lic['seatCount']}\n"
                    
                    if len(licenses) > 5:
                        response += f"\n  ... and {len(licenses)-5} more\n"
                    response += "\n"
            else:
                response += "*No licenses found*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting licenses: {str(e)}"
    
    @app.tool(
        name="get_org_license",
        description="📜 Get details of a specific license"
    )
    def get_org_license(
        organization_id: str,
        license_id: str
    ):
        """Get specific license details."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationLicense(
                organization_id, license_id
            )
            
            response = f"# 📜 License Details\n\n"
            
            if result:
                response += f"**License Type**: {result.get('licenseType', 'Unknown')}\n"
                response += f"**ID**: {result.get('id', 'N/A')}\n"
                response += f"**State**: {result.get('state', 'N/A')}\n\n"
                
                # Assignment
                if result.get('deviceSerial'):
                    response += f"## Assignment\n"
                    response += f"- **Device Serial**: {result['deviceSerial']}\n"
                    if result.get('networkId'):
                        response += f"- **Network ID**: {result['networkId']}\n"
                else:
                    response += "**Status**: Unassigned\n"
                
                # Duration
                if result.get('activationDate'):
                    response += f"\n## Duration\n"
                    response += f"- **Activated**: {result['activationDate']}\n"
                if result.get('expirationDate'):
                    response += f"- **Expires**: {result['expirationDate']}\n"
                
                # Seats
                if result.get('seatCount'):
                    response += f"\n## Capacity\n"
                    response += f"- **Total Seats**: {result['seatCount']}\n"
                    if result.get('totalDurationInDays'):
                        response += f"- **Duration**: {result['totalDurationInDays']} days\n"
            else:
                response += "*License not found*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting license: {str(e)}"
    
    @app.tool(
        name="update_org_license",
        description="📜✏️ Update a license (reassign device)"
    )
    def update_org_license(
        organization_id: str,
        license_id: str,
        device_serial: Optional[str] = None
    ):
        """
        Update a license.
        
        Args:
            organization_id: Organization ID
            license_id: License ID
            device_serial: Device serial to assign license to
        """
        try:
            kwargs = {}
            
            if device_serial:
                kwargs['deviceSerial'] = device_serial
            
            result = meraki_client.dashboard.organizations.updateOrganizationLicense(
                organization_id, license_id, **kwargs
            )
            
            response = f"# ✅ Updated License\n\n"
            response += f"**License ID**: {license_id}\n"
            if device_serial:
                response += f"**Assigned to**: {device_serial}\n"
            
            return response
        except Exception as e:
            return f"❌ Error updating license: {str(e)}"
    
    @app.tool(
        name="get_org_licenses_overview",
        description="📊 Get overview of organization licenses"
    )
    def get_org_licenses_overview(
        organization_id: str
    ):
        """Get licenses overview."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationLicensesOverview(
                organization_id
            )
            
            response = f"# 📊 Licenses Overview\n\n"
            
            if result:
                # Status counts
                status = result.get('status', {})
                if status:
                    response += "## License Status\n"
                    response += f"- ✅ **Active**: {status.get('active', 0)}\n"
                    response += f"- ⏳ **Unused**: {status.get('unused', 0)}\n"
                    response += f"- ⚠️ **Expiring Soon**: {status.get('expiringSoon', 0)}\n"
                    response += f"- ❌ **Expired**: {status.get('expired', 0)}\n"
                    response += f"- **Total**: {status.get('total', 0)}\n\n"
                
                # Expiration summary
                expiration = result.get('expirationDate', {})
                if expiration:
                    response += "## Expiration Summary\n"
                    response += f"- **Earliest**: {expiration.get('earliest', 'N/A')}\n"
                    response += f"- **Latest**: {expiration.get('latest', 'N/A')}\n\n"
                
                # License types
                types = result.get('licenseTypes', [])
                if types:
                    response += "## License Types\n"
                    for lic_type in types:
                        response += f"- **{lic_type.get('licenseType', 'Unknown')}**: {lic_type.get('count', 0)}\n"
            else:
                response += "*No overview data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting overview: {str(e)}"
    
    @app.tool(
        name="assign_org_licenses_seats",
        description="📜➕ Assign license seats to a network"
    )
    def assign_org_licenses_seats(
        organization_id: str,
        license_id: str,
        network_id: str,
        seat_count: int
    ):
        """
        Assign license seats.
        
        Args:
            organization_id: Organization ID
            license_id: License ID
            network_id: Network ID to assign seats to
            seat_count: Number of seats to assign
        """
        try:
            result = meraki_client.dashboard.organizations.assignOrganizationLicensesSeats(
                organization_id,
                licenseId=license_id,
                networkId=network_id,
                seatCount=seat_count
            )
            
            response = f"# ✅ Assigned License Seats\n\n"
            response += f"**License ID**: {license_id}\n"
            response += f"**Network ID**: {network_id}\n"
            response += f"**Seats Assigned**: {seat_count}\n"
            
            if result:
                response += f"\n**Remaining Seats**: {result.get('remainingSeats', 'N/A')}\n"
            
            return response
        except Exception as e:
            return f"❌ Error assigning seats: {str(e)}"
    
    @app.tool(
        name="move_org_licenses",
        description="📜➡️ Move licenses between organizations"
    )
    def move_org_licenses(
        organization_id: str,
        dest_organization_id: str,
        license_ids: str
    ):
        """
        Move licenses to another organization.
        
        Args:
            organization_id: Source organization ID
            dest_organization_id: Destination organization ID
            license_ids: Comma-separated license IDs to move
        """
        try:
            license_list = [l.strip() for l in license_ids.split(',')]
            
            result = meraki_client.dashboard.organizations.moveOrganizationLicenses(
                organization_id,
                destOrganizationId=dest_organization_id,
                licenseIds=license_list
            )
            
            response = f"# ✅ Moved Licenses\n\n"
            response += f"**From**: {organization_id}\n"
            response += f"**To**: {dest_organization_id}\n"
            response += f"**Licenses**: {license_ids}\n"
            
            if result:
                response += f"\n**Remaining Licenses**: {result.get('remainingLicenses', 'N/A')}\n"
            
            return response
        except Exception as e:
            return f"❌ Error moving licenses: {str(e)}"
    
    @app.tool(
        name="move_org_licenses_seats",
        description="📜➡️ Move license seats between networks"
    )
    def move_org_licenses_seats(
        organization_id: str,
        dest_organization_id: str,
        license_id: str,
        seat_count: int
    ):
        """
        Move license seats to another organization.
        
        Args:
            organization_id: Source organization ID
            dest_organization_id: Destination organization ID
            license_id: License ID
            seat_count: Number of seats to move
        """
        try:
            result = meraki_client.dashboard.organizations.moveOrganizationLicensesSeats(
                organization_id,
                destOrganizationId=dest_organization_id,
                licenseId=license_id,
                seatCount=seat_count
            )
            
            response = f"# ✅ Moved License Seats\n\n"
            response += f"**From**: {organization_id}\n"
            response += f"**To**: {dest_organization_id}\n"
            response += f"**License**: {license_id}\n"
            response += f"**Seats Moved**: {seat_count}\n"
            
            if result:
                response += f"\n**Remaining Seats**: {result.get('remainingSeats', 'N/A')}\n"
            
            return response
        except Exception as e:
            return f"❌ Error moving seats: {str(e)}"
    
    @app.tool(
        name="renew_org_licenses_seats",
        description="📜🔄 Renew expiring license seats"
    )
    def renew_org_licenses_seats(
        organization_id: str,
        license_id_to_renew: str,
        unused_license_id: str
    ):
        """
        Renew expiring license seats.
        
        Args:
            organization_id: Organization ID
            license_id_to_renew: License ID that needs renewal
            unused_license_id: Unused license ID to use for renewal
        """
        try:
            result = meraki_client.dashboard.organizations.renewOrganizationLicensesSeats(
                organization_id,
                licenseIdToRenew=license_id_to_renew,
                unusedLicenseId=unused_license_id
            )
            
            response = f"# ✅ Renewed License Seats\n\n"
            response += f"**Renewed License**: {license_id_to_renew}\n"
            response += f"**Using License**: {unused_license_id}\n"
            
            if result:
                response += f"\n**New Expiration**: {result.get('expirationDate', 'N/A')}\n"
            
            return response
        except Exception as e:
            return f"❌ Error renewing seats: {str(e)}"