# Event Log Analysis Guide

Powerful tools for analyzing network events, finding patterns, and identifying root causes.

## Quick Start

**Start with the help tool to see what's available:**
```
event_analysis_help()
```

This will show you which event analysis tool to use for your specific needs.

## Core Event Analysis Tools

### 1. Search Event Logs
```python
# Search for specific events
search_event_logs(
    network_id,
    search_text="authentication failed",
    timespan=86400  # Last 24 hours
)

# Filter by event type
search_event_logs(
    network_id,
    event_type="security",
    severity="critical"
)

# Search by device
search_event_logs(
    network_id,
    device_serial="Q2XX-XXXX-XXXX",
    timespan=3600
)
```

**Parameters:**
- `search_text`: Free text search
- `event_type`: "security", "wireless", "appliance", "switch"
- `device_serial`: Specific device
- `client_mac`: Specific client
- `severity`: "critical", "warning", "informational"
- `timespan`: Seconds (max 2592000 = 30 days)

**Use cases:**
- Find authentication failures
- Track configuration changes
- Monitor security events
- Debug client issues

### 2. Analyze Error Patterns
```python
# Find recurring issues
analyze_error_patterns(network_id, timespan=604800)  # 7 days

# Focus on specific area
analyze_error_patterns(
    network_id,
    pattern_type="authentication",
    timespan=86400
)
```

**Pattern types:**
- `authentication`: Login/auth failures
- `connectivity`: Connection drops
- `performance`: Slowness issues
- `security`: Security events
- `configuration`: Config errors

**Returns:**
- Error frequency
- Affected devices
- Time patterns
- Severity distribution
- Recommendations

### 3. Identify Root Causes
```python
# Analyze events for root cause
identify_root_causes(
    network_id,
    issue_description="Users can't connect to WiFi",
    timespan=3600
)

# With specific client
identify_root_causes(
    network_id,
    issue_description="Client keeps disconnecting",
    client_mac="AA:BB:CC:DD:EE:FF"
)
```

**Analyzes:**
- Event correlations
- Timing relationships
- Common patterns
- Device dependencies
- Configuration impacts

### 4. Correlate Events
```python
# Find related events around specific time
correlate_events(
    network_id,
    timestamp="2025-01-20T10:30:00Z",
    window_minutes=30  # 30 mins before/after
)

# Correlate with specific event
correlate_events(
    network_id,
    reference_event_id="12345",
    window_minutes=15
)
```

**Correlation analysis:**
- Temporal proximity
- Device relationships
- Client impacts
- Service dependencies
- Cascade effects

### 5. Generate Incident Timeline
```python
# Create incident report
generate_incident_timeline(
    network_id,
    start_time="2025-01-20T09:00:00Z",
    end_time="2025-01-20T11:00:00Z",
    incident_type="outage"
)

# With impact analysis
generate_incident_timeline(
    network_id,
    start_time="2025-01-20T09:00:00Z",
    end_time="2025-01-20T11:00:00Z",
    incident_type="security",
    include_impact=True
)
```

**Incident types:**
- `outage`: Service disruption
- `security`: Security incident
- `performance`: Performance degradation
- `maintenance`: Planned maintenance

## Common Analysis Scenarios

### Scenario 1: "Multiple authentication failures"
```python
# 1. Search for auth failures
search_event_logs(
    network_id,
    search_text="authentication failed",
    timespan=3600
)

# 2. Analyze patterns
analyze_error_patterns(
    network_id,
    pattern_type="authentication"
)

# 3. Find root cause
identify_root_causes(
    network_id,
    issue_description="Multiple auth failures"
)
```

### Scenario 2: "Network outage investigation"
```python
# 1. Generate timeline
generate_incident_timeline(
    network_id,
    start_time="2025-01-20T10:00:00Z",
    end_time="2025-01-20T11:00:00Z",
    incident_type="outage"
)

# 2. Correlate events
correlate_events(
    network_id,
    timestamp="2025-01-20T10:15:00Z",
    window_minutes=30
)

# 3. Identify root cause
identify_root_causes(
    network_id,
    issue_description="Complete network outage"
)
```

