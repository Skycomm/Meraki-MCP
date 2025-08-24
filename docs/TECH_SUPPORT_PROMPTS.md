# 🔧 Tech Support Prompts & Troubleshooting Guide

## 🚨 Common Support Scenarios & Resolution Prompts

### 1. 🔴 "The Internet is Down!"

#### Initial Assessment
```
Prompt: "Check if the internet is down for the entire site or specific users"

Step 1: Test WAN connectivity from the MX
create_device_ping_test serial: "[MX_SERIAL]" target: "8.8.8.8" count: 10

Step 2: Check uplink status
get_organization_appliance_uplink_statuses org_id: "[ORG_ID]"

Step 3: Check for packet loss
get_organization_devices_uplinks_loss_and_latency org_id: "[ORG_ID]" timespan: 300

Step 4: Verify DNS resolution
create_device_ping_test serial: "[MX_SERIAL]" target: "google.com"
```

#### Resolution Paths
- **If WAN1 down**: Check if WAN2 is active (failover working?)
- **If high packet loss**: Contact ISP with specific metrics
- **If DNS failing**: Check content filtering isn't blocking

### 2. 📶 "WiFi is Not Working!"

#### Diagnosis Workflow
```
Prompt: "Diagnose WiFi connectivity issues systematically"

Step 1: Check if SSID is broadcasting
get_network_wireless_ssids network_id: "[NETWORK_ID]"
Look for: enabled = true

Step 2: Check authentication failures
get_network_connection_stats network_id: "[NETWORK_ID]" timespan: 300
Alert if: Auth failures > 10%

Step 3: Check specific client attempts
get_network_wireless_clients network_id: "[NETWORK_ID]" timespan: 300
Search for: User's MAC address

Step 4: Test from AP perspective
create_device_ping_test serial: "[AP_SERIAL]" target: "192.168.1.1"
```

#### Common Fixes
- **Wrong password**: Use `get_network_wireless_passwords` to verify
- **Client isolated**: Check client isolation settings
- **Capacity issue**: Check client count per AP

### 3. 🐌 "The Network is Slow!"

#### Performance Analysis
```
Prompt: "Identify the source of network slowness"

Step 1: Test actual throughput
create_device_throughput_test serial: "[DEVICE1]" target_serial: "[DEVICE2]"

Step 2: Check switch port utilization
get_device_switch_port_statuses serial: "[SWITCH_SERIAL]"
Alert if: Any port > 80% utilization

Step 3: Check wireless latency
get_network_latency_stats network_id: "[NETWORK_ID]" timespan: 3600

Step 4: Identify bandwidth hogs
get_network_clients network_id: "[NETWORK_ID]" timespan: 300
Sort by: usage_sent + usage_recv
```

#### Escalation Triggers
- Throughput < 50% of expected
- Latency > 100ms on LAN
- Packet loss > 1%

### 4. 🔍 "I Can't Find My Device!"

#### Device Location Workflow
```
Prompt: "Locate a missing network device"

Step 1: Search by MAC across all switches
create_switch_mac_table serial: "[SWITCH1_SERIAL]"
get_switch_mac_table serial: "[SWITCH1_SERIAL]" request_id: "[ID]"

Step 2: Check client list
get_network_clients network_id: "[NETWORK_ID]" timespan: 86400
Search for: MAC, IP, or hostname

Step 3: Physical identification
blink_device_leds serial: "[DEVICE_SERIAL]" duration: 60

Step 4: Check which port it's on
Look in MAC table results for port number
```

### 5. 🚫 "Website/Application Blocked!"

#### Access Control Diagnosis
```
Prompt: "Determine why user can't access specific resources"

Step 1: Check content filtering
get_network_appliance_content_filtering network_id: "[NETWORK_ID]"
Look for: Blocked categories

Step 2: Check firewall rules
get_network_appliance_firewall_l3_rules network_id: "[NETWORK_ID]"
Look for: Deny rules matching destination

Step 3: Check group policies
Review if client has restricted policy

Step 4: Test connectivity from MX
create_device_ping_test serial: "[MX_SERIAL]" target: "[BLOCKED_SITE]"
```

