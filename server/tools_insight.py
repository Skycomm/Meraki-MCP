"""
Application Insight Tools for Cisco Meraki MCP Server
Monitor application performance and gain network insights
"""

from mcp.server import FastMCP
from typing import Optional, Dict, Any, List
import json
from datetime import datetime, timedelta
from meraki_client import MerakiClient
from utils.helpers import format_error_message
from contextlib import contextmanager

# This will be set by register function
mcp_app = None
meraki = None

def format_error(operation: str, error: Exception) -> str:
    """Format error message with operation context."""
    return f"❌ Failed to {operation}: {format_error_message(error)}"

@contextmanager
def safe_api_call(operation: str):
    """Context manager for safe API calls with consistent error handling."""
    try:
        yield
    except Exception as e:
        raise Exception(f"Failed to {operation}: {str(e)}")


def get_organization_insight_applications(org_id: str) -> str:
    """
    📱 Get monitored applications for insights.
    
    Shows applications being monitored for performance insights.
    
    Args:
        org_id: Organization ID
    
    Returns:
        Formatted list of monitored applications
    """
    try:
        with safe_api_call("get insight applications"):
            apps = meraki.dashboard.insight.getOrganizationInsightApplications(org_id)
            
            if not apps:
                return f"No applications configured for insights in organization {org_id}"
            
            output = ["📱 Monitored Applications", "=" * 50, ""]
            
            # Group by application type
            by_type = {}
            for app in apps:
                app_type = app.get('applicationType', 'Unknown')
                if app_type not in by_type:
                    by_type[app_type] = []
                by_type[app_type].append(app)
            
            for app_type, type_apps in by_type.items():
                output.append(f"📊 {app_type} Applications ({len(type_apps)}):")
                
                for app in type_apps:
                    app_id = app.get('applicationId', 'Unknown')
                    name = app.get('name', app_id)
                    output.append(f"   • {name}")
                    
                    # Thresholds if configured
                    thresholds = app.get('thresholds', {})
                    if thresholds:
                        if thresholds.get('type') == 'smart':
                            output.append("     📈 Smart thresholds enabled")
                        else:
                            output.append("     📏 Custom thresholds:")
                            if thresholds.get('byNetwork'):
                                for net_threshold in thresholds['byNetwork']:
                                    net_id = net_threshold.get('networkId', 'Unknown')
                                    goodput = net_threshold.get('goodput', 0)
                                    responseDuration = net_threshold.get('responseDuration', 0)
                                    output.append(f"        Network {net_id[-4:]}: {goodput} kbps, {responseDuration}ms")
                
                output.append("")
            
            # Summary stats
            total_apps = len(apps)
            smart_threshold_apps = len([a for a in apps if a.get('thresholds', {}).get('type') == 'smart'])
            
            output.append("📊 Summary:")
            output.append(f"   Total Applications: {total_apps}")
            output.append(f"   Smart Thresholds: {smart_threshold_apps}")
            output.append(f"   Custom Thresholds: {total_apps - smart_threshold_apps}")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("get insight applications", e)


