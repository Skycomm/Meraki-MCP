# 📚 Complete Cisco Meraki MCP Server Features Guide 2025

## 🎯 Overview
**Total Tools**: 94
**Categories**: 15
**New in 2025**: 39 tools

---

## 🏢 Organization Management (7 tools)

### 1. `get_organizations`
**Purpose**: List all organizations you have access to
**Returns**: Organization names, IDs, and URLs
**Example Output**:
```
Organizations:
1. Skycomm (ID: 686470)
2. Lab Environment (ID: 123456)
```

### 2. `get_organization`
**Purpose**: Get detailed info about specific organization
**Parameters**: `org_id`
**Returns**: Full org details, licensing model, API settings

### 3. `create_organization`
**Purpose**: Create a new organization
**Parameters**: `name`
**Returns**: New org ID and details

### 4. `update_organization`
**Purpose**: Modify organization settings
**Parameters**: `org_id`, `name`
**Use Case**: Rename organization

### 5. `delete_organization`
**Purpose**: Remove an organization
**Parameters**: `organization_id`
**Warning**: This is permanent!

### 6. `get_organization_networks`
**Purpose**: List all networks in an organization
**Returns**: Network names, types, tags
**Example**:
```
Networks in Skycomm:
- Reserve St (Combined)
- Suite 36 - Hollywood (Wireless)
- Lab Network (Switch)
```

### 7. `get_organization_devices`
**Purpose**: List all devices across organization
**Returns**: Serial numbers, models, networks

---

## 🌐 Network Management (8 tools)

### 8. `get_network`
**Purpose**: Get network configuration details
**Parameters**: `network_id`
**Returns**: Network settings, timezone, tags

### 9. `create_network`
**Purpose**: Create a new network
**Parameters**: `organization_id`, `name`, `productTypes`
**Product Types**: `wireless`, `switch`, `appliance`, `camera`

### 10. `update_network`
**Purpose**: Modify network settings
**Parameters**: `network_id`, `name`, `tags`
**Use Case**: Add tags for organization

### 11. `delete_network`
**Purpose**: Remove a network
**Parameters**: `network_id`
**Warning**: Removes all device associations

### 12. `get_network_devices`
**Purpose**: List devices in specific network
**Returns**: Device inventory for network
**Example**:
```
Devices in Reserve St:
- MX84 (Q2PD-7QTD-SZG2) - Security Appliance
- MS225-48LP (Q2HP-ZK5N-XG8L) - Switch
- MR33 (Q2DD-XXXX-YYYY) - Access Point
```

### 13. `get_network_clients`
**Purpose**: List connected clients
**Parameters**: `network_id`, `timespan` (seconds)
**Returns**: MAC, IP, hostname, usage

### 14. `get_network_vlans`
**Purpose**: List configured VLANs
**Returns**: VLAN IDs, names, subnets
**Example**:
```
VLANs:
- VLAN 1: Default (192.168.1.0/24)
- VLAN 10: Corporate (10.0.10.0/24)
- VLAN 20: Guest (172.16.20.0/24)
```

### 15. `get_network_alerts_settings`
**Purpose**: View alert configuration
**Returns**: Alert types, recipients, filters

---

## 📱 Systems Manager/MDM (6 tools) - NEW 2025

### 16. `get_network_sm_devices`
**Purpose**: List all managed mobile devices
**Returns**: Device OS, battery, user, apps
**Example**:
```
📱 Systems Manager Devices
iOS (89 devices):
- iPhone 12 - John Smith (85% battery)
- iPad Pro - Sarah Jones (42% battery) ⚠️

Android (38 devices):
- Samsung S21 - Mike Wilson (67% battery)
```

### 17. `get_network_sm_device_detail`
**Purpose**: Detailed device information
**Parameters**: `network_id`, `device_id`
**Returns**: Hardware specs, security status, network info

### 18. `get_network_sm_device_apps`
**Purpose**: List installed applications
**Returns**: App names, versions, managed status
**Example**:
```
Managed Apps:
- Microsoft Outlook v4.2.1 (2.3GB)
- Salesforce v3.1.0 (156MB)
- VPN Client v2.0 (45MB)

Other Apps:
- Instagram v245.0
- TikTok v28.1.0
```

