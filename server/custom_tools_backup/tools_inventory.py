"""
Inventory Management Tools for Cisco Meraki MCP Server
Manage organization inventory, device claiming, and license management
"""

from mcp.server import FastMCP
from typing import Optional, Dict, Any, List
import json
from datetime import datetime
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


def get_organization_inventory_devices(
    org_id: str,
    used_state: Optional[str] = None,
    search: Optional[str] = None,
    tags: Optional[List[str]] = None,
    tags_filter_type: Optional[str] = None,
    product_types: Optional[List[str]] = None,
    serials: Optional[List[str]] = None,
    models: Optional[List[str]] = None,
    network_ids: Optional[List[str]] = None,
    per_page: Optional[int] = None
) -> str:
    """
    📦 Get device inventory for an organization.
    
    Lists all devices in the organization's inventory with detailed information.
    
    Args:
        org_id: Organization ID
        used_state: Filter by usage state (unused, used)
        search: Search for devices by serial, MAC, or model
        tags: Filter by tags
        tags_filter_type: Tag filter type (withAllTags, withAnyTags)
        product_types: Filter by product types (wireless, switch, appliance, etc.)
        serials: Filter by specific serial numbers
        models: Filter by specific models
        network_ids: Filter by network IDs
        per_page: Number of results per page
    
    Returns:
        Inventory device list with details
    """
    try:
        with safe_api_call("get inventory devices"):
            # Build parameters
            params = {}
            if used_state:
                params['usedState'] = used_state
            if search:
                params['search'] = search
            if tags:
                params['tags'] = tags
            if tags_filter_type:
                params['tagsFilterType'] = tags_filter_type
            if product_types:
                params['productTypes'] = product_types
            if serials:
                params['serials'] = serials
            if models:
                params['models'] = models
            if network_ids:
                params['networkIds'] = network_ids
            if per_page:
                params['perPage'] = per_page
            
            devices = meraki.dashboard.organizations.getOrganizationInventoryDevices(
                org_id,
                **params
            )
            
            output = ["📦 Organization Inventory", "=" * 50, ""]
            
            if not devices:
                output.append("No devices found in inventory")
                return "\n".join(output)
            
            # Group devices by status and type
            by_status = {'unused': [], 'used': []}
            by_type = {}
            
            for device in devices:
                # Status grouping
                if device.get('networkId'):
                    by_status['used'].append(device)
                else:
                    by_status['unused'].append(device)
                
                # Type grouping
                product_type = device.get('productType', 'Unknown')
                if product_type not in by_type:
                    by_type[product_type] = []
                by_type[product_type].append(device)
            
            # Summary
            output.append(f"Total Devices: {len(devices)}")
            output.append(f"   📗 In Use: {len(by_status['used'])}")
            output.append(f"   📘 Available: {len(by_status['unused'])}")
            output.append("")
            
            # By product type
            output.append("📊 By Product Type:")
            for prod_type, type_devices in sorted(by_type.items()):
                output.append(f"   {prod_type}: {len(type_devices)}")
            output.append("")
            
            # Show device details
            output.append("📋 Device Details:")
            
            # Show unused devices first (more important)
            if by_status['unused']:
                output.append("\n🆕 Available Devices:")
                for device in by_status['unused'][:10]:  # First 10
                    serial = device.get('serial', 'Unknown')
                    model = device.get('model', 'Unknown')
                    mac = device.get('mac', 'N/A')
                    name = device.get('name') or 'Unnamed'
                    
                    output.append(f"\n   📱 {name}")
                    output.append(f"      Serial: {serial}")
                    output.append(f"      Model: {model}")
                    output.append(f"      MAC: {mac}")
                    
                    # Order info
                    if device.get('orderNumber'):
                        output.append(f"      Order: {device['orderNumber']}")
                    
                    # License info
                    if device.get('licenseExpirationDate'):
                        output.append(f"      License Expires: {device['licenseExpirationDate']}")
                    
                    # Tags
                    if device.get('tags'):
                        output.append(f"      Tags: {', '.join(device['tags'])}")
                
                if len(by_status['unused']) > 10:
                    output.append(f"\n   ... and {len(by_status['unused']) - 10} more available devices")
            
            # Show in-use devices
            if by_status['used']:
                output.append("\n✅ Devices In Use:")
                for device in by_status['used'][:5]:  # First 5
                    serial = device.get('serial', 'Unknown')
                    model = device.get('model', 'Unknown')
                    name = device.get('name') or serial
                    network_id = device.get('networkId', 'N/A')
                    
                    output.append(f"\n   📱 {name}")
                    output.append(f"      Serial: {serial}")
                    output.append(f"      Model: {model}")
                    output.append(f"      Network: {network_id}")
                    
                    if device.get('claimedAt'):
                        output.append(f"      Claimed: {device['claimedAt']}")
                
                if len(by_status['used']) > 5:
                    output.append(f"\n   ... and {len(by_status['used']) - 5} more devices in use")
            
            # Recommendations
            output.append("\n💡 Inventory Tips:")
            output.append("• Claim unused devices to networks")
            output.append("• Tag devices for easier management")
            output.append("• Monitor license expiration dates")
            output.append("• Use search to find specific devices")
            output.append("• Export inventory for auditing")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("get inventory devices", e)


