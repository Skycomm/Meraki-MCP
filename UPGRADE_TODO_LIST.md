# Meraki MCP Server - Upgrade TODO List

## Priority 1 - High Value Features (Most Requested)

### 1. Traffic Shaping Tools
- `get_traffic_shaping_rules` - View QoS configuration
- `update_traffic_shaping_rules` - Set bandwidth limits per application
- `get_traffic_shaping_uplink_selection` - View WAN failover settings
- `update_traffic_shaping_vpn_exclusions` - Exclude apps from VPN tunnel
- `manage_custom_performance_classes` - Create QoS profiles

### 2. Firewall Management Tools  
- `get_l3_firewall_rules` - Layer 3 firewall rules
- `get_l7_firewall_rules` - Application-based rules
- `get_port_forwarding_rules` - NAT/port forwarding
- `update_firewall_rules` - Modify security rules
- `manage_firewall_services` - Configure allowed services

### 3. Enhanced Monitoring Dashboard
- `get_network_health_summary` - Combined health metrics
- `get_uplink_bandwidth_history` - Historical bandwidth (up to 31 days)
- `get_vpn_performance_stats` - VPN tunnel metrics
- `get_critical_alerts` - Priority alerts only
- `get_device_utilization` - CPU/memory stats

### 4. Troubleshooting & Diagnostics Tools
- `diagnose_connectivity_issues` - Auto-detect common problems
- `analyze_packet_loss_patterns` - Identify loss trends/causes
- `check_dns_resolution` - DNS troubleshooting
- `verify_dhcp_operations` - DHCP lease issues
- `test_vlan_connectivity` - Inter-VLAN routing tests
- `analyze_wireless_issues` - WiFi performance problems

### 5. Event Log Analysis
- `search_error_events` - Find specific errors
- `analyze_failure_patterns` - Identify recurring issues
- `track_config_changes` - Who changed what, when
- `correlate_events` - Link related events
- `generate_incident_timeline` - Event sequence for issues

### 6. Client Connectivity Troubleshooting
- `trace_client_connection` - Full connection path
- `analyze_client_failures` - Why clients can't connect
- `check_authentication_logs` - 802.1X/RADIUS issues
- `monitor_client_roaming` - AP handoff problems
- `diagnose_slow_performance` - Client speed issues

### 7. Network Change Tracking
- `get_recent_config_changes` - Last 24hr/7d/30d changes
- `compare_config_versions` - Before/after comparison
- `track_admin_actions` - Audit trail
- `detect_unauthorized_changes` - Security monitoring
- `backup_current_config` - Configuration snapshots

### 8. Diagnostic Report Generator
- `generate_health_report` - Comprehensive network health
- `create_troubleshooting_report` - For support tickets
- `export_performance_metrics` - Historical data export
- `generate_compliance_report` - Security/policy compliance
- `create_executive_summary` - High-level status

## Priority 2 - Advanced Features

### 4. Alert Configuration
- `get_alert_settings` - Current alert configuration
- `update_alert_thresholds` - Set alert triggers
- `configure_snmp_alerts` - SNMP trap setup
- `get_alert_history` - Past alerts/events

### 5. VPN Configuration
- `get_vpn_status` - Current VPN state
- `configure_site_to_site_vpn` - S2S VPN setup
- `manage_vpn_peers` - Third-party VPN
- `get_vpn_client_stats` - Client VPN usage

### 6. Uplink Monitoring
- `monitor_wan_failover` - Failover status
- `get_uplink_usage_trends` - Bandwidth trends
- `configure_wan_preferences` - Primary/backup WAN

## Priority 3 - Specialized Tools

### 7. Live Tools
- `run_ping_test` - Network connectivity test
- `run_traceroute` - Path analysis
- `run_cable_test` - Physical cable testing
- `blink_device_leds` - Physical identification

### 8. Firmware Management
- `check_firmware_updates` - Available updates
- `schedule_firmware_upgrade` - Plan updates
- `get_upgrade_history` - Past upgrades

## Implementation Guidelines

### For Each Tool Category:
1. **Add Helper Tool** - Like `check_dhcp_network_type`
2. **Clear Prefixes** - [MX], [MS], [MR], [MG] for device types  
3. **Error Messages** - Guide users to correct tools
4. **Documentation** - Create category guide (like DHCP_TOOLS_GUIDE.md)

## Notes
- Total new tools estimated: 150-200
- API confirmed working for all listed features
- Packet loss monitoring limited to 5 minutes (API constraint)
- Some features require specific device types or licenses