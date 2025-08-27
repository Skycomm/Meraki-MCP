# MCP Validation Test Suite - Parameter Verification

## Test Execution Instructions
Run these prompts through Meraki MCP and verify the responses match expected behavior.
Focus on validating that perPage=1000 and proper defaults are being used.

---

## 🧪 Test Set A: Data Volume Tests

### Test A1: Heavy Client Network
**Prompt:** "Show me all devices and clients in the Reserve St network, I need a complete inventory"

**Validation Points:**
- ✅ Should return ALL clients without "showing first X" messages
- ✅ Should list complete device inventory
- ✅ Total client count should be accurate
- ❌ FAIL if see "limited to 20" or "showing partial results"

**Internal Check:** Uses perPage=1000 for getNetworkClients

---

### Test A2: Historical Events Deep Dive  
**Prompt:** "Get me all network events from Reserve St for the past week, I need to see everything"

**Validation Points:**
- ✅ Should attempt to retrieve ALL events (even if returns empty)
- ✅ Should try multiple product types (appliance, wireless, switch)
- ✅ No pagination warnings
- ❌ FAIL if only shows 10-20 events when more exist

**Internal Check:** Each productType call uses perPage=1000

---

### Test A3: Organization-Wide Device Status
**Prompt:** "Give me the availability status for every single device in the Skycomm organization"

**Validation Points:**
- ✅ Should return all device statuses
- ✅ Should show online/offline/dormant states
- ✅ Complete device list without truncation
- ❌ FAIL if missing devices or shows "partial list"

**Internal Check:** Uses perPage=1000 for getOrganizationDevicesAvailabilities

---

## 🧪 Test Set B: Security & Monitoring Tests

### Test B1: Security Incident Investigation
**Prompt:** "I need to investigate security incidents - show me all security events for Reserve St network from the past month"

**Validation Points:**
- ✅ Should retrieve 31 days of data (2678400 seconds)
- ✅ Should get up to 1000 events per page
- ✅ Should mention the time period covered
- ❌ FAIL if only shows last 24 hours or limits to 100 events

**Internal Check:** Uses perPage=1000 AND timespan=2678400

---

### Test B2: Alert Analysis
**Prompt:** "Pull the complete alert history for Reserve St network, I need to analyze patterns"

**Validation Points:**
- ✅ Should retrieve complete alert history
- ✅ No "limited to 100 alerts" message (old behavior)
- ✅ Should use maximum pagination
- ❌ FAIL if truncated at 100 alerts

**Internal Check:** Uses perPage=1000 (not the old 100)

---

### Test B3: Wireless Security Audit
**Prompt:** "Audit all wireless SSIDs in Reserve St - show me their security settings including isolation status"

**Validation Points:**
- ✅ Should show all SSIDs with full configuration
- ✅ Must display "LAN Isolation: 🔒 Enabled" or "🔓 Disabled"
- ✅ Should show auth modes and encryption
- ❌ FAIL if isolation status missing

**Internal Check:** Properly displays lanIsolationEnabled field

---

## 🧪 Test Set C: Performance & Scale Tests

### Test C1: Busy Network Analysis
**Prompt:** "Analyze all wireless client connections in Reserve St network - show me everyone who's connected"

**Validation Points:**
- ✅ Should return ALL wireless clients
- ✅ Should show MAC, IP, SSID, RSSI for each
- ✅ Complete list without "showing first 20" limits
- ❌ FAIL if artificially limited client count

**Internal Check:** Uses perPage=1000 for getNetworkWirelessClients

---

### Test C2: Multi-Network Overview
**Prompt:** "Give me client counts for ALL networks in Skycomm - need to see which are busiest"

**Validation Points:**
- ✅ Should process all 9 networks
- ✅ Each network should show complete client count
- ✅ No pagination issues per network
- ❌ FAIL if counts seem artificially low

**Internal Check:** Each network uses perPage=1000 for clients

---

### Test C3: Traffic Pattern Analysis
**Prompt:** "Show me network traffic and usage patterns for Reserve St"

**Validation Points:**
- ✅ Should retrieve comprehensive traffic data
- ✅ Should include proper time ranges
- ✅ Complete data without sampling issues
- ❌ FAIL if data appears limited

**Internal Check:** Uses appropriate perPage and timespan

---

## 🧪 Test Set D: Edge Cases & Validation

### Test D1: Empty Network Check
**Prompt:** "Check for any events or alerts in the 'test' network"

**Validation Points:**
- ✅ Should properly handle empty responses
- ✅ Should still use perPage=1000 internally
- ✅ No errors from empty data
- ❌ FAIL if crashes or shows errors

**Internal Check:** Parameters still set correctly even for empty results

---

### Test D2: Cross-Product Query
**Prompt:** "Show me everything happening in Reserve St - events from switches, APs, and firewalls"

**Validation Points:**
- ✅ Should query multiple product types
- ✅ Each query uses perPage=1000
- ✅ Aggregates results properly
- ❌ FAIL if only shows one product type

**Internal Check:** Multiple API calls each with perPage=1000

---

### Test D3: SSID Isolation Toggle Check
**Prompt:** "I need to verify the isolation settings on all SSIDs in Reserve St - show me which ones have LAN isolation enabled"

**Validation Points:**
- ✅ Lists all SSIDs with clear isolation status
- ✅ Shows 🔒 for enabled, 🔓 for disabled
- ✅ Mentions Bridge mode requirement
- ❌ FAIL if isolation info missing or unclear

**Internal Check:** Correctly reads lanIsolationEnabled parameter

---

## 🧪 Test Set E: Comprehensive Validation

### Test E1: Full Network Health Check
**Prompt:** "Run a complete health check on Reserve St - I need device status, client lists, recent events, and any alerts"

**Validation Points:**
- ✅ All data complete without pagination limits
- ✅ Events use perPage=1000
- ✅ Clients show all connected devices
- ✅ Comprehensive report generated
- ❌ FAIL if any section shows "partial data"

---

### Test E2: Time-Range Query
**Prompt:** "Get me the last 7 days of security events and alerts for Reserve St"

**Validation Points:**
- ✅ Should retrieve full 7 days of data
- ✅ Should handle large result sets
- ✅ Uses proper timespan parameter
- ❌ FAIL if only shows recent 24h

---

## 📊 Validation Checklist

After running all tests, verify:

- [ ] No "showing only 20" or "limited to 100" messages
- [ ] Security events default to 31 days
- [ ] All client lists are complete
- [ ] SSID isolation status displays correctly
- [ ] Empty results handled gracefully
- [ ] Multi-product queries work properly
- [ ] Large datasets retrieved successfully
- [ ] Time-based queries use proper ranges

## 🎯 Success Criteria

**PASS** = All data retrieval is complete, using maximum pagination (1000) and proper defaults
**FAIL** = Any artificial limits, missing data, or pagination issues

## 📝 Results Template

```
Test A1: ✅/❌ [Notes]
Test A2: ✅/❌ [Notes]
Test A3: ✅/❌ [Notes]
Test B1: ✅/❌ [Notes]
Test B2: ✅/❌ [Notes]
Test B3: ✅/❌ [Notes]
Test C1: ✅/❌ [Notes]
Test C2: ✅/❌ [Notes]
Test C3: ✅/❌ [Notes]
Test D1: ✅/❌ [Notes]
Test D2: ✅/❌ [Notes]
Test D3: ✅/❌ [Notes]
Test E1: ✅/❌ [Notes]
Test E2: ✅/❌ [Notes]

Overall: X/14 tests passed
```