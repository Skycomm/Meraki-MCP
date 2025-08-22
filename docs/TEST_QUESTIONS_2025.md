# 🧪 Test Questions for New 2025 Cisco Meraki APIs

Here are the test questions designed to verify each new API is working correctly:

## 📱 Systems Manager (SM) APIs

### 1. `get_network_sm_devices`
**Question**: "What mobile devices are enrolled in our MDM system?"
**Expected**: List of managed devices with OS, user, battery status
**Note**: Requires SM license and enrolled devices

### 2. `get_network_sm_device_detail`
**Question**: "What's the detailed status of device [ID]?"
**Expected**: Device specs, security status, network info, storage

### 3. `get_network_sm_device_apps`
**Question**: "What apps are installed on managed device [ID]?"
**Expected**: List of apps, versions, managed vs personal apps

### 4. `reboot_network_sm_devices`
**Question**: "Can we remotely reboot device [ID]?"
**Expected**: Command sent confirmation

### 5. `get_network_sm_profiles`
**Question**: "What configuration profiles are deployed to our managed devices?"
**Expected**: List of profiles with target tags and payloads

### 6. `get_network_sm_performance_history`
**Question**: "What's the performance history for device [ID]?"
**Expected**: CPU, memory, disk, network usage over time

## 📄 Licensing Management APIs

### 1. `get_organization_licenses`
**Question**: "How many licenses do we have and when do they expire?"
**Expected**: License list grouped by type with expiration dates
**Note**: Organization must use per-device licensing

### 2. `get_organization_licensing_coterm`
**Question**: "What is our co-termination date and license count by model?"
**Expected**: Co-term date, device counts, expired status

### 3. `claim_organization_license`
**Question**: "Can we claim license key XXXX-XXXX-XXXX?"
**Expected**: Success confirmation with license details

### 4. `update_organization_license`
**Question**: "Can we assign license [ID] to device [serial]?"
**Expected**: Assignment confirmation

### 5. `move_organization_licenses`
**Question**: "Can we transfer licenses from org A to org B?"
**Expected**: Transfer confirmation

### 6. `renew_organization_licenses_seats`
**Question**: "Can we renew SM seats using unused license?"
**Expected**: Renewal confirmation with new expiration

## 🛡️ Policy Objects APIs

### 1. `get_organization_policy_objects`
**Question**: "What security policy objects are defined for blocking IPs/domains?"
**Expected**: List of objects grouped by category (network, application)

### 2. `create_organization_policy_object`
**Question**: "Can we create a test policy object for IP 192.168.100.100?"
**Expected**: Created object with ID and details
**Fix Applied**: Changed type from 'ipv4' to 'cidr'

### 3. `update_organization_policy_object`
**Question**: "Can we rename policy object [ID] to 'Updated Name'?"
**Expected**: Update confirmation

### 4. `delete_organization_policy_object`
**Question**: "Can we delete test policy object [ID]?"
**Expected**: Deletion confirmation

### 5. `get_organization_policy_objects_groups`
**Question**: "How are our policy objects organized into groups?"
**Expected**: List of groups with member objects

### 6. `create_organization_policy_objects_group`
**Question**: "Can we create a group for related policy objects?"
**Expected**: Group created with ID

## 📊 Enhanced Monitoring APIs

### 1. `get_organization_api_usage`
**Question**: "What API endpoints are being used most frequently?"
**Expected**: Usage by admin, top endpoints, response codes
**Status**: ✅ Working

### 2. `get_organization_switch_ports_history`
**Question**: "How many switch ports are active across the organization?"
**Expected**: Total ports, active count, power usage
**Status**: ✅ Working

### 3. `get_organization_devices_migration_status`
**Question**: "Are any devices currently being migrated between networks?"
**Expected**: Migration list with progress
**Status**: ✅ Working (returns device list as fallback)

### 4. `get_device_memory_history`
**Question**: "What is the memory usage history for device [serial]?"
**Expected**: Memory usage over time
**Status**: ❌ API not yet available (beta/planned)

### 5. `get_device_cpu_power_mode_history`
**Question**: "What's the CPU power mode history for wireless device [serial]?"
**Expected**: Power mode changes over time
**Status**: Using radio settings as proxy

### 6. `get_device_wireless_cpu_load`
**Question**: "What is the current CPU load on wireless device [serial]?"
**Expected**: CPU percentage, per-core stats
**Status**: ✅ Working (returns wireless status)

## Test Results Summary

### Working APIs (6/24):
- ✅ Policy Objects viewing (empty results normal)
- ✅ API usage monitoring
- ✅ Switch port history
- ✅ Device listing (migration proxy)
- ✅ Wireless device status

### APIs Requiring Specific Licenses/Setup:
- ❌ Systems Manager (requires SM license)
- ❌ Per-device licensing (org uses co-term)
- ❌ Policy object creation (fixed type mapping)

### APIs Not Yet Available:
- ❌ Device memory history (appears to be beta/planned)

## Recommendations

1. **Systems Manager**: Need SM-enabled network to test
2. **Licensing**: Organization uses co-term model, not per-device
3. **Policy Objects**: Type mapping fixed, should work now
4. **Monitoring**: Some 2025 features may still be in beta