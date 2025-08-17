"""
Cisco Meraki API client.
"""

import meraki
from typing import Dict, List, Any, Optional
from config import MERAKI_API_KEY, TIMEOUT

class MerakiClient:
    """Client for the Cisco Meraki API."""
    
    def __init__(self):
        """Initialize the Meraki API client."""
        self.dashboard = meraki.DashboardAPI(
            api_key=MERAKI_API_KEY,
            output_log=False,
            suppress_logging=True,
            wait_on_rate_limit=True
            # timeout parameter has been removed as it's not supported by the current SDK version
        )
    
    # Organizations
    def get_organizations(self) -> List[Dict[str, Any]]:
        """Get all organizations the user has access to."""
        return self.dashboard.organizations.getOrganizations()
    
    def get_organization(self, org_id: str) -> Dict[str, Any]:
        """Get information about a specific organization."""
        return self.dashboard.organizations.getOrganization(org_id)
    
    # Networks
    def get_organization_networks(self, org_id: str) -> List[Dict[str, Any]]:
        """Get networks in an organization."""
        return self.dashboard.organizations.getOrganizationNetworks(org_id)
    
    def get_network(self, network_id: str) -> Dict[str, Any]:
        """Get information about a specific network."""
        return self.dashboard.networks.getNetwork(network_id)
    
    # Devices
    def get_network_devices(self, network_id: str) -> List[Dict[str, Any]]:
        """Get devices in a network."""
        return self.dashboard.networks.getNetworkDevices(network_id)
    
    def get_device(self, serial: str) -> Dict[str, Any]:
        """Get information about a specific device."""
        return self.dashboard.devices.getDevice(serial)
    
    # Clients
    def get_network_clients(self, network_id: str, timespan: Optional[int] = 86400) -> List[Dict[str, Any]]:
        """Get clients in a network (default timespan: 24 hours)."""
        return self.dashboard.networks.getNetworkClients(network_id, timespan=timespan)
    
    # SSID
    def get_network_wireless_ssids(self, network_id: str) -> List[Dict[str, Any]]:
        """Get wireless SSIDs in a network."""
        return self.dashboard.wireless.getNetworkWirelessSsids(network_id)
    
    # VLANs
    def get_network_vlans(self, network_id: str) -> List[Dict[str, Any]]:
        """Get VLANs in a network."""
        return self.dashboard.networks.getNetworkVlans(network_id)
    
    # Alerts
    def get_organization_alerts(self, org_id: str) -> Dict[str, Any]:
        """Get alert settings for an organization."""
        return self.dashboard.organizations.getOrganizationAlertsSettings(org_id)
    
    # Firmware
    def get_organization_firmware_upgrades(self, org_id: str) -> List[Dict[str, Any]]:
        """Get firmware upgrades for an organization."""
        return self.dashboard.organizations.getOrganizationFirmwareUpgrades(org_id)
    
    # Switch ports
    def get_device_switch_ports(self, serial: str) -> List[Dict[str, Any]]:
        """Get switch ports for a switch."""
        return self.dashboard.switch.getDeviceSwitchPorts(serial)
    
    def update_device_switch_port(self, serial: str, port_id: str, **kwargs) -> Dict[str, Any]:
        """Update a switch port configuration."""
        return self.dashboard.switch.updateDeviceSwitchPort(serial, port_id, **kwargs)
    
    # Camera
    def get_device_camera_video_link(self, serial: str, timestamp: Optional[str] = None) -> Dict[str, Any]:
        """Get video link for a camera."""
        return self.dashboard.camera.getDeviceCameraVideoLink(serial, timestamp=timestamp)
    
    # REAL Analytics API Methods
    def get_organization_devices_uplinks_loss_and_latency(self, org_id: str, timespan: int = 86400):
        """Get organization uplinks loss and latency - REAL packet loss data."""
        return self.dashboard.organizations.getOrganizationDevicesUplinksLossAndLatency(org_id, timespan=timespan)
    
    def get_organization_appliance_uplink_statuses(self, org_id: str):
        """Get appliance uplink statuses - REAL uplink status data."""
        return self.dashboard.organizations.getOrganizationApplianceUplinkStatuses(org_id)
    
    def get_network_connection_stats(self, network_id: str, timespan: int = 86400):
        """Get network connection statistics - REAL method."""
        return self.dashboard.networks.getNetworkConnectionStats(network_id, timespan=timespan)
    
    def get_network_latency_stats(self, network_id: str, timespan: int = 86400):
        """Get network latency statistics - REAL method."""
        return self.dashboard.networks.getNetworkLatencyStats(network_id, timespan=timespan)
    
    # REAL Wireless API Methods
    def get_network_wireless_passwords(self, network_id: str):
        """Get wireless network passwords/PSK - REAL method."""
        return self.dashboard.wireless.getNetworkWirelessSsids(network_id)
    
    def get_network_wireless_clients(self, network_id: str, timespan: int = 86400):
        """Get wireless clients - REAL method."""
        return self.dashboard.wireless.getNetworkWirelessClients(network_id, timespan=timespan)
    
    def get_network_wireless_usage(self, network_id: str, timespan: int = 86400):
        """Get wireless usage history - REAL method."""
        return self.dashboard.wireless.getNetworkWirelessUsageHistory(network_id, timespan=timespan)
    
    def update_network_wireless_ssid(self, network_id: str, number: int, name: str = None, enabled: bool = None):
        """Update wireless SSID - REAL method."""
        kwargs = {}
        if name is not None:
            kwargs['name'] = name
        if enabled is not None:
            kwargs['enabled'] = enabled
        return self.dashboard.wireless.updateNetworkWirelessSsid(network_id, number, **kwargs)
    
    # REAL Network Management Methods
    def update_network(self, network_id: str, name: str = None, tags: List[str] = None) -> Dict[str, Any]:
        """Update a network - REAL method."""
        kwargs = {}
        if name is not None:
            kwargs['name'] = name
        if tags is not None:
            kwargs['tags'] = tags
        return self.dashboard.networks.updateNetwork(network_id, **kwargs)
    
    def create_network(self, organization_id: str, name: str, productTypes: List[str]) -> Dict[str, Any]:
        """Create a new network - REAL method."""
        return self.dashboard.organizations.createOrganizationNetwork(
            organization_id, 
            name=name, 
            productTypes=productTypes
        )
    
    def delete_network(self, network_id: str) -> None:
        """Delete a network - REAL method."""
        return self.dashboard.networks.deleteNetwork(network_id)
    
    # REAL Device Management Methods  
    def update_device(self, serial: str, name: str = None, tags: List[str] = None, address: str = None) -> Dict[str, Any]:
        """Update a device - REAL method."""
        kwargs = {}
        if name is not None:
            kwargs['name'] = name
        if tags is not None:
            kwargs['tags'] = tags
        if address is not None:
            kwargs['address'] = address
        return self.dashboard.devices.updateDevice(serial, **kwargs)
    
    def get_device_clients(self, serial: str, timespan: int = 86400) -> List[Dict[str, Any]]:
        """Get clients for a specific device - REAL method."""
        return self.dashboard.devices.getDeviceClients(serial, timespan=timespan)
    
    def get_device_status(self, serial: str) -> Dict[str, Any]:
        """Get device status - REAL method."""
        return self.dashboard.devices.getDevice(serial)
    
    def reboot_device(self, serial: str) -> Dict[str, Any]:
        """Reboot a device - REAL method."""
        return self.dashboard.devices.rebootDevice(serial)
    
    # REAL Organization Management Methods
    def create_organization(self, name: str) -> Dict[str, Any]:
        """Create a new organization - REAL method."""
        return self.dashboard.organizations.createOrganization(name=name)
    
    def update_organization(self, organization_id: str, name: str) -> Dict[str, Any]:
        """Update an organization - REAL method."""
        return self.dashboard.organizations.updateOrganization(organization_id, name=name)
    
    def delete_organization(self, organization_id: str) -> None:
        """Delete an organization - REAL method."""
        return self.dashboard.organizations.deleteOrganization(organization_id)
    
    # REAL Switch Management Methods
    def get_device_switch_port_statuses(self, serial: str) -> List[Dict[str, Any]]:
        """Get switch port statuses - REAL method."""
        return self.dashboard.switch.getDeviceSwitchPortsStatuses(serial)
    
    def get_device_switch_vlans(self, serial: str) -> List[Dict[str, Any]]:
        """Get switch VLANs - This is not a per-device API, getting network VLANs instead."""
        # Note: Meraki API doesn't have per-device VLAN endpoint, VLANs are network-wide
        device = self.dashboard.devices.getDevice(serial)
        network_id = device.get('networkId')
        if network_id:
            return self.dashboard.networks.getNetworkVlans(network_id)
        return []
    
    def create_device_switch_vlan(self, serial: str, vlan_id: str, name: str, subnet: str = None) -> Dict[str, Any]:
        """Create a VLAN - VLANs are network-wide in Meraki, not per-device."""
        # Get the network ID from the device
        device = self.dashboard.devices.getDevice(serial)
        network_id = device.get('networkId')
        if not network_id:
            raise ValueError(f"Device {serial} is not in a network")
        
        kwargs = {
            'id': vlan_id,
            'name': name
        }
        if subnet:
            kwargs['subnet'] = subnet
            kwargs['applianceIp'] = subnet.split('/')[0]  # Use first IP as gateway
        
        return self.dashboard.networks.createNetworkVlan(network_id, **kwargs)
    
    # REAL Alert & Webhook Methods
    def get_organization_webhooks(self, org_id: str):
        """Get organization webhooks - REAL method."""
        return self.dashboard.organizations.getOrganizationWebhooks(org_id)
    
    def create_organization_webhook(self, org_id: str, **kwargs):
        """Create organization webhook - REAL method."""
        return self.dashboard.organizations.createOrganizationWebhook(org_id, **kwargs)
    
    def get_network_webhook_http_servers(self, network_id: str):
        """Get network webhook HTTP servers - REAL method."""
        return self.dashboard.networks.getNetworkWebhookHttpServers(network_id)
    
    def create_network_webhook_http_server(self, network_id: str, **kwargs):
        """Create network webhook HTTP server - REAL method."""
        return self.dashboard.networks.createNetworkWebhookHttpServer(network_id, **kwargs)
    
    def get_network_alerts_settings(self, network_id: str):
        """Get network alerts settings - REAL method."""
        return self.dashboard.networks.getNetworkAlertsSettings(network_id)
    
    def update_network_alerts_settings(self, network_id: str, **kwargs):
        """Update network alerts settings - REAL method."""
        return self.dashboard.networks.updateNetworkAlertsSettings(network_id, **kwargs)
    
    # REAL Security Appliance Methods
    def get_network_appliance_firewall_l3_rules(self, network_id: str):
        """Get L3 firewall rules - REAL method."""
        return self.dashboard.appliance.getNetworkApplianceFirewallL3FirewallRules(network_id)
    
    def update_network_appliance_firewall_l3_rules(self, network_id: str, **kwargs):
        """Update L3 firewall rules - REAL method."""
        return self.dashboard.appliance.updateNetworkApplianceFirewallL3FirewallRules(network_id, **kwargs)
    
    def get_network_appliance_content_filtering(self, network_id: str):
        """Get content filtering settings - REAL method."""
        return self.dashboard.appliance.getNetworkApplianceContentFiltering(network_id)
    
    def get_network_appliance_vpn_site_to_site(self, network_id: str):
        """Get site-to-site VPN settings - REAL method."""
        return self.dashboard.appliance.getNetworkApplianceVpnSiteToSiteVpn(network_id)
    
    def get_network_appliance_security_malware(self, network_id: str):
        """Get malware protection settings - REAL method."""
        return self.dashboard.appliance.getNetworkApplianceSecurityMalware(network_id)
    
    def get_network_appliance_security_intrusion(self, network_id: str):
        """Get intrusion detection settings - REAL method."""
        return self.dashboard.appliance.getNetworkApplianceSecurityIntrusion(network_id)
    
    # REAL Camera Methods (additional to existing)
    def get_device_camera_snapshot(self, serial: str, timestamp: str = None):
        """Generate camera snapshot - REAL method."""
        kwargs = {}
        if timestamp:
            kwargs['timestamp'] = timestamp
        return self.dashboard.camera.generateDeviceCameraSnapshot(serial, **kwargs)
    
    def get_device_camera_video_settings(self, serial: str):
        """Get camera video settings - REAL method."""
        return self.dashboard.camera.getDeviceCameraVideoSettings(serial)
    
    def update_device_camera_video_settings(self, serial: str, **kwargs):
        """Update camera video settings - REAL method."""
        return self.dashboard.camera.updateDeviceCameraVideoSettings(serial, **kwargs)
    
    def get_device_camera_analytics_zones(self, serial: str):
        """Get camera analytics zones - REAL method."""
        return self.dashboard.camera.getDeviceCameraAnalyticsZones(serial)
    
    def get_device_camera_sense(self, serial: str):
        """Get camera motion detection settings - REAL method."""
        return self.dashboard.camera.getDeviceCameraSense(serial)
    
    # More REAL Wireless Methods
    def get_network_wireless_rf_profiles(self, network_id: str):
        """Get wireless RF profiles - REAL method."""
        return self.dashboard.wireless.getNetworkWirelessRfProfiles(network_id)
    
    def get_network_wireless_air_marshal(self, network_id: str, timespan: int = 3600):
        """Get Air Marshal (rogue AP) data - REAL method."""
        return self.dashboard.wireless.getNetworkWirelessAirMarshal(network_id, timespan=timespan)
    
    def get_network_wireless_bluetooth_clients(self, network_id: str):
        """Get Bluetooth clients - REAL method."""
        return self.dashboard.wireless.getNetworkWirelessBluetoothClients(network_id)
    
    def get_network_wireless_channel_utilization(self, network_id: str, timespan: int = 3600):
        """Get channel utilization history - REAL method."""
        return self.dashboard.wireless.getNetworkWirelessChannelUtilizationHistory(network_id, timespan=timespan)
