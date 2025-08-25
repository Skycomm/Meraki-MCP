"""
Additional Organizations endpoints for Cisco Meraki MCP Server.
Auto-generated to achieve 100% API coverage.
"""

# Global variables to store app and meraki client
app = None
meraki_client = None

def format_dict_response(data: dict, resource_name: str) -> str:
    """Format dictionary response."""
    result = f"# {resource_name}\n\n"
    for key, value in data.items():
        if value is not None:
            result += f"**{key}**: {value}\n"
    return result

def format_list_response(data: list, resource_name: str) -> str:
    """Format list response."""
    if not data:
        return f"No {resource_name.lower()} found."
    
    result = f"# {resource_name}\n\n"
    result += f"**Total**: {len(data)}\n\n"
    
    for idx, item in enumerate(data[:10], 1):
        if isinstance(item, dict):
            name = item.get('name', item.get('id', f'Item {idx}'))
            result += f"## {name}\n"
            for key, value in item.items():
                if value is not None and key not in ['name']:
                    result += f"- **{key}**: {value}\n"
            result += "\n"
        else:
            result += f"- {item}\n"
    
    if len(data) > 10:
        result += f"\n... and {len(data) - 10} more items"
    
    return result

def register_organizations_additional_tools(mcp_app, meraki):
    """Register additional organizations tools with the MCP server."""
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    
    # Register all additional tools
    register_organizations_additional_handlers()

