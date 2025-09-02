"""
Inventory and device management tools for Cisco Meraki MCP server.

This module provides tools for managing organization inventory, devices, and packet captures.
"""

from typing import Optional, Dict, Any, List
from datetime import datetime
import json

# Global references to be set by register function
app = None
meraki_client = None

def register_inventory_tools(mcp_app, meraki):
    """
    Register inventory tools with the MCP server.
    
    Args:
        mcp_app: MCP server instance
        meraki: Meraki client instance
    """
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    
    # ==================== DEVICE INVENTORY ====================
    
    @app.tool(
        name="get_org_inventory_devices",
        description="📦 List all devices in organization inventory"
    )
    def get_org_inventory_devices(
        organization_id: str,
        per_page: int = 100,
        starting_after: Optional[str] = None,
        ending_before: Optional[str] = None,
        used_state: Optional[str] = None,
        search: Optional[str] = None,
        mac: Optional[str] = None,
        serial: Optional[str] = None,
        model: Optional[str] = None,
        order_numbers: Optional[str] = None,
        network_ids: Optional[str] = None,
        serials: Optional[str] = None,
        tags: Optional[str] = None,
        tags_filter_type: Optional[str] = None,
        product_types: Optional[str] = None
    ):
        """Get organization inventory devices."""
        try:
            kwargs = {"perPage": per_page}
            
            if starting_after:
                kwargs["startingAfter"] = starting_after
            if ending_before:
                kwargs["endingBefore"] = ending_before
            if used_state:
                kwargs["usedState"] = used_state
            if search:
                kwargs["search"] = search
            if mac:
                kwargs["mac"] = mac
            if serial:
                kwargs["serial"] = serial
            if model:
                kwargs["model"] = model
            if order_numbers:
                kwargs["orderNumbers"] = [n.strip() for n in order_numbers.split(',')]
            if network_ids:
                kwargs["networkIds"] = [n.strip() for n in network_ids.split(',')]
            if serials:
                kwargs["serials"] = [s.strip() for s in serials.split(',')]
            if tags:
                kwargs["tags"] = [t.strip() for t in tags.split(',')]
            if tags_filter_type:
                kwargs["tagsFilterType"] = tags_filter_type
            if product_types:
                kwargs["productTypes"] = [p.strip() for p in product_types.split(',')]
            
            result = meraki_client.dashboard.organizations.getOrganizationInventoryDevices(
                organization_id, **kwargs
            )
            
            response = f"# 📦 Organization Inventory\n\n"
            
            if result and isinstance(result, list):
                response += f"**Total Devices**: {len(result)}\n\n"
                
                # Group by product type
                by_type = {}
                for device in result:
                    product_type = device.get('productType', 'Unknown')
                    if product_type not in by_type:
                        by_type[product_type] = []
                    by_type[product_type].append(device)
                
                for product_type, devices in by_type.items():
                    response += f"## {product_type} ({len(devices)})\n"
                    for device in devices[:5]:
                        response += f"- **{device.get('model', 'Unknown')}** - {device.get('serial', 'N/A')}"
                        if device.get('name'):
                            response += f" ({device['name']})"
                        if device.get('networkId'):
                            response += f" [Assigned]"
                        else:
                            response += f" [Unassigned]"
                        response += "\n"
                    if len(devices) > 5:
                        response += f"  ... and {len(devices)-5} more\n"
                    response += "\n"
            else:
                response += "*No devices in inventory*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting inventory: {str(e)}"
    
    @app.tool(
        name="get_org_inventory_device",
        description="📦 Get details of a specific device in inventory"
    )
    def get_org_inventory_device(
        organization_id: str,
        serial: str
    ):
        """Get specific inventory device details."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationInventoryDevice(
                organization_id, serial
            )
            
            response = f"# 📦 Device Inventory Details\n\n"
            
            if result:
                response += f"**Model**: {result.get('model', 'Unknown')}\n"
                response += f"**Serial**: {result.get('serial', 'N/A')}\n"
                response += f"**Name**: {result.get('name', 'Not named')}\n"
                response += f"**MAC**: {result.get('mac', 'N/A')}\n"
                response += f"**Product Type**: {result.get('productType', 'N/A')}\n\n"
                
                # Network assignment
                if result.get('networkId'):
                    response += f"## Network Assignment\n"
                    response += f"- **Network ID**: {result['networkId']}\n"
                    response += f"- **Tags**: {', '.join(result.get('tags', []))}\n"
                else:
                    response += "**Status**: Unassigned\n"
                
                # Order info
                if result.get('orderNumber'):
                    response += f"\n## Order Information\n"
                    response += f"- **Order Number**: {result['orderNumber']}\n"
                    response += f"- **Claimed At**: {result.get('claimedAt', 'N/A')}\n"
                
                # License info
                if result.get('licenseExpirationDate'):
                    response += f"\n## License\n"
                    response += f"- **Expires**: {result['licenseExpirationDate']}\n"
            else:
                response += "*Device not found*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting device: {str(e)}"
    
    @app.tool(
        name="claim_into_org_inventory",
        description="📦➕ Claim devices into organization inventory"
    )
    def claim_into_org_inventory(
        organization_id: str,
        orders: Optional[str] = None,
        serials: Optional[str] = None,
        licenses: Optional[str] = None
    ):
        """
        Claim devices into inventory.
        
        Args:
            organization_id: Organization ID
            orders: Comma-separated order numbers
            serials: Comma-separated serial numbers
            licenses: JSON string of license configurations
        """
        try:
            kwargs = {}
            
            if orders:
                kwargs['orders'] = [o.strip() for o in orders.split(',')]
            if serials:
                kwargs['serials'] = [s.strip() for s in serials.split(',')]
            if licenses:
                kwargs['licenses'] = json.loads(licenses) if isinstance(licenses, str) else licenses
            
            result = meraki_client.dashboard.organizations.claimIntoOrganizationInventory(
                organization_id, **kwargs
            )
            
            response = f"# ✅ Claimed Devices\n\n"
            response += f"**Organization**: {organization_id}\n"
            
            if orders:
                response += f"**Orders**: {orders}\n"
            if serials:
                response += f"**Serials**: {serials}\n"
            
            return response
        except Exception as e:
            return f"❌ Error claiming devices: {str(e)}"
    
    @app.tool(
        name="release_from_org_inventory",
        description="📦❌ Release devices from organization inventory"
    )
    def release_from_org_inventory(
        organization_id: str,
        serials: str
    ):
        """
        Release devices from inventory.
        
        Args:
            organization_id: Organization ID
            serials: Comma-separated serial numbers
        """
        try:
            serial_list = [s.strip() for s in serials.split(',')]
            
            result = meraki_client.dashboard.organizations.releaseFromOrganizationInventory(
                organization_id, serials=serial_list
            )
            
            response = f"# ✅ Released Devices\n\n"
            response += f"**Serials**: {serials}\n"
            response += "Devices have been released from inventory.\n"
            
            return response
        except Exception as e:
            return f"❌ Error releasing devices: {str(e)}"
    
    # ==================== DEVICE STATUS & MONITORING ====================
    
    @app.tool(
        name="get_org_devices_statuses",
        description="📊 Get status of all devices in an organization"
    )
    def get_org_devices_statuses(
        organization_id: str,
        per_page: int = 100,
        starting_after: Optional[str] = None,
        ending_before: Optional[str] = None,
        network_ids: Optional[str] = None,
        serials: Optional[str] = None,
        statuses: Optional[str] = None,
        product_types: Optional[str] = None,
        models: Optional[str] = None,
        tags: Optional[str] = None,
        tags_filter_type: Optional[str] = None
    ):
        """Get device statuses."""
        try:
            kwargs = {"perPage": per_page}
            
            if starting_after:
                kwargs["startingAfter"] = starting_after
            if ending_before:
                kwargs["endingBefore"] = ending_before
            if network_ids:
                kwargs["networkIds"] = [n.strip() for n in network_ids.split(',')]
            if serials:
                kwargs["serials"] = [s.strip() for s in serials.split(',')]
            if statuses:
                kwargs["statuses"] = [s.strip() for s in statuses.split(',')]
            if product_types:
                kwargs["productTypes"] = [p.strip() for p in product_types.split(',')]
            if models:
                kwargs["models"] = [m.strip() for m in models.split(',')]
            if tags:
                kwargs["tags"] = [t.strip() for t in tags.split(',')]
            if tags_filter_type:
                kwargs["tagsFilterType"] = tags_filter_type
            
            result = meraki_client.dashboard.organizations.getOrganizationDevicesStatuses(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Device Statuses\n\n"
            
            if result and isinstance(result, list):
                response += f"**Total Devices**: {len(result)}\n\n"
                
                # Count by status
                status_counts = {}
                for device in result:
                    status = device.get('status', 'Unknown')
                    status_counts[status] = status_counts.get(status, 0) + 1
                
                response += "## Status Summary\n"
                for status, count in status_counts.items():
                    icon = "🟢" if status == "online" else "🔴" if status == "offline" else "🟡"
                    response += f"- {icon} **{status}**: {count}\n"
                
                response += "\n## Devices\n"
                for device in result[:10]:
                    status = device.get('status', 'unknown')
                    icon = "🟢" if status == "online" else "🔴"
                    response += f"{icon} **{device.get('name', device.get('serial', 'Unknown'))}**\n"
                    response += f"  - Model: {device.get('model', 'N/A')}\n"
                    response += f"  - Serial: {device.get('serial', 'N/A')}\n"
                    if device.get('lastReportedAt'):
                        response += f"  - Last Seen: {device['lastReportedAt']}\n"
                
                if len(result) > 10:
                    response += f"\n... and {len(result)-10} more devices\n"
            else:
                response += "*No devices found*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting device statuses: {str(e)}"
    
    @app.tool(
        name="get_org_devices_availabilities",
        description="📈 Get availability history for devices"
    )
    def get_org_devices_availabilities(
        organization_id: str,
        per_page: int = 100,
        starting_after: Optional[str] = None,
        ending_before: Optional[str] = None,
        network_ids: Optional[str] = None,
        serials: Optional[str] = None,
        product_types: Optional[str] = None,
        tags: Optional[str] = None,
        tags_filter_type: Optional[str] = None
    ):
        """Get device availability history."""
        try:
            kwargs = {"perPage": per_page}
            
            if starting_after:
                kwargs["startingAfter"] = starting_after
            if ending_before:
                kwargs["endingBefore"] = ending_before
            if network_ids:
                kwargs["networkIds"] = [n.strip() for n in network_ids.split(',')]
            if serials:
                kwargs["serials"] = [s.strip() for s in serials.split(',')]
            if product_types:
                kwargs["productTypes"] = [p.strip() for p in product_types.split(',')]
            if tags:
                kwargs["tags"] = [t.strip() for t in tags.split(',')]
            if tags_filter_type:
                kwargs["tagsFilterType"] = tags_filter_type
            
            result = meraki_client.dashboard.organizations.getOrganizationDevicesAvailabilities(
                organization_id, **kwargs
            )
            
            response = f"# 📈 Device Availabilities\n\n"
            
            if result and isinstance(result, list):
                response += f"**Total Devices**: {len(result)}\n\n"
                
                for device in result[:10]:
                    response += f"## {device.get('name', device.get('serial', 'Unknown'))}\n"
                    response += f"- **Serial**: {device.get('serial', 'N/A')}\n"
                    response += f"- **Status**: {device.get('status', 'N/A')}\n"
                    
                    # Availability history
                    history = device.get('availabilityHistory', [])
                    if history:
                        response += f"- **Availability (last 24h)**: "
                        online_count = sum(1 for h in history if h.get('status') == 'online')
                        percentage = (online_count / len(history) * 100) if history else 0
                        response += f"{percentage:.1f}%\n"
                    
                    response += "\n"
                
                if len(result) > 10:
                    response += f"... and {len(result)-10} more devices\n"
            else:
                response += "*No availability data found*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting availabilities: {str(e)}"
    
    @app.tool(
        name="get_org_devices_availabilities_change_history",
        description="📈 Get availability change history for devices"
    )
    def get_org_devices_availabilities_change_history(
        organization_id: str,
        per_page: int = 100,
        starting_after: Optional[str] = None,
        ending_before: Optional[str] = None,
        t0: Optional[str] = None,
        t1: Optional[str] = None,
        timespan: Optional[float] = None,
        serials: Optional[str] = None,
        product_types: Optional[str] = None,
        network_ids: Optional[str] = None
    ):
        """Get device availability change history."""
        try:
            kwargs = {"perPage": per_page}
            
            if starting_after:
                kwargs["startingAfter"] = starting_after
            if ending_before:
                kwargs["endingBefore"] = ending_before
            if t0:
                kwargs["t0"] = t0
            if t1:
                kwargs["t1"] = t1
            if timespan:
                kwargs["timespan"] = timespan
            if serials:
                kwargs["serials"] = [s.strip() for s in serials.split(',')]
            if product_types:
                kwargs["productTypes"] = [p.strip() for p in product_types.split(',')]
            if network_ids:
                kwargs["networkIds"] = [n.strip() for n in network_ids.split(',')]
            
            result = meraki_client.dashboard.organizations.getOrganizationDevicesAvailabilitiesChangeHistory(
                organization_id, **kwargs
            )
            
            response = f"# 📈 Availability Change History\n\n"
            
            if result and isinstance(result, list):
                response += f"**Total Changes**: {len(result)}\n\n"
                
                for change in result[:20]:
                    device = change.get('device', {})
                    response += f"## {device.get('name', device.get('serial', 'Unknown'))}\n"
                    response += f"- **Time**: {change.get('ts', 'N/A')}\n"
                    
                    details = change.get('details', {})
                    old_status = details.get('oldStatus', 'N/A')
                    new_status = details.get('newStatus', 'N/A')
                    
                    old_icon = "🟢" if old_status == "online" else "🔴"
                    new_icon = "🟢" if new_status == "online" else "🔴"
                    
                    response += f"- **Change**: {old_icon} {old_status} → {new_icon} {new_status}\n\n"
                
                if len(result) > 20:
                    response += f"... and {len(result)-20} more changes\n"
            else:
                response += "*No availability changes found*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting change history: {str(e)}"
    
    @app.tool(
        name="get_org_devices_statuses_overview",
        description="📊 Get overview of device statuses in organization"
    )
    def get_org_devices_statuses_overview(
        organization_id: str,
        product_types: Optional[str] = None,
        network_ids: Optional[str] = None
    ):
        """Get device statuses overview."""
        try:
            kwargs = {}
            
            if product_types:
                kwargs["productTypes"] = [p.strip() for p in product_types.split(',')]
            if network_ids:
                kwargs["networkIds"] = [n.strip() for n in network_ids.split(',')]
            
            result = meraki_client.dashboard.organizations.getOrganizationDevicesStatusesOverview(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Device Statuses Overview\n\n"
            
            if result:
                # Overall summary
                summary = result.get('summary', {})
                if summary:
                    response += "## Summary\n"
                    response += f"- 🟢 **Online**: {summary.get('online', 0)}\n"
                    response += f"- 🔴 **Offline**: {summary.get('offline', 0)}\n"
                    response += f"- 🟡 **Alerting**: {summary.get('alerting', 0)}\n"
                    response += f"- 🟠 **Dormant**: {summary.get('dormant', 0)}\n"
                    response += f"- **Total**: {summary.get('total', 0)}\n\n"
                
                # By product type
                by_product = result.get('byProductType', [])
                if by_product:
                    response += "## By Product Type\n"
                    for product in by_product:
                        response += f"### {product.get('productType', 'Unknown')}\n"
                        response += f"- Online: {product.get('online', 0)}\n"
                        response += f"- Offline: {product.get('offline', 0)}\n"
                        response += f"- Total: {product.get('total', 0)}\n\n"
            else:
                response += "*No overview data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting overview: {str(e)}"
    
    @app.tool(
        name="get_org_devices_uplinks_addresses_by_device",
        description="🔗 Get uplink addresses for devices"
    )
    def get_org_devices_uplinks_addresses_by_device(
        organization_id: str,
        per_page: int = 100,
        starting_after: Optional[str] = None,
        ending_before: Optional[str] = None,
        network_ids: Optional[str] = None,
        product_types: Optional[str] = None,
        serials: Optional[str] = None,
        tags: Optional[str] = None,
        tags_filter_type: Optional[str] = None
    ):
        """Get device uplink addresses."""
        try:
            kwargs = {"perPage": per_page}
            
            if starting_after:
                kwargs["startingAfter"] = starting_after
            if ending_before:
                kwargs["endingBefore"] = ending_before
            if network_ids:
                kwargs["networkIds"] = [n.strip() for n in network_ids.split(',')]
            if product_types:
                kwargs["productTypes"] = [p.strip() for p in product_types.split(',')]
            if serials:
                kwargs["serials"] = [s.strip() for s in serials.split(',')]
            if tags:
                kwargs["tags"] = [t.strip() for t in tags.split(',')]
            if tags_filter_type:
                kwargs["tagsFilterType"] = tags_filter_type
            
            result = meraki_client.dashboard.organizations.getOrganizationDevicesUplinksAddressesByDevice(
                organization_id, **kwargs
            )
            
            response = f"# 🔗 Device Uplink Addresses\n\n"
            
            if result and isinstance(result, list):
                response += f"**Total Devices**: {len(result)}\n\n"
                
                for device in result[:10]:
                    response += f"## {device.get('name', device.get('serial', 'Unknown'))}\n"
                    response += f"- **Serial**: {device.get('serial', 'N/A')}\n"
                    response += f"- **Model**: {device.get('model', 'N/A')}\n"
                    
                    # Uplinks
                    uplinks = device.get('uplinks', [])
                    if uplinks:
                        response += "- **Uplinks**:\n"
                        for uplink in uplinks:
                            response += f"  - {uplink.get('interface', 'N/A')}: "
                            
                            # Public IP
                            public_ip = uplink.get('public', {})
                            if public_ip.get('address'):
                                response += f"{public_ip['address']}"
                            
                            # Status
                            if uplink.get('status'):
                                icon = "🟢" if uplink['status'] == 'active' else "🔴"
                                response += f" {icon} {uplink['status']}"
                            
                            response += "\n"
                    
                    response += "\n"
                
                if len(result) > 10:
                    response += f"... and {len(result)-10} more devices\n"
            else:
                response += "*No uplink data found*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting uplink addresses: {str(e)}"
    
    @app.tool(
        name="get_org_devices_uplinks_loss_and_latency",
        description="📉 Get uplink loss and latency for devices"
    )
    def get_org_devices_uplinks_loss_and_latency(
        organization_id: str,
        t0: Optional[str] = None,
        t1: Optional[str] = None,
        timespan: Optional[float] = None,
        uplink: Optional[str] = None,
        ip: Optional[str] = None
    ):
        """Get device uplink loss and latency."""
        try:
            kwargs = {}
            
            if t0:
                kwargs["t0"] = t0
            if t1:
                kwargs["t1"] = t1
            if timespan:
                kwargs["timespan"] = timespan
            if uplink:
                kwargs["uplink"] = uplink
            if ip:
                kwargs["ip"] = ip
            
            result = meraki_client.dashboard.organizations.getOrganizationDevicesUplinksLossAndLatency(
                organization_id, **kwargs
            )
            
            response = f"# 📉 Uplink Loss and Latency\n\n"
            
            if result and isinstance(result, list):
                response += f"**Total Devices**: {len(result)}\n\n"
                
                for device in result[:10]:
                    response += f"## {device.get('networkName', 'Unknown Network')}\n"
                    response += f"- **Device**: {device.get('serial', 'N/A')}\n"
                    
                    # Time series data
                    time_series = device.get('timeSeries', [])
                    if time_series:
                        # Get latest data point
                        latest = time_series[-1] if time_series else {}
                        response += f"- **Latest** ({latest.get('ts', 'N/A')}):\n"
                        response += f"  - Loss: {latest.get('lossPercent', 0):.1f}%\n"
                        response += f"  - Latency: {latest.get('latencyMs', 0):.1f}ms\n"
                        
                        # Calculate averages
                        avg_loss = sum(t.get('lossPercent', 0) for t in time_series) / len(time_series)
                        avg_latency = sum(t.get('latencyMs', 0) for t in time_series) / len(time_series)
                        response += f"- **Averages**:\n"
                        response += f"  - Loss: {avg_loss:.1f}%\n"
                        response += f"  - Latency: {avg_latency:.1f}ms\n"
                    
                    response += "\n"
                
                if len(result) > 10:
                    response += f"... and {len(result)-10} more devices\n"
            else:
                response += "*No loss/latency data found*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting loss/latency: {str(e)}"
    
    # ==================== BULK OPERATIONS ====================
    
    @app.tool(
        name="bulk_update_org_devices_details",
        description="📦✏️ Bulk update device details"
    )
    def bulk_update_org_devices_details(
        organization_id: str,
        serials: str,
        details: str
    ):
        """
        Bulk update device details.
        
        Args:
            organization_id: Organization ID
            serials: Comma-separated serial numbers
            details: JSON string of device details to update
        """
        try:
            serial_list = [s.strip() for s in serials.split(',')]
            details_dict = json.loads(details) if isinstance(details, str) else details
            
            result = meraki_client.dashboard.organizations.bulkUpdateOrganizationDevicesDetails(
                organization_id, 
                serials=serial_list,
                details=details_dict
            )
            
            response = f"# ✅ Bulk Updated Devices\n\n"
            response += f"**Serials**: {serials}\n"
            response += f"**Updates Applied**: {json.dumps(details_dict, indent=2)}\n"
            
            return response
        except Exception as e:
            return f"❌ Error bulk updating: {str(e)}"