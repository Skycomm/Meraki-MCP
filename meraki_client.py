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
