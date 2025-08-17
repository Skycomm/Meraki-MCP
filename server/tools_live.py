"""
Live Tools for the Cisco Meraki MCP Server - Beta/Early Access features.
These are new 2025 live diagnostic tools available with early API access.
"""

# Global variables to store app and meraki client
app = None
meraki_client = None

def register_live_tools(mcp_app, meraki):
    """
    Register live tools with the MCP server.
    
    Args:
        mcp_app: MCP server instance
        meraki: Meraki client instance
    """
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    
    # Register all live tools
    register_live_tool_handlers()

def register_live_tool_handlers():
    """Register all live tool handlers using ONLY REAL API methods."""
    
    @app.tool(
        name="create_device_ping_test",
        description="🏓 Run a ping test from a device (beta)"
    )
    def create_device_ping_test(serial: str, target: str, count: int = 5):
        """
        Create a ping test from a device.
        
        Args:
            serial: Device serial number
            target: Target IP or hostname to ping
            count: Number of pings (default 5, max 5)
            
        Returns:
            Ping test job details
        """
        try:
            # Ensure count doesn't exceed maximum
            if count > 5:
                count = 5
                
            result = meraki_client.create_device_live_tools_ping(
                serial,
                target=target,
                count=count
            )
            
            # Check if we got a valid response
            if not result:
                return "❌ Error: No response from API. The device may be offline or Live Tools may not be enabled."
            
            # Get the job ID - it might be 'id' or 'pingId'
            job_id = result.get('pingId') or result.get('id')
            
            if not job_id:
                return f"""❌ Error: Ping test creation failed.
                
API Response: {result}

Possible causes:
- Device is offline or unreachable
- Live Tools not enabled for this organization
- Invalid target address
- Device doesn't support Live Tools"""
            
            response = f"# 🏓 Ping Test Started Successfully\n\n"
            response += f"**Device**: {serial}\n"
            response += f"**Target**: {target}\n"
            response += f"**Count**: {count}\n"
            response += f"**Job ID**: `{job_id}`\n"
            response += f"**Status**: {result.get('status', 'Unknown')}\n\n"
            
            response += "⏳ Test in progress. Use `get_device_ping_test` with the job ID to check results.\n"
            response += f"\nExample: `get_device_ping_test serial=\"{serial}\" ping_id=\"{job_id}\"`\n"
            
            return response
            
        except Exception as e:
            return f"Error creating ping test: {str(e)}"
    
    @app.tool(
        name="get_device_ping_test",
        description="🏓 Get ping test results (beta)"
    )
    def get_device_ping_test(serial: str, ping_id: str):
        """
        Get results of a ping test.
        
        Args:
            serial: Device serial number
            ping_id: Ping test job ID
            
        Returns:
            Ping test results
        """
        try:
            result = meraki_client.get_device_live_tools_ping(serial, ping_id)
            
            response = f"# 🏓 Ping Test Results\n\n"
            response += f"**Status**: {result.get('status', 'Unknown')}\n"
            
            # Results
            results = result.get('results', {})
            if results:
                response += f"\n## Results\n"
                response += f"- **Sent**: {results.get('sent', 0)} packets\n"
                response += f"- **Received**: {results.get('received', 0)} packets\n"
                response += f"- **Loss**: {results.get('loss', {}).get('percentage', 0)}%\n"
                
                # Latency stats
                latency = results.get('latency', {})
                if latency:
                    response += f"\n## Latency\n"
                    response += f"- **Min**: {latency.get('minimum', 0)}ms\n"
                    response += f"- **Avg**: {latency.get('average', 0)}ms\n"
                    response += f"- **Max**: {latency.get('maximum', 0)}ms\n"
                
                # Individual replies
                replies = results.get('replies', [])
                if replies:
                    response += f"\n## Replies\n"
                    for i, reply in enumerate(replies[:5], 1):
                        response += f"{i}. Seq {reply.get('sequenceId')}: {reply.get('size')} bytes, {reply.get('latency')}ms\n"
                        
            return response
            
        except Exception as e:
            return f"Error getting ping test results: {str(e)}"
    
    @app.tool(
        name="create_device_throughput_test",
        description="🚀 Run throughput test between devices (beta)"
    )
    def create_device_throughput_test(serial: str, target_serial: str):
        """
        Create a throughput test between two devices.
        
        Args:
            serial: Source device serial
            target_serial: Target device serial
            
        Returns:
            Throughput test job details
        """
        try:
            result = meraki_client.create_device_live_tools_throughput_test(
                serial,
                targetSerial=target_serial
            )
            
            # Check if we got a valid response
            if not result:
                return "❌ Error: No response from API. Live Tools may not be enabled."
            
            # Get the job ID - it might be 'id' or 'throughputTestId'
            job_id = result.get('throughputTestId') or result.get('id')
            
            if not job_id:
                return f"""❌ Error: Throughput test creation failed.
                
API Response: {result}

Possible causes:
- Devices must be on the same network
- Both devices must support Live Tools
- Devices must be compatible (e.g., switch to switch, MX to MX)
- Live Tools not enabled for this organization
- One or both devices may be offline"""
            
            response = f"# 🚀 Throughput Test Started Successfully\n\n"
            response += f"**Source Device**: {serial}\n"
            response += f"**Target Device**: {target_serial}\n"
            response += f"**Job ID**: `{job_id}`\n"
            response += f"**Status**: {result.get('status', 'Unknown')}\n\n"
            
            response += "⏳ Test in progress. This may take 1-3 minutes.\n"
            response += f"\nExample: `get_device_throughput_test serial=\"{serial}\" test_id=\"{job_id}\"`\n"
            
            return response
            
        except Exception as e:
            error_msg = str(e)
            
            # Provide helpful error messages for common issues
            if "400" in error_msg:
                return f"""❌ Error: {error_msg}

Common causes:
- Devices must be on the same network
- Device types must be compatible
- Both devices must support Live Tools throughput testing"""
            elif "404" in error_msg:
                return f"""❌ Error: {error_msg}

Device not found or Live Tools not available."""
            else:
                return f"❌ Error creating throughput test: {error_msg}"
    
    @app.tool(
        name="get_device_throughput_test",
        description="🚀 Get throughput test results (beta)"
    )
    def get_device_throughput_test(serial: str, test_id: str):
        """
        Get results of a throughput test.
        
        Args:
            serial: Device serial number
            test_id: Test job ID
            
        Returns:
            Throughput test results
        """
        try:
            result = meraki_client.get_device_live_tools_throughput_test(serial, test_id)
            
            response = f"# 🚀 Throughput Test Results\n\n"
            response += f"**Status**: {result.get('status', 'Unknown')}\n"
            
            # Results
            results = result.get('results', {})
            if results:
                speeds = results.get('speeds', {})
                if speeds:
                    response += f"\n## Speed Results\n"
                    response += f"- **Download**: {speeds.get('downstream', 0)} Mbps\n"
                    response += f"- **Upload**: {speeds.get('upstream', 0)} Mbps\n"
                    
            return response
            
        except Exception as e:
            return f"Error getting throughput test results: {str(e)}"
    
    @app.tool(
        name="create_switch_cable_test",
        description="🔌 Run cable diagnostic test on switch port (beta)"
    )
    def create_switch_cable_test(serial: str, port: str):
        """
        Run cable diagnostic test on a switch port.
        
        Args:
            serial: Switch serial number
            port: Port ID (e.g., "1", "5")
            
        Returns:
            Cable test job details
        """
        try:
            result = meraki_client.create_device_live_tools_cable_test(
                serial,
                ports=[port]
            )
            
            response = f"# 🔌 Cable Test Started\n\n"
            response += f"**Switch**: {serial}\n"
            response += f"**Port**: {port}\n"
            response += f"**Job ID**: {result.get('id', 'N/A')}\n\n"
            
            response += "⏳ Testing cable. Use `get_switch_cable_test` to check results.\n"
            
            return response
            
        except Exception as e:
            return f"Error creating cable test: {str(e)}"
    
    @app.tool(
        name="get_switch_cable_test",
        description="🔌 Get cable test results (beta)"
    )
    def get_switch_cable_test(serial: str, test_id: str):
        """
        Get results of a cable test.
        
        Args:
            serial: Switch serial number
            test_id: Test job ID
            
        Returns:
            Cable test results
        """
        try:
            result = meraki_client.get_device_live_tools_cable_test(serial, test_id)
            
            response = f"# 🔌 Cable Test Results\n\n"
            response += f"**Status**: {result.get('status', 'Unknown')}\n"
            
            # Results
            results = result.get('results', {})
            if results:
                ports = results.get('ports', {})
                for port_id, port_data in ports.items():
                    response += f"\n## Port {port_id}\n"
                    response += f"- **Status**: {port_data.get('status', 'Unknown')}\n"
                    response += f"- **Speed**: {port_data.get('speedMbps', 'N/A')} Mbps\n"
                    
                    # Pairs (cable pairs)
                    pairs = port_data.get('pairs', [])
                    if pairs:
                        response += "- **Cable Pairs**:\n"
                        for pair in pairs:
                            status = pair.get('status', 'Unknown')
                            length = pair.get('lengthMeters', 'N/A')
                            icon = "✅" if status == 'ok' else "❌"
                            response += f"  - Pair {pair.get('index')}: {icon} {status} ({length}m)\n"
                            
            return response
            
        except Exception as e:
            return f"Error getting cable test results: {str(e)}"
    
    @app.tool(
        name="create_device_wake_on_lan",
        description="⏰ Send Wake-on-LAN to device (beta)"
    )
    def create_device_wake_on_lan(serial: str, vlan_id: int, mac_address: str):
        """
        Send Wake-on-LAN packet to wake up a device.
        
        Args:
            serial: Device serial to send WOL from
            vlan_id: VLAN ID
            mac_address: Target MAC address to wake
            
        Returns:
            WOL job details
        """
        try:
            result = meraki_client.create_device_live_tools_wake_on_lan(
                serial,
                vlanId=vlan_id,
                mac=mac_address
            )
            
            response = f"# ⏰ Wake-on-LAN Sent\n\n"
            response += f"**From Device**: {serial}\n"
            response += f"**Target MAC**: {mac_address}\n"
            response += f"**VLAN**: {vlan_id}\n"
            response += f"**Job ID**: {result.get('id', 'N/A')}\n\n"
            
            response += "✅ Magic packet sent to wake the device.\n"
            
            return response
            
        except Exception as e:
            return f"Error sending Wake-on-LAN: {str(e)}"
    
    @app.tool(
        name="create_switch_mac_table",
        description="📋 Get MAC address table from switch (beta)"
    )
    def create_switch_mac_table(serial: str):
        """
        Request MAC address table from a switch.
        
        Args:
            serial: Switch serial number
            
        Returns:
            MAC table job details
        """
        try:
            result = meraki_client.create_device_live_tools_mac_table(serial)
            
            response = f"# 📋 MAC Table Request Started\n\n"
            response += f"**Switch**: {serial}\n"
            response += f"**Job ID**: {result.get('id', 'N/A')}\n\n"
            
            response += "⏳ Retrieving MAC table. Use `get_switch_mac_table` to view results.\n"
            
            return response
            
        except Exception as e:
            return f"Error creating MAC table request: {str(e)}"
    
    @app.tool(
        name="get_switch_mac_table",
        description="📋 Get MAC table results (beta)"
    )
    def get_switch_mac_table(serial: str, request_id: str):
        """
        Get MAC address table results.
        
        Args:
            serial: Switch serial number
            request_id: MAC table request ID
            
        Returns:
            MAC table entries
        """
        try:
            result = meraki_client.get_device_live_tools_mac_table(serial, request_id)
            
            response = f"# 📋 MAC Address Table\n\n"
            response += f"**Status**: {result.get('status', 'Unknown')}\n"
            
            # Entries
            entries = result.get('entries', [])
            if entries:
                response += f"\n**Total Entries**: {len(entries)}\n\n"
                
                # Group by VLAN
                vlan_groups = {}
                for entry in entries:
                    vlan = entry.get('vlanId', 'Unknown')
                    if vlan not in vlan_groups:
                        vlan_groups[vlan] = []
                    vlan_groups[vlan].append(entry)
                
                for vlan, vlan_entries in sorted(vlan_groups.items()):
                    response += f"## VLAN {vlan} ({len(vlan_entries)} entries)\n"
                    
                    for entry in vlan_entries[:10]:  # Show first 10 per VLAN
                        mac = entry.get('mac', 'Unknown')
                        port = entry.get('port', 'Unknown')
                        response += f"- **{mac}** → Port {port}\n"
                    
                    if len(vlan_entries) > 10:
                        response += f"... and {len(vlan_entries) - 10} more entries\n"
                    response += "\n"
                    
            return response
            
        except Exception as e:
            return f"Error getting MAC table results: {str(e)}"
    
    @app.tool(
        name="blink_device_leds",
        description="💡 Blink device LEDs for identification (beta)"
    )
    def blink_device_leds(serial: str, duration: int = 30):
        """
        Blink device LEDs to help identify it physically.
        
        Args:
            serial: Device serial number
            duration: Duration in seconds (default 30)
            
        Returns:
            LED blink job details
        """
        try:
            result = meraki_client.create_device_live_tools_leds_blink(
                serial,
                duration=duration
            )
            
            response = f"# 💡 LED Blink Started\n\n"
            response += f"**Device**: {serial}\n"
            response += f"**Duration**: {duration} seconds\n"
            response += f"**Job ID**: {result.get('id', 'N/A')}\n\n"
            
            response += "✨ Device LEDs are now blinking to help identify it!\n"
            
            return response
            
        except Exception as e:
            return f"Error blinking LEDs: {str(e)}"