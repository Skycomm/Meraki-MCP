# MCP Test Round 2 - Advanced Validation Scenarios

## 🔬 Stress & Scale Tests

### Stress Test 1: Maximum Data Retrieval
**Prompt:** "I need EVERYTHING from Reserve St - every single client, all events from today, all alerts, don't miss anything"

**Validation:**
- ✅ PASS if retrieves all data without "showing partial" messages
- ✅ Should use perPage=1000 for each API call
- ❌ FAIL if any data truncation or pagination limits

**Tests:** Multiple APIs with maximum pagination

---

### Stress Test 2: Multi-Site Client Analysis  
**Prompt:** "Count total clients across ALL networks in Skycomm - Attadale, Midland, Murdoch, Burswood, Reserve St, Taiwan, testing - give me exact totals"

**Validation:**
- ✅ Each network query uses perPage=1000
- ✅ Complete counts without estimation
- ✅ Should handle 7+ network queries efficiently
- ❌ FAIL if counts seem artificially low

**Tests:** Batch operations with proper pagination

---

### Stress Test 3: Organization-Wide Device Inventory
**Prompt:** "Generate a complete device inventory for Skycomm - every AP, switch, camera, and firewall with their status"

**Validation:**
- ✅ Returns ALL devices without limits
- ✅ Shows model, serial, status for each
- ❌ FAIL if device list incomplete

**Tests:** getOrganizationDevices with perPage=1000

---

## ⏰ Time-Based Query Tests

### Time Test 1: Specific Time Window
**Prompt:** "Show me security events from Reserve St for exactly the last 48 hours"

**Validation:**
- ✅ Should retrieve 48 hours of data (172800 seconds)
- ✅ Still uses perPage=1000 for results
- ❌ FAIL if defaults to different timespan

**Tests:** Custom timespan with maximum pagination

---

### Time Test 2: Maximum Historical Data
**Prompt:** "Get me the maximum available history of security events for Reserve St network"

**Validation:**
- ✅ Should attempt maximum timespan (365 days for security events)
- ✅ Uses perPage=1000 to get all events
- ❌ FAIL if limited to default 31 days when more requested

**Tests:** Maximum timespan handling

---

### Time Test 3: Recent Activity Check
**Prompt:** "What happened in Reserve St in the last 5 minutes? Show me all events and client activity"

**Validation:**
- ✅ Should query with 300-second timespan
- ✅ Still uses perPage=1000 (even for short timespan)
- ❌ FAIL if misses recent data

**Tests:** Short timespan with proper pagination

---

## 🔍 Search & Filter Tests

### Search Test 1: MAC Address Hunt
**Prompt:** "Find all clients with MAC addresses starting with 'AC:' across the entire Skycomm organization"

**Validation:**
- ✅ Searches through ALL clients (perPage=1000)
- ✅ Checks all networks
- ❌ FAIL if search limited by pagination

**Tests:** Filtered searches with maximum results

---

### Search Test 2: Event Type Filtering
**Prompt:** "Show me only IDS/IPS alerts and blocked connections from Reserve St security events"

**Validation:**
- ✅ Filters events but still uses perPage=1000
- ✅ Covers full timespan (31 days default)
- ❌ FAIL if filtered results truncated

**Tests:** Filtered queries maintain pagination

---

### Search Test 3: VLAN-Specific Clients
**Prompt:** "List all clients on VLAN 10 in Reserve St network"

**Validation:**
- ✅ Returns all matching clients
- ✅ No artificial limits on VLAN filtering
- ❌ FAIL if VLAN filter reduces pagination

**Tests:** Filtered client lists

---

## 🌐 Cross-Network Operations

### Cross Test 1: Wireless Comparison
**Prompt:** "Compare wireless client counts between Reserve St and Taiwan networks - show me detailed numbers"

**Validation:**
- ✅ Both networks use perPage=1000
- ✅ Accurate counts for comparison
- ❌ FAIL if either network has limited data

**Tests:** Multiple network queries with consistent pagination

---

### Cross Test 2: Multi-Network Security Scan
**Prompt:** "Check for security events across Reserve St, Burswood, and Midland networks simultaneously"

**Validation:**
- ✅ Each network: perPage=1000, timespan=2678400
- ✅ Parallel or sequential queries all use max params
- ❌ FAIL if any network has different parameters

**Tests:** Consistent parameters across networks

---

### Cross Test 3: Global SSID Audit
**Prompt:** "Show me ALL SSIDs across every network in Skycomm with their isolation settings"

**Validation:**
- ✅ Every SSID shows isolation status (🔒/🔓)
- ✅ Complete SSID list from all networks
- ❌ FAIL if any isolation status missing

**Tests:** SSID enumeration with lanIsolationEnabled

---

## 🔧 Diagnostic & Troubleshooting Tests

### Diagnostic Test 1: Connection Issues
**Prompt:** "Troubleshoot connectivity - show me failed connections, authentication failures, and DHCP issues in Reserve St"

**Validation:**
- ✅ Retrieves all relevant events (perPage=1000)
- ✅ Covers appropriate timespan
- ❌ FAIL if diagnostic data incomplete

**Tests:** Troubleshooting queries use max pagination

---

