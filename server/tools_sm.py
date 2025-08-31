"""
Systems Manager (SM) tools for Cisco Meraki MCP server.

This module provides comprehensive mobile device management tools covering all SDK methods.
Includes device management, app control, profiles, compliance, and user management.
"""

from typing import Optional, Dict, Any, List
import json

# Global references to be set by register function
app = None
meraki_client = None

def register_sm_tools(mcp_app, meraki):
    """
    Register SM tools with the MCP server.
    
    Args:
        mcp_app: MCP server instance
        meraki: Meraki client instance
    """
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    
    # Register tool handlers
    register_sm_tool_handlers()

def register_sm_tool_handlers():
    """Register all SM tool handlers."""
    
    # ==================== DEVICE MANAGEMENT ====================
    
    @app.tool(
        name="get_network_sm_devices",
        description="📱 List all Systems Manager devices in a network. Shows mobile devices, tablets, and laptops."
    )
    def get_network_sm_devices(
        network_id: str,
        fields: Optional[str] = None,
        wifi_macs: Optional[str] = None,
        serials: Optional[str] = None,
        ids: Optional[str] = None,
        usernames: Optional[str] = None,
        emails: Optional[str] = None,
        per_page: Optional[int] = 100
    ):
        """
        Get all SM devices in a network.
        
        Args:
            network_id: Network ID
            fields: Comma-separated fields to include (reduces response size)
            wifi_macs: Filter by WiFi MAC addresses (comma-separated)
            serials: Filter by device serials (comma-separated)
            ids: Filter by device IDs (comma-separated)
            usernames: Filter by usernames (comma-separated)
            emails: Filter by user emails (comma-separated)
            per_page: Results per page (max 1000)
        """
        try:
            kwargs = {}
            if fields:
                kwargs['fields'] = [f.strip() for f in fields.split(',')]
            if wifi_macs:
                kwargs['wifiMacs'] = [m.strip() for m in wifi_macs.split(',')]
            if serials:
                kwargs['serials'] = [s.strip() for s in serials.split(',')]
            if ids:
                kwargs['ids'] = [i.strip() for i in ids.split(',')]
            if usernames:
                kwargs['usernames'] = [u.strip() for u in usernames.split(',')]
            if emails:
                kwargs['emails'] = [e.strip() for e in emails.split(',')]
            if per_page:
                kwargs['perPage'] = min(per_page, 1000)
            
            result = meraki_client.dashboard.sm.getNetworkSmDevices(network_id, **kwargs)
            
            response = f"# 📱 Systems Manager Devices\n\n"
            
            if result and isinstance(result, list):
                response += f"**Total Devices**: {len(result)}\n\n"
                
                # Group by OS
                ios_count = sum(1 for d in result if 'iOS' in d.get('osName', ''))
                android_count = sum(1 for d in result if 'Android' in d.get('osName', ''))
                windows_count = sum(1 for d in result if 'Windows' in d.get('osName', ''))
                mac_count = sum(1 for d in result if 'Mac' in d.get('osName', ''))
                
                response += f"## Device Distribution\n"
                response += f"- 🍎 **iOS**: {ios_count}\n"
                response += f"- 🤖 **Android**: {android_count}\n"
                response += f"- 🪟 **Windows**: {windows_count}\n"
                response += f"- 🖥️ **macOS**: {mac_count}\n\n"
                
                for device in result[:10]:  # Limit output
                    response += f"## {device.get('name', 'Unknown Device')}\n"
                    response += f"- **ID**: {device.get('id', 'N/A')}\n"
                    response += f"- **Serial**: {device.get('serialNumber', 'N/A')}\n"
                    response += f"- **OS**: {device.get('osName', 'N/A')}\n"
                    response += f"- **Model**: {device.get('systemModel', 'N/A')}\n"
                    response += f"- **User**: {device.get('ownerEmail', device.get('ownerUsername', 'N/A'))}\n"
                    response += f"- **WiFi MAC**: {device.get('wifiMac', 'N/A')}\n"
                    response += f"- **Last Seen**: {device.get('lastConnectAt', 'Never')}\n"
                    
                    # Compliance status
                    response += f"- **Compliant**: {'✅' if device.get('isManaged') else '❌'}\n"
                    
                    # Tags
                    tags = device.get('tags', [])
                    if tags:
                        response += f"- **Tags**: {', '.join(tags)}\n"
                    
                    response += "\n"
                
                if len(result) > 10:
                    response += f"*Showing 10 of {len(result)} devices. Use filters to narrow results.*\n"
            else:
                response += "*No SM devices found*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting SM devices: {str(e)}"
    
    @app.tool(
        name="checkin_network_sm_devices",
        description="📲 Force check-in for SM devices. Requires confirmation. Updates device status immediately."
    )
    def checkin_network_sm_devices(
        network_id: str,
        wifi_macs: Optional[str] = None,
        ids: Optional[str] = None,
        serials: Optional[str] = None,
        confirmed: bool = False
    ):
        """
        Force devices to check in.
        
        Args:
            network_id: Network ID
            wifi_macs: WiFi MACs to check in (comma-separated)
            ids: Device IDs to check in (comma-separated)
            serials: Device serials to check in (comma-separated)
            confirmed: Must be true to execute
        """
        if not confirmed:
            return "⚠️ Device check-in requires confirmed=true to execute"
        
        try:
            kwargs = {}
            if wifi_macs:
                kwargs['wifiMacs'] = [m.strip() for m in wifi_macs.split(',')]
            if ids:
                kwargs['ids'] = [i.strip() for i in ids.split(',')]
            if serials:
                kwargs['serials'] = [s.strip() for s in serials.split(',')]
            
            result = meraki_client.dashboard.sm.checkinNetworkSmDevices(network_id, **kwargs)
            
            response = f"# ✅ Device Check-in Initiated\n\n"
            
            if result:
                response += f"**Request ID**: {result.get('id', 'N/A')}\n\n"
                response += "Devices will check in within the next few minutes.\n"
            
            return response
        except Exception as e:
            return f"❌ Error initiating check-in: {str(e)}"
    
    @app.tool(
        name="update_network_sm_devices_fields",
        description="✏️ Update custom fields for SM devices. Set custom attributes and metadata."
    )
    def update_network_sm_devices_fields(
        network_id: str,
        device_fields: str,
        wifi_macs: Optional[str] = None,
        ids: Optional[str] = None,
        serials: Optional[str] = None
    ):
        """
        Update device custom fields.
        
        Args:
            network_id: Network ID
            device_fields: JSON object of fields to update (e.g. {"notes": "Test device"})
            wifi_macs: Target devices by WiFi MAC (comma-separated)
            ids: Target devices by ID (comma-separated)
            serials: Target devices by serial (comma-separated)
        """
        try:
            kwargs = {}
            kwargs['deviceFields'] = json.loads(device_fields) if isinstance(device_fields, str) else device_fields
            
            if wifi_macs:
                kwargs['wifiMacs'] = [m.strip() for m in wifi_macs.split(',')]
            if ids:
                kwargs['ids'] = [i.strip() for i in ids.split(',')]
            if serials:
                kwargs['serials'] = [s.strip() for s in serials.split(',')]
            
            result = meraki_client.dashboard.sm.updateNetworkSmDevicesFields(network_id, **kwargs)
            
            response = f"# ✅ Updated Device Fields\n\n"
            
            if result:
                updated = result.get('ids', [])
                response += f"**Devices Updated**: {len(updated)}\n\n"
                response += f"**Fields Set**: {device_fields}\n"
            
            return response
        except Exception as e:
            return f"❌ Error updating fields: {str(e)}"
    
    @app.tool(
        name="lock_network_sm_devices",
        description="🔒 Lock SM devices remotely. Requires confirmation. Prevents device access."
    )
    def lock_network_sm_devices(
        network_id: str,
        wifi_macs: Optional[str] = None,
        ids: Optional[str] = None,
        serials: Optional[str] = None,
        pin: Optional[int] = None,
        confirmed: bool = False
    ):
        """
        Lock devices remotely.
        
        Args:
            network_id: Network ID
            wifi_macs: WiFi MACs to lock (comma-separated)
            ids: Device IDs to lock (comma-separated)
            serials: Device serials to lock (comma-separated)
            pin: PIN code to unlock (optional)
            confirmed: Must be true to execute
        """
        if not confirmed:
            return "⚠️ Device lock requires confirmed=true to execute. This will prevent device access!"
        
        try:
            kwargs = {}
            if wifi_macs:
                kwargs['wifiMacs'] = [m.strip() for m in wifi_macs.split(',')]
            if ids:
                kwargs['ids'] = [i.strip() for i in ids.split(',')]
            if serials:
                kwargs['serials'] = [s.strip() for s in serials.split(',')]
            if pin:
                kwargs['pin'] = pin
            
            result = meraki_client.dashboard.sm.lockNetworkSmDevices(network_id, **kwargs)
            
            response = f"# 🔒 Devices Locked\n\n"
            
            if result:
                response += f"**Request ID**: {result.get('id', 'N/A')}\n\n"
                response += "⚠️ Devices are now locked and require unlock code to access.\n"
                if pin:
                    response += f"**Unlock PIN**: {pin}\n"
            
            return response
        except Exception as e:
            return f"❌ Error locking devices: {str(e)}"
    
    @app.tool(
        name="modify_network_sm_devices_tags",
        description="🏷️ Add, delete, or update tags on SM devices for organization and filtering."
    )
    def modify_network_sm_devices_tags(
        network_id: str,
        tags: str,
        update_action: str,
        wifi_macs: Optional[str] = None,
        ids: Optional[str] = None,
        serials: Optional[str] = None
    ):
        """
        Modify device tags.
        
        Args:
            network_id: Network ID
            tags: Tags to modify (comma-separated)
            update_action: Action to perform (add, delete, replace)
            wifi_macs: Target devices by WiFi MAC (comma-separated)
            ids: Target devices by ID (comma-separated)
            serials: Target devices by serial (comma-separated)
        """
        try:
            kwargs = {}
            kwargs['tags'] = [t.strip() for t in tags.split(',')]
            kwargs['updateAction'] = update_action
            
            if wifi_macs:
                kwargs['wifiMacs'] = [m.strip() for m in wifi_macs.split(',')]
            if ids:
                kwargs['ids'] = [i.strip() for i in ids.split(',')]
            if serials:
                kwargs['serials'] = [s.strip() for s in serials.split(',')]
            
            result = meraki_client.dashboard.sm.modifyNetworkSmDevicesTags(network_id, **kwargs)
            
            response = f"# 🏷️ Tags Modified\n\n"
            
            if result:
                response += f"**Action**: {update_action}\n"
                response += f"**Tags**: {tags}\n"
                response += f"**Devices Updated**: {len(result.get('ids', []))}\n"
            
            return response
        except Exception as e:
            return f"❌ Error modifying tags: {str(e)}"
    
    @app.tool(
        name="move_network_sm_devices",
        description="🔄 Move SM devices to a new network. Requires confirmation."
    )
    def move_network_sm_devices(
        network_id: str,
        new_network: str,
        wifi_macs: Optional[str] = None,
        ids: Optional[str] = None,
        serials: Optional[str] = None,
        confirmed: bool = False
    ):
        """
        Move devices to another network.
        
        Args:
            network_id: Current network ID
            new_network: Destination network ID
            wifi_macs: WiFi MACs to move (comma-separated)
            ids: Device IDs to move (comma-separated)
            serials: Device serials to move (comma-separated)
            confirmed: Must be true to execute
        """
        if not confirmed:
            return "⚠️ Device move requires confirmed=true to execute"
        
        try:
            kwargs = {}
            kwargs['newNetwork'] = new_network
            
            if wifi_macs:
                kwargs['wifiMacs'] = [m.strip() for m in wifi_macs.split(',')]
            if ids:
                kwargs['ids'] = [i.strip() for i in ids.split(',')]
            if serials:
                kwargs['serials'] = [s.strip() for s in serials.split(',')]
            
            result = meraki_client.dashboard.sm.moveNetworkSmDevices(network_id, **kwargs)
            
            response = f"# ✅ Devices Moved\n\n"
            
            if result:
                response += f"**New Network**: {new_network}\n"
                response += f"**Devices Moved**: {len(result.get('ids', []))}\n"
            
            return response
        except Exception as e:
            return f"❌ Error moving devices: {str(e)}"
    
    @app.tool(
        name="reboot_network_sm_devices",
        description="🔄 Reboot SM devices remotely. Requires confirmation."
    )
    def reboot_network_sm_devices(
        network_id: str,
        wifi_macs: Optional[str] = None,
        ids: Optional[str] = None,
        serials: Optional[str] = None,
        confirmed: bool = False
    ):
        """
        Reboot devices remotely.
        
        Args:
            network_id: Network ID
            wifi_macs: WiFi MACs to reboot (comma-separated)
            ids: Device IDs to reboot (comma-separated)
            serials: Device serials to reboot (comma-separated)
            confirmed: Must be true to execute
        """
        if not confirmed:
            return "⚠️ Device reboot requires confirmed=true to execute"
        
        try:
            kwargs = {}
            if wifi_macs:
                kwargs['wifiMacs'] = [m.strip() for m in wifi_macs.split(',')]
            if ids:
                kwargs['ids'] = [i.strip() for i in ids.split(',')]
            if serials:
                kwargs['serials'] = [s.strip() for s in serials.split(',')]
            
            result = meraki_client.dashboard.sm.rebootNetworkSmDevices(network_id, **kwargs)
            
            response = f"# 🔄 Devices Rebooting\n\n"
            
            if result:
                response += f"**Request ID**: {result.get('id', 'N/A')}\n\n"
                response += "Devices will reboot and reconnect within a few minutes.\n"
            
            return response
        except Exception as e:
            return f"❌ Error rebooting devices: {str(e)}"
    
    @app.tool(
        name="shutdown_network_sm_devices",
        description="⚡ Shutdown SM devices remotely. Requires confirmation."
    )
    def shutdown_network_sm_devices(
        network_id: str,
        wifi_macs: Optional[str] = None,
        ids: Optional[str] = None,
        serials: Optional[str] = None,
        confirmed: bool = False
    ):
        """
        Shutdown devices remotely.
        
        Args:
            network_id: Network ID
            wifi_macs: WiFi MACs to shutdown (comma-separated)
            ids: Device IDs to shutdown (comma-separated)
            serials: Device serials to shutdown (comma-separated)
            confirmed: Must be true to execute
        """
        if not confirmed:
            return "⚠️ Device shutdown requires confirmed=true to execute"
        
        try:
            kwargs = {}
            if wifi_macs:
                kwargs['wifiMacs'] = [m.strip() for m in wifi_macs.split(',')]
            if ids:
                kwargs['ids'] = [i.strip() for i in ids.split(',')]
            if serials:
                kwargs['serials'] = [s.strip() for s in serials.split(',')]
            
            result = meraki_client.dashboard.sm.shutdownNetworkSmDevices(network_id, **kwargs)
            
            response = f"# ⚡ Devices Shutting Down\n\n"
            
            if result:
                response += f"**Request ID**: {result.get('id', 'N/A')}\n\n"
                response += "⚠️ Devices are shutting down and will need manual power on.\n"
            
            return response
        except Exception as e:
            return f"❌ Error shutting down devices: {str(e)}"
    
    @app.tool(
        name="wipe_network_sm_devices",
        description="⚠️ Factory reset SM devices. DESTRUCTIVE! Requires confirmation. All data will be erased."
    )
    def wipe_network_sm_devices(
        network_id: str,
        wifi_macs: Optional[str] = None,
        ids: Optional[str] = None,
        serials: Optional[str] = None,
        pin: Optional[int] = None,
        confirmed: bool = False
    ):
        """
        Wipe devices to factory settings.
        
        Args:
            network_id: Network ID
            wifi_macs: WiFi MACs to wipe (comma-separated)
            ids: Device IDs to wipe (comma-separated)
            serials: Device serials to wipe (comma-separated)
            pin: PIN code for iOS devices
            confirmed: Must be true to execute
        """
        if not confirmed:
            return "⚠️ Device wipe requires confirmed=true. WARNING: This will ERASE ALL DATA!"
        
        try:
            kwargs = {}
            if wifi_macs:
                kwargs['wifiMacs'] = [m.strip() for m in wifi_macs.split(',')]
            if ids:
                kwargs['ids'] = [i.strip() for i in ids.split(',')]
            if serials:
                kwargs['serials'] = [s.strip() for s in serials.split(',')]
            if pin:
                kwargs['pin'] = pin
            
            result = meraki_client.dashboard.sm.wipeNetworkSmDevices(network_id, **kwargs)
            
            response = f"# ⚠️ Devices Being Wiped\n\n"
            
            if result:
                response += f"**Request ID**: {result.get('id', 'N/A')}\n\n"
                response += "🚨 **WARNING**: All data on these devices is being erased!\n"
                response += "Devices will reset to factory settings.\n"
            
            return response
        except Exception as e:
            return f"❌ Error wiping devices: {str(e)}"
    
    # ==================== DEVICE DETAILS ====================
    
    @app.tool(
        name="get_network_sm_device_cellular_usage",
        description="📶 Get cellular data usage history for a device."
    )
    def get_network_sm_device_cellular_usage(
        network_id: str,
        device_id: str
    ):
        """
        Get device cellular usage history.
        
        Args:
            network_id: Network ID
            device_id: Device ID
        """
        try:
            result = meraki_client.dashboard.sm.getNetworkSmDeviceCellularUsageHistory(
                network_id, device_id
            )
            
            response = f"# 📶 Cellular Usage History\n\n"
            response += f"**Device**: {device_id}\n\n"
            
            if result and isinstance(result, list):
                total_sent = sum(d.get('sent', 0) for d in result)
                total_recv = sum(d.get('received', 0) for d in result)
                
                response += f"## Total Usage\n"
                response += f"- **Sent**: {total_sent / 1024 / 1024:.2f} MB\n"
                response += f"- **Received**: {total_recv / 1024 / 1024:.2f} MB\n"
                response += f"- **Total**: {(total_sent + total_recv) / 1024 / 1024:.2f} MB\n\n"
                
                response += f"## Recent Usage\n"
                for usage in result[:10]:
                    response += f"- **{usage.get('ts', 'N/A')}**: "
                    response += f"↑ {usage.get('sent', 0)/1024:.1f} KB "
                    response += f"↓ {usage.get('received', 0)/1024:.1f} KB\n"
            else:
                response += "*No cellular usage data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting cellular usage: {str(e)}"
    
    @app.tool(
        name="get_network_sm_device_certs",
        description="🔐 Get certificates installed on a device."
    )
    def get_network_sm_device_certs(
        network_id: str,
        device_id: str
    ):
        """
        Get device certificates.
        
        Args:
            network_id: Network ID
            device_id: Device ID
        """
        try:
            result = meraki_client.dashboard.sm.getNetworkSmDeviceCerts(network_id, device_id)
            
            response = f"# 🔐 Device Certificates\n\n"
            response += f"**Device**: {device_id}\n\n"
            
            if result and isinstance(result, list):
                response += f"**Total Certificates**: {len(result)}\n\n"
                
                for cert in result:
                    response += f"## {cert.get('name', 'Unnamed Certificate')}\n"
                    response += f"- **Issuer**: {cert.get('issuer', 'N/A')}\n"
                    response += f"- **Subject**: {cert.get('subject', 'N/A')}\n"
                    response += f"- **Valid From**: {cert.get('notValidBefore', 'N/A')}\n"
                    response += f"- **Valid Until**: {cert.get('notValidAfter', 'N/A')}\n"
                    response += f"- **Certificate ID**: {cert.get('certificateId', 'N/A')}\n"
                    response += "\n"
            else:
                response += "*No certificates found*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting certificates: {str(e)}"
    
    @app.tool(
        name="get_network_sm_device_connectivity",
        description="🌐 Get connectivity status for a device including signal strength and connection info."
    )
    def get_network_sm_device_connectivity(
        network_id: str,
        device_id: str,
        per_page: Optional[int] = 100
    ):
        """
        Get device connectivity information.
        
        Args:
            network_id: Network ID
            device_id: Device ID
            per_page: Results per page
        """
        try:
            kwargs = {}
            if per_page:
                kwargs['perPage'] = min(per_page, 1000)
            
            result = meraki_client.dashboard.sm.getNetworkSmDeviceConnectivity(
                network_id, device_id, **kwargs
            )
            
            response = f"# 🌐 Device Connectivity\n\n"
            response += f"**Device**: {device_id}\n\n"
            
            if result and isinstance(result, list):
                # Get latest status
                if result:
                    latest = result[0]
                    response += f"## Current Status\n"
                    response += f"- **Connected**: {'✅' if latest.get('connected') else '❌'}\n"
                    response += f"- **Signal Strength**: {latest.get('signalStrength', 'N/A')} dBm\n"
                    response += f"- **Connection Type**: {latest.get('connectionType', 'N/A')}\n"
                    response += f"- **Last Seen**: {latest.get('ts', 'N/A')}\n\n"
                
                response += f"## Connection History\n"
                for conn in result[:10]:
                    status = '🟢' if conn.get('connected') else '🔴'
                    response += f"- {status} **{conn.get('ts', 'N/A')}**: "
                    response += f"{conn.get('connectionType', 'N/A')} "
                    response += f"({conn.get('signalStrength', 'N/A')} dBm)\n"
            else:
                response += "*No connectivity data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting connectivity: {str(e)}"
    
    @app.tool(
        name="get_network_sm_device_desktop_logs",
        description="🖥️ Get desktop logs for a device (macOS/Windows)."
    )
    def get_network_sm_device_desktop_logs(
        network_id: str,
        device_id: str,
        per_page: Optional[int] = 100
    ):
        """
        Get desktop device logs.
        
        Args:
            network_id: Network ID
            device_id: Device ID
            per_page: Results per page
        """
        try:
            kwargs = {}
            if per_page:
                kwargs['perPage'] = min(per_page, 1000)
            
            result = meraki_client.dashboard.sm.getNetworkSmDeviceDesktopLogs(
                network_id, device_id, **kwargs
            )
            
            response = f"# 🖥️ Desktop Logs\n\n"
            response += f"**Device**: {device_id}\n\n"
            
            if result and isinstance(result, list):
                response += f"**Total Logs**: {len(result)}\n\n"
                
                for log in result[:20]:
                    response += f"- **{log.get('ts', 'N/A')}**: "
                    response += f"{log.get('user', 'N/A')} - "
                    response += f"{log.get('event', 'N/A')}\n"
                    
                    details = log.get('details')
                    if details:
                        response += f"  Details: {details}\n"
            else:
                response += "*No desktop logs available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting desktop logs: {str(e)}"
    
    @app.tool(
        name="get_network_sm_device_command_logs",
        description="📜 Get command logs showing all MDM commands sent to a device."
    )
    def get_network_sm_device_command_logs(
        network_id: str,
        device_id: str,
        per_page: Optional[int] = 100
    ):
        """
        Get device command logs.
        
        Args:
            network_id: Network ID
            device_id: Device ID
            per_page: Results per page
        """
        try:
            kwargs = {}
            if per_page:
                kwargs['perPage'] = min(per_page, 1000)
            
            result = meraki_client.dashboard.sm.getNetworkSmDeviceDeviceCommandLogs(
                network_id, device_id, **kwargs
            )
            
            response = f"# 📜 Device Command Logs\n\n"
            response += f"**Device**: {device_id}\n\n"
            
            if result and isinstance(result, list):
                response += f"**Total Commands**: {len(result)}\n\n"
                
                for cmd in result[:20]:
                    status_icon = '✅' if cmd.get('status') == 'completed' else '⏳'
                    response += f"- {status_icon} **{cmd.get('name', 'Unknown Command')}**\n"
                    response += f"  - Time: {cmd.get('ts', 'N/A')}\n"
                    response += f"  - Status: {cmd.get('status', 'N/A')}\n"
                    response += f"  - Action: {cmd.get('action', 'N/A')}\n"
                    
                    error = cmd.get('error')
                    if error:
                        response += f"  - ❌ Error: {error}\n"
                    
                    response += "\n"
            else:
                response += "*No command logs available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting command logs: {str(e)}"
    
    @app.tool(
        name="get_network_sm_device_profiles",
        description="📋 Get configuration profiles installed on a device."
    )
    def get_network_sm_device_profiles(
        network_id: str,
        device_id: str
    ):
        """
        Get device configuration profiles.
        
        Args:
            network_id: Network ID
            device_id: Device ID
        """
        try:
            result = meraki_client.dashboard.sm.getNetworkSmDeviceDeviceProfiles(
                network_id, device_id
            )
            
            response = f"# 📋 Device Profiles\n\n"
            response += f"**Device**: {device_id}\n\n"
            
            if result and isinstance(result, list):
                response += f"**Total Profiles**: {len(result)}\n\n"
                
                for profile in result:
                    response += f"## {profile.get('name', 'Unnamed Profile')}\n"
                    response += f"- **ID**: {profile.get('id', 'N/A')}\n"
                    response += f"- **Version**: {profile.get('version', 'N/A')}\n"
                    response += f"- **Description**: {profile.get('description', 'N/A')}\n"
                    response += f"- **Is Encrypted**: {profile.get('isEncrypted', False)}\n"
                    response += f"- **Is Managed**: {profile.get('isManaged', False)}\n"
                    response += "\n"
            else:
                response += "*No profiles installed*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting profiles: {str(e)}"
    
    @app.tool(
        name="install_network_sm_device_apps",
        description="📲 Install apps on SM devices. Requires app IDs from catalog."
    )
    def install_network_sm_device_apps(
        network_id: str,
        device_id: str,
        app_ids: str,
        force: bool = False
    ):
        """
        Install apps on a device.
        
        Args:
            network_id: Network ID
            device_id: Device ID
            app_ids: App IDs to install (comma-separated)
            force: Force reinstall if already installed
        """
        try:
            kwargs = {}
            kwargs['appIds'] = [a.strip() for a in app_ids.split(',')]
            if force:
                kwargs['force'] = force
            
            result = meraki_client.dashboard.sm.installNetworkSmDeviceApps(
                network_id, device_id, **kwargs
            )
            
            response = f"# 📲 Apps Installing\n\n"
            response += f"**Device**: {device_id}\n"
            response += f"**Apps**: {app_ids}\n\n"
            
            if result:
                response += "Installation command sent. Apps will install based on device policy.\n"
            
            return response
        except Exception as e:
            return f"❌ Error installing apps: {str(e)}"
    
    @app.tool(
        name="get_network_sm_device_network_adapters",
        description="🔌 Get network adapter information for a device."
    )
    def get_network_sm_device_network_adapters(
        network_id: str,
        device_id: str
    ):
        """
        Get device network adapters.
        
        Args:
            network_id: Network ID
            device_id: Device ID
        """
        try:
            result = meraki_client.dashboard.sm.getNetworkSmDeviceNetworkAdapters(
                network_id, device_id
            )
            
            response = f"# 🔌 Network Adapters\n\n"
            response += f"**Device**: {device_id}\n\n"
            
            if result and isinstance(result, list):
                response += f"**Total Adapters**: {len(result)}\n\n"
                
                for adapter in result:
                    response += f"## {adapter.get('name', 'Unknown Adapter')}\n"
                    response += f"- **MAC Address**: {adapter.get('mac', 'N/A')}\n"
                    response += f"- **IP Address**: {adapter.get('ip', 'N/A')}\n"
                    response += f"- **Gateway**: {adapter.get('gateway', 'N/A')}\n"
                    response += f"- **Subnet**: {adapter.get('subnet', 'N/A')}\n"
                    response += f"- **DNS**: {adapter.get('dns', 'N/A')}\n"
                    response += f"- **DHCP Server**: {adapter.get('dhcpServer', 'N/A')}\n"
                    response += "\n"
            else:
                response += "*No network adapters found*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting network adapters: {str(e)}"
    
    @app.tool(
        name="get_network_sm_device_performance",
        description="📊 Get performance metrics history for a device (CPU, memory, disk)."
    )
    def get_network_sm_device_performance(
        network_id: str,
        device_id: str,
        per_page: Optional[int] = 100
    ):
        """
        Get device performance history.
        
        Args:
            network_id: Network ID
            device_id: Device ID
            per_page: Results per page
        """
        try:
            kwargs = {}
            if per_page:
                kwargs['perPage'] = min(per_page, 1000)
            
            result = meraki_client.dashboard.sm.getNetworkSmDevicePerformanceHistory(
                network_id, device_id, **kwargs
            )
            
            response = f"# 📊 Performance History\n\n"
            response += f"**Device**: {device_id}\n\n"
            
            if result and isinstance(result, list):
                # Get latest metrics
                if result:
                    latest = result[0]
                    response += f"## Current Performance\n"
                    response += f"- **CPU Usage**: {latest.get('cpuPercentUsed', 0):.1f}%\n"
                    response += f"- **Memory Usage**: {latest.get('memPercentUsed', 0):.1f}%\n"
                    response += f"- **Disk Usage**: {latest.get('diskPercentUsed', 0):.1f}%\n"
                    response += f"- **Time**: {latest.get('ts', 'N/A')}\n\n"
                
                # Calculate averages
                cpu_avg = sum(p.get('cpuPercentUsed', 0) for p in result) / len(result)
                mem_avg = sum(p.get('memPercentUsed', 0) for p in result) / len(result)
                disk_avg = sum(p.get('diskPercentUsed', 0) for p in result) / len(result)
                
                response += f"## Averages\n"
                response += f"- **CPU**: {cpu_avg:.1f}%\n"
                response += f"- **Memory**: {mem_avg:.1f}%\n"
                response += f"- **Disk**: {disk_avg:.1f}%\n\n"
                
                response += f"## Recent History\n"
                for perf in result[:10]:
                    response += f"- **{perf.get('ts', 'N/A')}**: "
                    response += f"CPU {perf.get('cpuPercentUsed', 0):.0f}% | "
                    response += f"Mem {perf.get('memPercentUsed', 0):.0f}% | "
                    response += f"Disk {perf.get('diskPercentUsed', 0):.0f}%\n"
            else:
                response += "*No performance data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting performance: {str(e)}"
    
    @app.tool(
        name="refresh_network_sm_device_details",
        description="🔄 Refresh device details from the device."
    )
    def refresh_network_sm_device_details(
        network_id: str,
        device_id: str
    ):
        """
        Refresh device details.
        
        Args:
            network_id: Network ID
            device_id: Device ID
        """
        try:
            result = meraki_client.dashboard.sm.refreshNetworkSmDeviceDetails(
                network_id, device_id
            )
            
            response = f"# 🔄 Device Refresh Initiated\n\n"
            response += f"**Device**: {device_id}\n\n"
            response += "Device will update its details within the next few minutes.\n"
            
            return response
        except Exception as e:
            return f"❌ Error refreshing device: {str(e)}"
    
    @app.tool(
        name="get_network_sm_device_restrictions",
        description="🚫 Get restrictions/compliance status for a device."
    )
    def get_network_sm_device_restrictions(
        network_id: str,
        device_id: str
    ):
        """
        Get device restrictions and compliance.
        
        Args:
            network_id: Network ID
            device_id: Device ID
        """
        try:
            result = meraki_client.dashboard.sm.getNetworkSmDeviceRestrictions(
                network_id, device_id
            )
            
            response = f"# 🚫 Device Restrictions\n\n"
            response += f"**Device**: {device_id}\n\n"
            
            if result:
                response += f"## Compliance Status\n"
                response += f"- **Compliant**: {'✅' if result.get('compliant') else '❌'}\n\n"
                
                # Restrictions
                restrictions = result.get('restrictions', {})
                if restrictions:
                    response += f"## Applied Restrictions\n"
                    for key, value in restrictions.items():
                        response += f"- **{key}**: {value}\n"
                
                # Violations
                violations = result.get('violations', [])
                if violations:
                    response += f"\n## Policy Violations ({len(violations)})\n"
                    for violation in violations:
                        response += f"- ❌ {violation}\n"
            else:
                response += "*No restrictions data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting restrictions: {str(e)}"
    
    @app.tool(
        name="get_network_sm_device_security_centers",
        description="🛡️ Get security center information for a device."
    )
    def get_network_sm_device_security_centers(
        network_id: str,
        device_id: str
    ):
        """
        Get device security centers.
        
        Args:
            network_id: Network ID
            device_id: Device ID
        """
        try:
            result = meraki_client.dashboard.sm.getNetworkSmDeviceSecurityCenters(
                network_id, device_id
            )
            
            response = f"# 🛡️ Security Centers\n\n"
            response += f"**Device**: {device_id}\n\n"
            
            if result and isinstance(result, list):
                for center in result:
                    response += f"## {center.get('name', 'Unknown')}\n"
                    response += f"- **Running**: {'✅' if center.get('running') else '❌'}\n"
                    response += f"- **Version**: {center.get('version', 'N/A')}\n"
                    response += f"- **Last Update**: {center.get('lastUpdate', 'N/A')}\n"
                    response += f"- **ID**: {center.get('id', 'N/A')}\n"
                    response += "\n"
            else:
                response += "*No security center data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting security centers: {str(e)}"
    
    @app.tool(
        name="get_network_sm_device_softwares",
        description="💿 Get installed software/apps on a device."
    )
    def get_network_sm_device_softwares(
        network_id: str,
        device_id: str
    ):
        """
        Get installed software on device.
        
        Args:
            network_id: Network ID
            device_id: Device ID
        """
        try:
            result = meraki_client.dashboard.sm.getNetworkSmDeviceSoftwares(
                network_id, device_id
            )
            
            response = f"# 💿 Installed Software\n\n"
            response += f"**Device**: {device_id}\n\n"
            
            if result and isinstance(result, list):
                response += f"**Total Apps**: {len(result)}\n\n"
                
                # Group by status
                installed = [s for s in result if s.get('status') == 'installed']
                pending = [s for s in result if s.get('status') == 'pending']
                
                if installed:
                    response += f"## Installed ({len(installed)})\n"
                    for sw in installed[:20]:
                        response += f"- **{sw.get('name', 'Unknown')}** "
                        response += f"v{sw.get('version', 'N/A')}\n"
                        response += f"  Size: {sw.get('appSize', 0)/1024/1024:.1f} MB\n"
                
                if pending:
                    response += f"\n## Pending Installation ({len(pending)})\n"
                    for sw in pending:
                        response += f"- {sw.get('name', 'Unknown')}\n"
            else:
                response += "*No software data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting software: {str(e)}"
    
    @app.tool(
        name="unenroll_network_sm_device",
        description="❌ Unenroll a device from Systems Manager. Requires confirmation."
    )
    def unenroll_network_sm_device(
        network_id: str,
        device_id: str,
        confirmed: bool = False
    ):
        """
        Unenroll device from SM.
        
        Args:
            network_id: Network ID
            device_id: Device ID
            confirmed: Must be true to execute
        """
        if not confirmed:
            return "⚠️ Device unenrollment requires confirmed=true. Device will lose MDM management!"
        
        try:
            result = meraki_client.dashboard.sm.unenrollNetworkSmDevice(
                network_id, device_id
            )
            
            response = f"# ❌ Device Unenrolled\n\n"
            response += f"**Device**: {device_id}\n\n"
            response += "Device has been removed from Systems Manager.\n"
            response += "MDM profiles and policies will be removed from the device.\n"
            
            return response
        except Exception as e:
            return f"❌ Error unenrolling device: {str(e)}"
    
    @app.tool(
        name="uninstall_network_sm_device_apps",
        description="🗑️ Uninstall apps from SM devices."
    )
    def uninstall_network_sm_device_apps(
        network_id: str,
        device_id: str,
        app_ids: str
    ):
        """
        Uninstall apps from device.
        
        Args:
            network_id: Network ID
            device_id: Device ID
            app_ids: App IDs to uninstall (comma-separated)
        """
        try:
            kwargs = {}
            kwargs['appIds'] = [a.strip() for a in app_ids.split(',')]
            
            result = meraki_client.dashboard.sm.uninstallNetworkSmDeviceApps(
                network_id, device_id, **kwargs
            )
            
            response = f"# 🗑️ Apps Uninstalling\n\n"
            response += f"**Device**: {device_id}\n"
            response += f"**Apps**: {app_ids}\n\n"
            response += "Uninstall command sent. Apps will be removed based on device policy.\n"
            
            return response
        except Exception as e:
            return f"❌ Error uninstalling apps: {str(e)}"
    
    @app.tool(
        name="get_network_sm_device_wlan_lists",
        description="📶 Get WiFi network lists configured on a device."
    )
    def get_network_sm_device_wlan_lists(
        network_id: str,
        device_id: str
    ):
        """
        Get device WiFi networks.
        
        Args:
            network_id: Network ID
            device_id: Device ID
        """
        try:
            result = meraki_client.dashboard.sm.getNetworkSmDeviceWlanLists(
                network_id, device_id
            )
            
            response = f"# 📶 WiFi Networks\n\n"
            response += f"**Device**: {device_id}\n\n"
            
            if result and isinstance(result, list):
                response += f"**Total Networks**: {len(result)}\n\n"
                
                for wlan in result:
                    response += f"## {wlan.get('ssid', 'Unknown SSID')}\n"
                    response += f"- **Security**: {wlan.get('security', 'Open')}\n"
                    response += f"- **Auto Join**: {wlan.get('autoJoin', False)}\n"
                    response += f"- **Hidden**: {wlan.get('hidden', False)}\n"
                    response += f"- **Identity**: {wlan.get('identity', 'N/A')}\n"
                    response += "\n"
            else:
                response += "*No WiFi networks configured*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting WiFi networks: {str(e)}"
    
    # ==================== PROFILES & POLICIES ====================
    
    @app.tool(
        name="get_network_sm_profiles",
        description="📋 List all configuration profiles for the network."
    )
    def get_network_sm_profiles(
        network_id: str
    ):
        """
        Get all SM profiles.
        
        Args:
            network_id: Network ID
        """
        try:
            result = meraki_client.dashboard.sm.getNetworkSmProfiles(network_id)
            
            response = f"# 📋 SM Configuration Profiles\n\n"
            
            if result and isinstance(result, list):
                response += f"**Total Profiles**: {len(result)}\n\n"
                
                for profile in result:
                    response += f"## {profile.get('name', 'Unnamed Profile')}\n"
                    response += f"- **ID**: {profile.get('id', 'N/A')}\n"
                    response += f"- **Description**: {profile.get('description', 'N/A')}\n"
                    response += f"- **Scope**: {profile.get('scope', 'N/A')}\n"
                    
                    # Tags
                    tags = profile.get('tags', [])
                    if tags:
                        response += f"- **Tags**: {', '.join(tags)}\n"
                    
                    response += "\n"
            else:
                response += "*No profiles configured*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting profiles: {str(e)}"
    
    @app.tool(
        name="get_network_sm_target_groups",
        description="🎯 List all target groups for deploying profiles and apps."
    )
    def get_network_sm_target_groups(
        network_id: str
    ):
        """
        Get all SM target groups.
        
        Args:
            network_id: Network ID
        """
        try:
            result = meraki_client.dashboard.sm.getNetworkSmTargetGroups(network_id)
            
            response = f"# 🎯 SM Target Groups\n\n"
            
            if result and isinstance(result, list):
                response += f"**Total Groups**: {len(result)}\n\n"
                
                for group in result:
                    response += f"## {group.get('name', 'Unnamed Group')}\n"
                    response += f"- **ID**: {group.get('id', 'N/A')}\n"
                    response += f"- **Type**: {group.get('type', 'N/A')}\n"
                    
                    # Tags
                    tags = group.get('tags', [])
                    if tags:
                        response += f"- **Tags**: {', '.join(tags)}\n"
                    
                    response += "\n"
            else:
                response += "*No target groups configured*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting target groups: {str(e)}"
    
    @app.tool(
        name="get_network_sm_target_group",
        description="🎯 Get details of a specific target group."
    )
    def get_network_sm_target_group(
        network_id: str,
        target_group_id: str
    ):
        """
        Get specific target group.
        
        Args:
            network_id: Network ID
            target_group_id: Target group ID
        """
        try:
            result = meraki_client.dashboard.sm.getNetworkSmTargetGroup(
                network_id, target_group_id
            )
            
            response = f"# 🎯 Target Group Details\n\n"
            
            if result:
                response += f"**Name**: {result.get('name', 'Unnamed')}\n"
                response += f"**ID**: {target_group_id}\n"
                response += f"**Type**: {result.get('type', 'N/A')}\n\n"
                
                # Tags
                tags = result.get('tags', [])
                if tags:
                    response += f"## Tags ({len(tags)})\n"
                    for tag in tags:
                        response += f"- {tag}\n"
            else:
                response += "*Target group not found*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting target group: {str(e)}"
    
    @app.tool(
        name="get_network_sm_trusted_access_configs",
        description="🔐 Get trusted access configurations for the network."
    )
    def get_network_sm_trusted_access_configs(
        network_id: str,
        per_page: Optional[int] = 100
    ):
        """
        Get trusted access configs.
        
        Args:
            network_id: Network ID
            per_page: Results per page
        """
        try:
            kwargs = {}
            if per_page:
                kwargs['perPage'] = min(per_page, 1000)
            
            result = meraki_client.dashboard.sm.getNetworkSmTrustedAccessConfigs(
                network_id, **kwargs
            )
            
            response = f"# 🔐 Trusted Access Configs\n\n"
            
            if result and isinstance(result, list):
                response += f"**Total Configs**: {len(result)}\n\n"
                
                for config in result:
                    response += f"## {config.get('name', 'Unnamed')}\n"
                    response += f"- **Access Type**: {config.get('accessType', 'N/A')}\n"
                    response += f"- **Host Type**: {config.get('hostType', 'N/A')}\n"
                    response += f"- **Port**: {config.get('port', 'N/A')}\n"
                    response += "\n"
            else:
                response += "*No trusted access configs*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting trusted access: {str(e)}"
    
    # ==================== USER MANAGEMENT ====================
    
    @app.tool(
        name="get_network_sm_user_access_devices",
        description="👤 Get user access devices for the network."
    )
    def get_network_sm_user_access_devices(
        network_id: str,
        per_page: Optional[int] = 100
    ):
        """
        Get user access devices.
        
        Args:
            network_id: Network ID
            per_page: Results per page
        """
        try:
            kwargs = {}
            if per_page:
                kwargs['perPage'] = min(per_page, 1000)
            
            result = meraki_client.dashboard.sm.getNetworkSmUserAccessDevices(
                network_id, **kwargs
            )
            
            response = f"# 👤 User Access Devices\n\n"
            
            if result and isinstance(result, list):
                response += f"**Total Devices**: {len(result)}\n\n"
                
                for device in result[:20]:
                    response += f"## {device.get('name', 'Unknown')}\n"
                    response += f"- **Email**: {device.get('email', 'N/A')}\n"
                    response += f"- **Username**: {device.get('username', 'N/A')}\n"
                    response += f"- **MAC**: {device.get('mac', 'N/A')}\n"
                    response += f"- **Device ID**: {device.get('id', 'N/A')}\n"
                    
                    # Trusted access status
                    trusted = device.get('trustedAccessConnections', [])
                    if trusted:
                        response += f"- **Trusted Connections**: {len(trusted)}\n"
                    
                    response += "\n"
            else:
                response += "*No user access devices*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting user devices: {str(e)}"
    
    @app.tool(
        name="get_network_sm_users",
        description="👥 Get all users enrolled in Systems Manager."
    )
    def get_network_sm_users(
        network_id: str,
        usernames: Optional[str] = None,
        emails: Optional[str] = None,
        ids: Optional[str] = None
    ):
        """
        Get SM users.
        
        Args:
            network_id: Network ID
            usernames: Filter by usernames (comma-separated)
            emails: Filter by emails (comma-separated)
            ids: Filter by user IDs (comma-separated)
        """
        try:
            kwargs = {}
            if usernames:
                kwargs['usernames'] = [u.strip() for u in usernames.split(',')]
            if emails:
                kwargs['emails'] = [e.strip() for e in emails.split(',')]
            if ids:
                kwargs['ids'] = [i.strip() for i in ids.split(',')]
            
            result = meraki_client.dashboard.sm.getNetworkSmUsers(network_id, **kwargs)
            
            response = f"# 👥 Systems Manager Users\n\n"
            
            if result and isinstance(result, list):
                response += f"**Total Users**: {len(result)}\n\n"
                
                for user in result[:20]:
                    response += f"## {user.get('displayName', user.get('username', 'Unknown'))}\n"
                    response += f"- **ID**: {user.get('id', 'N/A')}\n"
                    response += f"- **Email**: {user.get('email', 'N/A')}\n"
                    response += f"- **Username**: {user.get('username', 'N/A')}\n"
                    response += f"- **Full Name**: {user.get('fullName', 'N/A')}\n"
                    response += f"- **Has Password**: {user.get('hasPassword', False)}\n"
                    
                    # Tags
                    tags = user.get('tags', [])
                    if tags:
                        response += f"- **Tags**: {', '.join(tags)}\n"
                    
                    # Device count
                    device_count = user.get('deviceCount', 0)
                    if device_count:
                        response += f"- **Devices**: {device_count}\n"
                    
                    response += "\n"
            else:
                response += "*No users found*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting users: {str(e)}"
    
    @app.tool(
        name="get_network_sm_user_device_profiles",
        description="📋 Get device profiles for a specific user."
    )
    def get_network_sm_user_device_profiles(
        network_id: str,
        user_id: str
    ):
        """
        Get user's device profiles.
        
        Args:
            network_id: Network ID
            user_id: User ID
        """
        try:
            result = meraki_client.dashboard.sm.getNetworkSmUserDeviceProfiles(
                network_id, user_id
            )
            
            response = f"# 📋 User Device Profiles\n\n"
            response += f"**User**: {user_id}\n\n"
            
            if result and isinstance(result, list):
                response += f"**Total Profiles**: {len(result)}\n\n"
                
                for profile in result:
                    response += f"## {profile.get('profileName', 'Unknown')}\n"
                    response += f"- **Profile ID**: {profile.get('profileId', 'N/A')}\n"
                    response += f"- **Device Name**: {profile.get('deviceName', 'N/A')}\n"
                    response += f"- **Device ID**: {profile.get('deviceId', 'N/A')}\n"
                    response += f"- **Is Managed**: {profile.get('isManaged', False)}\n"
                    response += f"- **Is Encrypted**: {profile.get('isEncrypted', False)}\n"
                    response += "\n"
            else:
                response += "*No profiles for this user*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting user profiles: {str(e)}"
    
    @app.tool(
        name="get_network_sm_user_softwares",
        description="💿 Get software installed on a user's devices."
    )
    def get_network_sm_user_softwares(
        network_id: str,
        user_id: str
    ):
        """
        Get user's installed software.
        
        Args:
            network_id: Network ID
            user_id: User ID
        """
        try:
            result = meraki_client.dashboard.sm.getNetworkSmUserSoftwares(
                network_id, user_id
            )
            
            response = f"# 💿 User Software\n\n"
            response += f"**User**: {user_id}\n\n"
            
            if result and isinstance(result, list):
                response += f"**Total Software**: {len(result)}\n\n"
                
                # Group by device
                devices = {}
                for sw in result:
                    device = sw.get('deviceId', 'Unknown')
                    if device not in devices:
                        devices[device] = []
                    devices[device].append(sw)
                
                for device_id, softwares in devices.items():
                    response += f"## Device {device_id}\n"
                    for sw in softwares[:10]:
                        response += f"- **{sw.get('name', 'Unknown')}** "
                        response += f"v{sw.get('version', 'N/A')}\n"
                    
                    if len(softwares) > 10:
                        response += f"  *...and {len(softwares)-10} more*\n"
                    response += "\n"
            else:
                response += "*No software data for this user*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting user software: {str(e)}"
    
    # ==================== ORGANIZATION SM ====================
    
    @app.tool(
        name="get_organization_sm_admins_roles",
        description="👮 Get SM admin roles for the organization."
    )
    def get_organization_sm_admins_roles(
        organization_id: str,
        per_page: Optional[int] = 100
    ):
        """
        Get organization SM admin roles.
        
        Args:
            organization_id: Organization ID
            per_page: Results per page
        """
        try:
            kwargs = {}
            if per_page:
                kwargs['perPage'] = min(per_page, 1000)
            
            result = meraki_client.dashboard.sm.getOrganizationSmAdminsRoles(
                organization_id, **kwargs
            )
            
            response = f"# 👮 SM Admin Roles\n\n"
            
            if result and isinstance(result, list):
                response += f"**Total Roles**: {len(result)}\n\n"
                
                for role in result:
                    response += f"## {role.get('name', 'Unnamed Role')}\n"
                    response += f"- **Role ID**: {role.get('roleId', 'N/A')}\n"
                    response += f"- **Scope**: {role.get('scope', 'N/A')}\n"
                    
                    # Tags
                    tags = role.get('tags', [])
                    if tags:
                        response += f"- **Tags**: {', '.join(tags)}\n"
                    
                    # Networks
                    networks = role.get('networks', [])
                    if networks:
                        response += f"- **Networks**: {len(networks)} assigned\n"
                    
                    response += "\n"
            else:
                response += "*No SM admin roles*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting admin roles: {str(e)}"
    
    @app.tool(
        name="get_organization_sm_admins_role",
        description="👮 Get details of a specific SM admin role."
    )
    def get_organization_sm_admins_role(
        organization_id: str,
        role_id: str
    ):
        """
        Get specific SM admin role.
        
        Args:
            organization_id: Organization ID
            role_id: Role ID
        """
        try:
            result = meraki_client.dashboard.sm.getOrganizationSmAdminsRole(
                organization_id, role_id
            )
            
            response = f"# 👮 SM Admin Role Details\n\n"
            
            if result:
                response += f"**Name**: {result.get('name', 'Unnamed')}\n"
                response += f"**Role ID**: {role_id}\n"
                response += f"**Scope**: {result.get('scope', 'N/A')}\n\n"
                
                # Permissions
                perms = result.get('permissions', [])
                if perms:
                    response += f"## Permissions ({len(perms)})\n"
                    for perm in perms:
                        response += f"- {perm}\n"
                
                # Networks
                networks = result.get('networks', [])
                if networks:
                    response += f"\n## Networks ({len(networks)})\n"
                    for net in networks[:10]:
                        response += f"- {net}\n"
            else:
                response += "*Role not found*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting role details: {str(e)}"
    
    @app.tool(
        name="create_network_sm_bypass_activation_lock",
        description="🔓 Create bypass activation lock attempt for iOS devices."
    )
    def create_network_sm_bypass_activation_lock(
        network_id: str,
        ids: str
    ):
        """
        Bypass activation lock on iOS devices.
        
        Args:
            network_id: Network ID
            ids: Device IDs (comma-separated)
        """
        try:
            kwargs = {}
            kwargs['ids'] = [i.strip() for i in ids.split(',')]
            
            result = meraki_client.dashboard.sm.createNetworkSmBypassActivationLockAttempt(
                network_id, **kwargs
            )
            
            response = f"# 🔓 Activation Lock Bypass Initiated\n\n"
            
            if result:
                response += f"**Attempt ID**: {result.get('id', 'N/A')}\n"
                response += f"**Status**: {result.get('status', 'pending')}\n"
                response += f"**Devices**: {ids}\n\n"
                response += "Bypass attempt in progress. Check status with attempt ID.\n"
            
            return response
        except Exception as e:
            return f"❌ Error bypassing activation lock: {str(e)}"
    
    @app.tool(
        name="get_network_sm_bypass_activation_lock",
        description="🔓 Get status of activation lock bypass attempt."
    )
    def get_network_sm_bypass_activation_lock(
        network_id: str,
        attempt_id: str
    ):
        """
        Get bypass activation lock status.
        
        Args:
            network_id: Network ID
            attempt_id: Bypass attempt ID
        """
        try:
            result = meraki_client.dashboard.sm.getNetworkSmBypassActivationLockAttempt(
                network_id, attempt_id
            )
            
            response = f"# 🔓 Activation Lock Bypass Status\n\n"
            response += f"**Attempt ID**: {attempt_id}\n\n"
            
            if result:
                response += f"**Status**: {result.get('status', 'unknown')}\n"
                response += f"**Created**: {result.get('createdAt', 'N/A')}\n\n"
                
                # Device results
                devices = result.get('data', {}).get('devices', [])
                if devices:
                    response += f"## Device Results\n"
                    for device in devices:
                        status_icon = '✅' if device.get('success') else '❌'
                        response += f"- {status_icon} **{device.get('deviceId')}**: "
                        response += f"{device.get('status', 'N/A')}\n"
                        
                        error = device.get('error')
                        if error:
                            response += f"  Error: {error}\n"
            else:
                response += "*Attempt not found*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting bypass status: {str(e)}"
    
    # ========== MISSING SM SDK METHODS ==========
    
    @app.tool(
        name="create_network_sm_device_command",
        description="📱 Send a command to an SM device - REQUIRES CONFIRMATION"
    )
    def create_network_sm_device_command(
        network_id: str,
        device_id: str,
        command: str,
        confirmed: bool = False
    ):
        """
        Send a command to an SM device (lock, wipe, etc.).
        
        ⚠️ WARNING: Some commands like wipe are destructive!
        
        Args:
            network_id: Network ID
            device_id: Device ID
            command: Command type (lock, wipe, reboot, shutdown)
            confirmed: Must be True for destructive operations
            
        Returns:
            Command execution status
        """
        if command in ["wipe", "shutdown"] and not confirmed:
            return f"⚠️ Command {command} requires confirmation. Set confirmed=true to proceed."
            
        try:
            result = meraki_client.dashboard.sm.createNetworkSmDeviceCommand(
                network_id,
                deviceId=device_id,
                command=command
            )
            
            return f"✅ Command '{command}' sent to device {device_id}"
            
        except Exception as e:
            return f"Error sending command: {str(e)}"
    
    @app.tool(
        name="get_network_sm_device_network_adapters",
        description="🌐 Get network adapter info for an SM device"
    )
    def get_network_sm_device_network_adapters(
        network_id: str,
        device_id: str
    ):
        """
        Get network adapter information for an SM device.
        
        Args:
            network_id: Network ID
            device_id: Device ID
            
        Returns:
            Network adapter details
        """
        try:
            adapters = meraki_client.dashboard.sm.getNetworkSmDeviceNetworkAdapters(
                network_id, device_id
            )
            
            result = f"# 🌐 Network Adapters\n\n"
            
            for adapter in adapters:
                result += f"## {adapter.get('name', 'Unknown Adapter')}\n"
                result += f"- **MAC Address**: {adapter.get('mac', 'N/A')}\n"
                result += f"- **IP Address**: {adapter.get('ip', 'N/A')}\n"
                result += f"- **Gateway**: {adapter.get('gateway', 'N/A')}\n"
                result += f"- **DHCP Server**: {adapter.get('dhcpServer', 'N/A')}\n"
                result += f"- **DNS Servers**: {', '.join(adapter.get('dnsServers', []))}\n\n"
                
            return result if adapters else "No network adapters found"
            
        except Exception as e:
            return f"Error retrieving network adapters: {str(e)}"
    
    @app.tool(
        name="get_network_sm_device_performance_history",
        description="📊 Get performance history for an SM device"
    )
    def get_network_sm_device_performance_history(
        network_id: str,
        device_id: str,
        per_page: int = 100,
        starting_after: Optional[str] = None,
        ending_before: Optional[str] = None
    ):
        """
        Get performance history for an SM device.
        
        Args:
            network_id: Network ID
            device_id: Device ID
            per_page: Number of entries per page
            starting_after: Starting cursor for pagination
            ending_before: Ending cursor for pagination
            
        Returns:
            Performance history data
        """
        try:
            kwargs = {"perPage": per_page}
            if starting_after:
                kwargs["startingAfter"] = starting_after
            if ending_before:
                kwargs["endingBefore"] = ending_before
                
            history = meraki_client.dashboard.sm.getNetworkSmDevicePerformanceHistory(
                network_id, device_id, **kwargs
            )
            
            result = f"# 📊 Performance History\n\n"
            
            for entry in history:
                result += f"## {entry.get('ts', 'Unknown time')}\n"
                result += f"- **CPU Usage**: {entry.get('cpuPercentUsed', 'N/A')}%\n"
                result += f"- **Memory Usage**: {entry.get('memPercentUsed', 'N/A')}%\n"
                result += f"- **Disk Usage**: {entry.get('diskPercentUsed', 'N/A')}%\n"
                result += f"- **Network Sent**: {entry.get('networkSent', 'N/A')} bytes\n"
                result += f"- **Network Received**: {entry.get('networkReceived', 'N/A')} bytes\n\n"
                
            return result if history else "No performance history available"
            
        except Exception as e:
            return f"Error retrieving performance history: {str(e)}"
    
    @app.tool(
        name="get_network_sm_device_restrictions",
        description="🔒 Get restrictions for an SM device"
    )
    def get_network_sm_device_restrictions(
        network_id: str,
        device_id: str
    ):
        """
        Get restrictions for an SM device.
        
        Args:
            network_id: Network ID
            device_id: Device ID
            
        Returns:
            Device restrictions
        """
        try:
            restrictions = meraki_client.dashboard.sm.getNetworkSmDeviceRestrictions(
                network_id, device_id
            )
            
            result = f"# 🔒 Device Restrictions\n\n"
            
            if restrictions.get("restrictions"):
                for key, value in restrictions["restrictions"].items():
                    result += f"- **{key}**: {value}\n"
            else:
                result += "No restrictions configured\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving restrictions: {str(e)}"
    
    @app.tool(
        name="get_network_sm_device_security_centers",
        description="🛡️ Get security center info for SM devices"
    )
    def get_network_sm_device_security_centers(
        network_id: str,
        device_ids: str
    ):
        """
        Get security center information for SM devices.
        
        Args:
            network_id: Network ID
            device_ids: Comma-separated device IDs
            
        Returns:
            Security center information
        """
        try:
            centers = meraki_client.dashboard.sm.getNetworkSmDeviceSecurityCenters(
                network_id,
                deviceIds=device_ids.split(",")
            )
            
            result = f"# 🛡️ Security Centers\n\n"
            
            for center in centers:
                device_id = center.get("deviceId", "Unknown")
                result += f"## Device: {device_id}\n"
                
                if center.get("antivirusStatus"):
                    av = center["antivirusStatus"]
                    result += f"### Antivirus\n"
                    result += f"- **Enabled**: {'✅' if av.get('isEnabled') else '❌'}\n"
                    result += f"- **Running**: {'✅' if av.get('isRunning') else '❌'}\n"
                    result += f"- **Up to Date**: {'✅' if av.get('isUpToDate') else '❌'}\n"
                    
                if center.get("firewallStatus"):
                    fw = center["firewallStatus"]
                    result += f"### Firewall\n"
                    result += f"- **Enabled**: {'✅' if fw.get('isEnabled') else '❌'}\n"
                    result += f"- **Running**: {'✅' if fw.get('isRunning') else '❌'}\n"
                    
                if center.get("hasAntivirusIssue") or center.get("hasFirewallIssue"):
                    result += f"\n⚠️ **Security Issues Detected**\n"
                    
                result += "\n"
                
            return result if centers else "No security center data available"
            
        except Exception as e:
            return f"Error retrieving security centers: {str(e)}"
    
    @app.tool(
        name="refresh_network_sm_device_details",
        description="🔄 Refresh details for an SM device"
    )
    def refresh_network_sm_device_details(
        network_id: str,
        device_id: str
    ):
        """
        Refresh details for an SM device.
        
        Args:
            network_id: Network ID
            device_id: Device ID
            
        Returns:
            Refresh status
        """
        try:
            meraki_client.dashboard.sm.refreshNetworkSmDeviceDetails(
                network_id, device_id
            )
            
            return f"✅ Device {device_id} details refresh initiated"
            
        except Exception as e:
            return f"Error refreshing device details: {str(e)}"
    
    @app.tool(
        name="unenroll_network_sm_device",
        description="🗑️ Unenroll an SM device - REQUIRES CONFIRMATION"
    )
    def unenroll_network_sm_device(
        network_id: str,
        device_id: str,
        confirmed: bool = False
    ):
        """
        Unenroll an SM device from management.
        
        ⚠️ WARNING: This will remove the device from management!
        
        Args:
            network_id: Network ID
            device_id: Device ID
            confirmed: Must be True to execute this operation
            
        Returns:
            Unenrollment status
        """
        if not confirmed:
            return "⚠️ Device unenrollment requires confirmation. Set confirmed=true to proceed."
            
        try:
            result = meraki_client.dashboard.sm.unenrollNetworkSmDevice(
                network_id, device_id
            )
            
            return f"✅ Device {device_id} unenrolled successfully"
            
        except Exception as e:
            return f"Error unenrolling device: {str(e)}"

