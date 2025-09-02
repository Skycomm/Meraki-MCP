# Wireless Tools NOT Used in Comprehensive Audit

## Tools That Were Missed (Should Test These):

### 1. Client-Specific Analytics
- `get_network_wireless_client` - Get details for specific client (only used clients list)
- `get_network_wireless_client_latency_stats` - Individual client latency
- `get_network_wireless_clients_connection_stats` - Client connection stats
- `get_network_wireless_clients_latency_stats` - Multiple clients latency

### 2. Device-Specific Performance
- `get_device_wireless_connection_stats` - Per-AP connection stats
- `get_device_wireless_latency_stats` - Per-AP latency stats
- `get_device_wireless_cpu_load` - AP CPU load
- `get_device_wireless_alternate_management_interface` - AP mgmt interface
- `get_device_wireless_alternate_management_interface_ipv6` - IPv6 mgmt
- `get_device_wireless_electronic_shelf_label` - ESL per device

### 3. Network-Wide Analytics
- `get_network_wireless_usage` - Current usage (only got history)
- `get_network_wireless_devices_connection_stats` - All APs connection stats
- `get_network_wireless_devices_latencies` - Real-time latencies
- `get_network_wireless_devices_latency_stats` - Latency stats for all APs
- `get_network_wireless_devices_packet_loss` - Packet loss for all APs
- `get_network_wireless_latency_history` - Historical latency data
- `get_network_wireless_l7_firewall_rules_application_categories` - App categories

### 4. Ethernet Ports on APs
- `get_network_wireless_ethernet_ports_profiles` - Ethernet port profiles
- `get_network_wireless_ethernet_ports_profile` - Specific profile

### 5. Organization-Wide Analytics  
- `get_org_wireless_channel_util_history_by_device` - Channel util by device
- `get_org_wireless_channel_util_history_by_network` - Channel util by network
- `get_organization_wireless_devices_channel_utilization_by_device` - Per device
- `get_organization_wireless_devices_channel_utilization_by_network` - Per network
- `get_organization_wireless_devices_packet_loss_by_client` - Loss by client
- `get_organization_wireless_devices_packet_loss_by_device` - Loss by device
- `get_organization_wireless_devices_packet_loss_by_network` - Loss by network
- `get_organization_wireless_devices_power_mode_history` - Power mode history
- `get_organization_wireless_devices_system_cpu_load_history` - CPU history
- `get_organization_wireless_devices_wireless_controllers_by_device` - Controllers
- `get_organization_wireless_clients_overview_by_device` - Client overview
- `get_organization_wireless_air_marshal_settings_by_network` - Security settings
- `get_organization_wireless_location_scanning_by_network` - Location per network
- `get_organization_wireless_location_scanning_receivers` - Location receivers

### 6. RadSec & Security
- `get_org_wireless_radsec_authorities` - RadSec authorities
- `get_org_wireless_radsec_crl_deltas` - CRL deltas
- `get_org_wireless_radsec_crls` - Certificate revocation lists
- `get_organization_wireless_radsec_certificate_authorities` - Cert authorities

### 7. Bluetooth
- `get_network_wireless_bluetooth_clients` - Bluetooth clients
- `get_device_wireless_bluetooth_settings` - Per-AP Bluetooth

### 8. RF Management
- `get_network_wireless_rf_profiles_assignments_by_device` - RF assignments
- `get_organization_wireless_rf_profiles_assignments_by_device` - Org RF assignments
- `recalculate_organization_wireless_radio_auto_rf_channels` - Recalc channels

### 9. Isolation Allowlist
- `get_org_wireless_isolation_allowlist` - Full allowlist (not just entries)

## Test Commands for Missing Tools

```python
# Test specific client details
await session.call_tool('get_network_wireless_client', {
    'network_id': 'L_726205439913500692',
    'client_id': '00:11:22:33:44:55'  # Use actual MAC from clients list
})

# Test per-AP performance
await session.call_tool('get_device_wireless_connection_stats', {
    'serial': 'Q2PD-SRPB-4JTT'  # Bathroom AP
})

# Test CPU load
await session.call_tool('get_device_wireless_cpu_load', {
    'serial': 'Q2PD-SRPB-4JTT'
})

# Test Bluetooth clients
await session.call_tool('get_network_wireless_bluetooth_clients', {
    'network_id': 'L_726205439913500692'
})

# Test current usage (not history)
await session.call_tool('get_network_wireless_usage', {
    'network_id': 'L_726205439913500692'
})

# Test ethernet port profiles
await session.call_tool('get_network_wireless_ethernet_ports_profiles', {
    'network_id': 'L_726205439913500692'
})

# Test organization-wide CPU history
await session.call_tool('get_organization_wireless_devices_system_cpu_load_history', {
    'organization_id': '686470'
})

# Test RadSec authorities
await session.call_tool('get_org_wireless_radsec_authorities', {
    'organization_id': '686470'
})
```

## Summary
- **Total Wireless Tools**: 142
- **Tools Used in Audit**: ~45
- **Tools NOT Used**: ~97 (mostly update/create/delete operations)
- **Read-Only Tools Missed**: ~40

The audit missed many detailed analytics tools that could provide deeper insights, especially:
1. Per-device performance metrics
2. Per-client analytics
3. Bluetooth functionality
4. Ethernet port profiles on APs
5. RadSec security features
6. CPU and power mode history