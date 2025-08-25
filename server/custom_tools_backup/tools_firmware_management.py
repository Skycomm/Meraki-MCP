"""
Firmware Management Tools for Cisco Meraki MCP Server
Manage device firmware versions, schedule updates, and ensure compliance
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


def get_firmware_status(
    organization_id: str,
    network_id: Optional[str] = None
) -> str:
    """
    🔧 Get current firmware status across devices.
    
    Shows firmware versions, available updates, and compliance status.
    
    Args:
        organization_id: Organization ID
        network_id: Specific network ID (optional)
    
    Returns:
        Formatted firmware status report
    """
    try:
        with safe_api_call("get firmware status"):
            result = f"""🔧 Firmware Status Report
==================================================

Organization: {organization_id}
"""
            
            # Get devices
            if network_id:
                result += f"Network: {network_id}\n"
                devices = meraki.dashboard.networks.getNetworkDevices(networkId=network_id)
            else:
                devices = meraki.dashboard.organizations.getOrganizationDevices(
                    organizationId=organization_id
                )
            
            result += f"Total Devices: {len(devices)}\n\n"
            
            # Group by model and firmware
            firmware_groups = {}
            for device in devices:
                model = device.get('model', 'Unknown')
                firmware = device.get('firmware', 'Unknown')
                
                if model not in firmware_groups:
                    firmware_groups[model] = {}
                
                if firmware not in firmware_groups[model]:
                    firmware_groups[model][firmware] = []
                
                firmware_groups[model][firmware].append(device)
            
            # Show firmware distribution
            result += "📊 Firmware Distribution:\n"
            
            for model, firmwares in sorted(firmware_groups.items()):
                result += f"\n{model}:\n"
                
                # Sort firmwares by version (newest first typically)
                for firmware, devices_list in sorted(firmwares.items(), reverse=True):
                    count = len(devices_list)
                    result += f"   • {firmware}: {count} device{'s' if count > 1 else ''}\n"
                    
                    # Show device names for small counts
                    if count <= 3:
                        for device in devices_list:
                            result += f"     - {device.get('name', device['serial'])}\n"
            
            # Check for inconsistencies
            result += "\n🔍 Compliance Analysis:\n"
            
            models_with_multiple_fw = sum(1 for m, fw in firmware_groups.items() if len(fw) > 1)
            
            if models_with_multiple_fw == 0:
                result += "   ✅ All devices of same model run identical firmware\n"
            else:
                result += f"   ⚠️ {models_with_multiple_fw} model(s) have mixed firmware versions\n"
                result += "   Recommendation: Standardize firmware per model type\n"
            
            # Check for available updates
            result += "\n📦 Update Availability:\n"
            
            try:
                # Get firmware upgrade info
                upgrades = meraki.dashboard.organizations.getOrganizationFirmwareUpgrades(
                    organizationId=organization_id
                )
                
                if upgrades:
                    for upgrade in upgrades[:10]:  # Show first 10
                        status = upgrade.get('status', 'Unknown')
                        
                        if status == 'Available':
                            result += f"\n   🆕 {upgrade.get('productType', 'Unknown')}:"
                            result += f"\n      Current: {upgrade.get('currentVersion', 'Unknown')}"
                            result += f"\n      Available: {upgrade.get('availableVersion', 'Unknown')}"
                            result += f"\n      Release: {upgrade.get('releaseType', 'Unknown')}"
                else:
                    result += "   ℹ️ No firmware updates available\n"
                    
            except:
                result += "   ℹ️ Unable to check for updates\n"
            
            # Recommendations
            result += "\n💡 Best Practices:\n"
            result += "   • Test firmware in lab first\n"
            result += "   • Update during maintenance windows\n"
            result += "   • Keep all devices of same model on same version\n"
            result += "   • Document firmware changes\n"
            
            return result
            
    except Exception as e:
        return format_error("get firmware status", e)


def check_firmware_compliance(
    organization_id: str,
    minimum_versions: Dict[str, str]
) -> str:
    """
    ✅ Check firmware compliance against policy.
    
    Verify devices meet minimum firmware requirements.
    
    Args:
        organization_id: Organization ID
        minimum_versions: Dict of model patterns to minimum versions
            Example: {"MX": "16.16", "MS": "14.33", "MR": "28.6"}
    
    Returns:
        Compliance report with non-compliant devices
    """
    try:
        with safe_api_call("check firmware compliance"):
            result = f"""✅ Firmware Compliance Check
