# 📅 Daily Operations Guide - Cisco Meraki MCP Server

## 🌅 Morning Health Check Questions (Start of Day)

### 1. Network Status Overview
```
Q: "Are all critical devices online across the organization?"
Tool: get_organization_devices (check status)
Alert: Any device showing offline
```

### 2. Overnight Issues
```
Q: "Were there any critical alerts overnight?"
Tool: get_organization_api_analytics (timespan: 28800 - last 8 hours)
Check: 4xx/5xx errors, rate limiting
```

### 3. WAN Health
```
Q: "Is there packet loss on any WAN links?"
Tool: get_organization_devices_uplinks_loss_and_latency
Alert: Loss > 1% or latency > 100ms
```

### 4. Wireless Performance
```
Q: "What's the wireless connection success rate this morning?"
Tool: get_network_connection_stats (timespan: 3600)
Alert: Success rate < 95%
```

## 🏢 Business Hours Monitoring (Every 2-4 hours)

### 5. Client Connectivity
```
Q: "How many clients are connected and is it normal for this time?"
Tool: get_network_clients
Compare: Historical averages for same time/day
```

### 6. Switch Port Utilization
```
Q: "Are we running out of switch ports anywhere?"
Tool: get_organization_switch_ports_history
Alert: > 85% utilization at any location
```

### 7. API Usage Health
```
Q: "Are we approaching API rate limits?"
Tool: get_organization_api_analytics
Alert: > 8 calls/second sustained or 429 errors
```

### 8. Live Connectivity Test
```
Q: "Can all sites reach critical services (DNS, cloud apps)?"
Tool: create_device_ping_test (test from each site MX)
Targets: 8.8.8.8, Office365, critical apps
```

## 🔒 Security Checks (2x Daily)

### 9. Rogue Access Points
```
Q: "Are there any new rogue APs detected?"
Tool: get_network_wireless_air_marshal
Action: Investigate any new/unknown APs
```

### 10. Security Events
```
Q: "Were any malware or intrusion attempts blocked?"
Tools: 
- get_network_appliance_security_malware
- get_network_appliance_security_intrusion
Follow-up: Check source IPs, affected clients
```

### 11. VPN Status
```
Q: "Are all site-to-site VPN tunnels up?"
Tool: get_network_appliance_vpn_site_to_site
Alert: Any tunnel down > 5 minutes
```

## 🔧 Proactive Maintenance (Daily)

### 12. Firmware Updates
```
Q: "Which devices need firmware updates?"
Tool: get_organization_firmware_upgrades
Plan: Schedule updates for maintenance window
```

### 13. Cable Health Check
```
Q: "Are there any degraded network cables?"
Tool: create_switch_cable_test (test suspicious ports)
Action: Schedule cable replacement for bad pairs
```

### 14. License Expiration
```
Q: "Are any licenses expiring in the next 30 days?"
Tool: get_organization_licensing_coterm
Action: Plan renewal before expiration
```

## 📊 Performance Optimization (Weekly)

### 15. Bandwidth Analysis
```
Q: "Which applications are consuming the most bandwidth?"
Tool: get_network_traffic_analysis
Optimize: QoS rules, bandwidth allocation
```

### 16. Wireless Channel Optimization
```
Q: "Which wireless channels are most congested?"
Tool: get_network_wireless_channel_utilization
Action: Adjust RF profiles to avoid interference
```

### 17. Port Error Detection
```
Q: "Which switch ports are showing errors?"
Tool: get_device_switch_port_statuses
Investigate: CRC errors, collisions, duplex mismatches
```

## 🚨 Incident Response Questions

### 18. User Can't Connect
```
Q: "Why can't user X connect to WiFi?"
Tools in order:
1. get_network_wireless_clients (check if seen)
2. get_network_connection_stats (check failures)
3. create_device_ping_test (from AP to services)
```

### 19. Slow Network Complaint
```
Q: "Why is the network slow at location Y?"
Tools:
1. get_device_switch_port_statuses (check utilization)
2. create_device_throughput_test (measure actual speed)
3. get_network_latency_stats (check wireless latency)
4. get_organization_devices_uplinks_loss_and_latency (WAN issues)
```

### 20. Device Not Responding
```
Q: "Where is device with IP 192.168.1.50?"
Tools:
1. create_switch_mac_table (find MAC location)
2. get_device_switch_port_statuses (check port status)
3. create_switch_cable_test (test physical connection)
4. blink_device_leds (physically locate if needed)
```

## 💡 Helpful Daily Workflows

