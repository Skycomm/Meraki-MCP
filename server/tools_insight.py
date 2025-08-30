"""
Insight monitoring and application health tools for Cisco Meraki MCP server.

This module provides tools for monitoring application health and performance insights.
"""

from typing import Optional, Dict, Any, List
from datetime import datetime
import json

# Global references to be set by register function
app = None
meraki_client = None

def register_insight_tools(mcp_app, meraki):
    """
    Register insight tools with the MCP server.
    
    Args:
        mcp_app: MCP server instance
        meraki: Meraki client instance
    """
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    
    # ==================== APPLICATION HEALTH ====================
    
    @app.tool(
        name="get_network_insight_application_health_by_time",
        description="📊🏥 Get application health metrics over time for a network"
    )
    def get_network_insight_application_health_by_time(
        network_id: str,
        application_id: str,
        t0: Optional[str] = None,
        t1: Optional[str] = None,
        timespan: Optional[float] = 86400,
        resolution: Optional[int] = None
    ):
        """Get application health metrics over time."""
        try:
            kwargs = {}
            if t0:
                kwargs['t0'] = t0
            if t1:
                kwargs['t1'] = t1
            if timespan:
                kwargs['timespan'] = timespan
            if resolution:
                kwargs['resolution'] = resolution
            
            result = meraki_client.insight.getNetworkInsightApplicationHealthByTime(
                network_id, application_id, **kwargs
            )
            
            response = f"# 📊 Application Health Over Time\n\n"
            response += f"**Application ID**: {application_id}\n"
            response += f"**Timespan**: {timespan/3600:.1f} hours\n\n"
            
            if result:
                # Show health scores
                scores = result.get('healthScores', [])
                if scores:
                    response += "## Health Scores\n\n"
                    response += "| Time | Score | Performance | Quality |\n"
                    response += "|------|-------|------------|---------||\n"
                    
                    for score in scores[:10]:  # Show first 10
                        time = score.get('startTs', 'N/A')
                        health = score.get('score', 0)
                        perf = score.get('performance', {}).get('score', 0)
                        qual = score.get('quality', {}).get('score', 0)
                        response += f"| {time} | {health:.1f} | {perf:.1f} | {qual:.1f} |\n"
                    
                    if len(scores) > 10:
                        response += f"\n*...and {len(scores)-10} more data points*\n"
                
                # Show average metrics
                avg_score = sum(s.get('score', 0) for s in scores) / len(scores) if scores else 0
                response += f"\n**Average Health Score**: {avg_score:.1f}/100\n"
            else:
                response += "*No health data available for this application*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting application health: {str(e)}"
    
    @app.tool(
        name="get_organization_insight_applications",
        description="📊📱 Get all monitored applications for an organization"
    )
    def get_organization_insight_applications(
        organization_id: str
    ):
        """Get list of all monitored applications."""
        try:
            result = meraki_client.insight.getOrganizationInsightApplications(organization_id)
            
            response = f"# 📱 Monitored Applications\n\n"
            
            if result and isinstance(result, list):
                response += f"**Total Applications**: {len(result)}\n\n"
                
                for app_info in result:
                    response += f"## {app_info.get('name', 'Unknown')}\n"
                    response += f"- ID: {app_info.get('applicationId', 'N/A')}\n"
                    response += f"- Category: {app_info.get('category', 'N/A')}\n"
                    response += f"- Monitored: {'✅' if app_info.get('isMonitored') else '❌'}\n"
                    
                    # Show thresholds if configured
                    thresholds = app_info.get('thresholds', {})
                    if thresholds:
                        response += f"- Thresholds:\n"
                        response += f"  - Good: >{thresholds.get('goodness', 0)}\n"
                        response += f"  - Fair: >{thresholds.get('fairness', 0)}\n"
                    
                    response += "\n"
            else:
                response += "*No monitored applications configured*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting applications: {str(e)}"
    
    # ==================== MONITORED MEDIA SERVERS ====================
    
    @app.tool(
        name="get_organization_insight_monitored_media_servers",
        description="📊🎬 Get all monitored media servers for an organization"
    )
    def get_organization_insight_monitored_media_servers(
        organization_id: str
    ):
        """Get all monitored media servers."""
        try:
            result = meraki_client.insight.getOrganizationInsightMonitoredMediaServers(organization_id)
            
            response = f"# 🎬 Monitored Media Servers\n\n"
            
            if result and isinstance(result, list):
                response += f"**Total Servers**: {len(result)}\n\n"
                
                for server in result:
                    response += f"## {server.get('name', 'Unknown')}\n"
                    response += f"- ID: {server.get('id', 'N/A')}\n"
                    response += f"- Address: {server.get('address', 'N/A')}\n"
                    response += f"- Port: {server.get('port', 'N/A')}\n"
                    response += f"- Transport: {server.get('transport', 'N/A')}\n"
                    response += f"- Monitored: {'✅' if server.get('isMonitored') else '❌'}\n\n"
            else:
                response += "*No monitored media servers configured*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting media servers: {str(e)}"
    
    @app.tool(
        name="get_organization_insight_monitored_media_server",
        description="📊🎬 Get details of a specific monitored media server"
    )
    def get_organization_insight_monitored_media_server(
        organization_id: str,
        monitored_media_server_id: str
    ):
        """Get details of a specific monitored media server."""
        try:
            result = meraki_client.insight.getOrganizationInsightMonitoredMediaServer(
                organization_id, monitored_media_server_id
            )
            
            response = f"# 🎬 Media Server Details\n\n"
            
            if result:
                response += f"**Name**: {result.get('name', 'Unknown')}\n"
                response += f"**ID**: {result.get('id', 'N/A')}\n"
                response += f"**Address**: {result.get('address', 'N/A')}\n"
                response += f"**Port**: {result.get('port', 'N/A')}\n"
                response += f"**Transport**: {result.get('transport', 'N/A')}\n"
                response += f"**Monitored**: {'✅' if result.get('isMonitored') else '❌'}\n\n"
                
                # Show configuration details
                config = result.get('config', {})
                if config:
                    response += "## Configuration\n\n"
                    response += f"- Codec: {config.get('codec', 'N/A')}\n"
                    response += f"- Bitrate: {config.get('bitrate', 'N/A')}\n"
                    response += f"- Sample Rate: {config.get('sampleRate', 'N/A')}\n"
            else:
                response += "*Media server not found*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting media server: {str(e)}"
    
    @app.tool(
        name="create_organization_insight_monitored_media_server",
        description="📊➕ Create a new monitored media server"
    )
    def create_organization_insight_monitored_media_server(
        organization_id: str,
        name: str,
        address: str,
        port: Optional[int] = 5060,
        transport: Optional[str] = "UDP"
    ):
        """
        Create a new monitored media server.
        
        Args:
            organization_id: Organization ID
            name: Name of the media server
            address: IP address or hostname
            port: Port number (default 5060)
            transport: Transport protocol (UDP/TCP)
        """
        try:
            kwargs = {
                'name': name,
                'address': address
            }
            if port:
                kwargs['port'] = port
            if transport:
                kwargs['transport'] = transport
            
            result = meraki_client.insight.createOrganizationInsightMonitoredMediaServer(
                organization_id, **kwargs
            )
            
            response = f"# ✅ Media Server Created\n\n"
            
            if result:
                response += f"**Name**: {result.get('name')}\n"
                response += f"**ID**: {result.get('id')}\n"
                response += f"**Address**: {result.get('address')}:{result.get('port')}\n"
                response += f"**Transport**: {result.get('transport')}\n\n"
                response += "The media server is now being monitored for performance insights.\n"
            
            return response
        except Exception as e:
            return f"❌ Error creating media server: {str(e)}"
    
    @app.tool(
        name="update_organization_insight_monitored_media_server",
        description="📊✏️ Update a monitored media server configuration"
    )
    def update_organization_insight_monitored_media_server(
        organization_id: str,
        monitored_media_server_id: str,
        name: Optional[str] = None,
        address: Optional[str] = None,
        port: Optional[int] = None,
        transport: Optional[str] = None
    ):
        """Update a monitored media server."""
        try:
            kwargs = {}
            if name:
                kwargs['name'] = name
            if address:
                kwargs['address'] = address
            if port:
                kwargs['port'] = port
            if transport:
                kwargs['transport'] = transport
            
            result = meraki_client.insight.updateOrganizationInsightMonitoredMediaServer(
                organization_id, monitored_media_server_id, **kwargs
            )
            
            response = f"# ✅ Media Server Updated\n\n"
            
            if result:
                response += f"**Name**: {result.get('name')}\n"
                response += f"**Address**: {result.get('address')}:{result.get('port')}\n"
                response += f"**Transport**: {result.get('transport')}\n"
            
            return response
        except Exception as e:
            return f"❌ Error updating media server: {str(e)}"
    
    @app.tool(
        name="delete_organization_insight_monitored_media_server",
        description="📊❌ Delete a monitored media server"
    )
    def delete_organization_insight_monitored_media_server(
        organization_id: str,
        monitored_media_server_id: str
    ):
        """Delete a monitored media server."""
        try:
            meraki_client.insight.deleteOrganizationInsightMonitoredMediaServer(
                organization_id, monitored_media_server_id
            )
            
            response = f"# ✅ Media Server Deleted\n\n"
            response += f"**Server ID**: {monitored_media_server_id}\n\n"
            response += "The media server has been removed from monitoring.\n"
            
            return response
        except Exception as e:
            error_msg = str(e)
            if '404' in error_msg:
                return f"❌ Media server not found: {monitored_media_server_id}"
            return f"❌ Error deleting media server: {error_msg}"