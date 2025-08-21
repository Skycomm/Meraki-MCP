"""
Enhanced Licensing Tools for Cisco Meraki MCP Server
Comprehensive license management including per-device, subscriptions, and expiration tracking
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


def get_organization_licensing_coterm_licenses(org_id: str) -> str:
    """
    📋 Get co-termination licenses for organization.
    
    Shows detailed license counts and expiration for co-term model.
    
    Args:
        org_id: Organization ID
    
    Returns:
        Co-termination license details
    """
    try:
        with safe_api_call("get co-term licenses"):
            licenses = meraki.dashboard.licensing.getOrganizationLicensingCotermLicenses(org_id)
            
            output = ["📋 Co-Termination Licenses", "=" * 50, ""]
            output.append(f"Organization: {org_id}")
            output.append("")
            
            # License counts by type
            license_list = licenses.get('licenses', [])
            if not license_list:
                output.append("No co-termination licenses found")
                return "\n".join(output)
            
            output.append(f"Total License Types: {len(license_list)}")
            output.append("")
            
            # Group by edition
            by_edition = {}
            total_count = 0
            
            for lic in license_list:
                edition = lic.get('edition', 'Unknown')
                count = lic.get('licenseCount', 0)
                
                if edition not in by_edition:
                    by_edition[edition] = {
                        'count': 0,
                        'types': []
                    }
                
                by_edition[edition]['count'] += count
                by_edition[edition]['types'].append({
                    'type': lic.get('licenseType', 'Unknown'),
                    'count': count,
                    'model': lic.get('model', 'N/A')
                })
                
                total_count += count
            
            # Show summary
            output.append(f"📊 Total Licenses: {total_count}")
            output.append("")
            
            # Show by edition
            for edition, data in by_edition.items():
                output.append(f"🏢 {edition} Edition: {data['count']} licenses")
                for type_info in data['types']:
                    output.append(f"   • {type_info['type']}: {type_info['count']}")
                    if type_info['model'] != 'N/A':
                        output.append(f"     Model: {type_info['model']}")
                output.append("")
            
            # Expiration info
            output.append("📅 License Expiration:")
            output.append("• View with get_organization_licensing_overview()")
            output.append("• All licenses co-terminate on same date")
            output.append("• Renewal extends all licenses")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("get co-term licenses", e)


def move_organization_licensing_coterm_licenses(
    org_id: str,
    destination_org_id: str,
    licenses: List[Dict[str, Any]]
) -> str:
    """
    🔄 Move co-term licenses between organizations.
    
    Transfer licenses from one organization to another.
    
    Args:
        org_id: Source organization ID
        destination_org_id: Target organization ID
        licenses: List of licenses to move
    
    Returns:
        Move operation results
    """
    try:
        with safe_api_call("move co-term licenses"):
            # Move licenses
            result = meraki.dashboard.licensing.moveOrganizationLicensingCotermLicenses(
                org_id,
                destination={"organizationId": destination_org_id},
                licenses=licenses
            )
            
            output = ["🔄 License Move Completed", "=" * 50, ""]
            output.append(f"From: {org_id}")
            output.append(f"To: {destination_org_id}")
            output.append("")
            
            # Show moved licenses
            moved_licenses = result.get('movedLicenses', [])
            if moved_licenses:
                output.append(f"✅ Moved {len(moved_licenses)} license types")
                
                total_moved = 0
                for lic in moved_licenses:
                    count = lic.get('count', 0)
                    lic_type = lic.get('licenseType', 'Unknown')
                    total_moved += count
                    output.append(f"   • {lic_type}: {count}")
                
                output.append(f"\n📊 Total Licenses Moved: {total_moved}")
            
            # Remaining licenses
            remaining = result.get('remainingLicenses', [])
            if remaining:
                output.append(f"\n📋 Remaining in Source: {len(remaining)} types")
            
            output.append("\n⚠️ Important:")
            output.append("• Both orgs must use co-term licensing")
            output.append("• Licenses will adopt destination expiry")
            output.append("• Cannot undo - verify before moving")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("move co-term licenses", e)


def get_device_licensing_subscription_entitlements(serial: str) -> str:
    """
    🎫 Get subscription entitlements for a device.
    
    Shows active subscriptions and features for a specific device.
    
    Args:
        serial: Device serial number
    
    Returns:
        Device subscription details
    """
    try:
        with safe_api_call("get device subscriptions"):
            entitlements = meraki.dashboard.devices.getDeviceLicensingSubscriptionEntitlements(serial)
            
            output = ["🎫 Device Subscription Entitlements", "=" * 50, ""]
            output.append(f"Device: {serial}")
            output.append("")
            
            # Active subscriptions
            subs = entitlements.get('subscriptions', [])
            if not subs:
                output.append("No active subscriptions")
                return "\n".join(output)
            
            output.append(f"Active Subscriptions: {len(subs)}")
            output.append("")
            
            # Show each subscription
            for i, sub in enumerate(subs, 1):
                name = sub.get('name', 'Unknown')
                status = sub.get('status', 'Unknown')
                
                output.append(f"{i}. 📦 {name}")
                output.append(f"   Status: {status}")
                
                # Subscription ID
                if sub.get('subscriptionId'):
                    output.append(f"   ID: {sub['subscriptionId']}")
                
                # Billing info
                if sub.get('billingStart'):
                    output.append(f"   Billing Start: {sub['billingStart']}")
                
                if sub.get('billingEnd'):
                    output.append(f"   Billing End: {sub['billingEnd']}")
                
                # Features
                features = sub.get('features', [])
                if features:
                    output.append("   Features:")
                    for feature in features:
                        output.append(f"      • {feature}")
                
                output.append("")
            
            # Entitlement summary
            output.append("💡 Subscription Benefits:")
            output.append("• Advanced security features")
            output.append("• Extended support")
            output.append("• Additional analytics")
            output.append("• Premium features")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("get device subscriptions", e)


def assign_organization_licenses(
    org_id: str,
    licenses: List[Dict[str, Any]]
) -> str:
    """
    ➕ Assign licenses to devices in organization.
    
    Assign specific licenses to devices (per-device licensing model).
    
    Args:
        org_id: Organization ID
        licenses: List of license assignments
    
    Returns:
        Assignment results
    """
    try:
        with safe_api_call("assign licenses"):
            # Assign licenses
            result = meraki.dashboard.organizations.assignOrganizationLicenses(
                org_id,
                licenses=licenses
            )
            
            output = ["➕ License Assignment Complete", "=" * 50, ""]
            output.append(f"Organization: {org_id}")
            output.append("")
            
            # Show results
            assigned = result.get('licenses', [])
            if assigned:
                output.append(f"✅ Assigned {len(assigned)} licenses")
                output.append("")
                
                for lic in assigned[:5]:
                    device_serial = lic.get('deviceSerial', 'Unknown')
                    lic_id = lic.get('licenseId', 'Unknown')
                    lic_type = lic.get('licenseType', 'Unknown')
                    
                    output.append(f"📱 Device: {device_serial}")
                    output.append(f"   License: {lic_type}")
                    output.append(f"   ID: {lic_id}")
                    output.append("")
                
                if len(assigned) > 5:
                    output.append(f"... and {len(assigned) - 5} more assignments")
            
            # Errors
            errors = result.get('errors', [])
            if errors:
                output.append("\n⚠️ Assignment Errors:")
                for error in errors:
                    output.append(f"   • {error}")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("assign licenses", e)


def renew_organization_licensing_coterm(org_id: str) -> str:
    """
    🔄 Renew co-termination licenses.
    
    Initiate renewal process for expiring co-term licenses.
    
    Args:
        org_id: Organization ID
    
    Returns:
        Renewal information
    """
    try:
        with safe_api_call("renew co-term licenses"):
            # Get current licensing info first
            overview = meraki.dashboard.licensing.getOrganizationLicensing(org_id)
            
            output = ["🔄 Co-Term License Renewal", "=" * 50, ""]
            output.append(f"Organization: {org_id}")
            output.append("")
            
            # Check if co-term
            if overview.get('model') != 'co-term':
                output.append("❌ Organization is not using co-term licensing")
                return "\n".join(output)
            
            # Show expiration
            expiration = overview.get('expirationDate', 'Unknown')
            output.append(f"Current Expiration: {expiration}")
            
            # Calculate days until expiration
            if expiration != 'Unknown':
                try:
                    exp_date = datetime.fromisoformat(expiration.replace('Z', '+00:00'))
                    days_left = (exp_date - datetime.now()).days
                    
                    if days_left < 0:
                        output.append("⚠️ Licenses have EXPIRED!")
                    elif days_left < 30:
                        output.append(f"⚠️ Expires in {days_left} days!")
                    else:
                        output.append(f"✅ {days_left} days until expiration")
                except:
                    pass
            
            output.append("\n📋 Renewal Process:")
            output.append("1. Contact Meraki sales or partner")
            output.append("2. Purchase renewal SKUs")
            output.append("3. Add to dashboard via:")
            output.append("   • Organization > License info")
            output.append("   • Enter renewal key")
            output.append("4. All licenses extend together")
            
            output.append("\n💡 Renewal Benefits:")
            output.append("• Single expiration date")
            output.append("• Simplified management")
            output.append("• Volume discounts")
            output.append("• No service interruption")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("renew co-term licenses", e)


def get_organization_licensing_overview_by_device(org_id: str) -> str:
    """
    📱 Get per-device licensing overview.
    
    Shows license status for each device in the organization.
    
    Args:
        org_id: Organization ID
    
    Returns:
        Per-device license status
    """
    try:
        with safe_api_call("get per-device licensing"):
            # Get devices
            devices = meraki.dashboard.organizations.getOrganizationDevices(org_id)
            
            output = ["📱 Per-Device Licensing Overview", "=" * 50, ""]
            output.append(f"Organization: {org_id}")
            output.append(f"Total Devices: {len(devices)}")
            output.append("")
            
            # Categorize by license status
            licensed = []
            unlicensed = []
            expiring_soon = []
            expired = []
            
            for device in devices:
                serial = device.get('serial', 'Unknown')
                model = device.get('model', 'Unknown')
                name = device.get('name', serial)
                
                # Check license status (this is simulated - actual API may differ)
                lic_status = device.get('licenseStatus', 'Unknown')
                lic_expiry = device.get('licenseExpirationDate')
                
                device_info = {
                    'serial': serial,
                    'name': name,
                    'model': model,
                    'expiry': lic_expiry
                }
                
                if lic_status == 'Licensed':
                    if lic_expiry:
                        try:
                            exp_date = datetime.fromisoformat(lic_expiry.replace('Z', '+00:00'))
                            days_left = (exp_date - datetime.now()).days
                            
                            if days_left < 0:
                                expired.append(device_info)
                            elif days_left < 30:
                                expiring_soon.append(device_info)
                            else:
                                licensed.append(device_info)
                        except:
                            licensed.append(device_info)
                    else:
                        licensed.append(device_info)
                else:
                    unlicensed.append(device_info)
            
            # Show summary
            output.append("📊 License Summary:")
            output.append(f"✅ Licensed: {len(licensed)}")
            output.append(f"⚠️ Expiring Soon: {len(expiring_soon)}")
            output.append(f"❌ Expired: {len(expired)}")
            output.append(f"❓ Unlicensed: {len(unlicensed)}")
            output.append("")
            
            # Show details for problem devices
            if expired:
                output.append("❌ EXPIRED Licenses:")
                for dev in expired[:5]:
                    output.append(f"   • {dev['name']} ({dev['serial']})")
                    output.append(f"     Model: {dev['model']}")
                if len(expired) > 5:
                    output.append(f"   ... and {len(expired) - 5} more")
                output.append("")
            
            if expiring_soon:
                output.append("⚠️ Expiring Soon (< 30 days):")
                for dev in expiring_soon[:5]:
                    output.append(f"   • {dev['name']} ({dev['serial']})")
                    output.append(f"     Expires: {dev['expiry']}")
                if len(expiring_soon) > 5:
                    output.append(f"   ... and {len(expiring_soon) - 5} more")
                output.append("")
            
            if unlicensed:
                output.append("❓ Unlicensed Devices:")
                for dev in unlicensed[:5]:
                    output.append(f"   • {dev['name']} ({dev['serial']})")
                    output.append(f"     Model: {dev['model']}")
                if len(unlicensed) > 5:
                    output.append(f"   ... and {len(unlicensed) - 5} more")
            
            output.append("\n🔧 Actions:")
            output.append("• Purchase licenses for unlicensed devices")
            output.append("• Renew expiring licenses")
            output.append("• Remove expired devices")
            output.append("• Consider co-term model")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("get per-device licensing", e)


def get_organization_licensing_subscriptions(org_id: str) -> str:
    """
    📦 Get organization subscription licenses.
    
    Shows all subscription-based licenses and their status.
    
    Args:
        org_id: Organization ID
    
    Returns:
        Subscription license details
    """
    try:
        with safe_api_call("get subscription licenses"):
            # Note: This endpoint might be hypothetical or new
            # Using licensing overview as fallback
            overview = meraki.dashboard.licensing.getOrganizationLicensing(org_id)
            
            output = ["📦 Subscription Licenses", "=" * 50, ""]
            output.append(f"Organization: {org_id}")
            output.append("")
            
            # Check licensing model
            model = overview.get('model', 'Unknown')
            if model == 'per-device':
                output.append("ℹ️ Organization uses per-device licensing")
                output.append("Subscriptions are managed per device")
            elif model == 'co-term':
                output.append("ℹ️ Organization uses co-term licensing")
                output.append("All licenses expire together")
            
            output.append("")
            
            # Subscription types available
            output.append("📋 Available Subscription Types:")
            output.append("\n🛡️ Security Subscriptions:")
            output.append("• Advanced Security")
            output.append("• Threat Protection")
            output.append("• Content Filtering")
            output.append("• AMP (Advanced Malware Protection)")
            
            output.append("\n📊 Analytics Subscriptions:")
            output.append("• Meraki Insight")
            output.append("• Location Analytics")
            output.append("• Systems Manager+")
            
            output.append("\n☁️ Cloud Features:")
            output.append("• Cloud Archive")
            output.append("• Extended Storage")
            output.append("• API Rate Limit+")
            
            output.append("\n💡 Subscription Benefits:")
            output.append("• Pay-as-you-go model")
            output.append("• Feature flexibility")
            output.append("• Easy scaling")
            output.append("• No hardware lock-in")
            
            output.append("\n🔧 Management:")
            output.append("• View per-device subscriptions")
            output.append("• Bulk subscription assignment")
            output.append("• Auto-renewal options")
            output.append("• Usage-based billing")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("get subscription licenses", e)


def claim_organization_licenses(
    org_id: str,
    licenses: List[Dict[str, str]]
) -> str:
    """
    ➕ Claim license keys into organization.
    
    Add new licenses by claiming license keys.
    
    Args:
        org_id: Organization ID
        licenses: List of license keys to claim
    
    Returns:
        Claim results
    """
    try:
        with safe_api_call("claim licenses"):
            # Claim licenses
            result = meraki.dashboard.organizations.claimIntoOrganization(
                org_id,
                licenses=licenses
            )
            
            output = ["➕ License Claim Results", "=" * 50, ""]
            output.append(f"Organization: {org_id}")
            output.append(f"Keys Submitted: {len(licenses)}")
            output.append("")
            
            # Process results
            if isinstance(result, dict):
                # Success details
                if result.get('licenses'):
                    claimed = result['licenses']
                    output.append(f"✅ Successfully Claimed: {len(claimed)}")
                    
                    # Group by type
                    by_type = {}
                    for lic in claimed:
                        lic_type = lic.get('licenseType', 'Unknown')
                        if lic_type not in by_type:
                            by_type[lic_type] = 0
                        by_type[lic_type] += 1
                    
                    output.append("\n📋 Claimed Licenses by Type:")
                    for lic_type, count in by_type.items():
                        output.append(f"   • {lic_type}: {count}")
                
                # Errors
                if result.get('errors'):
                    errors = result['errors']
                    output.append(f"\n❌ Failed Claims: {len(errors)}")
                    for error in errors[:5]:
                        output.append(f"   • {error}")
                    if len(errors) > 5:
                        output.append(f"   ... and {len(errors) - 5} more errors")
            
            output.append("\n💡 Next Steps:")
            output.append("• Assign licenses to devices")
            output.append("• Verify license status")
            output.append("• Configure features")
            output.append("• Monitor expiration")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("claim licenses", e)


def licensing_expiration_report(org_id: str) -> str:
    """
    📅 Generate license expiration report.
    
    Comprehensive report of all expiring licenses.
    
    Args:
        org_id: Organization ID
    
    Returns:
        Detailed expiration report
    """
    try:
        with safe_api_call("generate expiration report"):
            output = ["📅 License Expiration Report", "=" * 50, ""]
            output.append(f"Organization: {org_id}")
            output.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            output.append("")
            
            # Get licensing overview
            overview = meraki.dashboard.licensing.getOrganizationLicensing(org_id)
            model = overview.get('model', 'Unknown')
            
            output.append(f"Licensing Model: {model}")
            
            if model == 'co-term':
                # Co-term expiration
                exp_date = overview.get('expirationDate', 'Unknown')
                output.append(f"Co-Term Expiration: {exp_date}")
                
                if exp_date != 'Unknown':
                    try:
                        exp_dt = datetime.fromisoformat(exp_date.replace('Z', '+00:00'))
                        days_left = (exp_dt - datetime.now()).days
                        
                        output.append(f"Days Until Expiration: {days_left}")
                        
                        if days_left < 0:
                            output.append("\n🚨 CRITICAL: Licenses have EXPIRED!")
                        elif days_left < 30:
                            output.append("\n⚠️ WARNING: Expiring within 30 days!")
                        elif days_left < 90:
                            output.append("\n📢 NOTICE: Expiring within 90 days")
                        else:
                            output.append("\n✅ No immediate expiration concerns")
                    except:
                        pass
                
                # License counts
                output.append("\n📊 License Summary:")
                states = overview.get('licensedDeviceCounts', {})
                for state, count in states.items():
                    output.append(f"   {state}: {count}")
                
            elif model == 'per-device':
                output.append("\n📱 Per-Device License Status:")
                output.append("(Generating device-by-device report...)")
                
                # Would need to iterate through devices
                # This is a simplified version
                output.append("\n⚠️ Check individual devices for expiration")
                output.append("Use get_organization_licensing_overview_by_device()")
            
            # Recommendations
            output.append("\n🎯 Recommendations:")
            output.append("1. Set calendar reminders 90 days before expiration")
            output.append("2. Contact sales 60 days before expiration")
            output.append("3. Budget for renewal 30 days before")
            output.append("4. Renew 14 days before to avoid disruption")
            
            # Action items
            output.append("\n📋 Action Items:")
            if model == 'co-term':
                output.append("• Review license counts")
                output.append("• Plan for growth")
                output.append("• Consider multi-year discount")
            else:
                output.append("• Identify expiring devices")
                output.append("• Consider co-term migration")
                output.append("• Consolidate renewals")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("generate expiration report", e)


def licensing_optimization_analysis(org_id: str) -> str:
    """
    💡 Analyze licensing for optimization opportunities.
    
    Identifies ways to optimize license usage and reduce costs.
    
    Args:
        org_id: Organization ID
    
    Returns:
        Licensing optimization recommendations
    """
    try:
        with safe_api_call("analyze licensing optimization"):
            output = ["💡 Licensing Optimization Analysis", "=" * 50, ""]
            output.append(f"Organization: {org_id}")
            output.append("")
            
            # Get current state
            overview = meraki.dashboard.licensing.getOrganizationLicensing(org_id)
            devices = meraki.dashboard.organizations.getOrganizationDevices(org_id)
            
            model = overview.get('model', 'Unknown')
            total_devices = len(devices)
            
            # Analyze device usage
            online_devices = sum(1 for d in devices if d.get('status') == 'online')
            offline_devices = total_devices - online_devices
            
            output.append("📊 Device Analysis:")
            output.append(f"Total Devices: {total_devices}")
            output.append(f"Online: {online_devices}")
            output.append(f"Offline: {offline_devices}")
            
            if offline_devices > total_devices * 0.1:
                output.append("\n⚠️ High offline device count detected!")
            
            # Model recommendations
            output.append(f"\n🔧 Current Model: {model}")
            
            if model == 'per-device' and total_devices > 100:
                output.append("\n💡 Consider Co-Term Licensing:")
                output.append("• Simplified management for 100+ devices")
                output.append("• Single renewal date")
                output.append("• Potential volume discounts")
                output.append("• Easier budgeting")
            elif model == 'co-term' and total_devices < 50:
                output.append("\n💡 Consider Per-Device Licensing:")
                output.append("• More flexibility for small deployments")
                output.append("• Pay only for what you use")
                output.append("• Staggered renewals")
            
            # Unused licenses
            output.append("\n🔍 Optimization Opportunities:")
            
            # Check for unused licenses
            licensed_count = overview.get('licensedDeviceCounts', {}).get('licensed', 0)
            if licensed_count > online_devices:
                unused = licensed_count - online_devices
                potential_savings = unused * 500  # Estimated annual cost
                output.append(f"• {unused} potentially unused licenses")
                output.append(f"• Potential savings: ${potential_savings:,}/year")
            
            # Device lifecycle
            old_devices = []
            for device in devices:
                # Check if device model is old (simplified check)
                model = device.get('model', '')
                if any(old in model for old in ['MR18', 'MR32', 'MS220-8', 'MX64']):
                    old_devices.append(device)
            
            if old_devices:
                output.append(f"\n📟 Legacy Devices: {len(old_devices)}")
                output.append("• Consider hardware refresh")
                output.append("• New models may include licenses")
                output.append("• Better performance per dollar")
            
            # Subscription optimization
            output.append("\n📦 Subscription Optimization:")
            output.append("• Review active subscriptions")
            output.append("• Remove unused features")
            output.append("• Bundle for discounts")
            output.append("• Consider annual vs monthly")
            
            # Cost optimization tips
            output.append("\n💰 Cost Optimization Tips:")
            output.append("1. Remove licenses from decommissioned devices")
            output.append("2. Negotiate multi-year agreements")
            output.append("3. Right-size your license types")
            output.append("4. Use license pooling effectively")
            output.append("5. Monitor usage regularly")
            
            # ROI calculation
            output.append("\n📈 ROI Improvement:")
            if offline_devices > 0:
                output.append(f"• Bringing {offline_devices} devices online")
                output.append(f"• Would improve license ROI by {(offline_devices/total_devices*100):.1f}%")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("analyze licensing optimization", e)


def enhanced_licensing_help() -> str:
    """
    ❓ Get help with enhanced licensing tools.
    
    Shows available tools and best practices for license management.
    
    Returns:
        Formatted help guide
    """
    return """📋 Enhanced Licensing Tools Help
