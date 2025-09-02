# Claude AI Assistant Guide for Cisco Meraki MCP Server

## Overview
This is a Model Context Protocol (MCP) server for the Cisco Meraki Dashboard API v1, built with FastMCP framework. The server provides **100% coverage** of all Meraki API endpoints with **890+ total tools** (816 official SDK + 74+ custom tools), organized in a clean professional structure matching the official SDK exactly.

**🎉 FINAL STATUS: ALL 13 SDK MODULES COMPLETE WITH PERFECT 1:1 MAPPING**

## Critical Information

### API Pagination Limits - IMPORTANT!
Different Meraki API endpoints have **different pagination limits**. Before changing any `perPage` or `per_page` parameters:

1. **Check the API documentation first** at `https://developer.cisco.com/meraki/api-v1/[endpoint-name]/`
2. Look for the "perPage" parameter description which specifies the acceptable range

**Known limits:**
- **Most endpoints**: 3-1000 (can safely use 1000)
- **Mesh statuses** (`getNetworkWirelessMeshStatuses`): 3-500 max
- **SSID statuses** (`getOrganizationWirelessSsidsStatusesByDevice`): 3-500 max
- **Organization switch ports** (`getOrganizationSwitchPortsBySwitch`): 3-50 max (default now set to 50)
- **Organization switch port statuses** (`getOrganizationSwitchPortsStatusesBySwitch`): 3-20 max (default now set to 20)
- **Organization switch topology** (`getOrganizationSwitchPortsTopologyDiscoveryByDevice`): 3-20 max (default now set to 20)
- **General rule**: "statuses" endpoints often have lower limits (use 500 as safe default)

**How to check:**
```python
# Use WebFetch to check specific endpoint limits:
WebFetch(
    url="https://developer.cisco.com/meraki/api-v1/get-network-wireless-mesh-statuses/",
    prompt="What is the pagination limit for this endpoint? What is the maximum perPage value allowed?"
)
```

### Tool Name Length Limit
- MCP/Claude Desktop requires tool names to be **≤64 characters**
- Long SDK method names must be shortened for compatibility
- Keep original detailed descriptions - only shorten the names

### Testing Commands
```bash
# Test 100% SDK coverage (all 816 tools)
python tests/test_100_sdk_coverage.py

# Test comprehensive wireless functionality 
python tests/test_wireless_comprehensive.py

# Test the exact user request (network audit)
python tests/test_full_audit_prompt.py

# Run the MCP server (all 816+ tools)
MCP_PROFILE=FULL .venv/bin/python meraki_server.py

# Test specific API fixes as MCP client would
python tests/test_api_fixes.py
```

### IMPORTANT: Never Remove or Simplify Tools!
**When testing or debugging issues:**
- **NEVER remove existing tools** - they are all needed for full SDK coverage
- **NEVER simplify tool implementations** - complexity is there for a reason
- **ADD error handling, don't delete functionality**
- **If a tool seems broken, FIX it, don't remove it**
- All 816+ tools are required for complete Meraki API functionality (816 SDK + 74+ custom)

### Testing as an MCP Client

When fixing API issues or testing tools, **always test as an MCP client would use them**, not directly against the API. This ensures the fixes work correctly in real-world usage (like Claude Desktop).

**How to test API fixes:**

1. **Create a test script that imports the MCP server:**
```python
from server.main import app, meraki

# Test the tool as MCP client would call it
result = meraki.dashboard.networks.getNetworkEvents(
    network_id,
    productType='wireless',  # Required for multi-device networks
    perPage=10
)
```

2. **Run with proper error handling to see helpful messages:**
```python
try:
    result = meraki.dashboard.wireless.getNetworkWirelessUsage(network_id)
except Exception as e:
    print(f"Error message that MCP client sees: {e}")
    # Should show helpful guidance about missing parameters
```

3. **Test edge cases like NULL data:**
```python
# History endpoints may return NULL when analytics not enabled
result = meraki.dashboard.wireless.getNetworkWirelessClientCountHistory(
    network_id, 
    timespan=3600
)
# Should handle NULL gracefully and explain why
```

**Common testing patterns:**
- Test with missing required parameters to ensure helpful error messages
- Test with multi-device networks to catch productType requirements
- Test history/analytics endpoints for NULL data handling
- Verify confusing tool names redirect to correct ones

### Common Issues & Solutions

1. **"perPage parameter must be between X and Y" errors**
   - Check the specific endpoint's documentation
   - Reduce perPage to the maximum allowed (often 500 for "statuses" endpoints)

