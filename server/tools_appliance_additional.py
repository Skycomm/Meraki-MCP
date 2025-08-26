"""
Additional Appliance endpoints for Cisco Meraki MCP Server.
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

def register_appliance_additional_tools(mcp_app, meraki):
    """Register additional appliance tools with the MCP server."""
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    
    # Register all additional tools
    register_appliance_additional_handlers()

def register_appliance_additional_handlers():
    """Register additional appliance tool handlers."""

    @app.tool(
        name="bulk_org_appliance_dns_local_profiles_assignments_create",
        description="⚡ Execute organization appliance dns local profiles assignments create"
    )
    def bulk_organization_appliance_dns_local_profiles_assignments_create(organization_id: str):
        """Execute organization appliance dns local profiles assignments create."""
        try:
            result = meraki_client.dashboard.appliance.bulkOrganizationApplianceDnsLocalProfilesAssignmentsCreate(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Appliance Dns Local Profiles Assignments Create")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Appliance Dns Local Profiles Assignments Create")
            else:
                return f"✅ Execute organization appliance dns local profiles assignments create completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="create_device_appliance_vmx_authentication_token",
        description="➕ Create device appliance vmx authentication token"
    )
    def create_device_appliance_vmx_authentication_token(serial: str, **kwargs):
        """Create device appliance vmx authentication token."""
        try:
            result = meraki_client.dashboard.appliance.createDeviceApplianceVmxAuthenticationToken(
                serial, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Device Appliance Vmx Authentication Token")
            elif isinstance(result, list):
                return format_list_response(result, "Device Appliance Vmx Authentication Token")
            else:
                return f"✅ Create device appliance vmx authentication token completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="create_network_appliance_prefixes_delegated_static",
        description="➕ Create network appliance prefixes delegated static"
    )
    def create_network_appliance_prefixes_delegated_static(network_id: str, **kwargs):
        """Create network appliance prefixes delegated static."""
        try:
            result = meraki_client.dashboard.appliance.createNetworkAppliancePrefixesDelegatedStatic(
                network_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Appliance Prefixes Delegated Static")
            elif isinstance(result, list):
                return format_list_response(result, "Network Appliance Prefixes Delegated Static")
            else:
                return f"✅ Create network appliance prefixes delegated static completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="create_network_appliance_rf_profile",
        description="➕ Create network appliance rf profile"
    )
    def create_network_appliance_rf_profile(network_id: str, **kwargs):
        """Create network appliance rf profile."""
        try:
            result = meraki_client.dashboard.appliance.createNetworkApplianceRfProfile(
                network_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Appliance Rf Profile")
            elif isinstance(result, list):
                return format_list_response(result, "Network Appliance Rf Profile")
            else:
                return f"✅ Create network appliance rf profile completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="create_network_app_traffic_shaping_custom_performance_class",
        description="➕ Create network appliance traffic shaping custom performance class"
    )
    def create_network_appliance_traffic_shaping_custom_performance_class(network_id: str, **kwargs):
        """Create network appliance traffic shaping custom performance class."""
        try:
            result = meraki_client.dashboard.appliance.createNetworkApplianceTrafficShapingCustomPerformanceClass(
                network_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Appliance Traffic Shaping Custom Performance Class")
            elif isinstance(result, list):
                return format_list_response(result, "Network Appliance Traffic Shaping Custom Performance Class")
            else:
                return f"✅ Create network appliance traffic shaping custom performance class completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="create_organization_appliance_dns_local_profile",
        description="➕ Create organization appliance dns local profile"
    )
    def create_organization_appliance_dns_local_profile(organization_id: str, **kwargs):
        """Create organization appliance dns local profile."""
        try:
            result = meraki_client.dashboard.appliance.createOrganizationApplianceDnsLocalProfile(
                organization_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Appliance Dns Local Profile")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Appliance Dns Local Profile")
            else:
                return f"✅ Create organization appliance dns local profile completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="create_org_appliance_dns_local_profiles_assignments_bulk_delete",
        description="➕ Create organization appliance dns local profiles assignments bulk delete"
    )
    def create_organization_appliance_dns_local_profiles_assignments_bulk_delete(organization_id: str, **kwargs):
        """Create organization appliance dns local profiles assignments bulk delete."""
        try:
            result = meraki_client.dashboard.appliance.createOrganizationApplianceDnsLocalProfilesAssignmentsBulkDelete(
                organization_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Appliance Dns Local Profiles Assignments Bulk Delete")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Appliance Dns Local Profiles Assignments Bulk Delete")
            else:
                return f"✅ Create organization appliance dns local profiles assignments bulk delete completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="create_organization_appliance_dns_local_record",
        description="➕ Create organization appliance dns local record"
    )
    def create_organization_appliance_dns_local_record(organization_id: str, **kwargs):
        """Create organization appliance dns local record."""
        try:
            result = meraki_client.dashboard.appliance.createOrganizationApplianceDnsLocalRecord(
                organization_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Appliance Dns Local Record")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Appliance Dns Local Record")
            else:
                return f"✅ Create organization appliance dns local record completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="create_organization_appliance_dns_split_profile",
        description="➕ Create organization appliance dns split profile"
    )
    def create_organization_appliance_dns_split_profile(organization_id: str, **kwargs):
        """Create organization appliance dns split profile."""
        try:
            result = meraki_client.dashboard.appliance.createOrganizationApplianceDnsSplitProfile(
                organization_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Appliance Dns Split Profile")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Appliance Dns Split Profile")
            else:
                return f"✅ Create organization appliance dns split profile completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="create_org_appliance_dns_split_profiles_assignments_bulk_create",
        description="➕ Create organization appliance dns split profiles assignments bulk create"
    )
    def create_organization_appliance_dns_split_profiles_assignments_bulk_create(organization_id: str, **kwargs):
        """Create organization appliance dns split profiles assignments bulk create."""
        try:
            result = meraki_client.dashboard.appliance.createOrganizationApplianceDnsSplitProfilesAssignmentsBulkCreate(
                organization_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Appliance Dns Split Profiles Assignments Bulk Create")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Appliance Dns Split Profiles Assignments Bulk Create")
            else:
                return f"✅ Create organization appliance dns split profiles assignments bulk create completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="create_org_appliance_dns_split_profiles_assignments_bulk_delete",
        description="➕ Create organization appliance dns split profiles assignments bulk delete"
    )
    def create_organization_appliance_dns_split_profiles_assignments_bulk_delete(organization_id: str, **kwargs):
        """Create organization appliance dns split profiles assignments bulk delete."""
        try:
            result = meraki_client.dashboard.appliance.createOrganizationApplianceDnsSplitProfilesAssignmentsBulkDelete(
                organization_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Appliance Dns Split Profiles Assignments Bulk Delete")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Appliance Dns Split Profiles Assignments Bulk Delete")
            else:
                return f"✅ Create organization appliance dns split profiles assignments bulk delete completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="delete_network_appliance_prefixes_delegated_static",
        description="🗑️ Delete network appliance prefixes delegated static"
    )
    def delete_network_appliance_prefixes_delegated_static(network_id: str):
        """Delete network appliance prefixes delegated static."""
        try:
            result = meraki_client.dashboard.appliance.deleteNetworkAppliancePrefixesDelegatedStatic(
                network_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Appliance Prefixes Delegated Static")
            elif isinstance(result, list):
                return format_list_response(result, "Network Appliance Prefixes Delegated Static")
            else:
                return f"✅ Delete network appliance prefixes delegated static completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="delete_network_appliance_rf_profile",
        description="🗑️ Delete network appliance rf profile"
    )
    def delete_network_appliance_rf_profile(network_id: str):
        """Delete network appliance rf profile."""
        try:
            result = meraki_client.dashboard.appliance.deleteNetworkApplianceRfProfile(
                network_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Appliance Rf Profile")
            elif isinstance(result, list):
                return format_list_response(result, "Network Appliance Rf Profile")
            else:
                return f"✅ Delete network appliance rf profile completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="delete_network_app_traffic_shaping_custom_performance_class",
        description="🗑️ Delete network appliance traffic shaping custom performance class"
    )
    def delete_network_appliance_traffic_shaping_custom_performance_class(network_id: str):
        """Delete network appliance traffic shaping custom performance class."""
        try:
            result = meraki_client.dashboard.appliance.deleteNetworkApplianceTrafficShapingCustomPerformanceClass(
                network_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Appliance Traffic Shaping Custom Performance Class")
            elif isinstance(result, list):
                return format_list_response(result, "Network Appliance Traffic Shaping Custom Performance Class")
            else:
                return f"✅ Delete network appliance traffic shaping custom performance class completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="delete_organization_appliance_dns_local_profile",
        description="🗑️ Delete organization appliance dns local profile"
    )
    def delete_organization_appliance_dns_local_profile(organization_id: str):
        """Delete organization appliance dns local profile."""
        try:
            result = meraki_client.dashboard.appliance.deleteOrganizationApplianceDnsLocalProfile(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Appliance Dns Local Profile")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Appliance Dns Local Profile")
            else:
                return f"✅ Delete organization appliance dns local profile completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="delete_organization_appliance_dns_local_record",
        description="🗑️ Delete organization appliance dns local record"
    )
    def delete_organization_appliance_dns_local_record(organization_id: str):
        """Delete organization appliance dns local record."""
        try:
            result = meraki_client.dashboard.appliance.deleteOrganizationApplianceDnsLocalRecord(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Appliance Dns Local Record")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Appliance Dns Local Record")
            else:
                return f"✅ Delete organization appliance dns local record completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="delete_organization_appliance_dns_split_profile",
        description="🗑️ Delete organization appliance dns split profile"
    )
    def delete_organization_appliance_dns_split_profile(organization_id: str):
        """Delete organization appliance dns split profile."""
        try:
            result = meraki_client.dashboard.appliance.deleteOrganizationApplianceDnsSplitProfile(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Appliance Dns Split Profile")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Appliance Dns Split Profile")
            else:
                return f"✅ Delete organization appliance dns split profile completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_device_appliance_prefixes_delegated_vlan_assignments",
        description="📊 Get device appliance prefixes delegated vlan assignments"
    )
    def get_device_appliance_prefixes_delegated_vlan_assignments(serial: str):
        """Get device appliance prefixes delegated vlan assignments."""
        try:
            result = meraki_client.dashboard.appliance.getDeviceAppliancePrefixesDelegatedVlanAssignments(
                serial
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Device Appliance Prefixes Delegated Vlan Assignments")
            elif isinstance(result, list):
                return format_list_response(result, "Device Appliance Prefixes Delegated Vlan Assignments")
            else:
                return f"✅ Get device appliance prefixes delegated vlan assignments completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_device_appliance_radio_settings",
        description="📊 Get device appliance radio settings"
    )
    def get_device_appliance_radio_settings(serial: str):
        """Get device appliance radio settings."""
        try:
            result = meraki_client.dashboard.appliance.getDeviceApplianceRadioSettings(
                serial
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Device Appliance Radio Settings")
            elif isinstance(result, list):
                return format_list_response(result, "Device Appliance Radio Settings")
            else:
                return f"✅ Get device appliance radio settings completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_network_appliance_client_security_events",
        description="📊 Get network appliance client security events"
    )
    def get_network_appliance_client_security_events(network_id: str):
        """Get network appliance client security events."""
        try:
            result = meraki_client.dashboard.appliance.getNetworkApplianceClientSecurityEvents(
                network_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Appliance Client Security Events")
            elif isinstance(result, list):
                return format_list_response(result, "Network Appliance Client Security Events")
            else:
                return f"✅ Get network appliance client security events completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_network_appliance_content_filtering_categories",
        description="📊 Get network appliance content filtering categories"
    )
    def get_network_appliance_content_filtering_categories(network_id: str):
        """Get network appliance content filtering categories."""
        try:
            result = meraki_client.dashboard.appliance.getNetworkApplianceContentFilteringCategories(
                network_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Appliance Content Filtering Categories")
            elif isinstance(result, list):
                return format_list_response(result, "Network Appliance Content Filtering Categories")
            else:
                return f"✅ Get network appliance content filtering categories completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_network_appliance_firewall_inbound_firewall_rules",
        description="📊 Get network appliance firewall inbound firewall rules"
    )
    def get_network_appliance_firewall_inbound_firewall_rules(network_id: str):
        """Get network appliance firewall inbound firewall rules."""
        try:
            result = meraki_client.dashboard.appliance.getNetworkApplianceFirewallInboundFirewallRules(
                network_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Appliance Firewall Inbound Firewall Rules")
            elif isinstance(result, list):
                return format_list_response(result, "Network Appliance Firewall Inbound Firewall Rules")
            else:
                return f"✅ Get network appliance firewall inbound firewall rules completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_net_app_firewall_l7_firewall_rules_application_categories",
        description="📊 Get network appliance firewall l7 firewall rules application categories"
    )
    def get_network_appliance_firewall_l7_firewall_rules_application_categories(network_id: str):
        """Get network appliance firewall l7 firewall rules application categories."""
        try:
            result = meraki_client.dashboard.appliance.getNetworkApplianceFirewallL7FirewallRulesApplicationCategories(
                network_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Appliance Firewall L7 Firewall Rules Application Categories")
            elif isinstance(result, list):
                return format_list_response(result, "Network Appliance Firewall L7 Firewall Rules Application Categories")
            else:
                return f"✅ Get network appliance firewall l7 firewall rules application categories completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_network_appliance_firewall_settings",
        description="📊 Get network appliance firewall settings"
    )
    def get_network_appliance_firewall_settings(network_id: str):
        """Get network appliance firewall settings."""
        try:
            result = meraki_client.dashboard.appliance.getNetworkApplianceFirewallSettings(
                network_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Appliance Firewall Settings")
            elif isinstance(result, list):
                return format_list_response(result, "Network Appliance Firewall Settings")
            else:
                return f"✅ Get network appliance firewall settings completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_network_appliance_prefixes_delegated_static",
        description="📊 Get network appliance prefixes delegated static"
    )
    def get_network_appliance_prefixes_delegated_static(network_id: str):
        """Get network appliance prefixes delegated static."""
        try:
            result = meraki_client.dashboard.appliance.getNetworkAppliancePrefixesDelegatedStatic(
                network_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Appliance Prefixes Delegated Static")
            elif isinstance(result, list):
                return format_list_response(result, "Network Appliance Prefixes Delegated Static")
            else:
                return f"✅ Get network appliance prefixes delegated static completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_network_appliance_prefixes_delegated_statics",
        description="📊 Get network appliance prefixes delegated statics"
    )
    def get_network_appliance_prefixes_delegated_statics(network_id: str):
        """Get network appliance prefixes delegated statics."""
        try:
            result = meraki_client.dashboard.appliance.getNetworkAppliancePrefixesDelegatedStatics(
                network_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Appliance Prefixes Delegated Statics")
            elif isinstance(result, list):
                return format_list_response(result, "Network Appliance Prefixes Delegated Statics")
            else:
                return f"✅ Get network appliance prefixes delegated statics completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_network_appliance_rf_profile",
        description="📊 Get network appliance rf profile"
    )
    def get_network_appliance_rf_profile(network_id: str):
        """Get network appliance rf profile."""
        try:
            result = meraki_client.dashboard.appliance.getNetworkApplianceRfProfile(
                network_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Appliance Rf Profile")
            elif isinstance(result, list):
                return format_list_response(result, "Network Appliance Rf Profile")
            else:
                return f"✅ Get network appliance rf profile completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_network_appliance_security_events",
        description="📊 Get network appliance security events"
    )
    def get_network_appliance_security_events(network_id: str):
        """Get network appliance security events."""
        try:
            result = meraki_client.dashboard.appliance.getNetworkApplianceSecurityEvents(
                network_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Appliance Security Events")
            elif isinstance(result, list):
                return format_list_response(result, "Network Appliance Security Events")
            else:
                return f"✅ Get network appliance security events completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_network_appliance_traffic_shaping_custom_performance_class",
        description="📊 Get network appliance traffic shaping custom performance class"
    )
    def get_network_appliance_traffic_shaping_custom_performance_class(network_id: str):
        """Get network appliance traffic shaping custom performance class."""
        try:
            result = meraki_client.dashboard.appliance.getNetworkApplianceTrafficShapingCustomPerformanceClass(
                network_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Appliance Traffic Shaping Custom Performance Class")
            elif isinstance(result, list):
                return format_list_response(result, "Network Appliance Traffic Shaping Custom Performance Class")
            else:
                return f"✅ Get network appliance traffic shaping custom performance class completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_network_appliance_traffic_shaping_custom_performance_classes",
        description="📊 Get network appliance traffic shaping custom performance classes"
    )
    def get_network_appliance_traffic_shaping_custom_performance_classes(network_id: str):
        """Get network appliance traffic shaping custom performance classes."""
        try:
            result = meraki_client.dashboard.appliance.getNetworkApplianceTrafficShapingCustomPerformanceClasses(
                network_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Appliance Traffic Shaping Custom Performance Classes")
            elif isinstance(result, list):
                return format_list_response(result, "Network Appliance Traffic Shaping Custom Performance Classes")
            else:
                return f"✅ Get network appliance traffic shaping custom performance classes completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_network_appliance_traffic_shaping_uplink_selection",
        description="📊 Get network appliance traffic shaping uplink selection"
    )
    def get_network_appliance_traffic_shaping_uplink_selection(network_id: str):
        """Get network appliance traffic shaping uplink selection."""
        try:
            result = meraki_client.dashboard.appliance.getNetworkApplianceTrafficShapingUplinkSelection(
                network_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Appliance Traffic Shaping Uplink Selection")
            elif isinstance(result, list):
                return format_list_response(result, "Network Appliance Traffic Shaping Uplink Selection")
            else:
                return f"✅ Get network appliance traffic shaping uplink selection completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_network_appliance_uplinks_usage_history",
        description="📊 Get network appliance uplinks usage history"
    )
    def get_network_appliance_uplinks_usage_history(network_id: str, **kwargs):
        """Get network appliance uplinks usage history."""
        try:
            # Add default timespan if not specified
            if 'timespan' not in kwargs and 't0' not in kwargs:
                kwargs['timespan'] = 86400  # Default to 1 day
            
            result = meraki_client.dashboard.appliance.getNetworkApplianceUplinksUsageHistory(
                network_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Appliance Uplinks Usage History")
            elif isinstance(result, list):
                return format_list_response(result, "Network Appliance Uplinks Usage History")
            else:
                return f"✅ Get network appliance uplinks usage history completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_network_appliance_vlans_settings",
        description="📊 Get network appliance vlans settings"
    )
    def get_network_appliance_vlans_settings(network_id: str):
        """Get network appliance vlans settings."""
        try:
            result = meraki_client.dashboard.appliance.getNetworkApplianceVlansSettings(
                network_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Appliance Vlans Settings")
            elif isinstance(result, list):
                return format_list_response(result, "Network Appliance Vlans Settings")
            else:
                return f"✅ Get network appliance vlans settings completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_appliance_dns_local_profiles",
        description="📊 Get organization appliance dns local profiles"
    )
    def get_organization_appliance_dns_local_profiles(organization_id: str):
        """Get organization appliance dns local profiles."""
        try:
            result = meraki_client.dashboard.appliance.getOrganizationApplianceDnsLocalProfiles(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Appliance Dns Local Profiles")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Appliance Dns Local Profiles")
            else:
                return f"✅ Get organization appliance dns local profiles completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_appliance_dns_local_profiles_assignments",
        description="📊 Get organization appliance dns local profiles assignments"
    )
    def get_organization_appliance_dns_local_profiles_assignments(organization_id: str):
        """Get organization appliance dns local profiles assignments."""
        try:
            result = meraki_client.dashboard.appliance.getOrganizationApplianceDnsLocalProfilesAssignments(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Appliance Dns Local Profiles Assignments")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Appliance Dns Local Profiles Assignments")
            else:
                return f"✅ Get organization appliance dns local profiles assignments completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_appliance_dns_local_records",
        description="📊 Get organization appliance dns local records"
    )
    def get_organization_appliance_dns_local_records(organization_id: str):
        """Get organization appliance dns local records."""
        try:
            result = meraki_client.dashboard.appliance.getOrganizationApplianceDnsLocalRecords(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Appliance Dns Local Records")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Appliance Dns Local Records")
            else:
                return f"✅ Get organization appliance dns local records completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_appliance_dns_split_profiles",
        description="📊 Get organization appliance dns split profiles"
    )
    def get_organization_appliance_dns_split_profiles(organization_id: str):
        """Get organization appliance dns split profiles."""
        try:
            result = meraki_client.dashboard.appliance.getOrganizationApplianceDnsSplitProfiles(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Appliance Dns Split Profiles")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Appliance Dns Split Profiles")
            else:
                return f"✅ Get organization appliance dns split profiles completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_appliance_dns_split_profiles_assignments",
        description="📊 Get organization appliance dns split profiles assignments"
    )
    def get_organization_appliance_dns_split_profiles_assignments(organization_id: str):
        """Get organization appliance dns split profiles assignments."""
        try:
            result = meraki_client.dashboard.appliance.getOrganizationApplianceDnsSplitProfilesAssignments(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Appliance Dns Split Profiles Assignments")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Appliance Dns Split Profiles Assignments")
            else:
                return f"✅ Get organization appliance dns split profiles assignments completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_org_appliance_firewall_multicast_forwarding_by_network",
        description="📊 Get organization appliance firewall multicast forwarding by network"
    )
    def get_organization_appliance_firewall_multicast_forwarding_by_network(organization_id: str):
        """Get organization appliance firewall multicast forwarding by network."""
        try:
            result = meraki_client.dashboard.appliance.getOrganizationApplianceFirewallMulticastForwardingByNetwork(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Appliance Firewall Multicast Forwarding By Network")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Appliance Firewall Multicast Forwarding By Network")
            else:
                return f"✅ Get organization appliance firewall multicast forwarding by network completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_appliance_security_intrusion",
        description="📊 Get organization appliance security intrusion"
    )
    def get_organization_appliance_security_intrusion(organization_id: str):
        """Get organization appliance security intrusion."""
        try:
            result = meraki_client.dashboard.appliance.getOrganizationApplianceSecurityIntrusion(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Appliance Security Intrusion")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Appliance Security Intrusion")
            else:
                return f"✅ Get organization appliance security intrusion completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_org_appliance_traffic_shaping_vpn_exclusions_by_network",
        description="📊 Get organization appliance traffic shaping vpn exclusions by network"
    )
    def get_organization_appliance_traffic_shaping_vpn_exclusions_by_network(organization_id: str):
        """Get organization appliance traffic shaping vpn exclusions by network."""
        try:
            result = meraki_client.dashboard.appliance.getOrganizationApplianceTrafficShapingVpnExclusionsByNetwork(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Appliance Traffic Shaping Vpn Exclusions By Network")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Appliance Traffic Shaping Vpn Exclusions By Network")
            else:
                return f"✅ Get organization appliance traffic shaping vpn exclusions by network completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_appliance_uplinks_statuses_overview",
        description="📊 Get organization appliance uplinks statuses overview"
    )
    def get_organization_appliance_uplinks_statuses_overview(organization_id: str):
        """Get organization appliance uplinks statuses overview."""
        try:
            result = meraki_client.dashboard.appliance.getOrganizationApplianceUplinksStatusesOverview(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Appliance Uplinks Statuses Overview")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Appliance Uplinks Statuses Overview")
            else:
                return f"✅ Get organization appliance uplinks statuses overview completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_appliance_uplinks_usage_by_network",
        description="📊 Get organization appliance uplinks usage by network"
    )
    def get_organization_appliance_uplinks_usage_by_network(organization_id: str):
        """Get organization appliance uplinks usage by network."""
        try:
            result = meraki_client.dashboard.appliance.getOrganizationApplianceUplinksUsageByNetwork(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Appliance Uplinks Usage By Network")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Appliance Uplinks Usage By Network")
            else:
                return f"✅ Get organization appliance uplinks usage by network completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_appliance_vpn_stats",
        description="📊 Get organization appliance vpn stats"
    )
    def get_organization_appliance_vpn_stats(organization_id: str):
        """Get organization appliance vpn stats."""
        try:
            result = meraki_client.dashboard.appliance.getOrganizationApplianceVpnStats(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Appliance Vpn Stats")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Appliance Vpn Stats")
            else:
                return f"✅ Get organization appliance vpn stats completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_appliance_vpn_vpn_firewall_rules",
        description="📊 Get organization appliance vpn vpn firewall rules"
    )
    def get_organization_appliance_vpn_vpn_firewall_rules(organization_id: str):
        """Get organization appliance vpn vpn firewall rules."""
        try:
            result = meraki_client.dashboard.appliance.getOrganizationApplianceVpnVpnFirewallRules(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Appliance Vpn Vpn Firewall Rules")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Appliance Vpn Vpn Firewall Rules")
            else:
                return f"✅ Get organization appliance vpn vpn firewall rules completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="update_device_appliance_radio_settings",
        description="✏️ Update device appliance radio settings"
    )
    def update_device_appliance_radio_settings(serial: str, **kwargs):
        """Update device appliance radio settings."""
        try:
            result = meraki_client.dashboard.appliance.updateDeviceApplianceRadioSettings(
                serial, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Device Appliance Radio Settings")
            elif isinstance(result, list):
                return format_list_response(result, "Device Appliance Radio Settings")
            else:
                return f"✅ Update device appliance radio settings completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="update_network_appliance_firewall_inbound_firewall_rules",
        description="✏️ Update network appliance firewall inbound firewall rules"
    )
    def update_network_appliance_firewall_inbound_firewall_rules(network_id: str, **kwargs):
        """Update network appliance firewall inbound firewall rules."""
        try:
            result = meraki_client.dashboard.appliance.updateNetworkApplianceFirewallInboundFirewallRules(
                network_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Appliance Firewall Inbound Firewall Rules")
            elif isinstance(result, list):
                return format_list_response(result, "Network Appliance Firewall Inbound Firewall Rules")
            else:
                return f"✅ Update network appliance firewall inbound firewall rules completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="update_network_appliance_firewall_multicast_forwarding",
        description="✏️ Update network appliance firewall multicast forwarding"
    )
    def update_network_appliance_firewall_multicast_forwarding(network_id: str, **kwargs):
        """Update network appliance firewall multicast forwarding."""
        try:
            result = meraki_client.dashboard.appliance.updateNetworkApplianceFirewallMulticastForwarding(
                network_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Appliance Firewall Multicast Forwarding")
            elif isinstance(result, list):
                return format_list_response(result, "Network Appliance Firewall Multicast Forwarding")
            else:
                return f"✅ Update network appliance firewall multicast forwarding completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="update_network_appliance_firewall_one_to_many_nat_rules",
        description="✏️ Update network appliance firewall one to many nat rules"
    )
    def update_network_appliance_firewall_one_to_many_nat_rules(network_id: str, **kwargs):
        """Update network appliance firewall one to many nat rules."""
        try:
            result = meraki_client.dashboard.appliance.updateNetworkApplianceFirewallOneToManyNatRules(
                network_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Appliance Firewall One To Many Nat Rules")
            elif isinstance(result, list):
                return format_list_response(result, "Network Appliance Firewall One To Many Nat Rules")
            else:
                return f"✅ Update network appliance firewall one to many nat rules completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="update_network_appliance_firewall_settings",
        description="✏️ Update network appliance firewall settings"
    )
    def update_network_appliance_firewall_settings(network_id: str, **kwargs):
        """Update network appliance firewall settings."""
        try:
            result = meraki_client.dashboard.appliance.updateNetworkApplianceFirewallSettings(
                network_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Appliance Firewall Settings")
            elif isinstance(result, list):
                return format_list_response(result, "Network Appliance Firewall Settings")
            else:
                return f"✅ Update network appliance firewall settings completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="update_network_appliance_prefixes_delegated_static",
        description="✏️ Update network appliance prefixes delegated static"
    )
    def update_network_appliance_prefixes_delegated_static(network_id: str, **kwargs):
        """Update network appliance prefixes delegated static."""
        try:
            result = meraki_client.dashboard.appliance.updateNetworkAppliancePrefixesDelegatedStatic(
                network_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Appliance Prefixes Delegated Static")
            elif isinstance(result, list):
                return format_list_response(result, "Network Appliance Prefixes Delegated Static")
            else:
                return f"✅ Update network appliance prefixes delegated static completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="update_network_appliance_rf_profile",
        description="✏️ Update network appliance rf profile"
    )
    def update_network_appliance_rf_profile(network_id: str, **kwargs):
        """Update network appliance rf profile."""
        try:
            result = meraki_client.dashboard.appliance.updateNetworkApplianceRfProfile(
                network_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Appliance Rf Profile")
            elif isinstance(result, list):
                return format_list_response(result, "Network Appliance Rf Profile")
            else:
                return f"✅ Update network appliance rf profile completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="update_network_app_traffic_shaping_custom_performance_class",
        description="✏️ Update network appliance traffic shaping custom performance class"
    )
    def update_network_appliance_traffic_shaping_custom_performance_class(network_id: str, **kwargs):
        """Update network appliance traffic shaping custom performance class."""
        try:
            result = meraki_client.dashboard.appliance.updateNetworkApplianceTrafficShapingCustomPerformanceClass(
                network_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Appliance Traffic Shaping Custom Performance Class")
            elif isinstance(result, list):
                return format_list_response(result, "Network Appliance Traffic Shaping Custom Performance Class")
            else:
                return f"✅ Update network appliance traffic shaping custom performance class completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="update_network_appliance_traffic_shaping_uplink_selection",
        description="✏️ Update network appliance traffic shaping uplink selection"
    )
    def update_network_appliance_traffic_shaping_uplink_selection(network_id: str, **kwargs):
        """Update network appliance traffic shaping uplink selection."""
        try:
            result = meraki_client.dashboard.appliance.updateNetworkApplianceTrafficShapingUplinkSelection(
                network_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Appliance Traffic Shaping Uplink Selection")
            elif isinstance(result, list):
                return format_list_response(result, "Network Appliance Traffic Shaping Uplink Selection")
            else:
                return f"✅ Update network appliance traffic shaping uplink selection completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="update_network_appliance_traffic_shaping_vpn_exclusions",
        description="✏️ Update network appliance traffic shaping vpn exclusions"
    )
    def update_network_appliance_traffic_shaping_vpn_exclusions(network_id: str, **kwargs):
        """Update network appliance traffic shaping vpn exclusions."""
        try:
            result = meraki_client.dashboard.appliance.updateNetworkApplianceTrafficShapingVpnExclusions(
                network_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Appliance Traffic Shaping Vpn Exclusions")
            elif isinstance(result, list):
                return format_list_response(result, "Network Appliance Traffic Shaping Vpn Exclusions")
            else:
                return f"✅ Update network appliance traffic shaping vpn exclusions completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="update_network_appliance_vlans_settings",
        description="✏️ Enable or disable VLANs on network appliance"
    )
    def update_network_appliance_vlans_settings(network_id: str, vlansEnabled: bool = None):
        """Enable or disable VLANs for the network appliance.
        
        Args:
            network_id: Network ID
            vlansEnabled: True to enable VLANs, False to disable (required)
        """
        try:
            if vlansEnabled is None:
                return "❌ Error: vlansEnabled parameter is required (True to enable, False to disable)"
            
            result = meraki_client.dashboard.appliance.updateNetworkApplianceVlansSettings(
                network_id, 
                vlansEnabled=vlansEnabled
            )
            
            if isinstance(result, dict):
                status = "enabled" if result.get('vlansEnabled') else "disabled"
                return f"✅ VLANs {status} successfully on network {network_id}"
            elif isinstance(result, list):
                return format_list_response(result, "Network Appliance Vlans Settings")
            else:
                return f"✅ VLAN settings updated successfully!"
                
        except Exception as e:
            return f"Error updating VLAN settings: {str(e)}"

    @app.tool(
        name="update_organization_appliance_dns_local_profile",
        description="✏️ Update organization appliance dns local profile"
    )
    def update_organization_appliance_dns_local_profile(organization_id: str, **kwargs):
        """Update organization appliance dns local profile."""
        try:
            result = meraki_client.dashboard.appliance.updateOrganizationApplianceDnsLocalProfile(
                organization_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Appliance Dns Local Profile")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Appliance Dns Local Profile")
            else:
                return f"✅ Update organization appliance dns local profile completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="update_organization_appliance_dns_local_record",
        description="✏️ Update organization appliance dns local record"
    )
    def update_organization_appliance_dns_local_record(organization_id: str, **kwargs):
        """Update organization appliance dns local record."""
        try:
            result = meraki_client.dashboard.appliance.updateOrganizationApplianceDnsLocalRecord(
                organization_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Appliance Dns Local Record")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Appliance Dns Local Record")
            else:
                return f"✅ Update organization appliance dns local record completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="update_organization_appliance_dns_split_profile",
        description="✏️ Update organization appliance dns split profile"
    )
    def update_organization_appliance_dns_split_profile(organization_id: str, **kwargs):
        """Update organization appliance dns split profile."""
        try:
            result = meraki_client.dashboard.appliance.updateOrganizationApplianceDnsSplitProfile(
                organization_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Appliance Dns Split Profile")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Appliance Dns Split Profile")
            else:
                return f"✅ Update organization appliance dns split profile completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="update_organization_appliance_security_intrusion",
        description="✏️ Update organization appliance security intrusion"
    )
    def update_organization_appliance_security_intrusion(organization_id: str, **kwargs):
        """Update organization appliance security intrusion."""
        try:
            result = meraki_client.dashboard.appliance.updateOrganizationApplianceSecurityIntrusion(
                organization_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Appliance Security Intrusion")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Appliance Security Intrusion")
            else:
                return f"✅ Update organization appliance security intrusion completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="update_organization_appliance_vpn_vpn_firewall_rules",
        description="✏️ Update organization appliance vpn vpn firewall rules"
    )
    def update_organization_appliance_vpn_vpn_firewall_rules(organization_id: str, **kwargs):
        """Update organization appliance vpn vpn firewall rules."""
        try:
            result = meraki_client.dashboard.appliance.updateOrganizationApplianceVpnVpnFirewallRules(
                organization_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Appliance Vpn Vpn Firewall Rules")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Appliance Vpn Vpn Firewall Rules")
            else:
                return f"✅ Update organization appliance vpn vpn firewall rules completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"
