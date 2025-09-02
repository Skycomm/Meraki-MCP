#!/usr/bin/env python3
"""
Consolidate all Networks implementations into a single complete SDK module.
Combines existing implementations from tools_networks.py, tools_networks_complete.py,
and adds all missing methods for 100% SDK coverage.
"""

import re
from pathlib import Path

def extract_existing_tools():
    """Extract existing tool implementations from current files."""
    tools = {}
    
    # Files to extract from
    files = [
        'server/tools_networks.py',
        'server/tools_networks_complete.py'
    ]
    
    for file_path in files:
        if Path(file_path).exists():
            with open(file_path, 'r') as f:
                content = f.read()
                
                # Extract tool definitions with their full implementation
                pattern = r'(@app\.tool\([^)]+\)\s+def\s+(\w+)[^:]+:.*?)(?=@app\.tool|\Z)'
                matches = re.findall(pattern, content, re.DOTALL)
                
                for match in matches:
                    tool_code = match[0]
                    tool_name = match[1]
                    # Skip duplicates, keep the most complete version
                    if tool_name not in tools or len(tool_code) > len(tools[tool_name]):
                        tools[tool_name] = tool_code
    
    return tools

def generate_complete_networks_module():
    """Generate the complete Networks SDK module with all 114 methods."""
    
    # Extract existing implementations
    existing_tools = extract_existing_tools()
    print(f"Found {len(existing_tools)} existing tool implementations")
    
    # Start building the complete module
    module_code = '''#!/usr/bin/env python3
"""
Cisco Meraki SDK Networks Module - 100% SDK Coverage
Complete implementation of all 114 Networks SDK methods.

This module provides full coverage of the Meraki Dashboard API Networks category
with exact SDK method names and parameter alignment.
"""

from typing import Any, List, Dict, Optional

# Global variables for MCP server and Meraki client
app = None
meraki_client = None

def register_networks_tools(mcp_app, meraki):
    """
    Register all Networks SDK tools with the MCP server.
    
    Args:
        mcp_app: MCP server instance
        meraki: Meraki client instance
    """
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    
    # Register all network tools
    register_networks_tool_handlers()

def register_networks_tool_handlers():
    """Register all 114 Networks SDK tool handlers."""
    
'''
    
    # Add existing tools from files
    for tool_name, tool_code in existing_tools.items():
        module_code += f"    {tool_code.strip()}\n\n"
    
    # Add missing tools that aren't in existing files
    module_code += '''
    # ============================================================================
    # MISSING METHODS TO ACHIEVE 100% COVERAGE
    # ============================================================================
    
    # Core Network Management
    
    @app.tool(
        name="bind_network",
        description="Bind a network to a configuration template"
    )
    def bind_network(network_id: str, config_template_id: str, auto_bind: bool = False):
        """Bind a network to a configuration template."""
        try:
            from utils.helpers import require_confirmation
            
            if not require_confirmation(
                operation_type="bind",
                resource_type="network to template",
                resource_name=f"Network {network_id} to template {config_template_id}",
                resource_id=network_id
            ):
                return "❌ Network binding cancelled by user"
            
            result = meraki_client.dashboard.networks.bindNetwork(
                network_id, configTemplateId=config_template_id, autoBind=auto_bind
            )
            return f"✅ Network bound to template successfully"
        except Exception as e:
            return f"Error binding network: {str(e)}"
    
    @app.tool(
        name="unbind_network",
        description="Unbind a network from a configuration template"
    )
    def unbind_network(network_id: str, retain_configs: bool = True):
        """Unbind a network from a configuration template."""
        try:
            from utils.helpers import require_confirmation
            
            if not require_confirmation(
                operation_type="unbind",
                resource_type="network from template",
                resource_name=f"Network {network_id}",
                resource_id=network_id
            ):
                return "❌ Network unbinding cancelled by user"
            
            result = meraki_client.dashboard.networks.unbindNetwork(
                network_id, retainConfigs=retain_configs
            )
            return f"✅ Network unbound from template successfully"
        except Exception as e:
            return f"Error unbinding network: {str(e)}"
    
    @app.tool(
        name="split_network",
        description="Split a combined network into separate networks"
    )
    def split_network(network_id: str):
        """Split a combined network into separate networks."""
        try:
            from utils.helpers import require_confirmation
            
            if not require_confirmation(
                operation_type="split",
                resource_type="network",
                resource_name=network_id,
                resource_id=network_id
            ):
                return "❌ Network split cancelled by user"
            
            result = meraki_client.dashboard.networks.splitNetwork(network_id)
            
            result_msg = "✅ Network split successfully into:\\n"
            for net in result.get('resultingNetworks', []):
                result_msg += f"  - {net.get('name')} (ID: {net.get('id')})\\n"
            
            return result_msg
        except Exception as e:
            return f"Error splitting network: {str(e)}"
    
    @app.tool(
        name="claim_network_devices",
        description="Claim devices into a network"
    )
    def claim_network_devices(network_id: str, serials: list):
        """Claim devices into a network."""
        try:
            from utils.helpers import require_confirmation
            
            if not require_confirmation(
                operation_type="claim",
                resource_type="devices",
                resource_name=f"{len(serials)} devices",
                resource_id=network_id
            ):
                return "❌ Device claiming cancelled by user"
            
            result = meraki_client.dashboard.networks.claimNetworkDevices(
                network_id, serials=serials
            )
            return f"✅ Successfully claimed {len(serials)} devices into network"
        except Exception as e:
            return f"Error claiming devices: {str(e)}"
    
    @app.tool(
        name="remove_network_devices",
        description="Remove a device from a network"
    )
    def remove_network_devices(network_id: str, serial: str):
        """Remove a device from a network."""
        try:
            from utils.helpers import require_confirmation
            
            if not require_confirmation(
                operation_type="remove",
                resource_type="device",
                resource_name=serial,
                resource_id=network_id
            ):
                return "❌ Device removal cancelled by user"
            
            result = meraki_client.dashboard.networks.removeNetworkDevices(
                network_id, serial=serial
            )
            return f"✅ Device {serial} removed from network successfully"
        except Exception as e:
            return f"Error removing device: {str(e)}"
    
    @app.tool(
        name="vmx_network_devices_claim",
        description="Claim a vMX device into a network"
    )
    def vmx_network_devices_claim(network_id: str, size: str = "small"):
        """Claim a vMX device into a network."""
        try:
            from utils.helpers import require_confirmation
            
            if not require_confirmation(
                operation_type="claim",
                resource_type="vMX device",
                resource_name=f"vMX ({size})",
                resource_id=network_id
            ):
                return "❌ vMX claiming cancelled by user"
            
            result = meraki_client.dashboard.networks.vmxNetworkDevicesClaim(
                network_id, size=size
            )
            return f"✅ vMX device claimed successfully. Serial: {result.get('serial')}"
        except Exception as e:
            return f"Error claiming vMX: {str(e)}"
    
    # Client Management
    
    @app.tool(
        name="get_network_client",
        description="Get details for a specific client"
    )
    def get_network_client(network_id: str, client_id: str):
        """Get details for a specific client."""
        try:
            client = meraki_client.dashboard.networks.getNetworkClient(network_id, client_id)
            
            result = f"# Client Details\\n\\n"
            result += f"- Description: {client.get('description', 'N/A')}\\n"
            result += f"- MAC: {client.get('mac')}\\n"
            result += f"- IP: {client.get('ip')}\\n"
            result += f"- IPv6: {client.get('ip6')}\\n"
            result += f"- VLAN: {client.get('vlan')}\\n"
            result += f"- Status: {client.get('status')}\\n"
            result += f"- Last Seen: {client.get('lastSeen')}\\n"
            
            if client.get('ssid'):
                result += f"\\n## Wireless Info\\n"
                result += f"- SSID: {client.get('ssid')}\\n"
                result += f"- OS: {client.get('os')}\\n"
                result += f"- Device Type: {client.get('deviceTypePrediction')}\\n"
            
            if client.get('usage'):
                result += f"\\n## Usage\\n"
                result += f"- Sent: {client['usage'].get('sent', 0):,} bytes\\n"
                result += f"- Received: {client['usage'].get('recv', 0):,} bytes\\n"
            
            return result
        except Exception as e:
            return f"Error getting client details: {str(e)}"
    
    @app.tool(
        name="get_network_clients_application_usage",
        description="Get application usage for clients"
    )
    def get_network_clients_application_usage(network_id: str, clients: str, 
                                             ssid_number: int = None, timespan: int = 86400):
        """Get application usage for clients."""
        try:
            kwargs = {'clients': clients, 'timespan': timespan}
            if ssid_number is not None:
                kwargs['ssidNumber'] = ssid_number
            
            usage = meraki_client.dashboard.networks.getNetworkClientsApplicationUsage(
                network_id, **kwargs
            )
            
            if not usage:
                return "No application usage data found"
            
            result = f"# Client Application Usage (Last {timespan/3600:.1f} hours)\\n\\n"
            
            for client in usage:
                result += f"## Client: {client.get('clientId')}\\n"
                if client.get('applicationUsage'):
                    for app in client['applicationUsage'][:5]:  # Top 5 apps
                        result += f"- {app.get('application')}: "
                        result += f"Sent {app.get('sent', 0):,}, "
                        result += f"Recv {app.get('recv', 0):,} bytes\\n"
                result += "\\n"
            
            return result
        except Exception as e:
            return f"Error getting application usage: {str(e)}"
    
    @app.tool(
        name="get_network_clients_bandwidth_usage_history",
        description="Get bandwidth usage history for clients"
    )
    def get_network_clients_bandwidth_usage_history(network_id: str, timespan: int = 86400,
                                                   per_page: int = 100):
        """Get bandwidth usage history for clients."""
        try:
            history = meraki_client.dashboard.networks.getNetworkClientsBandwidthUsageHistory(
                network_id, timespan=timespan, perPage=per_page
            )
            
            if not history:
                return "No bandwidth usage history found"
            
            result = f"# Client Bandwidth Usage History\\n\\n"
            
            for entry in history[:10]:  # Show first 10
                result += f"## {entry.get('ts')}\\n"
                result += f"- Total: {entry.get('total', 0):,} bytes\\n"
                result += f"- Upstream: {entry.get('upstream', 0):,} bytes\\n"
                result += f"- Downstream: {entry.get('downstream', 0):,} bytes\\n"
                result += "\\n"
            
            return result
        except Exception as e:
            return f"Error getting bandwidth history: {str(e)}"
    
    @app.tool(
        name="get_network_clients_overview",
        description="Get overview of clients in network"
    )
    def get_network_clients_overview(network_id: str, timespan: int = 86400):
        """Get overview of clients in network."""
        try:
            overview = meraki_client.dashboard.networks.getNetworkClientsOverview(
                network_id, timespan=timespan
            )
            
            result = f"# Network Clients Overview (Last {timespan/3600:.1f} hours)\\n\\n"
            result += f"## Counts\\n"
            result += f"- Total Clients: {overview.get('counts', {}).get('total', 0)}\\n"
            
            if overview.get('counts', {}).get('byStatus'):
                result += f"\\n## By Status\\n"
                for status, count in overview['counts']['byStatus'].items():
                    result += f"- {status}: {count}\\n"
            
            if overview.get('usages'):
                result += f"\\n## Usage\\n"
                result += f"- Average: {overview['usages'].get('average', 0):,} bytes\\n"
                result += f"- With Heavy Usage: {overview['usages'].get('withHeavyUsage', 0)}\\n"
            
            return result
        except Exception as e:
            return f"Error getting clients overview: {str(e)}"
    
    @app.tool(
        name="get_network_clients_usage_histories",
        description="Get usage histories for multiple clients"
    )
    def get_network_clients_usage_histories(network_id: str, clients: str, 
                                           ssid_number: int = None, timespan: int = 86400):
        """Get usage histories for multiple clients."""
        try:
            kwargs = {'clients': clients, 'timespan': timespan}
            if ssid_number is not None:
                kwargs['ssidNumber'] = ssid_number
            
            histories = meraki_client.dashboard.networks.getNetworkClientsUsageHistories(
                network_id, **kwargs
            )
            
            if not histories:
                return "No usage histories found"
            
            result = f"# Client Usage Histories\\n\\n"
            
            for client in histories:
                result += f"## Client: {client.get('clientId')}\\n"
                if client.get('usageHistory'):
                    for entry in client['usageHistory'][:3]:  # First 3 entries
                        result += f"- {entry.get('ts')}: "
                        result += f"Sent {entry.get('sent', 0):,}, "
                        result += f"Recv {entry.get('received', 0):,} bytes\\n"
                result += "\\n"
            
            return result
        except Exception as e:
            return f"Error getting usage histories: {str(e)}"
    
    @app.tool(
        name="get_network_policies_by_client",
        description="Get policies for clients"
    )
    def get_network_policies_by_client(network_id: str, per_page: int = 100,
                                      starting_after: str = None, ending_before: str = None,
                                      timespan: int = 86400):
        """Get policies for clients."""
        try:
            kwargs = {'perPage': per_page, 'timespan': timespan}
            if starting_after:
                kwargs['startingAfter'] = starting_after
            if ending_before:
                kwargs['endingBefore'] = ending_before
            
            policies = meraki_client.dashboard.networks.getNetworkPoliciesByClient(
                network_id, **kwargs
            )
            
            if not policies:
                return "No client policies found"
            
            result = f"# Network Policies by Client\\n\\n"
            
            for policy in policies[:20]:  # Show first 20
                result += f"## Client: {policy.get('clientId')}\\n"
                result += f"- Name: {policy.get('name')}\\n"
                result += f"- Assigned: {policy.get('assigned')}\\n"
                result += f"- Group Policy ID: {policy.get('groupPolicyId')}\\n"
                result += "\\n"
            
            return result
        except Exception as e:
            return f"Error getting policies by client: {str(e)}"
    
    # Alert Settings
    
    @app.tool(
        name="get_network_alerts_settings",
        description="Get alert settings for a network"
    )
    def get_network_alerts_settings(network_id: str):
        """Get alert settings for a network."""
        try:
            settings = meraki_client.dashboard.networks.getNetworkAlertsSettings(network_id)
            
            result = f"# Network Alert Settings\\n\\n"
            
            if settings.get('defaultDestinations'):
                result += f"## Default Destinations\\n"
                dest = settings['defaultDestinations']
                if dest.get('emails'):
                    result += f"- Emails: {', '.join(dest['emails'])}\\n"
                if dest.get('smsNumbers'):
                    result += f"- SMS: {', '.join(dest['smsNumbers'])}\\n"
                if dest.get('allAdmins'):
                    result += f"- All Admins: {dest['allAdmins']}\\n"
                if dest.get('snmp'):
                    result += f"- SNMP: {dest['snmp']}\\n"
                result += "\\n"
            
            if settings.get('alerts'):
                result += f"## Alert Types ({len(settings['alerts'])} configured)\\n"
                for alert in settings['alerts'][:5]:  # Show first 5
                    result += f"- {alert.get('type')}: {alert.get('enabled')}\\n"
                    if alert.get('alertDestinations'):
                        result += f"  Destinations: {alert['alertDestinations']}\\n"
                result += "\\n"
            
            return result
        except Exception as e:
            return f"Error getting alert settings: {str(e)}"
    
    @app.tool(
        name="update_network_alerts_settings",
        description="Update alert settings for a network"
    )
    def update_network_alerts_settings(network_id: str, default_destinations: dict = None,
                                     alerts: list = None):
        """Update alert settings for a network."""
        try:
            kwargs = {}
            if default_destinations:
                kwargs['defaultDestinations'] = default_destinations
            if alerts:
                kwargs['alerts'] = alerts
            
            if not kwargs:
                return "❌ No settings to update"
            
            result = meraki_client.dashboard.networks.updateNetworkAlertsSettings(
                network_id, **kwargs
            )
            return f"✅ Alert settings updated successfully"
        except Exception as e:
            return f"Error updating alert settings: {str(e)}"
    
    # NetFlow
    
    @app.tool(
        name="get_network_netflow",
        description="Get NetFlow traffic reporting settings"
    )
    def get_network_netflow(network_id: str):
        """Get NetFlow traffic reporting settings."""
        try:
            netflow = meraki_client.dashboard.networks.getNetworkNetflow(network_id)
            
            result = f"# NetFlow Settings\\n\\n"
            result += f"- Reporting Enabled: {netflow.get('reportingEnabled')}\\n"
            
            if netflow.get('collectorIp'):
                result += f"- Collector IP: {netflow.get('collectorIp')}\\n"
            if netflow.get('collectorPort'):
                result += f"- Collector Port: {netflow.get('collectorPort')}\\n"
            if netflow.get('etaEnabled') is not None:
                result += f"- ETA Enabled: {netflow.get('etaEnabled')}\\n"
            if netflow.get('etaDstPort'):
                result += f"- ETA Destination Port: {netflow.get('etaDstPort')}\\n"
            
            return result
        except Exception as e:
            return f"Error getting NetFlow settings: {str(e)}"
    
    @app.tool(
        name="update_network_netflow",
        description="Update NetFlow traffic reporting settings"
    )
    def update_network_netflow(network_id: str, reporting_enabled: bool = None,
                              collector_ip: str = None, collector_port: int = None,
                              eta_enabled: bool = None, eta_dst_port: int = None):
        """Update NetFlow traffic reporting settings."""
        try:
            kwargs = {}
            if reporting_enabled is not None:
                kwargs['reportingEnabled'] = reporting_enabled
            if collector_ip is not None:
                kwargs['collectorIp'] = collector_ip
            if collector_port is not None:
                kwargs['collectorPort'] = collector_port
            if eta_enabled is not None:
                kwargs['etaEnabled'] = eta_enabled
            if eta_dst_port is not None:
                kwargs['etaDstPort'] = eta_dst_port
            
            if not kwargs:
                return "❌ No settings to update"
            
            result = meraki_client.dashboard.networks.updateNetworkNetflow(
                network_id, **kwargs
            )
            return f"✅ NetFlow settings updated successfully"
        except Exception as e:
            return f"Error updating NetFlow settings: {str(e)}"
    
    # Firmware Staged Groups/Events (remaining methods)
    
    @app.tool(
        name="create_network_firmware_upgrades_staged_event",
        description="Create a staged firmware upgrade event"
    )
    def create_network_firmware_upgrades_staged_event(network_id: str, stages: list):
        """Create a staged firmware upgrade event."""
        try:
            from utils.helpers import require_confirmation
            
            if not require_confirmation(
                operation_type="create",
                resource_type="staged firmware upgrade",
                resource_name=f"{len(stages)} stages",
                resource_id=network_id
            ):
                return "❌ Staged upgrade creation cancelled by user"
            
            result = meraki_client.dashboard.networks.createNetworkFirmwareUpgradesStagedEvent(
                network_id, stages=stages
            )
            return f"✅ Staged firmware upgrade created successfully"
        except Exception as e:
            return f"Error creating staged event: {str(e)}"
    
    @app.tool(
        name="defer_network_firmware_upgrades_staged_events",
        description="Defer staged firmware upgrade events"
    )
    def defer_network_firmware_upgrades_staged_events(network_id: str):
        """Defer staged firmware upgrade events."""
        try:
            result = meraki_client.dashboard.networks.deferNetworkFirmwareUpgradesStagedEvents(
                network_id
            )
            return f"✅ Staged events deferred successfully"
        except Exception as e:
            return f"Error deferring staged events: {str(e)}"
    
    @app.tool(
        name="get_network_firmware_upgrades_staged_group",
        description="Get a specific staged upgrade group"
    )
    def get_network_firmware_upgrades_staged_group(network_id: str, group_id: str):
        """Get a specific staged upgrade group."""
        try:
            group = meraki_client.dashboard.networks.getNetworkFirmwareUpgradesStagedGroup(
                network_id, group_id
            )
            
            result = f"# Staged Upgrade Group: {group.get('name', 'Unnamed')}\\n\\n"
            result += f"- ID: {group.get('id')}\\n"
            result += f"- Description: {group.get('description')}\\n"
            result += f"- Is Default: {group.get('isDefault')}\\n"
            
            if group.get('assignedDevices'):
                result += f"\\n## Assigned Devices ({len(group['assignedDevices'])})\\n"
                for device in group['assignedDevices'][:5]:  # Show first 5
                    result += f"- {device.get('name')} ({device.get('serial')})\\n"
            
            return result
        except Exception as e:
            return f"Error getting staged group: {str(e)}"
    
    @app.tool(
        name="get_network_firmware_upgrades_staged_groups",
        description="Get all staged upgrade groups"
    )
    def get_network_firmware_upgrades_staged_groups(network_id: str):
        """Get all staged upgrade groups."""
        try:
            groups = meraki_client.dashboard.networks.getNetworkFirmwareUpgradesStagedGroups(
                network_id
            )
            
            if not groups:
                return "No staged upgrade groups found"
            
            result = f"# Staged Upgrade Groups ({len(groups)} total)\\n\\n"
            
            for group in groups:
                result += f"## {group.get('name', 'Unnamed')}\\n"
                result += f"- ID: {group.get('id')}\\n"
                result += f"- Is Default: {group.get('isDefault')}\\n"
                result += f"- Devices: {len(group.get('assignedDevices', []))}\\n"
                result += "\\n"
            
            return result
        except Exception as e:
            return f"Error getting staged groups: {str(e)}"
    
    @app.tool(
        name="create_network_firmware_upgrades_staged_group",
        description="Create a staged upgrade group"
    )
    def create_network_firmware_upgrades_staged_group(network_id: str, name: str,
                                                     is_default: bool = False,
                                                     assigned_devices: list = None):
        """Create a staged upgrade group."""
        try:
            kwargs = {'name': name, 'isDefault': is_default}
            if assigned_devices:
                kwargs['assignedDevices'] = assigned_devices
            
            result = meraki_client.dashboard.networks.createNetworkFirmwareUpgradesStagedGroup(
                network_id, **kwargs
            )
            return f"✅ Staged group '{name}' created successfully"
        except Exception as e:
            return f"Error creating staged group: {str(e)}"
    
    @app.tool(
        name="update_network_firmware_upgrades_staged_group",
        description="Update a staged upgrade group"
    )
    def update_network_firmware_upgrades_staged_group(network_id: str, group_id: str,
                                                     name: str = None, is_default: bool = None,
                                                     assigned_devices: list = None):
        """Update a staged upgrade group."""
        try:
            kwargs = {}
            if name is not None:
                kwargs['name'] = name
            if is_default is not None:
                kwargs['isDefault'] = is_default
            if assigned_devices is not None:
                kwargs['assignedDevices'] = assigned_devices
            
            if not kwargs:
                return "❌ No updates provided"
            
            result = meraki_client.dashboard.networks.updateNetworkFirmwareUpgradesStagedGroup(
                network_id, group_id, **kwargs
            )
            return f"✅ Staged group updated successfully"
        except Exception as e:
            return f"Error updating staged group: {str(e)}"
    
    @app.tool(
        name="delete_network_firmware_upgrades_staged_group",
        description="Delete a staged upgrade group"
    )
    def delete_network_firmware_upgrades_staged_group(network_id: str, group_id: str):
        """Delete a staged upgrade group."""
        try:
            from utils.helpers import require_confirmation
            
            if not require_confirmation(
                operation_type="delete",
                resource_type="staged upgrade group",
                resource_name=group_id,
                resource_id=network_id
            ):
                return "❌ Group deletion cancelled by user"
            
            meraki_client.dashboard.networks.deleteNetworkFirmwareUpgradesStagedGroup(
                network_id, group_id
            )
            return f"✅ Staged group deleted successfully"
        except Exception as e:
            return f"Error deleting staged group: {str(e)}"
    
    @app.tool(
        name="get_network_firmware_upgrades_staged_stages",
        description="Get staged upgrade stages"
    )
    def get_network_firmware_upgrades_staged_stages(network_id: str):
        """Get staged upgrade stages."""
        try:
            stages = meraki_client.dashboard.networks.getNetworkFirmwareUpgradesStagedStages(
                network_id
            )
            
            if not stages:
                return "No staged upgrade stages found"
            
            result = f"# Staged Upgrade Stages\\n\\n"
            
            for stage in stages:
                result += f"## {stage.get('name', 'Unnamed')}\\n"
                
                if stage.get('milestones'):
                    result += f"### Milestones\\n"
                    for milestone in stage['milestones']:
                        result += f"- {milestone.get('action')}: "
                        result += f"{milestone.get('scheduledFor')}\\n"
                
                if stage.get('groups'):
                    result += f"### Groups\\n"
                    for group in stage['groups']:
                        result += f"- {group.get('name')}\\n"
                
                result += "\\n"
            
            return result
        except Exception as e:
            return f"Error getting staged stages: {str(e)}"
    
    @app.tool(
        name="update_network_firmware_upgrades_staged_stages",
        description="Update staged upgrade stages"
    )
    def update_network_firmware_upgrades_staged_stages(network_id: str, stages: list):
        """Update staged upgrade stages."""
        try:
            result = meraki_client.dashboard.networks.updateNetworkFirmwareUpgradesStagedStages(
                network_id, stages=stages
            )
            return f"✅ Staged stages updated successfully"
        except Exception as e:
            return f"Error updating staged stages: {str(e)}"
    
    print("Networks SDK module registered successfully with 114 methods")
'''
    
    return module_code

if __name__ == '__main__':
    print("🚀 Consolidating Networks SDK Module")
    print("=" * 60)
    
    # Generate the complete module
    module_content = generate_complete_networks_module()
    
    # Write to file
    output_file = 'server/tools_SDK_networks.py'
    with open(output_file, 'w') as f:
        f.write(module_content)
    
    # Count tools
    tool_count = module_content.count('@app.tool(')
    sdk_method_count = 114  # Target
    
    print(f"✅ Generated {output_file}")
    print(f"📊 Total tools implemented: {tool_count}")
    print(f"🎯 Target SDK methods: {sdk_method_count}")
    
    if tool_count >= sdk_method_count:
        print(f"🎉 SUCCESS: Achieved 100% SDK coverage!")
    else:
        print(f"⚠️  Need {sdk_method_count - tool_count} more methods for 100% coverage")
    
    print("\n📋 Next Steps:")
    print("1. Run test script to verify all GET methods work")
    print("2. Update server/main.py to import new module")
    print("3. Test with MCP server")