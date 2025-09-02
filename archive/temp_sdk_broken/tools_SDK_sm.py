"""
Cisco Meraki MCP Server - Sm SDK Tools
Complete implementation of all 49 official Meraki Sm API methods.

This module provides 100% coverage of the Sm category from the official Meraki Dashboard API SDK.
Each tool corresponds directly to a method in the meraki.dashboard.sm namespace.
"""

# Import removed to avoid circular import
import meraki


def register_sm_tools(app, meraki_client):
    """Register all sm SDK tools."""
    print(f"📱 Registering 49 sm SDK tools...")


@app.tool(
    name="checkin_network_sm_devices",
    description="Manage checkinsms"
)
def checkin_network_sm_devices():
    """
    Manage checkinsms
    
    Args:

    
    Returns:
        dict: API response with checkinsms data
    """
    try:
        result = meraki_client.dashboard.sm.checkinNetworkSmDevices()
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="create_network_sm_bypass_activation_lock_attempt",
    description="Create smbypassactivationlockattempt"
)
def create_network_sm_bypass_activation_lock_attempt(network_id: str, **kwargs):
    """
    Create smbypassactivationlockattempt
    
    Args:
        network_id: Network ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with smbypassactivationlockattempt data
    """
    try:
        result = meraki_client.dashboard.sm.createNetworkSmBypassActivationLockAttempt(network_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="create_network_sm_target_group",
    description="Create smtargroup"
)
def create_network_sm_target_group(network_id: str, **kwargs):
    """
    Create smtargroup
    
    Args:
        network_id: Network ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with smtargroup data
    """
    try:
        result = meraki_client.dashboard.sm.createNetworkSmTargetGroup(network_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="create_organization_sm_admins_role",
    description="Create smadminsrole"
)
def create_organization_sm_admins_role(organization_id: str, **kwargs):
    """
    Create smadminsrole
    
    Args:
        organization_id: Organization ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with smadminsrole data
    """
    try:
        result = meraki_client.dashboard.sm.createOrganizationSmAdminsRole(organization_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="delete_network_sm_target_group",
    description="Delete smtargroup"
)
def delete_network_sm_target_group(network_id: str):
    """
    Delete smtargroup
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with smtargroup data
    """
    try:
        result = meraki_client.dashboard.sm.deleteNetworkSmTargetGroup(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="delete_network_sm_user_access_device",
    description="Delete smuseraccess"
)
def delete_network_sm_user_access_device(network_id: str):
    """
    Delete smuseraccess
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with smuseraccess data
    """
    try:
        result = meraki_client.dashboard.sm.deleteNetworkSmUserAccessDevice(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="delete_organization_sm_admins_role",
    description="Delete smadminsrole"
)
def delete_organization_sm_admins_role(organization_id: str):
    """
    Delete smadminsrole
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with smadminsrole data
    """
    try:
        result = meraki_client.dashboard.sm.deleteOrganizationSmAdminsRole(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_sm_bypass_activation_lock_attempt",
    description="Retrieve smbypassactivationlockattempt"
)
def get_network_sm_bypass_activation_lock_attempt(network_id: str):
    """
    Retrieve smbypassactivationlockattempt
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with smbypassactivationlockattempt data
    """
    try:
        result = meraki_client.dashboard.sm.getNetworkSmBypassActivationLockAttempt(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_sm_device_cellular_usage_history",
    description="Retrieve smcellularusagehistory"
)
def get_network_sm_device_cellular_usage_history(network_id: str, timespan: int = 86400):
    """
    Retrieve smcellularusagehistory
    
    Args:
        network_id: Network ID
        timespan: Timespan in seconds (default: 86400)
    
    Returns:
        dict: API response with smcellularusagehistory data
    """
    try:
        result = meraki_client.dashboard.sm.getNetworkSmDeviceCellularUsageHistory(network_id, timespan=timespan)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_sm_device_certs",
    description="Retrieve smcerts"
)
def get_network_sm_device_certs(network_id: str):
    """
    Retrieve smcerts
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with smcerts data
    """
    try:
        result = meraki_client.dashboard.sm.getNetworkSmDeviceCerts(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_sm_device_connectivity",
    description="Retrieve smconnectivity"
)
def get_network_sm_device_connectivity(network_id: str):
    """
    Retrieve smconnectivity
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with smconnectivity data
    """
    try:
        result = meraki_client.dashboard.sm.getNetworkSmDeviceConnectivity(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_sm_device_desktop_logs",
    description="Retrieve smdesktoplogs"
)
def get_network_sm_device_desktop_logs(network_id: str):
    """
    Retrieve smdesktoplogs
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with smdesktoplogs data
    """
    try:
        result = meraki_client.dashboard.sm.getNetworkSmDeviceDesktopLogs(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_sm_device_device_command_logs",
    description="Retrieve smcommandlogs"
)
def get_network_sm_device_device_command_logs(network_id: str):
    """
    Retrieve smcommandlogs
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with smcommandlogs data
    """
    try:
        result = meraki_client.dashboard.sm.getNetworkSmDeviceDeviceCommandLogs(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_sm_device_device_profiles",
    description="Retrieve smprofiles"
)
def get_network_sm_device_device_profiles(network_id: str):
    """
    Retrieve smprofiles
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with smprofiles data
    """
    try:
        result = meraki_client.dashboard.sm.getNetworkSmDeviceDeviceProfiles(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_sm_device_network_adapters",
    description="Retrieve smadapters"
)
def get_network_sm_device_network_adapters(network_id: str):
    """
    Retrieve smadapters
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with smadapters data
    """
    try:
        result = meraki_client.dashboard.sm.getNetworkSmDeviceNetworkAdapters(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_sm_device_performance_history",
    description="Retrieve smperformancehistory"
)
def get_network_sm_device_performance_history(network_id: str, timespan: int = 86400):
    """
    Retrieve smperformancehistory
    
    Args:
        network_id: Network ID
        timespan: Timespan in seconds (default: 86400)
    
    Returns:
        dict: API response with smperformancehistory data
    """
    try:
        result = meraki_client.dashboard.sm.getNetworkSmDevicePerformanceHistory(network_id, timespan=timespan)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_sm_device_restrictions",
    description="Retrieve smrestrictions"
)
def get_network_sm_device_restrictions(network_id: str):
    """
    Retrieve smrestrictions
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with smrestrictions data
    """
    try:
        result = meraki_client.dashboard.sm.getNetworkSmDeviceRestrictions(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_sm_device_security_centers",
    description="Retrieve smsecuritycenters"
)
def get_network_sm_device_security_centers(network_id: str):
    """
    Retrieve smsecuritycenters
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with smsecuritycenters data
    """
    try:
        result = meraki_client.dashboard.sm.getNetworkSmDeviceSecurityCenters(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_sm_device_softwares",
    description="Retrieve smsoftwares"
)
def get_network_sm_device_softwares(network_id: str):
    """
    Retrieve smsoftwares
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with smsoftwares data
    """
    try:
        result = meraki_client.dashboard.sm.getNetworkSmDeviceSoftwares(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_sm_device_wlan_lists",
    description="Retrieve smwlanlists"
)
def get_network_sm_device_wlan_lists(network_id: str):
    """
    Retrieve smwlanlists
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with smwlanlists data
    """
    try:
        result = meraki_client.dashboard.sm.getNetworkSmDeviceWlanLists(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_sm_devices",
    description="Retrieve sms"
)
def get_network_sm_devices(network_id: str):
    """
    Retrieve sms
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with sms data
    """
    try:
        result = meraki_client.dashboard.sm.getNetworkSmDevices(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_sm_profiles",
    description="Retrieve smprofiles"
)
def get_network_sm_profiles(network_id: str):
    """
    Retrieve smprofiles
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with smprofiles data
    """
    try:
        result = meraki_client.dashboard.sm.getNetworkSmProfiles(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_sm_target_group",
    description="Retrieve smtargroup"
)
def get_network_sm_target_group(network_id: str):
    """
    Retrieve smtargroup
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with smtargroup data
    """
    try:
        result = meraki_client.dashboard.sm.getNetworkSmTargetGroup(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_sm_target_groups",
    description="Retrieve smtargroups"
)
def get_network_sm_target_groups(network_id: str):
    """
    Retrieve smtargroups
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with smtargroups data
    """
    try:
        result = meraki_client.dashboard.sm.getNetworkSmTargetGroups(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_sm_trusted_access_configs",
    description="Retrieve smtrustedaccessconfigs"
)
def get_network_sm_trusted_access_configs(network_id: str):
    """
    Retrieve smtrustedaccessconfigs
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with smtrustedaccessconfigs data
    """
    try:
        result = meraki_client.dashboard.sm.getNetworkSmTrustedAccessConfigs(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_sm_user_access_devices",
    description="Retrieve smuseraccesss"
)
def get_network_sm_user_access_devices(network_id: str):
    """
    Retrieve smuseraccesss
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with smuseraccesss data
    """
    try:
        result = meraki_client.dashboard.sm.getNetworkSmUserAccessDevices(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_sm_user_device_profiles",
    description="Retrieve smuserprofiles"
)
def get_network_sm_user_device_profiles(network_id: str):
    """
    Retrieve smuserprofiles
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with smuserprofiles data
    """
    try:
        result = meraki_client.dashboard.sm.getNetworkSmUserDeviceProfiles(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_sm_user_softwares",
    description="Retrieve smusersoftwares"
)
def get_network_sm_user_softwares(network_id: str):
    """
    Retrieve smusersoftwares
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with smusersoftwares data
    """
    try:
        result = meraki_client.dashboard.sm.getNetworkSmUserSoftwares(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_sm_users",
    description="Retrieve smusers"
)
def get_network_sm_users(network_id: str):
    """
    Retrieve smusers
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with smusers data
    """
    try:
        result = meraki_client.dashboard.sm.getNetworkSmUsers(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_sm_admins_role",
    description="Retrieve smadminsrole"
)
def get_organization_sm_admins_role(organization_id: str):
    """
    Retrieve smadminsrole
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with smadminsrole data
    """
    try:
        result = meraki_client.dashboard.sm.getOrganizationSmAdminsRole(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_sm_admins_roles",
    description="Retrieve smadminsroles"
)
def get_organization_sm_admins_roles(organization_id: str):
    """
    Retrieve smadminsroles
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with smadminsroles data
    """
    try:
        result = meraki_client.dashboard.sm.getOrganizationSmAdminsRoles(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_sm_apns_cert",
    description="Retrieve smapnscert"
)
def get_organization_sm_apns_cert(organization_id: str):
    """
    Retrieve smapnscert
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with smapnscert data
    """
    try:
        result = meraki_client.dashboard.sm.getOrganizationSmApnsCert(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_sm_sentry_policies_assignments_by_network",
    description="Retrieve smsentrypoliciesassignmentsby"
)
def get_organization_sm_sentry_policies_assignments_by_network(organization_id: str):
    """
    Retrieve smsentrypoliciesassignmentsby
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with smsentrypoliciesassignmentsby data
    """
    try:
        result = meraki_client.dashboard.sm.getOrganizationSmSentryPoliciesAssignmentsByNetwork(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_sm_vpp_account",
    description="Retrieve smvppaccount"
)
def get_organization_sm_vpp_account(organization_id: str):
    """
    Retrieve smvppaccount
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with smvppaccount data
    """
    try:
        result = meraki_client.dashboard.sm.getOrganizationSmVppAccount(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_sm_vpp_accounts",
    description="Retrieve smvppaccounts"
)
def get_organization_sm_vpp_accounts(organization_id: str):
    """
    Retrieve smvppaccounts
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with smvppaccounts data
    """
    try:
        result = meraki_client.dashboard.sm.getOrganizationSmVppAccounts(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="install_network_sm_device_apps",
    description="Manage installsmapps"
)
def install_network_sm_device_apps():
    """
    Manage installsmapps
    
    Args:

    
    Returns:
        dict: API response with installsmapps data
    """
    try:
        result = meraki_client.dashboard.sm.installNetworkSmDeviceApps()
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="lock_network_sm_devices",
    description="Manage locksms"
)
def lock_network_sm_devices():
    """
    Manage locksms
    
    Args:

    
    Returns:
        dict: API response with locksms data
    """
    try:
        result = meraki_client.dashboard.sm.lockNetworkSmDevices()
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="modify_network_sm_devices_tags",
    description="Manage modifysmstags"
)
def modify_network_sm_devices_tags():
    """
    Manage modifysmstags
    
    Args:

    
    Returns:
        dict: API response with modifysmstags data
    """
    try:
        result = meraki_client.dashboard.sm.modifyNetworkSmDevicesTags()
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="move_network_sm_devices",
    description="Manage movesms"
)
def move_network_sm_devices():
    """
    Manage movesms
    
    Args:

    
    Returns:
        dict: API response with movesms data
    """
    try:
        result = meraki_client.dashboard.sm.moveNetworkSmDevices()
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="reboot_network_sm_devices",
    description="Manage rebootsms"
)
def reboot_network_sm_devices():
    """
    Manage rebootsms
    
    Args:

    
    Returns:
        dict: API response with rebootsms data
    """
    try:
        result = meraki_client.dashboard.sm.rebootNetworkSmDevices()
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="refresh_network_sm_device_details",
    description="Manage refreshsmdetails"
)
def refresh_network_sm_device_details():
    """
    Manage refreshsmdetails
    
    Args:

    
    Returns:
        dict: API response with refreshsmdetails data
    """
    try:
        result = meraki_client.dashboard.sm.refreshNetworkSmDeviceDetails()
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="shutdown_network_sm_devices",
    description="Manage shutdownsms"
)
def shutdown_network_sm_devices():
    """
    Manage shutdownsms
    
    Args:

    
    Returns:
        dict: API response with shutdownsms data
    """
    try:
        result = meraki_client.dashboard.sm.shutdownNetworkSmDevices()
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="unenroll_network_sm_device",
    description="Manage unenrollsm"
)
def unenroll_network_sm_device():
    """
    Manage unenrollsm
    
    Args:

    
    Returns:
        dict: API response with unenrollsm data
    """
    try:
        result = meraki_client.dashboard.sm.unenrollNetworkSmDevice()
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="uninstall_network_sm_device_apps",
    description="Manage uninstallsmapps"
)
def uninstall_network_sm_device_apps():
    """
    Manage uninstallsmapps
    
    Args:

    
    Returns:
        dict: API response with uninstallsmapps data
    """
    try:
        result = meraki_client.dashboard.sm.uninstallNetworkSmDeviceApps()
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_network_sm_devices_fields",
    description="Update smsfields"
)
def update_network_sm_devices_fields(network_id: str, **kwargs):
    """
    Update smsfields
    
    Args:
        network_id: Network ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with smsfields data
    """
    try:
        result = meraki_client.dashboard.sm.updateNetworkSmDevicesFields(network_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_network_sm_target_group",
    description="Update smtargroup"
)
def update_network_sm_target_group(network_id: str, **kwargs):
    """
    Update smtargroup
    
    Args:
        network_id: Network ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with smtargroup data
    """
    try:
        result = meraki_client.dashboard.sm.updateNetworkSmTargetGroup(network_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_organization_sm_admins_role",
    description="Update smadminsrole"
)
def update_organization_sm_admins_role(organization_id: str, **kwargs):
    """
    Update smadminsrole
    
    Args:
        organization_id: Organization ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with smadminsrole data
    """
    try:
        result = meraki_client.dashboard.sm.updateOrganizationSmAdminsRole(organization_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_organization_sm_sentry_policies_assignments",
    description="Update smsentrypoliciesassignments"
)
def update_organization_sm_sentry_policies_assignments(organization_id: str, **kwargs):
    """
    Update smsentrypoliciesassignments
    
    Args:
        organization_id: Organization ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with smsentrypoliciesassignments data
    """
    try:
        result = meraki_client.dashboard.sm.updateOrganizationSmSentryPoliciesAssignments(organization_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="wipe_network_sm_devices",
    description="Manage wipesms"
)
def wipe_network_sm_devices():
    """
    Manage wipesms
    
    Args:

    
    Returns:
        dict: API response with wipesms data
    """
    try:
        result = meraki_client.dashboard.sm.wipeNetworkSmDevices()
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}