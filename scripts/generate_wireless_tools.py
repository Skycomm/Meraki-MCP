#!/usr/bin/env python3
"""
Generate the complete wireless tools file with all 116 SDK methods.
"""

import re

# All 116 SDK methods
sdk_methods = [
    "assignNetworkWirelessEthernetPortsProfiles",
    "createNetworkWirelessAirMarshalRule",
    "createNetworkWirelessEthernetPortsProfile",
    "createNetworkWirelessRfProfile",
    "createNetworkWirelessSsidIdentityPsk",
    "createOrganizationWirelessDevicesRadsecCertificatesAuthority",
    "createOrganizationWirelessLocationScanningReceiver",
    "createOrganizationWirelessSsidsFirewallIsolationAllowlistEntry",
    "deleteNetworkWirelessAirMarshalRule",
    "deleteNetworkWirelessEthernetPortsProfile",
    "deleteNetworkWirelessRfProfile",
    "deleteNetworkWirelessSsidIdentityPsk",
    "deleteOrganizationWirelessLocationScanningReceiver",
    "deleteOrganizationWirelessSsidsFirewallIsolationAllowlistEntry",
    "getDeviceWirelessBluetoothSettings",
    "getDeviceWirelessConnectionStats",
    "getDeviceWirelessElectronicShelfLabel",
    "getDeviceWirelessLatencyStats",
    "getDeviceWirelessRadioSettings",
    "getDeviceWirelessStatus",
    "getNetworkWirelessAirMarshal",
    "getNetworkWirelessAlternateManagementInterface",
    "getNetworkWirelessBilling",
    "getNetworkWirelessBluetoothSettings",
    "getNetworkWirelessChannelUtilizationHistory",
    "getNetworkWirelessClientConnectionStats",
    "getNetworkWirelessClientConnectivityEvents",
    "getNetworkWirelessClientCountHistory",
    "getNetworkWirelessClientLatencyHistory",
    "getNetworkWirelessClientLatencyStats",
    "getNetworkWirelessClientsConnectionStats",
    "getNetworkWirelessClientsLatencyStats",
    "getNetworkWirelessConnectionStats",
    "getNetworkWirelessDataRateHistory",
    "getNetworkWirelessDevicesConnectionStats",
    "getNetworkWirelessDevicesLatencyStats",
    "getNetworkWirelessElectronicShelfLabel",
    "getNetworkWirelessElectronicShelfLabelConfiguredDevices",
    "getNetworkWirelessEthernetPortsProfile",
    "getNetworkWirelessEthernetPortsProfiles",
    "getNetworkWirelessFailedConnections",
    "getNetworkWirelessLatencyHistory",
    "getNetworkWirelessLatencyStats",
    "getNetworkWirelessMeshStatuses",
    "getNetworkWirelessRfProfile",
    "getNetworkWirelessRfProfiles",
    "getNetworkWirelessSettings",
    "getNetworkWirelessSignalQualityHistory",
    "getNetworkWirelessSsid",
    "getNetworkWirelessSsidBonjourForwarding",
    "getNetworkWirelessSsidDeviceTypeGroupPolicies",
    "getNetworkWirelessSsidEapOverride",
    "getNetworkWirelessSsidFirewallL3FirewallRules",
    "getNetworkWirelessSsidFirewallL7FirewallRules",
    "getNetworkWirelessSsidHotspot20",
    "getNetworkWirelessSsidIdentityPsk",
    "getNetworkWirelessSsidIdentityPsks",
    "getNetworkWirelessSsids",
    "getNetworkWirelessSsidSchedules",
    "getNetworkWirelessSsidSplashSettings",
    "getNetworkWirelessSsidTrafficShapingRules",
    "getNetworkWirelessSsidVpn",
    "getNetworkWirelessUsageHistory",
    "getOrganizationWirelessAirMarshalRules",
    "getOrganizationWirelessAirMarshalSettingsByNetwork",
    "getOrganizationWirelessClientsOverviewByDevice",
    "getOrganizationWirelessDevicesChannelUtilizationByDevice",
    "getOrganizationWirelessDevicesChannelUtilizationByNetwork",
    "getOrganizationWirelessDevicesChannelUtilizationHistoryByDeviceByInterval",
    "getOrganizationWirelessDevicesChannelUtilizationHistoryByNetworkByInterval",
    "getOrganizationWirelessDevicesEthernetStatuses",
    "getOrganizationWirelessDevicesPacketLossByClient",
    "getOrganizationWirelessDevicesPacketLossByDevice",
    "getOrganizationWirelessDevicesPacketLossByNetwork",
    "getOrganizationWirelessDevicesPowerModeHistory",
    "getOrganizationWirelessDevicesRadsecCertificatesAuthorities",
    "getOrganizationWirelessDevicesRadsecCertificatesAuthoritiesCrls",
    "getOrganizationWirelessDevicesRadsecCertificatesAuthoritiesCrlsDeltas",
    "getOrganizationWirelessDevicesSystemCpuLoadHistory",
    "getOrganizationWirelessDevicesWirelessControllersByDevice",
    "getOrganizationWirelessLocationScanningByNetwork",
    "getOrganizationWirelessLocationScanningReceivers",
    "getOrganizationWirelessRfProfilesAssignmentsByDevice",
    "getOrganizationWirelessSsidsFirewallIsolationAllowlistEntries",
    "getOrganizationWirelessSsidsStatusesByDevice",
    "recalculateOrganizationWirelessRadioAutoRfChannels",
    "setNetworkWirelessEthernetPortsProfilesDefault",
    "updateDeviceWirelessAlternateManagementInterfaceIpv6",
    "updateDeviceWirelessBluetoothSettings",
    "updateDeviceWirelessElectronicShelfLabel",
    "updateDeviceWirelessRadioSettings",
    "updateNetworkWirelessAirMarshalRule",
    "updateNetworkWirelessAirMarshalSettings",
    "updateNetworkWirelessAlternateManagementInterface",
    "updateNetworkWirelessBilling",
    "updateNetworkWirelessBluetoothSettings",
    "updateNetworkWirelessElectronicShelfLabel",
    "updateNetworkWirelessEthernetPortsProfile",
    "updateNetworkWirelessLocationScanning",
    "updateNetworkWirelessRfProfile",
    "updateNetworkWirelessSettings",
    "updateNetworkWirelessSsid",
    "updateNetworkWirelessSsidBonjourForwarding",
    "updateNetworkWirelessSsidDeviceTypeGroupPolicies",
    "updateNetworkWirelessSsidEapOverride",
    "updateNetworkWirelessSsidFirewallL3FirewallRules",
    "updateNetworkWirelessSsidFirewallL7FirewallRules",
    "updateNetworkWirelessSsidHotspot20",
    "updateNetworkWirelessSsidIdentityPsk",
    "updateNetworkWirelessSsidSchedules",
    "updateNetworkWirelessSsidSplashSettings",
    "updateNetworkWirelessSsidTrafficShapingRules",
    "updateNetworkWirelessSsidVpn",
    "updateOrganizationWirelessDevicesRadsecCertificatesAuthorities",
    "updateOrganizationWirelessLocationScanningReceiver",
    "updateOrganizationWirelessSsidsFirewallIsolationAllowlistEntry"
]

