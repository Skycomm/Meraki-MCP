# Client Troubleshooting Guide

Specialized tools for diagnosing and resolving individual client connection issues.

## Quick Start

**When a client has issues, start here:**
```
client_troubleshooting_help()
```

This shows which tool to use for specific client problems.

## Core Client Troubleshooting Tools

### 1. Get Client Details
```python
# Basic client information
get_client_details(network_id, "AA:BB:CC:DD:EE:FF")

# With extended history
get_client_details(
    network_id,
    client_id_or_mac="AA:BB:CC:DD:EE:FF",
    timespan=604800  # 7 days
)
```

**Shows:**
- Device information (OS, manufacturer)
- Current connection status
- IP addressing details
- Data usage statistics
- Security information

**Use when:**
- Starting any client troubleshooting
- Need basic client information
- Checking current status
- Verifying client identity

### 2. Diagnose Client Connection
```python
# Quick diagnosis
diagnose_client_connection(network_id, "AA:BB:CC:DD:EE:FF")

# Detailed analysis
diagnose_client_connection(
    network_id,
    client_mac="AA:BB:CC:DD:EE:FF",
    timespan=86400  # Last 24 hours
)
```

**Analyzes:**
- Authentication failures
- DHCP issues
- Disconnection events
- Signal quality problems
- Recent error patterns

**Returns:**
- Specific issue identification
- Root cause analysis
- Step-by-step fixes
- Preventive measures

### 3. Client Connection History
```python
# View connection timeline
get_client_connection_history(
    network_id,
    client_mac="AA:BB:CC:DD:EE:FF",
    timespan=86400  # 24 hours
)
```

**Tracks:**
- Association/disassociation events
- Roaming between APs
- Connection stability
- Usage patterns
- Time-based trends

**Use when:**
- Client reports intermittent issues
- Need to see connection patterns
- Troubleshooting roaming problems
- Analyzing stability over time

### 4. Analyze Client Performance
```python
# Performance metrics
analyze_client_performance(
    network_id,
    client_mac="AA:BB:CC:DD:EE:FF"
)

# Extended analysis
analyze_client_performance(
    network_id,
    client_mac="AA:BB:CC:DD:EE:FF",
    timespan=7200  # 2 hours
)
```

**Examines:**
- Signal strength (RSSI)
- Signal quality (SNR)
- Data rates and usage
- Latency indicators
- Performance bottlenecks

**Provides:**
- Performance assessment
- Optimization suggestions
- Hardware recommendations
- Configuration tweaks

### 5. Compare Client Behavior
```python
# Compare against network baseline
compare_client_behavior(
    network_id,
    client_mac="AA:BB:CC:DD:EE:FF"
)

# Long-term comparison
compare_client_behavior(
    network_id,
    client_mac="AA:BB:CC:DD:EE:FF",
    timespan=2592000  # 30 days
)
```

**Compares:**
- Usage vs network average
- Signal vs other clients
- Connection patterns
- Device type behavior
- SSID-specific issues

**Identifies:**
- Unique vs common problems
- Outlier behavior
- Environmental factors
- Policy impacts

## Common Troubleshooting Scenarios

### Scenario 1: "Client Can't Connect at All"
```python
# 1. Check current status
get_client_details(network_id, "AA:BB:CC:DD:EE:FF")

# 2. Diagnose the issue
diagnose_client_connection(network_id, "AA:BB:CC:DD:EE:FF")

# 3. Review history for patterns
get_client_connection_history(network_id, "AA:BB:CC:DD:EE:FF")
```

### Scenario 2: "Client Keeps Disconnecting"
```python
# 1. Check connection history
get_client_connection_history(
    network_id, 
    "AA:BB:CC:DD:EE:FF",
    timespan=86400
)

# 2. Analyze performance
analyze_client_performance(network_id, "AA:BB:CC:DD:EE:FF")

# 3. Compare behavior
compare_client_behavior(network_id, "AA:BB:CC:DD:EE:FF")
```

### Scenario 3: "Client Has Slow Performance"
```python
# 1. Performance analysis
analyze_client_performance(network_id, "AA:BB:CC:DD:EE:FF")

# 2. Compare to baseline
compare_client_behavior(network_id, "AA:BB:CC:DD:EE:FF")

# 3. Check for connection issues
diagnose_client_connection(network_id, "AA:BB:CC:DD:EE:FF")
```

### Scenario 4: "Client Can't Get IP Address"
```python
# 1. Diagnose DHCP issues
diagnose_client_connection(
    network_id,
    "AA:BB:CC:DD:EE:FF",
    timespan=3600
)

# 2. Check current details
get_client_details(network_id, "AA:BB:CC:DD:EE:FF")

# 3. Review connection events
get_client_connection_history(network_id, "AA:BB:CC:DD:EE:FF")
```

