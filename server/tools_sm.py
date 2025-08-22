"""
Systems Manager (SM/MDM) tools for the Cisco Meraki MCP Server - ONLY REAL API METHODS.
"""

# Global variables to store app and meraki client
app = None
meraki_client = None

def register_sm_tools(mcp_app, meraki):
    """
    Register Systems Manager tools with the MCP server.
    
    Args:
        mcp_app: MCP server instance
        meraki: Meraki client instance
    """
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    
    # Register all SM tools
    register_sm_tool_handlers()

def register_sm_tool_handlers():
    """Register all Systems Manager tool handlers using ONLY REAL API methods."""
    
    @app.tool(
        name="get_network_sm_devices",
        description="📱 List all Systems Manager (MDM) devices in a network"
    )
    def get_network_sm_devices(network_id: str):
        """
        List all devices enrolled in Systems Manager for a network.
        
        Args:
            network_id: Network ID
            
        Returns:
            List of SM devices with details
        """
        try:
            devices = meraki_client.get_network_sm_devices(network_id)
            
            if not devices:
                return f"No Systems Manager devices found in network {network_id}."
                
            result = f"# 📱 Systems Manager Devices - Network {network_id}\n\n"
            result += f"**Total Devices**: {len(devices)}\n\n"
            
            # Group by OS
            os_groups = {}
            for device in devices:
                os_name = device.get('osName', 'Unknown')
                if os_name not in os_groups:
                    os_groups[os_name] = []
                os_groups[os_name].append(device)
            
            for os_name, os_devices in os_groups.items():
                result += f"## {os_name} ({len(os_devices)} devices)\n"
                
                for device in os_devices[:10]:  # Show first 10 per OS
                    name = device.get('name', 'Unnamed')
                    serial = device.get('serialNumber', device.get('id', 'Unknown'))
                    model = device.get('systemModel', 'Unknown')
                    
                    result += f"### 📱 {name}\n"
                    result += f"- **Serial/ID**: {serial}\n"
                    result += f"- **Model**: {model}\n"
                    result += f"- **User**: {device.get('ownerEmail', device.get('ownerUsername', 'Unknown'))}\n"
                    
                    # Status indicators
                    wifi_mac = device.get('wifiMac')
                    if wifi_mac:
                        result += f"- **WiFi MAC**: {wifi_mac}\n"
                        result += f"- **Last SSID**: {device.get('ssid', 'Not connected')}\n"
                    
                    # Battery if available
                    battery = device.get('batteryEstCharge')
                    if battery:
                        battery_icon = "🔋" if battery > 50 else "🪫" if battery > 20 else "🔴"
                        result += f"- **Battery**: {battery_icon} {battery}%\n"
                    
                    # Tags
                    tags = device.get('tags', [])
                    if tags:
                        result += f"- **Tags**: {', '.join(tags)}\n"
                        
                    result += "\n"
                
                if len(os_devices) > 10:
                    result += f"... and {len(os_devices) - 10} more {os_name} devices\n\n"
                    
            return result
            
        except Exception as e:
            return f"Error retrieving SM devices: {str(e)}"
    
    @app.tool(
        name="get_network_sm_device_detail",
        description="📱 Get detailed info for a specific SM device"
    )
    def get_network_sm_device_detail(network_id: str, device_id: str):
        """
        Get detailed information for a specific Systems Manager device.
        
        Args:
            network_id: Network ID
            device_id: Device ID or serial number
            
        Returns:
            Detailed device information
        """
        try:
            device = meraki_client.get_network_sm_device(network_id, device_id)
            
            result = f"# 📱 SM Device Details: {device.get('name', 'Unknown')}\n\n"
            
            # Basic Info
            result += "## Device Information\n"
            result += f"- **Serial/ID**: {device.get('serialNumber', device.get('id'))}\n"
            result += f"- **Model**: {device.get('systemModel', 'Unknown')}\n"
            result += f"- **OS**: {device.get('osName', 'Unknown')} {device.get('systemVersion', '')}\n"
            result += f"- **UUID**: {device.get('uuid', 'N/A')}\n"
            
            # User Info
            result += "\n## User Information\n"
            result += f"- **Owner**: {device.get('ownerEmail', device.get('ownerUsername', 'Unknown'))}\n"
            result += f"- **User Email**: {device.get('userEmail', 'N/A')}\n"
            
            # Network Info
            result += "\n## Network Status\n"
            result += f"- **WiFi MAC**: {device.get('wifiMac', 'N/A')}\n"
            result += f"- **Last SSID**: {device.get('ssid', 'Not connected')}\n"
            result += f"- **IP**: {device.get('ip', 'N/A')}\n"
            result += f"- **Has Cellular**: {'✅' if device.get('hasCellular') else '❌'}\n"
            
            # Security Status
            result += "\n## Security Status\n"
            result += f"- **Managed**: {'✅' if device.get('managed') else '❌'}\n"
            result += f"- **Supervised**: {'✅' if device.get('isSupervised') else '❌'}\n"
            
            # Battery if available
            battery = device.get('batteryEstCharge')
            if battery:
                battery_icon = "🔋" if battery > 50 else "🪫" if battery > 20 else "🔴"
                result += f"- **Battery**: {battery_icon} {battery}%\n"
            
            # Storage
            disk_info = device.get('diskInfo')
            if disk_info:
                result += f"\n## Storage\n"
                for disk in disk_info:
                    used = disk.get('used', 0)
                    size = disk.get('size', 1)
                    percent = (used / size * 100) if size > 0 else 0
                    result += f"- **{disk.get('name', 'Disk')}**: {percent:.1f}% used ({used}GB/{size}GB)\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving SM device details: {str(e)}"
    
    @app.tool(
        name="get_network_sm_device_apps",
        description="📲 List installed apps on an SM device"
    )
    def get_network_sm_device_apps(network_id: str, device_id: str):
        """
        List all apps installed on a Systems Manager device.
        
        Args:
            network_id: Network ID
            device_id: Device ID or serial number
            
        Returns:
            List of installed applications
        """
        try:
            apps = meraki_client.get_network_sm_device_apps(network_id, device_id)
            
            if not apps:
                return f"No apps found on device {device_id}."
                
            result = f"# 📲 Installed Apps on Device {device_id}\n\n"
            result += f"**Total Apps**: {len(apps)}\n\n"
            
            # Group by app status
            managed_apps = [app for app in apps if app.get('isManaged')]
            other_apps = [app for app in apps if not app.get('isManaged')]
            
            if managed_apps:
                result += "## 🏢 Managed Apps\n"
                for app in managed_apps[:20]:
                    result += f"- **{app.get('name', 'Unknown')}** v{app.get('version', '?')}\n"
                    result += f"  - Bundle ID: {app.get('bundleId', 'N/A')}\n"
                    result += f"  - Size: {app.get('bundleSize', 0) / 1024 / 1024:.1f} MB\n"
                    if app.get('isVppApp'):
                        result += "  - VPP App ✅\n"
                    result += "\n"
                    
            if other_apps:
                result += "## 📱 Other Apps\n"
                for app in other_apps[:20]:
                    result += f"- **{app.get('name', 'Unknown')}** v{app.get('version', '?')}\n"
                    
            if len(apps) > 40:
                result += f"\n... and {len(apps) - 40} more apps\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving device apps: {str(e)}"
    
    @app.tool(
        name="reboot_network_sm_devices",
        description="⚠️ REBOOT Systems Manager devices - REQUIRES CONFIRMATION"
    )
    def reboot_network_sm_devices(network_id: str, device_ids: str):
        """
        Reboot one or more Systems Manager devices.
        
        ⚠️ WARNING: This will force devices to restart!
        
        Args:
            network_id: Network ID
            device_ids: Comma-separated device IDs to reboot
            
        Returns:
            Reboot command status
        """
        try:
            ids_list = [id.strip() for id in device_ids.split(',')]
            device_count = len(ids_list)
            
            # Import helper function
            from utils.helpers import require_confirmation
            
            # Require confirmation
            if not require_confirmation(
                operation_type="reboot",
                resource_type="SM devices",
                resource_name=f"{device_count} device(s) in network {network_id}",
                resource_id=f"Network: {network_id}"
            ):
                return "❌ SM device reboot cancelled by user"
            
            # Perform reboot
            result = meraki_client.reboot_network_sm_devices(network_id, ids=ids_list)
            
            response = f"""✅ SM REBOOT COMMAND SENT

**Network**: {network_id}
**Devices rebooted**: {len(ids_list)}
**Device IDs**: {', '.join(ids_list)}
**Command ID**: {result.get('id', 'N/A')}

The reboot command has been sent to all devices. They will restart shortly."""
            
            return response
            
        except Exception as e:
            return f"❌ Error sending reboot command: {str(e)}"
    
    
    @app.tool(
        name="get_network_sm_profiles",
        description="📋 List Systems Manager profiles"
    )
    def get_network_sm_profiles(network_id: str):
        """
        List all Systems Manager profiles for a network.
        
        Args:
            network_id: Network ID
            
        Returns:
            List of SM profiles
        """
        try:
            profiles = meraki_client.get_network_sm_profiles(network_id)
            
            if not profiles:
                return f"No SM profiles found in network {network_id}."
                
            result = f"# 📋 Systems Manager Profiles - Network {network_id}\n\n"
            
            for profile in profiles:
                result += f"## {profile.get('name', 'Unnamed Profile')}\n"
                result += f"- **ID**: {profile.get('id')}\n"
                result += f"- **Description**: {profile.get('description', 'No description')}\n"
                result += f"- **Scope**: {profile.get('scope', 'Unknown')}\n"
                
                # Tags targeted
                tags = profile.get('tags', [])
                if tags:
                    result += f"- **Target Tags**: {', '.join(tags)}\n"
                    
                # Payload count
                payloads = profile.get('payloadTypes', [])
                if payloads:
                    result += f"- **Payload Types**: {', '.join(payloads)}\n"
                    
                result += "\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving SM profiles: {str(e)}"
    
    @app.tool(
        name="get_network_sm_performance_history",
        description="📊 Get performance history for an SM device"
    )
    def get_network_sm_performance_history(network_id: str, device_id: str):
        """
        Get performance history for a Systems Manager device.
        
        Args:
            network_id: Network ID
            device_id: Device ID
            
        Returns:
            Device performance metrics over time
        """
        try:
            history = meraki_client.get_network_sm_device_performance_history(network_id, device_id)
            
            if not history:
                return f"No performance history found for device {device_id}."
                
            result = f"# 📊 Performance History - Device {device_id}\n\n"
            
            for entry in history[-10:]:  # Last 10 entries
                timestamp = entry.get('ts', 'Unknown time')
                result += f"## {timestamp}\n"
                
                # CPU usage
                cpu_percent = entry.get('cpuPercentUsed')
                if cpu_percent is not None:
                    cpu_icon = "🟢" if cpu_percent < 50 else "🟡" if cpu_percent < 80 else "🔴"
                    result += f"- **CPU Usage**: {cpu_icon} {cpu_percent}%\n"
                
                # Memory usage
                mem_free = entry.get('memFree', 0)
                mem_active = entry.get('memActive', 0)
                mem_inactive = entry.get('memInactive', 0)
                mem_wired = entry.get('memWired', 0)
                
                if mem_free or mem_active:
                    total_mem = mem_free + mem_active + mem_inactive + mem_wired
                    if total_mem > 0:
                        mem_percent = ((mem_active + mem_wired) / total_mem) * 100
                        mem_icon = "🟢" if mem_percent < 70 else "🟡" if mem_percent < 90 else "🔴"
                        result += f"- **Memory**: {mem_icon} {mem_percent:.1f}% used\n"
                        result += f"  - Free: {mem_free}MB\n"
                        result += f"  - Active: {mem_active}MB\n"
                
                # Disk usage
                disk_usage = entry.get('diskUsage', {})
                if disk_usage:
                    for disk, usage in disk_usage.items():
                        used = usage.get('used', 0)
                        total = usage.get('total', 1)
                        percent = (used / total * 100) if total > 0 else 0
                        disk_icon = "🟢" if percent < 80 else "🟡" if percent < 90 else "🔴"
                        result += f"- **Disk {disk}**: {disk_icon} {percent:.1f}% used\n"
                
                # Network usage
                network_sent = entry.get('networkSent', 0)
                network_recv = entry.get('networkReceived', 0)
                if network_sent or network_recv:
                    result += f"- **Network**: ↑{network_sent}KB ↓{network_recv}KB\n"
                
                result += "\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving performance history: {str(e)}"