# Organization Analysis Tools

This document describes the comprehensive organization analysis tools added to the Cisco Meraki MCP Server.

## check_organization_comprehensive

Performs a deep analysis of a Meraki organization to understand its configuration and identify if it's empty or a clone.

### Usage
```python
# Check all aspects of an organization
result = check_organization_comprehensive(org_id="726205439913493748", check_type="all")

# Check specific aspects only
result = check_organization_comprehensive(org_id="726205439913493748", check_type="settings")
```

### Parameters
- `org_id`: The organization ID to analyze
- `check_type`: Type of check to perform
  - `"all"`: Check everything (default)
  - `"settings"`: Organization settings, alerts, firmware, early access
  - `"devices"`: Device inventory
  - `"policies"`: Policy objects and groups
  - `"webhooks"`: Webhook configurations
  - `"licenses"`: License information

### What it checks:
1. **Basic Information**: Name, URL, API status, cloud region
2. **Networks**: Count and types of networks
3. **Devices**: Inventory grouped by model
4. **Alert Settings**: Enabled alert types and destinations
5. **Webhooks**: Configured webhook endpoints
6. **Firmware Settings**: Upgrade configurations
7. **Licenses**: License states and counts
8. **Policy Objects**: Configured policies by category
9. **Early Access Features**: Opted-in beta features
10. **Administrators**: Admin counts and access levels
11. **API Usage**: Recent API activity

## compare_organizations

Compares two organizations side-by-side to identify similarities and differences.

### Usage
```python
result = compare_organizations(
    org_id_1="726205439913493746",  # Main organization
    org_id_2="726205439913493748"   # Clone organization
)
```

### What it compares:
1. **Basic Information**: Names, URLs, API status, regions
2. **Networks**: Count and types
3. **Devices**: Models and counts
4. **Administrators**: Including common admins
5. **Licenses**: States and counts

### Clone Detection
The tool identifies potential clone indicators:
- Both organizations have no networks or devices
- Both have "clone" in their names
- They share common administrators
- They're in the same cloud region

## Example Scripts

### check_clone_orgs_comprehensive.py
A ready-to-use script that:
1. Checks both Clone organizations comprehensively
2. Compares them to each other
3. Compares them to the main Skycomm organization

To run:
```bash
cd /Users/david/docker/cisco-meraki-mcp-server-tvi
python meraki_server.py
# In another terminal:
./check_clone_orgs_comprehensive.py
```

## Understanding Clone Organizations

Clone organizations in Meraki are typically created for:
1. **Testing**: Safe environment for testing API integrations
2. **Templates**: Pre-configured organizational settings
3. **Staging**: Testing configurations before production
4. **Backup**: Maintaining organization structure without active devices

The comprehensive check helps identify:
- Whether they're truly empty
- What settings they retain
- Who has access to them
- Their relationship to other organizations