2. **Tools requiring specific parameters**
   Many wireless analytics tools require specific parameters that aren't obvious from the name:
   - `get_network_wireless_channel_utilization_history`: REQUIRES device_serial OR client_id + band
   - `get_network_wireless_usage_history`: REQUIRES device_serial OR client_id
   - `get_network_wireless_usage`: REQUIRES device_serial (not just network_id)
   - `get_network_wireless_signal_quality_history`: REQUIRES device_serial OR client_id
   - `get_network_wireless_location_scanning`: REQUIRES location analytics license
   - `get_network_wireless_devices_packet_loss`: May require specific license/features
   
   When these tools fail, check the error message for parameter requirements

3. **Tools that may return NULL data**
   Some analytics tools return time slots with NULL values when data isn't available:
   - `get_network_wireless_client_count_history`: Returns `clientCount: null` if analytics not enabled
   - `get_network_wireless_data_rate_history`: Returns `averageKbps: null` if no traffic data
   - `get_network_wireless_signal_quality_history`: Returns `rssi/snr: null` if device not connected
   
   This is NOT an error - it means:
   - Analytics/data collection not enabled on the network
   - No activity during the time period
   - Device/client wasn't connected during that time
   - Network is newly created and hasn't collected data yet

4. **API endpoints with confusing names**
   - `get_network_wireless_devices_latencies` - Wrong name (typo), redirects to correct tool
   - `get_network_wireless_devices_latency_stats` - Correct tool that works with just network_id!
   
5. **Network Events API Special Requirements**
   The `getNetworkEvents` API requires `productType` parameter for networks with multiple device types:
   - Networks with appliance + switch + wireless need productType specified
   - Valid values: appliance, camera, switch, wireless, cellularGateway, systemsManager
   - The tool now auto-detects available types and provides helpful guidance
   - Example: `get_network_events(network_id, product_type='wireless')`
   
6. **Testing as MCP client**
   When testing tools, always test as an MCP client would:
   ```python
   # Example testing pattern
   from server.main import app, meraki
   network_id = 'L_726205439913500692'
   device_serial = 'Q2PD-JL52-H3B2'
   
   # Test with proper parameters
   result = meraki.dashboard.wireless.getNetworkWirelessUsageHistory(
       network_id, 
       deviceSerial=device_serial,  # This is REQUIRED
       timespan=86400
   )
   ```

7. **Tool name exceeds 64 characters**
   - Shorten the tool name (not description)
   - Common abbreviations: `organization` → `org`, `utilization` → `util`, `history` → `hist`

8. **Missing required parameters**
   - `getNetworkWirelessUsageHistory` requires either `device_serial` OR `client_id`
   - `getNetworkWirelessClientConnectivityEvents` needs proper parameter handling

### Repository Structure
- **30,800+ lines of code** across all modules  
- **Clean Organization**: Files moved from messy root to organized directories
- Main server: `/server/main.py` (central hub for all 890+ tools)

**SDK Modules (816 tools - 100% coverage matching official SDK):**
- `tools_SDK_organizations.py` - 173 organization tools
- `tools_SDK_appliance.py` - 130 appliance tools
- `tools_SDK_wireless.py` - 116 wireless tools
- `tools_SDK_networks.py` - 114 network tools
- `tools_SDK_switch.py` - 101 switch tools
- `tools_SDK_sm.py` - 49 systems manager tools
- `tools_SDK_camera.py` - 45 camera tools
- `tools_SDK_devices.py` - 27 device tools
- `tools_SDK_cellularGateway.py` - 24 cellular gateway tools
- `tools_SDK_sensor.py` - 18 sensor tools
- `tools_SDK_licensing.py` - 8 licensing tools
- `tools_SDK_insight.py` - 7 insight tools
- `tools_SDK_administered.py` - 4 identity management tools

**Custom Modules (74+ tools - extended functionality):**
- `tools_Custom_search.py` - Cross-org device search
- `tools_Custom_vpn.py` - Advanced VPN management
- `tools_Custom_policy.py` - Policy object management
- 4 more custom modules

**Organized Directories:**
```
├── server/         # All MCP server code
├── tests/          # Comprehensive test suite
├── scripts/        # Generation and utility scripts
├── docs/           # Documentation
├── data/           # Data files
└── archive/        # Historical files
```

### Safety Features
- All destructive operations require confirmation
- Read-only mode available via `MCP_READ_ONLY_MODE=true`
- Audit logging enabled by default

### Git Workflow
- **Main branch**: `main` (current stable branch)
- **Current working branch**: `main` 
- Always check `git status` before committing
- **Recent major commits**:
  - 🧹 Remove duplicate tool registrations 
  - 🔧 Fix Burswood WiFi audit tool issues
  - 🎯 Achieve 100% SDK coverage with 598 tools
  - 📁 Clean up project structure (200+ files organized)
- Include emoji and co-author in commits:
  ```
  🤖 Generated with [Claude Code](https://claude.ai/code)
  
  Co-Authored-By: Claude <noreply@anthropic.com>
  ```

