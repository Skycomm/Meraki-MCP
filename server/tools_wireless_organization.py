"""
Wireless Organization-wide Analytics Tools for the Cisco Meraki MCP Server.
Implements organization-level wireless analytics, packet loss monitoring, and overview tools.
Previously named tools_wireless_final.py
"""

from typing import Optional, List, Dict, Any
import json

# Global variables to store app and meraki client
app = None
meraki_client = None

def register_wireless_final_tools(mcp_app, meraki):
    """
    Register organization-wide wireless analytics tools with the MCP server.
    Includes packet loss monitoring, device analytics, and organization overviews.
    
    Args:
        mcp_app: MCP server instance
        meraki: Meraki client instance
    """
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    
    # Register all organization-wide wireless analytics tool handlers
    # register_update_alternate_mgmt_tools()  # Already in complete
    # register_device_type_policies_tools()  # Already in complete
    register_location_receivers_tools()
    register_air_marshal_settings_tools()
    register_organization_packet_loss_tools()
    register_organization_overview_tools()

# ==================== UPDATE ALTERNATE MANAGEMENT ====================

def register_update_alternate_mgmt_tools():
    """Register update alternate management interface tools."""
    
    @app.tool(
        name="update_network_wireless_alternate_management_interface",
        description="📡🔧 Update alternate management interface settings for wireless network"
    )
    def update_network_wireless_alternate_management_interface(
        network_id: str,
        enabled: bool,
        vlan_id: Optional[int] = None,
        protocols: Optional[str] = None,
        access_points: Optional[str] = None
    ):
        """Update alternate management interface configuration."""
        try:
            kwargs = {'enabled': enabled}
            
            if vlan_id and enabled:
                kwargs['vlanId'] = vlan_id
            
            if protocols and enabled:
                kwargs['protocols'] = json.loads(protocols) if isinstance(protocols, str) else protocols
            
            if access_points and enabled:
                kwargs['accessPoints'] = json.loads(access_points) if isinstance(access_points, str) else access_points
            
            result = meraki_client.dashboard.wireless.updateNetworkWirelessAlternateManagementInterface(
                network_id, **kwargs
            )
            
            status = "Enabled ✅" if result.get('enabled') else "Disabled ❌"
            return f"✅ Updated alternate management interface - {status}"
            
        except Exception as e:
            return f"❌ Error updating alternate management interface: {str(e)}"

# ==================== DEVICE TYPE GROUP POLICIES ====================

def register_device_type_policies_tools():
    """Register additional device type group policy tools."""
    
    @app.tool(
        name="get_network_wireless_ssid_device_type_group_policies",
        description="📡📱 Get device type group policies for a wireless SSID"
    )
    def get_network_wireless_ssid_device_type_group_policies(
        network_id: str,
        number: str
    ):
        """Get SSID device type group policies."""
        try:
            result = meraki_client.dashboard.wireless.getNetworkWirelessSsidDeviceTypeGroupPolicies(
                network_id, number
            )
            
            response = f"# 📡 SSID {number} - Device Type Group Policies\n\n"
            response += f"**Enabled**: {result.get('enabled', False)}\n"
            
            if result.get('enabled') and result.get('deviceTypePolicies'):
                response += f"\n## Device Policies ({len(result.get('deviceTypePolicies'))})\n"
                for policy in result.get('deviceTypePolicies', []):
                    response += f"- **Device Type**: {policy.get('deviceType')}\n"
                    response += f"  - Policy: {policy.get('devicePolicy')}\n"
                    if policy.get('groupPolicyId'):
                        response += f"  - Group Policy ID: {policy.get('groupPolicyId')}\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error getting device type policies: {str(e)}"
    
    @app.tool(
        name="update_network_wireless_ssid_device_type_group_policies",
        description="📡📱 Update device type group policies for a wireless SSID"
    )
    def update_network_wireless_ssid_device_type_group_policies(
        network_id: str,
        number: str,
        enabled: bool,
        device_type_policies: Optional[str] = None
    ):
        """Update SSID device type group policies."""
        try:
            kwargs = {'enabled': enabled}
            
            if device_type_policies and enabled:
                kwargs['deviceTypePolicies'] = json.loads(device_type_policies) if isinstance(device_type_policies, str) else device_type_policies
            
            result = meraki_client.dashboard.wireless.updateNetworkWirelessSsidDeviceTypeGroupPolicies(
                network_id, number, **kwargs
            )
            
            status = "Enabled ✅" if result.get('enabled') else "Disabled ❌"
            return f"✅ Updated SSID {number} device type policies - {status}"
            
        except Exception as e:
            return f"❌ Error updating device type policies: {str(e)}"

