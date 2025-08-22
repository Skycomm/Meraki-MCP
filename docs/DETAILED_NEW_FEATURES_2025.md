# 🔍 Detailed Guide to New 2025 Cisco Meraki Features

## 📊 API Analytics & Monitoring (New 2025)

### 1. **API Usage Analytics Dashboard**
The new API analytics feature provides comprehensive insights into your API usage patterns.

#### What it shows:
- **Request Volume**: Total API calls made over time
- **Response Code Distribution**: Success rates, errors, rate limiting
- **Top Endpoints**: Most frequently accessed API endpoints
- **Admin Activity**: Which admins are making API calls
- **Rate Limit Analysis**: When you're hitting API limits

#### Example Output:
```
📊 API Analytics - Organization 686470

Time Period: Last 24 hours
Total API Calls: 1,247

## Response Code Distribution
- 200 Success: ✅ 1,180 calls (94.6%)
- 429 Rate Limited: ⚠️ 45 calls (3.6%)
- 404 Not Found: ❌ 22 calls (1.8%)

## Top API Endpoints
- /organizations/686470/networks: 342 calls
- /devices/{serial}/clients: 198 calls
- /networks/{id}/wireless/ssids: 156 calls

## Rate Limiting
- Rate Limited Calls: 45
- Percentage: 3.6%
- Recommendation: Consider implementing request throttling
```

#### Use Cases:
- **Optimize API Usage**: Identify inefficient API patterns
- **Monitor Rate Limits**: Prevent hitting 429 errors
- **Audit API Access**: Track who's using APIs
- **Troubleshoot Issues**: Find failing API calls
- **Capacity Planning**: Understand API load

### 2. **Organization-Wide Switch Port Monitoring**
New aggregated view of all switch ports across your entire organization.

#### Features:
- **Total Port Count**: All ports across all switches
- **Active Port Tracking**: Real-time active port count
- **Power Usage**: Total PoE consumption
- **Error Detection**: Ports with errors/issues
- **Historical Trends**: Port usage over time

#### Example Output:
```
🔌 Organization Switch Ports History

Time Period: Last 1 hour

## Summary
- Total Ports: 2,456
- Active Ports: 1,823 (74.2%)
- Error Ports: 12
- Total Power: 3,245W

## Recent Activity
### 2025-08-17 20:15:00
- Active: 1,823/2,456
- Errors: 12
- Power Usage: 3,245W
```

### 3. **Device Migration Tracking**
Monitor devices being moved between networks in real-time.

#### What it tracks:
- **Migration Status**: In progress, completed, failed
- **Source/Destination**: Where devices are moving from/to
- **Progress Percentage**: Real-time migration progress
- **Timing**: When migrations started/completed

#### Example:
```
🔄 Device Migration Status

Total Migrations: 3

## 🔄 In Progress (2 devices)
### Switch-Office-01 (Q2HP-ZK5N-XG8L)
- From: Old Office Network
- To: New Office Network
- Progress: [████████░░] 80%
- Started: 2025-08-17 19:45:00

## ✅ Completed (1 device)
### AP-Lobby-01 (Q2PD-7QTD-SZG2)
- Migrated successfully
- Duration: 12 minutes
```

## 🔧 Live Tools (Beta/Early Access)

### 1. **Ping Test from Devices**
Run ping tests FROM your Meraki devices to any destination.

#### Capabilities:
- **Source**: Any Meraki device (MX, MS, MR)
- **Target**: IP address or hostname
- **Customizable**: Packet count, size
- **Results**: Latency, packet loss, jitter

#### Example Usage:
```bash
# Start ping test
create_device_ping_test serial: "Q2PD-7QTD-SZG2" target: "google.com" count: 10

# Returns Job ID: ping_12345

# Check results
get_device_ping_test serial: "Q2PD-7QTD-SZG2" ping_id: "ping_12345"

# Results:
🏓 Ping Test Results
- Sent: 10 packets
- Received: 10 packets
- Loss: 0%
- Latency: Min: 12ms, Avg: 15ms, Max: 18ms
```

### 2. **Throughput Testing**
Measure actual bandwidth between Meraki devices.

#### Features:
- **Device-to-Device**: Test between any two Meraki devices
- **Bidirectional**: Tests both upload and download
- **Real Performance**: Actual throughput, not theoretical

#### Example:
```bash
create_device_throughput_test serial: "SW1" target_serial: "SW2"

# Results:
🚀 Throughput Test Results
- Download: 945 Mbps
- Upload: 932 Mbps
```

### 3. **Cable Diagnostics**
Test physical cable quality on switch ports.

#### What it detects:
- **Cable Length**: Measured in meters
- **Cable Quality**: OK, marginal, or failed
- **Pair Status**: Individual wire pair testing
- **Link Speed**: Negotiated speed

#### Example:
```bash
create_switch_cable_test serial: "Q2HP-ZK5N-XG8L" port: "5"

# Results:
🔌 Cable Test Results - Port 5
- Status: Connected
- Speed: 1000 Mbps
- Cable Pairs:
  - Pair 1: ✅ OK (23m)
  - Pair 2: ✅ OK (23m)
  - Pair 3: ✅ OK (23m)
  - Pair 4: ✅ OK (23m)
```

### 4. **MAC Address Table Query**
Real-time MAC address table from switches.

#### Information Provided:
- **MAC Addresses**: All learned MACs
- **Port Mapping**: Which port each MAC is on
- **VLAN Assignment**: VLAN for each MAC
- **Dynamic Updates**: Real-time changes

