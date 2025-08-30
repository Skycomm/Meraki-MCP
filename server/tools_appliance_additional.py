"""
Extended Appliance tools for Cisco Meraki MCP server.

This module provides additional appliance tools for DNS, VLANs, traffic shaping, and more.
"""

from typing import Optional, Dict, Any, List
from datetime import datetime
import json

# Global references to be set by register function
app = None
meraki_client = None

def register_appliance_extended_tools(mcp_app, meraki):
    """
    Register extended appliance tools with the MCP server.
    
    Args:
        mcp_app: MCP server instance
        meraki: Meraki client instance
    """
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    
    # ==================== VLAN MANAGEMENT ====================
    
    # SKIP: Already defined in tools_appliance.py
    '''@app.tool(
        name="create_network_appliance_vlan",
        description="🔧➕ Create a new VLAN on MX appliance (id, name, subnet, appliance_ip)"
    )
    def create_network_appliance_vlan(
        network_id: str,
        vlan_id: str,
        name: str,
        subnet: str,
        appliance_ip: str,
        group_policy_id: Optional[str] = None,
        dhcp_handling: Optional[str] = "Run a DHCP server",
        dhcp_lease_time: Optional[str] = "1 day",
        dhcp_boot_options_enabled: Optional[bool] = False,
        dns_nameservers: Optional[str] = "upstream_dns"
    ):
        """
        Create a new VLAN.
        
        Args:
            network_id: Network ID
            vlan_id: VLAN ID (1-4094)
            name: VLAN name
            subnet: Subnet (e.g., 192.168.1.0/24)
            appliance_ip: MX IP address (e.g., 192.168.1.1)
            group_policy_id: Group policy ID (optional)
            dhcp_handling: DHCP mode ('Run a DHCP server', 'Relay DHCP', 'Do not respond')
            dhcp_lease_time: Lease time ('30 minutes', '1 hour', '4 hours', '12 hours', '1 day', '1 week')
            dhcp_boot_options_enabled: Enable DHCP boot options
            dns_nameservers: DNS servers (comma-separated IPs or 'upstream_dns')
        """
        try:
            kwargs = {
                'id': vlan_id,
                'name': name,
                'subnet': subnet,
                'applianceIp': appliance_ip
            }
            
            if group_policy_id:
                kwargs['groupPolicyId'] = group_policy_id
            
            kwargs['dhcpHandling'] = dhcp_handling
            kwargs['dhcpLeaseTime'] = dhcp_lease_time
            kwargs['dhcpBootOptionsEnabled'] = dhcp_boot_options_enabled
            
            if dns_nameservers != 'upstream_dns':
                kwargs['dnsNameservers'] = dns_nameservers
            
            result = meraki_client.dashboard.appliance.createNetworkApplianceVlan(
                network_id, **kwargs
            )
            
            response = f"# ✅ VLAN Created\n\n"
            response += f"**VLAN ID**: {vlan_id}\n"
            response += f"**Name**: {name}\n"
            response += f"**Subnet**: {subnet}\n"
            response += f"**MX IP**: {appliance_ip}\n"
            response += f"**DHCP**: {dhcp_handling}\n"
            
            return response
        except Exception as e:
            return f"❌ Error creating VLAN: {str(e)}"'''
    
    # SKIP: Already defined in tools_appliance.py
    '''@app.tool(
        name="delete_network_appliance_vlan",
        description="🔧❌ Delete a VLAN from MX appliance"
    )
    def delete_network_appliance_vlan(
        network_id: str,
        vlan_id: str
    ):
        """Delete a VLAN."""
        try:
            meraki_client.dashboard.appliance.deleteNetworkApplianceVlan(
                network_id, vlan_id
            )
            
            response = f"# ✅ VLAN Deleted\n\n"
            response += f"**VLAN ID**: {vlan_id}\n"
            
            return response
        except Exception as e:
            return f"❌ Error deleting VLAN: {str(e)}"'''
    
    @app.tool(
        name="get_network_appliance_vlan",
        description="🔧🔍 Get details of a specific VLAN"
    )
    def get_network_appliance_vlan(
        network_id: str,
        vlan_id: str
    ):
        """Get VLAN details."""
        try:
            result = meraki_client.dashboard.appliance.getNetworkApplianceVlan(
                network_id, vlan_id
            )
            
            response = f"# 🔧 VLAN Details\n\n"
            response += f"**VLAN ID**: {vlan_id}\n"
            response += f"**Name**: {result.get('name', 'N/A')}\n"
            response += f"**Subnet**: {result.get('subnet', 'N/A')}\n"
            response += f"**MX IP**: {result.get('applianceIp', 'N/A')}\n"
            response += f"**DHCP**: {result.get('dhcpHandling', 'N/A')}\n"
            
            # Reserved IP ranges
            reserved = result.get('reservedIpRanges', [])
            if reserved:
                response += "\n## Reserved IP Ranges\n"
                for r in reserved:
                    response += f"- {r.get('start')} - {r.get('end')}: {r.get('comment', '')}\n"
            
            # Fixed IP assignments
            fixed = result.get('fixedIpAssignments', {})
            if fixed:
                response += "\n## Fixed IP Assignments\n"
                for mac, ip_info in fixed.items():
                    response += f"- {mac}: {ip_info.get('ip')} ({ip_info.get('name', 'N/A')})\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting VLAN: {str(e)}"
    
    # SKIP: Already defined in tools_appliance.py
    '''@app.tool(
        name="update_network_appliance_vlan",
        description="🔧✏️ Update VLAN settings (name, subnet, dhcp, dns)"
    )
    def update_network_appliance_vlan(
        network_id: str,
        vlan_id: str,
        name: Optional[str] = None,
        subnet: Optional[str] = None,
        appliance_ip: Optional[str] = None,
        dhcp_handling: Optional[str] = None,
        dns_nameservers: Optional[str] = None
    ):
        """Update VLAN configuration."""
        try:
            kwargs = {}
            
            if name:
                kwargs['name'] = name
            if subnet:
                kwargs['subnet'] = subnet
            if appliance_ip:
                kwargs['applianceIp'] = appliance_ip
            if dhcp_handling:
                kwargs['dhcpHandling'] = dhcp_handling
            if dns_nameservers:
                if dns_nameservers == 'upstream_dns':
                    kwargs['dnsNameservers'] = 'upstream_dns'
                else:
                    kwargs['dnsNameservers'] = dns_nameservers
            
            result = meraki_client.dashboard.appliance.updateNetworkApplianceVlan(
                network_id, vlan_id, **kwargs
            )
            
            response = f"# ✅ VLAN Updated\n\n"
            response += f"**VLAN ID**: {vlan_id}\n"
            if name:
                response += f"**Name**: {name}\n"
            if subnet:
                response += f"**Subnet**: {subnet}\n"
            
            return response
        except Exception as e:
            return f"❌ Error updating VLAN: {str(e)}"'''
    
    @app.tool(
        name="get_network_appliance_vlans_settings",
        description="🔧⚙️ Get VLAN settings for the network"
    )
    def get_network_appliance_vlans_settings(
        network_id: str
    ):
        """Get VLAN settings."""
        try:
            result = meraki_client.dashboard.appliance.getNetworkApplianceVlansSettings(network_id)
            
            response = f"# ⚙️ VLAN Settings\n\n"
            response += f"**VLANs Enabled**: {'✅' if result.get('vlansEnabled') else '❌'}\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting VLAN settings: {str(e)}"
    
    @app.tool(
        name="update_network_appliance_vlans_settings",
        description="🔧⚙️ Enable or disable VLANs on the network"
    )
    def update_network_appliance_vlans_settings(
        network_id: str,
        vlans_enabled: bool
    ):
        """Update VLAN settings."""
        try:
            result = meraki_client.dashboard.appliance.updateNetworkApplianceVlansSettings(
                network_id, vlansEnabled=vlans_enabled
            )
            
            response = f"# ✅ VLAN Settings Updated\n\n"
            response += f"**VLANs**: {'Enabled' if vlans_enabled else 'Disabled'}\n"
            
            return response
        except Exception as e:
            return f"❌ Error updating VLAN settings: {str(e)}"
    
    # ==================== STATIC ROUTES ====================
    
    # SKIP: Already defined in tools_appliance.py
    '''@app.tool(
        name="create_network_appliance_static_route",
        description="🔧🛤️ Create static route (name, subnet, gateway_ip, gateway_vlan_id)"
    )
    def create_network_appliance_static_route(
        network_id: str,
        name: str,
        subnet: str,
        gateway_ip: Optional[str] = None,
        gateway_vlan_id: Optional[str] = None,
        enabled: Optional[bool] = True
    ):
        """
        Create static route.
        
        Args:
            network_id: Network ID
            name: Route name
            subnet: Destination subnet (e.g., 192.168.2.0/24)
            gateway_ip: Next hop IP address
            gateway_vlan_id: Next hop VLAN ID (if using VLAN as gateway)
            enabled: Enable the route
        """
        try:
            kwargs = {
                'name': name,
                'subnet': subnet,
                'enabled': enabled
            }
            
            if gateway_ip:
                kwargs['gatewayIp'] = gateway_ip
            elif gateway_vlan_id:
                kwargs['gatewayVlanId'] = gateway_vlan_id
            else:
                return "❌ Either gateway_ip or gateway_vlan_id must be specified"
            
            result = meraki_client.dashboard.appliance.createNetworkApplianceStaticRoute(
                network_id, **kwargs
            )
            
            response = f"# ✅ Static Route Created\n\n"
            response += f"**Name**: {name}\n"
            response += f"**Subnet**: {subnet}\n"
            if gateway_ip:
                response += f"**Gateway**: {gateway_ip}\n"
            else:
                response += f"**Gateway VLAN**: {gateway_vlan_id}\n"
            
            return response
        except Exception as e:
            return f"❌ Error creating static route: {str(e)}"'''
    
    @app.tool(
        name="delete_network_appliance_static_route",
        description="🔧❌ Delete a static route"
    )
    def delete_network_appliance_static_route(
        network_id: str,
        static_route_id: str
    ):
        """Delete static route."""
        try:
            meraki_client.dashboard.appliance.deleteNetworkApplianceStaticRoute(
                network_id, static_route_id
            )
            
            response = f"# ✅ Static Route Deleted\n\n"
            response += f"**Route ID**: {static_route_id}\n"
            
            return response
        except Exception as e:
            return f"❌ Error deleting static route: {str(e)}"
    
    @app.tool(
        name="get_network_appliance_static_route",
        description="🔧🛤️ Get details of a specific static route"
    )
    def get_network_appliance_static_route(
        network_id: str,
        static_route_id: str
    ):
        """Get static route details."""
        try:
            result = meraki_client.dashboard.appliance.getNetworkApplianceStaticRoute(
                network_id, static_route_id
            )
            
            response = f"# 🛤️ Static Route Details\n\n"
            response += f"**ID**: {static_route_id}\n"
            response += f"**Name**: {result.get('name', 'N/A')}\n"
            response += f"**Subnet**: {result.get('subnet', 'N/A')}\n"
            response += f"**Gateway IP**: {result.get('gatewayIp', 'N/A')}\n"
            response += f"**Gateway VLAN**: {result.get('gatewayVlanId', 'N/A')}\n"
            response += f"**Enabled**: {'✅' if result.get('enabled') else '❌'}\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting static route: {str(e)}"
    
    # SKIP: Already defined in tools_appliance.py
    '''@app.tool(
        name="get_network_appliance_static_routes",
        description="🔧🛤️ List all static routes for the network"
    )
    def get_network_appliance_static_routes(
        network_id: str
    ):
        """Get all static routes."""
        try:
            result = meraki_client.dashboard.appliance.getNetworkApplianceStaticRoutes(network_id)
            
            response = f"# 🛤️ Static Routes\n\n"
            
            if result and isinstance(result, list):
                response += f"**Total Routes**: {len(result)}\n\n"
                
                for route in result:
                    enabled = '✅' if route.get('enabled') else '❌'
                    response += f"## {enabled} {route.get('name', 'Unknown')}\n"
                    response += f"- ID: {route.get('id')}\n"
                    response += f"- Subnet: {route.get('subnet')}\n"
                    response += f"- Gateway: {route.get('gatewayIp', route.get('gatewayVlanId', 'N/A'))}\n\n"
            else:
                response += "*No static routes configured*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting static routes: {str(e)}"'''
    
    @app.tool(
        name="update_network_appliance_static_route",
        description="🔧✏️ Update static route settings"
    )
    def update_network_appliance_static_route(
        network_id: str,
        static_route_id: str,
        name: Optional[str] = None,
        subnet: Optional[str] = None,
        gateway_ip: Optional[str] = None,
        enabled: Optional[bool] = None
    ):
        """Update static route."""
        try:
            kwargs = {}
            
            if name:
                kwargs['name'] = name
            if subnet:
                kwargs['subnet'] = subnet
            if gateway_ip:
                kwargs['gatewayIp'] = gateway_ip
            if enabled is not None:
                kwargs['enabled'] = enabled
            
            result = meraki_client.dashboard.appliance.updateNetworkApplianceStaticRoute(
                network_id, static_route_id, **kwargs
            )
            
            response = f"# ✅ Static Route Updated\n\n"
            response += f"**Route ID**: {static_route_id}\n"
            if name:
                response += f"**Name**: {name}\n"
            if subnet:
                response += f"**Subnet**: {subnet}\n"
            
            return response
        except Exception as e:
            return f"❌ Error updating static route: {str(e)}"
    
    # ==================== TRAFFIC SHAPING ====================
    
    @app.tool(
        name="get_network_appliance_traffic_shaping",
        description="🔧🚦 Get traffic shaping settings"
    )
    def get_network_appliance_traffic_shaping(
        network_id: str
    ):
        """Get traffic shaping configuration."""
        try:
            result = meraki_client.dashboard.appliance.getNetworkApplianceTrafficShaping(network_id)
            
            response = f"# 🚦 Traffic Shaping Settings\n\n"
            
            # Global bandwidth limits
            global_bw = result.get('globalBandwidthLimits', {})
            if global_bw:
                response += "## Global Bandwidth Limits\n"
                response += f"- Download: {global_bw.get('limitDown', 'Unlimited')} Mbps\n"
                response += f"- Upload: {global_bw.get('limitUp', 'Unlimited')} Mbps\n\n"
            
            # Per-client limits
            per_client = result.get('perClientBandwidthLimits', {})
            if per_client:
                response += "## Per-Client Limits\n"
                response += f"- Download: {per_client.get('limitDown', 'Unlimited')} Mbps\n"
                response += f"- Upload: {per_client.get('limitUp', 'Unlimited')} Mbps\n\n"
            
            # Traffic shaping rules
            rules = result.get('rules', [])
            if rules:
                response += f"## Traffic Shaping Rules ({len(rules)})\n"
                for rule in rules[:5]:
                    response += f"### {rule.get('definitions', [{}])[0].get('value', 'Unknown')}\n"
                    response += f"- Priority: {rule.get('priority', 'normal')}\n"
                    
                    per_client = rule.get('perClientBandwidthLimits', {})
                    if per_client:
                        response += f"- Limits: {per_client.get('limitDown', 'N/A')}↓/{per_client.get('limitUp', 'N/A')}↑ Mbps\n"
                    
                    dscp = rule.get('dscpTagValue')
                    if dscp:
                        response += f"- DSCP Tag: {dscp}\n"
                    response += "\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting traffic shaping: {str(e)}"
    
    @app.tool(
        name="update_network_appliance_traffic_shaping",
        description="🔧🚦 Update traffic shaping (global_limit_down, global_limit_up Mbps)"
    )
    def update_network_appliance_traffic_shaping(
        network_id: str,
        global_limit_down: Optional[int] = None,
        global_limit_up: Optional[int] = None,
        per_client_limit_down: Optional[int] = None,
        per_client_limit_up: Optional[int] = None
    ):
        """Update traffic shaping settings."""
        try:
            kwargs = {}
            
            if global_limit_down is not None or global_limit_up is not None:
                kwargs['globalBandwidthLimits'] = {}
                if global_limit_down is not None:
                    kwargs['globalBandwidthLimits']['limitDown'] = global_limit_down
                if global_limit_up is not None:
                    kwargs['globalBandwidthLimits']['limitUp'] = global_limit_up
            
            if per_client_limit_down is not None or per_client_limit_up is not None:
                kwargs['perClientBandwidthLimits'] = {}
                if per_client_limit_down is not None:
                    kwargs['perClientBandwidthLimits']['limitDown'] = per_client_limit_down
                if per_client_limit_up is not None:
                    kwargs['perClientBandwidthLimits']['limitUp'] = per_client_limit_up
            
            result = meraki_client.dashboard.appliance.updateNetworkApplianceTrafficShaping(
                network_id, **kwargs
            )
            
            response = f"# ✅ Traffic Shaping Updated\n\n"
            if global_limit_down or global_limit_up:
                response += f"**Global Limits**: {global_limit_down or 'N/A'}↓/{global_limit_up or 'N/A'}↑ Mbps\n"
            if per_client_limit_down or per_client_limit_up:
                response += f"**Per-Client**: {per_client_limit_down or 'N/A'}↓/{per_client_limit_up or 'N/A'}↑ Mbps\n"
            
            return response
        except Exception as e:
            return f"❌ Error updating traffic shaping: {str(e)}"
    
    @app.tool(
        name="create_network_appliance_traffic_shaping_custom",
        description="🔧🎯 Create custom performance class for traffic shaping"
    )
    def create_network_appliance_traffic_shaping_custom(
        network_id: str,
        name: str,
        max_latency: Optional[int] = 100,
        max_jitter: Optional[int] = 100,
        max_loss_percentage: Optional[int] = 5
    ):
        """
        Create custom performance class.
        
        Args:
            network_id: Network ID
            name: Class name
            max_latency: Maximum latency in ms (default 100)
            max_jitter: Maximum jitter in ms (default 100)
            max_loss_percentage: Maximum loss percentage (default 5)
        """
        try:
            kwargs = {
                'name': name,
                'maxLatency': max_latency,
                'maxJitter': max_jitter,
                'maxLossPercentage': max_loss_percentage
            }
            
            result = meraki_client.dashboard.appliance.createNetworkApplianceTrafficShapingCustomPerformanceClass(
                network_id, **kwargs
            )
            
            response = f"# ✅ Custom Performance Class Created\n\n"
            response += f"**Name**: {name}\n"
            response += f"**Max Latency**: {max_latency}ms\n"
            response += f"**Max Jitter**: {max_jitter}ms\n"
            response += f"**Max Loss**: {max_loss_percentage}%\n"
            
            return response
        except Exception as e:
            return f"❌ Error creating performance class: {str(e)}"
    
    @app.tool(
        name="delete_network_appliance_traffic_shaping_custom",
        description="🔧❌ Delete custom performance class"
    )
    def delete_network_appliance_traffic_shaping_custom(
        network_id: str,
        custom_performance_class_id: str
    ):
        """Delete custom performance class."""
        try:
            meraki_client.dashboard.appliance.deleteNetworkApplianceTrafficShapingCustomPerformanceClass(
                network_id, custom_performance_class_id
            )
            
            response = f"# ✅ Performance Class Deleted\n\n"
            response += f"**Class ID**: {custom_performance_class_id}\n"
            
            return response
        except Exception as e:
            return f"❌ Error deleting performance class: {str(e)}"
    
    @app.tool(
        name="get_network_appliance_traffic_shaping_custom",
        description="🔧🎯 Get custom performance class details"
    )
    def get_network_appliance_traffic_shaping_custom(
        network_id: str,
        custom_performance_class_id: str
    ):
        """Get custom performance class."""
        try:
            result = meraki_client.dashboard.appliance.getNetworkApplianceTrafficShapingCustomPerformanceClass(
                network_id, custom_performance_class_id
            )
            
            response = f"# 🎯 Custom Performance Class\n\n"
            response += f"**ID**: {custom_performance_class_id}\n"
            response += f"**Name**: {result.get('name', 'N/A')}\n"
            response += f"**Max Latency**: {result.get('maxLatency', 'N/A')}ms\n"
            response += f"**Max Jitter**: {result.get('maxJitter', 'N/A')}ms\n"
            response += f"**Max Loss**: {result.get('maxLossPercentage', 'N/A')}%\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting performance class: {str(e)}"
    
    @app.tool(
        name="get_network_appliance_traffic_shaping_custom_classes",
        description="🔧🎯 List all custom performance classes"
    )
    def get_network_appliance_traffic_shaping_custom_classes(
        network_id: str
    ):
        """Get all custom performance classes."""
        try:
            result = meraki_client.dashboard.appliance.getNetworkApplianceTrafficShapingCustomPerformanceClasses(
                network_id
            )
            
            response = f"# 🎯 Custom Performance Classes\n\n"
            
            if result and isinstance(result, list):
                response += f"**Total Classes**: {len(result)}\n\n"
                
                for perf_class in result:
                    response += f"## {perf_class.get('name', 'Unknown')}\n"
                    response += f"- ID: {perf_class.get('id')}\n"
                    response += f"- Latency: ≤{perf_class.get('maxLatency')}ms\n"
                    response += f"- Jitter: ≤{perf_class.get('maxJitter')}ms\n"
                    response += f"- Loss: ≤{perf_class.get('maxLossPercentage')}%\n\n"
            else:
                response += "*No custom performance classes defined*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting performance classes: {str(e)}"
    
    @app.tool(
        name="update_network_appliance_traffic_shaping_custom",
        description="🔧✏️ Update custom performance class parameters"
    )
    def update_network_appliance_traffic_shaping_custom(
        network_id: str,
        custom_performance_class_id: str,
        name: Optional[str] = None,
        max_latency: Optional[int] = None,
        max_jitter: Optional[int] = None,
        max_loss_percentage: Optional[int] = None
    ):
        """Update custom performance class."""
        try:
            kwargs = {}
            
            if name:
                kwargs['name'] = name
            if max_latency is not None:
                kwargs['maxLatency'] = max_latency
            if max_jitter is not None:
                kwargs['maxJitter'] = max_jitter
            if max_loss_percentage is not None:
                kwargs['maxLossPercentage'] = max_loss_percentage
            
            result = meraki_client.dashboard.appliance.updateNetworkApplianceTrafficShapingCustomPerformanceClass(
                network_id, custom_performance_class_id, **kwargs
            )
            
            response = f"# ✅ Performance Class Updated\n\n"
            response += f"**Class ID**: {custom_performance_class_id}\n"
            if name:
                response += f"**Name**: {name}\n"
            if max_latency:
                response += f"**Max Latency**: {max_latency}ms\n"
            
            return response
        except Exception as e:
            return f"❌ Error updating performance class: {str(e)}"
    
    # ==================== RF PROFILES ====================
    
    @app.tool(
        name="create_network_appliance_rf_profile",
        description="🔧📡 Create RF profile for wireless on MX (name, settings)"
    )
    def create_network_appliance_rf_profile(
        network_id: str,
        name: str,
        two_four_ghz_settings: Optional[str] = None,
        five_ghz_settings: Optional[str] = None,
        per_ssid_settings: Optional[str] = None
    ):
        """
        Create RF profile.
        
        Args:
            network_id: Network ID
            name: Profile name
            two_four_ghz_settings: JSON string for 2.4GHz settings
            five_ghz_settings: JSON string for 5GHz settings
            per_ssid_settings: JSON string for per-SSID settings
        """
        try:
            kwargs = {'name': name}
            
            if two_four_ghz_settings:
                kwargs['twoFourGhzSettings'] = json.loads(two_four_ghz_settings)
            if five_ghz_settings:
                kwargs['fiveGhzSettings'] = json.loads(five_ghz_settings)
            if per_ssid_settings:
                kwargs['perSsidSettings'] = json.loads(per_ssid_settings)
            
            result = meraki_client.dashboard.appliance.createNetworkApplianceRfProfile(
                network_id, **kwargs
            )
            
            response = f"# ✅ RF Profile Created\n\n"
            response += f"**Name**: {name}\n"
            response += f"**Profile ID**: {result.get('id', 'N/A')}\n"
            
            return response
        except Exception as e:
            return f"❌ Error creating RF profile: {str(e)}"
    
    @app.tool(
        name="delete_network_appliance_rf_profile",
        description="🔧❌ Delete RF profile"
    )
    def delete_network_appliance_rf_profile(
        network_id: str,
        rf_profile_id: str
    ):
        """Delete RF profile."""
        try:
            meraki_client.dashboard.appliance.deleteNetworkApplianceRfProfile(
                network_id, rf_profile_id
            )
            
            response = f"# ✅ RF Profile Deleted\n\n"
            response += f"**Profile ID**: {rf_profile_id}\n"
            
            return response
        except Exception as e:
            return f"❌ Error deleting RF profile: {str(e)}"
    
    @app.tool(
        name="get_network_appliance_rf_profile",
        description="🔧📡 Get RF profile details"
    )
    def get_network_appliance_rf_profile(
        network_id: str,
        rf_profile_id: str
    ):
        """Get RF profile."""
        try:
            result = meraki_client.dashboard.appliance.getNetworkApplianceRfProfile(
                network_id, rf_profile_id
            )
            
            response = f"# 📡 RF Profile Details\n\n"
            response += f"**ID**: {rf_profile_id}\n"
            response += f"**Name**: {result.get('name', 'N/A')}\n"
            response += f"**Network**: {result.get('networkId', 'N/A')}\n\n"
            
            # 2.4GHz settings
            two_four = result.get('twoFourGhzSettings', {})
            if two_four:
                response += "## 2.4GHz Settings\n"
                response += f"- Min Bitrate: {two_four.get('minBitrate', 'N/A')}\n"
                response += f"- Ax Enabled: {'✅' if two_four.get('axEnabled') else '❌'}\n\n"
            
            # 5GHz settings
            five = result.get('fiveGhzSettings', {})
            if five:
                response += "## 5GHz Settings\n"
                response += f"- Min Bitrate: {five.get('minBitrate', 'N/A')}\n"
                response += f"- Channel Width: {five.get('channelWidth', 'N/A')}\n\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting RF profile: {str(e)}"
    
    @app.tool(
        name="get_network_appliance_rf_profiles",
        description="🔧📡 List all RF profiles for the network"
    )
    def get_network_appliance_rf_profiles(
        network_id: str
    ):
        """Get all RF profiles."""
        try:
            result = meraki_client.dashboard.appliance.getNetworkApplianceRfProfiles(network_id)
            
            response = f"# 📡 RF Profiles\n\n"
            
            # Assigned profile
            assigned = result.get('assigned', [])
            if assigned:
                response += "## Assigned Profiles\n"
                for profile in assigned:
                    response += f"- {profile.get('name', 'Unknown')} (ID: {profile.get('id')})\n"
                response += "\n"
            
            # Available profiles
            profiles = result.get('profiles', [])
            if profiles:
                response += f"## Available Profiles ({len(profiles)})\n"
                for profile in profiles:
                    response += f"### {profile.get('name', 'Unknown')}\n"
                    response += f"- ID: {profile.get('id')}\n"
                    response += f"- Network: {profile.get('networkId', 'N/A')}\n\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting RF profiles: {str(e)}"
    
    @app.tool(
        name="update_network_appliance_rf_profile",
        description="🔧✏️ Update RF profile settings"
    )
    def update_network_appliance_rf_profile(
        network_id: str,
        rf_profile_id: str,
        name: Optional[str] = None,
        two_four_ghz_settings: Optional[str] = None,
        five_ghz_settings: Optional[str] = None
    ):
        """Update RF profile."""
        try:
            kwargs = {}
            
            if name:
                kwargs['name'] = name
            if two_four_ghz_settings:
                kwargs['twoFourGhzSettings'] = json.loads(two_four_ghz_settings)
            if five_ghz_settings:
                kwargs['fiveGhzSettings'] = json.loads(five_ghz_settings)
            
            result = meraki_client.dashboard.appliance.updateNetworkApplianceRfProfile(
                network_id, rf_profile_id, **kwargs
            )
            
            response = f"# ✅ RF Profile Updated\n\n"
            response += f"**Profile ID**: {rf_profile_id}\n"
            if name:
                response += f"**Name**: {name}\n"
            
            return response
        except Exception as e:
            return f"❌ Error updating RF profile: {str(e)}"
    
    # ==================== PREFIXES ====================
    
    @app.tool(
        name="get_network_appliance_prefixes_delegated",
        description="🔧🔢 Get delegated IPv6 prefixes"
    )
    def get_network_appliance_prefixes_delegated(
        network_id: str
    ):
        """Get delegated prefixes."""
        try:
            result = meraki_client.dashboard.appliance.getNetworkAppliancePrefixesDelegated(network_id)
            
            response = f"# 🔢 Delegated Prefixes\n\n"
            
            if result and isinstance(result, list):
                response += f"**Total Prefixes**: {len(result)}\n\n"
                
                for prefix in result:
                    response += f"## {prefix.get('prefix', 'Unknown')}\n"
                    response += f"- Origin: {prefix.get('origin', 'N/A')}\n"
                    response += f"- Description: {prefix.get('description', 'N/A')}\n\n"
            else:
                response += "*No delegated prefixes configured*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting delegated prefixes: {str(e)}"
    
    @app.tool(
        name="create_network_appliance_prefixes_delegated_static",
        description="🔧➕ Create static delegated IPv6 prefix"
    )
    def create_network_appliance_prefixes_delegated_static(
        network_id: str,
        prefix: str,
        origin_type: str,
        origin_interfaces: str,
        description: Optional[str] = None
    ):
        """
        Create static delegated prefix.
        
        Args:
            network_id: Network ID
            prefix: IPv6 prefix (e.g., 2001:db8::/48)
            origin_type: Origin type ('internet' or 'wan')
            origin_interfaces: Comma-separated interface names
            description: Description (optional)
        """
        try:
            interfaces = [i.strip() for i in origin_interfaces.split(',')]
            
            kwargs = {
                'prefix': prefix,
                'origin': {
                    'type': origin_type,
                    'interfaces': interfaces
                }
            }
            
            if description:
                kwargs['description'] = description
            
            result = meraki_client.dashboard.appliance.createNetworkAppliancePrefixesDelegatedStatic(
                network_id, **kwargs
            )
            
            response = f"# ✅ Static Delegated Prefix Created\n\n"
            response += f"**Prefix**: {prefix}\n"
            response += f"**Origin**: {origin_type}\n"
            response += f"**Interfaces**: {origin_interfaces}\n"
            
            return response
        except Exception as e:
            return f"❌ Error creating delegated prefix: {str(e)}"
    
    @app.tool(
        name="delete_network_appliance_prefixes_delegated_static",
        description="🔧❌ Delete static delegated prefix"
    )
    def delete_network_appliance_prefixes_delegated_static(
        network_id: str,
        static_delegated_prefix_id: str
    ):
        """Delete static delegated prefix."""
        try:
            meraki_client.dashboard.appliance.deleteNetworkAppliancePrefixesDelegatedStatic(
                network_id, static_delegated_prefix_id
            )
            
            response = f"# ✅ Delegated Prefix Deleted\n\n"
            response += f"**Prefix ID**: {static_delegated_prefix_id}\n"
            
            return response
        except Exception as e:
            return f"❌ Error deleting delegated prefix: {str(e)}"
    
    @app.tool(
        name="get_network_appliance_prefixes_delegated_static",
        description="🔧🔢 Get specific static delegated prefix"
    )
    def get_network_appliance_prefixes_delegated_static(
        network_id: str,
        static_delegated_prefix_id: str
    ):
        """Get static delegated prefix."""
        try:
            result = meraki_client.dashboard.appliance.getNetworkAppliancePrefixesDelegatedStatic(
                network_id, static_delegated_prefix_id
            )
            
            response = f"# 🔢 Static Delegated Prefix\n\n"
            response += f"**ID**: {static_delegated_prefix_id}\n"
            response += f"**Prefix**: {result.get('prefix', 'N/A')}\n"
            response += f"**Description**: {result.get('description', 'N/A')}\n"
            
            origin = result.get('origin', {})
            if origin:
                response += f"**Origin Type**: {origin.get('type', 'N/A')}\n"
                response += f"**Interfaces**: {', '.join(origin.get('interfaces', []))}\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting delegated prefix: {str(e)}"
    
    @app.tool(
        name="get_network_appliance_prefixes_delegated_statics",
        description="🔧🔢 List all static delegated prefixes"
    )
    def get_network_appliance_prefixes_delegated_statics(
        network_id: str
    ):
        """Get all static delegated prefixes."""
        try:
            result = meraki_client.dashboard.appliance.getNetworkAppliancePrefixesDelegatedStatics(network_id)
            
            response = f"# 🔢 Static Delegated Prefixes\n\n"
            
            if result and isinstance(result, list):
                response += f"**Total Prefixes**: {len(result)}\n\n"
                
                for prefix in result:
                    response += f"## {prefix.get('prefix', 'Unknown')}\n"
                    response += f"- ID: {prefix.get('staticDelegatedPrefixId')}\n"
                    response += f"- Description: {prefix.get('description', 'N/A')}\n"
                    
                    origin = prefix.get('origin', {})
                    if origin:
                        response += f"- Origin: {origin.get('type')} ({', '.join(origin.get('interfaces', []))})\n"
                    response += "\n"
            else:
                response += "*No static delegated prefixes configured*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting static delegated prefixes: {str(e)}"
    
    @app.tool(
        name="update_network_appliance_prefixes_delegated_static",
        description="🔧✏️ Update static delegated prefix"
    )
    def update_network_appliance_prefixes_delegated_static(
        network_id: str,
        static_delegated_prefix_id: str,
        prefix: Optional[str] = None,
        origin_type: Optional[str] = None,
        origin_interfaces: Optional[str] = None,
        description: Optional[str] = None
    ):
        """Update static delegated prefix."""
        try:
            kwargs = {}
            
            if prefix:
                kwargs['prefix'] = prefix
            if origin_type and origin_interfaces:
                interfaces = [i.strip() for i in origin_interfaces.split(',')]
                kwargs['origin'] = {
                    'type': origin_type,
                    'interfaces': interfaces
                }
            if description:
                kwargs['description'] = description
            
            result = meraki_client.dashboard.appliance.updateNetworkAppliancePrefixesDelegatedStatic(
                network_id, static_delegated_prefix_id, **kwargs
            )
            
            response = f"# ✅ Delegated Prefix Updated\n\n"
            response += f"**Prefix ID**: {static_delegated_prefix_id}\n"
            if prefix:
                response += f"**Prefix**: {prefix}\n"
            
            return response
        except Exception as e:
            return f"❌ Error updating delegated prefix: {str(e)}"