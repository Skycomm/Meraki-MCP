# 🌐 Multi-Organization Management Guide

## 🏢 Cross-Organization Monitoring Questions

### 1. Global Health Check
```
Q: "Are there any issues across ANY of my organizations?"

Step 1: Get all your organizations
get_organizations

Step 2: For each org, check device status
for org in organizations:
    get_organization_devices org_id: "[ORG_ID]"
    
Alert on: Any device offline, any device with warnings
```

### 2. Multi-Org WAN Health
```
Q: "Is there packet loss at any of my sites across all organizations?"

For each org:
get_organization_devices_uplinks_loss_and_latency org_id: "[ORG_ID]" timespan: 300

Consolidate results showing:
- Org Name | Site | WAN1 Loss | WAN2 Loss | Primary Latency
- Highlight any > 1% loss or > 100ms latency
```

### 3. Global License Status
```
Q: "Which organizations have licenses expiring soon?"

For each org:
get_organization_licensing_coterm org_id: "[ORG_ID]"

Summary table:
- Organization | Expiration Date | Days Remaining | Device Count
- Sort by: Days remaining (urgent first)
```

### 4. Firmware Compliance
```
Q: "Which devices across all my organizations need firmware updates?"

For each org:
get_organization_firmware_upgrades org_id: "[ORG_ID]"

Report showing:
- Total devices needing updates
- Critical updates vs. optional
- Group by model/version
```

### 5. Security Posture
```
Q: "Are there security threats detected in any organization?"

For each org and network:
- get_network_appliance_security_malware network_id: "[NET_ID]"
- get_network_appliance_security_intrusion network_id: "[NET_ID]"
- get_network_wireless_air_marshal network_id: "[NET_ID]"

Dashboard:
- Organization | Malware Blocked | IDS Alerts | Rogue APs
```

## 📊 Comparative Analytics

### 6. Performance Comparison
```
Q: "Which organization has the best/worst network performance?"

Metrics to compare:
- Average WAN latency
- Packet loss percentage  
- WiFi success rates
- Client satisfaction scores

For each org:
1. get_organization_devices_uplinks_loss_and_latency
2. get_network_connection_stats (for each network)
3. Calculate averages
```

### 7. Capacity Planning
```
Q: "Which organizations are running out of capacity?"

Check across all orgs:
- Switch port utilization
- License usage
- IP address usage
- Access point density

get_organization_switch_ports_history org_id: "[ORG_ID]"
```

### 8. Cost Analysis  
```
Q: "What's my total bandwidth usage across all organizations?"

For each org:
- Get device count
- Get client count
- Get bandwidth usage
- Calculate per-location costs

Useful for:
- ISP billing verification
- Budget planning
- Cost allocation
```

## 🚨 Multi-Org Incident Detection

### 9. Widespread Outages
```
Q: "Is this issue affecting multiple organizations?"

Quick check pattern:
1. Identify symptom (e.g., high latency)
2. Check same metric across all orgs
3. Look for patterns:
   - Same ISP?
   - Same geographic region?
   - Same time frame?
   - Same device model?
```

### 10. Configuration Drift
```
Q: "Are all my organizations configured consistently?"

Compare across orgs:
- Firewall rules
- Content filtering
- Wireless settings
- Alert configurations

Flag differences that might indicate:
- Missing security rules
- Inconsistent policies
- Forgotten changes
```

## 🔧 Bulk Operations

### 11. Mass Updates
```
Q: "How do I update settings across all organizations?"

Example: Update DNS across all orgs
For each org:
    For each network:
        Check current DNS
        Update if needed
        Verify change
```

### 12. Global Search
```
Q: "Where is device/client X across all my organizations?"

Search pattern:
For each org:
    get_organization_devices org_id: "[ORG_ID]"
    Search for: Serial, MAC, name
    
For each network:
    get_network_clients network_id: "[NET_ID]"
    Search for: MAC, IP, hostname
```

## 📈 Executive Dashboards

### 13. Weekly Executive Summary
```
Q: "What's the network health across all organizations this week?"

Key metrics:
- Total sites online: X/Y (percentage)
- Average uptime: 99.X%
- Security incidents blocked: X
- Licenses expiring within 30 days: X
- Devices needing updates: X
- Top issues by frequency
```

### 14. Growth Tracking
```
Q: "How is network usage growing across organizations?"

Track month-over-month:
- New devices added
- Client count growth
- Bandwidth increase
- New locations
```