# ==================== LOCATION SCANNING RECEIVERS ====================

def register_location_receivers_tools():
    """Register location scanning receiver tools."""
    
    @app.tool(
        name="get_organization_wireless_location_scanning_receivers",
        description="📡📍 Get location scanning receivers for organization"
    )
    def get_organization_wireless_location_scanning_receivers(
        organization_id: str
    ):
        """Get organization location scanning receivers."""
        try:
            result = meraki_client.dashboard.wireless.getOrganizationWirelessLocationScanningReceivers(
                organization_id
            )
            
            response = f"# 📍 Location Scanning Receivers\n\n"
            
            receivers = result
            if receivers:
                response += f"**Total Receivers**: {len(receivers)}\n\n"
                for receiver in receivers:
                    response += f"## Receiver: {receiver.get('name')}\n"
                    response += f"- **ID**: {receiver.get('receiverId')}\n"
                    response += f"- **URL**: {receiver.get('url')}\n"
                    response += f"- **Networks**: {len(receiver.get('networks', []))}\n"
            else:
                response += "No location scanning receivers configured\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error getting location receivers: {str(e)}"
    
    @app.tool(
        name="create_organization_wireless_location_scanning_receiver",
        description="📡📍 Create a location scanning receiver for organization"
    )
    def create_organization_wireless_location_scanning_receiver(
        organization_id: str,
        name: str,
        url: str,
        secret: str,
        networks: Optional[str] = None
    ):
        """Create organization location scanning receiver."""
        try:
            kwargs = {
                'name': name,
                'url': url,
                'secret': secret
            }
            
            if networks:
                kwargs['networks'] = json.loads(networks) if isinstance(networks, str) else networks
            
            result = meraki_client.dashboard.wireless.createOrganizationWirelessLocationScanningReceiver(
                organization_id, **kwargs
            )
            
            return f"✅ Created location receiver '{result.get('name')}' - ID: {result.get('receiverId')}"
            
        except Exception as e:
            return f"❌ Error creating location receiver: {str(e)}"
    
    @app.tool(
        name="update_organization_wireless_location_scanning_receiver",
        description="📡📍 Update a location scanning receiver for organization"
    )
    def update_organization_wireless_location_scanning_receiver(
        organization_id: str,
        receiver_id: str,
        name: Optional[str] = None,
        url: Optional[str] = None,
        secret: Optional[str] = None,
        networks: Optional[str] = None
    ):
        """Update organization location scanning receiver."""
        try:
            kwargs = {}
            
            if name:
                kwargs['name'] = name
            if url:
                kwargs['url'] = url
            if secret:
                kwargs['secret'] = secret
            if networks:
                kwargs['networks'] = json.loads(networks) if isinstance(networks, str) else networks
            
            result = meraki_client.dashboard.wireless.updateOrganizationWirelessLocationScanningReceiver(
                organization_id, receiver_id, **kwargs
            )
            
            return f"✅ Updated location receiver {receiver_id}"
            
        except Exception as e:
            return f"❌ Error updating location receiver: {str(e)}"
    
    @app.tool(
        name="delete_organization_wireless_location_scanning_receiver",
        description="📡📍 Delete a location scanning receiver from organization"
    )
    def delete_organization_wireless_location_scanning_receiver(
        organization_id: str,
        receiver_id: str
    ):
        """Delete organization location scanning receiver."""
        try:
            meraki_client.dashboard.wireless.deleteOrganizationWirelessLocationScanningReceiver(
                organization_id, receiver_id
            )
            
            return f"✅ Deleted location receiver {receiver_id}"
            
        except Exception as e:
            return f"❌ Error deleting location receiver: {str(e)}"
    
    @app.tool(
        name="get_organization_wireless_location_scanning_by_network",
        description="📡📍 Get location scanning settings by network for organization"
    )
    def get_organization_wireless_location_scanning_by_network(
        organization_id: str,
        per_page: Optional[int] = 1000
    ):
        """Get organization location scanning settings by network."""
        try:
            result = meraki_client.dashboard.wireless.getOrganizationWirelessLocationScanningByNetwork(
                organization_id,
                perPage=per_page
            )
            
            response = f"# 📍 Location Scanning by Network\n\n"
            
            networks = result
            if networks:
                response += f"**Total Networks**: {len(networks)}\n\n"
                for network in networks[:10]:  # Show first 10
                    response += f"- **{network.get('name')}**\n"
                    response += f"  - Analytics: {network.get('analyticsEnabled')}\n"
                    response += f"  - Scanning API: {network.get('scanningApiEnabled')}\n"
            else:
                response += "No network location scanning configured\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error getting location scanning by network: {str(e)}"

