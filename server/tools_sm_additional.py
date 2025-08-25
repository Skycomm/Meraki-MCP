"""
Additional Sm endpoints for Cisco Meraki MCP Server.
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

def register_sm_additional_tools(mcp_app, meraki):
    """Register additional sm tools with the MCP server."""
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    
    # Register all additional tools
    register_sm_additional_handlers()

def register_sm_additional_handlers():
    """Register additional sm tool handlers."""

    @app.tool(
        name="checkin_network_sm_devices",
        description="⚡ Execute network sm devices"
    )
    def checkin_network_sm_devices(network_id: str):
        """Execute network sm devices."""
        try:
            result = meraki_client.dashboard.sm.checkinNetworkSmDevices(
                network_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Sm Devices")
            elif isinstance(result, list):
                return format_list_response(result, "Network Sm Devices")
            else:
                return f"✅ Execute network sm devices completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="create_network_sm_bypass_activation_lock_attempt",
        description="➕ Create network sm bypass activation lock attempt"
    )
    def create_network_sm_bypass_activation_lock_attempt(network_id: str, **kwargs):
        """Create network sm bypass activation lock attempt."""
        try:
            result = meraki_client.dashboard.sm.createNetworkSmBypassActivationLockAttempt(
                network_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Sm Bypass Activation Lock Attempt")
            elif isinstance(result, list):
                return format_list_response(result, "Network Sm Bypass Activation Lock Attempt")
            else:
                return f"✅ Create network sm bypass activation lock attempt completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="create_network_sm_target_group",
        description="➕ Create network sm tar group"
    )
    def create_network_sm_target_group(network_id: str, **kwargs):
        """Create network sm tar group."""
        try:
            result = meraki_client.dashboard.sm.createNetworkSmTargetGroup(
                network_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Sm Tar Group")
            elif isinstance(result, list):
                return format_list_response(result, "Network Sm Tar Group")
            else:
                return f"✅ Create network sm tar group completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="create_organization_sm_admins_role",
        description="➕ Create organization sm admins role"
    )
    def create_organization_sm_admins_role(organization_id: str, **kwargs):
        """Create organization sm admins role."""
        try:
            result = meraki_client.dashboard.sm.createOrganizationSmAdminsRole(
                organization_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Sm Admins Role")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Sm Admins Role")
            else:
                return f"✅ Create organization sm admins role completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="delete_network_sm_target_group",
        description="🗑️ Delete network sm tar group"
    )
    def delete_network_sm_target_group(network_id: str):
        """Delete network sm tar group."""
        try:
            result = meraki_client.dashboard.sm.deleteNetworkSmTargetGroup(
                network_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Sm Tar Group")
            elif isinstance(result, list):
                return format_list_response(result, "Network Sm Tar Group")
            else:
                return f"✅ Delete network sm tar group completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="delete_network_sm_user_access_device",
        description="🗑️ Delete network sm user access device"
    )
    def delete_network_sm_user_access_device(network_id: str):
        """Delete network sm user access device."""
        try:
            result = meraki_client.dashboard.sm.deleteNetworkSmUserAccessDevice(
                network_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Sm User Access Device")
            elif isinstance(result, list):
                return format_list_response(result, "Network Sm User Access Device")
            else:
                return f"✅ Delete network sm user access device completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="delete_organization_sm_admins_role",
        description="🗑️ Delete organization sm admins role"
    )
    def delete_organization_sm_admins_role(organization_id: str):
        """Delete organization sm admins role."""
        try:
            result = meraki_client.dashboard.sm.deleteOrganizationSmAdminsRole(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Sm Admins Role")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Sm Admins Role")
            else:
                return f"✅ Delete organization sm admins role completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_network_sm_bypass_activation_lock_attempt",
        description="📊 Get network sm bypass activation lock attempt"
    )
    def get_network_sm_bypass_activation_lock_attempt(network_id: str):
        """Get network sm bypass activation lock attempt."""
        try:
            result = meraki_client.dashboard.sm.getNetworkSmBypassActivationLockAttempt(
                network_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Sm Bypass Activation Lock Attempt")
            elif isinstance(result, list):
                return format_list_response(result, "Network Sm Bypass Activation Lock Attempt")
            else:
                return f"✅ Get network sm bypass activation lock attempt completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_network_sm_device_cellular_usage_history",
        description="📊 Get network sm device cellular usage history"
    )
    def get_network_sm_device_cellular_usage_history(network_id: str):
        """Get network sm device cellular usage history."""
        try:
            result = meraki_client.dashboard.sm.getNetworkSmDeviceCellularUsageHistory(
                network_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Sm Device Cellular Usage History")
            elif isinstance(result, list):
                return format_list_response(result, "Network Sm Device Cellular Usage History")
            else:
                return f"✅ Get network sm device cellular usage history completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_network_sm_device_certs",
        description="📊 Get network sm device certs"
    )
    def get_network_sm_device_certs(network_id: str):
        """Get network sm device certs."""
        try:
            result = meraki_client.dashboard.sm.getNetworkSmDeviceCerts(
                network_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Sm Device Certs")
            elif isinstance(result, list):
                return format_list_response(result, "Network Sm Device Certs")
            else:
                return f"✅ Get network sm device certs completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_network_sm_device_connectivity",
        description="📊 Get network sm device connectivity"
    )
    def get_network_sm_device_connectivity(network_id: str):
        """Get network sm device connectivity."""
        try:
            result = meraki_client.dashboard.sm.getNetworkSmDeviceConnectivity(
                network_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Sm Device Connectivity")
            elif isinstance(result, list):
                return format_list_response(result, "Network Sm Device Connectivity")
            else:
                return f"✅ Get network sm device connectivity completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_network_sm_device_desktop_logs",
        description="📊 Get network sm device desktop logs"
    )
    def get_network_sm_device_desktop_logs(network_id: str):
        """Get network sm device desktop logs."""
        try:
            result = meraki_client.dashboard.sm.getNetworkSmDeviceDesktopLogs(
                network_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Sm Device Desktop Logs")
            elif isinstance(result, list):
                return format_list_response(result, "Network Sm Device Desktop Logs")
            else:
                return f"✅ Get network sm device desktop logs completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_network_sm_device_device_command_logs",
        description="📊 Get network sm device device command logs"
    )
    def get_network_sm_device_device_command_logs(network_id: str):
        """Get network sm device device command logs."""
        try:
            result = meraki_client.dashboard.sm.getNetworkSmDeviceDeviceCommandLogs(
                network_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Sm Device Device Command Logs")
            elif isinstance(result, list):
                return format_list_response(result, "Network Sm Device Device Command Logs")
            else:
                return f"✅ Get network sm device device command logs completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_network_sm_device_device_profiles",
        description="📊 Get network sm device device profiles"
    )
    def get_network_sm_device_device_profiles(network_id: str):
        """Get network sm device device profiles."""
        try:
            result = meraki_client.dashboard.sm.getNetworkSmDeviceDeviceProfiles(
                network_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Sm Device Device Profiles")
            elif isinstance(result, list):
                return format_list_response(result, "Network Sm Device Device Profiles")
            else:
                return f"✅ Get network sm device device profiles completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_network_sm_device_network_adapters",
        description="📊 Get network sm device network adapters"
    )
    def get_network_sm_device_network_adapters(network_id: str):
        """Get network sm device network adapters."""
        try:
            result = meraki_client.dashboard.sm.getNetworkSmDeviceNetworkAdapters(
                network_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Sm Device Network Adapters")
            elif isinstance(result, list):
                return format_list_response(result, "Network Sm Device Network Adapters")
            else:
                return f"✅ Get network sm device network adapters completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_network_sm_device_performance_history",
        description="📊 Get network sm device performance history"
    )
    def get_network_sm_device_performance_history(network_id: str):
        """Get network sm device performance history."""
        try:
            result = meraki_client.dashboard.sm.getNetworkSmDevicePerformanceHistory(
                network_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Sm Device Performance History")
            elif isinstance(result, list):
                return format_list_response(result, "Network Sm Device Performance History")
            else:
                return f"✅ Get network sm device performance history completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_network_sm_device_restrictions",
        description="📊 Get network sm device restrictions"
    )
    def get_network_sm_device_restrictions(network_id: str):
        """Get network sm device restrictions."""
        try:
            result = meraki_client.dashboard.sm.getNetworkSmDeviceRestrictions(
                network_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Sm Device Restrictions")
            elif isinstance(result, list):
                return format_list_response(result, "Network Sm Device Restrictions")
            else:
                return f"✅ Get network sm device restrictions completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_network_sm_device_security_centers",
        description="📊 Get network sm device security centers"
    )
    def get_network_sm_device_security_centers(network_id: str):
        """Get network sm device security centers."""
        try:
            result = meraki_client.dashboard.sm.getNetworkSmDeviceSecurityCenters(
                network_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Sm Device Security Centers")
            elif isinstance(result, list):
                return format_list_response(result, "Network Sm Device Security Centers")
            else:
                return f"✅ Get network sm device security centers completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_network_sm_device_softwares",
        description="📊 Get network sm device softwares"
    )
    def get_network_sm_device_softwares(network_id: str):
        """Get network sm device softwares."""
        try:
            result = meraki_client.dashboard.sm.getNetworkSmDeviceSoftwares(
                network_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Sm Device Softwares")
            elif isinstance(result, list):
                return format_list_response(result, "Network Sm Device Softwares")
            else:
                return f"✅ Get network sm device softwares completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_network_sm_device_wlan_lists",
        description="📊 Get network sm device wlan lists"
    )
    def get_network_sm_device_wlan_lists(network_id: str):
        """Get network sm device wlan lists."""
        try:
            result = meraki_client.dashboard.sm.getNetworkSmDeviceWlanLists(
                network_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Sm Device Wlan Lists")
            elif isinstance(result, list):
                return format_list_response(result, "Network Sm Device Wlan Lists")
            else:
                return f"✅ Get network sm device wlan lists completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_network_sm_target_group",
        description="📊 Get network sm tar group"
    )
    def get_network_sm_target_group(network_id: str):
        """Get network sm tar group."""
        try:
            result = meraki_client.dashboard.sm.getNetworkSmTargetGroup(
                network_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Sm Tar Group")
            elif isinstance(result, list):
                return format_list_response(result, "Network Sm Tar Group")
            else:
                return f"✅ Get network sm tar group completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_network_sm_target_groups",
        description="📊 Get network sm tar groups"
    )
    def get_network_sm_target_groups(network_id: str):
        """Get network sm tar groups."""
        try:
            result = meraki_client.dashboard.sm.getNetworkSmTargetGroups(
                network_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Sm Tar Groups")
            elif isinstance(result, list):
                return format_list_response(result, "Network Sm Tar Groups")
            else:
                return f"✅ Get network sm tar groups completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_network_sm_trusted_access_configs",
        description="📊 Get network sm trusted access configs"
    )
    def get_network_sm_trusted_access_configs(network_id: str):
        """Get network sm trusted access configs."""
        try:
            result = meraki_client.dashboard.sm.getNetworkSmTrustedAccessConfigs(
                network_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Sm Trusted Access Configs")
            elif isinstance(result, list):
                return format_list_response(result, "Network Sm Trusted Access Configs")
            else:
                return f"✅ Get network sm trusted access configs completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_network_sm_user_access_devices",
        description="📊 Get network sm user access devices"
    )
    def get_network_sm_user_access_devices(network_id: str):
        """Get network sm user access devices."""
        try:
            result = meraki_client.dashboard.sm.getNetworkSmUserAccessDevices(
                network_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Sm User Access Devices")
            elif isinstance(result, list):
                return format_list_response(result, "Network Sm User Access Devices")
            else:
                return f"✅ Get network sm user access devices completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_network_sm_user_device_profiles",
        description="📊 Get network sm user device profiles"
    )
    def get_network_sm_user_device_profiles(network_id: str):
        """Get network sm user device profiles."""
        try:
            result = meraki_client.dashboard.sm.getNetworkSmUserDeviceProfiles(
                network_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Sm User Device Profiles")
            elif isinstance(result, list):
                return format_list_response(result, "Network Sm User Device Profiles")
            else:
                return f"✅ Get network sm user device profiles completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_network_sm_user_softwares",
        description="📊 Get network sm user softwares"
    )
    def get_network_sm_user_softwares(network_id: str):
        """Get network sm user softwares."""
        try:
            result = meraki_client.dashboard.sm.getNetworkSmUserSoftwares(
                network_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Sm User Softwares")
            elif isinstance(result, list):
                return format_list_response(result, "Network Sm User Softwares")
            else:
                return f"✅ Get network sm user softwares completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_network_sm_users",
        description="📊 Get network sm users"
    )
    def get_network_sm_users(network_id: str):
        """Get network sm users."""
        try:
            result = meraki_client.dashboard.sm.getNetworkSmUsers(
                network_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Sm Users")
            elif isinstance(result, list):
                return format_list_response(result, "Network Sm Users")
            else:
                return f"✅ Get network sm users completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_sm_admins_role",
        description="📊 Get organization sm admins role"
    )
    def get_organization_sm_admins_role(organization_id: str):
        """Get organization sm admins role."""
        try:
            result = meraki_client.dashboard.sm.getOrganizationSmAdminsRole(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Sm Admins Role")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Sm Admins Role")
            else:
                return f"✅ Get organization sm admins role completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_sm_admins_roles",
        description="📊 Get organization sm admins roles"
    )
    def get_organization_sm_admins_roles(organization_id: str):
        """Get organization sm admins roles."""
        try:
            result = meraki_client.dashboard.sm.getOrganizationSmAdminsRoles(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Sm Admins Roles")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Sm Admins Roles")
            else:
                return f"✅ Get organization sm admins roles completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_sm_apns_cert",
        description="📊 Get organization sm apns cert"
    )
    def get_organization_sm_apns_cert(organization_id: str):
        """Get organization sm apns cert."""
        try:
            result = meraki_client.dashboard.sm.getOrganizationSmApnsCert(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Sm Apns Cert")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Sm Apns Cert")
            else:
                return f"✅ Get organization sm apns cert completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_sm_sentry_policies_assignments_by_network",
        description="📊 Get organization sm sentry policies assignments by network"
    )
    def get_organization_sm_sentry_policies_assignments_by_network(organization_id: str):
        """Get organization sm sentry policies assignments by network."""
        try:
            result = meraki_client.dashboard.sm.getOrganizationSmSentryPoliciesAssignmentsByNetwork(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Sm Sentry Policies Assignments By Network")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Sm Sentry Policies Assignments By Network")
            else:
                return f"✅ Get organization sm sentry policies assignments by network completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_sm_vpp_account",
        description="📊 Get organization sm vpp account"
    )
    def get_organization_sm_vpp_account(organization_id: str):
        """Get organization sm vpp account."""
        try:
            result = meraki_client.dashboard.sm.getOrganizationSmVppAccount(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Sm Vpp Account")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Sm Vpp Account")
            else:
                return f"✅ Get organization sm vpp account completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_sm_vpp_accounts",
        description="📊 Get organization sm vpp accounts"
    )
    def get_organization_sm_vpp_accounts(organization_id: str):
        """Get organization sm vpp accounts."""
        try:
            result = meraki_client.dashboard.sm.getOrganizationSmVppAccounts(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Sm Vpp Accounts")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Sm Vpp Accounts")
            else:
                return f"✅ Get organization sm vpp accounts completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="install_network_sm_device_apps",
        description="⚡ Execute network sm device apps"
    )
    def install_network_sm_device_apps(network_id: str):
        """Execute network sm device apps."""
        try:
            result = meraki_client.dashboard.sm.installNetworkSmDeviceApps(
                network_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Sm Device Apps")
            elif isinstance(result, list):
                return format_list_response(result, "Network Sm Device Apps")
            else:
                return f"✅ Execute network sm device apps completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="lock_network_sm_devices",
        description="⚡ Execute network sm devices"
    )
    def lock_network_sm_devices(network_id: str):
        """Execute network sm devices."""
        try:
            result = meraki_client.dashboard.sm.lockNetworkSmDevices(
                network_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Sm Devices")
            elif isinstance(result, list):
                return format_list_response(result, "Network Sm Devices")
            else:
                return f"✅ Execute network sm devices completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="modify_network_sm_devices_tags",
        description="⚡ Execute network sm devices tags"
    )
    def modify_network_sm_devices_tags(network_id: str):
        """Execute network sm devices tags."""
        try:
            result = meraki_client.dashboard.sm.modifyNetworkSmDevicesTags(
                network_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Sm Devices Tags")
            elif isinstance(result, list):
                return format_list_response(result, "Network Sm Devices Tags")
            else:
                return f"✅ Execute network sm devices tags completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="move_network_sm_devices",
        description="⚡ Execute network sm devices"
    )
    def move_network_sm_devices(network_id: str):
        """Execute network sm devices."""
        try:
            result = meraki_client.dashboard.sm.moveNetworkSmDevices(
                network_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Sm Devices")
            elif isinstance(result, list):
                return format_list_response(result, "Network Sm Devices")
            else:
                return f"✅ Execute network sm devices completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="refresh_network_sm_device_details",
        description="⚡ Execute network sm device details"
    )
    def refresh_network_sm_device_details(network_id: str):
        """Execute network sm device details."""
        try:
            result = meraki_client.dashboard.sm.refreshNetworkSmDeviceDetails(
                network_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Sm Device Details")
            elif isinstance(result, list):
                return format_list_response(result, "Network Sm Device Details")
            else:
                return f"✅ Execute network sm device details completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="shutdown_network_sm_devices",
        description="⚡ Execute network sm devices"
    )
    def shutdown_network_sm_devices(network_id: str):
        """Execute network sm devices."""
        try:
            result = meraki_client.dashboard.sm.shutdownNetworkSmDevices(
                network_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Sm Devices")
            elif isinstance(result, list):
                return format_list_response(result, "Network Sm Devices")
            else:
                return f"✅ Execute network sm devices completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="unenroll_network_sm_device",
        description="⚡ Execute network sm device"
    )
    def unenroll_network_sm_device(network_id: str):
        """Execute network sm device."""
        try:
            result = meraki_client.dashboard.sm.unenrollNetworkSmDevice(
                network_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Sm Device")
            elif isinstance(result, list):
                return format_list_response(result, "Network Sm Device")
            else:
                return f"✅ Execute network sm device completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="uninstall_network_sm_device_apps",
        description="⚡ Execute network sm device apps"
    )
    def uninstall_network_sm_device_apps(network_id: str):
        """Execute network sm device apps."""
        try:
            result = meraki_client.dashboard.sm.uninstallNetworkSmDeviceApps(
                network_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Sm Device Apps")
            elif isinstance(result, list):
                return format_list_response(result, "Network Sm Device Apps")
            else:
                return f"✅ Execute network sm device apps completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="update_network_sm_devices_fields",
        description="✏️ Update network sm devices fields"
    )
    def update_network_sm_devices_fields(network_id: str, **kwargs):
        """Update network sm devices fields."""
        try:
            result = meraki_client.dashboard.sm.updateNetworkSmDevicesFields(
                network_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Sm Devices Fields")
            elif isinstance(result, list):
                return format_list_response(result, "Network Sm Devices Fields")
            else:
                return f"✅ Update network sm devices fields completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="update_network_sm_target_group",
        description="✏️ Update network sm tar group"
    )
    def update_network_sm_target_group(network_id: str, **kwargs):
        """Update network sm tar group."""
        try:
            result = meraki_client.dashboard.sm.updateNetworkSmTargetGroup(
                network_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Sm Tar Group")
            elif isinstance(result, list):
                return format_list_response(result, "Network Sm Tar Group")
            else:
                return f"✅ Update network sm tar group completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="update_organization_sm_admins_role",
        description="✏️ Update organization sm admins role"
    )
    def update_organization_sm_admins_role(organization_id: str, **kwargs):
        """Update organization sm admins role."""
        try:
            result = meraki_client.dashboard.sm.updateOrganizationSmAdminsRole(
                organization_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Sm Admins Role")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Sm Admins Role")
            else:
                return f"✅ Update organization sm admins role completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="update_organization_sm_sentry_policies_assignments",
        description="✏️ Update organization sm sentry policies assignments"
    )
    def update_organization_sm_sentry_policies_assignments(organization_id: str, **kwargs):
        """Update organization sm sentry policies assignments."""
        try:
            result = meraki_client.dashboard.sm.updateOrganizationSmSentryPoliciesAssignments(
                organization_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Sm Sentry Policies Assignments")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Sm Sentry Policies Assignments")
            else:
                return f"✅ Update organization sm sentry policies assignments completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="wipe_network_sm_devices",
        description="⚡ Execute network sm devices"
    )
    def wipe_network_sm_devices(network_id: str):
        """Execute network sm devices."""
        try:
            result = meraki_client.dashboard.sm.wipeNetworkSmDevices(
                network_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Sm Devices")
            elif isinstance(result, list):
                return format_list_response(result, "Network Sm Devices")
            else:
                return f"✅ Execute network sm devices completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"
