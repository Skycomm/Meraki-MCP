#!/usr/bin/env python3
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
    
    @app.tool(
        name="get_network",
        description="Get details about a specific Meraki network"
    )
    def get_network(network_id: str):
        """
        Get details about a specific Meraki network.
        
        Args:
            network_id: ID of the network to retrieve
            
        Returns:
            Network details
        """
        return meraki_client.get_network(network_id)

    @app.tool(
        name="update_network",
        description="Update a Meraki network - name, tags, or timezone"
    )
    def update_network(network_id: str, name: str = None, tags: list = None, timezone: str = None):
        """
        Update a Meraki network.
        
        Args:
            network_id: ID of the network to update
            name: New name for the network (optional)
            tags: New tags for the network (optional)
            timezone: New timezone for the network (e.g., 'Australia/Perth', 'America/Los_Angeles') (optional)
            
        Returns:
            Updated network details
        """
        try:
            # Get current network details
            network = meraki_client.get_network(network_id)
            current_name = network.get('name', 'Unknown')
            
            # If renaming, require confirmation
            if name and name != current_name:
                from utils.helpers import require_confirmation
                
                if not require_confirmation(
                    operation_type="rename",
                    resource_type="network",
                    resource_name=f"{current_name} → {name}",
                    resource_id=network_id
                ):
                    return "❌ Network rename cancelled by user"
            
            # Perform update
            result = meraki_client.update_network(network_id, name, tags, timezone)
            
            # Build response message
            updates = []
            if name:
                updates.append(f"name: {name}")
            if tags:
                updates.append(f"tags: {tags}")
            if timezone:
                updates.append(f"timezone: {timezone}")
            
            return f"✅ Network updated successfully - {', '.join(updates)}"
            
        except Exception as e:
            return f"Failed to update network: {str(e)}"

    @app.tool(
        name="get_network_devices",
        description="List devices in a Meraki network"
    )
    def get_network_devices(network_id: str):
        """
        List devices in a Meraki network.
        
        Args:
            network_id: ID of the network
            
        Returns:
            Formatted list of devices
        """
        try:
            devices = meraki_client.get_network_devices(network_id)
            
            if not devices:
                return f"No devices found for network {network_id}."
                
            # Format the output for readability
            result = f"# Devices in Network ({network_id})\n\n"
            for device in devices:
                result += f"- **{device.get('name', 'Unnamed')}** (Model: {device.get('model', 'Unknown')})\n"
                result += f"  - Serial: `{device.get('serial', 'Unknown')}`\n"
                result += f"  - MAC: `{device.get('mac', 'Unknown')}`\n"
                result += f"  - Status: {device.get('status', 'Unknown')}\n"
                
                # Add location if available
                lat = device.get('lat')
                lng = device.get('lng')
                address = device.get('address')
                
                if lat and lng:
                    result += f"  - Location: ({lat}, {lng})\n"
                if address:
                    result += f"  - Address: {address}\n"
                
                result += "\n"
                
            return result
            
        except Exception as e:
            return f"Failed to list devices for network {network_id}: {str(e)}"

    @app.tool(
        name="get_network_clients",
        description="List clients in a Meraki network"
    )
    def get_network_clients(network_id: str):
        """
        List clients in a Meraki network.
        
        Args:
            network_id: ID of the network
            
        Returns:
            Formatted list of clients
        """
        try:
            clients = meraki_client.get_network_clients(network_id)
            
            if not clients:
                return f"No clients found for network {network_id}."
                
            # Format the output for readability
            result = f"# Clients in Network ({network_id})\n\n"
            for client in clients:
                result += f"- **{client.get('description', 'Unknown Device')}**\n"
                result += f"  - MAC: `{client.get('mac', 'Unknown')}`\n"
                result += f"  - IP: `{client.get('ip', 'Unknown')}`\n"
                result += f"  - VLAN: {client.get('vlan', 'Unknown')}\n"
                result += f"  - Connection: {client.get('status', 'Unknown')}\n"
                
                # Add usage if available
                usage = client.get('usage')
                if usage:
                    result += f"  - Usage: {usage.get('sent', 0)} sent, {usage.get('recv', 0)} received\n"
                
                result += "\n"
                
            return result
            
        except Exception as e:
            error_msg = str(e)
            if "400" in error_msg:
                return f"❌ Cannot get clients for network {network_id}. This network may not have wireless or may not track clients."
            elif "404" in error_msg:
                return f"❌ Network {network_id} not found."
            elif "403" in error_msg:
                return f"❌ Access denied to network {network_id}."
            else:
                return f"❌ Failed to list clients: {error_msg}"

    @app.tool(
        name="create_network",
        description="Create a new Meraki network in an organization"
    )
    def create_network(organization_id: str, name: str, product_types: str = "wireless"):
        """
        Create a new Meraki network in an organization.
        
        Args:
            organization_id: ID of the organization to create the network in
            name: Name for the new network
            product_types: Comma-separated product types (appliance,switch,wireless,camera,sensor)
            
        Returns:
            New network details
        """
        # Convert comma-separated string to list
        types_list = [t.strip() for t in product_types.split(',')]
        # BUGFIX: Pass productTypes as named parameter instead of positional
        return meraki_client.create_network(organization_id, name, productTypes=types_list)

    @app.tool(
        name="delete_network",
        description="Delete a Meraki network - REQUIRES CONFIRMATION"
    )
    def delete_network(network_id: str):
        """
        Delete a Meraki network.
        
        Args:
            network_id: ID of the network to delete
            
        Returns:
            Success/failure information
        """
        try:
            # Get network details first
            network = meraki_client.get_network(network_id)
            
            # Import helper functions
            from utils.helpers import require_confirmation, get_read_only_message
            
            # Check if in read-only mode first
            if os.getenv("MCP_READ_ONLY_MODE", "false").lower() == "true":
                return get_read_only_message(
                    operation_type="delete",
                    resource_type="network",
                    resource_name=network.get('name', 'Unknown'),
                    resource_id=network_id
                )
            
            # Require confirmation
            if not require_confirmation(
                operation_type="delete",
                resource_type="network", 
                resource_name=network.get('name', 'Unknown'),
                resource_id=network_id
            ):
                return "❌ Network deletion cancelled by user"
            
            # Perform deletion
            meraki_client.delete_network(network_id)
            return f"✅ Network '{network['name']}' deleted successfully"
            
        except Exception as e:
            return f"Failed to delete network: {str(e)}"

    @app.tool(
        name="get_network_alerts_history",
        description="🚨 Get historical alerts for a network"
    )
    def get_network_alerts_history(
        network_id: str,
        per_page: Optional[int] = 100,
        starting_after: Optional[str] = None,
        ending_before: Optional[str] = None
    ):
        """Get historical network alerts."""
        try:
            kwargs = {}
            if per_page:
                kwargs['perPage'] = per_page
            if starting_after:
                kwargs['startingAfter'] = starting_after
            if ending_before:
                kwargs['endingBefore'] = ending_before
                
            alerts = meraki_client.dashboard.networks.getNetworkAlertsHistory(network_id, **kwargs)
            
            if not alerts:
                return f"No alerts found for network {network_id}"
                
            result = f"# 🚨 Network Alerts History\n\n"
            for alert in alerts[:50]:
                result += f"## {alert.get('occurredAt', 'Unknown time')}\n"
                result += f"- **Type**: {alert.get('type')}\n"
                result += f"- **Severity**: {alert.get('severity')}\n"
                result += f"- **Category**: {alert.get('category')}\n\n"
                
            if len(alerts) > 50:
                result += f"*Showing 50 of {len(alerts)} alerts*\n"
                
            return result
        except Exception as e:
            error_msg = str(e)
            if "404 Not Found" in error_msg:
                return f"⚠️ Network alerts history is not available for this network.\n\nThis could mean:\n- The network doesn't have alert reporting enabled\n- No alerts have been generated yet\n- The network type doesn't support alert history\n\nAlternatively, try 'get_network_events' to see network activity."
            return f"Error retrieving alerts history: {error_msg}"
    
    # ========== BLUETOOTH CLIENTS ==========

    @app.tool(
        name="get_network_bluetooth_clients",
        description="📱 Get Bluetooth clients detected by a network"
    )
    def get_network_bluetooth_clients(
        network_id: str,
        timespan: Optional[int] = 86400,
        per_page: Optional[int] = 100,
        starting_after: Optional[str] = None,
        ending_before: Optional[str] = None,
        include_connectivity_history: Optional[bool] = None
    ):
        """Get Bluetooth clients detected by a network."""
        try:
            kwargs = {'timespan': timespan}
            if per_page:
                kwargs['perPage'] = per_page
            if starting_after:
                kwargs['startingAfter'] = starting_after
            if ending_before:
                kwargs['endingBefore'] = ending_before
            if include_connectivity_history is not None:
                kwargs['includeConnectivityHistory'] = include_connectivity_history
                
            clients = meraki_client.dashboard.networks.getNetworkBluetoothClients(network_id, **kwargs)
            
            if not clients:
                return "No Bluetooth clients detected"
                
            result = f"# 📱 Bluetooth Clients\n\n"
            for client in clients[:50]:
                result += f"- **{client.get('name', 'Unknown')}**\n"
                result += f"  - MAC: `{client.get('mac')}`\n"
                result += f"  - Manufacturer: {client.get('manufacturer')}\n"
                result += f"  - Last seen: {client.get('lastSeen')}\n\n"
                
            if len(clients) > 50:
                result += f"*Showing 50 of {len(clients)} clients*\n"
                
            return result
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_network_bluetooth_client",
        description="📱 Get details for a specific Bluetooth client"
    )
    def get_network_bluetooth_client(
        network_id: str,
        bluetooth_client_id: str,
        include_connectivity_history: Optional[bool] = None,
        connectivity_history_timespan: Optional[int] = None
    ):
        """Get details for a specific Bluetooth client."""
        try:
            kwargs = {}
            if include_connectivity_history is not None:
                kwargs['includeConnectivityHistory'] = include_connectivity_history
            if connectivity_history_timespan:
                kwargs['connectivityHistoryTimespan'] = connectivity_history_timespan
                
            client = meraki_client.dashboard.networks.getNetworkBluetoothClient(
                network_id, bluetooth_client_id, **kwargs
            )
            
            result = f"# 📱 Bluetooth Client Details\n\n"
            result += f"**Name**: {client.get('name', 'Unknown')}\n"
            result += f"**MAC**: `{client.get('mac')}`\n"
            result += f"**Manufacturer**: {client.get('manufacturer')}\n"
            result += f"**Last seen**: {client.get('lastSeen')}\n"
            
            if client.get('connectivityHistory'):
                result += "\n## Connectivity History\n"
                for history in client['connectivityHistory'][:10]:
                    result += f"- {history.get('seenTime')}: {history.get('seenByDevice')}\n"
                    
            return result
        except Exception as e:
            return f"Error: {str(e)}"
    
    # ========== CLIENTS ==========

    @app.tool(
        name="get_network_client_details",
        description="👤 Get detailed information about a specific client"
    )
    def get_network_client_details(
        network_id: str,
        client_id: str
    ):
        """Get detailed information about a specific client."""
        try:
            client = meraki_client.get_network_client(network_id, client_id)
            
            result = f"# 👤 Client Details\n\n"
            result += f"**Description**: {client.get('description', 'Unknown')}\n"
            result += f"**MAC**: `{client.get('mac')}`\n"
            result += f"**IP**: `{client.get('ip')}`\n"
            result += f"**VLAN**: {client.get('vlan')}\n"
            result += f"**Status**: {client.get('status')}\n"
            
            usage = client.get('usage')
            if usage:
                result += f"\n## Usage\n"
                result += f"- **Sent**: {usage.get('sent')} bytes\n"
                result += f"- **Received**: {usage.get('recv')} bytes\n"
                
            return result
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_network_client_policy",
        description="📋 Get the policy assigned to a client"
    )
    def get_network_client_policy(
        network_id: str,
        client_id: str
    ):
        """Get the policy assigned to a client."""
        try:
            policy = meraki_client.get_network_client_policy(network_id, client_id)
            
            result = f"# 📋 Client Policy\n\n"
            result += f"**Device Policy**: {policy.get('devicePolicy', 'Normal')}\n"
            
            if policy.get('groupPolicyId'):
                result += f"**Group Policy ID**: {policy['groupPolicyId']}\n"
                
            return result
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="update_network_client_policy",
        description="📋 Update the policy assigned to a client"
    )
    def update_network_client_policy(
        network_id: str,
        client_id: str,
        device_policy: str,
        group_policy_id: Optional[str] = None
    ):
        """Update the policy assigned to a client."""
        try:
            kwargs = {'devicePolicy': device_policy}
            if group_policy_id:
                kwargs['groupPolicyId'] = group_policy_id
                
            result = meraki_client.update_network_client_policy(
                network_id, client_id, **kwargs
            )
            return "✅ Client policy updated"
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_network_client_splash_authorization_status",
        description="🌊 Get splash authorization status for a client"
    )
    def get_network_client_splash_authorization_status(
        network_id: str,
        client_id: str
    ):
        """Get splash authorization status for a client."""
        try:
            status = meraki_client.get_network_client_splash_authorization_status(
                network_id, client_id
            )
            
            result = f"# 🌊 Splash Authorization Status\n\n"
            result += f"**SSID**: {status.get('ssids', {})}\n"
            
            for ssid_num, auth_status in status.get('ssids', {}).items():
                result += f"\n## SSID {ssid_num}\n"
                result += f"- **Authorized**: {'✅' if auth_status.get('isAuthorized') else '❌'}\n"
                result += f"- **Authorized at**: {auth_status.get('authorizedAt')}\n"
                result += f"- **Expires at**: {auth_status.get('expiresAt')}\n"
                
            return result
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="update_network_client_splash_authorization_status",
        description="🌊 Update splash authorization status for a client"
    )
    def update_network_client_splash_authorization_status(
        network_id: str,
        client_id: str,
        ssids: str
    ):
        """Update splash authorization status for a client."""
        try:
            ssids_dict = json.loads(ssids)
            result = meraki_client.update_network_client_splash_authorization_status(
                network_id, client_id,
                ssids=ssids_dict
            )
            return "✅ Splash authorization updated"
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_network_client_traffic_history",
        description="📊 Get traffic history for a client"
    )
    def get_network_client_traffic_history(
        network_id: str,
        client_id: str,
        per_page: Optional[int] = 100,
        starting_after: Optional[str] = None,
        ending_before: Optional[str] = None
    ):
        """Get traffic history for a client."""
        try:
            kwargs = {}
            if per_page:
                kwargs['perPage'] = per_page
            if starting_after:
                kwargs['startingAfter'] = starting_after
            if ending_before:
                kwargs['endingBefore'] = ending_before
                
            history = meraki_client.get_network_client_traffic_history(
                network_id, client_id, **kwargs
            )
            
            if not history:
                return "No traffic history found"
                
            result = f"# 📊 Client Traffic History\n\n"
            for entry in history[:30]:
                result += f"- **{entry.get('application', 'Unknown')}**\n"
                result += f"  - Destination: {entry.get('destination')}\n"
                result += f"  - Port: {entry.get('port')}\n"
                result += f"  - Sent: {entry.get('sent')} bytes\n"
                result += f"  - Received: {entry.get('recv')} bytes\n\n"
                
            if len(history) > 30:
                result += f"*Showing 30 of {len(history)} entries*\n"
                
            return result
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_network_client_usage_history",
        description="📈 Get usage history for a client"
    )
    def get_network_client_usage_history(
        network_id: str,
        client_id: str
    ):
        """Get usage history for a client."""
        try:
            history = meraki_client.get_network_client_usage_history(network_id, client_id)
            
            result = f"# 📈 Client Usage History\n\n"
            for entry in history[:30]:
                result += f"## {entry.get('ts')}\n"
                result += f"- **Sent**: {entry.get('sent')} bytes\n"
                result += f"- **Received**: {entry.get('received')} bytes\n\n"
                
            if len(history) > 30:
                result += f"*Showing 30 of {len(history)} entries*\n"
                
            return result
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="provision_network_clients",
        description="👥 Provision multiple clients with policies"
    )
    def provision_network_clients(
        network_id: str,
        clients: str,
        device_policy: str,
        group_policy_id: Optional[str] = None,
        policies_by_security_appliance: Optional[str] = None,
        policies_by_ssid: Optional[str] = None
    ):
        """Provision multiple clients with policies."""
        try:
            clients_list = json.loads(clients)
            
            kwargs = {
                'clients': clients_list,
                'devicePolicy': device_policy
            }
            if group_policy_id:
                kwargs['groupPolicyId'] = group_policy_id
            if policies_by_security_appliance:
                kwargs['policiesBySecurityAppliance'] = json.loads(policies_by_security_appliance)
            if policies_by_ssid:
                kwargs['policiesBySsid'] = json.loads(policies_by_ssid)
                
            result = meraki_client.provision_network_clients(network_id, **kwargs)
            return f"✅ Provisioned {len(clients_list)} clients"
        except Exception as e:
            return f"Error: {str(e)}"
    
    # ========== EVENTS ==========

    @app.tool(
        name="get_network_events_detailed",
        description="📅 Get detailed events for a network with advanced filtering"
    )
    def get_network_events(
        network_id: str,
        product_type: Optional[str] = None,
        included_event_types: Optional[str] = None,
        excluded_event_types: Optional[str] = None,
        device_mac: Optional[str] = None,
        device_serial: Optional[str] = None,
        device_name: Optional[str] = None,
        client_ip: Optional[str] = None,
        client_mac: Optional[str] = None,
        client_name: Optional[str] = None,
        sm_device_mac: Optional[str] = None,
        sm_device_name: Optional[str] = None,
        per_page: Optional[int] = 100,
        starting_after: Optional[str] = None,
        ending_before: Optional[str] = None
    ):
        """Get events for a network."""
        try:
            kwargs = {}
            if product_type:
                kwargs['productType'] = product_type
            if included_event_types:
                kwargs['includedEventTypes'] = [t.strip() for t in included_event_types.split(',')]
            if excluded_event_types:
                kwargs['excludedEventTypes'] = [t.strip() for t in excluded_event_types.split(',')]
            if device_mac:
                kwargs['deviceMac'] = device_mac
            if device_serial:
                kwargs['deviceSerial'] = device_serial
            if device_name:
                kwargs['deviceName'] = device_name
            if client_ip:
                kwargs['clientIp'] = client_ip
            if client_mac:
                kwargs['clientMac'] = client_mac
            if client_name:
                kwargs['clientName'] = client_name
            if sm_device_mac:
                kwargs['smDeviceMac'] = sm_device_mac
            if sm_device_name:
                kwargs['smDeviceName'] = sm_device_name
            if per_page:
                kwargs['perPage'] = per_page
            if starting_after:
                kwargs['startingAfter'] = starting_after
            if ending_before:
                kwargs['endingBefore'] = ending_before
                
            # Try to get events - may require productType for multi-device networks
            try:
                events = meraki_client.dashboard.networks.getNetworkEvents(network_id, **kwargs)
            except Exception as api_error:
                error_msg = str(api_error)
                # Check if productType is required
                if 'productType' in error_msg or 'multiple device types' in error_msg:
                    # Try to detect network types
                    try:
                        network_info = meraki_client.dashboard.networks.getNetwork(network_id)
                        product_types = network_info.get('productTypes', [])
                        
                        if not product_types:
                            # Try to detect from devices
                            devices = meraki_client.dashboard.networks.getNetworkDevices(network_id)
                            detected_types = set()
                            for device in devices:
                                model = device.get('model', '')
                                if model.startswith('MX'):
                                    detected_types.add('appliance')
                                elif model.startswith('MS'):
                                    detected_types.add('switch')
                                elif model.startswith('MR'):
                                    detected_types.add('wireless')
                                elif model.startswith('MV'):
                                    detected_types.add('camera')
                            product_types = list(detected_types)
                        
                        if product_types:
                            return ("❌ Network has multiple device types. Please specify product_type parameter:\n"
                                   f"Available types: {', '.join(product_types)}\n\n"
                                   "💡 Examples:\n"
                                   f"  • get_network_events('{network_id}', product_type='wireless')\n"
                                   f"  • get_network_events('{network_id}', product_type='switch')\n"
                                   f"  • get_network_events('{network_id}', product_type='appliance')")
                    except:
                        pass
                    
                    return ("❌ This network requires productType parameter.\n"
                           "Common values: appliance, switch, wireless, camera\n\n"
                           "💡 Try: get_network_events(network_id, product_type='wireless')")
                else:
                    raise  # Re-raise original error
            
            if not events or not events.get('events'):
                return "No events found"
                
            event_list = events['events']
            result = f"# 📅 Network Events\n\n"
            result += f"**Time Period**: {events.get('pageStartAt', 'Unknown')} to {events.get('pageEndAt', 'Unknown')}\n"
            result += f"**Total Events**: {len(event_list)}\n\n"
            
            for event in event_list[:50]:
                result += f"## {event.get('occurredAt')}\n"
                result += f"- **Type**: {event.get('type')}\n"
                result += f"- **Category**: {event.get('category')}\n"
                result += f"- **Description**: {event.get('description')}\n"
                if event.get('deviceName'):
                    result += f"- **Device**: {event['deviceName']} ({event.get('deviceSerial', 'N/A')})\n"
                if event.get('clientDescription'):
                    result += f"- **Client**: {event['clientDescription']} ({event.get('clientMac', 'N/A')})\n"
                result += "\n"
                
            if len(event_list) > 50:
                result += f"*Showing 50 of {len(event_list)} events*\n"
                
            return result
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_network_events_event_types",
        description="📅 Get event types for a network"
    )
    def get_network_events_event_types(network_id: str):
        """Get event types for a network."""
        try:
            event_types = meraki_client.get_network_events_event_types(network_id)
            
            result = f"# 📅 Network Event Types\n\n"
            for event_type in event_types:
                result += f"- **{event_type.get('type')}**\n"
                result += f"  - Category: {event_type.get('category')}\n"
                result += f"  - Description: {event_type.get('description')}\n\n"
                
            return result
        except Exception as e:
            return f"Error: {str(e)}"
    
    # ========== FIRMWARE UPGRADES ==========

    @app.tool(
        name="get_network_firmware_upgrades",
        description="🔧 Get firmware upgrade status and schedule"
    )
    def get_network_firmware_upgrades(network_id: str):
        """Get firmware upgrade status and schedule."""
        try:
            upgrades = meraki_client.get_network_firmware_upgrades(network_id)
            
            result = f"# 🔧 Firmware Upgrades\n\n"
            
            # Upgrade window
            window = upgrades.get('upgradeWindow')
            if window:
                result += "## Upgrade Window\n"
                result += f"- **Day**: {window.get('dayOfWeek')}\n"
                result += f"- **Hour**: {window.get('hourOfDay')}\n\n"
                
            # Products
            products = upgrades.get('products')
            if products:
                result += "## Products\n"
                for product, info in products.items():
                    result += f"### {product}\n"
                    
                    current = info.get('currentVersion')
                    if current:
                        result += f"- **Current**: {current.get('firmware')}\n"
                        result += f"  - Release date: {current.get('releaseDate')}\n"
                        
                    next_scheduled = info.get('nextScheduled')
                    if next_scheduled:
                        result += f"- **Next scheduled**: {next_scheduled.get('toVersion', {}).get('firmware')}\n"
                        result += f"  - Time: {next_scheduled.get('time')}\n"
                        
                    available = info.get('availableVersions')
                    if available:
                        result += f"- **Available versions**: {len(available)}\n"
                        
                    result += "\n"
                    
            return result
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="update_network_firmware_upgrades",
        description="🔧 Schedule firmware upgrades. Requires confirmation."
    )
    def update_network_firmware_upgrades(
        network_id: str,
        products: str,
        timezone: Optional[str] = None,
        upgrade_window: Optional[str] = None,
        confirmed: bool = False
    ):
        """Schedule firmware upgrades."""
        try:
            if not confirmed:
                return "⚠️ Set confirmed=true to schedule firmware upgrades"
                
            products_dict = json.loads(products)
            
            kwargs = {'products': products_dict}
            if timezone:
                kwargs['timezone'] = timezone
            if upgrade_window:
                kwargs['upgradeWindow'] = json.loads(upgrade_window)
                
            result = meraki_client.update_network_firmware_upgrades(network_id, **kwargs)
            return "✅ Firmware upgrades scheduled"
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="create_network_firmware_upgrades_rollback",
        description="🔧 Rollback firmware upgrade. Requires confirmation."
    )
    def create_network_firmware_upgrades_rollback(
        network_id: str,
        reasons: str,
        confirmed: bool = False
    ):
        """Rollback firmware upgrade."""
        try:
            if not confirmed:
                return "⚠️ Set confirmed=true to rollback firmware"
                
            reasons_list = json.loads(reasons)
            result = meraki_client.create_network_firmware_upgrades_rollback(
                network_id,
                reasons=reasons_list
            )
            return "✅ Firmware rollback initiated"
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_network_firmware_upgrades_staged_events",
        description="🔧 Get staged firmware upgrade events"
    )
    def get_network_firmware_upgrades_staged_events(network_id: str):
        """Get staged firmware upgrade events."""
        try:
            events = meraki_client.get_network_firmware_upgrades_staged_events(network_id)
            
            result = f"# 🔧 Staged Firmware Events\n\n"
            
            if events.get('stages'):
                for stage in events['stages']:
                    result += f"## Stage: {stage.get('name')}\n"
                    
                    for event in stage.get('milestones', []):
                        result += f"- **{event.get('name')}**\n"
                        result += f"  - Status: {event.get('status')}\n"
                        result += f"  - Scheduled: {event.get('scheduledFor')}\n"
                        result += f"  - Completed: {event.get('completedAt')}\n\n"
                        
            return result
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="update_network_firmware_upgrades_staged_events",
        description="🔧 Update staged firmware events"
    )
    def update_network_firmware_upgrades_staged_events(
        network_id: str,
        stages: str
    ):
        """Update staged firmware events."""
        try:
            stages_list = json.loads(stages)
            result = meraki_client.update_network_firmware_upgrades_staged_events(
                network_id,
                stages=stages_list
            )
            return "✅ Staged events updated"
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="rollback_network_firmware_upgrades_staged_events",
        description="🔧 Rollback staged firmware events. Requires confirmation."
    )
    def rollback_network_firmware_upgrades_staged_events(
        network_id: str,
        reasons: str,
        stages: str,
        confirmed: bool = False
    ):
        """Rollback staged firmware events."""
        try:
            if not confirmed:
                return "⚠️ Set confirmed=true to rollback"
                
            reasons_list = json.loads(reasons)
            stages_list = json.loads(stages)
            
            result = meraki_client.rollback_network_firmware_upgrades_staged_events(
                network_id,
                reasons=reasons_list,
                stages=stages_list
            )
            return "✅ Staged events rolled back"
        except Exception as e:
            return f"Error: {str(e)}"
    
    # ========== FLOOR PLANS ==========

    @app.tool(
        name="get_network_floor_plans",
        description="🏢 Get floor plans for a network"
    )
    def get_network_floor_plans(network_id: str):
        """Get floor plans for a network."""
        try:
            floor_plans = meraki_client.get_network_floor_plans(network_id)
            
            if not floor_plans:
                return "No floor plans configured"
                
            result = f"# 🏢 Floor Plans\n\n"
            for plan in floor_plans:
                result += f"## {plan.get('name', 'Unnamed')}\n"
                result += f"- **ID**: `{plan.get('floorPlanId')}`\n"
                result += f"- **Width**: {plan.get('width')} ft\n"
                result += f"- **Height**: {plan.get('height')} ft\n"
                
                devices = plan.get('devices', [])
                if devices:
                    result += f"- **Devices**: {len(devices)}\n"
                    
                result += "\n"
                
            return result
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_network_floor_plan",
        description="🏢 Get a specific floor plan"
    )
    def get_network_floor_plan(
        network_id: str,
        floor_plan_id: str
    ):
        """Get a specific floor plan."""
        try:
            plan = meraki_client.get_network_floor_plan(network_id, floor_plan_id)
            
            result = f"# 🏢 Floor Plan: {plan.get('name', 'Unnamed')}\n\n"
            result += f"- **ID**: `{plan.get('floorPlanId')}`\n"
            result += f"- **Width**: {plan.get('width')} ft\n"
            result += f"- **Height**: {plan.get('height')} ft\n"
            result += f"- **Image URL**: {plan.get('imageUrl')}\n"
            
            devices = plan.get('devices', [])
            if devices:
                result += f"\n## Devices ({len(devices)})\n"
                for device in devices:
                    result += f"- {device.get('name', 'Unknown')} ({device.get('serial')})\n"
                    result += f"  - Position: ({device.get('x')}, {device.get('y')})\n"
                    
            return result
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="create_network_floor_plan",
        description="🏢 Create a floor plan"
    )
    def create_network_floor_plan(
        network_id: str,
        name: str,
        image_contents: str,
        top_left_corner: str,
        top_right_corner: str,
        bottom_left_corner: str,
        bottom_right_corner: str
    ):
        """Create a floor plan."""
        try:
            result = meraki_client.create_network_floor_plan(
                network_id,
                name=name,
                imageContents=image_contents,
                topLeftCorner=json.loads(top_left_corner),
                topRightCorner=json.loads(top_right_corner),
                bottomLeftCorner=json.loads(bottom_left_corner),
                bottomRightCorner=json.loads(bottom_right_corner)
            )
            return f"✅ Created floor plan '{name}' with ID: {result.get('floorPlanId')}"
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="update_network_floor_plan",
        description="🏢 Update a floor plan"
    )
    def update_network_floor_plan(
        network_id: str,
        floor_plan_id: str,
        name: Optional[str] = None,
        image_contents: Optional[str] = None,
        top_left_corner: Optional[str] = None,
        top_right_corner: Optional[str] = None,
        bottom_left_corner: Optional[str] = None,
        bottom_right_corner: Optional[str] = None
    ):
        """Update a floor plan."""
        try:
            kwargs = {}
            if name:
                kwargs['name'] = name
            if image_contents:
                kwargs['imageContents'] = image_contents
            if top_left_corner:
                kwargs['topLeftCorner'] = json.loads(top_left_corner)
            if top_right_corner:
                kwargs['topRightCorner'] = json.loads(top_right_corner)
            if bottom_left_corner:
                kwargs['bottomLeftCorner'] = json.loads(bottom_left_corner)
            if bottom_right_corner:
                kwargs['bottomRightCorner'] = json.loads(bottom_right_corner)
                
            result = meraki_client.update_network_floor_plan(
                network_id, floor_plan_id, **kwargs
            )
            return "✅ Floor plan updated"
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="delete_network_floor_plan",
        description="🗑️ Delete a floor plan. Requires confirmation."
    )
    def delete_network_floor_plan(
        network_id: str,
        floor_plan_id: str,
        confirmed: bool = False
    ):
        """Delete a floor plan."""
        try:
            if not confirmed:
                return "⚠️ Set confirmed=true to delete"
                
            meraki_client.delete_network_floor_plan(network_id, floor_plan_id)
            return "✅ Floor plan deleted"
        except Exception as e:
            return f"Error: {str(e)}"
    
    # ========== GROUP POLICIES ==========

    @app.tool(
        name="get_network_group_policies",
        description="📋 Get group policies for a network"
    )
    def get_network_group_policies(network_id: str):
        """Get group policies for a network."""
        try:
            policies = meraki_client.get_network_group_policies(network_id)
            
            if not policies:
                return "No group policies configured"
                
            result = f"# 📋 Group Policies\n\n"
            for policy in policies:
                result += f"## {policy.get('name', 'Unnamed')}\n"
                result += f"- **ID**: {policy.get('groupPolicyId')}\n"
                
                if policy.get('bandwidth'):
                    bandwidth = policy['bandwidth']
                    result += f"- **Bandwidth limits**:\n"
                    if bandwidth.get('bandwidthLimits'):
                        limits = bandwidth['bandwidthLimits']
                        result += f"  - Down: {limits.get('limitDown')} Mbps\n"
                        result += f"  - Up: {limits.get('limitUp')} Mbps\n"
                        
                if policy.get('firewallAndTrafficShaping'):
                    result += f"- **Firewall rules**: Configured\n"
                    
                if policy.get('splashAuthSettings'):
                    result += f"- **Splash**: {policy['splashAuthSettings']}\n"
                    
                result += "\n"
                
            return result
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_network_group_policy",
        description="📋 Get a specific group policy"
    )
    def get_network_group_policy(
        network_id: str,
        group_policy_id: str
    ):
        """Get a specific group policy."""
        try:
            policy = meraki_client.get_network_group_policy(network_id, group_policy_id)
            
            result = f"# 📋 Group Policy: {policy.get('name', 'Unnamed')}\n\n"
            result += f"- **ID**: {policy.get('groupPolicyId')}\n"
            
            # Scheduling
            if policy.get('scheduling'):
                result += "\n## Scheduling\n"
                result += f"- **Enabled**: {policy['scheduling'].get('enabled')}\n"
                
            # Bandwidth
            if policy.get('bandwidth'):
                result += "\n## Bandwidth\n"
                settings = policy['bandwidth'].get('settings')
                if settings:
                    result += f"- **Settings**: {settings}\n"
                    
            # Firewall
            if policy.get('firewallAndTrafficShaping'):
                result += "\n## Firewall & Traffic Shaping\n"
                result += f"- **Settings**: {policy['firewallAndTrafficShaping'].get('settings')}\n"
                
            # Content filtering
            if policy.get('contentFiltering'):
                result += "\n## Content Filtering\n"
                blocked = policy['contentFiltering'].get('blockedUrlCategories', {})
                if blocked.get('categories'):
                    result += f"- **Blocked categories**: {', '.join(blocked['categories'])}\n"
                    
            return result
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="create_network_group_policy",
        description="📋 Create a group policy"
    )
    def create_network_group_policy(
        network_id: str,
        name: str,
        scheduling: Optional[str] = None,
        bandwidth: Optional[str] = None,
        firewall_and_traffic_shaping: Optional[str] = None,
        content_filtering: Optional[str] = None,
        splash_auth_settings: Optional[str] = None,
        vlan_tagging: Optional[str] = None,
        bonjour_forwarding: Optional[str] = None
    ):
        """Create a group policy."""
        try:
            kwargs = {'name': name}
            if scheduling:
                kwargs['scheduling'] = json.loads(scheduling)
            if bandwidth:
                kwargs['bandwidth'] = json.loads(bandwidth)
            if firewall_and_traffic_shaping:
                kwargs['firewallAndTrafficShaping'] = json.loads(firewall_and_traffic_shaping)
            if content_filtering:
                kwargs['contentFiltering'] = json.loads(content_filtering)
            if splash_auth_settings:
                kwargs['splashAuthSettings'] = splash_auth_settings
            if vlan_tagging:
                kwargs['vlanTagging'] = json.loads(vlan_tagging)
            if bonjour_forwarding:
                kwargs['bonjourForwarding'] = json.loads(bonjour_forwarding)
                
            policy = meraki_client.create_network_group_policy(network_id, **kwargs)
            return f"✅ Created group policy '{name}' with ID: {policy.get('groupPolicyId')}"
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="update_network_group_policy",
        description="📋 Update a group policy"
    )
    def update_network_group_policy(
        network_id: str,
        group_policy_id: str,
        name: Optional[str] = None,
        scheduling: Optional[str] = None,
        bandwidth: Optional[str] = None,
        firewall_and_traffic_shaping: Optional[str] = None,
        content_filtering: Optional[str] = None,
        splash_auth_settings: Optional[str] = None,
        vlan_tagging: Optional[str] = None,
        bonjour_forwarding: Optional[str] = None
    ):
        """Update a group policy."""
        try:
            kwargs = {}
            if name:
                kwargs['name'] = name
            if scheduling:
                kwargs['scheduling'] = json.loads(scheduling)
            if bandwidth:
                kwargs['bandwidth'] = json.loads(bandwidth)
            if firewall_and_traffic_shaping:
                kwargs['firewallAndTrafficShaping'] = json.loads(firewall_and_traffic_shaping)
            if content_filtering:
                kwargs['contentFiltering'] = json.loads(content_filtering)
            if splash_auth_settings:
                kwargs['splashAuthSettings'] = splash_auth_settings
            if vlan_tagging:
                kwargs['vlanTagging'] = json.loads(vlan_tagging)
            if bonjour_forwarding:
                kwargs['bonjourForwarding'] = json.loads(bonjour_forwarding)
                
            result = meraki_client.update_network_group_policy(
                network_id, group_policy_id, **kwargs
            )
            return "✅ Group policy updated"
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="delete_network_group_policy",
        description="🗑️ Delete a group policy. Requires confirmation."
    )
    def delete_network_group_policy(
        network_id: str,
        group_policy_id: str,
        confirmed: bool = False
    ):
        """Delete a group policy."""
        try:
            if not confirmed:
                return "⚠️ Set confirmed=true to delete"
                
            meraki_client.delete_network_group_policy(network_id, group_policy_id)
            return "✅ Group policy deleted"
        except Exception as e:
            return f"Error: {str(e)}"
    
    # ========== HEALTH ==========

    @app.tool(
        name="get_network_health_channel_utilization",
        description="📊 Get channel utilization health data"
    )
    def get_network_health_channel_utilization(
        network_id: str,
        timespan: Optional[int] = 86400,
        resolution: Optional[int] = None,
        per_page: Optional[int] = None,
        starting_after: Optional[str] = None,
        ending_before: Optional[str] = None
    ):
        """Get channel utilization health data."""
        try:
            kwargs = {'timespan': timespan}
            if resolution:
                kwargs['resolution'] = resolution
            if per_page:
                kwargs['perPage'] = per_page
            if starting_after:
                kwargs['startingAfter'] = starting_after
            if ending_before:
                kwargs['endingBefore'] = ending_before
                
            data = meraki_client.get_network_health_channel_utilization(network_id, **kwargs)
            
            result = f"# 📊 Channel Utilization Health\n\n"
            for entry in data[:20]:
                result += f"## {entry.get('startTs')}\n"
                
                if entry.get('wifi0'):
                    result += f"- **2.4 GHz**: {entry['wifi0']}% utilized\n"
                if entry.get('wifi1'):
                    result += f"- **5 GHz**: {entry['wifi1']}% utilized\n"
                    
                result += "\n"
                
            if len(data) > 20:
                result += f"*Showing 20 of {len(data)} data points*\n"
                
            return result
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_network_health_alerts",
        description="🚨 Get health alerts for a network"
    )
    def get_network_health_alerts(network_id: str):
        """Get health alerts for a network."""
        try:
            alerts = meraki_client.dashboard.networks.getNetworkHealthAlerts(network_id)
            
            if not alerts:
                return "No health alerts"
                
            result = f"# 🚨 Network Health Alerts\n\n"
            for alert in alerts:
                result += f"## {alert.get('type')}\n"
                result += f"- **Severity**: {alert.get('severity')}\n"
                result += f"- **Scope**: {alert.get('scope', {}).get('devices', [])} devices\n"
                result += f"- **Category**: {alert.get('category')}\n\n"
                
            return result
        except Exception as e:
            return f"Error: {str(e)}"
    
    # ========== MERAKI AUTH USERS ==========

    @app.tool(
        name="get_network_meraki_auth_users",
        description="👤 Get Meraki auth users for a network"
    )
    def get_network_meraki_auth_users(network_id: str):
        """Get Meraki auth users for a network."""
        try:
            users = meraki_client.get_network_meraki_auth_users(network_id)
            
            if not users:
                return "No Meraki auth users configured"
                
            result = f"# 👤 Meraki Auth Users\n\n"
            for user in users:
                result += f"## {user.get('name', user.get('email', 'Unknown'))}\n"
                result += f"- **ID**: {user.get('id')}\n"
                result += f"- **Email**: {user.get('email')}\n"
                result += f"- **Account Type**: {user.get('accountType')}\n"
                result += f"- **Created**: {user.get('createdAt')}\n"
                
                if user.get('authorizations'):
                    result += f"- **Authorizations**: {len(user['authorizations'])}\n"
                    
                result += "\n"
                
            return result
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_network_meraki_auth_user",
        description="👤 Get a specific Meraki auth user"
    )
    def get_network_meraki_auth_user(
        network_id: str,
        meraki_auth_user_id: str
    ):
        """Get a specific Meraki auth user."""
        try:
            user = meraki_client.get_network_meraki_auth_user(
                network_id, meraki_auth_user_id
            )
            
            result = f"# 👤 Meraki Auth User\n\n"
            result += f"**Name**: {user.get('name', user.get('email', 'Unknown'))}\n"
            result += f"**ID**: {user.get('id')}\n"
            result += f"**Email**: {user.get('email')}\n"
            result += f"**Account Type**: {user.get('accountType')}\n"
            result += f"**Created**: {user.get('createdAt')}\n"
            
            if user.get('authorizations'):
                result += f"\n## Authorizations\n"
                for auth in user['authorizations']:
                    result += f"- **{auth.get('ssidName')}**\n"
                    result += f"  - Authorized: {auth.get('authorizedAt')}\n"
                    result += f"  - Expires: {auth.get('expiresAt')}\n"
                    
            return result
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="create_network_meraki_auth_user",
        description="👤 Create a Meraki auth user"
    )
    def create_network_meraki_auth_user(
        network_id: str,
        email: str,
        name: str,
        password: str,
        account_type: str = "Guest",
        email_password_to_user: Optional[bool] = None,
        is_admin: Optional[bool] = None,
        authorizations: Optional[str] = None
    ):
        """Create a Meraki auth user."""
        try:
            kwargs = {
                'email': email,
                'name': name,
                'password': password,
                'accountType': account_type
            }
            if email_password_to_user is not None:
                kwargs['emailPasswordToUser'] = email_password_to_user
            if is_admin is not None:
                kwargs['isAdmin'] = is_admin
            if authorizations:
                kwargs['authorizations'] = json.loads(authorizations)
                
            user = meraki_client.create_network_meraki_auth_user(network_id, **kwargs)
            return f"✅ Created Meraki auth user '{name}' with ID: {user.get('id')}"
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="update_network_meraki_auth_user",
        description="👤 Update a Meraki auth user"
    )
    def update_network_meraki_auth_user(
        network_id: str,
        meraki_auth_user_id: str,
        name: Optional[str] = None,
        password: Optional[str] = None,
        email_password_to_user: Optional[bool] = None,
        is_admin: Optional[bool] = None,
        authorizations: Optional[str] = None
    ):
        """Update a Meraki auth user."""
        try:
            kwargs = {}
            if name:
                kwargs['name'] = name
            if password:
                kwargs['password'] = password
            if email_password_to_user is not None:
                kwargs['emailPasswordToUser'] = email_password_to_user
            if is_admin is not None:
                kwargs['isAdmin'] = is_admin
            if authorizations:
                kwargs['authorizations'] = json.loads(authorizations)
                
            result = meraki_client.update_network_meraki_auth_user(
                network_id, meraki_auth_user_id, **kwargs
            )
            return "✅ Meraki auth user updated"
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="delete_network_meraki_auth_user",
        description="🗑️ Delete a Meraki auth user. Requires confirmation."
    )
    def delete_network_meraki_auth_user(
        network_id: str,
        meraki_auth_user_id: str,
        confirmed: bool = False
    ):
        """Delete a Meraki auth user."""
        try:
            if not confirmed:
                return "⚠️ Set confirmed=true to delete"
                
            meraki_client.delete_network_meraki_auth_user(
                network_id, meraki_auth_user_id
            )
            return "✅ Meraki auth user deleted"
        except Exception as e:
            return f"Error: {str(e)}"
    
    # ========== MQTT BROKERS ==========

    @app.tool(
        name="get_network_mqtt_brokers",
        description="📡 Get MQTT brokers for a network"
    )
    def get_network_mqtt_brokers(network_id: str):
        """Get MQTT brokers for a network."""
        try:
            brokers = meraki_client.get_network_mqtt_brokers(network_id)
            
            if not brokers:
                return "No MQTT brokers configured"
                
            result = f"# 📡 MQTT Brokers\n\n"
            for broker in brokers:
                result += f"## {broker.get('name', 'Unnamed')}\n"
                result += f"- **ID**: `{broker.get('id')}`\n"
                result += f"- **Host**: {broker.get('host')}\n"
                result += f"- **Port**: {broker.get('port')}\n"
                
                security = broker.get('security', {})
                if security:
                    result += f"- **Security**: {security.get('mode')}\n"
                    
                result += "\n"
                
            return result
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_network_mqtt_broker",
        description="📡 Get a specific MQTT broker"
    )
    def get_network_mqtt_broker(
        network_id: str,
        mqtt_broker_id: str
    ):
        """Get a specific MQTT broker."""
        try:
            broker = meraki_client.get_network_mqtt_broker(network_id, mqtt_broker_id)
            
            result = f"# 📡 MQTT Broker: {broker.get('name', 'Unnamed')}\n\n"
            result += f"- **ID**: `{broker.get('id')}`\n"
            result += f"- **Host**: {broker.get('host')}\n"
            result += f"- **Port**: {broker.get('port')}\n"
            
            security = broker.get('security', {})
            if security:
                result += f"\n## Security\n"
                result += f"- **Mode**: {security.get('mode')}\n"
                if security.get('tls'):
                    result += f"- **TLS**: {security['tls'].get('verifyHostnames')}\n"
                    
            authentication = broker.get('authentication')
            if authentication:
                result += f"\n## Authentication\n"
                result += f"- **Username**: {authentication.get('username')}\n"
                
            return result
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="create_network_mqtt_broker",
        description="📡 Create an MQTT broker"
    )
    def create_network_mqtt_broker(
        network_id: str,
        name: str,
        host: str,
        port: int,
        security: Optional[str] = None,
        authentication: Optional[str] = None
    ):
        """Create an MQTT broker."""
        try:
            kwargs = {
                'name': name,
                'host': host,
                'port': port
            }
            if security:
                kwargs['security'] = json.loads(security)
            if authentication:
                kwargs['authentication'] = json.loads(authentication)
                
            broker = meraki_client.create_network_mqtt_broker(network_id, **kwargs)
            return f"✅ Created MQTT broker '{name}' with ID: {broker.get('id')}"
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="update_network_mqtt_broker",
        description="📡 Update an MQTT broker"
    )
    def update_network_mqtt_broker(
        network_id: str,
        mqtt_broker_id: str,
        name: Optional[str] = None,
        host: Optional[str] = None,
        port: Optional[int] = None,
        security: Optional[str] = None,
        authentication: Optional[str] = None
    ):
        """Update an MQTT broker."""
        try:
            kwargs = {}
            if name:
                kwargs['name'] = name
            if host:
                kwargs['host'] = host
            if port:
                kwargs['port'] = port
            if security:
                kwargs['security'] = json.loads(security)
            if authentication:
                kwargs['authentication'] = json.loads(authentication)
                
            result = meraki_client.update_network_mqtt_broker(
                network_id, mqtt_broker_id, **kwargs
            )
            return "✅ MQTT broker updated"
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="delete_network_mqtt_broker",
        description="🗑️ Delete an MQTT broker. Requires confirmation."
    )
    def delete_network_mqtt_broker(
        network_id: str,
        mqtt_broker_id: str,
        confirmed: bool = False
    ):
        """Delete an MQTT broker."""
        try:
            if not confirmed:
                return "⚠️ Set confirmed=true to delete"
                
            meraki_client.delete_network_mqtt_broker(network_id, mqtt_broker_id)
            return "✅ MQTT broker deleted"
        except Exception as e:
            return f"Error: {str(e)}"
    
    # ========== PII ==========

    @app.tool(
        name="get_network_pii_pii_keys",
        description="🔐 Get PII keys for a network"
    )
    def get_network_pii_pii_keys(
        network_id: str,
        username: Optional[str] = None,
        email: Optional[str] = None,
        mac: Optional[str] = None,
        serial: Optional[str] = None,
        imei: Optional[str] = None,
        bluetooth_mac: Optional[str] = None
    ):
        """Get PII keys for a network."""
        try:
            kwargs = {}
            if username:
                kwargs['username'] = username
            if email:
                kwargs['email'] = email
            if mac:
                kwargs['mac'] = mac
            if serial:
                kwargs['serial'] = serial
            if imei:
                kwargs['imei'] = imei
            if bluetooth_mac:
                kwargs['bluetoothMac'] = bluetooth_mac
                
            keys = meraki_client.get_network_pii_pii_keys(network_id, **kwargs)
            
            result = f"# 🔐 PII Keys\n\n"
            for key in keys.get('keys', []):
                result += f"- **{key}**\n"
                
            return result
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_network_pii_requests",
        description="🔐 Get PII requests for a network"
    )
    def get_network_pii_requests(network_id: str):
        """Get PII requests for a network."""
        try:
            requests = meraki_client.get_network_pii_requests(network_id)
            
            if not requests:
                return "No PII requests"
                
            result = f"# 🔐 PII Requests\n\n"
            for request in requests:
                result += f"## Request {request.get('id')}\n"
                result += f"- **Type**: {request.get('type')}\n"
                result += f"- **Status**: {request.get('status')}\n"
                result += f"- **Submitted**: {request.get('submittedAt')}\n"
                result += f"- **Completed**: {request.get('completedAt')}\n\n"
                
            return result
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_network_pii_request",
        description="🔐 Get a specific PII request"
    )
    def get_network_pii_request(
        network_id: str,
        request_id: str
    ):
        """Get a specific PII request."""
        try:
            request = meraki_client.get_network_pii_request(network_id, request_id)
            
            result = f"# 🔐 PII Request {request.get('id')}\n\n"
            result += f"- **Type**: {request.get('type')}\n"
            result += f"- **Status**: {request.get('status')}\n"
            result += f"- **Submitted**: {request.get('submittedAt')}\n"
            result += f"- **Completed**: {request.get('completedAt')}\n"
            
            if request.get('datasets'):
                result += f"\n## Datasets\n"
                for dataset in request['datasets']:
                    result += f"- {dataset}\n"
                    
            return result
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="create_network_pii_request",
        description="🔐 Create a PII request. Requires confirmation."
    )
    def create_network_pii_request(
        network_id: str,
        type: str,
        datasets: Optional[str] = None,
        username: Optional[str] = None,
        email: Optional[str] = None,
        mac: Optional[str] = None,
        sm_device_id: Optional[str] = None,
        sm_user_id: Optional[str] = None,
        confirmed: bool = False
    ):
        """Create a PII request."""
        try:
            if not confirmed:
                return "⚠️ Set confirmed=true to create PII request"
                
            kwargs = {'type': type}
            if datasets:
                kwargs['datasets'] = [d.strip() for d in datasets.split(',')]
            if username:
                kwargs['username'] = username
            if email:
                kwargs['email'] = email
            if mac:
                kwargs['mac'] = mac
            if sm_device_id:
                kwargs['smDeviceId'] = sm_device_id
            if sm_user_id:
                kwargs['smUserId'] = sm_user_id
                
            request = meraki_client.create_network_pii_request(network_id, **kwargs)
            return f"✅ Created PII request with ID: {request.get('id')}"
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="delete_network_pii_request",
        description="🗑️ Delete a PII request. Requires confirmation."
    )
    def delete_network_pii_request(
        network_id: str,
        request_id: str,
        confirmed: bool = False
    ):
        """Delete a PII request."""
        try:
            if not confirmed:
                return "⚠️ Set confirmed=true to delete"
                
            meraki_client.delete_network_pii_request(network_id, request_id)
            return "✅ PII request deleted"
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_network_pii_sm_devices_for_key",
        description="🔐 Get SM devices for a PII key"
    )
    def get_network_pii_sm_devices_for_key(
        network_id: str,
        username: Optional[str] = None,
        email: Optional[str] = None,
        mac: Optional[str] = None,
        serial: Optional[str] = None,
        imei: Optional[str] = None,
        bluetooth_mac: Optional[str] = None
    ):
        """Get SM devices for a PII key."""
        try:
            kwargs = {}
            if username:
                kwargs['username'] = username
            if email:
                kwargs['email'] = email
            if mac:
                kwargs['mac'] = mac
            if serial:
                kwargs['serial'] = serial
            if imei:
                kwargs['imei'] = imei
            if bluetooth_mac:
                kwargs['bluetoothMac'] = bluetooth_mac
                
            devices = meraki_client.get_network_pii_sm_devices_for_key(network_id, **kwargs)
            
            result = f"# 🔐 SM Devices for PII Key\n\n"
            for device_id in devices:
                result += f"- Device ID: `{device_id}`\n"
                
            return result
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_network_pii_sm_owners_for_key",
        description="🔐 Get SM owners for a PII key"
    )
    def get_network_pii_sm_owners_for_key(
        network_id: str,
        username: Optional[str] = None,
        email: Optional[str] = None,
        mac: Optional[str] = None,
        serial: Optional[str] = None,
        imei: Optional[str] = None,
        bluetooth_mac: Optional[str] = None
    ):
        """Get SM owners for a PII key."""
        try:
            kwargs = {}
            if username:
                kwargs['username'] = username
            if email:
                kwargs['email'] = email
            if mac:
                kwargs['mac'] = mac
            if serial:
                kwargs['serial'] = serial
            if imei:
                kwargs['imei'] = imei
            if bluetooth_mac:
                kwargs['bluetoothMac'] = bluetooth_mac
                
            owners = meraki_client.get_network_pii_sm_owners_for_key(network_id, **kwargs)
            
            result = f"# 🔐 SM Owners for PII Key\n\n"
            for owner_id in owners:
                result += f"- Owner ID: `{owner_id}`\n"
                
            return result
        except Exception as e:
            return f"Error: {str(e)}"
    
    # ========== SETTINGS ==========

    @app.tool(
        name="get_network_settings",
        description="⚙️ Get settings for a network"
    )
    def get_network_settings(network_id: str):
        """Get settings for a network."""
        try:
            settings = meraki_client.get_network_settings(network_id)
            
            result = f"# ⚙️ Network Settings\n\n"
            
            # Local status page
            if settings.get('localStatusPageEnabled') is not None:
                result += f"**Local Status Page**: {'✅' if settings['localStatusPageEnabled'] else '❌'}\n"
                
            # Remote status page
            if settings.get('remoteStatusPageEnabled') is not None:
                result += f"**Remote Status Page**: {'✅' if settings['remoteStatusPageEnabled'] else '❌'}\n"
                
            # Local status page authentication
            auth = settings.get('localStatusPage', {}).get('authentication')
            if auth:
                result += f"\n## Authentication\n"
                result += f"- **Enabled**: {auth.get('enabled')}\n"
                if auth.get('username'):
                    result += f"- **Username**: {auth['username']}\n"
                    
            # Secure port
            secure_port = settings.get('securePort', {})
            if secure_port:
                result += f"\n## Secure Port\n"
                result += f"- **Enabled**: {secure_port.get('enabled')}\n"
                
            # Named VLANs
            named_vlans = settings.get('namedVlans', {})
            if named_vlans:
                result += f"\n## Named VLANs\n"
                result += f"- **Enabled**: {named_vlans.get('enabled')}\n"
                
            return result
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="update_network_settings",
        description="⚙️ Update settings for a network"
    )
    def update_network_settings(
        network_id: str,
        local_status_page_enabled: Optional[bool] = None,
        remote_status_page_enabled: Optional[bool] = None,
        local_status_page: Optional[str] = None,
        secure_port: Optional[str] = None,
        named_vlans: Optional[str] = None
    ):
        """Update settings for a network."""
        try:
            kwargs = {}
            if local_status_page_enabled is not None:
                kwargs['localStatusPageEnabled'] = local_status_page_enabled
            if remote_status_page_enabled is not None:
                kwargs['remoteStatusPageEnabled'] = remote_status_page_enabled
            if local_status_page:
                kwargs['localStatusPage'] = json.loads(local_status_page)
            if secure_port:
                kwargs['securePort'] = json.loads(secure_port)
            if named_vlans:
                kwargs['namedVlans'] = json.loads(named_vlans)
                
            result = meraki_client.update_network_settings(network_id, **kwargs)
            return "✅ Network settings updated"
        except Exception as e:
            return f"Error: {str(e)}"
    
    # ========== SNMP ==========

    @app.tool(
        name="get_network_snmp",
        description="📡 Get SNMP settings for a network"
    )
    def get_network_snmp(network_id: str):
        """Get SNMP settings for a network."""
        try:
            snmp = meraki_client.get_network_snmp(network_id)
            
            result = f"# 📡 Network SNMP Settings\n\n"
            
            result += f"**Access**: {snmp.get('access', 'none')}\n"
            
            if snmp.get('communityString'):
                result += f"**Community String**: {snmp['communityString'][:5]}...\n"
                
            users = snmp.get('users', [])
            if users:
                result += f"\n## Users ({len(users)})\n"
                for user in users:
                    result += f"- {user.get('username')}\n"
                    
            return result
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="update_network_snmp",
        description="📡 Update SNMP settings for a network"
    )
    def update_network_snmp(
        network_id: str,
        access: Optional[str] = None,
        community_string: Optional[str] = None,
        users: Optional[str] = None
    ):
        """Update SNMP settings for a network."""
        try:
            kwargs = {}
            if access:
                kwargs['access'] = access
            if community_string:
                kwargs['communityString'] = community_string
            if users:
                kwargs['users'] = json.loads(users)
                
            result = meraki_client.update_network_snmp(network_id, **kwargs)
            return "✅ SNMP settings updated"
        except Exception as e:
            return f"Error: {str(e)}"
    
    # ========== SPLASH LOGIN ATTEMPTS ==========

    @app.tool(
        name="get_network_splash_login_attempts",
        description="🌊 Get splash page login attempts"
    )
    def get_network_splash_login_attempts(
        network_id: str,
        ssid_number: Optional[int] = None,
        login_identifier: Optional[str] = None,
        timespan: Optional[int] = None
    ):
        """Get splash page login attempts."""
        try:
            kwargs = {}
            if ssid_number is not None:
                kwargs['ssidNumber'] = ssid_number
            if login_identifier:
                kwargs['loginIdentifier'] = login_identifier
            if timespan:
                kwargs['timespan'] = timespan
                
            attempts = meraki_client.get_network_splash_login_attempts(network_id, **kwargs)
            
            if not attempts:
                return "No splash login attempts"
                
            result = f"# 🌊 Splash Login Attempts\n\n"
            for attempt in attempts[:50]:
                result += f"## {attempt.get('loginAt')}\n"
                result += f"- **Name**: {attempt.get('name')}\n"
                result += f"- **Login**: {attempt.get('login')}\n"
                result += f"- **SSID**: {attempt.get('ssidNumber')}\n"
                result += f"- **Client MAC**: {attempt.get('clientMac')}\n"
                result += f"- **Client IP**: {attempt.get('clientIp')}\n"
                result += f"- **Authorization**: {attempt.get('authorization')}\n\n"
                
            if len(attempts) > 50:
                result += f"*Showing 50 of {len(attempts)} attempts*\n"
                
            return result
        except Exception as e:
            return f"Error: {str(e)}"
    
    # ========== SYSLOG SERVERS ==========

    @app.tool(
        name="get_network_syslog_servers",
        description="📝 Get syslog servers for a network"
    )
    def get_network_syslog_servers(network_id: str):
        """Get syslog servers for a network."""
        try:
            servers = meraki_client.get_network_syslog_servers(network_id)
            
            result = f"# 📝 Syslog Servers\n\n"
            
            servers_list = servers.get('servers', [])
            if servers_list:
                for server in servers_list:
                    result += f"- **{server.get('host')}:{server.get('port')}**\n"
                    result += f"  - Roles: {', '.join(server.get('roles', []))}\n"
            else:
                result += "No syslog servers configured\n"
                
            return result
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="update_network_syslog_servers",
        description="📝 Update syslog servers for a network"
    )
    def update_network_syslog_servers(
        network_id: str,
        servers: str
    ):
        """Update syslog servers for a network."""
        try:
            servers_list = json.loads(servers)
            result = meraki_client.update_network_syslog_servers(
                network_id,
                servers=servers_list
            )
            return "✅ Syslog servers updated"
        except Exception as e:
            return f"Error: {str(e)}"
    
    # ========== TOPOLOGY ==========

    @app.tool(
        name="get_network_topology_link_layer",
        description="🔗 Get link layer topology for a network"
    )
    def get_network_topology_link_layer(network_id: str):
        """Get link layer topology for a network."""
        try:
            topology = meraki_client.dashboard.networks.getNetworkTopologyLinkLayer(network_id)
            
            result = f"# 🔗 Link Layer Topology\n\n"
            
            nodes = topology.get('nodes', [])
            if nodes:
                result += f"## Nodes ({len(nodes)})\n"
                for node in nodes[:20]:
                    result += f"- **{node.get('name', 'Unknown')}**\n"
                    result += f"  - Type: {node.get('type')}\n"
                    result += f"  - Model: {node.get('model')}\n"
                    
                if len(nodes) > 20:
                    result += f"*Showing 20 of {len(nodes)} nodes*\n"
                    
            links = topology.get('links', [])
            if links:
                result += f"\n## Links ({len(links)})\n"
                for link in links[:20]:
                    result += f"- {link.get('source')} ↔ {link.get('target')}\n"
                    
                if len(links) > 20:
                    result += f"*Showing 20 of {len(links)} links*\n"
                    
            return result
        except Exception as e:
            return f"Error: {str(e)}"
    
    # ========== TRAFFIC ==========

    @app.tool(
        name="get_network_traffic",
        description="📊 Get traffic data for a network"
    )
    def get_network_traffic(
        network_id: str,
        timespan: Optional[int] = 86400,
        device_type: Optional[str] = None
    ):
        """Get traffic data for a network."""
        try:
            kwargs = {'timespan': timespan}
            if device_type:
                kwargs['deviceType'] = device_type
                
            traffic = meraki_client.get_network_traffic(network_id, **kwargs)
            
            result = f"# 📊 Network Traffic (Last {timespan}s)\n\n"
            
            for app in traffic[:30]:
                result += f"- **{app.get('application', 'Unknown')}**\n"
                result += f"  - Destination: {app.get('destination')}\n"
                result += f"  - Port: {app.get('port')}\n"
                result += f"  - Sent: {app.get('sent')} bytes\n"
                result += f"  - Received: {app.get('recv')} bytes\n"
                result += f"  - Clients: {app.get('numClients')}\n\n"
                
            if len(traffic) > 30:
                result += f"*Showing 30 of {len(traffic)} applications*\n"
                
            return result
        except Exception as e:
            return f"Error: {str(e)}"
    
    # ========== TRAFFIC ANALYSIS ==========

    @app.tool(
        name="get_network_traffic_analysis",
        description="📊 Get traffic analysis settings"
    )
    def get_network_traffic_analysis(network_id: str):
        """Get traffic analysis settings."""
        try:
            analysis = meraki_client.get_network_traffic_analysis(network_id)
            
            result = f"# 📊 Traffic Analysis Settings\n\n"
            result += f"**Mode**: {analysis.get('mode', 'disabled')}\n"
            
            custom_pie_chart = analysis.get('customPieChartItems', [])
            if custom_pie_chart:
                result += f"\n## Custom Pie Chart Items\n"
                for item in custom_pie_chart:
                    result += f"- **{item.get('name')}**\n"
                    result += f"  - Type: {item.get('type')}\n"
                    result += f"  - Value: {item.get('value')}\n"
                    
            return result
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="update_network_traffic_analysis",
        description="📊 Update traffic analysis settings"
    )
    def update_network_traffic_analysis(
        network_id: str,
        mode: Optional[str] = None,
        custom_pie_chart_items: Optional[str] = None
    ):
        """Update traffic analysis settings."""
        try:
            kwargs = {}
            if mode:
                kwargs['mode'] = mode
            if custom_pie_chart_items:
                kwargs['customPieChartItems'] = json.loads(custom_pie_chart_items)
                
            result = meraki_client.update_network_traffic_analysis(network_id, **kwargs)
            return "✅ Traffic analysis settings updated"
        except Exception as e:
            return f"Error: {str(e)}"
    
    # ========== TRAFFIC SHAPING ==========

    @app.tool(
        name="get_network_traffic_shaping_application_categories",
        description="📊 Get traffic shaping application categories"
    )
    def get_network_traffic_shaping_application_categories(network_id: str):
        """Get traffic shaping application categories."""
        try:
            categories = meraki_client.get_network_traffic_shaping_application_categories(network_id)
            
            result = f"# 📊 Traffic Shaping Application Categories\n\n"
            
            app_categories = categories.get('applicationCategories', [])
            for category in app_categories:
                result += f"- **{category.get('name')}**\n"
                result += f"  - ID: {category.get('id')}\n"
                result += f"  - Applications: {len(category.get('applications', []))}\n"
                
            return result
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_network_traffic_shaping_dscp_tagging_options",
        description="📊 Get DSCP tagging options"
    )
    def get_network_traffic_shaping_dscp_tagging_options(network_id: str):
        """Get DSCP tagging options."""
        try:
            options = meraki_client.get_network_traffic_shaping_dscp_tagging_options(network_id)
            
            result = f"# 📊 DSCP Tagging Options\n\n"
            
            for option in options:
                result += f"- **{option.get('description')}**\n"
                result += f"  - DSCP Value: {option.get('dscpValue')}\n"
                
            return result
        except Exception as e:
            return f"Error: {str(e)}"
    
    # ========== WEBHOOKS ==========

    @app.tool(
        name="get_network_webhooks_http_servers",
        description="🔗 Get webhook HTTP servers for a network"
    )
    def get_network_webhooks_http_servers(network_id: str):
        """Get webhook HTTP servers for a network."""
        try:
            servers = meraki_client.get_network_webhooks_http_servers(network_id)
            
            if not servers:
                return "No webhook servers configured"
                
            result = f"# 🔗 Webhook HTTP Servers\n\n"
            for server in servers:
                result += f"## {server.get('name', 'Unnamed')}\n"
                result += f"- **ID**: `{server.get('id')}`\n"
                result += f"- **URL**: {server.get('url')}\n"
                result += f"- **Shared Secret**: {'Set' if server.get('sharedSecret') else 'Not set'}\n\n"
                
            return result
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="create_network_webhooks_http_server",
        description="🔗 Create a webhook HTTP server"
    )
    def create_network_webhooks_http_server(
        network_id: str,
        name: str,
        url: str,
        shared_secret: Optional[str] = None,
        payload_template_id: Optional[str] = None,
        payload_template: Optional[str] = None
    ):
        """Create a webhook HTTP server."""
        try:
            kwargs = {
                'name': name,
                'url': url
            }
            if shared_secret:
                kwargs['sharedSecret'] = shared_secret
            if payload_template_id:
                kwargs['payloadTemplateId'] = payload_template_id
            if payload_template:
                kwargs['payloadTemplate'] = json.loads(payload_template)
                
            server = meraki_client.create_network_webhooks_http_server(network_id, **kwargs)
            return f"✅ Created webhook server '{name}' with ID: {server.get('id')}"
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_network_webhooks_webhook_test",
        description="🔗 Get webhook test status"
    )
    def get_network_webhooks_webhook_test(
        network_id: str,
        webhook_test_id: str
    ):
        """Get webhook test status."""
        try:
            test = meraki_client.get_network_webhooks_webhook_test(network_id, webhook_test_id)
            
            result = f"# 🔗 Webhook Test {webhook_test_id}\n\n"
            result += f"- **Status**: {test.get('status')}\n"
            result += f"- **URL**: {test.get('url')}\n"
            
            return result
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="create_network_webhooks_webhook_test",
        description="🔗 Test a webhook"
    )
    def create_network_webhooks_webhook_test(
        network_id: str,
        url: str,
        shared_secret: Optional[str] = None,
        payload_template_id: Optional[str] = None,
        payload_template: Optional[str] = None,
        alert_type_id: Optional[str] = None
    ):
        """Test a webhook."""
        try:
            kwargs = {'url': url}
            if shared_secret:
                kwargs['sharedSecret'] = shared_secret
            if payload_template_id:
                kwargs['payloadTemplateId'] = payload_template_id
            if payload_template:
                kwargs['payloadTemplate'] = json.loads(payload_template)
            if alert_type_id:
                kwargs['alertTypeId'] = alert_type_id
                
            test = meraki_client.create_network_webhooks_webhook_test(network_id, **kwargs)
            return f"✅ Webhook test created with ID: {test.get('id')}"
        except Exception as e:
            return f"Error: {str(e)}"


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
            
            result_msg = "✅ Network split successfully into:\n"
            for net in result.get('resultingNetworks', []):
                result_msg += f"  - {net.get('name')} (ID: {net.get('id')})\n"
            
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
            
            result = f"# Client Details\n\n"
            result += f"- Description: {client.get('description', 'N/A')}\n"
            result += f"- MAC: {client.get('mac')}\n"
            result += f"- IP: {client.get('ip')}\n"
            result += f"- IPv6: {client.get('ip6')}\n"
            result += f"- VLAN: {client.get('vlan')}\n"
            result += f"- Status: {client.get('status')}\n"
            result += f"- Last Seen: {client.get('lastSeen')}\n"
            
            if client.get('ssid'):
                result += f"\n## Wireless Info\n"
                result += f"- SSID: {client.get('ssid')}\n"
                result += f"- OS: {client.get('os')}\n"
                result += f"- Device Type: {client.get('deviceTypePrediction')}\n"
            
            if client.get('usage'):
                result += f"\n## Usage\n"
                result += f"- Sent: {client['usage'].get('sent', 0):,} bytes\n"
                result += f"- Received: {client['usage'].get('recv', 0):,} bytes\n"
            
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
            
            result = f"# Client Application Usage (Last {timespan/3600:.1f} hours)\n\n"
            
            for client in usage:
                result += f"## Client: {client.get('clientId')}\n"
                if client.get('applicationUsage'):
                    for app in client['applicationUsage'][:5]:  # Top 5 apps
                        result += f"- {app.get('application')}: "
                        result += f"Sent {app.get('sent', 0):,}, "
                        result += f"Recv {app.get('recv', 0):,} bytes\n"
                result += "\n"
            
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
            
            result = f"# Client Bandwidth Usage History\n\n"
            
            for entry in history[:10]:  # Show first 10
                result += f"## {entry.get('ts')}\n"
                result += f"- Total: {entry.get('total', 0):,} bytes\n"
                result += f"- Upstream: {entry.get('upstream', 0):,} bytes\n"
                result += f"- Downstream: {entry.get('downstream', 0):,} bytes\n"
                result += "\n"
            
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
            
            result = f"# Network Clients Overview (Last {timespan/3600:.1f} hours)\n\n"
            result += f"## Counts\n"
            result += f"- Total Clients: {overview.get('counts', {}).get('total', 0)}\n"
            
            if overview.get('counts', {}).get('byStatus'):
                result += f"\n## By Status\n"
                for status, count in overview['counts']['byStatus'].items():
                    result += f"- {status}: {count}\n"
            
            if overview.get('usages'):
                result += f"\n## Usage\n"
                result += f"- Average: {overview['usages'].get('average', 0):,} bytes\n"
                result += f"- With Heavy Usage: {overview['usages'].get('withHeavyUsage', 0)}\n"
            
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
            
            result = f"# Client Usage Histories\n\n"
            
            for client in histories:
                result += f"## Client: {client.get('clientId')}\n"
                if client.get('usageHistory'):
                    for entry in client['usageHistory'][:3]:  # First 3 entries
                        result += f"- {entry.get('ts')}: "
                        result += f"Sent {entry.get('sent', 0):,}, "
                        result += f"Recv {entry.get('received', 0):,} bytes\n"
                result += "\n"
            
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
            
            result = f"# Network Policies by Client\n\n"
            
            for policy in policies[:20]:  # Show first 20
                result += f"## Client: {policy.get('clientId')}\n"
                result += f"- Name: {policy.get('name')}\n"
                result += f"- Assigned: {policy.get('assigned')}\n"
                result += f"- Group Policy ID: {policy.get('groupPolicyId')}\n"
                result += "\n"
            
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
            
            result = f"# Network Alert Settings\n\n"
            
            if settings.get('defaultDestinations'):
                result += f"## Default Destinations\n"
                dest = settings['defaultDestinations']
                if dest.get('emails'):
                    result += f"- Emails: {', '.join(dest['emails'])}\n"
                if dest.get('smsNumbers'):
                    result += f"- SMS: {', '.join(dest['smsNumbers'])}\n"
                if dest.get('allAdmins'):
                    result += f"- All Admins: {dest['allAdmins']}\n"
                if dest.get('snmp'):
                    result += f"- SNMP: {dest['snmp']}\n"
                result += "\n"
            
            if settings.get('alerts'):
                result += f"## Alert Types ({len(settings['alerts'])} configured)\n"
                for alert in settings['alerts'][:5]:  # Show first 5
                    result += f"- {alert.get('type')}: {alert.get('enabled')}\n"
                    if alert.get('alertDestinations'):
                        result += f"  Destinations: {alert['alertDestinations']}\n"
                result += "\n"
            
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
            
            result = f"# NetFlow Settings\n\n"
            result += f"- Reporting Enabled: {netflow.get('reportingEnabled')}\n"
            
            if netflow.get('collectorIp'):
                result += f"- Collector IP: {netflow.get('collectorIp')}\n"
            if netflow.get('collectorPort'):
                result += f"- Collector Port: {netflow.get('collectorPort')}\n"
            if netflow.get('etaEnabled') is not None:
                result += f"- ETA Enabled: {netflow.get('etaEnabled')}\n"
            if netflow.get('etaDstPort'):
                result += f"- ETA Destination Port: {netflow.get('etaDstPort')}\n"
            
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
            
            result = f"# Staged Upgrade Group: {group.get('name', 'Unnamed')}\n\n"
            result += f"- ID: {group.get('id')}\n"
            result += f"- Description: {group.get('description')}\n"
            result += f"- Is Default: {group.get('isDefault')}\n"
            
            if group.get('assignedDevices'):
                result += f"\n## Assigned Devices ({len(group['assignedDevices'])})\n"
                for device in group['assignedDevices'][:5]:  # Show first 5
                    result += f"- {device.get('name')} ({device.get('serial')})\n"
            
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
            
            result = f"# Staged Upgrade Groups ({len(groups)} total)\n\n"
            
            for group in groups:
                result += f"## {group.get('name', 'Unnamed')}\n"
                result += f"- ID: {group.get('id')}\n"
                result += f"- Is Default: {group.get('isDefault')}\n"
                result += f"- Devices: {len(group.get('assignedDevices', []))}\n"
                result += "\n"
            
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
            
            result = f"# Staged Upgrade Stages\n\n"
            
            for stage in stages:
                result += f"## {stage.get('name', 'Unnamed')}\n"
                
                if stage.get('milestones'):
                    result += f"### Milestones\n"
                    for milestone in stage['milestones']:
                        result += f"- {milestone.get('action')}: "
                        result += f"{milestone.get('scheduledFor')}\n"
                
                if stage.get('groups'):
                    result += f"### Groups\n"
                    for group in stage['groups']:
                        result += f"- {group.get('name')}\n"
                
                result += "\n"
            
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
