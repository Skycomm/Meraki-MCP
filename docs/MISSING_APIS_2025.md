# 🆕 Missing Cisco Meraki APIs in 2025

Based on research of the latest Cisco Meraki API documentation (v1.61.0 - August 2025), here are the API categories and endpoints we haven't implemented yet:

## 1. 🔐 Administered/Identity APIs
- `GET /administered/identities/me` - Get current user identity
- OAuth 2.0 support endpoints

## 2. 📋 Policy Objects & Groups
- `GET /organizations/{org_id}/policyObjects` - List policy objects
- `POST /organizations/{org_id}/policyObjects` - Create policy object
- `GET /organizations/{org_id}/policyObjects/{id}` - Get specific policy object
- `PUT /organizations/{org_id}/policyObjects/{id}` - Update policy object
- `DELETE /organizations/{org_id}/policyObjects/{id}` - Delete policy object
- `GET /organizations/{org_id}/policyObjects/groups` - List policy object groups
- Similar CRUD operations for policy object groups

## 3. 📱 Systems Manager (SM) Endpoints
- `GET /networks/{network_id}/sm/devices` - List SM devices
- `GET /networks/{network_id}/sm/devices/{device_id}` - Get SM device details
- `PUT /networks/{network_id}/sm/devices/{device_id}` - Update SM device
- `GET /networks/{network_id}/sm/devices/{device_id}/performanceHistory` - Device performance
- `POST /networks/{network_id}/sm/devices/reboot` - Reboot SM devices
- `POST /networks/{network_id}/sm/devices/shutdown` - Shutdown SM devices
- `GET /networks/{network_id}/sm/devices/{device_id}/apps` - List installed apps
- `GET /networks/{network_id}/sm/profiles` - List SM profiles
- `GET /networks/{network_id}/sm/trustedServers` - List trusted servers
- PII endpoints for SM owners

## 4. 📄 Licensing APIs
- `GET /organizations/{org_id}/licenses` - List licenses
- `GET /organizations/{org_id}/licenses/{license_id}` - Get specific license
- `POST /organizations/{org_id}/licenses/claim` - Claim license
- `PUT /organizations/{org_id}/licenses/{license_id}` - Update license
- `POST /administered/licensing/subscription/subscriptions/claim` - Claim subscription
- `GET /organizations/{org_id}/licensing/coterm/licenses` - Co-term licenses

## 5. 🌐 Spaces Integration
- `GET /organizations/{org_id}/spaces/integrate/status` - Spaces integration status

## 6. 📊 Enhanced Monitoring (2025 New)
- `GET /devices/{serial}/memory/history` - Device memory utilization history
- `GET /devices/{serial}/wireless/cpuPowerMode/history` - CPU power mode history
- `GET /devices/{serial}/wireless/cpuLoad` - Wireless CPU load monitoring
- `GET /organizations/{org_id}/switch/ports/history` - Org-wide switchport history
- `GET /organizations/{org_id}/devices/migration/status` - Device migration status

## 7. 🔌 Cellular Gateway
- `GET /devices/{serial}/cellular/sims` - Get SIM info (now includes iccid, imsi, msisdn)
- `PUT /devices/{serial}/cellular/sims` - Update SIM settings
- `GET /networks/{network_id}/cellularGateway/uplink` - Cellular uplink settings

## 8. 🛡️ Enhanced Security Features
- `GET /networks/{network_id}/appliance/dns` - Local/Split DNS profiles
- `PUT /networks/{network_id}/appliance/dns` - Update DNS settings
- `GET /networks/{network_id}/appliance/trafficShaping/uplinkSelection` - Updated WAN selection

## 9. 🏭 MAC Table Live Tools (2025 New)
- `POST /devices/{serial}/liveTools/macTable` - Request MAC table from device
- `GET /devices/{serial}/liveTools/macTable/{id}` - Get MAC table job status

## 10. 📈 API Analytics
- API Analytics Dashboard endpoints (for monitoring API usage)

## 11. 🔧 Configuration Changes
- `GET /organizations/{org_id}/configurationChanges` - Audit log of changes

## 12. 🎯 Early Access/BETA Features
- Various endpoints marked as BETA in the API index

## Summary Statistics:
- **Current Implementation**: 55 tools across 9 categories
- **Missing Categories**: ~12 major categories
- **Estimated Missing Endpoints**: 100-150 additional endpoints
- **2025 New Features**: OAuth 2.0, MAC Tables, Enhanced Monitoring, API Analytics

## Priority Recommendations:
1. **High Priority**: Systems Manager (MDM capabilities)
2. **High Priority**: Licensing Management
3. **Medium Priority**: Policy Objects for advanced security
4. **Medium Priority**: Enhanced Monitoring features
5. **Low Priority**: Spaces integration, BETA features

## Notes:
- Many endpoints require specific licenses (SM, Advanced Security)
- OAuth 2.0 is now available as an alternative to API keys
- Rate limits remain at 10 calls/second per organization
- New sustained rate limits for MAC table requests (1 req/5 sec per device)