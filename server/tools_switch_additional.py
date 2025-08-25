"""
Additional Switch endpoints for Cisco Meraki MCP Server.
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

def register_switch_additional_tools(mcp_app, meraki):
    """Register additional switch tools with the MCP server."""
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    
    # Register all additional tools
    register_switch_additional_handlers()

def register_switch_additional_handlers():
    """Register additional switch tool handlers."""

    @app.tool(
        name="create_network_switch_routing_multicast_rendezvous_point",
        description="➕ Create network switch routing multicast rendezvous point"
    )
    def create_network_switch_routing_multicast_rendezvous_point(network_id: str, **kwargs):
        """Create network switch routing multicast rendezvous point."""
        try:
            result = meraki_client.dashboard.switch.createNetworkSwitchRoutingMulticastRendezvousPoint(
                network_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Switch Routing Multicast Rendezvous Point")
            elif isinstance(result, list):
                return format_list_response(result, "Network Switch Routing Multicast Rendezvous Point")
            else:
                return f"✅ Create network switch routing multicast rendezvous point completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="create_network_switch_stack_routing_interface",
        description="➕ Create network switch stack routing interface"
    )
    def create_network_switch_stack_routing_interface(network_id: str, **kwargs):
        """Create network switch stack routing interface."""
        try:
            result = meraki_client.dashboard.switch.createNetworkSwitchStackRoutingInterface(
                network_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Switch Stack Routing Interface")
            elif isinstance(result, list):
                return format_list_response(result, "Network Switch Stack Routing Interface")
            else:
                return f"✅ Create network switch stack routing interface completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="create_network_switch_stack_routing_static_route",
        description="➕ Create network switch stack routing static route"
    )
    def create_network_switch_stack_routing_static_route(network_id: str, **kwargs):
        """Create network switch stack routing static route."""
        try:
            result = meraki_client.dashboard.switch.createNetworkSwitchStackRoutingStaticRoute(
                network_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Switch Stack Routing Static Route")
            elif isinstance(result, list):
                return format_list_response(result, "Network Switch Stack Routing Static Route")
            else:
                return f"✅ Create network switch stack routing static route completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="delete_network_switch_routing_multicast_rendezvous_point",
        description="🗑️ Delete network switch routing multicast rendezvous point"
    )
    def delete_network_switch_routing_multicast_rendezvous_point(network_id: str):
        """Delete network switch routing multicast rendezvous point."""
        try:
            result = meraki_client.dashboard.switch.deleteNetworkSwitchRoutingMulticastRendezvousPoint(
                network_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Switch Routing Multicast Rendezvous Point")
            elif isinstance(result, list):
                return format_list_response(result, "Network Switch Routing Multicast Rendezvous Point")
            else:
                return f"✅ Delete network switch routing multicast rendezvous point completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="delete_network_switch_stack_routing_interface",
        description="🗑️ Delete network switch stack routing interface"
    )
    def delete_network_switch_stack_routing_interface(network_id: str):
        """Delete network switch stack routing interface."""
        try:
            result = meraki_client.dashboard.switch.deleteNetworkSwitchStackRoutingInterface(
                network_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Switch Stack Routing Interface")
            elif isinstance(result, list):
                return format_list_response(result, "Network Switch Stack Routing Interface")
            else:
                return f"✅ Delete network switch stack routing interface completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="delete_network_switch_stack_routing_static_route",
        description="🗑️ Delete network switch stack routing static route"
    )
    def delete_network_switch_stack_routing_static_route(network_id: str):
        """Delete network switch stack routing static route."""
        try:
            result = meraki_client.dashboard.switch.deleteNetworkSwitchStackRoutingStaticRoute(
                network_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Switch Stack Routing Static Route")
            elif isinstance(result, list):
                return format_list_response(result, "Network Switch Stack Routing Static Route")
            else:
                return f"✅ Delete network switch stack routing static route completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_network_switch_routing_multicast_rendezvous_point",
        description="📊 Get network switch routing multicast rendezvous point"
    )
    def get_network_switch_routing_multicast_rendezvous_point(network_id: str):
        """Get network switch routing multicast rendezvous point."""
        try:
            result = meraki_client.dashboard.switch.getNetworkSwitchRoutingMulticastRendezvousPoint(
                network_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Switch Routing Multicast Rendezvous Point")
            elif isinstance(result, list):
                return format_list_response(result, "Network Switch Routing Multicast Rendezvous Point")
            else:
                return f"✅ Get network switch routing multicast rendezvous point completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_network_switch_routing_multicast_rendezvous_points",
        description="📊 Get network switch routing multicast rendezvous points"
    )
    def get_network_switch_routing_multicast_rendezvous_points(network_id: str):
        """Get network switch routing multicast rendezvous points."""
        try:
            result = meraki_client.dashboard.switch.getNetworkSwitchRoutingMulticastRendezvousPoints(
                network_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Switch Routing Multicast Rendezvous Points")
            elif isinstance(result, list):
                return format_list_response(result, "Network Switch Routing Multicast Rendezvous Points")
            else:
                return f"✅ Get network switch routing multicast rendezvous points completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_network_switch_stack_routing_interface",
        description="📊 Get network switch stack routing interface"
    )
    def get_network_switch_stack_routing_interface(network_id: str):
        """Get network switch stack routing interface."""
        try:
            result = meraki_client.dashboard.switch.getNetworkSwitchStackRoutingInterface(
                network_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Switch Stack Routing Interface")
            elif isinstance(result, list):
                return format_list_response(result, "Network Switch Stack Routing Interface")
            else:
                return f"✅ Get network switch stack routing interface completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_network_switch_stack_routing_interface_dhcp",
        description="📊 Get network switch stack routing interface dhcp"
    )
    def get_network_switch_stack_routing_interface_dhcp(network_id: str):
        """Get network switch stack routing interface dhcp."""
        try:
            result = meraki_client.dashboard.switch.getNetworkSwitchStackRoutingInterfaceDhcp(
                network_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Switch Stack Routing Interface Dhcp")
            elif isinstance(result, list):
                return format_list_response(result, "Network Switch Stack Routing Interface Dhcp")
            else:
                return f"✅ Get network switch stack routing interface dhcp completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_network_switch_stack_routing_static_route",
        description="📊 Get network switch stack routing static route"
    )
    def get_network_switch_stack_routing_static_route(network_id: str):
        """Get network switch stack routing static route."""
        try:
            result = meraki_client.dashboard.switch.getNetworkSwitchStackRoutingStaticRoute(
                network_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Switch Stack Routing Static Route")
            elif isinstance(result, list):
                return format_list_response(result, "Network Switch Stack Routing Static Route")
            else:
                return f"✅ Get network switch stack routing static route completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_network_switch_stack_routing_static_routes",
        description="📊 Get network switch stack routing static routes"
    )
    def get_network_switch_stack_routing_static_routes(network_id: str):
        """Get network switch stack routing static routes."""
        try:
            result = meraki_client.dashboard.switch.getNetworkSwitchStackRoutingStaticRoutes(
                network_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Switch Stack Routing Static Routes")
            elif isinstance(result, list):
                return format_list_response(result, "Network Switch Stack Routing Static Routes")
            else:
                return f"✅ Get network switch stack routing static routes completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_config_template_switch_profile_port",
        description="📊 Get organization config template switch profile port"
    )
    def get_organization_config_template_switch_profile_port(organization_id: str):
        """Get organization config template switch profile port."""
        try:
            result = meraki_client.dashboard.switch.getOrganizationConfigTemplateSwitchProfilePort(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Config Template Switch Profile Port")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Config Template Switch Profile Port")
            else:
                return f"✅ Get organization config template switch profile port completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_config_template_switch_profile_ports",
        description="📊 Get organization config template switch profile ports"
    )
    def get_organization_config_template_switch_profile_ports(organization_id: str):
        """Get organization config template switch profile ports."""
        try:
            result = meraki_client.dashboard.switch.getOrganizationConfigTemplateSwitchProfilePorts(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Config Template Switch Profile Ports")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Config Template Switch Profile Ports")
            else:
                return f"✅ Get organization config template switch profile ports completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_config_template_switch_profiles",
        description="📊 Get organization config template switch profiles"
    )
    def get_organization_config_template_switch_profiles(organization_id: str):
        """Get organization config template switch profiles."""
        try:
            result = meraki_client.dashboard.switch.getOrganizationConfigTemplateSwitchProfiles(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Config Template Switch Profiles")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Config Template Switch Profiles")
            else:
                return f"✅ Get organization config template switch profiles completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_switch_ports_clients_overview_by_device",
        description="📊 Get organization switch ports clients overview by device"
    )
    def get_organization_switch_ports_clients_overview_by_device(organization_id: str):
        """Get organization switch ports clients overview by device."""
        try:
            result = meraki_client.dashboard.switch.getOrganizationSwitchPortsClientsOverviewByDevice(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Switch Ports Clients Overview By Device")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Switch Ports Clients Overview By Device")
            else:
                return f"✅ Get organization switch ports clients overview by device completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_switch_ports_overview",
        description="📊 Get organization switch ports overview"
    )
    def get_organization_switch_ports_overview(organization_id: str):
        """Get organization switch ports overview."""
        try:
            result = meraki_client.dashboard.switch.getOrganizationSwitchPortsOverview(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Switch Ports Overview")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Switch Ports Overview")
            else:
                return f"✅ Get organization switch ports overview completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_switch_ports_statuses_by_switch",
        description="📊 Get organization switch ports statuses by switch"
    )
    def get_organization_switch_ports_statuses_by_switch(organization_id: str):
        """Get organization switch ports statuses by switch."""
        try:
            result = meraki_client.dashboard.switch.getOrganizationSwitchPortsStatusesBySwitch(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Switch Ports Statuses By Switch")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Switch Ports Statuses By Switch")
            else:
                return f"✅ Get organization switch ports statuses by switch completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_switch_ports_topology_discovery_by_device",
        description="📊 Get organization switch ports topology discovery by device"
    )
    def get_organization_switch_ports_topology_discovery_by_device(organization_id: str):
        """Get organization switch ports topology discovery by device."""
        try:
            result = meraki_client.dashboard.switch.getOrganizationSwitchPortsTopologyDiscoveryByDevice(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Switch Ports Topology Discovery By Device")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Switch Ports Topology Discovery By Device")
            else:
                return f"✅ Get organization switch ports topology discovery by device completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_org_switch_ports_usage_by_device",
        description="📊 Get organization switch ports usage history by device by interval"
    )
    def get_organization_switch_ports_usage_history_by_device_by_interval(organization_id: str):
        """Get organization switch ports usage history by device by interval."""
        try:
            result = meraki_client.dashboard.switch.getOrganizationSwitchPortsUsageHistoryByDeviceByInterval(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Switch Ports Usage History By Device By Interval")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Switch Ports Usage History By Device By Interval")
            else:
                return f"✅ Get organization switch ports usage history by device by interval completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="update_network_switch_routing_multicast_rendezvous_point",
        description="✏️ Update network switch routing multicast rendezvous point"
    )
    def update_network_switch_routing_multicast_rendezvous_point(network_id: str, **kwargs):
        """Update network switch routing multicast rendezvous point."""
        try:
            result = meraki_client.dashboard.switch.updateNetworkSwitchRoutingMulticastRendezvousPoint(
                network_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Switch Routing Multicast Rendezvous Point")
            elif isinstance(result, list):
                return format_list_response(result, "Network Switch Routing Multicast Rendezvous Point")
            else:
                return f"✅ Update network switch routing multicast rendezvous point completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="update_network_switch_stack_routing_interface",
        description="✏️ Update network switch stack routing interface"
    )
    def update_network_switch_stack_routing_interface(network_id: str, **kwargs):
        """Update network switch stack routing interface."""
        try:
            result = meraki_client.dashboard.switch.updateNetworkSwitchStackRoutingInterface(
                network_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Switch Stack Routing Interface")
            elif isinstance(result, list):
                return format_list_response(result, "Network Switch Stack Routing Interface")
            else:
                return f"✅ Update network switch stack routing interface completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="update_network_switch_stack_routing_interface_dhcp",
        description="✏️ Update network switch stack routing interface dhcp"
    )
    def update_network_switch_stack_routing_interface_dhcp(network_id: str, **kwargs):
        """Update network switch stack routing interface dhcp."""
        try:
            result = meraki_client.dashboard.switch.updateNetworkSwitchStackRoutingInterfaceDhcp(
                network_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Switch Stack Routing Interface Dhcp")
            elif isinstance(result, list):
                return format_list_response(result, "Network Switch Stack Routing Interface Dhcp")
            else:
                return f"✅ Update network switch stack routing interface dhcp completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="update_network_switch_stack_routing_static_route",
        description="✏️ Update network switch stack routing static route"
    )
    def update_network_switch_stack_routing_static_route(network_id: str, **kwargs):
        """Update network switch stack routing static route."""
        try:
            result = meraki_client.dashboard.switch.updateNetworkSwitchStackRoutingStaticRoute(
                network_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Switch Stack Routing Static Route")
            elif isinstance(result, list):
                return format_list_response(result, "Network Switch Stack Routing Static Route")
            else:
                return f"✅ Update network switch stack routing static route completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="update_organization_config_template_switch_profile_port",
        description="✏️ Update organization config template switch profile port"
    )
    def update_organization_config_template_switch_profile_port(organization_id: str, **kwargs):
        """Update organization config template switch profile port."""
        try:
            result = meraki_client.dashboard.switch.updateOrganizationConfigTemplateSwitchProfilePort(
                organization_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Config Template Switch Profile Port")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Config Template Switch Profile Port")
            else:
                return f"✅ Update organization config template switch profile port completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"