### Diagnostic Test 2: Performance Analysis
**Prompt:** "Analyze network performance for Reserve St - show latency stats, packet loss, and bandwidth usage"

**Validation:**
- ✅ Complete performance metrics
- ✅ No sampling/averaging due to pagination
- ❌ FAIL if metrics seem incomplete

**Tests:** Analytics APIs with proper parameters

---

### Diagnostic Test 3: Alert Correlation
**Prompt:** "Correlate all alerts and events for Reserve St from the past 24 hours - I need to see patterns"

**Validation:**
- ✅ Gets ALL events/alerts for correlation
- ✅ 24-hour timespan with perPage=1000
- ❌ FAIL if data too limited for correlation

**Tests:** Correlation requires complete datasets

---

## 🎯 Edge Cases & Boundaries

### Edge Test 1: Empty Network Query
**Prompt:** "Show me all clients and events for the 'test' network (N_726205439913520849)"

**Validation:**
- ✅ Handles empty results gracefully
- ✅ Still uses perPage=1000 internally
- ❌ FAIL if empty results cause errors

**Tests:** Empty result handling

---

### Edge Test 2: Single Device Network
**Prompt:** "Get complete details for a network with only one device"

**Validation:**
- ✅ Pagination parameters still set correctly
- ✅ No optimization that breaks parameters
- ❌ FAIL if single item changes behavior

**Tests:** Small dataset handling

---

### Edge Test 3: Rapid Sequential Queries
**Prompt:** "Quick checks: 1) Count Reserve St clients, 2) Get latest alert, 3) Check SSID status - all within 5 seconds"

**Validation:**
- ✅ Each rapid query uses correct params
- ✅ No parameter shortcuts for speed
- ❌ FAIL if rapid queries skip pagination

**Tests:** Consistent parameters under time pressure

---

## 📊 Aggregation & Summary Tests

### Summary Test 1: Daily Statistics
**Prompt:** "Generate daily statistics for Reserve St - total clients, events, alerts, and security incidents"

**Validation:**
- ✅ Each statistic based on complete data
- ✅ All counts use perPage=1000
- ❌ FAIL if statistics seem underreported

**Tests:** Aggregations use complete datasets

---

### Summary Test 2: Bandwidth Leaders
**Prompt:** "Show me the top 50 bandwidth consumers in Reserve St network with their usage details"

**Validation:**
- ✅ Gets ALL clients first (perPage=1000)
- ✅ Then sorts/filters for top 50
- ❌ FAIL if only queries 50 clients

**Tests:** Top-N queries still retrieve all data

---

## 🧪 Validation Checklist After Running Tests

### Parameters to Verify:
- [ ] All client queries use perPage=1000
- [ ] Security events use perPage=1000 + timespan=2678400 (or custom)
- [ ] Alert history uses perPage=1000 (not old 100)
- [ ] Device queries use perPage=1000
- [ ] Wireless client queries use perPage=1000
- [ ] Event queries try multiple product types with perPage=1000 each
- [ ] SSID queries show lanIsolationEnabled status

### Expected Behaviors:
- [ ] No "showing first X" messages
- [ ] Complete datasets for analysis
- [ ] Proper timespan handling
- [ ] Isolation status visible (🔒/🔓)
- [ ] Empty results handled gracefully
- [ ] Consistent behavior across all networks

### Red Flags (Should NOT See):
- ❌ "Limited to 20 results"
- ❌ "Showing partial data"
- ❌ "First 100 alerts" (should be 1000)
- ❌ Missing isolation information
- ❌ Incomplete client lists
- ❌ Truncated event logs

## 📝 Test Execution Template

```markdown
Round 2 Test Results:

Stress Tests:
- Test 1 (Everything): ✅/❌ 
- Test 2 (Multi-Site): ✅/❌
- Test 3 (Inventory): ✅/❌

Time Tests:
- Test 1 (48 hours): ✅/❌
- Test 2 (Max history): ✅/❌
- Test 3 (5 minutes): ✅/❌

Search Tests:
- Test 1 (MAC search): ✅/❌
- Test 2 (Event filter): ✅/❌
- Test 3 (VLAN filter): ✅/❌

Cross-Network:
- Test 1 (Wireless compare): ✅/❌
- Test 2 (Security scan): ✅/❌
- Test 3 (SSID audit): ✅/❌

Diagnostic:
- Test 1 (Connectivity): ✅/❌
- Test 2 (Performance): ✅/❌
- Test 3 (Correlation): ✅/❌

Edge Cases:
- Test 1 (Empty): ✅/❌
- Test 2 (Single): ✅/❌
- Test 3 (Rapid): ✅/❌

Aggregation:
- Test 1 (Statistics): ✅/❌
- Test 2 (Top 50): ✅/❌

Total: X/20 tests passed
```

## 🎯 Success Metrics

**EXCELLENT:** 20/20 - All parameter improvements working perfectly
**GOOD:** 18-19/20 - Minor issues, non-critical
**NEEDS WORK:** <18/20 - Parameter improvements need fixes

---

**Note:** These tests are read-only and safe for production networks. They validate that the MCP server retrieves complete data using maximum pagination (perPage=1000) and appropriate time ranges.