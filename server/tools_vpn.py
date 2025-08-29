"""
VPN management tools for the Cisco Meraki MCP Server - matches official API site exactly.
"""

from typing import Optional, List, Dict, Any

# Global variables to store app and meraki client
app = None
meraki_client = None

def register_vpn_tools(mcp_app, meraki):
    """
    Register VPN tools with the MCP server.
    
    Args:
        mcp_app: MCP server instance
        meraki: Meraki client instance
    """
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    
    # Register all VPN tools
    register_vpn_tool_handlers()

def register_vpn_tool_handlers():
    """Register all VPN tool handlers using official API methods."""
    
    @app.tool(
        name="get_organization_appliance_vpn_third_party_vpn_peers",
        description="Return the third party VPN peers for an organization"
    )
    async def get_organization_appliance_vpn_third_party_vpn_peers(
        organization_id: str
    ) -> List[Dict[str, Any]]:
        """Return the third party VPN peers for an organization."""
        try:
            result = meraki_client.dashboard.appliance.getOrganizationApplianceVpnThirdPartyVPNPeers(
                organization_id
            )
            return result
        except Exception as e:
            return {"error": str(e)}
    
    @app.tool(
        name="update_organization_appliance_vpn_third_party_vpn_peers",
        description="Update the third party VPN peers for an organization"
    )
    async def update_organization_appliance_vpn_third_party_vpn_peers(
        organization_id: str,
        peers: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Update the third party VPN peers for an organization."""
        try:
            result = meraki_client.dashboard.appliance.updateOrganizationApplianceVpnThirdPartyVPNPeers(
                organization_id,
                peers=peers
            )
            return result
        except Exception as e:
            return {"error": str(e)}
    
    @app.tool(
        name="get_organization_appliance_vpn_statuses",
        description="Show VPN status for networks in an organization"
    )
    async def get_organization_appliance_vpn_statuses(
        organization_id: str,
        per_page: Optional[int] = None,
        starting_after: Optional[str] = None,
        ending_before: Optional[str] = None,
        network_ids: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """Show VPN status for networks in an organization."""
        try:
            kwargs = {}
            if per_page is not None:
                kwargs['perPage'] = per_page
            if starting_after is not None:
                kwargs['startingAfter'] = starting_after
            if ending_before is not None:
                kwargs['endingBefore'] = ending_before
            if network_ids is not None:
                kwargs['networkIds'] = network_ids
                
            result = meraki_client.dashboard.appliance.getOrganizationApplianceVpnStatuses(
                organization_id, **kwargs
            )
            return result
        except Exception as e:
            return {"error": str(e)}
    
    @app.tool(
        name="get_network_appliance_vpn_bgp",
        description="Return a Hub BGP Configuration"
    )
    async def get_network_appliance_vpn_bgp(
        network_id: str
    ) -> Dict[str, Any]:
        """Return a Hub BGP Configuration."""
        try:
            result = meraki_client.dashboard.appliance.getNetworkApplianceVpnBgp(network_id)
            return result
        except Exception as e:
            return {"error": str(e)}
    
    @app.tool(
        name="update_network_appliance_vpn_bgp",
        description="Update a Hub BGP Configuration"
    )
    async def update_network_appliance_vpn_bgp(
        network_id: str,
        enabled: bool,
        as_number: Optional[int] = None,
        ibgp_hold_timer: Optional[int] = None,
        neighbors: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """Update a Hub BGP Configuration."""
        try:
            kwargs = {'enabled': enabled}
            if as_number is not None:
                kwargs['asNumber'] = as_number
            if ibgp_hold_timer is not None:
                kwargs['ibgpHoldTimer'] = ibgp_hold_timer
            if neighbors is not None:
                kwargs['neighbors'] = neighbors
                
            result = meraki_client.dashboard.appliance.updateNetworkApplianceVpnBgp(
                network_id, **kwargs
            )
            return result
        except Exception as e:
            return {"error": str(e)}
    
    @app.tool(
        name="get_organization_appliance_vpn_vpn_firewall_rules",
        description="Return the VPN firewall rules for an organization"
    )
    async def get_organization_appliance_vpn_vpn_firewall_rules(
        organization_id: str
    ) -> Dict[str, Any]:
        """Return the VPN firewall rules for an organization."""
        try:
            result = meraki_client.dashboard.appliance.getOrganizationApplianceVpnVpnFirewallRules(
                organization_id
            )
            return result
        except Exception as e:
            return {"error": str(e)}
    
    @app.tool(
        name="update_organization_appliance_vpn_vpn_firewall_rules",
        description="Update the VPN firewall rules of an organization"
    )
    async def update_organization_appliance_vpn_vpn_firewall_rules(
        organization_id: str,
        rules: Optional[List[Dict[str, Any]]] = None,
        syslog_default_rule: Optional[bool] = None
    ) -> Dict[str, Any]:
        """Update the VPN firewall rules of an organization."""
        try:
            kwargs = {}
            if rules is not None:
                kwargs['rules'] = rules
            if syslog_default_rule is not None:
                kwargs['syslogDefaultRule'] = syslog_default_rule
                
            result = meraki_client.dashboard.appliance.updateOrganizationApplianceVpnVpnFirewallRules(
                organization_id, **kwargs
            )
            return result
        except Exception as e:
            return {"error": str(e)}
    
    @app.tool(
        name="get_device_appliance_uplinks_settings",
        description="Return the uplink settings for an MX appliance"
    )
    async def get_device_appliance_uplinks_settings(
        serial: str
    ) -> Dict[str, Any]:
        """Return the uplink settings for an MX appliance."""
        try:
            result = meraki_client.dashboard.appliance.getDeviceApplianceUplinksSettings(serial)
            return result
        except Exception as e:
            return {"error": str(e)}
    
    @app.tool(
        name="update_device_appliance_uplinks_settings",
        description="Update the uplink settings for an MX appliance"
    )
    async def update_device_appliance_uplinks_settings(
        serial: str,
        interfaces: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Update the uplink settings for an MX appliance."""
        try:
            kwargs = {}
            if interfaces is not None:
                kwargs['interfaces'] = interfaces
                
            result = meraki_client.dashboard.appliance.updateDeviceApplianceUplinksSettings(
                serial, **kwargs
            )
            return result
        except Exception as e:
            return {"error": str(e)}