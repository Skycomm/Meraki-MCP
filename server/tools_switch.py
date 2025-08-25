"""
Switch management tools for the Cisco Meraki MCP Server - COMPLETE v1.61 IMPLEMENTATION.
"""

from typing import Optional, List, Dict, Any

# Global variables to store app and meraki client
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
    
    # Register all switch tools
    register_switch_tool_handlers()

def register_switch_tool_handlers():
    """Register all switch tool handlers - COMPLETE SET."""
    
    # ========== Port Management ==========
    
    @app.tool(
        name="get_device_switch_ports",
        description="🔌 Get all ports on a switch"
    )
    def get_device_switch_ports(serial: str):
        """Get all ports on a switch device."""
        try:
            ports = meraki_client.dashboard.switch.getDeviceSwitchPorts(serial)
            
            if not ports:
                return f"No ports found for switch {serial}."
                
            result = f"# 🔌 Switch Ports for Device {serial}\n\n"
            for port in ports:
                port_id = port.get('portId', 'Unknown')
                result += f"## Port {port_id}: {port.get('name', 'Unnamed')}\n"
                result += f"- **Enabled**: {'✅' if port.get('enabled') else '❌'}\n"
                result += f"- **Type**: {port.get('type', 'N/A')}\n"
                result += f"- **VLAN**: {port.get('vlan', 'N/A')}\n"
                result += f"- **PoE**: {'✅ Enabled' if port.get('poeEnabled') else '❌ Disabled'}\n"
                
                if port.get('voiceVlan'):
                    result += f"- **Voice VLAN**: {port['voiceVlan']}\n"
                    
                if port.get('allowedVlans'):
                    result += f"- **Allowed VLANs**: {port['allowedVlans']}\n"
                    
                if port.get('linkNegotiation'):
                    result += f"- **Link Negotiation**: {port['linkNegotiation']}\n"
                    
                result += "\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving switch ports: {str(e)}"
    
    @app.tool(
        name="get_device_switch_port",
        description="🔌 Get details of a specific switch port"
    )
    def get_device_switch_port(serial: str, port_id: str):
        """Get configuration for a specific switch port."""
        try:
            port = meraki_client.dashboard.switch.getDeviceSwitchPort(serial, port_id)
            
            result = f"# 🔌 Port {port_id} Configuration\n\n"
            result += f"**Name**: {port.get('name', 'Unnamed')}\n"
            result += f"**Enabled**: {'✅' if port.get('enabled') else '❌'}\n"
            result += f"**Type**: {port.get('type', 'N/A')}\n"
            result += f"**VLAN**: {port.get('vlan', 'N/A')}\n"
            result += f"**PoE Enabled**: {'✅' if port.get('poeEnabled') else '❌'}\n"
            
            if port.get('voiceVlan'):
                result += f"**Voice VLAN**: {port['voiceVlan']}\n"
                
            if port.get('allowedVlans'):
                result += f"**Allowed VLANs**: {port['allowedVlans']}\n"
                
            if port.get('isolationEnabled'):
                result += f"**Port Isolation**: ✅ Enabled\n"
                
            if port.get('rstpEnabled') is not None:
                result += f"**RSTP**: {'✅ Enabled' if port['rstpEnabled'] else '❌ Disabled'}\n"
                
            if port.get('stpGuard'):
                result += f"**STP Guard**: {port['stpGuard']}\n"
                
            if port.get('linkNegotiation'):
                result += f"**Link Negotiation**: {port['linkNegotiation']}\n"
                
            if port.get('portScheduleId'):
                result += f"**Port Schedule**: {port['portScheduleId']}\n"
                
            if port.get('udld'):
                result += f"**UDLD**: {port['udld']}\n"
                
            if port.get('accessPolicyType'):
                result += f"**Access Policy Type**: {port['accessPolicyType']}\n"
                if port.get('accessPolicyNumber'):
                    result += f"**Access Policy Number**: {port['accessPolicyNumber']}\n"
                    
            if port.get('macAllowList'):
                result += f"\n## MAC Allow List\n"
                for mac in port['macAllowList']:
                    result += f"- {mac}\n"
                    
            if port.get('stickyMacAllowList'):
                result += f"\n## Sticky MAC Allow List\n"
                for mac in port['stickyMacAllowList']:
                    result += f"- {mac}\n"
                    
            if port.get('tags'):
                result += f"\n**Tags**: {', '.join(port['tags'])}\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving port {port_id}: {str(e)}"
    
    @app.tool(
        name="update_device_switch_port",
        description="🔌 Update switch port configuration"
    )
    def update_device_switch_port(
        serial: str,
        port_id: str,
        name: Optional[str] = None,
        enabled: Optional[bool] = None,
        type: Optional[str] = None,
        vlan: Optional[int] = None,
        voice_vlan: Optional[int] = None,
        poe_enabled: Optional[bool] = None,
        isolation_enabled: Optional[bool] = None,
        rstp_enabled: Optional[bool] = None,
        stp_guard: Optional[str] = None,
        link_negotiation: Optional[str] = None,
        port_schedule_id: Optional[str] = None,
        udld: Optional[str] = None,
        access_policy_type: Optional[str] = None,
        access_policy_number: Optional[int] = None,
        allowed_vlans: Optional[str] = None,
        tags: Optional[List[str]] = None
    ):
        """Update configuration for a switch port."""
        try:
            kwargs = {}
            if name is not None:
                kwargs['name'] = name
            if enabled is not None:
                kwargs['enabled'] = enabled
            if type is not None:
                kwargs['type'] = type
            if vlan is not None:
                kwargs['vlan'] = vlan
            if voice_vlan is not None:
                kwargs['voiceVlan'] = voice_vlan
            if poe_enabled is not None:
                kwargs['poeEnabled'] = poe_enabled
            if isolation_enabled is not None:
                kwargs['isolationEnabled'] = isolation_enabled
            if rstp_enabled is not None:
                kwargs['rstpEnabled'] = rstp_enabled
            if stp_guard is not None:
                kwargs['stpGuard'] = stp_guard
            if link_negotiation is not None:
                kwargs['linkNegotiation'] = link_negotiation
            if port_schedule_id is not None:
                kwargs['portScheduleId'] = port_schedule_id
            if udld is not None:
                kwargs['udld'] = udld
            if access_policy_type is not None:
                kwargs['accessPolicyType'] = access_policy_type
            if access_policy_number is not None:
                kwargs['accessPolicyNumber'] = access_policy_number
            if allowed_vlans is not None:
                kwargs['allowedVlans'] = allowed_vlans
            if tags is not None:
                kwargs['tags'] = tags
                
            result = meraki_client.dashboard.switch.updateDeviceSwitchPort(
                serial,
                port_id,
                **kwargs
            )
            
            return f"✅ Port {port_id} updated successfully!"
            
        except Exception as e:
            return f"Error updating port: {str(e)}"
    
    @app.tool(
        name="cycle_device_switch_ports",
        description="🔄 Power cycle switch ports (reboot PoE devices)"
    )
    def cycle_device_switch_ports(serial: str, ports: List[str]):
        """Power cycle switch ports to reboot PoE devices."""
        try:
            result = meraki_client.dashboard.switch.cycleDeviceSwitchPorts(
                serial,
                ports=ports
            )
            
            return f"✅ Successfully initiated power cycle for ports: {', '.join(ports)}\n\nDevices connected to these ports will be rebooted."
            
        except Exception as e:
            return f"Error cycling ports: {str(e)}"
    
    @app.tool(
        name="get_device_switch_ports_statuses",
        description="📊 Get real-time port statuses"
    )
    def get_device_switch_ports_statuses(
        serial: str,
        timespan: Optional[int] = 60
    ):
        """Get real-time status information for all switch ports."""
        try:
            statuses = meraki_client.dashboard.switch.getDeviceSwitchPortsStatuses(
                serial,
                timespan=timespan
            )
            
            if not statuses:
                return f"No port statuses found for switch {serial}."
                
            result = f"# 📊 Port Statuses for Switch {serial}\n"
            result += f"*Last {timespan} seconds*\n\n"
            
            for port_status in statuses:
                port_id = port_status.get('portId', 'Unknown')
                result += f"## Port {port_id}\n"
                
                # Connection status
                if port_status.get('enabled'):
                    status = port_status.get('status', 'Unknown')
                    if status == 'Connected':
                        result += f"- **Status**: ✅ Connected\n"
                    elif status == 'Disconnected':
                        result += f"- **Status**: ❌ Disconnected\n"
                    else:
                        result += f"- **Status**: {status}\n"
                else:
                    result += f"- **Status**: ⚫ Disabled\n"
                    
                # Speed and duplex
                if port_status.get('speed'):
                    result += f"- **Speed**: {port_status['speed']} Mbps\n"
                if port_status.get('duplex'):
                    result += f"- **Duplex**: {port_status['duplex']}\n"
                    
                # Traffic
                if port_status.get('usageInKb'):
                    usage_mb = port_status['usageInKb'].get('total', 0) / 1024
                    result += f"- **Traffic**: {usage_mb:.2f} MB total\n"
                    if port_status['usageInKb'].get('sent'):
                        sent_mb = port_status['usageInKb']['sent'] / 1024
                        result += f"  - Sent: {sent_mb:.2f} MB\n"
                    if port_status['usageInKb'].get('recv'):
                        recv_mb = port_status['usageInKb']['recv'] / 1024
                        result += f"  - Received: {recv_mb:.2f} MB\n"
                        
                # Errors and warnings
                if port_status.get('errors'):
                    result += f"- **Errors**: {', '.join(port_status['errors'])}\n"
                if port_status.get('warnings'):
                    result += f"- **Warnings**: {', '.join(port_status['warnings'])}\n"
                    
                # Client info
                if port_status.get('clientCount'):
                    result += f"- **Connected Clients**: {port_status['clientCount']}\n"
                    
                # PoE info
                if port_status.get('powerUsageInWh') is not None:
                    result += f"- **PoE Power**: {port_status['powerUsageInWh']} Wh\n"
                    
                # CDP/LLDP info
                if port_status.get('cdp'):
                    cdp = port_status['cdp']
                    result += f"- **CDP Neighbor**: {cdp.get('deviceId', 'Unknown')}\n"
                    if cdp.get('portId'):
                        result += f"  - Remote Port: {cdp['portId']}\n"
                        
                if port_status.get('lldp'):
                    lldp = port_status['lldp']
                    result += f"- **LLDP Neighbor**: {lldp.get('systemName', 'Unknown')}\n"
                    if lldp.get('portId'):
                        result += f"  - Remote Port: {lldp['portId']}\n"
                        
                result += "\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving port statuses: {str(e)}"
    
    @app.tool(
        name="get_device_switch_ports_statuses_packets",
        description="📊 Get packet counters for switch ports"
    )
    def get_device_switch_ports_statuses_packets(
        serial: str,
        timespan: Optional[int] = 60
    ):
        """Get packet counter information for switch ports."""
        try:
            packets = meraki_client.dashboard.switch.getDeviceSwitchPortsStatusesPackets(
                serial,
                timespan=timespan
            )
            
            if not packets:
                return f"No packet data found for switch {serial}."
                
            result = f"# 📊 Packet Counters for Switch {serial}\n"
            result += f"*Last {timespan} seconds*\n\n"
            
            for port_packets in packets:
                port_id = port_packets.get('portId', 'Unknown')
                result += f"## Port {port_id}\n"
                
                # Packet counts
                if port_packets.get('packets'):
                    pkts = port_packets['packets']
                    
                    # Sent packets
                    if pkts.get('sent'):
                        result += f"- **Sent Packets**: {pkts['sent']:,}\n"
                        
                    # Received packets
                    if pkts.get('recv'):
                        result += f"- **Received Packets**: {pkts['recv']:,}\n"
                        
                    # Rates
                    if port_packets.get('ratePerSec'):
                        rates = port_packets['ratePerSec']
                        if rates.get('sent'):
                            result += f"- **Send Rate**: {rates['sent']:,} pps\n"
                        if rates.get('recv'):
                            result += f"- **Receive Rate**: {rates['recv']:,} pps\n"
                            
                result += "\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving packet counters: {str(e)}"
    
    # ========== Access Policies ==========
    
    @app.tool(
        name="get_network_switch_access_policies",
        description="🔐 Get all switch access policies"
    )
    def get_network_switch_access_policies(network_id: str):
        """Get all access policies configured for switches in a network."""
        try:
            policies = meraki_client.dashboard.switch.getNetworkSwitchAccessPolicies(network_id)
            
            if not policies:
                return f"No access policies found for network {network_id}."
                
            result = f"# 🔐 Switch Access Policies for Network {network_id}\n\n"
            
            for policy in policies:
                result += f"## Policy: {policy.get('name', 'Unnamed')}\n"
                result += f"- **Access Policy Number**: {policy.get('accessPolicyNumber', 'N/A')}\n"
                
                # RADIUS settings
                if policy.get('radiusServers'):
                    result += f"- **RADIUS Servers**: {len(policy['radiusServers'])} configured\n"
                    
                if policy.get('radiusTestingEnabled'):
                    result += f"- **RADIUS Testing**: ✅ Enabled\n"
                    
                if policy.get('radiusCoaSupportEnabled'):
                    result += f"- **RADIUS CoA**: ✅ Enabled\n"
                    
                if policy.get('radiusAccountingEnabled'):
                    result += f"- **RADIUS Accounting**: ✅ Enabled\n"
                    if policy.get('radiusAccountingServers'):
                        result += f"  - Accounting Servers: {len(policy['radiusAccountingServers'])}\n"
                        
                # Authentication methods
                if policy.get('radiusGroupAttribute'):
                    result += f"- **RADIUS Group Attribute**: {policy['radiusGroupAttribute']}\n"
                    
                if policy.get('hostMode'):
                    result += f"- **Host Mode**: {policy['hostMode']}\n"
                    
                if policy.get('accessPolicyType'):
                    result += f"- **Access Policy Type**: {policy['accessPolicyType']}\n"
                    
                # Voice VLAN
                if policy.get('voiceVlanClients'):
                    result += f"- **Voice VLAN Clients**: ✅ Enabled\n"
                    
                # URL redirect
                if policy.get('urlRedirectWalledGardenEnabled'):
                    result += f"- **URL Redirect**: ✅ Enabled\n"
                    if policy.get('urlRedirectWalledGardenRanges'):
                        result += f"  - Walled Garden: {', '.join(policy['urlRedirectWalledGardenRanges'])}\n"
                        
                result += "\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving access policies: {str(e)}"
    
    @app.tool(
        name="get_network_switch_access_policy",
        description="🔐 Get a specific access policy"
    )
    def get_network_switch_access_policy(
        network_id: str,
        access_policy_number: str
    ):
        """Get details of a specific switch access policy."""
        try:
            policy = meraki_client.dashboard.switch.getNetworkSwitchAccessPolicy(
                network_id,
                access_policy_number
            )
            
            result = f"# 🔐 Access Policy Details\n\n"
            result += f"**Name**: {policy.get('name', 'Unnamed')}\n"
            result += f"**Access Policy Number**: {policy.get('accessPolicyNumber', 'N/A')}\n"
            
            # RADIUS settings
            if policy.get('radiusServers'):
                result += f"\n## RADIUS Servers\n"
                for idx, server in enumerate(policy['radiusServers'], 1):
                    result += f"### Server {idx}\n"
                    result += f"- **Host**: {server.get('host', 'N/A')}\n"
                    result += f"- **Port**: {server.get('port', 1812)}\n"
                    
            # Authentication settings
            if policy.get('hostMode'):
                result += f"\n**Host Mode**: {policy['hostMode']}\n"
                
            if policy.get('accessPolicyType'):
                result += f"**Access Policy Type**: {policy['accessPolicyType']}\n"
                
            if policy.get('increaseAccessSpeed'):
                result += f"**Increase Access Speed**: ✅ Enabled\n"
                
            # Guest settings
            if policy.get('guestPortBouncing'):
                result += f"**Guest Port Bouncing**: ✅ Enabled\n"
                
            if policy.get('guestVlanId'):
                result += f"**Guest VLAN**: {policy['guestVlanId']}\n"
                
            # Voice VLAN
            if policy.get('voiceVlanClients'):
                result += f"**Voice VLAN Clients**: ✅ Enabled\n"
                
            # Failed auth VLAN
            if policy.get('failedAuthVlanId'):
                result += f"**Failed Auth VLAN**: {policy['failedAuthVlanId']}\n"
                
            # Critical auth
            if policy.get('criticalAuth'):
                critical = policy['criticalAuth']
                result += f"\n## Critical Auth\n"
                result += f"- **Data VLAN**: {critical.get('dataVlanId', 'N/A')}\n"
                result += f"- **Voice VLAN**: {critical.get('voiceVlanId', 'N/A')}\n"
                result += f"- **Suspend Port Bounce**: {'✅' if critical.get('suspendPortBounce') else '❌'}\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving access policy: {str(e)}"
    
    @app.tool(
        name="create_network_switch_access_policy",
        description="🔐 Create a new access policy"
    )
    def create_network_switch_access_policy(
        network_id: str,
        name: str,
        radius_servers: List[Dict[str, Any]],
        host_mode: Optional[str] = 'Single-Host',
        access_policy_type: Optional[str] = 'Hybrid authentication',
        radius_testing_enabled: Optional[bool] = False,
        radius_coa_support_enabled: Optional[bool] = False,
        radius_accounting_enabled: Optional[bool] = False,
        guest_vlan_id: Optional[int] = None
    ):
        """Create a new switch access policy."""
        try:
            kwargs = {
                'name': name,
                'radiusServers': radius_servers,
                'hostMode': host_mode,
                'accessPolicyType': access_policy_type,
                'radiusTestingEnabled': radius_testing_enabled,
                'radiusCoaSupportEnabled': radius_coa_support_enabled,
                'radiusAccountingEnabled': radius_accounting_enabled
            }
            
            if guest_vlan_id is not None:
                kwargs['guestVlanId'] = guest_vlan_id
                
            policy = meraki_client.dashboard.switch.createNetworkSwitchAccessPolicy(
                network_id,
                **kwargs
            )
            
            return f"✅ Access policy '{name}' created successfully!\n\nAccess Policy Number: {policy.get('accessPolicyNumber', 'N/A')}"
            
        except Exception as e:
            return f"Error creating access policy: {str(e)}"
    
    @app.tool(
        name="update_network_switch_access_policy",
        description="🔐 Update an access policy"
    )
    def update_network_switch_access_policy(
        network_id: str,
        access_policy_number: str,
        name: Optional[str] = None,
        radius_servers: Optional[List[Dict[str, Any]]] = None,
        host_mode: Optional[str] = None,
        access_policy_type: Optional[str] = None,
        guest_vlan_id: Optional[int] = None
    ):
        """Update an existing switch access policy."""
        try:
            kwargs = {}
            if name is not None:
                kwargs['name'] = name
            if radius_servers is not None:
                kwargs['radiusServers'] = radius_servers
            if host_mode is not None:
                kwargs['hostMode'] = host_mode
            if access_policy_type is not None:
                kwargs['accessPolicyType'] = access_policy_type
            if guest_vlan_id is not None:
                kwargs['guestVlanId'] = guest_vlan_id
                
            policy = meraki_client.dashboard.switch.updateNetworkSwitchAccessPolicy(
                network_id,
                access_policy_number,
                **kwargs
            )
            
            return f"✅ Access policy updated successfully!"
            
        except Exception as e:
            return f"Error updating access policy: {str(e)}"
    
    @app.tool(
        name="delete_network_switch_access_policy",
        description="🔐 Delete an access policy"
    )
    def delete_network_switch_access_policy(
        network_id: str,
        access_policy_number: str
    ):
        """Delete a switch access policy."""
        try:
            meraki_client.dashboard.switch.deleteNetworkSwitchAccessPolicy(
                network_id,
                access_policy_number
            )
            
            return f"✅ Access policy deleted successfully!"
            
        except Exception as e:
            return f"Error deleting access policy: {str(e)}"
    
    # ========== Port Schedules ==========
    
    @app.tool(
        name="get_network_switch_port_schedules",
        description="⏰ Get all port schedules"
    )
    def get_network_switch_port_schedules(network_id: str):
        """Get all port schedules configured for a network."""
        try:
            schedules = meraki_client.dashboard.switch.getNetworkSwitchPortSchedules(network_id)
            
            if not schedules:
                return f"No port schedules found for network {network_id}."
                
            result = f"# ⏰ Port Schedules for Network {network_id}\n\n"
            
            for schedule in schedules:
                result += f"## Schedule: {schedule.get('name', 'Unnamed')}\n"
                result += f"- **ID**: {schedule.get('id', 'N/A')}\n"
                
                if schedule.get('portSchedule'):
                    port_schedule = schedule['portSchedule']
                    
                    # Monday schedule
                    if port_schedule.get('monday'):
                        result += f"- **Monday**: {port_schedule['monday'].get('active', 'N/A')} ({port_schedule['monday'].get('from', 'N/A')} - {port_schedule['monday'].get('to', 'N/A')})\n"
                        
                    # Tuesday schedule
                    if port_schedule.get('tuesday'):
                        result += f"- **Tuesday**: {port_schedule['tuesday'].get('active', 'N/A')} ({port_schedule['tuesday'].get('from', 'N/A')} - {port_schedule['tuesday'].get('to', 'N/A')})\n"
                        
                    # Wednesday schedule
                    if port_schedule.get('wednesday'):
                        result += f"- **Wednesday**: {port_schedule['wednesday'].get('active', 'N/A')} ({port_schedule['wednesday'].get('from', 'N/A')} - {port_schedule['wednesday'].get('to', 'N/A')})\n"
                        
                    # Thursday schedule
                    if port_schedule.get('thursday'):
                        result += f"- **Thursday**: {port_schedule['thursday'].get('active', 'N/A')} ({port_schedule['thursday'].get('from', 'N/A')} - {port_schedule['thursday'].get('to', 'N/A')})\n"
                        
                    # Friday schedule
                    if port_schedule.get('friday'):
                        result += f"- **Friday**: {port_schedule['friday'].get('active', 'N/A')} ({port_schedule['friday'].get('from', 'N/A')} - {port_schedule['friday'].get('to', 'N/A')})\n"
                        
                    # Saturday schedule
                    if port_schedule.get('saturday'):
                        result += f"- **Saturday**: {port_schedule['saturday'].get('active', 'N/A')} ({port_schedule['saturday'].get('from', 'N/A')} - {port_schedule['saturday'].get('to', 'N/A')})\n"
                        
                    # Sunday schedule
                    if port_schedule.get('sunday'):
                        result += f"- **Sunday**: {port_schedule['sunday'].get('active', 'N/A')} ({port_schedule['sunday'].get('from', 'N/A')} - {port_schedule['sunday'].get('to', 'N/A')})\n"
                        
                result += "\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving port schedules: {str(e)}"
    
    @app.tool(
        name="create_network_switch_port_schedule",
        description="⏰ Create a new port schedule"
    )
    def create_network_switch_port_schedule(
        network_id: str,
        name: str,
        port_schedule: Dict[str, Any]
    ):
        """Create a new port schedule."""
        try:
            schedule = meraki_client.dashboard.switch.createNetworkSwitchPortSchedule(
                network_id,
                name=name,
                portSchedule=port_schedule
            )
            
            return f"✅ Port schedule '{name}' created successfully!\n\nSchedule ID: {schedule.get('id', 'N/A')}"
            
        except Exception as e:
            return f"Error creating port schedule: {str(e)}"
    
    @app.tool(
        name="update_network_switch_port_schedule",
        description="⏰ Update a port schedule"
    )
    def update_network_switch_port_schedule(
        network_id: str,
        port_schedule_id: str,
        name: Optional[str] = None,
        port_schedule: Optional[Dict[str, Any]] = None
    ):
        """Update an existing port schedule."""
        try:
            kwargs = {}
            if name is not None:
                kwargs['name'] = name
            if port_schedule is not None:
                kwargs['portSchedule'] = port_schedule
                
            schedule = meraki_client.dashboard.switch.updateNetworkSwitchPortSchedule(
                network_id,
                port_schedule_id,
                **kwargs
            )
            
            return f"✅ Port schedule updated successfully!"
            
        except Exception as e:
            return f"Error updating port schedule: {str(e)}"
    
    @app.tool(
        name="delete_network_switch_port_schedule",
        description="⏰ Delete a port schedule"
    )
    def delete_network_switch_port_schedule(
        network_id: str,
        port_schedule_id: str
    ):
        """Delete a port schedule."""
        try:
            meraki_client.dashboard.switch.deleteNetworkSwitchPortSchedule(
                network_id,
                port_schedule_id
            )
            
            return f"✅ Port schedule deleted successfully!"
            
        except Exception as e:
            return f"Error deleting port schedule: {str(e)}"
    
    # ========== Link Aggregation ==========
    
    @app.tool(
        name="get_network_switch_link_aggregations",
        description="🔗 Get all link aggregations (LAGs)"
    )
    def get_network_switch_link_aggregations(network_id: str):
        """Get all link aggregations configured in a network."""
        try:
            lags = meraki_client.dashboard.switch.getNetworkSwitchLinkAggregations(network_id)
            
            if not lags:
                return f"No link aggregations found for network {network_id}."
                
            result = f"# 🔗 Link Aggregations for Network {network_id}\n\n"
            
            for lag in lags:
                result += f"## LAG ID: {lag.get('id', 'Unknown')}\n"
                
                # Switch ports in LAG
                if lag.get('switchPorts'):
                    result += "### Member Ports\n"
                    for port in lag['switchPorts']:
                        result += f"- **{port.get('serial', 'Unknown')}** - Port {port.get('portId', 'Unknown')}\n"
                        
                # Configuration
                if lag.get('switchProfilePorts'):
                    result += "### Switch Profile Ports\n"
                    for profile_port in lag['switchProfilePorts']:
                        result += f"- **{profile_port.get('profile', 'Unknown')}** - Port {profile_port.get('portId', 'Unknown')}\n"
                        
                result += "\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving link aggregations: {str(e)}"
    
    @app.tool(
        name="create_network_switch_link_aggregation",
        description="🔗 Create a new link aggregation"
    )
    def create_network_switch_link_aggregation(
        network_id: str,
        switch_ports: Optional[List[Dict[str, Any]]] = None,
        switch_profile_ports: Optional[List[Dict[str, Any]]] = None
    ):
        """Create a new link aggregation."""
        try:
            kwargs = {}
            if switch_ports is not None:
                kwargs['switchPorts'] = switch_ports
            if switch_profile_ports is not None:
                kwargs['switchProfilePorts'] = switch_profile_ports
                
            lag = meraki_client.dashboard.switch.createNetworkSwitchLinkAggregation(
                network_id,
                **kwargs
            )
            
            return f"✅ Link aggregation created successfully!\n\nLAG ID: {lag.get('id', 'N/A')}"
            
        except Exception as e:
            return f"Error creating link aggregation: {str(e)}"
    
    @app.tool(
        name="update_network_switch_link_aggregation",
        description="🔗 Update a link aggregation"
    )
    def update_network_switch_link_aggregation(
        network_id: str,
        link_aggregation_id: str,
        switch_ports: Optional[List[Dict[str, Any]]] = None,
        switch_profile_ports: Optional[List[Dict[str, Any]]] = None
    ):
        """Update an existing link aggregation."""
        try:
            kwargs = {}
            if switch_ports is not None:
                kwargs['switchPorts'] = switch_ports
            if switch_profile_ports is not None:
                kwargs['switchProfilePorts'] = switch_profile_ports
                
            lag = meraki_client.dashboard.switch.updateNetworkSwitchLinkAggregation(
                network_id,
                link_aggregation_id,
                **kwargs
            )
            
            return f"✅ Link aggregation updated successfully!"
            
        except Exception as e:
            return f"Error updating link aggregation: {str(e)}"
    
    @app.tool(
        name="delete_network_switch_link_aggregation",
        description="🔗 Delete a link aggregation"
    )
    def delete_network_switch_link_aggregation(
        network_id: str,
        link_aggregation_id: str
    ):
        """Delete a link aggregation."""
        try:
            meraki_client.dashboard.switch.deleteNetworkSwitchLinkAggregation(
                network_id,
                link_aggregation_id
            )
            
            return f"✅ Link aggregation deleted successfully!"
            
        except Exception as e:
            return f"Error deleting link aggregation: {str(e)}"
    
    # ========== QoS Rules ==========
    
    @app.tool(
        name="get_network_switch_qos_rules",
        description="🎯 Get all QoS rules"
    )
    def get_network_switch_qos_rules(network_id: str):
        """Get all QoS rules configured for a network."""
        try:
            rules = meraki_client.dashboard.switch.getNetworkSwitchQosRules(network_id)
            
            if not rules:
                return f"No QoS rules found for network {network_id}."
                
            result = f"# 🎯 QoS Rules for Network {network_id}\n\n"
            
            for rule in rules:
                result += f"## Rule ID: {rule.get('id', 'Unknown')}\n"
                
                # Basic info
                if rule.get('vlan'):
                    result += f"- **VLAN**: {rule['vlan']}\n"
                    
                if rule.get('protocol'):
                    result += f"- **Protocol**: {rule['protocol']}\n"
                    
                # Source
                if rule.get('srcPort'):
                    result += f"- **Source Port**: {rule['srcPort']}\n"
                if rule.get('srcPortRange'):
                    result += f"- **Source Port Range**: {rule['srcPortRange']}\n"
                    
                # Destination
                if rule.get('dstPort'):
                    result += f"- **Destination Port**: {rule['dstPort']}\n"
                if rule.get('dstPortRange'):
                    result += f"- **Destination Port Range**: {rule['dstPortRange']}\n"
                    
                # DSCP value
                if rule.get('dscp') is not None:
                    result += f"- **DSCP**: {rule['dscp']}\n"
                    
                result += "\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving QoS rules: {str(e)}"
    
    @app.tool(
        name="get_network_switch_qos_rule",
        description="🎯 Get a specific QoS rule"
    )
    def get_network_switch_qos_rule(
        network_id: str,
        qos_rule_id: str
    ):
        """Get details of a specific QoS rule."""
        try:
            rule = meraki_client.dashboard.switch.getNetworkSwitchQosRule(
                network_id,
                qos_rule_id
            )
            
            result = f"# 🎯 QoS Rule Details\n\n"
            result += f"**Rule ID**: {rule.get('id', 'Unknown')}\n"
            
            if rule.get('vlan'):
                result += f"**VLAN**: {rule['vlan']}\n"
                
            if rule.get('protocol'):
                result += f"**Protocol**: {rule['protocol']}\n"
                
            # Source
            if rule.get('srcPort'):
                result += f"**Source Port**: {rule['srcPort']}\n"
            if rule.get('srcPortRange'):
                result += f"**Source Port Range**: {rule['srcPortRange']}\n"
                
            # Destination
            if rule.get('dstPort'):
                result += f"**Destination Port**: {rule['dstPort']}\n"
            if rule.get('dstPortRange'):
                result += f"**Destination Port Range**: {rule['dstPortRange']}\n"
                
            # DSCP value
            if rule.get('dscp') is not None:
                result += f"**DSCP**: {rule['dscp']}\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving QoS rule: {str(e)}"
    
    @app.tool(
        name="create_network_switch_qos_rule",
        description="🎯 Create a new QoS rule"
    )
    def create_network_switch_qos_rule(
        network_id: str,
        vlan: int,
        dscp: int,
        protocol: Optional[str] = None,
        src_port: Optional[int] = None,
        src_port_range: Optional[str] = None,
        dst_port: Optional[int] = None,
        dst_port_range: Optional[str] = None
    ):
        """Create a new QoS rule."""
        try:
            kwargs = {
                'vlan': vlan,
                'dscp': dscp
            }
            
            if protocol:
                kwargs['protocol'] = protocol
            if src_port:
                kwargs['srcPort'] = src_port
            if src_port_range:
                kwargs['srcPortRange'] = src_port_range
            if dst_port:
                kwargs['dstPort'] = dst_port
            if dst_port_range:
                kwargs['dstPortRange'] = dst_port_range
                
            rule = meraki_client.dashboard.switch.createNetworkSwitchQosRule(
                network_id,
                **kwargs
            )
            
            return f"✅ QoS rule created successfully!\n\nRule ID: {rule.get('id', 'N/A')}"
            
        except Exception as e:
            return f"Error creating QoS rule: {str(e)}"
    
    @app.tool(
        name="update_network_switch_qos_rule",
        description="🎯 Update a QoS rule"
    )
    def update_network_switch_qos_rule(
        network_id: str,
        qos_rule_id: str,
        vlan: Optional[int] = None,
        dscp: Optional[int] = None,
        protocol: Optional[str] = None,
        src_port: Optional[int] = None,
        src_port_range: Optional[str] = None,
        dst_port: Optional[int] = None,
        dst_port_range: Optional[str] = None
    ):
        """Update an existing QoS rule."""
        try:
            kwargs = {}
            if vlan is not None:
                kwargs['vlan'] = vlan
            if dscp is not None:
                kwargs['dscp'] = dscp
            if protocol is not None:
                kwargs['protocol'] = protocol
            if src_port is not None:
                kwargs['srcPort'] = src_port
            if src_port_range is not None:
                kwargs['srcPortRange'] = src_port_range
            if dst_port is not None:
                kwargs['dstPort'] = dst_port
            if dst_port_range is not None:
                kwargs['dstPortRange'] = dst_port_range
                
            rule = meraki_client.dashboard.switch.updateNetworkSwitchQosRule(
                network_id,
                qos_rule_id,
                **kwargs
            )
            
            return f"✅ QoS rule updated successfully!"
            
        except Exception as e:
            return f"Error updating QoS rule: {str(e)}"
    
    @app.tool(
        name="delete_network_switch_qos_rule",
        description="🎯 Delete a QoS rule"
    )
    def delete_network_switch_qos_rule(
        network_id: str,
        qos_rule_id: str
    ):
        """Delete a QoS rule."""
        try:
            meraki_client.dashboard.switch.deleteNetworkSwitchQosRule(
                network_id,
                qos_rule_id
            )
            
            return f"✅ QoS rule deleted successfully!"
            
        except Exception as e:
            return f"Error deleting QoS rule: {str(e)}"
    
    @app.tool(
        name="get_network_switch_qos_rules_order",
        description="🎯 Get QoS rules order"
    )
    def get_network_switch_qos_rules_order(network_id: str):
        """Get the order in which QoS rules are processed."""
        try:
            order = meraki_client.dashboard.switch.getNetworkSwitchQosRulesOrder(network_id)
            
            result = f"# 🎯 QoS Rules Processing Order for Network {network_id}\n\n"
            
            if order.get('ruleIds'):
                result += "Rules are processed in the following order:\n\n"
                for idx, rule_id in enumerate(order['ruleIds'], 1):
                    result += f"{idx}. Rule ID: {rule_id}\n"
            else:
                result += "No QoS rules order configured.\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving QoS rules order: {str(e)}"
    
    @app.tool(
        name="update_network_switch_qos_rules_order",
        description="🎯 Update QoS rules processing order"
    )
    def update_network_switch_qos_rules_order(
        network_id: str,
        rule_ids: List[str]
    ):
        """Update the order in which QoS rules are processed."""
        try:
            order = meraki_client.dashboard.switch.updateNetworkSwitchQosRulesOrder(
                network_id,
                ruleIds=rule_ids
            )
            
            return f"✅ QoS rules order updated successfully!\n\nNew order: {', '.join(rule_ids)}"
            
        except Exception as e:
            return f"Error updating QoS rules order: {str(e)}"
    
    # ========== STP Configuration ==========
    
    @app.tool(
        name="get_network_switch_stp",
        description="🌳 Get Spanning Tree Protocol settings"
    )
    def get_network_switch_stp(network_id: str):
        """Get Spanning Tree Protocol settings for a network."""
        try:
            stp = meraki_client.dashboard.switch.getNetworkSwitchStp(network_id)
            
            result = f"# 🌳 STP Settings for Network {network_id}\n\n"
            
            # RSTP enabled
            if stp.get('rstpEnabled') is not None:
                result += f"**RSTP Enabled**: {'✅' if stp['rstpEnabled'] else '❌'}\n"
                
            # STP bridge priority
            if stp.get('stpBridgePriority'):
                result += f"\n## STP Bridge Priority\n"
                for vlan_priority in stp['stpBridgePriority']:
                    result += f"- **VLAN {vlan_priority.get('vlanId', 'N/A')}**: {vlan_priority.get('stpPriority', 'N/A')}\n"
                    
            return result
            
        except Exception as e:
            return f"Error retrieving STP settings: {str(e)}"
    
    @app.tool(
        name="update_network_switch_stp",
        description="🌳 Update STP settings"
    )
    def update_network_switch_stp(
        network_id: str,
        rstp_enabled: Optional[bool] = None,
        stp_bridge_priority: Optional[List[Dict[str, Any]]] = None
    ):
        """Update Spanning Tree Protocol settings."""
        try:
            kwargs = {}
            if rstp_enabled is not None:
                kwargs['rstpEnabled'] = rstp_enabled
            if stp_bridge_priority is not None:
                kwargs['stpBridgePriority'] = stp_bridge_priority
                
            stp = meraki_client.dashboard.switch.updateNetworkSwitchStp(
                network_id,
                **kwargs
            )
            
            return f"✅ STP settings updated successfully!"
            
        except Exception as e:
            return f"Error updating STP settings: {str(e)}"
    
    # ========== Storm Control ==========
    
    @app.tool(
        name="get_network_switch_storm_control",
        description="⛈️ Get storm control settings"
    )
    def get_network_switch_storm_control(network_id: str):
        """Get storm control settings for a network."""
        try:
            storm_control = meraki_client.dashboard.switch.getNetworkSwitchStormControl(network_id)
            
            result = f"# ⛈️ Storm Control Settings for Network {network_id}\n\n"
            
            # Broadcast threshold
            if storm_control.get('broadcastThreshold') is not None:
                result += f"**Broadcast Threshold**: {storm_control['broadcastThreshold']}%\n"
                
            # Multicast threshold
            if storm_control.get('multicastThreshold') is not None:
                result += f"**Multicast Threshold**: {storm_control['multicastThreshold']}%\n"
                
            # Unknown unicast threshold
            if storm_control.get('unknownUnicastThreshold') is not None:
                result += f"**Unknown Unicast Threshold**: {storm_control['unknownUnicastThreshold']}%\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving storm control settings: {str(e)}"
    
    @app.tool(
        name="update_network_switch_storm_control",
        description="⛈️ Update storm control settings"
    )
    def update_network_switch_storm_control(
        network_id: str,
        broadcast_threshold: Optional[int] = None,
        multicast_threshold: Optional[int] = None,
        unknown_unicast_threshold: Optional[int] = None
    ):
        """Update storm control settings."""
        try:
            kwargs = {}
            if broadcast_threshold is not None:
                kwargs['broadcastThreshold'] = broadcast_threshold
            if multicast_threshold is not None:
                kwargs['multicastThreshold'] = multicast_threshold
            if unknown_unicast_threshold is not None:
                kwargs['unknownUnicastThreshold'] = unknown_unicast_threshold
                
            storm_control = meraki_client.dashboard.switch.updateNetworkSwitchStormControl(
                network_id,
                **kwargs
            )
            
            return f"✅ Storm control settings updated successfully!"
            
        except Exception as e:
            return f"Error updating storm control settings: {str(e)}"
    
    # ========== Switch Settings ==========
    
    @app.tool(
        name="get_network_switch_settings",
        description="⚙️ Get general switch settings"
    )
    def get_network_switch_settings(network_id: str):
        """Get general settings for switches in a network."""
        try:
            settings = meraki_client.dashboard.switch.getNetworkSwitchSettings(network_id)
            
            result = f"# ⚙️ Switch Settings for Network {network_id}\n\n"
            
            # VLAN
            if settings.get('vlan') is not None:
                result += f"**Management VLAN**: {settings['vlan']}\n"
                
            # Use combined power
            if settings.get('useCombinedPower') is not None:
                result += f"**Use Combined Power**: {'✅' if settings['useCombinedPower'] else '❌'}\n"
                
            # Power exceptions
            if settings.get('powerExceptions'):
                result += f"\n## Power Exceptions\n"
                for exception in settings['powerExceptions']:
                    result += f"- **{exception.get('serial', 'Unknown')}**: {exception.get('powerType', 'N/A')}\n"
                    
            # UplinkClientSampling
            if settings.get('uplinkClientSampling'):
                sampling = settings['uplinkClientSampling']
                result += f"\n## Uplink Client Sampling\n"
                result += f"- **Enabled**: {'✅' if sampling.get('enabled') else '❌'}\n"
                
            # MAC blocklist
            if settings.get('macBlocklist'):
                blocklist = settings['macBlocklist']
                result += f"\n## MAC Blocklist\n"
                result += f"- **Enabled**: {'✅' if blocklist.get('enabled') else '❌'}\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving switch settings: {str(e)}"
    
    @app.tool(
        name="update_network_switch_settings",
        description="⚙️ Update general switch settings"
    )
    def update_network_switch_settings(
        network_id: str,
        vlan: Optional[int] = None,
        use_combined_power: Optional[bool] = None,
        power_exceptions: Optional[List[Dict[str, str]]] = None
    ):
        """Update general switch settings."""
        try:
            kwargs = {}
            if vlan is not None:
                kwargs['vlan'] = vlan
            if use_combined_power is not None:
                kwargs['useCombinedPower'] = use_combined_power
            if power_exceptions is not None:
                kwargs['powerExceptions'] = power_exceptions
                
            settings = meraki_client.dashboard.switch.updateNetworkSwitchSettings(
                network_id,
                **kwargs
            )
            
            return f"✅ Switch settings updated successfully!"
            
        except Exception as e:
            return f"Error updating switch settings: {str(e)}"
    
    # ========== Routing ==========
    
    @app.tool(
        name="get_device_switch_routing_interfaces",
        description="🛣️ Get Layer 3 interfaces on a switch"
    )
    def get_device_switch_routing_interfaces(serial: str):
        """Get all Layer 3 interfaces on a switch."""
        try:
            interfaces = meraki_client.dashboard.switch.getDeviceSwitchRoutingInterfaces(serial)
            
            if not interfaces:
                return f"No routing interfaces found for switch {serial}."
                
            result = f"# 🛣️ Routing Interfaces for Switch {serial}\n\n"
            
            for interface in interfaces:
                result += f"## Interface: {interface.get('name', 'Unnamed')}\n"
                result += f"- **Interface ID**: {interface.get('interfaceId', 'N/A')}\n"
                result += f"- **Interface IP**: {interface.get('interfaceIp', 'N/A')}\n"
                result += f"- **Subnet**: {interface.get('subnet', 'N/A')}\n"
                result += f"- **VLAN ID**: {interface.get('vlanId', 'N/A')}\n"
                
                if interface.get('multicastRouting'):
                    result += f"- **Multicast Routing**: {interface['multicastRouting']}\n"
                    
                if interface.get('ospfSettings'):
                    ospf = interface['ospfSettings']
                    result += f"\n### OSPF Settings\n"
                    result += f"- **Area**: {ospf.get('area', 'N/A')}\n"
                    result += f"- **Cost**: {ospf.get('cost', 'N/A')}\n"
                    result += f"- **Passive**: {'✅' if ospf.get('isPassiveEnabled') else '❌'}\n"
                    
                result += "\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving routing interfaces: {str(e)}"
    
    @app.tool(
        name="get_device_switch_routing_interface",
        description="🛣️ Get a specific Layer 3 interface"
    )
    def get_device_switch_routing_interface(
        serial: str,
        interface_id: str
    ):
        """Get details of a specific Layer 3 interface."""
        try:
            interface = meraki_client.dashboard.switch.getDeviceSwitchRoutingInterface(
                serial,
                interface_id
            )
            
            result = f"# 🛣️ Routing Interface Details\n\n"
            result += f"**Name**: {interface.get('name', 'Unnamed')}\n"
            result += f"**Interface ID**: {interface.get('interfaceId', 'N/A')}\n"
            result += f"**Interface IP**: {interface.get('interfaceIp', 'N/A')}\n"
            result += f"**Subnet**: {interface.get('subnet', 'N/A')}\n"
            result += f"**VLAN ID**: {interface.get('vlanId', 'N/A')}\n"
            
            if interface.get('multicastRouting'):
                result += f"**Multicast Routing**: {interface['multicastRouting']}\n"
                
            if interface.get('ospfSettings'):
                ospf = interface['ospfSettings']
                result += f"\n## OSPF Settings\n"
                result += f"- **Area**: {ospf.get('area', 'N/A')}\n"
                result += f"- **Cost**: {ospf.get('cost', 'N/A')}\n"
                result += f"- **Passive**: {'✅' if ospf.get('isPassiveEnabled') else '❌'}\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving routing interface: {str(e)}"
    
    @app.tool(
        name="create_device_switch_routing_interface",
        description="🛣️ Create a Layer 3 interface"
    )
    def create_device_switch_routing_interface(
        serial: str,
        name: str,
        vlan_id: int,
        interface_ip: str,
        subnet: str,
        multicast_routing: Optional[str] = 'disabled',
        default_gateway: Optional[str] = None
    ):
        """Create a new Layer 3 interface on a switch."""
        try:
            kwargs = {
                'name': name,
                'vlanId': vlan_id,
                'interfaceIp': interface_ip,
                'subnet': subnet,
                'multicastRouting': multicast_routing
            }
            
            if default_gateway:
                kwargs['defaultGateway'] = default_gateway
                
            interface = meraki_client.dashboard.switch.createDeviceSwitchRoutingInterface(
                serial,
                **kwargs
            )
            
            return f"✅ Routing interface '{name}' created successfully!\n\nInterface ID: {interface.get('interfaceId', 'N/A')}"
            
        except Exception as e:
            return f"Error creating routing interface: {str(e)}"
    
    @app.tool(
        name="update_device_switch_routing_interface",
        description="🛣️ Update a Layer 3 interface"
    )
    def update_device_switch_routing_interface(
        serial: str,
        interface_id: str,
        name: Optional[str] = None,
        interface_ip: Optional[str] = None,
        subnet: Optional[str] = None,
        vlan_id: Optional[int] = None,
        multicast_routing: Optional[str] = None
    ):
        """Update a Layer 3 interface on a switch."""
        try:
            kwargs = {}
            if name is not None:
                kwargs['name'] = name
            if interface_ip is not None:
                kwargs['interfaceIp'] = interface_ip
            if subnet is not None:
                kwargs['subnet'] = subnet
            if vlan_id is not None:
                kwargs['vlanId'] = vlan_id
            if multicast_routing is not None:
                kwargs['multicastRouting'] = multicast_routing
                
            interface = meraki_client.dashboard.switch.updateDeviceSwitchRoutingInterface(
                serial,
                interface_id,
                **kwargs
            )
            
            return f"✅ Routing interface updated successfully!"
            
        except Exception as e:
            return f"Error updating routing interface: {str(e)}"
    
    @app.tool(
        name="delete_device_switch_routing_interface",
        description="🛣️ Delete a Layer 3 interface"
    )
    def delete_device_switch_routing_interface(
        serial: str,
        interface_id: str
    ):
        """Delete a Layer 3 interface from a switch."""
        try:
            meraki_client.dashboard.switch.deleteDeviceSwitchRoutingInterface(
                serial,
                interface_id
            )
            
            return f"✅ Routing interface deleted successfully!"
            
        except Exception as e:
            return f"Error deleting routing interface: {str(e)}"
    
    # ========== Static Routes ==========
    
    @app.tool(
        name="get_device_switch_routing_static_routes",
        description="🛣️ Get static routes on a switch"
    )
    def get_device_switch_routing_static_routes(serial: str):
        """Get all static routes configured on a switch."""
        try:
            routes = meraki_client.dashboard.switch.getDeviceSwitchRoutingStaticRoutes(serial)
            
            if not routes:
                return f"No static routes found for switch {serial}."
                
            result = f"# 🛣️ Static Routes for Switch {serial}\n\n"
            
            for route in routes:
                result += f"## Route: {route.get('name', 'Unnamed')}\n"
                result += f"- **Static Route ID**: {route.get('staticRouteId', 'N/A')}\n"
                result += f"- **Network**: {route.get('subnet', 'N/A')}\n"
                result += f"- **Next Hop IP**: {route.get('nextHopIp', 'N/A')}\n"
                
                if route.get('advertiseViaOspfEnabled') is not None:
                    result += f"- **Advertise via OSPF**: {'✅' if route['advertiseViaOspfEnabled'] else '❌'}\n"
                    
                if route.get('preferOverOspfRoutesEnabled') is not None:
                    result += f"- **Prefer over OSPF**: {'✅' if route['preferOverOspfRoutesEnabled'] else '❌'}\n"
                    
                result += "\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving static routes: {str(e)}"
    
    @app.tool(
        name="get_device_switch_routing_static_route",
        description="🛣️ Get a specific static route"
    )
    def get_device_switch_routing_static_route(
        serial: str,
        static_route_id: str
    ):
        """Get details of a specific static route."""
        try:
            route = meraki_client.dashboard.switch.getDeviceSwitchRoutingStaticRoute(
                serial,
                static_route_id
            )
            
            result = f"# 🛣️ Static Route Details\n\n"
            result += f"**Name**: {route.get('name', 'Unnamed')}\n"
            result += f"**Static Route ID**: {route.get('staticRouteId', 'N/A')}\n"
            result += f"**Network**: {route.get('subnet', 'N/A')}\n"
            result += f"**Next Hop IP**: {route.get('nextHopIp', 'N/A')}\n"
            
            if route.get('advertiseViaOspfEnabled') is not None:
                result += f"**Advertise via OSPF**: {'✅' if route['advertiseViaOspfEnabled'] else '❌'}\n"
                
            if route.get('preferOverOspfRoutesEnabled') is not None:
                result += f"**Prefer over OSPF**: {'✅' if route['preferOverOspfRoutesEnabled'] else '❌'}\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving static route: {str(e)}"
    
    @app.tool(
        name="create_device_switch_routing_static_route",
        description="🛣️ Create a static route"
    )
    def create_device_switch_routing_static_route(
        serial: str,
        name: str,
        subnet: str,
        next_hop_ip: str,
        advertise_via_ospf_enabled: Optional[bool] = False,
        prefer_over_ospf_routes_enabled: Optional[bool] = False
    ):
        """Create a new static route on a switch."""
        try:
            route = meraki_client.dashboard.switch.createDeviceSwitchRoutingStaticRoute(
                serial,
                name=name,
                subnet=subnet,
                nextHopIp=next_hop_ip,
                advertiseViaOspfEnabled=advertise_via_ospf_enabled,
                preferOverOspfRoutesEnabled=prefer_over_ospf_routes_enabled
            )
            
            return f"✅ Static route '{name}' created successfully!\n\nRoute ID: {route.get('staticRouteId', 'N/A')}"
            
        except Exception as e:
            return f"Error creating static route: {str(e)}"
    
    @app.tool(
        name="update_device_switch_routing_static_route",
        description="🛣️ Update a static route"
    )
    def update_device_switch_routing_static_route(
        serial: str,
        static_route_id: str,
        name: Optional[str] = None,
        subnet: Optional[str] = None,
        next_hop_ip: Optional[str] = None,
        advertise_via_ospf_enabled: Optional[bool] = None,
        prefer_over_ospf_routes_enabled: Optional[bool] = None
    ):
        """Update a static route on a switch."""
        try:
            kwargs = {}
            if name is not None:
                kwargs['name'] = name
            if subnet is not None:
                kwargs['subnet'] = subnet
            if next_hop_ip is not None:
                kwargs['nextHopIp'] = next_hop_ip
            if advertise_via_ospf_enabled is not None:
                kwargs['advertiseViaOspfEnabled'] = advertise_via_ospf_enabled
            if prefer_over_ospf_routes_enabled is not None:
                kwargs['preferOverOspfRoutesEnabled'] = prefer_over_ospf_routes_enabled
                
            route = meraki_client.dashboard.switch.updateDeviceSwitchRoutingStaticRoute(
                serial,
                static_route_id,
                **kwargs
            )
            
            return f"✅ Static route updated successfully!"
            
        except Exception as e:
            return f"Error updating static route: {str(e)}"
    
    @app.tool(
        name="delete_device_switch_routing_static_route",
        description="🛣️ Delete a static route"
    )
    def delete_device_switch_routing_static_route(
        serial: str,
        static_route_id: str
    ):
        """Delete a static route from a switch."""
        try:
            meraki_client.dashboard.switch.deleteDeviceSwitchRoutingStaticRoute(
                serial,
                static_route_id
            )
            
            return f"✅ Static route deleted successfully!"
            
        except Exception as e:
            return f"Error deleting static route: {str(e)}"
    
    # ========== DHCP ==========
    
    @app.tool(
        name="get_device_switch_routing_interface_dhcp",
        description="🌐 Get DHCP settings for a Layer 3 interface"
    )
    def get_device_switch_routing_interface_dhcp(
        serial: str,
        interface_id: str
    ):
        """Get DHCP settings for a Layer 3 interface."""
        try:
            dhcp = meraki_client.dashboard.switch.getDeviceSwitchRoutingInterfaceDhcp(
                serial,
                interface_id
            )
            
            result = f"# 🌐 DHCP Settings for Interface {interface_id}\n\n"
            
            # DHCP mode
            result += f"**DHCP Mode**: {dhcp.get('dhcpMode', 'N/A')}\n"
            
            if dhcp.get('dhcpMode') == 'dhcpServer':
                # DHCP lease time
                if dhcp.get('dhcpLeaseTime'):
                    result += f"**Lease Time**: {dhcp['dhcpLeaseTime']}\n"
                    
                # DNS servers
                if dhcp.get('dnsNameserversOption'):
                    result += f"**DNS Option**: {dhcp['dnsNameserversOption']}\n"
                    
                if dhcp.get('dnsCustomNameservers'):
                    result += f"**Custom DNS Servers**: {', '.join(dhcp['dnsCustomNameservers'])}\n"
                    
                # Boot options
                if dhcp.get('bootOptionsEnabled'):
                    result += f"**Boot Options**: ✅ Enabled\n"
                    if dhcp.get('bootNextServer'):
                        result += f"  - Next Server: {dhcp['bootNextServer']}\n"
                    if dhcp.get('bootFileName'):
                        result += f"  - Boot File: {dhcp['bootFileName']}\n"
                        
                # DHCP options
                if dhcp.get('dhcpOptions'):
                    result += f"\n## DHCP Options\n"
                    for option in dhcp['dhcpOptions']:
                        result += f"- **Code {option.get('code')}**: {option.get('type')} - {option.get('value')}\n"
                        
                # Reserved IP ranges
                if dhcp.get('reservedIpRanges'):
                    result += f"\n## Reserved IP Ranges\n"
                    for range_info in dhcp['reservedIpRanges']:
                        result += f"- {range_info.get('start')} to {range_info.get('end')} ({range_info.get('comment', 'No comment')})\n"
                        
                # Fixed IP assignments
                if dhcp.get('fixedIpAssignments'):
                    result += f"\n## Fixed IP Assignments\n"
                    for mac, assignment in dhcp['fixedIpAssignments'].items():
                        result += f"- **{mac}**: {assignment.get('ip')} ({assignment.get('name', 'No name')})\n"
                        
            elif dhcp.get('dhcpMode') == 'dhcpRelay':
                # DHCP relay servers
                if dhcp.get('dhcpRelayServerIps'):
                    result += f"**DHCP Relay Servers**: {', '.join(dhcp['dhcpRelayServerIps'])}\n"
                    
            return result
            
        except Exception as e:
            return f"Error retrieving DHCP settings: {str(e)}"
    
    @app.tool(
        name="update_device_switch_routing_interface_dhcp",
        description="🌐 Update DHCP settings for a Layer 3 interface"
    )
    def update_device_switch_routing_interface_dhcp(
        serial: str,
        interface_id: str,
        dhcp_mode: Optional[str] = None,
        dhcp_lease_time: Optional[str] = None,
        dns_nameservers_option: Optional[str] = None,
        dns_custom_nameservers: Optional[List[str]] = None,
        boot_options_enabled: Optional[bool] = None,
        boot_next_server: Optional[str] = None,
        boot_file_name: Optional[str] = None,
        dhcp_options: Optional[List[Dict[str, Any]]] = None,
        reserved_ip_ranges: Optional[List[Dict[str, str]]] = None,
        fixed_ip_assignments: Optional[Dict[str, Dict[str, str]]] = None,
        dhcp_relay_server_ips: Optional[List[str]] = None
    ):
        """Update DHCP settings for a Layer 3 interface."""
        try:
            kwargs = {}
            if dhcp_mode is not None:
                kwargs['dhcpMode'] = dhcp_mode
            if dhcp_lease_time is not None:
                kwargs['dhcpLeaseTime'] = dhcp_lease_time
            if dns_nameservers_option is not None:
                kwargs['dnsNameserversOption'] = dns_nameservers_option
            if dns_custom_nameservers is not None:
                kwargs['dnsCustomNameservers'] = dns_custom_nameservers
            if boot_options_enabled is not None:
                kwargs['bootOptionsEnabled'] = boot_options_enabled
            if boot_next_server is not None:
                kwargs['bootNextServer'] = boot_next_server
            if boot_file_name is not None:
                kwargs['bootFileName'] = boot_file_name
            if dhcp_options is not None:
                kwargs['dhcpOptions'] = dhcp_options
            if reserved_ip_ranges is not None:
                kwargs['reservedIpRanges'] = reserved_ip_ranges
            if fixed_ip_assignments is not None:
                kwargs['fixedIpAssignments'] = fixed_ip_assignments
            if dhcp_relay_server_ips is not None:
                kwargs['dhcpRelayServerIps'] = dhcp_relay_server_ips
                
            dhcp = meraki_client.dashboard.switch.updateDeviceSwitchRoutingInterfaceDhcp(
                serial,
                interface_id,
                **kwargs
            )
            
            return f"✅ DHCP settings updated successfully!"
            
        except Exception as e:
            return f"Error updating DHCP settings: {str(e)}"
    
    # ========== Warm Spare ==========
    
    @app.tool(
        name="get_device_switch_warm_spare",
        description="🔄 Get warm spare configuration"
    )
    def get_device_switch_warm_spare(serial: str):
        """Get warm spare configuration for a switch."""
        try:
            spare = meraki_client.dashboard.switch.getDeviceSwitchWarmSpare(serial)
            
            result = f"# 🔄 Warm Spare Configuration for Switch {serial}\n\n"
            
            result += f"**Enabled**: {'✅' if spare.get('enabled') else '❌'}\n"
            
            if spare.get('primarySerial'):
                result += f"**Primary Serial**: {spare['primarySerial']}\n"
                
            if spare.get('spareSerial'):
                result += f"**Spare Serial**: {spare['spareSerial']}\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving warm spare configuration: {str(e)}"
    
    @app.tool(
        name="update_device_switch_warm_spare",
        description="🔄 Update warm spare configuration"
    )
    def update_device_switch_warm_spare(
        serial: str,
        enabled: bool,
        spare_serial: Optional[str] = None
    ):
        """Update warm spare configuration for a switch."""
        try:
            kwargs = {'enabled': enabled}
            if spare_serial is not None:
                kwargs['spareSerial'] = spare_serial
                
            spare = meraki_client.dashboard.switch.updateDeviceSwitchWarmSpare(
                serial,
                **kwargs
            )
            
            return f"✅ Warm spare configuration updated successfully!"
            
        except Exception as e:
            return f"Error updating warm spare configuration: {str(e)}"
    
    # ========== DHCP Server Policy ==========
    
    @app.tool(
        name="get_network_switch_dhcp_server_policy",
        description="🌐 Get DHCP server policy"
    )
    def get_network_switch_dhcp_server_policy(network_id: str):
        """Get DHCP server policy settings for a network."""
        try:
            policy = meraki_client.dashboard.switch.getNetworkSwitchDhcpServerPolicy(network_id)
            
            result = f"# 🌐 DHCP Server Policy for Network {network_id}\n\n"
            
            # Alerts
            if policy.get('alerts'):
                alerts = policy['alerts']
                result += "## Alert Settings\n"
                result += f"- **Email**: {alerts.get('email', {}).get('enabled', False)}\n"
                
            # Default policy
            if policy.get('defaultPolicy'):
                result += f"\n**Default Policy**: {policy['defaultPolicy']}\n"
                
            # Allowed servers
            if policy.get('allowedServers'):
                result += f"\n## Allowed DHCP Servers\n"
                for server in policy['allowedServers']:
                    result += f"- {server}\n"
                    
            # Blocked servers
            if policy.get('blockedServers'):
                result += f"\n## Blocked DHCP Servers\n"
                for server in policy['blockedServers']:
                    result += f"- {server}\n"
                    
            # ARP inspection
            if policy.get('arpInspection'):
                arp = policy['arpInspection']
                result += f"\n## ARP Inspection\n"
                result += f"- **Enabled**: {'✅' if arp.get('enabled') else '❌'}\n"
                if arp.get('unsupportedModels'):
                    result += f"- **Unsupported Models**: {', '.join(arp['unsupportedModels'])}\n"
                    
            return result
            
        except Exception as e:
            return f"Error retrieving DHCP server policy: {str(e)}"
    
    @app.tool(
        name="update_network_switch_dhcp_server_policy",
        description="🌐 Update DHCP server policy"
    )
    def update_network_switch_dhcp_server_policy(
        network_id: str,
        default_policy: Optional[str] = None,
        allowed_servers: Optional[List[str]] = None,
        blocked_servers: Optional[List[str]] = None,
        arp_inspection_enabled: Optional[bool] = None
    ):
        """Update DHCP server policy settings."""
        try:
            kwargs = {}
            if default_policy is not None:
                kwargs['defaultPolicy'] = default_policy
            if allowed_servers is not None:
                kwargs['allowedServers'] = allowed_servers
            if blocked_servers is not None:
                kwargs['blockedServers'] = blocked_servers
            if arp_inspection_enabled is not None:
                kwargs['arpInspection'] = {'enabled': arp_inspection_enabled}
                
            policy = meraki_client.dashboard.switch.updateNetworkSwitchDhcpServerPolicy(
                network_id,
                **kwargs
            )
            
            return f"✅ DHCP server policy updated successfully!"
            
        except Exception as e:
            return f"Error updating DHCP server policy: {str(e)}"
    
    # ========== DSCP to CoS Mappings ==========
    
    @app.tool(
        name="get_network_switch_dscp_to_cos_mappings",
        description="🎯 Get DSCP to CoS mappings"
    )
    def get_network_switch_dscp_to_cos_mappings(network_id: str):
        """Get DSCP to CoS mappings for a network."""
        try:
            mappings = meraki_client.dashboard.switch.getNetworkSwitchDscpToCosMappings(network_id)
            
            result = f"# 🎯 DSCP to CoS Mappings for Network {network_id}\n\n"
            
            if mappings.get('mappings'):
                result += "## Mappings\n"
                for mapping in mappings['mappings']:
                    result += f"- **DSCP {mapping.get('dscp', 'N/A')}** → CoS {mapping.get('cos', 'N/A')}"
                    if mapping.get('title'):
                        result += f" ({mapping['title']})"
                    result += "\n"
            else:
                result += "No custom mappings configured. Using defaults.\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving DSCP to CoS mappings: {str(e)}"
    
    @app.tool(
        name="update_network_switch_dscp_to_cos_mappings",
        description="🎯 Update DSCP to CoS mappings"
    )
    def update_network_switch_dscp_to_cos_mappings(
        network_id: str,
        mappings: List[Dict[str, Any]]
    ):
        """Update DSCP to CoS mappings."""
        try:
            result = meraki_client.dashboard.switch.updateNetworkSwitchDscpToCosMappings(
                network_id,
                mappings=mappings
            )
            
            return f"✅ DSCP to CoS mappings updated successfully!"
            
        except Exception as e:
            return f"Error updating DSCP to CoS mappings: {str(e)}"
    
    # ========== MTU Configuration ==========
    
    @app.tool(
        name="get_network_switch_mtu",
        description="📏 Get MTU configuration"
    )
    def get_network_switch_mtu(network_id: str):
        """Get MTU configuration for a network."""
        try:
            mtu = meraki_client.dashboard.switch.getNetworkSwitchMtu(network_id)
            
            result = f"# 📏 MTU Configuration for Network {network_id}\n\n"
            
            if mtu.get('defaultMtuSize'):
                result += f"**Default MTU Size**: {mtu['defaultMtuSize']} bytes\n"
                
            if mtu.get('overrides'):
                result += f"\n## MTU Overrides\n"
                for override in mtu['overrides']:
                    result += f"- **{override.get('switches', 'Unknown')}**: {override.get('mtuSize', 'N/A')} bytes\n"
                    
            return result
            
        except Exception as e:
            return f"Error retrieving MTU configuration: {str(e)}"
    
    @app.tool(
        name="update_network_switch_mtu",
        description="📏 Update MTU configuration"
    )
    def update_network_switch_mtu(
        network_id: str,
        default_mtu_size: Optional[int] = None,
        overrides: Optional[List[Dict[str, Any]]] = None
    ):
        """Update MTU configuration."""
        try:
            kwargs = {}
            if default_mtu_size is not None:
                kwargs['defaultMtuSize'] = default_mtu_size
            if overrides is not None:
                kwargs['overrides'] = overrides
                
            mtu = meraki_client.dashboard.switch.updateNetworkSwitchMtu(
                network_id,
                **kwargs
            )
            
            return f"✅ MTU configuration updated successfully!"
            
        except Exception as e:
            return f"Error updating MTU configuration: {str(e)}"
    
    # ========== Multicast Routing ==========
    
    @app.tool(
        name="get_network_switch_routing_multicast",
        description="📡 Get multicast routing settings"
    )
    def get_network_switch_routing_multicast(network_id: str):
        """Get multicast routing settings for a network."""
        try:
            multicast = meraki_client.dashboard.switch.getNetworkSwitchRoutingMulticast(network_id)
            
            result = f"# 📡 Multicast Routing Settings for Network {network_id}\n\n"
            
            # Default settings
            if multicast.get('defaultSettings'):
                defaults = multicast['defaultSettings']
                result += "## Default Settings\n"
                result += f"- **IGMP Snooping**: {'✅ Enabled' if defaults.get('igmpSnoopingEnabled') else '❌ Disabled'}\n"
                result += f"- **Flood Unknown Multicast**: {'✅ Enabled' if defaults.get('floodUnknownMulticastTrafficEnabled') else '❌ Disabled'}\n"
                
            # Overrides
            if multicast.get('overrides'):
                result += f"\n## Overrides\n"
                for override in multicast['overrides']:
                    result += f"\n### {override.get('switches', 'Unknown Switches')}\n"
                    result += f"- **IGMP Snooping**: {'✅ Enabled' if override.get('igmpSnoopingEnabled') else '❌ Disabled'}\n"
                    result += f"- **Flood Unknown Multicast**: {'✅ Enabled' if override.get('floodUnknownMulticastTrafficEnabled') else '❌ Disabled'}\n"
                    
            return result
            
        except Exception as e:
            return f"Error retrieving multicast routing settings: {str(e)}"
    
    @app.tool(
        name="update_network_switch_routing_multicast",
        description="📡 Update multicast routing settings"
    )
    def update_network_switch_routing_multicast(
        network_id: str,
        default_settings: Optional[Dict[str, bool]] = None,
        overrides: Optional[List[Dict[str, Any]]] = None
    ):
        """Update multicast routing settings."""
        try:
            kwargs = {}
            if default_settings is not None:
                kwargs['defaultSettings'] = default_settings
            if overrides is not None:
                kwargs['overrides'] = overrides
                
            multicast = meraki_client.dashboard.switch.updateNetworkSwitchRoutingMulticast(
                network_id,
                **kwargs
            )
            
            return f"✅ Multicast routing settings updated successfully!"
            
        except Exception as e:
            return f"Error updating multicast routing settings: {str(e)}"
    
    # ========== OSPF Routing ==========
    
    @app.tool(
        name="get_network_switch_routing_ospf",
        description="🦉 Get OSPF routing settings"
    )
    def get_network_switch_routing_ospf(network_id: str):
        """Get OSPF routing settings for a network."""
        try:
            ospf = meraki_client.dashboard.switch.getNetworkSwitchRoutingOspf(network_id)
            
            result = f"# 🦉 OSPF Routing Settings for Network {network_id}\n\n"
            
            result += f"**Enabled**: {'✅' if ospf.get('enabled') else '❌'}\n"
            
            if ospf.get('helloTimerInSeconds'):
                result += f"**Hello Timer**: {ospf['helloTimerInSeconds']} seconds\n"
                
            if ospf.get('deadTimerInSeconds'):
                result += f"**Dead Timer**: {ospf['deadTimerInSeconds']} seconds\n"
                
            if ospf.get('areas'):
                result += f"\n## OSPF Areas\n"
                for area in ospf['areas']:
                    result += f"- **Area {area.get('areaId', 'N/A')}**: {area.get('areaName', 'Unnamed')}\n"
                    result += f"  Type: {area.get('areaType', 'N/A')}\n"
                    
            if ospf.get('v3'):
                v3 = ospf['v3']
                result += f"\n## OSPFv3 Settings\n"
                result += f"- **Enabled**: {'✅' if v3.get('enabled') else '❌'}\n"
                if v3.get('helloTimerInSeconds'):
                    result += f"- **Hello Timer**: {v3['helloTimerInSeconds']} seconds\n"
                if v3.get('deadTimerInSeconds'):
                    result += f"- **Dead Timer**: {v3['deadTimerInSeconds']} seconds\n"
                if v3.get('areas'):
                    result += "- **Areas**:\n"
                    for area in v3['areas']:
                        result += f"  - Area {area.get('areaId', 'N/A')}: {area.get('areaName', 'Unnamed')}\n"
                        
            if ospf.get('md5AuthenticationEnabled'):
                result += f"\n**MD5 Authentication**: ✅ Enabled\n"
                if ospf.get('md5AuthenticationKey'):
                    result += f"- **Key ID**: {ospf['md5AuthenticationKey'].get('id', 'N/A')}\n"
                    
            return result
            
        except Exception as e:
            return f"Error retrieving OSPF settings: {str(e)}"
    
    @app.tool(
        name="update_network_switch_routing_ospf",
        description="🦉 Update OSPF routing settings"
    )
    def update_network_switch_routing_ospf(
        network_id: str,
        enabled: Optional[bool] = None,
        hello_timer_in_seconds: Optional[int] = None,
        dead_timer_in_seconds: Optional[int] = None,
        areas: Optional[List[Dict[str, Any]]] = None,
        v3: Optional[Dict[str, Any]] = None,
        md5_authentication_enabled: Optional[bool] = None,
        md5_authentication_key: Optional[Dict[str, Any]] = None
    ):
        """Update OSPF routing settings."""
        try:
            kwargs = {}
            if enabled is not None:
                kwargs['enabled'] = enabled
            if hello_timer_in_seconds is not None:
                kwargs['helloTimerInSeconds'] = hello_timer_in_seconds
            if dead_timer_in_seconds is not None:
                kwargs['deadTimerInSeconds'] = dead_timer_in_seconds
            if areas is not None:
                kwargs['areas'] = areas
            if v3 is not None:
                kwargs['v3'] = v3
            if md5_authentication_enabled is not None:
                kwargs['md5AuthenticationEnabled'] = md5_authentication_enabled
            if md5_authentication_key is not None:
                kwargs['md5AuthenticationKey'] = md5_authentication_key
                
            ospf = meraki_client.dashboard.switch.updateNetworkSwitchRoutingOspf(
                network_id,
                **kwargs
            )
            
            return f"✅ OSPF routing settings updated successfully!"
            
        except Exception as e:
            return f"Error updating OSPF settings: {str(e)}"
    
    # ========== ACLs ==========
    
    @app.tool(
        name="get_network_switch_access_control_lists",
        description="🚦 Get switch ACLs"
    )
    def get_network_switch_access_control_lists(network_id: str):
        """Get access control lists (ACLs) for a network."""
        try:
            acls = meraki_client.dashboard.switch.getNetworkSwitchAccessControlLists(network_id)
            
            result = f"# 🚦 Access Control Lists for Network {network_id}\n\n"
            
            if acls.get('rules'):
                for idx, rule in enumerate(acls['rules'], 1):
                    result += f"## Rule {idx}: {rule.get('comment', 'No comment')}\n"
                    result += f"- **Policy**: {rule.get('policy', 'N/A')}\n"
                    result += f"- **Protocol**: {rule.get('ipProtocol', 'any')}\n"
                    result += f"- **Source**: {rule.get('srcCidr', 'any')}\n"
                    
                    if rule.get('srcPort'):
                        result += f"- **Source Port**: {rule['srcPort']}\n"
                        
                    result += f"- **Destination**: {rule.get('dstCidr', 'any')}\n"
                    
                    if rule.get('dstPort'):
                        result += f"- **Destination Port**: {rule['dstPort']}\n"
                        
                    if rule.get('vlan'):
                        result += f"- **VLAN**: {rule['vlan']}\n"
                        
                    result += "\n"
            else:
                result += "No ACL rules configured.\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving ACLs: {str(e)}"
    
    @app.tool(
        name="update_network_switch_access_control_lists",
        description="🚦 Update switch ACLs"
    )
    def update_network_switch_access_control_lists(
        network_id: str,
        rules: List[Dict[str, Any]]
    ):
        """Update access control lists (ACLs) for a network."""
        try:
            acls = meraki_client.dashboard.switch.updateNetworkSwitchAccessControlLists(
                network_id,
                rules=rules
            )
            
            return f"✅ ACLs updated successfully! Total rules: {len(rules)}"
            
        except Exception as e:
            return f"Error updating ACLs: {str(e)}"
    
    # ========== Alternate Management Interface ==========
    
    @app.tool(
        name="get_network_switch_alternate_management_interface",
        description="🔧 Get alternate management interface"
    )
    def get_network_switch_alternate_management_interface(network_id: str):
        """Get alternate management interface settings for a network."""
        try:
            alt_mgmt = meraki_client.dashboard.switch.getNetworkSwitchAlternateManagementInterface(network_id)
            
            result = f"# 🔧 Alternate Management Interface for Network {network_id}\n\n"
            
            result += f"**Enabled**: {'✅' if alt_mgmt.get('enabled') else '❌'}\n"
            
            if alt_mgmt.get('vlanId'):
                result += f"**VLAN ID**: {alt_mgmt['vlanId']}\n"
                
            if alt_mgmt.get('protocols'):
                result += f"**Protocols**: {', '.join(alt_mgmt['protocols'])}\n"
                
            if alt_mgmt.get('switches'):
                result += f"\n## Switch Configuration\n"
                for switch in alt_mgmt['switches']:
                    result += f"- **{switch.get('serial', 'Unknown')}**\n"
                    result += f"  - Alternate Management IP: {switch.get('alternateManagementIp', 'N/A')}\n"
                    result += f"  - Subnet Mask: {switch.get('subnetMask', 'N/A')}\n"
                    result += f"  - Gateway: {switch.get('gateway', 'N/A')}\n"
                    
            return result
            
        except Exception as e:
            return f"Error retrieving alternate management interface: {str(e)}"
    
    @app.tool(
        name="update_network_switch_alternate_management_interface",
        description="🔧 Update alternate management interface"
    )
    def update_network_switch_alternate_management_interface(
        network_id: str,
        enabled: Optional[bool] = None,
        vlan_id: Optional[int] = None,
        protocols: Optional[List[str]] = None,
        switches: Optional[List[Dict[str, str]]] = None
    ):
        """Update alternate management interface settings."""
        try:
            kwargs = {}
            if enabled is not None:
                kwargs['enabled'] = enabled
            if vlan_id is not None:
                kwargs['vlanId'] = vlan_id
            if protocols is not None:
                kwargs['protocols'] = protocols
            if switches is not None:
                kwargs['switches'] = switches
                
            alt_mgmt = meraki_client.dashboard.switch.updateNetworkSwitchAlternateManagementInterface(
                network_id,
                **kwargs
            )
            
            return f"✅ Alternate management interface updated successfully!"
            
        except Exception as e:
            return f"Error updating alternate management interface: {str(e)}"
    
    # ========== DHCP V4 Servers Seen ==========
    
    @app.tool(
        name="get_network_switch_dhcp_v4_servers_seen",
        description="🌐 Get DHCP servers seen on network"
    )
    def get_network_switch_dhcp_v4_servers_seen(
        network_id: str,
        timespan: Optional[int] = 86400
    ):
        """Get DHCP servers seen on the network."""
        try:
            servers = meraki_client.dashboard.switch.getNetworkSwitchDhcpV4ServersSeen(
                network_id,
                timespan=timespan
            )
            
            result = f"# 🌐 DHCP Servers Seen on Network {network_id}\n"
            result += f"*Last {timespan // 3600} hours*\n\n"
            
            if servers:
                for server in servers:
                    result += f"## Server: {server.get('mac', 'Unknown MAC')}\n"
                    result += f"- **IPv4**: {server.get('ipv4', {}).get('address', 'N/A')}\n"
                    result += f"- **VLAN**: {server.get('vlan', 'N/A')}\n"
                    result += f"- **Interface**: {server.get('interface', 'N/A')}\n"
                    
                    if server.get('device'):
                        device = server['device']
                        result += f"- **Device**: {device.get('name', 'Unknown')} ({device.get('serial', 'N/A')})\n"
                        result += f"- **Port**: {device.get('interface', {}).get('portId', 'N/A')}\n"
                        
                    result += f"- **Last Seen**: {server.get('lastSeenAt', 'N/A')}\n"
                    result += f"- **Type**: {server.get('type', 'N/A')}\n"
                    
                    if server.get('clientsResponded'):
                        result += f"- **Clients Responded**: {server['clientsResponded']}\n"
                        
                    if server.get('isAllowed') is not None:
                        result += f"- **Status**: {'✅ Allowed' if server['isAllowed'] else '❌ Rogue'}\n"
                        
                    if server.get('isConfigured'):
                        result += f"- **Configured**: ✅ Yes\n"
                        
                    result += "\n"
            else:
                result += "No DHCP servers detected in the specified timeframe.\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving DHCP servers: {str(e)}"
    
    # ========== Stack Management ==========
    
    @app.tool(
        name="get_network_switch_stacks",
        description="📚 Get all switch stacks"
    )
    def get_network_switch_stacks(network_id: str):
        """Get all switch stacks in a network."""
        try:
            stacks = meraki_client.dashboard.switch.getNetworkSwitchStacks(network_id)
            
            if not stacks:
                return f"No switch stacks found for network {network_id}."
                
            result = f"# 📚 Switch Stacks for Network {network_id}\n\n"
            
            for stack in stacks:
                result += f"## Stack: {stack.get('name', 'Unnamed')}\n"
                result += f"- **Stack ID**: {stack.get('id', 'N/A')}\n"
                
                if stack.get('serials'):
                    result += f"- **Member Switches**: {len(stack['serials'])}\n"
                    for serial in stack['serials']:
                        result += f"  - {serial}\n"
                        
                result += "\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving switch stacks: {str(e)}"
    
    @app.tool(
        name="get_network_switch_stack",
        description="📚 Get a specific switch stack"
    )
    def get_network_switch_stack(
        network_id: str,
        switch_stack_id: str
    ):
        """Get details of a specific switch stack."""
        try:
            stack = meraki_client.dashboard.switch.getNetworkSwitchStack(
                network_id,
                switch_stack_id
            )
            
            result = f"# 📚 Switch Stack Details\n\n"
            result += f"**Name**: {stack.get('name', 'Unnamed')}\n"
            result += f"**Stack ID**: {stack.get('id', 'N/A')}\n"
            
            if stack.get('serials'):
                result += f"\n## Member Switches ({len(stack['serials'])})\n"
                for idx, serial in enumerate(stack['serials'], 1):
                    result += f"{idx}. {serial}\n"
                    
            return result
            
        except Exception as e:
            return f"Error retrieving switch stack: {str(e)}"
    
    @app.tool(
        name="create_network_switch_stack",
        description="📚 Create a new switch stack"
    )
    def create_network_switch_stack(
        network_id: str,
        name: str,
        serials: List[str]
    ):
        """Create a new switch stack."""
        try:
            stack = meraki_client.dashboard.switch.createNetworkSwitchStack(
                network_id,
                name=name,
                serials=serials
            )
            
            return f"✅ Switch stack '{name}' created successfully!\n\nStack ID: {stack.get('id', 'N/A')}\nMembers: {', '.join(serials)}"
            
        except Exception as e:
            return f"Error creating switch stack: {str(e)}"
    
    @app.tool(
        name="add_network_switch_stack",
        description="📚 Add a switch to an existing stack"
    )
    def add_network_switch_stack(
        network_id: str,
        switch_stack_id: str,
        serial: str
    ):
        """Add a switch to an existing stack."""
        try:
            stack = meraki_client.dashboard.switch.addNetworkSwitchStack(
                network_id,
                switch_stack_id,
                serial=serial
            )
            
            return f"✅ Switch {serial} added to stack successfully!"
            
        except Exception as e:
            return f"Error adding switch to stack: {str(e)}"
    
    @app.tool(
        name="remove_network_switch_stack",
        description="📚 Remove a switch from a stack"
    )
    def remove_network_switch_stack(
        network_id: str,
        switch_stack_id: str,
        serial: str
    ):
        """Remove a switch from a stack."""
        try:
            stack = meraki_client.dashboard.switch.removeNetworkSwitchStack(
                network_id,
                switch_stack_id,
                serial=serial
            )
            
            return f"✅ Switch {serial} removed from stack successfully!"
            
        except Exception as e:
            return f"Error removing switch from stack: {str(e)}"
    
    @app.tool(
        name="delete_network_switch_stack",
        description="📚 Delete a switch stack"
    )
    def delete_network_switch_stack(
        network_id: str,
        switch_stack_id: str
    ):
        """Delete a switch stack."""
        try:
            meraki_client.dashboard.switch.deleteNetworkSwitchStack(
                network_id,
                switch_stack_id
            )
            
            return f"✅ Switch stack deleted successfully!"
            
        except Exception as e:
            return f"Error deleting switch stack: {str(e)}"
    
    # ========== Stack Routing ==========
    
    @app.tool(
        name="get_network_switch_stack_routing_interfaces",
        description="🛣️ Get routing interfaces for a stack"
    )
    def get_network_switch_stack_routing_interfaces(
        network_id: str,
        switch_stack_id: str
    ):
        """Get all Layer 3 interfaces for a switch stack."""
        try:
            interfaces = meraki_client.dashboard.switch.getNetworkSwitchStackRoutingInterfaces(
                network_id,
                switch_stack_id
            )
            
            if not interfaces:
                return f"No routing interfaces found for stack {switch_stack_id}."
                
            result = f"# 🛣️ Stack Routing Interfaces\n\n"
            
            for interface in interfaces:
                result += f"## Interface: {interface.get('name', 'Unnamed')}\n"
                result += f"- **Interface ID**: {interface.get('interfaceId', 'N/A')}\n"
                result += f"- **Interface IP**: {interface.get('interfaceIp', 'N/A')}\n"
                result += f"- **Subnet**: {interface.get('subnet', 'N/A')}\n"
                result += f"- **VLAN ID**: {interface.get('vlanId', 'N/A')}\n"
                
                if interface.get('multicastRouting'):
                    result += f"- **Multicast Routing**: {interface['multicastRouting']}\n"
                    
                result += "\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving stack routing interfaces: {str(e)}"
    
    # ========== Organization-Level Switch Functions ==========
    
    @app.tool(
        name="get_organization_switch_ports_by_switch",
        description="🏢 Get all switch ports in organization"
    )
    def get_organization_switch_ports_by_switch(
        org_id: str,
        per_page: Optional[int] = 50,
        configuration_updated_after: Optional[str] = None,
        network_ids: Optional[List[str]] = None
    ):
        """Get all switch ports for an organization grouped by switch."""
        try:
            kwargs = {'perPage': per_page}
            if configuration_updated_after:
                kwargs['configurationUpdatedAfter'] = configuration_updated_after
            if network_ids:
                kwargs['networkIds'] = network_ids
                
            ports = meraki_client.dashboard.switch.getOrganizationSwitchPortsBySwitch(
                org_id,
                **kwargs
            )
            
            if not ports:
                return f"No switch ports found for organization {org_id}."
                
            result = f"# 🏢 Switch Ports by Switch for Organization {org_id}\n\n"
            
            for item in ports['items'][:10]:  # Show first 10
                result += f"## Network: {item.get('network', {}).get('name', 'Unknown')}\n"
                result += f"**Switch**: {item.get('name', 'Unknown')} ({item.get('serial', 'N/A')})\n"
                result += f"**Model**: {item.get('model', 'N/A')}\n"
                
                if item.get('ports'):
                    result += f"\n### Ports ({len(item['ports'])})\n"
                    for port in item['ports'][:5]:  # Show first 5 ports
                        result += f"- **Port {port.get('portId')}**: "
                        result += f"{port.get('name', 'Unnamed')} - "
                        result += f"{'✅ Enabled' if port.get('enabled') else '❌ Disabled'}\n"
                        if port.get('vlan'):
                            result += f"  VLAN: {port['vlan']}\n"
                            
                    if len(item['ports']) > 5:
                        result += f"  ... and {len(item['ports']) - 5} more ports\n"
                        
                result += "\n"
                
            if len(ports['items']) > 10:
                result += f"... and {len(ports['items']) - 10} more switches\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving organization switch ports: {str(e)}"
    
    @app.tool(
        name="get_organization_summary_switch_power_history",
        description="⚡ Get switch power consumption history"
    )
    def get_organization_summary_switch_power_history(
        org_id: str,
        timespan: Optional[int] = 86400
    ):
        """Get power consumption history for all switches in an organization."""
        try:
            power_history = meraki_client.dashboard.switch.getOrganizationSummarySwitchPowerHistory(
                org_id,
                timespan=timespan
            )
            
            result = f"# ⚡ Switch Power History for Organization {org_id}\n"
            result += f"*Last {timespan // 3600} hours*\n\n"
            
            if power_history:
                # Show last 10 data points
                for idx, data_point in enumerate(power_history[-10:], 1):
                    result += f"## Data Point {idx}\n"
                    result += f"- **Timestamp**: {data_point.get('ts', 'N/A')}\n"
                    result += f"- **Total Power**: {data_point.get('totals', {}).get('powerWh', 0):.2f} Wh\n"
                    result += f"- **Switch Count**: {data_point.get('totals', {}).get('count', 0)}\n"
                    
                    if data_point.get('byModel'):
                        result += "- **By Model**:\n"
                        for model, stats in data_point['byModel'].items():
                            result += f"  - {model}: {stats.get('powerWh', 0):.2f} Wh ({stats.get('count', 0)} switches)\n"
                            
                    result += "\n"
            else:
                result += "No power history data available.\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving power history: {str(e)}"
    
    @app.tool(
        name="clone_organization_switch_devices",
        description="🔄 Clone switch configuration"
    )
    def clone_organization_switch_devices(
        org_id: str,
        source_serial: str,
        target_serials: List[str]
    ):
        """Clone configuration from one switch to other switches."""
        try:
            result = meraki_client.dashboard.switch.cloneOrganizationSwitchDevices(
                org_id,
                sourceSerial=source_serial,
                targetSerials=target_serials
            )
            
            return f"✅ Configuration cloned successfully!\n\nSource: {source_serial}\nTargets: {', '.join(target_serials)}"
            
        except Exception as e:
            return f"Error cloning switch configuration: {str(e)}"