# ==================== AIR MARSHAL SETTINGS BY NETWORK ====================

def register_air_marshal_settings_tools():
    """Register Air Marshal settings by network tools."""
    
    @app.tool(
        name="get_organization_wireless_air_marshal_settings_by_network",
        description="📡🛡️ Get Air Marshal settings by network for organization"
    )
    def get_organization_wireless_air_marshal_settings_by_network(
        organization_id: str,
        network_ids: Optional[str] = None,
        per_page: Optional[int] = 1000
    ):
        """Get organization Air Marshal settings by network."""
        try:
            kwargs = {'perPage': per_page}
            
            if network_ids:
                kwargs['networkIds'] = json.loads(network_ids) if isinstance(network_ids, str) else network_ids
            
            result = meraki_client.dashboard.wireless.getOrganizationWirelessAirMarshalSettingsByNetwork(
                organization_id, **kwargs
            )
            
            response = f"# 🛡️ Air Marshal Settings by Network\n\n"
            
            items = result.get('items', [])
            if items:
                response += f"**Total Networks**: {len(items)}\n\n"
                for network in items[:10]:  # Show first 10
                    response += f"## Network: {network.get('network', {}).get('name')}\n"
                    response += f"- **Default Policy**: {network.get('defaultPolicy')}\n"
                    response += f"- **Whitelist**: {len(network.get('whitelist', []))} entries\n"
                    response += f"- **Rules**: {len(network.get('rules', []))} configured\n\n"
            else:
                response += "No Air Marshal settings configured\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error getting Air Marshal settings by network: {str(e)}"

# ==================== ORGANIZATION PACKET LOSS ====================