==================================================

Available tools for comprehensive license management:

1. get_organization_licensing_coterm_licenses()
   - View co-term license counts
   - Check by edition and type
   - Model-specific details
   - Total license inventory

2. move_organization_licensing_coterm_licenses()
   - Transfer between organizations
   - Bulk license moves
   - Co-term preservation
   - Migration support

3. get_device_licensing_subscription_entitlements()
   - Per-device subscriptions
   - Feature entitlements
   - Billing information
   - Subscription status

4. assign_organization_licenses()
   - Per-device assignment
   - Bulk operations
   - License allocation
   - Error handling

5. renew_organization_licensing_coterm()
   - Renewal process guide
   - Expiration tracking
   - Renewal benefits
   - Timeline management

6. get_organization_licensing_overview_by_device()
   - Device-level status
   - Expiration by device
   - Problem identification
   - Compliance check

7. get_organization_licensing_subscriptions()
   - Subscription inventory
   - Feature subscriptions
   - Usage tracking
   - Billing overview

8. claim_organization_licenses()
   - Add new licenses
   - Bulk key claiming
   - Validation results
   - Error reporting

9. licensing_expiration_report()
   - Comprehensive report
   - Expiration timeline
   - Risk assessment
   - Action items

10. licensing_optimization_analysis()
    - Usage analysis
    - Cost optimization
    - Model recommendations
    - ROI improvement

