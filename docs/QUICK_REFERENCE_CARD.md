# 🎯 Cisco Meraki MCP Server - Quick Reference Card

## 🚀 Most Used Commands

### Network Status (Top 5)
```bash
# 1. Check all devices status
get_organization_devices org_id: "686470"

# 2. View connected clients  
get_network_clients network_id: "L_669347494617953785"

# 3. Check WAN health
get_organization_devices_uplinks_loss_and_latency org_id: "686470"

# 4. Test connectivity FROM device
create_device_ping_test serial: "Q2PD-7QTD-SZG2" target: "8.8.8.8"

# 5. Get WiFi password
get_network_wireless_passwords network_id: "L_669347494617953785"
```

### Troubleshooting (Top 5)
```bash
# 1. Find device on network
create_switch_mac_table serial: "Q2HP-ZK5N-XG8L"

# 2. Test cable quality
create_switch_cable_test serial: "Q2HP-ZK5N-XG8L" port: "1"

# 3. Identify device physically
blink_device_leds serial: "Q2HP-ZK5N-XG8L" duration: 30

# 4. Check wireless issues
get_network_connection_stats network_id: "L_669347494617953785"

# 5. View firewall rules
get_network_appliance_firewall_l3_rules network_id: "L_669347494617953785"
```

## 📊 Daily Health Checks

### Morning (5 min)
```bash
get_organization_devices org_id: "686470"                    # All devices up?
get_organization_api_analytics org_id: "686470" timespan: 28800  # Overnight issues?
get_organization_devices_uplinks_loss_and_latency org_id: "686470"  # WAN health?
```

### Midday (3 min)
```bash
get_network_clients network_id: "L_669347494617953785"       # Client count normal?
get_network_wireless_air_marshal network_id: "L_669347494617953785"  # Rogue APs?
```

### End of Day (5 min)
```bash
get_organization_firmware_upgrades org_id: "686470"          # Updates needed?
get_organization_licensing_coterm org_id: "686470"           # Licenses OK?
```

## 🔧 Common Fixes

### "Internet Down"
```bash
1. create_device_ping_test serial: "[MX]" target: "8.8.8.8"
2. get_organization_appliance_uplink_statuses org_id: "[ORG]"
3. Check ISP status
```

### "WiFi Not Working"
```bash
1. get_network_wireless_ssids network_id: "[NET]"
2. get_network_connection_stats network_id: "[NET]"
3. get_network_wireless_passwords network_id: "[NET]"
```

### "Can't Find Device"
```bash
1. create_switch_mac_table serial: "[SWITCH]"
2. get_network_clients network_id: "[NET]" 
3. blink_device_leds serial: "[DEVICE]"
```

### "Network Slow"
```bash
1. create_device_throughput_test serial: "[DEV1]" target_serial: "[DEV2]"
2. get_device_switch_port_statuses serial: "[SWITCH]"
3. get_network_latency_stats network_id: "[NET]"
```

## 🆕 Beta Features (Live Tools)

### Revolutionary Diagnostics
```bash
# Ping FROM your devices (not TO them!)
create_device_ping_test serial: "Q2PD-7QTD-SZG2" target: "google.com"

# Test actual bandwidth between devices
create_device_throughput_test serial: "SW1" target_serial: "SW2"

# Real-time MAC table lookup
create_switch_mac_table serial: "Q2HP-ZK5N-XG8L"
get_switch_mac_table serial: "Q2HP-ZK5N-XG8L" request_id: "[ID]"

# Cable quality testing
create_switch_cable_test serial: "Q2HP-ZK5N-XG8L" port: "24"

# Wake sleeping computers
create_device_wake_on_lan serial: "SW1" vlan_id: 10 mac_address: "aa:bb:cc:dd:ee:ff"
```

## 📈 Performance Metrics

### What's Normal?
- **API Response**: < 1 second
- **Ping Latency**: < 50ms internet, < 5ms LAN
- **Packet Loss**: < 0.1%
- **WiFi Success**: > 95%
- **CPU Usage**: < 80%
- **Port Utilization**: < 70%

### Alert Thresholds
- 🔴 **Critical**: Packet loss > 5%, WiFi success < 90%
- 🟡 **Warning**: Packet loss > 1%, WiFi success < 95%
- 🟢 **Normal**: Packet loss < 0.1%, WiFi success > 98%

## 🔑 Key Parameters

### Organization & Network
```
Skycomm Org ID: 686470
Reserve St Network: L_669347494617953785
MX Serial: Q2PD-7QTD-SZG2
Switch Serial: Q2HP-ZK5N-XG8L
```

### Common Timespans
```
300 = 5 minutes
3600 = 1 hour
86400 = 24 hours
604800 = 7 days
```

## 💡 Pro Tips

### 1. Batch Operations
Run multiple tests at once:
```bash
create_device_ping_test serial: "MX1" target: "8.8.8.8"
create_device_ping_test serial: "MX2" target: "8.8.8.8"
create_device_ping_test serial: "MX3" target: "8.8.8.8"
```

### 2. Historical Analysis
Always check trends:
```bash
# Compare current to historical
get_organization_devices_uplinks_loss_and_latency org_id: "686470" timespan: 86400
```

### 3. Document Patterns
Track issues:
- Time of day
- Specific devices
- After changes
- During events

## 🚨 Emergency Contacts

### Internal Escalation
1. Check device status
2. Run basic diagnostics
3. Document findings
4. Escalate with data

### Vendor Support Prep
Gather before calling:
- Organization ID
- Network ID
- Device serials
- Error messages
- Test results

## 📱 Mobile-Friendly Commands

### Quick Status
```
# Everything OK?
get_organization_devices org_id: "686470"
```

### Quick Test
```
# Internet working?
create_device_ping_test serial: "Q2PD-7QTD-SZG2" target: "8.8.8.8"
```

### Quick Find
```
# Where's that device?
create_switch_mac_table serial: "Q2HP-ZK5N-XG8L"
```

## 🎯 Decision Tree

```
Network Issue?
├─> Affecting everyone?
│   ├─> Yes → Check WAN/MX
│   └─> No → Check specific device/user
├─> Wired or Wireless?
│   ├─> Wired → Cable test, port status
│   └─> Wireless → Connection stats, RF check
└─> When started?
    ├─> Just now → Check recent changes
    └─> Gradual → Check growth/capacity
```

## ⚡ Speed Commands

Copy-paste ready:

```bash
# Full health check (30 seconds)
get_organization_devices org_id: "686470"
get_organization_devices_uplinks_loss_and_latency org_id: "686470" timespan: 300
get_network_clients network_id: "L_669347494617953785" timespan: 300
get_network_connection_stats network_id: "L_669347494617953785" timespan: 3600

# Quick connectivity test (10 seconds)
create_device_ping_test serial: "Q2PD-7QTD-SZG2" target: "8.8.8.8" count: 5
create_device_ping_test serial: "Q2PD-7QTD-SZG2" target: "google.com" count: 5

# Find and fix (20 seconds)
create_switch_mac_table serial: "Q2HP-ZK5N-XG8L"
blink_device_leds serial: "Q2HP-ZK5N-XG8L" duration: 20
```

Remember: This card has the 20% of commands you'll use 80% of the time!