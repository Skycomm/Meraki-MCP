# 🧪 Complete Test Questions for All Cisco Meraki MCP Server Features

## 📊 API Analytics & Monitoring

### 1. API Usage Analytics
**Q**: "What are the top 10 most used API endpoints in the last 24 hours?"
**Tool**: `get_organization_api_analytics`
**Expected**: List of endpoints with call counts, response codes, rate limit warnings

### 2. API Error Analysis
**Q**: "How many API calls failed with 4xx or 5xx errors today?"
**Tool**: `get_organization_api_analytics`
**Expected**: Error count breakdown by response code

### 3. Rate Limit Monitoring
**Q**: "Are we close to hitting API rate limits?"
**Tool**: `get_organization_api_analytics`
**Expected**: 429 response count and percentage

### 4. Switch Port Organization Stats
**Q**: "What percentage of switch ports are currently active across all locations?"
**Tool**: `get_organization_switch_ports_history`
**Expected**: Total ports, active count, utilization percentage

### 5. Power Usage Monitoring
**Q**: "What's the total PoE power consumption across all switches?"
**Tool**: `get_organization_switch_ports_history`
**Expected**: Total power in watts

### 6. Device Migration Status
**Q**: "Are any devices currently being migrated between networks?"
**Tool**: `get_organization_devices_migration_status`
**Expected**: List of devices with migration progress

## 🔧 Live Tools (Beta)

### 7. Ping Test - Internet Connectivity
**Q**: "Can the MX at Reserve St ping Google DNS (8.8.8.8)?"
**Tool**: `create_device_ping_test` then `get_device_ping_test`
**Expected**: 0% packet loss, latency < 50ms

### 8. Ping Test - Internal Connectivity
**Q**: "Can Switch-01 reach the internal server at 192.168.1.100?"
**Tool**: `create_device_ping_test`
**Expected**: Successful pings with low latency

### 9. Throughput Between Switches
**Q**: "What's the actual bandwidth between the core switch and distribution switch?"
**Tool**: `create_device_throughput_test` then `get_device_throughput_test`
**Expected**: Near line-rate speeds (900+ Mbps for gigabit)

### 10. Cable Quality Check
**Q**: "Is the cable on switch port 24 functioning properly?"
**Tool**: `create_switch_cable_test` then `get_switch_cable_test`
**Expected**: All 4 pairs OK, correct length

### 11. Identify Faulty Cable
**Q**: "Which ports have cable issues on Switch-Floor2?"
**Tool**: `create_switch_cable_test` for multiple ports
**Expected**: List of ports with pair failures

### 12. MAC Address Search
**Q**: "Which switch port is device with MAC aa:bb:cc:dd:ee:ff connected to?"
**Tool**: `create_switch_mac_table` then `get_switch_mac_table`
**Expected**: Port number and VLAN

### 13. VLAN Member Count
**Q**: "How many devices are currently on VLAN 10?"
**Tool**: `get_switch_mac_table`
**Expected**: Count of MAC addresses on VLAN 10

### 14. Physical Device Location
**Q**: "Which device in the server room is Q2HP-ZK5N-XG8L?"
**Tool**: `blink_device_leds`
**Expected**: LEDs blink for identification

### 15. Wake Sleeping Computer
**Q**: "Can we wake up the conference room PC (MAC: 11:22:33:44:55:66)?"
**Tool**: `create_device_wake_on_lan`
**Expected**: WOL packet sent confirmation

## 🛡️ Policy Objects

### 16. Security Policy Inventory
**Q**: "What IP address objects are defined for our security policies?"
**Tool**: `get_organization_policy_objects`
**Expected**: List of IP/CIDR objects with names

### 17. Create Server Group
**Q**: "Can we create a policy object for our web servers (192.168.1.10-15)?"
**Tool**: `create_organization_policy_object`
**Expected**: Object created with ID

### 18. Block Malicious Domain
**Q**: "How do we block access to malicious-site.com across all networks?"
**Tool**: `create_organization_policy_object` with type: "fqdn"
**Expected**: FQDN object created

### 19. Policy Group Management
**Q**: "Can we group all server objects into a 'Production-Servers' group?"
**Tool**: `create_organization_policy_objects_group`
**Expected**: Group created with member objects

### 20. Update Security Object
**Q**: "Can we change the IP range for 'Guest-Network' object?"
**Tool**: `update_organization_policy_object`
**Expected**: Object updated successfully

### 21. Policy Cleanup
**Q**: "Which policy objects are no longer in use?"
**Tool**: `get_organization_policy_objects`
**Expected**: Objects not assigned to any rules