### 19. `reboot_network_sm_devices`
**Purpose**: Remotely reboot devices
**Parameters**: `network_id`, `device_ids`
**Use Case**: Fix frozen devices

### 20. `get_network_sm_profiles`
**Purpose**: List configuration profiles
**Returns**: VPN, WiFi, email profiles
**Example**:
```
Profiles:
- Corporate VPN (deployed to 127 devices)
- Email Configuration (deployed to all)
- WiFi Auto-Join (deployed to iOS)
```

### 21. `get_network_sm_performance_history`
**Purpose**: Device performance metrics
**Returns**: CPU, memory, disk usage over time
**Visualization**:
```
CPU: [████████░░] 78%
Memory: [██████░░░░] 62%
Disk: [█████████░] 89%
```

---

## 📄 License Management (6 tools) - NEW 2025

### 22. `get_organization_licenses`
**Purpose**: View all licenses
**Returns**: License keys, expiration, assignment
**Note**: Only for per-device licensing model

### 23. `get_organization_licensing_coterm`
**Purpose**: Co-termination license info
**Returns**: Unified expiration date, device counts
**Example**:
```
Co-termination: March 15, 2026
- 120 AP licenses
- 85 Switch licenses
- 12 MX licenses
```

### 24. `claim_organization_license`
**Purpose**: Add new license key
**Parameters**: `org_id`, `license_key`
**Format**: `XXXX-XXXX-XXXX-XXXX`

### 25. `update_organization_license`
**Purpose**: Assign/unassign license to device
**Parameters**: `license_id`, `device_serial`

### 26. `move_organization_licenses`
**Purpose**: Transfer licenses between orgs
**Parameters**: `source_org_id`, `dest_org_id`, `license_ids`

### 27. `renew_organization_licenses_seats`
**Purpose**: Renew SM seats using unused licenses
**Use Case**: Extend mobile device management

---

## 🛡️ Policy Objects (6 tools) - NEW 2025

### 28. `get_organization_policy_objects`
**Purpose**: List security policy objects
**Returns**: IP ranges, domains, groups
**Example**:
```
Policy Objects:
Network Objects:
- Production-Servers (10.0.1.0/24)
- DMZ-Subnet (172.16.0.0/24)

Application Objects:
- Blocked-Sites (malware.com, phishing.net)
- Allowed-Cloud (*.microsoft.com, *.google.com)
```

### 29. `create_organization_policy_object`
**Purpose**: Define new security object
**Types**: `cidr` (IP), `fqdn` (domain), `ipAndMask`
**Examples**:
```python
# Block IP range
create_organization_policy_object(
    name="Malicious-IPs",
    type="ipv4",
    cidr="192.168.100.0/24"
)

# Block domain
create_organization_policy_object(
    name="Gambling-Sites",
    type="fqdn",
    fqdn="casino.com"
)
```

### 30. `update_organization_policy_object`
**Purpose**: Modify existing object
**Use Case**: Update IP ranges, rename objects

### 31. `delete_organization_policy_object`
**Purpose**: Remove policy object
**Warning**: Check if in use first

### 32. `get_organization_policy_objects_groups`
**Purpose**: List policy groups
**Returns**: Group memberships

### 33. `create_organization_policy_objects_group`
**Purpose**: Group related objects
**Example**: All database servers in one group

---

## 📊 Enhanced Monitoring (6 tools) - NEW 2025

### 34. `get_organization_api_usage`
**Purpose**: API analytics dashboard
**Metrics**: Calls per endpoint, errors, rate limits
**Visualization**:
```
API Usage (24h):
/networks: ████████████ 342 calls
/devices:  ████████░░░░ 198 calls
/clients:  ██████░░░░░░ 156 calls

Response Codes:
200 OK: ████████████ 94.6%
429 Rate: █░░░░░░░░░░░  3.6%
404 Error: █░░░░░░░░░░░  1.8%
```