def get_network_insight_application_health_by_time(
    network_id: str,
    application_id: str,
    timespan: Optional[int] = 86400,
    resolution: Optional[int] = 3600
) -> str:
    """
    📈 Get application health metrics over time.
    
    Shows performance metrics for a specific application.
    
    Args:
        network_id: Network ID
        application_id: Application ID to monitor
        timespan: Time period in seconds (default: 86400 = 24 hours)
        resolution: Data resolution in seconds (default: 3600 = 1 hour)
    
    Returns:
        Application health metrics
    """
    try:
        with safe_api_call("get application health"):
            health = meraki.dashboard.insight.getNetworkInsightApplicationHealthByTime(
                network_id,
                applicationId=application_id,
                timespan=timespan,
                resolution=resolution
            )
            
            output = ["📈 Application Health Metrics", "=" * 50, ""]
            output.append(f"Application ID: {application_id}")
            output.append(f"Time Period: Last {timespan // 3600} hours")
            output.append(f"Resolution: {resolution // 60} minutes")
            output.append("")
            
            if not health:
                return "\n".join(output + ["No health data available for this period"])
            
            # Process metrics
            metrics = {
                'goodput': [],
                'responseDuration': [],
                'numClients': [],
                'score': []
            }
            
            for point in health:
                if 'goodput' in point:
                    metrics['goodput'].append(point['goodput'])
                if 'responseDuration' in point:
                    metrics['responseDuration'].append(point['responseDuration'])
                if 'numClients' in point:
                    metrics['numClients'].append(point['numClients'])
                
                # Calculate health score
                score = 100
                if point.get('responseDuration', 0) > 1000:
                    score -= 20
                elif point.get('responseDuration', 0) > 500:
                    score -= 10
                
                if point.get('goodput', 100) < 50:
                    score -= 20
                elif point.get('goodput', 100) < 80:
                    score -= 10
                    
                metrics['score'].append(max(0, score))
            
            # Show averages
            if metrics['goodput']:
                avg_goodput = sum(metrics['goodput']) / len(metrics['goodput'])
                output.append(f"📊 Average Goodput: {avg_goodput:.1f} kbps")
                output.append(f"   Peak: {max(metrics['goodput']):.1f} kbps")
                output.append(f"   Low: {min(metrics['goodput']):.1f} kbps")
            
            if metrics['responseDuration']:
                avg_response = sum(metrics['responseDuration']) / len(metrics['responseDuration'])
                output.append(f"\n⏱️ Average Response Time: {avg_response:.0f} ms")
                output.append(f"   Peak: {max(metrics['responseDuration']):.0f} ms")
                output.append(f"   Best: {min(metrics['responseDuration']):.0f} ms")
            
            if metrics['numClients']:
                avg_clients = sum(metrics['numClients']) / len(metrics['numClients'])
                output.append(f"\n👥 Average Active Clients: {avg_clients:.0f}")
                output.append(f"   Peak: {max(metrics['numClients'])}")
            
            if metrics['score']:
                avg_score = sum(metrics['score']) / len(metrics['score'])
                score_icon = "🟢" if avg_score >= 80 else "🟡" if avg_score >= 60 else "🔴"
                output.append(f"\n{score_icon} Health Score: {avg_score:.0f}/100")
            
            # Recent trend
            if len(health) >= 3:
                recent = health[-3:]
                recent_goodput = [p.get('goodput', 0) for p in recent]
                recent_response = [p.get('responseDuration', 0) for p in recent]
                
                output.append("\n📈 Recent Trend (last 3 data points):")
                if recent_goodput[-1] > recent_goodput[0]:
                    output.append("   ✅ Goodput improving")
                elif recent_goodput[-1] < recent_goodput[0]:
                    output.append("   ⚠️ Goodput degrading")
                    
                if recent_response[-1] < recent_response[0]:
                    output.append("   ✅ Response time improving")
                elif recent_response[-1] > recent_response[0]:
                    output.append("   ⚠️ Response time increasing")
            
            # Recommendations
            output.append("\n💡 Performance Guidelines:")
            output.append("• Response time <200ms: Excellent")
            output.append("• Response time 200-500ms: Good")
            output.append("• Response time >1000ms: Poor")
            output.append("• Goodput >80%: Optimal")
            output.append("• Monitor during peak hours")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("get application health", e)