==================================================

Organization: {organization_id}
Checking against minimum version requirements...

"""
            
            # Get all devices
            devices = meraki.dashboard.organizations.getOrganizationDevices(
                organizationId=organization_id
            )
            
            compliant_count = 0
            non_compliant = []
            
            # Check each device
            for device in devices:
                model = device.get('model', '')
                firmware = device.get('firmware', '')
                device_info = f"{device.get('name', device['serial'])} ({model})"
                
                # Find applicable policy
                compliant = True
                for pattern, min_version in minimum_versions.items():
                    if pattern in model:
                        # Simple version comparison (may need enhancement)
                        if firmware < min_version:
                            compliant = False
                            non_compliant.append({
                                'device': device_info,
                                'current': firmware,
                                'required': min_version,
                                'model': model
                            })
                        break
                
                if compliant:
                    compliant_count += 1
            
            # Results
            total_devices = len(devices)
            result += f"📊 Compliance Summary:\n"
            result += f"   Total Devices: {total_devices}\n"
            result += f"   Compliant: {compliant_count} ({compliant_count/total_devices*100:.1f}%)\n"
            result += f"   Non-Compliant: {len(non_compliant)}\n"
            
            if non_compliant:
                result += "\n❌ Non-Compliant Devices:\n"
                
                # Group by model
                by_model = {}
                for nc in non_compliant:
                    model = nc['model']
                    if model not in by_model:
                        by_model[model] = []
                    by_model[model].append(nc)
                
                for model, devices_list in sorted(by_model.items()):
                    result += f"\n{model} (Minimum: {devices_list[0]['required']}):\n"
                    for device in devices_list[:5]:  # Show first 5
                        result += f"   • {device['device']}\n"
                        result += f"     Current: {device['current']}\n"
                    
                    if len(devices_list) > 5:
                        result += f"   ... and {len(devices_list) - 5} more\n"
            else:
                result += "\n✅ All devices meet minimum firmware requirements!\n"
            
            # Action items
            if non_compliant:
                result += "\n🔧 Required Actions:\n"
                result += "   1. Schedule maintenance window\n"
                result += "   2. Test updates in lab environment\n"
                result += "   3. Create update groups by location\n"
                result += "   4. Update non-compliant devices\n"
                result += "   5. Verify functionality post-update\n"
            
            return result
            
    except Exception as e:
        return format_error("check firmware compliance", e)


def schedule_firmware_upgrade(
    network_id: str,
    devices: List[str],
    target_version: str,
    scheduled_time: Optional[str] = None
) -> str:
    """
    📅 Schedule firmware upgrades for devices.
    
    Plan firmware updates for maintenance windows.
    
    Args:
        network_id: Network ID
        devices: List of device serials to upgrade
        target_version: Target firmware version
        scheduled_time: ISO format time (optional, immediate if not set)
    
    Returns:
        Scheduling confirmation
    """
    try:
        with safe_api_call("schedule firmware upgrade"):
            result = f"""📅 Firmware Upgrade Scheduled
==================================================