def to_snake_case(name):
    """Convert camelCase to snake_case."""
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

# Group methods by category
categories = {
    'SSID Core': [],
    'SSID Firewall': [],
    'SSID Identity PSK': [],
    'SSID Advanced': [],
    'Network Wireless': [],
    'Device Wireless': [],
    'Organization Wireless': [],
    'RF Profiles': [],
    'Ethernet Ports': [],
    'Air Marshal': [],
    'Location Scanning': [],
    'RADSEC': [],
    'Other': []
}

for method in sdk_methods:
    snake = to_snake_case(method)
    
    if 'ssid_firewall' in snake or 'ssid_traffic_shaping' in snake:
        categories['SSID Firewall'].append((method, snake))
    elif 'ssid_identity_psk' in snake:
        categories['SSID Identity PSK'].append((method, snake))
    elif 'ssid_hotspot' in snake or 'ssid_splash' in snake or 'ssid_schedule' in snake or 'ssid_vpn' in snake or 'ssid_bonjour' in snake or 'ssid_eap' in snake or 'ssid_device_type' in snake:
        categories['SSID Advanced'].append((method, snake))
    elif 'ssid' in snake:
        categories['SSID Core'].append((method, snake))
    elif 'device_wireless' in snake:
        categories['Device Wireless'].append((method, snake))
    elif 'organization_wireless' in snake:
        categories['Organization Wireless'].append((method, snake))
    elif 'rf_profile' in snake:
        categories['RF Profiles'].append((method, snake))
    elif 'ethernet_ports' in snake:
        categories['Ethernet Ports'].append((method, snake))
    elif 'air_marshal' in snake:
        categories['Air Marshal'].append((method, snake))
    elif 'location_scanning' in snake:
        categories['Location Scanning'].append((method, snake))
    elif 'radsec' in snake:
        categories['RADSEC'].append((method, snake))
    elif 'network_wireless' in snake:
        categories['Network Wireless'].append((method, snake))
    else:
        categories['Other'].append((method, snake))

print("=" * 60)
print("WIRELESS TOOLS STRUCTURE (116 SDK Methods)")
print("=" * 60)

total = 0
for cat, methods in categories.items():
    if methods:
        print(f"\n{cat}: {len(methods)} methods")
        total += len(methods)
        for camel, snake in methods[:3]:
            print(f"  - {snake}")
        if len(methods) > 3:
            print(f"  ... and {len(methods)-3} more")

print(f"\nTotal: {total} methods")
print("✅ Ready to generate comprehensive wireless tools file")