## Understanding Client Issues

### Authentication Problems
**Common Causes:**
- Wrong password/credentials
- Certificate expired
- RADIUS server issues
- MAC address not authorized
- Wrong VLAN assignment

**Quick Fixes:**
- Re-enter credentials
- Update certificates
- Check RADIUS logs
- Verify MAC filtering
- Review VLAN policies

### DHCP Failures
**Common Causes:**
- DHCP pool exhausted
- VLAN misconfiguration
- Firewall blocking DHCP
- Static IP conflict
- DHCP relay issues

**Quick Fixes:**
- Expand DHCP pool
- Verify VLAN settings
- Check firewall rules
- Clear IP conflicts
- Test DHCP relay

### Performance Issues
**Common Causes:**
- Weak signal strength
- High interference
- Band congestion
- QoS restrictions
- Client power saving

**Quick Fixes:**
- Move closer to AP
- Switch to 5GHz
- Change channels
- Adjust QoS rules
- Disable power saving

### Roaming Problems
**Common Causes:**
- Sticky client
- Poor AP overlap
- Different SSID settings
- Authentication delays
- Client driver issues

**Quick Fixes:**
- Update client drivers
- Adjust roaming thresholds
- Ensure consistent SSID
- Enable fast roaming
- Check AP placement

## Client Metrics Guide

### Signal Strength (RSSI)
- **-30 to -50 dBm**: Excellent
- **-50 to -67 dBm**: Very Good
- **-67 to -75 dBm**: Good
- **-75 to -80 dBm**: Fair
- **Below -80 dBm**: Poor

### Signal-to-Noise Ratio (SNR)
- **Above 25 dB**: Excellent
- **20-25 dB**: Very Good
- **15-20 dB**: Good
- **10-15 dB**: Fair
- **Below 10 dB**: Poor

### Data Usage Patterns
- **Light**: < 100 MB/day
- **Normal**: 100 MB - 1 GB/day
- **Heavy**: 1-5 GB/day
- **Very Heavy**: > 5 GB/day

## Best Practices

### Initial Assessment
1. Always start with get_client_details()
2. Note the client OS and type
3. Check current connection status
4. Review recent activity

### Systematic Diagnosis
1. Gather symptoms from user
2. Run diagnostic tools
3. Compare against baseline
4. Check for patterns
5. Test solutions

### Documentation
- Record MAC address
- Note time of issues
- Document symptoms
- Track solutions tried
- Follow up on fixes

### Common Solutions Priority
1. **Restart client WiFi**
2. **Forget and rejoin network**
3. **Update device drivers**
4. **Check credentials**
5. **Move to better coverage**

## Advanced Troubleshooting

### Using Multiple Tools Together
```python
# Comprehensive client analysis
def analyze_client_completely(network_id, mac):
    # Get all data
    details = get_client_details(network_id, mac)
    diagnosis = diagnose_client_connection(network_id, mac)
    history = get_client_connection_history(network_id, mac)
    performance = analyze_client_performance(network_id, mac)
    comparison = compare_client_behavior(network_id, mac)
    
    # Combine insights for full picture
```

### Time-Based Analysis
- Recent issues: Use 1-hour timespan
- Daily patterns: Use 24-hour timespan  
- Weekly trends: Use 7-day timespan
- Historical: Use 30-day timespan

### Environmental Factors
- Check multiple clients in same area
- Look for time-of-day patterns
- Consider physical obstacles
- Review recent changes

### Policy Verification
- Group policy restrictions
- RADIUS attributes
- Bandwidth limits
- Access control lists

## Quick Reference

### MAC Address Format
Always use colon-separated format:
- ✅ Correct: `AA:BB:CC:DD:EE:FF`
- ❌ Wrong: `AA-BB-CC-DD-EE-FF`
- ❌ Wrong: `AABBCCDDEEFF`

### Common Error Messages
- **"Client not found"**: Client hasn't connected recently
- **"No events"**: Extend timespan or check MAC
- **"Access denied"**: Verify API permissions
- **"Invalid MAC"**: Check format

### Performance Thresholds
- Signal < -80 dBm: Connectivity issues likely
- SNR < 10 dB: High interference
- Disconnects > 5/hour: Stability problem
- Usage > 10 GB/day: Heavy user

### When to Escalate
- Hardware failure suspected
- Multiple clients same issue
- Infrastructure problem
- Security incident
- Consistent failures after fixes