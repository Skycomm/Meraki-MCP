"""
Wireless Infrastructure and RADSEC Tools for the Cisco Meraki MCP Server.
Implements RADSEC certificates, device management, and infrastructure configuration.
Previously named tools_wireless_missing.py
"""

from typing import Optional, List, Dict, Any
import json

# Global variables
app = None
meraki_client = None

def register_wireless_missing_tools(mcp_app, meraki):
    """
    Register wireless infrastructure and RADSEC tools.
    Includes RADSEC certificates, device management, and infrastructure settings.
    
    Args:
        mcp_app: MCP server instance
        meraki: Meraki client instance
    """
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    
    register_missing_device_tools()
    register_missing_network_tools()
    register_missing_organization_tools()

# ==================== MISSING DEVICE TOOLS (2) ====================

def register_missing_device_tools():
    """Register missing device wireless tools."""
    
    @app.tool(
        name="get_device_wireless_alternate_management_interface",
        description="📡🔧 Get alternate management interface settings for wireless device"
    )
    def get_device_wireless_alternate_management_interface(serial: str):
        """Get device alternate management interface settings."""
        try:
            result = meraki_client.dashboard.wireless.getDeviceWirelessAlternateManagementInterface(serial)
            
            response = f"# 📡 Device {serial} - Alternate Management Interface\n\n"
            response += f"**Enabled**: {result.get('enabled', False)}\n"
            
            if result.get('enabled'):
                response += f"**VLAN ID**: {result.get('vlanId', 'N/A')}\n"
                protocols = result.get('protocols', [])
                if protocols:
                    response += f"**Protocols**: {', '.join(protocols)}\n"
                    
                aps = result.get('accessPoints', [])
                if aps:
                    response += f"\n## Access Points ({len(aps)})\n"
                    for ap in aps[:5]:  # Show first 5
                        response += f"- {ap.get('serial', 'Unknown')}: {ap.get('alternateManagementIp', 'N/A')}\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error getting alternate management interface: {str(e)}"
    
    @app.tool(
        name="update_device_wireless_alternate_management_interface",
        description="📡🔧 Update alternate management interface settings for wireless device"
    )
    def update_device_wireless_alternate_management_interface(
        serial: str,
        enabled: bool,
        vlan_id: Optional[int] = None,
        protocols: Optional[str] = None
    ):
        """Update device alternate management interface settings."""
        try:
            kwargs = {'enabled': enabled}
            
            if enabled and vlan_id:
                kwargs['vlanId'] = vlan_id
            
            if enabled and protocols:
                kwargs['protocols'] = json.loads(protocols) if isinstance(protocols, str) else protocols
            
            result = meraki_client.dashboard.wireless.updateDeviceWirelessAlternateManagementInterface(
                serial, **kwargs
            )
            
            status = "Enabled ✅" if result.get('enabled') else "Disabled ❌"
            return f"✅ Updated alternate management interface for device {serial} - {status}"
            
        except Exception as e:
            return f"❌ Error updating alternate management interface: {str(e)}"
    
    @app.tool(
        name="get_device_wireless_alternate_management_interface_ipv6",
        description="📡🔧 Get IPv6 alternate management interface for wireless device"
    )
    def get_device_wireless_alternate_management_interface_ipv6(serial: str):
        """Get device IPv6 alternate management interface."""
        try:
            result = meraki_client.dashboard.wireless.getDeviceWirelessAlternateManagementInterfaceIpv6(serial)
            
            response = f"# 📡 Device {serial} - IPv6 Alternate Management\n\n"
            addresses = result.get('addresses', [])
            
            if addresses:
                response += f"## IPv6 Addresses ({len(addresses)})\n"
                for addr in addresses:
                    response += f"- **Address**: {addr.get('address', 'N/A')}\n"
                    response += f"  - Protocol: {addr.get('protocol', 'N/A')}\n"
                    response += f"  - Assignment: {addr.get('assignmentMode', 'N/A')}\n"
                    response += f"  - Gateway: {addr.get('gateway', 'N/A')}\n"
                    response += f"  - Prefix: {addr.get('prefix', 'N/A')}\n\n"
            else:
                response += "No IPv6 addresses configured\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error getting IPv6 alternate management: {str(e)}"
    
    @app.tool(
        name="update_device_wireless_alternate_management_interface_ipv6",
        description="📡🔧 Update IPv6 alternate management interface for wireless device"
    )
    def update_device_wireless_alternate_management_interface_ipv6(
        serial: str,
        addresses: Optional[str] = None
    ):
        """Update device IPv6 alternate management interface."""
        try:
            kwargs = {}
            if addresses:
                kwargs['addresses'] = json.loads(addresses) if isinstance(addresses, str) else addresses
            
            result = meraki_client.dashboard.wireless.updateDeviceWirelessAlternateManagementInterfaceIpv6(
                serial, **kwargs
            )
            
            return f"✅ Updated IPv6 alternate management for device {serial}"
            
        except Exception as e:
            return f"❌ Error updating IPv6 alternate management: {str(e)}"
    
    @app.tool(
        name="get_device_wireless_latency_stats",
        description="📡📊 Get latency statistics for a wireless device"
    )
    def get_device_wireless_latency_stats(
        serial: str,
        t0: Optional[str] = None,
        t1: Optional[str] = None,
        timespan: Optional[float] = 86400,
        band: Optional[str] = None,
        ssid: Optional[int] = None,
        vlan: Optional[int] = None,
        ap_tag: Optional[str] = None,
        fields: Optional[str] = None
    ):
        """Get device wireless latency statistics."""
        try:
            kwargs = {}
            if t0:
                kwargs['t0'] = t0
            if t1:
                kwargs['t1'] = t1
            if timespan:
                kwargs['timespan'] = timespan
            if band:
                kwargs['band'] = band
            if ssid is not None:
                kwargs['ssid'] = ssid
            if vlan is not None:
                kwargs['vlan'] = vlan
            if ap_tag:
                kwargs['apTag'] = ap_tag
            if fields:
                kwargs['fields'] = fields
            
            result = meraki_client.dashboard.wireless.getDeviceWirelessLatencyStats(serial, **kwargs)
            
            response = f"# 📊 Device {serial} - Latency Stats\n\n"
            if isinstance(result, dict):
                response += f"**Background Traffic**: {result.get('backgroundTraffic', {}).get('avg', 0):.1f} ms avg\n"
                response += f"**Best Effort**: {result.get('bestEffortTraffic', {}).get('avg', 0):.1f} ms avg\n"
                response += f"**Video**: {result.get('videoTraffic', {}).get('avg', 0):.1f} ms avg\n"
                response += f"**Voice**: {result.get('voiceTraffic', {}).get('avg', 0):.1f} ms avg\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error getting device latency stats: {str(e)}"

