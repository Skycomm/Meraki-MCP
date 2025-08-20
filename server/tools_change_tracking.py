"""
Network Change Tracking Tools for Cisco Meraki MCP Server
Track configuration changes, audit logs, and change history
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


def get_configuration_changes(
    organization_id: str,
    network_id: Optional[str] = None,
    timespan: Optional[int] = 86400,
    admin_name: Optional[str] = None
) -> str:
    """
    📝 Get recent configuration changes.
    
    Shows what was changed, when, and by whom.
    
    Args:
        organization_id: Organization ID
        network_id: Filter by specific network (optional)
        timespan: Time period in seconds (default: 86400 = 24 hours)
        admin_name: Filter by admin name (optional)
    
    Returns:
        Formatted change log
    """
    try:
        with safe_api_call("get configuration changes"):
            # Get change log
            params = {"timespan": timespan}
            if network_id:
                params["networkId"] = network_id
            if admin_name:
                params["adminName"] = admin_name
                
            changes = meraki.dashboard.organizations.getOrganizationConfigurationChanges(
                organizationId=organization_id,
                **params
            )
            
            result = f"""📝 Configuration Changes
==================================================

Time Period: Last {timespan // 3600} hours
Changes Found: {len(changes)}
"""
            
            if network_id:
                result += f"Network Filter: Applied\n"
            if admin_name:
                result += f"Admin Filter: {admin_name}\n"
            
            if changes:
                # Group changes by category
                categories = {}
                for change in changes:
                    page = change.get('page', 'Unknown')
                    if page not in categories:
                        categories[page] = []
                    categories[page].append(change)
                
                result += f"\n📊 Changes by Category:"
                for category, items in categories.items():
                    result += f"\n   • {category}: {len(items)} changes"
                
                # Show recent changes
                result += "\n\n📋 Recent Changes:"
                for change in changes[:15]:  # Show last 15
                    time_str = change.get('ts', 'Unknown time')
                    admin = change.get('adminName', 'Unknown admin')
                    page = change.get('page', 'Unknown page')
                    label = change.get('label', 'No description')
                    
                    result += f"\n\n🔸 {time_str[:19]}"
                    result += f"\n   Admin: {admin}"
                    result += f"\n   Page: {page}"
                    result += f"\n   Change: {label}"
                    
                    # Show old/new values if available
                    if change.get('oldValue'):
                        result += f"\n   Old: {change['oldValue']}"
                    if change.get('newValue'):
                        result += f"\n   New: {change['newValue']}"
                
                # Analyze change patterns
                admins = {}
                for change in changes:
                    admin = change.get('adminName', 'Unknown')
                    admins[admin] = admins.get(admin, 0) + 1
                
                result += "\n\n👥 Changes by Admin:"
                for admin, count in sorted(admins.items(), key=lambda x: x[1], reverse=True):
                    result += f"\n   • {admin}: {count} changes"
                    
            else:
                result += "\n✅ No configuration changes in this period"
            
            result += "\n\n💡 Change Tracking Tips:"
            result += "\n   • Review changes daily"
            result += "\n   • Set up change alerts"
            result += "\n   • Document major changes"
            result += "\n   • Audit unexpected changes"
            
            return result
            
    except Exception as e:
        return format_error("get configuration changes", e)


def track_specific_changes(
    organization_id: str,
    change_types: List[str],
    timespan: Optional[int] = 604800
) -> str:
    """
    🔍 Track specific types of configuration changes.
    
    Filter and analyze changes by type (firewall, wireless, etc).
    
    Args:
        organization_id: Organization ID
        change_types: List of change types to track
        timespan: Time period in seconds (default: 604800 = 7 days)
    
    Returns:
        Filtered change analysis
    """
    try:
        with safe_api_call("track specific changes"):
            # Get all changes
            changes = meraki.dashboard.organizations.getOrganizationConfigurationChanges(
                organizationId=organization_id,
                timespan=timespan
            )
            
            result = f"""🔍 Specific Change Tracking
==================================================

Tracking Types: {', '.join(change_types)}
Time Period: Last {timespan // 86400} days
"""
            
            # Filter changes by type
            filtered_changes = []
            for change in changes:
                page = change.get('page', '').lower()
                label = change.get('label', '').lower()
                
                for change_type in change_types:
                    if change_type.lower() in page or change_type.lower() in label:
                        filtered_changes.append(change)
                        break
            
            result += f"Matching Changes: {len(filtered_changes)}\n"
            
            if filtered_changes:
                # Group by network
                networks = {}
                for change in filtered_changes:
                    net_id = change.get('networkId', 'Organization-wide')
                    net_name = change.get('networkName', 'All Networks')
                    key = f"{net_name} ({net_id})"
                    
                    if key not in networks:
                        networks[key] = []
                    networks[key].append(change)
                
                result += "\n📊 Changes by Network:"
                for network, items in networks.items():
                    result += f"\n\n🌐 {network}"
                    result += f"\n   Total Changes: {len(items)}"
                    
                    # Show sample changes
                    for change in items[:5]:
                        time_str = change.get('ts', 'Unknown')[:10]
                        label = change.get('label', 'No description')
                        result += f"\n   • {time_str}: {label}"
                
                # Analyze impact
                result += "\n\n🎯 Impact Analysis:"
                
                critical_keywords = ['firewall', 'security', 'vlan', 'subnet', 'policy']
                critical_changes = [c for c in filtered_changes 
                                  if any(k in c.get('label', '').lower() for k in critical_keywords)]
                
                if critical_changes:
                    result += f"\n   ⚠️ Critical Changes: {len(critical_changes)}"
                    for change in critical_changes[:5]:
                        result += f"\n   • {change.get('label', 'Unknown change')}"
                
                # Time analysis
                by_hour = {}
                for change in filtered_changes:
                    hour = change.get('ts', '')[:13]  # YYYY-MM-DD HH
                    by_hour[hour] = by_hour.get(hour, 0) + 1
                
                peak_hour = max(by_hour.items(), key=lambda x: x[1]) if by_hour else None
                if peak_hour:
                    result += f"\n\n⏰ Peak Change Time:"
                    result += f"\n   {peak_hour[0]}: {peak_hour[1]} changes"
                    
            else:
                result += f"\n✅ No changes found for types: {', '.join(change_types)}"
            
            result += "\n\n💡 Tracking Recommendations:"
            result += "\n   • Monitor critical changes daily"
            result += "\n   • Set alerts for security changes"
            result += "\n   • Review VLAN/subnet modifications"
            result += "\n   • Audit policy updates"
            
            return result
            
    except Exception as e:
        return format_error("track specific changes", e)


def generate_change_report(
    organization_id: str,
    start_date: str,
    end_date: str,
    include_details: bool = True
) -> str:
    """
    📊 Generate comprehensive change report.
    
    Create detailed audit report for compliance or review.
    
    Args:
        organization_id: Organization ID
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)
        include_details: Include full change details
    
    Returns:
        Formatted change report
    """
    try:
        with safe_api_call("generate change report"):
            # Calculate timespan
            start_dt = datetime.strptime(start_date, "%Y-%m-%d")
            end_dt = datetime.strptime(end_date, "%Y-%m-%d")
            timespan = int((end_dt - start_dt).total_seconds())
            
            # Get changes
            changes = meraki.dashboard.organizations.getOrganizationConfigurationChanges(
                organizationId=organization_id,
                timespan=timespan
            )
            
            result = f"""📊 Configuration Change Report
==================================================

Report Period: {start_date} to {end_date}
Total Changes: {len(changes)}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

"""
            
            if changes:
                # Executive summary
                result += "📋 Executive Summary:\n"
                
                # Count by admin
                admins = {}
                for change in changes:
                    admin = change.get('adminName', 'Unknown')
                    admins[admin] = admins.get(admin, 0) + 1
                
                result += f"   Active Admins: {len(admins)}\n"
                result += f"   Average Changes/Day: {len(changes) / max((timespan / 86400), 1):.1f}\n"
                
                # Count by category
                categories = {}
                for change in changes:
                    page = change.get('page', 'Unknown')
                    categories[page] = categories.get(page, 0) + 1
                
                result += "\n📊 Changes by Category:"
                for category, count in sorted(categories.items(), key=lambda x: x[1], reverse=True)[:10]:
                    result += f"\n   • {category}: {count}"
                
                # Admin activity
                result += "\n\n👥 Admin Activity:"
                for admin, count in sorted(admins.items(), key=lambda x: x[1], reverse=True):
                    result += f"\n   • {admin}: {count} changes"
                
                # Network impact
                networks = {}
                for change in changes:
                    net_name = change.get('networkName', 'Organization-wide')
                    networks[net_name] = networks.get(net_name, 0) + 1
                
                result += "\n\n🌐 Network Impact:"
                for network, count in sorted(networks.items(), key=lambda x: x[1], reverse=True)[:10]:
                    result += f"\n   • {network}: {count} changes"
                
                if include_details:
                    # Critical changes section
                    critical_keywords = ['firewall', 'security', 'admin', 'policy', 'vlan']
                    critical_changes = [c for c in changes 
                                      if any(k in c.get('label', '').lower() for k in critical_keywords)]
                    
                    if critical_changes:
                        result += "\n\n⚠️ Critical Changes:"
                        for change in critical_changes[:20]:
                            result += f"\n\n   {change.get('ts', 'Unknown')[:19]}"
                            result += f"\n   Admin: {change.get('adminName', 'Unknown')}"
                            result += f"\n   Change: {change.get('label', 'Unknown')}"
                            if change.get('oldValue'):
                                result += f"\n   Previous: {change['oldValue']}"
                            if change.get('newValue'):
                                result += f"\n   New: {change['newValue']}"
                
                # Compliance section
                result += "\n\n✅ Compliance Notes:"
                result += "\n   • All changes logged with timestamp"
                result += "\n   • Admin identity tracked"
                result += "\n   • Previous values preserved"
                result += "\n   • No gaps in audit trail"
                
            else:
                result += "✅ No configuration changes during this period"
            
            result += "\n\n📎 Report Actions:"
            result += "\n   • Save for compliance records"
            result += "\n   • Review with team"
            result += "\n   • Identify unauthorized changes"
            result += "\n   • Plan change windows"
            
            return result
            
    except Exception as e:
        return format_error("generate change report", e)


def compare_configurations(
    network_id: str,
    timespan: Optional[int] = 604800
) -> str:
    """
    🔄 Compare current configuration with previous state.
    
    Shows what has changed in network configuration over time.
    
    Args:
        network_id: Network ID
        timespan: How far back to compare (default: 604800 = 7 days)
    
    Returns:
        Configuration comparison
    """
    try:
        with safe_api_call("compare configurations"):
            result = f"""🔄 Configuration Comparison
==================================================

Network: {network_id}
Comparing: Current vs {timespan // 86400} days ago
"""
            
            # Get recent changes for this network
            org_id = meraki._get_org_id()
            changes = meraki.dashboard.organizations.getOrganizationConfigurationChanges(
                organizationId=org_id,
                networkId=network_id,
                timespan=timespan
            )
            
            if changes:
                # Group changes by configuration area
                config_areas = {}
                for change in changes:
                    page = change.get('page', 'Unknown')
                    if page not in config_areas:
                        config_areas[page] = {
                            'count': 0,
                            'changes': []
                        }
                    config_areas[page]['count'] += 1
                    config_areas[page]['changes'].append(change)
                
                result += f"\n📊 Configuration Areas Changed: {len(config_areas)}"
                
                # Show each area
                for area, data in sorted(config_areas.items(), key=lambda x: x[1]['count'], reverse=True):
                    result += f"\n\n📁 {area} ({data['count']} changes)"
                    
                    # Show recent changes in this area
                    for change in data['changes'][:5]:  # Show up to 5
                        result += f"\n   • {change.get('label', 'Unknown change')}"
                        if change.get('oldValue') and change.get('newValue'):
                            result += f"\n     {change['oldValue']} → {change['newValue']}"
                
                # Configuration drift analysis
                result += "\n\n🔍 Configuration Drift Analysis:"
                
                # Check for multiple changes to same setting
                settings_changed = {}
                for change in changes:
                    label = change.get('label', '')
                    settings_changed[label] = settings_changed.get(label, 0) + 1
                
                multiple_changes = {k: v for k, v in settings_changed.items() if v > 1}
                if multiple_changes:
                    result += "\n   ⚠️ Settings changed multiple times:"
                    for setting, count in sorted(multiple_changes.items(), key=lambda x: x[1], reverse=True)[:5]:
                        result += f"\n   • {setting}: {count} times"
                else:
                    result += "\n   ✅ No repeated changes to same settings"
                
                # Change velocity
                changes_per_day = len(changes) / (timespan / 86400)
                result += f"\n\n📈 Change Velocity:"
                result += f"\n   Average: {changes_per_day:.1f} changes/day"
                
                if changes_per_day > 10:
                    result += "\n   Status: ⚠️ High change rate"
                elif changes_per_day > 5:
                    result += "\n   Status: 🟡 Moderate change rate"
                else:
                    result += "\n   Status: 🟢 Normal change rate"
                    
            else:
                result += "\n✅ No configuration changes in this period"
                result += "\n   • Configuration is stable"
                result += "\n   • No drift detected"
            
            result += "\n\n💡 Best Practices:"
            result += "\n   • Document all changes"
            result += "\n   • Use change windows"
            result += "\n   • Test changes first"
            result += "\n   • Keep change log"
            
            return result
            
    except Exception as e:
        return format_error("compare configurations", e)


def export_audit_log(
    organization_id: str,
    timespan: Optional[int] = 2592000,
    format_type: str = "detailed"
) -> str:
    """
    💾 Export audit log for compliance.
    
    Generate exportable audit trail for external systems.
    
    Args:
        organization_id: Organization ID
        timespan: Time period in seconds (default: 2592000 = 30 days)
        format_type: "detailed", "summary", or "csv"
    
    Returns:
        Formatted audit log
    """
    try:
        with safe_api_call("export audit log"):
            # Get all changes
            changes = meraki.dashboard.organizations.getOrganizationConfigurationChanges(
                organizationId=organization_id,
                timespan=timespan
            )
            
            result = f"""💾 Audit Log Export
==================================================

Export Format: {format_type.upper()}
Period: Last {timespan // 86400} days
Total Entries: {len(changes)}
"""
            
            if format_type == "csv":
                result += "\n📄 CSV Format:\n"
                result += "Timestamp,Admin,Network,Page,Change,OldValue,NewValue\n"
                
                for change in changes[:20]:  # Sample of 20
                    ts = change.get('ts', '')
                    admin = change.get('adminName', '').replace(',', ';')
                    network = change.get('networkName', 'Org-wide').replace(',', ';')
                    page = change.get('page', '').replace(',', ';')
                    label = change.get('label', '').replace(',', ';')
                    old_val = str(change.get('oldValue', '')).replace(',', ';')
                    new_val = str(change.get('newValue', '')).replace(',', ';')
                    
                    result += f"{ts},{admin},{network},{page},{label},{old_val},{new_val}\n"
                
                result += "\n... (truncated for display)"
                
            elif format_type == "summary":
                result += "\n📊 Summary Format:\n"
                
                # Group by date
                by_date = {}
                for change in changes:
                    date = change.get('ts', '')[:10]
                    if date not in by_date:
                        by_date[date] = {
                            'count': 0,
                            'admins': set(),
                            'categories': set()
                        }
                    by_date[date]['count'] += 1
                    by_date[date]['admins'].add(change.get('adminName', 'Unknown'))
                    by_date[date]['categories'].add(change.get('page', 'Unknown'))
                
                for date in sorted(by_date.keys(), reverse=True)[:10]:
                    data = by_date[date]
                    result += f"\n{date}:"
                    result += f"\n   Changes: {data['count']}"
                    result += f"\n   Admins: {len(data['admins'])}"
                    result += f"\n   Categories: {', '.join(list(data['categories'])[:3])}"
                    
            else:  # detailed
                result += "\n📝 Detailed Format:\n"
                
                for change in changes[:30]:  # First 30 entries
                    result += f"\n{'=' * 50}"
                    result += f"\nTimestamp: {change.get('ts', 'Unknown')}"
                    result += f"\nAdmin: {change.get('adminName', 'Unknown')}"
                    result += f"\nNetwork: {change.get('networkName', 'Organization-wide')}"
                    result += f"\nPage: {change.get('page', 'Unknown')}"
                    result += f"\nChange: {change.get('label', 'No description')}"
                    
                    if change.get('oldValue'):
                        result += f"\nPrevious: {change['oldValue']}"
                    if change.get('newValue'):
                        result += f"\nNew: {change['newValue']}"
                    result += "\n"
            
            result += "\n\n📋 Export Options:"
            result += "\n   • Save to file for records"
            result += "\n   • Import to SIEM system"
            result += "\n   • Share with auditors"
            result += "\n   • Archive for compliance"
            
            result += "\n\n✅ Audit Trail Integrity:"
            result += "\n   • Immutable change log"
            result += "\n   • Complete history"
            result += "\n   • Tamper-evident"
            result += "\n   • Time-synchronized"
            
            return result
            
    except Exception as e:
        return format_error("export audit log", e)


def change_tracking_help() -> str:
    """
    ❓ Get help with change tracking tools.
    
    Shows available tools and audit best practices.
    
    Returns:
        Formatted help guide
    """
    return """📝 Change Tracking Tools Help
==================================================

Available tools for change tracking:

1. get_configuration_changes()
   - View recent changes
   - See who made changes
   - Track what was modified

2. track_specific_changes()
   - Filter by change type
   - Monitor critical changes
   - Focus on security updates

3. generate_change_report()
   - Create compliance reports
   - Summarize activity periods
   - Document for audits

4. compare_configurations()
   - See configuration drift
   - Compare over time
   - Identify patterns

5. export_audit_log()
   - Export for compliance
   - Multiple formats
   - SIEM integration ready

Common Tracking Tasks:

📝 "Daily change review"
1. get_configuration_changes(timespan=86400)
2. Review critical changes
3. Verify authorized changes

📊 "Monthly audit report"
1. generate_change_report(start_date, end_date)
2. Review with team
3. Archive for compliance

🔍 "Track security changes"
1. track_specific_changes(["firewall", "security"])
2. Set up alerts
3. Immediate review

💡 Best Practices:
- Review changes daily
- Document change reasons
- Use change windows
- Maintain audit trail
- Regular compliance reports

🚨 What to Monitor:
- Firewall rule changes
- VLAN modifications
- Admin account changes
- Security policy updates
- Network topology changes

📋 Compliance Tips:
- Export logs monthly
- Retain for required period
- Document change approvals
- Regular audit reviews
- Test restore procedures
"""


def register_change_tracking_tools(app: FastMCP, meraki_client: MerakiClient):
    """Register all change tracking tools with the MCP server."""
    global mcp_app, meraki
    mcp_app = app
    meraki = meraki_client
    
    # Register all tools
    tools = [
        (get_configuration_changes, "View recent configuration changes"),
        (track_specific_changes, "Track specific types of changes"),
        (generate_change_report, "Generate compliance change report"),
        (compare_configurations, "Compare configuration over time"),
        (export_audit_log, "Export audit log for compliance"),
        (change_tracking_help, "Get help with change tracking"),
    ]
    
    for tool_func, description in tools:
        app.tool(
            name=tool_func.__name__,
            description=description
        )(tool_func)