## 🎯 Proactive Multi-Org Monitoring

### 15. Morning Global Check
```
Q: "Give me a 5-minute overview of all organizations"

Quick script:
1. List all orgs
2. For each: Count offline devices
3. For each: Check for critical alerts
4. For each: Verify WAN health
5. Generate summary report
```

### 16. Pattern Recognition
```
Q: "Are there any concerning patterns across organizations?"

Look for:
- Multiple sites with same issue
- Gradual degradation across orgs
- Time-based patterns
- Geography-based issues
```

## 💡 Multi-Org Best Practices

### Template Organizations
```
Q: "How do I maintain consistency across organizations?"

1. Create template org with standard:
   - Firewall rules
   - Wireless settings
   - Alert configurations
   
2. Compare others against template
3. Flag and fix deviations
```

### Automated Reporting
```
Q: "How do I automate multi-org reporting?"

Daily automated checks:
- Device status summary
- License expiration warnings
- Security incident summary
- Performance degradation alerts
```

## 🚀 Advanced Multi-Org Queries

### 17. Compliance Auditing
```
Q: "Are all organizations meeting compliance requirements?"

Check across all:
- Encryption standards
- Password policies
- Firewall rules
- Access controls
- Logging enabled
```

### 18. Vendor Management
```
Q: "Which ISPs are performing best/worst?"

Compare by ISP across orgs:
- Uptime percentages
- Average latency
- Packet loss rates
- Support ticket frequency
```

### 19. Site Comparisons
```
Q: "How does Site A compare to Site B across different orgs?"

Benchmark metrics:
- Devices per user
- Bandwidth per user
- WiFi clients per AP
- Support tickets per site
```

### 20. Disaster Recovery
```
Q: "If Org A fails, can Org B handle the load?"

Capacity checks:
- Available switch ports
- License headroom
- Bandwidth capacity
- VPN tunnel limits
```

## 📊 Sample Multi-Org Dashboard

```
═══════════════════════════════════════════════════════════
                 GLOBAL NETWORK STATUS
═══════════════════════════════════════════════════════════
Organization    | Devices | Status  | WAN Health | WiFi    
----------------|---------|---------|------------|--------
Skycomm         | 45/45   | ✅ 100% | ✅ 0.1%   | ✅ 98%
Lab Corp        | 23/25   | ⚠️  92% | ⚠️ 1.5%   | ✅ 96%
Branch Office   | 12/12   | ✅ 100% | ✅ 0.0%   | ✅ 99%
Remote Sites    | 89/92   | ⚠️  97% | 🔴 3.2%   | ⚠️ 94%

ALERTS: 
- Remote Sites: 3 devices offline
- Lab Corp: WAN2 packet loss detected
- 4 devices need firmware updates

UPCOMING:
- Skycomm licenses expire in 45 days
- Lab Corp: Scheduled maintenance Tuesday
═══════════════════════════════════════════════════════════
```

## 🔍 Quick Multi-Org Commands

### Everything at a Glance
```bash
# List all orgs
get_organizations

# Critical issues check (for each org)
get_organization_devices org_id: "[ORG]"  # Any offline?
get_organization_devices_uplinks_loss_and_latency org_id: "[ORG]"  # WAN issues?
get_organization_licensing_coterm org_id: "[ORG]"  # License warnings?
```

### Find Anything Anywhere
```bash
# Search across all orgs for device
For each org:
    get_organization_devices org_id: "[ORG]"
    grep -i "[SEARCH_TERM]"
```

### Global Health Score
```bash
# Calculate health percentage
For each org:
    total_devices = count(get_organization_devices)
    online_devices = count(status == "online")
    health_score = (online_devices / total_devices) * 100
```

## 📋 Multi-Org Checklist

### Daily Global Checks
- [ ] All critical devices online across all orgs
- [ ] No WAN packet loss > 1% anywhere
- [ ] No security alerts in any org
- [ ] WiFi success > 95% everywhere
- [ ] No licenses expiring < 30 days

### Weekly Global Review  
- [ ] Firmware compliance check
- [ ] Capacity planning review
- [ ] Security posture audit
- [ ] Performance benchmarking
- [ ] Cost analysis update

### Monthly Executive Report
- [ ] Uptime percentages by org
- [ ] Growth metrics
- [ ] Incident summary
- [ ] Budget vs. actual
- [ ] Recommendations

Remember: Managing multiple organizations is about finding patterns, maintaining consistency, and catching issues before they spread!