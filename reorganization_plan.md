# PROPOSED WIRELESS TOOLS REORGANIZATION

## Current Problems:
- Files named "complete", "final", "100", "missing" are confusing
- Tools are scattered across files without clear logic
- Duplicates exist (device_type_policies in 2 files, etc.)

## Proposed Consolidation:

### 1. tools_wireless_ssids.py (Keep existing tools_wireless.py)
- Basic SSID CRUD operations
- SSID configuration
- Client management
- Usage statistics

### 2. tools_wireless_ssid_features.py (Merge from complete/final/100)
- Hotspot 2.0 settings
- Splash page configuration
- SSID schedules
- VPN settings
- Bonjour forwarding
- EAP override
- Device type group policies
- Identity PSKs (all CRUD operations)

### 3. tools_wireless_security.py (Keep existing firewall + add Air Marshal)
- L3 firewall rules
- L7 firewall rules
- Traffic shaping
- Air Marshal rules and settings
- Firewall isolation allowlist

### 4. tools_wireless_rf.py (Keep existing rf_profiles)
- RF profiles (CRUD)
- Radio settings
- Channel utilization
- Mesh status

### 5. tools_wireless_analytics.py (Merge from advanced)
- Connection stats
- Latency stats/history
- Failed connections
- Client health scores
- Usage history
- Data rate history
- Signal quality history

### 6. tools_wireless_infrastructure.py (New consolidation)
- Bluetooth settings (network & device)
- Electronic shelf labels
- Ethernet ports profiles
- Alternate management interface
- Location scanning
- Billing

### 7. tools_wireless_organization.py (Merge from final/missing)
- Organization-wide analytics
- Packet loss by client/device/network
- Channel utilization by device/network
- Power mode history
- CPU load history
- RADSEC certificates
- Wireless controllers

## Benefits:
✅ Clear, logical grouping by functionality
✅ No confusing names
✅ Easier to find tools
✅ Matches SDK organization better
✅ Eliminates duplicates
