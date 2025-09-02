"""
Enhanced Monitoring tools for the Cisco Meraki MCP Server - ONLY REAL API METHODS.
New 2025 features including device memory, CPU monitoring, and migration status.
"""

# Global variables to store app and meraki client
app = None
meraki_client = None

def register_monitoring_tools(mcp_app, meraki):
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    """
    Register enhanced monitoring tools with the MCP server.
    
    Args:
        mcp_app: MCP server instance
        meraki: Meraki client instance
    """
    
    # Register all monitoring tools
    register_monitoring_tool_handlers()

def register_monitoring_tool_handlers():
    """Register all enhanced monitoring tool handlers using ONLY REAL API methods."""
    
    @app.tool(
        name="get_device_memory_history",
        description="💾 Get device memory utilization history (2025 feature)"
    )
    def get_device_memory_history(serial: str, timespan: int = 3600):
        """
        Get memory utilization history for a device.
        
        Args:
            serial: Device serial number
            timespan: Time span in seconds (default 1 hour)
            
        Returns:
            Memory utilization history
        """
        try:
            history = meraki_client.get_device_memory_history(serial, timespan=timespan)
            
            if not history:
                return f"No memory history available for device {serial}."
                
            result = f"# 💾 Memory History - Device {serial}\n\n"
            result += f"**Time Period**: Last {timespan/3600:.1f} hours\n\n"
            
            # Show recent data points
            for entry in history[-10:]:
                timestamp = entry.get('ts', 'Unknown')
                used_mb = entry.get('memoryUsedMb', 0)
                total_mb = entry.get('memoryTotalMb', 1)
                percent = (used_mb / total_mb * 100) if total_mb > 0 else 0
                
                # Status icon based on usage
                icon = "🟢" if percent < 70 else "🟡" if percent < 90 else "🔴"
                
                result += f"## {timestamp}\n"
                result += f"- **Usage**: {icon} {percent:.1f}% ({used_mb}MB / {total_mb}MB)\n"
                result += f"- **Free**: {total_mb - used_mb}MB\n\n"
            
            # Calculate average
            if history:
                avg_percent = sum((e.get('memoryUsedMb', 0) / e.get('memoryTotalMb', 1) * 100) 
                                for e in history if e.get('memoryTotalMb', 0) > 0) / len(history)
                result += f"### Average Usage: {avg_percent:.1f}%\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving memory history: {str(e)}"
    
    @app.tool(
        name="get_device_cpu_power_mode_history",
        description="⚡ Get wireless device CPU power mode history (2025 feature)"
    )
    def get_device_cpu_power_mode_history(serial: str, timespan: int = 3600):
        """
        Get CPU power mode history for a wireless device.
        
        Args:
            serial: Device serial number
            timespan: Time span in seconds (default 1 hour)
            
        Returns:
            CPU power mode history
        """
        try:
            history = meraki_client.get_device_cpu_power_mode_history(serial, timespan=timespan)
            
            if not history:
                return f"No CPU power mode history available for device {serial}."
                
            result = f"# ⚡ CPU Power Mode History - Device {serial}\n\n"
            result += f"**Time Period**: Last {timespan/3600:.1f} hours\n\n"
            
            # Count modes
            mode_counts = {}
            for entry in history:
                mode = entry.get('powerMode', 'unknown')
                mode_counts[mode] = mode_counts.get(mode, 0) + 1
            
            result += "## Power Mode Distribution\n"
            for mode, count in mode_counts.items():
                percent = (count / len(history) * 100) if history else 0
                icon = "🟢" if mode == 'low' else "🟡" if mode == 'medium' else "🔴"
                result += f"- **{mode.title()}**: {icon} {percent:.1f}% ({count} samples)\n"
            
            result += f"\n## Recent History\n"
            for entry in history[-10:]:
                timestamp = entry.get('ts', 'Unknown')
                mode = entry.get('powerMode', 'unknown')
                icon = "🟢" if mode == 'low' else "🟡" if mode == 'medium' else "🔴"
                
                result += f"- {timestamp}: {icon} {mode}\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving CPU power mode history: {str(e)}"
    
    @app.tool(
        name="get_device_wireless_cpu_load",
        description="📊 Get wireless device CPU load monitoring (2025 feature)"
    )
    def get_device_wireless_cpu_load(serial: str):
        """
        Get current CPU load for a wireless device.
        
        Args:
            serial: Device serial number
            
        Returns:
            Current CPU load information
        """
        try:
            cpu_load = meraki_client.get_device_wireless_cpu_load(serial)
            
            result = f"# 📊 CPU Load - Wireless Device {serial}\n\n"
            
            # Overall CPU load
            overall = cpu_load.get('overall', {})
            if overall:
                load_percent = overall.get('percentage', 0)
                icon = "🟢" if load_percent < 50 else "🟡" if load_percent < 80 else "🔴"
                
                result += f"## Overall CPU Load\n"
                result += f"- **Current Load**: {icon} {load_percent}%\n"
                result += f"- **1 Min Average**: {overall.get('avg1Min', 0)}%\n"
                result += f"- **5 Min Average**: {overall.get('avg5Min', 0)}%\n"
                result += f"- **15 Min Average**: {overall.get('avg15Min', 0)}%\n\n"
            
            # Per-core information
            cores = cpu_load.get('perCore', [])
            if cores:
                result += f"## Per-Core Load ({len(cores)} cores)\n"
                for i, core in enumerate(cores):
                    core_percent = core.get('percentage', 0)
                    icon = "🟢" if core_percent < 50 else "🟡" if core_percent < 80 else "🔴"
                    result += f"- **Core {i}**: {icon} {core_percent}%\n"
            
            # Process information
            top_processes = cpu_load.get('topProcesses', [])
            if top_processes:
                result += f"\n## Top Processes\n"
                for proc in top_processes[:5]:
                    result += f"- **{proc.get('name', 'Unknown')}**: {proc.get('cpuPercentage', 0)}%\n"
                    
            return result
            
        except Exception as e:
            return f"Error retrieving CPU load: {str(e)}"
    
    @app.tool(
        name="get_organization_switch_ports_history",
        description="🔌 Get organization-wide switch port history (2025 feature)"
    )
    def get_organization_switch_ports_history(org_id: str, timespan: int = 3600):
        """
        Get aggregated switch port statistics history for entire organization.
        
        Args:
            org_id: Organization ID
            timespan: Time span in seconds (default 1 hour)
            
        Returns:
            Organization-wide switch port history
        """
        try:
            history = meraki_client.get_organization_switch_ports_history(org_id, timespan=timespan)
            
            if not history:
                return f"No switch port history available for organization {org_id}."
                
            result = f"# 🔌 Organization Switch Ports History - Org {org_id}\n\n"
            result += f"**Time Period**: Last {timespan/3600:.1f} hours\n\n"
            
            # Aggregate statistics
            total_ports = 0
            active_ports = 0
            error_ports = 0
            
            for entry in history:
                stats = entry.get('stats', {})
                total_ports = max(total_ports, stats.get('totalPorts', 0))
                active_ports = max(active_ports, stats.get('activePorts', 0))
                error_ports = max(error_ports, stats.get('errorPorts', 0))
            
            result += f"## Summary\n"
            result += f"- **Total Ports**: {total_ports}\n"
            result += f"- **Active Ports**: {active_ports} ({(active_ports/total_ports*100) if total_ports else 0:.1f}%)\n"
            result += f"- **Error Ports**: {error_ports}\n\n"
            
            # Recent history
            result += f"## Recent Activity\n"
            for entry in history[-10:]:
                timestamp = entry.get('ts', 'Unknown')
                stats = entry.get('stats', {})
                
                result += f"### {timestamp}\n"
                result += f"- Active: {stats.get('activePorts', 0)}/{stats.get('totalPorts', 0)}\n"
                result += f"- Errors: {stats.get('errorPorts', 0)}\n"
                result += f"- Power Usage: {stats.get('totalPowerWatts', 0)}W\n\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving switch ports history: {str(e)}"
    
    @app.tool(
        name="get_organization_devices_migration_status",
        description="🔄 Get device migration status across organization (2025 feature)"
    )
    def get_organization_devices_migration_status(org_id: str):
        """
        Get migration status for devices being migrated in the organization.
        
        Args:
            org_id: Organization ID
            
        Returns:
            Device migration status
        """
        try:
            migrations = meraki_client.get_organization_devices_migration_status(org_id)
            
            if not migrations:
                return f"No device migrations in progress for organization {org_id}."
                
            result = f"# 🔄 Device Migration Status - Org {org_id}\n\n"
            result += f"**Total Migrations**: {len(migrations)}\n\n"
            
            # Group by status
            status_groups = {}
            for migration in migrations:
                status = migration.get('status', 'unknown')
                if status not in status_groups:
                    status_groups[status] = []
                status_groups[status].append(migration)
            
            # Display by status
            for status, devices in status_groups.items():
                icon = "✅" if status == 'completed' else "🔄" if status == 'in_progress' else "⚠️"
                result += f"## {icon} {status.title()} ({len(devices)} devices)\n"
                
                for device in devices[:5]:
                    serial = device.get('serial', 'Unknown')
                    name = device.get('name', 'Unnamed')
                    from_network = device.get('fromNetwork', {}).get('name', 'Unknown')
                    to_network = device.get('toNetwork', {}).get('name', 'Unknown')
                    
                    result += f"### {name} ({serial})\n"
                    result += f"- **From**: {from_network}\n"
                    result += f"- **To**: {to_network}\n"
                    
                    # Progress percentage
                    progress = device.get('progressPercent')
                    if progress is not None:
                        progress_bar = "█" * (progress // 10) + "░" * (10 - progress // 10)
                        result += f"- **Progress**: [{progress_bar}] {progress}%\n"
                    
                    # Start time
                    started = device.get('startedAt')
                    if started:
                        result += f"- **Started**: {started}\n"
                    
                    result += "\n"
                
                if len(devices) > 5:
                    result += f"... and {len(devices) - 5} more {status} migrations\n\n"
                    
            return result
            
        except Exception as e:
            return f"Error retrieving migration status: {str(e)}"
    
    @app.tool(
        name="get_network_events",
        description="📋 Get network events (TIP: Specify product_type for multi-device networks: appliance/switch/wireless/camera)"
    )
    def get_network_events(network_id: str, product_type: str = None, event_types: str = None, 
                          per_page: int = 1000, timespan: int = 86400):
        """
        Get network events including port status changes.
        
        Args:
            network_id: Network ID
            product_type: Filter by product type (appliance, switch, wireless, etc.)
            event_types: Comma-separated event types to filter (e.g. 'port_carrier_change')
            per_page: Number of events per page (max 1000)
            timespan: Time span in seconds (default 24 hours)
            
        Returns:
            Network events with focus on port changes
        """
        try:
            kwargs = {
                'perPage': per_page,
                'timespan': timespan
            }
            
            if product_type:
                kwargs['productType'] = product_type
            if event_types:
                kwargs['includedEventTypes'] = event_types.split(',')
            
            # Try to get events without productType first
            try:
                events = meraki_client.dashboard.networks.getNetworkEvents(network_id, **kwargs)
            except Exception as e:
                error_msg = str(e)
                # Check if productType is required
                if 'productType' in error_msg or 'multiple device types' in error_msg:
                    # Try to detect network types
                    try:
                        network_info = meraki_client.dashboard.networks.getNetwork(network_id)
                        product_types = network_info.get('productTypes', [])
                        
                        if not product_types:
                            # Try to detect from devices
                            devices = meraki_client.dashboard.networks.getNetworkDevices(network_id)
                            detected_types = set()
                            for device in devices:
                                model = device.get('model', '')
                                if model.startswith('MX'):
                                    detected_types.add('appliance')
                                elif model.startswith('MS'):
                                    detected_types.add('switch')
                                elif model.startswith('MR'):
                                    detected_types.add('wireless')
                                elif model.startswith('MV'):
                                    detected_types.add('camera')
                            product_types = list(detected_types)
                        
                        if product_types:
                            return ("❌ Network has multiple device types. Please specify product_type parameter:\n"
                                   f"Available types: {', '.join(product_types)}\n\n"
                                   "💡 Examples:\n"
                                   f"  • get_network_events('{network_id}', product_type='wireless')\n"
                                   f"  • get_network_events('{network_id}', product_type='switch')\n"
                                   f"  • get_network_events('{network_id}', product_type='appliance')")
                    except:
                        pass
                    
                    return ("❌ This network requires productType parameter.\n"
                           "Common values: appliance, switch, wireless, camera\n\n"
                           "💡 Try: get_network_events(network_id, product_type='wireless')")
                else:
                    raise  # Re-raise original error
            
            if not events:
                return f"No events found for network {network_id} in the last {timespan/3600:.0f} hours."
                
            result = f"# 📋 Network Events - Network {network_id}\n\n"
            result += f"**Time Period**: Last {timespan/3600:.0f} hours\n"
            result += f"**Total Events**: {len(events)}\n\n"
            
            # Group events by type
            event_groups = {}
            for event in events:
                event_type = event.get('type', 'unknown')
                if event_type not in event_groups:
                    event_groups[event_type] = []
                event_groups[event_type].append(event)
            
            # Show port carrier changes first if any
            if 'port_carrier_change' in event_groups:
                port_events = event_groups['port_carrier_change']
                result += f"## 🔌 Port Carrier Changes ({len(port_events)} events)\n"
                
                for event in port_events[:20]:  # Show latest 20
                    timestamp = event.get('occurredAt', 'Unknown')
                    device_name = event.get('deviceName', 'Unknown')
                    device_serial = event.get('deviceSerial', 'Unknown')
                    details = event.get('eventData', {})
                    
                    port_num = details.get('port', 'Unknown')
                    carrier_status = details.get('status', 'Unknown')
                    icon = "🟢" if carrier_status == 'up' else "🔴"
                    
                    result += f"### {timestamp}\n"
                    result += f"- **Device**: {device_name} ({device_serial})\n"
                    result += f"- **Port**: {port_num}\n"
                    result += f"- **Status**: {icon} {carrier_status}\n"
                    
                    # Add additional details if available
                    if details.get('speed'):
                        result += f"- **Speed**: {details['speed']}\n"
                    if details.get('duplex'):
                        result += f"- **Duplex**: {details['duplex']}\n"
                    
                    result += "\n"
                
                if len(port_events) > 20:
                    result += f"... and {len(port_events) - 20} more port carrier changes\n\n"
            
            # Show other event types
            for event_type, events_list in event_groups.items():
                if event_type == 'port_carrier_change':
                    continue  # Already shown
                    
                # Map event types to friendly names and icons
                event_icons = {
                    'vpn_connectivity_change': '🔐',
                    'appliance_went_down': '🔴',
                    'appliance_came_up': '🟢',
                    'client_connected': '📱',
                    'client_disconnected': '📴',
                    'config_change': '⚙️',
                    'dhcp_issue': '⚠️'
                }
                
                icon = event_icons.get(event_type, '📄')
                result += f"\n## {icon} {event_type.replace('_', ' ').title()} ({len(events_list)} events)\n"
                
                for event in events_list[:5]:  # Show latest 5 of each type
                    timestamp = event.get('occurredAt', 'Unknown')
                    device_name = event.get('deviceName', '')
                    description = event.get('description', event.get('type', 'Unknown event'))
                    
                    result += f"- **{timestamp}**: {description}\n"
                    if device_name:
                        result += f"  - Device: {device_name}\n"
                    
                if len(events_list) > 5:
                    result += f"... and {len(events_list) - 5} more {event_type} events\n"
                    
            return result
            
        except Exception as e:
            return f"Error retrieving network events: {str(e)}"
    
    @app.tool(
        name="get_organization_api_usage",
        description="📈 Get API usage analytics for the organization"
    )
    def get_organization_api_usage(org_id: str, timespan: int = 86400):
        """
        Get API usage statistics for monitoring API consumption.
        
        Args:
            org_id: Organization ID
            timespan: Time span in seconds (default 24 hours)
            
        Returns:
            API usage analytics
        """
        try:
            usage = meraki_client.get_organization_api_requests(org_id, timespan=timespan)
            
            if not usage:
                return f"No API usage data available for organization {org_id}."
                
            result = f"# 📈 API Usage Analytics - Org {org_id}\n\n"
            result += f"**Time Period**: Last {timespan/3600:.0f} hours\n"
            result += f"**Total Requests**: {len(usage)}\n\n"
            
            # Group by admin
            admin_usage = {}
            for req in usage:
                admin = req.get('adminId', 'Unknown')
                if admin not in admin_usage:
                    admin_usage[admin] = 0
                admin_usage[admin] += 1
            
            result += "## Usage by Admin\n"
            for admin, count in sorted(admin_usage.items(), key=lambda x: x[1], reverse=True)[:5]:
                result += f"- **{admin}**: {count} requests\n"
            
            # Group by path
            path_usage = {}
            for req in usage:
                path = req.get('path', 'Unknown')
                # Simplify path to endpoint
                path_parts = path.split('/')
                if len(path_parts) > 3:
                    endpoint = f"/{path_parts[1]}/{path_parts[2]}/..."
                else:
                    endpoint = path
                    
                if endpoint not in path_usage:
                    path_usage[endpoint] = 0
                path_usage[endpoint] += 1
            
            result += "\n## Top Endpoints\n"
            for endpoint, count in sorted(path_usage.items(), key=lambda x: x[1], reverse=True)[:10]:
                result += f"- **{endpoint}**: {count} requests\n"
            
            # Response codes
            response_codes = {}
            for req in usage:
                code = req.get('responseCode', 0)
                if code not in response_codes:
                    response_codes[code] = 0
                response_codes[code] += 1
            
            result += "\n## Response Codes\n"
            for code, count in sorted(response_codes.items()):
                icon = "✅" if 200 <= code < 300 else "⚠️" if 400 <= code < 500 else "🔴"
                result += f"- **{code}**: {icon} {count} responses\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving API usage: {str(e)}"