"""
Network management tools for the Cisco Meraki MCP Server - COMPLETE v1.61 IMPLEMENTATION.
"""

# Global variables to store app and meraki client
app = None
meraki_client = None

def register_network_tools(mcp_app, meraki):
    """
    Register network-related tools with the MCP server.
    
    Args:
        mcp_app: MCP server instance
        meraki: Meraki client instance
    """
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    
    # Register all network tools
    register_network_tool_handlers()

def register_network_tool_handlers():
    """Register all network-related tool handlers using the decorator pattern."""
    
    # Basic Network Operations
    @app.tool(
        name="get_network",
        description="🌐 Get details about a specific network"
    )
    def get_network(network_id: str):
        """Get details about a specific Meraki network."""
        try:
            network = meraki_client.dashboard.networks.getNetwork(network_id)
            
            result = f"# 🌐 Network Details\n\n"
            result += f"**Name**: {network.get('name', 'Unknown')}\n"
            result += f"**ID**: {network.get('id')}\n"
            result += f"**Organization ID**: {network.get('organizationId')}\n"
            result += f"**Time Zone**: {network.get('timeZone', 'Not set')}\n"
            result += f"**Product Types**: {', '.join(network.get('productTypes', []))}\n"
            
            if network.get('tags'):
                result += f"**Tags**: {', '.join(network['tags'])}\n"
            
            if network.get('notes'):
                result += f"**Notes**: {network['notes']}\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving network details: {str(e)}"
    
    @app.tool(
        name="update_network",
        description="🔧 Update network settings"
    )
    def update_network(network_id: str, **kwargs):
        """Update a Meraki network."""
        try:
            result = meraki_client.dashboard.networks.updateNetwork(network_id, **kwargs)
            return f"✅ Network updated successfully!\n\nUpdated settings applied."
            
        except Exception as e:
            return f"Error updating network: {str(e)}"
    
    @app.tool(
        name="delete_network",
        description="🗑️ Delete a network (CAUTION!)"
    )
    def delete_network(network_id: str):
        """Delete a Meraki network."""
        try:
            meraki_client.dashboard.networks.deleteNetwork(network_id)
            return f"✅ Network {network_id} deleted successfully!"
            
        except Exception as e:
            return f"Error deleting network: {str(e)}"
    
    @app.tool(
        name="bind_network",
        description="🔗 Bind a network to a template"
    )
    def bind_network(network_id: str, configTemplateId: str, **kwargs):
        """Bind a network to a configuration template."""
        try:
            meraki_client.dashboard.networks.bindNetwork(network_id, configTemplateId, **kwargs)
            return f"✅ Network bound to template {configTemplateId} successfully!"
            
        except Exception as e:
            return f"Error binding network to template: {str(e)}"
    
    @app.tool(
        name="unbind_network",
        description="🔓 Unbind a network from template"
    )
    def unbind_network(network_id: str, **kwargs):
        """Unbind a network from its configuration template."""
        try:
            meraki_client.dashboard.networks.unbindNetwork(network_id, **kwargs)
            return f"✅ Network unbound from template successfully!"
            
        except Exception as e:
            return f"Error unbinding network: {str(e)}"
    
    @app.tool(
        name="split_network",
        description="✂️ Split a combined network"
    )
    def split_network(network_id: str):
        """Split a combined network into individual networks."""
        try:
            result = meraki_client.dashboard.networks.splitNetwork(network_id)
            
            networks = result.get('resulting_networks', [])
            response = f"✅ Network split successfully!\n\n"
            response += f"**Created {len(networks)} networks**:\n\n"
            
            for net in networks:
                response += f"- {net.get('name')} (ID: {net.get('id')})\n"
            
            return response
            
        except Exception as e:
            return f"Error splitting network: {str(e)}"
    
    @app.tool(
        name="combine_organization_networks",
        description="🔀 Combine multiple networks"
    )
    def combine_organization_networks(organizationId: str, name: str, networkIds: list, **kwargs):
        """Combine multiple networks into a single network."""
        try:
            result = meraki_client.dashboard.networks.combineOrganizationNetworks(
                organizationId, name, networkIds, **kwargs
            )
            
            return f"✅ Networks combined successfully!\n\nNew network: {result.get('name')} (ID: {result.get('id')})"
            
        except Exception as e:
            return f"Error combining networks: {str(e)}"
    
    # Device Management
    @app.tool(
        name="get_network_devices",
        description="📟 List all devices in a network"
    )
    def get_network_devices(network_id: str):
        """List all devices in a network."""
        try:
            devices = meraki_client.dashboard.networks.getNetworkDevices(network_id)
            
            if not devices:
                return f"No devices found in network {network_id}."
            
            result = f"# 📟 Network Devices\n\n"
            result += f"**Total Devices**: {len(devices)}\n\n"
            
            # Group by model
            by_model = {}
            for device in devices:
                model = device.get('model', 'Unknown')
                if model not in by_model:
                    by_model[model] = []
                by_model[model].append(device)
            
            for model, devices_list in sorted(by_model.items()):
                result += f"## {model} ({len(devices_list)} devices)\n\n"
                
                for device in devices_list:
                    result += f"### {device.get('name', 'Unnamed')}\n"
                    result += f"- Serial: `{device.get('serial')}`\n"
                    result += f"- MAC: `{device.get('mac')}`\n"
                    # Status may not be available from this API
                    status = device.get('status')
                    if status:
                        result += f"- Status: {status}\n"
                    else:
                        result += f"- Status: Not reported (check device statuses API)\n"
                    
                    if device.get('address'):
                        result += f"- Address: {device['address']}\n"
                    
                    if device.get('firmware'):
                        result += f"- Firmware: {device['firmware']}\n"
                    
                    result += "\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving devices: {str(e)}"
    
    @app.tool(
        name="claim_network_devices",
        description="📲 Claim devices into a network"
    )
    def claim_network_devices(network_id: str, serials: list):
        """Claim devices into a network."""
        try:
            meraki_client.dashboard.networks.claimNetworkDevices(network_id, serials)
            return f"✅ Successfully claimed {len(serials)} device(s) into the network!"
            
        except Exception as e:
            return f"Error claiming devices: {str(e)}"
    
    @app.tool(
        name="remove_network_devices",
        description="📤 Remove devices from a network"
    )
    def remove_network_devices(network_id: str, serial: str):
        """Remove a device from a network."""
        try:
            meraki_client.dashboard.networks.removeNetworkDevices(network_id, serial)
            return f"✅ Device {serial} removed from network successfully!"
            
        except Exception as e:
            return f"Error removing device: {str(e)}"
    
    # Client Management
    @app.tool(
        name="get_network_clients",
        description="👥 List clients in a network"
    )
    def get_network_clients(network_id: str, **kwargs):
        """List clients in a network."""
        try:
            # Ensure maximum pagination - Meraki API max is 1000 per page
            if 'perPage' not in kwargs:
                kwargs['perPage'] = 1000  # Maximum allowed by Meraki API
            if 'total_pages' not in kwargs:
                kwargs['total_pages'] = 'all'  # Get all pages
            
            clients = meraki_client.dashboard.networks.getNetworkClients(network_id, **kwargs)
            
            if not clients:
                return f"No clients found in network {network_id}."
            
            result = f"# 👥 Network Clients\n\n"
            result += f"**Total Clients**: {len(clients)}\n\n"
            
            # Group by connection type
            wired = []
            wireless = []
            
            for client in clients:
                if client.get('ssid'):
                    wireless.append(client)
                else:
                    wired.append(client)
            
            if wireless:
                result += f"## 📶 Wireless Clients ({len(wireless)})\n\n"
                for client in wireless[:10]:
                    result += f"- **{client.get('description', 'Unknown')}**\n"
                    result += f"  - MAC: {client.get('mac')}\n"
                    result += f"  - IP: {client.get('ip', 'No IP')}\n"
                    result += f"  - SSID: {client.get('ssid')}\n"
                    result += f"  - Status: {client.get('status')}\n\n"
            
            if wired:
                result += f"## 🔌 Wired Clients ({len(wired)})\n\n"
                for client in wired[:10]:
                    result += f"- **{client.get('description', 'Unknown')}**\n"
                    result += f"  - MAC: {client.get('mac')}\n"
                    result += f"  - IP: {client.get('ip', 'No IP')}\n"
                    result += f"  - VLAN: {client.get('vlan', 'Unknown')}\n"
                    result += f"  - Switch Port: {client.get('switchport', 'Unknown')}\n\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving clients: {str(e)}"
    
    @app.tool(
        name="get_network_client",
        description="👤 Get details for a specific client"
    )
    def get_network_client(network_id: str, clientId: str):
        """Get details for a specific client."""
        try:
            client = meraki_client.dashboard.networks.getNetworkClient(network_id, clientId)
            
            result = f"# 👤 Client Details\n\n"
            result += f"**Description**: {client.get('description', 'Unknown')}\n"
            result += f"**MAC**: {client.get('mac')}\n"
            result += f"**IP**: {client.get('ip', 'No IP')}\n"
            result += f"**IPv6**: {client.get('ip6', 'No IPv6')}\n"
            result += f"**Status**: {client.get('status')}\n"
            
            if client.get('user'):
                result += f"**User**: {client['user']}\n"
            
            if client.get('manufacturer'):
                result += f"**Manufacturer**: {client['manufacturer']}\n"
            
            if client.get('os'):
                result += f"**OS**: {client['os']}\n"
            
            if client.get('ssid'):
                result += f"\n**Wireless Connection**:\n"
                result += f"- SSID: {client['ssid']}\n"
                result += f"- RSSI: {client.get('rssi')} dBm\n"
            
            if client.get('switchport'):
                result += f"\n**Wired Connection**:\n"
                result += f"- Switch Port: {client['switchport']}\n"
                result += f"- VLAN: {client.get('vlan')}\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving client details: {str(e)}"
    
    @app.tool(
        name="provision_network_clients",
        description="🔧 Provision clients with policies"
    )
    def provision_network_clients(network_id: str, clients: list, **kwargs):
        """Provision network clients with specific policies."""
        try:
            result = meraki_client.dashboard.networks.provisionNetworkClients(
                network_id, clients, **kwargs
            )
            
            return f"✅ Successfully provisioned {len(clients)} client(s)!"
            
        except Exception as e:
            return f"Error provisioning clients: {str(e)}"
    
    @app.tool(
        name="get_network_client_splash_authorization_status",
        description="🎫 Get splash authorization status"
    )
    def get_network_client_splash_authorization_status(network_id: str, clientId: str):
        """Get splash authorization status for a client."""
        try:
            status = meraki_client.dashboard.networks.getNetworkClientSplashAuthorizationStatus(
                network_id, clientId
            )
            
            result = f"# 🎫 Splash Authorization Status\n\n"
            result += f"**SSID**: {status.get('ssids', {})}\n"
            result += f"**Authorized**: {'✅' if status.get('isAuthorized') else '❌'}\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving splash status: {str(e)}"
    
    @app.tool(
        name="update_network_client_splash_authorization_status",
        description="🎫 Update splash authorization"
    )
    def update_network_client_splash_authorization_status(network_id: str, clientId: str, ssids: dict):
        """Update splash authorization status for a client."""
        try:
            result = meraki_client.dashboard.networks.updateNetworkClientSplashAuthorizationStatus(
                network_id, clientId, ssids
            )
            
            return f"✅ Splash authorization updated successfully!"
            
        except Exception as e:
            return f"Error updating splash authorization: {str(e)}"
    
    # Bluetooth Clients - MOVED TO tools_bluetooth_clients.py
    '''
    @app.tool(
        name="get_network_bluetooth_clients",
        description="📱 Get Bluetooth clients in network"
    )
    def get_network_bluetooth_clients(network_id: str, **kwargs):
        """Get Bluetooth clients seen by the network."""
        try:
            clients = meraki_client.dashboard.networks.getNetworkBluetoothClients(
                network_id, **kwargs
            )
            
            if not clients:
                return f"No Bluetooth clients found in network {network_id}."
            
            result = f"# 📱 Bluetooth Clients\n\n"
            result += f"**Total Clients**: {len(clients)}\n\n"
            
            for client in clients[:20]:
                result += f"- **{client.get('name', 'Unknown')}**\n"
                result += f"  - MAC: {client.get('mac')}\n"
                result += f"  - Manufacturer: {client.get('manufacturer', 'Unknown')}\n"
                result += f"  - Device Type: {client.get('deviceType', 'Unknown')}\n"
                result += f"  - Last Seen: {client.get('lastSeen')}\n\n"
            
            if len(clients) > 20:
                result += f"... and {len(clients) - 20} more clients\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving Bluetooth clients: {str(e)}"
    
    @app.tool(
        name="get_network_bluetooth_client",
        description="📱 Get details for a Bluetooth client"
    )
    def get_network_bluetooth_client(network_id: str, bluetoothClientId: str):
        """Get details for a specific Bluetooth client."""
        try:
            client = meraki_client.dashboard.networks.getNetworkBluetoothClient(
                network_id, bluetoothClientId
            )
            
            result = f"# 📱 Bluetooth Client Details\n\n"
            result += f"**Name**: {client.get('name', 'Unknown')}\n"
            result += f"**MAC**: {client.get('mac')}\n"
            result += f"**Manufacturer**: {client.get('manufacturer', 'Unknown')}\n"
            result += f"**Device Type**: {client.get('deviceType', 'Unknown')}\n"
            result += f"**Last Seen**: {client.get('lastSeen')}\n"
            
            if client.get('tags'):
                result += f"**Tags**: {', '.join(client['tags'])}\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving Bluetooth client: {str(e)}"
    '''
    
    # Events
    @app.tool(
        name="get_network_events",
        description="📅 Get network events"
    )
    def get_network_events(network_id: str, **kwargs):
        """Get events for the network."""
        try:
            # If no productType specified, try multiple product types
            if 'productType' not in kwargs:
                # Try each product type to gather all events
                product_types = ['appliance', 'wireless', 'switch', 'camera', 'cellularGateway']
                all_events = []
                successful_types = []
                
                for product_type in product_types:
                    try:
                        kwargs_copy = kwargs.copy()
                        kwargs_copy['productType'] = product_type
                        # Add default perPage if not specified
                        if 'perPage' not in kwargs_copy:
                            kwargs_copy['perPage'] = 100
                        
                        response = meraki_client.dashboard.networks.getNetworkEvents(network_id, **kwargs_copy)
                        
                        if response and response.get('events'):
                            events = response.get('events', [])
                            all_events.extend(events)
                            successful_types.append(product_type)
                    except:
                        # Some product types may not be available for this network
                        continue
                
                if not all_events:
                    # If no events found with any product type, try without productType
                    try:
                        if 'perPage' not in kwargs:
                            kwargs['perPage'] = 100
                        response = meraki_client.dashboard.networks.getNetworkEvents(network_id, **kwargs)
                        if response and response.get('events'):
                            all_events = response.get('events', [])
                    except:
                        pass
                
                if not all_events:
                    result = f"# 📅 Network Events\n\n"
                    result += f"No recent events found for network.\n\n"
                    result += f"**Searched product types**: {', '.join(product_types)}\n"
                    result += f"\n💡 **Tip**: Events may be filtered by time. Try specifying:\n"
                    result += f"- A specific productType (appliance, wireless, switch)\n"
                    result += f"- A specific device with deviceSerial parameter\n"
                    result += f"- Different time periods\n"
                    return result
                
                # Process combined events
                result = f"# 📅 Network Events\n\n"
                result += f"**Total Events Found**: {len(all_events)}\n"
                if successful_types:
                    result += f"**Product Types with Events**: {', '.join(successful_types)}\n\n"
                
                # Sort events by time (most recent first)
                all_events.sort(key=lambda x: x.get('occurredAt', ''), reverse=True)
                
                # Group by type
                by_type = {}
                for event in all_events:
                    event_type = event.get('type', 'Unknown')
                    if event_type not in by_type:
                        by_type[event_type] = []
                    by_type[event_type].append(event)
                
                for event_type, events in sorted(by_type.items()):
                    result += f"## {event_type} ({len(events)} events)\n\n"
                    
                    for event in events[:5]:  # Show first 5 of each type
                        result += f"- **{event.get('occurredAt')}**\n"
                        result += f"  - Description: {event.get('description', 'No description')}\n"
                        
                        if event.get('deviceName'):
                            result += f"  - Device: {event['deviceName']}\n"
                        if event.get('productType'):
                            result += f"  - Type: {event['productType']}\n"
                        
                        result += "\n"
                    
                    if len(events) > 5:
                        result += f"  ... and {len(events) - 5} more {event_type} events\n\n"
                
                return result
            
            else:
                # Use specified productType
                if 'perPage' not in kwargs:
                    kwargs['perPage'] = 100
                    
                events = meraki_client.dashboard.networks.getNetworkEvents(network_id, **kwargs)
                
                if not events or not events.get('events'):
                    return f"No events found for network {network_id} with productType: {kwargs.get('productType')}."
                
                result = f"# 📅 Network Events\n\n"
                
                event_list = events.get('events', [])
                result += f"**Total Events**: {len(event_list)}\n"
                result += f"**Product Type**: {kwargs.get('productType')}\n\n"
                
                # Group by type
                by_type = {}
                for event in event_list:
                    event_type = event.get('type', 'Unknown')
                    if event_type not in by_type:
                        by_type[event_type] = []
                    by_type[event_type].append(event)
                
                for event_type, events in sorted(by_type.items()):
                    result += f"## {event_type} ({len(events)} events)\n\n"
                    
                    for event in events[:5]:  # Show first 5 of each type
                        result += f"- **{event.get('occurredAt')}**\n"
                        result += f"  - Description: {event.get('description', 'No description')}\n"
                        
                        if event.get('deviceName'):
                            result += f"  - Device: {event['deviceName']}\n"
                        
                        result += "\n"
                    
                    if len(events) > 5:
                        result += f"  ... and {len(events) - 5} more {event_type} events\n\n"
                
                return result
            
        except Exception as e:
            return f"Error retrieving events: {str(e)}"
    
    @app.tool(
        name="get_network_events_event_types",
        description="📋 Get available event types"
    )
    def get_network_events_event_types(network_id: str):
        """Get the event types available for the network."""
        try:
            event_types = meraki_client.dashboard.networks.getNetworkEventsEventTypes(network_id)
            
            result = f"# 📋 Available Event Types\n\n"
            
            for event_type in event_types:
                result += f"- **{event_type.get('type')}**\n"
                result += f"  - Description: {event_type.get('description', 'No description')}\n\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving event types: {str(e)}"
    
    # Firmware Upgrades
    @app.tool(
        name="get_network_firmware_upgrades",
        description="💿 Get firmware upgrade information"
    )
    def get_network_firmware_upgrades(network_id: str):
        """Get firmware upgrade information for the network."""
        try:
            upgrades = meraki_client.dashboard.networks.getNetworkFirmwareUpgrades(network_id)
            
            result = f"# 💿 Firmware Upgrades\n\n"
            
            # Products
            products = upgrades.get('products', {})
            for product, info in products.items():
                result += f"## {product.upper()}\n"
                
                current = info.get('currentVersion')
                if current:
                    result += f"**Current Version**: {current.get('firmware', 'Unknown')}\n"
                    result += f"**Release Date**: {current.get('releaseDate', 'Unknown')}\n"
                
                next_scheduled = info.get('nextUpgrade')
                if next_scheduled:
                    result += f"\n**Next Scheduled Upgrade**:\n"
                    result += f"- Version: {next_scheduled.get('toVersion', {}).get('firmware', 'Unknown')}\n"
                    result += f"- Time: {next_scheduled.get('time', 'Not scheduled')}\n"
                
                available = info.get('availableVersions', [])
                if available:
                    result += f"\n**Available Versions**: {len(available)}\n"
                    for ver in available[:3]:  # Show first 3
                        result += f"- {ver.get('firmware')} ({ver.get('releaseType', 'Unknown')})\n"
                
                result += "\n"
            
            # Upgrade settings
            settings = upgrades.get('upgradeSettings', {})
            if settings:
                result += "## Upgrade Settings\n"
                result += f"**Upgrade Window**: {settings.get('upgradeWindow', {})}\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving firmware upgrades: {str(e)}"
    
    @app.tool(
        name="update_network_firmware_upgrades",
        description="💿 Schedule firmware upgrades"
    )
    def update_network_firmware_upgrades(network_id: str, **kwargs):
        """Update firmware upgrade settings for the network."""
        try:
            result = meraki_client.dashboard.networks.updateNetworkFirmwareUpgrades(
                network_id, **kwargs
            )
            
            return f"✅ Firmware upgrade settings updated successfully!"
            
        except Exception as e:
            return f"Error updating firmware upgrades: {str(e)}"
    
    @app.tool(
        name="create_network_firmware_upgrades_rollback",
        description="⏪ Rollback firmware upgrade"
    )
    def create_network_firmware_upgrades_rollback(network_id: str, product: str, **kwargs):
        """Rollback a firmware upgrade for a network."""
        try:
            result = meraki_client.dashboard.networks.createNetworkFirmwareUpgradesRollback(
                network_id, product, **kwargs
            )
            
            return f"✅ Firmware rollback initiated for {product}!"
            
        except Exception as e:
            return f"Error initiating rollback: {str(e)}"
    
    @app.tool(
        name="create_network_firmware_upgrades_staged_events",
        description="🎯 Create staged firmware upgrade"
    )
    def create_network_firmware_upgrades_staged_events(network_id: str, stages: list):
        """Create a staged firmware upgrade event."""
        try:
            result = meraki_client.dashboard.networks.createNetworkFirmwareUpgradesStagedEvents(
                network_id, stages
            )
            
            return f"✅ Staged firmware upgrade created successfully!"
            
        except Exception as e:
            return f"Error creating staged upgrade: {str(e)}"
    
    @app.tool(
        name="update_network_firmware_upgrades_staged_events",
        description="🎯 Update staged firmware upgrade"
    )
    def update_network_firmware_upgrades_staged_events(network_id: str, **kwargs):
        """Update staged firmware upgrade event."""
        try:
            result = meraki_client.dashboard.networks.updateNetworkFirmwareUpgradesStagedEvents(
                network_id, **kwargs
            )
            
            return f"✅ Staged firmware upgrade updated successfully!"
            
        except Exception as e:
            return f"Error updating staged upgrade: {str(e)}"
    
    @app.tool(
        name="defer_network_firmware_upgrades_staged_events",
        description="⏸️ Defer staged firmware upgrade"
    )
    def defer_network_firmware_upgrades_staged_events(network_id: str):
        """Defer a staged firmware upgrade event."""
        try:
            meraki_client.dashboard.networks.deferNetworkFirmwareUpgradesStagedEvents(network_id)
            
            return f"✅ Staged firmware upgrade deferred successfully!"
            
        except Exception as e:
            return f"Error deferring staged upgrade: {str(e)}"
    
    @app.tool(
        name="rollbacks_network_firmware_upgrades_staged_events",
        description="⏪ Rollback staged firmware upgrade"
    )
    def rollbacks_network_firmware_upgrades_staged_events(network_id: str, **kwargs):
        """Rollback a staged firmware upgrade."""
        try:
            result = meraki_client.dashboard.networks.rollbacksNetworkFirmwareUpgradesStagedEvents(
                network_id, **kwargs
            )
            
            return f"✅ Staged firmware upgrade rolled back successfully!"
            
        except Exception as e:
            return f"Error rolling back staged upgrade: {str(e)}"
    
    # Floor Plans - MOVED TO tools_floor_plans.py
    '''
    @app.tool(
        name="get_network_floor_plans",
        description="🏢 Get floor plans"
    )
    def get_network_floor_plans(network_id: str):
        """List floor plans for a network."""
        try:
            floor_plans = meraki_client.dashboard.networks.getNetworkFloorPlans(network_id)
            
            if not floor_plans:
                return f"No floor plans found for network {network_id}."
            
            result = f"# 🏢 Floor Plans\n\n"
            result += f"**Total Floor Plans**: {len(floor_plans)}\n\n"
            
            for plan in floor_plans:
                result += f"## {plan.get('name', 'Unnamed')}\n"
                result += f"- ID: {plan.get('floorPlanId')}\n"
                result += f"- Width: {plan.get('width')} ft\n"
                result += f"- Height: {plan.get('height')} ft\n"
                
                devices = plan.get('devices', [])
                if devices:
                    result += f"- Devices: {len(devices)}\n"
                
                result += "\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving floor plans: {str(e)}"
    
    @app.tool(
        name="create_network_floor_plan",
        description="🏢 Create a floor plan"
    )
    def create_network_floor_plan(network_id: str, name: str, **kwargs):
        """Create a floor plan."""
        try:
            result = meraki_client.dashboard.networks.createNetworkFloorPlan(
                network_id, name, **kwargs
            )
            
            return f"✅ Floor plan '{name}' created successfully!\n\nFloor Plan ID: {result.get('floorPlanId')}"
            
        except Exception as e:
            return f"Error creating floor plan: {str(e)}"
    
    @app.tool(
        name="get_network_floor_plan",
        description="🏢 Get floor plan details"
    )
    def get_network_floor_plan(network_id: str, floorPlanId: str):
        """Get details of a floor plan."""
        try:
            plan = meraki_client.dashboard.networks.getNetworkFloorPlan(network_id, floorPlanId)
            
            result = f"# 🏢 Floor Plan Details\n\n"
            result += f"**Name**: {plan.get('name')}\n"
            result += f"**ID**: {plan.get('floorPlanId')}\n"
            result += f"**Dimensions**: {plan.get('width')} x {plan.get('height')} ft\n"
            
            if plan.get('center'):
                center = plan['center']
                result += f"**Center**: ({center.get('lat')}, {center.get('lng')})\n"
            
            devices = plan.get('devices', [])
            if devices:
                result += f"\n**Devices on Floor Plan**: {len(devices)}\n"
                for device in devices[:10]:
                    result += f"- {device.get('name', 'Unknown')} ({device.get('serial')})\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving floor plan: {str(e)}"
    
    @app.tool(
        name="update_network_floor_plan",
        description="🏢 Update a floor plan"
    )
    def update_network_floor_plan(network_id: str, floorPlanId: str, **kwargs):
        """Update a floor plan."""
        try:
            result = meraki_client.dashboard.networks.updateNetworkFloorPlan(
                network_id, floorPlanId, **kwargs
            )
            
            return f"✅ Floor plan updated successfully!"
            
        except Exception as e:
            return f"Error updating floor plan: {str(e)}"
    
    @app.tool(
        name="delete_network_floor_plan",
        description="🏢 Delete a floor plan"
    )
    def delete_network_floor_plan(network_id: str, floorPlanId: str):
        """Delete a floor plan."""
        try:
            meraki_client.dashboard.networks.deleteNetworkFloorPlan(network_id, floorPlanId)
            
            return f"✅ Floor plan deleted successfully!"
            
        except Exception as e:
            return f"Error deleting floor plan: {str(e)}"
    '''
    
    # Group Policies - MOVED TO tools_group_policies.py
    '''
    @app.tool(
        name="get_network_group_policies",
        description="👥 Get group policies"
    )
    def get_network_group_policies(network_id: str):
        """List group policies for a network."""
        try:
            policies = meraki_client.dashboard.networks.getNetworkGroupPolicies(network_id)
            
            if not policies:
                return f"No group policies found for network {network_id}."
            
            result = f"# 👥 Group Policies\n\n"
            result += f"**Total Policies**: {len(policies)}\n\n"
            
            for policy in policies:
                result += f"## {policy.get('name', 'Unnamed')}\n"
                result += f"- ID: {policy.get('groupPolicyId')}\n"
                
                if policy.get('bandwidth'):
                    bw = policy['bandwidth']
                    result += f"- Bandwidth: {bw.get('bandwidthLimits', 'No limits')}\n"
                
                if policy.get('firewallAndTrafficShaping'):
                    fw = policy['firewallAndTrafficShaping']
                    if fw.get('l3FirewallRules'):
                        result += f"- L3 Firewall Rules: {len(fw['l3FirewallRules'])}\n"
                    if fw.get('l7FirewallRules'):
                        result += f"- L7 Firewall Rules: {len(fw['l7FirewallRules'])}\n"
                
                if policy.get('vlanTagging'):
                    vlan = policy['vlanTagging']
                    result += f"- VLAN: {vlan.get('vlanId', 'Not set')}\n"
                
                result += "\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving group policies: {str(e)}"
    
    @app.tool(
        name="create_network_group_policy",
        description="👥 Create a group policy"
    )
    def create_network_group_policy(network_id: str, name: str, **kwargs):
        """Create a group policy."""
        try:
            result = meraki_client.dashboard.networks.createNetworkGroupPolicy(
                network_id, name, **kwargs
            )
            
            return f"✅ Group policy '{name}' created successfully!\n\nPolicy ID: {result.get('groupPolicyId')}"
            
        except Exception as e:
            return f"Error creating group policy: {str(e)}"
    
    @app.tool(
        name="get_network_group_policy",
        description="👥 Get group policy details"
    )
    def get_network_group_policy(network_id: str, groupPolicyId: str):
        """Get details of a group policy."""
        try:
            policy = meraki_client.dashboard.networks.getNetworkGroupPolicy(
                network_id, groupPolicyId
            )
            
            result = f"# 👥 Group Policy Details\n\n"
            result += f"**Name**: {policy.get('name')}\n"
            result += f"**ID**: {policy.get('groupPolicyId')}\n"
            
            if policy.get('bandwidth'):
                result += "\n**Bandwidth Settings**:\n"
                bw = policy['bandwidth']
                settings = bw.get('settings')
                if settings == 'custom':
                    limits = bw.get('bandwidthLimits', {})
                    result += f"- Download: {limits.get('limitDown', 'Unlimited')} Mbps\n"
                    result += f"- Upload: {limits.get('limitUp', 'Unlimited')} Mbps\n"
                else:
                    result += f"- Settings: {settings}\n"
            
            if policy.get('vlanTagging'):
                vlan = policy['vlanTagging']
                result += f"\n**VLAN Settings**:\n"
                result += f"- VLAN ID: {vlan.get('vlanId', 'Not set')}\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving group policy: {str(e)}"
    
    @app.tool(
        name="update_network_group_policy",
        description="👥 Update a group policy"
    )
    def update_network_group_policy(network_id: str, groupPolicyId: str, **kwargs):
        """Update a group policy."""
        try:
            result = meraki_client.dashboard.networks.updateNetworkGroupPolicy(
                network_id, groupPolicyId, **kwargs
            )
            
            return f"✅ Group policy updated successfully!"
            
        except Exception as e:
            return f"Error updating group policy: {str(e)}"
    
    @app.tool(
        name="delete_network_group_policy",
        description="👥 Delete a group policy"
    )
    def delete_network_group_policy(network_id: str, groupPolicyId: str):
        """Delete a group policy."""
        try:
            meraki_client.dashboard.networks.deleteNetworkGroupPolicy(network_id, groupPolicyId)
            
            return f"✅ Group policy deleted successfully!"
            
        except Exception as e:
            return f"Error deleting group policy: {str(e)}"
    '''
    
    # Health
    @app.tool(
        name="get_network_health_channel_utilization",
        description="📊 Get channel utilization"
    )
    def get_network_health_channel_utilization(network_id: str, **kwargs):
        """Get channel utilization over time."""
        try:
            # Use the correct API endpoint from wireless module
            utilization = meraki_client.dashboard.wireless.getNetworkWirelessChannelUtilizationHistory(
                network_id, **kwargs
            )
            
            if not utilization:
                return f"No channel utilization data available for network {network_id}."
            
            result = f"# 📊 Channel Utilization\n\n"
            
            # Show last 10 entries for readability
            for data in utilization[-10:]:
                time = data.get('startTs', 'Unknown time')
                result += f"## {time[:16] if len(time) > 16 else time}\n"
                
                # WiFi utilization
                wifi = data.get('wifi', {})
                if wifi:
                    result += f"**WiFi Utilization**: {wifi.get('percentage', 0)}%\n"
                
                # Non-WiFi interference
                non_wifi = data.get('nonWifi', {})
                if non_wifi:
                    result += f"**Non-WiFi Interference**: {non_wifi.get('percentage', 0)}%\n"
                
                # Total utilization
                total = data.get('total', {})
                if total:
                    result += f"**Total Channel Utilization**: {total.get('percentage', 0)}%\n"
                
                result += "\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving channel utilization: {str(e)}"
    
    @app.tool(
        name="get_network_health_summary",
        description="🏥 Get network health summary"
    )
    def get_network_health_summary(network_id: str):
        """Get overall network health summary."""
        try:
            # Get various health metrics
            devices = meraki_client.dashboard.networks.getNetworkDevices(network_id)
            
            # Get organization ID to fetch device statuses
            org_id = None
            try:
                network = meraki_client.dashboard.networks.getNetwork(network_id)
                org_id = network.get('organizationId')
            except:
                pass
            
            # Get real device statuses from organization API
            device_statuses = {}
            if org_id:
                try:
                    statuses = meraki_client.dashboard.organizations.getOrganizationDevicesStatuses(
                        org_id,
                        networkIds=[network_id],
                        perPage=1000,
                        total_pages='all'
                    )
                    # Create lookup by serial - handle both dict and list responses
                    if isinstance(statuses, list):
                        for status in statuses:
                            if isinstance(status, dict):
                                serial = status.get('serial')
                                if serial:
                                    device_statuses[serial] = status.get('status', 'unknown')
                    elif isinstance(statuses, dict):
                        # Handle single device response
                        serial = statuses.get('serial')
                        if serial:
                            device_statuses[serial] = statuses.get('status', 'unknown')
                except:
                    pass
            
            # Count devices by status using real status data
            online = 0
            alerting = 0
            offline = 0
            dormant = 0
            no_status = 0
            
            for device in devices:
                serial = device.get('serial')
                status = None
                
                # First try to get status from organization API
                if serial and serial in device_statuses:
                    status = device_statuses[serial]
                else:
                    # Fallback to device's own status field if available
                    status = device.get('status')
                
                # Convert status to lowercase for consistent comparison
                if status:
                    status = status.lower()
                
                if status == 'online':
                    online += 1
                elif status == 'alerting':
                    alerting += 1
                elif status == 'offline':
                    offline += 1
                elif status == 'dormant':
                    dormant += 1
                else:
                    no_status += 1
            
            result = f"# 🏥 Network Health Summary\n\n"
            result += f"**Total Infrastructure Devices**: {len(devices)}\n"
            result += f"- 🟢 Online: {online}\n"
            result += f"- 🟡 Alerting: {alerting}\n"
            result += f"- 🔴 Offline: {offline}\n"
            if dormant > 0:
                result += f"- 😴 Dormant: {dormant} (not reporting to cloud but may be operational)\n"
            if no_status > 0:
                result += f"- ⚪ Status Not Reported: {no_status} (may be operating normally)\n"
            result += "\n"
            
            # Get client count - use overview API for accurate count
            try:
                # Try to get client overview first (more efficient)
                overview = meraki_client.dashboard.networks.getNetworkClientsOverview(network_id)
                client_count = overview.get('counts', {}).get('total', 0)
                result += f"**Connected Client Devices**: {client_count} active\n"
            except:
                # Fallback to getting actual client list with pagination
                try:
                    clients = meraki_client.dashboard.networks.getNetworkClients(
                        network_id, 
                        perPage=1000,  # Maximum pagination
                        total_pages='all'  # Get all pages for accurate count
                    )
                    result += f"**Connected Client Devices**: {len(clients)} active\n"
                except:
                    pass
            
            # Overall health score - base on devices with known status
            # Include dormant devices as "working" since they may be operational
            devices_with_status = online + alerting + offline + dormant
            if devices_with_status > 0:
                # Consider online and dormant as healthy (dormant devices often still pass traffic)
                healthy_devices = online + dormant
                health_percentage = (healthy_devices / devices_with_status) * 100
                if health_percentage >= 95:
                    result += f"\n**Overall Health**: 🟢 Excellent ({health_percentage:.1f}%)"
                elif health_percentage >= 80:
                    result += f"\n**Overall Health**: 🟡 Good ({health_percentage:.1f}%)"
                else:
                    result += f"\n**Overall Health**: 🔴 Poor ({health_percentage:.1f}%)"
                
                if dormant > 0:
                    result += f"\n*Note: {dormant} dormant device(s) included as operational*"
            elif no_status > 0:
                result += f"\n**Overall Health**: ⚪ Unknown - Unable to determine device status"
                result += f"\n*Devices may be operational but status unavailable*"
            
            return result
            
        except Exception as e:
            return f"Error retrieving health summary: {str(e)}"
    
    # MQTT Brokers
    # COMMENTED OUT - Moved to dedicated module (tools_mqtt.py, tools_snmp.py, or tools_syslog.py)
    #     @app.tool(
    #         name="get_network_mqtt_brokers",
    #         description="📡 Get MQTT brokers"
    #     )
    #     def get_network_mqtt_brokers(network_id: str):
    #         """List MQTT brokers for a network."""
    #         try:
    #             brokers = meraki_client.dashboard.networks.getNetworkMqttBrokers(network_id)
    #
    #             if not brokers:
    #                 return f"No MQTT brokers found for network {network_id}."
    #
    #             result = f"# 📡 MQTT Brokers\n\n"
    #             result += f"**Total Brokers**: {len(brokers)}\n\n"
    #
    #             for broker in brokers:
    #                 result += f"## {broker.get('name', 'Unnamed')}\n"
    #                 result += f"- ID: {broker.get('id')}\n"
    #                 result += f"- Host: {broker.get('host')}\n"
    #                 result += f"- Port: {broker.get('port', 1883)}\n"
    #
    #                 if broker.get('security'):
    #                     security = broker['security']
    #                     result += f"- Security: {security.get('mode', 'None')}\n"
    #
    #                 result += "\n"
    #
    #             return result
    #
    #         except Exception as e:
    #             return f"Error retrieving MQTT brokers: {str(e)}"
    #
    # COMMENTED OUT - Moved to dedicated module (tools_mqtt.py, tools_snmp.py, or tools_syslog.py)
    #     @app.tool(
    #         name="create_network_mqtt_broker",
    #         description="📡 Create MQTT broker"
    #     )
    #     def create_network_mqtt_broker(network_id: str, name: str, host: str, port: int, **kwargs):
    #         """Create an MQTT broker."""
    #         try:
    #             result = meraki_client.dashboard.networks.createNetworkMqttBroker(
    #                 network_id, name, host, port, **kwargs
    #             )
    #
    #             return f"✅ MQTT broker '{name}' created successfully!\n\nBroker ID: {result.get('id')}"
    #
    #         except Exception as e:
    #             return f"Error creating MQTT broker: {str(e)}"
    #
    #     # COMMENTED OUT - Moved to dedicated module (tools_mqtt.py, tools_snmp.py, or tools_syslog.py)
    #     #     @app.tool(
    #     #         name="get_network_mqtt_broker",
    #     #         description="📡 Get MQTT broker details"
    #     #     )
    #     #     def get_network_mqtt_broker(network_id: str, mqttBrokerId: str):
    #     #         """Get details of an MQTT broker."""
    #     #         try:
    #     #             broker = meraki_client.dashboard.networks.getNetworkMqttBroker(
    #     #                 network_id, mqttBrokerId
    #     #             )
    #     #
    #     #             result = f"# 📡 MQTT Broker Details\n\n"
    #     #             result += f"**Name**: {broker.get('name')}\n"
    #     #             result += f"**Host**: {broker.get('host')}\n"
    #     #             result += f"**Port**: {broker.get('port')}\n"
    #     #
    #     #             if broker.get('security'):
    #     #                 security = broker['security']
    #     #                 result += f"\n**Security**:\n"
    #     #                 result += f"- Mode: {security.get('mode', 'None')}\n"
    #     #
    #     #                 if security.get('tls'):
    #     #                     result += f"- TLS: Enabled\n"
    #     #
    #     #             return result
    #     #
    #     #         except Exception as e:
    #     #             return f"Error retrieving MQTT broker: {str(e)}"
    #     #
    # COMMENTED OUT - Moved to dedicated module (tools_mqtt.py, tools_snmp.py, or tools_syslog.py)
    #     @app.tool(
    #         name="update_network_mqtt_broker",
    #         description="📡 Update MQTT broker"
    #     )
    #     def update_network_mqtt_broker(network_id: str, mqttBrokerId: str, **kwargs):
    #         """Update an MQTT broker."""
    #         try:
    #             result = meraki_client.dashboard.networks.updateNetworkMqttBroker(
    #                 network_id, mqttBrokerId, **kwargs
    #             )
    #
    #             return f"✅ MQTT broker updated successfully!"
    #
    #         except Exception as e:
    #             return f"Error updating MQTT broker: {str(e)}"
    #
    # COMMENTED OUT - Moved to dedicated module (tools_mqtt.py, tools_snmp.py, or tools_syslog.py)
    #     @app.tool(
    #         name="delete_network_mqtt_broker",
    #         description="📡 Delete MQTT broker"
    #     )
    #     def delete_network_mqtt_broker(network_id: str, mqttBrokerId: str):
    #         """Delete an MQTT broker."""
    #         try:
    #             meraki_client.dashboard.networks.deleteNetworkMqttBroker(
    #                 network_id, mqttBrokerId
    #             )
    #
    #             return f"✅ MQTT broker deleted successfully!"
    #
    #         except Exception as e:
    #             return f"Error deleting MQTT broker: {str(e)}"
    #
    #     # Policies by Client
    @app.tool(
        name="get_network_policies_by_client",
        description="📋 Get policies by client"
    )
    def get_network_policies_by_client(network_id: str, **kwargs):
        """Get policies for all clients in a network."""
        try:
            policies = meraki_client.dashboard.networks.getNetworkPoliciesByClient(
                network_id, **kwargs
            )
            
            if not policies:
                return f"No client policies found for network {network_id}."
            
            result = f"# 📋 Policies by Client\n\n"
            
            for client in policies[:20]:
                result += f"## {client.get('name', client.get('mac', 'Unknown'))}\n"
                result += f"- Client ID: {client.get('clientId')}\n"
                
                assigned = client.get('assigned', [])
                if assigned:
                    result += f"- Assigned Policies: {len(assigned)}\n"
                    for policy in assigned:
                        result += f"  - {policy.get('name')} ({policy.get('type')})\n"
                
                result += "\n"
            
            if len(policies) > 20:
                result += f"... and {len(policies) - 20} more clients\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving client policies: {str(e)}"
    
    # Settings
    @app.tool(
        name="get_network_settings",
        description="⚙️ Get network settings"
    )
    def get_network_settings(network_id: str):
        """Get general network settings."""
        try:
            settings = meraki_client.dashboard.networks.getNetworkSettings(network_id)
            
            result = f"# ⚙️ Network Settings\n\n"
            
            if settings.get('localStatusPageEnabled') is not None:
                result += f"**Local Status Page**: {'✅ Enabled' if settings['localStatusPageEnabled'] else '❌ Disabled'}\n"
            
            if settings.get('remoteStatusPageEnabled') is not None:
                result += f"**Remote Status Page**: {'✅ Enabled' if settings['remoteStatusPageEnabled'] else '❌ Disabled'}\n"
            
            if settings.get('localStatusPage'):
                auth = settings['localStatusPage'].get('authentication', {})
                result += f"\n**Local Status Page Auth**:\n"
                result += f"- Enabled: {'✅' if auth.get('enabled') else '❌'}\n"
                if auth.get('username'):
                    result += f"- Username: {auth['username']}\n"
            
            if settings.get('secureConnect'):
                sc = settings['secureConnect']
                result += f"\n**Secure Connect**:\n"
                result += f"- Enabled: {'✅' if sc.get('enabled') else '❌'}\n"
            
            if settings.get('namingFormat'):
                result += f"\n**Client Naming Format**: {settings['namingFormat']}\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving network settings: {str(e)}"
    
    @app.tool(
        name="update_network_settings",
        description="⚙️ Update network settings"
    )
    def update_network_settings(network_id: str, **kwargs):
        """Update general network settings."""
        try:
            result = meraki_client.dashboard.networks.updateNetworkSettings(
                network_id, **kwargs
            )
            
            return f"✅ Network settings updated successfully!"
            
        except Exception as e:
            return f"Error updating network settings: {str(e)}"
    
    # SNMP
    # COMMENTED OUT - Moved to dedicated module (tools_mqtt.py, tools_snmp.py, or tools_syslog.py)
    #     @app.tool(
    #         name="get_network_snmp",
    #         description="📊 Get SNMP settings"
    #     )
    #     def get_network_snmp(network_id: str):
    #         """Get SNMP settings for a network."""
    #         try:
    #             snmp = meraki_client.dashboard.networks.getNetworkSnmp(network_id)
    #
    #             result = f"# 📊 SNMP Settings\n\n"
    #             result += f"**Access**: {snmp.get('access', 'None')}\n"
    #
    #             if snmp.get('communityString'):
    #                 result += f"**Community String**: {'Set' if snmp['communityString'] else 'Not set'}\n"
    #
    #             users = snmp.get('users', [])
    #             if users:
    #                 result += f"\n**SNMP v3 Users**: {len(users)}\n"
    #                 for user in users:
    #                     result += f"- {user.get('username')} ({user.get('authLevel', 'Unknown')})\n"
    #
    #             return result
    #
    #         except Exception as e:
    #             return f"Error retrieving SNMP settings: {str(e)}"
    #
    # COMMENTED OUT - Moved to dedicated module (tools_mqtt.py, tools_snmp.py, or tools_syslog.py)
    #     @app.tool(
    #         name="update_network_snmp",
    #         description="📊 Update SNMP settings"
    #     )
    #     def update_network_snmp(network_id: str, **kwargs):
    #         """Update SNMP settings for a network."""
    #         try:
    #             result = meraki_client.dashboard.networks.updateNetworkSnmp(
    #                 network_id, **kwargs
    #             )
    #
    #             return f"✅ SNMP settings updated successfully!"
    #
    #         except Exception as e:
    #             return f"Error updating SNMP settings: {str(e)}"
    #
    #     # Syslog Servers
    # COMMENTED OUT - Moved to dedicated module (tools_mqtt.py, tools_snmp.py, or tools_syslog.py)
    #     @app.tool(
    #         name="get_network_syslog_servers",
    #         description="📝 Get syslog servers"
    #     )
    #     def get_network_syslog_servers(network_id: str):
    #         """List syslog servers for a network."""
    #         try:
    #             servers = meraki_client.dashboard.networks.getNetworkSyslogServers(network_id)
    #
    #             result = f"# 📝 Syslog Servers\n\n"
    #
    #             server_list = servers.get('servers', [])
    #             if not server_list:
    #                 return result + "No syslog servers configured."
    #
    #             result += f"**Total Servers**: {len(server_list)}\n\n"
    #
    #             for server in server_list:
    #                 result += f"- **{server.get('host')}**\n"
    #                 result += f"  - Port: {server.get('port', 514)}\n"
    #
    #                 roles = server.get('roles', [])
    #                 if roles:
    #                     result += f"  - Roles: {', '.join(roles)}\n"
    #
    #                 result += "\n"
    #
    #             return result
    #
    #         except Exception as e:
    #             return f"Error retrieving syslog servers: {str(e)}"
    #
    # COMMENTED OUT - Moved to dedicated module (tools_mqtt.py, tools_snmp.py, or tools_syslog.py)
    #     @app.tool(
    #         name="update_network_syslog_servers",
    #         description="📝 Update syslog servers"
    #     )
    #     def update_network_syslog_servers(network_id: str, servers: list):
    #         """Update syslog servers for a network."""
    #         try:
    #             result = meraki_client.dashboard.networks.updateNetworkSyslogServers(
    #                 network_id, servers
    #             )
    #
    #             return f"✅ Syslog servers updated successfully!"
    #
    #         except Exception as e:
    #             return f"Error updating syslog servers: {str(e)}"
    #
    #     # Traffic Shaping
    @app.tool(
        name="get_network_traffic_shaping_application_categories",
        description="🚦 Get application categories"
    )
    def get_network_traffic_shaping_application_categories(network_id: str):
        """Get traffic shaping application categories."""
        try:
            categories = meraki_client.dashboard.networks.getNetworkTrafficShapingApplicationCategories(network_id)
            
            result = f"# 🚦 Application Categories\n\n"
            
            app_categories = categories.get('applicationCategories', [])
            result += f"**Total Categories**: {len(app_categories)}\n\n"
            
            for category in app_categories[:20]:
                result += f"- **{category.get('name')}**\n"
                result += f"  - ID: {category.get('id')}\n"
                
                apps = category.get('applications', [])
                if apps:
                    result += f"  - Applications: {len(apps)}\n"
                
                result += "\n"
            
            if len(app_categories) > 20:
                result += f"... and {len(app_categories) - 20} more categories\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving application categories: {str(e)}"
    
    @app.tool(
        name="get_network_traffic_shaping_dscp_tagging_options",
        description="🏷️ Get DSCP tagging options"
    )
    def get_network_traffic_shaping_dscp_tagging_options(network_id: str):
        """Get DSCP tagging options for traffic shaping."""
        try:
            options = meraki_client.dashboard.networks.getNetworkTrafficShapingDscpTaggingOptions(network_id)
            
            result = f"# 🏷️ DSCP Tagging Options\n\n"
            
            for option in options:
                result += f"- **{option.get('description')}**\n"
                result += f"  - DSCP Value: {option.get('dscpValue')}\n\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving DSCP tagging options: {str(e)}"
    
    # Webhooks
    @app.tool(
        name="get_network_webhooks_http_servers",
        description="🪝 Get webhook HTTP servers"
    )
    def get_network_webhooks_http_servers(network_id: str):
        """List webhook HTTP servers for a network."""
        try:
            servers = meraki_client.dashboard.networks.getNetworkWebhooksHttpServers(network_id)
            
            if not servers:
                return f"No webhook servers found for network {network_id}."
            
            result = f"# 🪝 Webhook HTTP Servers\n\n"
            result += f"**Total Servers**: {len(servers)}\n\n"
            
            for server in servers:
                result += f"## {server.get('name', 'Unnamed')}\n"
                result += f"- ID: {server.get('id')}\n"
                result += f"- URL: {server.get('url')}\n"
                result += f"- Shared Secret: {'Set' if server.get('sharedSecret') else 'Not set'}\n"
                
                payload = server.get('payloadTemplate')
                if payload:
                    result += f"- Payload Template: {payload.get('name', 'Default')}\n"
                
                result += "\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving webhook servers: {str(e)}"
    
    @app.tool(
        name="create_network_webhooks_http_server",
        description="🪝 Create webhook HTTP server"
    )
    def create_network_webhooks_http_server(network_id: str, name: str, url: str, **kwargs):
        """Create a webhook HTTP server."""
        try:
            result = meraki_client.dashboard.networks.createNetworkWebhooksHttpServer(
                network_id, name, url, **kwargs
            )
            
            return f"✅ Webhook server '{name}' created successfully!\n\nServer ID: {result.get('id')}"
            
        except Exception as e:
            return f"Error creating webhook server: {str(e)}"
    
    @app.tool(
        name="get_network_webhooks_http_server",
        description="🪝 Get webhook server details"
    )
    def get_network_webhooks_http_server(network_id: str, httpServerId: str):
        """Get details of a webhook HTTP server."""
        try:
            server = meraki_client.dashboard.networks.getNetworkWebhooksHttpServer(
                network_id, httpServerId
            )
            
            result = f"# 🪝 Webhook Server Details\n\n"
            result += f"**Name**: {server.get('name')}\n"
            result += f"**URL**: {server.get('url')}\n"
            result += f"**ID**: {server.get('id')}\n"
            
            if server.get('payloadTemplate'):
                template = server['payloadTemplate']
                result += f"\n**Payload Template**:\n"
                result += f"- Name: {template.get('name')}\n"
                if template.get('body'):
                    result += f"- Custom Body: Yes\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving webhook server: {str(e)}"
    
    @app.tool(
        name="update_network_webhooks_http_server",
        description="🪝 Update webhook HTTP server"
    )
    def update_network_webhooks_http_server(network_id: str, httpServerId: str, **kwargs):
        """Update a webhook HTTP server."""
        try:
            result = meraki_client.dashboard.networks.updateNetworkWebhooksHttpServer(
                network_id, httpServerId, **kwargs
            )
            
            return f"✅ Webhook server updated successfully!"
            
        except Exception as e:
            return f"Error updating webhook server: {str(e)}"
    
    @app.tool(
        name="delete_network_webhooks_http_server",
        description="🪝 Delete webhook HTTP server"
    )
    def delete_network_webhooks_http_server(network_id: str, httpServerId: str):
        """Delete a webhook HTTP server."""
        try:
            meraki_client.dashboard.networks.deleteNetworkWebhooksHttpServer(
                network_id, httpServerId
            )
            
            return f"✅ Webhook server deleted successfully!"
            
        except Exception as e:
            return f"Error deleting webhook server: {str(e)}"
    
    @app.tool(
        name="create_network_webhooks_webhook_test",
        description="🪝 Test a webhook"
    )
    def create_network_webhooks_webhook_test(network_id: str, url: str, **kwargs):
        """Test a webhook by sending a test webhook."""
        try:
            result = meraki_client.dashboard.networks.createNetworkWebhooksWebhookTest(
                network_id, url, **kwargs
            )
            
            return f"✅ Webhook test sent successfully!\n\nTest ID: {result.get('id')}"
            
        except Exception as e:
            return f"Error testing webhook: {str(e)}"
    
    @app.tool(
        name="get_network_webhooks_webhook_test",
        description="🪝 Get webhook test status"
    )
    def get_network_webhooks_webhook_test(network_id: str, webhookTestId: str):
        """Get the status of a webhook test."""
        try:
            test = meraki_client.dashboard.networks.getNetworkWebhooksWebhookTest(
                network_id, webhookTestId
            )
            
            result = f"# 🪝 Webhook Test Status\n\n"
            result += f"**Test ID**: {test.get('id')}\n"
            result += f"**URL**: {test.get('url')}\n"
            result += f"**Status**: {test.get('status', 'Unknown')}\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving webhook test: {str(e)}"
    
    # Payload Templates
    @app.tool(
        name="get_network_webhooks_payload_templates",
        description="📄 Get webhook payload templates"
    )
    def get_network_webhooks_payload_templates(network_id: str):
        """List webhook payload templates."""
        try:
            templates = meraki_client.dashboard.networks.getNetworkWebhooksPayloadTemplates(network_id)
            
            if not templates:
                return f"No payload templates found for network {network_id}."
            
            result = f"# 📄 Webhook Payload Templates\n\n"
            result += f"**Total Templates**: {len(templates)}\n\n"
            
            for template in templates:
                result += f"## {template.get('name', 'Unnamed')}\n"
                result += f"- ID: {template.get('payloadTemplateId')}\n"
                result += f"- Type: {template.get('type', 'Unknown')}\n"
                
                if template.get('body'):
                    result += f"- Custom Body: Yes\n"
                
                result += "\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving payload templates: {str(e)}"
    
    @app.tool(
        name="create_network_webhooks_payload_template",
        description="📄 Create webhook payload template"
    )
    def create_network_webhooks_payload_template(network_id: str, name: str, **kwargs):
        """Create a webhook payload template."""
        try:
            result = meraki_client.dashboard.networks.createNetworkWebhooksPayloadTemplate(
                network_id, name, **kwargs
            )
            
            return f"✅ Payload template '{name}' created successfully!\n\nTemplate ID: {result.get('payloadTemplateId')}"
            
        except Exception as e:
            return f"Error creating payload template: {str(e)}"
    
    @app.tool(
        name="get_network_webhooks_payload_template",
        description="📄 Get payload template details"
    )
    def get_network_webhooks_payload_template(network_id: str, payloadTemplateId: str):
        """Get details of a webhook payload template."""
        try:
            template = meraki_client.dashboard.networks.getNetworkWebhooksPayloadTemplate(
                network_id, payloadTemplateId
            )
            
            result = f"# 📄 Payload Template Details\n\n"
            result += f"**Name**: {template.get('name')}\n"
            result += f"**ID**: {template.get('payloadTemplateId')}\n"
            result += f"**Type**: {template.get('type')}\n"
            
            if template.get('body'):
                result += f"\n**Custom Body**: Present\n"
            
            if template.get('headers'):
                result += f"\n**Custom Headers**: {len(template['headers'])}\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving payload template: {str(e)}"
    
    @app.tool(
        name="update_network_webhooks_payload_template",
        description="📄 Update webhook payload template"
    )
    def update_network_webhooks_payload_template(network_id: str, payloadTemplateId: str, **kwargs):
        """Update a webhook payload template."""
        try:
            result = meraki_client.dashboard.networks.updateNetworkWebhooksPayloadTemplate(
                network_id, payloadTemplateId, **kwargs
            )
            
            return f"✅ Payload template updated successfully!"
            
        except Exception as e:
            return f"Error updating payload template: {str(e)}"
    
    @app.tool(
        name="delete_network_webhooks_payload_template",
        description="📄 Delete webhook payload template"
    )
    def delete_network_webhooks_payload_template(network_id: str, payloadTemplateId: str):
        """Delete a webhook payload template."""
        try:
            meraki_client.dashboard.networks.deleteNetworkWebhooksPayloadTemplate(
                network_id, payloadTemplateId
            )
            
            return f"✅ Payload template deleted successfully!"
            
        except Exception as e:
            return f"Error deleting payload template: {str(e)}"
    
    # Topology
    @app.tool(
        name="get_network_topology_link_layer",
        description="🔗 Get link layer topology"
    )
    def get_network_topology_link_layer(network_id: str):
        """Get the link layer topology for a network."""
        try:
            topology = meraki_client.dashboard.networks.getNetworkTopologyLinkLayer(network_id)
            
            result = f"# 🔗 Link Layer Topology\n\n"
            
            nodes = topology.get('nodes', [])
            links = topology.get('links', [])
            
            result += f"**Nodes**: {len(nodes)}\n"
            result += f"**Links**: {len(links)}\n\n"
            
            if nodes:
                result += "## Network Devices\n\n"
                for node in nodes[:10]:
                    result += f"- **{node.get('name', 'Unknown')}**\n"
                    result += f"  - Type: {node.get('type')}\n"
                    result += f"  - Model: {node.get('model')}\n"
                    result += f"  - Serial: {node.get('serial')}\n\n"
            
            if links:
                result += "## Connections\n\n"
                for link in links[:10]:
                    result += f"- {link.get('lastReportedAt')}\n"
                    
                    ends = link.get('ends', [])
                    if len(ends) == 2:
                        result += f"  - From: {ends[0].get('node', {}).get('name', 'Unknown')} (Port {ends[0].get('port')})\n"
                        result += f"  - To: {ends[1].get('node', {}).get('name', 'Unknown')} (Port {ends[1].get('port')})\n"
                    
                    result += "\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving topology: {str(e)}"
    
    # VLANs
    @app.tool(
        name="get_network_vlan_assignments_by_device",
        description="🏷️ Get VLAN assignments by device"
    )
    def get_network_vlan_assignments_by_device(network_id: str, **kwargs):
        """Get VLAN assignments for devices in a network."""
        try:
            assignments = meraki_client.dashboard.networks.getNetworkVlanAssignmentsByDevice(
                network_id, **kwargs
            )
            
            if not assignments:
                return f"No VLAN assignments found for network {network_id}."
            
            result = f"# 🏷️ VLAN Assignments by Device\n\n"
            
            for device in assignments:
                result += f"## {device.get('name', 'Unknown')} ({device.get('serial')})\n"
                
                vlans = device.get('vlanAssignments', [])
                if vlans:
                    for vlan in vlans:
                        result += f"- Port {vlan.get('port')}: VLAN {vlan.get('vlan')}\n"
                else:
                    result += "- No VLAN assignments\n"
                
                result += "\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving VLAN assignments: {str(e)}"
    
    # VPN Firewall Rules
    @app.tool(
        name="get_network_appliance_firewall_inbound_cellular_firewall_rules",
        description="📱 Get inbound cellular firewall rules"
    )
    def get_network_appliance_firewall_inbound_cellular_firewall_rules(network_id: str):
        """Get inbound cellular firewall rules."""
        try:
            rules = meraki_client.dashboard.networks.getNetworkApplianceFirewallInboundCellularFirewallRules(network_id)
            
            result = f"# 📱 Inbound Cellular Firewall Rules\n\n"
            
            rule_list = rules.get('rules', [])
            if not rule_list:
                return result + "No inbound cellular firewall rules configured."
            
            for idx, rule in enumerate(rule_list, 1):
                result += f"## Rule {idx}: {rule.get('comment', 'No comment')}\n"
                result += f"- Policy: {rule.get('policy')}\n"
                result += f"- Protocol: {rule.get('protocol')}\n"
                result += f"- Source: {rule.get('srcCidr')}\n"
                result += f"- Destination: {rule.get('destCidr')}\n"
                
                if rule.get('destPort'):
                    result += f"- Dest Port: {rule['destPort']}\n"
                
                result += "\n"
            
            return result
            
        except Exception as e:
            return f"Error retrieving cellular firewall rules: {str(e)}"
    
    @app.tool(
        name="update_network_cellular_firewall_inbound_rules",
        description="📱 Update inbound cellular firewall rules"
    )
    def update_network_appliance_firewall_inbound_cellular_firewall_rules(network_id: str, **kwargs):
        """Update inbound cellular firewall rules."""
        try:
            result = meraki_client.dashboard.networks.updateNetworkApplianceFirewallInboundCellularFirewallRules(
                network_id, **kwargs
            )
            
            return f"✅ Inbound cellular firewall rules updated successfully!"
            
        except Exception as e:
            return f"Error updating cellular firewall rules: {str(e)}"