# MCP Test Round 3 - Advanced Validation Scenarios

## 🔍 Deep Inspection Tests

### Deep Test 1: Client Journey Tracking
**Prompt:** "Track a specific client's journey through Reserve St network - show me their connection history, data usage, and any issues"

**Validation:**
- ✅ Should retrieve complete client history
- ✅ Uses perPage=1000 for all related queries
- ✅ Shows comprehensive data without limits
- ❌ FAIL if client data truncated

**Tests:** Client-specific queries with full pagination

---

### Deep Test 2: VLAN Traffic Analysis
**Prompt:** "Analyze traffic patterns across all VLANs in Reserve St - show me which VLANs have the most activity"

**Validation:**
- ✅ Retrieves data for ALL VLANs
- ✅ Complete traffic statistics per VLAN
- ✅ No sampling due to pagination limits
- ❌ FAIL if VLAN data incomplete

**Tests:** VLAN-segmented analysis with perPage=1000

---

### Deep Test 3: Rogue AP Detection
**Prompt:** "Scan for rogue APs and unauthorized wireless devices across Reserve St network"

**Validation:**
- ✅ Complete Air Marshal data
- ✅ All detected devices listed
- ✅ Uses maximum pagination for detection
- ❌ FAIL if rogue device list truncated

**Tests:** Air Marshal API with perPage=1000

---

## 🏥 Health Check Tests

### Health Test 1: Device Uptime Analysis
**Prompt:** "Show me device uptime and reboot history for all devices in Reserve St network"

**Validation:**
- ✅ Complete device list with uptime
- ✅ Full reboot history per device
- ✅ No "showing first X devices" limits
- ❌ FAIL if device history incomplete

**Tests:** Device status APIs with full pagination

---

### Health Test 2: Port Utilization Audit
**Prompt:** "Audit all switch ports in Reserve St - show me utilization, errors, and connected devices"

**Validation:**
- ✅ ALL switch ports analyzed
- ✅ Complete error statistics
- ✅ Full client mapping to ports
- ❌ FAIL if port data limited

**Tests:** Switch port APIs with perPage=1000

---

### Health Test 3: Firmware Compliance Check
**Prompt:** "Check firmware versions across all devices in Skycomm organization - identify any outdated devices"

**Validation:**
- ✅ Complete device inventory checked
- ✅ All firmware versions listed
- ✅ No device limit in compliance check
- ❌ FAIL if device list incomplete

**Tests:** Organization device APIs with perPage=1000

---

## 🔐 Security Deep Dive Tests

### Security Test 1: Threat Analysis
**Prompt:** "Analyze all security threats detected in Reserve St over the past 2 weeks - categorize by severity"

**Validation:**
- ✅ 14 days of security data (1209600 seconds)
- ✅ ALL threats retrieved (perPage=1000)
- ✅ Complete categorization possible
- ❌ FAIL if threat data limited

**Tests:** Security events with custom timespan + perPage=1000

---

### Security Test 2: Failed Authentication Audit
**Prompt:** "Show me all failed authentication attempts across Reserve St network in the last 72 hours"

**Validation:**
- ✅ 72 hours of auth data (259200 seconds)
- ✅ Complete failure log
- ✅ No pagination limits on failures
- ❌ FAIL if auth log truncated

**Tests:** Auth failure events with perPage=1000

---

### Security Test 3: Firewall Rule Effectiveness
**Prompt:** "Analyze firewall rule hits for Reserve St - show me which rules are triggered most"

**Validation:**
- ✅ Complete rule hit statistics
- ✅ All firewall events analyzed
- ✅ Proper timespan coverage
- ❌ FAIL if rule data incomplete

**Tests:** Firewall events with maximum pagination

---

## 📡 Wireless Specific Tests

### Wireless Test 1: SSID Performance Comparison
**Prompt:** "Compare performance metrics across all SSIDs in Reserve St - connection success rates, speeds, and client distribution"

**Validation:**
- ✅ ALL SSIDs analyzed completely
- ✅ Each SSID shows isolation status (🔒/🔓)
- ✅ Complete client lists per SSID
- ❌ FAIL if SSID data limited or isolation missing

**Tests:** SSID metrics with perPage=1000 + lanIsolationEnabled

---

### Wireless Test 2: RF Environment Analysis
**Prompt:** "Analyze the RF environment in Reserve St - show channel utilization, interference, and neighboring APs"

**Validation:**
- ✅ Complete RF data for all APs
- ✅ Full neighboring AP list
- ✅ No sampling in interference data
- ❌ FAIL if RF data incomplete

**Tests:** RF analytics with proper pagination

---

### Wireless Test 3: Client Roaming Patterns
**Prompt:** "Track client roaming patterns in Reserve St - show me how clients move between APs"