## 📱 Systems Manager (MDM)

### 22. Device Inventory
**Q**: "How many iOS vs Android devices are enrolled in MDM?"
**Tool**: `get_network_sm_devices`
**Expected**: Count by OS type

### 23. Battery Monitoring
**Q**: "Which mobile devices have battery level below 20%?"
**Tool**: `get_network_sm_devices`
**Expected**: List of devices with low battery

### 24. Device Details
**Q**: "What's the storage usage on John's iPhone?"
**Tool**: `get_network_sm_device_detail`
**Expected**: Storage percentage and GB used

### 25. App Inventory
**Q**: "What apps are installed on the sales team iPads?"
**Tool**: `get_network_sm_device_apps`
**Expected**: List of apps with versions

### 26. Unauthorized App Detection
**Q**: "Are there any non-approved apps on company devices?"
**Tool**: `get_network_sm_device_apps`
**Expected**: Apps not in managed list

### 27. Device Performance
**Q**: "Is the CEO's iPad running slow (high CPU/memory)?"
**Tool**: `get_network_sm_performance_history`
**Expected**: CPU and memory usage trends

### 28. Remote Reboot
**Q**: "Can we reboot the frozen tablet in reception?"
**Tool**: `reboot_network_sm_devices`
**Expected**: Reboot command sent

### 29. Configuration Profiles
**Q**: "What VPN profiles are deployed to remote workers?"
**Tool**: `get_network_sm_profiles`
**Expected**: List of profiles with settings

## 📄 License Management

### 30. License Expiration
**Q**: "Which licenses are expiring in the next 30 days?"
**Tool**: `get_organization_licenses`
**Expected**: List with expiration dates

### 31. License Utilization
**Q**: "How many unused licenses do we have?"
**Tool**: `get_organization_licenses`
**Expected**: Count by device type

### 32. Co-term Status
**Q**: "What's our co-termination date and device count?"
**Tool**: `get_organization_licensing_coterm`
**Expected**: Single expiration date, counts

### 33. License Assignment
**Q**: "Can we assign the spare AP license to the new device?"
**Tool**: `update_organization_license`
**Expected**: License assigned to serial

### 34. License Transfer
**Q**: "Can we move 5 switch licenses from Lab to Production org?"
**Tool**: `move_organization_licenses`
**Expected**: Transfer confirmation

### 35. Seat Renewal
**Q**: "Can we renew the expiring SM seats?"
**Tool**: `renew_organization_licenses_seats`
**Expected**: New expiration date

## 🧪 Beta/Early Access

### 36. Available Features
**Q**: "What beta features can we enable?"
**Tool**: `get_organization_early_access_features`
**Expected**: List of 15+ features

### 37. Current Beta Status
**Q**: "Which beta features are already enabled?"
**Tool**: `get_organization_early_access_opt_ins`
**Expected**: Active features list

### 38. Enable New Beta
**Q**: "Can we enable the VLAN Database beta feature?"
**Tool**: `enable_organization_early_access_feature`
**Expected**: Feature enabled confirmation

### 39. Beta Impact Check
**Q**: "Will enabling SmartPorts affect all networks?"
**Tool**: `check_beta_apis_status`
**Expected**: Scope and impact details

### 40. Disable Beta Feature
**Q**: "How do we disable a beta feature if it causes issues?"
**Tool**: `disable_organization_early_access_feature`
**Expected**: Feature disabled

## 🌐 Network Management

### 41. Network Inventory
**Q**: "How many networks do we have and what types?"
**Tool**: `get_organization_networks`
**Expected**: Count by type (wireless, switch, etc.)

### 42. Device Status Check
**Q**: "Are all devices at Reserve St online?"
**Tool**: `get_network_devices`
**Expected**: Online/offline status

### 43. Client Count
**Q**: "How many clients are connected right now?"
**Tool**: `get_network_clients`
**Expected**: Total client count

### 44. Wireless Password Retrieval
**Q**: "What's the WiFi password for the Guest network?"
**Tool**: `get_network_wireless_passwords`
**Expected**: PSK for Guest SSID

### 45. VLAN Configuration
**Q**: "What VLANs are configured on the network?"
**Tool**: `get_network_vlans`
**Expected**: VLAN list with subnets

## 🚨 Alerts & Security

### 46. Alert Configuration
**Q**: "What network alerts are currently enabled?"
**Tool**: `get_network_alerts_settings`
**Expected**: List of alert types and recipients

### 47. Security Events
**Q**: "Were there any security alerts in the last hour?"
**Tool**: `get_organization_alerts`
**Expected**: Security event list