### Morning Routine (15 minutes)
```bash
1. Check device status: get_organization_devices
2. Review overnight alerts: get_organization_api_analytics
3. Verify WAN health: get_organization_devices_uplinks_loss_and_latency
4. Check wireless performance: get_network_connection_stats
5. Quick ping test to internet: create_device_ping_test target: "8.8.8.8"
```

### Midday Check (10 minutes)
```bash
1. Client count check: get_network_clients
2. API usage review: get_organization_api_analytics
3. Security scan: get_network_wireless_air_marshal
4. VPN status: get_network_appliance_vpn_site_to_site
```

### End of Day (20 minutes)
```bash
1. Full device inventory: get_organization_devices
2. Review day's alerts: get_network_alerts_settings
3. Check firmware updates: get_organization_firmware_upgrades
4. Plan tomorrow's maintenance: Review any issues found
```

## 🎯 Quick Troubleshooting Guides

### "Internet is Down"
```bash
1. create_device_ping_test serial: "MX_SERIAL" target: "8.8.8.8"
2. get_organization_devices_uplinks_loss_and_latency
3. get_organization_appliance_uplink_statuses
4. Check ISP status externally
```

### "WiFi Not Working"
```bash
1. get_network_wireless_ssids (verify enabled)
2. get_network_wireless_clients (check associations)
3. get_network_connection_stats (check auth failures)
4. get_network_wireless_rf_profiles (check power levels)
```

### "Can't Find a Device"
```bash
1. create_switch_mac_table serial: "SWITCH_SERIAL"
2. get_network_clients (search by MAC/IP)
3. blink_device_leds (physical identification)
```

## 📈 KPI Monitoring Questions

### Daily KPIs
- **Uptime**: "What's our network availability percentage?"
- **Client Count**: "How many unique clients today vs average?"
- **Bandwidth**: "What's our peak bandwidth utilization?"
- **Incidents**: "How many support tickets were network-related?"

### Weekly KPIs
- **Firmware Compliance**: "What % of devices are on latest firmware?"
- **Security Events**: "How many security events were blocked?"
- **Performance**: "What's our average wireless client latency?"
- **Growth**: "How many new devices/clients this week?"

## 🔮 Predictive Questions

### Capacity Planning
```
Q: "When will we run out of switch ports at current growth?"
Track: Port utilization trend over time
Tool: get_organization_switch_ports_history
```

### License Planning
```
Q: "When do our licenses expire and how many do we need?"
Tool: get_organization_licensing_coterm
Plan: Budget for renewals
```

### Bandwidth Forecasting
```
Q: "Will our WAN links handle holiday traffic?"
Analyze: Historical patterns, growth trends
Tools: get_organization_devices_uplinks_loss_and_latency
```

## 🛡️ Beta Features to Try

### Enhanced Diagnostics
```
Q: "Can we diagnose that intermittent issue?"
New Tools:
- Live ping FROM devices (not just TO them)
- Cable quality testing
- Real-time MAC table queries
- LED blinking for physical ID
```

### API Analytics
```
Q: "Who's making the most API calls?"
Tool: get_organization_api_analytics
Insight: Optimize integrations, reduce unnecessary calls
```

## 📋 Daily Checklist

### ✅ Must Do Daily:
- [ ] Check all devices online
- [ ] Review overnight alerts
- [ ] Verify WAN health
- [ ] Check wireless performance
- [ ] Review security events
- [ ] Monitor client counts

### ✅ Should Do Daily:
- [ ] Check firmware updates
- [ ] Review API usage
- [ ] Test critical connectivity
- [ ] Check switch port capacity
- [ ] Scan for rogue APs

### ✅ Weekly Tasks:
- [ ] Full cable health audit
- [ ] License expiration review
- [ ] Bandwidth analysis
- [ ] RF optimization check
- [ ] Performance trending

## 💡 Pro Tips

1. **Automate Morning Checks**: Script the morning routine
2. **Set Alerts**: Configure webhooks for critical events
3. **Track Trends**: Compare daily metrics to baseline
4. **Document Issues**: Keep notes on recurring problems
5. **Test Proactively**: Use live tools before users complain

## 🚀 Advanced Daily Questions

### Performance Optimization
```
Q: "Which clients are consuming excessive bandwidth?"
Combine: get_network_clients + traffic analysis
Action: Apply client policies if needed
```

### Security Posture
```
Q: "Are all security features properly configured?"
Audit: Firewall rules, content filtering, IDS/IPS
Tools: All security get_ tools
```

### Change Management
```
Q: "What configuration changes were made today?"
Tool: get_organization_api_analytics (filter PUT/POST)
Verify: All changes were authorized
```

Remember: The best network is one where users don't notice it's there! Use these daily questions to stay ahead of issues.