def get_organization_inventory_device(
    org_id: str,
    serial: str
) -> str:
    """
    🔍 Get details for a specific device in inventory.
    
    Shows comprehensive information about a single device.
    
    Args:
        org_id: Organization ID
        serial: Device serial number
    
    Returns:
        Detailed device information
    """
    try:
        with safe_api_call("get inventory device"):
            device = meraki.dashboard.organizations.getOrganizationInventoryDevice(
                org_id,
                serial
            )
            
            output = ["🔍 Device Details", "=" * 50, ""]
            
            # Basic info
            output.append(f"📱 {device.get('name') or device.get('serial', 'Unknown')}")
            output.append(f"Serial: {device.get('serial', 'Unknown')}")
            output.append(f"Model: {device.get('model', 'Unknown')}")
            output.append(f"MAC: {device.get('mac', 'N/A')}")
            output.append("")
            
            # Status
            if device.get('networkId'):
                output.append("📊 Status: ✅ In Use")
                output.append(f"   Network ID: {device['networkId']}")
                if device.get('claimedAt'):
                    output.append(f"   Claimed: {device['claimedAt']}")
            else:
                output.append("📊 Status: 📘 Available")
                output.append("   Not assigned to any network")
            
            # Product info
            output.append(f"\n📦 Product Type: {device.get('productType', 'Unknown')}")
            
            # Order info
            if device.get('orderNumber'):
                output.append(f"\n📋 Order Information:")
                output.append(f"   Order Number: {device['orderNumber']}")
                if device.get('claimedAt'):
                    output.append(f"   Claimed Date: {device['claimedAt']}")
            
            # License info
            if device.get('licenseExpirationDate'):
                output.append(f"\n📅 License:")
                output.append(f"   Expires: {device['licenseExpirationDate']}")
                
                # Calculate days until expiration
                try:
                    exp_date = datetime.fromisoformat(device['licenseExpirationDate'].replace('Z', '+00:00'))
                    days_left = (exp_date - datetime.now(exp_date.tzinfo)).days
                    
                    if days_left < 0:
                        output.append(f"   ⚠️ EXPIRED {abs(days_left)} days ago")
                    elif days_left < 30:
                        output.append(f"   ⚠️ Expiring in {days_left} days")
                    else:
                        output.append(f"   ✅ Valid for {days_left} days")
                except:
                    pass
            
            # Tags
            if device.get('tags'):
                output.append(f"\n🏷️ Tags: {', '.join(device['tags'])}")
            
            # Location info
            if device.get('countryCode'):
                output.append(f"\n📍 Country: {device['countryCode']}")
            
            # Additional details
            details = device.get('details', [])
            if details:
                output.append("\n📝 Additional Details:")
                for detail in details:
                    name = detail.get('name', 'Unknown')
                    value = detail.get('value', 'N/A')
                    output.append(f"   {name}: {value}")
            
            # Actions available
            output.append("\n🔧 Available Actions:")
            if not device.get('networkId'):
                output.append("   • Claim to a network")
                output.append("   • Add tags")
            else:
                output.append("   • Move to different network")
                output.append("   • Update tags")
                output.append("   • Release from network")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("get inventory device", e)