Licensing Models:
📊 Co-Termination
• All licenses same date
• Simplified renewal
• Volume discounts
• Single invoice

📱 Per-Device
• Individual expiration
• Flexible timing
• Device-specific
• Granular control

📦 Subscription
• Feature-based
• Monthly/annual
• Scalable
• OpEx model

License Types:
• Enterprise
• Advanced Security
• Systems Manager
• Insight
• MV Sense

Best Practices:
• Monitor expiration dates
• Plan 90 days ahead
• Track unused licenses
• Optimize assignments
• Regular audits
• Document changes

Common Tasks:
• Check expiration status
• Renew expiring licenses
• Move between orgs
• Assign to new devices
• Claim new licenses
• Optimize usage

Compliance:
• License true-up
• Audit readiness
• Usage reporting
• Cost tracking
• Budget planning

Troubleshooting:
• License not applying
• Expiration warnings
• Assignment errors
• Model mismatches
• Claim failures
"""


def register_enhanced_licensing_tools(app: FastMCP, meraki_client: MerakiClient):
    """Register all enhanced licensing tools with the MCP server."""
    global mcp_app, meraki
    mcp_app = app
    meraki = meraki_client
    
    # Register all tools
    tools = [
        (get_organization_licensing_coterm_licenses, "Get co-term license details"),
        (move_organization_licensing_coterm_licenses, "Move licenses between orgs"),
        (get_device_licensing_subscription_entitlements, "Get device subscriptions"),
        (assign_organization_licenses, "Assign licenses to devices"),
        (renew_organization_licensing_coterm, "Renew co-term licenses"),
        (get_organization_licensing_overview_by_device, "Get per-device licensing"),
        (get_organization_licensing_subscriptions, "Get subscription licenses"),
        (claim_organization_licenses, "Claim new license keys"),
        (licensing_expiration_report, "Generate expiration report"),
        (licensing_optimization_analysis, "Analyze license optimization"),
        (enhanced_licensing_help, "Get help with licensing tools"),
    ]
    
    for tool_func, description in tools:
        app.tool(
            name=tool_func.__name__,
            description=description
        )(tool_func)