def get_organization_insight_monitored_media_servers(org_id: str) -> str:
    """
    📹 Get monitored media servers.
    
    Shows media servers configured for insights monitoring.
    
    Args:
        org_id: Organization ID
    
    Returns:
        List of monitored media servers
    """
    try:
        with safe_api_call("get monitored media servers"):
            servers = meraki.dashboard.insight.getOrganizationInsightMonitoredMediaServers(org_id)
            
            if not servers:
                return f"No media servers configured for monitoring in organization {org_id}"
            
            output = ["📹 Monitored Media Servers", "=" * 50, ""]
            
            for server in servers:
                server_id = server.get('id', 'Unknown')
                name = server.get('name', 'Unnamed Server')
                address = server.get('address', 'No address')
                
                output.append(f"🖥️ {name}")
                output.append(f"   ID: {server_id}")
                output.append(f"   Address: {address}")
                
                # Best effort monitoring
                if server.get('bestEffortMonitoringEnabled'):
                    output.append("   📊 Best effort monitoring: Enabled")
                
                output.append("")
            
            output.append(f"Total Servers: {len(servers)}")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("get monitored media servers", e)


def create_insight_monitored_media_server(
    org_id: str,
    name: str,
    address: str,
    best_effort_monitoring_enabled: bool = True
) -> str:
    """
    ➕ Add a media server for insights monitoring.
    
    Configure a new media server for performance monitoring.
    
    Args:
        org_id: Organization ID
        name: Server name
        address: Server address/hostname
        best_effort_monitoring_enabled: Enable best effort monitoring
    
    Returns:
        Creation result
    """
    try:
        with safe_api_call("create monitored media server"):
            server = meraki.dashboard.insight.createOrganizationInsightMonitoredMediaServer(
                org_id,
                name=name,
                address=address,
                bestEffortMonitoringEnabled=best_effort_monitoring_enabled
            )
            
            output = ["✅ Media Server Added for Monitoring", "=" * 50, ""]
            output.append(f"Name: {server.get('name', name)}")
            output.append(f"ID: {server.get('id', 'N/A')}")
            output.append(f"Address: {server.get('address', address)}")
            
            if server.get('bestEffortMonitoringEnabled'):
                output.append("📊 Best effort monitoring: Enabled")
            
            output.append("\n💡 Next Steps:")
            output.append("• Monitor server performance metrics")
            output.append("• Set up alerts for quality issues")
            output.append("• Review call quality regularly")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("create monitored media server", e)


def analyze_application_performance(org_id: str, network_id: str) -> str:
    """
    🔍 Analyze overall application performance.
    
    Provides insights and recommendations for application optimization.
    
    Args:
        org_id: Organization ID
        network_id: Network ID
    
    Returns:
        Performance analysis and recommendations
    """
    try:
        with safe_api_call("analyze application performance"):
            # Get monitored applications
            apps = meraki.dashboard.insight.getOrganizationInsightApplications(org_id)
            
            output = ["🔍 Application Performance Analysis", "=" * 50, ""]
            output.append(f"Network: {network_id}")
            output.append("")
            
            if not apps:
                output.append("No applications configured for monitoring")
                output.append("\n💡 Recommendation: Enable application insights for critical apps")
                return "\n".join(output)
            
            # Analyze each application
            app_scores = []
            issues = []
            
            for app in apps[:5]:  # Analyze top 5 apps
                app_id = app.get('applicationId')
                app_name = app.get('name', app_id)
                
                try:
                    # Get recent health data
                    health = meraki.dashboard.insight.getNetworkInsightApplicationHealthByTime(
                        network_id,
                        applicationId=app_id,
                        timespan=3600,  # Last hour
                        resolution=300  # 5 minutes
                    )
                    
                    if health:
                        # Calculate performance score
                        recent_data = health[-1] if health else {}
                        goodput = recent_data.get('goodput', 0)
                        response_time = recent_data.get('responseDuration', 0)
                        
                        score = 100
                        if response_time > 1000:
                            score -= 30
                            issues.append(f"{app_name}: High response time ({response_time}ms)")
                        elif response_time > 500:
                            score -= 15
                        
                        if goodput < 50:
                            score -= 30
                            issues.append(f"{app_name}: Low goodput ({goodput}%)")
                        elif goodput < 80:
                            score -= 15
                        
                        app_scores.append((app_name, max(0, score)))
                        
                except:
                    # Skip if no data available
                    continue
            
            # Show results
            if app_scores:
                output.append("📊 Application Scores:")
                app_scores.sort(key=lambda x: x[1], reverse=True)
                
                for app_name, score in app_scores:
                    icon = "🟢" if score >= 80 else "🟡" if score >= 60 else "🔴"
                    output.append(f"   {icon} {app_name}: {score}/100")
                
                avg_score = sum(s[1] for s in app_scores) / len(app_scores)
                overall_icon = "🟢" if avg_score >= 80 else "🟡" if avg_score >= 60 else "🔴"
                output.append(f"\n{overall_icon} Overall Score: {avg_score:.0f}/100")
            
            # Show issues
            if issues:
                output.append("\n⚠️ Performance Issues Detected:")
                for issue in issues:
                    output.append(f"   • {issue}")
            
            # Recommendations
            output.append("\n💡 Optimization Recommendations:")
            
            if any("response time" in issue for issue in issues):
                output.append("• Check server resources and network latency")
                output.append("• Consider content caching or CDN")
                output.append("• Optimize application code")
            
            if any("goodput" in issue for issue in issues):
                output.append("• Review network congestion")
                output.append("• Check for packet loss")
                output.append("• Consider QoS policies")
            
            output.append("\n📋 Best Practices:")
            output.append("• Monitor during peak usage hours")
            output.append("• Set up proactive alerts")
            output.append("• Review trends weekly")
            output.append("• Document performance baselines")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("analyze application performance", e)