### 48. Firewall Rules
**Q**: "What L3 firewall rules are blocking traffic?"
**Tool**: `get_network_appliance_firewall_l3_rules`
**Expected**: Deny rules list

### 49. Content Filtering
**Q**: "What categories are blocked by content filtering?"
**Tool**: `get_network_appliance_content_filtering`
**Expected**: Blocked category list

### 50. VPN Status
**Q**: "Is the site-to-site VPN tunnel up?"
**Tool**: `get_network_appliance_vpn_site_to_site`
**Expected**: Tunnel status and peers

## 📹 Camera Operations

### 51. Camera Snapshot
**Q**: "Can we get a current snapshot from the lobby camera?"
**Tool**: `get_device_camera_snapshot`
**Expected**: Image URL

### 52. Video History
**Q**: "Can we review video from 2 hours ago?"
**Tool**: `get_device_camera_video_link`
**Expected**: Video playback link

### 53. Camera Settings
**Q**: "What quality settings are configured for cameras?"
**Tool**: `get_device_camera_video_settings`
**Expected**: Resolution and fps

### 54. Motion Detection
**Q**: "Which cameras have motion detection enabled?"
**Tool**: `get_device_camera_sense`
**Expected**: Motion settings list

### 55. Analytics Zones
**Q**: "What areas are configured for people counting?"
**Tool**: `get_device_camera_analytics_zones`
**Expected**: Zone definitions

## 🔀 Switch Operations

### 56. Port Status
**Q**: "Which switch ports are showing errors?"
**Tool**: `get_device_switch_port_statuses`
**Expected**: Ports with error counts

### 57. Port Configuration
**Q**: "What's the VLAN configuration for port 10?"
**Tool**: `get_device_switch_ports`
**Expected**: VLAN, voice VLAN, trunk settings

### 58. PoE Status
**Q**: "Which devices are drawing PoE power?"
**Tool**: `get_device_switch_port_statuses`
**Expected**: Ports with power draw

### 59. Port Security
**Q**: "Are there any port security violations?"
**Tool**: `get_device_switch_port_statuses`
**Expected**: Security status per port

### 60. Trunk Verification
**Q**: "Which ports are configured as trunks?"
**Tool**: `get_device_switch_ports`
**Expected**: List of trunk ports

## 📡 Wireless Analytics

### 61. Connection Stats
**Q**: "What's the connection success rate for the last hour?"
**Tool**: `get_network_connection_stats`
**Expected**: Success/failure percentages

### 62. Latency Analysis
**Q**: "Is there high latency on the wireless network?"
**Tool**: `get_network_latency_stats`
**Expected**: Latency distribution

### 63. Channel Utilization
**Q**: "Which channels are most congested?"
**Tool**: `get_network_wireless_channel_utilization`
**Expected**: Utilization by channel

### 64. Rogue AP Detection
**Q**: "Are there any rogue access points detected?"
**Tool**: `get_network_wireless_air_marshal`
**Expected**: Rogue AP list

### 65. RF Profile Check
**Q**: "What RF profiles are configured?"
**Tool**: `get_network_wireless_rf_profiles`
**Expected**: Profile settings

## 🔧 Device Operations

### 66. Firmware Status
**Q**: "Which devices need firmware updates?"
**Tool**: `get_organization_firmware_upgrades`
**Expected**: Devices below latest version

### 67. Device Uptime
**Q**: "Has any device rebooted unexpectedly?"
**Tool**: `get_device`
**Expected**: Uptime information

### 68. Serial Number Lookup
**Q**: "What model is device Q2PD-7QTD-SZG2?"
**Tool**: `get_device`
**Expected**: Model and details

### 69. Device Tags
**Q**: "Which devices are tagged as 'critical'?"
**Tool**: `get_network_devices`
**Expected**: Devices with critical tag

### 70. Reboot Schedule
**Q**: "Can we schedule a reboot for maintenance?"
**Tool**: `reboot_device`
**Expected**: Reboot scheduled

## 🏢 Organization Management

### 71. Admin List
**Q**: "Who has admin access to the dashboard?"
**Tool**: `get_organization`
**Expected**: Admin user list

### 72. Organization Settings
**Q**: "What's the organization ID for Skycomm?"
**Tool**: `get_organizations`
**Expected**: Org ID and details

### 73. Network Creation
**Q**: "Can we create a new network for the branch office?"
**Tool**: `create_network`
**Expected**: Network created

### 74. Configuration Templates
**Q**: "What configuration templates are available?"
**Tool**: Resources query
**Expected**: Template list

