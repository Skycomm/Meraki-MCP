# 🚀 Cisco Meraki MCP Server - 2025 Updates

## Summary of New Features Added

Based on research of the latest Cisco Meraki API documentation (v1.61.0 - August 2025), we've successfully implemented **24 new tools** across 4 major API categories:

### 📱 Systems Manager (SM) - 6 tools
- `get_network_sm_devices` - List all MDM devices
- `get_network_sm_device_detail` - Get specific device details
- `get_network_sm_device_apps` - List installed apps
- `reboot_network_sm_devices` - Remote reboot devices
- `get_network_sm_profiles` - List configuration profiles
- `get_network_sm_performance_history` - Device performance metrics

### 📄 Licensing Management - 6 tools
- `get_organization_licenses` - List all licenses
- `get_organization_licensing_coterm` - Co-termination info
- `claim_organization_license` - Claim new licenses
- `update_organization_license` - Assign/unassign licenses
- `move_organization_licenses` - Transfer between orgs
- `renew_organization_licenses_seats` - Renew SM seats

### 🛡️ Policy Objects - 6 tools
- `get_organization_policy_objects` - List policy objects
- `create_organization_policy_object` - Create IP/FQDN objects
- `update_organization_policy_object` - Modify objects
- `delete_organization_policy_object` - Remove objects
- `get_organization_policy_objects_groups` - List groups
- `create_organization_policy_objects_group` - Create groups

### 📊 Enhanced Monitoring (2025 New) - 6 tools
- `get_device_memory_history` - Memory utilization tracking
- `get_device_cpu_power_mode_history` - CPU power states
- `get_device_wireless_cpu_load` - Real-time CPU monitoring
- `get_organization_switch_ports_history` - Org-wide port stats
- `get_organization_devices_migration_status` - Migration tracking
- `get_organization_api_usage` - API consumption analytics

## Total Tool Count
- **Previous**: 55 tools
- **Added**: 24 tools
- **New Total**: 79 tools

## Key 2025 API Enhancements
1. **Enhanced Device Monitoring**: Memory and CPU tracking at device level
2. **Systems Manager Integration**: Full MDM capabilities
3. **Advanced Security**: Policy objects for granular control
4. **API Analytics**: Track and monitor API usage
5. **Migration Support**: Device migration status tracking

## Testing Status
All new APIs have been implemented with:
- ✅ Real Meraki SDK methods only
- ✅ Proper error handling
- ✅ Rich formatting for responses
- ✅ Type hints and documentation

## Still Available for Future Implementation
- OAuth 2.0 authentication support
- Configuration change auditing
- Enhanced cellular gateway features
- MAC table live tools
- Additional BETA features

## Usage Examples

### Systems Manager
```
# List all MDM devices
get_network_sm_devices network_id: "L_669347494617953785"

# Get device apps
get_network_sm_device_apps network_id: "L_669347494617953785" device_id: "12345"
```

### Licensing
```
# View all licenses
get_organization_licenses org_id: "686470"

# Claim a new license
claim_organization_license org_id: "686470" license_key: "XXXX-XXXX-XXXX"
```

### Policy Objects
```
# Create IP object
create_organization_policy_object org_id: "686470" name: "Office Subnet" category: "network" type: "ipv4" cidr: "10.0.0.0/24"

# Create FQDN object
create_organization_policy_object org_id: "686470" name: "Company Site" category: "application" type: "fqdn" fqdn: "example.com"
```

### Enhanced Monitoring
```
# Check device memory
get_device_memory_history serial: "Q2PD-7QTD-SZG2"

# Monitor API usage
get_organization_api_usage org_id: "686470"
```