"""
Insight monitoring tools for Cisco Meraki MCP server.

This module provides complete coverage of all Insight SDK methods for monitoring
application health and media server performance.
"""

from typing import Optional, Dict, Any, List

# Global references to be set by register function
app = None
meraki_client = None

def register_insight_tools(mcp_app, meraki):
    """
    Register Insight tools with the MCP server.
    
    Args:
        mcp_app: MCP server instance
        meraki: Meraki client instance
    """
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    
    # Register tool handlers
    register_insight_tool_handlers()

def register_insight_tool_handlers():
    """Register all Insight tool handlers."""
    
    # ==================== MONITORED MEDIA SERVERS ====================
    
    @app.tool(
        name="get_org_insight_monitored_media_servers",
        description="📊 List all monitored media servers for the organization."
    )
    def get_org_insight_monitored_media_servers(
        organization_id: str
    ):
        """
        List all monitored media servers.
        
        Args:
            organization_id: Organization ID
        """
        try:
            result = meraki_client.dashboard.insight.getOrganizationInsightMonitoredMediaServers(
                organization_id
            )
            
            response = f"# 📊 Monitored Media Servers\n\n"
            response += f"**Organization**: {organization_id}\n\n"
            
            if result and isinstance(result, list):
                response += f"**Total Servers**: {len(result)}\n\n"
                
                for server in result:
                    server_id = server.get('id', 'Unknown')
                    response += f"## Server {server_id}\n"
                    response += f"- **Name**: {server.get('name', 'Unnamed')}\n"
                    response += f"- **Address**: {server.get('address', 'N/A')}\n"
                    response += f"- **Media Type**: {server.get('mediaType', 'N/A')}\n"
                    response += f"- **Best Effort**: {server.get('bestEffortMonitoringEnabled', False)}\n"
                    
                    # Remote site IDs if configured
                    remote_sites = server.get('remoteSiteIds', [])
                    if remote_sites:
                        response += f"- **Remote Sites**: {', '.join(remote_sites)}\n"
                    
                    response += "\n"
            else:
                response += "*No monitored media servers configured*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting monitored media servers: {str(e)}"
    
    @app.tool(
        name="get_org_insight_monitored_media_server",
        description="📊 Get details of a specific monitored media server."
    )
    def get_org_insight_monitored_media_server(
        organization_id: str,
        monitored_media_server_id: str
    ):
        """
        Get specific monitored media server details.
        
        Args:
            organization_id: Organization ID
            monitored_media_server_id: Monitored media server ID
        """
        try:
            result = meraki_client.dashboard.insight.getOrganizationInsightMonitoredMediaServer(
                organization_id, monitored_media_server_id
            )
            
            response = f"# 📊 Monitored Media Server Details\n\n"
            response += f"**Server ID**: {monitored_media_server_id}\n\n"
            
            if result:
                response += f"## Configuration\n"
                response += f"- **Name**: {result.get('name', 'Unnamed')}\n"
                response += f"- **Address**: {result.get('address', 'N/A')}\n"
                response += f"- **Media Type**: {result.get('mediaType', 'N/A')}\n"
                response += f"- **Best Effort Monitoring**: {result.get('bestEffortMonitoringEnabled', False)}\n"
                
                # Remote site configuration
                remote_sites = result.get('remoteSiteIds', [])
                if remote_sites:
                    response += f"\n## Remote Sites ({len(remote_sites)})\n"
                    for site_id in remote_sites:
                        response += f"- Site ID: {site_id}\n"
                
                # Additional details if available
                if result.get('description'):
                    response += f"\n## Description\n{result['description']}\n"
            else:
                response += "*Media server not found*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting media server details: {str(e)}"
    
    @app.tool(
        name="create_org_insight_monitored_media_server",
        description="➕ Create a new monitored media server. Requires confirmation."
    )
    def create_org_insight_monitored_media_server(
        organization_id: str,
        name: str,
        address: str,
        media_type: str = "auto",
        best_effort_monitoring_enabled: bool = True,
        remote_site_ids: Optional[List[str]] = None,
        confirmed: bool = False
    ):
        """
        Create a new monitored media server.
        
        Args:
            organization_id: Organization ID
            name: Server name
            address: Server address (IP or hostname)
            media_type: Media type ("auto", "webex", "zoom", "teams", etc.)
            best_effort_monitoring_enabled: Enable best effort monitoring
            remote_site_ids: List of remote site IDs to monitor from
            confirmed: Must be true to execute
        """
        if not confirmed:
            return "⚠️ Creating monitored media server requires confirmed=true"
        
        try:
            kwargs = {
                "name": name,
                "address": address,
                "mediaType": media_type,
                "bestEffortMonitoringEnabled": best_effort_monitoring_enabled
            }
            
            if remote_site_ids:
                kwargs["remoteSiteIds"] = remote_site_ids
            
            result = meraki_client.dashboard.insight.createOrganizationInsightMonitoredMediaServer(
                organization_id, **kwargs
            )
            
            server_id = result.get('id', 'Unknown')
            return f"✅ Created monitored media server '{name}' with ID {server_id}"
        except Exception as e:
            return f"❌ Error creating monitored media server: {str(e)}"
    
    @app.tool(
        name="update_org_insight_monitored_media_server",
        description="✏️ Update a monitored media server configuration. Requires confirmation."
    )
    def update_org_insight_monitored_media_server(
        organization_id: str,
        monitored_media_server_id: str,
        name: Optional[str] = None,
        address: Optional[str] = None,
        media_type: Optional[str] = None,
        best_effort_monitoring_enabled: Optional[bool] = None,
        remote_site_ids: Optional[List[str]] = None,
        confirmed: bool = False
    ):
        """
        Update a monitored media server.
        
        Args:
            organization_id: Organization ID
            monitored_media_server_id: Monitored media server ID
            name: Server name
            address: Server address
            media_type: Media type
            best_effort_monitoring_enabled: Enable best effort monitoring
            remote_site_ids: Remote site IDs
            confirmed: Must be true to execute
        """
        if not confirmed:
            return "⚠️ Updating monitored media server requires confirmed=true"
        
        try:
            kwargs = {}
            
            if name is not None:
                kwargs["name"] = name
            if address is not None:
                kwargs["address"] = address
            if media_type is not None:
                kwargs["mediaType"] = media_type
            if best_effort_monitoring_enabled is not None:
                kwargs["bestEffortMonitoringEnabled"] = best_effort_monitoring_enabled
            if remote_site_ids is not None:
                kwargs["remoteSiteIds"] = remote_site_ids
            
            result = meraki_client.dashboard.insight.updateOrganizationInsightMonitoredMediaServer(
                organization_id, monitored_media_server_id, **kwargs
            )
            
            return f"✅ Updated monitored media server {monitored_media_server_id}"
        except Exception as e:
            return f"❌ Error updating monitored media server: {str(e)}"
    
    @app.tool(
        name="delete_org_insight_monitored_media_server",
        description="🗑️ Delete a monitored media server. Requires confirmation."
    )
    def delete_org_insight_monitored_media_server(
        organization_id: str,
        monitored_media_server_id: str,
        confirmed: bool = False
    ):
        """
        Delete a monitored media server.
        
        Args:
            organization_id: Organization ID
            monitored_media_server_id: Monitored media server ID
            confirmed: Must be true to execute
        """
        if not confirmed:
            return "⚠️ Deleting monitored media server requires confirmed=true. This cannot be undone!"
        
        try:
            meraki_client.dashboard.insight.deleteOrganizationInsightMonitoredMediaServer(
                organization_id, monitored_media_server_id
            )
            return f"✅ Deleted monitored media server {monitored_media_server_id}"
        except Exception as e:
            return f"❌ Error deleting monitored media server: {str(e)}"
    
    # ==================== APPLICATION HEALTH ====================
    
    @app.tool(
        name="get_organization_insight_applications",
        description="📱 List all monitored applications for the organization."
    )
    def get_organization_insight_applications(
        organization_id: str
    ):
        """
        List all monitored applications.
        
        Args:
            organization_id: Organization ID
        """
        try:
            result = meraki_client.dashboard.insight.getOrganizationInsightApplications(
                organization_id
            )
            
            response = f"# 📱 Monitored Applications\n\n"
            response += f"**Organization**: {organization_id}\n\n"
            
            if result and isinstance(result, list):
                response += f"**Total Applications**: {len(result)}\n\n"
                
                # Group applications by category if available
                by_category = {}
                for app in result:
                    category = app.get('category', 'Uncategorized')
                    if category not in by_category:
                        by_category[category] = []
                    by_category[category].append(app)
                
                for category, apps in sorted(by_category.items()):
                    response += f"## {category}\n"
                    for app in apps:
                        app_id = app.get('applicationId', 'Unknown')
                        name = app.get('name', 'Unnamed')
                        response += f"- **{name}** (ID: {app_id})\n"
                        
                        if app.get('thresholds'):
                            thresholds = app['thresholds']
                            response += f"  - Thresholds configured: "
                            if thresholds.get('type'):
                                response += f"{thresholds['type']}"
                            response += "\n"
                        
                        if app.get('monitored'):
                            response += f"  - Monitoring: Enabled\n"
                    response += "\n"
            else:
                response += "*No applications being monitored*\n"
                response += "\n💡 Insight monitors application performance including:\n"
                response += "- VoIP (WebEx, Zoom, Teams)\n"
                response += "- Business applications\n"
                response += "- Custom applications\n"
            
            return response
        except Exception as e:
            error_msg = str(e)
            if "Insight" in error_msg or "license" in error_msg.lower():
                return f"⚠️ Insight features may require additional licensing. Error: {error_msg}"
            return f"❌ Error getting monitored applications: {error_msg}"
    
    @app.tool(
        name="get_network_insight_app_health_by_time",
        description="📈 Get application health metrics over time for a network."
    )
    def get_network_insight_app_health_by_time(
        network_id: str,
        application_id: str,
        timespan: int = 86400,
        resolution: int = 60,
        device_serial: Optional[str] = None
    ):
        """
        Get application health metrics over time.
        
        Args:
            network_id: Network ID
            application_id: Application ID to monitor
            timespan: Timespan in seconds (default 24 hours)
            resolution: Time resolution in seconds (60, 300, 600, 1800, 3600)
            device_serial: Optional device serial to filter by
        """
        try:
            kwargs = {
                "applicationId": application_id,
                "t0": None,  # Use timespan instead
                "t1": None,
                "timespan": timespan,
                "resolution": resolution
            }
            
            if device_serial:
                kwargs["deviceSerial"] = device_serial
            
            result = meraki_client.dashboard.insight.getNetworkInsightApplicationHealthByTime(
                network_id, **kwargs
            )
            
            response = f"# 📈 Application Health Metrics\n\n"
            response += f"**Network**: {network_id}\n"
            response += f"**Application ID**: {application_id}\n"
            response += f"**Timespan**: {timespan} seconds\n"
            response += f"**Resolution**: {resolution} seconds\n"
            
            if device_serial:
                response += f"**Device**: {device_serial}\n"
            
            response += "\n"
            
            if result and isinstance(result, list):
                response += f"**Data Points**: {len(result)}\n\n"
                
                # Show recent metrics
                response += "## Recent Metrics (last 5 data points)\n"
                for i, point in enumerate(result[-5:] if len(result) > 5 else result):
                    response += f"\n### {point.get('startTs', 'Unknown time')}\n"
                    
                    # Performance score
                    perf_score = point.get('performanceScore')
                    if perf_score is not None:
                        response += f"- **Performance Score**: {perf_score}/100\n"
                    
                    # Responsiveness
                    responsiveness = point.get('responsiveness')
                    if responsiveness is not None:
                        response += f"- **Responsiveness**: {responsiveness}ms\n"
                    
                    # Packet loss
                    packet_loss = point.get('packetLoss')
                    if packet_loss is not None:
                        response += f"- **Packet Loss**: {packet_loss}%\n"
                    
                    # Latency
                    latency = point.get('latency')
                    if latency is not None:
                        response += f"- **Latency**: {latency}ms\n"
                    
                    # Jitter
                    jitter = point.get('jitter')
                    if jitter is not None:
                        response += f"- **Jitter**: {jitter}ms\n"
                    
                    # Number of clients
                    num_clients = point.get('numClients')
                    if num_clients is not None:
                        response += f"- **Active Clients**: {num_clients}\n"
                    
                    # MOS score for VoIP
                    mos = point.get('mos')
                    if mos is not None:
                        response += f"- **MOS Score**: {mos}/5.0 (VoIP quality)\n"
                
                # Calculate averages
                if len(result) > 0:
                    response += f"\n## Summary Statistics\n"
                    
                    avg_perf = sum(p.get('performanceScore', 0) for p in result if p.get('performanceScore') is not None)
                    count_perf = sum(1 for p in result if p.get('performanceScore') is not None)
                    if count_perf > 0:
                        response += f"- **Average Performance**: {avg_perf/count_perf:.1f}/100\n"
                    
                    avg_loss = sum(p.get('packetLoss', 0) for p in result if p.get('packetLoss') is not None)
                    count_loss = sum(1 for p in result if p.get('packetLoss') is not None)
                    if count_loss > 0:
                        response += f"- **Average Packet Loss**: {avg_loss/count_loss:.2f}%\n"
                    
                    avg_latency = sum(p.get('latency', 0) for p in result if p.get('latency') is not None)
                    count_latency = sum(1 for p in result if p.get('latency') is not None)
                    if count_latency > 0:
                        response += f"- **Average Latency**: {avg_latency/count_latency:.1f}ms\n"
            else:
                response += "*No health data available for this application*\n"
                response += "\n💡 This could mean:\n"
                response += "- Application is not actively monitored\n"
                response += "- No traffic detected for this application\n"
                response += "- Insight license may be required\n"
            
            return response
        except Exception as e:
            error_msg = str(e)
            if "Insight" in error_msg or "license" in error_msg.lower():
                return f"⚠️ Insight features require additional licensing. Error: {error_msg}"
            return f"❌ Error getting application health: {error_msg}"