# ==================== MISSING NETWORK TOOLS (5) ====================

def register_missing_network_tools():
    """Register missing network wireless tools."""
    
    @app.tool(
        name="get_network_wireless_devices_latency_stats",
        description="📡📊 Get aggregated latency stats for all wireless devices in network (works with just network_id)"
    )
    def get_network_wireless_devices_latency_stats(
        network_id: str,
        t0: Optional[str] = None,
        t1: Optional[str] = None,
        timespan: Optional[float] = 86400,
        band: Optional[str] = None,
        ssid: Optional[int] = None,
        vlan: Optional[int] = None,
        ap_tag: Optional[str] = None,
        fields: Optional[str] = None
    ):
        """Get latency stats for all wireless devices in network."""
        try:
            kwargs = {}
            if t0:
                kwargs['t0'] = t0
            if t1:
                kwargs['t1'] = t1
            if timespan:
                kwargs['timespan'] = timespan
            if band:
                kwargs['band'] = band
            if ssid is not None:
                kwargs['ssid'] = ssid
            if vlan is not None:
                kwargs['vlan'] = vlan
            if ap_tag:
                kwargs['apTag'] = ap_tag
            if fields:
                kwargs['fields'] = fields
            
            result = meraki_client.dashboard.wireless.getNetworkWirelessDevicesLatencyStats(
                network_id, **kwargs
            )
            
            response = f"# 📊 Network Devices Latency Stats\n\n"
            if isinstance(result, list):
                response += f"**Total Devices**: {len(result)}\n\n"
                for device in result[:5]:
                    response += f"## Device: {device.get('serial')}\n"
                    stats = device.get('latencyStats', {})
                    response += f"- Background: {stats.get('backgroundTraffic', {}).get('avg', 0):.1f} ms\n"
                    response += f"- Best Effort: {stats.get('bestEffortTraffic', {}).get('avg', 0):.1f} ms\n\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error getting network devices latency stats: {str(e)}"
    
    @app.tool(
        name="get_network_wireless_electronic_shelf_label_configured_devices",
        description="📡🏷️ Get ESL configured devices for network"
    )
    def get_network_wireless_electronic_shelf_label_configured_devices(network_id: str):
        """Get ESL configured devices."""
        try:
            result = meraki_client.dashboard.wireless.getNetworkWirelessElectronicShelfLabelConfiguredDevices(
                network_id
            )
            
            response = f"# 🏷️ ESL Configured Devices\n\n"
            if isinstance(result, list):
                response += f"**Total Devices**: {len(result)}\n\n"
                for device in result:
                    response += f"- **{device.get('name')}** ({device.get('serial')})\n"
                    response += f"  - Enabled: {device.get('enabled')}\n"
                    response += f"  - Provider: {device.get('provider')}\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error getting ESL configured devices: {str(e)}"
    
    @app.tool(
        name="set_network_wireless_ethernet_ports_profiles_default",
        description="📡🔌 Set default Ethernet ports profile for network"
    )
    def set_network_wireless_ethernet_ports_profiles_default(
        network_id: str,
        profile_id: str
    ):
        """Set default Ethernet ports profile."""
        try:
            result = meraki_client.dashboard.wireless.setNetworkWirelessEthernetPortsProfilesDefault(
                network_id,
                profileId=profile_id
            )
            
            return f"✅ Set default Ethernet ports profile to {profile_id}"
            
        except Exception as e:
            return f"❌ Error setting default profile: {str(e)}"
    
    @app.tool(
        name="get_network_wireless_ethernet_ports_profile",
        description="📡🔌 Get a specific Ethernet ports profile"
    )
    def get_network_wireless_ethernet_ports_profile(
        network_id: str,
        profile_id: str
    ):
        """Get specific Ethernet ports profile."""
        try:
            result = meraki_client.dashboard.wireless.getNetworkWirelessEthernetPortsProfile(
                network_id, profile_id
            )
            
            response = f"# 🔌 Ethernet Ports Profile\n\n"
            response += f"**Name**: {result.get('name')}\n"
            response += f"**ID**: {result.get('profileId')}\n"
            response += f"**Is Default**: {result.get('isDefault', False)}\n"
            
            ports = result.get('ports', [])
            if ports:
                response += f"\n## Ports ({len(ports)})\n"
                for port in ports:
                    response += f"- **{port.get('name')}**: "
                    response += f"VLAN {port.get('vlan')}, "
                    response += f"{'Enabled' if port.get('enabled') else 'Disabled'}\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error getting Ethernet ports profile: {str(e)}"
    
    @app.tool(
        name="get_network_wireless_latency_history",
        description="📡📈 Get latency history for wireless network"
    )
    def get_network_wireless_latency_history(
        network_id: str,
        t0: Optional[str] = None,
        t1: Optional[str] = None,
        timespan: Optional[float] = 86400,
        resolution: Optional[int] = 300,
        auto_resolution: Optional[bool] = True,
        client_id: Optional[str] = None,
        device_serial: Optional[str] = None,
        ap_tag: Optional[str] = None,
        band: Optional[str] = None,
        ssid: Optional[int] = None
    ):
        """Get latency history for network."""
        try:
            kwargs = {}
            if t0:
                kwargs['t0'] = t0
            if t1:
                kwargs['t1'] = t1
            if timespan:
                kwargs['timespan'] = timespan
            if resolution:
                kwargs['resolution'] = resolution
            if auto_resolution is not None:
                kwargs['autoResolution'] = auto_resolution
            if client_id:
                kwargs['clientId'] = client_id
            if device_serial:
                kwargs['deviceSerial'] = device_serial
            if ap_tag:
                kwargs['apTag'] = ap_tag
            if band:
                kwargs['band'] = band
            if ssid is not None:
                kwargs['ssid'] = ssid
            
            result = meraki_client.dashboard.wireless.getNetworkWirelessLatencyHistory(
                network_id, **kwargs
            )
            
            response = f"# 📈 Latency History\n\n"
            response += f"**Timespan**: {timespan/3600:.1f} hours\n"
            
            if isinstance(result, list) and result:
                response += f"**Data Points**: {len(result)}\n\n"
                
                # Calculate averages
                avg_bg = sum(d.get('backgroundTraffic', {}).get('avg', 0) for d in result) / len(result)
                avg_be = sum(d.get('bestEffortTraffic', {}).get('avg', 0) for d in result) / len(result)
                
                response += f"## Average Latency\n"
                response += f"- Background: {avg_bg:.1f} ms\n"
                response += f"- Best Effort: {avg_be:.1f} ms\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error getting latency history: {str(e)}"