def claim_into_organization_inventory(
    org_id: str,
    orders: Optional[List[str]] = None,
    serials: Optional[List[str]] = None,
    licenses: Optional[List[Dict[str, str]]] = None
) -> str:
    """
    ➕ Claim devices, licenses, and/or orders into inventory.
    
    Add new equipment to the organization's inventory.
    
    Args:
        org_id: Organization ID
        orders: List of order numbers to claim
        serials: List of device serial numbers to claim
        licenses: List of license keys with mode (renew/addDevices)
    
    Returns:
        Claim results and status
    """
    try:
        with safe_api_call("claim into inventory"):
            # Build claim request
            claim_data = {}
            
            if orders:
                claim_data['orders'] = orders
            if serials:
                claim_data['serials'] = serials
            if licenses:
                claim_data['licenses'] = licenses
            
            if not claim_data:
                return "❌ No items specified to claim. Provide orders, serials, or licenses."
            
            # Perform the claim
            result = meraki.dashboard.organizations.claimIntoOrganizationInventory(
                org_id,
                **claim_data
            )
            
            output = ["➕ Inventory Claim Results", "=" * 50, ""]
            
            # Show what was claimed
            if orders:
                output.append(f"📦 Orders Claimed: {len(orders)}")
                for order in orders[:5]:
                    output.append(f"   • {order}")
                if len(orders) > 5:
                    output.append(f"   ... and {len(orders) - 5} more")
                output.append("")
            
            if serials:
                output.append(f"📱 Devices Claimed: {len(serials)}")
                for serial in serials[:10]:
                    output.append(f"   • {serial}")
                if len(serials) > 10:
                    output.append(f"   ... and {len(serials) - 10} more")
                output.append("")
            
            if licenses:
                output.append(f"🔑 Licenses Claimed: {len(licenses)}")
                for lic in licenses[:5]:
                    mode = lic.get('mode', 'unknown')
                    output.append(f"   • License: ****{lic.get('key', '')[-4:]} (Mode: {mode})")
                if len(licenses) > 5:
                    output.append(f"   ... and {len(licenses) - 5} more")
            
            # Process results
            if isinstance(result, dict):
                # Check for errors
                errors = result.get('errors', [])
                if errors:
                    output.append("\n❌ Errors:")
                    for error in errors:
                        output.append(f"   • {error}")
                
                # Successfully claimed items
                if result.get('orders'):
                    output.append(f"\n✅ Orders processed: {len(result['orders'])}")
                
                if result.get('serials'):
                    output.append(f"✅ Devices added: {len(result['serials'])}")
                
                if result.get('licenses'):
                    output.append(f"✅ Licenses added: {len(result['licenses'])}")
            
            output.append("\n💡 Next Steps:")
            output.append("• Check inventory for new devices")
            output.append("• Assign devices to networks")
            output.append("• Configure device settings")
            output.append("• Apply tags for organization")
            
            # Rate limit warning
            output.append("\n⚠️ Note: Claiming is rate-limited to 10 requests per 5 minutes")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("claim into inventory", e)


def release_from_organization_inventory(
    org_id: str,
    serials: List[str]
) -> str:
    """
    ➖ Release devices from organization inventory.
    
    Remove devices from the organization. Devices must not be in use.
    
    Args:
        org_id: Organization ID
        serials: List of device serial numbers to release
    
    Returns:
        Release results
    """
    try:
        with safe_api_call("release from inventory"):
            if not serials:
                return "❌ No serial numbers provided to release"
            
            # Perform the release
            result = meraki.dashboard.organizations.releaseFromOrganizationInventory(
                org_id,
                serials=serials
            )
            
            output = ["➖ Inventory Release Results", "=" * 50, ""]
            output.append(f"Organization: {org_id}")
            output.append(f"Devices to Release: {len(serials)}")
            output.append("")
            
            # List devices
            output.append("📱 Devices Released:")
            for serial in serials[:10]:
                output.append(f"   • {serial}")
            if len(serials) > 10:
                output.append(f"   ... and {len(serials) - 10} more")
            
            # Process results
            if isinstance(result, dict):
                # Check for errors
                errors = result.get('errors', [])
                if errors:
                    output.append("\n❌ Errors:")
                    for error in errors:
                        output.append(f"   • {error}")
                    output.append("\n💡 Common issues:")
                    output.append("• Device is assigned to a network")
                    output.append("• Device has active configuration")
                    output.append("• Invalid serial number")
                else:
                    output.append("\n✅ All devices successfully released")
            
            output.append("\n⚠️ Important:")
            output.append("• Released devices are removed from organization")
            output.append("• This action cannot be undone")
            output.append("• Devices must be unclaimed from networks first")
            output.append("• License seats may be affected")
            
            # Rate limit warning
            output.append("\n⚠️ Note: Release is rate-limited to 10 requests per 5 minutes")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("release from inventory", e)