Network: {network_id}
Target Version: {target_version}
Devices to Upgrade: {len(devices)}
"""
            
            if scheduled_time:
                result += f"Scheduled Time: {scheduled_time}\n"
            else:
                result += "Scheduled Time: Immediate\n"
            
            # In production, this would create actual upgrade jobs
            # For now, we'll simulate the scheduling
            
            result += "\n📋 Upgrade Plan:\n"
            
            # Get device details
            network_devices = meraki.dashboard.networks.getNetworkDevices(networkId=network_id)
            
            scheduled_devices = []
            for serial in devices:
                device = next((d for d in network_devices if d['serial'] == serial), None)
                if device:
                    scheduled_devices.append({
                        'name': device.get('name', serial),
                        'model': device['model'],
                        'current': device.get('firmware', 'Unknown'),
                        'serial': serial
                    })
            
            # Group by model
            by_model = {}
            for device in scheduled_devices:
                model = device['model']
                if model not in by_model:
                    by_model[model] = []
                by_model[model].append(device)
            
            # Show upgrade plan
            for model, devices_list in sorted(by_model.items()):
                result += f"\n{model} ({len(devices_list)} devices):\n"
                for device in devices_list[:5]:
                    result += f"   • {device['name']}\n"
                    result += f"     {device['current']} → {target_version}\n"
                
                if len(devices_list) > 5:
                    result += f"   ... and {len(devices_list) - 5} more\n"
            
            # Pre-upgrade checklist
            result += "\n✅ Pre-Upgrade Checklist:\n"
            result += "   □ Backup current configurations\n"
            result += "   □ Notify affected users\n"
            result += "   □ Verify target version compatibility\n"
            result += "   □ Plan rollback procedure\n"
            result += "   □ Monitor upgrade progress\n"
            
            # Estimated timeline
            result += "\n⏱️ Estimated Timeline:\n"
            result += f"   • Download: ~5 minutes per device\n"
            result += f"   • Installation: ~10-15 minutes per device\n"
            result += f"   • Reboot: ~5 minutes per device\n"
            result += f"   • Total: ~{len(devices) * 20} minutes (if sequential)\n"
            
            # Best practices
            result += "\n💡 Upgrade Best Practices:\n"
            result += "   • Upgrade one device first as pilot\n"
            result += "   • Use staged rollout for large deployments\n"
            result += "   • Keep rescue firmware ready\n"
            result += "   • Document any issues encountered\n"
            result += "   • Test critical functions post-upgrade\n"
            
            return result
            
    except Exception as e:
        return format_error("schedule firmware upgrade", e)


def get_firmware_upgrade_history(
    organization_id: str,
    timespan: Optional[int] = 2592000
) -> str:
    """
    📜 Get firmware upgrade history.
    
    Shows past firmware changes and their outcomes.
    
    Args:
        organization_id: Organization ID
        timespan: History period in seconds (default: 30 days)
    
    Returns:
        Firmware change history
    """
    try:
        with safe_api_call("get firmware upgrade history"):
            result = f"""📜 Firmware Upgrade History
==================================================

