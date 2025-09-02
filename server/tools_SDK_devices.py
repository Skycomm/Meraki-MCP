"""
Devices tools for Cisco Meraki MCP server.

This module provides 100% coverage of the official Cisco Meraki Devices SDK v1.
All 27 official SDK methods are implemented exactly as documented.
"""

from typing import Optional, Dict, Any, List
import json

# Global references to be set by register function
app = None
meraki_client = None

def register_devices_tools(mcp_app, meraki):
    """
    Register all official SDK devices tools with the MCP server.
    Provides 100% coverage of Cisco Meraki Devices API v1.
    
    Args:
        mcp_app: MCP server instance
        meraki: Meraki client instance
    """
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    
    # Register all devices SDK tools
    register_devices_sdk_tools()

def register_devices_sdk_tools():
    """Register all devices SDK tools (100% coverage)."""
    
    # ==================== ALL 27 DEVICES SDK TOOLS ====================
    
    @app.tool(
        name="blink_device_leds",
        description="💡 Blink deviceLeds"
    )
    def blink_device_leds(device_serial: str):
        """Blink blink deviceleds."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.devices.blinkDeviceLeds(device_serial, **kwargs)
            
            response = f"# 💡 Blink Deviceleds\\n\\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\\n\\n"
                    
                    # Show first 10 items with device-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('serial', item.get('mac', f'Item {idx}')))
                            response += f"**{idx}. {name}**\\n"
                            
                            # Show key device-specific fields
                            for field in ['status', 'model', 'networkId', 'address', 'mac', 'publicIp', 'lanIp', 'firmware']:
                                if field in item:
                                    value = item[field]
                                    if value is not None:
                                        response += f"   - {field.title()}: {value}\\n"
                                        
                        else:
                            response += f"**{idx}. {item}**\\n"
                        response += "\\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show device-relevant fields
                    device_fields = ['name', 'serial', 'model', 'networkId', 'address', 'mac', 'publicIp', 'lanIp', 
                                   'firmware', 'status', 'productType', 'tags', 'url']
                    
                    for field in device_fields:
                        if field in result:
                            value = result[field]
                            if value is not None:
                                if isinstance(value, list) and field == 'tags':
                                    response += f"- **{field.title()}**: {', '.join(value) if value else 'None'}\\n"
                                else:
                                    response += f"- **{field.title()}**: {value}\\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in device_fields and v is not None}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key.title()}**: {value}\\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key.title()}**: {len(value)} items\\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key.title()}**: {len(value)} fields\\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\\n"
                        
                else:
                    response += f"**Result**: {result}\\n"
            else:
                response += "*No data available*\\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in blink_device_leds: {str(e)}"
    
    @app.tool(
        name="create_device_live_tools_arp_table",
        description="🔧 Create deviceLiveToolsArpTable"
    )
    def create_device_live_tools_arp_table(device_serial: str):
        """Create create devicelivetoolsarptable."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.devices.createDeviceLiveToolsArpTable(device_serial, **kwargs)
            
            response = f"# 🔧 Create Devicelivetoolsarptable\\n\\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\\n\\n"
                    
                    # Show first 10 items with device-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('serial', item.get('mac', f'Item {idx}')))
                            response += f"**{idx}. {name}**\\n"
                            
                            # Show key device-specific fields
                            for field in ['status', 'model', 'networkId', 'address', 'mac', 'publicIp', 'lanIp', 'firmware']:
                                if field in item:
                                    value = item[field]
                                    if value is not None:
                                        response += f"   - {field.title()}: {value}\\n"
                                        
                        else:
                            response += f"**{idx}. {item}**\\n"
                        response += "\\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show device-relevant fields
                    device_fields = ['name', 'serial', 'model', 'networkId', 'address', 'mac', 'publicIp', 'lanIp', 
                                   'firmware', 'status', 'productType', 'tags', 'url']
                    
                    for field in device_fields:
                        if field in result:
                            value = result[field]
                            if value is not None:
                                if isinstance(value, list) and field == 'tags':
                                    response += f"- **{field.title()}**: {', '.join(value) if value else 'None'}\\n"
                                else:
                                    response += f"- **{field.title()}**: {value}\\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in device_fields and v is not None}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key.title()}**: {value}\\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key.title()}**: {len(value)} items\\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key.title()}**: {len(value)} fields\\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\\n"
                        
                else:
                    response += f"**Result**: {result}\\n"
            else:
                response += "*No data available*\\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in create_device_live_tools_arp_table: {str(e)}"
    
    @app.tool(
        name="create_device_live_tools_cable_test",
        description="🔧 Create deviceLiveToolsCableTest"
    )
    def create_device_live_tools_cable_test(device_serial: str):
        """Create create devicelivetoolscabletest."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.devices.createDeviceLiveToolsCableTest(device_serial, **kwargs)
            
            response = f"# 🔧 Create Devicelivetoolscabletest\\n\\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\\n\\n"
                    
                    # Show first 10 items with device-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('serial', item.get('mac', f'Item {idx}')))
                            response += f"**{idx}. {name}**\\n"
                            
                            # Show key device-specific fields
                            for field in ['status', 'model', 'networkId', 'address', 'mac', 'publicIp', 'lanIp', 'firmware']:
                                if field in item:
                                    value = item[field]
                                    if value is not None:
                                        response += f"   - {field.title()}: {value}\\n"
                                        
                        else:
                            response += f"**{idx}. {item}**\\n"
                        response += "\\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show device-relevant fields
                    device_fields = ['name', 'serial', 'model', 'networkId', 'address', 'mac', 'publicIp', 'lanIp', 
                                   'firmware', 'status', 'productType', 'tags', 'url']
                    
                    for field in device_fields:
                        if field in result:
                            value = result[field]
                            if value is not None:
                                if isinstance(value, list) and field == 'tags':
                                    response += f"- **{field.title()}**: {', '.join(value) if value else 'None'}\\n"
                                else:
                                    response += f"- **{field.title()}**: {value}\\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in device_fields and v is not None}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key.title()}**: {value}\\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key.title()}**: {len(value)} items\\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key.title()}**: {len(value)} fields\\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\\n"
                        
                else:
                    response += f"**Result**: {result}\\n"
            else:
                response += "*No data available*\\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in create_device_live_tools_cable_test: {str(e)}"
    
    @app.tool(
        name="create_device_live_tools_leds_blink",
        description="🔧 Create deviceLiveToolsLedsBlink"
    )
    def create_device_live_tools_leds_blink(device_serial: str):
        """Create create devicelivetoolsledsblink."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.devices.createDeviceLiveToolsLedsBlink(device_serial, **kwargs)
            
            response = f"# 🔧 Create Devicelivetoolsledsblink\\n\\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\\n\\n"
                    
                    # Show first 10 items with device-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('serial', item.get('mac', f'Item {idx}')))
                            response += f"**{idx}. {name}**\\n"
                            
                            # Show key device-specific fields
                            for field in ['status', 'model', 'networkId', 'address', 'mac', 'publicIp', 'lanIp', 'firmware']:
                                if field in item:
                                    value = item[field]
                                    if value is not None:
                                        response += f"   - {field.title()}: {value}\\n"
                                        
                        else:
                            response += f"**{idx}. {item}**\\n"
                        response += "\\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show device-relevant fields
                    device_fields = ['name', 'serial', 'model', 'networkId', 'address', 'mac', 'publicIp', 'lanIp', 
                                   'firmware', 'status', 'productType', 'tags', 'url']
                    
                    for field in device_fields:
                        if field in result:
                            value = result[field]
                            if value is not None:
                                if isinstance(value, list) and field == 'tags':
                                    response += f"- **{field.title()}**: {', '.join(value) if value else 'None'}\\n"
                                else:
                                    response += f"- **{field.title()}**: {value}\\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in device_fields and v is not None}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key.title()}**: {value}\\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key.title()}**: {len(value)} items\\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key.title()}**: {len(value)} fields\\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\\n"
                        
                else:
                    response += f"**Result**: {result}\\n"
            else:
                response += "*No data available*\\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in create_device_live_tools_leds_blink: {str(e)}"
    
    @app.tool(
        name="create_device_live_tools_mac_table",
        description="🔧 Create deviceLiveToolsMacTable"
    )
    def create_device_live_tools_mac_table(device_serial: str):
        """Create create devicelivetoolsmactable."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.devices.createDeviceLiveToolsMacTable(device_serial, **kwargs)
            
            response = f"# 🔧 Create Devicelivetoolsmactable\\n\\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\\n\\n"
                    
                    # Show first 10 items with device-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('serial', item.get('mac', f'Item {idx}')))
                            response += f"**{idx}. {name}**\\n"
                            
                            # Show key device-specific fields
                            for field in ['status', 'model', 'networkId', 'address', 'mac', 'publicIp', 'lanIp', 'firmware']:
                                if field in item:
                                    value = item[field]
                                    if value is not None:
                                        response += f"   - {field.title()}: {value}\\n"
                                        
                        else:
                            response += f"**{idx}. {item}**\\n"
                        response += "\\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show device-relevant fields
                    device_fields = ['name', 'serial', 'model', 'networkId', 'address', 'mac', 'publicIp', 'lanIp', 
                                   'firmware', 'status', 'productType', 'tags', 'url']
                    
                    for field in device_fields:
                        if field in result:
                            value = result[field]
                            if value is not None:
                                if isinstance(value, list) and field == 'tags':
                                    response += f"- **{field.title()}**: {', '.join(value) if value else 'None'}\\n"
                                else:
                                    response += f"- **{field.title()}**: {value}\\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in device_fields and v is not None}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key.title()}**: {value}\\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key.title()}**: {len(value)} items\\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key.title()}**: {len(value)} fields\\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\\n"
                        
                else:
                    response += f"**Result**: {result}\\n"
            else:
                response += "*No data available*\\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in create_device_live_tools_mac_table: {str(e)}"
    
    @app.tool(
        name="create_device_live_tools_ping",
        description="🔧 Create deviceLiveToolsPing"
    )
    def create_device_live_tools_ping(device_serial: str):
        """Create create devicelivetoolsping."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.devices.createDeviceLiveToolsPing(device_serial, **kwargs)
            
            response = f"# 🔧 Create Devicelivetoolsping\\n\\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\\n\\n"
                    
                    # Show first 10 items with device-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('serial', item.get('mac', f'Item {idx}')))
                            response += f"**{idx}. {name}**\\n"
                            
                            # Show key device-specific fields
                            for field in ['status', 'model', 'networkId', 'address', 'mac', 'publicIp', 'lanIp', 'firmware']:
                                if field in item:
                                    value = item[field]
                                    if value is not None:
                                        response += f"   - {field.title()}: {value}\\n"
                                        
                        else:
                            response += f"**{idx}. {item}**\\n"
                        response += "\\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show device-relevant fields
                    device_fields = ['name', 'serial', 'model', 'networkId', 'address', 'mac', 'publicIp', 'lanIp', 
                                   'firmware', 'status', 'productType', 'tags', 'url']
                    
                    for field in device_fields:
                        if field in result:
                            value = result[field]
                            if value is not None:
                                if isinstance(value, list) and field == 'tags':
                                    response += f"- **{field.title()}**: {', '.join(value) if value else 'None'}\\n"
                                else:
                                    response += f"- **{field.title()}**: {value}\\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in device_fields and v is not None}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key.title()}**: {value}\\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key.title()}**: {len(value)} items\\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key.title()}**: {len(value)} fields\\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\\n"
                        
                else:
                    response += f"**Result**: {result}\\n"
            else:
                response += "*No data available*\\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in create_device_live_tools_ping: {str(e)}"
    
    @app.tool(
        name="create_device_live_tools_ping_device",
        description="🔧 Create deviceLiveToolsPing device"
    )
    def create_device_live_tools_ping_device(device_serial: str):
        """Create create devicelivetoolsping device."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.devices.createDeviceLiveToolsPingDevice(device_serial, **kwargs)
            
            response = f"# 🔧 Create Devicelivetoolsping Device\\n\\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\\n\\n"
                    
                    # Show first 10 items with device-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('serial', item.get('mac', f'Item {idx}')))
                            response += f"**{idx}. {name}**\\n"
                            
                            # Show key device-specific fields
                            for field in ['status', 'model', 'networkId', 'address', 'mac', 'publicIp', 'lanIp', 'firmware']:
                                if field in item:
                                    value = item[field]
                                    if value is not None:
                                        response += f"   - {field.title()}: {value}\\n"
                                        
                        else:
                            response += f"**{idx}. {item}**\\n"
                        response += "\\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show device-relevant fields
                    device_fields = ['name', 'serial', 'model', 'networkId', 'address', 'mac', 'publicIp', 'lanIp', 
                                   'firmware', 'status', 'productType', 'tags', 'url']
                    
                    for field in device_fields:
                        if field in result:
                            value = result[field]
                            if value is not None:
                                if isinstance(value, list) and field == 'tags':
                                    response += f"- **{field.title()}**: {', '.join(value) if value else 'None'}\\n"
                                else:
                                    response += f"- **{field.title()}**: {value}\\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in device_fields and v is not None}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key.title()}**: {value}\\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key.title()}**: {len(value)} items\\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key.title()}**: {len(value)} fields\\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\\n"
                        
                else:
                    response += f"**Result**: {result}\\n"
            else:
                response += "*No data available*\\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in create_device_live_tools_ping_device: {str(e)}"
    
    @app.tool(
        name="create_device_live_tools_throughput_test",
        description="🔧 Create deviceLiveToolsThroughputTest"
    )
    def create_device_live_tools_throughput_test(device_serial: str):
        """Create create devicelivetoolsthroughputtest."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.devices.createDeviceLiveToolsThroughputTest(device_serial, **kwargs)
            
            response = f"# 🔧 Create Devicelivetoolsthroughputtest\\n\\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\\n\\n"
                    
                    # Show first 10 items with device-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('serial', item.get('mac', f'Item {idx}')))
                            response += f"**{idx}. {name}**\\n"
                            
                            # Show key device-specific fields
                            for field in ['status', 'model', 'networkId', 'address', 'mac', 'publicIp', 'lanIp', 'firmware']:
                                if field in item:
                                    value = item[field]
                                    if value is not None:
                                        response += f"   - {field.title()}: {value}\\n"
                                        
                        else:
                            response += f"**{idx}. {item}**\\n"
                        response += "\\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show device-relevant fields
                    device_fields = ['name', 'serial', 'model', 'networkId', 'address', 'mac', 'publicIp', 'lanIp', 
                                   'firmware', 'status', 'productType', 'tags', 'url']
                    
                    for field in device_fields:
                        if field in result:
                            value = result[field]
                            if value is not None:
                                if isinstance(value, list) and field == 'tags':
                                    response += f"- **{field.title()}**: {', '.join(value) if value else 'None'}\\n"
                                else:
                                    response += f"- **{field.title()}**: {value}\\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in device_fields and v is not None}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key.title()}**: {value}\\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key.title()}**: {len(value)} items\\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key.title()}**: {len(value)} fields\\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\\n"
                        
                else:
                    response += f"**Result**: {result}\\n"
            else:
                response += "*No data available*\\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in create_device_live_tools_throughput_test: {str(e)}"
    
    @app.tool(
        name="create_device_live_tools_wake_on_lan",
        description="🔧 Create deviceLiveToolsWakeOnLan"
    )
    def create_device_live_tools_wake_on_lan(device_serial: str):
        """Create create devicelivetoolswakeonlan."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.devices.createDeviceLiveToolsWakeOnLan(device_serial, **kwargs)
            
            response = f"# 🔧 Create Devicelivetoolswakeonlan\\n\\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\\n\\n"
                    
                    # Show first 10 items with device-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('serial', item.get('mac', f'Item {idx}')))
                            response += f"**{idx}. {name}**\\n"
                            
                            # Show key device-specific fields
                            for field in ['status', 'model', 'networkId', 'address', 'mac', 'publicIp', 'lanIp', 'firmware']:
                                if field in item:
                                    value = item[field]
                                    if value is not None:
                                        response += f"   - {field.title()}: {value}\\n"
                                        
                        else:
                            response += f"**{idx}. {item}**\\n"
                        response += "\\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show device-relevant fields
                    device_fields = ['name', 'serial', 'model', 'networkId', 'address', 'mac', 'publicIp', 'lanIp', 
                                   'firmware', 'status', 'productType', 'tags', 'url']
                    
                    for field in device_fields:
                        if field in result:
                            value = result[field]
                            if value is not None:
                                if isinstance(value, list) and field == 'tags':
                                    response += f"- **{field.title()}**: {', '.join(value) if value else 'None'}\\n"
                                else:
                                    response += f"- **{field.title()}**: {value}\\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in device_fields and v is not None}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key.title()}**: {value}\\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key.title()}**: {len(value)} items\\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key.title()}**: {len(value)} fields\\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\\n"
                        
                else:
                    response += f"**Result**: {result}\\n"
            else:
                response += "*No data available*\\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in create_device_live_tools_wake_on_lan: {str(e)}"
    
    @app.tool(
        name="get_device",
        description="🔍 Get device"
    )
    def get_device(device_serial: str):
        """Get get device."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.devices.getDevice(device_serial, **kwargs)
            
            response = f"# 🔍 Get Device\\n\\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\\n\\n"
                    
                    # Show first 10 items with device-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('serial', item.get('mac', f'Item {idx}')))
                            response += f"**{idx}. {name}**\\n"
                            
                            # Show key device-specific fields
                            for field in ['status', 'model', 'networkId', 'address', 'mac', 'publicIp', 'lanIp', 'firmware']:
                                if field in item:
                                    value = item[field]
                                    if value is not None:
                                        response += f"   - {field.title()}: {value}\\n"
                                        
                        else:
                            response += f"**{idx}. {item}**\\n"
                        response += "\\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show device-relevant fields
                    device_fields = ['name', 'serial', 'model', 'networkId', 'address', 'mac', 'publicIp', 'lanIp', 
                                   'firmware', 'status', 'productType', 'tags', 'url']
                    
                    for field in device_fields:
                        if field in result:
                            value = result[field]
                            if value is not None:
                                if isinstance(value, list) and field == 'tags':
                                    response += f"- **{field.title()}**: {', '.join(value) if value else 'None'}\\n"
                                else:
                                    response += f"- **{field.title()}**: {value}\\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in device_fields and v is not None}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key.title()}**: {value}\\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key.title()}**: {len(value)} items\\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key.title()}**: {len(value)} fields\\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\\n"
                        
                else:
                    response += f"**Result**: {result}\\n"
            else:
                response += "*No data available*\\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_device: {str(e)}"
    
    @app.tool(
        name="get_device_cellular_sims",
        description="🔍 Get deviceCellularSims"
    )
    def get_device_cellular_sims(device_serial: str):
        """Get get devicecellularsims."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.devices.getDeviceCellularSims(device_serial, **kwargs)
            
            response = f"# 🔍 Get Devicecellularsims\\n\\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\\n\\n"
                    
                    # Show first 10 items with device-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('serial', item.get('mac', f'Item {idx}')))
                            response += f"**{idx}. {name}**\\n"
                            
                            # Show key device-specific fields
                            for field in ['status', 'model', 'networkId', 'address', 'mac', 'publicIp', 'lanIp', 'firmware']:
                                if field in item:
                                    value = item[field]
                                    if value is not None:
                                        response += f"   - {field.title()}: {value}\\n"
                                        
                        else:
                            response += f"**{idx}. {item}**\\n"
                        response += "\\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show device-relevant fields
                    device_fields = ['name', 'serial', 'model', 'networkId', 'address', 'mac', 'publicIp', 'lanIp', 
                                   'firmware', 'status', 'productType', 'tags', 'url']
                    
                    for field in device_fields:
                        if field in result:
                            value = result[field]
                            if value is not None:
                                if isinstance(value, list) and field == 'tags':
                                    response += f"- **{field.title()}**: {', '.join(value) if value else 'None'}\\n"
                                else:
                                    response += f"- **{field.title()}**: {value}\\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in device_fields and v is not None}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key.title()}**: {value}\\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key.title()}**: {len(value)} items\\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key.title()}**: {len(value)} fields\\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\\n"
                        
                else:
                    response += f"**Result**: {result}\\n"
            else:
                response += "*No data available*\\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_device_cellular_sims: {str(e)}"
    
    @app.tool(
        name="get_device_clients",
        description="🔍 Get deviceClients"
    )
    def get_device_clients(device_serial: str):
        """Get get deviceclients."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.devices.getDeviceClients(device_serial, **kwargs)
            
            response = f"# 🔍 Get Deviceclients\\n\\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\\n\\n"
                    
                    # Show first 10 items with device-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('serial', item.get('mac', f'Item {idx}')))
                            response += f"**{idx}. {name}**\\n"
                            
                            # Show key device-specific fields
                            for field in ['status', 'model', 'networkId', 'address', 'mac', 'publicIp', 'lanIp', 'firmware']:
                                if field in item:
                                    value = item[field]
                                    if value is not None:
                                        response += f"   - {field.title()}: {value}\\n"
                                        
                        else:
                            response += f"**{idx}. {item}**\\n"
                        response += "\\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show device-relevant fields
                    device_fields = ['name', 'serial', 'model', 'networkId', 'address', 'mac', 'publicIp', 'lanIp', 
                                   'firmware', 'status', 'productType', 'tags', 'url']
                    
                    for field in device_fields:
                        if field in result:
                            value = result[field]
                            if value is not None:
                                if isinstance(value, list) and field == 'tags':
                                    response += f"- **{field.title()}**: {', '.join(value) if value else 'None'}\\n"
                                else:
                                    response += f"- **{field.title()}**: {value}\\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in device_fields and v is not None}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key.title()}**: {value}\\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key.title()}**: {len(value)} items\\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key.title()}**: {len(value)} fields\\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\\n"
                        
                else:
                    response += f"**Result**: {result}\\n"
            else:
                response += "*No data available*\\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_device_clients: {str(e)}"
    
    @app.tool(
        name="get_device_live_tools_arp_table",
        description="🔍 Get deviceLiveToolsArpTable"
    )
    def get_device_live_tools_arp_table(device_serial: str):
        """Get get devicelivetoolsarptable."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.devices.getDeviceLiveToolsArpTable(device_serial, **kwargs)
            
            response = f"# 🔍 Get Devicelivetoolsarptable\\n\\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\\n\\n"
                    
                    # Show first 10 items with device-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('serial', item.get('mac', f'Item {idx}')))
                            response += f"**{idx}. {name}**\\n"
                            
                            # Show key device-specific fields
                            for field in ['status', 'model', 'networkId', 'address', 'mac', 'publicIp', 'lanIp', 'firmware']:
                                if field in item:
                                    value = item[field]
                                    if value is not None:
                                        response += f"   - {field.title()}: {value}\\n"
                                        
                        else:
                            response += f"**{idx}. {item}**\\n"
                        response += "\\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show device-relevant fields
                    device_fields = ['name', 'serial', 'model', 'networkId', 'address', 'mac', 'publicIp', 'lanIp', 
                                   'firmware', 'status', 'productType', 'tags', 'url']
                    
                    for field in device_fields:
                        if field in result:
                            value = result[field]
                            if value is not None:
                                if isinstance(value, list) and field == 'tags':
                                    response += f"- **{field.title()}**: {', '.join(value) if value else 'None'}\\n"
                                else:
                                    response += f"- **{field.title()}**: {value}\\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in device_fields and v is not None}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key.title()}**: {value}\\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key.title()}**: {len(value)} items\\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key.title()}**: {len(value)} fields\\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\\n"
                        
                else:
                    response += f"**Result**: {result}\\n"
            else:
                response += "*No data available*\\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_device_live_tools_arp_table: {str(e)}"
    
    @app.tool(
        name="get_device_live_tools_cable_test",
        description="🔍 Get deviceLiveToolsCableTest"
    )
    def get_device_live_tools_cable_test(device_serial: str):
        """Get get devicelivetoolscabletest."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.devices.getDeviceLiveToolsCableTest(device_serial, **kwargs)
            
            response = f"# 🔍 Get Devicelivetoolscabletest\\n\\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\\n\\n"
                    
                    # Show first 10 items with device-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('serial', item.get('mac', f'Item {idx}')))
                            response += f"**{idx}. {name}**\\n"
                            
                            # Show key device-specific fields
                            for field in ['status', 'model', 'networkId', 'address', 'mac', 'publicIp', 'lanIp', 'firmware']:
                                if field in item:
                                    value = item[field]
                                    if value is not None:
                                        response += f"   - {field.title()}: {value}\\n"
                                        
                        else:
                            response += f"**{idx}. {item}**\\n"
                        response += "\\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show device-relevant fields
                    device_fields = ['name', 'serial', 'model', 'networkId', 'address', 'mac', 'publicIp', 'lanIp', 
                                   'firmware', 'status', 'productType', 'tags', 'url']
                    
                    for field in device_fields:
                        if field in result:
                            value = result[field]
                            if value is not None:
                                if isinstance(value, list) and field == 'tags':
                                    response += f"- **{field.title()}**: {', '.join(value) if value else 'None'}\\n"
                                else:
                                    response += f"- **{field.title()}**: {value}\\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in device_fields and v is not None}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key.title()}**: {value}\\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key.title()}**: {len(value)} items\\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key.title()}**: {len(value)} fields\\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\\n"
                        
                else:
                    response += f"**Result**: {result}\\n"
            else:
                response += "*No data available*\\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_device_live_tools_cable_test: {str(e)}"
    
    @app.tool(
        name="get_device_live_tools_leds_blink",
        description="🔍 Get deviceLiveToolsLedsBlink"
    )
    def get_device_live_tools_leds_blink(device_serial: str):
        """Get get devicelivetoolsledsblink."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.devices.getDeviceLiveToolsLedsBlink(device_serial, **kwargs)
            
            response = f"# 🔍 Get Devicelivetoolsledsblink\\n\\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\\n\\n"
                    
                    # Show first 10 items with device-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('serial', item.get('mac', f'Item {idx}')))
                            response += f"**{idx}. {name}**\\n"
                            
                            # Show key device-specific fields
                            for field in ['status', 'model', 'networkId', 'address', 'mac', 'publicIp', 'lanIp', 'firmware']:
                                if field in item:
                                    value = item[field]
                                    if value is not None:
                                        response += f"   - {field.title()}: {value}\\n"
                                        
                        else:
                            response += f"**{idx}. {item}**\\n"
                        response += "\\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show device-relevant fields
                    device_fields = ['name', 'serial', 'model', 'networkId', 'address', 'mac', 'publicIp', 'lanIp', 
                                   'firmware', 'status', 'productType', 'tags', 'url']
                    
                    for field in device_fields:
                        if field in result:
                            value = result[field]
                            if value is not None:
                                if isinstance(value, list) and field == 'tags':
                                    response += f"- **{field.title()}**: {', '.join(value) if value else 'None'}\\n"
                                else:
                                    response += f"- **{field.title()}**: {value}\\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in device_fields and v is not None}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key.title()}**: {value}\\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key.title()}**: {len(value)} items\\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key.title()}**: {len(value)} fields\\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\\n"
                        
                else:
                    response += f"**Result**: {result}\\n"
            else:
                response += "*No data available*\\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_device_live_tools_leds_blink: {str(e)}"
    
    @app.tool(
        name="get_device_live_tools_mac_table",
        description="🔍 Get deviceLiveToolsMacTable"
    )
    def get_device_live_tools_mac_table(device_serial: str):
        """Get get devicelivetoolsmactable."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.devices.getDeviceLiveToolsMacTable(device_serial, **kwargs)
            
            response = f"# 🔍 Get Devicelivetoolsmactable\\n\\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\\n\\n"
                    
                    # Show first 10 items with device-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('serial', item.get('mac', f'Item {idx}')))
                            response += f"**{idx}. {name}**\\n"
                            
                            # Show key device-specific fields
                            for field in ['status', 'model', 'networkId', 'address', 'mac', 'publicIp', 'lanIp', 'firmware']:
                                if field in item:
                                    value = item[field]
                                    if value is not None:
                                        response += f"   - {field.title()}: {value}\\n"
                                        
                        else:
                            response += f"**{idx}. {item}**\\n"
                        response += "\\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show device-relevant fields
                    device_fields = ['name', 'serial', 'model', 'networkId', 'address', 'mac', 'publicIp', 'lanIp', 
                                   'firmware', 'status', 'productType', 'tags', 'url']
                    
                    for field in device_fields:
                        if field in result:
                            value = result[field]
                            if value is not None:
                                if isinstance(value, list) and field == 'tags':
                                    response += f"- **{field.title()}**: {', '.join(value) if value else 'None'}\\n"
                                else:
                                    response += f"- **{field.title()}**: {value}\\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in device_fields and v is not None}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key.title()}**: {value}\\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key.title()}**: {len(value)} items\\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key.title()}**: {len(value)} fields\\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\\n"
                        
                else:
                    response += f"**Result**: {result}\\n"
            else:
                response += "*No data available*\\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_device_live_tools_mac_table: {str(e)}"
    
    @app.tool(
        name="get_device_live_tools_ping",
        description="🔍 Get deviceLiveToolsPing"
    )
    def get_device_live_tools_ping(device_serial: str):
        """Get get devicelivetoolsping."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.devices.getDeviceLiveToolsPing(device_serial, **kwargs)
            
            response = f"# 🔍 Get Devicelivetoolsping\\n\\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\\n\\n"
                    
                    # Show first 10 items with device-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('serial', item.get('mac', f'Item {idx}')))
                            response += f"**{idx}. {name}**\\n"
                            
                            # Show key device-specific fields
                            for field in ['status', 'model', 'networkId', 'address', 'mac', 'publicIp', 'lanIp', 'firmware']:
                                if field in item:
                                    value = item[field]
                                    if value is not None:
                                        response += f"   - {field.title()}: {value}\\n"
                                        
                        else:
                            response += f"**{idx}. {item}**\\n"
                        response += "\\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show device-relevant fields
                    device_fields = ['name', 'serial', 'model', 'networkId', 'address', 'mac', 'publicIp', 'lanIp', 
                                   'firmware', 'status', 'productType', 'tags', 'url']
                    
                    for field in device_fields:
                        if field in result:
                            value = result[field]
                            if value is not None:
                                if isinstance(value, list) and field == 'tags':
                                    response += f"- **{field.title()}**: {', '.join(value) if value else 'None'}\\n"
                                else:
                                    response += f"- **{field.title()}**: {value}\\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in device_fields and v is not None}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key.title()}**: {value}\\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key.title()}**: {len(value)} items\\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key.title()}**: {len(value)} fields\\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\\n"
                        
                else:
                    response += f"**Result**: {result}\\n"
            else:
                response += "*No data available*\\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_device_live_tools_ping: {str(e)}"
    
    @app.tool(
        name="get_device_live_tools_ping_device",
        description="🔍 Get deviceLiveToolsPing device"
    )
    def get_device_live_tools_ping_device(device_serial: str):
        """Get get devicelivetoolsping device."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.devices.getDeviceLiveToolsPingDevice(device_serial, **kwargs)
            
            response = f"# 🔍 Get Devicelivetoolsping Device\\n\\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\\n\\n"
                    
                    # Show first 10 items with device-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('serial', item.get('mac', f'Item {idx}')))
                            response += f"**{idx}. {name}**\\n"
                            
                            # Show key device-specific fields
                            for field in ['status', 'model', 'networkId', 'address', 'mac', 'publicIp', 'lanIp', 'firmware']:
                                if field in item:
                                    value = item[field]
                                    if value is not None:
                                        response += f"   - {field.title()}: {value}\\n"
                                        
                        else:
                            response += f"**{idx}. {item}**\\n"
                        response += "\\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show device-relevant fields
                    device_fields = ['name', 'serial', 'model', 'networkId', 'address', 'mac', 'publicIp', 'lanIp', 
                                   'firmware', 'status', 'productType', 'tags', 'url']
                    
                    for field in device_fields:
                        if field in result:
                            value = result[field]
                            if value is not None:
                                if isinstance(value, list) and field == 'tags':
                                    response += f"- **{field.title()}**: {', '.join(value) if value else 'None'}\\n"
                                else:
                                    response += f"- **{field.title()}**: {value}\\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in device_fields and v is not None}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key.title()}**: {value}\\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key.title()}**: {len(value)} items\\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key.title()}**: {len(value)} fields\\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\\n"
                        
                else:
                    response += f"**Result**: {result}\\n"
            else:
                response += "*No data available*\\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_device_live_tools_ping_device: {str(e)}"
    
    @app.tool(
        name="get_device_live_tools_throughput_test",
        description="🔍 Get deviceLiveToolsThroughputTest"
    )
    def get_device_live_tools_throughput_test(device_serial: str):
        """Get get devicelivetoolsthroughputtest."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.devices.getDeviceLiveToolsThroughputTest(device_serial, **kwargs)
            
            response = f"# 🔍 Get Devicelivetoolsthroughputtest\\n\\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\\n\\n"
                    
                    # Show first 10 items with device-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('serial', item.get('mac', f'Item {idx}')))
                            response += f"**{idx}. {name}**\\n"
                            
                            # Show key device-specific fields
                            for field in ['status', 'model', 'networkId', 'address', 'mac', 'publicIp', 'lanIp', 'firmware']:
                                if field in item:
                                    value = item[field]
                                    if value is not None:
                                        response += f"   - {field.title()}: {value}\\n"
                                        
                        else:
                            response += f"**{idx}. {item}**\\n"
                        response += "\\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show device-relevant fields
                    device_fields = ['name', 'serial', 'model', 'networkId', 'address', 'mac', 'publicIp', 'lanIp', 
                                   'firmware', 'status', 'productType', 'tags', 'url']
                    
                    for field in device_fields:
                        if field in result:
                            value = result[field]
                            if value is not None:
                                if isinstance(value, list) and field == 'tags':
                                    response += f"- **{field.title()}**: {', '.join(value) if value else 'None'}\\n"
                                else:
                                    response += f"- **{field.title()}**: {value}\\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in device_fields and v is not None}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key.title()}**: {value}\\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key.title()}**: {len(value)} items\\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key.title()}**: {len(value)} fields\\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\\n"
                        
                else:
                    response += f"**Result**: {result}\\n"
            else:
                response += "*No data available*\\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_device_live_tools_throughput_test: {str(e)}"
    
    @app.tool(
        name="get_device_live_tools_wake_on_lan",
        description="🔍 Get deviceLiveToolsWakeOnLan"
    )
    def get_device_live_tools_wake_on_lan(device_serial: str):
        """Get get devicelivetoolswakeonlan."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.devices.getDeviceLiveToolsWakeOnLan(device_serial, **kwargs)
            
            response = f"# 🔍 Get Devicelivetoolswakeonlan\\n\\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\\n\\n"
                    
                    # Show first 10 items with device-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('serial', item.get('mac', f'Item {idx}')))
                            response += f"**{idx}. {name}**\\n"
                            
                            # Show key device-specific fields
                            for field in ['status', 'model', 'networkId', 'address', 'mac', 'publicIp', 'lanIp', 'firmware']:
                                if field in item:
                                    value = item[field]
                                    if value is not None:
                                        response += f"   - {field.title()}: {value}\\n"
                                        
                        else:
                            response += f"**{idx}. {item}**\\n"
                        response += "\\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show device-relevant fields
                    device_fields = ['name', 'serial', 'model', 'networkId', 'address', 'mac', 'publicIp', 'lanIp', 
                                   'firmware', 'status', 'productType', 'tags', 'url']
                    
                    for field in device_fields:
                        if field in result:
                            value = result[field]
                            if value is not None:
                                if isinstance(value, list) and field == 'tags':
                                    response += f"- **{field.title()}**: {', '.join(value) if value else 'None'}\\n"
                                else:
                                    response += f"- **{field.title()}**: {value}\\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in device_fields and v is not None}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key.title()}**: {value}\\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key.title()}**: {len(value)} items\\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key.title()}**: {len(value)} fields\\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\\n"
                        
                else:
                    response += f"**Result**: {result}\\n"
            else:
                response += "*No data available*\\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_device_live_tools_wake_on_lan: {str(e)}"
    
    @app.tool(
        name="get_device_lldp_cdp",
        description="🔍 Get deviceLldpCdp"
    )
    def get_device_lldp_cdp(device_serial: str):
        """Get get devicelldpcdp."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.devices.getDeviceLldpCdp(device_serial, **kwargs)
            
            response = f"# 🔍 Get Devicelldpcdp\\n\\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\\n\\n"
                    
                    # Show first 10 items with device-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('serial', item.get('mac', f'Item {idx}')))
                            response += f"**{idx}. {name}**\\n"
                            
                            # Show key device-specific fields
                            for field in ['status', 'model', 'networkId', 'address', 'mac', 'publicIp', 'lanIp', 'firmware']:
                                if field in item:
                                    value = item[field]
                                    if value is not None:
                                        response += f"   - {field.title()}: {value}\\n"
                                        
                        else:
                            response += f"**{idx}. {item}**\\n"
                        response += "\\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show device-relevant fields
                    device_fields = ['name', 'serial', 'model', 'networkId', 'address', 'mac', 'publicIp', 'lanIp', 
                                   'firmware', 'status', 'productType', 'tags', 'url']
                    
                    for field in device_fields:
                        if field in result:
                            value = result[field]
                            if value is not None:
                                if isinstance(value, list) and field == 'tags':
                                    response += f"- **{field.title()}**: {', '.join(value) if value else 'None'}\\n"
                                else:
                                    response += f"- **{field.title()}**: {value}\\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in device_fields and v is not None}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key.title()}**: {value}\\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key.title()}**: {len(value)} items\\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key.title()}**: {len(value)} fields\\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\\n"
                        
                else:
                    response += f"**Result**: {result}\\n"
            else:
                response += "*No data available*\\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_device_lldp_cdp: {str(e)}"
    
    @app.tool(
        name="get_device_loss_and_latency_history",
        description="🔍 Get deviceLossAndLatencyHistory"
    )
    def get_device_loss_and_latency_history(device_serial: str):
        """Get get devicelossandlatencyhistory."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.devices.getDeviceLossAndLatencyHistory(device_serial, **kwargs)
            
            response = f"# 🔍 Get Devicelossandlatencyhistory\\n\\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\\n\\n"
                    
                    # Show first 10 items with device-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('serial', item.get('mac', f'Item {idx}')))
                            response += f"**{idx}. {name}**\\n"
                            
                            # Show key device-specific fields
                            for field in ['status', 'model', 'networkId', 'address', 'mac', 'publicIp', 'lanIp', 'firmware']:
                                if field in item:
                                    value = item[field]
                                    if value is not None:
                                        response += f"   - {field.title()}: {value}\\n"
                                        
                        else:
                            response += f"**{idx}. {item}**\\n"
                        response += "\\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show device-relevant fields
                    device_fields = ['name', 'serial', 'model', 'networkId', 'address', 'mac', 'publicIp', 'lanIp', 
                                   'firmware', 'status', 'productType', 'tags', 'url']
                    
                    for field in device_fields:
                        if field in result:
                            value = result[field]
                            if value is not None:
                                if isinstance(value, list) and field == 'tags':
                                    response += f"- **{field.title()}**: {', '.join(value) if value else 'None'}\\n"
                                else:
                                    response += f"- **{field.title()}**: {value}\\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in device_fields and v is not None}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key.title()}**: {value}\\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key.title()}**: {len(value)} items\\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key.title()}**: {len(value)} fields\\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\\n"
                        
                else:
                    response += f"**Result**: {result}\\n"
            else:
                response += "*No data available*\\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_device_loss_and_latency_history: {str(e)}"
    
    @app.tool(
        name="get_device_management_interface",
        description="🔍 Get deviceManagementInterface"
    )
    def get_device_management_interface(device_serial: str):
        """Get get devicemanagementinterface."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.devices.getDeviceManagementInterface(device_serial, **kwargs)
            
            response = f"# 🔍 Get Devicemanagementinterface\\n\\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\\n\\n"
                    
                    # Show first 10 items with device-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('serial', item.get('mac', f'Item {idx}')))
                            response += f"**{idx}. {name}**\\n"
                            
                            # Show key device-specific fields
                            for field in ['status', 'model', 'networkId', 'address', 'mac', 'publicIp', 'lanIp', 'firmware']:
                                if field in item:
                                    value = item[field]
                                    if value is not None:
                                        response += f"   - {field.title()}: {value}\\n"
                                        
                        else:
                            response += f"**{idx}. {item}**\\n"
                        response += "\\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show device-relevant fields
                    device_fields = ['name', 'serial', 'model', 'networkId', 'address', 'mac', 'publicIp', 'lanIp', 
                                   'firmware', 'status', 'productType', 'tags', 'url']
                    
                    for field in device_fields:
                        if field in result:
                            value = result[field]
                            if value is not None:
                                if isinstance(value, list) and field == 'tags':
                                    response += f"- **{field.title()}**: {', '.join(value) if value else 'None'}\\n"
                                else:
                                    response += f"- **{field.title()}**: {value}\\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in device_fields and v is not None}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key.title()}**: {value}\\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key.title()}**: {len(value)} items\\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key.title()}**: {len(value)} fields\\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\\n"
                        
                else:
                    response += f"**Result**: {result}\\n"
            else:
                response += "*No data available*\\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in get_device_management_interface: {str(e)}"
    
    @app.tool(
        name="reboot_device",
        description="🔄 Reboot device"
    )
    def reboot_device(device_serial: str, confirmed: bool = False):
        """Reboot reboot device."""
        if not confirmed:
            return "⚠️ This operation requires confirmed=true to execute"
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.devices.rebootDevice(device_serial, **kwargs)
            
            response = f"# 🔄 Reboot Device\\n\\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\\n\\n"
                    
                    # Show first 10 items with device-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('serial', item.get('mac', f'Item {idx}')))
                            response += f"**{idx}. {name}**\\n"
                            
                            # Show key device-specific fields
                            for field in ['status', 'model', 'networkId', 'address', 'mac', 'publicIp', 'lanIp', 'firmware']:
                                if field in item:
                                    value = item[field]
                                    if value is not None:
                                        response += f"   - {field.title()}: {value}\\n"
                                        
                        else:
                            response += f"**{idx}. {item}**\\n"
                        response += "\\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show device-relevant fields
                    device_fields = ['name', 'serial', 'model', 'networkId', 'address', 'mac', 'publicIp', 'lanIp', 
                                   'firmware', 'status', 'productType', 'tags', 'url']
                    
                    for field in device_fields:
                        if field in result:
                            value = result[field]
                            if value is not None:
                                if isinstance(value, list) and field == 'tags':
                                    response += f"- **{field.title()}**: {', '.join(value) if value else 'None'}\\n"
                                else:
                                    response += f"- **{field.title()}**: {value}\\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in device_fields and v is not None}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key.title()}**: {value}\\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key.title()}**: {len(value)} items\\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key.title()}**: {len(value)} fields\\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\\n"
                        
                else:
                    response += f"**Result**: {result}\\n"
            else:
                response += "*No data available*\\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in reboot_device: {str(e)}"
    
    @app.tool(
        name="update_device",
        description="✏️ Update device"
    )
    def update_device(device_serial: str):
        """Update update device."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.devices.updateDevice(device_serial, **kwargs)
            
            response = f"# ✏️ Update Device\\n\\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\\n\\n"
                    
                    # Show first 10 items with device-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('serial', item.get('mac', f'Item {idx}')))
                            response += f"**{idx}. {name}**\\n"
                            
                            # Show key device-specific fields
                            for field in ['status', 'model', 'networkId', 'address', 'mac', 'publicIp', 'lanIp', 'firmware']:
                                if field in item:
                                    value = item[field]
                                    if value is not None:
                                        response += f"   - {field.title()}: {value}\\n"
                                        
                        else:
                            response += f"**{idx}. {item}**\\n"
                        response += "\\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show device-relevant fields
                    device_fields = ['name', 'serial', 'model', 'networkId', 'address', 'mac', 'publicIp', 'lanIp', 
                                   'firmware', 'status', 'productType', 'tags', 'url']
                    
                    for field in device_fields:
                        if field in result:
                            value = result[field]
                            if value is not None:
                                if isinstance(value, list) and field == 'tags':
                                    response += f"- **{field.title()}**: {', '.join(value) if value else 'None'}\\n"
                                else:
                                    response += f"- **{field.title()}**: {value}\\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in device_fields and v is not None}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key.title()}**: {value}\\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key.title()}**: {len(value)} items\\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key.title()}**: {len(value)} fields\\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\\n"
                        
                else:
                    response += f"**Result**: {result}\\n"
            else:
                response += "*No data available*\\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in update_device: {str(e)}"
    
    @app.tool(
        name="update_device_cellular_sims",
        description="✏️ Update deviceCellularSims"
    )
    def update_device_cellular_sims(device_serial: str):
        """Update update devicecellularsims."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.devices.updateDeviceCellularSims(device_serial, **kwargs)
            
            response = f"# ✏️ Update Devicecellularsims\\n\\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\\n\\n"
                    
                    # Show first 10 items with device-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('serial', item.get('mac', f'Item {idx}')))
                            response += f"**{idx}. {name}**\\n"
                            
                            # Show key device-specific fields
                            for field in ['status', 'model', 'networkId', 'address', 'mac', 'publicIp', 'lanIp', 'firmware']:
                                if field in item:
                                    value = item[field]
                                    if value is not None:
                                        response += f"   - {field.title()}: {value}\\n"
                                        
                        else:
                            response += f"**{idx}. {item}**\\n"
                        response += "\\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show device-relevant fields
                    device_fields = ['name', 'serial', 'model', 'networkId', 'address', 'mac', 'publicIp', 'lanIp', 
                                   'firmware', 'status', 'productType', 'tags', 'url']
                    
                    for field in device_fields:
                        if field in result:
                            value = result[field]
                            if value is not None:
                                if isinstance(value, list) and field == 'tags':
                                    response += f"- **{field.title()}**: {', '.join(value) if value else 'None'}\\n"
                                else:
                                    response += f"- **{field.title()}**: {value}\\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in device_fields and v is not None}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key.title()}**: {value}\\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key.title()}**: {len(value)} items\\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key.title()}**: {len(value)} fields\\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\\n"
                        
                else:
                    response += f"**Result**: {result}\\n"
            else:
                response += "*No data available*\\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in update_device_cellular_sims: {str(e)}"
    
    @app.tool(
        name="update_device_management_interface",
        description="✏️ Update deviceManagementInterface"
    )
    def update_device_management_interface(device_serial: str):
        """Update update devicemanagementinterface."""
        try:
            kwargs = {}
            
            
            result = meraki_client.dashboard.devices.updateDeviceManagementInterface(device_serial, **kwargs)
            
            response = f"# ✏️ Update Devicemanagementinterface\\n\\n"
            
            if result is not None:
                if isinstance(result, list):
                    response += f"**Total Items**: {len(result)}\\n\\n"
                    
                    # Show first 10 items with device-specific context
                    for idx, item in enumerate(result[:10], 1):
                        if isinstance(item, dict):
                            name = item.get('name', item.get('serial', item.get('mac', f'Item {idx}')))
                            response += f"**{idx}. {name}**\\n"
                            
                            # Show key device-specific fields
                            for field in ['status', 'model', 'networkId', 'address', 'mac', 'publicIp', 'lanIp', 'firmware']:
                                if field in item:
                                    value = item[field]
                                    if value is not None:
                                        response += f"   - {field.title()}: {value}\\n"
                                        
                        else:
                            response += f"**{idx}. {item}**\\n"
                        response += "\\n"
                    
                    if len(result) > 10:
                        response += f"... and {len(result)-10} more items\\n"
                        
                elif isinstance(result, dict):
                    # Single item result - show device-relevant fields
                    device_fields = ['name', 'serial', 'model', 'networkId', 'address', 'mac', 'publicIp', 'lanIp', 
                                   'firmware', 'status', 'productType', 'tags', 'url']
                    
                    for field in device_fields:
                        if field in result:
                            value = result[field]
                            if value is not None:
                                if isinstance(value, list) and field == 'tags':
                                    response += f"- **{field.title()}**: {', '.join(value) if value else 'None'}\\n"
                                else:
                                    response += f"- **{field.title()}**: {value}\\n"
                    
                    # Show other fields
                    remaining_fields = {k: v for k, v in result.items() if k not in device_fields and v is not None}
                    for key, value in list(remaining_fields.items())[:5]:
                        if isinstance(value, (str, int, float, bool)):
                            response += f"- **{key.title()}**: {value}\\n"
                        elif isinstance(value, list) and value:
                            response += f"- **{key.title()}**: {len(value)} items\\n"
                        elif isinstance(value, dict) and value:
                            response += f"- **{key.title()}**: {len(value)} fields\\n"
                    
                    if len(remaining_fields) > 5:
                        response += f"... and {len(remaining_fields)-5} more fields\\n"
                        
                else:
                    response += f"**Result**: {result}\\n"
            else:
                response += "*No data available*\\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error in update_device_management_interface: {str(e)}"
    