def create_organization_inventory_devices_swaps_bulk(
    org_id: str,
    swaps: List[Dict[str, Any]]
) -> str:
    """
    🔄 Bulk swap devices in networks.
    
    Replace multiple devices across networks in a single operation.
    
    Args:
        org_id: Organization ID
        swaps: List of swap operations with old/new device info
    
    Returns:
        Swap operation results
    """
    try:
        with safe_api_call("bulk device swaps"):
            if not swaps:
                return "❌ No swap operations provided"
            
            # Perform the swaps
            result = meraki.dashboard.organizations.createOrganizationInventoryDevicesSwapsBulk(
                org_id,
                swaps=swaps
            )
            
            output = ["🔄 Bulk Device Swap Results", "=" * 50, ""]
            output.append(f"Organization: {org_id}")
            output.append(f"Swap Operations: {len(swaps)}")
            output.append("")
            
            # Show swap details
            output.append("📋 Swap Operations:")
            for i, swap in enumerate(swaps[:5], 1):
                old_serial = swap.get('devices', {}).get('old', {}).get('serial', 'Unknown')
                new_serial = swap.get('devices', {}).get('new', {}).get('serial', 'Unknown')
                
                output.append(f"\n{i}. Swap Operation:")
                output.append(f"   Old Device: {old_serial}")
                output.append(f"   New Device: {new_serial}")
                
                # Check for afterAction
                after_action = swap.get('afterAction', 'release')
                output.append(f"   After Action: {after_action}")
            
            if len(swaps) > 5:
                output.append(f"\n... and {len(swaps) - 5} more swaps")
            
            # Process results
            if isinstance(result, dict):
                swap_id = result.get('id', 'Unknown')
                status = result.get('status', 'Unknown')
                
                output.append(f"\n📊 Swap Status:")
                output.append(f"   Swap ID: {swap_id}")
                output.append(f"   Status: {status}")
                
                # Check for errors
                errors = result.get('errors', [])
                if errors:
                    output.append("\n❌ Errors:")
                    for error in errors:
                        output.append(f"   • {error}")
            
            output.append("\n💡 Swap Guidelines:")
            output.append("• Old device must be in a network")
            output.append("• New device must be in inventory")
            output.append("• Devices must be same product type")
            output.append("• Configuration is preserved")
            output.append("• Monitor swap status for completion")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("bulk device swaps", e)


def analyze_inventory_usage(org_id: str) -> str:
    """
    📊 Analyze inventory usage and provide recommendations.
    
    Shows inventory statistics and optimization suggestions.
    
    Args:
        org_id: Organization ID
    
    Returns:
        Inventory analysis and recommendations
    """
    try:
        with safe_api_call("analyze inventory"):
            # Get all inventory devices
            devices = meraki.dashboard.organizations.getOrganizationInventoryDevices(org_id)
            
            output = ["📊 Inventory Analysis", "=" * 50, ""]
            
            if not devices:
                output.append("No devices in inventory")
                return "\n".join(output)
            
            # Calculate statistics
            total = len(devices)
            used = len([d for d in devices if d.get('networkId')])
            unused = total - used
            usage_rate = (used / total * 100) if total > 0 else 0
            
            # License analysis
            expiring_soon = []
            expired = []
            
            for device in devices:
                if device.get('licenseExpirationDate'):
                    try:
                        exp_date = datetime.fromisoformat(
                            device['licenseExpirationDate'].replace('Z', '+00:00')
                        )
                        days_left = (exp_date - datetime.now(exp_date.tzinfo)).days
                        
                        if days_left < 0:
                            expired.append(device)
                        elif days_left < 90:
                            expiring_soon.append((device, days_left))
                    except:
                        pass
            
            # Show statistics
            output.append(f"📈 Inventory Statistics:")
            output.append(f"   Total Devices: {total}")
            output.append(f"   In Use: {used} ({usage_rate:.1f}%)")
            output.append(f"   Available: {unused}")
            output.append("")
            
            # Device type breakdown
            by_type = {}
            for device in devices:
                prod_type = device.get('productType', 'Unknown')
                if prod_type not in by_type:
                    by_type[prod_type] = {'total': 0, 'used': 0}
                by_type[prod_type]['total'] += 1
                if device.get('networkId'):
                    by_type[prod_type]['used'] += 1
            
            output.append("📱 By Product Type:")
            for prod_type, counts in sorted(by_type.items()):
                usage = (counts['used'] / counts['total'] * 100) if counts['total'] > 0 else 0
                output.append(f"   {prod_type}: {counts['used']}/{counts['total']} ({usage:.0f}% used)")
            
            # License warnings
            if expired or expiring_soon:
                output.append("\n⚠️ License Alerts:")
                
                if expired:
                    output.append(f"   🔴 Expired: {len(expired)} devices")
                    for device in expired[:3]:
                        output.append(f"      • {device.get('serial')} - {device.get('model')}")
                
                if expiring_soon:
                    output.append(f"   🟡 Expiring Soon: {len(expiring_soon)} devices")
                    for device, days in sorted(expiring_soon, key=lambda x: x[1])[:3]:
                        output.append(f"      • {device.get('serial')} - {days} days left")
            
            # Recommendations
            output.append("\n💡 Recommendations:")
            
            if usage_rate < 80:
                output.append(f"• Low utilization ({usage_rate:.0f}%) - Deploy {unused} available devices")
            
            if expired:
                output.append(f"• Renew licenses for {len(expired)} expired devices")
            
            if expiring_soon:
                output.append(f"• Plan renewal for {len(expiring_soon)} expiring licenses")
            
            # Model diversity
            model_count = len(set(d.get('model') for d in devices))
            if model_count > 10:
                output.append(f"• High model diversity ({model_count} models) - Consider standardization")
            
            # Unused device recommendations
            if unused > 10:
                output.append("\n📦 Unused Device Actions:")
                output.append("• Deploy to new locations")
                output.append("• Keep as spare inventory")
                output.append("• Release unneeded devices")
                output.append("• Consider license optimization")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("analyze inventory", e)


