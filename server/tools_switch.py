"""
Switch management tools for Cisco Meraki MCP server.

This module provides comprehensive switch management tools covering all SDK methods.
Includes port configuration, VLANs, routing, QoS, storm control, STP, and more.
"""

from typing import Optional, Dict, Any, List
import json
import time

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
            
            # Validate port IDs exist on the switch before cycling
            try:
                switch_ports = meraki_client.dashboard.switch.getDeviceSwitchPorts(serial)
                available_ports = [str(port.get('portId')) for port in switch_ports if port.get('portId')]
                
                invalid_ports = [p for p in port_list if p not in available_ports]
                if invalid_ports:
                    return f"❌ Invalid port IDs: {', '.join(invalid_ports)}\n\nAvailable ports on {serial}: {', '.join(available_ports)}"
                
            except Exception as e:
                # If we can't validate, proceed with warning
                pass
            
            result = meraki_client.dashboard.switch.cycleDeviceSwitchPorts(
                serial, ports=port_list
            )
            
            response = f"# ✅ Cycled Switch Ports\n\n"
            response += f"**Switch**: {serial}\n"
            response += f"**Cycled Ports**: {', '.join(port_list)}\n\n"
            response += "⚠️ Ports are rebooting. Connected devices will reconnect momentarily.\n"
            
            return response
        except Exception as e:
            error_msg = str(e)
            if "invalid port" in error_msg.lower() or "port list" in error_msg.lower():
                return f"❌ Invalid port list error: {error_msg}\n\n💡 Check that all port IDs exist on this switch using get_device_switch_ports first."
            return f"❌ Error cycling ports: {error_msg}"
    
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
        per_page: Optional[int] = 50,
        network_ids: Optional[str] = None,
        serial: Optional[str] = None
    ):
        """
        Get ports across organization switches.
        
        Args:
            organization_id: Organization ID
            per_page: Results per page (IMPORTANT: max 50, API enforces 3-50 range)
            network_ids: Comma-separated network IDs to filter
            serial: Switch serial to filter
        """
        try:
            kwargs = {}
            if per_page:
                # API enforces perPage between 3 and 50 for this endpoint
                kwargs['perPage'] = min(max(per_page, 3), 50)
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
    
    @app.tool(
        name="get_network_switch_routing_multicast_rendezvous_point",
        description="📡 Get details of a specific multicast rendezvous point."
    )
    def get_network_switch_routing_multicast_rendezvous_point(
        network_id: str,
        rendezvous_point_id: str
    ):
        """
        Get specific multicast rendezvous point details.
        
        Args:
            network_id: Network ID
            rendezvous_point_id: Rendezvous point ID
        """
        try:
            result = meraki_client.dashboard.switch.getNetworkSwitchRoutingMulticastRendezvousPoint(
                network_id, rendezvous_point_id
            )
            
            response = f"# 📡 Multicast Rendezvous Point Details\n\n"
            response += f"**RP ID**: {rendezvous_point_id}\n\n"
            
            if result:
                response += f"## Configuration\n"
                response += f"- **Interface Name**: {result.get('interfaceName', 'N/A')}\n"
                response += f"- **Interface IP**: {result.get('interfaceIp', 'N/A')}\n"
                response += f"- **Multicast Group**: {result.get('multicastGroup', 'N/A')}\n"
                response += f"- **Serial**: {result.get('serial', 'N/A')}\n"
            else:
                response += "*Rendezvous point not found*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting rendezvous point: {str(e)}"
    
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
    
    # ==================== PORT USAGE HISTORY ====================
    
    @app.tool(
        name="get_org_switch_ports_usage_history",
        description="📊 Get switch port usage history across the organization by device and interval."
    )
    def get_org_switch_ports_usage_history(
        organization_id: str,
        timespan: Optional[int] = 86400,
        per_page: Optional[int] = 25,
        network_ids: Optional[str] = None
    ):
        """
        Get switch port usage history by device and interval.
        
        Args:
            organization_id: Organization ID
            timespan: Timespan in seconds (default 24 hours)
            per_page: Results per page (3-1000)
            network_ids: Comma-separated network IDs to filter
        """
        try:
            kwargs = {}
            kwargs['timespan'] = timespan if timespan else 86400
            if per_page:
                kwargs['perPage'] = min(max(per_page, 3), 1000)
            if network_ids:
                kwargs['networkIds'] = [n.strip() for n in network_ids.split(',')]
            
            result = meraki_client.dashboard.switch.getOrganizationSwitchPortsUsageHistoryByDeviceByInterval(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Switch Port Usage History\n\n"
            
            if result and isinstance(result, list):
                response += f"**Analysis Period**: {timespan if timespan else 86400} seconds\n"
                response += f"**Devices Found**: {len(result)}\n\n"
                
                for idx, device in enumerate(result[:10], 1):
                    response += f"## {idx}. {device.get('name', 'Unknown')}\n"
                    response += f"- **Serial**: {device.get('serial')}\n"
                    response += f"- **Model**: {device.get('model', 'N/A')}\n"
                    response += f"- **Network**: {device.get('network', {}).get('name', 'N/A')}\n"
                    
                    # Show usage history if available
                    history = device.get('history', [])
                    if history:
                        response += f"- **Usage History**: {len(history)} data points\n"
                        # Show latest data point
                        latest = history[0] if history else {}
                        if latest:
                            response += f"  - Latest timestamp: {latest.get('ts', 'N/A')}\n"
                            ports = latest.get('ports', [])
                            if ports:
                                response += f"  - Active ports: {len([p for p in ports if p.get('recv', 0) > 0 or p.get('sent', 0) > 0])}\n"
                    
                    response += "\n"
                
                if len(result) > 10:
                    response += f"*Showing 10 of {len(result)} devices. Use network_ids filter to narrow results.*\n"
            else:
                response += "*No usage history data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting switch port usage history: {str(e)}"
    
    @app.tool(
        name="get_org_switch_ports_statuses_by_switch",
        description="📊 Get port statuses across all switches in organization. Shows connection status, errors, warnings."
    )
    def get_org_switch_ports_statuses_by_switch(
        organization_id: str,
        per_page: Optional[int] = 20,
        network_ids: Optional[str] = None
    ):
        """
        Get port statuses for all switches in organization.
        
        Args:
            organization_id: Organization ID
            per_page: Results per page (max 20)
            network_ids: Comma-separated network IDs to filter
        """
        try:
            kwargs = {}
            if per_page:
                kwargs['perPage'] = min(max(per_page, 3), 20)
            if network_ids:
                kwargs['networkIds'] = [n.strip() for n in network_ids.split(',')]
            
            result = meraki_client.dashboard.switch.getOrganizationSwitchPortsStatusesBySwitch(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Organization Switch Port Statuses\n\n"
            
            if result and isinstance(result, list):
                response += f"**Switches Found**: {len(result)}\n\n"
                
                for switch in result[:10]:
                    serial = switch.get('serial', 'Unknown')
                    response += f"## Switch: {serial}\n"
                    response += f"- **Name**: {switch.get('name', 'Unnamed')}\n"
                    response += f"- **Model**: {switch.get('model', 'N/A')}\n"
                    response += f"- **Network**: {switch.get('network', {}).get('name', 'N/A')}\n\n"
                    
                    ports = switch.get('ports', [])
                    if ports:
                        response += f"### Port Statuses ({len(ports)} ports)\n"
                        for port in ports[:5]:
                            port_id = port.get('portId', 'Unknown')
                            status = port.get('status', 'Unknown')
                            response += f"- **Port {port_id}**: {status}"
                            
                            if port.get('errors'):
                                response += f" ⚠️ Errors: {', '.join(port['errors'])}"
                            if port.get('warnings'):
                                response += f" ⚠️ Warnings: {', '.join(port['warnings'])}"
                            if port.get('speed'):
                                response += f" | {port['speed']}"
                            if port.get('duplex'):
                                response += f" | {port['duplex']}"
                            
                            response += "\n"
                        
                        if len(ports) > 5:
                            response += f"  *...and {len(ports) - 5} more ports*\n"
                    
                    response += "\n"
                
                if len(result) > 10:
                    response += f"*Showing 10 of {len(result)} switches. Use filters to narrow results.*\n"
            else:
                response += "*No switches found*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting switch port statuses: {str(e)}"
    
    @app.tool(
        name="get_org_switch_ports_overview",
        description="📈 Get organization-wide switch port usage overview and statistics."
    )
    def get_org_switch_ports_overview(
        organization_id: str
    ):
        """
        Get switch ports overview for organization.
        
        Args:
            organization_id: Organization ID
        """
        try:
            result = meraki_client.dashboard.switch.getOrganizationSwitchPortsOverview(
                organization_id
            )
            
            response = f"# 📈 Organization Switch Ports Overview\n\n"
            
            if result:
                # Port counts
                counts = result.get('counts', {})
                if counts:
                    response += "## Port Statistics\n"
                    response += f"- **Total Ports**: {counts.get('total', 0)}\n"
                    response += f"- **Connected**: {counts.get('connected', 0)}\n"
                    response += f"- **Disabled**: {counts.get('disabled', 0)}\n"
                    response += f"- **Errored**: {counts.get('errored', 0)}\n"
                    response += f"- **Warned**: {counts.get('warned', 0)}\n\n"
                
                # Power over Ethernet
                poe = result.get('powerOverEthernet', {})
                if poe:
                    response += "## Power over Ethernet\n"
                    response += f"- **Total Power**: {poe.get('total', 0)} W\n"
                    response += f"- **Used Power**: {poe.get('used', 0)} W\n"
                    response += f"- **Available Power**: {poe.get('available', 0)} W\n\n"
                
                # By status
                by_status = result.get('byStatus', {})
                if by_status:
                    response += "## Ports by Status\n"
                    for status, count in by_status.items():
                        response += f"- **{status}**: {count}\n"
                    response += "\n"
                
                # By speed
                by_speed = result.get('bySpeed', {})
                if by_speed:
                    response += "## Ports by Speed\n"
                    for speed, count in by_speed.items():
                        response += f"- **{speed}**: {count}\n"
            else:
                response += "*No overview data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting switch ports overview: {str(e)}"
    
    @app.tool(
        name="get_org_summary_switch_power_history",
        description="⚡ Get historical power consumption data for organization switches."
    )
    def get_org_summary_switch_power_history(
        organization_id: str,
        timespan: Optional[int] = 86400
    ):
        """
        Get switch power consumption history.
        
        Args:
            organization_id: Organization ID
            timespan: Time span in seconds (default 24 hours)
        """
        try:
            kwargs = {}
            if timespan:
                kwargs['timespan'] = timespan
            
            result = meraki_client.dashboard.switch.getOrganizationSummarySwitchPowerHistory(
                organization_id, **kwargs
            )
            
            response = f"# ⚡ Switch Power Consumption History\n\n"
            response += f"**Timespan**: {timespan} seconds\n\n"
            
            if result and isinstance(result, list):
                response += f"**Data Points**: {len(result)}\n\n"
                
                # Show latest readings
                if result:
                    latest = result[-1] if result else {}
                    response += "## Latest Reading\n"
                    response += f"- **Timestamp**: {latest.get('ts', 'N/A')}\n"
                    response += f"- **Total Power**: {latest.get('total', 0)} W\n"
                    response += f"- **PoE Power**: {latest.get('poe', 0)} W\n"
                    response += f"- **System Power**: {latest.get('system', 0)} W\n\n"
                    
                    # Calculate averages
                    if len(result) > 1:
                        total_avg = sum(p.get('total', 0) for p in result) / len(result)
                        poe_avg = sum(p.get('poe', 0) for p in result) / len(result)
                        
                        response += "## Averages\n"
                        response += f"- **Average Total**: {total_avg:.2f} W\n"
                        response += f"- **Average PoE**: {poe_avg:.2f} W\n\n"
                    
                    # Show peak usage
                    peak_total = max(result, key=lambda x: x.get('total', 0))
                    response += "## Peak Usage\n"
                    response += f"- **Peak Total**: {peak_total.get('total', 0)} W\n"
                    response += f"- **Peak Time**: {peak_total.get('ts', 'N/A')}\n"
            else:
                response += "*No power history data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting switch power history: {str(e)}"
    
    @app.tool(
        name="get_device_switch_ports_statuses_packets",
        description="📦 Get detailed packet statistics for all ports on a switch."
    )
    def get_device_switch_ports_statuses_packets(
        serial: str,
        timespan: Optional[int] = 3600
    ):
        """
        Get packet statistics for switch ports.
        
        Args:
            serial: Switch serial number
            timespan: Time span in seconds (default 1 hour)
        """
        try:
            kwargs = {}
            if timespan:
                kwargs['timespan'] = timespan
            
            result = meraki_client.dashboard.switch.getDeviceSwitchPortsStatusesPackets(
                serial, **kwargs
            )
            
            response = f"# 📦 Switch Port Packet Statistics\n\n"
            response += f"**Switch**: {serial}\n"
            response += f"**Timespan**: {timespan} seconds\n\n"
            
            if result and isinstance(result, list):
                response += f"**Ports with Data**: {len(result)}\n\n"
                
                total_rx = 0
                total_tx = 0
                
                for port in result:
                    port_id = port.get('portId', 'Unknown')
                    packets = port.get('packets', [])
                    
                    # Handle packets as list of packet type objects
                    rx_total = 0
                    tx_total = 0
                    rates = {}
                    packet_types = {}
                    
                    if isinstance(packets, list):
                        for packet_info in packets:
                            desc = packet_info.get('desc', '')
                            if desc == 'Total':
                                rx_total = packet_info.get('recv', 0)
                                tx_total = packet_info.get('sent', 0)
                                rates = packet_info.get('ratePerSec', {})
                            elif desc and packet_info.get('total', 0) > 0:
                                packet_types[desc] = {
                                    'total': packet_info.get('total', 0),
                                    'sent': packet_info.get('sent', 0),
                                    'recv': packet_info.get('recv', 0)
                                }
                    
                    total_rx += rx_total
                    total_tx += tx_total
                    
                    response += f"## Port {port_id}\n"
                    response += f"- **Received**: {rx_total:,} packets\n"
                    response += f"- **Sent**: {tx_total:,} packets\n"
                    
                    # Detailed packet types
                    if packet_types:
                        response += "- **By Type**:\n"
                        for pkt_type, counts in packet_types.items():
                            response += f"  - {pkt_type}: {counts['total']:,} "
                            response += f"(sent: {counts['sent']:,}, recv: {counts['recv']:,})\n"
                    
                    # Rate info if available
                    if rates:
                        response += f"- **Rate**: {rates.get('recv', 0)} rx/s, {rates.get('sent', 0)} tx/s\n"
                    
                    response += "\n"
                
                response += f"## Totals\n"
                response += f"- **Total Received**: {total_rx:,} packets\n"
                response += f"- **Total Sent**: {total_tx:,} packets\n"
            else:
                response += "*No packet data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting port packet statistics: {str(e)}"
    
    @app.tool(
        name="get_org_switch_ports_clients_overview",
        description="👥 Get client distribution overview across organization switches."
    )
    def get_org_switch_ports_clients_overview(
        organization_id: str,
        timespan: Optional[int] = 86400
    ):
        """
        Get client overview for organization switch ports.
        
        Args:
            organization_id: Organization ID
            timespan: Time span in seconds (default 24 hours)
        """
        try:
            kwargs = {}
            if timespan:
                kwargs['t0'] = str(int(time.time() - timespan))
                kwargs['t1'] = str(int(time.time()))
            
            result = meraki_client.dashboard.switch.getOrganizationSwitchPortsClientsOverviewByDevice(
                organization_id, **kwargs
            )
            
            response = f"# 👥 Switch Ports Client Overview\n\n"
            response += f"**Timespan**: {timespan} seconds\n\n"
            
            if result and isinstance(result, dict):
                counts = result.get('counts', {})
                items = result.get('items', [])
                
                if counts:
                    response += "## Summary\n"
                    response += f"- **Total Clients**: {counts.get('clients', 0)}\n"
                    response += f"- **Switches with Clients**: {counts.get('devices', 0)}\n\n"
                
                if items:
                    response += "## Client Distribution by Switch\n"
                    for item in items[:10]:
                        switch = item.get('device', {})
                        usage = item.get('usage', {})
                        clients = item.get('clients', {})
                        
                        response += f"### {switch.get('name', 'Unknown')} ({switch.get('serial', 'N/A')})\n"
                        response += f"- **Total Clients**: {clients.get('count', 0)}\n"
                        
                        if usage:
                            response += f"- **Traffic**: {usage.get('recv', 0)} bytes rx, {usage.get('sent', 0)} bytes tx\n"
                        
                        # Top clients
                        top_clients = clients.get('top', [])
                        if top_clients:
                            response += "- **Top Clients**:\n"
                            for client in top_clients[:3]:
                                response += f"  - {client.get('mac', 'Unknown')}: {client.get('name', 'Unnamed')}\n"
                        
                        response += "\n"
                    
                    if len(items) > 10:
                        response += f"*Showing 10 of {len(items)} switches*\n"
            else:
                response += "*No client data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting client overview: {str(e)}"
    
    @app.tool(
        name="get_org_switch_ports_topology_discovery",
        description="🗺️ Get network topology discovered via CDP/LLDP on organization switches."
    )
    def get_org_switch_ports_topology_discovery(
        organization_id: str,
        per_page: Optional[int] = 20
    ):
        """
        Get topology discovery data for organization switches.
        
        Args:
            organization_id: Organization ID
            per_page: Results per page (max 20)
        """
        try:
            kwargs = {}
            if per_page:
                kwargs['perPage'] = min(max(per_page, 3), 20)
            
            result = meraki_client.dashboard.switch.getOrganizationSwitchPortsTopologyDiscoveryByDevice(
                organization_id, **kwargs
            )
            
            response = f"# 🗺️ Switch Network Topology Discovery\n\n"
            
            if result and isinstance(result, list):
                response += f"**Devices with Topology Data**: {len(result)}\n\n"
                
                for device in result[:10]:
                    serial = device.get('serial', 'Unknown')
                    response += f"## Switch: {serial}\n"
                    response += f"- **Name**: {device.get('name', 'Unnamed')}\n"
                    response += f"- **Model**: {device.get('model', 'N/A')}\n\n"
                    
                    ports = device.get('ports', [])
                    if ports:
                        response += f"### Discovered Connections ({len(ports)} ports)\n"
                        for port in ports:
                            port_id = port.get('portId', 'Unknown')
                            cdp = port.get('cdp', {})
                            lldp = port.get('lldp', {})
                            
                            if cdp or lldp:
                                response += f"- **Port {port_id}**:\n"
                                
                                if cdp:
                                    response += f"  - CDP: {cdp.get('deviceId', 'Unknown')} "
                                    response += f"({cdp.get('platform', 'N/A')})\n"
                                    response += f"    Port: {cdp.get('portId', 'N/A')}\n"
                                
                                if lldp:
                                    response += f"  - LLDP: {lldp.get('systemName', 'Unknown')}\n"
                                    response += f"    Port: {lldp.get('portId', 'N/A')}\n"
                                    if lldp.get('systemDescription'):
                                        response += f"    Desc: {lldp['systemDescription']}\n"
                        
                        response += "\n"
                
                if len(result) > 10:
                    response += f"*Showing 10 of {len(result)} devices*\n"
            else:
                response += "*No topology data available (CDP/LLDP may be disabled)*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting topology discovery: {str(e)}"
    
    @app.tool(
        name="get_network_switch_dhcp_arp_warnings",
        description="⚠️ Get DHCP ARP inspection warnings for network switches."
    )
    def get_network_switch_dhcp_arp_warnings(
        network_id: str,
        per_page: Optional[int] = 50
    ):
        """
        Get DHCP ARP inspection warnings by device.
        
        Args:
            network_id: Network ID
            per_page: Results per page (max 1000)
        """
        try:
            kwargs = {}
            if per_page:
                kwargs['perPage'] = min(max(per_page, 3), 1000)
            
            result = meraki_client.dashboard.switch.getNetworkSwitchDhcpServerPolicyArpInspectionWarningsByDevice(
                network_id, **kwargs
            )
            
            response = f"# ⚠️ DHCP ARP Inspection Warnings\n\n"
            
            if result and isinstance(result, list):
                response += f"**Devices with Warnings**: {len(result)}\n\n"
                
                for device in result:
                    serial = device.get('serial', 'Unknown')
                    response += f"## Device: {serial}\n"
                    response += f"- **Name**: {device.get('name', 'Unnamed')}\n"
                    response += f"- **URL**: {device.get('url', 'N/A')}\n\n"
                    
                    warnings = device.get('arpInspectionWarnings', [])
                    if warnings:
                        response += f"### Warnings ({len(warnings)})\n"
                        for warning in warnings[:10]:
                            response += f"- **Timestamp**: {warning.get('timestamp', 'N/A')}\n"
                            response += f"  - **Type**: {warning.get('type', 'Unknown')}\n"
                            response += f"  - **Message**: {warning.get('message', 'N/A')}\n"
                            response += f"  - **Details**: {warning.get('details', {})}\n\n"
                        
                        if len(warnings) > 10:
                            response += f"*Showing 10 of {len(warnings)} warnings*\n"
                    else:
                        response += "*No warnings for this device*\n"
                    
                    response += "\n"
            else:
                response += "*No ARP inspection warnings found (this is good!)*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting ARP inspection warnings: {str(e)}"
    
    @app.tool(
        name="update_device_switch_warm_spare",
        description="🔄 Update warm spare configuration for a switch. Requires confirmation."
    )
    def update_device_switch_warm_spare(
        serial: str,
        enabled: bool,
        spare_serial: Optional[str] = None,
        confirmed: bool = False
    ):
        """
        Update switch warm spare configuration.
        
        Args:
            serial: Primary switch serial number
            enabled: Enable/disable warm spare
            spare_serial: Spare switch serial (required if enabling)
            confirmed: Must be true to execute
        """
        if not confirmed:
            return "⚠️ Warm spare update requires confirmed=true. This will modify switch redundancy configuration!"
        
        try:
            kwargs = {'enabled': enabled}
            if enabled and spare_serial:
                kwargs['spareSerial'] = spare_serial
            
            result = meraki_client.dashboard.switch.updateDeviceSwitchWarmSpare(
                serial, **kwargs
            )
            
            response = f"# ✅ Warm Spare Configuration Updated\n\n"
            response += f"**Primary Switch**: {serial}\n"
            
            if result:
                response += f"## New Configuration\n"
                response += f"- **Enabled**: {result.get('enabled', False)}\n"
                response += f"- **Primary Serial**: {result.get('primarySerial', 'N/A')}\n"
                response += f"- **Spare Serial**: {result.get('spareSerial', 'N/A')}\n"
                
                if enabled:
                    response += "\n⚠️ **Important**: Ensure spare switch is properly connected and configured.\n"
            
            return response
        except Exception as e:
            return f"❌ Error updating warm spare: {str(e)}"
    
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

    
    # ==================== ACCESS CONTROL & QOS MANAGEMENT ====================
    
    @app.tool(
        name="create_network_switch_access_policy",
        description="➕ Create a new switch access policy for 802.1X authentication. Requires confirmation."
    )
    def create_network_switch_access_policy(
        network_id: str,
        name: str,
        radius_servers: List[Dict[str, Any]],
        radius_testing_enabled: bool = False,
        radius_coa_support_enabled: bool = False,
        radius_accounting_enabled: bool = False,
        radius_accounting_servers: Optional[List[Dict[str, Any]]] = None,
        radius_group_attribute: Optional[str] = None,
        host_mode: str = "Single-Host",
        access_policy_type: str = "Hybrid authentication",
        increase_access_speed: bool = False,
        guest_vlan_id: Optional[int] = None,
        dot1x_control_direction: str = "both",
        voice_vlan_clients: bool = True,
        url_redirect_walled_garden_enabled: bool = False,
        url_redirect_walled_garden_ranges: Optional[List[str]] = None,
        confirmed: bool = False
    ):
        """
        Create a new switch access policy.
        
        Args:
            network_id: Network ID
            name: Policy name
            radius_servers: List of RADIUS server configs [{"host": "1.2.3.4", "port": 1812, "secret": "secret"}]
            radius_testing_enabled: Enable periodic RADIUS server connectivity tests
            radius_coa_support_enabled: Enable Change of Authorization (CoA) support
            radius_accounting_enabled: Enable RADIUS accounting
            radius_accounting_servers: RADIUS accounting servers (if different from auth)
            radius_group_attribute: RADIUS attribute for group authorization
            host_mode: "Single-Host" or "Multi-Domain" or "Multi-Host" or "Multi-Auth"
            access_policy_type: "Hybrid authentication" or "802.1x"
            increase_access_speed: Increase 802.1X access speed
            guest_vlan_id: Guest VLAN ID for failed authentication
            dot1x_control_direction: "both" or "inbound"
            voice_vlan_clients: Allow voice VLAN clients
            url_redirect_walled_garden_enabled: Enable walled garden for URL redirect
            url_redirect_walled_garden_ranges: IP ranges for walled garden
            confirmed: Must be true to execute
        """
        if not confirmed:
            return "⚠️ Creating access policy requires confirmed=true"
        
        try:
            kwargs = {
                "name": name,
                "radiusServers": radius_servers,
                "radiusTestingEnabled": radius_testing_enabled,
                "radiusCoaSupportEnabled": radius_coa_support_enabled,
                "radiusAccountingEnabled": radius_accounting_enabled,
                "hostMode": host_mode,
                "accessPolicyType": access_policy_type,
                "increaseAccessSpeed": increase_access_speed,
                "dot1xControlDirection": dot1x_control_direction,
                "voiceVlanClients": voice_vlan_clients,
                "urlRedirectWalledGardenEnabled": url_redirect_walled_garden_enabled
            }
            
            if radius_accounting_servers:
                kwargs["radiusAccountingServers"] = radius_accounting_servers
            if radius_group_attribute:
                kwargs["radiusGroupAttribute"] = radius_group_attribute
            if guest_vlan_id:
                kwargs["guestVlanId"] = guest_vlan_id
            if url_redirect_walled_garden_ranges:
                kwargs["urlRedirectWalledGardenRanges"] = url_redirect_walled_garden_ranges
            
            result = meraki_client.dashboard.switch.createNetworkSwitchAccessPolicy(
                network_id, **kwargs
            )
            
            return f"✅ Created access policy '{name}' with number {result.get('accessPolicyNumber')}"
        except Exception as e:
            return f"❌ Error creating access policy: {str(e)}"
    
    @app.tool(
        name="update_network_switch_access_policy",
        description="✏️ Update an existing switch access policy. Requires confirmation."
    )
    def update_network_switch_access_policy(
        network_id: str,
        access_policy_number: str,
        name: Optional[str] = None,
        radius_servers: Optional[List[Dict[str, Any]]] = None,
        radius_testing_enabled: Optional[bool] = None,
        radius_coa_support_enabled: Optional[bool] = None,
        radius_accounting_enabled: Optional[bool] = None,
        radius_accounting_servers: Optional[List[Dict[str, Any]]] = None,
        radius_group_attribute: Optional[str] = None,
        host_mode: Optional[str] = None,
        access_policy_type: Optional[str] = None,
        increase_access_speed: Optional[bool] = None,
        guest_vlan_id: Optional[int] = None,
        dot1x_control_direction: Optional[str] = None,
        voice_vlan_clients: Optional[bool] = None,
        url_redirect_walled_garden_enabled: Optional[bool] = None,
        url_redirect_walled_garden_ranges: Optional[List[str]] = None,
        confirmed: bool = False
    ):
        """
        Update an existing switch access policy.
        
        Args:
            network_id: Network ID
            access_policy_number: Access policy number to update
            name: Policy name
            radius_servers: List of RADIUS server configs
            radius_testing_enabled: Enable periodic RADIUS server connectivity tests
            radius_coa_support_enabled: Enable Change of Authorization support
            radius_accounting_enabled: Enable RADIUS accounting
            radius_accounting_servers: RADIUS accounting servers
            radius_group_attribute: RADIUS attribute for group authorization
            host_mode: "Single-Host", "Multi-Domain", "Multi-Host", or "Multi-Auth"
            access_policy_type: "Hybrid authentication" or "802.1x"
            increase_access_speed: Increase 802.1X access speed
            guest_vlan_id: Guest VLAN ID
            dot1x_control_direction: "both" or "inbound"
            voice_vlan_clients: Allow voice VLAN clients
            url_redirect_walled_garden_enabled: Enable walled garden
            url_redirect_walled_garden_ranges: IP ranges for walled garden
            confirmed: Must be true to execute
        """
        if not confirmed:
            return "⚠️ Updating access policy requires confirmed=true"
        
        try:
            kwargs = {}
            if name is not None:
                kwargs["name"] = name
            if radius_servers is not None:
                kwargs["radiusServers"] = radius_servers
            if radius_testing_enabled is not None:
                kwargs["radiusTestingEnabled"] = radius_testing_enabled
            if radius_coa_support_enabled is not None:
                kwargs["radiusCoaSupportEnabled"] = radius_coa_support_enabled
            if radius_accounting_enabled is not None:
                kwargs["radiusAccountingEnabled"] = radius_accounting_enabled
            if radius_accounting_servers is not None:
                kwargs["radiusAccountingServers"] = radius_accounting_servers
            if radius_group_attribute is not None:
                kwargs["radiusGroupAttribute"] = radius_group_attribute
            if host_mode is not None:
                kwargs["hostMode"] = host_mode
            if access_policy_type is not None:
                kwargs["accessPolicyType"] = access_policy_type
            if increase_access_speed is not None:
                kwargs["increaseAccessSpeed"] = increase_access_speed
            if guest_vlan_id is not None:
                kwargs["guestVlanId"] = guest_vlan_id
            if dot1x_control_direction is not None:
                kwargs["dot1xControlDirection"] = dot1x_control_direction
            if voice_vlan_clients is not None:
                kwargs["voiceVlanClients"] = voice_vlan_clients
            if url_redirect_walled_garden_enabled is not None:
                kwargs["urlRedirectWalledGardenEnabled"] = url_redirect_walled_garden_enabled
            if url_redirect_walled_garden_ranges is not None:
                kwargs["urlRedirectWalledGardenRanges"] = url_redirect_walled_garden_ranges
            
            result = meraki_client.dashboard.switch.updateNetworkSwitchAccessPolicy(
                network_id, access_policy_number, **kwargs
            )
            
            return f"✅ Updated access policy {access_policy_number}"
        except Exception as e:
            return f"❌ Error updating access policy: {str(e)}"
    
    @app.tool(
        name="delete_network_switch_access_policy",
        description="🗑️ Delete a switch access policy. Requires confirmation."
    )
    def delete_network_switch_access_policy(
        network_id: str,
        access_policy_number: str,
        confirmed: bool = False
    ):
        """
        Delete a switch access policy.
        
        Args:
            network_id: Network ID
            access_policy_number: Access policy number to delete
            confirmed: Must be true to execute
        """
        if not confirmed:
            return "⚠️ Deleting access policy requires confirmed=true. This cannot be undone!"
        
        try:
            meraki_client.dashboard.switch.deleteNetworkSwitchAccessPolicy(
                network_id, access_policy_number
            )
            return f"✅ Deleted access policy {access_policy_number}"
        except Exception as e:
            return f"❌ Error deleting access policy: {str(e)}"
    
    @app.tool(
        name="create_network_switch_qos_rule",
        description="➕ Create a new QoS rule for traffic prioritization. Requires confirmation."
    )
    def create_network_switch_qos_rule(
        network_id: str,
        vlan: int,
        protocol: Optional[str] = None,
        src_port: Optional[int] = None,
        src_port_range: Optional[str] = None,
        dst_port: Optional[int] = None,
        dst_port_range: Optional[str] = None,
        dscp: Optional[int] = None,
        confirmed: bool = False
    ):
        """
        Create a new switch QoS rule.
        
        Args:
            network_id: Network ID
            vlan: VLAN ID (1-4095)
            protocol: Protocol ("TCP", "UDP", "ANY")
            src_port: Source port
            src_port_range: Source port range (e.g., "1-65535")
            dst_port: Destination port
            dst_port_range: Destination port range
            dscp: DSCP value (0-63)
            confirmed: Must be true to execute
        """
        if not confirmed:
            return "⚠️ Creating QoS rule requires confirmed=true"
        
        try:
            kwargs = {"vlan": vlan}
            
            if protocol:
                kwargs["protocol"] = protocol
            if src_port:
                kwargs["srcPort"] = src_port
            if src_port_range:
                kwargs["srcPortRange"] = src_port_range
            if dst_port:
                kwargs["dstPort"] = dst_port
            if dst_port_range:
                kwargs["dstPortRange"] = dst_port_range
            if dscp is not None:
                kwargs["dscp"] = dscp
            
            result = meraki_client.dashboard.switch.createNetworkSwitchQosRule(
                network_id, **kwargs
            )
            
            return f"✅ Created QoS rule with ID {result.get('id')} for VLAN {vlan}"
        except Exception as e:
            return f"❌ Error creating QoS rule: {str(e)}"
    
    @app.tool(
        name="update_network_switch_qos_rule",
        description="✏️ Update an existing QoS rule. Requires confirmation."
    )
    def update_network_switch_qos_rule(
        network_id: str,
        qos_rule_id: str,
        vlan: Optional[int] = None,
        protocol: Optional[str] = None,
        src_port: Optional[int] = None,
        src_port_range: Optional[str] = None,
        dst_port: Optional[int] = None,
        dst_port_range: Optional[str] = None,
        dscp: Optional[int] = None,
        confirmed: bool = False
    ):
        """
        Update a switch QoS rule.
        
        Args:
            network_id: Network ID
            qos_rule_id: QoS rule ID to update
            vlan: VLAN ID (1-4095)
            protocol: Protocol ("TCP", "UDP", "ANY")
            src_port: Source port
            src_port_range: Source port range
            dst_port: Destination port
            dst_port_range: Destination port range
            dscp: DSCP value (0-63)
            confirmed: Must be true to execute
        """
        if not confirmed:
            return "⚠️ Updating QoS rule requires confirmed=true"
        
        try:
            kwargs = {}
            
            if vlan is not None:
                kwargs["vlan"] = vlan
            if protocol:
                kwargs["protocol"] = protocol
            if src_port:
                kwargs["srcPort"] = src_port
            if src_port_range:
                kwargs["srcPortRange"] = src_port_range
            if dst_port:
                kwargs["dstPort"] = dst_port
            if dst_port_range:
                kwargs["dstPortRange"] = dst_port_range
            if dscp is not None:
                kwargs["dscp"] = dscp
            
            result = meraki_client.dashboard.switch.updateNetworkSwitchQosRule(
                network_id, qos_rule_id, **kwargs
            )
            
            return f"✅ Updated QoS rule {qos_rule_id}"
        except Exception as e:
            return f"❌ Error updating QoS rule: {str(e)}"
    
    @app.tool(
        name="delete_network_switch_qos_rule",
        description="🗑️ Delete a QoS rule. Requires confirmation."
    )
    def delete_network_switch_qos_rule(
        network_id: str,
        qos_rule_id: str,
        confirmed: bool = False
    ):
        """
        Delete a switch QoS rule.
        
        Args:
            network_id: Network ID
            qos_rule_id: QoS rule ID to delete
            confirmed: Must be true to execute
        """
        if not confirmed:
            return "⚠️ Deleting QoS rule requires confirmed=true. This cannot be undone!"
        
        try:
            meraki_client.dashboard.switch.deleteNetworkSwitchQosRule(
                network_id, qos_rule_id
            )
            return f"✅ Deleted QoS rule {qos_rule_id}"
        except Exception as e:
            return f"❌ Error deleting QoS rule: {str(e)}"
    
    @app.tool(
        name="get_network_switch_qos_rules_order",
        description="📊 Get the order of QoS rules for a network."
    )
    def get_network_switch_qos_rules_order(
        network_id: str
    ):
        """
        Get the order of QoS rules.
        
        Args:
            network_id: Network ID
        """
        try:
            result = meraki_client.dashboard.switch.getNetworkSwitchQosRulesOrder(network_id)
            
            response = f"# 📊 QoS Rules Order\n\n"
            response += f"**Network**: {network_id}\n\n"
            
            if result and 'ruleIds' in result:
                rule_ids = result['ruleIds']
                response += f"**Total Rules**: {len(rule_ids)}\n\n"
                response += "## Rule Order (highest to lowest priority):\n"
                for i, rule_id in enumerate(rule_ids, 1):
                    response += f"{i}. Rule ID: {rule_id}\n"
            else:
                response += "*No QoS rules configured*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting QoS rules order: {str(e)}"
    
    @app.tool(
        name="update_network_switch_qos_rules_order",
        description="✏️ Update the order of QoS rules (priority). Requires confirmation."
    )
    def update_network_switch_qos_rules_order(
        network_id: str,
        rule_ids: List[str],
        confirmed: bool = False
    ):
        """
        Update the order of QoS rules.
        
        Args:
            network_id: Network ID
            rule_ids: Ordered list of rule IDs (first = highest priority)
            confirmed: Must be true to execute
        """
        if not confirmed:
            return "⚠️ Updating QoS rules order requires confirmed=true"
        
        try:
            result = meraki_client.dashboard.switch.updateNetworkSwitchQosRulesOrder(
                network_id, ruleIds=rule_ids
            )
            return f"✅ Updated QoS rules order. New order: {rule_ids}"
        except Exception as e:
            return f"❌ Error updating QoS rules order: {str(e)}"
    
    # ==================== PORT MANAGEMENT ====================
    
    @app.tool(
        name="update_device_switch_port",
        description="✏️ Update switch port configuration. Requires confirmation."
    )
    def update_device_switch_port(
        serial: str,
        port_id: str,
        name: Optional[str] = None,
        tags: Optional[List[str]] = None,
        enabled: Optional[bool] = None,
        port_schedule_id: Optional[str] = None,
        udld: Optional[str] = None,
        isolation_enabled: Optional[bool] = None,
        rstp_enabled: Optional[bool] = None,
        stp_guard: Optional[str] = None,
        link_negotiation: Optional[str] = None,
        access_policy_number: Optional[int] = None,
        type: Optional[str] = None,
        vlan: Optional[int] = None,
        voice_vlan: Optional[int] = None,
        allowed_vlans: Optional[str] = None,
        poe_enabled: Optional[bool] = None,
        confirmed: bool = False
    ):
        """
        Update a switch port configuration.
        
        Args:
            serial: Switch serial number
            port_id: Port ID
            name: Port name
            tags: Port tags
            enabled: Enable/disable port
            port_schedule_id: Port schedule ID
            udld: UDLD status ("Alert only", "Enforce")
            isolation_enabled: Port isolation
            rstp_enabled: RSTP enable
            stp_guard: "disabled", "root guard", "bpdu guard", "loop guard"
            link_negotiation: "Auto negotiate", "100 Megabit (auto)", "100 Megabit full duplex"
            access_policy_number: Access policy number
            type: "trunk" or "access"
            vlan: Access VLAN
            voice_vlan: Voice VLAN
            allowed_vlans: Allowed VLANs for trunk ports
            poe_enabled: Enable PoE
            confirmed: Must be true to execute
        """
        if not confirmed:
            return "⚠️ Updating port configuration requires confirmed=true"
        
        try:
            kwargs = {}
            
            if name is not None:
                kwargs["name"] = name
            if tags is not None:
                kwargs["tags"] = tags
            if enabled is not None:
                kwargs["enabled"] = enabled
            if port_schedule_id is not None:
                kwargs["portScheduleId"] = port_schedule_id
            if udld is not None:
                kwargs["udld"] = udld
            if isolation_enabled is not None:
                kwargs["isolationEnabled"] = isolation_enabled
            if rstp_enabled is not None:
                kwargs["rstpEnabled"] = rstp_enabled
            if stp_guard is not None:
                kwargs["stpGuard"] = stp_guard
            if link_negotiation is not None:
                kwargs["linkNegotiation"] = link_negotiation
            if access_policy_number is not None:
                kwargs["accessPolicyNumber"] = access_policy_number
            if type is not None:
                kwargs["type"] = type
            if vlan is not None:
                kwargs["vlan"] = vlan
            if voice_vlan is not None:
                kwargs["voiceVlan"] = voice_vlan
            if allowed_vlans is not None:
                kwargs["allowedVlans"] = allowed_vlans
            if poe_enabled is not None:
                kwargs["poeEnabled"] = poe_enabled
            
            result = meraki_client.dashboard.switch.updateDeviceSwitchPort(
                serial, port_id, **kwargs
            )
            
            return f"✅ Updated port {port_id} on switch {serial}"
        except Exception as e:
            return f"❌ Error updating port: {str(e)}"
    
    @app.tool(
        name="create_network_switch_port_schedule",
        description="➕ Create a port schedule for time-based port control. Requires confirmation."
    )
    def create_network_switch_port_schedule(
        network_id: str,
        name: str,
        port_schedule: Dict[str, Any],
        confirmed: bool = False
    ):
        """
        Create a switch port schedule.
        
        Args:
            network_id: Network ID
            name: Schedule name
            port_schedule: Schedule config {"monday": {"active": true, "from": "00:00", "to": "24:00"}, ...}
            confirmed: Must be true to execute
        """
        if not confirmed:
            return "⚠️ Creating port schedule requires confirmed=true"
        
        try:
            result = meraki_client.dashboard.switch.createNetworkSwitchPortSchedule(
                network_id, name=name, portSchedule=port_schedule
            )
            
            return f"✅ Created port schedule '{name}' with ID {result.get('id')}"
        except Exception as e:
            return f"❌ Error creating port schedule: {str(e)}"
    
    @app.tool(
        name="update_network_switch_port_schedule",
        description="✏️ Update a port schedule. Requires confirmation."
    )
    def update_network_switch_port_schedule(
        network_id: str,
        port_schedule_id: str,
        name: Optional[str] = None,
        port_schedule: Optional[Dict[str, Any]] = None,
        confirmed: bool = False
    ):
        """
        Update a switch port schedule.
        
        Args:
            network_id: Network ID
            port_schedule_id: Port schedule ID
            name: Schedule name
            port_schedule: Schedule config
            confirmed: Must be true to execute
        """
        if not confirmed:
            return "⚠️ Updating port schedule requires confirmed=true"
        
        try:
            kwargs = {}
            if name is not None:
                kwargs["name"] = name
            if port_schedule is not None:
                kwargs["portSchedule"] = port_schedule
            
            result = meraki_client.dashboard.switch.updateNetworkSwitchPortSchedule(
                network_id, port_schedule_id, **kwargs
            )
            
            return f"✅ Updated port schedule {port_schedule_id}"
        except Exception as e:
            return f"❌ Error updating port schedule: {str(e)}"
    
    @app.tool(
        name="delete_network_switch_port_schedule",
        description="🗑️ Delete a port schedule. Requires confirmation."
    )
    def delete_network_switch_port_schedule(
        network_id: str,
        port_schedule_id: str,
        confirmed: bool = False
    ):
        """
        Delete a switch port schedule.
        
        Args:
            network_id: Network ID
            port_schedule_id: Port schedule ID
            confirmed: Must be true to execute
        """
        if not confirmed:
            return "⚠️ Deleting port schedule requires confirmed=true. This cannot be undone!"
        
        try:
            meraki_client.dashboard.switch.deleteNetworkSwitchPortSchedule(
                network_id, port_schedule_id
            )
            return f"✅ Deleted port schedule {port_schedule_id}"
        except Exception as e:
            return f"❌ Error deleting port schedule: {str(e)}"
    
    # ==================== LINK AGGREGATION ====================
    
    @app.tool(
        name="create_network_switch_link_aggregation",
        description="➕ Create a link aggregation group (LAG). Requires confirmation."
    )
    def create_network_switch_link_aggregation(
        network_id: str,
        switch_ports: List[Dict[str, Any]],
        switch_profile_ports: Optional[List[Dict[str, Any]]] = None,
        confirmed: bool = False
    ):
        """
        Create a link aggregation group.
        
        Args:
            network_id: Network ID
            switch_ports: List of switch ports [{"serial": "XXXX", "portId": "1"}]
            switch_profile_ports: List of switch profile ports for templates
            confirmed: Must be true to execute
        """
        if not confirmed:
            return "⚠️ Creating link aggregation requires confirmed=true"
        
        try:
            kwargs = {"switchPorts": switch_ports}
            if switch_profile_ports:
                kwargs["switchProfilePorts"] = switch_profile_ports
            
            result = meraki_client.dashboard.switch.createNetworkSwitchLinkAggregation(
                network_id, **kwargs
            )
            
            return f"✅ Created link aggregation with ID {result.get('id')}"
        except Exception as e:
            return f"❌ Error creating link aggregation: {str(e)}"
    
    @app.tool(
        name="update_network_switch_link_aggregation",
        description="✏️ Update a link aggregation group. Requires confirmation."
    )
    def update_network_switch_link_aggregation(
        network_id: str,
        link_aggregation_id: str,
        switch_ports: Optional[List[Dict[str, Any]]] = None,
        switch_profile_ports: Optional[List[Dict[str, Any]]] = None,
        confirmed: bool = False
    ):
        """
        Update a link aggregation group.
        
        Args:
            network_id: Network ID
            link_aggregation_id: Link aggregation ID
            switch_ports: List of switch ports
            switch_profile_ports: List of switch profile ports
            confirmed: Must be true to execute
        """
        if not confirmed:
            return "⚠️ Updating link aggregation requires confirmed=true"
        
        try:
            kwargs = {}
            if switch_ports is not None:
                kwargs["switchPorts"] = switch_ports
            if switch_profile_ports is not None:
                kwargs["switchProfilePorts"] = switch_profile_ports
            
            result = meraki_client.dashboard.switch.updateNetworkSwitchLinkAggregation(
                network_id, link_aggregation_id, **kwargs
            )
            
            return f"✅ Updated link aggregation {link_aggregation_id}"
        except Exception as e:
            return f"❌ Error updating link aggregation: {str(e)}"
    
    @app.tool(
        name="delete_network_switch_link_aggregation",
        description="🗑️ Delete a link aggregation group. Requires confirmation."
    )
    def delete_network_switch_link_aggregation(
        network_id: str,
        link_aggregation_id: str,
        confirmed: bool = False
    ):
        """
        Delete a link aggregation group.
        
        Args:
            network_id: Network ID
            link_aggregation_id: Link aggregation ID
            confirmed: Must be true to execute
        """
        if not confirmed:
            return "⚠️ Deleting link aggregation requires confirmed=true. This cannot be undone!"
        
        try:
            meraki_client.dashboard.switch.deleteNetworkSwitchLinkAggregation(
                network_id, link_aggregation_id
            )
            return f"✅ Deleted link aggregation {link_aggregation_id}"
        except Exception as e:
            return f"❌ Error deleting link aggregation: {str(e)}"
    
    # ==================== LAYER 3 ROUTING ====================
    
    @app.tool(
        name="create_device_switch_routing_interface",
        description="➕ Create a Layer 3 interface on a switch. Requires confirmation."
    )
    def create_device_switch_routing_interface(
        serial: str,
        name: str,
        subnet: str,
        interface_ip: str,
        multicast_routing: str = "disabled",
        vlan_id: int = 1,
        default_gateway: Optional[str] = None,
        ospf_settings: Optional[Dict[str, Any]] = None,
        ospf_v3: Optional[Dict[str, Any]] = None,
        ipv6: Optional[Dict[str, Any]] = None,
        confirmed: bool = False
    ):
        """
        Create a Layer 3 interface.
        
        Args:
            serial: Switch serial number
            name: Interface name
            subnet: Subnet (e.g., "192.168.1.0/24")
            interface_ip: Interface IP address
            multicast_routing: "disabled", "enabled", "IGMP snooping querier"
            vlan_id: VLAN ID
            default_gateway: Default gateway IP
            ospf_settings: OSPF configuration
            ospf_v3: OSPFv3 configuration
            ipv6: IPv6 configuration
            confirmed: Must be true to execute
        """
        if not confirmed:
            return "⚠️ Creating routing interface requires confirmed=true"
        
        try:
            kwargs = {
                "name": name,
                "subnet": subnet,
                "interfaceIp": interface_ip,
                "multicastRouting": multicast_routing,
                "vlanId": vlan_id
            }
            
            if default_gateway:
                kwargs["defaultGateway"] = default_gateway
            if ospf_settings:
                kwargs["ospfSettings"] = ospf_settings
            if ospf_v3:
                kwargs["ospfV3"] = ospf_v3
            if ipv6:
                kwargs["ipv6"] = ipv6
            
            result = meraki_client.dashboard.switch.createDeviceSwitchRoutingInterface(
                serial, **kwargs
            )
            
            return f"✅ Created routing interface '{name}' with ID {result.get('interfaceId')}"
        except Exception as e:
            return f"❌ Error creating routing interface: {str(e)}"
    
    @app.tool(
        name="update_device_switch_routing_interface",
        description="✏️ Update a Layer 3 interface. Requires confirmation."
    )
    def update_device_switch_routing_interface(
        serial: str,
        interface_id: str,
        name: Optional[str] = None,
        subnet: Optional[str] = None,
        interface_ip: Optional[str] = None,
        multicast_routing: Optional[str] = None,
        vlan_id: Optional[int] = None,
        default_gateway: Optional[str] = None,
        ospf_settings: Optional[Dict[str, Any]] = None,
        ospf_v3: Optional[Dict[str, Any]] = None,
        ipv6: Optional[Dict[str, Any]] = None,
        confirmed: bool = False
    ):
        """
        Update a Layer 3 interface.
        
        Args:
            serial: Switch serial number
            interface_id: Interface ID
            name: Interface name
            subnet: Subnet
            interface_ip: Interface IP
            multicast_routing: Multicast routing mode
            vlan_id: VLAN ID
            default_gateway: Default gateway
            ospf_settings: OSPF configuration
            ospf_v3: OSPFv3 configuration
            ipv6: IPv6 configuration
            confirmed: Must be true to execute
        """
        if not confirmed:
            return "⚠️ Updating routing interface requires confirmed=true"
        
        try:
            kwargs = {}
            
            if name is not None:
                kwargs["name"] = name
            if subnet is not None:
                kwargs["subnet"] = subnet
            if interface_ip is not None:
                kwargs["interfaceIp"] = interface_ip
            if multicast_routing is not None:
                kwargs["multicastRouting"] = multicast_routing
            if vlan_id is not None:
                kwargs["vlanId"] = vlan_id
            if default_gateway is not None:
                kwargs["defaultGateway"] = default_gateway
            if ospf_settings is not None:
                kwargs["ospfSettings"] = ospf_settings
            if ospf_v3 is not None:
                kwargs["ospfV3"] = ospf_v3
            if ipv6 is not None:
                kwargs["ipv6"] = ipv6
            
            result = meraki_client.dashboard.switch.updateDeviceSwitchRoutingInterface(
                serial, interface_id, **kwargs
            )
            
            return f"✅ Updated routing interface {interface_id}"
        except Exception as e:
            return f"❌ Error updating routing interface: {str(e)}"
    
    @app.tool(
        name="update_device_switch_routing_interface_dhcp",
        description="✏️ Update DHCP settings for a Layer 3 interface. Requires confirmation."
    )
    def update_device_switch_routing_interface_dhcp(
        serial: str,
        interface_id: str,
        dhcp_mode: str,
        dhcp_relay_server_ips: Optional[List[str]] = None,
        dhcp_lease_time: Optional[str] = None,
        dns_nameservers_option: Optional[str] = None,
        dns_custom_nameservers: Optional[List[str]] = None,
        boot_options_enabled: Optional[bool] = None,
        boot_next_server: Optional[str] = None,
        boot_filename: Optional[str] = None,
        dhcp_options: Optional[List[Dict[str, Any]]] = None,
        reserved_ip_ranges: Optional[List[Dict[str, str]]] = None,
        fixed_ip_assignments: Optional[Dict[str, Dict[str, str]]] = None,
        confirmed: bool = False
    ):
        """
        Update DHCP settings for a Layer 3 interface.
        
        Args:
            serial: Switch serial number
            interface_id: Interface ID
            dhcp_mode: "dhcpDisabled", "dhcpRelay", or "dhcpServer"
            dhcp_relay_server_ips: DHCP relay server IPs
            dhcp_lease_time: Lease time ("30 minutes", "1 hour", "4 hours", "12 hours", "1 day", "1 week")
            dns_nameservers_option: "googlePublicDns", "openDns", "custom"
            dns_custom_nameservers: Custom DNS servers
            boot_options_enabled: Enable boot options
            boot_next_server: Boot server IP
            boot_filename: Boot filename
            dhcp_options: DHCP options
            reserved_ip_ranges: Reserved IP ranges
            fixed_ip_assignments: Fixed IP assignments
            confirmed: Must be true to execute
        """
        if not confirmed:
            return "⚠️ Updating DHCP settings requires confirmed=true"
        
        try:
            kwargs = {"dhcpMode": dhcp_mode}
            
            if dhcp_relay_server_ips is not None:
                kwargs["dhcpRelayServerIps"] = dhcp_relay_server_ips
            if dhcp_lease_time is not None:
                kwargs["dhcpLeaseTime"] = dhcp_lease_time
            if dns_nameservers_option is not None:
                kwargs["dnsNameserversOption"] = dns_nameservers_option
            if dns_custom_nameservers is not None:
                kwargs["dnsCustomNameservers"] = dns_custom_nameservers
            if boot_options_enabled is not None:
                kwargs["bootOptionsEnabled"] = boot_options_enabled
            if boot_next_server is not None:
                kwargs["bootNextServer"] = boot_next_server
            if boot_filename is not None:
                kwargs["bootFilename"] = boot_filename
            if dhcp_options is not None:
                kwargs["dhcpOptions"] = dhcp_options
            if reserved_ip_ranges is not None:
                kwargs["reservedIpRanges"] = reserved_ip_ranges
            if fixed_ip_assignments is not None:
                kwargs["fixedIpAssignments"] = fixed_ip_assignments
            
            result = meraki_client.dashboard.switch.updateDeviceSwitchRoutingInterfaceDhcp(
                serial, interface_id, **kwargs
            )
            
            return f"✅ Updated DHCP settings for interface {interface_id}"
        except Exception as e:
            return f"❌ Error updating DHCP settings: {str(e)}"
    
    @app.tool(
        name="create_device_switch_routing_static_route",
        description="➕ Create a static route on a Layer 3 switch. Requires confirmation."
    )
    def create_device_switch_routing_static_route(
        serial: str,
        subnet: str,
        next_hop_ip: str,
        name: Optional[str] = None,
        advertise_via_ospf_enabled: bool = False,
        prefer_over_ospf_routes_enabled: bool = False,
        confirmed: bool = False
    ):
        """
        Create a static route.
        
        Args:
            serial: Switch serial number
            subnet: Destination subnet (e.g., "192.168.2.0/24")
            next_hop_ip: Next hop IP address
            name: Route name
            advertise_via_ospf_enabled: Advertise via OSPF
            prefer_over_ospf_routes_enabled: Prefer over OSPF routes
            confirmed: Must be true to execute
        """
        if not confirmed:
            return "⚠️ Creating static route requires confirmed=true"
        
        try:
            kwargs = {
                "subnet": subnet,
                "nextHopIp": next_hop_ip,
                "advertiseViaOspfEnabled": advertise_via_ospf_enabled,
                "preferOverOspfRoutesEnabled": prefer_over_ospf_routes_enabled
            }
            
            if name:
                kwargs["name"] = name
            
            result = meraki_client.dashboard.switch.createDeviceSwitchRoutingStaticRoute(
                serial, **kwargs
            )
            
            return f"✅ Created static route to {subnet} via {next_hop_ip}"
        except Exception as e:
            return f"❌ Error creating static route: {str(e)}"
    
    @app.tool(
        name="update_device_switch_routing_static_route",
        description="✏️ Update a static route. Requires confirmation."
    )
    def update_device_switch_routing_static_route(
        serial: str,
        static_route_id: str,
        subnet: Optional[str] = None,
        next_hop_ip: Optional[str] = None,
        name: Optional[str] = None,
        advertise_via_ospf_enabled: Optional[bool] = None,
        prefer_over_ospf_routes_enabled: Optional[bool] = None,
        confirmed: bool = False
    ):
        """
        Update a static route.
        
        Args:
            serial: Switch serial number
            static_route_id: Static route ID
            subnet: Destination subnet
            next_hop_ip: Next hop IP
            name: Route name
            advertise_via_ospf_enabled: Advertise via OSPF
            prefer_over_ospf_routes_enabled: Prefer over OSPF routes
            confirmed: Must be true to execute
        """
        if not confirmed:
            return "⚠️ Updating static route requires confirmed=true"
        
        try:
            kwargs = {}
            
            if subnet is not None:
                kwargs["subnet"] = subnet
            if next_hop_ip is not None:
                kwargs["nextHopIp"] = next_hop_ip
            if name is not None:
                kwargs["name"] = name
            if advertise_via_ospf_enabled is not None:
                kwargs["advertiseViaOspfEnabled"] = advertise_via_ospf_enabled
            if prefer_over_ospf_routes_enabled is not None:
                kwargs["preferOverOspfRoutesEnabled"] = prefer_over_ospf_routes_enabled
            
            result = meraki_client.dashboard.switch.updateDeviceSwitchRoutingStaticRoute(
                serial, static_route_id, **kwargs
            )
            
            return f"✅ Updated static route {static_route_id}"
        except Exception as e:
            return f"❌ Error updating static route: {str(e)}"
    
    @app.tool(
        name="delete_device_switch_routing_static_route",
        description="🗑️ Delete a static route. Requires confirmation."
    )
    def delete_device_switch_routing_static_route(
        serial: str,
        static_route_id: str,
        confirmed: bool = False
    ):
        """
        Delete a static route.
        
        Args:
            serial: Switch serial number
            static_route_id: Static route ID
            confirmed: Must be true to execute
        """
        if not confirmed:
            return "⚠️ Deleting static route requires confirmed=true. This cannot be undone!"
        
        try:
            meraki_client.dashboard.switch.deleteDeviceSwitchRoutingStaticRoute(
                serial, static_route_id
            )
            return f"✅ Deleted static route {static_route_id}"
        except Exception as e:
            return f"❌ Error deleting static route: {str(e)}"
    
    @app.tool(
        name="create_network_switch_routing_multicast_rendezvous",
        description="➕ Create a multicast rendezvous point. Requires confirmation."
    )
    def create_network_switch_routing_multicast_rendezvous(
        network_id: str,
        interface_ip: str,
        multicast_group: str,
        confirmed: bool = False
    ):
        """
        Create a multicast rendezvous point.
        
        Args:
            network_id: Network ID
            interface_ip: Interface IP address
            multicast_group: Multicast group (e.g., "239.0.0.0/8")
            confirmed: Must be true to execute
        """
        if not confirmed:
            return "⚠️ Creating rendezvous point requires confirmed=true"
        
        try:
            result = meraki_client.dashboard.switch.createNetworkSwitchRoutingMulticastRendezvousPoint(
                network_id, interfaceIp=interface_ip, multicastGroup=multicast_group
            )
            
            return f"✅ Created rendezvous point at {interface_ip} for group {multicast_group}"
        except Exception as e:
            return f"❌ Error creating rendezvous point: {str(e)}"
    
    @app.tool(
        name="update_network_switch_routing_multicast",
        description="✏️ Update multicast routing settings. Requires confirmation."
    )
    def update_network_switch_routing_multicast(
        network_id: str,
        default_settings: Optional[Dict[str, Any]] = None,
        overrides: Optional[List[Dict[str, Any]]] = None,
        confirmed: bool = False
    ):
        """
        Update multicast routing settings.
        
        Args:
            network_id: Network ID
            default_settings: Default multicast settings
            overrides: Override settings for specific switches
            confirmed: Must be true to execute
        """
        if not confirmed:
            return "⚠️ Updating multicast routing requires confirmed=true"
        
        try:
            kwargs = {}
            
            if default_settings is not None:
                kwargs["defaultSettings"] = default_settings
            if overrides is not None:
                kwargs["overrides"] = overrides
            
            result = meraki_client.dashboard.switch.updateNetworkSwitchRoutingMulticast(
                network_id, **kwargs
            )
            
            return f"✅ Updated multicast routing settings"
        except Exception as e:
            return f"❌ Error updating multicast routing: {str(e)}"
    
    @app.tool(
        name="update_network_switch_routing_multicast_rendezvous",
        description="✏️ Update a multicast rendezvous point. Requires confirmation."
    )
    def update_network_switch_routing_multicast_rendezvous(
        network_id: str,
        rendezvous_point_id: str,
        interface_ip: Optional[str] = None,
        multicast_group: Optional[str] = None,
        confirmed: bool = False
    ):
        """
        Update a multicast rendezvous point.
        
        Args:
            network_id: Network ID
            rendezvous_point_id: Rendezvous point ID
            interface_ip: Interface IP address
            multicast_group: Multicast group
            confirmed: Must be true to execute
        """
        if not confirmed:
            return "⚠️ Updating rendezvous point requires confirmed=true"
        
        try:
            kwargs = {}
            
            if interface_ip is not None:
                kwargs["interfaceIp"] = interface_ip
            if multicast_group is not None:
                kwargs["multicastGroup"] = multicast_group
            
            result = meraki_client.dashboard.switch.updateNetworkSwitchRoutingMulticastRendezvousPoint(
                network_id, rendezvous_point_id, **kwargs
            )
            
            return f"✅ Updated rendezvous point {rendezvous_point_id}"
        except Exception as e:
            return f"❌ Error updating rendezvous point: {str(e)}"
    
    @app.tool(
        name="delete_network_switch_routing_multicast_rendezvous",
        description="🗑️ Delete a multicast rendezvous point. Requires confirmation."
    )
    def delete_network_switch_routing_multicast_rendezvous(
        network_id: str,
        rendezvous_point_id: str,
        confirmed: bool = False
    ):
        """
        Delete a multicast rendezvous point.
        
        Args:
            network_id: Network ID
            rendezvous_point_id: Rendezvous point ID
            confirmed: Must be true to execute
        """
        if not confirmed:
            return "⚠️ Deleting rendezvous point requires confirmed=true. This cannot be undone!"
        
        try:
            meraki_client.dashboard.switch.deleteNetworkSwitchRoutingMulticastRendezvousPoint(
                network_id, rendezvous_point_id
            )
            return f"✅ Deleted rendezvous point {rendezvous_point_id}"
        except Exception as e:
            return f"❌ Error deleting rendezvous point: {str(e)}"
    
    @app.tool(
        name="update_network_switch_routing_ospf",
        description="✏️ Update OSPF routing settings. Requires confirmation."
    )
    def update_network_switch_routing_ospf(
        network_id: str,
        enabled: Optional[bool] = None,
        hello_timer_in_seconds: Optional[int] = None,
        dead_timer_in_seconds: Optional[int] = None,
        areas: Optional[List[Dict[str, Any]]] = None,
        v3: Optional[Dict[str, Any]] = None,
        md5_authentication_enabled: Optional[bool] = None,
        md5_authentication_key: Optional[Dict[str, Any]] = None,
        confirmed: bool = False
    ):
        """
        Update OSPF routing settings.
        
        Args:
            network_id: Network ID
            enabled: Enable OSPF
            hello_timer_in_seconds: Hello timer (1-255)
            dead_timer_in_seconds: Dead timer (1-65535)
            areas: OSPF areas configuration
            v3: OSPFv3 configuration
            md5_authentication_enabled: Enable MD5 authentication
            md5_authentication_key: MD5 authentication key
            confirmed: Must be true to execute
        """
        if not confirmed:
            return "⚠️ Updating OSPF settings requires confirmed=true"
        
        try:
            kwargs = {}
            
            if enabled is not None:
                kwargs["enabled"] = enabled
            if hello_timer_in_seconds is not None:
                kwargs["helloTimerInSeconds"] = hello_timer_in_seconds
            if dead_timer_in_seconds is not None:
                kwargs["deadTimerInSeconds"] = dead_timer_in_seconds
            if areas is not None:
                kwargs["areas"] = areas
            if v3 is not None:
                kwargs["v3"] = v3
            if md5_authentication_enabled is not None:
                kwargs["md5AuthenticationEnabled"] = md5_authentication_enabled
            if md5_authentication_key is not None:
                kwargs["md5AuthenticationKey"] = md5_authentication_key
            
            result = meraki_client.dashboard.switch.updateNetworkSwitchRoutingOspf(
                network_id, **kwargs
            )
            
            return f"✅ Updated OSPF routing settings"
        except Exception as e:
            return f"❌ Error updating OSPF settings: {str(e)}"
    
    # ==================== SWITCH STACKS ====================
    
    @app.tool(
        name="create_network_switch_stack",
        description="➕ Create a switch stack. Requires confirmation."
    )
    def create_network_switch_stack(
        network_id: str,
        name: str,
        serials: List[str],
        confirmed: bool = False
    ):
        """
        Create a switch stack.
        
        Args:
            network_id: Network ID
            name: Stack name
            serials: List of switch serial numbers to stack
            confirmed: Must be true to execute
        """
        if not confirmed:
            return "⚠️ Creating switch stack requires confirmed=true"
        
        try:
            result = meraki_client.dashboard.switch.createNetworkSwitchStack(
                network_id, name=name, serials=serials
            )
            
            return f"✅ Created switch stack '{name}' with ID {result.get('id')}"
        except Exception as e:
            return f"❌ Error creating switch stack: {str(e)}"
    
    @app.tool(
        name="delete_network_switch_stack",
        description="🗑️ Delete a switch stack. Requires confirmation."
    )
    def delete_network_switch_stack(
        network_id: str,
        switch_stack_id: str,
        confirmed: bool = False
    ):
        """
        Delete a switch stack.
        
        Args:
            network_id: Network ID
            switch_stack_id: Switch stack ID
            confirmed: Must be true to execute
        """
        if not confirmed:
            return "⚠️ Deleting switch stack requires confirmed=true. This cannot be undone!"
        
        try:
            meraki_client.dashboard.switch.deleteNetworkSwitchStack(
                network_id, switch_stack_id
            )
            return f"✅ Deleted switch stack {switch_stack_id}"
        except Exception as e:
            return f"❌ Error deleting switch stack: {str(e)}"
    
    @app.tool(
        name="add_network_switch_stack",
        description="➕ Add a switch to an existing stack. Requires confirmation."
    )
    def add_network_switch_stack(
        network_id: str,
        switch_stack_id: str,
        serial: str,
        confirmed: bool = False
    ):
        """
        Add a switch to an existing stack.
        
        Args:
            network_id: Network ID
            switch_stack_id: Switch stack ID
            serial: Serial number of switch to add
            confirmed: Must be true to execute
        """
        if not confirmed:
            return "⚠️ Adding switch to stack requires confirmed=true"
        
        try:
            result = meraki_client.dashboard.switch.addNetworkSwitchStack(
                network_id, switch_stack_id, serial=serial
            )
            return f"✅ Added switch {serial} to stack {switch_stack_id}"
        except Exception as e:
            return f"❌ Error adding switch to stack: {str(e)}"
    
    @app.tool(
        name="remove_network_switch_stack",
        description="🗑️ Remove a switch from a stack. Requires confirmation."
    )
    def remove_network_switch_stack(
        network_id: str,
        switch_stack_id: str,
        serial: str,
        confirmed: bool = False
    ):
        """
        Remove a switch from a stack.
        
        Args:
            network_id: Network ID
            switch_stack_id: Switch stack ID
            serial: Serial number of switch to remove
            confirmed: Must be true to execute
        """
        if not confirmed:
            return "⚠️ Removing switch from stack requires confirmed=true"
        
        try:
            result = meraki_client.dashboard.switch.removeNetworkSwitchStack(
                network_id, switch_stack_id, serial=serial
            )
            return f"✅ Removed switch {serial} from stack {switch_stack_id}"
        except Exception as e:
            return f"❌ Error removing switch from stack: {str(e)}"
    
    @app.tool(
        name="create_network_switch_stack_routing_interface",
        description="➕ Create a Layer 3 interface on a switch stack. Requires confirmation."
    )
    def create_network_switch_stack_routing_interface(
        network_id: str,
        switch_stack_id: str,
        name: str,
        subnet: str,
        interface_ip: str,
        multicast_routing: str = "disabled",
        vlan_id: int = 1,
        default_gateway: Optional[str] = None,
        ospf_settings: Optional[Dict[str, Any]] = None,
        ospf_v3: Optional[Dict[str, Any]] = None,
        ipv6: Optional[Dict[str, Any]] = None,
        confirmed: bool = False
    ):
        """
        Create a Layer 3 interface on a switch stack.
        
        Args:
            network_id: Network ID
            switch_stack_id: Switch stack ID
            name: Interface name
            subnet: Subnet (e.g., "192.168.1.0/24")
            interface_ip: Interface IP address
            multicast_routing: "disabled", "enabled", "IGMP snooping querier"
            vlan_id: VLAN ID
            default_gateway: Default gateway IP
            ospf_settings: OSPF configuration
            ospf_v3: OSPFv3 configuration
            ipv6: IPv6 configuration
            confirmed: Must be true to execute
        """
        if not confirmed:
            return "⚠️ Creating stack routing interface requires confirmed=true"
        
        try:
            kwargs = {
                "name": name,
                "subnet": subnet,
                "interfaceIp": interface_ip,
                "multicastRouting": multicast_routing,
                "vlanId": vlan_id
            }
            
            if default_gateway:
                kwargs["defaultGateway"] = default_gateway
            if ospf_settings:
                kwargs["ospfSettings"] = ospf_settings
            if ospf_v3:
                kwargs["ospfV3"] = ospf_v3
            if ipv6:
                kwargs["ipv6"] = ipv6
            
            result = meraki_client.dashboard.switch.createNetworkSwitchStackRoutingInterface(
                network_id, switch_stack_id, **kwargs
            )
            
            return f"✅ Created stack routing interface '{name}' with ID {result.get('interfaceId')}"
        except Exception as e:
            return f"❌ Error creating stack routing interface: {str(e)}"
    
    @app.tool(
        name="update_network_switch_stack_routing_interface",
        description="✏️ Update a Layer 3 interface on a switch stack. Requires confirmation."
    )
    def update_network_switch_stack_routing_interface(
        network_id: str,
        switch_stack_id: str,
        interface_id: str,
        name: Optional[str] = None,
        subnet: Optional[str] = None,
        interface_ip: Optional[str] = None,
        multicast_routing: Optional[str] = None,
        vlan_id: Optional[int] = None,
        default_gateway: Optional[str] = None,
        ospf_settings: Optional[Dict[str, Any]] = None,
        ospf_v3: Optional[Dict[str, Any]] = None,
        ipv6: Optional[Dict[str, Any]] = None,
        confirmed: bool = False
    ):
        """
        Update a Layer 3 interface on a switch stack.
        
        Args:
            network_id: Network ID
            switch_stack_id: Switch stack ID
            interface_id: Interface ID
            name: Interface name
            subnet: Subnet
            interface_ip: Interface IP
            multicast_routing: Multicast routing mode
            vlan_id: VLAN ID
            default_gateway: Default gateway
            ospf_settings: OSPF configuration
            ospf_v3: OSPFv3 configuration
            ipv6: IPv6 configuration
            confirmed: Must be true to execute
        """
        if not confirmed:
            return "⚠️ Updating stack routing interface requires confirmed=true"
        
        try:
            kwargs = {}
            
            if name is not None:
                kwargs["name"] = name
            if subnet is not None:
                kwargs["subnet"] = subnet
            if interface_ip is not None:
                kwargs["interfaceIp"] = interface_ip
            if multicast_routing is not None:
                kwargs["multicastRouting"] = multicast_routing
            if vlan_id is not None:
                kwargs["vlanId"] = vlan_id
            if default_gateway is not None:
                kwargs["defaultGateway"] = default_gateway
            if ospf_settings is not None:
                kwargs["ospfSettings"] = ospf_settings
            if ospf_v3 is not None:
                kwargs["ospfV3"] = ospf_v3
            if ipv6 is not None:
                kwargs["ipv6"] = ipv6
            
            result = meraki_client.dashboard.switch.updateNetworkSwitchStackRoutingInterface(
                network_id, switch_stack_id, interface_id, **kwargs
            )
            
            return f"✅ Updated stack routing interface {interface_id}"
        except Exception as e:
            return f"❌ Error updating stack routing interface: {str(e)}"
    
    @app.tool(
        name="get_network_switch_stack_routing_interface_dhcp",
        description="🖥️ Get DHCP configuration for a stack layer 3 interface."
    )
    def get_network_switch_stack_routing_interface_dhcp(
        network_id: str,
        switch_stack_id: str,
        interface_id: str
    ):
        """
        Get DHCP configuration for a stack interface.
        
        Args:
            network_id: Network ID
            switch_stack_id: Switch stack ID
            interface_id: Interface ID
        """
        try:
            result = meraki_client.dashboard.switch.getNetworkSwitchStackRoutingInterfaceDhcp(
                network_id, switch_stack_id, interface_id
            )
            
            response = f"# 🖥️ Stack Interface DHCP Configuration\n\n"
            response += f"**Stack ID**: {switch_stack_id}\n"
            response += f"**Interface ID**: {interface_id}\n\n"
            
            if result:
                response += f"## DHCP Settings\n"
                response += f"- **DHCP Mode**: {result.get('dhcpMode', 'N/A')}\n"
                
                # DHCP relay settings
                if result.get('dhcpRelayServerIps'):
                    response += f"- **DHCP Relay Servers**: {', '.join(result['dhcpRelayServerIps'])}\n"
                
                # DHCP server settings
                if result.get('dhcpMode') == 'dhcpServer':
                    response += f"- **Lease Time**: {result.get('dhcpLeaseTime', 'N/A')}\n"
                    response += f"- **DNS Nameservers**: {result.get('dnsNameserversOption', 'N/A')}\n"
                    
                    if result.get('dnsCustomNameservers'):
                        response += f"- **Custom DNS**: {', '.join(result['dnsCustomNameservers'])}\n"
                    
                    # Boot options
                    if result.get('bootOptionsEnabled'):
                        response += f"\n## Boot Options\n"
                        response += f"- **Next Server**: {result.get('bootNextServer', 'N/A')}\n"
                        response += f"- **Boot Filename**: {result.get('bootFilename', 'N/A')}\n"
                    
                    # DHCP options
                    if result.get('dhcpOptions'):
                        response += f"\n## DHCP Options\n"
                        for option in result['dhcpOptions']:
                            response += f"- **Option {option.get('code')}**: {option.get('type', 'N/A')} = {option.get('value', 'N/A')}\n"
                    
                    # Reserved IP ranges
                    if result.get('reservedIpRanges'):
                        response += f"\n## Reserved IP Ranges\n"
                        for range_item in result['reservedIpRanges']:
                            response += f"- **{range_item.get('comment', 'Range')}**: {range_item.get('start')} - {range_item.get('end')}\n"
                    
                    # Fixed IP assignments
                    if result.get('fixedIpAssignments'):
                        response += f"\n## Fixed IP Assignments\n"
                        for mac, assignment in result['fixedIpAssignments'].items():
                            response += f"- **{mac}**: {assignment.get('ip')} ({assignment.get('name', 'Unnamed')})\n"
            else:
                response += "*No DHCP configuration found*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting stack interface DHCP configuration: {str(e)}"
    
    @app.tool(
        name="update_network_switch_stack_routing_interface_dhcp",
        description="✏️ Update DHCP settings for a stack interface. Requires confirmation."
    )
    def update_network_switch_stack_routing_interface_dhcp(
        network_id: str,
        switch_stack_id: str,
        interface_id: str,
        dhcp_mode: str,
        dhcp_relay_server_ips: Optional[List[str]] = None,
        dhcp_lease_time: Optional[str] = None,
        dns_nameservers_option: Optional[str] = None,
        dns_custom_nameservers: Optional[List[str]] = None,
        boot_options_enabled: Optional[bool] = None,
        boot_next_server: Optional[str] = None,
        boot_filename: Optional[str] = None,
        dhcp_options: Optional[List[Dict[str, Any]]] = None,
        reserved_ip_ranges: Optional[List[Dict[str, str]]] = None,
        fixed_ip_assignments: Optional[Dict[str, Dict[str, str]]] = None,
        confirmed: bool = False
    ):
        """
        Update DHCP settings for a stack interface.
        
        Args:
            network_id: Network ID
            switch_stack_id: Switch stack ID
            interface_id: Interface ID
            dhcp_mode: "dhcpDisabled", "dhcpRelay", or "dhcpServer"
            dhcp_relay_server_ips: DHCP relay server IPs
            dhcp_lease_time: Lease time
            dns_nameservers_option: DNS option
            dns_custom_nameservers: Custom DNS servers
            boot_options_enabled: Enable boot options
            boot_next_server: Boot server IP
            boot_filename: Boot filename
            dhcp_options: DHCP options
            reserved_ip_ranges: Reserved IP ranges
            fixed_ip_assignments: Fixed IP assignments
            confirmed: Must be true to execute
        """
        if not confirmed:
            return "⚠️ Updating stack DHCP settings requires confirmed=true"
        
        try:
            kwargs = {"dhcpMode": dhcp_mode}
            
            if dhcp_relay_server_ips is not None:
                kwargs["dhcpRelayServerIps"] = dhcp_relay_server_ips
            if dhcp_lease_time is not None:
                kwargs["dhcpLeaseTime"] = dhcp_lease_time
            if dns_nameservers_option is not None:
                kwargs["dnsNameserversOption"] = dns_nameservers_option
            if dns_custom_nameservers is not None:
                kwargs["dnsCustomNameservers"] = dns_custom_nameservers
            if boot_options_enabled is not None:
                kwargs["bootOptionsEnabled"] = boot_options_enabled
            if boot_next_server is not None:
                kwargs["bootNextServer"] = boot_next_server
            if boot_filename is not None:
                kwargs["bootFilename"] = boot_filename
            if dhcp_options is not None:
                kwargs["dhcpOptions"] = dhcp_options
            if reserved_ip_ranges is not None:
                kwargs["reservedIpRanges"] = reserved_ip_ranges
            if fixed_ip_assignments is not None:
                kwargs["fixedIpAssignments"] = fixed_ip_assignments
            
            result = meraki_client.dashboard.switch.updateNetworkSwitchStackRoutingInterfaceDhcp(
                network_id, switch_stack_id, interface_id, **kwargs
            )
            
            return f"✅ Updated DHCP settings for stack interface {interface_id}"
        except Exception as e:
            return f"❌ Error updating stack DHCP settings: {str(e)}"
    
    @app.tool(
        name="delete_network_switch_stack_routing_interface",
        description="🗑️ Delete a Layer 3 interface from a switch stack. Requires confirmation."
    )
    def delete_network_switch_stack_routing_interface(
        network_id: str,
        switch_stack_id: str,
        interface_id: str,
        confirmed: bool = False
    ):
        """
        Delete a Layer 3 interface from a switch stack.
        
        Args:
            network_id: Network ID
            switch_stack_id: Switch stack ID
            interface_id: Interface ID
            confirmed: Must be true to execute
        """
        if not confirmed:
            return "⚠️ Deleting stack routing interface requires confirmed=true. This cannot be undone!"
        
        try:
            meraki_client.dashboard.switch.deleteNetworkSwitchStackRoutingInterface(
                network_id, switch_stack_id, interface_id
            )
            return f"✅ Deleted stack routing interface {interface_id}"
        except Exception as e:
            return f"❌ Error deleting stack routing interface: {str(e)}"
    
    @app.tool(
        name="create_network_switch_stack_routing_static_route",
        description="➕ Create a static route on a switch stack. Requires confirmation."
    )
    def create_network_switch_stack_routing_static_route(
        network_id: str,
        switch_stack_id: str,
        subnet: str,
        next_hop_ip: str,
        name: Optional[str] = None,
        advertise_via_ospf_enabled: bool = False,
        prefer_over_ospf_routes_enabled: bool = False,
        confirmed: bool = False
    ):
        """
        Create a static route on a switch stack.
        
        Args:
            network_id: Network ID
            switch_stack_id: Switch stack ID
            subnet: Destination subnet (e.g., "192.168.2.0/24")
            next_hop_ip: Next hop IP address
            name: Route name
            advertise_via_ospf_enabled: Advertise via OSPF
            prefer_over_ospf_routes_enabled: Prefer over OSPF routes
            confirmed: Must be true to execute
        """
        if not confirmed:
            return "⚠️ Creating stack static route requires confirmed=true"
        
        try:
            kwargs = {
                "subnet": subnet,
                "nextHopIp": next_hop_ip,
                "advertiseViaOspfEnabled": advertise_via_ospf_enabled,
                "preferOverOspfRoutesEnabled": prefer_over_ospf_routes_enabled
            }
            
            if name:
                kwargs["name"] = name
            
            result = meraki_client.dashboard.switch.createNetworkSwitchStackRoutingStaticRoute(
                network_id, switch_stack_id, **kwargs
            )
            
            return f"✅ Created stack static route to {subnet} via {next_hop_ip}"
        except Exception as e:
            return f"❌ Error creating stack static route: {str(e)}"
    
    @app.tool(
        name="update_network_switch_stack_routing_static_route",
        description="✏️ Update a static route on a switch stack. Requires confirmation."
    )
    def update_network_switch_stack_routing_static_route(
        network_id: str,
        switch_stack_id: str,
        static_route_id: str,
        subnet: Optional[str] = None,
        next_hop_ip: Optional[str] = None,
        name: Optional[str] = None,
        advertise_via_ospf_enabled: Optional[bool] = None,
        prefer_over_ospf_routes_enabled: Optional[bool] = None,
        confirmed: bool = False
    ):
        """
        Update a static route on a switch stack.
        
        Args:
            network_id: Network ID
            switch_stack_id: Switch stack ID
            static_route_id: Static route ID
            subnet: Destination subnet
            next_hop_ip: Next hop IP
            name: Route name
            advertise_via_ospf_enabled: Advertise via OSPF
            prefer_over_ospf_routes_enabled: Prefer over OSPF routes
            confirmed: Must be true to execute
        """
        if not confirmed:
            return "⚠️ Updating stack static route requires confirmed=true"
        
        try:
            kwargs = {}
            
            if subnet is not None:
                kwargs["subnet"] = subnet
            if next_hop_ip is not None:
                kwargs["nextHopIp"] = next_hop_ip
            if name is not None:
                kwargs["name"] = name
            if advertise_via_ospf_enabled is not None:
                kwargs["advertiseViaOspfEnabled"] = advertise_via_ospf_enabled
            if prefer_over_ospf_routes_enabled is not None:
                kwargs["preferOverOspfRoutesEnabled"] = prefer_over_ospf_routes_enabled
            
            result = meraki_client.dashboard.switch.updateNetworkSwitchStackRoutingStaticRoute(
                network_id, switch_stack_id, static_route_id, **kwargs
            )
            
            return f"✅ Updated stack static route {static_route_id}"
        except Exception as e:
            return f"❌ Error updating stack static route: {str(e)}"
    
    @app.tool(
        name="delete_network_switch_stack_routing_static_route",
        description="🗑️ Delete a static route from a switch stack. Requires confirmation."
    )
    def delete_network_switch_stack_routing_static_route(
        network_id: str,
        switch_stack_id: str,
        static_route_id: str,
        confirmed: bool = False
    ):
        """
        Delete a static route from a switch stack.
        
        Args:
            network_id: Network ID
            switch_stack_id: Switch stack ID
            static_route_id: Static route ID
            confirmed: Must be true to execute
        """
        if not confirmed:
            return "⚠️ Deleting stack static route requires confirmed=true. This cannot be undone!"
        
        try:
            meraki_client.dashboard.switch.deleteNetworkSwitchStackRoutingStaticRoute(
                network_id, switch_stack_id, static_route_id
            )
            return f"✅ Deleted stack static route {static_route_id}"
        except Exception as e:
            return f"❌ Error deleting stack static route: {str(e)}"
    
    # ==================== NETWORK SETTINGS ====================
    
    @app.tool(
        name="update_network_switch_settings",
        description="✏️ Update general switch network settings. Requires confirmation."
    )
    def update_network_switch_settings(
        network_id: str,
        vlan: Optional[int] = None,
        use_combined_power: Optional[bool] = None,
        power_exceptions: Optional[List[Dict[str, Any]]] = None,
        uplink_client_sampling: Optional[Dict[str, Any]] = None,
        mac_blocklist: Optional[Dict[str, Any]] = None,
        confirmed: bool = False
    ):
        """
        Update general switch network settings.
        
        Args:
            network_id: Network ID
            vlan: Management VLAN
            use_combined_power: Use combined power for PoE
            power_exceptions: Power exceptions for specific switches
            uplink_client_sampling: Uplink client sampling configuration
            mac_blocklist: MAC blocklist configuration
            confirmed: Must be true to execute
        """
        if not confirmed:
            return "⚠️ Updating switch settings requires confirmed=true"
        
        try:
            kwargs = {}
            
            if vlan is not None:
                kwargs["vlan"] = vlan
            if use_combined_power is not None:
                kwargs["useCombinedPower"] = use_combined_power
            if power_exceptions is not None:
                kwargs["powerExceptions"] = power_exceptions
            if uplink_client_sampling is not None:
                kwargs["uplinkClientSampling"] = uplink_client_sampling
            if mac_blocklist is not None:
                kwargs["macBlocklist"] = mac_blocklist
            
            result = meraki_client.dashboard.switch.updateNetworkSwitchSettings(
                network_id, **kwargs
            )
            
            return f"✅ Updated switch network settings"
        except Exception as e:
            return f"❌ Error updating switch settings: {str(e)}"
    
    @app.tool(
        name="update_network_switch_access_control_lists",
        description="✏️ Update switch ACLs. Requires confirmation."
    )
    def update_network_switch_access_control_lists(
        network_id: str,
        rules: List[Dict[str, Any]],
        confirmed: bool = False
    ):
        """
        Update switch access control lists.
        
        Args:
            network_id: Network ID
            rules: List of ACL rules
            confirmed: Must be true to execute
        """
        if not confirmed:
            return "⚠️ Updating ACLs requires confirmed=true"
        
        try:
            result = meraki_client.dashboard.switch.updateNetworkSwitchAccessControlLists(
                network_id, rules=rules
            )
            
            return f"✅ Updated switch ACLs with {len(rules)} rules"
        except Exception as e:
            return f"❌ Error updating ACLs: {str(e)}"
    
    @app.tool(
        name="update_network_switch_stp",
        description="✏️ Update Spanning Tree Protocol settings. Requires confirmation."
    )
    def update_network_switch_stp(
        network_id: str,
        rstp_enabled: Optional[bool] = None,
        stp_bridge_priority: Optional[List[Dict[str, Any]]] = None,
        confirmed: bool = False
    ):
        """
        Update STP settings.
        
        Args:
            network_id: Network ID
            rstp_enabled: Enable Rapid STP
            stp_bridge_priority: Bridge priority settings per VLAN
            confirmed: Must be true to execute
        """
        if not confirmed:
            return "⚠️ Updating STP settings requires confirmed=true"
        
        try:
            kwargs = {}
            
            if rstp_enabled is not None:
                kwargs["rstpEnabled"] = rstp_enabled
            if stp_bridge_priority is not None:
                kwargs["stpBridgePriority"] = stp_bridge_priority
            
            result = meraki_client.dashboard.switch.updateNetworkSwitchStp(
                network_id, **kwargs
            )
            
            return f"✅ Updated STP settings"
        except Exception as e:
            return f"❌ Error updating STP: {str(e)}"
    
    @app.tool(
        name="update_network_switch_storm_control",
        description="✏️ Update storm control settings. Requires confirmation."
    )
    def update_network_switch_storm_control(
        network_id: str,
        broadcast_threshold: Optional[int] = None,
        multicast_threshold: Optional[int] = None,
        unknown_unicast_threshold: Optional[int] = None,
        confirmed: bool = False
    ):
        """
        Update storm control settings.
        
        Args:
            network_id: Network ID
            broadcast_threshold: Broadcast threshold percentage (1-100)
            multicast_threshold: Multicast threshold percentage (1-100)
            unknown_unicast_threshold: Unknown unicast threshold percentage (1-100)
            confirmed: Must be true to execute
        """
        if not confirmed:
            return "⚠️ Updating storm control requires confirmed=true"
        
        try:
            kwargs = {}
            
            if broadcast_threshold is not None:
                kwargs["broadcastThreshold"] = broadcast_threshold
            if multicast_threshold is not None:
                kwargs["multicastThreshold"] = multicast_threshold
            if unknown_unicast_threshold is not None:
                kwargs["unknownUnicastThreshold"] = unknown_unicast_threshold
            
            result = meraki_client.dashboard.switch.updateNetworkSwitchStormControl(
                network_id, **kwargs
            )
            
            return f"✅ Updated storm control settings"
        except Exception as e:
            return f"❌ Error updating storm control: {str(e)}"
    
    @app.tool(
        name="update_network_switch_mtu",
        description="✏️ Update MTU settings. Requires confirmation."
    )
    def update_network_switch_mtu(
        network_id: str,
        default_mtu_size: Optional[int] = None,
        overrides: Optional[List[Dict[str, Any]]] = None,
        confirmed: bool = False
    ):
        """
        Update MTU settings.
        
        Args:
            network_id: Network ID
            default_mtu_size: Default MTU size (1500-9578)
            overrides: MTU overrides for specific switches/ports
            confirmed: Must be true to execute
        """
        if not confirmed:
            return "⚠️ Updating MTU settings requires confirmed=true"
        
        try:
            kwargs = {}
            
            if default_mtu_size is not None:
                kwargs["defaultMtuSize"] = default_mtu_size
            if overrides is not None:
                kwargs["overrides"] = overrides
            
            result = meraki_client.dashboard.switch.updateNetworkSwitchMtu(
                network_id, **kwargs
            )
            
            return f"✅ Updated MTU settings"
        except Exception as e:
            return f"❌ Error updating MTU: {str(e)}"
    
    @app.tool(
        name="update_network_switch_alternate_management_interface",
        description="✏️ Update alternate management interface. Requires confirmation."
    )
    def update_network_switch_alternate_management_interface(
        network_id: str,
        enabled: Optional[bool] = None,
        vlan_id: Optional[int] = None,
        protocols: Optional[List[str]] = None,
        switches: Optional[List[Dict[str, Any]]] = None,
        confirmed: bool = False
    ):
        """
        Update alternate management interface settings.
        
        Args:
            network_id: Network ID
            enabled: Enable alternate management interface
            vlan_id: VLAN ID for management
            protocols: Management protocols (e.g., ["radius", "snmp", "syslog"])
            switches: Switch-specific configurations
            confirmed: Must be true to execute
        """
        if not confirmed:
            return "⚠️ Updating alternate management interface requires confirmed=true"
        
        try:
            kwargs = {}
            
            if enabled is not None:
                kwargs["enabled"] = enabled
            if vlan_id is not None:
                kwargs["vlanId"] = vlan_id
            if protocols is not None:
                kwargs["protocols"] = protocols
            if switches is not None:
                kwargs["switches"] = switches
            
            result = meraki_client.dashboard.switch.updateNetworkSwitchAlternateManagementInterface(
                network_id, **kwargs
            )
            
            return f"✅ Updated alternate management interface"
        except Exception as e:
            return f"❌ Error updating alternate management interface: {str(e)}"
    
    @app.tool(
        name="update_network_switch_dscp_to_cos_mappings",
        description="✏️ Update DSCP to CoS mappings. Requires confirmation."
    )
    def update_network_switch_dscp_to_cos_mappings(
        network_id: str,
        mappings: List[Dict[str, Any]],
        confirmed: bool = False
    ):
        """
        Update DSCP to CoS mappings.
        
        Args:
            network_id: Network ID
            mappings: List of DSCP to CoS mappings [{"dscp": 0, "cos": 0, "title": "Best effort"}]
            confirmed: Must be true to execute
        """
        if not confirmed:
            return "⚠️ Updating DSCP to CoS mappings requires confirmed=true"
        
        try:
            result = meraki_client.dashboard.switch.updateNetworkSwitchDscpToCosMappings(
                network_id, mappings=mappings
            )
            
            return f"✅ Updated DSCP to CoS mappings"
        except Exception as e:
            return f"❌ Error updating DSCP to CoS mappings: {str(e)}"
    
    @app.tool(
        name="update_device_switch_warm_spare",
        description="✏️ Update warm spare configuration. Requires confirmation."
    )
    def update_device_switch_warm_spare(
        serial: str,
        enabled: bool,
        spare_serial: Optional[str] = None,
        confirmed: bool = False
    ):
        """
        Update warm spare configuration.
        
        Args:
            serial: Primary switch serial number
            enabled: Enable warm spare
            spare_serial: Spare switch serial number
            confirmed: Must be true to execute
        """
        if not confirmed:
            return "⚠️ Updating warm spare requires confirmed=true"
        
        try:
            kwargs = {"enabled": enabled}
            
            if spare_serial:
                kwargs["spareSerial"] = spare_serial
            
            result = meraki_client.dashboard.switch.updateDeviceSwitchWarmSpare(
                serial, **kwargs
            )
            
            return f"✅ Updated warm spare configuration"
        except Exception as e:
            return f"❌ Error updating warm spare: {str(e)}"
    
    # ==================== DHCP & ARP ====================
    
    @app.tool(
        name="create_network_switch_dhcp_server_policy_arp_inspection",
        description="➕ Create ARP inspection trusted server. Requires confirmation."
    )
    def create_network_switch_dhcp_server_policy_arp_inspection(
        network_id: str,
        mac: str,
        vlan: int,
        ipv4: Dict[str, str],
        confirmed: bool = False
    ):
        """
        Create ARP inspection trusted server.
        
        Args:
            network_id: Network ID
            mac: MAC address
            vlan: VLAN ID
            ipv4: IPv4 configuration {"address": "192.168.1.1"}
            confirmed: Must be true to execute
        """
        if not confirmed:
            return "⚠️ Creating ARP inspection trusted server requires confirmed=true"
        
        try:
            result = meraki_client.dashboard.switch.createNetworkSwitchDhcpServerPolicyArpInspectionTrustedServer(
                network_id, mac=mac, vlan=vlan, ipv4=ipv4
            )
            
            return f"✅ Created ARP inspection trusted server for {mac}"
        except Exception as e:
            return f"❌ Error creating ARP inspection trusted server: {str(e)}"
    
    @app.tool(
        name="update_network_switch_dhcp_server_policy",
        description="✏️ Update DHCP server policy. Requires confirmation."
    )
    def update_network_switch_dhcp_server_policy(
        network_id: str,
        default_policy: Optional[str] = None,
        alerts: Optional[Dict[str, Any]] = None,
        arp_inspection: Optional[Dict[str, Any]] = None,
        allowed_servers: Optional[List[str]] = None,
        blocked_servers: Optional[List[str]] = None,
        confirmed: bool = False
    ):
        """
        Update DHCP server policy.
        
        Args:
            network_id: Network ID
            default_policy: "allow" or "block"
            alerts: Alert configuration
            arp_inspection: ARP inspection configuration
            allowed_servers: List of allowed DHCP server IPs
            blocked_servers: List of blocked DHCP server IPs
            confirmed: Must be true to execute
        """
        if not confirmed:
            return "⚠️ Updating DHCP server policy requires confirmed=true"
        
        try:
            kwargs = {}
            
            if default_policy is not None:
                kwargs["defaultPolicy"] = default_policy
            if alerts is not None:
                kwargs["alerts"] = alerts
            if arp_inspection is not None:
                kwargs["arpInspection"] = arp_inspection
            if allowed_servers is not None:
                kwargs["allowedServers"] = allowed_servers
            if blocked_servers is not None:
                kwargs["blockedServers"] = blocked_servers
            
            result = meraki_client.dashboard.switch.updateNetworkSwitchDhcpServerPolicy(
                network_id, **kwargs
            )
            
            return f"✅ Updated DHCP server policy"
        except Exception as e:
            return f"❌ Error updating DHCP server policy: {str(e)}"
    
    @app.tool(
        name="update_network_switch_dhcp_server_policy_arp_inspection",
        description="✏️ Update ARP inspection trusted server. Requires confirmation."
    )
    def update_network_switch_dhcp_server_policy_arp_inspection(
        network_id: str,
        trusted_server_id: str,
        mac: Optional[str] = None,
        vlan: Optional[int] = None,
        ipv4: Optional[Dict[str, str]] = None,
        confirmed: bool = False
    ):
        """
        Update ARP inspection trusted server.
        
        Args:
            network_id: Network ID
            trusted_server_id: Trusted server ID
            mac: MAC address
            vlan: VLAN ID
            ipv4: IPv4 configuration
            confirmed: Must be true to execute
        """
        if not confirmed:
            return "⚠️ Updating ARP inspection trusted server requires confirmed=true"
        
        try:
            kwargs = {}
            
            if mac is not None:
                kwargs["mac"] = mac
            if vlan is not None:
                kwargs["vlan"] = vlan
            if ipv4 is not None:
                kwargs["ipv4"] = ipv4
            
            result = meraki_client.dashboard.switch.updateNetworkSwitchDhcpServerPolicyArpInspectionTrustedServer(
                network_id, trusted_server_id, **kwargs
            )
            
            return f"✅ Updated ARP inspection trusted server {trusted_server_id}"
        except Exception as e:
            return f"❌ Error updating ARP inspection trusted server: {str(e)}"
    
    @app.tool(
        name="delete_network_switch_dhcp_server_policy_arp_inspection",
        description="🗑️ Delete ARP inspection trusted server. Requires confirmation."
    )
    def delete_network_switch_dhcp_server_policy_arp_inspection(
        network_id: str,
        trusted_server_id: str,
        confirmed: bool = False
    ):
        """
        Delete ARP inspection trusted server.
        
        Args:
            network_id: Network ID
            trusted_server_id: Trusted server ID
            confirmed: Must be true to execute
        """
        if not confirmed:
            return "⚠️ Deleting ARP inspection trusted server requires confirmed=true. This cannot be undone!"
        
        try:
            meraki_client.dashboard.switch.deleteNetworkSwitchDhcpServerPolicyArpInspectionTrustedServer(
                network_id, trusted_server_id
            )
            return f"✅ Deleted ARP inspection trusted server {trusted_server_id}"
        except Exception as e:
            return f"❌ Error deleting ARP inspection trusted server: {str(e)}"
    
    # ==================== TEMPLATES & OTHER ====================
    
    @app.tool(
        name="update_organization_config_template_switch_profile_port",
        description="✏️ Update a switch profile port in a config template. Requires confirmation."
    )
    def update_organization_config_template_switch_profile_port(
        organization_id: str,
        config_template_id: str,
        profile_id: str,
        port_id: str,
        name: Optional[str] = None,
        type: Optional[str] = None,
        vlan: Optional[int] = None,
        voice_vlan: Optional[int] = None,
        allowed_vlans: Optional[str] = None,
        isolation_enabled: Optional[bool] = None,
        rstp_enabled: Optional[bool] = None,
        stp_guard: Optional[str] = None,
        access_policy_type: Optional[str] = None,
        access_policy_number: Optional[int] = None,
        link_negotiation: Optional[str] = None,
        port_schedule_id: Optional[str] = None,
        udld: Optional[str] = None,
        confirmed: bool = False
    ):
        """
        Update a switch profile port in a config template.
        
        Args:
            organization_id: Organization ID
            config_template_id: Config template ID
            profile_id: Switch profile ID
            port_id: Port ID
            name: Port name
            type: "trunk" or "access"
            vlan: Access VLAN
            voice_vlan: Voice VLAN
            allowed_vlans: Allowed VLANs for trunk
            isolation_enabled: Port isolation
            rstp_enabled: RSTP enable
            stp_guard: STP guard mode
            access_policy_type: Access policy type
            access_policy_number: Access policy number
            link_negotiation: Link negotiation mode
            port_schedule_id: Port schedule ID
            udld: UDLD mode
            confirmed: Must be true to execute
        """
        if not confirmed:
            return "⚠️ Updating template port requires confirmed=true"
        
        try:
            kwargs = {}
            
            if name is not None:
                kwargs["name"] = name
            if type is not None:
                kwargs["type"] = type
            if vlan is not None:
                kwargs["vlan"] = vlan
            if voice_vlan is not None:
                kwargs["voiceVlan"] = voice_vlan
            if allowed_vlans is not None:
                kwargs["allowedVlans"] = allowed_vlans
            if isolation_enabled is not None:
                kwargs["isolationEnabled"] = isolation_enabled
            if rstp_enabled is not None:
                kwargs["rstpEnabled"] = rstp_enabled
            if stp_guard is not None:
                kwargs["stpGuard"] = stp_guard
            if access_policy_type is not None:
                kwargs["accessPolicyType"] = access_policy_type
            if access_policy_number is not None:
                kwargs["accessPolicyNumber"] = access_policy_number
            if link_negotiation is not None:
                kwargs["linkNegotiation"] = link_negotiation
            if port_schedule_id is not None:
                kwargs["portScheduleId"] = port_schedule_id
            if udld is not None:
                kwargs["udld"] = udld
            
            result = meraki_client.dashboard.switch.updateOrganizationConfigTemplateSwitchProfilePort(
                organization_id, config_template_id, profile_id, port_id, **kwargs
            )
            
            return f"✅ Updated template port {port_id}"
        except Exception as e:
            return f"❌ Error updating template port: {str(e)}"
    
    @app.tool(
        name="clone_organization_switch_devices",
        description="🔄 Clone switch configuration to other switches. Requires confirmation."
    )
    def clone_organization_switch_devices(
        organization_id: str,
        source_serial: str,
        target_serials: List[str],
        confirmed: bool = False
    ):
        """
        Clone switch configuration to other switches.
        
        Args:
            organization_id: Organization ID
            source_serial: Source switch serial number
            target_serials: List of target switch serial numbers
            confirmed: Must be true to execute
        """
        if not confirmed:
            return "⚠️ Cloning switch configuration requires confirmed=true"
        
        try:
            result = meraki_client.dashboard.switch.cloneOrganizationSwitchDevices(
                organization_id, sourceSerial=source_serial, targetSerials=target_serials
            )
            
            return f"✅ Cloned configuration from {source_serial} to {len(target_serials)} switches"
        except Exception as e:
            return f"❌ Error cloning switch configuration: {str(e)}"