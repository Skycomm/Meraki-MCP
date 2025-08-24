"""
Summary Analytics Tools for Cisco Meraki MCP Server
Get organization-wide usage summaries and top reports
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


def get_organization_summary_top_devices_by_usage(
    org_id: str,
    t0: Optional[str] = None,
    t1: Optional[str] = None,
    timespan: Optional[int] = 86400,
    quantity: Optional[int] = 10,
    ssid_name: Optional[str] = None,
    usage_uplink: Optional[str] = None
) -> str:
    """
    📊 Get top devices by data usage.
    
    Shows the top devices sorted by total data usage over a time period.
    
    Args:
        org_id: Organization ID
        t0: Start time (ISO 8601)
        t1: End time (ISO 8601)
        timespan: Time period in seconds (default: 86400 = 24 hours)
        quantity: Number of devices to return (default: 10)
        ssid_name: Filter by SSID name
        usage_uplink: Filter by uplink (wan1, wan2, cellular)
    
    Returns:
        Top devices by data usage
    """
    try:
        with safe_api_call("get top devices by usage"):
            # Build parameters
            params = {}
            if t0:
                params['t0'] = t0
            if t1:
                params['t1'] = t1
            elif timespan:
                params['timespan'] = timespan
            if quantity:
                params['quantity'] = quantity
            if ssid_name:
                params['ssidName'] = ssid_name
            if usage_uplink:
                params['usageUplink'] = usage_uplink
            
            results = meraki.dashboard.organizations.getOrganizationSummaryTopDevicesByUsage(
                org_id,
                **params
            )
            
            output = ["📊 Top Devices by Data Usage", "=" * 50, ""]
            output.append(f"Time Period: Last {timespan // 3600} hours")
            output.append("")
            
            if not results:
                output.append("No data available for this time period")
                return "\n".join(output)
            
            # Process results
            total_usage = sum(device.get('usage', {}).get('total', 0) for device in results)
            
            output.append(f"📈 Total Data Usage: {format_data_size(total_usage)}")
            output.append(f"Devices Shown: {len(results)}")
            output.append("")
            
            # Show each device
            for i, device in enumerate(results, 1):
                name = device.get('name', device.get('mac', 'Unknown'))
                model = device.get('model', 'Unknown')
                serial = device.get('serial', 'Unknown')
                network = device.get('network', {})
                usage_data = device.get('usage', {})
                
                total = usage_data.get('total', 0)
                percentage = usage_data.get('percentage', 0)
                
                # Determine icon based on device type
                if 'MX' in model:
                    icon = '🔥'  # Firewall
                elif 'MS' in model:
                    icon = '🔌'  # Switch
                elif 'MR' in model:
                    icon = '📡'  # Access Point
                elif 'MV' in model:
                    icon = '📹'  # Camera
                else:
                    icon = '📱'  # Generic device
                
                output.append(f"{i}. {icon} {name}")
                output.append(f"   Model: {model}")
                output.append(f"   Serial: {serial}")
                output.append(f"   Network: {network.get('name', 'Unknown')}")
                output.append(f"   Usage: {format_data_size(total)} ({percentage:.1f}%)")
                
                # Show client count if available
                clients = device.get('clients', {})
                if clients.get('counts', {}).get('total'):
                    output.append(f"   Clients: {clients['counts']['total']}")
                
                output.append("")
            
            # Analysis
            output.append("📊 Usage Analysis:")
            
            # Check for heavy users
            if results and results[0].get('usage', {}).get('percentage', 0) > 50:
                top_device = results[0]
                output.append(f"   ⚠️ Top device using {top_device['usage']['percentage']:.1f}% of total")
            
            # Device type breakdown
            device_types = {}
            for device in results:
                model_prefix = device.get('model', 'Unknown')[:2]
                device_types[model_prefix] = device_types.get(model_prefix, 0) + 1
            
            if len(device_types) > 1:
                output.append("   Device Types:")
                for prefix, count in sorted(device_types.items()):
                    output.append(f"      {prefix}: {count} devices")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("get top devices by usage", e)


def get_organization_summary_top_appliances_by_utilization(
    org_id: str,
    t0: Optional[str] = None,
    t1: Optional[str] = None,
    timespan: Optional[int] = 86400,
    quantity: Optional[int] = 10
) -> str:
    """
    🔥 Get top appliances by utilization.
    
    Shows MX appliances with highest CPU/memory utilization.
    
    Args:
        org_id: Organization ID
        t0: Start time (ISO 8601)
        t1: End time (ISO 8601)
        timespan: Time period in seconds (default: 86400 = 24 hours)
        quantity: Number of appliances to return (default: 10)
    
    Returns:
        Top appliances by utilization percentage
    """
    try:
        with safe_api_call("get top appliances by utilization"):
            # Build parameters
            params = {}
            if t0:
                params['t0'] = t0
            if t1:
                params['t1'] = t1
            elif timespan:
                params['timespan'] = timespan
            if quantity:
                params['quantity'] = quantity
            
            results = meraki.dashboard.organizations.getOrganizationSummaryTopAppliancesByUtilization(
                org_id,
                **params
            )
            
            output = ["🔥 Top Appliances by Utilization", "=" * 50, ""]
            output.append(f"Time Period: Last {timespan // 3600} hours")
            output.append("")
            
            if not results:
                output.append("No appliance data available")
                return "\n".join(output)
            
            # Show each appliance
            for i, appliance in enumerate(results, 1):
                name = appliance.get('name', appliance.get('mac', 'Unknown'))
                model = appliance.get('model', 'Unknown')
                serial = appliance.get('serial', 'Unknown')
                network = appliance.get('network', {})
                utilization = appliance.get('utilization', {}).get('average', {}).get('percentage', 0)
                
                # Determine status icon based on utilization
                if utilization > 90:
                    status_icon = '🔴'  # Critical
                elif utilization > 70:
                    status_icon = '🟡'  # Warning
                else:
                    status_icon = '🟢'  # Good
                
                output.append(f"{i}. {status_icon} {name}")
                output.append(f"   Model: {model}")
                output.append(f"   Serial: {serial}")
                output.append(f"   Network: {network.get('name', 'Unknown')}")
                output.append(f"   Utilization: {utilization:.1f}%")
                
                # Add utilization bar
                bar_length = 20
                filled = int(utilization / 100 * bar_length)
                bar = '█' * filled + '░' * (bar_length - filled)
                output.append(f"   [{bar}]")
                
                output.append("")
            
            # Analysis
            output.append("📊 Utilization Analysis:")
            
            # Count by utilization level
            critical = sum(1 for a in results if a.get('utilization', {}).get('average', {}).get('percentage', 0) > 90)
            warning = sum(1 for a in results if 70 < a.get('utilization', {}).get('average', {}).get('percentage', 0) <= 90)
            
            if critical > 0:
                output.append(f"   🔴 Critical (>90%): {critical} appliances")
            if warning > 0:
                output.append(f"   🟡 Warning (70-90%): {warning} appliances")
            
            # Recommendations
            if critical > 0:
                output.append("\n⚠️ Recommendations:")
                output.append("   • Review high-utilization appliances")
                output.append("   • Consider upgrading hardware")
                output.append("   • Optimize traffic policies")
                output.append("   • Check for resource-intensive features")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("get top appliances by utilization", e)


def get_organization_summary_top_applications_by_usage(
    org_id: str,
    t0: Optional[str] = None,
    t1: Optional[str] = None,
    timespan: Optional[int] = 86400,
    quantity: Optional[int] = 10
) -> str:
    """
    📱 Get top applications by data usage.
    
    Shows applications consuming the most bandwidth.
    
    Args:
        org_id: Organization ID
        t0: Start time (ISO 8601)
        t1: End time (ISO 8601)
        timespan: Time period in seconds (default: 86400 = 24 hours)
        quantity: Number of applications to return (default: 10)
    
    Returns:
        Top applications by data usage
    """
    try:
        with safe_api_call("get top applications by usage"):
            # Build parameters
            params = {}
            if t0:
                params['t0'] = t0
            if t1:
                params['t1'] = t1
            elif timespan:
                params['timespan'] = timespan
            if quantity:
                params['quantity'] = quantity
            
            results = meraki.dashboard.organizations.getOrganizationSummaryTopApplicationsByUsage(
                org_id,
                **params
            )
            
            output = ["📱 Top Applications by Usage", "=" * 50, ""]
            output.append(f"Time Period: Last {timespan // 3600} hours")
            output.append("")
            
            if not results:
                output.append("No application data available")
                return "\n".join(output)
            
            # Calculate total usage
            total_usage = sum(app.get('total', 0) for app in results)
            
            output.append(f"📈 Total Data Usage: {format_data_size(total_usage)}")
            output.append(f"Applications Shown: {len(results)}")
            output.append("")
            
            # Show each application
            for i, app in enumerate(results, 1):
                name = app.get('name', 'Unknown')
                total = app.get('total', 0)
                downstream = app.get('downstream', 0)
                upstream = app.get('upstream', 0)
                percentage = app.get('percentage', 0)
                
                # Determine icon based on app type
                icon = get_app_icon(name)
                
                output.append(f"{i}. {icon} {name}")
                output.append(f"   Total: {format_data_size(total)} ({percentage:.1f}%)")
                output.append(f"   ↓ Down: {format_data_size(downstream)}")
                output.append(f"   ↑ Up: {format_data_size(upstream)}")
                
                # Show ratio
                if downstream > 0:
                    ratio = upstream / downstream
                    output.append(f"   Ratio: 1:{1/ratio:.1f}")
                
                output.append("")
            
            # Analysis
            output.append("📊 Application Analysis:")
            
            # Categorize applications
            categories = {
                'streaming': [],
                'cloud': [],
                'social': [],
                'business': [],
                'other': []
            }
            
            for app in results:
                name = app.get('name', '').lower()
                if any(x in name for x in ['video', 'youtube', 'netflix', 'streaming']):
                    categories['streaming'].append(app)
                elif any(x in name for x in ['cloud', 'aws', 'azure', 'google']):
                    categories['cloud'].append(app)
                elif any(x in name for x in ['facebook', 'twitter', 'instagram', 'social']):
                    categories['social'].append(app)
                elif any(x in name for x in ['office', 'microsoft', 'salesforce', 'zoom']):
                    categories['business'].append(app)
                else:
                    categories['other'].append(app)
            
            for cat_name, apps in categories.items():
                if apps:
                    cat_usage = sum(app.get('total', 0) for app in apps)
                    cat_percentage = (cat_usage / total_usage * 100) if total_usage > 0 else 0
                    output.append(f"   {cat_name.capitalize()}: {format_data_size(cat_usage)} ({cat_percentage:.1f}%)")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("get top applications by usage", e)


def get_org_top_app_categories_by_usage(
    org_id: str,
    t0: Optional[str] = None,
    t1: Optional[str] = None,
    timespan: Optional[int] = 86400,
    quantity: Optional[int] = 10
) -> str:
    """
    📂 Get top application categories by usage.
    
    Shows application categories consuming the most bandwidth.
    
    Args:
        org_id: Organization ID
        t0: Start time (ISO 8601)
        t1: End time (ISO 8601)
        timespan: Time period in seconds (default: 86400 = 24 hours)
        quantity: Number of categories to return (default: 10)
    
    Returns:
        Top application categories by data usage
    """
    try:
        with safe_api_call("get top application categories"):
            # Build parameters
            params = {}
            if t0:
                params['t0'] = t0
            if t1:
                params['t1'] = t1
            elif timespan:
                params['timespan'] = timespan
            if quantity:
                params['quantity'] = quantity
            
            results = meraki.dashboard.organizations.getOrganizationSummaryTopApplicationsCategoriesByUsage(
                org_id,
                **params
            )
            
            output = ["📂 Top Application Categories", "=" * 50, ""]
            output.append(f"Time Period: Last {timespan // 3600} hours")
            output.append("")
            
            if not results:
                output.append("No category data available")
                return "\n".join(output)
            
            # Calculate total usage
            total_usage = sum(cat.get('total', 0) for cat in results)
            
            output.append(f"📈 Total Data Usage: {format_data_size(total_usage)}")
            output.append(f"Categories Shown: {len(results)}")
            output.append("")
            
            # Show each category
            for i, category in enumerate(results, 1):
                name = category.get('category', 'Unknown')
                total = category.get('total', 0)
                downstream = category.get('downstream', 0)
                upstream = category.get('upstream', 0)
                percentage = category.get('percentage', 0)
                
                # Determine icon
                icon = get_category_icon(name)
                
                output.append(f"{i}. {icon} {name}")
                output.append(f"   Total: {format_data_size(total)} ({percentage:.1f}%)")
                output.append(f"   ↓ Down: {format_data_size(downstream)}")
                output.append(f"   ↑ Up: {format_data_size(upstream)}")
                
                # Visual bar
                bar_length = 30
                filled = int(percentage / 100 * bar_length)
                bar = '█' * filled + '░' * (bar_length - filled)
                output.append(f"   [{bar}]")
                
                output.append("")
            
            # Analysis
            output.append("📊 Category Analysis:")
            
            # Check for concerning usage
            if results:
                top_category = results[0]
                if top_category.get('percentage', 0) > 50:
                    output.append(f"   ⚠️ {top_category['category']} using {top_category['percentage']:.1f}% of bandwidth")
                
                # Check for non-business categories
                non_business = [cat for cat in results if cat.get('category', '').lower() in 
                              ['streaming', 'social media', 'gaming', 'peer-to-peer']]
                if non_business:
                    non_business_usage = sum(cat.get('total', 0) for cat in non_business)
                    non_business_pct = (non_business_usage / total_usage * 100) if total_usage > 0 else 0
                    output.append(f"   📱 Non-business: {format_data_size(non_business_usage)} ({non_business_pct:.1f}%)")
            
            output.append("\n💡 Recommendations:")
            output.append("• Review high-usage categories")
            output.append("• Consider application control policies")
            output.append("• Monitor for shadow IT")
            output.append("• Implement QoS for critical apps")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("get top application categories", e)


def get_organization_summary_top_clients_by_usage(
    org_id: str,
    t0: Optional[str] = None,
    t1: Optional[str] = None,
    timespan: Optional[int] = 86400,
    quantity: Optional[int] = 10
) -> str:
    """
    👥 Get top clients by data usage.
    
    Shows clients/users consuming the most bandwidth.
    
    Args:
        org_id: Organization ID
        t0: Start time (ISO 8601)
        t1: End time (ISO 8601)
        timespan: Time period in seconds (default: 86400 = 24 hours)
        quantity: Number of clients to return (default: 10)
    
    Returns:
        Top clients by data usage
    """
    try:
        with safe_api_call("get top clients by usage"):
            # Build parameters
            params = {}
            if t0:
                params['t0'] = t0
            if t1:
                params['t1'] = t1
            elif timespan:
                params['timespan'] = timespan
            if quantity:
                params['quantity'] = quantity
            
            results = meraki.dashboard.organizations.getOrganizationSummaryTopClientsByUsage(
                org_id,
                **params
            )
            
            output = ["👥 Top Clients by Usage", "=" * 50, ""]
            output.append(f"Time Period: Last {timespan // 3600} hours")
            output.append("")
            
            if not results:
                output.append("No client data available")
                return "\n".join(output)
            
            # Calculate total usage
            total_usage = sum(client.get('usage', {}).get('total', 0) for client in results)
            
            output.append(f"📈 Total Data Usage: {format_data_size(total_usage)}")
            output.append(f"Clients Shown: {len(results)}")
            output.append("")
            
            # Show each client
            for i, client in enumerate(results, 1):
                name = client.get('name') or client.get('mac', 'Unknown')
                mac = client.get('mac', 'Unknown')
                network = client.get('network', {})
                usage_data = client.get('usage', {})
                
                total = usage_data.get('total', 0)
                downstream = usage_data.get('downstream', 0)
                upstream = usage_data.get('upstream', 0)
                percentage = usage_data.get('percentage', 0)
                
                output.append(f"{i}. 👤 {name}")
                if name != mac:
                    output.append(f"   MAC: {mac}")
                output.append(f"   Network: {network.get('name', 'Unknown')}")
                output.append(f"   Usage: {format_data_size(total)} ({percentage:.1f}%)")
                output.append(f"   ↓ Down: {format_data_size(downstream)}")
                output.append(f"   ↑ Up: {format_data_size(upstream)}")
                
                # Check for heavy user
                if percentage > 20:
                    output.append("   ⚠️ Heavy user")
                
                output.append("")
            
            # Analysis
            output.append("📊 Client Analysis:")
            
            # Check concentration
            if results:
                top_5_usage = sum(client.get('usage', {}).get('percentage', 0) for client in results[:5])
                output.append(f"   Top 5 clients: {top_5_usage:.1f}% of total usage")
                
                # Check for outliers
                if results[0].get('usage', {}).get('percentage', 0) > 30:
                    output.append(f"   ⚠️ Top client using excessive bandwidth")
            
            output.append("\n💡 Recommendations:")
            output.append("• Investigate heavy users")
            output.append("• Consider per-client bandwidth limits")
            output.append("• Review acceptable use policies")
            output.append("• Monitor for abnormal patterns")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("get top clients by usage", e)


def get_organization_summary_top_ssids_by_usage(
    org_id: str,
    t0: Optional[str] = None,
    t1: Optional[str] = None,
    timespan: Optional[int] = 86400,
    quantity: Optional[int] = 10
) -> str:
    """
    📶 Get top SSIDs by data usage.
    
    Shows wireless networks with highest data consumption.
    
    Args:
        org_id: Organization ID
        t0: Start time (ISO 8601)
        t1: End time (ISO 8601)
        timespan: Time period in seconds (default: 86400 = 24 hours)
        quantity: Number of SSIDs to return (default: 10)
    
    Returns:
        Top SSIDs by data usage
    """
    try:
        with safe_api_call("get top SSIDs by usage"):
            # Build parameters
            params = {}
            if t0:
                params['t0'] = t0
            if t1:
                params['t1'] = t1
            elif timespan:
                params['timespan'] = timespan
            if quantity:
                params['quantity'] = quantity
            
            results = meraki.dashboard.organizations.getOrganizationSummaryTopSsidsByUsage(
                org_id,
                **params
            )
            
            output = ["📶 Top SSIDs by Usage", "=" * 50, ""]
            output.append(f"Time Period: Last {timespan // 3600} hours")
            output.append("")
            
            if not results:
                output.append("No SSID data available")
                return "\n".join(output)
            
            # Calculate total usage
            total_usage = sum(ssid.get('usage', {}).get('total', 0) for ssid in results)
            
            output.append(f"📈 Total Wireless Usage: {format_data_size(total_usage)}")
            output.append(f"SSIDs Shown: {len(results)}")
            output.append("")
            
            # Show each SSID
            for i, ssid in enumerate(results, 1):
                name = ssid.get('name', 'Unknown SSID')
                usage_data = ssid.get('usage', {})
                
                total = usage_data.get('total', 0)
                downstream = usage_data.get('downstream', 0)
                upstream = usage_data.get('upstream', 0)
                percentage = usage_data.get('percentage', 0)
                
                # Determine icon based on SSID name
                if 'guest' in name.lower():
                    icon = '🏨'  # Guest network
                elif 'corp' in name.lower() or 'employee' in name.lower():
                    icon = '🏢'  # Corporate network
                elif 'iot' in name.lower():
                    icon = '🔌'  # IoT network
                else:
                    icon = '📶'  # Generic wireless
                
                output.append(f"{i}. {icon} {name}")
                output.append(f"   Usage: {format_data_size(total)} ({percentage:.1f}%)")
                output.append(f"   ↓ Down: {format_data_size(downstream)}")
                output.append(f"   ↑ Up: {format_data_size(upstream)}")
                
                # Client count if available
                clients_data = ssid.get('clients', {})
                if clients_data.get('counts', {}).get('total'):
                    client_count = clients_data['counts']['total']
                    output.append(f"   Clients: {client_count}")
                    
                    # Usage per client
                    if client_count > 0:
                        per_client = total / client_count
                        output.append(f"   Per Client: {format_data_size(per_client)}")
                
                output.append("")
            
            # Analysis
            output.append("📊 SSID Analysis:")
            
            # Check for guest network usage
            guest_ssids = [s for s in results if 'guest' in s.get('name', '').lower()]
            if guest_ssids:
                guest_usage = sum(s.get('usage', {}).get('total', 0) for s in guest_ssids)
                guest_pct = (guest_usage / total_usage * 100) if total_usage > 0 else 0
                output.append(f"   🏨 Guest Networks: {format_data_size(guest_usage)} ({guest_pct:.1f}%)")
            
            # Check for imbalance
            if results and results[0].get('usage', {}).get('percentage', 0) > 60:
                output.append(f"   ⚠️ Imbalanced usage - consider load distribution")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("get top SSIDs by usage", e)


def format_data_size(bytes_value: float) -> str:
    """Format bytes into human-readable size."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.2f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.2f} PB"