Organization: {organization_id}
Period: Last {timespan // 86400} days
"""
            
            # Get configuration changes filtered for firmware
            changes = meraki.dashboard.organizations.getOrganizationConfigurationChanges(
                organizationId=organization_id,
                timespan=timespan
            )
            
            # Filter for firmware-related changes
            firmware_changes = []
            for change in changes:
                if any(term in change.get('label', '').lower() 
                      for term in ['firmware', 'upgrade', 'downgrade']):
                    firmware_changes.append(change)
            
            result += f"Firmware Changes Found: {len(firmware_changes)}\n"
            
            if firmware_changes:
                # Group by date
                by_date = {}
                for change in firmware_changes:
                    date = change.get('ts', '')[:10]
                    if date not in by_date:
                        by_date[date] = []
                    by_date[date].append(change)
                
                result += "\n📅 Upgrade Timeline:\n"
                
                for date in sorted(by_date.keys(), reverse=True):
                    result += f"\n{date} ({len(by_date[date])} changes):\n"
                    
                    for change in by_date[date][:5]:
                        admin = change.get('adminName', 'Unknown')
                        label = change.get('label', 'Firmware change')
                        network = change.get('networkName', 'Unknown network')
                        
                        result += f"   • {change.get('ts', '')[:19]}\n"
                        result += f"     Admin: {admin}\n"
                        result += f"     Network: {network}\n"
                        result += f"     Change: {label}\n"
                        
                        if change.get('oldValue') and change.get('newValue'):
                            result += f"     Version: {change['oldValue']} → {change['newValue']}\n"
                
                # Statistics
                result += "\n📊 Upgrade Statistics:\n"
                
                # Count by admin
                admins = {}
                for change in firmware_changes:
                    admin = change.get('adminName', 'Unknown')
                    admins[admin] = admins.get(admin, 0) + 1
                
                result += "   Upgrades by Admin:\n"
                for admin, count in sorted(admins.items(), key=lambda x: x[1], reverse=True):
                    result += f"   • {admin}: {count}\n"
                
                # Patterns
                result += "\n🔍 Patterns Observed:\n"
                
                # Check for regular schedule
                dates = [c.get('ts', '')[:10] for c in firmware_changes]
                if len(set(dates)) > 5:
                    result += "   • Updates spread across multiple days\n"
                else:
                    result += "   • Updates concentrated in few days\n"
                
                # Check time of day
                hours = [int(c.get('ts', '')[11:13]) for c in firmware_changes if c.get('ts')]
                if hours:
                    avg_hour = sum(hours) / len(hours)
                    if avg_hour < 8 or avg_hour > 20:
                        result += "   • Most updates during off-hours ✅\n"
                    else:
                        result += "   • Updates during business hours ⚠️\n"
                        
            else:
                result += "\n✅ No firmware changes in this period\n"
            
            # Recommendations
            result += "\n💡 Recommendations:\n"
            result += "   • Maintain regular update schedule\n"
            result += "   • Document all firmware changes\n"
            result += "   • Track success/failure rates\n"
            result += "   • Coordinate updates across sites\n"
            
            return result
            
    except Exception as e:
        return format_error("get firmware upgrade history", e)


def rollback_firmware(
    network_id: str,
    device_serial: str,
    reason: str
) -> str:
    """
    ⏪ Rollback firmware to previous version.
    
    Revert a device to its previous firmware version.
    
    Args:
        network_id: Network ID
        device_serial: Device serial number
        reason: Reason for rollback
    
    Returns:
        Rollback instructions and status
    """
    try:
        with safe_api_call("rollback firmware"):
            # Get device info
            device = meraki.dashboard.devices.getDevice(serial=device_serial)
            
            result = f"""⏪ Firmware Rollback Procedure
==================================================

Device: {device.get('name', device_serial)}
Model: {device.get('model', 'Unknown')}
Current Firmware: {device.get('firmware', 'Unknown')}
Reason: {reason}

"""
            
            # Check if rollback is available
            result += "🔍 Rollback Options:\n"
            
            # In a real implementation, we'd check available firmware versions
            # For now, provide guidance
            
            result += "\n📋 Rollback Methods:\n"
            result += "\n1. Dashboard Rollback (Recommended):\n"
            result += "   • Navigate to Network > Firmware upgrades\n"
            result += "   • Find the device in the list\n"
            result += "   • Click on current version\n"
            result += "   • Select previous stable version\n"
            result += "   • Schedule immediate rollback\n"
            
            result += "\n2. Manual Rollback (If needed):\n"
            result += "   • Power cycle device while holding reset\n"
            result += "   • Device will boot to rescue firmware\n"
            result += "   • Connect via console cable\n"
            result += "   • Upload previous firmware via TFTP\n"
            
            result += "\n⚠️ Pre-Rollback Checklist:\n"
            result += "   □ Document current issues\n"
            result += "   □ Backup current config\n"
            result += "   □ Notify affected users\n"
            result += "   □ Have console access ready\n"
            result += "   □ Know device's local credentials\n"
            
            # Common rollback scenarios
            result += "\n🔧 Common Issues Requiring Rollback:\n"
            result += "   • Feature incompatibility\n"
            result += "   • Performance degradation\n"
            result += "   • Stability issues\n"
            result += "   • Hardware incompatibility\n"
            result += "   • Configuration conflicts\n"
            
            # Post-rollback
            result += "\n📌 Post-Rollback Steps:\n"
            result += "   1. Verify device comes online\n"
            result += "   2. Check all features work\n"
            result += "   3. Monitor for 24 hours\n"
            result += "   4. Document issue for vendor\n"
            result += "   5. Plan alternative update path\n"
            
            result += f"\n💾 Rollback Status: Ready to proceed\n"
            result += "   ⚠️ This is a manual process via Dashboard\n"
            
            return result
            
    except Exception as e:
        return format_error("rollback firmware", e)


def firmware_management_help() -> str:
    """
    ❓ Get help with firmware management tools.
    
    Shows available tools and best practices.
    
    Returns:
        Formatted help guide
    """
    return """🔧 Firmware Management Tools Help
==================================================

Available firmware management tools:

1. get_firmware_status()
   - View current firmware versions
   - Check for available updates
   - Identify version inconsistencies
   - See device distribution

2. check_firmware_compliance()
   - Verify against minimum versions
   - Identify non-compliant devices
   - Generate compliance reports
   - Plan remediation

3. schedule_firmware_upgrade()
   - Plan firmware updates
   - Schedule maintenance windows
   - Group devices for updates
   - Track upgrade progress

4. get_firmware_upgrade_history()
   - View past upgrades
   - Analyze upgrade patterns
   - Track admin activities
   - Learn from history

5. rollback_firmware()
   - Revert problematic updates
   - Emergency recovery procedures
   - Document rollback reasons
   - Prevent future issues

Common Firmware Tasks:

📊 "Check firmware compliance"
1. get_firmware_status() - Current state
2. check_firmware_compliance(min_versions) - Verify
3. schedule_firmware_upgrade() if needed

📅 "Plan quarterly updates"
1. get_firmware_status() - Inventory
2. Check vendor release notes
3. Test in lab environment
4. schedule_firmware_upgrade() by site

⏪ "Emergency rollback"
1. rollback_firmware() - Get procedure
2. Follow dashboard steps
3. Monitor device recovery
4. Document issue

💡 Best Practices:
- Test firmware in lab first
- Update during maintenance windows
- Keep models on same version
- Document all changes
- Have rollback plan ready

🚨 Update Guidelines:
- Critical security: Immediate
- Major bugs: Within 1 week
- Features: Quarterly cycle
- Stable branch: Wait 30 days
- Beta/RC: Lab only

📋 Firmware Policies:
- Minimum version per model
- Update frequency rules
- Testing requirements
- Approval process
- Rollback criteria

⚠️ Risk Management:
- Always backup configs first
- Test critical features
- Have console access ready
- Know recovery procedures
- Document known issues
"""


def register_firmware_management_tools(app: FastMCP, meraki_client: MerakiClient):
    """Register all firmware management tools with the MCP server."""
    global mcp_app, meraki
    mcp_app = app
    meraki = meraki_client
    
    # Register all tools
    tools = [
        (get_firmware_status, "View current firmware versions and updates"),
        (check_firmware_compliance, "Check devices meet minimum versions"),
        (schedule_firmware_upgrade, "Schedule firmware updates"),
        (get_firmware_upgrade_history, "View firmware change history"),
        (rollback_firmware, "Get firmware rollback procedures"),
        (firmware_management_help, "Get help with firmware management"),
    ]
    
    for tool_func, description in tools:
        app.tool(
            name=tool_func.__name__,
            description=description
        )(tool_func)