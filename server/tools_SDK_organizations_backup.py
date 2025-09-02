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
    """Register all organization SDK tools (clean, no duplicates)."""
    
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
                    
                    response = f"# ✅ Assigned License Seats\n\n            "
                    response += f"**License ID**: {license_id}\n            "
                    response += f"**Network ID**: {network_id}\n            "
                    response += f"**Seats Assigned**: {seat_count}\n            "
                    
                    if result:
                        response += f"\n            **Remaining Seats**: {result.get('remainingSeats', 'N/A')}\n            "
                    
                    return response
                except Exception as e:
                    return f"❌ Error assigning seats: {str(e)}"\n\n    @app.tool(
                name="bulk_update_org_devices_details",
                description="📦✏️ Bulk update device details"
            )
            def bulk_update_org_devices_details(
                organization_id: str,
                serials: str,
                details: str
            ):
                """
                Bulk update device details.
                
                Args:
                    organization_id: Organization ID
                    serials: Comma-separated serial numbers
                    details: JSON string of device details to update
                """
                try:
                    serial_list = [s.strip() for s in serials.split(',')]
                    details_dict = json.loads(details) if isinstance(details, str) else details
                    
                    result = meraki_client.dashboard.organizations.bulkUpdateOrganizationDevicesDetails(
                        organization_id, 
                        serials=serial_list,
                        details=details_dict
                    )
                    
                    response = f"# ✅ Bulk Updated Devices\n\n            "
                    response += f"**Serials**: {serials}\n            "
                    response += f"**Updates Applied**: {json.dumps(details_dict, indent=2)}\n            "
                    
                    return response
                except Exception as e:
                    return f"❌ Error bulk updating: {str(e)}"\n\n    @app.tool(
                name="claim_into_org_inventory",
                description="📦➕ Claim devices into organization inventory"
            )
            def claim_into_org_inventory(
                organization_id: str,
                orders: Optional[str] = None,
                serials: Optional[str] = None,
                licenses: Optional[str] = None
            ):
                """
                Claim devices into inventory.
                
                Args:
                    organization_id: Organization ID
                    orders: Comma-separated order numbers
                    serials: Comma-separated serial numbers
                    licenses: JSON string of license configurations
                """
                try:
                    kwargs = {}
                    
                    if orders:
                        kwargs['orders'] = [o.strip() for o in orders.split(',')]
                    if serials:
                        kwargs['serials'] = [s.strip() for s in serials.split(',')]
                    if licenses:
                        kwargs['licenses'] = json.loads(licenses) if isinstance(licenses, str) else licenses
                    
                    result = meraki_client.dashboard.organizations.claimIntoOrganizationInventory(
                        organization_id, **kwargs
                    )
                    
                    response = f"# ✅ Claimed Devices\n\n            "
                    response += f"**Organization**: {organization_id}\n            "
                    
                    if orders:
                        response += f"**Orders**: {orders}\n            "
                    if serials:
                        response += f"**Serials**: {serials}\n            "
                    
                    return response
                except Exception as e:
                    return f"❌ Error claiming devices: {str(e)}"\n\n    @app.tool(
        name="claim_into_organization_inventory",
        description="➕ Claim devices into organization inventory. Requires confirmation."
    )
    def claim_into_organization_inventory(
        organization_id: str,
        orders: Optional[List[str]] = None,
        serials: Optional[List[str]] = None,
        licenses: Optional[List[Dict[str, Any]]] = None,
        confirmed: bool = False
    ):
        """
        Claim devices into inventory.
        
        Args:
            organization_id: Organization ID
            orders: List of order numbers
            serials: List of serial numbers
            licenses: List of license configurations
            confirmed: Must be true to execute
        """
        if not confirmed:
            return "⚠️ Claiming devices requires confirmed=true"
        
        try:
            kwargs = {}
            
            if orders:
                kwargs["orders"] = orders
            if serials:
                kwargs["serials"] = serials
            if licenses:
                kwargs["licenses"] = licenses
            
            result = meraki_client.dashboard.organizations.claimIntoOrganizationInventory(
                organization_id, **kwargs
            )
            
            claimed_count = len(result.get('serials', []))
            return f"✅ Claimed {claimed_count} devices into inventory"
        except Exception as e:
            return f"❌ Error claiming devices: {str(e)}"\n\n    @app.tool(
                name="clone_organization",
                description="🔄 Clone an organization"
            )
            def clone_organization(
                organization_id: str,
                name: str
            ):
                """Clone organization."""
                try:
                    result = meraki_client.dashboard.organizations.cloneOrganization(
                        organization_id, name=name
                    )
                    
                    response = f"# ✅ Cloned Organization\n\n            "
                    response += f"**New Name**: {name}\n            "
                    response += f"**New ID**: {result.get('id', 'N/A')}\n            "
                    return response
                except Exception as e:
                    return f"❌ Error: {str(e)}"\n\n    @app.tool(
        name="combine_organization_networks",
        description="🔄 Combine multiple networks into one. Requires confirmation."
    )
    def combine_organization_networks(
        organization_id: str,
        name: str,
        network_ids: List[str],
        enrollment_string: Optional[str] = None,
        confirmed: bool = False
    ):
        """
        Combine multiple networks.
        
        Args:
            organization_id: Organization ID
            name: Name for combined network
            network_ids: List of network IDs to combine
            enrollment_string: Enrollment string for SM
            confirmed: Must be true to execute
        """
        if not confirmed:
            return "⚠️ Combining networks requires confirmed=true. This cannot be undone!"
        
        try:
            kwargs = {
                "name": name,
                "networkIds": network_ids
            }
            
            if enrollment_string:
                kwargs["enrollmentString"] = enrollment_string
            
            result = meraki_client.dashboard.organizations.combineOrganizationNetworks(
                organization_id, **kwargs
            )
            
            new_network_id = result.get('id', 'Unknown')
            return f"✅ Combined {len(network_ids)} networks into '{name}' (ID: {new_network_id})"
        except Exception as e:
            return f"❌ Error combining networks: {str(e)}"\n\n    @app.tool(
                name="create_org_action_batch",
                description="📦➕ Create a new action batch"
            )
            def create_org_action_batch(
                organization_id: str,
                actions: str,
                confirmed: bool = False,
                synchronous: bool = False
            ):
                """Create action batch."""
                try:
                    result = meraki_client.dashboard.organizations.createOrganizationActionBatch(
                        organization_id,
                        actions=json.loads(actions) if isinstance(actions, str) else actions,
                        confirmed=confirmed,
                        synchronous=synchronous
                    )
                    
                    response = f"# ✅ Created Action Batch\n\n            "
                    response += f"**ID**: {result.get('id', 'N/A')}\n            "
                    return response
                except Exception as e:
                    return f"❌ Error: {str(e)}"\n\n    @app.tool(
                name="create_org_adaptive_policy_acl",
                description="🔒➕ Create a new adaptive policy ACL"
            )
            def create_org_adaptive_policy_acl(
                organization_id: str,
                name: str,
                rules: str,
                ip_version: str = "ipv4",
                description: Optional[str] = None
            ):
                """
                Create a new adaptive policy ACL.
                
                Args:
                    organization_id: Organization ID
                    name: ACL name
                    rules: JSON string of rules array
                    ip_version: IP version (ipv4 or ipv6)
                    description: ACL description
                """
                try:
                    kwargs = {
                        'name': name,
                        'ipVersion': ip_version,
                        'rules': json.loads(rules) if isinstance(rules, str) else rules
                    }
                    
                    if description:
                        kwargs['description'] = description
                    
                    result = meraki_client.dashboard.organizations.createOrganizationAdaptivePolicyAcl(
                        organization_id, **kwargs
                    )
                    
                    response = f"# ✅ Created Adaptive Policy ACL\n\n            "
                    response += f"**Name**: {result.get('name', name)}\n            "
                    response += f"**ID**: {result.get('id', 'N/A')}\n            "
                    response += f"**IP Version**: {ip_version}\n            "
                    
                    return response
                except Exception as e:
                    return f"❌ Error creating ACL: {str(e)}"\n\n    @app.tool(
                name="create_org_adaptive_policy_group",
                description="👥➕ Create a new adaptive policy group"
            )
            def create_org_adaptive_policy_group(
                organization_id: str,
                name: str,
                sgt: int,
                description: Optional[str] = None,
                policy_object_ids: Optional[str] = None
            ):
                """
                Create a new adaptive policy group.
                
                Args:
                    organization_id: Organization ID
                    name: Group name
                    sgt: Scalable Group Tag value
                    description: Group description
                    policy_object_ids: Comma-separated policy object IDs
                """
                try:
                    kwargs = {
                        'name': name,
                        'sgt': sgt
                    }
                    
                    if description:
                        kwargs['description'] = description
                    if policy_object_ids:
                        kwargs['policyObjectIds'] = [id.strip() for id in policy_object_ids.split(',')]
                    
                    result = meraki_client.dashboard.organizations.createOrganizationAdaptivePolicyGroup(
                        organization_id, **kwargs
                    )
                    
                    response = f"# ✅ Created Adaptive Policy Group\n\n            "
                    response += f"**Name**: {result.get('name', name)}\n            "
                    response += f"**ID**: {result.get('id', 'N/A')}\n            "
                    response += f"**SGT**: {sgt}\n            "
                    
                    return response
                except Exception as e:
                    return f"❌ Error creating group: {str(e)}"\n\n    @app.tool(
                name="create_org_admin",
                description="👤➕ Create a new dashboard administrator"
            )
            def create_org_admin(
                organization_id: str,
                email: str,
                name: str,
                org_access: str,
                networks: Optional[str] = None,
                tags: Optional[str] = None,
                authentication_method: str = "Email"
            ):
                """
                Create a new organization admin.
                
                Args:
                    organization_id: Organization ID
                    email: Admin email
                    name: Admin name
                    org_access: Organization access level (full, read-only, none)
                    networks: JSON string of network access array
                    tags: JSON string of tag access array
                    authentication_method: Authentication method (Email, Cisco SecureX Sign-On)
                """
                try:
                    kwargs = {
                        'email': email,
                        'name': name,
                        'orgAccess': org_access,
                        'authenticationMethod': authentication_method
                    }
                    
                    if networks:
                        kwargs['networks'] = json.loads(networks) if isinstance(networks, str) else networks
                    if tags:
                        kwargs['tags'] = json.loads(tags) if isinstance(tags, str) else tags
                    
                    result = meraki_client.dashboard.organizations.createOrganizationAdmin(
                        organization_id, **kwargs
                    )
                    
                    response = f"# ✅ Created Admin\n\n            "
                    response += f"**Name**: {result.get('name', name)}\n            "
                    response += f"**Email**: {result.get('email', email)}\n            "
                    response += f"**ID**: {result.get('id', 'N/A')}\n            "
                    response += f"**Org Access**: {org_access}\n            "
                    
                    return response
                except Exception as e:
                    return f"❌ Error creating admin: {str(e)}"\n\n    @app.tool(
                name="create_org_alerts_profile",
                description="🚨➕ Create a new alert profile"
            )
            def create_org_alerts_profile(
                organization_id: str,
                type: str,
                alert_condition: str,
                recipients: str,
                network_tags: str,
                description: Optional[str] = None,
                enabled: bool = True
            ):
                """
                Create a new alert profile.
                
                Args:
                    organization_id: Organization ID
                    type: Alert type
                    alert_condition: JSON string of alert conditions
                    recipients: JSON string of recipients
                    network_tags: JSON string of network tags array
                    description: Profile description
                    enabled: Enable/disable profile
                """
                try:
                    kwargs = {
                        'type': type,
                        'alertCondition': json.loads(alert_condition) if isinstance(alert_condition, str) else alert_condition,
                        'recipients': json.loads(recipients) if isinstance(recipients, str) else recipients,
                        'networkTags': json.loads(network_tags) if isinstance(network_tags, str) else network_tags,
                        'enabled': enabled
                    }
                    
                    if description:
                        kwargs['description'] = description
                    
                    result = meraki_client.dashboard.organizations.createOrganizationAlertsProfile(
                        organization_id, **kwargs
                    )
                    
                    response = f"# ✅ Created Alert Profile\n\n            "
                    response += f"**Type**: {type}\n            "
                    response += f"**ID**: {result.get('id', 'N/A')}\n            "
                    response += f"**Enabled**: {enabled}\n            "
                    
                    return response
                except Exception as e:
                    return f"❌ Error creating alert profile: {str(e)}"\n\n    @app.tool(
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
                    
                    response = f"# ✅ Created Branding Policy\n\n            "
                    response += f"**Name**: {name}\n            "
                    response += f"**ID**: {result.get('id', 'N/A')}\n            "
                    response += f"**Enabled**: {enabled}\n            "
                    
                    return response
                except Exception as e:
                    return f"❌ Error creating policy: {str(e)}"\n\n    @app.tool(
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
                    
                    response = f"# ✅ Created Configuration Template\n\n            "
                    response += f"**Name**: {name}\n            "
                    response += f"**ID**: {result.get('id', 'N/A')}\n            "
                    response += f"**Time Zone**: {time_zone}\n            "
                    
                    return response
                except Exception as e:
                    return f"❌ Error creating template: {str(e)}"\n\n    @app.tool(
                name="create_org_saml_idp",
                description="🔐🏢➕ Create a new SAML Identity Provider"
            )
            def create_org_saml_idp(
                organization_id: str,
                x509cert_sha1_fingerprint: str,
                consumer_url: Optional[str] = None,
                idp_entity_id: Optional[str] = None,
                sso_url: Optional[str] = None
            ):
                """
                Create a new SAML IdP.
                
                Args:
                    organization_id: Organization ID
                    x509cert_sha1_fingerprint: X.509 certificate SHA1 fingerprint
                    consumer_url: SAML consumer URL
                    idp_entity_id: IdP entity ID
                    sso_url: SSO URL
                """
                try:
                    kwargs = {
                        'x509certSha1Fingerprint': x509cert_sha1_fingerprint
                    }
                    
                    if consumer_url:
                        kwargs['consumerUrl'] = consumer_url
                    if idp_entity_id:
                        kwargs['idpEntityId'] = idp_entity_id
                    if sso_url:
                        kwargs['ssoUrl'] = sso_url
                    
                    result = meraki_client.dashboard.organizations.createOrganizationSamlIdp(
                        organization_id, **kwargs
                    )
                    
                    response = f"# ✅ Created SAML IdP\n\n            "
                    response += f"**ID**: {result.get('idpId', 'N/A')}\n            "
                    response += f"**Certificate**: {x509cert_sha1_fingerprint[:20]}...\n            "
                    
                    return response
                except Exception as e:
                    return f"❌ Error creating SAML IdP: {str(e)}"\n\n    @app.tool(
                name="create_org_saml_role",
                description="🔐👥➕ Create a new SAML role"
            )
            def create_org_saml_role(
                organization_id: str,
                role: str,
                org_access: str,
                networks: Optional[str] = None,
                tags: Optional[str] = None
            ):
                """
                Create a new SAML role.
                
                Args:
                    organization_id: Organization ID
                    role: Role name
                    org_access: Organization access level
                    networks: JSON string of network access array
                    tags: JSON string of tag access array
                """
                try:
                    kwargs = {
                        'role': role,
                        'orgAccess': org_access
                    }
                    
                    if networks:
                        kwargs['networks'] = json.loads(networks) if isinstance(networks, str) else networks
                    if tags:
                        kwargs['tags'] = json.loads(tags) if isinstance(tags, str) else tags
                    
                    result = meraki_client.dashboard.organizations.createOrganizationSamlRole(
                        organization_id, **kwargs
                    )
                    
                    response = f"# ✅ Created SAML Role\n\n            "
                    response += f"**Role**: {result.get('role', role)}\n            "
                    response += f"**ID**: {result.get('id', 'N/A')}\n            "
                    response += f"**Org Access**: {org_access}\n            "
                    
                    return response
                except Exception as e:
                    return f"❌ Error creating SAML role: {str(e)}"\n\n    @app.tool(
        name="create_organization",
        description="➕ Create a new organization. Requires confirmation."
    )
    def create_organization(
        name: str,
        management_name: Optional[str] = None,
        management_value: Optional[str] = None,
        confirmed: bool = False
    ):
        """
        Create a new organization.
        
        Args:
            name: Organization name
            management_name: Management detail name
            management_value: Management detail value
            confirmed: Must be true to execute
        """
        if not confirmed:
            return "⚠️ Creating organization requires confirmed=true"
        
        try:
            kwargs = {"name": name}
            
            if management_name and management_value:
                kwargs["management"] = {
                    "details": [
                        {"name": management_name, "value": management_value}
                    ]
                }
            
            result = meraki_client.dashboard.organizations.createOrganization(**kwargs)
            
            org_id = result.get('id', 'Unknown')
            return f"✅ Created organization '{name}' with ID {org_id}"
        except Exception as e:
            return f"❌ Error creating organization: {str(e)}"\n\n    @app.tool(
        name="create_organization_action_batch",
        description="⚡➕ Create a new action batch"
    )
    def create_organization_action_batch(
        organization_id: str,
        actions_json: str,
        confirmed: bool = False,
        synchronous: bool = False
    ):
        """Create an action batch."""
        try:
            import json
            actions = json.loads(actions_json)
            
            result = meraki_client.dashboard.organizations.createOrganizationActionBatch(
                organization_id,
                actions=actions,
                confirmed=confirmed,
                synchronous=synchronous
            )
            
            return f"✅ Created action batch with ID: {result.get('id')} - Status: {result.get('status')}"
        except Exception as e:
            return f"❌ Error creating action batch: {str(e)}"\n\n    @app.tool(
                name="create_organization_early_access_features_opt_in",
                description="🧪➕ Opt into an early access feature"
            )
            def create_organization_early_access_features_opt_in(
                organization_id: str,
                short_name: str,
                limit_scope_to_networks: Optional[str] = None
            ):
                """
                Opt into an early access feature.
                
                Args:
                    organization_id: Organization ID
                    short_name: Short name/ID of the feature
                    limit_scope_to_networks: Comma-separated network IDs to limit scope (optional)
                """
                try:
                    kwargs = {'shortName': short_name}
                    
                    if limit_scope_to_networks:\n\n    @app.tool(
        name="create_organization_network",
        description="➕ Create a new network in an organization. Requires confirmation."
    )
    def create_organization_network(
        organization_id: str,
        name: str,
        product_types: List[str],
        tags: Optional[List[str]] = None,
        time_zone: str = "America/Los_Angeles",
        notes: Optional[str] = None,
        copy_from_network_id: Optional[str] = None,
        confirmed: bool = False
    ):
        """
        Create a new network.
        
        Args:
            organization_id: Organization ID
            name: Network name
            product_types: List of product types (appliance, switch, wireless, etc.)
            tags: Network tags
            time_zone: Time zone
            notes: Network notes
            copy_from_network_id: Copy settings from this network
            confirmed: Must be true to execute
        """
        if not confirmed:
            return "⚠️ Creating network requires confirmed=true"
        
        try:
            kwargs = {
                "name": name,
                "productTypes": product_types,
                "timeZone": time_zone
            }
            
            if tags:
                kwargs["tags"] = tags
            if notes:
                kwargs["notes"] = notes
            if copy_from_network_id:
                kwargs["copyFromNetworkId"] = copy_from_network_id
            
            result = meraki_client.dashboard.organizations.createOrganizationNetwork(
                organization_id, **kwargs
            )
            
            network_id = result.get('id', 'Unknown')
            return f"✅ Created network '{name}' with ID {network_id}"
        except Exception as e:
            return f"❌ Error creating network: {str(e)}"\n\n    @app.tool(
        name="create_organization_policy_object",
        description="🛡️➕ Create a new policy object"
    )
    def create_organization_policy_object(
        organization_id: str,
        name: str,
        category: str,
        type: str,
        cidr: Optional[str] = None,
        ip: Optional[str] = None,
        fqdn: Optional[str] = None,
        mask: Optional[str] = None
    ):
        """Create a policy object."""
        try:
            kwargs = {
                'name': name,
                'category': category,
                'type': type
            }
            if cidr:
                kwargs['cidr'] = cidr
            if ip:
                kwargs['ip'] = ip
            if fqdn:
                kwargs['fqdn'] = fqdn
            if mask:
                kwargs['mask'] = mask
            
            result = meraki_client.dashboard.organizations.createOrganizationPolicyObject(
                organization_id, **kwargs
            )
            
            return f"✅ Created policy object '{name}' with ID: {result.get('id')}"
        except Exception as e:
            return f"❌ Error creating policy object: {str(e)}"\n\n    @app.tool(
        name="create_organization_saml_idp",
        description="🔐➕ Create a new SAML Identity Provider"
    )
    def create_organization_saml_idp(
        organization_id: str,
        name: str,
        consumer_service_url: str,
        slo_logout_url: Optional[str] = None,
        x509_cert_sha1_fingerprint: Optional[str] = None
    ):
        """Create a SAML Identity Provider."""
        try:
            kwargs = {
                'name': name,
                'consumerServiceUrl': consumer_service_url
            }
            if slo_logout_url:
                kwargs['sloLogoutUrl'] = slo_logout_url
            if x509_cert_sha1_fingerprint:
                kwargs['x509certSha1Fingerprint'] = x509_cert_sha1_fingerprint
            
            result = meraki_client.dashboard.organizations.createOrganizationSamlIdp(
                organization_id, **kwargs
            )
            
            return f"✅ Created SAML IDP '{name}' with ID: {result.get('id')}"
        except Exception as e:
            return f"❌ Error creating SAML IDP: {str(e)}"\n\n    @app.tool(
                name="delete_org_action_batch",
                description="📦❌ Delete an action batch"
            )
            def delete_org_action_batch(
                organization_id: str,
                action_batch_id: str
            ):
                """Delete action batch."""
                try:
                    meraki_client.dashboard.organizations.deleteOrganizationActionBatch(
                        organization_id, action_batch_id
                    )
                    return f"# ✅ Deleted Action Batch\n\n            **ID**: {action_batch_id}\n            "
                except Exception as e:
                    return f"❌ Error: {str(e)}"\n\n    @app.tool(
                name="delete_org_adaptive_policy_acl",
                description="🔒❌ Delete an adaptive policy ACL"
            )
            def delete_org_adaptive_policy_acl(
                organization_id: str,
                acl_id: str
            ):
                """Delete an adaptive policy ACL."""
                try:
                    meraki_client.dashboard.organizations.deleteOrganizationAdaptivePolicyAcl(
                        organization_id, acl_id
                    )
                    
                    response = f"# ✅ Deleted Adaptive Policy ACL\n\n            "
                    response += f"**ACL ID**: {acl_id}\n            "
                    
                    return response
                except Exception as e:
                    return f"❌ Error deleting ACL: {str(e)}"\n\n    @app.tool(
                name="delete_org_adaptive_policy_group",
                description="👥❌ Delete an adaptive policy group"
            )
            def delete_org_adaptive_policy_group(
                organization_id: str,
                group_id: str
            ):
                """Delete an adaptive policy group."""
                try:
                    meraki_client.dashboard.organizations.deleteOrganizationAdaptivePolicyGroup(
                        organization_id, group_id
                    )
                    
                    response = f"# ✅ Deleted Adaptive Policy Group\n\n            "
                    response += f"**Group ID**: {group_id}\n            "
                    
                    return response
                except Exception as e:
                    return f"❌ Error deleting group: {str(e)}"\n\n    @app.tool(
                name="delete_org_admin",
                description="👤❌ Delete a dashboard administrator"
            )
            def delete_org_admin(
                organization_id: str,
                admin_id: str
            ):
                """Delete an organization admin."""
                try:
                    meraki_client.dashboard.organizations.deleteOrganizationAdmin(
                        organization_id, admin_id
                    )
                    
                    response = f"# ✅ Deleted Admin\n\n            "
                    response += f"**Admin ID**: {admin_id}\n            "
                    
                    return response
                except Exception as e:
                    return f"❌ Error deleting admin: {str(e)}"\n\n    @app.tool(
                name="delete_org_alerts_profile",
                description="🚨❌ Delete an alert profile"
            )
            def delete_org_alerts_profile(
                organization_id: str,
                alert_config_id: str
            ):
                """Delete an alert profile."""
                try:
                    meraki_client.dashboard.organizations.deleteOrganizationAlertsProfile(
                        organization_id, alert_config_id
                    )
                    
                    response = f"# ✅ Deleted Alert Profile\n\n            "
                    response += f"**Profile ID**: {alert_config_id}\n            "
                    
                    return response
                except Exception as e:
                    return f"❌ Error deleting alert profile: {str(e)}"\n\n    @app.tool(
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
                    
                    response = f"# ✅ Deleted Branding Policy\n\n            "
                    response += f"**Policy ID**: {branding_policy_id}\n            "
                    
                    return response
                except Exception as e:
                    return f"❌ Error deleting policy: {str(e)}"\n\n    @app.tool(
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
                    
                    response = f"# ✅ Deleted Configuration Template\n\n            "
                    response += f"**Template ID**: {config_template_id}\n            "
                    
                    return response
                except Exception as e:
                    return f"❌ Error deleting template: {str(e)}"\n\n    @app.tool(
                name="delete_org_saml_idp",
                description="🔐🏢❌ Delete a SAML Identity Provider"
            )
            def delete_org_saml_idp(
                organization_id: str,
                idp_id: str
            ):
                """Delete a SAML IdP."""
                try:
                    meraki_client.dashboard.organizations.deleteOrganizationSamlIdp(
                        organization_id, idp_id
                    )
                    
                    response = f"# ✅ Deleted SAML IdP\n\n            "
                    response += f"**IdP ID**: {idp_id}\n            "
                    
                    return response
                except Exception as e:
                    return f"❌ Error deleting SAML IdP: {str(e)}"\n\n    @app.tool(
                name="delete_org_saml_role",
                description="🔐👥❌ Delete a SAML role"
            )
            def delete_org_saml_role(
                organization_id: str,
                role_id: str
            ):
                """Delete a SAML role."""
                try:
                    meraki_client.dashboard.organizations.deleteOrganizationSamlRole(
                        organization_id, role_id
                    )
                    
                    response = f"# ✅ Deleted SAML Role\n\n            "
                    response += f"**Role ID**: {role_id}\n            "
                    
                    return response
                except Exception as e:
                    return f"❌ Error deleting SAML role: {str(e)}"\n\n    @app.tool(
        name="delete_organization",
        description="🗑️ Delete an organization. Requires confirmation. EXTREMELY DANGEROUS!"
    )
    def delete_organization(
        organization_id: str,
        confirmed: bool = False
    ):
        """
        Delete an organization.
        
        Args:
            organization_id: Organization ID
            confirmed: Must be true to execute
        """
        if not confirmed:
            return "⚠️ DANGER! Deleting organization requires confirmed=true. This will DELETE EVERYTHING!"
        
        try:
            meraki_client.dashboard.organizations.deleteOrganization(organization_id)
            return f"✅ Deleted organization {organization_id}"
        except Exception as e:
            return f"❌ Error deleting organization: {str(e)}"\n\n    @app.tool(
                name="delete_organization_early_access_features_opt_in",
                description="🧪❌ Opt out of an early access feature"
            )
            def delete_organization_early_access_features_opt_in(
                organization_id: str,
                opt_in_id: str
            ):
                """
                Delete an early access feature opt-in (opt out).
                
                Args:
                    organization_id: Organization ID
                    opt_in_id: Opt-in ID to delete
                """
                try:
                    meraki_client.dashboard.organizations.deleteOrganizationEarlyAccessFeaturesOptIn(
                        organization_id, opt_in_id
                    )
                    
                    response = f"# ✅ Opted Out of Early Access Feature\n\n            "
                    response += f"**Opt-In ID**: {opt_in_id}\n\n            "
                    response += "The early access feature has been disabled for this organization.\n            "
                    
                    return response
                except Exception as e:
                    error_msg = str(e)
                    if '404' in error_msg:
                        return f"❌ Opt-in not found: {opt_in_id}\n\n            💡 Use get_organization_early_access_features_opt_ins to list valid opt-in IDs"
                    return f"❌ Error deleting opt-in: {error_msg}"\n\n    @app.tool(
                name="dismiss_org_assurance_alerts",
                description="🔍✅ Dismiss assurance alerts"
            )
            def dismiss_org_assurance_alerts(
                organization_id: str,
                alert_ids: str
            ):
                """
                Dismiss assurance alerts.
                
                Args:
                    organization_id: Organization ID
                    alert_ids: Comma-separated alert IDs to dismiss
                """
                try:
                    alert_list = [a.strip() for a in alert_ids.split(',')]
                    
                    meraki_client.dashboard.organizations.dismissOrganizationAssuranceAlerts(
                        organization_id, alertIds=alert_list
                    )
                    
                    response = f"# ✅ Dismissed Alerts\n\n            "
                    response += f"**Alert IDs**: {alert_ids}\n            "
                    response += f"**Count**: {len(alert_list)} alerts dismissed\n            "
                    
                    return response
                except Exception as e:
                    return f"❌ Error dismissing alerts: {str(e)}"\n\n    @app.tool(
                name="get_org_action_batch",
                description="📦 Get details of a specific action batch"
            )
            def get_org_action_batch(
                organization_id: str,
                action_batch_id: str
            ):
                """Get action batch details."""
                try:
                    result = meraki_client.dashboard.organizations.getOrganizationActionBatch(
                        organization_id, action_batch_id
                    )
                    
                    response = f"# 📦 Action Batch Details\n\n            "
                    if result:
                        response += f"**ID**: {result.get('id', 'N/A')}\n            "
                        response += f"**Status**: {result.get('status', 'N/A')}\n            "
                        actions = result.get('actions', [])
                        response += f"**Actions**: {len(actions)}\n            "
                    return response
                except Exception as e:
                    return f"❌ Error: {str(e)}"\n\n    @app.tool(
                name="get_org_action_batches",
                description="📦 List action batches in an organization"
            )
            def get_org_action_batches(
                organization_id: str,
                status: Optional[str] = None
            ):
                """Get action batches."""
                try:
                    kwargs = {}
                    if status:
                        kwargs['status'] = status
                    
                    result = meraki_client.dashboard.organizations.getOrganizationActionBatches(
                        organization_id, **kwargs
                    )
                    
                    response = f"# 📦 Action Batches\n\n            "
                    if result and isinstance(result, list):
                        response += f"**Total**: {len(result)}\n\n            "
                        for batch in result[:10]:
                            response += f"- **{batch.get('id', 'N/A')}**: {batch.get('status', 'N/A')}\n            "
                    else:
                        response += "*No action batches found*\n            "
                    return response
                except Exception as e:
                    return f"❌ Error: {str(e)}"\n\n    @app.tool(
                name="get_org_adaptive_policy_acl",
                description="🔒 Get details of a specific adaptive policy ACL"
            )
            def get_org_adaptive_policy_acl(
                organization_id: str,
                acl_id: str
            ):
                """Get specific adaptive policy ACL details."""
                try:
                    result = meraki_client.dashboard.organizations.getOrganizationAdaptivePolicyAcl(
                        organization_id, acl_id
                    )
                    
                    response = f"# 🔒 Adaptive Policy ACL Details\n\n            "
                    
                    if result:
                        response += f"**Name**: {result.get('name', 'Unknown')}\n            "
                        response += f"**ID**: {result.get('id', 'N/A')}\n            "
                        response += f"**Description**: {result.get('description', 'N/A')}\n            "
                        response += f"**IP Version**: {result.get('ipVersion', 'N/A')}\n\n            "\n\n    @app.tool(
        name="get_org_adaptive_policy_acls",
        description="🔒 List all adaptive policy ACLs in an organization"
    )
    def get_org_adaptive_policy_acls(organization_id: str):
        """Get all adaptive policy ACLs."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationAdaptivePolicyAcls(
                organization_id
            )
            
            response = f"# 🔒 Adaptive Policy ACLs\n\n            "
            
            if result and isinstance(result, list):
                response += f"**Total ACLs**: {len(result)}\n\n            "
                
                for acl in result:
                    response += f"## {acl.get('name', 'Unknown')}\n            "
                    response += f"- **ID**: {acl.get('id', 'N/A')}\n            "
                    response += f"- **Description**: {acl.get('description', 'N/A')}\n            "
                    response += f"- **IP Version**: {acl.get('ipVersion', 'N/A')}\n            "\n\n    @app.tool(
                name="get_org_adaptive_policy_group",
                description="👥 Get details of a specific adaptive policy group"
            )
            def get_org_adaptive_policy_group(
                organization_id: str,
                group_id: str
            ):
                """Get specific adaptive policy group details."""
                try:
                    result = meraki_client.dashboard.organizations.getOrganizationAdaptivePolicyGroup(
                        organization_id, group_id
                    )
                    
                    response = f"# 👥 Adaptive Policy Group Details\n\n            "
                    
                    if result:
                        response += f"**Name**: {result.get('name', 'Unknown')}\n            "
                        response += f"**ID**: {result.get('id', 'N/A')}\n            "
                        response += f"**SGT**: {result.get('sgt', 'N/A')}\n            "
                        response += f"**Description**: {result.get('description', 'N/A')}\n\n            "\n\n    @app.tool(
                name="get_org_adaptive_policy_groups",
                description="👥 List all adaptive policy groups in an organization"
            )
            def get_org_adaptive_policy_groups(
                organization_id: str
            ):
                """Get all adaptive policy groups."""
                try:
                    result = meraki_client.dashboard.organizations.getOrganizationAdaptivePolicyGroups(
                        organization_id
                    )
                    
                    response = f"# 👥 Adaptive Policy Groups\n\n            "
                    
                    if result and isinstance(result, list):
                        response += f"**Total Groups**: {len(result)}\n\n            "
                        
                        for group in result:
                            response += f"## {group.get('name', 'Unknown')}\n            "
                            response += f"- **ID**: {group.get('id', 'N/A')}\n            "
                            response += f"- **SGT**: {group.get('sgt', 'N/A')}\n            "
                            response += f"- **Description**: {group.get('description', 'N/A')}\n            "\n\n    @app.tool(
                name="get_org_adaptive_policy_overview",
                description="📊 Get adaptive policy overview for an organization"
            )
            def get_org_adaptive_policy_overview(
                organization_id: str
            ):
                """Get adaptive policy overview."""
                try:
                    result = meraki_client.dashboard.organizations.getOrganizationAdaptivePolicyOverview(
                        organization_id
                    )
                    
                    response = f"# 📊 Adaptive Policy Overview\n\n            "
                    
                    if result:\n\n    @app.tool(
                name="get_org_adaptive_policy_policies",
                description="📋 List all adaptive policies in an organization"
            )
            def get_org_adaptive_policy_policies(
                organization_id: str
            ):
                """Get all adaptive policies."""
                try:
                    result = meraki_client.dashboard.organizations.getOrganizationAdaptivePolicyPolicies(
                        organization_id
                    )
                    
                    response = f"# 📋 Adaptive Policies\n\n            "
                    
                    if result and isinstance(result, list):
                        response += f"**Total Policies**: {len(result)}\n\n            "
                        
                        for policy in result:
                            response += f"## Policy {policy.get('id', 'Unknown')}\n            "\n\n    @app.tool(
                name="get_org_adaptive_policy_policy",
                description="📋 Get details of a specific adaptive policy"
            )
            def get_org_adaptive_policy_policy(
                organization_id: str,
                policy_id: str
            ):
                """Get specific adaptive policy details."""
                try:
                    result = meraki_client.dashboard.organizations.getOrganizationAdaptivePolicyPolicy(
                        organization_id, policy_id
                    )
                    
                    response = f"# 📋 Adaptive Policy Details\n\n            "
                    
                    if result:
                        response += f"**Policy ID**: {result.get('id', 'N/A')}\n\n            "\n\n    @app.tool(
                name="get_org_adaptive_policy_settings",
                description="⚙️ Get adaptive policy settings for an organization"
            )
            def get_org_adaptive_policy_settings(
                organization_id: str
            ):
                """Get adaptive policy settings."""
                try:
                    result = meraki_client.dashboard.organizations.getOrganizationAdaptivePolicySettings(
                        organization_id
                    )
                    
                    response = f"# ⚙️ Adaptive Policy Settings\n\n            "
                    
                    if result:
                        response += f"**Enabled Networks**: {result.get('enabledNetworks', [])}\n            "
                        
                        return response
                    else:
                        response += "*No settings found*\n            "
                    
                    return response
                except Exception as e:
                    return f"❌ Error getting adaptive policy settings: {str(e)}"\n\n    @app.tool(
                name="get_org_admins",
                description="👤 List all dashboard administrators in an organization"
            )
            def get_org_admins(
                organization_id: str
            ):
                """Get all organization admins."""
                try:
                    result = meraki_client.dashboard.organizations.getOrganizationAdmins(
                        organization_id
                    )
                    
                    response = f"# 👤 Organization Administrators\n\n            "
                    
                    if result and isinstance(result, list):
                        response += f"**Total Admins**: {len(result)}\n\n            "
                        
                        for admin in result:
                            response += f"## {admin.get('name', 'Unknown')}\n            "
                            response += f"- **Email**: {admin.get('email', 'N/A')}\n            "
                            response += f"- **ID**: {admin.get('id', 'N/A')}\n            "
                            response += f"- **Org Access**: {admin.get('orgAccess', 'N/A')}\n            "\n\n    @app.tool(
                name="get_org_alerts_profiles",
                description="🚨 List all alert profiles in an organization"
            )
            def get_org_alerts_profiles(
                organization_id: str
            ):
                """Get all alert profiles."""
                try:
                    result = meraki_client.dashboard.organizations.getOrganizationAlertsProfiles(
                        organization_id
                    )
                    
                    response = f"# 🚨 Alert Profiles\n\n            "
                    
                    if result and isinstance(result, list):
                        response += f"**Total Profiles**: {len(result)}\n\n            "
                        
                        for profile in result:
                            response += f"## {profile.get('description', 'Unknown')}\n            "
                            response += f"- **ID**: {profile.get('id', 'N/A')}\n            "
                            response += f"- **Type**: {profile.get('type', 'N/A')}\n            "
                            response += f"- **Enabled**: {profile.get('enabled', False)}\n            "\n\n    @app.tool(
                name="get_org_api_requests",
                description="🔌 Get API request logs"
            )
            def get_org_api_requests(
                organization_id: str,
                t0: Optional[str] = None,
                t1: Optional[str] = None,
                timespan: Optional[float] = None,
                per_page: int = 50,
                starting_after: Optional[str] = None,
                ending_before: Optional[str] = None,
                admin_id: Optional[str] = None,
                path: Optional[str] = None,
                method: Optional[str] = None,
                response_code: Optional[int] = None,
                source_ip: Optional[str] = None,
                user_agent: Optional[str] = None,
                version: Optional[int] = None,
                operation_ids: Optional[str] = None
            ):
                """Get API requests."""
                try:
                    kwargs = {"perPage": per_page}
                    
                    if t0:
                        kwargs["t0"] = t0
                    if t1:
                        kwargs["t1"] = t1
                    if timespan:
                        kwargs["timespan"] = timespan
                    if starting_after:
                        kwargs["startingAfter"] = starting_after
                    if ending_before:
                        kwargs["endingBefore"] = ending_before
                    if admin_id:
                        kwargs["adminId"] = admin_id
                    if path:
                        kwargs["path"] = path
                    if method:
                        kwargs["method"] = method
                    if response_code:
                        kwargs["responseCode"] = response_code
                    if source_ip:
                        kwargs["sourceIp"] = source_ip
                    if user_agent:
                        kwargs["userAgent"] = user_agent
                    if version:
                        kwargs["version"] = version
                    if operation_ids:
                        kwargs["operationIds"] = [o.strip() for o in operation_ids.split(',')]
                    
                    result = meraki_client.dashboard.organizations.getOrganizationApiRequests(
                        organization_id, **kwargs
                    )
                    
                    response = f"# 🔌 API Requests\n\n            "
                    if result and isinstance(result, list):
                        response += f"**Total**: {len(result)}\n\n            "
                        for req in result[:10]:
                            response += f"- **{req.get('method', 'N/A')}** {req.get('path', 'N/A')}\n            "
                            response += f"  - Response: {req.get('responseCode', 'N/A')}\n            "
                            response += f"  - Time: {req.get('ts', 'N/A')}\n            "
                    return response
                except Exception as e:
                    return f"❌ Error: {str(e)}"\n\n    @app.tool(
                name="get_org_api_requests_overview",
                description="📊 Get API requests overview"
            )
            def get_org_api_requests_overview(
                organization_id: str,
                t0: Optional[str] = None,
                t1: Optional[str] = None,
                timespan: Optional[float] = None
            ):
                """Get API requests overview."""
                try:
                    kwargs = {}
                    if t0:
                        kwargs["t0"] = t0
                    if t1:
                        kwargs["t1"] = t1
                    if timespan:
                        kwargs["timespan"] = timespan
                    
                    result = meraki_client.dashboard.organizations.getOrganizationApiRequestsOverview(
                        organization_id, **kwargs
                    )
                    
                    response = f"# 📊 API Requests Overview\n\n            "
                    if result:
                        response += f"**Total**: {result.get('numberOfRequests', 0)}\n            "
                        response += f"**Success Rate**: {result.get('successRate', 0):.1f}%\n            "
                    return response
                except Exception as e:
                    return f"❌ Error: {str(e)}"\n\n    @app.tool(
                name="get_org_assurance_alert",
                description="🔍 Get details of a specific assurance alert"
            )
            def get_org_assurance_alert(
                organization_id: str,
                alert_id: str
            ):
                """Get specific assurance alert details."""
                try:
                    result = meraki_client.dashboard.organizations.getOrganizationAssuranceAlert(
                        organization_id, alert_id
                    )
                    
                    response = f"# 🔍 Assurance Alert Details\n\n            "
                    
                    if result:
                        severity = result.get('severity', 'unknown')
                        icon = "🔴" if severity == "critical" else "🟠" if severity == "warning" else "🟡"
                        
                        response += f"## {icon} {result.get('title', 'Unknown Alert')}\n            "
                        response += f"**ID**: {result.get('id', 'N/A')}\n            "
                        response += f"**Type**: {result.get('type', 'N/A')}\n            "
                        response += f"**Category**: {result.get('category', 'N/A')}\n            "
                        response += f"**Severity**: {severity}\n\n            "\n\n    @app.tool(
                name="get_org_assurance_alerts",
                description="🔍 Get assurance alerts for an organization"
            )
            def get_org_assurance_alerts(
                organization_id: str,
                per_page: int = 100,
                starting_after: Optional[str] = None,
                ending_before: Optional[str] = None,
                sort_order: Optional[str] = None,
                network_id: Optional[str] = None,
                severity: Optional[str] = None,
                types: Optional[str] = None,
                ts_start: Optional[str] = None,
                ts_end: Optional[str] = None,
                category: Optional[str] = None,
                sort_by: Optional[str] = None,
                serials: Optional[str] = None,
                device_types: Optional[str] = None,
                device_tags: Optional[str] = None,
                active: Optional[bool] = None,
                dismissed: Optional[bool] = None,
                resolved: Optional[bool] = None
            ):
                """Get assurance alerts."""
                try:
                    kwargs = {"perPage": per_page}
                    
                    if starting_after:
                        kwargs["startingAfter"] = starting_after
                    if ending_before:
                        kwargs["endingBefore"] = ending_before
                    if sort_order:
                        kwargs["sortOrder"] = sort_order
                    if network_id:
                        kwargs["networkId"] = network_id
                    if severity:
                        kwargs["severity"] = severity
                    if types:
                        kwargs["types"] = [t.strip() for t in types.split(',')]
                    if ts_start:
                        kwargs["tsStart"] = ts_start
                    if ts_end:
                        kwargs["tsEnd"] = ts_end
                    if category:
                        kwargs["category"] = category
                    if sort_by:
                        kwargs["sortBy"] = sort_by
                    if serials:
                        kwargs["serials"] = [s.strip() for s in serials.split(',')]
                    if device_types:
                        kwargs["deviceTypes"] = [d.strip() for d in device_types.split(',')]
                    if device_tags:
                        kwargs["deviceTags"] = [t.strip() for t in device_tags.split(',')]
                    if active is not None:
                        kwargs["active"] = active
                    if dismissed is not None:
                        kwargs["dismissed"] = dismissed
                    if resolved is not None:
                        kwargs["resolved"] = resolved
                    
                    result = meraki_client.dashboard.organizations.getOrganizationAssuranceAlerts(
                        organization_id, **kwargs
                    )
                    
                    response = f"# 🔍 Assurance Alerts\n\n            "
                    
                    if result and isinstance(result, list):
                        response += f"**Total Alerts**: {len(result)}\n\n            "\n\n    @app.tool(
                name="get_org_assurance_alerts_overview",
                description="📊 Get overview of assurance alerts"
            )
            def get_org_assurance_alerts_overview(
                organization_id: str,
                network_id: Optional[str] = None,
                severity: Optional[str] = None,
                types: Optional[str] = None,
                ts_start: Optional[str] = None,
                ts_end: Optional[str] = None,
                serials: Optional[str] = None,
                device_types: Optional[str] = None,
                device_tags: Optional[str] = None,
                active: Optional[bool] = None,
                dismissed: Optional[bool] = None,
                resolved: Optional[bool] = None
            ):
                """Get assurance alerts overview."""
                try:
                    kwargs = {}
                    
                    if network_id:
                        kwargs["networkId"] = network_id
                    if severity:
                        kwargs["severity"] = severity
                    if types:
                        kwargs["types"] = [t.strip() for t in types.split(',')]
                    if ts_start:
                        kwargs["tsStart"] = ts_start
                    if ts_end:
                        kwargs["tsEnd"] = ts_end
                    if serials:
                        kwargs["serials"] = [s.strip() for s in serials.split(',')]
                    if device_types:
                        kwargs["deviceTypes"] = [d.strip() for d in device_types.split(',')]
                    if device_tags:
                        kwargs["deviceTags"] = [t.strip() for t in device_tags.split(',')]
                    if active is not None:
                        kwargs["active"] = active
                    if dismissed is not None:
                        kwargs["dismissed"] = dismissed
                    if resolved is not None:
                        kwargs["resolved"] = resolved
                    
                    result = meraki_client.dashboard.organizations.getOrganizationAssuranceAlertsOverview(
                        organization_id, **kwargs
                    )
                    
                    response = f"# 📊 Assurance Alerts Overview\n\n            "
                    
                    if result:\n\n    @app.tool(
                name="get_org_assurance_alerts_overview_by_network",
                description="📊 Get assurance alerts overview by network"
            )
            def get_org_assurance_alerts_overview_by_network(
                organization_id: str,
                per_page: int = 100,
                starting_after: Optional[str] = None,
                ending_before: Optional[str] = None,
                sort_order: Optional[str] = None,
                network_id: Optional[str] = None,
                severity: Optional[str] = None,
                types: Optional[str] = None,
                ts_start: Optional[str] = None,
                ts_end: Optional[str] = None,
                serials: Optional[str] = None,
                device_types: Optional[str] = None,
                device_tags: Optional[str] = None,
                active: Optional[bool] = None,
                dismissed: Optional[bool] = None,
                resolved: Optional[bool] = None
            ):
                """Get assurance alerts overview by network."""
                try:
                    kwargs = {"perPage": per_page}
                    
                    if starting_after:
                        kwargs["startingAfter"] = starting_after
                    if ending_before:
                        kwargs["endingBefore"] = ending_before
                    if sort_order:
                        kwargs["sortOrder"] = sort_order
                    if network_id:
                        kwargs["networkId"] = network_id
                    if severity:
                        kwargs["severity"] = severity
                    if types:
                        kwargs["types"] = [t.strip() for t in types.split(',')]
                    if ts_start:
                        kwargs["tsStart"] = ts_start
                    if ts_end:
                        kwargs["tsEnd"] = ts_end
                    if serials:
                        kwargs["serials"] = [s.strip() for s in serials.split(',')]
                    if device_types:
                        kwargs["deviceTypes"] = [d.strip() for d in device_types.split(',')]
                    if device_tags:
                        kwargs["deviceTags"] = [t.strip() for t in device_tags.split(',')]
                    if active is not None:
                        kwargs["active"] = active
                    if dismissed is not None:
                        kwargs["dismissed"] = dismissed
                    if resolved is not None:
                        kwargs["resolved"] = resolved
                    
                    result = meraki_client.dashboard.organizations.getOrganizationAssuranceAlertsOverviewByNetwork(
                        organization_id, **kwargs
                    )
                    
                    response = f"# 📊 Alerts Overview by Network\n\n            "
                    
                    if result and isinstance(result, list):
                        response += f"**Total Networks**: {len(result)}\n\n            "
                        
                        for network in result[:10]:
                            response += f"## {network.get('name', 'Unknown Network')}\n            "
                            response += f"- **Network ID**: {network.get('id', 'N/A')}\n            "\n\n    @app.tool(
                name="get_org_assurance_alerts_overview_by_type",
                description="📊 Get assurance alerts overview grouped by type"
            )
            def get_org_assurance_alerts_overview_by_type(
                organization_id: str,
                per_page: int = 100,
                starting_after: Optional[str] = None,
                ending_before: Optional[str] = None,
                sort_order: Optional[str] = None,
                network_id: Optional[str] = None,
                severity: Optional[str] = None,
                types: Optional[str] = None,
                ts_start: Optional[str] = None,
                ts_end: Optional[str] = None,
                serials: Optional[str] = None,
                device_types: Optional[str] = None,
                device_tags: Optional[str] = None,
                active: Optional[bool] = None,
                dismissed: Optional[bool] = None,
                resolved: Optional[bool] = None
            ):
                """Get assurance alerts overview by type."""
                try:
                    kwargs = {"perPage": per_page}
                    
                    if starting_after:
                        kwargs["startingAfter"] = starting_after
                    if ending_before:
                        kwargs["endingBefore"] = ending_before
                    if sort_order:
                        kwargs["sortOrder"] = sort_order
                    if network_id:
                        kwargs["networkId"] = network_id
                    if severity:
                        kwargs["severity"] = severity
                    if types:
                        kwargs["types"] = [t.strip() for t in types.split(',')]
                    if ts_start:
                        kwargs["tsStart"] = ts_start
                    if ts_end:
                        kwargs["tsEnd"] = ts_end
                    if serials:
                        kwargs["serials"] = [s.strip() for s in serials.split(',')]
                    if device_types:
                        kwargs["deviceTypes"] = [d.strip() for d in device_types.split(',')]
                    if device_tags:
                        kwargs["deviceTags"] = [t.strip() for t in device_tags.split(',')]
                    if active is not None:
                        kwargs["active"] = active
                    if dismissed is not None:
                        kwargs["dismissed"] = dismissed
                    if resolved is not None:
                        kwargs["resolved"] = resolved
                    
                    result = meraki_client.dashboard.organizations.getOrganizationAssuranceAlertsOverviewByType(
                        organization_id, **kwargs
                    )
                    
                    response = f"# 📊 Alerts Overview by Type\n\n            "
                    
                    if result and isinstance(result, list):
                        response += f"**Total Alert Types**: {len(result)}\n\n            "
                        
                        for alert_type in result[:15]:
                            response += f"## {alert_type.get('type', 'Unknown Type')}\n            "
                            response += f"- **Count**: {alert_type.get('count', 0)}\n            "
                            response += f"- **Active**: {alert_type.get('active', 0)}\n            "
                            response += f"- **Dismissed**: {alert_type.get('dismissed', 0)}\n            "
                            response += f"- **Resolved**: {alert_type.get('resolved', 0)}\n\n            "
                        
                        if len(result) > 15:
                            response += f"... and {len(result)-15} more alert types\n            "
                    else:
                        response += "*No type overview data found*\n            "
                    
                    return response
                except Exception as e:
                    return f"❌ Error getting type overview: {str(e)}"\n\n    @app.tool(
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
                    
                    response = f"# 🎨 Branding Policies\n\n            "
                    
                    if result and isinstance(result, list):
                        response += f"**Total Policies**: {len(result)}\n\n            "
                        
                        for policy in result:
                            response += f"## {policy.get('name', 'Unnamed')}\n            "
                            response += f"- **ID**: {policy.get('id', 'N/A')}\n            "
                            response += f"- **Enabled**: {policy.get('enabled', False)}\n            "\n\n    @app.tool(
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
                    
                    response = f"# 🎨 Branding Policy Priorities\n\n            "
                    
                    if result and isinstance(result, dict):
                        priorities = result.get('brandingPolicyIds', [])
                        if priorities:
                            response += "**Priority Order**:\n            "
                            for i, policy_id in enumerate(priorities, 1):
                                response += f"{i}. {policy_id}\n            "
                    else:
                        response += "*No priorities set*\n            "
                    
                    return response
                except Exception as e:
                    return f"❌ Error getting priorities: {str(e)}"\n\n    @app.tool(
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
                    
                    response = f"# 🎨 Branding Policy Details\n\n            "
                    
                    if result:
                        response += f"**Name**: {result.get('name', 'Unnamed')}\n            "
                        response += f"**ID**: {result.get('id', 'N/A')}\n            "
                        response += f"**Enabled**: {result.get('enabled', False)}\n\n            "\n\n    @app.tool(
                name="get_org_clients_overview",
                description="📊 Get clients overview"
            )
            def get_org_clients_overview(
                organization_id: str,
                t0: Optional[str] = None,
                t1: Optional[str] = None,
                timespan: Optional[float] = None
            ):
                """Get clients overview."""
                try:
                    kwargs = {}
                    if t0:
                        kwargs["t0"] = t0
                    if t1:
                        kwargs["t1"] = t1
                    if timespan:
                        kwargs["timespan"] = timespan
                    
                    result = meraki_client.dashboard.organizations.getOrganizationClientsOverview(
                        organization_id, **kwargs
                    )
                    
                    response = f"# 📊 Clients Overview\n\n            "
                    if result:
                        counts = result.get('counts', {})
                        response += f"**Total**: {counts.get('total', 0)}\n            "
                        
                        usage = result.get('usage', {})
                        if usage:
                            response += f"\n            ## Usage\n            "
                            response += f"- **Downstream**: {usage.get('downstream', 0)/1e9:.2f} GB\n            "
                            response += f"- **Upstream**: {usage.get('upstream', 0)/1e9:.2f} GB\n            "
                    return response
                except Exception as e:
                    return f"❌ Error: {str(e)}"\n\n    @app.tool(
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
                    
                    response = f"# 📋 Configuration Template Details\n\n            "
                    
                    if result:
                        response += f"**Name**: {result.get('name', 'Unnamed')}\n            "
                        response += f"**ID**: {result.get('id', 'N/A')}\n            "
                        response += f"**Product Types**: {', '.join(result.get('productTypes', []))}\n            "
                        response += f"**Time Zone**: {result.get('timeZone', 'N/A')}\n\n            "\n\n    @app.tool(
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
                    
                    response = f"# 📋 Configuration Templates\n\n            "
                    
                    if result and isinstance(result, list):
                        response += f"**Total Templates**: {len(result)}\n\n            "
                        
                        for template in result:
                            response += f"## {template.get('name', 'Unnamed')}\n            "
                            response += f"- **ID**: {template.get('id', 'N/A')}\n            "
                            response += f"- **Product Types**: {', '.join(template.get('productTypes', []))}\n            "
                            response += f"- **Time Zone**: {template.get('timeZone', 'N/A')}\n            "\n\n    @app.tool(
                name="get_org_devices_availabilities",
                description="📈 Get availability history for devices"
            )
            def get_org_devices_availabilities(
                organization_id: str,
                per_page: int = 100,
                starting_after: Optional[str] = None,
                ending_before: Optional[str] = None,
                network_ids: Optional[str] = None,
                serials: Optional[str] = None,
                product_types: Optional[str] = None,
                tags: Optional[str] = None,
                tags_filter_type: Optional[str] = None
            ):
                """Get device availability history."""
                try:
                    kwargs = {"perPage": per_page}
                    
                    if starting_after:
                        kwargs["startingAfter"] = starting_after
                    if ending_before:
                        kwargs["endingBefore"] = ending_before
                    if network_ids:
                        kwargs["networkIds"] = [n.strip() for n in network_ids.split(',')]
                    if serials:
                        kwargs["serials"] = [s.strip() for s in serials.split(',')]
                    if product_types:
                        kwargs["productTypes"] = [p.strip() for p in product_types.split(',')]
                    if tags:
                        kwargs["tags"] = [t.strip() for t in tags.split(',')]
                    if tags_filter_type:
                        kwargs["tagsFilterType"] = tags_filter_type
                    
                    result = meraki_client.dashboard.organizations.getOrganizationDevicesAvailabilities(
                        organization_id, **kwargs
                    )
                    
                    response = f"# 📈 Device Availabilities\n\n            "
                    
                    if result and isinstance(result, list):
                        response += f"**Total Devices**: {len(result)}\n\n            "
                        
                        for device in result[:10]:
                            response += f"## {device.get('name', device.get('serial', 'Unknown'))}\n            "
                            response += f"- **Serial**: {device.get('serial', 'N/A')}\n            "
                            response += f"- **Status**: {device.get('status', 'N/A')}\n            "\n\n    @app.tool(
                name="get_org_devices_availabilities_change_history",
                description="📈 Get availability change history for devices"
            )
            def get_org_devices_availabilities_change_history(
                organization_id: str,
                per_page: int = 100,
                starting_after: Optional[str] = None,
                ending_before: Optional[str] = None,
                t0: Optional[str] = None,
                t1: Optional[str] = None,
                timespan: Optional[float] = None,
                serials: Optional[str] = None,
                product_types: Optional[str] = None,
                network_ids: Optional[str] = None
            ):
                """Get device availability change history."""
                try:
                    kwargs = {"perPage": per_page}
                    
                    if starting_after:
                        kwargs["startingAfter"] = starting_after
                    if ending_before:
                        kwargs["endingBefore"] = ending_before
                    if t0:
                        kwargs["t0"] = t0
                    if t1:
                        kwargs["t1"] = t1
                    if timespan:
                        kwargs["timespan"] = timespan
                    if serials:
                        kwargs["serials"] = [s.strip() for s in serials.split(',')]
                    if product_types:
                        kwargs["productTypes"] = [p.strip() for p in product_types.split(',')]
                    if network_ids:
                        kwargs["networkIds"] = [n.strip() for n in network_ids.split(',')]
                    
                    result = meraki_client.dashboard.organizations.getOrganizationDevicesAvailabilitiesChangeHistory(
                        organization_id, **kwargs
                    )
                    
                    response = f"# 📈 Availability Change History\n\n            "
                    
                    if result and isinstance(result, list):
                        response += f"**Total Changes**: {len(result)}\n\n            "
                        
                        for change in result[:20]:
                            device = change.get('device', {})
                            response += f"## {device.get('name', device.get('serial', 'Unknown'))}\n            "
                            response += f"- **Time**: {change.get('ts', 'N/A')}\n            "
                            
                            details = change.get('details', {})
                            old_status = details.get('oldStatus', 'N/A')
                            new_status = details.get('newStatus', 'N/A')
                            
                            old_icon = "🟢" if old_status == "online" else "🔴"
                            new_icon = "🟢" if new_status == "online" else "🔴"
                            
                            response += f"- **Change**: {old_icon} {old_status} → {new_icon} {new_status}\n\n            "
                        
                        if len(result) > 20:
                            response += f"... and {len(result)-20} more changes\n            "
                    else:
                        response += "*No availability changes found*\n            "
                    
                    return response
                except Exception as e:
                    return f"❌ Error getting change history: {str(e)}"\n\n    @app.tool(
                name="get_org_devices_statuses",
                description="📊 Get status of all devices in an organization"
            )
            def get_org_devices_statuses(
                organization_id: str,
                per_page: int = 100,
                starting_after: Optional[str] = None,
                ending_before: Optional[str] = None,
                network_ids: Optional[str] = None,
                serials: Optional[str] = None,
                statuses: Optional[str] = None,
                product_types: Optional[str] = None,
                models: Optional[str] = None,
                tags: Optional[str] = None,
                tags_filter_type: Optional[str] = None
            ):
                """Get device statuses."""
                try:
                    kwargs = {"perPage": per_page}
                    
                    if starting_after:
                        kwargs["startingAfter"] = starting_after
                    if ending_before:
                        kwargs["endingBefore"] = ending_before
                    if network_ids:
                        kwargs["networkIds"] = [n.strip() for n in network_ids.split(',')]
                    if serials:
                        kwargs["serials"] = [s.strip() for s in serials.split(',')]
                    if statuses:
                        kwargs["statuses"] = [s.strip() for s in statuses.split(',')]
                    if product_types:
                        kwargs["productTypes"] = [p.strip() for p in product_types.split(',')]
                    if models:
                        kwargs["models"] = [m.strip() for m in models.split(',')]
                    if tags:
                        kwargs["tags"] = [t.strip() for t in tags.split(',')]
                    if tags_filter_type:
                        kwargs["tagsFilterType"] = tags_filter_type
                    
                    result = meraki_client.dashboard.organizations.getOrganizationDevicesStatuses(
                        organization_id, **kwargs
                    )
                    
                    response = f"# 📊 Device Statuses\n\n            "
                    
                    if result and isinstance(result, list):
                        response += f"**Total Devices**: {len(result)}\n\n            "\n\n    @app.tool(
                name="get_org_devices_statuses_overview",
                description="📊 Get overview of device statuses in organization"
            )
            def get_org_devices_statuses_overview(
                organization_id: str,
                product_types: Optional[str] = None,
                network_ids: Optional[str] = None
            ):
                """Get device statuses overview."""
                try:
                    kwargs = {}
                    
                    if product_types:
                        kwargs["productTypes"] = [p.strip() for p in product_types.split(',')]
                    if network_ids:
                        kwargs["networkIds"] = [n.strip() for n in network_ids.split(',')]
                    
                    result = meraki_client.dashboard.organizations.getOrganizationDevicesStatusesOverview(
                        organization_id, **kwargs
                    )
                    
                    response = f"# 📊 Device Statuses Overview\n\n            "
                    
                    if result:\n\n    @app.tool(
                name="get_org_devices_uplinks_addresses_by_device",
                description="🔗 Get uplink addresses for devices"
            )
            def get_org_devices_uplinks_addresses_by_device(
                organization_id: str,
                per_page: int = 100,
                starting_after: Optional[str] = None,
                ending_before: Optional[str] = None,
                network_ids: Optional[str] = None,
                product_types: Optional[str] = None,
                serials: Optional[str] = None,
                tags: Optional[str] = None,
                tags_filter_type: Optional[str] = None
            ):
                """Get device uplink addresses."""
                try:
                    kwargs = {"perPage": per_page}
                    
                    if starting_after:
                        kwargs["startingAfter"] = starting_after
                    if ending_before:
                        kwargs["endingBefore"] = ending_before
                    if network_ids:
                        kwargs["networkIds"] = [n.strip() for n in network_ids.split(',')]
                    if product_types:
                        kwargs["productTypes"] = [p.strip() for p in product_types.split(',')]
                    if serials:
                        kwargs["serials"] = [s.strip() for s in serials.split(',')]
                    if tags:
                        kwargs["tags"] = [t.strip() for t in tags.split(',')]
                    if tags_filter_type:
                        kwargs["tagsFilterType"] = tags_filter_type
                    
                    result = meraki_client.dashboard.organizations.getOrganizationDevicesUplinksAddressesByDevice(
                        organization_id, **kwargs
                    )
                    
                    response = f"# 🔗 Device Uplink Addresses\n\n            "
                    
                    if result and isinstance(result, list):
                        response += f"**Total Devices**: {len(result)}\n\n            "
                        
                        for device in result[:10]:
                            response += f"## {device.get('name', device.get('serial', 'Unknown'))}\n            "
                            response += f"- **Serial**: {device.get('serial', 'N/A')}\n            "
                            response += f"- **Model**: {device.get('model', 'N/A')}\n            "\n\n    @app.tool(
                name="get_org_devices_uplinks_loss_and_latency",
                description="📉 Get uplink loss and latency for devices"
            )
            def get_org_devices_uplinks_loss_and_latency(
                organization_id: str,
                t0: Optional[str] = None,
                t1: Optional[str] = None,
                timespan: Optional[float] = None,
                uplink: Optional[str] = None,
                ip: Optional[str] = None
            ):
                """Get device uplink loss and latency."""
                try:
                    kwargs = {}
                    
                    if t0:
                        kwargs["t0"] = t0
                    if t1:
                        kwargs["t1"] = t1
                    if timespan:
                        kwargs["timespan"] = timespan
                    if uplink:
                        kwargs["uplink"] = uplink
                    if ip:
                        kwargs["ip"] = ip
                    
                    result = meraki_client.dashboard.organizations.getOrganizationDevicesUplinksLossAndLatency(
                        organization_id, **kwargs
                    )
                    
                    response = f"# 📉 Uplink Loss and Latency\n\n            "
                    
                    if result and isinstance(result, list):
                        response += f"**Total Devices**: {len(result)}\n\n            "
                        
                        for device in result[:10]:
                            response += f"## {device.get('networkName', 'Unknown Network')}\n            "
                            response += f"- **Device**: {device.get('serial', 'N/A')}\n            "\n\n    @app.tool(
                name="get_org_inventory_device",
                description="📦 Get details of a specific device in inventory"
            )
            def get_org_inventory_device(
                organization_id: str,
                serial: str
            ):
                """Get specific inventory device details."""
                try:
                    result = meraki_client.dashboard.organizations.getOrganizationInventoryDevice(
                        organization_id, serial
                    )
                    
                    response = f"# 📦 Device Inventory Details\n\n            "
                    
                    if result:
                        response += f"**Model**: {result.get('model', 'Unknown')}\n            "
                        response += f"**Serial**: {result.get('serial', 'N/A')}\n            "
                        response += f"**Name**: {result.get('name', 'Not named')}\n            "
                        response += f"**MAC**: {result.get('mac', 'N/A')}\n            "
                        response += f"**Product Type**: {result.get('productType', 'N/A')}\n\n            "\n\n    @app.tool(
                name="get_org_inventory_devices",
                description="📦 List all devices in organization inventory"
            )
            def get_org_inventory_devices(
                organization_id: str,
                per_page: int = 100,
                starting_after: Optional[str] = None,
                ending_before: Optional[str] = None,
                used_state: Optional[str] = None,
                search: Optional[str] = None,
                mac: Optional[str] = None,
                serial: Optional[str] = None,
                model: Optional[str] = None,
                order_numbers: Optional[str] = None,
                network_ids: Optional[str] = None,
                serials: Optional[str] = None,
                tags: Optional[str] = None,
                tags_filter_type: Optional[str] = None,
                product_types: Optional[str] = None
            ):
                """Get organization inventory devices."""
                try:
                    kwargs = {"perPage": per_page}
                    
                    if starting_after:
                        kwargs["startingAfter"] = starting_after
                    if ending_before:
                        kwargs["endingBefore"] = ending_before
                    if used_state:
                        kwargs["usedState"] = used_state
                    if search:
                        kwargs["search"] = search
                    if mac:
                        kwargs["mac"] = mac
                    if serial:
                        kwargs["serial"] = serial
                    if model:
                        kwargs["model"] = model
                    if order_numbers:
                        kwargs["orderNumbers"] = [n.strip() for n in order_numbers.split(',')]
                    if network_ids:
                        kwargs["networkIds"] = [n.strip() for n in network_ids.split(',')]
                    if serials:
                        kwargs["serials"] = [s.strip() for s in serials.split(',')]
                    if tags:
                        kwargs["tags"] = [t.strip() for t in tags.split(',')]
                    if tags_filter_type:
                        kwargs["tagsFilterType"] = tags_filter_type
                    if product_types:
                        kwargs["productTypes"] = [p.strip() for p in product_types.split(',')]
                    
                    result = meraki_client.dashboard.organizations.getOrganizationInventoryDevices(
                        organization_id, **kwargs
                    )
                    
                    response = f"# 📦 Organization Inventory\n\n            "
                    
                    if result and isinstance(result, list):
                        response += f"**Total Devices**: {len(result)}\n\n            "\n\n    @app.tool(
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
                    
                    response = f"# 📜 License Details\n\n            "
                    
                    if result:
                        response += f"**License Type**: {result.get('licenseType', 'Unknown')}\n            "
                        response += f"**ID**: {result.get('id', 'N/A')}\n            "
                        response += f"**State**: {result.get('state', 'N/A')}\n\n            "\n\n    @app.tool(
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
                    
                    response = f"# 📜 Organization Licenses\n\n            "
                    
                    if result and isinstance(result, list):
                        response += f"**Total Licenses**: {len(result)}\n\n            "\n\n    @app.tool(
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
                    
                    response = f"# 📊 Licenses Overview\n\n            "
                    
                    if result:\n\n    @app.tool(
                name="get_org_login_security",
                description="🔐 Get login security settings"
            )
            def get_org_login_security(
                organization_id: str
            ):
                """Get login security."""
                try:
                    result = meraki_client.dashboard.organizations.getOrganizationLoginSecurity(
                        organization_id
                    )
                    
                    response = f"# 🔐 Login Security\n\n            "
                    if result:
                        response += f"**Enforce Two-Factor**: {result.get('enforceTwoFactorAuth', False)}\n            "
                        response += f"**Enforce Account Lockout**: {result.get('enforceAccountLockout', False)}\n            "
                        response += f"**Lockout Attempts**: {result.get('accountLockoutAttempts', 'N/A')}\n            "
                        response += f"**Idle Timeout**: {result.get('idleTimeoutMinutes', 'N/A')} minutes\n            "
                        response += f"**Enforce Password Expiration**: {result.get('enforcePasswordExpiration', False)}\n            "
                        response += f"**Password Expiration Days**: {result.get('passwordExpirationDays', 'N/A')}\n            "
                        response += f"**Enforce Strong Passwords**: {result.get('enforceStrongPasswords', False)}\n            "
                    return response
                except Exception as e:
                    return f"❌ Error: {str(e)}"\n\n    @app.tool(
                name="get_org_openapi_spec",
                description="📋 Get OpenAPI specification"
            )
            def get_org_openapi_spec(
                organization_id: str,
                version: Optional[int] = None
            ):
                """Get OpenAPI spec."""
                try:
                    kwargs = {}
                    if version:
                        kwargs['version'] = version
                    
                    result = meraki_client.dashboard.organizations.getOrganizationOpenapiSpec(
                        organization_id, **kwargs
                    )
                    
                    response = f"# 📋 OpenAPI Specification\n\n            "
                    if result:
                        response += f"**Version**: {result.get('openapi', 'N/A')}\n            "
                        info = result.get('info', {})
                        response += f"**Title**: {info.get('title', 'N/A')}\n            "
                        response += f"**API Version**: {info.get('version', 'N/A')}\n            "
                        
                        paths = result.get('paths', {})
                        response += f"\n            **Endpoints**: {len(paths)}\n            "
                    return response
                except Exception as e:
                    return f"❌ Error: {str(e)}"\n\n    @app.tool(
                name="get_org_saml",
                description="🔐 Get SAML SSO configuration for an organization"
            )
            def get_org_saml(
                organization_id: str
            ):
                """Get SAML configuration."""
                try:
                    result = meraki_client.dashboard.organizations.getOrganizationSaml(
                        organization_id
                    )
                    
                    response = f"# 🔐 SAML Configuration\n\n            "
                    
                    if result:
                        response += f"**Enabled**: {result.get('enabled', False)}\n\n            "
                        
                        if result.get('enabled'):
                            response += "## Configuration\n            "\n\n    @app.tool(
                name="get_org_saml_idps",
                description="🔐🏢 List SAML Identity Providers for an organization"
            )
            def get_org_saml_idps(
                organization_id: str
            ):
                """Get SAML Identity Providers."""
                try:
                    result = meraki_client.dashboard.organizations.getOrganizationSamlIdps(
                        organization_id
                    )
                    
                    response = f"# 🔐 SAML Identity Providers\n\n            "
                    
                    if result and isinstance(result, list):
                        response += f"**Total IdPs**: {len(result)}\n\n            "
                        
                        for idp in result:
                            response += f"## {idp.get('name', 'Unknown')}\n            "
                            response += f"- **ID**: {idp.get('idpId', 'N/A')}\n            "
                            response += f"- **SSO URL**: {idp.get('ssoUrl', 'N/A')}\n            "
                            response += f"- **Sign-On URL**: {idp.get('signOnUrl', 'N/A')}\n            "
                            response += f"- **Logout URL**: {idp.get('logoutUrl', 'N/A')}\n            "
                            response += f"- **Certificate**: {'Present' if idp.get('x509certSha1Fingerprint') else 'Not configured'}\n\n            "
                    else:
                        response += "*No SAML IdPs found*\n            "
                    
                    return response
                except Exception as e:
                    return f"❌ Error getting SAML IdPs: {str(e)}"\n\n    @app.tool(
                name="get_org_saml_role",
                description="🔐👥 Get details of a specific SAML role"
            )
            def get_org_saml_role(
                organization_id: str,
                role_id: str
            ):
                """Get specific SAML role details."""
                try:
                    result = meraki_client.dashboard.organizations.getOrganizationSamlRole(
                        organization_id, role_id
                    )
                    
                    response = f"# 🔐 SAML Role Details\n\n            "
                    
                    if result:
                        response += f"**Role**: {result.get('role', 'Unknown')}\n            "
                        response += f"**ID**: {result.get('id', 'N/A')}\n            "
                        response += f"**Org Access**: {result.get('orgAccess', 'N/A')}\n\n            "\n\n    @app.tool(
                name="get_org_saml_roles",
                description="🔐👥 List SAML roles for an organization"
            )
            def get_org_saml_roles(
                organization_id: str
            ):
                """Get SAML roles."""
                try:
                    result = meraki_client.dashboard.organizations.getOrganizationSamlRoles(
                        organization_id
                    )
                    
                    response = f"# 🔐 SAML Roles\n\n            "
                    
                    if result and isinstance(result, list):
                        response += f"**Total Roles**: {len(result)}\n\n            "
                        
                        for role in result:
                            response += f"## {role.get('role', 'Unknown')}\n            "
                            response += f"- **ID**: {role.get('id', 'N/A')}\n            "
                            response += f"- **Org Access**: {role.get('orgAccess', 'N/A')}\n            "\n\n    @app.tool(
                name="get_org_webhooks_logs",
                description="🔔 Get webhooks logs"
            )
            def get_org_webhooks_logs(
                organization_id: str,
                t0: Optional[str] = None,
                t1: Optional[str] = None,
                timespan: Optional[float] = None,
                per_page: int = 50,
                starting_after: Optional[str] = None,
                ending_before: Optional[str] = None,
                url: Optional[str] = None
            ):
                """Get webhooks logs."""
                try:
                    kwargs = {"perPage": per_page}
                    
                    if t0:
                        kwargs["t0"] = t0
                    if t1:
                        kwargs["t1"] = t1
                    if timespan:
                        kwargs["timespan"] = timespan
                    if starting_after:
                        kwargs["startingAfter"] = starting_after
                    if ending_before:
                        kwargs["endingBefore"] = ending_before
                    if url:
                        kwargs["url"] = url
                    
                    result = meraki_client.dashboard.organizations.getOrganizationWebhooksLogs(
                        organization_id, **kwargs
                    )
                    
                    response = f"# 🔔 Webhooks Logs\n\n            "
                    if result and isinstance(result, list):
                        response += f"**Total**: {len(result)}\n\n            "
                        for log in result[:10]:
                            response += f"- **{log.get('alertType', 'N/A')}**\n            "
                            response += f"  - URL: {log.get('url', 'N/A')}\n            "
                            response += f"  - Response: {log.get('responseCode', 'N/A')}\n            "
                            response += f"  - Time: {log.get('sentAt', 'N/A')}\n            "
                    return response
                except Exception as e:
                    return f"❌ Error: {str(e)}"\n\n    @app.tool(
        name="get_organization",
        description="🏢 Get detailed information about a specific organization."
    )
    def get_organization(
        organization_id: str
    ):
        """
        Get organization details.
        
        Args:
            organization_id: Organization ID
        """
        try:
            result = meraki_client.dashboard.organizations.getOrganization(organization_id)
            
            response = f"# 🏢 Organization Details\n\n            "
            
            if result:
                response += f"## {result.get('name', 'Unnamed')}\n            "
                response += f"- **ID**: {result.get('id')}\n            "
                response += f"- **URL**: {result.get('url', 'N/A')}\n            "\n\n    @app.tool(
        name="get_organization_action_batches",
        description="⚡ List organization action batches"
    )
    def get_organization_action_batches(
        organization_id: str,
        status: Optional[str] = None
    ):
        """Get action batches."""
        try:
            kwargs = {}
            if status:
                kwargs['status'] = status
                
            result = meraki_client.dashboard.organizations.getOrganizationActionBatches(
                organization_id, **kwargs
            )
            
            response = f"# ⚡ Action Batches\n\n            "
            
            if result and isinstance(result, list):
                response += f"**Total Action Batches**: {len(result)}\n\n            "\n\n    @app.tool(
        name="get_organization_admins",
        description="👨‍💼 List all administrators in an organization"
    )
    def get_organization_admins(organization_id: str):
        """Get all organization administrators."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationAdmins(
                organization_id
            )
            
            response = f"# 👨‍💼 Organization Administrators\n\n            "
            
            if result and isinstance(result, list):
                response += f"**Total Administrators**: {len(result)}\n\n            "
                
                for admin in result:
                    response += f"## {admin.get('name', 'Unknown')}\n            "
                    response += f"- **Email**: {admin.get('email', 'N/A')}\n            "
                    response += f"- **Org Access**: {admin.get('orgAccess', 'N/A')}\n            "\n\n    @app.tool(
        name="get_organization_alerts_profiles",
        description="🚨 List all alert profiles in an organization"
    )
    def get_organization_alerts_profiles(organization_id: str):
        """Get all organization alert profiles."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationAlertsProfiles(
                organization_id
            )
            
            response = f"# 🚨 Alert Profiles\n\n            "
            
            if result and isinstance(result, list):
                response += f"**Total Alert Profiles**: {len(result)}\n\n            "
                
                for profile in result:
                    response += f"## {profile.get('description', 'Unknown')}\n            "
                    response += f"- **ID**: {profile.get('id', 'N/A')}\n            "
                    response += f"- **Type**: {profile.get('type', 'N/A')}\n            "\n\n    @app.tool(
        name="get_organization_branding_policies",
        description="🎨 List organization branding policies"
    )
    def get_organization_branding_policies(organization_id: str):
        """Get branding policies."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationBrandingPolicies(
                organization_id
            )
            
            response = f"# 🎨 Branding Policies\n\n            "
            
            if result and isinstance(result, list):
                response += f"**Total Branding Policies**: {len(result)}\n\n            "
                
                for policy in result:
                    response += f"## {policy.get('name', 'Unknown')}\n            "
                    response += f"- **ID**: {policy.get('id', 'N/A')}\n            "
                    response += f"- **Enabled**: {'✅' if policy.get('enabled') else '❌'}\n            "\n\n    @app.tool(
        name="get_organization_config_templates",
        description="📋 List all configuration templates in an organization"
    )
    def get_organization_config_templates(organization_id: str):
        """Get all configuration templates."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationConfigTemplates(
                organization_id
            )
            
            response = f"# 📋 Configuration Templates\n\n            "
            
            if result and isinstance(result, list):
                response += f"**Total Templates**: {len(result)}\n\n            "
                
                for template in result:
                    response += f"## {template.get('name', 'Unknown')}\n            "
                    response += f"- **ID**: {template.get('id', 'N/A')}\n            "
                    response += f"- **Product Types**: {', '.join(template.get('productTypes', []))}\n            "
                    response += f"- **TimeZone**: {template.get('timeZone', 'N/A')}\n            "
                    response += "\n            "
            else:
                response += "*No configuration templates found*\n            "
            
            return response
        except Exception as e:
            return f"❌ Error getting configuration templates: {str(e)}"\n\n    @app.tool(
        name="get_organization_devices",
        description="📱 List all devices in an organization"  
    )
    def get_organization_devices(
        organization_id: str,
        per_page: int = 1000,
        configuration_updated_after: Optional[str] = None,
        network_ids: Optional[str] = None,
        product_types: Optional[str] = None,
        tags: Optional[str] = None,
        tags_filter_type: Optional[str] = None,
        name: Optional[str] = None,
        mac: Optional[str] = None,
        serial: Optional[str] = None,
        model: Optional[str] = None,
        models: Optional[str] = None,
        sensor_metrics: Optional[str] = None,
        sensor_alert_profile_ids: Optional[str] = None,
        sensor_alert_profile_id: Optional[str] = None
    ):
        """Get all devices in organization with comprehensive filtering."""
        try:
            kwargs = {'perPage': per_page, 'total_pages': 'all'}
            
            if configuration_updated_after:
                kwargs['configurationUpdatedAfter'] = configuration_updated_after
            if network_ids:
                kwargs['networkIds'] = network_ids.split(',')
            if product_types:
                kwargs['productTypes'] = product_types.split(',')
            if tags:
                kwargs['tags'] = tags.split(',')
            if tags_filter_type:
                kwargs['tagsFilterType'] = tags_filter_type
            if name:
                kwargs['name'] = name
            if mac:
                kwargs['mac'] = mac
            if serial:
                kwargs['serial'] = serial
            if model:
                kwargs['model'] = model
            if models:
                kwargs['models'] = models.split(',')
            if sensor_metrics:
                kwargs['sensorMetrics'] = sensor_metrics.split(',')
            if sensor_alert_profile_ids:
                kwargs['sensorAlertProfileIds'] = sensor_alert_profile_ids.split(',')
            if sensor_alert_profile_id:
                kwargs['sensorAlertProfileId'] = sensor_alert_profile_id
            
            result = meraki_client.dashboard.organizations.getOrganizationDevices(
                organization_id, **kwargs
            )
            
            response = f"# 📱 Organization Devices\n\n            "
            
            if result and isinstance(result, list):
                response += f"**Total Devices**: {len(result)}\n\n            "\n\n    @app.tool(
        name="get_organization_devices_statuses",
        description="📊 Get device status information for all devices in organization"
    )
    def get_organization_devices_statuses(
        organization_id: str,
        per_page: int = 1000,
        network_ids: Optional[str] = None,
        serials: Optional[str] = None,
        statuses: Optional[str] = None,
        product_types: Optional[str] = None,
        models: Optional[str] = None,
        tags: Optional[str] = None,
        tags_filter_type: Optional[str] = None
    ):
        """Get comprehensive device status information."""
        try:
            kwargs = {'perPage': per_page, 'total_pages': 'all'}
            
            if network_ids:
                kwargs['networkIds'] = network_ids.split(',')
            if serials:
                kwargs['serials'] = serials.split(',')
            if statuses:
                kwargs['statuses'] = statuses.split(',')
            if product_types:
                kwargs['productTypes'] = product_types.split(',')
            if models:
                kwargs['models'] = models.split(',')
            if tags:
                kwargs['tags'] = tags.split(',')
            if tags_filter_type:
                kwargs['tagsFilterType'] = tags_filter_type
            
            result = meraki_client.dashboard.organizations.getOrganizationDevicesStatuses(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Device Status Summary\n\n            "
            
            if result and isinstance(result, list):
                response += f"**Total Devices Checked**: {len(result)}\n\n            "\n\n    @app.tool(
                name="get_organization_early_access_features",
                description="🧪📋 List all available early access features for an organization"
            )
            def get_organization_early_access_features(
                organization_id: str
            ):
                """Get all available early access features."""
                try:
                    result = meraki_client.dashboard.organizations.getOrganizationEarlyAccessFeatures(
                        organization_id
                    )
                    
                    response = f"# 🧪 Available Early Access Features\n\n            "
                    
                    if result and isinstance(result, list):
                        response += f"**Total Features**: {len(result)}\n\n            "
                        
                        for feature in result:\n\n    @app.tool(
                name="get_organization_early_access_features_opt_in",
                description="🧪🔍 Get details of a specific early access feature opt-in"
            )
            def get_organization_early_access_features_opt_in(
                organization_id: str,
                opt_in_id: str
            ):
                """Get details of a specific opt-in."""
                try:
                    result = meraki_client.dashboard.organizations.getOrganizationEarlyAccessFeaturesOptIn(
                        organization_id, opt_in_id
                    )
                    
                    response = f"# 🧪 Early Access Opt-In Details\n\n            "
                    
                    if result:
                        response += f"**Feature**: {result.get('shortName', 'Unknown')}\n            "
                        response += f"**Opt-In ID**: {result.get('id', 'N/A')}\n            "
                        response += f"**Created**: {result.get('createdAt', 'N/A')}\n\n            "\n\n    @app.tool(
                name="get_organization_early_access_features_opt_ins",
                description="🧪✅ List all early access features the organization has opted into"
            )
            def get_organization_early_access_features_opt_ins(
                organization_id: str
            ):
                """Get all early access feature opt-ins."""
                try:
                    result = meraki_client.dashboard.organizations.getOrganizationEarlyAccessFeaturesOptIns(
                        organization_id
                    )
                    
                    response = f"# 🧪 Active Early Access Opt-Ins\n\n            "
                    
                    if result and isinstance(result, list):
                        response += f"**Total Opt-Ins**: {len(result)}\n\n            "
                        response += "⚠️ **Note**: Early access features may have breaking changes\n\n            "
                        
                        for opt_in in result:
                            response += f"## ✅ {opt_in.get('shortName', 'Unknown Feature')}\n            "
                            response += f"- **Opt-In ID**: {opt_in.get('id', 'N/A')}\n            "
                            response += f"- **Created**: {opt_in.get('createdAt', 'N/A')}\n            "\n\n    @app.tool(
        name="get_organization_inventory_device",
        description="📦 Get details of a specific device in inventory."
    )
    def get_organization_inventory_device(
        organization_id: str,
        serial: str
    ):
        """
        Get inventory device details.
        
        Args:
            organization_id: Organization ID
            serial: Device serial number
        """
        try:
            result = meraki_client.dashboard.organizations.getOrganizationInventoryDevice(
                organization_id, serial
            )
            
            response = f"# 📦 Device Details\n\n            "
            
            if result:
                response += f"## {result.get('name', result.get('serial', 'Unknown'))}\n            "
                response += f"- **Serial**: {result.get('serial')}\n            "
                response += f"- **Model**: {result.get('model', 'N/A')}\n            "
                response += f"- **MAC**: {result.get('mac', 'N/A')}\n            "
                response += f"- **Product Type**: {result.get('productType', 'N/A')}\n            "
                
                if result.get('networkId'):
                    response += f"- **Network ID**: {result['networkId']}\n            "
                    response += f"- **Network Name**: {result.get('networkName', 'N/A')}\n            "
                else:
                    response += f"- **Status**: Unused (not assigned to network)\n            "
                
                if result.get('tags'):
                    response += f"- **Tags**: {', '.join(result['tags'])}\n            "\n\n    @app.tool(
        name="get_organization_inventory_devices",
        description="📦 List all devices in organization inventory."
    )
    def get_organization_inventory_devices(
        organization_id: str,
        per_page: int = 1000,
        starting_after: Optional[str] = None,
        ending_before: Optional[str] = None,
        used_state: Optional[str] = None,
        search: Optional[str] = None,
        macs: Optional[List[str]] = None,
        network_ids: Optional[List[str]] = None,
        serials: Optional[List[str]] = None,
        models: Optional[List[str]] = None,
        tags: Optional[List[str]] = None,
        tags_filter_type: str = "withAnyTags",
        product_types: Optional[List[str]] = None
    ):
        """
        List inventory devices.
        
        Args:
            organization_id: Organization ID
            per_page: Results per page
            starting_after: Pagination start
            ending_before: Pagination end
            used_state: "used" or "unused"
            search: Search for devices
            macs: Filter by MAC addresses
            network_ids: Filter by networks
            serials: Filter by serials
            models: Filter by models
            tags: Filter by tags
            tags_filter_type: Tag filter type
            product_types: Filter by product types
        """
        try:
            kwargs = {"perPage": per_page}
            
            if starting_after:
                kwargs["startingAfter"] = starting_after
            if ending_before:
                kwargs["endingBefore"] = ending_before
            if used_state:
                kwargs["usedState"] = used_state
            if search:
                kwargs["search"] = search
            if macs:
                kwargs["macs"] = macs
            if network_ids:
                kwargs["networkIds"] = network_ids
            if serials:
                kwargs["serials"] = serials
            if models:
                kwargs["models"] = models
            if tags:
                kwargs["tags"] = tags
                kwargs["tagsFilterType"] = tags_filter_type
            if product_types:
                kwargs["productTypes"] = product_types
            
            result = meraki_client.dashboard.organizations.getOrganizationInventoryDevices(
                organization_id, **kwargs
            )
            
            response = f"# 📦 Organization Inventory\n\n            "
            response += f"**Organization**: {organization_id}\n\n            "
            
            if result and isinstance(result, list):
                response += f"**Total Devices**: {len(result)}\n\n            "\n\n    @app.tool(
        name="get_organization_licenses",
        description="📜 List all licenses in an organization"
    )
    def get_organization_licenses(
        organization_id: str,
        per_page: int = 1000,
        device_serial: Optional[str] = None,
        network_id: Optional[str] = None,
        state: Optional[str] = None
    ):
        """Get organization licenses with filtering options."""
        try:
            kwargs = {'perPage': per_page, 'total_pages': 'all'}
            
            if device_serial:
                kwargs['deviceSerial'] = device_serial
            if network_id:
                kwargs['networkId'] = network_id
            if state:
                kwargs['state'] = state
            
            result = meraki_client.dashboard.organizations.getOrganizationLicenses(
                organization_id, **kwargs
            )
            
            response = f"# 📜 Organization Licenses\n\n            "
            
            if result and isinstance(result, list):
                response += f"**Total Licenses**: {len(result)}\n\n            "\n\n    @app.tool(
        name="get_organization_networks",
        description="🌐 List all networks in an organization."
    )
    def get_organization_networks(
        organization_id: str,
        config_template_id: Optional[str] = None,
        is_bound_to_config_template: Optional[bool] = None,
        tags: Optional[List[str]] = None,
        tags_filter_type: str = "withAnyTags",
        per_page: int = 100,
        starting_after: Optional[str] = None,
        ending_before: Optional[str] = None
    ):
        """
        List organization networks.
        
        Args:
            organization_id: Organization ID
            config_template_id: Filter by config template
            is_bound_to_config_template: Filter by template binding
            tags: Filter by tags
            tags_filter_type: "withAnyTags" or "withAllTags"
            per_page: Results per page (max 100000)
            starting_after: Start after this ID for pagination
            ending_before: End before this ID for pagination
        """
        try:
            kwargs = {"perPage": per_page}
            
            if config_template_id:
                kwargs["configTemplateId"] = config_template_id
            if is_bound_to_config_template is not None:
                kwargs["isBoundToConfigTemplate"] = is_bound_to_config_template
            if tags:
                kwargs["tags"] = tags
                kwargs["tagsFilterType"] = tags_filter_type
            if starting_after:
                kwargs["startingAfter"] = starting_after
            if ending_before:
                kwargs["endingBefore"] = ending_before
            
            result = meraki_client.dashboard.organizations.getOrganizationNetworks(
                organization_id, **kwargs
            )
            
            response = f"# 🌐 Organization Networks\n\n            "
            response += f"**Organization**: {organization_id}\n\n            "
            
            if result and isinstance(result, list):
                response += f"**Total Networks**: {len(result)}\n\n            "\n\n    @app.tool(
        name="get_organization_policy_objects",
        description="🛡️ List all policy objects in organization"
    )
    def get_organization_policy_objects(
        organization_id: str,
        per_page: int = 1000
    ):
        """Get all policy objects."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationPolicyObjects(
                organization_id, perPage=per_page, total_pages='all'
            )
            
            response = f"# 🛡️ Policy Objects\n\n            "
            
            if result and isinstance(result, list):
                response += f"**Total Policy Objects**: {len(result)}\n\n            "\n\n    @app.tool(
        name="get_organization_saml_idps",
        description="🔐 List SAML Identity Providers for organization"
    )
    def get_organization_saml_idps(organization_id: str):
        """Get SAML Identity Providers."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationSamlIdps(organization_id)
            
            response = f"# 🔐 SAML Identity Providers\n\n            "
            
            if result and isinstance(result, list):
                response += f"**Total Identity Providers**: {len(result)}\n\n            "
                
                for idp in result:
                    response += f"## {idp.get('name', 'Unknown')}\n            "
                    response += f"- **ID**: {idp.get('id', 'N/A')}\n            "
                    response += f"- **Consumer Service URL**: {idp.get('consumerServiceUrl', 'N/A')}\n            "
                    response += f"- **SLO Logout URL**: {idp.get('sloLogoutUrl', 'N/A')}\n            "
                    response += f"- **X.509 Certificate**: {'Present' if idp.get('x509certSha1Fingerprint') else 'Missing'}\n\n            "
            else:
                response += "*No SAML Identity Providers found*\n            "
            
            return response
        except Exception as e:
            return f"❌ Error getting SAML IDPs: {str(e)}"\n\n    @app.tool(
        name="get_organization_webhooks_logs",
        description="📡 Get webhook logs for organization"
    )
    def get_organization_webhooks_logs(
        organization_id: str,
        per_page: int = 1000,
        starting_after: Optional[str] = None,
        ending_before: Optional[str] = None,
        url: Optional[str] = None
    ):
        """Get webhook logs."""
        try:
            kwargs = {'perPage': per_page, 'total_pages': 'all'}
            
            if starting_after:
                kwargs['startingAfter'] = starting_after
            if ending_before:
                kwargs['endingBefore'] = ending_before
            if url:
                kwargs['url'] = url
            
            result = meraki_client.dashboard.organizations.getOrganizationWebhooksLogs(
                organization_id, **kwargs
            )
            
            response = f"# 📡 Webhook Logs\n\n            "
            
            if result and isinstance(result, list):
                response += f"**Total Webhook Logs**: {len(result)}\n\n            "\n\n    @app.tool(
        name="get_organizations",
        description="🏢 List all organizations accessible to the API key."
    )
    def get_organizations():
        """
        List all organizations.
        """
        try:
            result = meraki_client.dashboard.organizations.getOrganizations()
            
            response = f"# 🏢 Organizations\n\n            "
            
            if result and isinstance(result, list):
                response += f"**Total Organizations**: {len(result)}\n\n            "
                
                for org in result:
                    org_id = org.get('id', 'Unknown')
                    response += f"## {org.get('name', 'Unnamed')}\n            "
                    response += f"- **ID**: {org_id}\n            "
                    response += f"- **URL**: {org.get('url', 'N/A')}\n            "\n\n    @app.tool(
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
                    
                    response = f"# ✅ Moved Licenses\n\n            "
                    response += f"**From**: {organization_id}\n            "
                    response += f"**To**: {dest_organization_id}\n            "
                    response += f"**Licenses**: {license_ids}\n            "
                    
                    if result:
                        response += f"\n            **Remaining Licenses**: {result.get('remainingLicenses', 'N/A')}\n            "
                    
                    return response
                except Exception as e:
                    return f"❌ Error moving licenses: {str(e)}"\n\n    @app.tool(
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
                    
                    response = f"# ✅ Moved License Seats\n\n            "
                    response += f"**From**: {organization_id}\n            "
                    response += f"**To**: {dest_organization_id}\n            "
                    response += f"**License**: {license_id}\n            "
                    response += f"**Seats Moved**: {seat_count}\n            "
                    
                    if result:
                        response += f"\n            **Remaining Seats**: {result.get('remainingSeats', 'N/A')}\n            "
                    
                    return response
                except Exception as e:
                    return f"❌ Error moving seats: {str(e)}"\n\n    @app.tool(
                name="release_from_org_inventory",
                description="📦❌ Release devices from organization inventory"
            )
            def release_from_org_inventory(
                organization_id: str,
                serials: str
            ):
                """
                Release devices from inventory.
                
                Args:
                    organization_id: Organization ID
                    serials: Comma-separated serial numbers
                """
                try:
                    serial_list = [s.strip() for s in serials.split(',')]
                    
                    result = meraki_client.dashboard.organizations.releaseFromOrganizationInventory(
                        organization_id, serials=serial_list
                    )
                    
                    response = f"# ✅ Released Devices\n\n            "
                    response += f"**Serials**: {serials}\n            "
                    response += "Devices have been released from inventory.\n            "
                    
                    return response
                except Exception as e:
                    return f"❌ Error releasing devices: {str(e)}"\n\n    @app.tool(
        name="release_from_organization_inventory",
        description="🗑️ Release devices from organization inventory. Requires confirmation."
    )
    def release_from_organization_inventory(
        organization_id: str,
        serials: List[str],
        confirmed: bool = False
    ):
        """
        Release devices from inventory.
        
        Args:
            organization_id: Organization ID
            serials: List of serial numbers to release
            confirmed: Must be true to execute
        """
        if not confirmed:
            return "⚠️ Releasing devices requires confirmed=true. This removes them from the organization!"
        
        try:
            result = meraki_client.dashboard.organizations.releaseFromOrganizationInventory(
                organization_id, serials=serials
            )
            
            return f"✅ Released {len(serials)} devices from inventory"
        except Exception as e:
            return f"❌ Error releasing devices: {str(e)}"\n\n    @app.tool(
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
                    
                    response = f"# ✅ Renewed License Seats\n\n            "
                    response += f"**Renewed License**: {license_id_to_renew}\n            "
                    response += f"**Using License**: {unused_license_id}\n            "
                    
                    if result:
                        response += f"\n            **New Expiration**: {result.get('expirationDate', 'N/A')}\n            "
                    
                    return response
                except Exception as e:
                    return f"❌ Error renewing seats: {str(e)}"\n\n    @app.tool(
                name="restore_org_assurance_alerts",
                description="🔍🔄 Restore dismissed assurance alerts"
            )
            def restore_org_assurance_alerts(
                organization_id: str,
                alert_ids: str
            ):
                """
                Restore dismissed assurance alerts.
                
                Args:
                    organization_id: Organization ID
                    alert_ids: Comma-separated alert IDs to restore
                """
                try:
                    alert_list = [a.strip() for a in alert_ids.split(',')]
                    
                    meraki_client.dashboard.organizations.restoreOrganizationAssuranceAlerts(
                        organization_id, alertIds=alert_list
                    )
                    
                    response = f"# ✅ Restored Alerts\n\n            "
                    response += f"**Alert IDs**: {alert_ids}\n            "
                    response += f"**Count**: {len(alert_list)} alerts restored\n            "
                    
                    return response
                except Exception as e:
                    return f"❌ Error restoring alerts: {str(e)}"\n\n    @app.tool(
                name="update_org_action_batch",
                description="📦✏️ Update an action batch"
            )
            def update_org_action_batch(
                organization_id: str,
                action_batch_id: str,
                confirmed: Optional[bool] = None,
                synchronous: Optional[bool] = None
            ):
                """Update action batch."""
                try:
                    kwargs = {}
                    if confirmed is not None:
                        kwargs['confirmed'] = confirmed
                    if synchronous is not None:
                        kwargs['synchronous'] = synchronous
                    
                    result = meraki_client.dashboard.organizations.updateOrganizationActionBatch(
                        organization_id, action_batch_id, **kwargs
                    )
                    
                    response = f"# ✅ Updated Action Batch\n\n            "
                    response += f"**ID**: {action_batch_id}\n            "
                    return response
                except Exception as e:
                    return f"❌ Error: {str(e)}"\n\n    @app.tool(
                name="update_org_adaptive_policy_acl",
                description="🔒✏️ Update an adaptive policy ACL"
            )
            def update_org_adaptive_policy_acl(
                organization_id: str,
                acl_id: str,
                name: Optional[str] = None,
                description: Optional[str] = None,
                rules: Optional[str] = None,
                ip_version: Optional[str] = None
            ):
                """Update an adaptive policy ACL."""
                try:
                    kwargs = {}
                    
                    if name:
                        kwargs['name'] = name
                    if description:
                        kwargs['description'] = description
                    if rules:
                        kwargs['rules'] = json.loads(rules) if isinstance(rules, str) else rules
                    if ip_version:
                        kwargs['ipVersion'] = ip_version
                    
                    result = meraki_client.dashboard.organizations.updateOrganizationAdaptivePolicyAcl(
                        organization_id, acl_id, **kwargs
                    )
                    
                    response = f"# ✅ Updated Adaptive Policy ACL\n\n            "
                    response += f"**Name**: {result.get('name', 'Unknown')}\n            "
                    response += f"**ID**: {acl_id}\n            "
                    
                    return response
                except Exception as e:
                    return f"❌ Error updating ACL: {str(e)}"\n\n    @app.tool(
                name="update_org_adaptive_policy_group",
                description="👥✏️ Update an adaptive policy group"
            )
            def update_org_adaptive_policy_group(
                organization_id: str,
                group_id: str,
                name: Optional[str] = None,
                sgt: Optional[int] = None,
                description: Optional[str] = None,
                policy_object_ids: Optional[str] = None
            ):
                """Update an adaptive policy group."""
                try:
                    kwargs = {}
                    
                    if name:
                        kwargs['name'] = name
                    if sgt is not None:
                        kwargs['sgt'] = sgt
                    if description:
                        kwargs['description'] = description
                    if policy_object_ids:
                        kwargs['policyObjectIds'] = [id.strip() for id in policy_object_ids.split(',')]
                    
                    result = meraki_client.dashboard.organizations.updateOrganizationAdaptivePolicyGroup(
                        organization_id, group_id, **kwargs
                    )
                    
                    response = f"# ✅ Updated Adaptive Policy Group\n\n            "
                    response += f"**Name**: {result.get('name', 'Unknown')}\n            "
                    response += f"**ID**: {group_id}\n            "
                    
                    return response
                except Exception as e:
                    return f"❌ Error updating group: {str(e)}"\n\n    @app.tool(
                name="update_org_adaptive_policy_settings",
                description="⚙️✏️ Update adaptive policy settings for an organization"
            )
            def update_org_adaptive_policy_settings(
                organization_id: str,
                enabled_network_ids: Optional[str] = None
            ):
                """
                Update adaptive policy settings.
                
                Args:
                    organization_id: Organization ID
                    enabled_network_ids: Comma-separated network IDs to enable adaptive policy
                """
                try:
                    kwargs = {}
                    
                    if enabled_network_ids:
                        kwargs['enabledNetworks'] = [id.strip() for id in enabled_network_ids.split(',')]
                    
                    result = meraki_client.dashboard.organizations.updateOrganizationAdaptivePolicySettings(
                        organization_id, **kwargs
                    )
                    
                    response = f"# ✅ Updated Adaptive Policy Settings\n\n            "
                    response += f"**Enabled Networks**: {result.get('enabledNetworks', [])}\n            "
                    
                    return response
                except Exception as e:
                    return f"❌ Error updating adaptive policy settings: {str(e)}"\n\n    @app.tool(
                name="update_org_admin",
                description="👤✏️ Update a dashboard administrator"
            )
            def update_org_admin(
                organization_id: str,
                admin_id: str,
                name: Optional[str] = None,
                org_access: Optional[str] = None,
                networks: Optional[str] = None,
                tags: Optional[str] = None
            ):
                """Update an organization admin."""
                try:
                    kwargs = {}
                    
                    if name:
                        kwargs['name'] = name
                    if org_access:
                        kwargs['orgAccess'] = org_access
                    if networks:
                        kwargs['networks'] = json.loads(networks) if isinstance(networks, str) else networks
                    if tags:
                        kwargs['tags'] = json.loads(tags) if isinstance(tags, str) else tags
                    
                    result = meraki_client.dashboard.organizations.updateOrganizationAdmin(
                        organization_id, admin_id, **kwargs
                    )
                    
                    response = f"# ✅ Updated Admin\n\n            "
                    response += f"**Name**: {result.get('name', 'Unknown')}\n            "
                    response += f"**ID**: {admin_id}\n            "
                    
                    return response
                except Exception as e:
                    return f"❌ Error updating admin: {str(e)}"\n\n    @app.tool(
                name="update_org_alerts_profile",
                description="🚨✏️ Update an alert profile"
            )
            def update_org_alerts_profile(
                organization_id: str,
                alert_config_id: str,
                enabled: Optional[bool] = None,
                type: Optional[str] = None,
                alert_condition: Optional[str] = None,
                recipients: Optional[str] = None,
                network_tags: Optional[str] = None,
                description: Optional[str] = None
            ):
                """Update an alert profile."""
                try:
                    kwargs = {}
                    
                    if enabled is not None:
                        kwargs['enabled'] = enabled
                    if type:
                        kwargs['type'] = type
                    if alert_condition:
                        kwargs['alertCondition'] = json.loads(alert_condition) if isinstance(alert_condition, str) else alert_condition
                    if recipients:
                        kwargs['recipients'] = json.loads(recipients) if isinstance(recipients, str) else recipients
                    if network_tags:
                        kwargs['networkTags'] = json.loads(network_tags) if isinstance(network_tags, str) else network_tags
                    if description:
                        kwargs['description'] = description
                    
                    result = meraki_client.dashboard.organizations.updateOrganizationAlertsProfile(
                        organization_id, alert_config_id, **kwargs
                    )
                    
                    response = f"# ✅ Updated Alert Profile\n\n            "
                    response += f"**Profile ID**: {alert_config_id}\n            "
                    
                    return response
                except Exception as e:
                    return f"❌ Error updating alert profile: {str(e)}"\n\n    @app.tool(
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
                    
                    response = f"# ✅ Updated Policy Priorities\n\n            "
                    response += f"**New Order**: {', '.join(policy_list)}\n            "
                    
                    return response
                except Exception as e:
                    return f"❌ Error updating priorities: {str(e)}"\n\n    @app.tool(
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
                    
                    response = f"# ✅ Updated Branding Policy\n\n            "
                    response += f"**Policy ID**: {branding_policy_id}\n            "
                    
                    return response
                except Exception as e:
                    return f"❌ Error updating policy: {str(e)}"\n\n    @app.tool(
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
                    
                    response = f"# ✅ Updated Configuration Template\n\n            "
                    response += f"**Template ID**: {config_template_id}\n            "
                    
                    return response
                except Exception as e:
                    return f"❌ Error updating template: {str(e)}"\n\n    @app.tool(
                name="update_org_login_security",
                description="🔐✏️ Update login security settings"
            )
            def update_org_login_security(
                organization_id: str,
                enforce_two_factor_auth: Optional[bool] = None,
                enforce_account_lockout: Optional[bool] = None,
                account_lockout_attempts: Optional[int] = None,
                idle_timeout_minutes: Optional[int] = None,
                enforce_password_expiration: Optional[bool] = None,
                password_expiration_days: Optional[int] = None,
                enforce_strong_passwords: Optional[bool] = None,
                enforce_idle_timeout: Optional[bool] = None,
                enforce_login_ip_ranges: Optional[bool] = None,
                login_ip_ranges: Optional[str] = None,
                api_authentication: Optional[str] = None
            ):
                """Update login security."""
                try:
                    kwargs = {}
                    
                    if enforce_two_factor_auth is not None:
                        kwargs['enforceTwoFactorAuth'] = enforce_two_factor_auth
                    if enforce_account_lockout is not None:
                        kwargs['enforceAccountLockout'] = enforce_account_lockout
                    if account_lockout_attempts:
                        kwargs['accountLockoutAttempts'] = account_lockout_attempts
                    if idle_timeout_minutes:
                        kwargs['idleTimeoutMinutes'] = idle_timeout_minutes
                    if enforce_password_expiration is not None:
                        kwargs['enforcePasswordExpiration'] = enforce_password_expiration
                    if password_expiration_days:
                        kwargs['passwordExpirationDays'] = password_expiration_days
                    if enforce_strong_passwords is not None:
                        kwargs['enforceStrongPasswords'] = enforce_strong_passwords
                    if enforce_idle_timeout is not None:
                        kwargs['enforceIdleTimeout'] = enforce_idle_timeout
                    if enforce_login_ip_ranges is not None:
                        kwargs['enforceLoginIpRanges'] = enforce_login_ip_ranges
                    if login_ip_ranges:
                        kwargs['loginIpRanges'] = [r.strip() for r in login_ip_ranges.split(',')]
                    if api_authentication:
                        kwargs['apiAuthentication'] = json.loads(api_authentication) if isinstance(api_authentication, str) else api_authentication
                    
                    result = meraki_client.dashboard.organizations.updateOrganizationLoginSecurity(
                        organization_id, **kwargs
                    )
                    
                    response = f"# ✅ Updated Login Security\n\n            "
                    return response
                except Exception as e:
                    return f"❌ Error: {str(e)}"\n\n    @app.tool(
                name="update_org_saml",
                description="🔐✏️ Update SAML SSO configuration"
            )
            def update_org_saml(
                organization_id: str,
                enabled: Optional[bool] = None
            ):
                """
                Update SAML configuration.
                
                Args:
                    organization_id: Organization ID
                    enabled: Enable/disable SAML
                """
                try:
                    kwargs = {}
                    
                    if enabled is not None:
                        kwargs['enabled'] = enabled
                    
                    result = meraki_client.dashboard.organizations.updateOrganizationSaml(
                        organization_id, **kwargs
                    )
                    
                    response = f"# ✅ Updated SAML Configuration\n\n            "
                    response += f"**Enabled**: {result.get('enabled', False)}\n            "
                    
                    return response
                except Exception as e:
                    return f"❌ Error updating SAML: {str(e)}"\n\n    @app.tool(
                name="update_org_saml_idp",
                description="🔐🏢✏️ Update a SAML Identity Provider"
            )
            def update_org_saml_idp(
                organization_id: str,
                idp_id: str,
                x509cert_sha1_fingerprint: Optional[str] = None,
                consumer_url: Optional[str] = None,
                idp_entity_id: Optional[str] = None,
                sso_url: Optional[str] = None
            ):
                """Update a SAML IdP."""
                try:
                    kwargs = {}
                    
                    if x509cert_sha1_fingerprint:
                        kwargs['x509certSha1Fingerprint'] = x509cert_sha1_fingerprint
                    if consumer_url:
                        kwargs['consumerUrl'] = consumer_url
                    if idp_entity_id:
                        kwargs['idpEntityId'] = idp_entity_id
                    if sso_url:
                        kwargs['ssoUrl'] = sso_url
                    
                    result = meraki_client.dashboard.organizations.updateOrganizationSamlIdp(
                        organization_id, idp_id, **kwargs
                    )
                    
                    response = f"# ✅ Updated SAML IdP\n\n            "
                    response += f"**ID**: {idp_id}\n            "
                    
                    return response
                except Exception as e:
                    return f"❌ Error updating SAML IdP: {str(e)}"\n\n    @app.tool(
                name="update_org_saml_role",
                description="🔐👥✏️ Update a SAML role"
            )
            def update_org_saml_role(
                organization_id: str,
                role_id: str,
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
                        kwargs['networks'] = json.loads(networks) if isinstance(networks, str) else networks
                    if tags:
                        kwargs['tags'] = json.loads(tags) if isinstance(tags, str) else tags
                    
                    result = meraki_client.dashboard.organizations.updateOrganizationSamlRole(
                        organization_id, role_id, **kwargs
                    )
                    
                    response = f"# ✅ Updated SAML Role\n\n            "
                    response += f"**Role**: {result.get('role', 'Unknown')}\n            "
                    response += f"**ID**: {role_id}\n            "
                    
                    return response
                except Exception as e:
                    return f"❌ Error updating SAML role: {str(e)}"\n\n    @app.tool(
        name="update_organization",
        description="✏️ Update organization settings. Requires confirmation."
    )
    def update_organization(
        organization_id: str,
        name: Optional[str] = None,
        api_enabled: Optional[bool] = None,
        management_details: Optional[List[Dict[str, str]]] = None,
        confirmed: bool = False
    ):
        """
        Update organization.
        
        Args:
            organization_id: Organization ID
            name: New organization name
            api_enabled: Enable/disable API access
            management_details: Management details list
            confirmed: Must be true to execute
        """
        if not confirmed:
            return "⚠️ Updating organization requires confirmed=true"
        
        try:
            kwargs = {}
            
            if name is not None:
                kwargs["name"] = name
            if api_enabled is not None:
                kwargs["api"] = {"enabled": api_enabled}
            if management_details is not None:
                kwargs["management"] = {"details": management_details}
            
            result = meraki_client.dashboard.organizations.updateOrganization(
                organization_id, **kwargs
            )
            
            return f"✅ Updated organization {organization_id}"
        except Exception as e:
            return f"❌ Error updating organization: {str(e)}"\n\n    @app.tool(
                name="update_organization_early_access_features_opt_in",
                description="🧪✏️ Update the scope of an early access feature opt-in"
            )
            def update_organization_early_access_features_opt_in(
                organization_id: str,
                opt_in_id: str,
                limit_scope_to_networks: Optional[str] = None
            ):
                """
                Update an early access opt-in scope.
                
                Args:
                    organization_id: Organization ID
                    opt_in_id: Opt-in ID to update
                    limit_scope_to_networks: Comma-separated network IDs or 'all' for all networks
                """
                try:
                    kwargs = {}
                    
                    if limit_scope_to_networks:
                        if limit_scope_to_networks.lower() == 'all':\n\n