# Enhanced Monitoring Dashboard Guide

Comprehensive network health monitoring combining multiple APIs for a complete view of your network.

## Prerequisites

**ALWAYS run this first:**
```
check_monitoring_prerequisites(network_id)
```

This verifies:
- Available device types
- Supported monitoring features
- API limitations

## Quick Start

### 1. Get Network Health Overview
```python
# Quick 5-minute health check
get_network_health_summary(network_id)

# 24-hour health summary
get_network_health_summary(network_id, timespan=86400)
```

### 2. Generate Full Health Report
```python
# Complete 1-hour report
generate_network_health_report(network_id)

# Custom 24-hour report
generate_network_health_report(
    network_id,
    include_bandwidth=True,
    include_vpn=True,
    include_devices=True,
    timespan=86400
)
```

## Tools Reference

### Core Monitoring
- `get_network_health_summary()` - Combined health metrics dashboard
- `generate_network_health_report()` - Comprehensive report generation
- `check_monitoring_prerequisites()` - Verify monitoring capabilities

### Performance Metrics
- `get_uplink_bandwidth_history()` - WAN bandwidth trends
- `get_device_utilization()` - CPU/memory/port usage
- `get_vpn_performance_stats()` - VPN tunnel metrics

### Alerts & Events
- `get_critical_alerts()` - High-priority network issues

## Dashboard Components

### 🏥 Health Summary
Shows:
- Device online/offline status
- Client connection success rates
- WAN uplink status
- Recent alerts
- Overall health score

### 📈 Bandwidth History
Displays:
- Upload/download speeds
- Peak usage times
- Average throughput
- Usage trends

### 💻 Device Utilization
Monitors:
- MX performance scores
- Switch port utilization
- AP wireless status
- Device uptime

### 🔒 VPN Performance
Tracks:
- Site-to-site tunnel status
- Latency and jitter
- Packet loss rates
- Data usage per tunnel

## Common Use Cases

### 1. Morning Health Check
```python
# Quick 5-minute overview
summary = get_network_health_summary(network_id, timespan=300)
print(summary)
```

### 2. Bandwidth Capacity Planning
```python
# Check last 7 days of bandwidth
bandwidth = get_uplink_bandwidth_history(
    network_id,
    timespan=604800,  # 7 days
    resolution=3600   # Hourly data
)
```

### 3. VPN Troubleshooting
```python
# Check VPN performance
vpn_stats = get_vpn_performance_stats(
    network_id,
    timespan=3600  # Last hour
)
```

### 4. Executive Report
```python
# Generate comprehensive report
report = generate_network_health_report(
    network_id,
    include_bandwidth=True,
    include_vpn=True,
    include_devices=True,
    timespan=86400  # 24 hours
)
```

## Understanding Metrics

### Health Score
- 🟢 80-100%: Healthy network
- 🟡 60-79%: Minor issues
- 🔴 0-59%: Critical problems

### Connection Success Rates
- Association → Authentication → DHCP → DNS → Success
- Each step shows success percentage
- Identifies where clients fail to connect

### Bandwidth Metrics
- Average: Typical usage
- Peak: Maximum observed
- Trend: Recent direction (📈📉➡️)

### VPN Metrics
- Latency: Round-trip time (target < 150ms)
- Jitter: Latency variation (target < 50ms)
- Loss: Packet loss rate (target < 1%)

## Time Ranges

### Supported Timespans
- 300 (5 minutes) - Real-time monitoring
- 3600 (1 hour) - Short-term analysis
- 86400 (24 hours) - Daily overview
- 604800 (7 days) - Weekly trends
- 2592000 (30 days) - Monthly analysis

### Resolution Options
- 300 - 5-minute intervals
- 600 - 10-minute intervals
- 1800 - 30-minute intervals
- 3600 - Hourly intervals
- 86400 - Daily intervals

## Limitations

### API Constraints
- Packet loss monitoring: 5 minutes maximum
- Some metrics require specific device types
- Historical data retention varies

### Device Requirements
- Bandwidth monitoring: Requires MX
- Port statistics: Requires MS
- Wireless metrics: Requires MR
- VPN stats: Requires MX with VPN

## Best Practices

### 1. Regular Monitoring
- Run health summary every hour
- Generate daily reports
- Archive weekly reports

### 2. Alert Response
- Check critical alerts immediately
- Investigate devices in alerting state
- Review connection failure patterns

### 3. Capacity Planning
- Monitor bandwidth trends weekly
- Track device utilization monthly
- Plan upgrades based on peaks

### 4. Documentation
- Save reports for compliance
- Track changes over time
- Document issue resolutions