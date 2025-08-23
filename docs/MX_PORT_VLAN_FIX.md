# 🔧 MX Port VLAN Configuration Fix

## Problem Description

When using the Meraki API to enable/disable MX appliance ports, VLAN configuration can be lost. This is due to the API using PUT semantics (complete replacement) rather than PATCH semantics (partial update).

### Example of the Issue

```python
# Original port configuration:
# Port 4: Trunk, Native VLAN 90, Allowed VLANs: all

# Disable port (WRONG WAY):
update_network_appliance_port(network_id, "4", enabled=False)
# Port is disabled ✓

# Re-enable port (WRONG WAY):
update_network_appliance_port(network_id, "4", enabled=True)
# Port is enabled ✓
# BUT: Native VLAN is lost! Port resets to default configuration ✗
```

## Root Cause

The Meraki API `updateNetworkAppliancePort` endpoint requires all configuration parameters to be sent when updating a port. If you only send `enabled: true/false`, other parameters may reset to defaults.

## Solution: New Safe Functions

### 1. `toggle_network_appliance_port`

**Purpose**: Safely enable/disable ports while preserving all VLAN settings

**How it works**:
1. Fetches current port configuration
2. Preserves all existing settings
3. Only changes the enabled state
4. Sends complete configuration back

**Usage**:
```python
# Disable port safely:
toggle_network_appliance_port(
    network_id="L_726205439913500692",
    port_id="4",
    enabled=False
)

# Re-enable port safely:
toggle_network_appliance_port(
    network_id="L_726205439913500692",
    port_id="4",
    enabled=True
)
# All VLAN settings preserved! ✓
```

### 2. `get_network_appliance_port`

**Purpose**: Get configuration for a single port (useful for verification)

**Usage**:
```python
get_network_appliance_port(
    network_id="L_726205439913500692",
    port_id="4"
)
```

### 3. Updated `update_network_appliance_port`

Now includes:
- Warning in documentation about configuration loss
- Runtime warning when only 'enabled' is updated
- Recommendation to use `toggle_network_appliance_port` instead

## Best Practices

### ✅ DO: Use toggle function for enable/disable
```python
toggle_network_appliance_port(network_id, port_id, enabled=True)
```

### ❌ DON'T: Use update with only enabled parameter
```python
update_network_appliance_port(network_id, port_id, enabled=True)
```

### ✅ DO: Include all parameters when updating
```python
update_network_appliance_port(
    network_id=network_id,
    port_id=port_id,
    enabled=True,
    type="trunk",
    vlan=90,
    allowed_vlans="all"
)
```

## Technical Details

- **API Method**: PUT (replaces entire configuration)
- **Affected Endpoints**: `/networks/{networkId}/appliance/ports/{portId}`
- **Affected Devices**: All MX appliances
- **Workaround**: GET current config → Modify → PUT complete config

## Testing the Fix

1. **Check current port config**:
   ```
   get_network_appliance_port network_id: "..." port_id: "4"
   ```

2. **Disable port safely**:
   ```
   toggle_network_appliance_port network_id: "..." port_id: "4" enabled: false
   ```

3. **Re-enable port safely**:
   ```
   toggle_network_appliance_port network_id: "..." port_id: "4" enabled: true
   ```

4. **Verify config preserved**:
   ```
   get_network_appliance_port network_id: "..." port_id: "4"
   ```

## Impact

This fix prevents:
- Loss of VLAN configuration during port toggles
- Network disruption from misconfigured ports
- Manual reconfiguration after port state changes
- Confusion about why devices lose connectivity

## Future Considerations

- Monitor Meraki API updates for potential PATCH support
- Consider similar patterns for other configuration endpoints
- Implement similar safe wrappers for other destructive operations