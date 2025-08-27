# Cisco Meraki MCP Server - Claude Context & Rules

## ⚠️ CRITICAL SAFETY WARNING ⚠️

**REAL INCIDENT**: During testing, 2 production networks were accidentally DELETED. This server provides REAL access to PRODUCTION infrastructure. Every command executes against LIVE systems.

## Project Overview

This is the STDIO implementation of the Cisco Meraki MCP Server, providing natural language access to 400+ Meraki Dashboard API functions through Claude Desktop.

**Key Facts:**
- 859 tools with 100% Meraki API v1.61.0 coverage
- 51 tool modules covering all Meraki product lines (MX, MS, MR, MV, MG, SM)
- Designed for local Claude Desktop integration (not network/SSE transport)
- Enhanced for seamless Claude Desktop usage (auto-pagination, smart defaults)
- Production-ready with extensive safety features BECAUSE OF PAST INCIDENTS

## 🔴 CRITICAL SAFETY RULES - READ FIRST!

### 1. **NEVER DELETE WITHOUT TRIPLE-CHECKING**
- **PRODUCTION NETWORKS HAVE BEEN ACCIDENTALLY DELETED BEFORE**
- Delete operations now require:
  1. User sees what will be deleted
  2. User must type "DELETE" in UPPERCASE
  3. 3-second countdown before execution
  4. For org deletion - SECOND confirmation required
- **ALWAYS verify network name and ID before ANY delete operation**
- **NEVER test delete operations on production**

### 2. **DEFAULT TO READ-ONLY MODE**
```bash
# SET THIS IMMEDIATELY when working with production:
export MCP_READ_ONLY_MODE=true
```
- This blocks ALL write operations
- Only disable when you're 100% sure of changes
- Re-enable immediately after making changes

### 3. **VERIFY ORGANIZATION/NETWORK BEFORE ANY OPERATION**
Before ANY change:
1. Run `list_organizations()` - CHECK you're in the right org
2. Run `get_organization_networks(org_id)` - VERIFY the network name
3. Look for "Test", "Lab", "Demo" in names for safe testing
4. NEVER assume - production networks can have similar names

### 4. **High-Risk Operations That Have Caused Issues**
- `delete_network()` - **DELETED PRODUCTION NETWORKS**
- `delete_organization()` - Can delete entire company infrastructure
- `update_network()` with wrong params - Can break connectivity
- `factory_reset_device()` - Wipes configuration
- Bulk operations - Can affect multiple sites at once

### 5. **Tool Name Length Limit**
- MCP tools MUST have names ≤ 64 characters
- Already fixed but watch for new tools

## Common Tasks & Best Practices

### Network Health Check
Start with the monitoring dashboard:
```
get_network_health_summary(network_id)
```
This shows:
- Infrastructure devices with accurate status (online, offline, dormant)
- Connected client devices (computers, phones, tablets) - actual users
- Overall health score
- Device type breakdown (Firewall, Switch, AP, Camera, etc.)

**Note**: "Dormant" devices are not reporting to cloud but may still be operational and passing traffic.

### Finding Things
1. **Find an organization**: `list_organizations()`
2. **Find networks in org**: `get_organization_networks(org_id)`
3. **Find devices**: `get_network_devices(network_id)`
4. **Find clients**: `get_network_clients(network_id)`

### Troubleshooting Patterns
1. **"Internet is down"**: 
   - Check uplinks: `get_organization_appliance_uplink_statuses()`
   - Test connectivity: `create_device_ping_test()`
   - Check packet loss: `get_organization_devices_uplinks_loss_and_latency()`

2. **"WiFi not working"**:
   - Check SSIDs: `get_network_wireless_ssids()`
   - Check connection stats: `get_network_connection_stats()`
   - Get password: `get_network_wireless_passwords()`

3. **"Can't find device"**:
   - Search MAC table: `create_switch_mac_table()`
   - Blink LEDs: `blink_device_leds()`

## Code Organization