def insight_monitoring_help() -> str:
    """
    ❓ Get help with insight monitoring tools.
    
    Shows available tools and best practices.
    
    Returns:
        Formatted help guide
    """
    return """📊 Insight Monitoring Tools Help
==================================================

Available tools for application insights:

1. get_organization_insight_applications()
   - View monitored applications
   - Check threshold configurations
   - See smart vs custom thresholds

2. get_network_insight_application_health_by_time()
   - Historical performance data
   - Response time metrics
   - Goodput measurements
   - Client counts

3. get_organization_insight_monitored_media_servers()
   - List media servers
   - VoIP/video monitoring
   - Best effort settings

4. create_insight_monitored_media_server()
   - Add new media server
   - Configure monitoring
   - Enable best effort

5. analyze_application_performance()
   - Performance scoring
   - Issue detection
   - Optimization tips

Key Metrics:
📈 Goodput: Percentage of successful data transfer
⏱️ Response Time: Application response duration
👥 Client Count: Active users
🎯 Health Score: Overall performance rating

Performance Thresholds:
• Response Time:
  - <200ms: Excellent ✅
  - 200-500ms: Good 🟡
  - >1000ms: Poor 🔴

• Goodput:
  - >80%: Optimal ✅
  - 60-80%: Acceptable 🟡
  - <60%: Poor 🔴

Best Practices:
- Enable smart thresholds for automatic baselines
- Monitor critical business applications
- Set up alerts for performance degradation
- Review trends during peak hours
- Compare performance across locations
"""


def register_insight_tools(app: FastMCP, meraki_client: MerakiClient):
    """Register all insight monitoring tools with the MCP server."""
    global mcp_app, meraki
    mcp_app = app
    meraki = meraki_client
    
    # Register all tools
    tools = [
        (get_organization_insight_applications, "View monitored applications"),
        (get_network_insight_application_health_by_time, "Get application health metrics"),
        (get_organization_insight_monitored_media_servers, "List monitored media servers"),
        (create_insight_monitored_media_server, "Add media server for monitoring"),
        (analyze_application_performance, "Analyze application performance"),
        (insight_monitoring_help, "Get help with insight monitoring"),
    ]
    
    for tool_func, description in tools:
        app.tool(
            name=tool_func.__name__,
            description=description
        )(tool_func)