def get_app_icon(app_name: str) -> str:
    """Get icon for application based on name."""
    app_lower = app_name.lower()
    if any(x in app_lower for x in ['video', 'youtube', 'netflix', 'streaming']):
        return '📺'
    elif any(x in app_lower for x in ['facebook', 'twitter', 'instagram', 'social']):
        return '💬'
    elif any(x in app_lower for x in ['office', 'microsoft', 'google', 'cloud']):
        return '☁️'
    elif any(x in app_lower for x in ['game', 'gaming', 'steam']):
        return '🎮'
    elif any(x in app_lower for x in ['email', 'mail']):
        return '📧'
    elif any(x in app_lower for x in ['web', 'http']):
        return '🌐'
    else:
        return '📱'


def get_category_icon(category_name: str) -> str:
    """Get icon for category based on name."""
    cat_lower = category_name.lower()
    if 'business' in cat_lower:
        return '💼'
    elif 'streaming' in cat_lower:
        return '📺'
    elif 'social' in cat_lower:
        return '💬'
    elif 'cloud' in cat_lower:
        return '☁️'
    elif 'gaming' in cat_lower:
        return '🎮'
    elif 'security' in cat_lower:
        return '🔒'
    else:
        return '📂'


def summary_help() -> str:
    """
    ❓ Get help with summary analytics tools.
    
    Shows available tools and best practices.
    
    Returns:
        Formatted help guide
    """
    return """📊 Summary Analytics Tools Help
==================================================

Available tools for organization-wide analytics:

1. get_organization_summary_top_devices_by_usage()
   - Top devices by data consumption
   - Filter by time period
   - Shows usage percentage
   - Client counts

2. get_organization_summary_top_appliances_by_utilization()
   - MX appliances by CPU/memory usage
   - Identify overloaded devices
   - Performance monitoring
   - Capacity planning

3. get_organization_summary_top_applications_by_usage()
   - Applications consuming bandwidth
   - Upstream/downstream breakdown
   - Usage percentages
   - Traffic patterns

4. get_org_top_app_categories_by_usage()
   - Application categories overview
   - Business vs non-business
   - Policy insights
   - Shadow IT detection

5. get_organization_summary_top_clients_by_usage()
   - Heavy bandwidth users
   - Client identification
   - Usage patterns
   - Policy violations

6. get_organization_summary_top_ssids_by_usage()
   - Wireless network usage
   - SSID performance
   - Client distribution
   - Guest vs corporate

Time Parameters:
• t0/t1: Specific time range (ISO 8601)
• timespan: Duration in seconds
• Default: Last 24 hours (86400s)

Common Timespans:
• 1 hour: 3600
• 24 hours: 86400
• 7 days: 604800
• 30 days: 2592000

Usage Metrics:
📊 Total: Combined up + down
↓ Downstream: Data to clients
↑ Upstream: Data from clients
% Percentage: Share of total

Best Practices:
• Monitor daily patterns
• Set up regular reports
• Track usage trends
• Identify anomalies
• Plan capacity upgrades
• Optimize traffic policies

Analysis Tips:
• Look for outliers
• Check time patterns
• Compare locations
• Monitor growth
• Validate policies
• Document baselines

Common Issues:
• Heavy streamers
• Backup traffic
• Cloud sync storms
• Malware activity
• Policy violations
"""


def register_summary_tools(app: FastMCP, meraki_client: MerakiClient):
    """Register all summary analytics tools with the MCP server."""
    global mcp_app, meraki
    mcp_app = app
    meraki = meraki_client
    
    # Register all tools
    tools = [
        (get_organization_summary_top_devices_by_usage, "Get top devices by data usage"),
        (get_organization_summary_top_appliances_by_utilization, "Get top appliances by utilization"),
        (get_organization_summary_top_applications_by_usage, "Get top applications by usage"),
        (get_org_top_app_categories_by_usage, "Get top app categories by usage"),
        (get_organization_summary_top_clients_by_usage, "Get top clients by data usage"),
        (get_organization_summary_top_ssids_by_usage, "Get top SSIDs by usage"),
        (summary_help, "Get help with summary analytics"),
    ]
    
    for tool_func, description in tools:
        app.tool(
            name=tool_func.__name__,
            description=description
        )(tool_func)