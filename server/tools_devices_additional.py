"""
Additional Devices endpoints for Cisco Meraki MCP Server.
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

def register_devices_additional_tools(mcp_app, meraki):
    """Register additional devices tools with the MCP server."""
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    
    # Register all additional tools
    register_devices_additional_handlers()

def register_devices_additional_handlers():
    """Register additional devices tool handlers."""

    @app.tool(
        name="create_device_live_tools_arp_table",
        description="➕ Create device live tools arp table"
    )
    def create_device_live_tools_arp_table(serial: str, **kwargs):
        """Create device live tools arp table."""
        try:
            result = meraki_client.dashboard.devices.createDeviceLiveToolsArpTable(
                serial, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Device Live Tools Arp Table")
            elif isinstance(result, list):
                return format_list_response(result, "Device Live Tools Arp Table")
            else:
                return f"✅ Create device live tools arp table completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="create_device_live_tools_cable_test",
        description="➕ Create device live tools cable test"
    )
    def create_device_live_tools_cable_test(serial: str, **kwargs):
        """Create device live tools cable test."""
        try:
            result = meraki_client.dashboard.devices.createDeviceLiveToolsCableTest(
                serial, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Device Live Tools Cable Test")
            elif isinstance(result, list):
                return format_list_response(result, "Device Live Tools Cable Test")
            else:
                return f"✅ Create device live tools cable test completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="create_device_live_tools_leds_blink",
        description="➕ Create device live tools leds blink"
    )
    def create_device_live_tools_leds_blink(serial: str, **kwargs):
        """Create device live tools leds blink."""
        try:
            result = meraki_client.dashboard.devices.createDeviceLiveToolsLedsBlink(
                serial, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Device Live Tools Leds Blink")
            elif isinstance(result, list):
                return format_list_response(result, "Device Live Tools Leds Blink")
            else:
                return f"✅ Create device live tools leds blink completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="create_device_live_tools_mac_table",
        description="➕ Create device live tools mac table"
    )
    def create_device_live_tools_mac_table(serial: str, **kwargs):
        """Create device live tools mac table."""
        try:
            result = meraki_client.dashboard.devices.createDeviceLiveToolsMacTable(
                serial, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Device Live Tools Mac Table")
            elif isinstance(result, list):
                return format_list_response(result, "Device Live Tools Mac Table")
            else:
                return f"✅ Create device live tools mac table completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="create_device_live_tools_ping",
        description="➕ Create device live tools ping"
    )
    def create_device_live_tools_ping(serial: str, **kwargs):
        """Create device live tools ping."""
        try:
            result = meraki_client.dashboard.devices.createDeviceLiveToolsPing(
                serial, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Device Live Tools Ping")
            elif isinstance(result, list):
                return format_list_response(result, "Device Live Tools Ping")
            else:
                return f"✅ Create device live tools ping completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="create_device_live_tools_ping_device",
        description="➕ Create device live tools ping device"
    )
    def create_device_live_tools_ping_device(serial: str, **kwargs):
        """Create device live tools ping device."""
        try:
            result = meraki_client.dashboard.devices.createDeviceLiveToolsPingDevice(
                serial, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Device Live Tools Ping Device")
            elif isinstance(result, list):
                return format_list_response(result, "Device Live Tools Ping Device")
            else:
                return f"✅ Create device live tools ping device completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="create_device_live_tools_throughput_test",
        description="➕ Create device live tools throughput test"
    )
    def create_device_live_tools_throughput_test(serial: str, **kwargs):
        """Create device live tools throughput test."""
        try:
            result = meraki_client.dashboard.devices.createDeviceLiveToolsThroughputTest(
                serial, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Device Live Tools Throughput Test")
            elif isinstance(result, list):
                return format_list_response(result, "Device Live Tools Throughput Test")
            else:
                return f"✅ Create device live tools throughput test completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="create_device_live_tools_wake_on_lan",
        description="➕ Create device live tools wake on lan"
    )
    def create_device_live_tools_wake_on_lan(serial: str, **kwargs):
        """Create device live tools wake on lan."""
        try:
            result = meraki_client.dashboard.devices.createDeviceLiveToolsWakeOnLan(
                serial, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Device Live Tools Wake On Lan")
            elif isinstance(result, list):
                return format_list_response(result, "Device Live Tools Wake On Lan")
            else:
                return f"✅ Create device live tools wake on lan completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_device_cellular_sims",
        description="📊 Get device cellular sims"
    )
    def get_device_cellular_sims(serial: str):
        """Get device cellular sims."""
        try:
            result = meraki_client.dashboard.devices.getDeviceCellularSims(
                serial
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Device Cellular Sims")
            elif isinstance(result, list):
                return format_list_response(result, "Device Cellular Sims")
            else:
                return f"✅ Get device cellular sims completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_device_live_tools_arp_table",
        description="📊 Get device live tools arp table"
    )
    def get_device_live_tools_arp_table(serial: str):
        """Get device live tools arp table."""
        try:
            result = meraki_client.dashboard.devices.getDeviceLiveToolsArpTable(
                serial
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Device Live Tools Arp Table")
            elif isinstance(result, list):
                return format_list_response(result, "Device Live Tools Arp Table")
            else:
                return f"✅ Get device live tools arp table completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_device_live_tools_cable_test",
        description="📊 Get device live tools cable test"
    )
    def get_device_live_tools_cable_test(serial: str):
        """Get device live tools cable test."""
        try:
            result = meraki_client.dashboard.devices.getDeviceLiveToolsCableTest(
                serial
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Device Live Tools Cable Test")
            elif isinstance(result, list):
                return format_list_response(result, "Device Live Tools Cable Test")
            else:
                return f"✅ Get device live tools cable test completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_device_live_tools_leds_blink",
        description="📊 Get device live tools leds blink"
    )
    def get_device_live_tools_leds_blink(serial: str):
        """Get device live tools leds blink."""
        try:
            result = meraki_client.dashboard.devices.getDeviceLiveToolsLedsBlink(
                serial
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Device Live Tools Leds Blink")
            elif isinstance(result, list):
                return format_list_response(result, "Device Live Tools Leds Blink")
            else:
                return f"✅ Get device live tools leds blink completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_device_live_tools_mac_table",
        description="📊 Get device live tools mac table"
    )
    def get_device_live_tools_mac_table(serial: str):
        """Get device live tools mac table."""
        try:
            result = meraki_client.dashboard.devices.getDeviceLiveToolsMacTable(
                serial
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Device Live Tools Mac Table")
            elif isinstance(result, list):
                return format_list_response(result, "Device Live Tools Mac Table")
            else:
                return f"✅ Get device live tools mac table completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_device_live_tools_ping",
        description="📊 Get device live tools ping"
    )
    def get_device_live_tools_ping(serial: str):
        """Get device live tools ping."""
        try:
            result = meraki_client.dashboard.devices.getDeviceLiveToolsPing(
                serial
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Device Live Tools Ping")
            elif isinstance(result, list):
                return format_list_response(result, "Device Live Tools Ping")
            else:
                return f"✅ Get device live tools ping completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_device_live_tools_ping_device",
        description="📊 Get device live tools ping device"
    )
    def get_device_live_tools_ping_device(serial: str):
        """Get device live tools ping device."""
        try:
            result = meraki_client.dashboard.devices.getDeviceLiveToolsPingDevice(
                serial
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Device Live Tools Ping Device")
            elif isinstance(result, list):
                return format_list_response(result, "Device Live Tools Ping Device")
            else:
                return f"✅ Get device live tools ping device completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_device_live_tools_throughput_test",
        description="📊 Get device live tools throughput test"
    )
    def get_device_live_tools_throughput_test(serial: str):
        """Get device live tools throughput test."""
        try:
            result = meraki_client.dashboard.devices.getDeviceLiveToolsThroughputTest(
                serial
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Device Live Tools Throughput Test")
            elif isinstance(result, list):
                return format_list_response(result, "Device Live Tools Throughput Test")
            else:
                return f"✅ Get device live tools throughput test completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_device_live_tools_wake_on_lan",
        description="📊 Get device live tools wake on lan"
    )
    def get_device_live_tools_wake_on_lan(serial: str):
        """Get device live tools wake on lan."""
        try:
            result = meraki_client.dashboard.devices.getDeviceLiveToolsWakeOnLan(
                serial
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Device Live Tools Wake On Lan")
            elif isinstance(result, list):
                return format_list_response(result, "Device Live Tools Wake On Lan")
            else:
                return f"✅ Get device live tools wake on lan completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_device_lldp_cdp",
        description="📊 Get LLDP/CDP neighbors - Shows what's connected to each port"
    )
    def get_device_lldp_cdp(serial: str):
        """Get LLDP/CDP information showing connected devices.
        
        CRITICAL: Check for loops where same device appears on multiple ports!
        """
        try:
            result = meraki_client.dashboard.devices.getDeviceLldpCdp(
                serial
            )
            
            # Check for loops
            loop_detected = False
            seen_devices = {}
            
            if isinstance(result, dict):
                ports_data = result.get('ports', {})
                
                # Track all connected devices
                for port_id, port_info in ports_data.items():
                    if port_info:
                        for neighbor in port_info:
                            device_id = neighbor.get('deviceId', '')
                            source_port = neighbor.get('portId', '')
                            
                            # Check if this is the same switch (loop)
                            if serial in device_id:
                                loop_detected = True
                                if not seen_devices.get('LOOP'):
                                    seen_devices['LOOP'] = []
                                seen_devices['LOOP'].append(f"Port {port_id}")
                            else:
                                # Track other devices
                                if device_id not in seen_devices:
                                    seen_devices[device_id] = []
                                seen_devices[device_id].append(f"Port {port_id}")
                
                # Format response with loop warning
                response = "# 📊 LLDP/CDP Neighbor Information\n\n"
                
                if loop_detected:
                    response += "🚨 **CRITICAL: LOOP DETECTED!**\n"
                    response += f"Ports {' and '.join(seen_devices.get('LOOP', []))} are connected to each other!\n"
                    response += "**Action Required**: Disconnect one cable immediately to prevent network issues!\n\n"
                
                response += format_dict_response(result, "Device LLDP/CDP")
                return response
                
            elif isinstance(result, list):
                return format_list_response(result, "Device LLDP/CDP")
            else:
                return f"✅ Get device LLDP/CDP completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_device_loss_and_latency_history",
        description="📊 Get device loss and latency history"
    )
    def get_device_loss_and_latency_history(serial: str, ip: str = "8.8.8.8", **kwargs):
        """Get device loss and latency history.
        
        Args:
            serial: Device serial number
            ip: Destination IP to test (default: 8.8.8.8)
            **kwargs: Additional parameters like timespan, uplink, resolution
        """
        try:
            # Add default timespan if not specified
            if 'timespan' not in kwargs and 't0' not in kwargs:
                kwargs['timespan'] = 86400  # Default to 1 day
            
            result = meraki_client.dashboard.devices.getDeviceLossAndLatencyHistory(
                serial, ip, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Device Loss And Latency History")
            elif isinstance(result, list):
                return format_list_response(result, "Device Loss And Latency History")
            else:
                return f"✅ Get device loss and latency history completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_device_management_interface",
        description="📊 Get device management interface"
    )
    def get_device_management_interface(serial: str):
        """Get device management interface."""
        try:
            result = meraki_client.dashboard.devices.getDeviceManagementInterface(
                serial
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Device Management Interface")
            elif isinstance(result, list):
                return format_list_response(result, "Device Management Interface")
            else:
                return f"✅ Get device management interface completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="update_device_cellular_sims",
        description="✏️ Update device cellular sims"
    )
    def update_device_cellular_sims(serial: str, **kwargs):
        """Update device cellular sims."""
        try:
            result = meraki_client.dashboard.devices.updateDeviceCellularSims(
                serial, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Device Cellular Sims")
            elif isinstance(result, list):
                return format_list_response(result, "Device Cellular Sims")
            else:
                return f"✅ Update device cellular sims completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="update_device_management_interface",
        description="✏️ Update device management interface"
    )
    def update_device_management_interface(serial: str, **kwargs):
        """Update device management interface."""
        try:
            result = meraki_client.dashboard.devices.updateDeviceManagementInterface(
                serial, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Device Management Interface")
            elif isinstance(result, list):
                return format_list_response(result, "Device Management Interface")
            else:
                return f"✅ Update device management interface completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"
