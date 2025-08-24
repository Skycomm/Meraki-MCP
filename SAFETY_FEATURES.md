# Cisco Meraki MCP Server - Safety Features

This document describes the safety features implemented to prevent accidental destructive operations.

## Overview

After an incident where testing resulted in production networks being deleted, comprehensive safety features have been implemented to prevent similar issues.

## Safety Features

### 1. Confirmation Prompts

All destructive operations now require explicit user confirmation:

- **Delete operations** (networks, organizations, policy objects)
- **Reboot operations** (devices, SM devices) 
- **Rename operations** (networks, organizations)

When a destructive operation is triggered:
1. User is shown details about what will be affected
2. User must type the operation name in UPPERCASE (e.g., "DELETE")
3. For extra-dangerous operations (org deletion), a second confirmation is required
4. A 3-second countdown occurs before execution

### 2. Read-Only Mode

Set the environment variable to enable read-only mode:
```bash
export MCP_READ_ONLY_MODE=true
```

When enabled:
- ALL write operations are blocked
- Server displays a prominent warning on startup
- Useful for testing without risk

### 3. Audit Logging

All operations are logged to `logs/meraki_mcp_audit.log` with:
- Timestamp
- Operation type
- Resource details
- User confirmation status
- API key hash (first 8 chars)

Enable/disable with:
```bash
export MCP_AUDIT_LOGGING=false  # Default is true
```

### 4. Disable Confirmations (NOT RECOMMENDED)

For automation, confirmations can be disabled:
```bash
export MCP_REQUIRE_CONFIRMATIONS=false  # Default is true
```

⚠️ **WARNING**: Only disable confirmations if you have other safeguards in place!

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `MCP_READ_ONLY_MODE` | false | Block all write operations |
| `MCP_REQUIRE_CONFIRMATIONS` | true | Require user confirmations |
| `MCP_AUDIT_LOGGING` | true | Enable audit logging |

## Protected Operations

### Network Operations
- `delete_network` - Requires confirmation
- `update_network` - Requires confirmation when renaming

### Organization Operations  
- `delete_organization` - Requires double confirmation
- `update_organization` - Requires confirmation when renaming

### Device Operations
- `reboot_device` - Requires confirmation
- `reboot_network_sm_devices` - Requires confirmation

### Policy Operations
- `delete_organization_policy_object` - Requires confirmation

## Best Practices

1. **Always test in read-only mode first**
   ```bash
   export MCP_READ_ONLY_MODE=true
   ```

2. **Review audit logs regularly**
   ```bash
   tail -f logs/meraki_mcp_audit.log
   ```

3. **Never disable confirmations in production**

4. **Use test organizations for development**

## Implementation Details

The safety system is implemented in:
- `utils/helpers.py` - Core confirmation and logging functions
- `config.py` - Environment variable configuration
- Individual tool files - Integration with destructive operations

The `require_confirmation()` function:
- Checks read-only mode first
- Displays operation details
- Requires exact match of operation name
- Logs all attempts (confirmed and cancelled)
- Adds countdown for destructive operations