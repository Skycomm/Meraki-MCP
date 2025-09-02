#!/usr/bin/env python3
"""
Check our wireless tools against official SDK methods.
"""

# Official SDK methods (116 total)
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

# Convert to snake_case for comparison with our tools
def to_snake_case(name):
    """Convert camelCase to snake_case."""
    import re
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

sdk_snake = [to_snake_case(m) for m in sdk_methods]

print(f"Official SDK has {len(sdk_methods)} wireless methods")
print("\nConverted to snake_case for our tools:")
for i, method in enumerate(sdk_snake[:10], 1):
    print(f"{i}. {method}")
print(f"... and {len(sdk_snake)-10} more")

# Save to file for comparison
with open("official_sdk_methods.txt", "w") as f:
    for method in sdk_snake:
        f.write(method + "\n")

print("\n✅ Saved official SDK methods to official_sdk_methods.txt")