def register_organization_packet_loss_tools():
    """Register organization packet loss analysis tools."""
    
    @app.tool(
        name="get_organization_wireless_devices_packet_loss_by_client",
        description="📡📉 Get packet loss by client for organization wireless devices"
    )
    def get_organization_wireless_devices_packet_loss_by_client(
        organization_id: str,
        network_ids: Optional[str] = None,
        ssids: Optional[str] = None,
        bands: Optional[str] = None,
        per_page: Optional[int] = 1000,
        timespan: Optional[int] = 86400
    ):
        """Get organization wireless packet loss by client."""
        try:
            kwargs = {'perPage': per_page}
            
            if network_ids:
                kwargs['networkIds'] = json.loads(network_ids) if isinstance(network_ids, str) else network_ids
            if ssids:
                kwargs['ssids'] = json.loads(ssids) if isinstance(ssids, str) else ssids
            if bands:
                kwargs['bands'] = json.loads(bands) if isinstance(bands, str) else bands
            if timespan:
                kwargs['timespan'] = timespan
            
            result = meraki_client.dashboard.wireless.getOrganizationWirelessDevicesPacketLossByClient(
                organization_id, **kwargs
            )
            
            response = f"# 📉 Packet Loss by Client\n\n"
            response += f"**Timespan**: {timespan/3600:.1f} hours\n\n"
            
            clients = result
            if clients:
                response += f"**Total Clients**: {len(clients)}\n\n"
                
                # Show top 10 clients with highest packet loss
                sorted_clients = sorted(clients, key=lambda x: x.get('lossPercentage', 0), reverse=True)
                response += "## Top 10 Clients with Packet Loss\n"
                for client in sorted_clients[:10]:
                    response += f"- **{client.get('mac')}**\n"
                    response += f"  - Loss: {client.get('lossPercentage', 0):.1f}%\n"
                    response += f"  - Network: {client.get('network', {}).get('name')}\n"
                    response += f"  - Device: {client.get('device', {}).get('name')}\n"
            else:
                response += "No packet loss data available\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error getting packet loss by client: {str(e)}"
    
    @app.tool(
        name="get_organization_wireless_devices_packet_loss_by_device",
        description="📡📉 Get packet loss by device for organization wireless"
    )
    def get_organization_wireless_devices_packet_loss_by_device(
        organization_id: str,
        network_ids: Optional[str] = None,
        serials: Optional[str] = None,
        bands: Optional[str] = None,
        ssids: Optional[str] = None,
        per_page: Optional[int] = 1000,
        timespan: Optional[int] = 86400
    ):
        """Get organization wireless packet loss by device."""
        try:
            kwargs = {'perPage': per_page}
            
            if network_ids:
                kwargs['networkIds'] = json.loads(network_ids) if isinstance(network_ids, str) else network_ids
            if serials:
                kwargs['serials'] = json.loads(serials) if isinstance(serials, str) else serials
            if bands:
                kwargs['bands'] = json.loads(bands) if isinstance(bands, str) else bands
            if ssids:
                kwargs['ssids'] = json.loads(ssids) if isinstance(ssids, str) else ssids
            if timespan:
                kwargs['timespan'] = timespan
            
            result = meraki_client.dashboard.wireless.getOrganizationWirelessDevicesPacketLossByDevice(
                organization_id, **kwargs
            )
            
            response = f"# 📉 Packet Loss by Device\n\n"
            response += f"**Timespan**: {timespan/3600:.1f} hours\n\n"
            
            devices = result
            if devices:
                response += f"**Total Devices**: {len(devices)}\n\n"
                
                # Show devices with highest packet loss
                sorted_devices = sorted(devices, key=lambda x: x.get('lossPercentage', 0), reverse=True)
                response += "## Devices with Highest Packet Loss\n"
                for device in sorted_devices[:10]:
                    response += f"- **{device.get('name')}** ({device.get('serial')})\n"
                    response += f"  - Loss: {device.get('lossPercentage', 0):.1f}%\n"
                    response += f"  - Network: {device.get('network', {}).get('name')}\n"
                    response += f"  - Model: {device.get('model')}\n"
            else:
                response += "No packet loss data available\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error getting packet loss by device: {str(e)}"
    
    @app.tool(
        name="get_organization_wireless_devices_packet_loss_by_network",
        description="📡📉 Get packet loss by network for organization wireless"
    )
    def get_organization_wireless_devices_packet_loss_by_network(
        organization_id: str,
        network_ids: Optional[str] = None,
        serials: Optional[str] = None,
        bands: Optional[str] = None,
        ssids: Optional[str] = None,
        per_page: Optional[int] = 1000,
        timespan: Optional[int] = 86400
    ):
        """Get organization wireless packet loss by network."""
        try:
            kwargs = {'perPage': per_page}
            
            if network_ids:
                kwargs['networkIds'] = json.loads(network_ids) if isinstance(network_ids, str) else network_ids
            if serials:
                kwargs['serials'] = json.loads(serials) if isinstance(serials, str) else serials
            if bands:
                kwargs['bands'] = json.loads(bands) if isinstance(bands, str) else bands
            if ssids:
                kwargs['ssids'] = json.loads(ssids) if isinstance(ssids, str) else ssids
            if timespan:
                kwargs['timespan'] = timespan
            
            result = meraki_client.dashboard.wireless.getOrganizationWirelessDevicesPacketLossByNetwork(
                organization_id, **kwargs
            )
            
            response = f"# 📉 Packet Loss by Network\n\n"
            response += f"**Timespan**: {timespan/3600:.1f} hours\n\n"
            
            networks = result
            if networks:
                response += f"**Total Networks**: {len(networks)}\n\n"
                
                # Show networks with highest packet loss
                sorted_networks = sorted(networks, key=lambda x: x.get('lossPercentage', 0), reverse=True)
                response += "## Networks with Highest Packet Loss\n"
                for network in sorted_networks:
                    response += f"- **{network.get('name')}**\n"
                    response += f"  - Loss: {network.get('lossPercentage', 0):.1f}%\n"
                    response += f"  - Clients: {network.get('clientCount', 0)}\n"
                    response += f"  - Devices: {network.get('deviceCount', 0)}\n"
            else:
                response += "No packet loss data available\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error getting packet loss by network: {str(e)}"

# ==================== ORGANIZATION OVERVIEW ====================