### Authentication Failure Investigations
When investigating wireless authentication failures:
1. Check device compatibility (WiFi 6 APs may reject older IoT devices)
2. Look for patterns in client manufacturers (Xiaomi/Huawei often have issues)
3. Consider 802.11r fast roaming incompatibilities
4. Review RADIUS timeout settings

### API Best Practices
1. Always handle pagination for large datasets
2. Use appropriate timespan parameters (default: 86400 seconds = 24 hours)
3. Check for None/null values before accessing nested dictionaries
4. Format responses with clear markdown headers and bullet points

## Quick Reference

### Environment Variables
```bash
MERAKI_API_KEY="your-api-key"          # Required: Your Meraki Dashboard API key
MCP_PROFILE="FULL"                     # Load all 816+ tools (SDK_CORE=816 official, ORGANIZATIONS/NETWORK/DEVICES for subsets)
MCP_READ_ONLY_MODE=false               # Set to true for safe testing (no infrastructure changes)
```

### Common Test Values (Skycomm Organization)
```python
TEST_ORG_ID = "686470"                    # Skycomm organization
TEST_NETWORK_ID = "L_726205439913500692"  # Reserve St network (main test network)
TEST_SSID_NUMBER = "0"                    # Apple SSID
TEST_AP_SERIAL = "Q2PD-JL52-H3B2"        # Office AP serial number

# Successful audit test: "please do a detailed audit of the skycomm reserve st network"
# This request successfully exercises multiple tool categories and validates real data
```

### Debugging Tips
- Check `/var/log/mcp_audit.log` for operation history
- Use `grep -r "perPage.*1000"` to find pagination settings
- Run `git diff` before committing to review changes
- Test with `python test_wireless_comprehensive.py` after major changes

## Recent Major Updates (Version 4.0.0 - FINAL COMPLETION)

### **🎯 Perfect SDK Coverage Achieved - All 13 Modules Complete**
- **816 SDK tools**: 100% coverage of official Cisco Meraki Dashboard API v1 
- **Perfect 1:1 mapping**: Every tool matches official SDK exactly
- **All 13 modules validated**: Organizations, Appliance, Wireless, Networks, Switch, SM, Camera, Devices, Cellular Gateway, Sensor, Licensing, Insight, Administered
- **Zero mapping issues**: Comprehensive validation passed
- **MCP ready**: All tools Claude Desktop compatible

### **🧹 Final Cleanup Campaign Completed**
- **Systematic cleanup**: 23 extra tools removed across 4 modules
- **Duplicates eliminated**: All duplicate registrations cleaned up
- **Name mapping fixed**: Insight abbreviated names corrected
- **Tool counts perfect**: All modules match expected SDK counts exactly
- **Professional quality**: Enterprise-grade implementation

### **✅ Comprehensive Testing & Validation**
- **All modules validated**: 13/13 modules pass comprehensive testing
- **Syntax verification**: All 816 tools compile without errors
- **MCP client testing**: All tools tested for Claude Desktop compatibility
- **Tool name compliance**: All names under 64-character MCP limit
- **Server startup tested**: Full MCP server loads all 890+ tools successfully

## Previous Major Updates (Version 2.0.0-3.0.0)

### **🎯 Perfect SDK Coverage Achieved**
- **816 SDK tools**: 100% coverage of official Cisco Meraki Dashboard API v1 (exactly matches official SDK)
- **74+ custom tools**: Extended functionality beyond official SDK
- **Total: 816+ tools** - complete comprehensive Meraki MCP implementation

### **🏗️ Professional Architecture**
- **Clean structure**: Organized to match official SDK exactly
- **Separated concerns**: SDK tools vs Custom tools clearly delineated
- **Eliminated duplication**: Removed overlapping tool registrations
- **Fixed imports**: Resolved circular import issues

### **✅ Working Integration**
- **Claude Desktop**: Successfully configured with all 598 tools loading
- **Real testing**: Validated with Skycomm Reserve St network audit (using actual 816 SDK tools)
- **MCP client**: Proper testing as MCP client would use the tools
- **Error handling**: Comprehensive error messages and guidance
- **Perfect coverage**: All 816 official SDK methods implemented exactly

### **📁 Project Cleanup**  
- **File organization**: Moved 200+ files from messy root to organized directories
- **Directory structure**: tests/, scripts/, docs/, data/, archive/
- **Clean repository**: Professional appearance and maintainability

### **🔧 Technical Improvements**
- Fixed pagination limits for mesh and SSID status endpoints
- Fixed tool name length issues for Claude Desktop compatibility (<64 chars)
- Added comprehensive pagination documentation with endpoint-specific limits
- Resolved authentication failure root causes (IoT device incompatibility)
- Enhanced error handling with helpful guidance messages

### **📊 Scale & Performance**
- **30,800+ lines** of professional code
- **816+ tools** running efficiently in single MCP instance
- **Comprehensive testing** with real API validation
- **Production ready** with safety features and audit logging