# ==================== MISSING ORGANIZATION TOOLS (13) ====================

def register_missing_organization_tools():
    """Register missing organization wireless tools."""
    
    @app.tool(
        name="get_org_wireless_channel_util_history_by_device",
        description="📡📊 Get channel utilization history by device and interval"
    )
    def get_organization_wireless_devices_channel_utilization_history_by_device_by_interval(
        organization_id: str,
        network_ids: Optional[str] = None,
        serials: Optional[str] = None,
        t0: Optional[str] = None,
        t1: Optional[str] = None,
        timespan: Optional[float] = 86400,
        interval: Optional[int] = 300
    ):
        """Get channel utilization history by device and interval."""
        try:
            kwargs = {}
            if network_ids:
                kwargs['networkIds'] = json.loads(network_ids) if isinstance(network_ids, str) else network_ids
            if serials:
                kwargs['serials'] = json.loads(serials) if isinstance(serials, str) else serials
            if t0:
                kwargs['t0'] = t0
            if t1:
                kwargs['t1'] = t1
            if timespan:
                kwargs['timespan'] = timespan
            if interval:
                kwargs['interval'] = interval
            
            result = meraki_client.dashboard.wireless.getOrganizationWirelessDevicesChannelUtilizationHistoryByDeviceByInterval(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Channel Utilization History by Device\n\n"
            response += f"**Timespan**: {timespan/3600:.1f} hours\n"
            response += f"**Interval**: {interval} seconds\n\n"
            
            if isinstance(result, list) and result:
                response += f"**Total Devices**: {len(result)}\n"
                for device in result[:3]:
                    response += f"\n## Device: {device.get('serial')}\n"
                    by_interval = device.get('byInterval', [])
                    if by_interval:
                        recent = by_interval[0]
                        response += f"- Latest Total Utilization: {recent.get('utilization', {}).get('total', 0):.1f}%\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error getting channel utilization history: {str(e)}"
    
    @app.tool(
        name="get_org_wireless_channel_util_history_by_network",
        description="📡📊 Get channel utilization history by network and interval"
    )
    def get_organization_wireless_devices_channel_utilization_history_by_network_by_interval(
        organization_id: str,
        network_ids: Optional[str] = None,
        serials: Optional[str] = None,
        t0: Optional[str] = None,
        t1: Optional[str] = None,
        timespan: Optional[float] = 86400,
        interval: Optional[int] = 300
    ):
        """Get channel utilization history by network and interval."""
        try:
            kwargs = {}
            if network_ids:
                kwargs['networkIds'] = json.loads(network_ids) if isinstance(network_ids, str) else network_ids
            if serials:
                kwargs['serials'] = json.loads(serials) if isinstance(serials, str) else serials
            if t0:
                kwargs['t0'] = t0
            if t1:
                kwargs['t1'] = t1
            if timespan:
                kwargs['timespan'] = timespan
            if interval:
                kwargs['interval'] = interval
            
            result = meraki_client.dashboard.wireless.getOrganizationWirelessDevicesChannelUtilizationHistoryByNetworkByInterval(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Channel Utilization History by Network\n\n"
            response += f"**Timespan**: {timespan/3600:.1f} hours\n"
            response += f"**Interval**: {interval} seconds\n\n"
            
            if isinstance(result, list) and result:
                response += f"**Total Networks**: {len(result)}\n"
                for network in result[:3]:
                    response += f"\n## Network: {network.get('network', {}).get('name')}\n"
                    by_interval = network.get('byInterval', [])
                    if by_interval:
                        recent = by_interval[0]
                        response += f"- Latest Utilization: {recent.get('utilization', {}).get('total', 0):.1f}%\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error getting channel utilization by network: {str(e)}"
    
    @app.tool(
        name="get_organization_wireless_devices_power_mode_history",
        description="📡⚡ Get power mode history for wireless devices"
    )
    def get_organization_wireless_devices_power_mode_history(
        organization_id: str,
        network_ids: Optional[str] = None,
        serials: Optional[str] = None,
        t0: Optional[str] = None,
        t1: Optional[str] = None,
        timespan: Optional[float] = 86400
    ):
        """Get power mode history for wireless devices."""
        try:
            kwargs = {}
            if network_ids:
                kwargs['networkIds'] = json.loads(network_ids) if isinstance(network_ids, str) else network_ids
            if serials:
                kwargs['serials'] = json.loads(serials) if isinstance(serials, str) else serials
            if t0:
                kwargs['t0'] = t0
            if t1:
                kwargs['t1'] = t1
            if timespan:
                kwargs['timespan'] = timespan
            
            result = meraki_client.dashboard.wireless.getOrganizationWirelessDevicesPowerModeHistory(
                organization_id, **kwargs
            )
            
            response = f"# ⚡ Power Mode History\n\n"
            response += f"**Timespan**: {timespan/3600:.1f} hours\n\n"
            
            if isinstance(result, list):
                response += f"**Total Devices**: {len(result)}\n"
                for device in result[:5]:
                    response += f"\n## Device: {device.get('serial')}\n"
                    response += f"- Network: {device.get('network', {}).get('name')}\n"
                    response += f"- Power Mode: {device.get('powerMode')}\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error getting power mode history: {str(e)}"
    
    @app.tool(
        name="get_org_wireless_radsec_authorities",
        description="📡🔒 Get RADSEC certificate authorities"
    )
    def get_organization_wireless_devices_radsec_certificates_authorities(
        organization_id: str
    ):
        """Get RADSEC certificate authorities."""
        try:
            result = meraki_client.dashboard.wireless.getOrganizationWirelessDevicesRadsecCertificatesAuthorities(
                organization_id
            )
            
            response = f"# 🔒 RADSEC Certificate Authorities\n\n"
            if isinstance(result, list):
                response += f"**Total CAs**: {len(result)}\n\n"
                for ca in result:
                    response += f"## CA: {ca.get('name')}\n"
                    response += f"- ID: {ca.get('certificateId')}\n"
                    response += f"- Root: {ca.get('root', False)}\n\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error getting RADSEC CAs: {str(e)}"
    
    @app.tool(
        name="create_org_wireless_radsec_authority",
        description="📡🔒 Create a RADSEC certificate authority"
    )
    def create_organization_wireless_devices_radsec_certificates_authority(
        organization_id: str,
        name: str,
        contents: str,
        root: Optional[bool] = False
    ):
        """Create RADSEC certificate authority."""
        try:
            result = meraki_client.dashboard.wireless.createOrganizationWirelessDevicesRadsecCertificatesAuthority(
                organization_id,
                name=name,
                contents=contents,
                root=root
            )
            
            return f"✅ Created RADSEC CA '{result.get('name')}' - ID: {result.get('certificateId')}"
            
        except Exception as e:
            return f"❌ Error creating RADSEC CA: {str(e)}"
    
    @app.tool(
        name="update_org_wireless_radsec_authorities",
        description="📡🔒 Update RADSEC certificate authorities"
    )
    def update_organization_wireless_devices_radsec_certificates_authorities(
        organization_id: str,
        certificate_ids: str
    ):
        """Update RADSEC certificate authorities."""
        try:
            ids = json.loads(certificate_ids) if isinstance(certificate_ids, str) else certificate_ids
            
            result = meraki_client.dashboard.wireless.updateOrganizationWirelessDevicesRadsecCertificatesAuthorities(
                organization_id,
                certificateIds=ids
            )
            
            return f"✅ Updated RADSEC certificate authorities"
            
        except Exception as e:
            return f"❌ Error updating RADSEC CAs: {str(e)}"
    
    @app.tool(
        name="get_org_wireless_radsec_crls",
        description="📡🔒 Get RADSEC certificate revocation lists"
    )
    def get_organization_wireless_devices_radsec_certificates_authorities_crls(
        organization_id: str
    ):
        """Get RADSEC CRLs."""
        try:
            result = meraki_client.dashboard.wireless.getOrganizationWirelessDevicesRadsecCertificatesAuthoritiesCrls(
                organization_id
            )
            
            response = f"# 🔒 RADSEC Certificate Revocation Lists\n\n"
            if isinstance(result, list):
                response += f"**Total CRLs**: {len(result)}\n"
                for crl in result:
                    response += f"- CRL ID: {crl.get('id')}\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error getting RADSEC CRLs: {str(e)}"
    
    @app.tool(
        name="get_org_wireless_radsec_crl_deltas",
        description="📡🔒 Get RADSEC CRL deltas"
    )
    def get_organization_wireless_devices_radsec_certificates_authorities_crls_deltas(
        organization_id: str
    ):
        """Get RADSEC CRL deltas."""
        try:
            result = meraki_client.dashboard.wireless.getOrganizationWirelessDevicesRadsecCertificatesAuthoritiesCrlsDeltas(
                organization_id
            )
            
            response = f"# 🔒 RADSEC CRL Deltas\n\n"
            if isinstance(result, list):
                response += f"**Total Deltas**: {len(result)}\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error getting RADSEC CRL deltas: {str(e)}"
    
    @app.tool(
        name="get_organization_wireless_devices_system_cpu_load_history",
        description="📡💻 Get CPU load history for wireless devices"
    )
    def get_organization_wireless_devices_system_cpu_load_history(
        organization_id: str,
        network_ids: Optional[str] = None,
        serials: Optional[str] = None,
        t0: Optional[str] = None,
        t1: Optional[str] = None,
        timespan: Optional[float] = 86400
    ):
        """Get CPU load history for wireless devices."""
        try:
            kwargs = {}
            if network_ids:
                kwargs['networkIds'] = json.loads(network_ids) if isinstance(network_ids, str) else network_ids
            if serials:
                kwargs['serials'] = json.loads(serials) if isinstance(serials, str) else serials
            if t0:
                kwargs['t0'] = t0
            if t1:
                kwargs['t1'] = t1
            if timespan:
                kwargs['timespan'] = timespan
            
            result = meraki_client.dashboard.wireless.getOrganizationWirelessDevicesSystemCpuLoadHistory(
                organization_id, **kwargs
            )
            
            response = f"# 💻 CPU Load History\n\n"
            response += f"**Timespan**: {timespan/3600:.1f} hours\n\n"
            
            if isinstance(result, list):
                response += f"**Total Devices**: {len(result)}\n"
                for device in result[:5]:
                    response += f"- {device.get('serial')}: {device.get('cpuPercentage', 0):.1f}% CPU\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error getting CPU load history: {str(e)}"
    
    @app.tool(
        name="get_organization_wireless_devices_wireless_controllers_by_device",
        description="📡🎮 Get wireless controllers by device"
    )
    def get_organization_wireless_devices_wireless_controllers_by_device(
        organization_id: str,
        network_ids: Optional[str] = None,
        serials: Optional[str] = None,
        per_page: Optional[int] = 1000
    ):
        """Get wireless controllers by device."""
        try:
            kwargs = {'perPage': per_page}
            if network_ids:
                kwargs['networkIds'] = json.loads(network_ids) if isinstance(network_ids, str) else network_ids
            if serials:
                kwargs['serials'] = json.loads(serials) if isinstance(serials, str) else serials
            
            result = meraki_client.dashboard.wireless.getOrganizationWirelessDevicesWirelessControllersByDevice(
                organization_id, **kwargs
            )
            
            response = f"# 🎮 Wireless Controllers by Device\n\n"
            if isinstance(result, list):
                response += f"**Total Devices**: {len(result)}\n"
                for device in result[:5]:
                    response += f"- {device.get('serial')}: {device.get('controller', {}).get('name', 'N/A')}\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error getting wireless controllers: {str(e)}"
    
    @app.tool(
        name="recalculate_organization_wireless_radio_auto_rf_channels",
        description="📡📻 Recalculate auto RF channels for organization"
    )
    def recalculate_organization_wireless_radio_auto_rf_channels(
        organization_id: str,
        serials: str
    ):
        """Recalculate auto RF channels."""
        try:
            serial_list = json.loads(serials) if isinstance(serials, str) else serials
            
            result = meraki_client.dashboard.wireless.recalculateOrganizationWirelessRadioAutoRfChannels(
                organization_id,
                serials=serial_list
            )
            
            return f"✅ Recalculated auto RF channels for {len(serial_list)} devices"
            
        except Exception as e:
            return f"❌ Error recalculating RF channels: {str(e)}"
    
    @app.tool(
        name="get_organization_wireless_rf_profiles_assignments_by_device",
        description="📡📻 Get RF profile assignments by device"
    )
    def get_organization_wireless_rf_profiles_assignments_by_device(
        organization_id: str,
        per_page: Optional[int] = 1000,
        network_ids: Optional[str] = None,
        product_types: Optional[str] = None
    ):
        """Get RF profile assignments by device."""
        try:
            kwargs = {'perPage': per_page}
            if network_ids:
                kwargs['networkIds'] = json.loads(network_ids) if isinstance(network_ids, str) else network_ids
            if product_types:
                kwargs['productTypes'] = json.loads(product_types) if isinstance(product_types, str) else product_types
            
            result = meraki_client.dashboard.wireless.getOrganizationWirelessRfProfilesAssignmentsByDevice(
                organization_id, **kwargs
            )
            
            response = f"# 📻 RF Profile Assignments\n\n"
            if isinstance(result, list):
                response += f"**Total Devices**: {len(result)}\n"
                
                # Group by profile
                profiles = {}
                for device in result:
                    profile_name = device.get('rfProfile', {}).get('name', 'Default')
                    if profile_name not in profiles:
                        profiles[profile_name] = 0
                    profiles[profile_name] += 1
                
                response += f"\n## Profile Distribution\n"
                for profile, count in profiles.items():
                    response += f"- {profile}: {count} devices\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error getting RF profile assignments: {str(e)}"
    
    @app.tool(
        name="get_org_wireless_isolation_allowlist",
        description="📡🔥 Get SSID firewall isolation allowlist entries"
    )
    def get_organization_wireless_ssids_firewall_isolation_allowlist_entries(
        organization_id: str,
        per_page: Optional[int] = 1000
    ):
        """Get SSID firewall isolation allowlist entries."""
        try:
            result = meraki_client.dashboard.wireless.getOrganizationWirelessSsidsFirewallIsolationAllowlistEntries(
                organization_id,
                perPage=per_page
            )
            
            response = f"# 🔥 SSID Firewall Isolation Allowlist\n\n"
            if isinstance(result, list):
                response += f"**Total Entries**: {len(result)}\n\n"
                for entry in result[:10]:
                    response += f"- **{entry.get('mac')}**: {entry.get('comment', 'No comment')}\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error getting isolation allowlist: {str(e)}"