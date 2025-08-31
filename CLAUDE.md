# Claude AI Assistant Guide for Cisco Meraki MCP Server

## Overview
This is a Model Context Protocol (MCP) server for the Cisco Meraki Dashboard API v1, built with FastMCP framework. The server provides 100% coverage of all Meraki API endpoints, with special focus on wireless functionality (142 tools covering all 116 SDK methods).

## Critical Information

### API Pagination Limits - IMPORTANT!
Different Meraki API endpoints have **different pagination limits**. Before changing any `perPage` or `per_page` parameters:

1. **Check the API documentation first** at `https://developer.cisco.com/meraki/api-v1/[endpoint-name]/`
2. Look for the "perPage" parameter description which specifies the acceptable range

**Known limits:**
- **Most endpoints**: 3-1000 (can safely use 1000)
- **Mesh statuses** (`getNetworkWirelessMeshStatuses`): 3-500 max
- **SSID statuses** (`getOrganizationWirelessSsidsStatusesByDevice`): 3-500 max
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
# Test wireless comprehensive coverage
python test_all_wireless_comprehensive.py

# Test 100% SDK coverage
python test_100_sdk_coverage.py

# Run the MCP server
.venv/bin/python meraki_server.py

# Test API fixes as MCP client would
python test_api_fixes.py
```

### IMPORTANT: Never Remove or Simplify Tools!
**When testing or debugging issues:**
- **NEVER remove existing tools** - they are all needed for full SDK coverage
- **NEVER simplify tool implementations** - complexity is there for a reason
- **ADD error handling, don't delete functionality**
- **If a tool seems broken, FIX it, don't remove it**
- All 500+ tools are required for complete Meraki API functionality

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
- Main server: `/server/main.py`
- Wireless tools split across multiple files:
  - `tools_wireless.py` - Core wireless functions
  - `tools_wireless_advanced.py` - Advanced features (has pagination docs)
  - `tools_wireless_organization.py` - Org-level operations
  - `tools_wireless_infrastructure.py` - AP and infrastructure
  - `tools_wireless_client_analytics.py` - Client analytics
  - `tools_wireless_rf_profiles.py` - RF profiles and radio settings
  - `tools_wireless_ssid_features.py` - SSID configuration

### Safety Features
- All destructive operations require confirmation
- Read-only mode available via `MCP_READ_ONLY_MODE=true`
- Audit logging enabled by default

### Git Workflow
- Main branch: `main`
- Current branch: `sse` or `stdio`
- Always check `git status` before committing
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
MERAKI_API_KEY="your-api-key"
MCP_READ_ONLY_MODE=false  # Set to true for safe testing
```

### Common Test Values
```python
TEST_ORG_ID = "686470"  # Skycomm
TEST_NETWORK_ID = "L_726205439913500692"  # Reserve St
TEST_SSID_NUMBER = "0"  # Apple SSID
TEST_AP_SERIAL = "Q2PD-JL52-H3B2"  # Office AP
```

### Debugging Tips
- Check `/var/log/mcp_audit.log` for operation history
- Use `grep -r "perPage.*1000"` to find pagination settings
- Run `git diff` before committing to review changes
- Test with `python test_wireless_comprehensive.py` after major changes

## Recent Updates (As of Last Session)
- Fixed pagination limits for mesh and SSID status endpoints
- Achieved 100% wireless SDK coverage (142 tools, all 116 methods)
- Fixed tool name length issues for Claude Desktop compatibility
- Added comprehensive pagination documentation
- Resolved authentication failure root causes (IoT device incompatibility)