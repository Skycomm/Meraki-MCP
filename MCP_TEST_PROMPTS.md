# MCP Test Prompts for Parameter Validation

## How to Test
Run these prompts through the Meraki MCP in Claude Desktop to verify the parameter improvements are working correctly.

## Test Prompts & Expected Results

### 1. Organization List Test
**Prompt:** "List all Meraki organizations I have access to"

**Expected:**
- Should return list of organizations
- Should show Skycomm organization (ID: 686470)
- Validates: Basic connectivity

---

### 2. Network List Test  
**Prompt:** "Show all networks in Skycomm organization"

**Expected:**
- Should list 9 networks including Reserve St
- Should retrieve all networks without pagination issues
- Validates: Basic list operations

---

### 3. Network Events Test (perPage=1000)
**Prompt:** "Get the last 50 network events for Reserve St network in Skycomm"

**Expected:**
- Should return events (may be empty if no recent events)
- Should NOT show "limited to 20 results" or similar
- Internally uses perPage=1000 even though we only display 50
- Validates: get_network_events uses perPage=1000

---

### 4. Client List Test (perPage=1000)
**Prompt:** "List all clients currently connected to Reserve St network, show me both wired and wireless"

**Expected:**
- Should return complete client list
- Should show total count of clients
- Should NOT have pagination warnings
- Validates: get_network_clients uses perPage=1000

---

### 5. Security Events Test (perPage + timespan)
**Prompt:** "Show me security events for Reserve St network"

**Expected:**
- Should return security events for 31 days by default
- Should NOT be limited to 100 events
- Should mention timeframe (31 days)
- Validates: get_network_appliance_security_events uses perPage=1000 and timespan=2678400

---

### 6. Wireless Clients Test
**Prompt:** "List all wireless clients in Reserve St network"

**Expected:**
- Should return all wireless clients
- Should show MAC, IP, SSID for each client
- Should NOT have "showing first 20" type limitations
- Validates: get_network_wireless_clients uses perPage=1000

---

### 7. Alert History Test
**Prompt:** "Get network alert history for Reserve St"

**Expected:**
- Should return alert history
- Should retrieve all alerts, not limited to 100
- Validates: get_network_alerts_history uses perPage=1000 (was 100)

---

### 8. SSID Isolation Test
**Prompt:** "Show me the SSID configuration for Reserve St network, especially the isolation settings"

**Expected:**
- Should list all SSIDs with their configurations
- Should show LAN Isolation status with 🔒 or 🔓 icons
- Should display "LAN Isolation: 🔒 Enabled" or "🔓 Disabled"
- Validates: SSID functions properly handle lanIsolationEnabled

---

### 9. Device Availability Test
**Prompt:** "Check device availability status for all devices in Skycomm organization"

**Expected:**
- Should return availability for all devices
- Should NOT be limited by pagination
- Validates: get_organization_devices_availabilities uses perPage=1000

---

### 10. Comprehensive Network Audit
**Prompt:** "Do a comprehensive audit of Reserve St network in Skycomm - show me events, clients, security events, and wireless configuration"

**Expected:**
- Should retrieve complete data for all categories
- Events should use perPage=1000
- Clients should show all connected devices
- Security events should cover 31 days
- No "limited results" warnings
- Validates: All APIs working together with correct parameters

---

## Success Criteria

✅ **PASS** if:
- No "limited to X results" messages (except where we intentionally limit display)
- Security events show 31-day timeframe
- Client lists are complete
- SSID details show isolation status
- No pagination warnings

❌ **FAIL** if:
- See "showing only 20 events" or similar
- Security events limited to short timeframe
- Client lists appear truncated
- Missing isolation status in SSID details
- Pagination errors or warnings

## Validation Summary

After running all prompts, you should see:
1. Complete data retrieval (no artificial limits)
2. Security events covering 31 days
3. SSID isolation properly displayed
4. All lists using maximum pagination (1000 items)
5. No performance issues from multiple API calls

## Note
These are read-only operations and safe to run on production networks.