### 35. `get_organization_switch_ports_history`
**Purpose**: Organization-wide port statistics
**Returns**: Total ports, active count, power usage
**Example**:
```
Switch Port Summary:
Total: 2,456 ports
Active: 1,823 (74.2%)
Errors: 12 ports
Power: 3,245W total PoE
```

### 36. `get_organization_devices_migration_status`
**Purpose**: Track device migrations
**Shows**: Progress bars for moves between networks

### 37. `get_device_memory_history`
**Purpose**: Device memory utilization
**Note**: Beta API - limited availability

### 38. `get_device_cpu_power_mode_history`
**Purpose**: Wireless CPU power states
**Returns**: Power mode distribution

### 39. `get_device_wireless_cpu_load`
**Purpose**: Real-time CPU monitoring
**Returns**: Load percentage, per-core stats

---

## 🧪 Beta/Early Access (6 tools) - NEW 2025

### 40. `get_organization_early_access_features`
**Purpose**: List available beta features
**Returns**: 15+ features with descriptions
**Example**:
```
Available Beta Features:
✅ Early API Access (enabled)
✅ AnyConnect VPN v2 (enabled)
🔒 SmartPorts Automation
🔒 VLAN Database
🔒 Client360 Analytics
```

### 41. `get_organization_early_access_opt_ins`
**Purpose**: Show enabled beta features
**Returns**: Active features with dates

### 42. `enable_organization_early_access_feature`
**Purpose**: Turn on beta feature
**Parameters**: `feature_id` (e.g., "has_vlan_db")
**Warning**: Affects all API users!

### 43. `disable_organization_early_access_feature`
**Purpose**: Turn off beta feature
**Parameters**: `opt_in_id`

### 44. `get_organization_api_analytics`
**Purpose**: Enhanced API analytics
**Note**: Requires early access

### 45. `check_beta_apis_status`
**Purpose**: Beta API availability check
**Returns**: Status of cutting-edge features

---

## 🔧 Live Tools (9 tools) - BETA with Early Access

### 46. `create_device_ping_test`
**Purpose**: Ping FROM Meraki devices
**Parameters**: `serial`, `target`, `count`
**Revolutionary**: Test from device perspective!
**Example**:
```bash
# Traditional: You → Meraki device
# Live Tools: Meraki device → Internet

create_device_ping_test 
  serial: "Q2PD-7QTD-SZG2"
  target: "google.com"
  count: 10
```

### 47. `get_device_ping_test`
**Purpose**: Retrieve ping results
**Returns**: Packet loss, latency stats
**Example Output**:
```
Ping Results:
Target: google.com
Sent: 10 packets
Received: 10 packets
Loss: 0%
Latency: Min 12ms, Avg 15ms, Max 18ms
```

### 48. `create_device_throughput_test`
**Purpose**: Bandwidth test between devices
**Parameters**: `serial`, `target_serial`
**Use Case**: Verify link speeds

### 49. `get_device_throughput_test`
**Purpose**: Get bandwidth results
**Returns**: Upload/download speeds
**Example**:
```
Throughput Test:
Download: 945 Mbps ⬇️
Upload: 932 Mbps ⬆️
```

### 50. `create_switch_cable_test`
**Purpose**: Test cable quality
**Parameters**: `serial`, `port`
**Tests**: All 4 wire pairs

### 51. `get_switch_cable_test`
**Purpose**: Cable test results
**Returns**: Pair status, length
**Example**:
```
Cable Test - Port 24:
Pair 1: ✅ OK (23m)
Pair 2: ✅ OK (23m)
Pair 3: ❌ Open (12m) - Broken!
Pair 4: ✅ OK (23m)
```

### 52. `create_switch_mac_table`
**Purpose**: Query MAC address table
**Returns**: Real-time MAC locations

### 53. `get_switch_mac_table`
**Purpose**: MAC table results
**Example**:
```
MAC Table (156 entries):
VLAN 10:
- aa:bb:cc:dd:ee:ff → Port 12
- 11:22:33:44:55:66 → Port 13

VLAN 20:
- 77:88:99:aa:bb:cc → Port 1
```

### 54. `blink_device_leds`
**Purpose**: Physically identify device
**Parameters**: `serial`, `duration`
**Use Case**: "Which switch is this?"