def inventory_help() -> str:
    """
    ❓ Get help with inventory management tools.
    
    Shows available tools and best practices.
    
    Returns:
        Formatted help guide
    """
    return """📦 Inventory Management Tools Help
==================================================

Available tools for inventory management:

1. get_organization_inventory_devices()
   - List all inventory devices
   - Filter by status, type, tags
   - Search by serial or MAC
   - Export-ready data

2. get_organization_inventory_device()
   - Detailed single device info
   - License status
   - Network assignment
   - Order information

3. claim_into_organization_inventory()
   - Claim devices by serial
   - Claim entire orders
   - Add licenses
   - Bulk operations

4. release_from_organization_inventory()
   - Remove unused devices
   - Free up licenses
   - Clean inventory
   - Bulk release

5. create_organization_inventory_devices_swaps_bulk()
   - Replace devices in networks
   - Preserve configuration
   - Bulk swaps
   - RMA workflows

6. analyze_inventory_usage()
   - Usage statistics
   - License warnings
   - Optimization tips
   - Deployment recommendations

Inventory States:
📗 In Use - Assigned to a network
📘 Available - In inventory, not assigned
🔴 Expired - License expired
🟡 Expiring - License expiring soon

Best Practices:
• Regular inventory audits
• Monitor license expiration
• Tag devices for tracking
• Maintain spare inventory
• Document serial numbers
• Plan device refresh cycles

Common Operations:
• Claiming new purchases
• Deploying to networks
• Swapping failed devices
• License management
• Inventory optimization

Rate Limits:
⚠️ Stricter limit: 10 requests per 5 minutes
• Applies to claim/release operations
• Plan bulk operations carefully
• Use batching when possible

Tips:
• Export inventory regularly
• Use tags for asset tracking
• Monitor usage patterns
• Plan for growth
• Keep spare devices ready
"""


def register_inventory_tools(app: FastMCP, meraki_client: MerakiClient):
    """Register all inventory management tools with the MCP server."""
    global mcp_app, meraki
    mcp_app = app
    meraki = meraki_client
    
    # Register all tools
    tools = [
        (get_organization_inventory_devices, "List organization inventory devices"),
        (get_organization_inventory_device, "Get specific device details"),
        (claim_into_organization_inventory, "Claim devices/licenses into inventory"),
        (release_from_organization_inventory, "Release devices from inventory"),
        (create_organization_inventory_devices_swaps_bulk, "Bulk swap devices"),
        (analyze_inventory_usage, "Analyze inventory usage and recommendations"),
        (inventory_help, "Get help with inventory management"),
    ]
    
    for tool_func, description in tools:
        app.tool(
            name=tool_func.__name__,
            description=description
        )(tool_func)