### Scenario 3: "Security incident response"
```python
# 1. Search security events
search_event_logs(
    network_id,
    event_type="security",
    severity="critical",
    timespan=86400
)

# 2. Generate incident report
generate_incident_timeline(
    network_id,
    start_time="2025-01-20T00:00:00Z",
    end_time="2025-01-20T23:59:59Z",
    incident_type="security"
)

# 3. Analyze patterns
analyze_error_patterns(
    network_id,
    pattern_type="security"
)
```

### Scenario 4: "Performance degradation"
```python
# 1. Search for performance events
search_event_logs(
    network_id,
    search_text="high latency OR packet loss",
    timespan=3600
)

# 2. Correlate with time
correlate_events(
    network_id,
    timestamp="2025-01-20T14:30:00Z",
    window_minutes=60
)

# 3. Root cause analysis
identify_root_causes(
    network_id,
    issue_description="Network running slow"
)
```

## Understanding Event Types

### Security Events
- IDS alerts
- Firewall blocks
- Authentication failures
- Rogue device detection
- Configuration changes

### Wireless Events
- Client associations
- Roaming events
- Channel changes
- RF interference
- Authentication issues

### Appliance Events
- WAN failover
- VPN connections
- Traffic shaping
- DHCP issues
- Routing changes

### Switch Events
- Port status changes
- STP topology changes
- PoE events
- VLAN changes
- Link failures

## Event Severity Levels

### Critical 🔴
- Service outages
- Security breaches
- Hardware failures
- License expiration

### Warning 🟡
- Performance degradation
- Failed authentications
- Configuration conflicts
- Threshold violations

### Informational 🔵
- Normal operations
- Client connections
- Configuration saves
- Scheduled tasks

## Best Practices

### Effective Searching
1. Start broad, then narrow
2. Use appropriate timespans
3. Combine multiple filters
4. Check related devices

### Pattern Analysis
1. Look for time patterns (hourly, daily)
2. Check affected device groups
3. Identify common factors
4. Review recent changes

### Root Cause Analysis
1. Start with symptom description
2. Review timeline of events
3. Check cascade effects
4. Verify with correlations

### Incident Documentation
1. Capture full timeline
2. Include all affected systems
3. Document resolution steps
4. Create post-mortem report

## Advanced Tips

### Time Formats
- ISO 8601: "2025-01-20T10:30:00Z"
- Relative: Use timespan in seconds
- Maximum timespan: 30 days (2592000 seconds)

### Search Operators
- AND: "failed AND authentication"
- OR: "timeout OR disconnect"
- NOT: "error NOT warning"
- Wildcards: "auth*" matches "authentication", "authorize"

### Performance Optimization
- Use specific time ranges
- Filter by device when possible
- Limit result sets appropriately
- Cache frequently used queries

### Integration Ideas
- Set up alerts for patterns
- Create daily summary reports
- Build incident playbooks
- Automate root cause analysis

## Common Event Patterns

### Authentication Loop
```
Pattern: Multiple auth failures → Success → Disconnect → Repeat
Cause: Wrong credentials, RADIUS timeout, certificate issues
```

### Cascading Failure
```
Pattern: WAN down → Failover → High CPU → Service degradation
Cause: Primary link failure causing resource exhaustion
```

### Broadcast Storm
```
Pattern: High broadcast traffic → Switch CPU spike → Port shutdowns
Cause: Loop in network, misconfigured STP
```

### RF Interference
```
Pattern: Channel changes → Client disconnects → Poor performance
Cause: External interference, overlapping channels
```

## Troubleshooting Event Analysis

### No Events Found
- Check timespan (max 30 days)
- Verify network has devices
- Ensure proper permissions
- Try broader search terms

### Too Many Results
- Narrow time range
- Add more filters
- Focus on severity
- Filter by device

### Missing Correlations
- Expand time window
- Check device relationships
- Review event types
- Verify timestamps

### Pattern Not Detected
- Increase analysis timespan
- Check pattern type
- Review event frequency
- Try manual correlation