### 55. `create_device_wake_on_lan`
**Purpose**: Wake sleeping computers
**Parameters**: `serial`, `vlan_id`, `mac_address`

---

## 🔒 Security & Firewall (8 tools)

### 56. `get_network_appliance_firewall_l3_rules`
**Purpose**: View Layer 3 firewall rules
**Returns**: Allow/deny rules with ports

### 57. `update_network_appliance_firewall_l3_rules`
**Purpose**: Modify firewall rules
**Use Case**: Block new threats

### 58. `get_network_appliance_content_filtering`
**Purpose**: Web filtering settings
**Returns**: Blocked categories

### 59. `get_network_appliance_vpn_site_to_site`
**Purpose**: VPN tunnel status
**Returns**: Peer connectivity

### 60. `get_network_appliance_security_malware`
**Purpose**: Malware protection status
**Returns**: Threat detections

### 61. `get_network_appliance_security_intrusion`
**Purpose**: IDS/IPS alerts
**Returns**: Intrusion attempts

### 62. `get_organization_alerts`
**Purpose**: Security alert profiles
**Returns**: Alert configurations

### 63. `update_network_alerts_settings`
**Purpose**: Configure alert recipients
**Parameters**: Email addresses, alert types

---

## 📡 Wireless Management (10 tools)

### 64. `get_network_wireless_ssids`
**Purpose**: List wireless networks
**Returns**: SSID names, security settings

### 65. `get_network_wireless_passwords`
**Purpose**: Retrieve WiFi passwords
**Returns**: PSK for each SSID
**Example**:
```
WiFi Passwords:
- Corporate: "SecurePass123!"
- Guest: "Welcome2024"
- IoT: "Dev1ce$Only"
```

### 66. `update_network_wireless_ssid`
**Purpose**: Modify SSID settings
**Parameters**: Name, PSK, enabled status

### 67. `get_network_wireless_clients`
**Purpose**: Connected wireless clients
**Returns**: Signal strength, data usage

### 68. `get_network_wireless_usage`
**Purpose**: Bandwidth usage history
**Note**: Requires device or client ID

### 69. `get_network_connection_stats`
**Purpose**: Connection success rates
**Returns**: Auth failures, association issues

### 70. `get_network_latency_stats`
**Purpose**: Wireless latency metrics
**Returns**: Latency distribution

### 71. `get_network_wireless_rf_profiles`
**Purpose**: Radio frequency settings
**Returns**: Channel width, power levels

### 72. `get_network_wireless_air_marshal`
**Purpose**: Rogue AP detection
**Returns**: Unauthorized access points

### 73. `get_network_wireless_channel_utilization`
**Purpose**: Channel congestion data
**Returns**: Utilization percentages

---

## 🔌 Switch Management (6 tools)

### 74. `get_device_switch_ports`
**Purpose**: Port configurations
**Returns**: VLAN, PoE, trunk settings

### 75. `update_device_switch_port`
**Purpose**: Modify port settings
**Parameters**: VLAN, PoE, enabled

### 76. `get_device_switch_port_statuses`
**Purpose**: Real-time port status
**Returns**: Link state, errors, power draw

### 77. `get_device_switch_vlans`
**Purpose**: VLAN configuration
**Note**: Network-wide, not per switch

### 78. `create_device_switch_vlan`
**Purpose**: Create new VLAN
**Parameters**: ID, name, subnet

### 79. `get_device_switch_port_statuses`
**Purpose**: Port health monitoring
**Shows**: CRC errors, collisions

---

## 📹 Camera Operations (5 tools)

### 80. `get_device_camera_video_link`
**Purpose**: Live/recorded video access
**Parameters**: `serial`, `timestamp`

### 81. `get_device_camera_snapshot`
**Purpose**: Current image capture
**Returns**: JPEG URL

### 82. `get_device_camera_video_settings`
**Purpose**: Quality configuration
**Returns**: Resolution, FPS, retention

### 83. `update_device_camera_video_settings`
**Purpose**: Adjust video quality
**Use Case**: Balance quality vs storage

### 84. `get_device_camera_analytics_zones`
**Purpose**: Motion detection areas
**Returns**: Zone definitions

