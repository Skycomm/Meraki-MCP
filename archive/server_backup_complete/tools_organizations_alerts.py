"""
Alerts and monitoring tools for Cisco Meraki MCP server.

This module provides tools for managing organization alerts and assurance monitoring.
"""

from typing import Optional, Dict, Any, List
from datetime import datetime
import json

# Global references to be set by register function
app = None
meraki_client = None

def register_alerts_tools(mcp_app, meraki):
    """
    Register alerts tools with the MCP server.
    
    Args:
        mcp_app: MCP server instance
        meraki: Meraki client instance
    """
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    
    # ==================== ALERT PROFILES ====================
    
    @app.tool(
        name="get_org_alerts_profiles",
        description="🚨 List all alert profiles in an organization"
    )
    def get_org_alerts_profiles(
        organization_id: str
    ):
        """Get all alert profiles."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationAlertsProfiles(
                organization_id
            )
            
            response = f"# 🚨 Alert Profiles\n\n"
            
            if result and isinstance(result, list):
                response += f"**Total Profiles**: {len(result)}\n\n"
                
                for profile in result:
                    response += f"## {profile.get('description', 'Unknown')}\n"
                    response += f"- **ID**: {profile.get('id', 'N/A')}\n"
                    response += f"- **Type**: {profile.get('type', 'N/A')}\n"
                    response += f"- **Enabled**: {profile.get('enabled', False)}\n"
                    
                    # Alert conditions
                    conditions = profile.get('alertCondition', {})
                    if conditions:
                        response += f"- **Conditions**:\n"
                        if conditions.get('duration'):
                            response += f"  - Duration: {conditions['duration']} minutes\n"
                        if conditions.get('window'):
                            response += f"  - Window: {conditions['window']} minutes\n"
                        if conditions.get('bit_rate_bps'):
                            response += f"  - Bit Rate: {conditions['bit_rate_bps']} bps\n"
                        if conditions.get('loss_ratio'):
                            response += f"  - Loss Ratio: {conditions['loss_ratio']}\n"
                        if conditions.get('latency_ms'):
                            response += f"  - Latency: {conditions['latency_ms']} ms\n"
                        if conditions.get('jitter_ms'):
                            response += f"  - Jitter: {conditions['jitter_ms']} ms\n"
                        if conditions.get('mos'):
                            response += f"  - MOS: {conditions['mos']}\n"
                    
                    # Recipients
                    recipients = profile.get('recipients', {})
                    if recipients:
                        emails = recipients.get('emails', [])
                        if emails:
                            response += f"- **Email Recipients**: {', '.join(emails[:3])}"
                            if len(emails) > 3:
                                response += f" and {len(emails)-3} more"
                            response += "\n"
                        
                        http_servers = recipients.get('httpServerIds', [])
                        if http_servers:
                            response += f"- **HTTP Servers**: {len(http_servers)}\n"
                    
                    # Network tags
                    network_tags = profile.get('networkTags', [])
                    if network_tags:
                        response += f"- **Network Tags**: {', '.join(network_tags)}\n"
                    
                    response += "\n"
            else:
                response += "*No alert profiles found*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting alert profiles: {str(e)}"
    
    @app.tool(
        name="create_org_alerts_profile",
        description="🚨➕ Create a new alert profile"
    )
    def create_org_alerts_profile(
        organization_id: str,
        type: str,
        alert_condition: str,
        recipients: str,
        network_tags: str,
        description: Optional[str] = None,
        enabled: bool = True
    ):
        """
        Create a new alert profile.
        
        Args:
            organization_id: Organization ID
            type: Alert type
            alert_condition: JSON string of alert conditions
            recipients: JSON string of recipients
            network_tags: JSON string of network tags array
            description: Profile description
            enabled: Enable/disable profile
        """
        try:
            kwargs = {
                'type': type,
                'alertCondition': json.loads(alert_condition) if isinstance(alert_condition, str) else alert_condition,
                'recipients': json.loads(recipients) if isinstance(recipients, str) else recipients,
                'networkTags': json.loads(network_tags) if isinstance(network_tags, str) else network_tags,
                'enabled': enabled
            }
            
            if description:
                kwargs['description'] = description
            
            result = meraki_client.dashboard.organizations.createOrganizationAlertsProfile(
                organization_id, **kwargs
            )
            
            response = f"# ✅ Created Alert Profile\n\n"
            response += f"**Type**: {type}\n"
            response += f"**ID**: {result.get('id', 'N/A')}\n"
            response += f"**Enabled**: {enabled}\n"
            
            return response
        except Exception as e:
            return f"❌ Error creating alert profile: {str(e)}"
    
    @app.tool(
        name="update_org_alerts_profile",
        description="🚨✏️ Update an alert profile"
    )
    def update_org_alerts_profile(
        organization_id: str,
        alert_config_id: str,
        enabled: Optional[bool] = None,
        type: Optional[str] = None,
        alert_condition: Optional[str] = None,
        recipients: Optional[str] = None,
        network_tags: Optional[str] = None,
        description: Optional[str] = None
    ):
        """Update an alert profile."""
        try:
            kwargs = {}
            
            if enabled is not None:
                kwargs['enabled'] = enabled
            if type:
                kwargs['type'] = type
            if alert_condition:
                kwargs['alertCondition'] = json.loads(alert_condition) if isinstance(alert_condition, str) else alert_condition
            if recipients:
                kwargs['recipients'] = json.loads(recipients) if isinstance(recipients, str) else recipients
            if network_tags:
                kwargs['networkTags'] = json.loads(network_tags) if isinstance(network_tags, str) else network_tags
            if description:
                kwargs['description'] = description
            
            result = meraki_client.dashboard.organizations.updateOrganizationAlertsProfile(
                organization_id, alert_config_id, **kwargs
            )
            
            response = f"# ✅ Updated Alert Profile\n\n"
            response += f"**Profile ID**: {alert_config_id}\n"
            
            return response
        except Exception as e:
            return f"❌ Error updating alert profile: {str(e)}"
    
    @app.tool(
        name="delete_org_alerts_profile",
        description="🚨❌ Delete an alert profile"
    )
    def delete_org_alerts_profile(
        organization_id: str,
        alert_config_id: str
    ):
        """Delete an alert profile."""
        try:
            meraki_client.dashboard.organizations.deleteOrganizationAlertsProfile(
                organization_id, alert_config_id
            )
            
            response = f"# ✅ Deleted Alert Profile\n\n"
            response += f"**Profile ID**: {alert_config_id}\n"
            
            return response
        except Exception as e:
            return f"❌ Error deleting alert profile: {str(e)}"
    
    # ==================== ASSURANCE ALERTS ====================
    
    @app.tool(
        name="get_org_assurance_alerts",
        description="🔍 Get assurance alerts for an organization"
    )
    def get_org_assurance_alerts(
        organization_id: str,
        per_page: int = 100,
        starting_after: Optional[str] = None,
        ending_before: Optional[str] = None,
        sort_order: Optional[str] = None,
        network_id: Optional[str] = None,
        severity: Optional[str] = None,
        types: Optional[str] = None,
        ts_start: Optional[str] = None,
        ts_end: Optional[str] = None,
        category: Optional[str] = None,
        sort_by: Optional[str] = None,
        serials: Optional[str] = None,
        device_types: Optional[str] = None,
        device_tags: Optional[str] = None,
        active: Optional[bool] = None,
        dismissed: Optional[bool] = None,
        resolved: Optional[bool] = None
    ):
        """Get assurance alerts."""
        try:
            kwargs = {"perPage": per_page}
            
            if starting_after:
                kwargs["startingAfter"] = starting_after
            if ending_before:
                kwargs["endingBefore"] = ending_before
            if sort_order:
                kwargs["sortOrder"] = sort_order
            if network_id:
                kwargs["networkId"] = network_id
            if severity:
                kwargs["severity"] = severity
            if types:
                kwargs["types"] = [t.strip() for t in types.split(',')]
            if ts_start:
                kwargs["tsStart"] = ts_start
            if ts_end:
                kwargs["tsEnd"] = ts_end
            if category:
                kwargs["category"] = category
            if sort_by:
                kwargs["sortBy"] = sort_by
            if serials:
                kwargs["serials"] = [s.strip() for s in serials.split(',')]
            if device_types:
                kwargs["deviceTypes"] = [d.strip() for d in device_types.split(',')]
            if device_tags:
                kwargs["deviceTags"] = [t.strip() for t in device_tags.split(',')]
            if active is not None:
                kwargs["active"] = active
            if dismissed is not None:
                kwargs["dismissed"] = dismissed
            if resolved is not None:
                kwargs["resolved"] = resolved
            
            result = meraki_client.dashboard.organizations.getOrganizationAssuranceAlerts(
                organization_id, **kwargs
            )
            
            response = f"# 🔍 Assurance Alerts\n\n"
            
            if result and isinstance(result, list):
                response += f"**Total Alerts**: {len(result)}\n\n"
                
                # Count by severity
                severity_counts = {}
                for alert in result:
                    sev = alert.get('severity', 'unknown')
                    severity_counts[sev] = severity_counts.get(sev, 0) + 1
                
                if severity_counts:
                    response += "## Severity Summary\n"
                    for sev, count in severity_counts.items():
                        icon = "🔴" if sev == "critical" else "🟠" if sev == "warning" else "🟡" if sev == "informational" else "⚪"
                        response += f"- {icon} **{sev}**: {count}\n"
                    response += "\n"
                
                # Show alerts
                for alert in result[:10]:
                    severity = alert.get('severity', 'unknown')
                    icon = "🔴" if severity == "critical" else "🟠" if severity == "warning" else "🟡"
                    
                    response += f"## {icon} {alert.get('title', 'Unknown Alert')}\n"
                    response += f"- **ID**: {alert.get('id', 'N/A')}\n"
                    response += f"- **Type**: {alert.get('type', 'N/A')}\n"
                    response += f"- **Category**: {alert.get('category', 'N/A')}\n"
                    response += f"- **Started**: {alert.get('startedAt', 'N/A')}\n"
                    
                    # Device info
                    device = alert.get('device', {})
                    if device:
                        response += f"- **Device**: {device.get('name', device.get('serial', 'N/A'))}\n"
                    
                    # Network info
                    network = alert.get('network', {})
                    if network:
                        response += f"- **Network**: {network.get('name', network.get('id', 'N/A'))}\n"
                    
                    # Status
                    if alert.get('dismissedAt'):
                        response += f"- **Status**: Dismissed at {alert['dismissedAt']}\n"
                    elif alert.get('resolvedAt'):
                        response += f"- **Status**: Resolved at {alert['resolvedAt']}\n"
                    else:
                        response += f"- **Status**: Active\n"
                    
                    response += "\n"
                
                if len(result) > 10:
                    response += f"... and {len(result)-10} more alerts\n"
            else:
                response += "*No assurance alerts found*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting assurance alerts: {str(e)}"
    
    @app.tool(
        name="get_org_assurance_alert",
        description="🔍 Get details of a specific assurance alert"
    )
    def get_org_assurance_alert(
        organization_id: str,
        alert_id: str
    ):
        """Get specific assurance alert details."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationAssuranceAlert(
                organization_id, alert_id
            )
            
            response = f"# 🔍 Assurance Alert Details\n\n"
            
            if result:
                severity = result.get('severity', 'unknown')
                icon = "🔴" if severity == "critical" else "🟠" if severity == "warning" else "🟡"
                
                response += f"## {icon} {result.get('title', 'Unknown Alert')}\n"
                response += f"**ID**: {result.get('id', 'N/A')}\n"
                response += f"**Type**: {result.get('type', 'N/A')}\n"
                response += f"**Category**: {result.get('category', 'N/A')}\n"
                response += f"**Severity**: {severity}\n\n"
                
                # Timeline
                response += "## Timeline\n"
                response += f"- **Started**: {result.get('startedAt', 'N/A')}\n"
                if result.get('dismissedAt'):
                    response += f"- **Dismissed**: {result['dismissedAt']}\n"
                if result.get('resolvedAt'):
                    response += f"- **Resolved**: {result['resolvedAt']}\n"
                
                # Device info
                device = result.get('device', {})
                if device:
                    response += f"\n## Device\n"
                    response += f"- **Name**: {device.get('name', 'N/A')}\n"
                    response += f"- **Serial**: {device.get('serial', 'N/A')}\n"
                    response += f"- **Model**: {device.get('model', 'N/A')}\n"
                
                # Network info
                network = result.get('network', {})
                if network:
                    response += f"\n## Network\n"
                    response += f"- **Name**: {network.get('name', 'N/A')}\n"
                    response += f"- **ID**: {network.get('id', 'N/A')}\n"
                
                # Details
                details = result.get('details', {})
                if details:
                    response += f"\n## Details\n"
                    for key, value in details.items():
                        response += f"- **{key}**: {value}\n"
            else:
                response += "*Alert not found*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting alert: {str(e)}"
    
    @app.tool(
        name="dismiss_org_assurance_alerts",
        description="🔍✅ Dismiss assurance alerts"
    )
    def dismiss_org_assurance_alerts(
        organization_id: str,
        alert_ids: str
    ):
        """
        Dismiss assurance alerts.
        
        Args:
            organization_id: Organization ID
            alert_ids: Comma-separated alert IDs to dismiss
        """
        try:
            alert_list = [a.strip() for a in alert_ids.split(',')]
            
            meraki_client.dashboard.organizations.dismissOrganizationAssuranceAlerts(
                organization_id, alertIds=alert_list
            )
            
            response = f"# ✅ Dismissed Alerts\n\n"
            response += f"**Alert IDs**: {alert_ids}\n"
            response += f"**Count**: {len(alert_list)} alerts dismissed\n"
            
            return response
        except Exception as e:
            return f"❌ Error dismissing alerts: {str(e)}"
    
    @app.tool(
        name="restore_org_assurance_alerts",
        description="🔍🔄 Restore dismissed assurance alerts"
    )
    def restore_org_assurance_alerts(
        organization_id: str,
        alert_ids: str
    ):
        """
        Restore dismissed assurance alerts.
        
        Args:
            organization_id: Organization ID
            alert_ids: Comma-separated alert IDs to restore
        """
        try:
            alert_list = [a.strip() for a in alert_ids.split(',')]
            
            meraki_client.dashboard.organizations.restoreOrganizationAssuranceAlerts(
                organization_id, alertIds=alert_list
            )
            
            response = f"# ✅ Restored Alerts\n\n"
            response += f"**Alert IDs**: {alert_ids}\n"
            response += f"**Count**: {len(alert_list)} alerts restored\n"
            
            return response
        except Exception as e:
            return f"❌ Error restoring alerts: {str(e)}"
    
    @app.tool(
        name="get_org_assurance_alerts_overview",
        description="📊 Get overview of assurance alerts"
    )
    def get_org_assurance_alerts_overview(
        organization_id: str,
        network_id: Optional[str] = None,
        severity: Optional[str] = None,
        types: Optional[str] = None,
        ts_start: Optional[str] = None,
        ts_end: Optional[str] = None,
        serials: Optional[str] = None,
        device_types: Optional[str] = None,
        device_tags: Optional[str] = None,
        active: Optional[bool] = None,
        dismissed: Optional[bool] = None,
        resolved: Optional[bool] = None
    ):
        """Get assurance alerts overview."""
        try:
            kwargs = {}
            
            if network_id:
                kwargs["networkId"] = network_id
            if severity:
                kwargs["severity"] = severity
            if types:
                kwargs["types"] = [t.strip() for t in types.split(',')]
            if ts_start:
                kwargs["tsStart"] = ts_start
            if ts_end:
                kwargs["tsEnd"] = ts_end
            if serials:
                kwargs["serials"] = [s.strip() for s in serials.split(',')]
            if device_types:
                kwargs["deviceTypes"] = [d.strip() for d in device_types.split(',')]
            if device_tags:
                kwargs["deviceTags"] = [t.strip() for t in device_tags.split(',')]
            if active is not None:
                kwargs["active"] = active
            if dismissed is not None:
                kwargs["dismissed"] = dismissed
            if resolved is not None:
                kwargs["resolved"] = resolved
            
            result = meraki_client.dashboard.organizations.getOrganizationAssuranceAlertsOverview(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Assurance Alerts Overview\n\n"
            
            if result:
                # Counts by severity
                by_severity = result.get('bySeverity', [])
                if by_severity:
                    response += "## By Severity\n"
                    for item in by_severity:
                        severity = item.get('severity', 'unknown')
                        icon = "🔴" if severity == "critical" else "🟠" if severity == "warning" else "🟡"
                        response += f"- {icon} **{severity}**: {item.get('count', 0)}\n"
                    response += "\n"
                
                # Counts by type
                by_type = result.get('byAlertType', [])
                if by_type:
                    response += "## By Alert Type\n"
                    for item in by_type[:10]:
                        response += f"- **{item.get('type', 'Unknown')}**: {item.get('count', 0)}\n"
                    if len(by_type) > 10:
                        response += f"... and {len(by_type)-10} more types\n"
                    response += "\n"
                
                # Totals
                totals = result.get('totals', {})
                if totals:
                    response += "## Totals\n"
                    response += f"- **Active**: {totals.get('active', 0)}\n"
                    response += f"- **Dismissed**: {totals.get('dismissed', 0)}\n"
                    response += f"- **Resolved**: {totals.get('resolved', 0)}\n"
                    response += f"- **Total**: {totals.get('total', 0)}\n"
            else:
                response += "*No overview data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting alerts overview: {str(e)}"
    
    @app.tool(
        name="get_org_assurance_alerts_overview_by_network",
        description="📊 Get assurance alerts overview by network"
    )
    def get_org_assurance_alerts_overview_by_network(
        organization_id: str,
        per_page: int = 100,
        starting_after: Optional[str] = None,
        ending_before: Optional[str] = None,
        sort_order: Optional[str] = None,
        network_id: Optional[str] = None,
        severity: Optional[str] = None,
        types: Optional[str] = None,
        ts_start: Optional[str] = None,
        ts_end: Optional[str] = None,
        serials: Optional[str] = None,
        device_types: Optional[str] = None,
        device_tags: Optional[str] = None,
        active: Optional[bool] = None,
        dismissed: Optional[bool] = None,
        resolved: Optional[bool] = None
    ):
        """Get assurance alerts overview by network."""
        try:
            kwargs = {"perPage": per_page}
            
            if starting_after:
                kwargs["startingAfter"] = starting_after
            if ending_before:
                kwargs["endingBefore"] = ending_before
            if sort_order:
                kwargs["sortOrder"] = sort_order
            if network_id:
                kwargs["networkId"] = network_id
            if severity:
                kwargs["severity"] = severity
            if types:
                kwargs["types"] = [t.strip() for t in types.split(',')]
            if ts_start:
                kwargs["tsStart"] = ts_start
            if ts_end:
                kwargs["tsEnd"] = ts_end
            if serials:
                kwargs["serials"] = [s.strip() for s in serials.split(',')]
            if device_types:
                kwargs["deviceTypes"] = [d.strip() for d in device_types.split(',')]
            if device_tags:
                kwargs["deviceTags"] = [t.strip() for t in device_tags.split(',')]
            if active is not None:
                kwargs["active"] = active
            if dismissed is not None:
                kwargs["dismissed"] = dismissed
            if resolved is not None:
                kwargs["resolved"] = resolved
            
            result = meraki_client.dashboard.organizations.getOrganizationAssuranceAlertsOverviewByNetwork(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Alerts Overview by Network\n\n"
            
            if result and isinstance(result, list):
                response += f"**Total Networks**: {len(result)}\n\n"
                
                for network in result[:10]:
                    response += f"## {network.get('name', 'Unknown Network')}\n"
                    response += f"- **Network ID**: {network.get('id', 'N/A')}\n"
                    
                    # Alert counts
                    counts = network.get('alertCounts', {})
                    if counts:
                        response += f"- **Critical**: {counts.get('critical', 0)}\n"
                        response += f"- **Warning**: {counts.get('warning', 0)}\n"
                        response += f"- **Informational**: {counts.get('informational', 0)}\n"
                        response += f"- **Total**: {counts.get('total', 0)}\n"
                    
                    response += "\n"
                
                if len(result) > 10:
                    response += f"... and {len(result)-10} more networks\n"
            else:
                response += "*No network overview data found*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting network overview: {str(e)}"
    
    @app.tool(
        name="get_org_assurance_alerts_overview_by_type",
        description="📊 Get assurance alerts overview grouped by type"
    )
    def get_org_assurance_alerts_overview_by_type(
        organization_id: str,
        per_page: int = 100,
        starting_after: Optional[str] = None,
        ending_before: Optional[str] = None,
        sort_order: Optional[str] = None,
        network_id: Optional[str] = None,
        severity: Optional[str] = None,
        types: Optional[str] = None,
        ts_start: Optional[str] = None,
        ts_end: Optional[str] = None,
        serials: Optional[str] = None,
        device_types: Optional[str] = None,
        device_tags: Optional[str] = None,
        active: Optional[bool] = None,
        dismissed: Optional[bool] = None,
        resolved: Optional[bool] = None
    ):
        """Get assurance alerts overview by type."""
        try:
            kwargs = {"perPage": per_page}
            
            if starting_after:
                kwargs["startingAfter"] = starting_after
            if ending_before:
                kwargs["endingBefore"] = ending_before
            if sort_order:
                kwargs["sortOrder"] = sort_order
            if network_id:
                kwargs["networkId"] = network_id
            if severity:
                kwargs["severity"] = severity
            if types:
                kwargs["types"] = [t.strip() for t in types.split(',')]
            if ts_start:
                kwargs["tsStart"] = ts_start
            if ts_end:
                kwargs["tsEnd"] = ts_end
            if serials:
                kwargs["serials"] = [s.strip() for s in serials.split(',')]
            if device_types:
                kwargs["deviceTypes"] = [d.strip() for d in device_types.split(',')]
            if device_tags:
                kwargs["deviceTags"] = [t.strip() for t in device_tags.split(',')]
            if active is not None:
                kwargs["active"] = active
            if dismissed is not None:
                kwargs["dismissed"] = dismissed
            if resolved is not None:
                kwargs["resolved"] = resolved
            
            result = meraki_client.dashboard.organizations.getOrganizationAssuranceAlertsOverviewByType(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Alerts Overview by Type\n\n"
            
            if result and isinstance(result, list):
                response += f"**Total Alert Types**: {len(result)}\n\n"
                
                for alert_type in result[:15]:
                    response += f"## {alert_type.get('type', 'Unknown Type')}\n"
                    response += f"- **Count**: {alert_type.get('count', 0)}\n"
                    response += f"- **Active**: {alert_type.get('active', 0)}\n"
                    response += f"- **Dismissed**: {alert_type.get('dismissed', 0)}\n"
                    response += f"- **Resolved**: {alert_type.get('resolved', 0)}\n\n"
                
                if len(result) > 15:
                    response += f"... and {len(result)-15} more alert types\n"
            else:
                response += "*No type overview data found*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting type overview: {str(e)}"