# Meraki MCP Server Reorganization Plan

## Objective
Reorganize the MCP server to match Cisco's official API structure for easier maintenance and tracking of API changes.

## Current Problems
1. **tools_networks.py is a mega-module** with 86 functions mixing multiple API categories
2. **No clear mapping** to Cisco's official API categories
3. **Hard to track changes** when Cisco updates specific APIs
4. **Duplicate functions** across modules causing conflicts

## APIs Currently Mixed in tools_networks.py
- Group Policies: 10 functions (lines 733-844)
- Floor Plans: 14 functions (lines 625-687)
- Bluetooth Clients: 5 functions (lines 362-394)
- PII Management: 14 functions (lines 1761-1895)
- Meraki Auth Users: 10 functions (lines 938-1025)
- Traffic Analysis: 4 functions
- Netflow: 9 functions
- **Total: 66 functions that should be in separate modules**

## Proposed New Structure

### Phase 1: Extract Functions from tools_networks.py
Create these new modules by extracting functions:

| New Module | Functions to Extract | Line Numbers in tools_networks.py |
|------------|---------------------|-----------------------------------|
| tools_group_policies.py | 10 functions | 733-844 |
| tools_floor_plans.py | 14 functions | 625-687 |
| tools_bluetooth_clients.py | 5 functions | 362-394 |
| tools_pii.py | 14 functions | 1761-1895 |
| tools_meraki_auth_users.py | 10 functions | 938-1025 |
| tools_traffic_analysis.py | 4 functions | Various |
| tools_netflow.py | 9 functions | Various |

### Phase 2: Add Missing Official APIs
Create these completely new modules:

| New Module | Purpose | Cisco API Category |
|------------|---------|-------------------|
| tools_org_admins.py | Organization admin management | Organizations → Admins |
| tools_login_security.py | Login security settings | Organizations → Login Security |

### Phase 3: Directory Reorganization (Optional)
```
server/
├── configure/
│   ├── adaptive_policy.py
│   ├── group_policies.py
│   ├── floor_plans.py
│   ├── meraki_auth_users.py
│   ├── traffic_analysis.py
│   ├── netflow.py
│   └── ...
├── monitor/
│   ├── bluetooth_clients.py
│   └── ...
├── live_tools/
│   └── (already in tools_live.py)
└── tools_networks.py (reduced to ~20 core network functions)
```

## Implementation Checklist

### Step 1: Extract Group Policies
- [ ] Copy functions from tools_networks.py lines 733-844
- [ ] Create tools_group_policies.py
- [ ] Functions to extract:
  - get_network_group_policies()
  - create_network_group_policy()
  - get_network_group_policy()
  - update_network_group_policy()
  - delete_network_group_policy()

### Step 2: Extract Floor Plans
- [ ] Copy functions from tools_networks.py lines 625-687
- [ ] Create tools_floor_plans.py
- [ ] Functions to extract:
  - get_network_floor_plans()
  - create_network_floor_plan()
  - get_network_floor_plan()
  - update_network_floor_plan()
  - delete_network_floor_plan()

### Step 3: Extract Bluetooth Clients
- [ ] Copy functions from tools_networks.py lines 362-394
- [ ] Create tools_bluetooth_clients.py
- [ ] Functions to extract:
  - get_network_bluetooth_clients()
  - get_network_bluetooth_client()

### Step 4: Extract PII Management
- [ ] Copy functions from tools_networks.py lines 1761-1895
- [ ] Create tools_pii.py
- [ ] Functions to extract:
  - get_network_pii_pii_keys()
  - get_network_pii_requests()
  - create_network_pii_request()
  - get_network_pii_request()
  - delete_network_pii_request()
  - get_network_pii_sm_devices_for_key()
  - get_network_pii_sm_owners_for_key()

### Step 5: Extract Meraki Auth Users
- [ ] Copy functions from tools_networks.py lines 938-1025
- [ ] Create tools_meraki_auth_users.py
- [ ] Functions to extract:
  - get_network_meraki_auth_users()
  - create_network_meraki_auth_user()
  - get_network_meraki_auth_user()
  - delete_network_meraki_auth_user()
  - update_network_meraki_auth_user()

### Step 6: Update main.py
- [ ] Import all new modules
- [ ] Register all new tools
- [ ] Remove duplicate registrations from tools_networks.py

### Step 7: Test
- [ ] Verify no duplicate tool names
- [ ] Test server starts without errors
- [ ] Confirm all functions work

## Benefits After Reorganization
1. **Clear 1:1 mapping** with Cisco's official API categories
2. **Easy to track changes** - when Cisco updates "Group Policies API", we update tools_group_policies.py
3. **No more conflicts** - each API category in its own module
4. **tools_networks.py reduced** from 86 to ~20 core network functions
5. **Better maintainability** - each module focused on one API category

## Files to Read When Starting This Work

1. **THIS FILE** - `/Users/david/docker/cisco-meraki-mcp-server-tvi/REORGANIZATION_PLAN.md`
2. **tools_networks.py** - The mega-module to extract from
3. **main.py** - To understand current registration pattern
4. **FINAL_API_COVERAGE_ANALYSIS.md** - To see what's currently implemented where

## Important Notes
- Each new module should follow the existing pattern of other tools_*.py files
- Use the same registration mechanism (register function returning dict of lambdas)
- Maintain the same function signatures when extracting
- After extraction, comment out (don't delete) the original functions in tools_networks.py first
- Test thoroughly before removing the commented functions