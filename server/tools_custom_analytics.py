"""
Network Analytics and Monitoring tools for the Cisco Meraki MCP Server - ONLY REAL API METHODS.
"""

# Global variables to store app and meraki client
app = None
meraki_client = None

def register_analytics_tools(mcp_app, meraki):
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    """
    Register analytics and monitoring tools with the MCP server.
    
    Args:
        mcp_app: MCP server instance
        meraki: Meraki client instance
    """
    
    # Register all analytics tools
    register_analytics_tool_handlers()

def register_analytics_tool_handlers():
    """Register all analytics and monitoring tool handlers using ONLY REAL API methods."""
    
    @app.tool(
        name="get_organization_uplinks_loss_and_latency", 
        description="🚨 Monitor packet loss & latency - detect DDoS attacks, ISP issues, network degradation across all sites"
    )
    def get_organization_uplinks_loss_and_latency(organization_id: str, timespan: int = 300):
        """
        Get REAL packet loss and latency data for all uplinks in organization.
        
        Args:
            organization_id: Organization ID
            timespan: Timespan in seconds (default: 300 = 5 minutes, max: 300)
            
        Returns:
            Formatted uplink loss and latency data
        """
        try:
            # Validate and ensure timespan doesn't exceed API limit
            if not isinstance(timespan, (int, float)):
                return "❌ Error: timespan must be a number (seconds)"
            
            if timespan <= 0:
                return "❌ Error: timespan must be positive"
                
            if timespan > 300:
                timespan = 300
                # Note: API limit is 300 seconds (5 minutes)
                
            loss_latency = meraki_client.dashboard.organizations.getOrganizationDevicesUplinksLossAndLatency(organization_id, timespan=timespan)
            
            if not loss_latency:
                return f"No uplink loss/latency data found for organization {organization_id}."
            
            # Build result
            result = f"# 🚨 UPLINK LOSS & LATENCY REPORT\n\n"
            result += f"**Organization**: {organization_id}\n"
            result += f"**Time Period**: Last {timespan//60} minutes\n"
            result += f"**Total Uplinks**: {len(loss_latency)}\n\n"
            
            # Group by device serial for easier reading
            devices = {}
            for entry in loss_latency:
                serial = entry.get('serial', 'Unknown')
                if serial not in devices:
                    devices[serial] = {
                        'network_id': entry.get('networkId', 'Unknown'),
                        'uplinks': []
                    }
                devices[serial]['uplinks'].append(entry)
            
            # Format output by device
            for serial, device_data in devices.items():
                result += f"## 📱 Device: {serial}\n"
                result += f"Network: {device_data['network_id']}\n\n"
                
                for uplink in device_data['uplinks']:
                    uplink_name = uplink.get('uplink', 'Unknown')
                    ip = uplink.get('ip', 'N/A')
                    
                    # Check if uplink_name exists before calling upper()
                    if uplink_name:
                        result += f"### 🔗 {uplink_name.upper()} ({ip})\n"
                    else:
                        result += f"### 🔗 Unknown Uplink ({ip})\n"
                    
                    # Get time series data
                    time_series = uplink.get('timeSeries', [])
                    
                    if time_series:
                        # Get latest reading
                        latest = time_series[-1]
                        current_loss = latest.get('lossPercent', 0)
                        current_latency = latest.get('latencyMs', 0)
                        
                        # Calculate statistics
                        losses = [p.get('lossPercent', 0) for p in time_series if p.get('lossPercent') is not None]
                        latencies = [p.get('latencyMs', 0) for p in time_series if p.get('latencyMs') is not None]
                        
                        if losses:
                            avg_loss = sum(losses) / len(losses)
                            max_loss = max(losses)
                            min_loss = min(losses)
                        else:
                            avg_loss = max_loss = min_loss = 0
                            
                        if latencies:
                            avg_latency = sum(latencies) / len(latencies)
                            max_latency = max(latencies)
                            min_latency = min(latencies)
                        else:
                            avg_latency = max_latency = min_latency = 0
                        
                        # Current status with indicators
                        loss_indicator = "🔴" if current_loss > 5 else "🟡" if current_loss > 1 else "🟢"
                        latency_indicator = "🔴" if current_latency > 150 else "🟡" if current_latency > 50 else "🟢"
                        
                        result += f"**Current Status:**\n"
                        result += f"- Packet Loss: {current_loss:.1f}% {loss_indicator}\n"
                        result += f"- Latency: {current_latency:.0f}ms {latency_indicator}\n\n"
                        
                        result += f"**5-Minute Statistics:**\n"
                        result += f"- Avg Loss: {avg_loss:.1f}% (Min: {min_loss:.1f}%, Max: {max_loss:.1f}%)\n"
                        result += f"- Avg Latency: {avg_latency:.0f}ms (Min: {min_latency:.0f}ms, Max: {max_latency:.0f}ms)\n"
                        result += f"- Data Points: {len(time_series)}\n\n"
                        
                        # Show last 5 readings
                        result += f"**Recent Readings:**\n"
                        for reading in time_series[-5:]:
                            ts = reading.get('ts', 'Unknown').split('T')[1].split('Z')[0]
                            loss = reading.get('lossPercent', 0)
                            lat = reading.get('latencyMs', 0)
                            result += f"- {ts}: Loss={loss:.1f}%, Latency={lat:.0f}ms\n"
                        
                        # Alert on issues
                        if avg_loss > 1:
                            result += f"\n⚠️ **WARNING**: Average packet loss above 1%!\n"
                        if avg_latency > 100:
                            result += f"\n⚠️ **WARNING**: High average latency detected!\n"
                            
                    else:
                        result += "- **Status**: No data available\n"
                    
                    result += "\n"
                    
            return result
            
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            return f"Error retrieving uplink loss/latency data:\n{str(e)}\n\nDetails:\n{error_details}"

    @app.tool(
        name="get_organization_appliance_uplink_statuses",
        description="🔗 Get REAL uplink status for all appliances in organization"
    )
    def get_organization_appliance_uplink_statuses(organization_id: str):
        """
        Get REAL uplink status for all appliances in organization.
        
        Args:
            organization_id: Organization ID
            
        Returns:
            Formatted appliance uplink status data
        """
        try:
            uplink_statuses = meraki_client.dashboard.appliance.getOrganizationApplianceUplinkStatuses(organization_id)
            
            if not uplink_statuses:
                return f"No appliance uplink status data found for organization {organization_id}."
                
            result = f"# 🔗 APPLIANCE UPLINK STATUS - Organization {organization_id}\n\n"
            
            # Group by network
            networks = {}
            for status in uplink_statuses:
                network_id = status.get('networkId', 'Unknown')
                network_name = status.get('networkName', network_id)
                if network_name not in networks:
                    networks[network_name] = []
                networks[network_name].append(status)
            
            for network_name, statuses in networks.items():
                result += f"## 🌐 {network_name}\n"
                
                for status in statuses:
                    serial = status.get('serial', 'Unknown')
                    model = status.get('model', 'Unknown')
                    result += f"### 📱 {model} ({serial})\n"
                    
                    uplinks = status.get('uplinks', [])
                    if not uplinks:
                        result += "- **Status**: No uplink data available\n"
                        continue
                        
                    for uplink in uplinks:
                        interface = uplink.get('interface', 'Unknown')
                        uplink_status = uplink.get('status', 'Unknown')
                        
                        # Status indicators
                        if uplink_status.lower() == 'active':
                            status_icon = "✅"
                        elif uplink_status.lower() == 'ready':
                            status_icon = "🟡"
                        elif uplink_status.lower() in ['failed', 'down']:
                            status_icon = "❌"
                        else:
                            status_icon = "⚠️"
                            
                        result += f"#### 🔗 {interface}: {uplink_status} {status_icon}\n"
                        
                        if uplink.get('ip'):
                            result += f"- **IP**: {uplink['ip']}\n"
                        if uplink.get('gateway'):
                            result += f"- **Gateway**: {uplink['gateway']}\n"
                        if uplink.get('publicIp'):
                            result += f"- **Public IP**: {uplink['publicIp']}\n"
                        if uplink.get('dns'):
                            result += f"- **DNS**: {uplink['dns']}\n"
                        if uplink.get('usingStaticIp'):
                            result += f"- **Static IP**: {uplink['usingStaticIp']}\n"
                        
                        result += "\n"
                        
            return result
            
        except Exception as e:
            error_msg = str(e)
            
            if "404" in error_msg:
                return f"""❌ Error: Organization not found or API not accessible.
                
Organization ID: {org_id}

Possible causes:
- Invalid organization ID
- No API access to this organization
- Organization doesn't have appliances
- API endpoint not available for your license"""
            elif "403" in error_msg:
                return f"""❌ Error: Permission denied.

Possible causes:
- API key doesn't have permission for this organization
- Feature not available for your license tier"""
            else:
                return f"❌ Error retrieving appliance uplink statuses: {error_msg}"

    @app.tool(
        name="get_network_connection_stats",
        description="📊 Get REAL network connection statistics"
    )
    def get_network_connection_stats(network_id: str, timespan: int = 86400):
        """
        Get REAL network connection statistics.
        
        Args:
            network_id: Network ID
            timespan: Timespan in seconds (default: 86400 = 24 hours)
            
        Returns:
            Formatted connection statistics
        """
        try:
            conn_stats = meraki_client.get_network_connection_stats(network_id, timespan)
            
            if not conn_stats:
                return f"No connection statistics found for network {network_id}."
                
            result = f"# 📊 Connection Statistics for Network {network_id}\n\n"
            result += f"**Time Period**: Last {timespan/3600:.1f} hours\n\n"
            
            # Handle both dict and list responses
            if isinstance(conn_stats, dict):
                # Single summary object
                result += f"## Summary Statistics\n"
                result += f"- **Total Associations**: {conn_stats.get('assoc', 0)}\n"
                result += f"- **Successful Authentications**: {conn_stats.get('auth', 0)}\n"
                result += f"- **DHCP Success**: {conn_stats.get('dhcp', 0)}\n"
                result += f"- **DNS Success**: {conn_stats.get('dns', 0)}\n"
                result += f"- **Overall Success**: {conn_stats.get('success', 0)}\n"
                
                # Check if all values are zero
                total_activity = sum([
                    conn_stats.get('assoc', 0),
                    conn_stats.get('auth', 0),
                    conn_stats.get('dhcp', 0),
                    conn_stats.get('dns', 0),
                    conn_stats.get('success', 0)
                ])
                
                if total_activity == 0:
                    result += f"\n📌 **Note**: No wireless client activity in the specified time period.\n"
                    result += "This could mean:\n"
                    result += "- No wireless clients connected\n"
                    result += "- All clients are wired\n"
                    result += "- The network is idle\n"
                    result += "- Try a longer timespan for more data\n"
                else:
                    # Calculate success rate if possible
                    if conn_stats.get('assoc', 0) > 0:
                        success_rate = (conn_stats.get('success', 0) / conn_stats.get('assoc', 0)) * 100
                        result += f"- **Success Rate**: {success_rate:.1f}%\n"
                        
                        if success_rate < 95:
                            result += f"\n⚠️ **WARNING**: Success rate below 95%!\n"
                        
            elif isinstance(conn_stats, list):
                # Time series data
                for entry in conn_stats:
                    result += f"## {entry.get('startTs', 'Unknown Time')}\n"
                    result += f"- **Successful Connections**: {entry.get('assoc', 'N/A')}\n"
                    result += f"- **Authentication Failures**: {entry.get('authFailures', 'N/A')}\n"
                    result += f"- **DHCP Failures**: {entry.get('dhcpFailures', 'N/A')}\n"
                    result += f"- **DNS Failures**: {entry.get('dnsFailures', 'N/A')}\n"
                    result += f"- **Success Rate**: {entry.get('successRate', 'N/A')}%\n"
                    result += "\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving connection statistics: {str(e)}"
    
    @app.tool(
        name="get_network_latency_stats",
        description="⚡ Get REAL network latency statistics"
    )
    def get_network_latency_stats(network_id: str, timespan: int = 86400):
        """
        Get REAL network latency statistics.
        
        Args:
            network_id: Network ID
            timespan: Timespan in seconds (default: 86400 = 24 hours)
            
        Returns:
            Formatted latency statistics
        """
        try:
            latency_data = meraki_client.get_network_latency_stats(network_id, timespan)
            
            if not latency_data:
                return f"No latency statistics found for network {network_id}."
                
            result = f"# ⚡ Network Latency Statistics for {network_id}\n\n"
            result += f"**Time Period**: Last {timespan/3600:.1f} hours\n\n"
            
            for entry in latency_data:
                result += f"## {entry.get('startTs', 'Unknown Time')}\n"
                result += f"- **Average Latency**: {entry.get('avgLatencyMs', 'N/A')} ms\n"
                result += f"- **Loss Percentage**: {entry.get('lossPercent', 'N/A')}%\n"
                result += f"- **Jitter**: {entry.get('jitterMs', 'N/A')} ms\n"
                if entry.get('uplink'):
                    result += f"- **Uplink**: {entry['uplink']}\n"
                result += "\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving latency statistics: {str(e)}"