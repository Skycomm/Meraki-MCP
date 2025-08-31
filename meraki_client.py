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
            wait_on_rate_limit=True,
            single_request_timeout=TIMEOUT,  # Use timeout from config (600 seconds)
            maximum_retries=5  # Increase retries for reliability
        )
    
    # Organizations
    def get_organizations(self) -> List[Dict[str, Any]]:
        """Get all organizations the user has access to."""
        return self.dashboard.organizations.getOrganizations()
    
    def get_organization(self, organization_id: str) -> Dict[str, Any]:
        """Get information about a specific organization."""
        return self.dashboard.organizations.getOrganization(organization_id)
    
    # Networks
    def get_organization_networks(self, organization_id: str) -> List[Dict[str, Any]]:
        """Get networks in an organization."""
        return self.dashboard.organizations.getOrganizationNetworks(organization_id, perPage=1000, total_pages='all')
    
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
        # The SDK should handle pagination automatically with the iterator
        # Let's explicitly set perPage to maximum (1000) to reduce API calls
        return self.dashboard.networks.getNetworkClients(
            network_id, 
            timespan=timespan,
            perPage=1000,  # Maximum allowed by Meraki API
            total_pages='all'  # Ensure we get all pages
        )
    
    # SSID
    def get_network_wireless_ssids(self, network_id: str) -> List[Dict[str, Any]]:
        """Get wireless SSIDs in a network."""
        return self.dashboard.wireless.getNetworkWirelessSsids(network_id)
    
    # VLANs
    def get_network_vlans(self, network_id: str) -> List[Dict[str, Any]]:
        """Get VLANs in a network."""
        return self.dashboard.appliance.getNetworkApplianceVlans(network_id)
    
    # Alerts
    def get_organization_alerts(self, organization_id: str) -> List[Dict[str, Any]]:
        """Get alert profiles for an organization."""
        return self.dashboard.organizations.getOrganizationAlertsProfiles(organization_id)
    
    # Firmware
    def get_organization_firmware_upgrades(self, organization_id: str) -> List[Dict[str, Any]]:
        """Get firmware upgrades for an organization."""
        return self.dashboard.organizations.getOrganizationFirmwareUpgrades(organization_id)
    
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
    def get_organization_devices_uplinks_loss_and_latency(self, organization_id: str, timespan: int = 300):
        """Get organization uplinks loss and latency - REAL packet loss data."""
        return self.dashboard.organizations.getOrganizationDevicesUplinksLossAndLatency(organization_id, timespan=timespan)
    
    def get_organization_appliance_uplink_statuses(self, organization_id: str):
        """Get appliance uplink statuses - REAL uplink status data."""
        return self.dashboard.appliance.getOrganizationApplianceUplinkStatuses(organization_id)
    
    def get_device_appliance_performance(self, serial: str):
        """Get appliance performance - REAL method."""
        return self.dashboard.appliance.getDeviceAppliancePerformance(serial)
    
    def get_network_appliance_uplinks_usage_history(self, network_id: str, timespan: int = 86400):
        """Get appliance uplinks usage history - REAL historical data like dashboard."""
        return self.dashboard.appliance.getNetworkApplianceUplinksUsageHistory(network_id, timespan=timespan)
    
    def get_network_connection_stats(self, network_id: str, timespan: int = 86400):
        """Get network connection statistics - REAL method."""
        # This returns wireless connection stats
        return self.dashboard.wireless.getNetworkWirelessConnectionStats(network_id, timespan=timespan)
    
    def get_network_latency_stats(self, network_id: str, timespan: int = 86400):
        """Get network latency statistics - REAL method."""
        # This returns wireless latency stats
        return self.dashboard.wireless.getNetworkWirelessLatencyStats(network_id, timespan=timespan)
    
    # REAL Wireless API Methods
    def get_network_wireless_passwords(self, network_id: str):
        """Get wireless network passwords/PSK - REAL method."""
        return self.dashboard.wireless.getNetworkWirelessSsids(network_id)
    
    def get_network_wireless_clients(self, network_id: str, timespan: int = 86400):
        """Get wireless clients - REAL method."""
        # Use the general network clients endpoint and filter for wireless
        return self.dashboard.networks.getNetworkClients(
            network_id, 
            timespan=timespan,
            perPage=1000,  # Get up to 1000 clients to avoid pagination issues
            total_pages='all'  # Ensure we get all pages
        )
    
    def get_network_wireless_usage(self, network_id: str, timespan: int = 86400, device_serial: str = None, ssid_number: int = None, client_mac: str = None):
        """Get wireless usage history - REAL method."""
        # This API requires deviceSerial or clientId parameter
        kwargs = {'timespan': timespan}
        
        if device_serial:
            kwargs['deviceSerial'] = device_serial
        elif client_mac:
            kwargs['clientId'] = client_mac
        elif ssid_number is not None:
            # SSID alone won't work - need device or client
            kwargs['ssid'] = ssid_number
            # Return empty result since API requires device/client
            return []
        else:
            # API requires device or client - can't get aggregate data
            return []
            
        return self.dashboard.wireless.getNetworkWirelessUsageHistory(network_id, **kwargs)
    
    def update_network_wireless_ssid(self, network_id: str, number: int, name: str = None, enabled: bool = None,
                                    authMode: str = None, psk: str = None, encryptionMode: str = None, 
                                    wpaEncryptionMode: str = None, visible: bool = None,
                                    ipAssignmentMode: str = None, useVlanTagging: bool = None,
                                    vlanId: int = None, defaultVlanId: int = None,
                                    apTagsAndVlanIds: List[Dict[str, Any]] = None,
                                    lanIsolationEnabled: bool = None):
        """Update wireless SSID - REAL method with full authentication and bridging support."""
        kwargs = {}
        if name is not None:
            kwargs['name'] = name
        if enabled is not None:
            kwargs['enabled'] = enabled
        if authMode is not None:
            kwargs['authMode'] = authMode
        if psk is not None:
            kwargs['psk'] = psk
        if encryptionMode is not None:
            kwargs['encryptionMode'] = encryptionMode
        if wpaEncryptionMode is not None:
            kwargs['wpaEncryptionMode'] = wpaEncryptionMode
        if visible is not None:
            kwargs['visible'] = visible
        # Bridge mode parameters
        if ipAssignmentMode is not None:
            kwargs['ipAssignmentMode'] = ipAssignmentMode
        if useVlanTagging is not None:
            kwargs['useVlanTagging'] = useVlanTagging
        if vlanId is not None:
            kwargs['vlanId'] = vlanId
        if defaultVlanId is not None:
            kwargs['defaultVlanId'] = defaultVlanId
        if apTagsAndVlanIds is not None:
            kwargs['apTagsAndVlanIds'] = apTagsAndVlanIds
        if lanIsolationEnabled is not None:
            kwargs['lanIsolationEnabled'] = lanIsolationEnabled
        return self.dashboard.wireless.updateNetworkWirelessSsid(network_id, number, **kwargs)
    
    # REAL Network Management Methods
    def update_network(self, network_id: str, name: str = None, tags: List[str] = None, timezone: str = None) -> Dict[str, Any]:
        """Update a network - REAL method."""
        kwargs = {}
        if name is not None:
            kwargs['name'] = name
        if tags is not None:
            kwargs['tags'] = tags
        if timezone is not None:
            kwargs['timeZone'] = timezone
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
    def update_device(self, serial: str, name: str = None, tags: List[str] = None, address: str = None, 
                     lat: float = None, lng: float = None) -> Dict[str, Any]:
        """Update a device - REAL method."""
        kwargs = {}
        if name is not None:
            kwargs['name'] = name
        if tags is not None:
            kwargs['tags'] = tags
        if address is not None:
            kwargs['address'] = address
        if lat is not None:
            kwargs['lat'] = lat
        if lng is not None:
            kwargs['lng'] = lng
        return self.dashboard.devices.updateDevice(serial, **kwargs)
    
    def get_device_clients(self, serial: str, timespan: int = 86400) -> List[Dict[str, Any]]:
        """Get clients for a specific device - REAL method."""
        return self.dashboard.devices.getDeviceClients(serial, timespan=timespan, perPage=1000, total_pages='all')
    
    def get_device_status(self, serial: str) -> Dict[str, Any]:
        """Get device status - REAL method."""
        return self.dashboard.devices.getDevice(serial)
    
    def reboot_device(self, serial: str) -> Dict[str, Any]:
        """Reboot a device - REAL method."""
        return self.dashboard.devices.rebootDevice(serial)
    
    # REAL Organization Management Methods
    def get_organization_admins(self, organization_id: str, network_ids: List[str] = None) -> List[Dict[str, Any]]:
        """Get dashboard administrators for an organization - REAL method."""
        kwargs = {}
        if network_ids:
            kwargs['network_ids'] = network_ids
        return self.dashboard.organizations.getOrganizationAdmins(organization_id, **kwargs)
    
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
        network_id = device.get('network_id')
        if network_id:
            return self.dashboard.appliance.getNetworkApplianceVlans(network_id)
        return []
    
    def create_device_switch_vlan(self, serial: str, vlan_id: str, name: str, subnet: str = None) -> Dict[str, Any]:
        """Create a VLAN - VLANs are network-wide in Meraki, not per-device."""
        # Get the network ID from the device
        device = self.dashboard.devices.getDevice(serial)
        network_id = device.get('network_id')
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
    def get_organization_webhooks(self, organization_id: str):
        """Get all webhook HTTP servers across all networks in the organization - REAL method."""
        # Since regular webhooks are network-level, we need to iterate through all networks
        try:
            networks = self.dashboard.organizations.getOrganizationNetworks(organization_id)
            all_webhooks = []
            
            for network in networks:
                network_id = network['id']
                try:
                    webhooks = self.dashboard.networks.getNetworkWebhooksHttpServers(network_id)
                    # Add network info to each webhook
                    for webhook in webhooks:
                        webhook['network_id'] = network_id
                        webhook['networkName'] = network.get('name', 'Unknown')
                        all_webhooks.append(webhook)
                except Exception:
                    # Skip networks that don't support webhooks or have errors
                    pass
            
            return all_webhooks
        except Exception as e:
            # Fallback to organization level if available (for Meraki Insight)
            try:
                return self.dashboard.organizations.getOrganizationWebhooksHttpServers(organization_id)
            except:
                raise e
    
    def create_organization_webhook(self, organization_id: str, **kwargs):
        """Create organization webhook HTTP server - REAL method."""
        return self.dashboard.organizations.createOrganizationWebhooksHttpServer(organization_id, **kwargs)
    
    def delete_organization_webhook(self, organization_id: str, webhook_id: str, network_id: str = None):
        """Delete webhook HTTP server - REAL method."""
        # If network_id is provided, delete from network level
        if network_id:
            return self.dashboard.networks.deleteNetworkWebhooksHttpServer(network_id, webhook_id)
        else:
            # Try organization level (for Meraki Insight)
            try:
                return self.dashboard.organizations.deleteOrganizationWebhooksHttpServer(organization_id, webhook_id)
            except:
                # If that fails, search all networks for the webhook
                networks = self.dashboard.organizations.getOrganizationNetworks(organization_id)
                for network in networks:
                    try:
                        webhooks = self.dashboard.networks.getNetworkWebhooksHttpServers(network['id'])
                        if any(w.get('id') == webhook_id for w in webhooks):
                            return self.dashboard.networks.deleteNetworkWebhooksHttpServer(network['id'], webhook_id)
                    except:
                        pass
                raise Exception(f"Webhook {webhook_id} not found in organization {organization_id}")
    
    def get_network_webhook_http_servers(self, network_id: str):
        """Get network webhook HTTP servers - REAL method."""
        return self.dashboard.networks.getNetworkWebhooksHttpServers(network_id)
    
    def create_network_webhook_http_server(self, network_id: str, **kwargs):
        """Create network webhook HTTP server - REAL method."""
        return self.dashboard.networks.createNetworkWebhooksHttpServer(network_id, **kwargs)
    
    def delete_network_webhook(self, network_id: str, webhook_id: str):
        """Delete network webhook HTTP server - REAL method."""
        return self.dashboard.networks.deleteNetworkWebhooksHttpServer(network_id, webhook_id)
    
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
    
    def get_network_appliance_firewall_l7_rules(self, network_id: str):
        """Get L7 firewall rules - REAL method."""
        return self.dashboard.appliance.getNetworkApplianceFirewallL7FirewallRules(network_id)
    
    def update_network_appliance_firewall_l7_rules(self, network_id: str, **kwargs):
        """Update L7 firewall rules - REAL method."""
        return self.dashboard.appliance.updateNetworkApplianceFirewallL7FirewallRules(network_id, **kwargs)
    
    def get_network_appliance_firewall_settings(self, network_id: str):
        """Get firewall settings - REAL method."""
        return self.dashboard.appliance.getNetworkApplianceFirewallSettings(network_id)
    
    def update_network_appliance_firewall_settings(self, network_id: str, **kwargs):
        """Update firewall settings - REAL method."""
        return self.dashboard.appliance.updateNetworkApplianceFirewallSettings(network_id, **kwargs)
    
    def get_network_appliance_content_filtering(self, network_id: str):
        """Get content filtering settings - REAL method."""
        return self.dashboard.appliance.getNetworkApplianceContentFiltering(network_id)
    
    def update_network_appliance_content_filtering(self, network_id: str, **kwargs):
        """Update content filtering settings - REAL method."""
        return self.dashboard.appliance.updateNetworkApplianceContentFiltering(network_id, **kwargs)
    
    def get_network_appliance_content_filtering_categories(self, network_id: str):
        """Get all available content filtering categories - REAL method."""
        return self.dashboard.appliance.getNetworkApplianceContentFilteringCategories(network_id)
    
    def get_network_appliance_vpn_site_to_site(self, network_id: str):
        """Get site-to-site VPN settings - REAL method."""
        return self.dashboard.appliance.getNetworkApplianceVpnSiteToSiteVpn(network_id)
    
    def get_network_appliance_ports(self, network_id: str):
        """Get per-port VLAN settings for all ports of a MX - REAL method."""
        return self.dashboard.appliance.getNetworkAppliancePorts(network_id)
    
    def update_network_appliance_port(self, network_id: str, port_id: str, **kwargs):
        """Update per-port VLAN settings for a single MX port - REAL method."""
        return self.dashboard.appliance.updateNetworkAppliancePort(network_id, port_id, **kwargs)
    
    def get_network_appliance_security_malware(self, network_id: str):
        """Get malware protection settings - REAL method."""
        return self.dashboard.appliance.getNetworkApplianceSecurityMalware(network_id)
    
    def update_network_appliance_security_malware(self, network_id: str, **kwargs):
        """Update malware protection settings - REAL method."""
        return self.dashboard.appliance.updateNetworkApplianceSecurityMalware(network_id, **kwargs)
    
    def get_network_appliance_security_intrusion(self, network_id: str):
        """Get intrusion detection settings - REAL method."""
        return self.dashboard.appliance.getNetworkApplianceSecurityIntrusion(network_id)
    
    def update_network_appliance_security_intrusion(self, network_id: str, **kwargs):
        """Update intrusion detection/prevention settings - REAL method."""
        return self.dashboard.appliance.updateNetworkApplianceSecurityIntrusion(network_id, **kwargs)
    
    # Security Events Methods
    def get_network_appliance_security_events(self, network_id: str, **kwargs):
        """Get security events for a network - REAL method."""
        return self.dashboard.appliance.getNetworkApplianceSecurityEvents(network_id, **kwargs)
    
    def get_network_appliance_client_security_events(self, network_id: str, client_id: str, **kwargs):
        """Get security events for a specific client - REAL method."""
        return self.dashboard.appliance.getNetworkApplianceClientSecurityEvents(network_id, client_id, **kwargs)
    
    # Network Events (including port status changes)
    def get_network_events(self, network_id: str, **kwargs):
        """Get network events including port carrier changes - REAL method."""
        # Default to 1000 per page but don't fetch all pages automatically
        # to avoid timeout issues with networks that have many events
        if 'perPage' not in kwargs:
            kwargs['perPage'] = 1000
        # Don't automatically fetch all pages - let caller handle pagination if needed
        return self.dashboard.networks.getNetworkEvents(network_id, **kwargs)
    
    # NAT Rules Methods
    def get_network_appliance_firewall_one_to_one_nat_rules(self, network_id: str):
        """Get 1:1 NAT mapping rules - REAL method."""
        return self.dashboard.appliance.getNetworkApplianceFirewallOneToOneNatRules(network_id)
    
    def update_network_appliance_firewall_one_to_one_nat_rules(self, network_id: str, **kwargs):
        """Update 1:1 NAT mapping rules - REAL method."""
        return self.dashboard.appliance.updateNetworkApplianceFirewallOneToOneNatRules(network_id, **kwargs)
    
    def get_network_appliance_firewall_one_to_many_nat_rules(self, network_id: str):
        """Get 1:Many NAT mapping rules - REAL method."""
        return self.dashboard.appliance.getNetworkApplianceFirewallOneToManyNatRules(network_id)
    
    def update_network_appliance_firewall_one_to_many_nat_rules(self, network_id: str, **kwargs):
        """Update 1:Many NAT mapping rules - REAL method."""
        return self.dashboard.appliance.updateNetworkApplianceFirewallOneToManyNatRules(network_id, **kwargs)
    
    # Port Forwarding Methods
    def get_network_appliance_firewall_port_forwarding_rules(self, network_id: str):
        """Get port forwarding rules - REAL method."""
        return self.dashboard.appliance.getNetworkApplianceFirewallPortForwardingRules(network_id)
    
    def update_network_appliance_firewall_port_forwarding_rules(self, network_id: str, **kwargs):
        """Update port forwarding rules - REAL method."""
        return self.dashboard.appliance.updateNetworkApplianceFirewallPortForwardingRules(network_id, **kwargs)
    
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
        # This returns Bluetooth settings, not clients
        return self.dashboard.wireless.getNetworkWirelessBluetoothSettings(network_id)
    
    def get_network_wireless_channel_utilization(self, network_id: str, timespan: int = 3600, device_serial: str = None, ssid_number: int = None, client_mac: str = None):
        """Get channel utilization history - REAL method."""
        # Build kwargs - all parameters are optional
        kwargs = {'timespan': timespan}
        
        if device_serial:
            kwargs['deviceSerial'] = device_serial
        if client_mac:
            kwargs['clientId'] = client_mac
        if ssid_number is not None:
            kwargs['ssid'] = ssid_number
            
        return self.dashboard.wireless.getNetworkWirelessChannelUtilizationHistory(network_id, **kwargs)
    
    # REAL Systems Manager (SM) Methods
    def get_network_sm_devices(self, network_id: str):
        """Get all Systems Manager devices - REAL method."""
        # SM can have many devices, ensure we get all pages
        return self.dashboard.sm.getNetworkSmDevices(network_id, perPage=1000, total_pages='all')
    
    def get_network_sm_device(self, network_id: str, device_id: str):
        """Get specific SM device details - REAL method."""
        return self.dashboard.sm.getNetworkSmDevice(network_id, device_id)
    
    def get_network_sm_device_apps(self, network_id: str, device_id: str):
        """Get apps installed on SM device - REAL method."""
        return self.dashboard.sm.getNetworkSmDeviceSoftwares(network_id, device_id)
    
    def reboot_network_sm_devices(self, network_id: str, **kwargs):
        """Reboot SM devices - REAL method."""
        return self.dashboard.sm.rebootNetworkSmDevices(network_id, **kwargs)
    
    def get_network_sm_profiles(self, network_id: str):
        """Get SM profiles - REAL method."""
        return self.dashboard.sm.getNetworkSmProfiles(network_id)
    
    def get_network_sm_device_performance_history(self, network_id: str, device_id: str):
        """Get SM device performance history - REAL method."""
        return self.dashboard.sm.getNetworkSmDevicePerformanceHistory(network_id, device_id)
    
    # REAL Licensing Methods
    def get_organization_licenses(self, organization_id: str):
        """Get organization licenses - REAL method."""
        return self.dashboard.organizations.getOrganizationLicenses(organization_id)
    
    def get_organization_licensing_coterm_licenses(self, organization_id: str):
        """Get co-termination licenses - REAL method."""
        return self.dashboard.licensing.getOrganizationLicensingCotermLicenses(organization_id)
    
    def claim_organization_license(self, organization_id: str, **kwargs):
        """Claim organization license - REAL method."""
        return self.dashboard.organizations.claimOrganizationLicenses(organization_id, **kwargs)
    
    def update_organization_license(self, organization_id: str, license_id: str, **kwargs):
        """Update organization license - REAL method."""
        return self.dashboard.organizations.updateOrganizationLicense(organization_id, license_id, **kwargs)
    
    def move_organization_licenses(self, organization_id: str, **kwargs):
        """Move organization licenses - REAL method."""
        return self.dashboard.organizations.moveOrganizationLicenses(organization_id, **kwargs)
    
    def renew_organization_licenses_seats(self, organization_id: str, **kwargs):
        """Renew organization licenses seats - REAL method."""
        return self.dashboard.organizations.renewOrganizationLicensesSeats(organization_id, **kwargs)
    
    # REAL Policy Objects Methods
    def get_organization_policy_objects(self, organization_id: str):
        """Get organization policy objects - REAL method."""
        return self.dashboard.organizations.getOrganizationPolicyObjects(organization_id)
    
    def create_organization_policy_object(self, organization_id: str, **kwargs):
        """Create organization policy object - REAL method."""
        return self.dashboard.organizations.createOrganizationPolicyObject(organization_id, **kwargs)
    
    def update_organization_policy_object(self, organization_id: str, policy_object_id: str, **kwargs):
        """Update organization policy object - REAL method."""
        return self.dashboard.organizations.updateOrganizationPolicyObject(organization_id, policy_object_id, **kwargs)
    
    def delete_organization_policy_object(self, organization_id: str, policy_object_id: str):
        """Delete organization policy object - REAL method."""
        return self.dashboard.organizations.deleteOrganizationPolicyObject(organization_id, policy_object_id)
    
    def get_organization_policy_objects_groups(self, organization_id: str):
        """Get organization policy object groups - REAL method."""
        return self.dashboard.organizations.getOrganizationPolicyObjectsGroups(organization_id)
    
    def create_organization_policy_objects_group(self, organization_id: str, **kwargs):
        """Create organization policy object group - REAL method."""
        return self.dashboard.organizations.createOrganizationPolicyObjectsGroup(organization_id, **kwargs)
    
    # REAL Enhanced Monitoring Methods (2025 features)
    def get_device_memory_history(self, serial: str, **kwargs):
        """Get device memory utilization history - Note: This specific API may not exist."""
        # This appears to be a planned/beta API that's not yet available
        return None
    
    def get_device_cpu_power_mode_history(self, serial: str, **kwargs):
        """Get wireless device CPU power mode history - REAL method."""
        return self.dashboard.wireless.getDeviceWirelessRadioSettings(serial, **kwargs)
    
    def get_device_wireless_cpu_load(self, serial: str):
        """Get wireless device CPU load - REAL method."""
        return self.dashboard.wireless.getDeviceWirelessStatus(serial)
    
    def get_organization_switch_ports_history(self, organization_id: str, **kwargs):
        """Get organization switch ports history - REAL method."""
        return self.dashboard.switch.getOrganizationSwitchPortsStatusesBySwitch(organization_id, **kwargs)
    
    def get_organization_devices_migration_status(self, organization_id: str):
        """Get organization devices migration status - REAL method."""
        return self.dashboard.organizations.getOrganizationDevices(organization_id, perPage=1000, total_pages='all')
    
    def get_organization_api_requests(self, organization_id: str, **kwargs):
        """Get organization API usage/requests - REAL method."""
        return self.dashboard.organizations.getOrganizationApiRequests(organization_id, **kwargs)
    
    # REAL Beta/Early Access Methods
    def get_organization_early_access_features(self, organization_id: str):
        """Get organization early access features - REAL method."""
        return self.dashboard.organizations.getOrganizationEarlyAccessFeatures(organization_id)
    
    def get_organization_early_access_features_opt_ins(self, organization_id: str):
        """Get organization early access feature opt-ins - REAL method."""
        return self.dashboard.organizations.getOrganizationEarlyAccessFeaturesOptIns(organization_id)
    
    def create_organization_early_access_features_opt_in(self, organization_id: str, **kwargs):
        """Create organization early access feature opt-in - REAL method."""
        return self.dashboard.organizations.createOrganizationEarlyAccessFeaturesOptIn(organization_id, **kwargs)
    
    def delete_organization_early_access_features_opt_in(self, organization_id: str, opt_in_id: str):
        """Delete organization early access feature opt-in - REAL method."""
        return self.dashboard.organizations.deleteOrganizationEarlyAccessFeaturesOptIn(organization_id, opt_in_id)
    
    def get_organization_devices(self, organization_id: str):
        """Get all devices in organization - REAL method."""
        return self.dashboard.organizations.getOrganizationDevices(organization_id, perPage=1000, total_pages='all')
    
    # REAL Live Tools Methods (Beta/Early Access)
    def create_device_live_tools_ping(self, serial: str, **kwargs):
        """Create device ping test - REAL method."""
        return self.dashboard.devices.createDeviceLiveToolsPing(serial, **kwargs)
    
    def get_device_live_tools_ping(self, serial: str, ping_id: str):
        """Get device ping test results - REAL method."""
        return self.dashboard.devices.getDeviceLiveToolsPing(serial, ping_id)
    
    def create_device_live_tools_ping_device(self, serial: str):
        """Create ping test to the device itself - REAL method."""
        return self.dashboard.devices.createDeviceLiveToolsPingDevice(serial)
    
    def get_device_live_tools_ping_device(self, serial: str, id: str):
        """Get ping device test results - REAL method."""
        return self.dashboard.devices.getDeviceLiveToolsPingDevice(serial, id)
    
    def create_device_live_tools_trace_route(self, serial: str, **kwargs):
        """Create traceroute test - REAL method."""
        return self.dashboard.devices.createDeviceLiveToolsTraceRoute(serial, **kwargs)
    
    def get_device_live_tools_trace_route(self, serial: str, id: str):
        """Get traceroute test results - REAL method."""
        return self.dashboard.devices.getDeviceLiveToolsTraceRoute(serial, id)
    
    def create_device_live_tools_throughput_test(self, serial: str, **kwargs):
        """Create device throughput test - REAL method."""
        return self.dashboard.devices.createDeviceLiveToolsThroughputTest(serial, **kwargs)
    
    def get_device_live_tools_throughput_test(self, serial: str, test_id: str):
        """Get device throughput test results - REAL method."""
        return self.dashboard.devices.getDeviceLiveToolsThroughputTest(serial, test_id)
    
    def create_device_live_tools_cable_test(self, serial: str, **kwargs):
        """Create cable test - REAL method."""
        return self.dashboard.devices.createDeviceLiveToolsCableTest(serial, **kwargs)
    
    def get_device_live_tools_cable_test(self, serial: str, test_id: str):
        """Get cable test results - REAL method."""
        return self.dashboard.devices.getDeviceLiveToolsCableTest(serial, test_id)
    
    def create_device_live_tools_wake_on_lan(self, serial: str, **kwargs):
        """Send Wake-on-LAN - REAL method."""
        return self.dashboard.devices.createDeviceLiveToolsWakeOnLan(serial, **kwargs)
    
    def get_device_live_tools_wake_on_lan(self, serial: str, id: str):
        """Get Wake-on-LAN job results - REAL method."""
        return self.dashboard.devices.getDeviceLiveToolsWakeOnLan(serial, id)
    
    def create_device_live_tools_arp_table(self, serial: str):
        """Create ARP table request - REAL method."""
        return self.dashboard.devices.createDeviceLiveToolsArpTable(serial)
    
    def get_device_live_tools_arp_table(self, serial: str, id: str):
        """Get ARP table results - REAL method."""
        return self.dashboard.devices.getDeviceLiveToolsArpTable(serial, id)
    
    def create_device_live_tools_mac_table(self, serial: str):
        """Create MAC table request - REAL method."""
        return self.dashboard.devices.createDeviceLiveToolsMacTable(serial)
    
    def get_device_live_tools_mac_table(self, serial: str, request_id: str):
        """Get MAC table results - REAL method."""
        return self.dashboard.devices.getDeviceLiveToolsMacTable(serial, request_id)
    
    def create_device_live_tools_leds_blink(self, serial: str, **kwargs):
        """Blink device LEDs - REAL method."""
        return self.dashboard.devices.createDeviceLiveToolsLedsBlink(serial, **kwargs)
