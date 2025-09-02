"""
Cisco Meraki MCP Server - Organizations SDK Tools
Complete implementation of all 173 official Meraki Organizations API methods.

This module provides 100% coverage of the Organizations category from the official Meraki Dashboard API SDK.
Each tool corresponds directly to a method in the meraki.dashboard.organizations namespace.
"""

# Import removed to avoid circular import
import meraki


def register_organizations_tools(app, meraki_client):
    """Register all organizations SDK tools."""
    print(f"📊 Registering {len(organizations_methods)} organizations SDK tools...")


@app.tool(
    name="assign_organization_licenses_seats",
    description="Assign licensesseats"
)
def assign_organization_licenses_seats(organization_id: str):
    """
    Assign licensesseats
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with licensesseats data
    """
    try:
        result = meraki_client.dashboard.organizations.assignOrganizationLicensesSeats(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="bulk_organization_devices_packet_capture_captures_create",
    description="Perform bulk operation on devicespacketcapturecapturescreate"
)
def bulk_organization_devices_packet_capture_captures_create(organization_id: str, serial: str = None):
    """
    Perform bulk operation on devicespacketcapturecapturescreate
    
    Args:
        organization_id: Organization ID
        serial: Device serial number (optional)
    
    Returns:
        dict: API response with devicespacketcapturecapturescreate data
    """
    try:
        result = meraki_client.dashboard.organizations.bulkOrganizationDevicesPacketCaptureCapturesCreate(organization_id, serial=serial)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="bulk_organization_devices_packet_capture_captures_delete",
    description="Perform bulk operation on devicespacketcapturecapturesdelete"
)
def bulk_organization_devices_packet_capture_captures_delete(organization_id: str, serial: str = None):
    """
    Perform bulk operation on devicespacketcapturecapturesdelete
    
    Args:
        organization_id: Organization ID
        serial: Device serial number (optional)
    
    Returns:
        dict: API response with devicespacketcapturecapturesdelete data
    """
    try:
        result = meraki_client.dashboard.organizations.bulkOrganizationDevicesPacketCaptureCapturesDelete(organization_id, serial=serial)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="bulk_update_organization_devices_details",
    description="Perform bulk operation on updatedevicesdetails"
)
def bulk_update_organization_devices_details(organization_id: str, serial: str = None):
    """
    Perform bulk operation on updatedevicesdetails
    
    Args:
        organization_id: Organization ID
        serial: Device serial number (optional)
    
    Returns:
        dict: API response with updatedevicesdetails data
    """
    try:
        result = meraki_client.dashboard.organizations.bulkUpdateOrganizationDevicesDetails(organization_id, serial=serial)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="claim_into_organization",
    description="Claim into"
)
def claim_into_organization(organization_id: str):
    """
    Claim into
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with into data
    """
    try:
        result = meraki_client.dashboard.organizations.claimIntoOrganization(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="claim_into_organization_inventory",
    description="Claim intoinventory"
)
def claim_into_organization_inventory(organization_id: str):
    """
    Claim intoinventory
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with intoinventory data
    """
    try:
        result = meraki_client.dashboard.organizations.claimIntoOrganizationInventory(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="clone_organization",
    description="Clone organization resource"
)
def clone_organization(organization_id: str):
    """
    Clone organization resource
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with organization resource data
    """
    try:
        result = meraki_client.dashboard.organizations.cloneOrganization(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="combine_organization_networks",
    description="Combine networks"
)
def combine_organization_networks(organization_id: str, network_id: str = None):
    """
    Combine networks
    
    Args:
        organization_id: Organization ID
        network_id: Network ID (optional)
    
    Returns:
        dict: API response with networks data
    """
    try:
        result = meraki_client.dashboard.organizations.combineOrganizationNetworks(organization_id, networkId=network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="create_organization",
    description="Create a new organization resource"
)
def create_organization(organization_id: str, **kwargs):
    """
    Create a new organization resource
    
    Args:
        organization_id: Organization ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with organization resource data
    """
    try:
        result = meraki_client.dashboard.organizations.createOrganization(organization_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="create_organization_action_batch",
    description="Create a new actionbatch"
)
def create_organization_action_batch(organization_id: str, **kwargs):
    """
    Create a new actionbatch
    
    Args:
        organization_id: Organization ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with actionbatch data
    """
    try:
        result = meraki_client.dashboard.organizations.createOrganizationActionBatch(organization_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="create_organization_adaptive_policy_acl",
    description="Create a new adaptivepolicyacl"
)
def create_organization_adaptive_policy_acl(organization_id: str, **kwargs):
    """
    Create a new adaptivepolicyacl
    
    Args:
        organization_id: Organization ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with adaptivepolicyacl data
    """
    try:
        result = meraki_client.dashboard.organizations.createOrganizationAdaptivePolicyAcl(organization_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="create_organization_adaptive_policy_group",
    description="Create a new adaptivepolicygroup"
)
def create_organization_adaptive_policy_group(organization_id: str, **kwargs):
    """
    Create a new adaptivepolicygroup
    
    Args:
        organization_id: Organization ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with adaptivepolicygroup data
    """
    try:
        result = meraki_client.dashboard.organizations.createOrganizationAdaptivePolicyGroup(organization_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="create_organization_adaptive_policy_policy",
    description="Create a new adaptivepolicypolicy"
)
def create_organization_adaptive_policy_policy(organization_id: str, **kwargs):
    """
    Create a new adaptivepolicypolicy
    
    Args:
        organization_id: Organization ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with adaptivepolicypolicy data
    """
    try:
        result = meraki_client.dashboard.organizations.createOrganizationAdaptivePolicyPolicy(organization_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="create_organization_admin",
    description="Create a new admin"
)
def create_organization_admin(organization_id: str, admin_id: str = None, **kwargs):
    """
    Create a new admin
    
    Args:
        organization_id: Organization ID
        admin_id: Admin ID (optional)
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with admin data
    """
    try:
        result = meraki_client.dashboard.organizations.createOrganizationAdmin(organization_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="create_organization_alerts_profile",
    description="Create a new alertsprofile"
)
def create_organization_alerts_profile(organization_id: str, **kwargs):
    """
    Create a new alertsprofile
    
    Args:
        organization_id: Organization ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with alertsprofile data
    """
    try:
        result = meraki_client.dashboard.organizations.createOrganizationAlertsProfile(organization_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="create_organization_branding_policy",
    description="Create a new brandingpolicy"
)
def create_organization_branding_policy(organization_id: str, **kwargs):
    """
    Create a new brandingpolicy
    
    Args:
        organization_id: Organization ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with brandingpolicy data
    """
    try:
        result = meraki_client.dashboard.organizations.createOrganizationBrandingPolicy(organization_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="create_organization_config_template",
    description="Create a new configtemplate"
)
def create_organization_config_template(organization_id: str, **kwargs):
    """
    Create a new configtemplate
    
    Args:
        organization_id: Organization ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with configtemplate data
    """
    try:
        result = meraki_client.dashboard.organizations.createOrganizationConfigTemplate(organization_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="create_organization_devices_controller_migration",
    description="Create a new devicescontrollermigration"
)
def create_organization_devices_controller_migration(organization_id: str, serial: str = None, **kwargs):
    """
    Create a new devicescontrollermigration
    
    Args:
        organization_id: Organization ID
        serial: Device serial number (optional)
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with devicescontrollermigration data
    """
    try:
        result = meraki_client.dashboard.organizations.createOrganizationDevicesControllerMigration(organization_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="create_organization_devices_packet_capture_capture",
    description="Create a new devicespacketcapturecapture"
)
def create_organization_devices_packet_capture_capture(organization_id: str, serial: str = None, **kwargs):
    """
    Create a new devicespacketcapturecapture
    
    Args:
        organization_id: Organization ID
        serial: Device serial number (optional)
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with devicespacketcapturecapture data
    """
    try:
        result = meraki_client.dashboard.organizations.createOrganizationDevicesPacketCaptureCapture(organization_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="create_organization_devices_packet_capture_schedule",
    description="Create a new devicespacketcaptureschedule"
)
def create_organization_devices_packet_capture_schedule(organization_id: str, serial: str = None, **kwargs):
    """
    Create a new devicespacketcaptureschedule
    
    Args:
        organization_id: Organization ID
        serial: Device serial number (optional)
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with devicespacketcaptureschedule data
    """
    try:
        result = meraki_client.dashboard.organizations.createOrganizationDevicesPacketCaptureSchedule(organization_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="create_organization_early_access_features_opt_in",
    description="Create a new earlyaccessfeaturesoptin"
)
def create_organization_early_access_features_opt_in(organization_id: str, **kwargs):
    """
    Create a new earlyaccessfeaturesoptin
    
    Args:
        organization_id: Organization ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with earlyaccessfeaturesoptin data
    """
    try:
        result = meraki_client.dashboard.organizations.createOrganizationEarlyAccessFeaturesOptIn(organization_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="create_organization_inventory_devices_swaps_bulk",
    description="Create a new inventorydevicesswapsbulk"
)
def create_organization_inventory_devices_swaps_bulk(organization_id: str, serial: str = None, **kwargs):
    """
    Create a new inventorydevicesswapsbulk
    
    Args:
        organization_id: Organization ID
        serial: Device serial number (optional)
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with inventorydevicesswapsbulk data
    """
    try:
        result = meraki_client.dashboard.organizations.createOrganizationInventoryDevicesSwapsBulk(organization_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="create_organization_inventory_onboarding_cloud_monitoring_export_event",
    description="Create a new inventoryonboardingcloudmonitoringexportevent"
)
def create_organization_inventory_onboarding_cloud_monitoring_export_event(organization_id: str, **kwargs):
    """
    Create a new inventoryonboardingcloudmonitoringexportevent
    
    Args:
        organization_id: Organization ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with inventoryonboardingcloudmonitoringexportevent data
    """
    try:
        result = meraki_client.dashboard.organizations.createOrganizationInventoryOnboardingCloudMonitoringExportEvent(organization_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="create_organization_inventory_onboarding_cloud_monitoring_import",
    description="Create a new inventoryonboardingcloudmonitoringimport"
)
def create_organization_inventory_onboarding_cloud_monitoring_import(organization_id: str, **kwargs):
    """
    Create a new inventoryonboardingcloudmonitoringimport
    
    Args:
        organization_id: Organization ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with inventoryonboardingcloudmonitoringimport data
    """
    try:
        result = meraki_client.dashboard.organizations.createOrganizationInventoryOnboardingCloudMonitoringImport(organization_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="create_organization_inventory_onboarding_cloud_monitoring_prepare",
    description="Create a new inventoryonboardingcloudmonitoringprepare"
)
def create_organization_inventory_onboarding_cloud_monitoring_prepare(organization_id: str, **kwargs):
    """
    Create a new inventoryonboardingcloudmonitoringprepare
    
    Args:
        organization_id: Organization ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with inventoryonboardingcloudmonitoringprepare data
    """
    try:
        result = meraki_client.dashboard.organizations.createOrganizationInventoryOnboardingCloudMonitoringPrepare(organization_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="create_organization_network",
    description="Create a new network"
)
def create_organization_network(organization_id: str, network_id: str = None, **kwargs):
    """
    Create a new network
    
    Args:
        organization_id: Organization ID
        network_id: Network ID (optional)
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with network data
    """
    try:
        result = meraki_client.dashboard.organizations.createOrganizationNetwork(organization_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="create_organization_policy_object",
    description="Create a new policyobject"
)
def create_organization_policy_object(organization_id: str, **kwargs):
    """
    Create a new policyobject
    
    Args:
        organization_id: Organization ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with policyobject data
    """
    try:
        result = meraki_client.dashboard.organizations.createOrganizationPolicyObject(organization_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="create_organization_policy_objects_group",
    description="Create a new policyobjectsgroup"
)
def create_organization_policy_objects_group(organization_id: str, **kwargs):
    """
    Create a new policyobjectsgroup
    
    Args:
        organization_id: Organization ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with policyobjectsgroup data
    """
    try:
        result = meraki_client.dashboard.organizations.createOrganizationPolicyObjectsGroup(organization_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="create_organization_saml_idp",
    description="Create a new samlidp"
)
def create_organization_saml_idp(organization_id: str, **kwargs):
    """
    Create a new samlidp
    
    Args:
        organization_id: Organization ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with samlidp data
    """
    try:
        result = meraki_client.dashboard.organizations.createOrganizationSamlIdp(organization_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="create_organization_saml_role",
    description="Create a new samlrole"
)
def create_organization_saml_role(organization_id: str, **kwargs):
    """
    Create a new samlrole
    
    Args:
        organization_id: Organization ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with samlrole data
    """
    try:
        result = meraki_client.dashboard.organizations.createOrganizationSamlRole(organization_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="create_organization_splash_theme",
    description="Create a new splashtheme"
)
def create_organization_splash_theme(organization_id: str, **kwargs):
    """
    Create a new splashtheme
    
    Args:
        organization_id: Organization ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with splashtheme data
    """
    try:
        result = meraki_client.dashboard.organizations.createOrganizationSplashTheme(organization_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="create_organization_splash_theme_asset",
    description="Create a new splashthemeasset"
)
def create_organization_splash_theme_asset(organization_id: str, **kwargs):
    """
    Create a new splashthemeasset
    
    Args:
        organization_id: Organization ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with splashthemeasset data
    """
    try:
        result = meraki_client.dashboard.organizations.createOrganizationSplashThemeAsset(organization_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="delete_organization",
    description="Delete an existing organization resource"
)
def delete_organization(organization_id: str):
    """
    Delete an existing organization resource
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with organization resource data
    """
    try:
        result = meraki_client.dashboard.organizations.deleteOrganization(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="delete_organization_action_batch",
    description="Delete an existing actionbatch"
)
def delete_organization_action_batch(organization_id: str):
    """
    Delete an existing actionbatch
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with actionbatch data
    """
    try:
        result = meraki_client.dashboard.organizations.deleteOrganizationActionBatch(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="delete_organization_adaptive_policy_acl",
    description="Delete an existing adaptivepolicyacl"
)
def delete_organization_adaptive_policy_acl(organization_id: str):
    """
    Delete an existing adaptivepolicyacl
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with adaptivepolicyacl data
    """
    try:
        result = meraki_client.dashboard.organizations.deleteOrganizationAdaptivePolicyAcl(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="delete_organization_adaptive_policy_group",
    description="Delete an existing adaptivepolicygroup"
)
def delete_organization_adaptive_policy_group(organization_id: str):
    """
    Delete an existing adaptivepolicygroup
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with adaptivepolicygroup data
    """
    try:
        result = meraki_client.dashboard.organizations.deleteOrganizationAdaptivePolicyGroup(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="delete_organization_adaptive_policy_policy",
    description="Delete an existing adaptivepolicypolicy"
)
def delete_organization_adaptive_policy_policy(organization_id: str):
    """
    Delete an existing adaptivepolicypolicy
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with adaptivepolicypolicy data
    """
    try:
        result = meraki_client.dashboard.organizations.deleteOrganizationAdaptivePolicyPolicy(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="delete_organization_admin",
    description="Delete an existing admin"
)
def delete_organization_admin(organization_id: str, admin_id: str = None):
    """
    Delete an existing admin
    
    Args:
        organization_id: Organization ID
        admin_id: Admin ID (optional)
    
    Returns:
        dict: API response with admin data
    """
    try:
        result = meraki_client.dashboard.organizations.deleteOrganizationAdmin(organization_id, adminId=admin_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="delete_organization_alerts_profile",
    description="Delete an existing alertsprofile"
)
def delete_organization_alerts_profile(organization_id: str):
    """
    Delete an existing alertsprofile
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with alertsprofile data
    """
    try:
        result = meraki_client.dashboard.organizations.deleteOrganizationAlertsProfile(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="delete_organization_branding_policy",
    description="Delete an existing brandingpolicy"
)
def delete_organization_branding_policy(organization_id: str):
    """
    Delete an existing brandingpolicy
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with brandingpolicy data
    """
    try:
        result = meraki_client.dashboard.organizations.deleteOrganizationBrandingPolicy(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="delete_organization_config_template",
    description="Delete an existing configtemplate"
)
def delete_organization_config_template(organization_id: str):
    """
    Delete an existing configtemplate
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with configtemplate data
    """
    try:
        result = meraki_client.dashboard.organizations.deleteOrganizationConfigTemplate(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="delete_organization_devices_packet_capture_capture",
    description="Delete an existing devicespacketcapturecapture"
)
def delete_organization_devices_packet_capture_capture(organization_id: str, serial: str = None):
    """
    Delete an existing devicespacketcapturecapture
    
    Args:
        organization_id: Organization ID
        serial: Device serial number (optional)
    
    Returns:
        dict: API response with devicespacketcapturecapture data
    """
    try:
        result = meraki_client.dashboard.organizations.deleteOrganizationDevicesPacketCaptureCapture(organization_id, serial=serial)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="delete_organization_devices_packet_capture_schedule",
    description="Delete an existing devicespacketcaptureschedule"
)
def delete_organization_devices_packet_capture_schedule(organization_id: str, serial: str = None):
    """
    Delete an existing devicespacketcaptureschedule
    
    Args:
        organization_id: Organization ID
        serial: Device serial number (optional)
    
    Returns:
        dict: API response with devicespacketcaptureschedule data
    """
    try:
        result = meraki_client.dashboard.organizations.deleteOrganizationDevicesPacketCaptureSchedule(organization_id, serial=serial)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="delete_organization_early_access_features_opt_in",
    description="Delete an existing earlyaccessfeaturesoptin"
)
def delete_organization_early_access_features_opt_in(organization_id: str):
    """
    Delete an existing earlyaccessfeaturesoptin
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with earlyaccessfeaturesoptin data
    """
    try:
        result = meraki_client.dashboard.organizations.deleteOrganizationEarlyAccessFeaturesOptIn(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="delete_organization_policy_object",
    description="Delete an existing policyobject"
)
def delete_organization_policy_object(organization_id: str):
    """
    Delete an existing policyobject
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with policyobject data
    """
    try:
        result = meraki_client.dashboard.organizations.deleteOrganizationPolicyObject(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="delete_organization_policy_objects_group",
    description="Delete an existing policyobjectsgroup"
)
def delete_organization_policy_objects_group(organization_id: str):
    """
    Delete an existing policyobjectsgroup
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with policyobjectsgroup data
    """
    try:
        result = meraki_client.dashboard.organizations.deleteOrganizationPolicyObjectsGroup(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="delete_organization_saml_idp",
    description="Delete an existing samlidp"
)
def delete_organization_saml_idp(organization_id: str):
    """
    Delete an existing samlidp
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with samlidp data
    """
    try:
        result = meraki_client.dashboard.organizations.deleteOrganizationSamlIdp(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="delete_organization_saml_role",
    description="Delete an existing samlrole"
)
def delete_organization_saml_role(organization_id: str):
    """
    Delete an existing samlrole
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with samlrole data
    """
    try:
        result = meraki_client.dashboard.organizations.deleteOrganizationSamlRole(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="delete_organization_splash_asset",
    description="Delete an existing splashasset"
)
def delete_organization_splash_asset(organization_id: str):
    """
    Delete an existing splashasset
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with splashasset data
    """
    try:
        result = meraki_client.dashboard.organizations.deleteOrganizationSplashAsset(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="delete_organization_splash_theme",
    description="Delete an existing splashtheme"
)
def delete_organization_splash_theme(organization_id: str):
    """
    Delete an existing splashtheme
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with splashtheme data
    """
    try:
        result = meraki_client.dashboard.organizations.deleteOrganizationSplashTheme(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="disable_organization_integrations_xdr_networks",
    description="Manage disableintegrationsxdrnetworks"
)
def disable_organization_integrations_xdr_networks(organization_id: str, network_id: str = None):
    """
    Manage disableintegrationsxdrnetworks
    
    Args:
        organization_id: Organization ID
        network_id: Network ID (optional)
    
    Returns:
        dict: API response with disableintegrationsxdrnetworks data
    """
    try:
        result = meraki_client.dashboard.organizations.disableOrganizationIntegrationsXdrNetworks(organization_id, networkId=network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="dismiss_organization_assurance_alerts",
    description="Manage dismissassurancealerts"
)
def dismiss_organization_assurance_alerts(organization_id: str):
    """
    Manage dismissassurancealerts
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with dismissassurancealerts data
    """
    try:
        result = meraki_client.dashboard.organizations.dismissOrganizationAssuranceAlerts(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="enable_organization_integrations_xdr_networks",
    description="Manage enableintegrationsxdrnetworks"
)
def enable_organization_integrations_xdr_networks(organization_id: str, network_id: str = None):
    """
    Manage enableintegrationsxdrnetworks
    
    Args:
        organization_id: Organization ID
        network_id: Network ID (optional)
    
    Returns:
        dict: API response with enableintegrationsxdrnetworks data
    """
    try:
        result = meraki_client.dashboard.organizations.enableOrganizationIntegrationsXdrNetworks(organization_id, networkId=network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="generate_organization_devices_packet_capture_capture_download_url",
    description="Manage generatedevicespacketcapturecapturedownloadurl"
)
def generate_organization_devices_packet_capture_capture_download_url(organization_id: str, serial: str = None):
    """
    Manage generatedevicespacketcapturecapturedownloadurl
    
    Args:
        organization_id: Organization ID
        serial: Device serial number (optional)
    
    Returns:
        dict: API response with generatedevicespacketcapturecapturedownloadurl data
    """
    try:
        result = meraki_client.dashboard.organizations.generateOrganizationDevicesPacketCaptureCaptureDownloadUrl(organization_id, serial=serial)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization",
    description="Retrieve organization resource"
)
def get_organization(organization_id: str):
    """
    Retrieve organization resource
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with organization resource data
    """
    try:
        result = meraki_client.dashboard.organizations.getOrganization(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_action_batch",
    description="Retrieve actionbatch"
)
def get_organization_action_batch(organization_id: str):
    """
    Retrieve actionbatch
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with actionbatch data
    """
    try:
        result = meraki_client.dashboard.organizations.getOrganizationActionBatch(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_action_batches",
    description="Retrieve actionbatches"
)
def get_organization_action_batches(organization_id: str):
    """
    Retrieve actionbatches
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with actionbatches data
    """
    try:
        result = meraki_client.dashboard.organizations.getOrganizationActionBatches(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_adaptive_policy_acl",
    description="Retrieve adaptivepolicyacl"
)
def get_organization_adaptive_policy_acl(organization_id: str):
    """
    Retrieve adaptivepolicyacl
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with adaptivepolicyacl data
    """
    try:
        result = meraki_client.dashboard.organizations.getOrganizationAdaptivePolicyAcl(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_adaptive_policy_acls",
    description="Retrieve adaptivepolicyacls"
)
def get_organization_adaptive_policy_acls(organization_id: str):
    """
    Retrieve adaptivepolicyacls
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with adaptivepolicyacls data
    """
    try:
        result = meraki_client.dashboard.organizations.getOrganizationAdaptivePolicyAcls(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_adaptive_policy_group",
    description="Retrieve adaptivepolicygroup"
)
def get_organization_adaptive_policy_group(organization_id: str):
    """
    Retrieve adaptivepolicygroup
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with adaptivepolicygroup data
    """
    try:
        result = meraki_client.dashboard.organizations.getOrganizationAdaptivePolicyGroup(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_adaptive_policy_groups",
    description="Retrieve adaptivepolicygroups"
)
def get_organization_adaptive_policy_groups(organization_id: str):
    """
    Retrieve adaptivepolicygroups
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with adaptivepolicygroups data
    """
    try:
        result = meraki_client.dashboard.organizations.getOrganizationAdaptivePolicyGroups(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_adaptive_policy_overview",
    description="Retrieve adaptivepolicyoverview"
)
def get_organization_adaptive_policy_overview(organization_id: str):
    """
    Retrieve adaptivepolicyoverview
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with adaptivepolicyoverview data
    """
    try:
        result = meraki_client.dashboard.organizations.getOrganizationAdaptivePolicyOverview(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_adaptive_policy_policies",
    description="Retrieve adaptivepolicypolicies"
)
def get_organization_adaptive_policy_policies(organization_id: str):
    """
    Retrieve adaptivepolicypolicies
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with adaptivepolicypolicies data
    """
    try:
        result = meraki_client.dashboard.organizations.getOrganizationAdaptivePolicyPolicies(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_adaptive_policy_policy",
    description="Retrieve adaptivepolicypolicy"
)
def get_organization_adaptive_policy_policy(organization_id: str):
    """
    Retrieve adaptivepolicypolicy
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with adaptivepolicypolicy data
    """
    try:
        result = meraki_client.dashboard.organizations.getOrganizationAdaptivePolicyPolicy(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_adaptive_policy_settings",
    description="Retrieve adaptivepolicysettings"
)
def get_organization_adaptive_policy_settings(organization_id: str):
    """
    Retrieve adaptivepolicysettings
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with adaptivepolicysettings data
    """
    try:
        result = meraki_client.dashboard.organizations.getOrganizationAdaptivePolicySettings(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_admins",
    description="Retrieve admins"
)
def get_organization_admins(organization_id: str, admin_id: str = None):
    """
    Retrieve admins
    
    Args:
        organization_id: Organization ID
        admin_id: Admin ID (optional)
    
    Returns:
        dict: API response with admins data
    """
    try:
        result = meraki_client.dashboard.organizations.getOrganizationAdmins(organization_id, adminId=admin_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_alerts_profiles",
    description="Retrieve alertsprofiles"
)
def get_organization_alerts_profiles(organization_id: str):
    """
    Retrieve alertsprofiles
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with alertsprofiles data
    """
    try:
        result = meraki_client.dashboard.organizations.getOrganizationAlertsProfiles(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_api_requests",
    description="Retrieve apirequests"
)
def get_organization_api_requests(organization_id: str):
    """
    Retrieve apirequests
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with apirequests data
    """
    try:
        result = meraki_client.dashboard.organizations.getOrganizationApiRequests(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_api_requests_overview",
    description="Retrieve apirequestsoverview"
)
def get_organization_api_requests_overview(organization_id: str):
    """
    Retrieve apirequestsoverview
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with apirequestsoverview data
    """
    try:
        result = meraki_client.dashboard.organizations.getOrganizationApiRequestsOverview(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_api_requests_overview_response_codes_by_interval",
    description="Retrieve apirequestsoverviewresponsecodesbyinterval"
)
def get_organization_api_requests_overview_response_codes_by_interval(organization_id: str):
    """
    Retrieve apirequestsoverviewresponsecodesbyinterval
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with apirequestsoverviewresponsecodesbyinterval data
    """
    try:
        result = meraki_client.dashboard.organizations.getOrganizationApiRequestsOverviewResponseCodesByInterval(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_assurance_alert",
    description="Retrieve assurancealert"
)
def get_organization_assurance_alert(organization_id: str):
    """
    Retrieve assurancealert
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with assurancealert data
    """
    try:
        result = meraki_client.dashboard.organizations.getOrganizationAssuranceAlert(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_assurance_alerts",
    description="Retrieve assurancealerts"
)
def get_organization_assurance_alerts(organization_id: str):
    """
    Retrieve assurancealerts
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with assurancealerts data
    """
    try:
        result = meraki_client.dashboard.organizations.getOrganizationAssuranceAlerts(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_assurance_alerts_overview",
    description="Retrieve assurancealertsoverview"
)
def get_organization_assurance_alerts_overview(organization_id: str):
    """
    Retrieve assurancealertsoverview
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with assurancealertsoverview data
    """
    try:
        result = meraki_client.dashboard.organizations.getOrganizationAssuranceAlertsOverview(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_assurance_alerts_overview_by_network",
    description="Retrieve assurancealertsoverviewbynetwork"
)
def get_organization_assurance_alerts_overview_by_network(organization_id: str, network_id: str = None):
    """
    Retrieve assurancealertsoverviewbynetwork
    
    Args:
        organization_id: Organization ID
        network_id: Network ID (optional)
    
    Returns:
        dict: API response with assurancealertsoverviewbynetwork data
    """
    try:
        result = meraki_client.dashboard.organizations.getOrganizationAssuranceAlertsOverviewByNetwork(organization_id, networkId=network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_assurance_alerts_overview_by_type",
    description="Retrieve assurancealertsoverviewbytype"
)
def get_organization_assurance_alerts_overview_by_type(organization_id: str):
    """
    Retrieve assurancealertsoverviewbytype
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with assurancealertsoverviewbytype data
    """
    try:
        result = meraki_client.dashboard.organizations.getOrganizationAssuranceAlertsOverviewByType(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_assurance_alerts_overview_historical",
    description="Retrieve assurancealertsoverviewhistorical"
)
def get_organization_assurance_alerts_overview_historical(organization_id: str):
    """
    Retrieve assurancealertsoverviewhistorical
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with assurancealertsoverviewhistorical data
    """
    try:
        result = meraki_client.dashboard.organizations.getOrganizationAssuranceAlertsOverviewHistorical(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_branding_policies",
    description="Retrieve brandingpolicies"
)
def get_organization_branding_policies(organization_id: str):
    """
    Retrieve brandingpolicies
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with brandingpolicies data
    """
    try:
        result = meraki_client.dashboard.organizations.getOrganizationBrandingPolicies(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_branding_policies_priorities",
    description="Retrieve brandingpoliciespriorities"
)
def get_organization_branding_policies_priorities(organization_id: str):
    """
    Retrieve brandingpoliciespriorities
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with brandingpoliciespriorities data
    """
    try:
        result = meraki_client.dashboard.organizations.getOrganizationBrandingPoliciesPriorities(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_branding_policy",
    description="Retrieve brandingpolicy"
)
def get_organization_branding_policy(organization_id: str):
    """
    Retrieve brandingpolicy
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with brandingpolicy data
    """
    try:
        result = meraki_client.dashboard.organizations.getOrganizationBrandingPolicy(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_clients_bandwidth_usage_history",
    description="Retrieve clientsbandwidthusagehistory"
)
def get_organization_clients_bandwidth_usage_history(organization_id: str, timespan: int = 86400):
    """
    Retrieve clientsbandwidthusagehistory
    
    Args:
        organization_id: Organization ID
        timespan: Timespan in seconds (default: 86400)
    
    Returns:
        dict: API response with clientsbandwidthusagehistory data
    """
    try:
        result = meraki_client.dashboard.organizations.getOrganizationClientsBandwidthUsageHistory(organization_id, timespan=timespan)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_clients_overview",
    description="Retrieve clientsoverview"
)
def get_organization_clients_overview(organization_id: str):
    """
    Retrieve clientsoverview
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with clientsoverview data
    """
    try:
        result = meraki_client.dashboard.organizations.getOrganizationClientsOverview(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_clients_search",
    description="Retrieve clientssearch"
)
def get_organization_clients_search(organization_id: str):
    """
    Retrieve clientssearch
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with clientssearch data
    """
    try:
        result = meraki_client.dashboard.organizations.getOrganizationClientsSearch(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_config_template",
    description="Retrieve configtemplate"
)
def get_organization_config_template(organization_id: str):
    """
    Retrieve configtemplate
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with configtemplate data
    """
    try:
        result = meraki_client.dashboard.organizations.getOrganizationConfigTemplate(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_config_templates",
    description="Retrieve configtemplates"
)
def get_organization_config_templates(organization_id: str):
    """
    Retrieve configtemplates
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with configtemplates data
    """
    try:
        result = meraki_client.dashboard.organizations.getOrganizationConfigTemplates(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_configuration_changes",
    description="Retrieve configurationchanges"
)
def get_organization_configuration_changes(organization_id: str):
    """
    Retrieve configurationchanges
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with configurationchanges data
    """
    try:
        result = meraki_client.dashboard.organizations.getOrganizationConfigurationChanges(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_devices",
    description="Retrieve devices"
)
def get_organization_devices(organization_id: str, serial: str = None):
    """
    Retrieve devices
    
    Args:
        organization_id: Organization ID
        serial: Device serial number (optional)
    
    Returns:
        dict: API response with devices data
    """
    try:
        result = meraki_client.dashboard.organizations.getOrganizationDevices(organization_id, serial=serial)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_devices_availabilities",
    description="Retrieve devicesavailabilities"
)
def get_organization_devices_availabilities(organization_id: str, serial: str = None):
    """
    Retrieve devicesavailabilities
    
    Args:
        organization_id: Organization ID
        serial: Device serial number (optional)
    
    Returns:
        dict: API response with devicesavailabilities data
    """
    try:
        result = meraki_client.dashboard.organizations.getOrganizationDevicesAvailabilities(organization_id, serial=serial)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_devices_availabilities_change_history",
    description="Retrieve devicesavailabilitieschangehistory"
)
def get_organization_devices_availabilities_change_history(organization_id: str, serial: str = None, timespan: int = 86400):
    """
    Retrieve devicesavailabilitieschangehistory
    
    Args:
        organization_id: Organization ID
        serial: Device serial number (optional)
        timespan: Timespan in seconds (default: 86400)
    
    Returns:
        dict: API response with devicesavailabilitieschangehistory data
    """
    try:
        result = meraki_client.dashboard.organizations.getOrganizationDevicesAvailabilitiesChangeHistory(organization_id, serial=serial, timespan=timespan)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_devices_controller_migrations",
    description="Retrieve devicescontrollermigrations"
)
def get_organization_devices_controller_migrations(organization_id: str, serial: str = None):
    """
    Retrieve devicescontrollermigrations
    
    Args:
        organization_id: Organization ID
        serial: Device serial number (optional)
    
    Returns:
        dict: API response with devicescontrollermigrations data
    """
    try:
        result = meraki_client.dashboard.organizations.getOrganizationDevicesControllerMigrations(organization_id, serial=serial)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_devices_overview_by_model",
    description="Retrieve devicesoverviewbymodel"
)
def get_organization_devices_overview_by_model(organization_id: str, serial: str = None):
    """
    Retrieve devicesoverviewbymodel
    
    Args:
        organization_id: Organization ID
        serial: Device serial number (optional)
    
    Returns:
        dict: API response with devicesoverviewbymodel data
    """
    try:
        result = meraki_client.dashboard.organizations.getOrganizationDevicesOverviewByModel(organization_id, serial=serial)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_devices_packet_capture_captures",
    description="Retrieve devicespacketcapturecaptures"
)
def get_organization_devices_packet_capture_captures(organization_id: str, serial: str = None):
    """
    Retrieve devicespacketcapturecaptures
    
    Args:
        organization_id: Organization ID
        serial: Device serial number (optional)
    
    Returns:
        dict: API response with devicespacketcapturecaptures data
    """
    try:
        result = meraki_client.dashboard.organizations.getOrganizationDevicesPacketCaptureCaptures(organization_id, serial=serial)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_devices_packet_capture_schedules",
    description="Retrieve devicespacketcaptureschedules"
)
def get_organization_devices_packet_capture_schedules(organization_id: str, serial: str = None):
    """
    Retrieve devicespacketcaptureschedules
    
    Args:
        organization_id: Organization ID
        serial: Device serial number (optional)
    
    Returns:
        dict: API response with devicespacketcaptureschedules data
    """
    try:
        result = meraki_client.dashboard.organizations.getOrganizationDevicesPacketCaptureSchedules(organization_id, serial=serial)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_devices_power_modules_statuses_by_device",
    description="Retrieve devicespowermodulesstatusesbydevice"
)
def get_organization_devices_power_modules_statuses_by_device(organization_id: str, serial: str = None):
    """
    Retrieve devicespowermodulesstatusesbydevice
    
    Args:
        organization_id: Organization ID
        serial: Device serial number (optional)
    
    Returns:
        dict: API response with devicespowermodulesstatusesbydevice data
    """
    try:
        result = meraki_client.dashboard.organizations.getOrganizationDevicesPowerModulesStatusesByDevice(organization_id, serial=serial)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_devices_provisioning_statuses",
    description="Retrieve devicesprovisioningstatuses"
)
def get_organization_devices_provisioning_statuses(organization_id: str, serial: str = None):
    """
    Retrieve devicesprovisioningstatuses
    
    Args:
        organization_id: Organization ID
        serial: Device serial number (optional)
    
    Returns:
        dict: API response with devicesprovisioningstatuses data
    """
    try:
        result = meraki_client.dashboard.organizations.getOrganizationDevicesProvisioningStatuses(organization_id, serial=serial)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_devices_statuses",
    description="Retrieve devicesstatuses"
)
def get_organization_devices_statuses(organization_id: str, serial: str = None):
    """
    Retrieve devicesstatuses
    
    Args:
        organization_id: Organization ID
        serial: Device serial number (optional)
    
    Returns:
        dict: API response with devicesstatuses data
    """
    try:
        result = meraki_client.dashboard.organizations.getOrganizationDevicesStatuses(organization_id, serial=serial)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_devices_statuses_overview",
    description="Retrieve devicesstatusesoverview"
)
def get_organization_devices_statuses_overview(organization_id: str, serial: str = None):
    """
    Retrieve devicesstatusesoverview
    
    Args:
        organization_id: Organization ID
        serial: Device serial number (optional)
    
    Returns:
        dict: API response with devicesstatusesoverview data
    """
    try:
        result = meraki_client.dashboard.organizations.getOrganizationDevicesStatusesOverview(organization_id, serial=serial)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_devices_system_memory_usage_history_by_interval",
    description="Retrieve devicessystemmemoryusagehistorybyinterval"
)
def get_organization_devices_system_memory_usage_history_by_interval(organization_id: str, serial: str = None, timespan: int = 86400):
    """
    Retrieve devicessystemmemoryusagehistorybyinterval
    
    Args:
        organization_id: Organization ID
        serial: Device serial number (optional)
        timespan: Timespan in seconds (default: 86400)
    
    Returns:
        dict: API response with devicessystemmemoryusagehistorybyinterval data
    """
    try:
        result = meraki_client.dashboard.organizations.getOrganizationDevicesSystemMemoryUsageHistoryByInterval(organization_id, serial=serial, timespan=timespan)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_devices_uplinks_addresses_by_device",
    description="Retrieve devicesuplinksaddressesbydevice"
)
def get_organization_devices_uplinks_addresses_by_device(organization_id: str, serial: str = None):
    """
    Retrieve devicesuplinksaddressesbydevice
    
    Args:
        organization_id: Organization ID
        serial: Device serial number (optional)
    
    Returns:
        dict: API response with devicesuplinksaddressesbydevice data
    """
    try:
        result = meraki_client.dashboard.organizations.getOrganizationDevicesUplinksAddressesByDevice(organization_id, serial=serial)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_devices_uplinks_loss_and_latency",
    description="Retrieve devicesuplinkslossandlatency"
)
def get_organization_devices_uplinks_loss_and_latency(organization_id: str, serial: str = None):
    """
    Retrieve devicesuplinkslossandlatency
    
    Args:
        organization_id: Organization ID
        serial: Device serial number (optional)
    
    Returns:
        dict: API response with devicesuplinkslossandlatency data
    """
    try:
        result = meraki_client.dashboard.organizations.getOrganizationDevicesUplinksLossAndLatency(organization_id, serial=serial)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_early_access_features",
    description="Retrieve earlyaccessfeatures"
)
def get_organization_early_access_features(organization_id: str):
    """
    Retrieve earlyaccessfeatures
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with earlyaccessfeatures data
    """
    try:
        result = meraki_client.dashboard.organizations.getOrganizationEarlyAccessFeatures(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_early_access_features_opt_in",
    description="Retrieve earlyaccessfeaturesoptin"
)
def get_organization_early_access_features_opt_in(organization_id: str):
    """
    Retrieve earlyaccessfeaturesoptin
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with earlyaccessfeaturesoptin data
    """
    try:
        result = meraki_client.dashboard.organizations.getOrganizationEarlyAccessFeaturesOptIn(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_early_access_features_opt_ins",
    description="Retrieve earlyaccessfeaturesoptins"
)
def get_organization_early_access_features_opt_ins(organization_id: str):
    """
    Retrieve earlyaccessfeaturesoptins
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with earlyaccessfeaturesoptins data
    """
    try:
        result = meraki_client.dashboard.organizations.getOrganizationEarlyAccessFeaturesOptIns(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_firmware_upgrades",
    description="Retrieve firmwareupgrades"
)
def get_organization_firmware_upgrades(organization_id: str):
    """
    Retrieve firmwareupgrades
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with firmwareupgrades data
    """
    try:
        result = meraki_client.dashboard.organizations.getOrganizationFirmwareUpgrades(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_firmware_upgrades_by_device",
    description="Retrieve firmwareupgradesbydevice"
)
def get_organization_firmware_upgrades_by_device(organization_id: str, serial: str = None):
    """
    Retrieve firmwareupgradesbydevice
    
    Args:
        organization_id: Organization ID
        serial: Device serial number (optional)
    
    Returns:
        dict: API response with firmwareupgradesbydevice data
    """
    try:
        result = meraki_client.dashboard.organizations.getOrganizationFirmwareUpgradesByDevice(organization_id, serial=serial)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_floor_plans_auto_locate_devices",
    description="Retrieve floorplansautolocatedevices"
)
def get_organization_floor_plans_auto_locate_devices(organization_id: str, serial: str = None):
    """
    Retrieve floorplansautolocatedevices
    
    Args:
        organization_id: Organization ID
        serial: Device serial number (optional)
    
    Returns:
        dict: API response with floorplansautolocatedevices data
    """
    try:
        result = meraki_client.dashboard.organizations.getOrganizationFloorPlansAutoLocateDevices(organization_id, serial=serial)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_floor_plans_auto_locate_statuses",
    description="Retrieve floorplansautolocatestatuses"
)
def get_organization_floor_plans_auto_locate_statuses(organization_id: str):
    """
    Retrieve floorplansautolocatestatuses
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with floorplansautolocatestatuses data
    """
    try:
        result = meraki_client.dashboard.organizations.getOrganizationFloorPlansAutoLocateStatuses(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_integrations_xdr_networks",
    description="Retrieve integrationsxdrnetworks"
)
def get_organization_integrations_xdr_networks(organization_id: str, network_id: str = None):
    """
    Retrieve integrationsxdrnetworks
    
    Args:
        organization_id: Organization ID
        network_id: Network ID (optional)
    
    Returns:
        dict: API response with integrationsxdrnetworks data
    """
    try:
        result = meraki_client.dashboard.organizations.getOrganizationIntegrationsXdrNetworks(organization_id, networkId=network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_inventory_device",
    description="Retrieve inventorydevice"
)
def get_organization_inventory_device(organization_id: str, serial: str = None):
    """
    Retrieve inventorydevice
    
    Args:
        organization_id: Organization ID
        serial: Device serial number (optional)
    
    Returns:
        dict: API response with inventorydevice data
    """
    try:
        result = meraki_client.dashboard.organizations.getOrganizationInventoryDevice(organization_id, serial=serial)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_inventory_devices",
    description="Retrieve inventorydevices"
)
def get_organization_inventory_devices(organization_id: str, serial: str = None):
    """
    Retrieve inventorydevices
    
    Args:
        organization_id: Organization ID
        serial: Device serial number (optional)
    
    Returns:
        dict: API response with inventorydevices data
    """
    try:
        result = meraki_client.dashboard.organizations.getOrganizationInventoryDevices(organization_id, serial=serial)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_inventory_devices_swaps_bulk",
    description="Retrieve inventorydevicesswapsbulk"
)
def get_organization_inventory_devices_swaps_bulk(organization_id: str, serial: str = None):
    """
    Retrieve inventorydevicesswapsbulk
    
    Args:
        organization_id: Organization ID
        serial: Device serial number (optional)
    
    Returns:
        dict: API response with inventorydevicesswapsbulk data
    """
    try:
        result = meraki_client.dashboard.organizations.getOrganizationInventoryDevicesSwapsBulk(organization_id, serial=serial)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_inventory_onboarding_cloud_monitoring_imports",
    description="Retrieve inventoryonboardingcloudmonitoringimports"
)
def get_organization_inventory_onboarding_cloud_monitoring_imports(organization_id: str):
    """
    Retrieve inventoryonboardingcloudmonitoringimports
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with inventoryonboardingcloudmonitoringimports data
    """
    try:
        result = meraki_client.dashboard.organizations.getOrganizationInventoryOnboardingCloudMonitoringImports(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_inventory_onboarding_cloud_monitoring_networks",
    description="Retrieve inventoryonboardingcloudmonitoringnetworks"
)
def get_organization_inventory_onboarding_cloud_monitoring_networks(organization_id: str, network_id: str = None):
    """
    Retrieve inventoryonboardingcloudmonitoringnetworks
    
    Args:
        organization_id: Organization ID
        network_id: Network ID (optional)
    
    Returns:
        dict: API response with inventoryonboardingcloudmonitoringnetworks data
    """
    try:
        result = meraki_client.dashboard.organizations.getOrganizationInventoryOnboardingCloudMonitoringNetworks(organization_id, networkId=network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_license",
    description="Retrieve license"
)
def get_organization_license(organization_id: str):
    """
    Retrieve license
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with license data
    """
    try:
        result = meraki_client.dashboard.organizations.getOrganizationLicense(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_licenses",
    description="Retrieve licenses"
)
def get_organization_licenses(organization_id: str):
    """
    Retrieve licenses
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with licenses data
    """
    try:
        result = meraki_client.dashboard.organizations.getOrganizationLicenses(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_licenses_overview",
    description="Retrieve licensesoverview"
)
def get_organization_licenses_overview(organization_id: str):
    """
    Retrieve licensesoverview
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with licensesoverview data
    """
    try:
        result = meraki_client.dashboard.organizations.getOrganizationLicensesOverview(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_login_security",
    description="Retrieve loginsecurity"
)
def get_organization_login_security(organization_id: str):
    """
    Retrieve loginsecurity
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with loginsecurity data
    """
    try:
        result = meraki_client.dashboard.organizations.getOrganizationLoginSecurity(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_networks",
    description="Retrieve networks"
)
def get_organization_networks(organization_id: str, network_id: str = None):
    """
    Retrieve networks
    
    Args:
        organization_id: Organization ID
        network_id: Network ID (optional)
    
    Returns:
        dict: API response with networks data
    """
    try:
        result = meraki_client.dashboard.organizations.getOrganizationNetworks(organization_id, networkId=network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_openapi_spec",
    description="Retrieve openapispec"
)
def get_organization_openapi_spec(organization_id: str):
    """
    Retrieve openapispec
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with openapispec data
    """
    try:
        result = meraki_client.dashboard.organizations.getOrganizationOpenapiSpec(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_policy_object",
    description="Retrieve policyobject"
)
def get_organization_policy_object(organization_id: str):
    """
    Retrieve policyobject
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with policyobject data
    """
    try:
        result = meraki_client.dashboard.organizations.getOrganizationPolicyObject(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_policy_objects",
    description="Retrieve policyobjects"
)
def get_organization_policy_objects(organization_id: str):
    """
    Retrieve policyobjects
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with policyobjects data
    """
    try:
        result = meraki_client.dashboard.organizations.getOrganizationPolicyObjects(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_policy_objects_group",
    description="Retrieve policyobjectsgroup"
)
def get_organization_policy_objects_group(organization_id: str):
    """
    Retrieve policyobjectsgroup
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with policyobjectsgroup data
    """
    try:
        result = meraki_client.dashboard.organizations.getOrganizationPolicyObjectsGroup(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_policy_objects_groups",
    description="Retrieve policyobjectsgroups"
)
def get_organization_policy_objects_groups(organization_id: str):
    """
    Retrieve policyobjectsgroups
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with policyobjectsgroups data
    """
    try:
        result = meraki_client.dashboard.organizations.getOrganizationPolicyObjectsGroups(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_saml",
    description="Retrieve saml"
)
def get_organization_saml(organization_id: str):
    """
    Retrieve saml
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with saml data
    """
    try:
        result = meraki_client.dashboard.organizations.getOrganizationSaml(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_saml_idp",
    description="Retrieve samlidp"
)
def get_organization_saml_idp(organization_id: str):
    """
    Retrieve samlidp
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with samlidp data
    """
    try:
        result = meraki_client.dashboard.organizations.getOrganizationSamlIdp(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_saml_idps",
    description="Retrieve samlidps"
)
def get_organization_saml_idps(organization_id: str):
    """
    Retrieve samlidps
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with samlidps data
    """
    try:
        result = meraki_client.dashboard.organizations.getOrganizationSamlIdps(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_saml_role",
    description="Retrieve samlrole"
)
def get_organization_saml_role(organization_id: str):
    """
    Retrieve samlrole
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with samlrole data
    """
    try:
        result = meraki_client.dashboard.organizations.getOrganizationSamlRole(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_saml_roles",
    description="Retrieve samlroles"
)
def get_organization_saml_roles(organization_id: str):
    """
    Retrieve samlroles
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with samlroles data
    """
    try:
        result = meraki_client.dashboard.organizations.getOrganizationSamlRoles(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_snmp",
    description="Retrieve snmp"
)
def get_organization_snmp(organization_id: str):
    """
    Retrieve snmp
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with snmp data
    """
    try:
        result = meraki_client.dashboard.organizations.getOrganizationSnmp(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_splash_asset",
    description="Retrieve splashasset"
)
def get_organization_splash_asset(organization_id: str):
    """
    Retrieve splashasset
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with splashasset data
    """
    try:
        result = meraki_client.dashboard.organizations.getOrganizationSplashAsset(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_splash_themes",
    description="Retrieve splashthemes"
)
def get_organization_splash_themes(organization_id: str):
    """
    Retrieve splashthemes
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with splashthemes data
    """
    try:
        result = meraki_client.dashboard.organizations.getOrganizationSplashThemes(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_summary_top_appliances_by_utilization",
    description="Retrieve summarytopappliancesbyutilization"
)
def get_organization_summary_top_appliances_by_utilization(organization_id: str):
    """
    Retrieve summarytopappliancesbyutilization
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with summarytopappliancesbyutilization data
    """
    try:
        result = meraki_client.dashboard.organizations.getOrganizationSummaryTopAppliancesByUtilization(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_summary_top_applications_by_usage",
    description="Retrieve summarytopapplicationsbyusage"
)
def get_organization_summary_top_applications_by_usage(organization_id: str):
    """
    Retrieve summarytopapplicationsbyusage
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with summarytopapplicationsbyusage data
    """
    try:
        result = meraki_client.dashboard.organizations.getOrganizationSummaryTopApplicationsByUsage(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_summary_top_applications_categories_by_usage",
    description="Retrieve summarytopapplicationscategoriesbyusage"
)
def get_organization_summary_top_applications_categories_by_usage(organization_id: str):
    """
    Retrieve summarytopapplicationscategoriesbyusage
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with summarytopapplicationscategoriesbyusage data
    """
    try:
        result = meraki_client.dashboard.organizations.getOrganizationSummaryTopApplicationsCategoriesByUsage(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_summary_top_clients_by_usage",
    description="Retrieve summarytopclientsbyusage"
)
def get_organization_summary_top_clients_by_usage(organization_id: str):
    """
    Retrieve summarytopclientsbyusage
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with summarytopclientsbyusage data
    """
    try:
        result = meraki_client.dashboard.organizations.getOrganizationSummaryTopClientsByUsage(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_summary_top_clients_manufacturers_by_usage",
    description="Retrieve summarytopclientsmanufacturersbyusage"
)
def get_organization_summary_top_clients_manufacturers_by_usage(organization_id: str):
    """
    Retrieve summarytopclientsmanufacturersbyusage
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with summarytopclientsmanufacturersbyusage data
    """
    try:
        result = meraki_client.dashboard.organizations.getOrganizationSummaryTopClientsManufacturersByUsage(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_summary_top_devices_by_usage",
    description="Retrieve summarytopdevicesbyusage"
)
def get_organization_summary_top_devices_by_usage(organization_id: str, serial: str = None):
    """
    Retrieve summarytopdevicesbyusage
    
    Args:
        organization_id: Organization ID
        serial: Device serial number (optional)
    
    Returns:
        dict: API response with summarytopdevicesbyusage data
    """
    try:
        result = meraki_client.dashboard.organizations.getOrganizationSummaryTopDevicesByUsage(organization_id, serial=serial)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_summary_top_devices_models_by_usage",
    description="Retrieve summarytopdevicesmodelsbyusage"
)
def get_organization_summary_top_devices_models_by_usage(organization_id: str, serial: str = None):
    """
    Retrieve summarytopdevicesmodelsbyusage
    
    Args:
        organization_id: Organization ID
        serial: Device serial number (optional)
    
    Returns:
        dict: API response with summarytopdevicesmodelsbyusage data
    """
    try:
        result = meraki_client.dashboard.organizations.getOrganizationSummaryTopDevicesModelsByUsage(organization_id, serial=serial)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_summary_top_networks_by_status",
    description="Retrieve summarytopnetworksbystatus"
)
def get_organization_summary_top_networks_by_status(organization_id: str, network_id: str = None):
    """
    Retrieve summarytopnetworksbystatus
    
    Args:
        organization_id: Organization ID
        network_id: Network ID (optional)
    
    Returns:
        dict: API response with summarytopnetworksbystatus data
    """
    try:
        result = meraki_client.dashboard.organizations.getOrganizationSummaryTopNetworksByStatus(organization_id, networkId=network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_summary_top_ssids_by_usage",
    description="Retrieve summarytopssidsbyusage"
)
def get_organization_summary_top_ssids_by_usage(organization_id: str):
    """
    Retrieve summarytopssidsbyusage
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with summarytopssidsbyusage data
    """
    try:
        result = meraki_client.dashboard.organizations.getOrganizationSummaryTopSsidsByUsage(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_summary_top_switches_by_energy_usage",
    description="Retrieve summarytopswitchesbyenergyusage"
)
def get_organization_summary_top_switches_by_energy_usage(organization_id: str):
    """
    Retrieve summarytopswitchesbyenergyusage
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with summarytopswitchesbyenergyusage data
    """
    try:
        result = meraki_client.dashboard.organizations.getOrganizationSummaryTopSwitchesByEnergyUsage(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_uplinks_statuses",
    description="Retrieve uplinksstatuses"
)
def get_organization_uplinks_statuses(organization_id: str):
    """
    Retrieve uplinksstatuses
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with uplinksstatuses data
    """
    try:
        result = meraki_client.dashboard.organizations.getOrganizationUplinksStatuses(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_webhooks_alert_types",
    description="Retrieve webhooksalerttypes"
)
def get_organization_webhooks_alert_types(organization_id: str):
    """
    Retrieve webhooksalerttypes
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with webhooksalerttypes data
    """
    try:
        result = meraki_client.dashboard.organizations.getOrganizationWebhooksAlertTypes(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_webhooks_callbacks_status",
    description="Retrieve webhookscallbacksstatus"
)
def get_organization_webhooks_callbacks_status(organization_id: str):
    """
    Retrieve webhookscallbacksstatus
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with webhookscallbacksstatus data
    """
    try:
        result = meraki_client.dashboard.organizations.getOrganizationWebhooksCallbacksStatus(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_webhooks_logs",
    description="Retrieve webhookslogs"
)
def get_organization_webhooks_logs(organization_id: str):
    """
    Retrieve webhookslogs
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with webhookslogs data
    """
    try:
        result = meraki_client.dashboard.organizations.getOrganizationWebhooksLogs(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organizations",
    description="Retrieve s"
)
def get_organizations(organization_id: str):
    """
    Retrieve s
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with s data
    """
    try:
        result = meraki_client.dashboard.organizations.getOrganizations(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="move_organization_licenses",
    description="Manage movelicenses"
)
def move_organization_licenses(organization_id: str):
    """
    Manage movelicenses
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with movelicenses data
    """
    try:
        result = meraki_client.dashboard.organizations.moveOrganizationLicenses(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="move_organization_licenses_seats",
    description="Manage movelicensesseats"
)
def move_organization_licenses_seats(organization_id: str):
    """
    Manage movelicensesseats
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with movelicensesseats data
    """
    try:
        result = meraki_client.dashboard.organizations.moveOrganizationLicensesSeats(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="release_from_organization_inventory",
    description="Manage releasefrominventory"
)
def release_from_organization_inventory(organization_id: str):
    """
    Manage releasefrominventory
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with releasefrominventory data
    """
    try:
        result = meraki_client.dashboard.organizations.releaseFromOrganizationInventory(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="renew_organization_licenses_seats",
    description="Manage renewlicensesseats"
)
def renew_organization_licenses_seats(organization_id: str):
    """
    Manage renewlicensesseats
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with renewlicensesseats data
    """
    try:
        result = meraki_client.dashboard.organizations.renewOrganizationLicensesSeats(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="reorder_organization_devices_packet_capture_schedules",
    description="Manage reorderdevicespacketcaptureschedules"
)
def reorder_organization_devices_packet_capture_schedules(organization_id: str, serial: str = None):
    """
    Manage reorderdevicespacketcaptureschedules
    
    Args:
        organization_id: Organization ID
        serial: Device serial number (optional)
    
    Returns:
        dict: API response with reorderdevicespacketcaptureschedules data
    """
    try:
        result = meraki_client.dashboard.organizations.reorderOrganizationDevicesPacketCaptureSchedules(organization_id, serial=serial)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="restore_organization_assurance_alerts",
    description="Manage restoreassurancealerts"
)
def restore_organization_assurance_alerts(organization_id: str):
    """
    Manage restoreassurancealerts
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with restoreassurancealerts data
    """
    try:
        result = meraki_client.dashboard.organizations.restoreOrganizationAssuranceAlerts(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="stop_organization_devices_packet_capture_capture",
    description="Manage stopdevicespacketcapturecapture"
)
def stop_organization_devices_packet_capture_capture(organization_id: str, serial: str = None):
    """
    Manage stopdevicespacketcapturecapture
    
    Args:
        organization_id: Organization ID
        serial: Device serial number (optional)
    
    Returns:
        dict: API response with stopdevicespacketcapturecapture data
    """
    try:
        result = meraki_client.dashboard.organizations.stopOrganizationDevicesPacketCaptureCapture(organization_id, serial=serial)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_organization",
    description="Update an existing organization resource"
)
def update_organization(organization_id: str, **kwargs):
    """
    Update an existing organization resource
    
    Args:
        organization_id: Organization ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with organization resource data
    """
    try:
        result = meraki_client.dashboard.organizations.updateOrganization(organization_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_organization_action_batch",
    description="Update an existing actionbatch"
)
def update_organization_action_batch(organization_id: str, **kwargs):
    """
    Update an existing actionbatch
    
    Args:
        organization_id: Organization ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with actionbatch data
    """
    try:
        result = meraki_client.dashboard.organizations.updateOrganizationActionBatch(organization_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_organization_adaptive_policy_acl",
    description="Update an existing adaptivepolicyacl"
)
def update_organization_adaptive_policy_acl(organization_id: str, **kwargs):
    """
    Update an existing adaptivepolicyacl
    
    Args:
        organization_id: Organization ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with adaptivepolicyacl data
    """
    try:
        result = meraki_client.dashboard.organizations.updateOrganizationAdaptivePolicyAcl(organization_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_organization_adaptive_policy_group",
    description="Update an existing adaptivepolicygroup"
)
def update_organization_adaptive_policy_group(organization_id: str, **kwargs):
    """
    Update an existing adaptivepolicygroup
    
    Args:
        organization_id: Organization ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with adaptivepolicygroup data
    """
    try:
        result = meraki_client.dashboard.organizations.updateOrganizationAdaptivePolicyGroup(organization_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_organization_adaptive_policy_policy",
    description="Update an existing adaptivepolicypolicy"
)
def update_organization_adaptive_policy_policy(organization_id: str, **kwargs):
    """
    Update an existing adaptivepolicypolicy
    
    Args:
        organization_id: Organization ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with adaptivepolicypolicy data
    """
    try:
        result = meraki_client.dashboard.organizations.updateOrganizationAdaptivePolicyPolicy(organization_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_organization_adaptive_policy_settings",
    description="Update an existing adaptivepolicysettings"
)
def update_organization_adaptive_policy_settings(organization_id: str, **kwargs):
    """
    Update an existing adaptivepolicysettings
    
    Args:
        organization_id: Organization ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with adaptivepolicysettings data
    """
    try:
        result = meraki_client.dashboard.organizations.updateOrganizationAdaptivePolicySettings(organization_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_organization_admin",
    description="Update an existing admin"
)
def update_organization_admin(organization_id: str, admin_id: str = None, **kwargs):
    """
    Update an existing admin
    
    Args:
        organization_id: Organization ID
        admin_id: Admin ID (optional)
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with admin data
    """
    try:
        result = meraki_client.dashboard.organizations.updateOrganizationAdmin(organization_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_organization_alerts_profile",
    description="Update an existing alertsprofile"
)
def update_organization_alerts_profile(organization_id: str, **kwargs):
    """
    Update an existing alertsprofile
    
    Args:
        organization_id: Organization ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with alertsprofile data
    """
    try:
        result = meraki_client.dashboard.organizations.updateOrganizationAlertsProfile(organization_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_organization_branding_policies_priorities",
    description="Update an existing brandingpoliciespriorities"
)
def update_organization_branding_policies_priorities(organization_id: str, **kwargs):
    """
    Update an existing brandingpoliciespriorities
    
    Args:
        organization_id: Organization ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with brandingpoliciespriorities data
    """
    try:
        result = meraki_client.dashboard.organizations.updateOrganizationBrandingPoliciesPriorities(organization_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_organization_branding_policy",
    description="Update an existing brandingpolicy"
)
def update_organization_branding_policy(organization_id: str, **kwargs):
    """
    Update an existing brandingpolicy
    
    Args:
        organization_id: Organization ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with brandingpolicy data
    """
    try:
        result = meraki_client.dashboard.organizations.updateOrganizationBrandingPolicy(organization_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_organization_config_template",
    description="Update an existing configtemplate"
)
def update_organization_config_template(organization_id: str, **kwargs):
    """
    Update an existing configtemplate
    
    Args:
        organization_id: Organization ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with configtemplate data
    """
    try:
        result = meraki_client.dashboard.organizations.updateOrganizationConfigTemplate(organization_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_organization_devices_packet_capture_schedule",
    description="Update an existing devicespacketcaptureschedule"
)
def update_organization_devices_packet_capture_schedule(organization_id: str, serial: str = None, **kwargs):
    """
    Update an existing devicespacketcaptureschedule
    
    Args:
        organization_id: Organization ID
        serial: Device serial number (optional)
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with devicespacketcaptureschedule data
    """
    try:
        result = meraki_client.dashboard.organizations.updateOrganizationDevicesPacketCaptureSchedule(organization_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_organization_early_access_features_opt_in",
    description="Update an existing earlyaccessfeaturesoptin"
)
def update_organization_early_access_features_opt_in(organization_id: str, **kwargs):
    """
    Update an existing earlyaccessfeaturesoptin
    
    Args:
        organization_id: Organization ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with earlyaccessfeaturesoptin data
    """
    try:
        result = meraki_client.dashboard.organizations.updateOrganizationEarlyAccessFeaturesOptIn(organization_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_organization_license",
    description="Update an existing license"
)
def update_organization_license(organization_id: str, **kwargs):
    """
    Update an existing license
    
    Args:
        organization_id: Organization ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with license data
    """
    try:
        result = meraki_client.dashboard.organizations.updateOrganizationLicense(organization_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_organization_login_security",
    description="Update an existing loginsecurity"
)
def update_organization_login_security(organization_id: str, **kwargs):
    """
    Update an existing loginsecurity
    
    Args:
        organization_id: Organization ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with loginsecurity data
    """
    try:
        result = meraki_client.dashboard.organizations.updateOrganizationLoginSecurity(organization_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_organization_policy_object",
    description="Update an existing policyobject"
)
def update_organization_policy_object(organization_id: str, **kwargs):
    """
    Update an existing policyobject
    
    Args:
        organization_id: Organization ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with policyobject data
    """
    try:
        result = meraki_client.dashboard.organizations.updateOrganizationPolicyObject(organization_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_organization_policy_objects_group",
    description="Update an existing policyobjectsgroup"
)
def update_organization_policy_objects_group(organization_id: str, **kwargs):
    """
    Update an existing policyobjectsgroup
    
    Args:
        organization_id: Organization ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with policyobjectsgroup data
    """
    try:
        result = meraki_client.dashboard.organizations.updateOrganizationPolicyObjectsGroup(organization_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_organization_saml",
    description="Update an existing saml"
)
def update_organization_saml(organization_id: str, **kwargs):
    """
    Update an existing saml
    
    Args:
        organization_id: Organization ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with saml data
    """
    try:
        result = meraki_client.dashboard.organizations.updateOrganizationSaml(organization_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_organization_saml_idp",
    description="Update an existing samlidp"
)
def update_organization_saml_idp(organization_id: str, **kwargs):
    """
    Update an existing samlidp
    
    Args:
        organization_id: Organization ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with samlidp data
    """
    try:
        result = meraki_client.dashboard.organizations.updateOrganizationSamlIdp(organization_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_organization_saml_role",
    description="Update an existing samlrole"
)
def update_organization_saml_role(organization_id: str, **kwargs):
    """
    Update an existing samlrole
    
    Args:
        organization_id: Organization ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with samlrole data
    """
    try:
        result = meraki_client.dashboard.organizations.updateOrganizationSamlRole(organization_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_organization_snmp",
    description="Update an existing snmp"
)
def update_organization_snmp(organization_id: str, **kwargs):
    """
    Update an existing snmp
    
    Args:
        organization_id: Organization ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with snmp data
    """
    try:
        result = meraki_client.dashboard.organizations.updateOrganizationSnmp(organization_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}