def register_organizations_additional_handlers():
    """Register additional organizations tool handlers."""

    @app.tool(
        name="assign_organization_licenses_seats",
        description="⚡ Execute organization licenses seats"
    )
    def assign_organization_licenses_seats(organization_id: str):
        """Execute organization licenses seats."""
        try:
            result = meraki_client.dashboard.organizations.assignOrganizationLicensesSeats(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Licenses Seats")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Licenses Seats")
            else:
                return f"✅ Execute organization licenses seats completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="bulk_organization_devices_packet_capture_captures_create",
        description="⚡ Execute organization devices packet capture captures create"
    )
    def bulk_organization_devices_packet_capture_captures_create(organization_id: str):
        """Execute organization devices packet capture captures create."""
        try:
            result = meraki_client.dashboard.organizations.bulkOrganizationDevicesPacketCaptureCapturesCreate(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Devices Packet Capture Captures Create")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Devices Packet Capture Captures Create")
            else:
                return f"✅ Execute organization devices packet capture captures create completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="bulk_organization_devices_packet_capture_captures_delete",
        description="⚡ Execute organization devices packet capture captures delete"
    )
    def bulk_organization_devices_packet_capture_captures_delete(organization_id: str):
        """Execute organization devices packet capture captures delete."""
        try:
            result = meraki_client.dashboard.organizations.bulkOrganizationDevicesPacketCaptureCapturesDelete(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Devices Packet Capture Captures Delete")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Devices Packet Capture Captures Delete")
            else:
                return f"✅ Execute organization devices packet capture captures delete completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="bulk_update_organization_devices_details",
        description="⚡ Execute update organization devices details"
    )
    def bulk_update_organization_devices_details(organization_id: str):
        """Execute update organization devices details."""
        try:
            result = meraki_client.dashboard.organizations.bulkUpdateOrganizationDevicesDetails(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Update Organization Devices Details")
            elif isinstance(result, list):
                return format_list_response(result, "Update Organization Devices Details")
            else:
                return f"✅ Execute update organization devices details completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="claim_into_organization",
        description="📥 Claim into organization"
    )
    def claim_into_organization(organization_id: str):
        """Claim into organization."""
        try:
            result = meraki_client.dashboard.organizations.claimIntoOrganization(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Into Organization")
            elif isinstance(result, list):
                return format_list_response(result, "Into Organization")
            else:
                return f"✅ Claim into organization completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="clone_organization",
        description="⚡ Execute organization"
    )
    def clone_organization(organization_id: str):
        """Execute organization."""
        try:
            result = meraki_client.dashboard.organizations.cloneOrganization(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization")
            elif isinstance(result, list):
                return format_list_response(result, "Organization")
            else:
                return f"✅ Execute organization completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="create_organization_alerts_profile",
        description="➕ Create organization alerts profile"
    )
    def create_organization_alerts_profile(organization_id: str, **kwargs):
        """Create organization alerts profile."""
        try:
            result = meraki_client.dashboard.organizations.createOrganizationAlertsProfile(
                organization_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Alerts Profile")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Alerts Profile")
            else:
                return f"✅ Create organization alerts profile completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="create_organization_devices_controller_migration",
        description="➕ Create organization devices controller migration"
    )
    def create_organization_devices_controller_migration(organization_id: str, **kwargs):
        """Create organization devices controller migration."""
        try:
            result = meraki_client.dashboard.organizations.createOrganizationDevicesControllerMigration(
                organization_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Devices Controller Migration")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Devices Controller Migration")
            else:
                return f"✅ Create organization devices controller migration completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="create_organization_devices_packet_capture_capture",
        description="➕ Create organization devices packet capture capture"
    )
    def create_organization_devices_packet_capture_capture(organization_id: str, **kwargs):
        """Create organization devices packet capture capture."""
        try:
            result = meraki_client.dashboard.organizations.createOrganizationDevicesPacketCaptureCapture(
                organization_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Devices Packet Capture Capture")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Devices Packet Capture Capture")
            else:
                return f"✅ Create organization devices packet capture capture completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="create_organization_devices_packet_capture_schedule",
        description="➕ Create organization devices packet capture schedule"
    )
    def create_organization_devices_packet_capture_schedule(organization_id: str, **kwargs):
        """Create organization devices packet capture schedule."""
        try:
            result = meraki_client.dashboard.organizations.createOrganizationDevicesPacketCaptureSchedule(
                organization_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Devices Packet Capture Schedule")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Devices Packet Capture Schedule")
            else:
                return f"✅ Create organization devices packet capture schedule completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="create_organization_early_access_features_opt_in",
        description="➕ Create organization early access features opt in"
    )
    def create_organization_early_access_features_opt_in(organization_id: str, **kwargs):
        """Create organization early access features opt in."""
        try:
            result = meraki_client.dashboard.organizations.createOrganizationEarlyAccessFeaturesOptIn(
                organization_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Early Access Features Opt In")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Early Access Features Opt In")
            else:
                return f"✅ Create organization early access features opt in completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="create_org_inventory_monitoring_export",
        description="➕ Create organization inventory onboarding cloud monitoring export event"
    )
    def create_organization_inventory_onboarding_cloud_monitoring_export_event(organization_id: str, **kwargs):
        """Create organization inventory onboarding cloud monitoring export event."""
        try:
            result = meraki_client.dashboard.organizations.createOrganizationInventoryOnboardingCloudMonitoringExportEvent(
                organization_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Inventory Onboarding Cloud Monitoring Export Event")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Inventory Onboarding Cloud Monitoring Export Event")
            else:
                return f"✅ Create organization inventory onboarding cloud monitoring export event completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="create_organization_inventory_onboarding_cloud_monitoring_import",
        description="➕ Create organization inventory onboarding cloud monitoring import"
    )
    def create_organization_inventory_onboarding_cloud_monitoring_import(organization_id: str, **kwargs):
        """Create organization inventory onboarding cloud monitoring import."""
        try:
            result = meraki_client.dashboard.organizations.createOrganizationInventoryOnboardingCloudMonitoringImport(
                organization_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Inventory Onboarding Cloud Monitoring Import")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Inventory Onboarding Cloud Monitoring Import")
            else:
                return f"✅ Create organization inventory onboarding cloud monitoring import completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="create_org_inventory_monitoring_prep",
        description="➕ Create organization inventory onboarding cloud monitoring prepare"
    )
    def create_organization_inventory_onboarding_cloud_monitoring_prepare(organization_id: str, **kwargs):
        """Create organization inventory onboarding cloud monitoring prepare."""
        try:
            result = meraki_client.dashboard.organizations.createOrganizationInventoryOnboardingCloudMonitoringPrepare(
                organization_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Inventory Onboarding Cloud Monitoring Prepare")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Inventory Onboarding Cloud Monitoring Prepare")
            else:
                return f"✅ Create organization inventory onboarding cloud monitoring prepare completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="create_organization_network",
        description="➕ Create organization network"
    )
    def create_organization_network(organization_id: str, **kwargs):
        """Create organization network."""
        try:
            result = meraki_client.dashboard.organizations.createOrganizationNetwork(
                organization_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Network")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Network")
            else:
                return f"✅ Create organization network completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="create_organization_saml_idp",
        description="➕ Create organization saml idp"
    )
    def create_organization_saml_idp(organization_id: str, **kwargs):
        """Create organization saml idp."""
        try:
            result = meraki_client.dashboard.organizations.createOrganizationSamlIdp(
                organization_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Saml Idp")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Saml Idp")
            else:
                return f"✅ Create organization saml idp completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="create_organization_splash_theme",
        description="➕ Create organization splash theme"
    )
    def create_organization_splash_theme(organization_id: str, **kwargs):
        """Create organization splash theme."""
        try:
            result = meraki_client.dashboard.organizations.createOrganizationSplashTheme(
                organization_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Splash Theme")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Splash Theme")
            else:
                return f"✅ Create organization splash theme completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="create_organization_splash_theme_asset",
        description="➕ Create organization splash theme asset"
    )
    def create_organization_splash_theme_asset(organization_id: str, **kwargs):
        """Create organization splash theme asset."""
        try:
            result = meraki_client.dashboard.organizations.createOrganizationSplashThemeAsset(
                organization_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Splash Theme Asset")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Splash Theme Asset")
            else:
                return f"✅ Create organization splash theme asset completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="delete_organization_adaptive_policy_acl",
        description="🗑️ Delete organization adaptive policy acl"
    )
    def delete_organization_adaptive_policy_acl(organization_id: str):
        """Delete organization adaptive policy acl."""
        try:
            result = meraki_client.dashboard.organizations.deleteOrganizationAdaptivePolicyAcl(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Adaptive Policy Acl")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Adaptive Policy Acl")
            else:
                return f"✅ Delete organization adaptive policy acl completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="delete_organization_adaptive_policy_group",
        description="🗑️ Delete organization adaptive policy group"
    )
    def delete_organization_adaptive_policy_group(organization_id: str):
        """Delete organization adaptive policy group."""
        try:
            result = meraki_client.dashboard.organizations.deleteOrganizationAdaptivePolicyGroup(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Adaptive Policy Group")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Adaptive Policy Group")
            else:
                return f"✅ Delete organization adaptive policy group completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="delete_organization_adaptive_policy_policy",
        description="🗑️ Delete organization adaptive policy policy"
    )
    def delete_organization_adaptive_policy_policy(organization_id: str):
        """Delete organization adaptive policy policy."""
        try:
            result = meraki_client.dashboard.organizations.deleteOrganizationAdaptivePolicyPolicy(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Adaptive Policy Policy")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Adaptive Policy Policy")
            else:
                return f"✅ Delete organization adaptive policy policy completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="delete_organization_alerts_profile",
        description="🗑️ Delete organization alerts profile"
    )
    def delete_organization_alerts_profile(organization_id: str):
        """Delete organization alerts profile."""
        try:
            result = meraki_client.dashboard.organizations.deleteOrganizationAlertsProfile(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Alerts Profile")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Alerts Profile")
            else:
                return f"✅ Delete organization alerts profile completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="delete_organization_config_template",
        description="🗑️ Delete organization config template"
    )
    def delete_organization_config_template(organization_id: str):
        """Delete organization config template."""
        try:
            result = meraki_client.dashboard.organizations.deleteOrganizationConfigTemplate(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Config Template")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Config Template")
            else:
                return f"✅ Delete organization config template completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="delete_organization_devices_packet_capture_capture",
        description="🗑️ Delete organization devices packet capture capture"
    )
    def delete_organization_devices_packet_capture_capture(organization_id: str):
        """Delete organization devices packet capture capture."""
        try:
            result = meraki_client.dashboard.organizations.deleteOrganizationDevicesPacketCaptureCapture(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Devices Packet Capture Capture")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Devices Packet Capture Capture")
            else:
                return f"✅ Delete organization devices packet capture capture completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="delete_organization_devices_packet_capture_schedule",
        description="🗑️ Delete organization devices packet capture schedule"
    )
    def delete_organization_devices_packet_capture_schedule(organization_id: str):
        """Delete organization devices packet capture schedule."""
        try:
            result = meraki_client.dashboard.organizations.deleteOrganizationDevicesPacketCaptureSchedule(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Devices Packet Capture Schedule")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Devices Packet Capture Schedule")
            else:
                return f"✅ Delete organization devices packet capture schedule completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="delete_organization_early_access_features_opt_in",
        description="🗑️ Delete organization early access features opt in"
    )
    def delete_organization_early_access_features_opt_in(organization_id: str):
        """Delete organization early access features opt in."""
        try:
            result = meraki_client.dashboard.organizations.deleteOrganizationEarlyAccessFeaturesOptIn(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Early Access Features Opt In")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Early Access Features Opt In")
            else:
                return f"✅ Delete organization early access features opt in completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="delete_organization_policy_objects_group",
        description="🗑️ Delete organization policy objects group"
    )
    def delete_organization_policy_objects_group(organization_id: str):
        """Delete organization policy objects group."""
        try:
            result = meraki_client.dashboard.organizations.deleteOrganizationPolicyObjectsGroup(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Policy Objects Group")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Policy Objects Group")
            else:
                return f"✅ Delete organization policy objects group completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="delete_organization_saml_idp",
        description="🗑️ Delete organization saml idp"
    )
    def delete_organization_saml_idp(organization_id: str, saml_id: str):
        """Delete organization saml idp."""
        try:
            result = meraki_client.dashboard.organizations.deleteOrganizationSamlIdp(
                organization_id, saml_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Saml Idp")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Saml Idp")
            else:
                return f"✅ Delete organization saml idp completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="delete_organization_splash_asset",
        description="🗑️ Delete organization splash asset"
    )
    def delete_organization_splash_asset(organization_id: str):
        """Delete organization splash asset."""
        try:
            result = meraki_client.dashboard.organizations.deleteOrganizationSplashAsset(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Splash Asset")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Splash Asset")
            else:
                return f"✅ Delete organization splash asset completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="delete_organization_splash_theme",
        description="🗑️ Delete organization splash theme"
    )
    def delete_organization_splash_theme(organization_id: str):
        """Delete organization splash theme."""
        try:
            result = meraki_client.dashboard.organizations.deleteOrganizationSplashTheme(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Splash Theme")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Splash Theme")
            else:
                return f"✅ Delete organization splash theme completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="disable_organization_integrations_xdr_networks",
        description="⚡ Execute organization integrations xdr networks"
    )
    def disable_organization_integrations_xdr_networks(organization_id: str):
        """Execute organization integrations xdr networks."""
        try:
            result = meraki_client.dashboard.organizations.disableOrganizationIntegrationsXdrNetworks(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Integrations Xdr Networks")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Integrations Xdr Networks")
            else:
                return f"✅ Execute organization integrations xdr networks completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="dismiss_organization_assurance_alerts",
        description="⚡ Execute organization assurance alerts"
    )
    def dismiss_organization_assurance_alerts(organization_id: str):
        """Execute organization assurance alerts."""
        try:
            result = meraki_client.dashboard.organizations.dismissOrganizationAssuranceAlerts(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Assurance Alerts")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Assurance Alerts")
            else:
                return f"✅ Execute organization assurance alerts completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="enable_organization_integrations_xdr_networks",
        description="⚡ Execute organization integrations xdr networks"
    )
    def enable_organization_integrations_xdr_networks(organization_id: str):
        """Execute organization integrations xdr networks."""
        try:
            result = meraki_client.dashboard.organizations.enableOrganizationIntegrationsXdrNetworks(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Integrations Xdr Networks")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Integrations Xdr Networks")
            else:
                return f"✅ Execute organization integrations xdr networks completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="generate_org_packet_capture_url",
        description="⚡ Execute organization devices packet capture capture download url"
    )
    def generate_organization_devices_packet_capture_capture_download_url(organization_id: str):
        """Execute organization devices packet capture capture download url."""
        try:
            result = meraki_client.dashboard.organizations.generateOrganizationDevicesPacketCaptureCaptureDownloadUrl(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Devices Packet Capture Capture Download Url")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Devices Packet Capture Capture Download Url")
            else:
                return f"✅ Execute organization devices packet capture capture download url completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_adaptive_policy_acl",
        description="📊 Get organization adaptive policy acl"
    )
    def get_organization_adaptive_policy_acl(organization_id: str):
        """Get organization adaptive policy acl."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationAdaptivePolicyAcl(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Adaptive Policy Acl")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Adaptive Policy Acl")
            else:
                return f"✅ Get organization adaptive policy acl completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_adaptive_policy_group",
        description="📊 Get organization adaptive policy group"
    )
    def get_organization_adaptive_policy_group(organization_id: str):
        """Get organization adaptive policy group."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationAdaptivePolicyGroup(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Adaptive Policy Group")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Adaptive Policy Group")
            else:
                return f"✅ Get organization adaptive policy group completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_adaptive_policy_overview",
        description="📊 Get organization adaptive policy overview"
    )
    def get_organization_adaptive_policy_overview(organization_id: str):
        """Get organization adaptive policy overview."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationAdaptivePolicyOverview(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Adaptive Policy Overview")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Adaptive Policy Overview")
            else:
                return f"✅ Get organization adaptive policy overview completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_adaptive_policy_policy",
        description="📊 Get organization adaptive policy policy"
    )
    def get_organization_adaptive_policy_policy(organization_id: str):
        """Get organization adaptive policy policy."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationAdaptivePolicyPolicy(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Adaptive Policy Policy")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Adaptive Policy Policy")
            else:
                return f"✅ Get organization adaptive policy policy completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_alerts_profiles",
        description="📊 Get organization alerts profiles"
    )
    def get_organization_alerts_profiles(organization_id: str):
        """Get organization alerts profiles."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationAlertsProfiles(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Alerts Profiles")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Alerts Profiles")
            else:
                return f"✅ Get organization alerts profiles completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_org_api_response_codes_by_interval",
        description="📊 Get organization api requests overview response codes by interval"
    )
    def get_organization_api_requests_overview_response_codes_by_interval(organization_id: str):
        """Get organization api requests overview response codes by interval."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationApiRequestsOverviewResponseCodesByInterval(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Api Requests Overview Response Codes By Interval")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Api Requests Overview Response Codes By Interval")
            else:
                return f"✅ Get organization api requests overview response codes by interval completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_assurance_alert",
        description="📊 Get organization assurance alert"
    )
    def get_organization_assurance_alert(organization_id: str):
        """Get organization assurance alert."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationAssuranceAlert(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Assurance Alert")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Assurance Alert")
            else:
                return f"✅ Get organization assurance alert completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_assurance_alerts",
        description="📊 Get organization assurance alerts"
    )
    def get_organization_assurance_alerts(organization_id: str):
        """Get organization assurance alerts."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationAssuranceAlerts(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Assurance Alerts")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Assurance Alerts")
            else:
                return f"✅ Get organization assurance alerts completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_assurance_alerts_overview",
        description="📊 Get organization assurance alerts overview"
    )
    def get_organization_assurance_alerts_overview(organization_id: str):
        """Get organization assurance alerts overview."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationAssuranceAlertsOverview(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Assurance Alerts Overview")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Assurance Alerts Overview")
            else:
                return f"✅ Get organization assurance alerts overview completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_assurance_alerts_overview_by_network",
        description="📊 Get organization assurance alerts overview by network"
    )
    def get_organization_assurance_alerts_overview_by_network(organization_id: str):
        """Get organization assurance alerts overview by network."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationAssuranceAlertsOverviewByNetwork(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Assurance Alerts Overview By Network")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Assurance Alerts Overview By Network")
            else:
                return f"✅ Get organization assurance alerts overview by network completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_assurance_alerts_overview_by_type",
        description="📊 Get organization assurance alerts overview by type"
    )
    def get_organization_assurance_alerts_overview_by_type(organization_id: str):
        """Get organization assurance alerts overview by type."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationAssuranceAlertsOverviewByType(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Assurance Alerts Overview By Type")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Assurance Alerts Overview By Type")
            else:
                return f"✅ Get organization assurance alerts overview by type completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_assurance_alerts_overview_historical",
        description="📊 Get organization assurance alerts overview historical"
    )
    def get_organization_assurance_alerts_overview_historical(organization_id: str):
        """Get organization assurance alerts overview historical."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationAssuranceAlertsOverviewHistorical(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Assurance Alerts Overview Historical")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Assurance Alerts Overview Historical")
            else:
                return f"✅ Get organization assurance alerts overview historical completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_branding_policies_priorities",
        description="📊 Get organization branding policies priorities"
    )
    def get_organization_branding_policies_priorities(organization_id: str):
        """Get organization branding policies priorities."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationBrandingPoliciesPriorities(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Branding Policies Priorities")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Branding Policies Priorities")
            else:
                return f"✅ Get organization branding policies priorities completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_branding_policy",
        description="📊 Get organization branding policy"
    )
    def get_organization_branding_policy(organization_id: str):
        """Get organization branding policy."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationBrandingPolicy(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Branding Policy")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Branding Policy")
            else:
                return f"✅ Get organization branding policy completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_clients_bandwidth_usage_history",
        description="📊 Get organization clients bandwidth usage history"
    )
    def get_organization_clients_bandwidth_usage_history(organization_id: str):
        """Get organization clients bandwidth usage history."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationClientsBandwidthUsageHistory(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Clients Bandwidth Usage History")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Clients Bandwidth Usage History")
            else:
                return f"✅ Get organization clients bandwidth usage history completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_clients_overview",
        description="📊 Get organization clients overview"
    )
    def get_organization_clients_overview(organization_id: str):
        """Get organization clients overview."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationClientsOverview(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Clients Overview")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Clients Overview")
            else:
                return f"✅ Get organization clients overview completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_clients_search",
        description="📊 Get organization clients search"
    )
    def get_organization_clients_search(organization_id: str):
        """Get organization clients search."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationClientsSearch(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Clients Search")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Clients Search")
            else:
                return f"✅ Get organization clients search completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_config_template",
        description="📊 Get organization config template"
    )
    def get_organization_config_template(organization_id: str):
        """Get organization config template."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationConfigTemplate(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Config Template")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Config Template")
            else:
                return f"✅ Get organization config template completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_configuration_changes",
        description="📊 Get organization configuration changes"
    )
    def get_organization_configuration_changes(organization_id: str):
        """Get organization configuration changes."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationConfigurationChanges(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Configuration Changes")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Configuration Changes")
            else:
                return f"✅ Get organization configuration changes completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_devices",
        description="📊 Get organization devices"
    )
    def get_organization_devices(organization_id: str):
        """Get organization devices."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationDevices(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Devices")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Devices")
            else:
                return f"✅ Get organization devices completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_devices_availabilities",
        description="📊 Get organization devices availabilities"
    )
    def get_organization_devices_availabilities(organization_id: str):
        """Get organization devices availabilities."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationDevicesAvailabilities(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Devices Availabilities")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Devices Availabilities")
            else:
                return f"✅ Get organization devices availabilities completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_devices_availabilities_change_history",
        description="📊 Get organization devices availabilities change history"
    )
    def get_organization_devices_availabilities_change_history(organization_id: str):
        """Get organization devices availabilities change history."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationDevicesAvailabilitiesChangeHistory(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Devices Availabilities Change History")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Devices Availabilities Change History")
            else:
                return f"✅ Get organization devices availabilities change history completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_devices_controller_migrations",
        description="📊 Get organization devices controller migrations"
    )
    def get_organization_devices_controller_migrations(organization_id: str):
        """Get organization devices controller migrations."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationDevicesControllerMigrations(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Devices Controller Migrations")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Devices Controller Migrations")
            else:
                return f"✅ Get organization devices controller migrations completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_devices_overview_by_model",
        description="📊 Get organization devices overview by model"
    )
    def get_organization_devices_overview_by_model(organization_id: str):
        """Get organization devices overview by model."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationDevicesOverviewByModel(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Devices Overview By Model")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Devices Overview By Model")
            else:
                return f"✅ Get organization devices overview by model completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_devices_packet_capture_captures",
        description="📊 Get organization devices packet capture captures"
    )
    def get_organization_devices_packet_capture_captures(organization_id: str):
        """Get organization devices packet capture captures."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationDevicesPacketCaptureCaptures(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Devices Packet Capture Captures")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Devices Packet Capture Captures")
            else:
                return f"✅ Get organization devices packet capture captures completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_devices_packet_capture_schedules",
        description="📊 Get organization devices packet capture schedules"
    )
    def get_organization_devices_packet_capture_schedules(organization_id: str):
        """Get organization devices packet capture schedules."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationDevicesPacketCaptureSchedules(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Devices Packet Capture Schedules")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Devices Packet Capture Schedules")
            else:
                return f"✅ Get organization devices packet capture schedules completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_devices_power_modules_statuses_by_device",
        description="📊 Get organization devices power modules statuses by device"
    )
    def get_organization_devices_power_modules_statuses_by_device(organization_id: str):
        """Get organization devices power modules statuses by device."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationDevicesPowerModulesStatusesByDevice(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Devices Power Modules Statuses By Device")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Devices Power Modules Statuses By Device")
            else:
                return f"✅ Get organization devices power modules statuses by device completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_devices_provisioning_statuses",
        description="📊 Get organization devices provisioning statuses"
    )
    def get_organization_devices_provisioning_statuses(organization_id: str):
        """Get organization devices provisioning statuses."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationDevicesProvisioningStatuses(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Devices Provisioning Statuses")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Devices Provisioning Statuses")
            else:
                return f"✅ Get organization devices provisioning statuses completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_devices_statuses",
        description="📊 Get organization devices statuses"
    )
    def get_organization_devices_statuses(organization_id: str):
        """Get organization devices statuses."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationDevicesStatuses(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Devices Statuses")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Devices Statuses")
            else:
                return f"✅ Get organization devices statuses completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_devices_statuses_overview",
        description="📊 Get organization devices statuses overview"
    )
    def get_organization_devices_statuses_overview(organization_id: str):
        """Get organization devices statuses overview."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationDevicesStatusesOverview(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Devices Statuses Overview")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Devices Statuses Overview")
            else:
                return f"✅ Get organization devices statuses overview completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_devices_system_memory_usage_history_by_interval",
        description="📊 Get organization devices system memory usage history by interval"
    )
    def get_organization_devices_system_memory_usage_history_by_interval(organization_id: str):
        """Get organization devices system memory usage history by interval."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationDevicesSystemMemoryUsageHistoryByInterval(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Devices System Memory Usage History By Interval")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Devices System Memory Usage History By Interval")
            else:
                return f"✅ Get organization devices system memory usage history by interval completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_devices_uplinks_addresses_by_device",
        description="📊 Get organization devices uplinks addresses by device"
    )
    def get_organization_devices_uplinks_addresses_by_device(organization_id: str):
        """Get organization devices uplinks addresses by device."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationDevicesUplinksAddressesByDevice(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Devices Uplinks Addresses By Device")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Devices Uplinks Addresses By Device")
            else:
                return f"✅ Get organization devices uplinks addresses by device completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_devices_uplinks_loss_and_latency",
        description="📊 Get organization devices uplinks loss and latency"
    )
    def get_organization_devices_uplinks_loss_and_latency(organization_id: str):
        """Get organization devices uplinks loss and latency."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationDevicesUplinksLossAndLatency(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Devices Uplinks Loss And Latency")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Devices Uplinks Loss And Latency")
            else:
                return f"✅ Get organization devices uplinks loss and latency completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_early_access_features_opt_in",
        description="📊 Get organization early access features opt in"
    )
    def get_organization_early_access_features_opt_in(organization_id: str):
        """Get organization early access features opt in."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationEarlyAccessFeaturesOptIn(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Early Access Features Opt In")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Early Access Features Opt In")
            else:
                return f"✅ Get organization early access features opt in completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_firmware_upgrades",
        description="📊 Get organization firmware upgrades"
    )
    def get_organization_firmware_upgrades(organization_id: str):
        """Get organization firmware upgrades."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationFirmwareUpgrades(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Firmware Upgrades")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Firmware Upgrades")
            else:
                return f"✅ Get organization firmware upgrades completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_firmware_upgrades_by_device",
        description="📊 Get organization firmware upgrades by device"
    )
    def get_organization_firmware_upgrades_by_device(organization_id: str):
        """Get organization firmware upgrades by device."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationFirmwareUpgradesByDevice(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Firmware Upgrades By Device")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Firmware Upgrades By Device")
            else:
                return f"✅ Get organization firmware upgrades by device completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_floor_plans_auto_locate_devices",
        description="📊 Get organization floor plans auto locate devices"
    )
    def get_organization_floor_plans_auto_locate_devices(organization_id: str):
        """Get organization floor plans auto locate devices."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationFloorPlansAutoLocateDevices(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Floor Plans Auto Locate Devices")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Floor Plans Auto Locate Devices")
            else:
                return f"✅ Get organization floor plans auto locate devices completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_floor_plans_auto_locate_statuses",
        description="📊 Get organization floor plans auto locate statuses"
    )
    def get_organization_floor_plans_auto_locate_statuses(organization_id: str):
        """Get organization floor plans auto locate statuses."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationFloorPlansAutoLocateStatuses(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Floor Plans Auto Locate Statuses")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Floor Plans Auto Locate Statuses")
            else:
                return f"✅ Get organization floor plans auto locate statuses completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_integrations_xdr_networks",
        description="📊 Get organization integrations xdr networks"
    )
    def get_organization_integrations_xdr_networks(organization_id: str):
        """Get organization integrations xdr networks."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationIntegrationsXdrNetworks(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Integrations Xdr Networks")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Integrations Xdr Networks")
            else:
                return f"✅ Get organization integrations xdr networks completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_inventory_devices_swaps_bulk",
        description="📊 Get organization inventory devices swaps bulk"
    )
    def get_organization_inventory_devices_swaps_bulk(organization_id: str):
        """Get organization inventory devices swaps bulk."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationInventoryDevicesSwapsBulk(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Inventory Devices Swaps Bulk")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Inventory Devices Swaps Bulk")
            else:
                return f"✅ Get organization inventory devices swaps bulk completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_inventory_onboarding_cloud_monitoring_imports",
        description="📊 Get organization inventory onboarding cloud monitoring imports"
    )
    def get_organization_inventory_onboarding_cloud_monitoring_imports(organization_id: str):
        """Get organization inventory onboarding cloud monitoring imports."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationInventoryOnboardingCloudMonitoringImports(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Inventory Onboarding Cloud Monitoring Imports")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Inventory Onboarding Cloud Monitoring Imports")
            else:
                return f"✅ Get organization inventory onboarding cloud monitoring imports completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_inventory_onboarding_cloud_monitoring_networks",
        description="📊 Get organization inventory onboarding cloud monitoring networks"
    )
    def get_organization_inventory_onboarding_cloud_monitoring_networks(organization_id: str):
        """Get organization inventory onboarding cloud monitoring networks."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationInventoryOnboardingCloudMonitoringNetworks(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Inventory Onboarding Cloud Monitoring Networks")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Inventory Onboarding Cloud Monitoring Networks")
            else:
                return f"✅ Get organization inventory onboarding cloud monitoring networks completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_license",
        description="📊 Get organization license"
    )
    def get_organization_license(organization_id: str):
        """Get organization license."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationLicense(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization License")
            elif isinstance(result, list):
                return format_list_response(result, "Organization License")
            else:
                return f"✅ Get organization license completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_licenses_overview",
        description="📊 Get organization licenses overview"
    )
    def get_organization_licenses_overview(organization_id: str):
        """Get organization licenses overview."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationLicensesOverview(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Licenses Overview")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Licenses Overview")
            else:
                return f"✅ Get organization licenses overview completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_openapi_spec",
        description="📊 Get organization openapi spec"
    )
    def get_organization_openapi_spec(organization_id: str):
        """Get organization openapi spec."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationOpenapiSpec(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Openapi Spec")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Openapi Spec")
            else:
                return f"✅ Get organization openapi spec completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_policy_object",
        description="📊 Get organization policy object"
    )
    def get_organization_policy_object(organization_id: str):
        """Get organization policy object."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationPolicyObject(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Policy Object")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Policy Object")
            else:
                return f"✅ Get organization policy object completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_policy_objects_group",
        description="📊 Get organization policy objects group"
    )
    def get_organization_policy_objects_group(organization_id: str):
        """Get organization policy objects group."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationPolicyObjectsGroup(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Policy Objects Group")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Policy Objects Group")
            else:
                return f"✅ Get organization policy objects group completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_saml_idp",
        description="📊 Get organization saml idp"
    )
    def get_organization_saml_idp(organization_id: str):
        """Get organization saml idp."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationSamlIdp(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Saml Idp")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Saml Idp")
            else:
                return f"✅ Get organization saml idp completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_saml_idps",
        description="📊 Get organization saml idps"
    )
    def get_organization_saml_idps(organization_id: str):
        """Get organization saml idps."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationSamlIdps(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Saml Idps")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Saml Idps")
            else:
                return f"✅ Get organization saml idps completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_splash_asset",
        description="📊 Get organization splash asset"
    )
    def get_organization_splash_asset(organization_id: str):
        """Get organization splash asset."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationSplashAsset(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Splash Asset")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Splash Asset")
            else:
                return f"✅ Get organization splash asset completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_splash_themes",
        description="📊 Get organization splash themes"
    )
    def get_organization_splash_themes(organization_id: str):
        """Get organization splash themes."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationSplashThemes(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Splash Themes")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Splash Themes")
            else:
                return f"✅ Get organization splash themes completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_summary_top_applications_categories_by_usage",
        description="📊 Get organization summary top applications categories by usage"
    )
    def get_organization_summary_top_applications_categories_by_usage(organization_id: str):
        """Get organization summary top applications categories by usage."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationSummaryTopApplicationsCategoriesByUsage(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Summary Top Applications Categories By Usage")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Summary Top Applications Categories By Usage")
            else:
                return f"✅ Get organization summary top applications categories by usage completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_summary_top_clients_manufacturers_by_usage",
        description="📊 Get organization summary top clients manufacturers by usage"
    )
    def get_organization_summary_top_clients_manufacturers_by_usage(organization_id: str):
        """Get organization summary top clients manufacturers by usage."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationSummaryTopClientsManufacturersByUsage(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Summary Top Clients Manufacturers By Usage")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Summary Top Clients Manufacturers By Usage")
            else:
                return f"✅ Get organization summary top clients manufacturers by usage completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_summary_top_devices_models_by_usage",
        description="📊 Get organization summary top devices models by usage"
    )
    def get_organization_summary_top_devices_models_by_usage(organization_id: str):
        """Get organization summary top devices models by usage."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationSummaryTopDevicesModelsByUsage(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Summary Top Devices Models By Usage")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Summary Top Devices Models By Usage")
            else:
                return f"✅ Get organization summary top devices models by usage completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_summary_top_networks_by_status",
        description="📊 Get organization summary top networks by status"
    )
    def get_organization_summary_top_networks_by_status(organization_id: str):
        """Get organization summary top networks by status."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationSummaryTopNetworksByStatus(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Summary Top Networks By Status")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Summary Top Networks By Status")
            else:
                return f"✅ Get organization summary top networks by status completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_summary_top_switches_by_energy_usage",
        description="📊 Get organization summary top switches by energy usage"
    )
    def get_organization_summary_top_switches_by_energy_usage(organization_id: str):
        """Get organization summary top switches by energy usage."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationSummaryTopSwitchesByEnergyUsage(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Summary Top Switches By Energy Usage")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Summary Top Switches By Energy Usage")
            else:
                return f"✅ Get organization summary top switches by energy usage completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_uplinks_statuses",
        description="📊 Get organization uplinks statuses"
    )
    def get_organization_uplinks_statuses(organization_id: str):
        """Get organization uplinks statuses."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationUplinksStatuses(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Uplinks Statuses")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Uplinks Statuses")
            else:
                return f"✅ Get organization uplinks statuses completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_webhooks_callbacks_status",
        description="📊 Get organization webhooks callbacks status"
    )
    def get_organization_webhooks_callbacks_status(organization_id: str):
        """Get organization webhooks callbacks status."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationWebhooksCallbacksStatus(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Webhooks Callbacks Status")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Webhooks Callbacks Status")
            else:
                return f"✅ Get organization webhooks callbacks status completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organizations",
        description="📊 Get organizations"
    )
    def get_organizations(organization_id: str):
        """Get organizations."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizations(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organizations")
            elif isinstance(result, list):
                return format_list_response(result, "Organizations")
            else:
                return f"✅ Get organizations completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="move_organization_licenses_seats",
        description="⚡ Execute organization licenses seats"
    )
    def move_organization_licenses_seats(organization_id: str):
        """Execute organization licenses seats."""
        try:
            result = meraki_client.dashboard.organizations.moveOrganizationLicensesSeats(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Licenses Seats")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Licenses Seats")
            else:
                return f"✅ Execute organization licenses seats completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="reorder_organization_devices_packet_capture_schedules",
        description="⚡ Execute organization devices packet capture schedules"
    )
    def reorder_organization_devices_packet_capture_schedules(organization_id: str):
        """Execute organization devices packet capture schedules."""
        try:
            result = meraki_client.dashboard.organizations.reorderOrganizationDevicesPacketCaptureSchedules(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Devices Packet Capture Schedules")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Devices Packet Capture Schedules")
            else:
                return f"✅ Execute organization devices packet capture schedules completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="restore_organization_assurance_alerts",
        description="⚡ Execute organization assurance alerts"
    )
    def restore_organization_assurance_alerts(organization_id: str):
        """Execute organization assurance alerts."""
        try:
            result = meraki_client.dashboard.organizations.restoreOrganizationAssuranceAlerts(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Assurance Alerts")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Assurance Alerts")
            else:
                return f"✅ Execute organization assurance alerts completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="stop_organization_devices_packet_capture_capture",
        description="⚡ Execute organization devices packet capture capture"
    )
    def stop_organization_devices_packet_capture_capture(organization_id: str):
        """Execute organization devices packet capture capture."""
        try:
            result = meraki_client.dashboard.organizations.stopOrganizationDevicesPacketCaptureCapture(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Devices Packet Capture Capture")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Devices Packet Capture Capture")
            else:
                return f"✅ Execute organization devices packet capture capture completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="update_organization_adaptive_policy_acl",
        description="✏️ Update organization adaptive policy acl"
    )
    def update_organization_adaptive_policy_acl(organization_id: str, **kwargs):
        """Update organization adaptive policy acl."""
        try:
            result = meraki_client.dashboard.organizations.updateOrganizationAdaptivePolicyAcl(
                organization_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Adaptive Policy Acl")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Adaptive Policy Acl")
            else:
                return f"✅ Update organization adaptive policy acl completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="update_organization_adaptive_policy_group",
        description="✏️ Update organization adaptive policy group"
    )
    def update_organization_adaptive_policy_group(organization_id: str, **kwargs):
        """Update organization adaptive policy group."""
        try:
            result = meraki_client.dashboard.organizations.updateOrganizationAdaptivePolicyGroup(
                organization_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Adaptive Policy Group")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Adaptive Policy Group")
            else:
                return f"✅ Update organization adaptive policy group completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="update_organization_adaptive_policy_policy",
        description="✏️ Update organization adaptive policy policy"
    )
    def update_organization_adaptive_policy_policy(organization_id: str, **kwargs):
        """Update organization adaptive policy policy."""
        try:
            result = meraki_client.dashboard.organizations.updateOrganizationAdaptivePolicyPolicy(
                organization_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Adaptive Policy Policy")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Adaptive Policy Policy")
            else:
                return f"✅ Update organization adaptive policy policy completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="update_organization_adaptive_policy_settings",
        description="✏️ Update organization adaptive policy settings"
    )
    def update_organization_adaptive_policy_settings(organization_id: str, **kwargs):
        """Update organization adaptive policy settings."""
        try:
            result = meraki_client.dashboard.organizations.updateOrganizationAdaptivePolicySettings(
                organization_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Adaptive Policy Settings")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Adaptive Policy Settings")
            else:
                return f"✅ Update organization adaptive policy settings completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="update_organization_alerts_profile",
        description="✏️ Update organization alerts profile"
    )
    def update_organization_alerts_profile(organization_id: str, **kwargs):
        """Update organization alerts profile."""
        try:
            result = meraki_client.dashboard.organizations.updateOrganizationAlertsProfile(
                organization_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Alerts Profile")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Alerts Profile")
            else:
                return f"✅ Update organization alerts profile completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="update_organization_branding_policies_priorities",
        description="✏️ Update organization branding policies priorities"
    )
    def update_organization_branding_policies_priorities(organization_id: str, **kwargs):
        """Update organization branding policies priorities."""
        try:
            result = meraki_client.dashboard.organizations.updateOrganizationBrandingPoliciesPriorities(
                organization_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Branding Policies Priorities")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Branding Policies Priorities")
            else:
                return f"✅ Update organization branding policies priorities completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="update_organization_config_template",
        description="✏️ Update organization config template"
    )
    def update_organization_config_template(organization_id: str, **kwargs):
        """Update organization config template."""
        try:
            result = meraki_client.dashboard.organizations.updateOrganizationConfigTemplate(
                organization_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Config Template")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Config Template")
            else:
                return f"✅ Update organization config template completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="update_organization_devices_packet_capture_schedule",
        description="✏️ Update organization devices packet capture schedule"
    )
    def update_organization_devices_packet_capture_schedule(organization_id: str, **kwargs):
        """Update organization devices packet capture schedule."""
        try:
            result = meraki_client.dashboard.organizations.updateOrganizationDevicesPacketCaptureSchedule(
                organization_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Devices Packet Capture Schedule")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Devices Packet Capture Schedule")
            else:
                return f"✅ Update organization devices packet capture schedule completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="update_organization_policy_objects_group",
        description="✏️ Update organization policy objects group"
    )
    def update_organization_policy_objects_group(organization_id: str, **kwargs):
        """Update organization policy objects group."""
        try:
            result = meraki_client.dashboard.organizations.updateOrganizationPolicyObjectsGroup(
                organization_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Policy Objects Group")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Policy Objects Group")
            else:
                return f"✅ Update organization policy objects group completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="update_organization_saml_idp",
        description="✏️ Update organization saml idp"
    )
    def update_organization_saml_idp(organization_id: str, **kwargs):
        """Update organization saml idp."""
        try:
            result = meraki_client.dashboard.organizations.updateOrganizationSamlIdp(
                organization_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Saml Idp")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Saml Idp")
            else:
                return f"✅ Update organization saml idp completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"
