"""
Switch management tools for Cisco Meraki MCP server.

This module provides comprehensive switch management tools covering all SDK methods.
Includes port configuration, VLANs, routing, QoS, storm control, STP, and more.
"""

from typing import Optional, Dict, Any, List
import json

# Global references to be set by register function
app = None
meraki_client = None

def register_switch_tools(mcp_app, meraki):
    """
    Register switch tools with the MCP server.
    
    Args:
        mcp_app: MCP server instance
        meraki: Meraki client instance
    """
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    
    # Register tool handlers
    register_switch_tool_handlers()

def register_switch_tool_handlers():
    """Register all switch tool handlers."""
    
    # ==================== SWITCH PORTS ====================
    
    @app.tool(
        name="get_device_switch_ports",
        description="📊 List all switch ports for a switch. Shows port configuration including VLANs, PoE, and settings."
    )
    def get_device_switch_ports(
        serial: str
    ):
        """
        List the switch ports for a switch.
        
        Args:
            serial: Switch serial number (e.g. Q2SW-XXXX-XXXX)
        """
        try:
            result = meraki_client.dashboard.switch.getDeviceSwitchPorts(serial)
            
            response = f"# 🔌 Switch Ports for {serial}\n\n"
            
            if result and isinstance(result, list):
                response += f"**Total Ports**: {len(result)}\n\n"
                
                for port in result:
                    port_id = port.get('portId', 'Unknown')
                    response += f"## Port {port_id}\n"
                    response += f"- **Name**: {port.get('name', 'Unnamed')}\n"
                    response += f"- **Enabled**: {port.get('enabled', False)}\n"
                    response += f"- **Type**: {port.get('type', 'trunk')}\n"
                    response += f"- **VLAN**: {port.get('vlan', 'N/A')}\n"
                    response += f"- **Voice VLAN**: {port.get('voiceVlan', 'N/A')}\n"
                    response += f"- **Allowed VLANs**: {port.get('allowedVlans', 'all')}\n"
                    response += f"- **PoE Enabled**: {port.get('poeEnabled', False)}\n"
                    response += f"- **Isolation**: {port.get('isolationEnabled', False)}\n"
                    response += f"- **RSTP**: {port.get('rstpEnabled', True)}\n"
                    response += f"- **STP Guard**: {port.get('stpGuard', 'disabled')}\n"
                    response += f"- **Link Negotiation**: {port.get('linkNegotiation', 'Auto')}\n"
                    response += "\n"
            else:
                response += "*No ports found or not a switch*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting switch ports: {str(e)}"
    
    @app.tool(
        name="cycle_device_switch_ports", 
        description="🔄 Cycle (reboot) a set of switch ports. Requires confirmation. Use to reset stuck ports."
    )
    def cycle_device_switch_ports(
        serial: str,
        ports: str,
        confirmed: bool = False
    ):
        """
        Cycle a set of switch ports (power cycle/reboot).
        
        Args:
            serial: Switch serial number
            ports: Comma-separated port IDs to cycle (e.g. "1,2,5")
            confirmed: Must be true to execute
        """
        if not confirmed:
            return "⚠️ Port cycling requires confirmed=true to execute. This will temporarily disconnect devices!"
        
        try:
            port_list = [p.strip() for p in ports.split(',')]
            result = meraki_client.dashboard.switch.cycleDeviceSwitchPorts(
                serial, ports=port_list
            )
            
            response = f"# ✅ Cycled Switch Ports\n\n"
            response += f"**Switch**: {serial}\n"
            response += f"**Cycled Ports**: {', '.join(port_list)}\n\n"
            response += "⚠️ Ports are rebooting. Connected devices will reconnect momentarily.\n"
            
            return response
        except Exception as e:
            return f"❌ Error cycling ports: {str(e)}"
    
    @app.tool(
        name="get_device_switch_ports_statuses",
        description="🟢 Get real-time status for all switch ports including link state, speed, duplex, traffic, errors, and warnings."
    )
    def get_device_switch_ports_statuses(
        serial: str,
        timespan: Optional[int] = None
    ):
        """
        Return the status for all ports of a switch.
        
        Args:
            serial: Switch serial number
            timespan: Timespan in seconds (default 1 day)
        """
        try:
            kwargs = {}
            if timespan:
                kwargs['timespan'] = timespan
            
            result = meraki_client.dashboard.switch.getDeviceSwitchPortsStatuses(serial, **kwargs)
            
            response = f"# 🟢 Switch Port Statuses - {serial}\n\n"
            
            if result and isinstance(result, list):
                active_ports = [p for p in result if p.get('status') == 'Connected']
                response += f"**Active Ports**: {len(active_ports)}/{len(result)}\n\n"
                
                for port in result:
                    port_id = port.get('portId', 'Unknown')
                    status = port.get('status', 'Unknown')
                    status_icon = "🟢" if status == 'Connected' else "⚫"
                    
                    response += f"## {status_icon} Port {port_id}\n"
                    response += f"- **Status**: {status}\n"
                    response += f"- **Speed**: {port.get('speed', 'N/A')} Mbps\n"
                    response += f"- **Duplex**: {port.get('duplex', 'N/A')}\n"
                    
                    # Traffic stats
                    usage = port.get('usageInKb', {})
                    if usage:
                        response += f"- **Traffic Sent**: {usage.get('sent', 0)/1024:.2f} MB\n"
                        response += f"- **Traffic Received**: {usage.get('recv', 0)/1024:.2f} MB\n"
                    
                    # Errors
                    errors = port.get('errors', [])
                    if errors:
                        response += f"- **Errors**: {', '.join(errors)}\n"
                    
                    # Warnings
                    warnings = port.get('warnings', [])
                    if warnings:
                        response += f"- **Warnings**: {', '.join(warnings)}\n"
                    
                    # Client info
                    client_count = port.get('clientCount', 0)
                    if client_count:
                        response += f"- **Connected Clients**: {client_count}\n"
                    
                    response += "\n"
            else:
                response += "*No port status data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting port statuses: {str(e)}"
    
    @app.tool(
        name="get_device_switch_ports_packets",
        description="📊 Get packet counters for all switch ports including sent/received packets and rates."
    )
    def get_device_switch_ports_packets(
        serial: str,
        timespan: Optional[int] = None
    ):
        """
        Return packet counters for all ports of a switch.
        
        Args:
            serial: Switch serial number
            timespan: Timespan in seconds
        """
        try:
            kwargs = {}
            if timespan:
                kwargs['timespan'] = timespan
            
            result = meraki_client.dashboard.switch.getDeviceSwitchPortsStatusesPackets(serial, **kwargs)
            
            response = f"# 📊 Switch Port Packet Counters - {serial}\n\n"
            
            if result and isinstance(result, list):
                total_packets = sum(p.get('packets', {}).get('sent', 0) + 
                                  p.get('packets', {}).get('recv', 0) for p in result)
                response += f"**Total Packets**: {total_packets:,}\n\n"
                
                for port in result:
                    port_id = port.get('portId', 'Unknown')
                    packets = port.get('packets', {})
                    
                    response += f"## Port {port_id}\n"
                    response += f"- **Packets Sent**: {packets.get('sent', 0):,}\n"
                    response += f"- **Packets Received**: {packets.get('recv', 0):,}\n"
                    
                    # Rates if available
                    rate_per_sec = port.get('packetsPerSec', {})
                    if rate_per_sec:
                        response += f"- **Send Rate**: {rate_per_sec.get('sent', 0)} pps\n"
                        response += f"- **Receive Rate**: {rate_per_sec.get('recv', 0)} pps\n"
                    
                    response += "\n"
            else:
                response += "*No packet counter data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting packet counters: {str(e)}"
    
    @app.tool(
        name="get_device_switch_port",
        description="🔍 Get detailed configuration for a specific switch port."
    )
    def get_device_switch_port(
        serial: str,
        port_id: str
    ):
        """
        Return a specific switch port configuration.
        
        Args:
            serial: Switch serial number
            port_id: Port identifier (e.g. "1", "24")
        """
        try:
            result = meraki_client.dashboard.switch.getDeviceSwitchPort(serial, port_id)
            
            response = f"# 🔌 Switch Port {port_id} Details\n\n"
            response += f"**Switch**: {serial}\n\n"
            
            if result:
                response += f"## Configuration\n"
                response += f"- **Name**: {result.get('name', 'Unnamed')}\n"
                response += f"- **Enabled**: {result.get('enabled', False)}\n"
                response += f"- **Type**: {result.get('type', 'trunk')}\n"
                response += f"- **VLAN**: {result.get('vlan', 'N/A')}\n"
                response += f"- **Voice VLAN**: {result.get('voiceVlan', 'N/A')}\n"
                response += f"- **Allowed VLANs**: {result.get('allowedVlans', 'all')}\n"
                response += f"- **PoE Enabled**: {result.get('poeEnabled', False)}\n"
                response += f"- **Isolation**: {result.get('isolationEnabled', False)}\n"
                response += f"- **RSTP**: {result.get('rstpEnabled', True)}\n"
                response += f"- **STP Guard**: {result.get('stpGuard', 'disabled')}\n"
                response += f"- **Access Policy Type**: {result.get('accessPolicyType', 'Open')}\n"
                response += f"- **Link Negotiation**: {result.get('linkNegotiation', 'Auto')}\n"
                
                # Tags
                tags = result.get('tags', [])
                if tags:
                    response += f"- **Tags**: {', '.join(tags)}\n"
            else:
                response += "*Port not found*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting port details: {str(e)}"
    
    @app.tool(
        name="update_device_switch_port",
        description="⚙️ Update switch port configuration including VLAN, PoE, name, type, and other settings."
    )
    def update_device_switch_port(
        serial: str,
        port_id: str,
        name: Optional[str] = None,
        enabled: Optional[bool] = None,
        type: Optional[str] = None,
        vlan: Optional[int] = None,
        voice_vlan: Optional[int] = None,
        allowed_vlans: Optional[str] = None,
        poe_enabled: Optional[bool] = None,
        isolation_enabled: Optional[bool] = None,
        rstp_enabled: Optional[bool] = None,
        stp_guard: Optional[str] = None,
        link_negotiation: Optional[str] = None,
        tags: Optional[str] = None
    ):
        """
        Update a switch port configuration.
        
        Args:
            serial: Switch serial number
            port_id: Port identifier
            name: Port name/description
            enabled: Enable/disable port
            type: Port type (access or trunk)
            vlan: Access VLAN ID
            voice_vlan: Voice VLAN ID
            allowed_vlans: Allowed VLANs for trunk (e.g. "1,10,20" or "all")
            poe_enabled: Enable/disable PoE
            isolation_enabled: Enable port isolation
            rstp_enabled: Enable RSTP
            stp_guard: STP guard mode (disabled, root guard, bpdu guard, loop guard)
            link_negotiation: Auto negotiate or force speed (Auto, 100 Megabit full duplex, etc)
            tags: Comma-separated tags
        """
        try:
            kwargs = {}
            if name is not None:
                kwargs['name'] = name
            if enabled is not None:
                kwargs['enabled'] = enabled
            if type:
                kwargs['type'] = type
            if vlan:
                kwargs['vlan'] = vlan
            if voice_vlan:
                kwargs['voiceVlan'] = voice_vlan
            if allowed_vlans:
                kwargs['allowedVlans'] = allowed_vlans
            if poe_enabled is not None:
                kwargs['poeEnabled'] = poe_enabled
            if isolation_enabled is not None:
                kwargs['isolationEnabled'] = isolation_enabled
            if rstp_enabled is not None:
                kwargs['rstpEnabled'] = rstp_enabled
            if stp_guard:
                kwargs['stpGuard'] = stp_guard
            if link_negotiation:
                kwargs['linkNegotiation'] = link_negotiation
            if tags:
                kwargs['tags'] = [t.strip() for t in tags.split(',')]
            
            result = meraki_client.dashboard.switch.updateDeviceSwitchPort(
                serial, port_id, **kwargs
            )
            
            response = f"# ✅ Updated Switch Port {port_id}\n\n"
            response += f"**Switch**: {serial}\n\n"
            response += "## New Configuration\n"
            
            for key, value in kwargs.items():
                response += f"- **{key}**: {value}\n"
            
            return response
        except Exception as e:
            return f"❌ Error updating port: {str(e)}"
    
    # ==================== ROUTING ====================
    
    @app.tool(
        name="get_device_switch_routing_interfaces",
        description="🛣️ List layer 3 interfaces for a switch. Shows VLANs, IPs, and routing configuration."
    )
    def get_device_switch_routing_interfaces(
        serial: str
    ):
        """
        List layer 3 interfaces for a switch.
        
        Args:
            serial: Switch serial number
        """
        try:
            result = meraki_client.dashboard.switch.getDeviceSwitchRoutingInterfaces(serial)
            
            response = f"# 🛣️ Layer 3 Routing Interfaces - {serial}\n\n"
            
            if result and isinstance(result, list):
                response += f"**Total Interfaces**: {len(result)}\n\n"
                
                for interface in result:
                    response += f"## Interface {interface.get('interfaceId', 'Unknown')}\n"
                    response += f"- **Name**: {interface.get('name', 'Unnamed')}\n"
                    response += f"- **VLAN**: {interface.get('vlanId', 'N/A')}\n"
                    response += f"- **Subnet**: {interface.get('subnet', 'N/A')}\n"
                    response += f"- **Interface IP**: {interface.get('interfaceIp', 'N/A')}\n"
                    response += f"- **Multicast Routing**: {interface.get('multicastRouting', 'disabled')}\n"
                    response += f"- **Default Gateway**: {interface.get('defaultGateway', 'N/A')}\n"
                    
                    # OSPF settings
                    ospf = interface.get('ospfSettings', {})
                    if ospf:
                        response += f"- **OSPF Area**: {ospf.get('area', 'N/A')}\n"
                        response += f"- **OSPF Cost**: {ospf.get('cost', 'N/A')}\n"
                        response += f"- **OSPF Passive**: {ospf.get('isPassiveEnabled', False)}\n"
                    
                    response += "\n"
            else:
                response += "*No layer 3 interfaces configured*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting routing interfaces: {str(e)}"
    
    @app.tool(
        name="get_device_switch_routing_static_routes",
        description="🛤️ List static routes configured on a layer 3 switch."
    )
    def get_device_switch_routing_static_routes(
        serial: str
    ):
        """
        List static routes for a layer 3 switch.
        
        Args:
            serial: Switch serial number
        """
        try:
            result = meraki_client.dashboard.switch.getDeviceSwitchRoutingStaticRoutes(serial)
            
            response = f"# 🛤️ Static Routes - {serial}\n\n"
            
            if result and isinstance(result, list):
                response += f"**Total Routes**: {len(result)}\n\n"
                
                for route in result:
                    response += f"## Route {route.get('staticRouteId', 'Unknown')}\n"
                    response += f"- **Name**: {route.get('name', 'Unnamed')}\n"
                    response += f"- **Subnet**: {route.get('subnet', 'N/A')}\n"
                    response += f"- **Next Hop IP**: {route.get('nextHopIp', 'N/A')}\n"
                    response += f"- **Advertise via OSPF**: {route.get('advertiseViaOspfEnabled', False)}\n"
                    response += f"- **Prefer over OSPF**: {route.get('preferOverOspfRoutesEnabled', False)}\n"
                    response += "\n"
            else:
                response += "*No static routes configured*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting static routes: {str(e)}"
    
    @app.tool(
        name="get_device_switch_warm_spare",
        description="🔄 Get warm spare configuration for a switch stack. Shows redundancy setup."
    )
    def get_device_switch_warm_spare(
        serial: str
    ):
        """
        Get warm spare configuration for a switch.
        
        Args:
            serial: Switch serial number
        """
        try:
            result = meraki_client.dashboard.switch.getDeviceSwitchWarmSpare(serial)
            
            response = f"# 🔄 Warm Spare Configuration - {serial}\n\n"
            
            if result:
                response += f"**Enabled**: {result.get('enabled', False)}\n"
                response += f"**Primary Serial**: {result.get('primarySerial', 'N/A')}\n"
                response += f"**Spare Serial**: {result.get('spareSerial', 'N/A')}\n"
            else:
                response += "*No warm spare configured*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting warm spare config: {str(e)}"
    
    # ==================== NETWORK-WIDE SWITCH SETTINGS ====================
    
    @app.tool(
        name="get_network_switch_acls",
        description="🔒 Get Access Control Lists (ACLs) for the network. Shows security rules."
    )
    def get_network_switch_acls(
        network_id: str
    ):
        """
        Get network switch ACLs.
        
        Args:
            network_id: Network ID
        """
        try:
            result = meraki_client.dashboard.switch.getNetworkSwitchAccessControlLists(network_id)
            
            response = f"# 🔒 Network Switch ACLs\n\n"
            
            if result:
                rules = result.get('rules', [])
                response += f"**Total Rules**: {len(rules)}\n\n"
                
                for idx, rule in enumerate(rules, 1):
                    response += f"## Rule {idx}\n"
                    response += f"- **Policy**: {rule.get('policy', 'deny')}\n"
                    response += f"- **Protocol**: {rule.get('ipProtocol', 'any')}\n"
                    response += f"- **Source**: {rule.get('srcCidr', 'any')}\n"
                    response += f"- **Source Port**: {rule.get('srcPort', 'any')}\n"
                    response += f"- **Destination**: {rule.get('dstCidr', 'any')}\n"
                    response += f"- **Destination Port**: {rule.get('dstPort', 'any')}\n"
                    response += f"- **VLAN**: {rule.get('vlan', 'any')}\n"
                    response += f"- **Comment**: {rule.get('comment', 'N/A')}\n"
                    response += "\n"
            else:
                response += "*No ACLs configured*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting ACLs: {str(e)}"
    
    @app.tool(
        name="get_network_switch_access_policies",
        description="🔐 List all access policies for the network. Shows 802.1X, MAB, and guest policies."
    )
    def get_network_switch_access_policies(
        network_id: str
    ):
        """
        List access policies for a network.
        
        Args:
            network_id: Network ID
        """
        try:
            result = meraki_client.dashboard.switch.getNetworkSwitchAccessPolicies(network_id)
            
            response = f"# 🔐 Network Switch Access Policies\n\n"
            
            if result and isinstance(result, list):
                response += f"**Total Policies**: {len(result)}\n\n"
                
                for policy in result:
                    response += f"## {policy.get('name', 'Unnamed Policy')}\n"
                    response += f"- **Access Policy Type**: {policy.get('accessPolicyType', 'N/A')}\n"
                    response += f"- **Host Mode**: {policy.get('hostMode', 'Single-Host')}\n"
                    response += f"- **RADIUS Accounting**: {policy.get('radiusAccountingEnabled', False)}\n"
                    response += f"- **URL Redirect on Deny**: {policy.get('urlRedirectWalledGardenEnabled', False)}\n"
                    
                    # RADIUS servers
                    radius = policy.get('radiusServers', [])
                    if radius:
                        response += f"- **RADIUS Servers**: {len(radius)} configured\n"
                    
                    # Guest VLAN
                    response += f"- **Guest VLAN**: {policy.get('guestVlanId', 'N/A')}\n"
                    
                    response += "\n"
            else:
                response += "*No access policies configured*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting access policies: {str(e)}"
    
    @app.tool(
        name="get_network_switch_alternate_mgmt",
        description="🔧 Get alternate management interface configuration for switches."
    )
    def get_network_switch_alternate_mgmt(
        network_id: str
    ):
        """
        Get alternate management interface for network switches.
        
        Args:
            network_id: Network ID
        """
        try:
            result = meraki_client.dashboard.switch.getNetworkSwitchAlternateManagementInterface(network_id)
            
            response = f"# 🔧 Alternate Management Interface\n\n"
            
            if result:
                response += f"**Enabled**: {result.get('enabled', False)}\n"
                response += f"**VLAN**: {result.get('vlanId', 'N/A')}\n"
                response += f"**Protocol**: {result.get('protocols', [])}\n"
                
                # Switches using this config
                switches = result.get('switches', [])
                if switches:
                    response += f"\n## Configured Switches ({len(switches)})\n"
                    for switch in switches:
                        response += f"- **{switch.get('serial')}**: {switch.get('alternateManagementIp', 'N/A')}\n"
            else:
                response += "*Not configured*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting alternate management interface: {str(e)}"
    
    @app.tool(
        name="get_network_switch_dhcp_servers_seen",
        description="🖥️ List DHCP servers detected on the network. Helps identify rogue DHCP servers."
    )
    def get_network_switch_dhcp_servers_seen(
        network_id: str,
        timespan: Optional[int] = None
    ):
        """
        List DHCP servers seen on the network.
        
        Args:
            network_id: Network ID
            timespan: Timespan in seconds (default 1 day)
        """
        try:
            kwargs = {}
            if timespan:
                kwargs['timespan'] = timespan
            
            result = meraki_client.dashboard.switch.getNetworkSwitchDhcpV4ServersSeen(network_id, **kwargs)
            
            response = f"# 🖥️ DHCP Servers Detected\n\n"
            
            if result and isinstance(result, list):
                response += f"**Total Servers**: {len(result)}\n\n"
                
                for server in result:
                    response += f"## {server.get('mac', 'Unknown MAC')}\n"
                    response += f"- **IPv4**: {server.get('ipv4', {}).get('address', 'N/A')}\n"
                    response += f"- **IPv6**: {server.get('ipv6', {}).get('address', 'N/A')}\n"
                    response += f"- **Last Seen**: {server.get('lastSeenAt', 'N/A')}\n"
                    response += f"- **VLAN**: {server.get('vlan', 'N/A')}\n"
                    response += f"- **Packets Seen**: {server.get('lastPacket', {}).get('type', 'N/A')}\n"
                    
                    # Device info
                    device = server.get('device', {})
                    if device:
                        response += f"- **Seen on Switch**: {device.get('serial', 'N/A')}\n"
                        response += f"- **Port**: {device.get('interface', {}).get('portId', 'N/A')}\n"
                    
                    response += f"- **Trusted**: {server.get('isConfigured', False)}\n"
                    response += "\n"
                
                # Warning about rogue DHCP
                untrusted = [s for s in result if not s.get('isConfigured', False)]
                if untrusted:
                    response += f"⚠️ **Warning**: {len(untrusted)} untrusted DHCP server(s) detected!\n"
            else:
                response += "*No DHCP servers detected*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting DHCP servers: {str(e)}"
    
    @app.tool(
        name="get_network_switch_dhcp_server_policy",
        description="📋 Get DHCP server policy settings including alerts and blocking for the network."
    )
    def get_network_switch_dhcp_server_policy(
        network_id: str
    ):
        """
        Get DHCP server policy for the network.
        
        Args:
            network_id: Network ID
        """
        try:
            result = meraki_client.dashboard.switch.getNetworkSwitchDhcpServerPolicy(network_id)
            
            response = f"# 📋 DHCP Server Policy\n\n"
            
            if result:
                response += f"**Default Policy**: {result.get('defaultPolicy', 'allow')}\n"
                response += f"**Alerts Enabled**: {result.get('alerts', {}).get('enabled', False)}\n"
                
                # ARP inspection
                arp = result.get('arpInspection', {})
                if arp:
                    response += f"\n## ARP Inspection\n"
                    response += f"- **Enabled**: {arp.get('enabled', False)}\n"
                    response += f"- **Unsupported Models**: {arp.get('unsupportedModels', [])}\n"
                
                # Allowed servers
                allowed = result.get('allowedServers', [])
                if allowed:
                    response += f"\n## Allowed DHCP Servers ({len(allowed)})\n"
                    for server in allowed:
                        response += f"- **{server.get('mac', 'N/A')}**: {server.get('ipv4', {}).get('address', 'N/A')}\n"
                
                # Blocked servers
                blocked = result.get('blockedServers', [])
                if blocked:
                    response += f"\n## Blocked DHCP Servers ({len(blocked)})\n"
                    for server in blocked:
                        response += f"- **{server.get('mac', 'N/A')}**: {server.get('ipv4', {}).get('address', 'N/A')}\n"
            else:
                response += "*Default policy applied*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting DHCP server policy: {str(e)}"
    
    @app.tool(
        name="get_network_switch_dscp_cos_mappings",
        description="🏷️ Get DSCP to CoS mappings for QoS on the network."
    )
    def get_network_switch_dscp_cos_mappings(
        network_id: str
    ):
        """
        Get DSCP to CoS mappings for the network.
        
        Args:
            network_id: Network ID
        """
        try:
            result = meraki_client.dashboard.switch.getNetworkSwitchDscpToCosMappings(network_id)
            
            response = f"# 🏷️ DSCP to CoS Mappings\n\n"
            
            if result:
                mappings = result.get('mappings', [])
                response += f"**Total Mappings**: {len(mappings)}\n\n"
                
                for mapping in mappings:
                    response += f"- **DSCP {mapping.get('dscp')}** → CoS {mapping.get('cos')}\n"
                    if mapping.get('title'):
                        response += f"  ({mapping.get('title')})\n"
            else:
                response += "*Using default mappings*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting DSCP mappings: {str(e)}"
    
    @app.tool(
        name="get_network_switch_mtu",
        description="📐 Get MTU configuration for the network switches."
    )
    def get_network_switch_mtu(
        network_id: str
    ):
        """
        Get MTU settings for network switches.
        
        Args:
            network_id: Network ID
        """
        try:
            result = meraki_client.dashboard.switch.getNetworkSwitchMtu(network_id)
            
            response = f"# 📐 Switch MTU Configuration\n\n"
            
            if result:
                response += f"**Default MTU**: {result.get('defaultMtuSize', 1500)} bytes\n"
                
                # Override settings
                overrides = result.get('overrides', [])
                if overrides:
                    response += f"\n## MTU Overrides ({len(overrides)})\n"
                    for override in overrides:
                        response += f"- **{override.get('switches', [])}**: {override.get('mtuSize')} bytes\n"
            else:
                response += "*Using default MTU (1500 bytes)*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting MTU config: {str(e)}"
    
    @app.tool(
        name="get_network_switch_port_schedules",
        description="⏰ List port schedules for automated port control."
    )
    def get_network_switch_port_schedules(
        network_id: str
    ):
        """
        List port schedules for the network.
        
        Args:
            network_id: Network ID
        """
        try:
            result = meraki_client.dashboard.switch.getNetworkSwitchPortSchedules(network_id)
            
            response = f"# ⏰ Switch Port Schedules\n\n"
            
            if result and isinstance(result, list):
                response += f"**Total Schedules**: {len(result)}\n\n"
                
                for schedule in result:
                    response += f"## {schedule.get('name', 'Unnamed')}\n"
                    response += f"- **ID**: {schedule.get('id')}\n"
                    
                    # Port schedule details
                    port_schedule = schedule.get('portSchedule', {})
                    if port_schedule:
                        response += f"- **Monday**: {port_schedule.get('monday', {})}\n"
                        response += f"- **Tuesday**: {port_schedule.get('tuesday', {})}\n"
                        response += f"- **Wednesday**: {port_schedule.get('wednesday', {})}\n"
                        response += f"- **Thursday**: {port_schedule.get('thursday', {})}\n"
                        response += f"- **Friday**: {port_schedule.get('friday', {})}\n"
                        response += f"- **Saturday**: {port_schedule.get('saturday', {})}\n"
                        response += f"- **Sunday**: {port_schedule.get('sunday', {})}\n"
                    
                    response += "\n"
            else:
                response += "*No port schedules configured*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting port schedules: {str(e)}"
    
    @app.tool(
        name="get_network_switch_qos_rules",
        description="⚡ Get QoS rules for the network including DSCP and CoS settings."
    )
    def get_network_switch_qos_rules(
        network_id: str
    ):
        """
        Get QoS rules for the network.
        
        Args:
            network_id: Network ID
        """
        try:
            result = meraki_client.dashboard.switch.getNetworkSwitchQosRules(network_id)
            
            response = f"# ⚡ Switch QoS Rules\n\n"
            
            if result and isinstance(result, list):
                response += f"**Total Rules**: {len(result)}\n\n"
                
                for idx, rule in enumerate(result, 1):
                    response += f"## Rule {idx}\n"
                    response += f"- **VLAN**: {rule.get('vlan', 'any')}\n"
                    response += f"- **Protocol**: {rule.get('protocol', 'any')}\n"
                    response += f"- **Source Port**: {rule.get('srcPort', 'any')}\n"
                    response += f"- **Source Port Range**: {rule.get('srcPortRange', 'N/A')}\n"
                    response += f"- **Destination Port**: {rule.get('dstPort', 'any')}\n"
                    response += f"- **Destination Port Range**: {rule.get('dstPortRange', 'N/A')}\n"
                    response += f"- **DSCP**: {rule.get('dscp', 'N/A')}\n"
                    response += "\n"
            else:
                response += "*No QoS rules configured*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting QoS rules: {str(e)}"
    
    @app.tool(
        name="get_network_switch_routing_multicast",
        description="📡 Get multicast routing settings for the network."
    )
    def get_network_switch_routing_multicast(
        network_id: str
    ):
        """
        Get multicast routing settings for the network.
        
        Args:
            network_id: Network ID
        """
        try:
            result = meraki_client.dashboard.switch.getNetworkSwitchRoutingMulticast(network_id)
            
            response = f"# 📡 Multicast Routing Settings\n\n"
            
            if result:
                response += f"**Default Settings**\n"
                response += f"- **IGMP Snooping**: {result.get('defaultSettings', {}).get('igmpSnoopingEnabled', False)}\n"
                response += f"- **Flood Unknown Multicast**: {result.get('defaultSettings', {}).get('floodUnknownMulticastTrafficEnabled', True)}\n"
                
                # Override settings
                overrides = result.get('overrides', [])
                if overrides:
                    response += f"\n## VLAN Overrides ({len(overrides)})\n"
                    for override in overrides:
                        response += f"- **VLAN {override.get('vlanId')}**:\n"
                        response += f"  - IGMP Snooping: {override.get('igmpSnoopingEnabled', False)}\n"
                        response += f"  - Flood Unknown: {override.get('floodUnknownMulticastTrafficEnabled', True)}\n"
            else:
                response += "*Using default multicast settings*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting multicast settings: {str(e)}"
    
    @app.tool(
        name="get_network_switch_routing_ospf",
        description="🦉 Get OSPF routing configuration for the network."
    )
    def get_network_switch_routing_ospf(
        network_id: str
    ):
        """
        Get OSPF configuration for the network.
        
        Args:
            network_id: Network ID
        """
        try:
            result = meraki_client.dashboard.switch.getNetworkSwitchRoutingOspf(network_id)
            
            response = f"# 🦉 OSPF Routing Configuration\n\n"
            
            if result:
                response += f"**Enabled**: {result.get('enabled', False)}\n"
                response += f"**Hello Timer**: {result.get('helloTimerInSeconds', 10)} seconds\n"
                response += f"**Dead Timer**: {result.get('deadTimerInSeconds', 40)} seconds\n"
                response += f"**MD5 Authentication**: {result.get('md5AuthenticationEnabled', False)}\n"
                
                # Areas
                areas = result.get('areas', [])
                if areas:
                    response += f"\n## OSPF Areas ({len(areas)})\n"
                    for area in areas:
                        response += f"- **Area {area.get('areaId')}**: {area.get('areaName', 'Unnamed')}\n"
                        response += f"  - Type: {area.get('areaType', 'normal')}\n"
                
                # V3 config
                v3 = result.get('v3', {})
                if v3.get('enabled'):
                    response += f"\n## OSPFv3 Configuration\n"
                    response += f"- **Enabled**: {v3.get('enabled', False)}\n"
                    response += f"- **Hello Timer**: {v3.get('helloTimerInSeconds', 10)} seconds\n"
                    response += f"- **Dead Timer**: {v3.get('deadTimerInSeconds', 40)} seconds\n"
            else:
                response += "*OSPF not configured*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting OSPF config: {str(e)}"
    
    @app.tool(
        name="get_network_switch_settings",
        description="⚙️ Get general network switch settings including VLAN, RSTP, and other configurations."
    )
    def get_network_switch_settings(
        network_id: str
    ):
        """
        Get general switch settings for the network.
        
        Args:
            network_id: Network ID
        """
        try:
            result = meraki_client.dashboard.switch.getNetworkSwitchSettings(network_id)
            
            response = f"# ⚙️ Network Switch Settings\n\n"
            
            if result:
                response += f"**VLAN Settings**\n"
                response += f"- **Use Combined Power**: {result.get('useCombinedPower', False)}\n"
                
                # Power exceptions
                power_exceptions = result.get('powerExceptions', [])
                if power_exceptions:
                    response += f"\n## Power Exceptions ({len(power_exceptions)})\n"
                    for exception in power_exceptions:
                        response += f"- **{exception.get('serial')}**: {exception.get('powerType')}\n"
                
                # MAC blocklist
                mac_blocklist = result.get('macBlocklist', {})
                if mac_blocklist.get('enabled'):
                    response += f"\n## MAC Blocklist\n"
                    response += f"- **Enabled**: True\n"
                    response += f"- **Blocked MACs**: {len(mac_blocklist.get('blacklist', []))}\n"
                
                # UplinkClientSampling
                uplink = result.get('uplinkClientSampling', {})
                if uplink:
                    response += f"\n## Uplink Client Sampling\n"
                    response += f"- **Enabled**: {uplink.get('enabled', False)}\n"
            else:
                response += "*Using default settings*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting switch settings: {str(e)}"
    
    @app.tool(
        name="get_network_switch_stacks",
        description="📚 List switch stacks in the network. Shows stack members and configuration."
    )
    def get_network_switch_stacks(
        network_id: str
    ):
        """
        List switch stacks in the network.
        
        Args:
            network_id: Network ID
        """
        try:
            result = meraki_client.dashboard.switch.getNetworkSwitchStacks(network_id)
            
            response = f"# 📚 Switch Stacks\n\n"
            
            if result and isinstance(result, list):
                response += f"**Total Stacks**: {len(result)}\n\n"
                
                for stack in result:
                    response += f"## Stack {stack.get('id', 'Unknown')}\n"
                    response += f"- **Name**: {stack.get('name', 'Unnamed')}\n"
                    
                    # Members
                    members = stack.get('serials', [])
                    if members:
                        response += f"- **Members** ({len(members)}):\n"
                        for serial in members:
                            response += f"  - {serial}\n"
                    
                    response += "\n"
            else:
                response += "*No switch stacks configured*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting switch stacks: {str(e)}"
    
    @app.tool(
        name="get_network_switch_stack_routing_interfaces",
        description="🛣️ List layer 3 interfaces for a switch stack."
    )
    def get_network_switch_stack_routing_interfaces(
        network_id: str,
        switch_stack_id: str
    ):
        """
        List layer 3 interfaces for a switch stack.
        
        Args:
            network_id: Network ID
            switch_stack_id: Switch stack ID
        """
        try:
            result = meraki_client.dashboard.switch.getNetworkSwitchStackRoutingInterfaces(
                network_id, switch_stack_id
            )
            
            response = f"# 🛣️ Stack Routing Interfaces\n\n"
            response += f"**Stack ID**: {switch_stack_id}\n\n"
            
            if result and isinstance(result, list):
                response += f"**Total Interfaces**: {len(result)}\n\n"
                
                for interface in result:
                    response += f"## Interface {interface.get('interfaceId', 'Unknown')}\n"
                    response += f"- **Name**: {interface.get('name', 'Unnamed')}\n"
                    response += f"- **VLAN**: {interface.get('vlanId', 'N/A')}\n"
                    response += f"- **Subnet**: {interface.get('subnet', 'N/A')}\n"
                    response += f"- **Interface IP**: {interface.get('interfaceIp', 'N/A')}\n"
                    response += f"- **Multicast Routing**: {interface.get('multicastRouting', 'disabled')}\n"
                    response += "\n"
            else:
                response += "*No layer 3 interfaces configured*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting stack routing interfaces: {str(e)}"
    
    @app.tool(
        name="get_network_switch_stack_routing_static_routes",
        description="🛤️ List static routes for a switch stack."
    )
    def get_network_switch_stack_routing_static_routes(
        network_id: str,
        switch_stack_id: str
    ):
        """
        List static routes for a switch stack.
        
        Args:
            network_id: Network ID
            switch_stack_id: Switch stack ID
        """
        try:
            result = meraki_client.dashboard.switch.getNetworkSwitchStackRoutingStaticRoutes(
                network_id, switch_stack_id
            )
            
            response = f"# 🛤️ Stack Static Routes\n\n"
            response += f"**Stack ID**: {switch_stack_id}\n\n"
            
            if result and isinstance(result, list):
                response += f"**Total Routes**: {len(result)}\n\n"
                
                for route in result:
                    response += f"## Route {route.get('staticRouteId', 'Unknown')}\n"
                    response += f"- **Name**: {route.get('name', 'Unnamed')}\n"
                    response += f"- **Subnet**: {route.get('subnet', 'N/A')}\n"
                    response += f"- **Next Hop IP**: {route.get('nextHopIp', 'N/A')}\n"
                    response += f"- **Advertise via OSPF**: {route.get('advertiseViaOspfEnabled', False)}\n"
                    response += "\n"
            else:
                response += "*No static routes configured*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting stack static routes: {str(e)}"
    
    @app.tool(
        name="get_network_switch_storm_control",
        description="⛈️ Get storm control settings to prevent broadcast storms."
    )
    def get_network_switch_storm_control(
        network_id: str
    ):
        """
        Get storm control settings for the network.
        
        Args:
            network_id: Network ID
        """
        try:
            result = meraki_client.dashboard.switch.getNetworkSwitchStormControl(network_id)
            
            response = f"# ⛈️ Storm Control Settings\n\n"
            
            if result:
                response += f"**Broadcast Threshold**: {result.get('broadcastThreshold', 100)}%\n"
                response += f"**Multicast Threshold**: {result.get('multicastThreshold', 100)}%\n"
                response += f"**Unknown Unicast Threshold**: {result.get('unknownUnicastThreshold', 100)}%\n"
            else:
                response += "*Storm control disabled*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting storm control settings: {str(e)}"
    
    @app.tool(
        name="get_network_switch_stp",
        description="🌳 Get Spanning Tree Protocol (STP) configuration for the network."
    )
    def get_network_switch_stp(
        network_id: str
    ):
        """
        Get STP settings for the network.
        
        Args:
            network_id: Network ID
        """
        try:
            result = meraki_client.dashboard.switch.getNetworkSwitchStp(network_id)
            
            response = f"# 🌳 Spanning Tree Protocol (STP) Settings\n\n"
            
            if result:
                response += f"**RSTP Enabled**: {result.get('rstpEnabled', True)}\n"
                
                # STP bridge priorities
                priorities = result.get('stpBridgePriority', [])
                if priorities:
                    response += f"\n## Bridge Priorities\n"
                    for priority in priorities:
                        response += f"- **VLAN {priority.get('vlanId', 'all')}**: Priority {priority.get('stpPriority', 32768)}\n"
            else:
                response += "*Using default STP settings*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting STP settings: {str(e)}"
    
    @app.tool(
        name="get_organization_switch_devices_clone",
        description="📋 Get switch devices available for cloning configuration."
    )
    def get_organization_switch_devices_clone(
        organization_id: str
    ):
        """
        Get switch devices available for config cloning.
        
        Args:
            organization_id: Organization ID
        """
        try:
            result = meraki_client.dashboard.switch.getOrganizationConfigTemplateSwitchProfilePorts(
                organization_id, "N/A"  # This endpoint might need adjustment
            )
            
            response = f"# 📋 Switch Devices for Cloning\n\n"
            
            if result and isinstance(result, list):
                response += f"**Available Devices**: {len(result)}\n\n"
                
                for device in result:
                    response += f"- **{device.get('serial')}**: {device.get('name', 'Unnamed')}\n"
                    response += f"  Model: {device.get('model', 'N/A')}\n"
            else:
                response += "*No devices available for cloning*\n"
            
            return response
        except Exception as e:
            # Try alternate endpoint
            return f"ℹ️ Clone configuration feature may require specific permissions or configuration templates.\n\nError: {str(e)}"
    
    @app.tool(
        name="get_organization_switch_ports_by_switch",
        description="📊 Get port information across all switches in the organization. Large dataset - use with filters."
    )
    def get_organization_switch_ports_by_switch(
        organization_id: str,
        per_page: Optional[int] = 100,
        network_ids: Optional[str] = None,
        serial: Optional[str] = None
    ):
        """
        Get ports across organization switches.
        
        Args:
            organization_id: Organization ID
            per_page: Results per page (max 1000)
            network_ids: Comma-separated network IDs to filter
            serial: Switch serial to filter
        """
        try:
            kwargs = {}
            if per_page:
                kwargs['perPage'] = min(per_page, 1000)
            if network_ids:
                kwargs['networkIds'] = [n.strip() for n in network_ids.split(',')]
            if serial:
                kwargs['serial'] = serial
            
            result = meraki_client.dashboard.switch.getOrganizationSwitchPortsBySwitch(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Organization Switch Ports\n\n"
            
            if result and isinstance(result, list):
                response += f"**Switches Found**: {len(result)}\n\n"
                
                for switch in result[:10]:  # Limit output
                    response += f"## {switch.get('serial', 'Unknown')}\n"
                    response += f"- **Name**: {switch.get('name', 'Unnamed')}\n"
                    response += f"- **Model**: {switch.get('model', 'N/A')}\n"
                    response += f"- **Network**: {switch.get('network', {}).get('name', 'N/A')}\n"
                    
                    ports = switch.get('ports', [])
                    if ports:
                        response += f"- **Ports**: {len(ports)} configured\n"
                        # Show first few ports
                        for port in ports[:3]:
                            response += f"  - Port {port.get('portId')}: {port.get('name', 'Unnamed')}\n"
                    
                    response += "\n"
                
                if len(result) > 10:
                    response += f"*Showing 10 of {len(result)} switches. Use filters to narrow results.*\n"
            else:
                response += "*No switches found*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting organization switch ports: {str(e)}"
    
    # ==================== DHCP ARP INSPECTION ====================
    
    @app.tool(
        name="get_network_switch_dhcp_arp_trusted_servers",
        description="🔐 Get trusted DHCP servers for ARP inspection."
    )
    def get_network_switch_dhcp_arp_trusted_servers(
        network_id: str
    ):
        """
        Get ARP inspection trusted servers.
        
        Args:
            network_id: Network ID
        """
        try:
            result = meraki_client.dashboard.switch.getNetworkSwitchDhcpServerPolicyArpInspectionTrustedServers(
                network_id
            )
            
            response = f"# 🔐 ARP Inspection Trusted Servers\n\n"
            
            if result and isinstance(result, list):
                response += f"**Total Trusted Servers**: {len(result)}\n\n"
                
                for server in result:
                    response += f"## {server.get('mac', 'Unknown MAC')}\n"
                    response += f"- **IPv4**: {server.get('ipv4', {}).get('address', 'N/A')}\n"
                    response += f"- **VLAN**: {server.get('vlan', 'N/A')}\n"
                    response += "\n"
            else:
                response += "*No trusted servers configured*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting ARP trusted servers: {str(e)}"
    
    # ==================== LINK AGGREGATION ====================
    
    @app.tool(
        name="get_network_switch_link_aggregations",
        description="🔗 List link aggregation groups (LAGs) for the network."
    )
    def get_network_switch_link_aggregations(
        network_id: str
    ):
        """
        List link aggregation groups.
        
        Args:
            network_id: Network ID
        """
        try:
            result = meraki_client.dashboard.switch.getNetworkSwitchLinkAggregations(network_id)
            
            response = f"# 🔗 Link Aggregation Groups (LAGs)\n\n"
            
            if result and isinstance(result, list):
                response += f"**Total LAGs**: {len(result)}\n\n"
                
                for lag in result:
                    response += f"## LAG {lag.get('id', 'Unknown')}\n"
                    
                    # Switch ports in LAG
                    switch_ports = lag.get('switchPorts', [])
                    if switch_ports:
                        response += f"**Member Ports** ({len(switch_ports)}):\n"
                        for port in switch_ports:
                            response += f"- **{port.get('serial')}** Port {port.get('portId')}\n"
                    
                    response += "\n"
            else:
                response += "*No link aggregations configured*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting link aggregations: {str(e)}"
    
    # ==================== RENDEZVOUS POINTS ====================
    
    @app.tool(
        name="get_network_switch_routing_multicast_rendezvous",
        description="📡 Get multicast rendezvous points for the network."
    )
    def get_network_switch_routing_multicast_rendezvous(
        network_id: str
    ):
        """
        Get multicast rendezvous points.
        
        Args:
            network_id: Network ID
        """
        try:
            result = meraki_client.dashboard.switch.getNetworkSwitchRoutingMulticastRendezvousPoints(network_id)
            
            response = f"# 📡 Multicast Rendezvous Points\n\n"
            
            if result and isinstance(result, list):
                response += f"**Total RPs**: {len(result)}\n\n"
                
                for rp in result:
                    response += f"## RP {rp.get('rendezvousPointId', 'Unknown')}\n"
                    response += f"- **Interface Name**: {rp.get('interfaceName', 'N/A')}\n"
                    response += f"- **Interface IP**: {rp.get('interfaceIp', 'N/A')}\n"
                    response += f"- **Multicast Group**: {rp.get('multicastGroup', 'N/A')}\n"
                    response += "\n"
            else:
                response += "*No rendezvous points configured*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting rendezvous points: {str(e)}"
    
    # ==================== INTERFACE DHCP ====================
    
    @app.tool(
        name="get_device_switch_routing_interface_dhcp",
        description="🖥️ Get DHCP configuration for a layer 3 interface."
    )
    def get_device_switch_routing_interface_dhcp(
        serial: str,
        interface_id: str
    ):
        """
        Get DHCP settings for a routing interface.
        
        Args:
            serial: Switch serial number
            interface_id: Interface ID
        """
        try:
            result = meraki_client.dashboard.switch.getDeviceSwitchRoutingInterfaceDhcp(
                serial, interface_id
            )
            
            response = f"# 🖥️ Interface DHCP Configuration\n\n"
            response += f"**Interface**: {interface_id}\n\n"
            
            if result:
                response += f"**DHCP Mode**: {result.get('dhcpMode', 'disabled')}\n"
                response += f"**DHCP Relay Server IPs**: {result.get('dhcpRelayServerIps', [])}\n"
                response += f"**DHCP Lease Time**: {result.get('dhcpLeaseTime', 'N/A')}\n"
                response += f"**DNS Nameservers**: {result.get('dnsNameserversOption', 'N/A')}\n"
                
                # DHCP options
                options = result.get('dhcpOptions', [])
                if options:
                    response += f"\n## DHCP Options ({len(options)})\n"
                    for opt in options:
                        response += f"- **Option {opt.get('code')}**: {opt.get('type')} = {opt.get('value')}\n"
                
                # Reserved IP ranges
                reserved = result.get('reservedIpRanges', [])
                if reserved:
                    response += f"\n## Reserved IP Ranges ({len(reserved)})\n"
                    for range in reserved:
                        response += f"- **{range.get('start')}** to **{range.get('end')}**\n"
                        response += f"  Comment: {range.get('comment', 'N/A')}\n"
                
                # Fixed IP assignments
                fixed = result.get('fixedIpAssignments', [])
                if fixed:
                    response += f"\n## Fixed IP Assignments ({len(fixed)})\n"
                    for assignment in fixed:
                        response += f"- **{assignment.get('mac')}**: {assignment.get('ip')}\n"
                        response += f"  Name: {assignment.get('name', 'N/A')}\n"
            else:
                response += "*DHCP not configured on this interface*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting interface DHCP: {str(e)}"
    
    # ==================== SWITCH PROFILES ====================
    
    @app.tool(
        name="get_org_config_template_switch_profiles",
        description="📋 List switch profiles for configuration templates."
    )
    def get_org_config_template_switch_profiles(
        organization_id: str,
        config_template_id: str
    ):
        """
        Get switch profiles for a config template.
        
        Args:
            organization_id: Organization ID
            config_template_id: Configuration template ID
        """
        try:
            result = meraki_client.dashboard.switch.getOrganizationConfigTemplateSwitchProfiles(
                organization_id, config_template_id
            )
            
            response = f"# 📋 Switch Profiles - Template {config_template_id}\n\n"
            
            if result and isinstance(result, list):
                response += f"**Total Profiles**: {len(result)}\n\n"
                
                for profile in result:
                    response += f"## Profile: {profile.get('name', 'Unnamed')}\n"
                    response += f"- **Model**: {profile.get('model', 'N/A')}\n"
                    response += f"- **Switch Profile ID**: {profile.get('switchProfileId', 'N/A')}\n"
                    response += "\n"
            else:
                response += "*No switch profiles found*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting switch profiles: {str(e)}"
    
    @app.tool(
        name="get_org_config_template_switch_profile_ports",
        description="📊 Get port configuration for a switch profile in a template."
    )
    def get_org_config_template_switch_profile_ports(
        organization_id: str,
        config_template_id: str,
        profile_id: str
    ):
        """
        Get ports for a switch profile.
        
        Args:
            organization_id: Organization ID
            config_template_id: Configuration template ID
            profile_id: Switch profile ID
        """
        try:
            result = meraki_client.dashboard.switch.getOrganizationConfigTemplateSwitchProfilePorts(
                organization_id, config_template_id, profile_id
            )
            
            response = f"# 📊 Switch Profile Ports\n\n"
            response += f"**Profile**: {profile_id}\n\n"
            
            if result and isinstance(result, list):
                response += f"**Total Ports**: {len(result)}\n\n"
                
                for port in result[:10]:  # Limit output
                    response += f"## Port {port.get('portId', 'Unknown')}\n"
                    response += f"- **Name**: {port.get('name', 'Unnamed')}\n"
                    response += f"- **Type**: {port.get('type', 'trunk')}\n"
                    response += f"- **VLAN**: {port.get('vlan', 'N/A')}\n"
                    response += f"- **Enabled**: {port.get('enabled', True)}\n"
                    response += "\n"
                
                if len(result) > 10:
                    response += f"*Showing 10 of {len(result)} ports*\n"
            else:
                response += "*No ports configured*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting profile ports: {str(e)}"
    
    @app.tool(
        name="get_org_config_template_switch_profile_port",
        description="🔍 Get a specific port from a switch profile."
    )
    def get_org_config_template_switch_profile_port(
        organization_id: str,
        config_template_id: str,
        profile_id: str,
        port_id: str
    ):
        """
        Get specific port details from a switch profile.
        
        Args:
            organization_id: Organization ID
            config_template_id: Configuration template ID
            profile_id: Switch profile ID
            port_id: Port ID
        """
        try:
            result = meraki_client.dashboard.switch.getOrganizationConfigTemplateSwitchProfilePort(
                organization_id, config_template_id, profile_id, port_id
            )
            
            response = f"# 🔍 Profile Port Details\n\n"
            response += f"**Port**: {port_id}\n\n"
            
            if result:
                response += f"## Configuration\n"
                response += f"- **Name**: {result.get('name', 'Unnamed')}\n"
                response += f"- **Enabled**: {result.get('enabled', False)}\n"
                response += f"- **Type**: {result.get('type', 'trunk')}\n"
                response += f"- **VLAN**: {result.get('vlan', 'N/A')}\n"
                response += f"- **Voice VLAN**: {result.get('voiceVlan', 'N/A')}\n"
                response += f"- **PoE Enabled**: {result.get('poeEnabled', False)}\n"
                response += f"- **STP Guard**: {result.get('stpGuard', 'disabled')}\n"
            else:
                response += "*Port not found*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting profile port: {str(e)}"
    
    # ==================== CONNECTIVITY MONITORING ====================
    
    @app.tool(
        name="get_org_switch_uplinks_status_overview",
        description="📡 Get uplink status overview for all switches in organization."
    )
    def get_org_switch_uplinks_status_overview(
        organization_id: str
    ):
        """
        Get overview of switch uplink statuses.
        
        Args:
            organization_id: Organization ID
        """
        try:
            result = meraki_client.dashboard.switch.getOrganizationSummaryTopSwitchesByEnergyUsage(
                organization_id
            )
            
            response = f"# 📡 Switch Uplinks Status Overview\n\n"
            
            if result and isinstance(result, list):
                response += f"**Total Switches**: {len(result)}\n\n"
                
                # Count by status
                online = sum(1 for s in result if s.get('status') == 'online')
                offline = sum(1 for s in result if s.get('status') == 'offline')
                alerting = sum(1 for s in result if s.get('status') == 'alerting')
                
                response += f"## Status Summary\n"
                response += f"- 🟢 **Online**: {online}\n"
                response += f"- 🔴 **Offline**: {offline}\n"
                response += f"- 🟡 **Alerting**: {alerting}\n\n"
                
                # Show problematic switches
                issues = [s for s in result if s.get('status') != 'online']
                if issues:
                    response += f"## Switches with Issues ({len(issues)})\n"
                    for switch in issues[:10]:
                        response += f"- **{switch.get('serial')}**: {switch.get('status')}\n"
                        response += f"  Network: {switch.get('network', {}).get('name', 'N/A')}\n"
            else:
                response += "*No uplink data available*\n"
            
            return response
        except Exception as e:
            # This endpoint might not exist, try alternate
            return f"ℹ️ Uplink status monitoring may require specific licensing.\n\nError: {str(e)}"
    
    # ==================== ENERGY USAGE ====================
    
    @app.tool(
        name="get_org_summary_top_switches_energy_usage",
        description="⚡ Get top switches by energy usage in the organization."
    )
    def get_org_summary_top_switches_energy_usage(
        organization_id: str,
        timespan: Optional[int] = None
    ):
        """
        Get top switches by energy consumption.
        
        Args:
            organization_id: Organization ID
            timespan: Timespan in seconds
        """
        try:
            kwargs = {}
            if timespan:
                kwargs['timespan'] = timespan
            
            result = meraki_client.dashboard.switch.getOrganizationSummaryTopSwitchesByEnergyUsage(
                organization_id, **kwargs
            )
            
            response = f"# ⚡ Top Switches by Energy Usage\n\n"
            
            if result and isinstance(result, list):
                response += f"**Analysis Period**: {timespan if timespan else 86400} seconds\n\n"
                
                for idx, switch in enumerate(result[:10], 1):
                    response += f"## {idx}. {switch.get('name', 'Unknown')}\n"
                    response += f"- **Serial**: {switch.get('serial')}\n"
                    response += f"- **Model**: {switch.get('model', 'N/A')}\n"
                    response += f"- **Network**: {switch.get('network', {}).get('name', 'N/A')}\n"
                    response += f"- **Energy Usage**: {switch.get('usage', 0):.2f} kWh\n"
                    response += f"- **Port Count**: {switch.get('portCount', 'N/A')}\n"
                    response += "\n"
            else:
                response += "*No energy usage data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting energy usage: {str(e)}"
    
    # ==================== INTERFACE STATUS ====================
    
    @app.tool(
        name="get_device_switch_routing_interface",
        description="🔍 Get details of a specific layer 3 interface."
    )
    def get_device_switch_routing_interface(
        serial: str,
        interface_id: str
    ):
        """
        Get specific routing interface details.
        
        Args:
            serial: Switch serial number
            interface_id: Interface ID
        """
        try:
            result = meraki_client.dashboard.switch.getDeviceSwitchRoutingInterface(
                serial, interface_id
            )
            
            response = f"# 🔍 Routing Interface Details\n\n"
            response += f"**Interface ID**: {interface_id}\n\n"
            
            if result:
                response += f"## Configuration\n"
                response += f"- **Name**: {result.get('name', 'Unnamed')}\n"
                response += f"- **VLAN**: {result.get('vlanId', 'N/A')}\n"
                response += f"- **Subnet**: {result.get('subnet', 'N/A')}\n"
                response += f"- **Interface IP**: {result.get('interfaceIp', 'N/A')}\n"
                response += f"- **Multicast Routing**: {result.get('multicastRouting', 'disabled')}\n"
                response += f"- **Default Gateway**: {result.get('defaultGateway', 'N/A')}\n"
                
                # OSPF settings
                ospf = result.get('ospfSettings', {})
                if ospf:
                    response += f"\n## OSPF Configuration\n"
                    response += f"- **Area**: {ospf.get('area', 'N/A')}\n"
                    response += f"- **Cost**: {ospf.get('cost', 'N/A')}\n"
                    response += f"- **Passive**: {ospf.get('isPassiveEnabled', False)}\n"
            else:
                response += "*Interface not found*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting interface details: {str(e)}"
    
    @app.tool(
        name="get_device_switch_routing_static_route",
        description="🛤️ Get details of a specific static route."
    )
    def get_device_switch_routing_static_route(
        serial: str,
        static_route_id: str
    ):
        """
        Get specific static route details.
        
        Args:
            serial: Switch serial number
            static_route_id: Static route ID
        """
        try:
            result = meraki_client.dashboard.switch.getDeviceSwitchRoutingStaticRoute(
                serial, static_route_id
            )
            
            response = f"# 🛤️ Static Route Details\n\n"
            response += f"**Route ID**: {static_route_id}\n\n"
            
            if result:
                response += f"## Configuration\n"
                response += f"- **Name**: {result.get('name', 'Unnamed')}\n"
                response += f"- **Subnet**: {result.get('subnet', 'N/A')}\n"
                response += f"- **Next Hop IP**: {result.get('nextHopIp', 'N/A')}\n"
                response += f"- **Advertise via OSPF**: {result.get('advertiseViaOspfEnabled', False)}\n"
                response += f"- **Prefer over OSPF**: {result.get('preferOverOspfRoutesEnabled', False)}\n"
            else:
                response += "*Route not found*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting route details: {str(e)}"
    
    @app.tool(
        name="get_network_switch_access_policy",
        description="🔐 Get details of a specific access policy."
    )
    def get_network_switch_access_policy(
        network_id: str,
        access_policy_number: str
    ):
        """
        Get specific access policy details.
        
        Args:
            network_id: Network ID
            access_policy_number: Access policy number
        """
        try:
            result = meraki_client.dashboard.switch.getNetworkSwitchAccessPolicy(
                network_id, access_policy_number
            )
            
            response = f"# 🔐 Access Policy Details\n\n"
            response += f"**Policy Number**: {access_policy_number}\n\n"
            
            if result:
                response += f"## Configuration\n"
                response += f"- **Name**: {result.get('name', 'Unnamed')}\n"
                response += f"- **Access Policy Type**: {result.get('accessPolicyType', 'N/A')}\n"
                response += f"- **Host Mode**: {result.get('hostMode', 'Single-Host')}\n"
                response += f"- **RADIUS Accounting**: {result.get('radiusAccountingEnabled', False)}\n"
                response += f"- **Guest VLAN**: {result.get('guestVlanId', 'N/A')}\n"
                
                # RADIUS servers
                radius = result.get('radiusServers', [])
                if radius:
                    response += f"\n## RADIUS Servers ({len(radius)})\n"
                    for server in radius:
                        response += f"- **{server.get('host')}**: Port {server.get('port', 1812)}\n"
                
                # Critical auth settings
                critical = result.get('criticalAuth', {})
                if critical:
                    response += f"\n## Critical Auth\n"
                    response += f"- **Data VLAN**: {critical.get('dataVlanId', 'N/A')}\n"
                    response += f"- **Voice VLAN**: {critical.get('voiceVlanId', 'N/A')}\n"
                    response += f"- **Suspend Port Bounce**: {critical.get('suspendPortBounce', False)}\n"
            else:
                response += "*Policy not found*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting access policy: {str(e)}"
    
    @app.tool(
        name="get_network_switch_stack",
        description="📚 Get details of a specific switch stack."
    )
    def get_network_switch_stack(
        network_id: str,
        switch_stack_id: str
    ):
        """
        Get specific switch stack details.
        
        Args:
            network_id: Network ID
            switch_stack_id: Switch stack ID
        """
        try:
            result = meraki_client.dashboard.switch.getNetworkSwitchStack(
                network_id, switch_stack_id
            )
            
            response = f"# 📚 Switch Stack Details\n\n"
            response += f"**Stack ID**: {switch_stack_id}\n\n"
            
            if result:
                response += f"## Configuration\n"
                response += f"- **Name**: {result.get('name', 'Unnamed')}\n"
                
                # Members
                members = result.get('serials', [])
                if members:
                    response += f"\n## Stack Members ({len(members)})\n"
                    for serial in members:
                        response += f"- {serial}\n"
            else:
                response += "*Stack not found*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting stack details: {str(e)}"
    
    @app.tool(
        name="get_network_switch_stack_routing_interface",
        description="🔍 Get details of a specific layer 3 interface on a switch stack."
    )
    def get_network_switch_stack_routing_interface(
        network_id: str,
        switch_stack_id: str,
        interface_id: str
    ):
        """
        Get specific stack routing interface.
        
        Args:
            network_id: Network ID
            switch_stack_id: Switch stack ID
            interface_id: Interface ID
        """
        try:
            result = meraki_client.dashboard.switch.getNetworkSwitchStackRoutingInterface(
                network_id, switch_stack_id, interface_id
            )
            
            response = f"# 🔍 Stack Interface Details\n\n"
            response += f"**Interface**: {interface_id}\n\n"
            
            if result:
                response += f"## Configuration\n"
                response += f"- **Name**: {result.get('name', 'Unnamed')}\n"
                response += f"- **VLAN**: {result.get('vlanId', 'N/A')}\n"
                response += f"- **Subnet**: {result.get('subnet', 'N/A')}\n"
                response += f"- **Interface IP**: {result.get('interfaceIp', 'N/A')}\n"
                response += f"- **Multicast Routing**: {result.get('multicastRouting', 'disabled')}\n"
            else:
                response += "*Interface not found*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting stack interface: {str(e)}"
    
    @app.tool(
        name="get_network_switch_stack_routing_static_route",
        description="🛤️ Get details of a specific static route on a switch stack."
    )
    def get_network_switch_stack_routing_static_route(
        network_id: str,
        switch_stack_id: str,
        static_route_id: str
    ):
        """
        Get specific stack static route.
        
        Args:
            network_id: Network ID
            switch_stack_id: Switch stack ID
            static_route_id: Static route ID
        """
        try:
            result = meraki_client.dashboard.switch.getNetworkSwitchStackRoutingStaticRoute(
                network_id, switch_stack_id, static_route_id
            )
            
            response = f"# 🛤️ Stack Route Details\n\n"
            response += f"**Route ID**: {static_route_id}\n\n"
            
            if result:
                response += f"## Configuration\n"
                response += f"- **Name**: {result.get('name', 'Unnamed')}\n"
                response += f"- **Subnet**: {result.get('subnet', 'N/A')}\n"
                response += f"- **Next Hop IP**: {result.get('nextHopIp', 'N/A')}\n"
                response += f"- **Advertise via OSPF**: {result.get('advertiseViaOspfEnabled', False)}\n"
            else:
                response += "*Route not found*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting stack route: {str(e)}"
    
    @app.tool(
        name="get_network_switch_port_schedule",
        description="⏰ Get details of a specific port schedule."
    )
    def get_network_switch_port_schedule(
        network_id: str,
        port_schedule_id: str
    ):
        """
        Get specific port schedule details.
        
        Args:
            network_id: Network ID
            port_schedule_id: Port schedule ID
        """
        try:
            result = meraki_client.dashboard.switch.getNetworkSwitchPortSchedule(
                network_id, port_schedule_id
            )
            
            response = f"# ⏰ Port Schedule Details\n\n"
            response += f"**Schedule ID**: {port_schedule_id}\n\n"
            
            if result:
                response += f"## Configuration\n"
                response += f"- **Name**: {result.get('name', 'Unnamed')}\n"
                
                # Schedule details
                schedule = result.get('portSchedule', {})
                if schedule:
                    response += f"\n## Weekly Schedule\n"
                    for day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
                        day_schedule = schedule.get(day, {})
                        if day_schedule:
                            response += f"- **{day.capitalize()}**: {day_schedule}\n"
            else:
                response += "*Schedule not found*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting port schedule: {str(e)}"
    
    @app.tool(
        name="get_network_switch_qos_rule",
        description="⚡ Get details of a specific QoS rule."
    )
    def get_network_switch_qos_rule(
        network_id: str,
        qos_rule_id: str
    ):
        """
        Get specific QoS rule details.
        
        Args:
            network_id: Network ID
            qos_rule_id: QoS rule ID
        """
        try:
            result = meraki_client.dashboard.switch.getNetworkSwitchQosRule(
                network_id, qos_rule_id
            )
            
            response = f"# ⚡ QoS Rule Details\n\n"
            response += f"**Rule ID**: {qos_rule_id}\n\n"
            
            if result:
                response += f"## Configuration\n"
                response += f"- **VLAN**: {result.get('vlan', 'any')}\n"
                response += f"- **Protocol**: {result.get('protocol', 'any')}\n"
                response += f"- **Source Port**: {result.get('srcPort', 'any')}\n"
                response += f"- **Destination Port**: {result.get('dstPort', 'any')}\n"
                response += f"- **DSCP**: {result.get('dscp', 'N/A')}\n"
            else:
                response += "*Rule not found*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting QoS rule: {str(e)}"
    
    # ========== MISSING SWITCH SDK METHODS ==========
    @app.tool(
        name="create_device_switch_routing_interface",
        description="🔧 Create a routing interface on a layer 3 switch"
    )
    def create_device_switch_routing_interface(
        serial: str,
        name: str,
        vlan_id: int,
        subnet: str,
        interface_ip: str,
        confirmed: bool = False
    ):
        """
        Create a routing interface on a layer 3 switch.
        
        ⚠️ WARNING: This modifies network routing configuration!
        
        Args:
            serial: Device serial number
            name: Interface name
            vlan_id: VLAN ID
            subnet: Subnet in CIDR notation (e.g., 192.168.1.0/24)
            interface_ip: Interface IP address
            confirmed: Must be True to execute this operation
            
        Returns:
            Created interface details
        """
        if not confirmed:
            return "⚠️ Creating routing interface requires confirmation. Set confirmed=true to proceed."
            
        try:
            result = meraki_client.dashboard.switch.createDeviceSwitchRoutingInterface(
                serial,
                name=name,
                vlanId=vlan_id,
                subnet=subnet,
                interfaceIp=interface_ip
            )
            
            return f"""✅ Routing Interface Created

**Name**: {name}
**VLAN**: {vlan_id}
**Subnet**: {subnet}
**Interface IP**: {interface_ip}"""
            
        except Exception as e:
            return f"Error creating routing interface: {str(e)}"
    
    @app.tool(
        name="update_device_switch_routing_interface",
        description="🔧 Update a routing interface on a layer 3 switch"
    )
    def update_device_switch_routing_interface(
        serial: str,
        interface_id: str,
        name: Optional[str] = None,
        vlan_id: Optional[int] = None,
        subnet: Optional[str] = None,
        interface_ip: Optional[str] = None
    ):
        """
        Update a routing interface on a layer 3 switch.
        
        Args:
            serial: Device serial number
            interface_id: Interface ID
            name: Interface name (optional)
            vlan_id: VLAN ID (optional)
            subnet: Subnet in CIDR notation (optional)
            interface_ip: Interface IP address (optional)
            
        Returns:
            Updated interface details
        """
        try:
            kwargs = {}
            if name:
                kwargs["name"] = name
            if vlan_id:
                kwargs["vlanId"] = vlan_id
            if subnet:
                kwargs["subnet"] = subnet
            if interface_ip:
                kwargs["interfaceIp"] = interface_ip
                
            result = meraki_client.dashboard.switch.updateDeviceSwitchRoutingInterface(
                serial,
                interface_id,
                **kwargs
            )
            
            return "✅ Routing interface updated successfully"
            
        except Exception as e:
            return f"Error updating routing interface: {str(e)}"
    
    @app.tool(
        name="delete_device_switch_routing_interface",
        description="🗑️ Delete a routing interface - REQUIRES CONFIRMATION"
    )
    def delete_device_switch_routing_interface(
        serial: str,
        interface_id: str,
        confirmed: bool = False
    ):
        """
        Delete a routing interface from a layer 3 switch.
        
        ⚠️ WARNING: This will remove the routing interface and disrupt connectivity!
        
        Args:
            serial: Device serial number
            interface_id: Interface ID to delete
            confirmed: Must be True to execute this operation
            
        Returns:
            Deletion status
        """
        if not confirmed:
            return "⚠️ Interface deletion requires confirmation. Set confirmed=true to proceed."
            
        try:
            meraki_client.dashboard.switch.deleteDeviceSwitchRoutingInterface(
                serial,
                interface_id
            )
            return f"✅ Routing interface {interface_id} deleted successfully"
            
        except Exception as e:
            return f"Error deleting routing interface: {str(e)}"