#### Example:
```bash
create_switch_mac_table serial: "Q2HP-ZK5N-XG8L"

# Results:
📋 MAC Address Table
Total Entries: 156

## VLAN 10 (45 entries)
- 00:1a:2b:3c:4d:5e → Port 12
- 00:1a:2b:3c:4d:5f → Port 13
- aa:bb:cc:dd:ee:ff → Port 24

## VLAN 20 (38 entries)
- 11:22:33:44:55:66 → Port 1
- 77:88:99:aa:bb:cc → Port 2
```

### 5. **LED Blinking**
Physically identify devices by blinking their LEDs.

#### Use Cases:
- **Device Location**: Find specific device in rack
- **Installation**: Verify correct device during setup
- **Troubleshooting**: Identify device for hands-on work

#### Example:
```bash
blink_device_leds serial: "Q2HP-ZK5N-XG8L" duration: 60

# Device LEDs will blink for 60 seconds
💡 LED Blink Started
Device: Q2HP-ZK5N-XG8L
Duration: 60 seconds
✨ Device LEDs are now blinking!
```

### 6. **Wake-on-LAN**
Wake up sleeping devices remotely.

#### Requirements:
- **Target Device**: Must support WoL
- **MAC Address**: Target device MAC
- **Same VLAN**: Device must be on specified VLAN

#### Example:
```bash
create_device_wake_on_lan serial: "Q2HP-ZK5N-XG8L" vlan_id: 10 mac_address: "aa:bb:cc:dd:ee:ff"

⏰ Wake-on-LAN Sent
Magic packet sent to wake the device.
```

## 🛡️ Policy Objects (Advanced Security)

### What are Policy Objects?
Policy Objects are reusable definitions for network security rules.

### Types of Policy Objects:

#### 1. **IP/CIDR Objects**
Define IP addresses or ranges for security rules.
```bash
# Single IP
create_organization_policy_object 
  name: "Server-01" 
  type: "ipv4" 
  cidr: "192.168.1.100/32"

# Subnet
create_organization_policy_object 
  name: "Guest-Network" 
  type: "ipv4" 
  cidr: "192.168.50.0/24"
```

#### 2. **FQDN Objects**
Define domain names for security policies.
```bash
create_organization_policy_object 
  name: "Blocked-Sites" 
  type: "fqdn" 
  fqdn: "malicious-site.com"
```

#### 3. **Policy Groups**
Combine multiple objects into groups.
```bash
create_organization_policy_objects_group 
  name: "All-Servers" 
  object_ids: "obj_123,obj_124,obj_125"
```

### Use Cases:
- **Firewall Rules**: Apply consistent security across networks
- **Content Filtering**: Block/allow specific sites
- **Access Control**: Define who can access what
- **Compliance**: Maintain security standards

## 📱 Systems Manager (MDM)

### Device Management Features:

#### 1. **Device Inventory**
```
📱 Systems Manager Devices
Total Devices: 127

## iOS (89 devices)
- iPhones: 67
- iPads: 22
- Battery Status: 12 devices < 20%

## Android (38 devices)
- Phones: 30
- Tablets: 8
```

#### 2. **App Management**
- View installed apps
- Deploy enterprise apps
- Remove unauthorized apps
- Track app versions

#### 3. **Performance Monitoring**
```
📊 Performance History - Device iPhone-001
CPU Usage: 🟢 45%
Memory: 🟡 78% used
  - Free: 512MB
  - Active: 3.2GB
Disk: 🟢 65% used
Network: ↑125KB ↓890KB
```

#### 4. **Remote Actions**
- Reboot devices
- Lock/unlock screens
- Wipe devices
- Push configurations

## 📄 Licensing Management

### Features:

#### 1. **License Overview**
```
📄 Organization Licenses
Total Licenses: 245

## Access Point Licenses (120)
- Active: 115
- Expired: 3
- Unused: 2

## Switch Licenses (85)
- Active: 82
- Expired: 0
- Unused: 3
```

#### 2. **Co-termination Management**
- Single expiration date
- License count by model
- Renewal reminders
- Usage tracking

#### 3. **License Operations**
- Claim new licenses
- Transfer between orgs
- Assign to devices
- Renew expiring licenses

## 🧪 Beta/Early Access Management

### Available Beta Features:
1. **API Early Access** - Access to latest APIs
2. **SmartPorts** - Dynamic port profiles
3. **Client360** - Enhanced client insights
4. **VLAN Database** - Centralized VLAN management
5. **Cloud CLI** - Command-line for cloud devices

### How to Enable:
```bash
# List available features
get_organization_early_access_features org_id: "686470"

# Enable a feature
enable_organization_early_access_feature 
  org_id: "686470" 
  feature_id: "has_vlan_db"
```

## 💡 Best Practices

### 1. **API Analytics**
- Check weekly for usage patterns
- Monitor for 429 rate limits
- Identify inefficient API calls

### 2. **Live Tools**
- Use ping before throughput tests
- Schedule cable tests during maintenance
- Document MAC table baselines

### 3. **Policy Objects**
- Create reusable objects
- Use descriptive names
- Group related objects

### 4. **Beta Features**
- Test in lab first
- Monitor for breaking changes
- Provide feedback to Meraki

## 🚀 Quick Start Commands

```bash
# Check API usage
get_organization_api_analytics org_id: "686470" timespan: 86400

# Test network connectivity
create_device_ping_test serial: "Q2PD-7QTD-SZG2" target: "8.8.8.8"

# Find a device physically
blink_device_leds serial: "Q2HP-ZK5N-XG8L"

# Check cable quality
create_switch_cable_test serial: "Q2HP-ZK5N-XG8L" port: "1"

# View all licenses
get_organization_licenses org_id: "686470"

# Enable beta feature
enable_organization_early_access_feature org_id: "686470" feature_id: "has_client360"
```