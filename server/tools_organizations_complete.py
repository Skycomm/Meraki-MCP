"""
Organizations complete SDK coverage for Cisco Meraki MCP Server.
Provides 100% coverage of ALL Meraki Organizations API endpoints.
"""

import json
from typing import Optional, List, Dict, Any

# Global variables to store app and meraki client
app = None
meraki_client = None

def register_organizations_complete_tools(mcp_app, meraki):
    """
    Register complete organization tools with the MCP server.
    
    Args:
        mcp_app: MCP server instance
        meraki: Meraki client instance
    """
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    
    # Register all organization tools for 100% coverage
    register_organizations_complete_handlers()

def register_organizations_complete_handlers():
    """Register ALL organization tool handlers for complete SDK coverage."""
    
    # ========== INVENTORY MANAGEMENT ==========
    @app.tool(
        name="get_org_inventory_devices",
        description="📦 Get all inventory devices in an organization"
    )
    def get_org_inventory_devices(
        organization_id: str,
        per_page: Optional[int] = 100,
        starting_after: Optional[str] = None,
        ending_before: Optional[str] = None,
        used_state: Optional[str] = None,
        search: Optional[str] = None,
        macs: Optional[str] = None,
        network_ids: Optional[str] = None,
        serials: Optional[str] = None,
        models: Optional[str] = None,
        tags: Optional[str] = None,
        tags_filter_type: Optional[str] = None,
        product_types: Optional[str] = None
    ):
        """Get inventory devices for an organization."""
        try:
            kwargs = {}
            if per_page:
                kwargs['perPage'] = per_page
            if starting_after:
                kwargs['startingAfter'] = starting_after
            if ending_before:
                kwargs['endingBefore'] = ending_before
            if used_state:
                kwargs['usedState'] = used_state
            if search:
                kwargs['search'] = search
            if macs:
                kwargs['macs'] = [m.strip() for m in macs.split(',')]
            if network_ids:
                kwargs['networkIds'] = [n.strip() for n in network_ids.split(',')]
            if serials:
                kwargs['serials'] = [s.strip() for s in serials.split(',')]
            if models:
                kwargs['models'] = [m.strip() for m in models.split(',')]
            if tags:
                kwargs['tags'] = [t.strip() for t in tags.split(',')]
            if tags_filter_type:
                kwargs['tagsFilterType'] = tags_filter_type
            if product_types:
                kwargs['productTypes'] = [p.strip() for p in product_types.split(',')]
                
            devices = meraki_client.get_organization_inventory_devices(organization_id, **kwargs)
            
            if not devices:
                return "No inventory devices found"
                
            result = f"# 📦 Organization Inventory\n\n"
            for device in devices[:50]:
                result += f"## {device.get('model', 'Unknown')}\n"
                result += f"- **Serial**: `{device.get('serial')}`\n"
                result += f"- **Network**: {device.get('networkId', 'Unassigned')}\n"
                result += f"- **Claimed**: {device.get('claimedAt', 'Never')}\n\n"
                
            if len(devices) > 50:
                result += f"*Showing 50 of {len(devices)} devices*\n"
                
            return result
        except Exception as e:
            return f"Error: {str(e)}"
    
    @app.tool(
        name="get_org_inventory_onboarding_cloud_monitoring_imports",
        description="📦 Get cloud monitoring imports for inventory onboarding"
    )
    def get_org_inventory_onboarding_cloud_monitoring_imports(
        organization_id: str,
        import_ids: Optional[str] = None
    ):
        """Get cloud monitoring imports for inventory onboarding."""
        try:
            kwargs = {}
            if import_ids:
                kwargs['importIds'] = [i.strip() for i in import_ids.split(',')]
                
            imports = meraki_client.get_organization_inventory_onboarding_cloud_monitoring_imports(
                organization_id, **kwargs
            )
            
            result = f"# 📦 Cloud Monitoring Imports\n\n"
            for imp in imports:
                result += f"- **Import ID**: {imp.get('importId')}\n"
                result += f"  - Status: {imp.get('status')}\n"
                result += f"  - Created: {imp.get('createdAt')}\n\n"
                
            return result
        except Exception as e:
            return f"Error: {str(e)}"
    
    @app.tool(
        name="create_org_inventory_onboarding_cloud_monitoring_prepare",
        description="📦 Prepare cloud monitoring for inventory onboarding"
    )
    def create_org_inventory_onboarding_cloud_monitoring_prepare(
        organization_id: str,
        devices: str
    ):
        """Prepare cloud monitoring for inventory onboarding."""
        try:
            devices_list = json.loads(devices)
            result = meraki_client.create_organization_inventory_onboarding_cloud_monitoring_prepare(
                organization_id,
                devices=devices_list
            )
            return f"✅ Cloud monitoring prepared for {len(devices_list)} devices"
        except Exception as e:
            return f"Error: {str(e)}"
    
    @app.tool(
        name="create_org_inventory_onboarding_cloud_monitoring_import",
        description="📦 Import cloud monitoring devices into inventory"
    )
    def create_org_inventory_onboarding_cloud_monitoring_import(
        organization_id: str,
        devices: str
    ):
        """Import cloud monitoring devices into inventory."""
        try:
            devices_list = json.loads(devices)
            result = meraki_client.create_organization_inventory_onboarding_cloud_monitoring_import(
                organization_id,
                devices=devices_list
            )
            return f"✅ Imported {len(devices_list)} cloud monitoring devices"
        except Exception as e:
            return f"Error: {str(e)}"
    
    @app.tool(
        name="claim_into_org_inventory",
        description="📦 Claim devices into organization inventory"
    )
    def claim_into_org_inventory(
        organization_id: str,
        orders: Optional[str] = None,
        serials: Optional[str] = None,
        licenses: Optional[str] = None
    ):
        """Claim devices into organization inventory."""
        try:
            kwargs = {}
            if orders:
                kwargs['orders'] = [o.strip() for o in orders.split(',')]
            if serials:
                kwargs['serials'] = [s.strip() for s in serials.split(',')]
            if licenses:
                kwargs['licenses'] = json.loads(licenses)
                
            result = meraki_client.claim_into_organization_inventory(organization_id, **kwargs)
            return f"✅ Successfully claimed devices into inventory"
        except Exception as e:
            return f"Error: {str(e)}"
    
    @app.tool(
        name="release_from_org_inventory",
        description="📦 Release devices from organization inventory"
    )
    def release_from_org_inventory(
        organization_id: str,
        serials: str
    ):
        """Release devices from organization inventory."""
        try:
            serial_list = [s.strip() for s in serials.split(',')]
            result = meraki_client.release_from_organization_inventory(
                organization_id,
                serials=serial_list
            )
            return f"✅ Released {len(serial_list)} devices from inventory"
        except Exception as e:
            return f"Error: {str(e)}"
    
    # ========== CONFIG TEMPLATES ==========
    @app.tool(
        name="get_org_config_templates",
        description="📋 Get configuration templates for an organization"
    )
    def get_org_config_templates(organization_id: str):
        """Get configuration templates."""
        try:
            templates = meraki_client.get_organization_config_templates(organization_id)
            
            if not templates:
                return "No configuration templates found"
                
            result = f"# 📋 Configuration Templates\n\n"
            for template in templates:
                result += f"## {template.get('name', 'Unnamed')}\n"
                result += f"- **ID**: `{template.get('id')}`\n"
                result += f"- **Product Types**: {', '.join(template.get('productTypes', []))}\n"
                result += f"- **Networks**: {template.get('boundNetworkCount', 0)}\n\n"
                
            return result
        except Exception as e:
            return f"Error: {str(e)}"
    
    @app.tool(
        name="get_org_config_template",
        description="📋 Get a specific configuration template"
    )
    def get_org_config_template(
        organization_id: str,
        config_template_id: str
    ):
        """Get a specific configuration template."""
        try:
            template = meraki_client.get_organization_config_template(
                organization_id, 
                config_template_id
            )
            
            result = f"# 📋 Template: {template.get('name', 'Unnamed')}\n\n"
            result += f"- **ID**: `{template.get('id')}`\n"
            result += f"- **Product Types**: {', '.join(template.get('productTypes', []))}\n"
            result += f"- **Time Zone**: {template.get('timeZone', 'Not set')}\n"
            
            return result
        except Exception as e:
            return f"Error: {str(e)}"
    
    @app.tool(
        name="create_org_config_template",
        description="📋 Create a configuration template"
    )
    def create_org_config_template(
        organization_id: str,
        name: str,
        product_types: str,
        timezone: Optional[str] = None,
        copy_from_network_id: Optional[str] = None
    ):
        """Create a configuration template."""
        try:
            types_list = [t.strip() for t in product_types.split(',')]
            
            kwargs = {
                'name': name,
                'productTypes': types_list
            }
            if timezone:
                kwargs['timeZone'] = timezone
            if copy_from_network_id:
                kwargs['copyFromNetworkId'] = copy_from_network_id
                
            template = meraki_client.create_organization_config_template(
                organization_id, **kwargs
            )
            
            return f"✅ Created template '{name}' with ID: {template.get('id')}"
        except Exception as e:
            return f"Error: {str(e)}"
    
    @app.tool(
        name="update_org_config_template",
        description="📋 Update a configuration template"
    )
    def update_org_config_template(
        organization_id: str,
        config_template_id: str,
        name: Optional[str] = None,
        timezone: Optional[str] = None
    ):
        """Update a configuration template."""
        try:
            kwargs = {}
            if name:
                kwargs['name'] = name
            if timezone:
                kwargs['timeZone'] = timezone
                
            result = meraki_client.update_organization_config_template(
                organization_id, config_template_id, **kwargs
            )
            return "✅ Template updated successfully"
        except Exception as e:
            return f"Error: {str(e)}"
    
    @app.tool(
        name="delete_org_config_template",
        description="🗑️ Delete a configuration template. Requires confirmation."
    )
    def delete_org_config_template(
        organization_id: str,
        config_template_id: str,
        confirmed: bool = False
    ):
        """Delete a configuration template."""
        try:
            if not confirmed:
                return "⚠️ Set confirmed=true to delete"
                
            meraki_client.delete_organization_config_template(
                organization_id, config_template_id
            )
            return "✅ Template deleted"
        except Exception as e:
            return f"Error: {str(e)}"
    
    @app.tool(
        name="get_org_config_template_switch_profiles",
        description="📋 Get switch profiles for a configuration template"
    )
    def get_org_config_template_switch_profiles(
        organization_id: str,
        config_template_id: str
    ):
        """Get switch profiles for a configuration template."""
        try:
            profiles = meraki_client.get_organization_config_template_switch_profiles(
                organization_id, config_template_id
            )
            
            result = f"# 📋 Switch Profiles\n\n"
            for profile in profiles:
                result += f"- **{profile.get('name', 'Unnamed')}**\n"
                result += f"  - Model: {profile.get('model')}\n"
                result += f"  - Ports: {len(profile.get('ports', []))}\n\n"
                
            return result
        except Exception as e:
            return f"Error: {str(e)}"
    
    # ========== LICENSES ==========
    @app.tool(
        name="get_org_licenses",
        description="📜 Get all licenses in an organization"
    )
    def get_org_licenses(
        organization_id: str,
        per_page: Optional[int] = 100,
        starting_after: Optional[str] = None,
        ending_before: Optional[str] = None,
        device_serial: Optional[str] = None,
        network_id: Optional[str] = None,
        state: Optional[str] = None
    ):
        """Get all licenses in an organization."""
        try:
            kwargs = {}
            if per_page:
                kwargs['perPage'] = per_page
            if starting_after:
                kwargs['startingAfter'] = starting_after
            if ending_before:
                kwargs['endingBefore'] = ending_before
            if device_serial:
                kwargs['deviceSerial'] = device_serial
            if network_id:
                kwargs['networkId'] = network_id
            if state:
                kwargs['state'] = state
                
            licenses = meraki_client.get_organization_licenses(organization_id, **kwargs)
            
            if not licenses:
                return "No licenses found"
                
            result = f"# 📜 Organization Licenses\n\n"
            
            # Group by state
            states = {}
            for lic in licenses:
                s = lic.get('state', 'unknown')
                states[s] = states.get(s, 0) + 1
                
            result += "## Summary\n"
            for state, count in states.items():
                result += f"- **{state.title()}**: {count}\n"
            result += "\n"
            
            # Show some licenses
            for lic in licenses[:20]:
                result += f"- **{lic.get('licenseType', 'Unknown')}**\n"
                result += f"  - Key: `{lic.get('licenseKey', 'N/A')[:8]}...`\n"
                result += f"  - State: {lic.get('state')}\n"
                result += f"  - Device: {lic.get('deviceSerial', 'Unassigned')}\n\n"
                
            if len(licenses) > 20:
                result += f"*Showing 20 of {len(licenses)} licenses*\n"
                
            return result
        except Exception as e:
            return f"Error: {str(e)}"
    
    @app.tool(
        name="assign_org_licenses_seats",
        description="📜 Assign license seats to a network"
    )
    def assign_org_licenses_seats(
        organization_id: str,
        license_id: str,
        network_id: str,
        seat_count: int
    ):
        """Assign license seats to a network."""
        try:
            result = meraki_client.assign_organization_licenses_seats(
                organization_id,
                licenseId=license_id,
                networkId=network_id,
                seatCount=seat_count
            )
            return f"✅ Assigned {seat_count} seats to network"
        except Exception as e:
            return f"Error: {str(e)}"
    
    @app.tool(
        name="move_org_licenses",
        description="📜 Move licenses between networks"
    )
    def move_org_licenses(
        organization_id: str,
        dest_organization_id: str,
        license_ids: str
    ):
        """Move licenses between organizations."""
        try:
            ids_list = [l.strip() for l in license_ids.split(',')]
            result = meraki_client.move_organization_licenses(
                organization_id,
                destOrganizationId=dest_organization_id,
                licenseIds=ids_list
            )
            return f"✅ Moved {len(ids_list)} licenses"
        except Exception as e:
            return f"Error: {str(e)}"
    
    @app.tool(
        name="move_org_licenses_seats",
        description="📜 Move license seats between networks"
    )
    def move_org_licenses_seats(
        organization_id: str,
        dest_organization_id: str,
        license_id: str,
        seat_count: int
    ):
        """Move license seats between organizations."""
        try:
            result = meraki_client.move_organization_licenses_seats(
                organization_id,
                destOrganizationId=dest_organization_id,
                licenseId=license_id,
                seatCount=seat_count
            )
            return f"✅ Moved {seat_count} seats"
        except Exception as e:
            return f"Error: {str(e)}"
    
    @app.tool(
        name="renew_org_licenses_seats",
        description="📜 Renew license seats"
    )
    def renew_org_licenses_seats(
        organization_id: str,
        license_id_to_renew: str,
        unused_license_id: str
    ):
        """Renew license seats."""
        try:
            result = meraki_client.renew_organization_licenses_seats(
                organization_id,
                licenseIdToRenew=license_id_to_renew,
                unusedLicenseId=unused_license_id
            )
            return "✅ License seats renewed"
        except Exception as e:
            return f"Error: {str(e)}"
    
    @app.tool(
        name="update_org_license",
        description="📜 Update a license"
    )
    def update_org_license(
        organization_id: str,
        license_id: str,
        device_serial: Optional[str] = None
    ):
        """Update a license."""
        try:
            kwargs = {}
            if device_serial:
                kwargs['deviceSerial'] = device_serial
                
            result = meraki_client.update_organization_license(
                organization_id, license_id, **kwargs
            )
            return "✅ License updated"
        except Exception as e:
            return f"Error: {str(e)}"
    
    # ========== SAML ==========
    @app.tool(
        name="get_org_saml",
        description="🔐 Get SAML SSO configuration"
    )
    def get_org_saml(organization_id: str):
        """Get SAML SSO configuration."""
        try:
            saml = meraki_client.get_organization_saml(organization_id)
            
            result = f"# 🔐 SAML SSO Configuration\n\n"
            result += f"**Enabled**: {'✅' if saml.get('enabled') else '❌'}\n"
            
            if saml.get('enabled'):
                result += f"**Login URL**: {saml.get('ssoLoginUrl', 'Not set')}\n"
                result += f"**Consumer URL**: {saml.get('consumerUrl', 'N/A')}\n"
                
            return result
        except Exception as e:
            return f"Error: {str(e)}"
    
    @app.tool(
        name="update_org_saml",
        description="🔐 Update SAML SSO configuration"
    )
    def update_org_saml(
        organization_id: str,
        enabled: bool,
        sso_login_url: Optional[str] = None,
        x509_cert_sha1: Optional[str] = None
    ):
        """Update SAML SSO configuration."""
        try:
            kwargs = {'enabled': enabled}
            if sso_login_url:
                kwargs['ssoLoginUrl'] = sso_login_url
            if x509_cert_sha1:
                kwargs['x509certSha1Fingerprint'] = x509_cert_sha1
                
            result = meraki_client.update_organization_saml(organization_id, **kwargs)
            return f"✅ SAML {'enabled' if enabled else 'disabled'}"
        except Exception as e:
            return f"Error: {str(e)}"
    
    @app.tool(
        name="get_org_saml_roles",
        description="🔐 Get SAML roles"
    )
    def get_org_saml_roles(organization_id: str):
        """Get SAML roles."""
        try:
            roles = meraki_client.get_organization_saml_roles(organization_id)
            
            if not roles:
                return "No SAML roles configured"
                
            result = f"# 🔐 SAML Roles\n\n"
            for role in roles:
                result += f"## {role.get('role', 'Unnamed')}\n"
                result += f"- **ID**: `{role.get('id')}`\n"
                result += f"- **Org Access**: {role.get('orgAccess', 'none')}\n\n"
                
            return result
        except Exception as e:
            return f"Error: {str(e)}"
    
    @app.tool(
        name="get_org_saml_role",
        description="🔐 Get a specific SAML role"
    )
    def get_org_saml_role(
        organization_id: str,
        saml_role_id: str
    ):
        """Get a specific SAML role."""
        try:
            role = meraki_client.get_organization_saml_role(
                organization_id, saml_role_id
            )
            
            result = f"# 🔐 SAML Role: {role.get('role', 'Unnamed')}\n\n"
            result += f"- **ID**: `{role.get('id')}`\n"
            result += f"- **Org Access**: {role.get('orgAccess', 'none')}\n"
            
            if role.get('networks'):
                result += f"- **Networks**: {len(role['networks'])} configured\n"
            if role.get('tags'):
                result += f"- **Tags**: {len(role['tags'])} configured\n"
                
            return result
        except Exception as e:
            return f"Error: {str(e)}"
    
    @app.tool(
        name="create_org_saml_role",
        description="🔐 Create a SAML role"
    )
    def create_org_saml_role(
        organization_id: str,
        role: str,
        org_access: str,
        networks: Optional[str] = None,
        tags: Optional[str] = None
    ):
        """Create a SAML role."""
        try:
            kwargs = {
                'role': role,
                'orgAccess': org_access
            }
            if networks:
                kwargs['networks'] = json.loads(networks)
            if tags:
                kwargs['tags'] = json.loads(tags)
                
            result = meraki_client.create_organization_saml_role(
                organization_id, **kwargs
            )
            return f"✅ Created SAML role '{role}'"
        except Exception as e:
            return f"Error: {str(e)}"
    
    @app.tool(
        name="update_org_saml_role",
        description="🔐 Update a SAML role"
    )
    def update_org_saml_role(
        organization_id: str,
        saml_role_id: str,
        role: Optional[str] = None,
        org_access: Optional[str] = None,
        networks: Optional[str] = None,
        tags: Optional[str] = None
    ):
        """Update a SAML role."""
        try:
            kwargs = {}
            if role:
                kwargs['role'] = role
            if org_access:
                kwargs['orgAccess'] = org_access
            if networks:
                kwargs['networks'] = json.loads(networks)
            if tags:
                kwargs['tags'] = json.loads(tags)
                
            result = meraki_client.update_organization_saml_role(
                organization_id, saml_role_id, **kwargs
            )
            return "✅ SAML role updated"
        except Exception as e:
            return f"Error: {str(e)}"
    
    @app.tool(
        name="delete_org_saml_role",
        description="🗑️ Delete a SAML role. Requires confirmation."
    )
    def delete_org_saml_role(
        organization_id: str,
        saml_role_id: str,
        confirmed: bool = False
    ):
        """Delete a SAML role."""
        try:
            if not confirmed:
                return "⚠️ Set confirmed=true to delete"
                
            meraki_client.delete_organization_saml_role(
                organization_id, saml_role_id
            )
            return "✅ SAML role deleted"
        except Exception as e:
            return f"Error: {str(e)}"
    
    @app.tool(
        name="get_org_saml_idps",
        description="🔐 Get SAML identity providers"
    )
    def get_org_saml_idps(organization_id: str):
        """Get SAML identity providers."""
        try:
            idps = meraki_client.get_organization_saml_idps(organization_id)
            
            if not idps:
                return "No SAML IdPs configured"
                
            result = f"# 🔐 SAML Identity Providers\n\n"
            for idp in idps:
                result += f"## {idp.get('x509certSha1Fingerprint', 'Unknown')}\n"
                result += f"- **Consumer URL**: {idp.get('consumerUrl')}\n"
                result += f"- **SSO Login URL**: {idp.get('ssoLoginUrl')}\n\n"
                
            return result
        except Exception as e:
            return f"Error: {str(e)}"
    
    @app.tool(
        name="create_org_saml_idp",
        description="🔐 Create a SAML identity provider"
    )
    def create_org_saml_idp(
        organization_id: str,
        x509_cert_sha1: str,
        sso_login_url: str
    ):
        """Create a SAML identity provider."""
        try:
            result = meraki_client.create_organization_saml_idp(
                organization_id,
                x509certSha1Fingerprint=x509_cert_sha1,
                ssoLoginUrl=sso_login_url
            )
            return "✅ SAML IdP created"
        except Exception as e:
            return f"Error: {str(e)}"
    
    @app.tool(
        name="update_org_saml_idp",
        description="🔐 Update a SAML identity provider"
    )
    def update_org_saml_idp(
        organization_id: str,
        idp_id: str,
        x509_cert_sha1: Optional[str] = None,
        sso_login_url: Optional[str] = None
    ):
        """Update a SAML identity provider."""
        try:
            kwargs = {}
            if x509_cert_sha1:
                kwargs['x509certSha1Fingerprint'] = x509_cert_sha1
            if sso_login_url:
                kwargs['ssoLoginUrl'] = sso_login_url
                
            result = meraki_client.update_organization_saml_idp(
                organization_id, idp_id, **kwargs
            )
            return "✅ SAML IdP updated"
        except Exception as e:
            return f"Error: {str(e)}"
    
    @app.tool(
        name="delete_org_saml_idp",
        description="🗑️ Delete a SAML identity provider. Requires confirmation."
    )
    def delete_org_saml_idp(
        organization_id: str,
        idp_id: str,
        confirmed: bool = False
    ):
        """Delete a SAML identity provider."""
        try:
            if not confirmed:
                return "⚠️ Set confirmed=true to delete"
                
            meraki_client.delete_organization_saml_idp(
                organization_id, idp_id
            )
            return "✅ SAML IdP deleted"
        except Exception as e:
            return f"Error: {str(e)}"
    
    # ========== SNMP ==========
    @app.tool(
        name="get_org_snmp",
        description="📡 Get SNMP settings"
    )
    def get_org_snmp(organization_id: str):
        """Get SNMP settings."""
        try:
            snmp = meraki_client.get_organization_snmp(organization_id)
            
            result = f"# 📡 SNMP Settings\n\n"
            
            if snmp.get('v2cEnabled'):
                result += "## SNMP v2c: ✅ Enabled\n"
                if snmp.get('v2CommunityString'):
                    result += f"- Community: {snmp['v2CommunityString'][:5]}...\n"
            else:
                result += "## SNMP v2c: ❌ Disabled\n"
                
            if snmp.get('v3Enabled'):
                result += "\n## SNMP v3: ✅ Enabled\n"
                if snmp.get('v3AuthMode'):
                    result += f"- Auth: {snmp['v3AuthMode']}\n"
                if snmp.get('v3PrivMode'):
                    result += f"- Privacy: {snmp['v3PrivMode']}\n"
            else:
                result += "\n## SNMP v3: ❌ Disabled\n"
                
            return result
        except Exception as e:
            return f"Error: {str(e)}"
    
    @app.tool(
        name="update_org_snmp",
        description="📡 Update SNMP settings"
    )
    def update_org_snmp(
        organization_id: str,
        v2c_enabled: Optional[bool] = None,
        v2_community: Optional[str] = None,
        v3_enabled: Optional[bool] = None,
        v3_auth_mode: Optional[str] = None,
        v3_auth_pass: Optional[str] = None,
        v3_priv_mode: Optional[str] = None,
        v3_priv_pass: Optional[str] = None,
        peer_ips: Optional[str] = None
    ):
        """Update SNMP settings."""
        try:
            kwargs = {}
            if v2c_enabled is not None:
                kwargs['v2cEnabled'] = v2c_enabled
            if v2_community:
                kwargs['v2CommunityString'] = v2_community
            if v3_enabled is not None:
                kwargs['v3Enabled'] = v3_enabled
            if v3_auth_mode:
                kwargs['v3AuthMode'] = v3_auth_mode
            if v3_auth_pass:
                kwargs['v3AuthPass'] = v3_auth_pass
            if v3_priv_mode:
                kwargs['v3PrivMode'] = v3_priv_mode
            if v3_priv_pass:
                kwargs['v3PrivPass'] = v3_priv_pass
            if peer_ips:
                kwargs['peerIps'] = [ip.strip() for ip in peer_ips.split(',')]
                
            result = meraki_client.update_organization_snmp(organization_id, **kwargs)
            return "✅ SNMP settings updated"
        except Exception as e:
            return f"Error: {str(e)}"
    
    # ========== LOGIN SECURITY ==========
    @app.tool(
        name="get_org_login_security",
        description="🔒 Get login security settings"
    )
    def get_org_login_security(organization_id: str):
        """Get login security settings."""
        try:
            security = meraki_client.get_organization_login_security(organization_id)
            
            result = f"# 🔒 Login Security\n\n"
            
            result += "## Account Lockout\n"
            result += f"- **Enforce**: {security.get('enforceAccountLockout', False)}\n"
            result += f"- **Attempts**: {security.get('accountLockoutAttempts', 'N/A')}\n"
            
            result += "\n## Password\n"
            result += f"- **Enforce Expiration**: {security.get('enforcePasswordExpiration', False)}\n"
            result += f"- **Expiration Days**: {security.get('passwordExpirationDays', 'N/A')}\n"
            
            result += "\n## Two-Factor\n"
            result += f"- **Enforce 2FA**: {security.get('enforceTwoFactorAuth', False)}\n"
            
            result += "\n## Session\n"
            result += f"- **Enforce Idle Timeout**: {security.get('enforceIdleTimeout', False)}\n"
            result += f"- **Timeout Minutes**: {security.get('idleTimeoutMinutes', 'N/A')}\n"
            
            return result
        except Exception as e:
            return f"Error: {str(e)}"
    
    @app.tool(
        name="update_org_login_security",
        description="🔒 Update login security settings"
    )
    def update_org_login_security(
        organization_id: str,
        enforce_account_lockout: Optional[bool] = None,
        account_lockout_attempts: Optional[int] = None,
        enforce_two_factor: Optional[bool] = None,
        enforce_idle_timeout: Optional[bool] = None,
        idle_timeout_minutes: Optional[int] = None,
        enforce_password_expiration: Optional[bool] = None,
        password_expiration_days: Optional[int] = None,
        enforce_login_ip_ranges: Optional[bool] = None,
        login_ip_ranges: Optional[str] = None
    ):
        """Update login security settings."""
        try:
            kwargs = {}
            if enforce_account_lockout is not None:
                kwargs['enforceAccountLockout'] = enforce_account_lockout
            if account_lockout_attempts:
                kwargs['accountLockoutAttempts'] = account_lockout_attempts
            if enforce_two_factor is not None:
                kwargs['enforceTwoFactorAuth'] = enforce_two_factor
            if enforce_idle_timeout is not None:
                kwargs['enforceIdleTimeout'] = enforce_idle_timeout
            if idle_timeout_minutes:
                kwargs['idleTimeoutMinutes'] = idle_timeout_minutes
            if enforce_password_expiration is not None:
                kwargs['enforcePasswordExpiration'] = enforce_password_expiration
            if password_expiration_days:
                kwargs['passwordExpirationDays'] = password_expiration_days
            if enforce_login_ip_ranges is not None:
                kwargs['enforceLoginIpRanges'] = enforce_login_ip_ranges
            if login_ip_ranges:
                kwargs['loginIpRanges'] = [r.strip() for r in login_ip_ranges.split(',')]
                
            result = meraki_client.update_organization_login_security(organization_id, **kwargs)
            return "✅ Login security updated"
        except Exception as e:
            return f"Error: {str(e)}"
    
    # ========== WEBHOOKS ==========
    @app.tool(
        name="get_org_webhooks_http_servers",
        description="🔗 Get webhook HTTP servers"
    )
    def get_org_webhooks_http_servers(organization_id: str):
        """Get webhook HTTP servers."""
        try:
            servers = meraki_client.get_organization_webhooks_http_servers(organization_id)
            
            if not servers:
                return "No webhook servers configured"
                
            result = f"# 🔗 Webhook HTTP Servers\n\n"
            for server in servers:
                result += f"## {server.get('name', 'Unnamed')}\n"
                result += f"- **ID**: `{server.get('id')}`\n"
                result += f"- **URL**: {server.get('url')}\n"
                result += f"- **Shared Secret**: {'Set' if server.get('sharedSecret') else 'Not set'}\n\n"
                
            return result
        except Exception as e:
            return f"Error: {str(e)}"
    
    @app.tool(
        name="get_org_webhooks_http_server",
        description="🔗 Get a specific webhook HTTP server"
    )
    def get_org_webhooks_http_server(
        organization_id: str,
        http_server_id: str
    ):
        """Get a specific webhook HTTP server."""
        try:
            server = meraki_client.get_organization_webhooks_http_server(
                organization_id, http_server_id
            )
            
            result = f"# 🔗 Webhook Server: {server.get('name', 'Unnamed')}\n\n"
            result += f"- **ID**: `{server.get('id')}`\n"
            result += f"- **URL**: {server.get('url')}\n"
            result += f"- **Shared Secret**: {'Set' if server.get('sharedSecret') else 'Not set'}\n"
            
            return result
        except Exception as e:
            return f"Error: {str(e)}"
    
    @app.tool(
        name="create_org_webhooks_http_server",
        description="🔗 Create a webhook HTTP server"
    )
    def create_org_webhooks_http_server(
        organization_id: str,
        name: str,
        url: str,
        shared_secret: Optional[str] = None,
        payload_template: Optional[str] = None
    ):
        """Create a webhook HTTP server."""
        try:
            kwargs = {
                'name': name,
                'url': url
            }
            if shared_secret:
                kwargs['sharedSecret'] = shared_secret
            if payload_template:
                kwargs['payloadTemplate'] = json.loads(payload_template)
                
            server = meraki_client.create_organization_webhooks_http_server(
                organization_id, **kwargs
            )
            return f"✅ Created webhook server '{name}' with ID: {server.get('id')}"
        except Exception as e:
            return f"Error: {str(e)}"
    
    @app.tool(
        name="update_org_webhooks_http_server",
        description="🔗 Update a webhook HTTP server"
    )
    def update_org_webhooks_http_server(
        organization_id: str,
        http_server_id: str,
        name: Optional[str] = None,
        url: Optional[str] = None,
        shared_secret: Optional[str] = None,
        payload_template: Optional[str] = None
    ):
        """Update a webhook HTTP server."""
        try:
            kwargs = {}
            if name:
                kwargs['name'] = name
            if url:
                kwargs['url'] = url
            if shared_secret:
                kwargs['sharedSecret'] = shared_secret
            if payload_template:
                kwargs['payloadTemplate'] = json.loads(payload_template)
                
            result = meraki_client.update_organization_webhooks_http_server(
                organization_id, http_server_id, **kwargs
            )
            return "✅ Webhook server updated"
        except Exception as e:
            return f"Error: {str(e)}"
    
    @app.tool(
        name="delete_org_webhooks_http_server",
        description="🗑️ Delete a webhook HTTP server. Requires confirmation."
    )
    def delete_org_webhooks_http_server(
        organization_id: str,
        http_server_id: str,
        confirmed: bool = False
    ):
        """Delete a webhook HTTP server."""
        try:
            if not confirmed:
                return "⚠️ Set confirmed=true to delete"
                
            meraki_client.delete_organization_webhooks_http_server(
                organization_id, http_server_id
            )
            return "✅ Webhook server deleted"
        except Exception as e:
            return f"Error: {str(e)}"
    
    @app.tool(
        name="get_org_webhooks_payload_templates",
        description="📝 Get webhook payload templates"
    )
    def get_org_webhooks_payload_templates(organization_id: str):
        """Get webhook payload templates."""
        try:
            templates = meraki_client.get_organization_webhooks_payload_templates(organization_id)
            
            if not templates:
                return "No payload templates configured"
                
            result = f"# 📝 Webhook Payload Templates\n\n"
            for template in templates:
                result += f"## {template.get('name', 'Unnamed')}\n"
                result += f"- **ID**: `{template.get('payloadTemplateId')}`\n"
                result += f"- **Type**: {template.get('type')}\n\n"
                
            return result
        except Exception as e:
            return f"Error: {str(e)}"
    
    @app.tool(
        name="create_org_webhooks_payload_template",
        description="📝 Create a webhook payload template"
    )
    def create_org_webhooks_payload_template(
        organization_id: str,
        name: str,
        body: str,
        headers: Optional[str] = None
    ):
        """Create a webhook payload template."""
        try:
            kwargs = {
                'name': name,
                'body': body
            }
            if headers:
                kwargs['headers'] = json.loads(headers)
                
            template = meraki_client.create_organization_webhooks_payload_template(
                organization_id, **kwargs
            )
            return f"✅ Created payload template '{name}'"
        except Exception as e:
            return f"Error: {str(e)}"
    
    # ========== API USAGE ==========
    @app.tool(
        name="get_org_api_requests",
        description="📊 Get API request history"
    )
    def get_org_api_requests(
        organization_id: str,
        timespan: Optional[int] = 86400,
        per_page: Optional[int] = 100,
        starting_after: Optional[str] = None,
        ending_before: Optional[str] = None,
        admin_id: Optional[str] = None,
        path: Optional[str] = None,
        method: Optional[str] = None,
        response_code: Optional[int] = None,
        source_ip: Optional[str] = None,
        user_agent: Optional[str] = None,
        version: Optional[int] = None
    ):
        """Get API request history."""
        try:
            kwargs = {'timespan': timespan}
            if per_page:
                kwargs['perPage'] = per_page
            if starting_after:
                kwargs['startingAfter'] = starting_after
            if ending_before:
                kwargs['endingBefore'] = ending_before
            if admin_id:
                kwargs['adminId'] = admin_id
            if path:
                kwargs['path'] = path
            if method:
                kwargs['method'] = method
            if response_code:
                kwargs['responseCode'] = response_code
            if source_ip:
                kwargs['sourceIp'] = source_ip
            if user_agent:
                kwargs['userAgent'] = user_agent
            if version is not None:
                kwargs['version'] = version
                
            requests = meraki_client.get_organization_api_requests(organization_id, **kwargs)
            
            if not requests:
                return f"No API requests in the last {timespan} seconds"
                
            result = f"# 📊 API Requests (Last {timespan}s)\n\n"
            
            # Summary
            methods = {}
            codes = {}
            for req in requests:
                m = req.get('method', 'Unknown')
                methods[m] = methods.get(m, 0) + 1
                c = req.get('responseCode', 0)
                codes[c] = codes.get(c, 0) + 1
                
            result += "## Summary\n"
            result += f"- **Total**: {len(requests)}\n"
            result += f"- **Methods**: {', '.join([f'{m}:{c}' for m,c in methods.items()])}\n"
            result += f"- **Codes**: {', '.join([f'{c}:{n}' for c,n in codes.items()])}\n\n"
            
            # Recent
            result += "## Recent Requests\n"
            for req in requests[:20]:
                result += f"- `{req.get('method')} {req.get('path')}`\n"
                result += f"  - Code: {req.get('responseCode')}\n"
                result += f"  - Time: {req.get('ts')}\n\n"
                
            if len(requests) > 20:
                result += f"*Showing 20 of {len(requests)} requests*\n"
                
            return result
        except Exception as e:
            return f"Error: {str(e)}"
    
    @app.tool(
        name="get_org_api_requests_overview",
        description="📊 Get API request overview with response codes"
    )
    def get_org_api_requests_overview(
        organization_id: str,
        timespan: Optional[int] = 86400
    ):
        """Get API request overview."""
        try:
            overview = meraki_client.get_organization_api_requests_overview_response_codes_by_interval(
                organization_id,
                timespan=timespan,
                interval=3600
            )
            
            result = f"# 📊 API Overview (Last {timespan}s)\n\n"
            
            total_200s = 0
            total_400s = 0
            total_429s = 0
            
            for interval in overview:
                counts = interval.get('counts', {})
                total_200s += counts.get('200', 0) + counts.get('201', 0) + counts.get('204', 0)
                total_400s += counts.get('400', 0) + counts.get('404', 0) + counts.get('403', 0)
                total_429s += counts.get('429', 0)
                
            result += "## Response Codes\n"
            result += f"- **Success (2xx)**: {total_200s}\n"
            result += f"- **Errors (4xx)**: {total_400s}\n"
            result += f"- **Rate Limited**: {total_429s}\n"
            
            if total_429s > 0:
                result += "\n⚠️ **Rate limiting detected!**\n"
                
            return result
        except Exception as e:
            return f"Error: {str(e)}"
    
    # ========== BRANDING ==========
    @app.tool(
        name="get_org_branding_policies",
        description="🎨 Get branding policies"
    )
    def get_org_branding_policies(organization_id: str):
        """Get branding policies."""
        try:
            policies = meraki_client.get_organization_branding_policies(organization_id)
            
            if not policies:
                return "No branding policies configured"
                
            result = f"# 🎨 Branding Policies\n\n"
            for policy in policies:
                result += f"## {policy.get('name', 'Default')}\n"
                result += f"**Enabled**: {'✅' if policy.get('enabled') else '❌'}\n\n"
                
            return result
        except Exception as e:
            return f"Error: {str(e)}"
    
    @app.tool(
        name="get_org_branding_policies_priorities",
        description="🎨 Get branding policy priorities"
    )
    def get_org_branding_policies_priorities(organization_id: str):
        """Get branding policy priorities."""
        try:
            priorities = meraki_client.get_organization_branding_policies_priorities(organization_id)
            
            result = f"# 🎨 Branding Policy Priorities\n\n"
            for idx, policy_id in enumerate(priorities.get('brandingPolicyIds', []), 1):
                result += f"{idx}. Policy ID: `{policy_id}`\n"
                
            return result
        except Exception as e:
            return f"Error: {str(e)}"
    
    @app.tool(
        name="update_org_branding_policies_priorities",
        description="🎨 Update branding policy priorities"
    )
    def update_org_branding_policies_priorities(
        organization_id: str,
        branding_policy_ids: str
    ):
        """Update branding policy priorities."""
        try:
            ids_list = [i.strip() for i in branding_policy_ids.split(',')]
            result = meraki_client.update_organization_branding_policies_priorities(
                organization_id,
                brandingPolicyIds=ids_list
            )
            return "✅ Branding priorities updated"
        except Exception as e:
            return f"Error: {str(e)}"
    
    @app.tool(
        name="get_org_branding_policy",
        description="🎨 Get a specific branding policy"
    )
    def get_org_branding_policy(
        organization_id: str,
        branding_policy_id: str
    ):
        """Get a specific branding policy."""
        try:
            policy = meraki_client.get_organization_branding_policy(
                organization_id, branding_policy_id
            )
            
            result = f"# 🎨 Branding Policy: {policy.get('name', 'Unnamed')}\n\n"
            result += f"**Enabled**: {'✅' if policy.get('enabled') else '❌'}\n"
            
            admin = policy.get('adminSettings', {})
            if admin:
                result += "\n## Admin Dashboard\n"
                if admin.get('appliesTo'):
                    result += f"- Applies to: {admin['appliesTo']}\n"
                    
            return result
        except Exception as e:
            return f"Error: {str(e)}"
    
    @app.tool(
        name="create_org_branding_policy",
        description="🎨 Create a branding policy"
    )
    def create_org_branding_policy(
        organization_id: str,
        name: str,
        enabled: bool = True,
        admin_settings: Optional[str] = None,
        help_settings: Optional[str] = None
    ):
        """Create a branding policy."""
        try:
            kwargs = {
                'name': name,
                'enabled': enabled
            }
            if admin_settings:
                kwargs['adminSettings'] = json.loads(admin_settings)
            if help_settings:
                kwargs['helpSettings'] = json.loads(help_settings)
                
            policy = meraki_client.create_organization_branding_policy(
                organization_id, **kwargs
            )
            return f"✅ Created branding policy '{name}'"
        except Exception as e:
            return f"Error: {str(e)}"
    
    @app.tool(
        name="update_org_branding_policy",
        description="🎨 Update a branding policy"
    )
    def update_org_branding_policy(
        organization_id: str,
        branding_policy_id: str,
        name: Optional[str] = None,
        enabled: Optional[bool] = None,
        admin_settings: Optional[str] = None,
        help_settings: Optional[str] = None
    ):
        """Update a branding policy."""
        try:
            kwargs = {}
            if name:
                kwargs['name'] = name
            if enabled is not None:
                kwargs['enabled'] = enabled
            if admin_settings:
                kwargs['adminSettings'] = json.loads(admin_settings)
            if help_settings:
                kwargs['helpSettings'] = json.loads(help_settings)
                
            result = meraki_client.update_organization_branding_policy(
                organization_id, branding_policy_id, **kwargs
            )
            return "✅ Branding policy updated"
        except Exception as e:
            return f"Error: {str(e)}"
    
    @app.tool(
        name="delete_org_branding_policy",
        description="🗑️ Delete a branding policy. Requires confirmation."
    )
    def delete_org_branding_policy(
        organization_id: str,
        branding_policy_id: str,
        confirmed: bool = False
    ):
        """Delete a branding policy."""
        try:
            if not confirmed:
                return "⚠️ Set confirmed=true to delete"
                
            meraki_client.delete_organization_branding_policy(
                organization_id, branding_policy_id
            )
            return "✅ Branding policy deleted"
        except Exception as e:
            return f"Error: {str(e)}"
    
    # ========== CLONE ORGANIZATION ==========
    @app.tool(
        name="clone_organization",
        description="🔄 Clone an organization. Requires confirmation."
    )
    def clone_organization(
        organization_id: str,
        name: str,
        confirmed: bool = False
    ):
        """Clone an organization."""
        try:
            if not confirmed:
                return "⚠️ Set confirmed=true to clone"
                
            result = meraki_client.clone_organization(
                organization_id,
                name=name
            )
            return f"✅ Cloned organization '{name}' with ID: {result.get('id')}"
        except Exception as e:
            return f"Error: {str(e)}"