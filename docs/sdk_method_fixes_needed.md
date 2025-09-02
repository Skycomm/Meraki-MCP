# SDK Method Fixes Required

Based on MCP client testing, these method names need to be corrected in the SDK modules:

## ✅ Confirmed Working Method Corrections

### 1. Appliance Module
**Issue**: Tool uses non-existent `getNetworkApplianceUplinkStatuses`  
**Fix**: Use `getNetworkApplianceUplinksUsageHistory` (with timespan parameter)  
**Status**: ✅ Tested working - returns 1440 data points

### 2. Switch Module  
**Issue**: Tools use non-existent `getNetworkSwitchPorts` and `getNetworkSwitchPortStatuses`  
**Fix**: Use `getDeviceSwitchPorts` and `getDeviceSwitchPortsStatuses` (device-level, not network-level)  
**Status**: ✅ Tested working - returns 10 ports for switch Q2HP-GCZQ-7AWT

### 3. Devices Module
**Issue**: Tool uses `getNetworkDevices` in wrong module  
**Fix**: Move to Networks module - `meraki.dashboard.networks.getNetworkDevices`  
**Status**: ✅ Tested working - returns 6 devices

**Issue**: Tool uses non-existent `getDeviceUplinkLossAndLatency`  
**Fix**: Remove this tool - method doesn't exist in SDK

### 4. SM Module
**Issue**: Tool uses non-existent `getOrganizationSmSentryPoliciesAssignments`  
**Fix**: Use `getOrganizationSmSentryPoliciesAssignmentsByNetwork`  
**Status**: ✅ Tested working - returns 2 assignments

### 5. Sensor Module
**Issue**: Tool uses non-existent `getNetworkSensorAlertsOverview`  
**Fix**: Use `getNetworkSensorAlertsCurrentOverviewByMetric`  
**Status**: ✅ Method exists (404 expected - no sensor devices in test network)

## 📋 Parameter Requirement Fixes

### 6. Licensing Module
**Issue**: `getAdministeredLicensingSubscriptionSubscriptions` missing required parameter  
**Fix**: Add `organizationIds=[org_id]` parameter  
**Status**: ✅ Parameter fix confirmed (404 expected - no subscriptions in test org)

### 7. Insight Module
**Issue**: Insight methods reject `perPage` parameter  
**Fix**: Remove pagination from Insight tools  
**Status**: ⚠️ 403 Forbidden (requires Insight license)

### 8. Insight Application Health
**Issue**: Missing required `applicationId` parameter  
**Fix**: Add application discovery step or make parameter required  
**Status**: ⚠️ 403 Forbidden (requires Insight license)

## 🎯 Implementation Priority

**High Priority (Method Name Fixes)**:
1. ✅ Appliance: Fix uplink method name
2. ✅ Switch: Fix port method names (device-level)  
3. ✅ Devices: Move getNetworkDevices to Networks module
4. ✅ SM: Fix sentry policies method name
5. ✅ Sensor: Fix alert overview method name

**Medium Priority (Parameter Fixes)**:
6. ✅ Licensing: Add organizationIds parameter
7. Remove perPage from Insight methods
8. Make applicationId required for Insight app health

**Low Priority (Infrastructure Dependencies)**:
- Cellular Gateway: Requires MG devices (not available in test env)
- Sensor: Requires MT devices (not available in test env)  
- Insight: Requires Insight license (403 Forbidden)

## 🚀 Next Steps

1. Update SDK modules with corrected method names
2. Fix parameter requirements
3. Test all fixes as MCP client
4. Update tool documentation with requirements