def register_organization_overview_tools():
    """Register organization wireless overview tools."""
    
    @app.tool(
        name="get_organization_wireless_clients_overview_by_device",
        description="📡👥 Get wireless clients overview by device for organization"
    )
    def get_organization_wireless_clients_overview_by_device(
        organization_id: str,
        network_ids: Optional[str] = None,
        serials: Optional[str] = None,
        per_page: Optional[int] = 1000,
        timespan: Optional[int] = 86400
    ):
        """Get organization wireless clients overview by device."""
        try:
            kwargs = {'perPage': per_page}
            
            if network_ids:
                kwargs['networkIds'] = json.loads(network_ids) if isinstance(network_ids, str) else network_ids
            if serials:
                kwargs['serials'] = json.loads(serials) if isinstance(serials, str) else serials
            if timespan:
                kwargs['timespan'] = timespan
            
            result = meraki_client.dashboard.wireless.getOrganizationWirelessClientsOverviewByDevice(
                organization_id, **kwargs
            )
            
            response = f"# 👥 Wireless Clients Overview by Device\n\n"
            response += f"**Timespan**: {timespan/3600:.1f} hours\n\n"
            
            items = result.get('items', [])
            if items:
                response += f"**Total Devices**: {len(items)}\n\n"
                
                # Sort by client count
                sorted_devices = sorted(items, key=lambda x: x.get('usage', {}).get('clientCount', 0), reverse=True)
                response += "## Top Devices by Client Count\n"
                for device in sorted_devices[:10]:
                    response += f"- **{device.get('device', {}).get('name')}**\n"
                    response += f"  - Serial: {device.get('device', {}).get('serial')}\n"
                    response += f"  - Clients: {device.get('usage', {}).get('clientCount', 0)}\n"
                    response += f"  - Usage: {device.get('usage', {}).get('totalMbps', 0):.1f} Mbps\n"
                    response += f"  - Network: {device.get('network', {}).get('name')}\n"
            else:
                response += "No client overview data available\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error getting clients overview by device: {str(e)}"
    
    @app.tool(
        name="get_organization_wireless_ssids_statuses_by_device",
        description="📡📶 Get SSID statuses by device for organization"
    )
    def get_organization_wireless_ssids_statuses_by_device(
        organization_id: str,
        network_ids: Optional[str] = None,
        serials: Optional[str] = None,
        bssids: Optional[str] = None,
        per_page: Optional[int] = 500  # API limit: must be between 3 and 500
    ):
        """Get organization SSID statuses by device."""
        try:
            kwargs = {'perPage': per_page}
            
            if network_ids:
                kwargs['networkIds'] = json.loads(network_ids) if isinstance(network_ids, str) else network_ids
            if serials:
                kwargs['serials'] = json.loads(serials) if isinstance(serials, str) else serials
            if bssids:
                kwargs['bssids'] = json.loads(bssids) if isinstance(bssids, str) else bssids
            
            result = meraki_client.dashboard.wireless.getOrganizationWirelessSsidsStatusesByDevice(
                organization_id, **kwargs
            )
            
            response = f"# 📶 SSID Statuses by Device\n\n"
            
            items = result.get('items', [])
            if items:
                response += f"**Total Device SSIDs**: {len(items)}\n\n"
                
                # Group by device
                devices = {}
                for item in items:
                    device_name = item.get('device', {}).get('name', 'Unknown')
                    if device_name not in devices:
                        devices[device_name] = []
                    devices[device_name].append(item)
                
                response += f"## Devices ({len(devices)})\n"
                for device_name, ssids in list(devices.items())[:5]:  # Show first 5 devices
                    response += f"\n### {device_name}\n"
                    for ssid in ssids[:3]:  # Show first 3 SSIDs per device
                        response += f"- **{ssid.get('ssid', {}).get('name')}**\n"
                        response += f"  - Enabled: {ssid.get('basicServiceSet', {}).get('enabled')}\n"
                        response += f"  - Visible: {ssid.get('basicServiceSet', {}).get('visible')}\n"
                        response += f"  - Band: {ssid.get('basicServiceSet', {}).get('band')}\n"
                        response += f"  - Channel: {ssid.get('basicServiceSet', {}).get('channel')}\n"
            else:
                response += "No SSID status data available\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error getting SSID statuses by device: {str(e)}"
    
    @app.tool(
        name="get_organization_wireless_devices_channel_utilization_by_device",
        description="📡📊 Get channel utilization by device for organization"
    )
    def get_organization_wireless_devices_channel_utilization_by_device(
        organization_id: str,
        network_ids: Optional[str] = None,
        serials: Optional[str] = None,
        per_page: Optional[int] = 1000,
        timespan: Optional[int] = 86400
    ):
        """Get organization wireless channel utilization by device."""
        try:
            kwargs = {'perPage': per_page}
            
            if network_ids:
                kwargs['networkIds'] = json.loads(network_ids) if isinstance(network_ids, str) else network_ids
            if serials:
                kwargs['serials'] = json.loads(serials) if isinstance(serials, str) else serials
            if timespan:
                kwargs['timespan'] = timespan
            
            result = meraki_client.dashboard.wireless.getOrganizationWirelessDevicesChannelUtilizationByDevice(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Channel Utilization by Device\n\n"
            response += f"**Timespan**: {timespan/3600:.1f} hours\n\n"
            
            devices = result
            if devices:
                response += f"**Total Devices**: {len(devices)}\n\n"
                
                # Sort by total utilization
                sorted_devices = sorted(devices, 
                    key=lambda x: x.get('byBand', [{}])[0].get('utilization', {}).get('total', 0) if x.get('byBand') else 0, 
                    reverse=True)
                
                response += "## Devices with Highest Channel Utilization\n"
                for device in sorted_devices[:10]:
                    response += f"- **{device.get('device', {}).get('name')}** ({device.get('device', {}).get('serial')})\n"
                    response += f"  - Network: {device.get('network', {}).get('name')}\n"
                    
                    by_band = device.get('byBand', [])
                    for band_data in by_band:
                        band = band_data.get('band')
                        util = band_data.get('utilization', {})
                        response += f"  - **{band} Band**:\n"
                        response += f"    - Total: {util.get('total', 0):.1f}%\n"
                        response += f"    - WiFi: {util.get('wifi', 0):.1f}%\n"
                        response += f"    - Non-WiFi: {util.get('nonWifi', 0):.1f}%\n"
            else:
                response += "No channel utilization data available\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error getting channel utilization by device: {str(e)}"
    
    @app.tool(
        name="get_organization_wireless_devices_channel_utilization_by_network",
        description="📡📊 Get channel utilization by network for organization"
    )
    def get_organization_wireless_devices_channel_utilization_by_network(
        organization_id: str,
        network_ids: Optional[str] = None,
        serials: Optional[str] = None,
        per_page: Optional[int] = 1000,
        timespan: Optional[int] = 86400
    ):
        """Get organization wireless channel utilization by network."""
        try:
            kwargs = {'perPage': per_page}
            
            if network_ids:
                kwargs['networkIds'] = json.loads(network_ids) if isinstance(network_ids, str) else network_ids
            if serials:
                kwargs['serials'] = json.loads(serials) if isinstance(serials, str) else serials
            if timespan:
                kwargs['timespan'] = timespan
            
            result = meraki_client.dashboard.wireless.getOrganizationWirelessDevicesChannelUtilizationByNetwork(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Channel Utilization by Network\n\n"
            response += f"**Timespan**: {timespan/3600:.1f} hours\n\n"
            
            networks = result
            if networks:
                response += f"**Total Networks**: {len(networks)}\n\n"
                
                # Sort by average utilization
                sorted_networks = sorted(networks, 
                    key=lambda x: x.get('byBand', [{}])[0].get('utilization', {}).get('total', 0) if x.get('byBand') else 0,
                    reverse=True)
                
                response += "## Networks with Highest Channel Utilization\n"
                for network in sorted_networks:
                    response += f"- **{network.get('network', {}).get('name')}**\n"
                    
                    by_band = network.get('byBand', [])
                    for band_data in by_band:
                        band = band_data.get('band')
                        util = band_data.get('utilization', {})
                        response += f"  - **{band} Band**:\n"
                        response += f"    - Total: {util.get('total', 0):.1f}%\n"
                        response += f"    - WiFi: {util.get('wifi', 0):.1f}%\n"
                        response += f"    - Non-WiFi: {util.get('nonWifi', 0):.1f}%\n"
            else:
                response += "No channel utilization data available\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error getting channel utilization by network: {str(e)}"