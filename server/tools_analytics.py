"""
Network Analytics and Monitoring tools for the Cisco Meraki MCP Server - ONLY REAL API METHODS.
"""

# Global variables to store app and meraki client
app = None
meraki_client = None

def register_analytics_tools(mcp_app, meraki):
    """
    Register analytics and monitoring tools with the MCP server.
    
    Args:
        mcp_app: MCP server instance
        meraki: Meraki client instance
    """
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    
    # Register all analytics tools
    register_analytics_tool_handlers()

def register_analytics_tool_handlers():
    """Register all analytics and monitoring tool handlers using ONLY REAL API methods."""
    
    @app.tool(
        name="get_organization_uplinks_loss_and_latency", 
        description="🚨 Get REAL packet loss and latency for all organization uplinks"
    )
    def get_organization_uplinks_loss_and_latency(org_id: str, timespan: int = 300):
        """
        Get REAL packet loss and latency data for all uplinks in organization.
        
        Args:
            org_id: Organization ID
            timespan: Timespan in seconds (default: 300 = 5 minutes, max: 300)
            
        Returns:
            Formatted uplink loss and latency data
        """
        try:
            loss_latency = meraki_client.get_organization_devices_uplinks_loss_and_latency(org_id, timespan)
            
            if not loss_latency:
                return f"No uplink loss/latency data found for organization {org_id}."
                
            result = f"# 🚨 UPLINK LOSS & LATENCY REPORT - Organization {org_id}\n\n"
            result += f"**Time Period**: Last {timespan/3600:.1f} hours\n\n"
            
            # Group by network and device
            networks = {}
            for entry in loss_latency:
                network_id = entry.get('networkId', 'Unknown')
                if network_id not in networks:
                    networks[network_id] = {'devices': {}}
                
                serial = entry.get('serial', 'Unknown')
                if serial not in networks[network_id]['devices']:
                    networks[network_id]['devices'][serial] = []
                
                networks[network_id]['devices'][serial].append(entry)
            
            # Format the output
            for network_id, network_data in networks.items():
                result += f"## 🌐 Network: {network_id}\n"
                
                for serial, uplinks in network_data['devices'].items():
                    result += f"### 📱 Device: {serial}\n"
                    
                    for uplink_data in uplinks:
                        uplink_name = uplink_data.get('uplink', 'Unknown')
                        ip = uplink_data.get('ip', 'N/A')
                        result += f"#### 🔗 {uplink_name.upper()}\n"
                        result += f"- **IP**: {ip}\n"
                        
                        # Get time series data
                        time_series = uplink_data.get('timeSeries', [])
                        
                        if time_series:
                            # Get the most recent data point
                            latest = time_series[-1]
                            timestamp = latest.get('ts', 'Unknown')
                            loss_percent = latest.get('lossPercent', None)
                            latency_ms = latest.get('latencyMs', None)
                            
                            # Calculate averages for the period
                            total_loss = sum(ts.get('lossPercent', 0) for ts in time_series)
                            total_latency = sum(ts.get('latencyMs', 0) for ts in time_series)
                            avg_loss = total_loss / len(time_series) if time_series else 0
                            avg_latency = total_latency / len(time_series) if time_series else 0
                            
                            # Display current values
                            result += f"- **Last Update**: {timestamp}\n"
                            
                            # Packet Loss
                            if loss_percent is not None:
                                if loss_percent > 5:
                                    result += f"- **🚨 PACKET LOSS**: {loss_percent:.1f}% ❌ CRITICAL\n"
                                elif loss_percent > 1:
                                    result += f"- **⚠️ Packet Loss**: {loss_percent:.1f}% ⚠️ WARNING\n"
                                else:
                                    result += f"- **Packet Loss**: {loss_percent:.1f}% ✅\n"
                            
                            # Latency
                            if latency_ms is not None:
                                if latency_ms > 150:
                                    result += f"- **🐌 LATENCY**: {latency_ms:.1f}ms ❌ HIGH\n"
                                elif latency_ms > 50:
                                    result += f"- **Latency**: {latency_ms:.1f}ms ⚠️\n"
                                else:
                                    result += f"- **Latency**: {latency_ms:.1f}ms ✅\n"
                            
                            # Show averages
                            result += f"\n**Period Averages**:\n"
                            result += f"- Average Loss: {avg_loss:.1f}%\n"
                            result += f"- Average Latency: {avg_latency:.1f}ms\n"
                            result += f"- Data Points: {len(time_series)}\n"
                            
                            # Show trend if multiple data points
                            if len(time_series) > 1:
                                first_loss = time_series[0].get('lossPercent', 0)
                                trend = "📈 Increasing" if loss_percent > first_loss else "📉 Decreasing" if loss_percent < first_loss else "➡️ Stable"
                                result += f"- Loss Trend: {trend}\n"
                        else:
                            result += "- **Status**: No data available\n"
                            
                        result += "\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving uplink loss/latency data: {str(e)}"

    @app.tool(
        name="get_organization_appliance_uplink_statuses",
        description="🔗 Get REAL uplink status for all appliances in organization"
    )
    def get_organization_appliance_uplink_statuses(org_id: str):
        """
        Get REAL uplink status for all appliances in organization.
        
        Args:
            org_id: Organization ID
            
        Returns:
            Formatted appliance uplink status data
        """
        try:
            uplink_statuses = meraki_client.get_organization_appliance_uplink_statuses(org_id)
            
            if not uplink_statuses:
                return f"No appliance uplink status data found for organization {org_id}."
                
            result = f"# 🔗 APPLIANCE UPLINK STATUS - Organization {org_id}\n\n"
            
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
            return f"Error retrieving appliance uplink statuses: {str(e)}"

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