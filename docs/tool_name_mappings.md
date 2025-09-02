# MCP Tool Name Mappings - 1:1 SDK Reference

This document maintains the mapping between shortened MCP tool names and their original SDK method names for perfect 1:1 correspondence.

## Overview
- **33 tool names** were shortened to meet MCP's 64-character limit
- **All original SDK method names preserved** in function names and descriptions
- **Perfect 1:1 mapping maintained** with official Cisco Meraki Python SDK

## Shortened Tool Names by Module

### Wireless Module (13 names shortened)
| Shortened MCP Name (≤64 chars) | Original SDK Method | Function Name |
|---|---|---|
| `get_org_wireless_devices_channel_util_hist_by_net_by_interval` | `getOrganizationWirelessDevicesChannelUtilizationHistoryByNetworkByInterval` | `get_organization_wireless_devices_channel_utilization_history_by_network_by_interval` |
| `get_org_wireless_devices_channel_util_hist_by_dev_by_interval` | `getOrganizationWirelessDevicesChannelUtilizationHistoryByDeviceByInterval` | `get_organization_wireless_devices_channel_utilization_history_by_device_by_interval` |
| `get_org_wireless_devices_radsec_certs_authorities_crls_deltas` | `getOrganizationWirelessDevicesRadsecCertificatesAuthoritiesCrlsDeltas` | `get_organization_wireless_devices_radsec_certificates_authorities_crls_deltas` |
| `get_org_wireless_devices_radsec_certs_authorities_crls` | `getOrganizationWirelessDevicesRadsecCertificatesAuthoritiesCrls` | `get_organization_wireless_devices_radsec_certificates_authorities_crls` |
| `get_org_wireless_devices_radsec_certs_authorities` | `getOrganizationWirelessDevicesRadsecCertificatesAuthorities` | `get_organization_wireless_devices_radsec_certificates_authorities` |
| `create_org_wireless_devices_radsec_certs_authority` | `createOrganizationWirelessDevicesRadsecCertificatesAuthority` | `create_organization_wireless_devices_radsec_certificates_authority` |
| `update_org_wireless_devices_radsec_certs_authorities` | `updateOrganizationWirelessDevicesRadsecCertificatesAuthorities` | `update_organization_wireless_devices_radsec_certificates_authorities` |
| `get_org_wireless_devices_channel_utilization_by_network` | `getOrganizationWirelessDevicesChannelUtilizationByNetwork` | `get_organization_wireless_devices_channel_utilization_by_network` |
| `get_org_wireless_ssids_firewall_isolation_allowlist_entries` | `getOrganizationWirelessSsidsFirewallIsolationAllowlistEntries` | `get_organization_wireless_ssids_firewall_isolation_allowlist_entries` |
| `create_org_wireless_ssids_firewall_isolation_allowlist_entry` | `createOrganizationWirelessSsidsFirewallIsolationAllowlistEntry` | `create_organization_wireless_ssids_firewall_isolation_allowlist_entry` |
| `update_org_wireless_ssids_firewall_isolation_allowlist_entry` | `updateOrganizationWirelessSsidsFirewallIsolationAllowlistEntry` | `update_organization_wireless_ssids_firewall_isolation_allowlist_entry` |
| `delete_org_wireless_ssids_firewall_isolation_allowlist_entry` | `deleteOrganizationWirelessSsidsFirewallIsolationAllowlistEntry` | `delete_organization_wireless_ssids_firewall_isolation_allowlist_entry` |
| `get_org_wireless_devices_wireless_controllers_by_device` | `getOrganizationWirelessDevicesWirelessControllersByDevice` | `get_organization_wireless_devices_wireless_controllers_by_device` |

### Switch Module (6 names shortened)
| Shortened MCP Name (≤64 chars) | Original SDK Method | Function Name |
|---|---|---|
| `create_network_switch_dhcp_server_policy_arp_trusted_server` | `createNetworkSwitchDhcpServerPolicyArpInspectionTrustedServer` | `create_network_switch_dhcp_server_policy_arp_inspection_trusted_server` |
| `delete_network_switch_dhcp_server_policy_arp_trusted_server` | `deleteNetworkSwitchDhcpServerPolicyArpInspectionTrustedServer` | `delete_network_switch_dhcp_server_policy_arp_inspection_trusted_server` |
| `get_network_switch_dhcp_server_policy_arp_trusted_servers` | `getNetworkSwitchDhcpServerPolicyArpInspectionTrustedServers` | `get_network_switch_dhcp_server_policy_arp_inspection_trusted_servers` |
| `get_network_switch_dhcp_server_policy_arp_warnings_by_device` | `getNetworkSwitchDhcpServerPolicyArpInspectionWarningsByDevice` | `get_network_switch_dhcp_server_policy_arp_inspection_warnings_by_device` |
| `get_org_switch_ports_usage_history_by_device_by_interval` | `getOrganizationSwitchPortsUsageHistoryByDeviceByInterval` | `get_organization_switch_ports_usage_history_by_device_by_interval` |
| `update_network_switch_dhcp_server_policy_arp_trusted_server` | `updateNetworkSwitchDhcpServerPolicyArpInspectionTrustedServer` | `update_network_switch_dhcp_server_policy_arp_inspection_trusted_server` |

