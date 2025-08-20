# Troubleshooting Dashboard Guide

Comprehensive network troubleshooting tools for diagnosing and resolving issues.

## Quick Start

**When something's wrong, start here:**
```
troubleshooting_help()
```

This shows which tool to use for your specific issue.

## Core Troubleshooting Tools

### 1. Connectivity Diagnosis
```python
# General connectivity check
diagnose_connectivity_issues(network_id)

# Specific client issues
diagnose_connectivity_issues(
    network_id, 
    client_mac="AA:BB:CC:DD:EE:FF",
    timespan=3600  # Last hour
)
```

**What it checks:**
- Device online/offline status
- Authentication success rates
- DHCP assignment failures
- DNS resolution issues
- Client-specific problems

**Use when:**
- Clients can't connect
- Frequent disconnections
- Authentication failures
- No IP assignment

### 2. Performance Analysis
```python
# Check for bottlenecks
analyze_performance_bottlenecks(network_id, timespan=3600)
```

**What it analyzes:**
- WAN bandwidth saturation
- Switch port utilization
- Wireless channel congestion
- Packet loss and latency
- Performance trends

**Use when:**
- Network feels slow
- Video calls dropping
- Large file transfers stall
- High latency complaints

### 3. Configuration Conflicts
```python
# Find misconfigurations
check_configuration_conflicts(network_id)
```

**What it validates:**
- VLAN subnet overlaps
- Firewall rule conflicts
- DHCP pool sizing
- Wireless security settings
- General best practices

**Use when:**
- After making changes
- Inherited network setup
- Periodic audit needed
- Things suddenly broke

### 4. Comprehensive Report
```python
# Full diagnostic report
generate_troubleshooting_report(
    network_id,
    include_connectivity=True,
    include_performance=True,
    include_configuration=True,
    client_mac="AA:BB:CC:DD:EE:FF"  # Optional
)
```

**Generates:**
- Complete network analysis
- All diagnostics combined
- Prioritized issues list
- Executive summary
- Support-ready documentation

### 5. Remediation Steps
```python
# Get fix instructions
suggest_remediation_steps(network_id, issue_type)

# Issue types:
# - "connectivity"
# - "performance" 
# - "dhcp"
# - "wireless"
# - "security"
```

**Provides:**
- Step-by-step fixes
- Dashboard navigation
- Best practices
- Escalation paths

## Common Troubleshooting Scenarios

### Scenario 1: "Users Can't Connect to WiFi"
```python
# 1. Check connectivity
diagnose_connectivity_issues(network_id)

# 2. If auth failures found
suggest_remediation_steps(network_id, "wireless")

# 3. Check specific client
diagnose_connectivity_issues(
    network_id,
    client_mac="AA:BB:CC:DD:EE:FF"
)
```

### Scenario 2: "Network is Slow"
```python
# 1. Analyze performance
analyze_performance_bottlenecks(network_id)

# 2. If bandwidth saturation
suggest_remediation_steps(network_id, "performance")

# 3. Generate report for management
generate_troubleshooting_report(network_id)
```

### Scenario 3: "DHCP Not Working"
```python
# 1. Check DHCP configuration
check_configuration_conflicts(network_id)

# 2. Diagnose connectivity
diagnose_connectivity_issues(network_id)

# 3. Get DHCP fix steps
suggest_remediation_steps(network_id, "dhcp")
```

### Scenario 4: "Everything Broke After Changes"
```python
# 1. Check all configurations
check_configuration_conflicts(network_id)

# 2. Full diagnostic
generate_troubleshooting_report(network_id)

# 3. Get rollback guidance
suggest_remediation_steps(network_id, "connectivity")
```

## Understanding the Output

### Connectivity Diagnosis Icons
- ✅ Component working normally
- ⚠️ Warning - potential issue
- ❌ Error - definite problem
- 📊 Statistics/metrics
- 💡 Recommendations

### Performance Metrics
- **Bandwidth**: Mbps utilization
- **Channel Util**: >70% = congested
- **Packet Loss**: >1% = problematic
- **Latency**: >100ms = high

### Common Issues Found

#### Authentication Failures
- Wrong password/PSK
- RADIUS server down
- Certificate expired
- Wrong VLAN assignment

#### DHCP Problems
- Pool exhausted
- Relay misconfigured
- VLAN mismatch
- Firewall blocking

#### Performance Issues
- WAN saturation
- Switch port bottleneck
- WiFi interference
- Packet loss

## Best Practices

### Regular Health Checks
```python
# Weekly performance check
analyze_performance_bottlenecks(network_id, timespan=604800)

# Monthly configuration audit
check_configuration_conflicts(network_id)

# Quarterly full report
generate_troubleshooting_report(network_id)
```

### Proactive Monitoring
1. Set up alerts for critical thresholds
2. Regular bandwidth trending
3. Client connection success tracking
4. Configuration change notifications

### Documentation
- Save troubleshooting reports
- Document all changes made
- Track recurring issues
- Build knowledge base

## Troubleshooting Workflow

```
1. Identify Symptoms
   ↓
2. Run Diagnostic Tool
   ↓
3. Analyze Results
   ↓
4. Get Remediation Steps
   ↓
5. Implement Fixes
   ↓
6. Verify Resolution
   ↓
7. Document Solution
```

## Advanced Tips

### Custom Timeframes
- 300 = 5 minutes (real-time)
- 3600 = 1 hour (recent issues)
- 86400 = 24 hours (daily patterns)
- 604800 = 7 days (weekly trends)

### Specific Client Analysis
Always include client MAC when troubleshooting individual devices for more accurate diagnosis.

### Performance Baselines
Run performance analysis during normal operations to establish baselines for comparison.

### Change Management
Always run configuration check before and after planned changes to catch conflicts early.