**Validation:**
- ✅ Complete roaming history
- ✅ All AP transitions captured
- ✅ No limit on roaming events
- ❌ FAIL if roaming data truncated

**Tests:** Client roaming with perPage=1000

---

## 🌍 Multi-Organization Tests

### Multi-Org Test 1: Cross-Organization Search
**Prompt:** "Search for a device with serial Q2XX-XXXX-XXXX across all my organizations"

**Validation:**
- ✅ Searches ALL organizations
- ✅ Each org query uses perPage=1000
- ✅ Complete device inventory searched
- ❌ FAIL if search incomplete

**Tests:** Multi-org device search with full pagination

---

### Multi-Org Test 2: License Utilization
**Prompt:** "Show me license utilization across all organizations - identify any expiring soon"

**Validation:**
- ✅ Complete license inventory
- ✅ All organizations checked
- ✅ No pagination limits
- ❌ FAIL if license data incomplete

**Tests:** License APIs with perPage=1000

---

### Multi-Org Test 3: Comparative Health
**Prompt:** "Compare network health between Skycomm and Kids ENT organizations"

**Validation:**
- ✅ Both orgs fully analyzed
- ✅ Complete device/client counts
- ✅ All health metrics retrieved
- ❌ FAIL if comparison data limited

**Tests:** Cross-org health with consistent pagination

---

## 🚨 Incident Response Tests

### Incident Test 1: Breach Investigation
**Prompt:** "Investigate potential breach - show me all unusual activities in Reserve St from the past 3 days"

**Validation:**
- ✅ 3 days of complete data (259200 seconds)
- ✅ ALL events retrieved for analysis
- ✅ Security events use perPage=1000
- ❌ FAIL if investigation data incomplete

**Tests:** Incident response with full data retrieval

---

### Incident Test 2: DDoS Detection
**Prompt:** "Check for DDoS patterns - analyze traffic spikes and connection floods in Reserve St"

**Validation:**
- ✅ Complete traffic analysis
- ✅ All connection data retrieved
- ✅ No sampling in spike detection
- ❌ FAIL if traffic data limited

**Tests:** DDoS detection with maximum pagination

---

### Incident Test 3: Configuration Audit Trail
**Prompt:** "Show me all configuration changes made to Reserve St network in the past week"

**Validation:**
- ✅ Complete change log
- ✅ 7 days of audit trail
- ✅ All changes captured
- ❌ FAIL if audit log truncated

**Tests:** Config change events with perPage=1000

---

## 🔄 State Change Tests

### State Test 1: Device State Transitions
**Prompt:** "Track all device state changes in Reserve St - online/offline/dormant transitions"

**Validation:**
- ✅ Complete state history
- ✅ All transitions captured
- ✅ No limit on state changes
- ❌ FAIL if state history incomplete

**Tests:** Device state with full pagination

---

### State Test 2: SSID Enable/Disable History
**Prompt:** "Show me the history of SSID enable/disable events for Reserve St"

**Validation:**
- ✅ Complete SSID state history
- ✅ Shows current isolation status
- ✅ All state changes listed
- ❌ FAIL if SSID history truncated

**Tests:** SSID state changes with perPage=1000

---

## 🎯 Validation Matrix

| Test Category | Focus Area | Key Parameter | Expected Result |
|--------------|------------|---------------|-----------------|
| Deep Inspection | Client tracking | perPage=1000 | Complete journey |
| Health Checks | Device uptime | perPage=1000 | All devices |
| Security | Threat analysis | perPage=1000 + timespan | Full coverage |
| Wireless | SSID comparison | lanIsolationEnabled | 🔒/🔓 visible |
| Multi-Org | Cross-org search | perPage=1000 per org | Complete search |
| Incident | Breach investigation | 259200s + perPage=1000 | Full forensics |
| State Changes | Transitions | perPage=1000 | Complete history |

## 📝 Quick Test Commands

```bash
# Test 1: Verify perPage=1000
"Get me EVERYTHING - all clients, all events, all alerts for Reserve St"

# Test 2: Verify timespan
"Show security events for exactly 14 days from Reserve St"

# Test 3: Verify isolation
"Display all SSID configurations with security settings"

# Test 4: Verify no limits
"Count exact total of all clients across entire Skycomm org"

# Test 5: Verify completeness
"Full device inventory with status for Skycomm"
```

## ✅ Success Criteria

After running these tests:
- No "showing first X" messages
- Security events cover requested timespan
- SSID isolation clearly displayed
- Complete data for analysis
- No pagination warnings

## 🚫 Failure Indicators

- "Limited to 20 results"
- "Showing partial data"
- Missing isolation icons
- Truncated histories
- Incomplete inventories

---

**Note:** These tests validate that the MCP server provides complete, unpaginated data suitable for enterprise network management and security analysis.