### 85. `get_device_camera_sense`
**Purpose**: Motion sensitivity settings
**Returns**: Detection thresholds

---

## 📈 Analytics & Performance (6 tools)

### 86. `get_network_traffic_analysis`
**Purpose**: Application visibility
**Returns**: Top apps by bandwidth

### 87. `get_organization_devices_uplinks_loss_and_latency`
**Purpose**: WAN health metrics
**Returns**: Packet loss percentages
**Example**:
```
Uplink Health:
WAN 1: 0.1% loss, 15ms latency ✅
WAN 2: 2.5% loss, 45ms latency ⚠️
```

### 88. `get_organization_appliance_uplink_statuses`
**Purpose**: Real-time uplink status
**Returns**: Active/failover state

### 89. `get_device_clients`
**Purpose**: Clients per device
**Use Case**: Load balancing

### 90. `get_device_status`
**Purpose**: Device health check
**Returns**: Online status, uptime

### 91. `get_organization_firmware_upgrades`
**Purpose**: Available updates
**Returns**: Current vs available versions

---

## 🔧 Device Operations (3 tools)

### 92. `update_device`
**Purpose**: Modify device settings
**Parameters**: Name, tags, address

### 93. `reboot_device`
**Purpose**: Remote device restart
**Warning**: Causes downtime!

### 94. `get_device`
**Purpose**: Detailed device info
**Returns**: Model, serial, network

---

## 📋 Complete Tool Summary

### By Category:
1. **Organization**: 7 tools
2. **Network**: 8 tools  
3. **Systems Manager**: 6 tools (NEW)
4. **Licensing**: 6 tools (NEW)
5. **Policy Objects**: 6 tools (NEW)
6. **Monitoring**: 6 tools (NEW)
7. **Beta/Early Access**: 6 tools (NEW)
8. **Live Tools**: 9 tools (BETA)
9. **Security**: 8 tools
10. **Wireless**: 10 tools
11. **Switch**: 6 tools
12. **Camera**: 5 tools
13. **Analytics**: 6 tools
14. **Device Ops**: 3 tools

### By Status:
- **Production Ready**: 70 tools
- **Beta (Early Access)**: 15 tools
- **Requires License**: 9 tools (SM, Camera)

### By Impact:
- **Read-Only**: 75 tools
- **Configuration**: 15 tools
- **Disruptive**: 4 tools (reboot, delete)

---

## 🚀 Quick Start Examples

### 1. Network Health Check
```python
# Check overall health
get_organization_devices_uplinks_loss_and_latency org_id: "686470"
get_network_clients network_id: "L_669347494617953785"
get_device_switch_port_statuses serial: "Q2HP-ZK5N-XG8L"
```

### 2. Security Audit
```python
# Review security settings
get_network_appliance_firewall_l3_rules network_id: "L_669347494617953785"
get_network_appliance_security_malware network_id: "L_669347494617953785"
get_network_wireless_air_marshal network_id: "L_669347494617953785"
```

### 3. Troubleshooting Workflow
```python
# Step 1: Test connectivity
create_device_ping_test serial: "Q2PD-7QTD-SZG2" target: "8.8.8.8"

# Step 2: Check physical layer
create_switch_cable_test serial: "Q2HP-ZK5N-XG8L" port: "24"

# Step 3: Find device
create_switch_mac_table serial: "Q2HP-ZK5N-XG8L"

# Step 4: Identify visually
blink_device_leds serial: "Q2HP-ZK5N-XG8L"
```

---

## 💡 Pro Tips

1. **Use Beta Features**: Early access unlocks powerful diagnostics
2. **Batch Operations**: Run multiple tools in parallel
3. **Monitor Rate Limits**: Stay under 10 calls/second
4. **Tag Everything**: Use tags for easy filtering
5. **Document Changes**: Track all modifications

---

## 🎯 Conclusion

The Cisco Meraki MCP Server now provides comprehensive network management through 94 specialized tools. With 2025 enhancements including live diagnostics, enhanced monitoring, and beta features, you have unprecedented visibility and control over your infrastructure.

**Remember**: With great power comes great responsibility. Always test in lab first!