"""
Live Tools for the Cisco Meraki MCP Server - Fixed to match official API exactly.
"""

from typing import Optional, Dict, Any

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
    
    # Register all live tool handlers
    register_live_tool_handlers()

def register_live_tool_handlers():
    """Register all live tool handlers matching official API."""
    
    # ==================== PING TOOLS ====================
    
    @app.tool(
        name="create_device_live_tools_ping",
        description="Enqueue a job to ping a target host from the device"
    )
    async def create_device_live_tools_ping(
        serial: str,
        target: str,
        count: Optional[int] = 5
    ) -> Dict[str, Any]:
        """
        Create a ping test from a device to an external target.
        Matches API: POST /devices/{serial}/liveTools/ping
        
        Args:
            serial: Device serial number
            target: Target IP or hostname to ping (e.g., "192.168.51.1")
            count: Number of pings (default 5, max 5)
            
        Returns:
            Ping test job details including pingId
        """
        try:
            result = meraki_client.dashboard.devices.createDeviceLiveToolsPing(
                serial,
                target=target,
                count=count
            )
            return result
        except Exception as e:
            return {"error": str(e)}
    
    @app.tool(
        name="get_device_live_tools_ping",
        description="Return a ping job result"
    )
    async def get_device_live_tools_ping(
        serial: str,
        id: str
    ) -> Dict[str, Any]:
        """
        Get results of a ping test.
        Matches API: GET /devices/{serial}/liveTools/ping/{id}
        
        Args:
            serial: Device serial number
            id: Ping test job ID
            
        Returns:
            Ping test results with sent/received counts, loss %, and latency
        """
        try:
            result = meraki_client.dashboard.devices.getDeviceLiveToolsPing(
                serial,
                id
            )
            return result
        except Exception as e:
            return {"error": str(e)}
    
    @app.tool(
        name="create_device_live_tools_ping_device",
        description="Enqueue a job to check connectivity status to the device"
    )
    async def create_device_live_tools_ping_device(
        serial: str
    ) -> Dict[str, Any]:
        """
        Create a ping test TO the device itself.
        Matches API: POST /devices/{serial}/liveTools/pingDevice
        
        Args:
            serial: Device serial number
            
        Returns:
            Ping device job details including id
        """
        try:
            result = meraki_client.dashboard.devices.createDeviceLiveToolsPingDevice(
                serial
            )
            return result
        except Exception as e:
            return {"error": str(e)}
    
    @app.tool(
        name="get_device_live_tools_ping_device",
        description="Return a ping device job result"
    )
    async def get_device_live_tools_ping_device(
        serial: str,
        id: str
    ) -> Dict[str, Any]:
        """
        Get results of a ping device test.
        Matches API: GET /devices/{serial}/liveTools/pingDevice/{id}
        
        Args:
            serial: Device serial number
            id: Ping device job ID
            
        Returns:
            Ping device test results
        """
        try:
            result = meraki_client.dashboard.devices.getDeviceLiveToolsPingDevice(
                serial,
                id
            )
            return result
        except Exception as e:
            return {"error": str(e)}
    
    # ==================== TRACEROUTE TOOLS ====================
    
    @app.tool(
        name="create_device_live_tools_trace_route",
        description="Enqueue a job for running traceroute from the device"
    )
    async def create_device_live_tools_trace_route(
        serial: str,
        target: str
    ) -> Dict[str, Any]:
        """
        Create a traceroute test from a device.
        Matches API: POST /devices/{serial}/liveTools/traceRoute
        
        Args:
            serial: Device serial number
            target: Target IP or hostname
            
        Returns:
            Traceroute job details including traceRouteId
        """
        try:
            result = meraki_client.dashboard.devices.createDeviceLiveToolsTraceRoute(
                serial,
                target=target
            )
            return result
        except Exception as e:
            return {"error": str(e)}
    
    @app.tool(
        name="get_device_live_tools_trace_route",
        description="Return a traceroute job result"
    )
    async def get_device_live_tools_trace_route(
        serial: str,
        id: str
    ) -> Dict[str, Any]:
        """
        Get results of a traceroute test.
        Matches API: GET /devices/{serial}/liveTools/traceRoute/{id}
        
        Args:
            serial: Device serial number
            id: Traceroute job ID
            
        Returns:
            Traceroute results with hop details
        """
        try:
            result = meraki_client.dashboard.devices.getDeviceLiveToolsTraceRoute(
                serial,
                id
            )
            return result
        except Exception as e:
            return {"error": str(e)}
    
    # ==================== CABLE TEST TOOLS ====================
    
    @app.tool(
        name="create_device_live_tools_cable_test",
        description="Enqueue a job for performing a cable test on a switch port"
    )
    async def create_device_live_tools_cable_test(
        serial: str,
        ports: list
    ) -> Dict[str, Any]:
        """
        Create a cable test for switch ports.
        Matches API: POST /devices/{serial}/liveTools/cableTest
        
        Args:
            serial: Switch serial number
            ports: List of port IDs to test (e.g., ["1", "2", "3"])
            
        Returns:
            Cable test job details including id
        """
        try:
            result = meraki_client.dashboard.devices.createDeviceLiveToolsCableTest(
                serial,
                ports=ports
            )
            return result
        except Exception as e:
            return {"error": str(e)}
    
    @app.tool(
        name="get_device_live_tools_cable_test",
        description="Return a cable test job result"
    )
    async def get_device_live_tools_cable_test(
        serial: str,
        id: str
    ) -> Dict[str, Any]:
        """
        Get results of a cable test.
        Matches API: GET /devices/{serial}/liveTools/cableTest/{id}
        
        Args:
            serial: Switch serial number
            id: Cable test job ID
            
        Returns:
            Cable test results for each port
        """
        try:
            result = meraki_client.dashboard.devices.getDeviceLiveToolsCableTest(
                serial,
                id
            )
            return result
        except Exception as e:
            return {"error": str(e)}
    
    # ==================== WAKE ON LAN ====================
    
    @app.tool(
        name="create_device_live_tools_wake_on_lan",
        description="Enqueue a job to send a Wake-on-LAN packet"
    )
    async def create_device_live_tools_wake_on_lan(
        serial: str,
        vlan_id: int,
        mac: str
    ) -> Dict[str, Any]:
        """
        Send a Wake-on-LAN packet from a device.
        Matches API: POST /devices/{serial}/liveTools/wakeOnLan
        
        Args:
            serial: Device serial number
            vlan_id: VLAN ID to send the packet on
            mac: MAC address of the target device
            
        Returns:
            Wake-on-LAN job details
        """
        try:
            result = meraki_client.dashboard.devices.createDeviceLiveToolsWakeOnLan(
                serial,
                vlanId=vlan_id,
                mac=mac
            )
            return result
        except Exception as e:
            return {"error": str(e)}
    
    @app.tool(
        name="get_device_live_tools_wake_on_lan",
        description="Return a Wake-on-LAN job result"
    )
    async def get_device_live_tools_wake_on_lan(
        serial: str,
        id: str
    ) -> Dict[str, Any]:
        """
        Get results of a Wake-on-LAN job.
        Matches API: GET /devices/{serial}/liveTools/wakeOnLan/{id}
        
        Args:
            serial: Device serial number
            id: Wake-on-LAN job ID
            
        Returns:
            Wake-on-LAN job status
        """
        try:
            result = meraki_client.dashboard.devices.getDeviceLiveToolsWakeOnLan(
                serial,
                id
            )
            return result
        except Exception as e:
            return {"error": str(e)}
    
    # ==================== THROUGHPUT TEST ====================
    
    @app.tool(
        name="create_device_live_tools_throughput_test",
        description="Enqueue a job for a throughput test from a device"
    )
    def create_device_live_tools_throughput_test(
        serial: str
    ):
        """
        Create a throughput test from a device.
        Matches API: POST /devices/{serial}/liveTools/throughputTest
        
        Args:
            serial: Device serial number
            
        Returns:
            Throughput test job details
        """
        try:
            result = meraki_client.dashboard.devices.createDeviceLiveToolsThroughputTest(
                serial
            )
            return result
        except Exception as e:
            return {"error": str(e)}
    
    @app.tool(
        name="get_device_live_tools_throughput_test",
        description="Return a throughput test job result"
    )
    def get_device_live_tools_throughput_test(
        serial: str,
        id: str
    ):
        """
        Get results of a throughput test.
        Matches API: GET /devices/{serial}/liveTools/throughputTest/{id}
        
        Args:
            serial: Device serial number
            id: Throughput test job ID
            
        Returns:
            Throughput test results with speeds
        """
        try:
            result = meraki_client.dashboard.devices.getDeviceLiveToolsThroughputTest(
                serial,
                id
            )
            return result
        except Exception as e:
            return {"error": str(e)}
    
    # ==================== ARP TABLE ====================
    
    @app.tool(
        name="create_device_live_tools_arp_table",
        description="Enqueue a job to perform an ARP table request for the device"
    )
    async def create_device_live_tools_arp_table(
        serial: str
    ) -> Dict[str, Any]:
        """
        Create an ARP table request for a device.
        Matches API: POST /devices/{serial}/liveTools/arpTable
        
        Args:
            serial: Device serial number
            
        Returns:
            ARP table job details including arpTableId
        """
        try:
            result = meraki_client.dashboard.devices.createDeviceLiveToolsArpTable(
                serial
            )
            return result
        except Exception as e:
            return {"error": str(e)}
    
    @app.tool(
        name="get_device_live_tools_arp_table",
        description="Return an ARP table job result"
    )
    async def get_device_live_tools_arp_table(
        serial: str,
        id: str
    ) -> Dict[str, Any]:
        """
        Get the ARP table job results from a device.
        Matches API: GET /devices/{serial}/liveTools/arpTable/{id}
        
        Args:
            serial: Device serial number
            id: ARP table job ID
            
        Returns:
            ARP table entries
        """
        try:
            result = meraki_client.dashboard.devices.getDeviceLiveToolsArpTable(
                serial,
                id
            )
            return result
        except Exception as e:
            return {"error": str(e)}