### Tool Modules (server/tools_*.py)
- `tools_networks.py` - Core network operations
- `tools_devices.py` - Device management
- `tools_wireless.py` - WiFi/SSID management
- `tools_switch.py` - Switch port operations
- `tools_appliance.py` - MX firewall/security
- `tools_monitoring_dashboard.py` - Health monitoring
- `tools_troubleshooting.py` - Diagnostic tools
- `tools_live.py` - Real-time operations (ping, cable test)

### Key Files
- `meraki_client.py` - API client wrapper
- `server/main.py` - MCP server setup
- `config.py` - Configuration (timeouts, retries)

## API Patterns

### Pagination
Many APIs paginate. Tools handle this automatically but be aware of limits:
- Default: 1000 items max
- Use `perPage` and pagination for large datasets

### Timespan Parameters
- Specified in seconds
- Common values: 300 (5 min), 3600 (1 hr), 86400 (24 hr), 604800 (7 days)
- Max varies by API (check docs)

### Error Handling
All tools wrap exceptions and return user-friendly messages:
```python
try:
    result = meraki_client.api_call()
except Exception as e:
    return f"Failed to perform operation: {str(e)}"
```

## Safe Testing Practices

### ⚠️ Testing Caused The Production Deletion Incident!

### BEFORE Testing ANYTHING:
1. **SET READ-ONLY MODE FIRST**
   ```bash
   export MCP_READ_ONLY_MODE=true
   ```
2. **Create a dedicated test network**
   - Name it clearly: "TEST-DELETEME-[date]"
   - Use a separate test organization if possible
   - NEVER use production-looking names

### Safe Test Progression:
1. **Read operations first** - List, get, view operations
2. **Non-destructive updates** - Change descriptions, names (on TEST only)
3. **Destructive operations** - ONLY on clearly marked test networks
4. **NEVER test delete operations without:**
   - Verifying you're in test network 3 times
   - Having someone else verify
   - Taking screenshot of network ID/name

### Before ANY Code Changes:
1. Run syntax check: `python -m py_compile server/tools_*.py`
2. Test specific tool: `python test_server_direct.py`
3. Run comprehensive suite: `python comprehensive_mcp_test_suite.py`

### Test Data Guidelines:
- Test org: Create separate "TEST-ONLY" organization
- Test networks: Must contain "TEST", "LAB", or "DEMO" 
- Production keywords to AVOID: "PROD", "MAIN", "PRIMARY", site names
- NEVER test destructive operations on anything without "TEST" in name

## Common Issues & Solutions

### "Tool not found"
- Check tool name length (≤ 64 chars)
- Ensure tool is registered in module's register function

### "API timeout"
- Default timeout is 600s (10 min)
- Some operations legitimately take time
- Check `config.py` for timeout settings

### "No data returned"
- Check if network has that product type (e.g., wireless APIs need MR devices)
- Verify timespan is appropriate
- Some APIs return empty arrays legitimately

## Branch Information
- **stdio** (current): Local Claude Desktop integration
- **sse**: HTTP/SSE server for network access
- **main**: Stable release branch

## When Modifying Code

### Adding New Tools
1. Keep names under 64 characters
2. Add to appropriate tools_*.py file
3. Include docstring with description
4. Handle errors gracefully
5. Test with `test_server_direct.py`

### Updating Existing Tools
1. Check if used in production workflows
2. Maintain backward compatibility
3. Update tests if behavior changes
4. Document changes in commit message

## Production Considerations

### High-Risk Operations
- Organization deletion/creation
- Network deletion
- Device factory reset
- Firmware upgrades
- License changes

### Safe for Regular Use
- All read operations
- Status checks
- Monitoring queries
- Report generation
- Search operations

### Performance Impact
Be cautious with:
- Org-wide queries on large organizations
- Historical data with long timespans
- Frequent polling (respect rate limits)

## Best Practices

