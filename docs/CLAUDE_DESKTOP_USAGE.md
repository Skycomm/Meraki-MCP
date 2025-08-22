# Claude Desktop MCP Usage Guide

## How Claude Desktop Uses MCP Tools

### Important: Session Context

**When you close and reopen Claude Desktop, it loses all context** about:
- What organizations/networks were already created
- What operations were already performed
- Previous conversation history

This means Claude will:
1. Try to create new resources with the same names (Meraki allows duplicate names)
2. Not know about existing resources unless it searches for them first

### The Device Claiming Issue

When Claude Desktop tries to add a device, it typically:
1. Uses `get_device` to check if device exists → Returns 404 for unclaimed devices
2. Fails because it thinks the device doesn't exist

**Solution**: Use the new `claim_device_direct` tool which bypasses the existence check.

### Best Practices

1. **Always check for existing resources first**:
   ```
   "First check if Test-Org already exists, then create it only if needed"
   ```

2. **Use unique names with timestamps**:
   ```
   "Create organization Test-Org-2025-08-22-1234"
   ```

3. **Clean up after testing**:
   ```
   "Delete the test organization and network when done"
   ```

4. **For device claiming, specify to use claim_device_direct**:
   ```
   "Use the claim_device_direct tool to add device Q2GD-VRAM-XSYA"
   ```

### Example Prompts for Claude Desktop

#### Good Prompt:
```
Check if organization "Test-Org" exists. If not, create it. 
Then create network "Test-Net" if it doesn't exist.
Use claim_device_direct to add device Q2GD-VRAM-XSYA to the network.
```

#### Better Prompt:
```
Create a new test organization with a unique name like "Test-Org-[timestamp]".
Create network "Test-Net" in it.
Use claim_device_direct tool to add device Q2GD-VRAM-XSYA.
Show me the IDs of what was created.
```

### Common Issues and Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| Duplicate organizations | Claude doesn't know about existing ones | Check first or use unique names |
| Device claim fails with 404 | Using get_device first | Use claim_device_direct tool |
| Can't delete org | Device stuck in inventory | Release device first |
| Operations seem to repeat | Lost context after restart | Document IDs for reference |

### Tool-Specific Notes

#### claim_device_direct
- **Purpose**: Bypass device existence check
- **When to use**: Always for unclaimed devices
- **Parameters**: network_id, serial
- **Success even when**: get_device returns 404

#### create_organization
- **Note**: Allows duplicate names
- **Returns**: Organization ID (save this!)
- **Best practice**: Use unique names

#### create_network  
- **Note**: Allows duplicate names within an org
- **Returns**: Network ID (save this!)
- **Requires**: Valid organization_id