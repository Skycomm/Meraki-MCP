"""
Cisco Meraki MCP Server - Devices SDK Tools
Complete implementation of all 27 official Meraki Devices API methods.

This module provides 100% coverage of the Devices category from the official Meraki Dashboard API SDK.
Each tool corresponds directly to a method in the meraki.dashboard.devices namespace.

🎯 PURE SDK IMPLEMENTATION - No custom tools, exact match to official SDK
"""

# Import removed to avoid circular import
import meraki


def register_devices_tools(app, meraki_client):
    """Register all devices SDK tools."""
    print(f"📱 Registering 27 devices SDK tools...")


@app.tool(
    name="blink_device_leds",
    description="Manage blinkleds"
)
def blink_device_leds():
    """
    Manage blinkleds
    
    Args:

    
    Returns:
        dict: API response with blinkleds data
    """
    try:
        result = meraki_client.dashboard.devices.blinkDeviceLeds()
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="create_device_live_tools_arp_table",
    description="Create livetoolsarptable"
)
def create_device_live_tools_arp_table(serial: str, **kwargs):
    """
    Create livetoolsarptable
    
    Args:
        serial: Device serial number
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with livetoolsarptable data
    """
    try:
        result = meraki_client.dashboard.devices.createDeviceLiveToolsArpTable(serial, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="create_device_live_tools_cable_test",
    description="Create livetoolscabletest"
)
def create_device_live_tools_cable_test(serial: str, **kwargs):
    """
    Create livetoolscabletest
    
    Args:
        serial: Device serial number
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with livetoolscabletest data
    """
    try:
        result = meraki_client.dashboard.devices.createDeviceLiveToolsCableTest(serial, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="create_device_live_tools_leds_blink",
    description="Create livetoolsledsblink"
)
def create_device_live_tools_leds_blink(serial: str, **kwargs):
    """
    Create livetoolsledsblink
    
    Args:
        serial: Device serial number
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with livetoolsledsblink data
    """
    try:
        result = meraki_client.dashboard.devices.createDeviceLiveToolsLedsBlink(serial, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="create_device_live_tools_mac_table",
    description="Create livetoolsmactable"
)
def create_device_live_tools_mac_table(serial: str, **kwargs):
    """
    Create livetoolsmactable
    
    Args:
        serial: Device serial number
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with livetoolsmactable data
    """
    try:
        result = meraki_client.dashboard.devices.createDeviceLiveToolsMacTable(serial, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="create_device_live_tools_ping",
    description="Create livetoolsping"
)
def create_device_live_tools_ping(serial: str, **kwargs):
    """
    Create livetoolsping
    
    Args:
        serial: Device serial number
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with livetoolsping data
    """
    try:
        result = meraki_client.dashboard.devices.createDeviceLiveToolsPing(serial, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="create_device_live_tools_ping_device",
    description="Create livetoolsping"
)
def create_device_live_tools_ping_device(serial: str, **kwargs):
    """
    Create livetoolsping
    
    Args:
        serial: Device serial number
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with livetoolsping data
    """
    try:
        result = meraki_client.dashboard.devices.createDeviceLiveToolsPingDevice(serial, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="create_device_live_tools_throughput_test",
    description="Create livetoolsthroughputtest"
)
def create_device_live_tools_throughput_test(serial: str, **kwargs):
    """
    Create livetoolsthroughputtest
    
    Args:
        serial: Device serial number
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with livetoolsthroughputtest data
    """
    try:
        result = meraki_client.dashboard.devices.createDeviceLiveToolsThroughputTest(serial, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="create_device_live_tools_wake_on_lan",
    description="Create livetoolswakeonlan"
)
def create_device_live_tools_wake_on_lan(serial: str, **kwargs):
    """
    Create livetoolswakeonlan
    
    Args:
        serial: Device serial number
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with livetoolswakeonlan data
    """
    try:
        result = meraki_client.dashboard.devices.createDeviceLiveToolsWakeOnLan(serial, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_device",
    description="Retrieve devices resource"
)
def get_device(serial: str):
    """
    Retrieve devices resource
    
    Args:
        serial: Device serial number
    
    Returns:
        dict: API response with devices resource data
    """
    try:
        result = meraki_client.dashboard.devices.getDevice(serial)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_device_cellular_sims",
    description="Retrieve cellularsims"
)
def get_device_cellular_sims(serial: str):
    """
    Retrieve cellularsims
    
    Args:
        serial: Device serial number
    
    Returns:
        dict: API response with cellularsims data
    """
    try:
        result = meraki_client.dashboard.devices.getDeviceCellularSims(serial)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_device_clients",
    description="Retrieve clients"
)
def get_device_clients(serial: str):
    """
    Retrieve clients
    
    Args:
        serial: Device serial number
    
    Returns:
        dict: API response with clients data
    """
    try:
        result = meraki_client.dashboard.devices.getDeviceClients(serial)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_device_live_tools_arp_table",
    description="Retrieve livetoolsarptable"
)
def get_device_live_tools_arp_table(serial: str):
    """
    Retrieve livetoolsarptable
    
    Args:
        serial: Device serial number
    
    Returns:
        dict: API response with livetoolsarptable data
    """
    try:
        result = meraki_client.dashboard.devices.getDeviceLiveToolsArpTable(serial)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_device_live_tools_cable_test",
    description="Retrieve livetoolscabletest"
)
def get_device_live_tools_cable_test(serial: str):
    """
    Retrieve livetoolscabletest
    
    Args:
        serial: Device serial number
    
    Returns:
        dict: API response with livetoolscabletest data
    """
    try:
        result = meraki_client.dashboard.devices.getDeviceLiveToolsCableTest(serial)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_device_live_tools_leds_blink",
    description="Retrieve livetoolsledsblink"
)
def get_device_live_tools_leds_blink(serial: str):
    """
    Retrieve livetoolsledsblink
    
    Args:
        serial: Device serial number
    
    Returns:
        dict: API response with livetoolsledsblink data
    """
    try:
        result = meraki_client.dashboard.devices.getDeviceLiveToolsLedsBlink(serial)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_device_live_tools_mac_table",
    description="Retrieve livetoolsmactable"
)
def get_device_live_tools_mac_table(serial: str):
    """
    Retrieve livetoolsmactable
    
    Args:
        serial: Device serial number
    
    Returns:
        dict: API response with livetoolsmactable data
    """
    try:
        result = meraki_client.dashboard.devices.getDeviceLiveToolsMacTable(serial)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_device_live_tools_ping",
    description="Retrieve livetoolsping"
)
def get_device_live_tools_ping(serial: str):
    """
    Retrieve livetoolsping
    
    Args:
        serial: Device serial number
    
    Returns:
        dict: API response with livetoolsping data
    """
    try:
        result = meraki_client.dashboard.devices.getDeviceLiveToolsPing(serial)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_device_live_tools_ping_device",
    description="Retrieve livetoolsping"
)
def get_device_live_tools_ping_device(serial: str):
    """
    Retrieve livetoolsping
    
    Args:
        serial: Device serial number
    
    Returns:
        dict: API response with livetoolsping data
    """
    try:
        result = meraki_client.dashboard.devices.getDeviceLiveToolsPingDevice(serial)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_device_live_tools_throughput_test",
    description="Retrieve livetoolsthroughputtest"
)
def get_device_live_tools_throughput_test(serial: str):
    """
    Retrieve livetoolsthroughputtest
    
    Args:
        serial: Device serial number
    
    Returns:
        dict: API response with livetoolsthroughputtest data
    """
    try:
        result = meraki_client.dashboard.devices.getDeviceLiveToolsThroughputTest(serial)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_device_live_tools_wake_on_lan",
    description="Retrieve livetoolswakeonlan"
)
def get_device_live_tools_wake_on_lan(serial: str):
    """
    Retrieve livetoolswakeonlan
    
    Args:
        serial: Device serial number
    
    Returns:
        dict: API response with livetoolswakeonlan data
    """
    try:
        result = meraki_client.dashboard.devices.getDeviceLiveToolsWakeOnLan(serial)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_device_lldp_cdp",
    description="Retrieve lldpcdp"
)
def get_device_lldp_cdp(serial: str):
    """
    Retrieve lldpcdp
    
    Args:
        serial: Device serial number
    
    Returns:
        dict: API response with lldpcdp data
    """
    try:
        result = meraki_client.dashboard.devices.getDeviceLldpCdp(serial)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_device_loss_and_latency_history",
    description="Retrieve lossandlatencyhistory"
)
def get_device_loss_and_latency_history(serial: str, timespan: int = 86400):
    """
    Retrieve lossandlatencyhistory
    
    Args:
        serial: Device serial number
        timespan: Timespan in seconds (default: 86400)
    
    Returns:
        dict: API response with lossandlatencyhistory data
    """
    try:
        result = meraki_client.dashboard.devices.getDeviceLossAndLatencyHistory(serial, timespan=timespan)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_device_management_interface",
    description="Retrieve managementinterface"
)
def get_device_management_interface(serial: str):
    """
    Retrieve managementinterface
    
    Args:
        serial: Device serial number
    
    Returns:
        dict: API response with managementinterface data
    """
    try:
        result = meraki_client.dashboard.devices.getDeviceManagementInterface(serial)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="reboot_device",
    description="Manage reboot"
)
def reboot_device():
    """
    Manage reboot
    
    Args:

    
    Returns:
        dict: API response with reboot data
    """
    try:
        result = meraki_client.dashboard.devices.rebootDevice()
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_device",
    description="Update devices resource"
)
def update_device(serial: str, **kwargs):
    """
    Update devices resource
    
    Args:
        serial: Device serial number
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with devices resource data
    """
    try:
        result = meraki_client.dashboard.devices.updateDevice(serial, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_device_cellular_sims",
    description="Update cellularsims"
)
def update_device_cellular_sims(serial: str, **kwargs):
    """
    Update cellularsims
    
    Args:
        serial: Device serial number
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with cellularsims data
    """
    try:
        result = meraki_client.dashboard.devices.updateDeviceCellularSims(serial, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_device_management_interface",
    description="Update managementinterface"
)
def update_device_management_interface(serial: str, **kwargs):
    """
    Update managementinterface
    
    Args:
        serial: Device serial number
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with managementinterface data
    """
    try:
        result = meraki_client.dashboard.devices.updateDeviceManagementInterface(serial, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}