### 75. Change Log
**Q**: "What configuration changes were made today?"
**Tool**: `get_organization_api_requests`
**Expected**: PUT/POST requests

## Performance Monitoring

### 76. Uplink Status
**Q**: "What's the WAN uplink utilization?"
**Tool**: `get_organization_appliance_uplink_statuses`
**Expected**: Bandwidth usage

### 77. Packet Loss Detection
**Q**: "Is there packet loss on the primary WAN?"
**Tool**: `get_organization_devices_uplinks_loss_and_latency`
**Expected**: Loss percentage

### 78. Application Performance
**Q**: "Which applications are using the most bandwidth?"
**Tool**: Analytics tools
**Expected**: Top applications

### 79. Client Performance
**Q**: "Which clients have poor connectivity?"
**Tool**: `get_network_clients`
**Expected**: Clients with low signal

### 80. Historical Trends
**Q**: "How has network usage changed over the past week?"
**Tool**: Various analytics with timespan
**Expected**: Usage trends

## 🛡️ Security Monitoring

### 81. Malware Detection
**Q**: "Were any malware attempts blocked?"
**Tool**: `get_network_appliance_security_malware`
**Expected**: Blocked threats

### 82. Intrusion Detection
**Q**: "Are there any IDS alerts?"
**Tool**: `get_network_appliance_security_intrusion`
**Expected**: Intrusion events

### 83. Client Isolation
**Q**: "Which SSIDs have client isolation enabled?"
**Tool**: `get_network_wireless_ssids`
**Expected**: Isolation settings

### 84. Guest Network Security
**Q**: "Is the guest network properly isolated?"
**Tool**: Various VLAN/firewall checks
**Expected**: Isolation confirmation

### 85. Security Compliance
**Q**: "Do all APs have minimum security settings?"
**Tool**: SSID security checks
**Expected**: Encryption standards

## 🔄 Automation & Integration

### 86. Webhook Configuration
**Q**: "What webhooks are configured for alerts?"
**Tool**: `get_organization_webhooks`
**Expected**: Webhook URLs

### 87. API Integration Health
**Q**: "Are all API integrations working?"
**Tool**: `get_organization_api_requests`
**Expected**: No repeated failures

### 88. Scheduled Tasks
**Q**: "What automated tasks run overnight?"
**Tool**: API request patterns
**Expected**: Scheduled API calls

### 89. Bulk Operations
**Q**: "Can we update all switch ports in VLAN 20?"
**Tool**: Bulk update capabilities
**Expected**: Mass update success

### 90. Template Application
**Q**: "Can we apply the standard config to new devices?"
**Tool**: Template operations
**Expected**: Config applied

## 📊 Reporting & Analytics

### 91. Executive Summary
**Q**: "What's the network health score?"
**Tool**: Multiple analytics combined
**Expected**: Overall health metrics

### 92. Capacity Planning
**Q**: "When will we run out of switch ports?"
**Tool**: Port utilization trends
**Expected**: Growth projections

### 93. License Forecast
**Q**: "How many licenses will we need next year?"
**Tool**: License usage trends
**Expected**: Projected needs

### 94. Cost Analysis
**Q**: "What's our bandwidth cost per location?"
**Tool**: Usage analytics
**Expected**: Usage by site

### 95. SLA Compliance
**Q**: "Are we meeting uptime SLAs?"
**Tool**: Uptime monitoring
**Expected**: Availability percentage

## 🚀 Advanced Diagnostics

### 96. Trace Route
**Q**: "What path does traffic take to reach 8.8.8.8?"
**Tool**: Live tools diagnostics
**Expected**: Hop-by-hop path

### 97. DNS Resolution
**Q**: "Can all sites resolve internal DNS?"
**Tool**: Ping tests to DNS names
**Expected**: Successful resolution

### 98. DHCP Monitoring
**Q**: "Is DHCP working on all VLANs?"
**Tool**: Client connection checks
**Expected**: IP assignment success

### 99. Spanning Tree
**Q**: "Are there any spanning tree issues?"
**Tool**: Switch port status
**Expected**: No blocked ports

### 100. Quality of Service
**Q**: "Is QoS properly prioritizing voice traffic?"
**Tool**: Traffic analytics
**Expected**: Voice traffic prioritized

## Test Execution Summary

Each question tests specific functionality:
- **Questions 1-6**: Core monitoring features
- **Questions 7-15**: Live diagnostic tools
- **Questions 16-21**: Security policy management
- **Questions 22-29**: Mobile device management
- **Questions 30-35**: License operations
- **Questions 36-40**: Beta feature control
- **Questions 41-100**: Comprehensive network management

Use these questions to verify all features are working correctly!