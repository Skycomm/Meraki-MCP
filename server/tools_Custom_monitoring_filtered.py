"""
Filtered Enhanced Monitoring tools - ONLY UNIQUE TOOLS (no SDK duplicates).
Contains 6 unique device analytics and monitoring tools not available in SDK.
"""

# Global variables to store app and meraki client
app = None
meraki_client = None

def register_monitoring_tools_filtered(mcp_app, meraki):
    """
    Register ONLY unique monitoring and analytics tools (6 tools).
    Excludes tools that duplicate SDK functionality.
    
    Args:
        mcp_app: MCP server instance
        meraki: Meraki client instance
    """
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    
    # Register only unique device analytics tools
    register_unique_monitoring_tools()

def register_unique_monitoring_tools():
    """Register unique device analytics and monitoring tools (6 tools)."""
    
    @app.tool(
        name="get_device_memory_history",
        description="💾 Get device memory utilization history"
    )
    def get_device_memory_history(device_serial: str, timespan: int = 86400):
        """Get device memory utilization history."""
        try:
            result = meraki_client.dashboard.devices.getDeviceMemoryHistory(
                device_serial, timespan=timespan
            )
            
            response = "# 💾 Device Memory History\\n\\n"
            
            if result and isinstance(result, list):
                response += f"**Memory Data Points**: {len(result)}\\n"
                response += f"**Device Serial**: {device_serial}\\n"
                response += f"**Timespan**: {timespan} seconds\\n\\n"
                
                # Show recent memory utilization
                for idx, entry in enumerate(result[-10:], 1):
                    if isinstance(entry, dict):
                        timestamp = entry.get('ts', 'Unknown')
                        memory_usage = entry.get('memoryUsage', {})
                        
                        response += f"**{idx}. {timestamp}**\\n"
                        if isinstance(memory_usage, dict):
                            total = memory_usage.get('total', 0)
                            used = memory_usage.get('used', 0)
                            free = memory_usage.get('free', 0)
                            usage_percent = (used / total * 100) if total > 0 else 0
                            
                            response += f"   - Total: {total:,} bytes\\n"
                            response += f"   - Used: {used:,} bytes ({usage_percent:.1f}%)\\n"
                            response += f"   - Free: {free:,} bytes\\n"
                        response += "\\n"
                
                if len(result) > 10:
                    response += f"... showing last 10 of {len(result)} data points\\n"
            else:
                response += "*No memory history data available*\\n"
                
            return response
            
        except Exception as e:
            return f"❌ Error getting device memory history: {str(e)}"
    
    @app.tool(
        name="get_device_cpu_power_mode_history",
        description="⚡ Get device CPU power mode history"
    )
    def get_device_cpu_power_mode_history(device_serial: str, timespan: int = 86400):
        """Get device CPU power mode history."""
        try:
            result = meraki_client.dashboard.devices.getDeviceCpuPowerModeHistory(
                device_serial, timespan=timespan
            )
            
            response = "# ⚡ Device CPU Power Mode History\\n\\n"
            
            if result and isinstance(result, list):
                response += f"**CPU Data Points**: {len(result)}\\n"
                response += f"**Device Serial**: {device_serial}\\n"
                response += f"**Timespan**: {timespan} seconds\\n\\n"
                
                # Show recent CPU power modes
                for idx, entry in enumerate(result[-10:], 1):
                    if isinstance(entry, dict):
                        timestamp = entry.get('ts', 'Unknown')
                        cpu_usage = entry.get('cpuUsage', {})
                        power_mode = entry.get('powerMode', 'Unknown')
                        
                        response += f"**{idx}. {timestamp}**\\n"
                        response += f"   - Power Mode: {power_mode}\\n"
                        if isinstance(cpu_usage, dict):
                            usage_percent = cpu_usage.get('percentage', 0)
                            response += f"   - CPU Usage: {usage_percent}%\\n"
                        response += "\\n"
                
                if len(result) > 10:
                    response += f"... showing last 10 of {len(result)} data points\\n"
            else:
                response += "*No CPU power mode history available*\\n"
                
            return response
            
        except Exception as e:
            return f"❌ Error getting CPU power mode history: {str(e)}"
    
    @app.tool(
        name="get_device_wireless_cpu_load",
        description="📡 Get wireless device CPU load metrics"
    )
    def get_device_wireless_cpu_load(device_serial: str, timespan: int = 86400):
        """Get wireless device CPU load metrics."""
        try:
            result = meraki_client.dashboard.wireless.getDeviceWirelessCpuLoad(
                device_serial, timespan=timespan
            )
            
            response = "# 📡 Wireless Device CPU Load\\n\\n"
            
            if result and isinstance(result, list):
                response += f"**CPU Load Data Points**: {len(result)}\\n"
                response += f"**Wireless Device**: {device_serial}\\n"
                response += f"**Timespan**: {timespan} seconds\\n\\n"
                
                # Show recent CPU load data
                for idx, entry in enumerate(result[-10:], 1):
                    if isinstance(entry, dict):
                        timestamp = entry.get('ts', 'Unknown')
                        cpu_load = entry.get('cpuLoad', {})
                        
                        response += f"**{idx}. {timestamp}**\\n"
                        if isinstance(cpu_load, dict):
                            avg_load = cpu_load.get('average', 0)
                            max_load = cpu_load.get('maximum', 0)
                            response += f"   - Average Load: {avg_load}%\\n"
                            response += f"   - Maximum Load: {max_load}%\\n"
                        response += "\\n"
                
                if len(result) > 10:
                    response += f"... showing last 10 of {len(result)} data points\\n"
            else:
                response += "*No wireless CPU load data available*\\n"
                
            return response
            
        except Exception as e:
            return f"❌ Error getting wireless CPU load: {str(e)}"
    
    @app.tool(
        name="get_organization_switch_ports_history",
        description="🔌 Get organization switch ports usage history"
    )
    def get_organization_switch_ports_history(organization_id: str, timespan: int = 86400, per_page: int = 1000):
        """Get organization switch ports usage history."""
        try:
            result = meraki_client.dashboard.switch.getOrganizationSwitchPortsHistory(
                organization_id, timespan=timespan, perPage=min(per_page, 1000)
            )
            
            response = "# 🔌 Organization Switch Ports History\\n\\n"
            
            if result and isinstance(result, list):
                response += f"**Switch Port Records**: {len(result)}\\n"
                response += f"**Organization**: {organization_id}\\n"
                response += f"**Timespan**: {timespan} seconds\\n\\n"
                
                # Group by switch and show port statistics
                switch_data = {}
                for entry in result:
                    if isinstance(entry, dict):
                        switch_serial = entry.get('serial', 'Unknown')
                        if switch_serial not in switch_data:
                            switch_data[switch_serial] = []
                        switch_data[switch_serial].append(entry)
                
                for idx, (switch_serial, ports) in enumerate(list(switch_data.items())[:5], 1):
                    response += f"**{idx}. Switch {switch_serial}**\\n"
                    response += f"   - Ports Monitored: {len(ports)}\\n"
                    
                    # Show port activity summary
                    active_ports = sum(1 for p in ports if p.get('status') == 'active')
                    response += f"   - Active Ports: {active_ports}/{len(ports)}\\n"
                    response += "\\n"
                
                if len(switch_data) > 5:
                    response += f"... and {len(switch_data)-5} more switches\\n"
            else:
                response += "*No switch port history available*\\n"
                
            return response
            
        except Exception as e:
            return f"❌ Error getting switch ports history: {str(e)}"
    
    @app.tool(
        name="get_organization_devices_migration_status",
        description="🔄 Get organization devices migration status"
    )
    def get_organization_devices_migration_status(organization_id: str):
        """Get organization devices migration status."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationDevicesMigrationStatus(
                organization_id
            )
            
            response = "# 🔄 Organization Devices Migration Status\\n\\n"
            
            if result and isinstance(result, list):
                response += f"**Devices in Migration**: {len(result)}\\n"
                response += f"**Organization**: {organization_id}\\n\\n"
                
                # Show migration status by category
                status_counts = {}
                for device in result:
                    if isinstance(device, dict):
                        status = device.get('migrationStatus', 'Unknown')
                        status_counts[status] = status_counts.get(status, 0) + 1
                
                response += "**Migration Status Summary**\\n"
                for status, count in status_counts.items():
                    response += f"- {status}: {count} devices\\n"
                
                response += "\\n**Device Details**\\n"
                for idx, device in enumerate(result[:10], 1):
                    if isinstance(device, dict):
                        serial = device.get('serial', 'Unknown')
                        status = device.get('migrationStatus', 'Unknown')
                        model = device.get('model', 'Unknown')
                        
                        response += f"**{idx}. {serial}**\\n"
                        response += f"   - Model: {model}\\n"
                        response += f"   - Status: {status}\\n"
                        if 'migrationDate' in device:
                            response += f"   - Migration Date: {device['migrationDate']}\\n"
                        response += "\\n"
                
                if len(result) > 10:
                    response += f"... and {len(result)-10} more devices\\n"
            else:
                response += "*No devices currently migrating*\\n"
                
            return response
            
        except Exception as e:
            return f"❌ Error getting migration status: {str(e)}"
    
    @app.tool(
        name="get_organization_api_usage",
        description="📊 Get organization API usage statistics"
    )
    def get_organization_api_usage(organization_id: str, timespan: int = 86400):
        """Get organization API usage statistics."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationApiUsage(
                organization_id, timespan=timespan
            )
            
            response = "# 📊 Organization API Usage\\n\\n"
            
            if result and isinstance(result, list):
                response += f"**API Usage Records**: {len(result)}\\n"
                response += f"**Organization**: {organization_id}\\n"
                response += f"**Timespan**: {timespan} seconds\\n\\n"
                
                # Calculate totals
                total_requests = sum(entry.get('requestCount', 0) for entry in result if isinstance(entry, dict))
                
                response += f"**Total API Requests**: {total_requests:,}\\n\\n"
                
                # Show recent usage patterns
                for idx, entry in enumerate(result[-10:], 1):
                    if isinstance(entry, dict):
                        timestamp = entry.get('ts', 'Unknown')
                        request_count = entry.get('requestCount', 0)
                        response_time = entry.get('averageResponseTime', 0)
                        
                        response += f"**{idx}. {timestamp}**\\n"
                        response += f"   - Requests: {request_count:,}\\n"
                        response += f"   - Avg Response Time: {response_time:.2f}ms\\n"
                        response += "\\n"
                
                if len(result) > 10:
                    response += f"... showing last 10 of {len(result)} records\\n"
            else:
                response += "*No API usage data available*\\n"
                
            return response
            
        except Exception as e:
            return f"❌ Error getting API usage: {str(e)}"