1. **Start broad, then narrow**: Organization → Network → Device → Port/Client
2. **Use monitoring tools first**: Get overall health before diving deep
3. **Check prerequisites**: Ensure devices exist before querying device-specific APIs
4. **Cache org/network IDs**: Reuse IDs instead of repeated lookups
5. **Respect rate limits**: 5 calls/second per org (this client handles automatically)

## Need Help?

1. Check `docs/TECH_SUPPORT_PROMPTS.md` for common scenarios
2. Review `docs/DAILY_OPERATIONS_GUIDE.md` for routine tasks
3. See `docs/QUICK_REFERENCE_CARD.md` for command examples
4. Read API docs at https://developer.cisco.com/meraki/api-v1/

## Pre-Flight Checklist (EVERY Session)

Before starting ANY work:
- [ ] Set `export MCP_READ_ONLY_MODE=true`
- [ ] Run `list_organizations()` - note which org you're in
- [ ] Identify production vs test networks
- [ ] If making changes, have the change request/ticket number
- [ ] If testing, create NEW test network with "TEST" in name

Before ANY write operation:
- [ ] Am I in the correct organization? (check twice)
- [ ] Am I targeting the correct network? (verify name AND ID)
- [ ] Is this a test or production network? (must be 100% sure)
- [ ] Do I have approval for this change?
- [ ] Have I tested this in a lab first?

## Remember - This Has Real Consequences

- **This server gives you powerful access to network infrastructure**
- **Real networks serving real users have been deleted by accident**
- **There is NO undo for delete operations**
- **Always verify you're in the right org/network before changes**
- **When in doubt, use read-only mode**
- **Test in lab networks first**
- **Infrastructure devices ≠ client devices (common confusion)**

## The Golden Rule

**If you're not 100% certain, STOP and verify. It's better to be slow and safe than fast and sorry. Production networks deleted = businesses offline = people can't work.**

## 🎯 100% API Coverage Achievement

As of the latest update, this MCP server has achieved **100% coverage** of the Meraki Dashboard API v1.61:
- **79 modules** containing **1,337 functions**
- **Every official Meraki API endpoint** is implemented
- All tool names are ≤ 64 characters (MCP requirement)
- Includes 14 auto-generated modules for complete coverage

### Important Files for Maintenance:
- `generate_missing_endpoints.py` - Auto-generates missing API endpoints
- `fix_long_names.py` - Fixes tool names exceeding 64 characters
- `100_PERCENT_COVERAGE_SUMMARY.md` - Complete achievement documentation
- `API_COMPARISON_GUIDE.md` - How to track API updates

### To Maintain 100% Coverage:
1. Run `compare_api_coverage()` monthly to check for new APIs
2. Use `generate_missing_endpoints.py` to add any new endpoints
3. Run `fix_long_names.py` if you encounter name length errors
4. Check Cisco's API changelog regularly

### Module Organization:
- **Original modules** (51): Core functionality, well-tested
- **Reorganized modules** (7): Extracted from tools_networks.py for better organization
- **Missing API modules** (7): High-priority APIs that were missing
- **Additional modules** (14): Auto-generated for 100% coverage
- **Utility modules** (2): Custom tools and API comparison

### Recent Enhancements (Latest):
- **get_network_events**: Auto-tries all product types when none specified
- **Device Type Identification**: Correctly identifies MX, MS, MR, MV, MG devices
- **Network Health Summary**: Shows accurate device statuses (was showing 0 online)
- **WAN Packet Loss**: Comprehensive status tool shows packet loss on uplinks
- **Maximum Pagination**: All tools use perPage=1000 for complete results

### Known Issues:
- Some duplicate tool warnings on startup (harmless, from MQTT/SNMP/Syslog overlaps)
- Large number of modules may slow initial load slightly
- Auto-generated modules use generic response formatting

### Testing Coverage:
To verify 100% coverage:
```bash
# This will show any missing endpoints (should be 0)
python -c "from generate_missing_endpoints import find_missing_endpoints; print(f'Missing: {sum(len(m) for m in find_missing_endpoints().values())}')"
```

