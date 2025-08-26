"""
Comprehensive Switch Port Analyzer for the Cisco Meraki MCP Server.
Enhanced diagnostics and troubleshooting tools.
"""

from typing import Optional, Dict, Any

# Global variables to store app and meraki client
app = None
meraki_client = None

def register_switch_analyzer_tools(mcp_app, meraki):
    """
    Register switch analyzer tools with the MCP server.
    
    Args:
        mcp_app: MCP server instance
        meraki: Meraki client instance
    """
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    
    @app.tool(
        name="analyze_switch_comprehensive",
        description="🔍 Comprehensive switch analysis - Detects loops, speed issues, unknown devices"
    )
    def analyze_switch_comprehensive(
        serial: str,
        include_cable_test: bool = False,
        identify_unknown_devices: bool = True
    ):
        """
        Perform comprehensive switch analysis including:
        - Loop detection
        - Speed/duplex issues
        - Unknown device identification
        - Cable quality problems
        - Port utilization
        - Error detection
        """
        try:
            result = f"# 🔍 Comprehensive Switch Analysis\n"
            result += f"**Switch Serial**: {serial}\n\n"
            
            # Track all issues found
            critical_issues = []
            warnings = []
            recommendations = []
            
            # 1. Get port statuses
            result += "## 1. Port Status Analysis\n"
            try:
                statuses = meraki_client.dashboard.switch.getDeviceSwitchPortsStatuses(serial, timespan=300)
                
                speed_issues = []
                potential_loops = []
                unknown_devices = []
                
                for port_status in statuses:
                    port_id = port_status.get('portId', 'Unknown')
                    status = port_status.get('status', 'Unknown')
                    
                    if status == 'Connected':
                        # Check speed issues
                        speed = port_status.get('speed', 0)
                        if speed == 100:
                            speed_issues.append({'port': port_id, 'speed': speed})
                        elif speed == 10:
                            critical_issues.append(f"Port {port_id}: Severely degraded speed (10 Mbps)")
                            
                        # Check duplex
                        if port_status.get('duplex') == 'half':
                            warnings.append(f"Port {port_id}: Half duplex detected")
                            
                        # Check for errors
                        if port_status.get('errors'):
                            warnings.append(f"Port {port_id}: Errors detected - {', '.join(port_status['errors'])}")
                            
                result += f"✅ Analyzed {len(statuses)} ports\n"
                
                if speed_issues:
                    result += f"⚠️ {len(speed_issues)} ports running below gigabit speed\n"
                    
            except Exception as e:
                result += f"❌ Error getting port statuses: {str(e)}\n"
                
            # 2. LLDP/CDP Analysis for loops and device identification
            result += "\n## 2. Device Discovery & Loop Detection\n"
            try:
                lldp_cdp = meraki_client.dashboard.devices.getDeviceLldpCdp(serial)
                
                ports_data = lldp_cdp.get('ports', {})
                seen_devices = {}
                
                for port_id, neighbors in ports_data.items():
                    if neighbors:
                        for neighbor in neighbors:
                            device_id = neighbor.get('deviceId', '')
                            system_name = neighbor.get('systemName', '')
                            
                            # Loop detection
                            if serial in device_id or serial in system_name:
                                if 'LOOP' not in seen_devices:
                                    seen_devices['LOOP'] = []
                                seen_devices['LOOP'].append(port_id)
                                critical_issues.append(f"LOOP DETECTED: Port {port_id} connected to same switch!")
                            else:
                                # Track devices
                                device_name = system_name or device_id
                                if device_name:
                                    if device_name not in seen_devices:
                                        seen_devices[device_name] = []
                                    seen_devices[device_name].append(port_id)
                                    
                result += f"✅ Found {len(seen_devices)} unique devices\n"
                
                if 'LOOP' in seen_devices:
                    result += f"🚨 CRITICAL: Loop detected on ports {', '.join(seen_devices['LOOP'])}\n"
                    
            except Exception as e:
                result += f"❌ Error getting LLDP/CDP: {str(e)}\n"
                
            # 3. Unknown Device Investigation
            if identify_unknown_devices:
                result += "\n## 3. Unknown Device Investigation\n"
                try:
                    # Get all ports
                    ports = meraki_client.dashboard.switch.getDeviceSwitchPorts(serial)
                    
                    # Get network clients
                    # First get the network ID
                    device_info = meraki_client.dashboard.devices.getDevice(serial)
                    network_id = device_info.get('networkId')
                    
                    if network_id:
                        clients = meraki_client.dashboard.networks.getNetworkClients(
                            network_id, 
                            timespan=300,
                            perPage=1000
                        )
                        
                        # Map clients to switch ports
                        for client in clients:
                            if client.get('switchport'):
                                port = client['switchport']
                                if not client.get('manufacturer') or client['manufacturer'] == 'Unknown':
                                    unknown_devices.append({
                                        'port': port,
                                        'mac': client.get('mac'),
                                        'ip': client.get('ip'),
                                        'description': client.get('description', 'Unknown')
                                    })
                                    
                        if unknown_devices:
                            result += f"⚠️ Found {len(unknown_devices)} unknown devices\n"
                            for device in unknown_devices[:5]:  # Show first 5
                                result += f"  - Port {device['port']}: {device['mac']} ({device['ip']})\n"
                        else:
                            result += "✅ All devices identified\n"
                            
                except Exception as e:
                    result += f"❌ Error investigating devices: {str(e)}\n"
                    
            # 4. Cable Test Recommendations
            if include_cable_test and speed_issues:
                result += "\n## 4. Cable Test Recommendations\n"
                result += "The following ports should have cable tests run:\n"
                for issue in speed_issues[:5]:  # Limit to first 5
                    result += f"  - Port {issue['port']}: Running at {issue['speed']} Mbps\n"
                result += "\nRun: `create_switch_cable_test(serial, port_id)` for each port\n"
                
            # 5. Port Utilization Summary
            result += "\n## 5. Port Utilization Summary\n"
            try:
                all_ports = meraki_client.dashboard.switch.getDeviceSwitchPorts(serial)
                total_ports = len(all_ports)
                enabled_ports = sum(1 for p in all_ports if p.get('enabled'))
                
                # Count connected ports from statuses
                connected_ports = sum(1 for s in statuses if s.get('status') == 'Connected')
                
                result += f"- Total Ports: {total_ports}\n"
                result += f"- Enabled: {enabled_ports}\n"
                result += f"- Connected: {connected_ports}\n"
                result += f"- Utilization: {(connected_ports/total_ports)*100:.1f}%\n"
                
                if (connected_ports/total_ports) > 0.9:
                    warnings.append("Port utilization above 90% - consider adding switches")
                    
            except Exception as e:
                result += f"❌ Error calculating utilization: {str(e)}\n"
                
            # Final Summary
            result += "\n## 📊 Analysis Summary\n\n"
            
            if critical_issues:
                result += "### 🚨 CRITICAL ISSUES\n"
                for issue in critical_issues:
                    result += f"- {issue}\n"
                result += "\n"
                
            if warnings:
                result += "### ⚠️ WARNINGS\n"
                for warning in warnings:
                    result += f"- {warning}\n"
                result += "\n"
                
            if not critical_issues and not warnings:
                result += "✅ **No issues detected** - Switch is healthy!\n"
            else:
                result += "### 💡 RECOMMENDATIONS\n"
                if 'LOOP' in seen_devices:
                    result += "1. **Immediately disconnect loop**: Unplug one cable from affected ports\n"
                if speed_issues:
                    result += "2. **Test cables**: Run cable tests on degraded ports\n"
                if unknown_devices:
                    result += "3. **Identify devices**: Investigate unknown MACs for security\n"
                    
            return result
            
        except Exception as e:
            return f"Error performing comprehensive analysis: {str(e)}"
            
    @app.tool(
        name="find_device_on_switch",
        description="🔎 Find a specific device/MAC address on the switch"
    )
    def find_device_on_switch(
        serial: str,
        search_term: str
    ):
        """
        Find a device on the switch by MAC, IP, or description.
        
        Args:
            serial: Switch serial number
            search_term: MAC address, IP address, or device description
        """
        try:
            result = f"# 🔎 Searching for '{search_term}' on switch {serial}\n\n"
            
            # Get network ID
            device_info = meraki_client.dashboard.devices.getDevice(serial)
            network_id = device_info.get('networkId')
            
            if not network_id:
                return "❌ Could not determine network ID for this switch"
                
            # Search clients
            clients = meraki_client.dashboard.networks.getNetworkClients(
                network_id,
                timespan=86400,  # Last 24 hours
                perPage=1000
            )
            
            matches = []
            search_lower = search_term.lower()
            
            for client in clients:
                # Check if this client matches search
                if (search_lower in client.get('mac', '').lower() or
                    search_lower in client.get('ip', '').lower() or
                    search_lower in client.get('description', '').lower() or
                    search_lower in client.get('manufacturer', '').lower()):
                    
                    # Check if on this switch
                    if client.get('switchport'):
                        matches.append(client)
                        
            if matches:
                result += f"Found {len(matches)} matching device(s):\n\n"
                for match in matches:
                    result += f"## {match.get('description', 'Unknown Device')}\n"
                    result += f"- **MAC**: {match.get('mac')}\n"
                    result += f"- **IP**: {match.get('ip', 'No IP')}\n"
                    result += f"- **Port**: {match.get('switchport')}\n"
                    result += f"- **VLAN**: {match.get('vlan', 'N/A')}\n"
                    result += f"- **Manufacturer**: {match.get('manufacturer', 'Unknown')}\n"
                    result += f"- **Last Seen**: {match.get('lastSeen', 'Unknown')}\n"
                    result += f"- **Status**: {match.get('status', 'Unknown')}\n\n"
                    
                # Provide action suggestions
                result += "### 📝 Suggested Actions:\n"
                result += f"1. **Blink LED**: `blink_device_leds('{serial}', 30)`\n"
                result += f"2. **Check port config**: `get_device_switch_port('{serial}', port_id)`\n"
                result += f"3. **View traffic**: `get_device_switch_port_statuses('{serial}')`\n"
            else:
                result += f"❌ No devices matching '{search_term}' found on this switch\n\n"
                result += "### 💡 Try:\n"
                result += "1. Check if the device was connected in the last 24 hours\n"
                result += "2. Use MAC address format: aa:bb:cc:dd:ee:ff\n"
                result += "3. Search on other switches in the network\n"
                
            return result
            
        except Exception as e:
            return f"Error searching for device: {str(e)}"