### Organizations Module (6 names shortened)
| Shortened MCP Name (≤64 chars) | Original SDK Method | Function Name |
|---|---|---|
| `create_org_inventory_onboarding_cloud_monitoring_export_event` | `createOrganizationInventoryOnboardingCloudMonitoringExportEvent` | `create_organization_inventory_onboarding_cloud_monitoring_export_event` |
| `create_org_inventory_onboarding_cloud_monitoring_import` | `createOrganizationInventoryOnboardingCloudMonitoringImport` | `create_organization_inventory_onboarding_cloud_monitoring_import` |
| `create_org_inventory_onboarding_cloud_monitoring_prepare` | `createOrganizationInventoryOnboardingCloudMonitoringPrepare` | `create_organization_inventory_onboarding_cloud_monitoring_prepare` |
| `generate_org_devices_packet_capture_capture_download_url` | `generateOrganizationDevicesPacketCaptureCaptureDownloadUrl` | `generate_organization_devices_packet_capture_capture_download_url` |
| `get_org_api_requests_overview_response_codes_by_interval` | `getOrganizationApiRequestsOverviewResponseCodesByInterval` | `get_organization_api_requests_overview_response_codes_by_interval` |
| `get_org_devices_system_memory_usage_history_by_interval` | `getOrganizationDevicesSystemMemoryUsageHistoryByInterval` | `get_organization_devices_system_memory_usage_history_by_interval` |

### Appliance Module (5 names shortened)
| Shortened MCP Name (≤64 chars) | Original SDK Method | Function Name |
|---|---|---|
| `bulk_org_appliance_dns_local_profiles_assignments_create` | `bulkOrganizationApplianceDnsLocalProfilesAssignmentsCreate` | `bulk_organization_appliance_dns_local_profiles_assignments_create` |
| `get_org_appliance_firewall_multicast_forwarding_by_network` | `getOrganizationApplianceFirewallMulticastForwardingByNetwork` | `get_organization_appliance_firewall_multicast_forwarding_by_network` |
| `get_org_appliance_traffic_shaping_vpn_exclusions_by_network` | `getOrganizationApplianceTrafficShapingVpnExclusionsByNetwork` | `get_organization_appliance_traffic_shaping_vpn_exclusions_by_network` |
| `get_network_appliance_firewall_l7_fw_rules_app_categories` | `getNetworkApplianceFirewallL7FirewallRulesApplicationCategories` | `get_network_appliance_firewall_l7_firewall_rules_application_categories` |
| `get_network_appliance_traffic_shaping_custom_perf_classes` | `getNetworkApplianceTrafficShapingCustomPerformanceClasses` | `get_network_appliance_traffic_shaping_custom_performance_classes` |

### Licensing Module (2 names shortened)
| Shortened MCP Name (≤64 chars) | Original SDK Method | Function Name |
|---|---|---|
| `get_admin_licensing_subscription_subs_compliance_statuses` | `getAdministeredLicensingSubscriptionSubscriptionsComplianceStatuses` | `get_administered_licensing_subscription_subscriptions_compliance_statuses` |
| `validate_admin_licensing_subscription_subscriptions_claim_key` | `validateAdministeredLicensingSubscriptionSubscriptionsClaimKey` | `validate_administered_licensing_subscription_subscriptions_claim_key` |

### Camera Module (1 name shortened)
| Shortened MCP Name (≤64 chars) | Original SDK Method | Function Name |
|---|---|---|
| `get_org_camera_detections_history_by_boundary_by_interval` | `getOrganizationCameraDetectionsHistoryByBoundaryByInterval` | `get_organization_camera_detections_history_by_boundary_by_interval` |

## Common Abbreviations Used
- `organization` → `org`
- `certificates` → `certs` 
- `utilization` → `util`
- `history` → `hist` (when needed)
- `network` → `net` (when needed)
- `device` → `dev` (when needed)
- `subscriptions` → `subs` (when needed)
- `performance` → `perf`
- `firewall` → `fw` (when needed)
- `application` → `app` (when needed)
- `administered` → `admin`

## Validation Status
✅ **All 816 SDK tools now MCP compliant**
✅ **All tool names under 64 characters**
✅ **Perfect 1:1 mapping maintained with SDK**
✅ **Original function names preserved for SDK calls**

## Usage in MCP Client
The shortened names are used in MCP tool calls, but all functionality remains identical to the original SDK methods. Example:

```python
# MCP tool call uses shortened name
result = await mcp_client.call_tool("get_org_wireless_devices_channel_util_hist_by_net_by_interval", {...})

# But internally calls original SDK method
meraki_client.dashboard.wireless.getOrganizationWirelessDevicesChannelUtilizationHistoryByNetworkByInterval(...)
```