## Testing & Validation Guide

### Running Direct API Tests (Without MCP)
When testing API functionality or debugging issues:

```python
# Direct API testing template
.venv/bin/python -c "
from meraki_client import MerakiClient

meraki = MerakiClient()
network_id = 'L_726205439913500692'  # Replace with your network
org_id = '686470'  # Replace with your org

# Test API calls directly
result = meraki.dashboard.networks.getNetwork(network_id)
print(f'Network: {result.get(\"name\")}')
"
```

### Common Test Scenarios

#### 1. Pagination Testing
Check if APIs are returning maximum data:
```python
# Test pagination (should get up to 1000 items)
events = meraki.dashboard.networks.getNetworkEvents(
    network_id, 
    productType='appliance',
    perPage=1000
)
print(f'Events retrieved: {len(events.get(\"events\", []))}')
# If only 20-100, pagination may not be working
```

#### 2. VLAN Configuration Testing
Test SSID VLAN assignments (Bridge mode uses `defaultVlanId`):
```python
ssids = meraki.dashboard.wireless.getNetworkWirelessSsids(network_id)
for ssid in ssids:
    if ssid.get('enabled'):
        vlan = ssid.get('defaultVlanId') or ssid.get('vlanId')
        print(f"SSID {ssid['name']}: VLAN {vlan}")
```

#### 3. Device Status Testing
Check if all devices report correct status:
```python
statuses = meraki.dashboard.organizations.getOrganizationDevicesStatuses(
    organizationId=org_id,
    networkIds=[network_id]
)
for device in statuses:
    print(f"{device.get('name')}: {device.get('status')}")
```

#### 4. Switch Port VLAN Testing
Test port VLAN behavior when enabling/disabling:
```python
# Update port with explicit VLAN (prevents VLAN 1 reversion)
result = meraki.dashboard.switch.updateDeviceSwitchPort(
    serial='Q2HP-GCZQ-7AWT',
    portId='5',
    enabled=False,
    vlan=101  # ALWAYS specify VLAN even when disabling
)
```

### Best Practices for Testing

#### Switch Port VLAN Management
- Always specify VLAN when updating ports, even when disabling
- Use VLAN 1 (192.168.128.0/24) or another valid VLAN for disabled ports
- This prevents VLAN mismatch alerts

#### SSID VLAN Verification
- Bridge mode SSIDs store VLAN in `defaultVlanId` field
- NAT mode SSIDs don't use VLAN tagging
- Check both fields when verifying configuration

#### Firmware Upgrades
For scheduling firmware upgrades, use this format:
```python
update_network_firmware_upgrades(
    network_id=network_id,
    upgradeWindow={'dayOfWeek': 'sun', 'hourOfDay': '03:00'},
    products={
        'wireless': {
            'nextUpgrade': {
                'time': '2025-08-31T03:00:00Z',
                'toVersion': {'shortName': 'wireless-31-1-8'}
            }
        }
    }
)
```

### Comprehensive Network Audit Script
Run a full audit to check for common issues:
```bash
python -c "
from meraki_client import MerakiClient
meraki = MerakiClient()

# Get network
network_id = 'YOUR_NETWORK_ID'

# 1. Check device statuses
devices = meraki.dashboard.networks.getNetworkDevices(network_id)
print(f'Devices: {len(devices)}')

# 2. Check VLAN configuration
vlans = meraki.dashboard.appliance.getNetworkApplianceVlans(network_id)
print(f'VLANs configured: {len(vlans)}')

# 3. Check SSIDs
ssids = meraki.dashboard.wireless.getNetworkWirelessSsids(network_id)
enabled = sum(1 for s in ssids if s.get('enabled'))
print(f'SSIDs enabled: {enabled}/15')

# 4. Check clients
clients = meraki.dashboard.networks.getNetworkClients(network_id, perPage=1000)
print(f'Active clients: {len(clients)}')
"
```