### 6. 🔌 "My Device Won't Connect!"

#### Physical Layer Troubleshooting
```
Prompt: "Diagnose physical connectivity issues"

Step 1: Test cable quality
create_switch_cable_test serial: "[SWITCH_SERIAL]" port: "[PORT_NUMBER]"
wait 10 seconds
get_switch_cable_test serial: "[SWITCH_SERIAL]" test_id: "[TEST_ID]"

Step 2: Check port configuration
get_device_switch_ports serial: "[SWITCH_SERIAL]"
Verify: Port enabled, correct VLAN

Step 3: Check PoE if applicable
get_device_switch_port_statuses serial: "[SWITCH_SERIAL]"
Look for: Power draw on port

Step 4: Try different port
update_device_switch_port serial: "[SWITCH_SERIAL]" port_id: "[PORT]" enabled: true
```

### 7. 📱 "Mobile Device Issues" (MDM)

#### MDM Troubleshooting
```
Prompt: "Diagnose Systems Manager device issues"

Step 1: Check device enrollment
get_network_sm_devices network_id: "[NETWORK_ID]"
Look for: Device in list

Step 2: Check device details
get_network_sm_device_detail network_id: "[NETWORK_ID]" device_id: "[DEVICE_ID]"
Check: Last seen, battery, network status

Step 3: Check installed profiles
get_network_sm_profiles network_id: "[NETWORK_ID]"
Verify: Required profiles deployed

Step 4: Remote action if needed
reboot_network_sm_devices network_id: "[NETWORK_ID]" device_ids: "[DEVICE_ID]"
```

### 8. 🎥 "Camera Not Working!"

#### Camera Diagnostics
```
Prompt: "Troubleshoot Meraki camera issues"

Step 1: Check camera status
get_device serial: "[CAMERA_SERIAL]"
Verify: Online status

Step 2: Test snapshot
get_device_camera_snapshot serial: "[CAMERA_SERIAL]"
Check: Returns valid image

Step 3: Check video settings
get_device_camera_video_settings serial: "[CAMERA_SERIAL]"
Verify: Quality settings appropriate

Step 4: Check network connectivity
create_device_ping_test serial: "[CAMERA_SERIAL]" target: "[DASHBOARD_IP]"
```

## 💬 Customer Communication Templates

### Initial Response
```
"I understand you're experiencing [ISSUE]. Let me run some diagnostics to identify the root cause."

Actions:
1. Run relevant diagnostic commands
2. Document findings
3. Provide timeline for resolution
```

### Status Update
```
"I've identified that [FINDING]. This is causing [IMPACT]. I'm now going to [ACTION]."

Example:
"I've identified 15% packet loss on your primary WAN link. This is causing slow internet speeds. I'm now going to test the backup link and contact your ISP."
```

### Resolution Confirmation
```
"I've resolved the issue by [ACTION]. The [METRIC] is now showing [GOOD_VALUE]. Can you please test and confirm it's working?"

Example:
"I've resolved the issue by adjusting the wireless channel to avoid interference. The connection success rate is now showing 99%. Can you please test and confirm WiFi is working properly?"
```

## 🎯 Quick Resolution Flowcharts

### WiFi Authentication Failures
```
High auth failures?
├─> Yes: Check RADIUS server
│   ├─> Server down: Check server connectivity
│   └─> Server up: Check credentials/certificates
└─> No: Check individual client
    ├─> Wrong password: Reset/provide password
    └─> Device issue: Update device drivers
```

