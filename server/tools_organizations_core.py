"""
Core organization management tools for Cisco Meraki MCP server.

This module provides fundamental organization management including
organization CRUD, networks, and basic inventory operations.
"""

from typing import Optional, Dict, Any, List

# Global references to be set by register function
app = None
meraki_client = None

def register_organizations_core_tools(mcp_app, meraki):
    """
    Register core organization tools with the MCP server.
    
    Args:
        mcp_app: MCP server instance
        meraki: Meraki client instance
    """
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    
    # Register tool handlers
    register_organizations_core_handlers()

def register_organizations_core_handlers():
    """Register all core organization tool handlers."""
    
    # ==================== ORGANIZATION MANAGEMENT ====================
    
    @app.tool(
        name="get_organizations",
        description="🏢 List all organizations accessible to the API key."
    )
    def get_organizations():
        """
        List all organizations.
        """
        try:
            result = meraki_client.dashboard.organizations.getOrganizations()
            
            response = f"# 🏢 Organizations\n\n"
            
            if result and isinstance(result, list):
                response += f"**Total Organizations**: {len(result)}\n\n"
                
                for org in result:
                    org_id = org.get('id', 'Unknown')
                    response += f"## {org.get('name', 'Unnamed')}\n"
                    response += f"- **ID**: {org_id}\n"
                    response += f"- **URL**: {org.get('url', 'N/A')}\n"
                    
                    # API settings
                    api = org.get('api', {})
                    if api.get('enabled'):
                        response += f"- **API**: Enabled\n"
                    
                    # Cloud region
                    cloud = org.get('cloud', {})
                    if cloud:
                        response += f"- **Region**: {cloud.get('region', {}).get('name', 'N/A')}\n"
                    
                    # Management details
                    mgmt = org.get('management', {})
                    if mgmt:
                        response += f"- **Management**: "
                        details = mgmt.get('details', [])
                        if details:
                            response += f"{', '.join(d.get('name', '') for d in details)}\n"
                        else:
                            response += "Standard\n"
                    
                    # Licensing
                    licensing = org.get('licensing', {})
                    if licensing:
                        model = licensing.get('model', 'N/A')
                        response += f"- **Licensing Model**: {model}\n"
                    
                    response += "\n"
            else:
                response += "*No organizations found*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting organizations: {str(e)}"
    
    @app.tool(
        name="get_organization",
        description="🏢 Get detailed information about a specific organization."
    )
    def get_organization(
        organization_id: str
    ):
        """
        Get organization details.
        
        Args:
            organization_id: Organization ID
        """
        try:
            result = meraki_client.dashboard.organizations.getOrganization(organization_id)
            
            response = f"# 🏢 Organization Details\n\n"
            
            if result:
                response += f"## {result.get('name', 'Unnamed')}\n"
                response += f"- **ID**: {result.get('id')}\n"
                response += f"- **URL**: {result.get('url', 'N/A')}\n"
                
                # API settings
                api = result.get('api', {})
                if api:
                    response += f"\n### API Settings\n"
                    response += f"- **Enabled**: {api.get('enabled', False)}\n"
                    
                # Cloud region
                cloud = result.get('cloud', {})
                if cloud:
                    region = cloud.get('region', {})
                    response += f"\n### Cloud Region\n"
                    response += f"- **Name**: {region.get('name', 'N/A')}\n"
                    response += f"- **Host**: {cloud.get('host', {}).get('name', 'N/A')}\n"
                
                # Management
                mgmt = result.get('management', {})
                if mgmt:
                    response += f"\n### Management\n"
                    details = mgmt.get('details', [])
                    for detail in details:
                        response += f"- {detail.get('name', 'N/A')}: {detail.get('value', 'N/A')}\n"
                
                # Licensing
                licensing = result.get('licensing', {})
                if licensing:
                    response += f"\n### Licensing\n"
                    response += f"- **Model**: {licensing.get('model', 'N/A')}\n"
                    if licensing.get('expiration'):
                        response += f"- **Expiration**: {licensing.get('expiration')}\n"
            else:
                response += "*Organization not found*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting organization: {str(e)}"
    
    @app.tool(
        name="create_organization",
        description="➕ Create a new organization. Requires confirmation."
    )
    def create_organization(
        name: str,
        management_name: Optional[str] = None,
        management_value: Optional[str] = None,
        confirmed: bool = False
    ):
        """
        Create a new organization.
        
        Args:
            name: Organization name
            management_name: Management detail name
            management_value: Management detail value
            confirmed: Must be true to execute
        """
        if not confirmed:
            return "⚠️ Creating organization requires confirmed=true"
        
        try:
            kwargs = {"name": name}
            
            if management_name and management_value:
                kwargs["management"] = {
                    "details": [
                        {"name": management_name, "value": management_value}
                    ]
                }
            
            result = meraki_client.dashboard.organizations.createOrganization(**kwargs)
            
            org_id = result.get('id', 'Unknown')
            return f"✅ Created organization '{name}' with ID {org_id}"
        except Exception as e:
            return f"❌ Error creating organization: {str(e)}"
    
    @app.tool(
        name="update_organization",
        description="✏️ Update organization settings. Requires confirmation."
    )
    def update_organization(
        organization_id: str,
        name: Optional[str] = None,
        api_enabled: Optional[bool] = None,
        management_details: Optional[List[Dict[str, str]]] = None,
        confirmed: bool = False
    ):
        """
        Update organization.
        
        Args:
            organization_id: Organization ID
            name: New organization name
            api_enabled: Enable/disable API access
            management_details: Management details list
            confirmed: Must be true to execute
        """
        if not confirmed:
            return "⚠️ Updating organization requires confirmed=true"
        
        try:
            kwargs = {}
            
            if name is not None:
                kwargs["name"] = name
            if api_enabled is not None:
                kwargs["api"] = {"enabled": api_enabled}
            if management_details is not None:
                kwargs["management"] = {"details": management_details}
            
            result = meraki_client.dashboard.organizations.updateOrganization(
                organization_id, **kwargs
            )
            
            return f"✅ Updated organization {organization_id}"
        except Exception as e:
            return f"❌ Error updating organization: {str(e)}"
    
    @app.tool(
        name="delete_organization",
        description="🗑️ Delete an organization. Requires confirmation. EXTREMELY DANGEROUS!"
    )
    def delete_organization(
        organization_id: str,
        confirmed: bool = False
    ):
        """
        Delete an organization.
        
        Args:
            organization_id: Organization ID
            confirmed: Must be true to execute
        """
        if not confirmed:
            return "⚠️ DANGER! Deleting organization requires confirmed=true. This will DELETE EVERYTHING!"
        
        try:
            meraki_client.dashboard.organizations.deleteOrganization(organization_id)
            return f"✅ Deleted organization {organization_id}"
        except Exception as e:
            return f"❌ Error deleting organization: {str(e)}"
    
    # ==================== NETWORKS MANAGEMENT ====================
    
    @app.tool(
        name="get_organization_networks",
        description="🌐 List all networks in an organization."
    )
    def get_organization_networks(
        organization_id: str,
        config_template_id: Optional[str] = None,
        is_bound_to_config_template: Optional[bool] = None,
        tags: Optional[List[str]] = None,
        tags_filter_type: str = "withAnyTags",
        per_page: int = 100,
        starting_after: Optional[str] = None,
        ending_before: Optional[str] = None
    ):
        """
        List organization networks.
        
        Args:
            organization_id: Organization ID
            config_template_id: Filter by config template
            is_bound_to_config_template: Filter by template binding
            tags: Filter by tags
            tags_filter_type: "withAnyTags" or "withAllTags"
            per_page: Results per page (max 100000)
            starting_after: Start after this ID for pagination
            ending_before: End before this ID for pagination
        """
        try:
            kwargs = {"perPage": per_page}
            
            if config_template_id:
                kwargs["configTemplateId"] = config_template_id
            if is_bound_to_config_template is not None:
                kwargs["isBoundToConfigTemplate"] = is_bound_to_config_template
            if tags:
                kwargs["tags"] = tags
                kwargs["tagsFilterType"] = tags_filter_type
            if starting_after:
                kwargs["startingAfter"] = starting_after
            if ending_before:
                kwargs["endingBefore"] = ending_before
            
            result = meraki_client.dashboard.organizations.getOrganizationNetworks(
                organization_id, **kwargs
            )
            
            response = f"# 🌐 Organization Networks\n\n"
            response += f"**Organization**: {organization_id}\n\n"
            
            if result and isinstance(result, list):
                response += f"**Total Networks**: {len(result)}\n\n"
                
                # Group by product type
                by_type = {}
                for network in result:
                    product_types = network.get('productTypes', ['Unknown'])
                    for ptype in product_types:
                        if ptype not in by_type:
                            by_type[ptype] = []
                        by_type[ptype].append(network)
                
                for ptype in sorted(by_type.keys()):
                    response += f"## {ptype} Networks ({len(by_type[ptype])})\n"
                    
                    for network in by_type[ptype]:
                        response += f"### {network.get('name', 'Unnamed')}\n"
                        response += f"- **ID**: {network.get('id')}\n"
                        response += f"- **Time Zone**: {network.get('timeZone', 'N/A')}\n"
                        
                        if network.get('tags'):
                            response += f"- **Tags**: {', '.join(network['tags'])}\n"
                        
                        if network.get('notes'):
                            response += f"- **Notes**: {network['notes']}\n"
                        
                        if network.get('isBoundToConfigTemplate'):
                            response += f"- **Config Template**: Bound\n"
                        
                        response += "\n"
            else:
                response += "*No networks found*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting organization networks: {str(e)}"
    
    @app.tool(
        name="create_organization_network",
        description="➕ Create a new network in an organization. Requires confirmation."
    )
    def create_organization_network(
        organization_id: str,
        name: str,
        product_types: List[str],
        tags: Optional[List[str]] = None,
        time_zone: str = "America/Los_Angeles",
        notes: Optional[str] = None,
        copy_from_network_id: Optional[str] = None,
        confirmed: bool = False
    ):
        """
        Create a new network.
        
        Args:
            organization_id: Organization ID
            name: Network name
            product_types: List of product types (appliance, switch, wireless, etc.)
            tags: Network tags
            time_zone: Time zone
            notes: Network notes
            copy_from_network_id: Copy settings from this network
            confirmed: Must be true to execute
        """
        if not confirmed:
            return "⚠️ Creating network requires confirmed=true"
        
        try:
            kwargs = {
                "name": name,
                "productTypes": product_types,
                "timeZone": time_zone
            }
            
            if tags:
                kwargs["tags"] = tags
            if notes:
                kwargs["notes"] = notes
            if copy_from_network_id:
                kwargs["copyFromNetworkId"] = copy_from_network_id
            
            result = meraki_client.dashboard.organizations.createOrganizationNetwork(
                organization_id, **kwargs
            )
            
            network_id = result.get('id', 'Unknown')
            return f"✅ Created network '{name}' with ID {network_id}"
        except Exception as e:
            return f"❌ Error creating network: {str(e)}"
    
    @app.tool(
        name="combine_organization_networks",
        description="🔄 Combine multiple networks into one. Requires confirmation."
    )
    def combine_organization_networks(
        organization_id: str,
        name: str,
        network_ids: List[str],
        enrollment_string: Optional[str] = None,
        confirmed: bool = False
    ):
        """
        Combine multiple networks.
        
        Args:
            organization_id: Organization ID
            name: Name for combined network
            network_ids: List of network IDs to combine
            enrollment_string: Enrollment string for SM
            confirmed: Must be true to execute
        """
        if not confirmed:
            return "⚠️ Combining networks requires confirmed=true. This cannot be undone!"
        
        try:
            kwargs = {
                "name": name,
                "networkIds": network_ids
            }
            
            if enrollment_string:
                kwargs["enrollmentString"] = enrollment_string
            
            result = meraki_client.dashboard.organizations.combineOrganizationNetworks(
                organization_id, **kwargs
            )
            
            new_network_id = result.get('id', 'Unknown')
            return f"✅ Combined {len(network_ids)} networks into '{name}' (ID: {new_network_id})"
        except Exception as e:
            return f"❌ Error combining networks: {str(e)}"
    
    # ==================== INVENTORY MANAGEMENT ====================
    
    @app.tool(
        name="get_organization_inventory_devices",
        description="📦 List all devices in organization inventory."
    )
    def get_organization_inventory_devices(
        organization_id: str,
        per_page: int = 1000,
        starting_after: Optional[str] = None,
        ending_before: Optional[str] = None,
        used_state: Optional[str] = None,
        search: Optional[str] = None,
        macs: Optional[List[str]] = None,
        network_ids: Optional[List[str]] = None,
        serials: Optional[List[str]] = None,
        models: Optional[List[str]] = None,
        tags: Optional[List[str]] = None,
        tags_filter_type: str = "withAnyTags",
        product_types: Optional[List[str]] = None
    ):
        """
        List inventory devices.
        
        Args:
            organization_id: Organization ID
            per_page: Results per page
            starting_after: Pagination start
            ending_before: Pagination end
            used_state: "used" or "unused"
            search: Search for devices
            macs: Filter by MAC addresses
            network_ids: Filter by networks
            serials: Filter by serials
            models: Filter by models
            tags: Filter by tags
            tags_filter_type: Tag filter type
            product_types: Filter by product types
        """
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
            if macs:
                kwargs["macs"] = macs
            if network_ids:
                kwargs["networkIds"] = network_ids
            if serials:
                kwargs["serials"] = serials
            if models:
                kwargs["models"] = models
            if tags:
                kwargs["tags"] = tags
                kwargs["tagsFilterType"] = tags_filter_type
            if product_types:
                kwargs["productTypes"] = product_types
            
            result = meraki_client.dashboard.organizations.getOrganizationInventoryDevices(
                organization_id, **kwargs
            )
            
            response = f"# 📦 Organization Inventory\n\n"
            response += f"**Organization**: {organization_id}\n\n"
            
            if result and isinstance(result, list):
                response += f"**Total Devices**: {len(result)}\n\n"
                
                # Group by product type
                by_type = {}
                for device in result:
                    ptype = device.get('productType', 'Unknown')
                    if ptype not in by_type:
                        by_type[ptype] = []
                    by_type[ptype].append(device)
                
                for ptype in sorted(by_type.keys()):
                    response += f"## {ptype} Devices ({len(by_type[ptype])})\n"
                    
                    for device in by_type[ptype]:
                        response += f"### {device.get('name', device.get('serial', 'Unknown'))}\n"
                        response += f"- **Serial**: {device.get('serial')}\n"
                        response += f"- **Model**: {device.get('model', 'N/A')}\n"
                        response += f"- **MAC**: {device.get('mac', 'N/A')}\n"
                        
                        if device.get('networkId'):
                            response += f"- **Network ID**: {device['networkId']}\n"
                        else:
                            response += f"- **Status**: Unused\n"
                        
                        if device.get('tags'):
                            response += f"- **Tags**: {', '.join(device['tags'])}\n"
                        
                        if device.get('licenseExpirationDate'):
                            response += f"- **License Expires**: {device['licenseExpirationDate']}\n"
                        
                        response += "\n"
            else:
                response += "*No devices in inventory*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting inventory: {str(e)}"
    
    @app.tool(
        name="get_organization_inventory_device",
        description="📦 Get details of a specific device in inventory."
    )
    def get_organization_inventory_device(
        organization_id: str,
        serial: str
    ):
        """
        Get inventory device details.
        
        Args:
            organization_id: Organization ID
            serial: Device serial number
        """
        try:
            result = meraki_client.dashboard.organizations.getOrganizationInventoryDevice(
                organization_id, serial
            )
            
            response = f"# 📦 Device Details\n\n"
            
            if result:
                response += f"## {result.get('name', result.get('serial', 'Unknown'))}\n"
                response += f"- **Serial**: {result.get('serial')}\n"
                response += f"- **Model**: {result.get('model', 'N/A')}\n"
                response += f"- **MAC**: {result.get('mac', 'N/A')}\n"
                response += f"- **Product Type**: {result.get('productType', 'N/A')}\n"
                
                if result.get('networkId'):
                    response += f"- **Network ID**: {result['networkId']}\n"
                    response += f"- **Network Name**: {result.get('networkName', 'N/A')}\n"
                else:
                    response += f"- **Status**: Unused (not assigned to network)\n"
                
                if result.get('tags'):
                    response += f"- **Tags**: {', '.join(result['tags'])}\n"
                
                # Details
                details = result.get('details', [])
                if details:
                    response += f"\n### Details\n"
                    for detail in details:
                        response += f"- **{detail.get('name', 'N/A')}**: {detail.get('value', 'N/A')}\n"
                
                # License info
                if result.get('licenseExpirationDate'):
                    response += f"\n### Licensing\n"
                    response += f"- **Expires**: {result['licenseExpirationDate']}\n"
                
                # Order info
                if result.get('orderNumber'):
                    response += f"\n### Order Information\n"
                    response += f"- **Order Number**: {result['orderNumber']}\n"
                    response += f"- **Claimed At**: {result.get('claimedAt', 'N/A')}\n"
            else:
                response += "*Device not found in inventory*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting device: {str(e)}"
    
    @app.tool(
        name="claim_into_organization_inventory",
        description="➕ Claim devices into organization inventory. Requires confirmation."
    )
    def claim_into_organization_inventory(
        organization_id: str,
        orders: Optional[List[str]] = None,
        serials: Optional[List[str]] = None,
        licenses: Optional[List[Dict[str, Any]]] = None,
        confirmed: bool = False
    ):
        """
        Claim devices into inventory.
        
        Args:
            organization_id: Organization ID
            orders: List of order numbers
            serials: List of serial numbers
            licenses: List of license configurations
            confirmed: Must be true to execute
        """
        if not confirmed:
            return "⚠️ Claiming devices requires confirmed=true"
        
        try:
            kwargs = {}
            
            if orders:
                kwargs["orders"] = orders
            if serials:
                kwargs["serials"] = serials
            if licenses:
                kwargs["licenses"] = licenses
            
            result = meraki_client.dashboard.organizations.claimIntoOrganizationInventory(
                organization_id, **kwargs
            )
            
            claimed_count = len(result.get('serials', []))
            return f"✅ Claimed {claimed_count} devices into inventory"
        except Exception as e:
            return f"❌ Error claiming devices: {str(e)}"
    
    @app.tool(
        name="release_from_organization_inventory",
        description="🗑️ Release devices from organization inventory. Requires confirmation."
    )
    def release_from_organization_inventory(
        organization_id: str,
        serials: List[str],
        confirmed: bool = False
    ):
        """
        Release devices from inventory.
        
        Args:
            organization_id: Organization ID
            serials: List of serial numbers to release
            confirmed: Must be true to execute
        """
        if not confirmed:
            return "⚠️ Releasing devices requires confirmed=true. This removes them from the organization!"
        
        try:
            result = meraki_client.dashboard.organizations.releaseFromOrganizationInventory(
                organization_id, serials=serials
            )
            
            return f"✅ Released {len(serials)} devices from inventory"
        except Exception as e:
            return f"❌ Error releasing devices: {str(e)}"
    
    # ==================== ONBOARDING ====================
    
    @app.tool(
        name="get_org_inventory_onboarding_statuses",
        description="📊 Get cloud monitoring onboarding statuses for devices."
    )
    def get_org_inventory_onboarding_statuses(
        organization_id: str,
        device_type: str = "switch",
        per_page: int = 100,
        starting_after: Optional[str] = None,
        ending_before: Optional[str] = None,
        search: Optional[str] = None
    ):
        """
        Get device onboarding statuses.
        
        Args:
            organization_id: Organization ID
            device_type: Device type (switch or wireless_controller)
            per_page: Results per page (3-100000)
            starting_after: Pagination start
            ending_before: Pagination end
            search: Search on network name
        """
        try:
            kwargs = {"deviceType": device_type, "perPage": per_page}
            
            if starting_after:
                kwargs["startingAfter"] = starting_after
            if ending_before:
                kwargs["endingBefore"] = ending_before
            if search:
                kwargs["search"] = search
            
            result = meraki_client.dashboard.organizations.getOrganizationInventoryOnboardingCloudMonitoringNetworks(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Device Onboarding Statuses\n\n"
            response += f"**Organization**: {organization_id}\n\n"
            
            if result and isinstance(result, list):
                response += f"**Total Devices**: {len(result)}\n\n"
                
                # Group by status
                by_status = {}
                for device in result:
                    status = device.get('status', 'Unknown')
                    if status not in by_status:
                        by_status[status] = []
                    by_status[status].append(device)
                
                for status in sorted(by_status.keys()):
                    response += f"## {status} ({len(by_status[status])} devices)\n"
                    
                    for device in by_status[status]:
                        response += f"- **{device.get('name', device.get('serial'))}**"
                        response += f" ({device.get('productType', 'N/A')})\n"
                        
                        if device.get('lastSync'):
                            response += f"  - Last Sync: {device['lastSync']}\n"
                        
                        if device.get('message'):
                            response += f"  - Message: {device['message']}\n"
                    
                    response += "\n"
            else:
                response += "*No onboarding statuses found*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting onboarding statuses: {str(e)}"
    
    @app.tool(
        name="create_org_inv_onboarding_cloud_monitor_prepare",
        description="➕ Prepare devices for cloud monitoring import. Requires confirmation."
    )
    def create_org_inv_onboarding_cloud_monitor_prepare(
        organization_id: str,
        devices: List[Dict[str, Any]],
        confirmed: bool = False
    ):
        """
        Prepare devices for cloud monitoring.
        
        Args:
            organization_id: Organization ID
            devices: List of device configurations
            confirmed: Must be true to execute
        """
        if not confirmed:
            return "⚠️ Preparing cloud monitoring requires confirmed=true"
        
        try:
            result = meraki_client.dashboard.organizations.createOrganizationInventoryOnboardingCloudMonitoringPrepare(
                organization_id, devices=devices
            )
            
            return f"✅ Prepared {len(devices)} devices for cloud monitoring"
        except Exception as e:
            return f"❌ Error preparing devices: {str(e)}"
    
    @app.tool(
        name="create_org_inv_onboarding_cloud_monitor_export",
        description="➕ Create cloud monitoring export event. Requires confirmation."
    )
    def create_org_inv_onboarding_cloud_monitor_export(
        organization_id: str,
        confirmed: bool = False
    ):
        """
        Create cloud monitoring export event.
        
        Args:
            organization_id: Organization ID
            confirmed: Must be true to execute
        """
        if not confirmed:
            return "⚠️ Creating export event requires confirmed=true"
        
        try:
            result = meraki_client.dashboard.organizations.createOrganizationInventoryOnboardingCloudMonitoringExportEvent(
                organization_id
            )
            
            export_id = result.get('exportId', 'Unknown')
            return f"✅ Created export event with ID {export_id}"
        except Exception as e:
            return f"❌ Error creating export event: {str(e)}"
    
    # ==================== DEVICE AVAILABILITY ====================
    
    @app.tool(
        name="get_org_devices_availabilities_change_history",
        description="📊 Get device availability change history."
    )
    def get_org_devices_availabilities_change_history(
        organization_id: str,
        per_page: int = 1000,
        starting_after: Optional[str] = None,
        ending_before: Optional[str] = None,
        t0: Optional[str] = None,
        t1: Optional[str] = None,
        timespan: float = 86400,
        serials: Optional[List[str]] = None,
        product_types: Optional[List[str]] = None,
        network_ids: Optional[List[str]] = None
    ):
        """
        Get device availability change history.
        
        Args:
            organization_id: Organization ID
            per_page: Results per page
            starting_after: Pagination start
            ending_before: Pagination end
            t0: Start time (ISO 8601)
            t1: End time (ISO 8601)
            timespan: Timespan in seconds (default 24 hours)
            serials: Filter by serials
            product_types: Filter by product types
            network_ids: Filter by networks
        """
        try:
            kwargs = {
                "perPage": per_page,
                "timespan": timespan
            }
            
            if starting_after:
                kwargs["startingAfter"] = starting_after
            if ending_before:
                kwargs["endingBefore"] = ending_before
            if t0:
                kwargs["t0"] = t0
            if t1:
                kwargs["t1"] = t1
            if serials:
                kwargs["serials"] = serials
            if product_types:
                kwargs["productTypes"] = product_types
            if network_ids:
                kwargs["networkIds"] = network_ids
            
            result = meraki_client.dashboard.organizations.getOrganizationDevicesAvailabilitiesChangeHistory(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Device Availability Changes\n\n"
            response += f"**Organization**: {organization_id}\n"
            response += f"**Timespan**: {timespan} seconds\n\n"
            
            if result and isinstance(result, list):
                response += f"**Total Changes**: {len(result)}\n\n"
                
                for change in result[:20]:  # Show first 20
                    response += f"## {change.get('ts', 'Unknown time')}\n"
                    
                    device = change.get('device', {})
                    response += f"- **Device**: {device.get('name', device.get('serial', 'Unknown'))}\n"
                    response += f"- **Model**: {device.get('model', 'N/A')}\n"
                    response += f"- **Network**: {change.get('network', {}).get('name', 'N/A')}\n"
                    
                    details = change.get('details', {})
                    if details:
                        old_status = details.get('oldStatus', 'N/A')
                        new_status = details.get('newStatus', 'N/A')
                        response += f"- **Change**: {old_status} → {new_status}\n"
                    
                    response += "\n"
                
                if len(result) > 20:
                    response += f"*... and {len(result) - 20} more changes*\n"
            else:
                response += "*No availability changes found*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting availability history: {str(e)}"
    
    @app.tool(
        name="get_org_devices_statuses_overview",
        description="📊 Get overview of device statuses across the organization."
    )
    def get_org_devices_statuses_overview(
        organization_id: str,
        product_types: Optional[List[str]] = None,
        network_ids: Optional[List[str]] = None
    ):
        """
        Get device statuses overview.
        
        Args:
            organization_id: Organization ID
            product_types: Filter by product types
            network_ids: Filter by networks
        """
        try:
            kwargs = {}
            
            if product_types:
                kwargs["productTypes"] = product_types
            if network_ids:
                kwargs["networkIds"] = network_ids
            
            result = meraki_client.dashboard.organizations.getOrganizationDevicesStatusesOverview(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Device Statuses Overview\n\n"
            response += f"**Organization**: {organization_id}\n\n"
            
            if result:
                # Overall counts
                counts = result.get('counts', {})
                if counts:
                    response += f"## Overall Status\n"
                    response += f"- **Online**: {counts.get('online', 0)} devices\n"
                    response += f"- **Alerting**: {counts.get('alerting', 0)} devices\n"
                    response += f"- **Offline**: {counts.get('offline', 0)} devices\n"
                    response += f"- **Dormant**: {counts.get('dormant', 0)} devices\n"
                    
                    total = sum(counts.values())
                    response += f"- **Total**: {total} devices\n\n"
                
                # By product type
                by_product = result.get('productTypes', [])
                if by_product:
                    response += f"## By Product Type\n"
                    for product in by_product:
                        ptype = product.get('productType', 'Unknown')
                        counts = product.get('counts', {})
                        
                        response += f"### {ptype}\n"
                        response += f"- Online: {counts.get('online', 0)}\n"
                        response += f"- Alerting: {counts.get('alerting', 0)}\n"
                        response += f"- Offline: {counts.get('offline', 0)}\n"
                        response += f"- Dormant: {counts.get('dormant', 0)}\n"
                        response += "\n"
            else:
                response += "*No status data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting status overview: {str(e)}"