### Slow Network Performance
```
Where is slowness?
├─> WAN: Check ISP links
│   ├─> High latency: ISP issue
│   └─> Packet loss: Cable/equipment issue
├─> LAN: Check switches
│   ├─> High utilization: Find bandwidth hog
│   └─> Errors on ports: Cable/duplex issue
└─> Wireless: Check RF environment
    ├─> Interference: Change channels
    └─> Coverage: Add APs/adjust power
```

## 🛠️ Advanced Troubleshooting Prompts

### Intermittent Issues
```
Prompt: "Diagnose intermittent connectivity problems"

1. Enable continuous monitoring:
   - Run ping test every 5 minutes
   - Log results with timestamps
   - Look for patterns (time of day, specific events)

2. Check for correlations:
   - High CPU/memory on devices
   - Backup jobs running
   - Peak usage times

3. Use historical data:
   get_organization_devices_uplinks_loss_and_latency timespan: 86400
   Look for: Patterns in packet loss
```

### Performance Degradation
```
Prompt: "Track down gradual performance degradation"

1. Baseline comparison:
   - Current throughput vs last month
   - Current latency vs baseline
   - Error rates over time

2. Growth analysis:
   - New devices added
   - Increased client count
   - New applications deployed

3. Capacity check:
   - Port utilization trends
   - License usage
   - Bandwidth consumption
```

## 📞 Escalation Guidelines

### When to Escalate to Senior Tech
- Multiple sites affected
- Hardware failure suspected
- ISP coordination needed
- Security breach indicators

### When to Engage Vendor Support
- Firmware bugs suspected
- API errors/inconsistencies
- Hardware RMA needed
- Feature not working as documented

### Information to Gather Before Escalation
```
1. Organization ID and affected network IDs
2. Device serials involved
3. Timestamps of issue occurrence
4. Diagnostic test results
5. Error messages (exact text)
6. Steps already tried
7. Business impact assessment
```

## 🔍 Proactive Support Prompts

### Daily Health Check
```
Prompt: "Perform proactive health check to prevent issues"

Run every morning:
1. Device status check - Any offline?
2. WAN health - Any packet loss?
3. Wireless performance - Success rate > 95%?
4. Security events - Any threats blocked?
5. Firmware updates - Any critical updates?
```

### Weekly Deep Dive
```
Prompt: "Weekly infrastructure analysis"

1. Cable health audit - Test all critical links
2. Capacity review - Ports/licenses/bandwidth
3. Security audit - Rules, policies, threats
4. Performance baseline - Document normal metrics
```

## 💡 Tech Support Best Practices

### Document Everything
```
For each ticket:
1. Initial symptoms reported
2. Diagnostic commands run
3. Results/findings
4. Actions taken
5. Resolution confirmed
6. Follow-up needed
```

### Set Expectations
```
"Based on the diagnostic results, this appears to be [ISSUE TYPE]. 
Resolution typically takes [TIMEFRAME]. 
I'll update you every [INTERVAL] until resolved."
```

### Verify Resolution
```
Never close ticket until:
1. Issue confirmed resolved
2. User has tested
3. Monitoring shows normal
4. Root cause documented
5. Prevention steps identified
```

## 🚀 Power User Prompts

### Bulk Diagnostics
```
Prompt: "Run diagnostics across multiple devices simultaneously"

Example: Test all switches in a network
for switch in [SWITCH_LIST]:
    create_switch_cable_test serial: switch port: "1"
    create_device_ping_test serial: switch target: "8.8.8.8"
```

### Automated Remediation
```
Prompt: "Automatically fix common issues"

If high WiFi auth failures:
1. Check RADIUS connectivity
2. Restart RADIUS if needed
3. Clear client deauth
4. Monitor for improvement
```

### Custom Alerts
```
Prompt: "Set up proactive alerting"

Monitor for:
- WAN packet loss > 1%
- WiFi success rate < 95%
- Switch port errors increasing
- API rate limit approaching
```

Remember: Great tech support is about being systematic, documenting everything, and communicating clearly with customers!