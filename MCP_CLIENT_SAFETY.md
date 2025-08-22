# MCP Client Safety Features

## How Safety Works with Claude Desktop and Other MCP Clients

When using the Meraki MCP Server through Claude Desktop or other MCP clients, the safety features work as follows:

### 1. Read-Only Mode Messages

When `MCP_READ_ONLY_MODE=true`, destructive operations return clear messages to the client:

```
❌ OPERATION BLOCKED - READ-ONLY MODE

The server is running in READ-ONLY mode for safety.
Attempted operation: DELETE network 'Reserve St'
Resource ID: L_726205439913500692

To enable this operation:
1. Set MCP_READ_ONLY_MODE=false in your environment
2. Restart the MCP server
3. Try the operation again

⚠️ WARNING: Only disable read-only mode if you're certain you want to make changes.
```

### 2. What the Client Sees

#### In Read-Only Mode:
- **Delete operations**: Return the above blocking message
- **Update operations**: Return the blocking message
- **Reboot operations**: Return the blocking message
- **Read operations**: Work normally

#### With Confirmations Enabled (default):
- Operations that would normally require console input will be blocked
- The client receives: "❌ Operation cancelled by user"
- This is because MCP clients can't handle interactive prompts

### 3. Setting Up Safe MCP Usage

#### For Testing/Development:
```bash
# Always use read-only mode for testing
export MCP_READ_ONLY_MODE=true
export MERAKI_API_KEY=your_api_key
python meraki_server.py
```

#### For Production (with caution):
```bash
# Only when you need to make actual changes
export MCP_READ_ONLY_MODE=false
export MCP_REQUIRE_CONFIRMATIONS=false  # Disables interactive prompts
export MCP_AUDIT_LOGGING=true          # Keep audit trail
export MERAKI_API_KEY=your_api_key
python meraki_server.py
```

### 4. Claude Desktop Configuration

In your Claude Desktop configuration file, you can set environment variables:

```json
{
  "mcpServers": {
    "meraki": {
      "command": "python",
      "args": ["/path/to/meraki_server.py"],
      "env": {
        "MERAKI_API_KEY": "your_api_key",
        "MCP_READ_ONLY_MODE": "true"  // Always safe!
      }
    }
  }
}
```

### 5. Best Practices for MCP Clients

1. **Always start with read-only mode**
   - Test your workflows safely
   - Verify the correct resources are targeted

2. **Use a test organization first**
   - Never test on production without read-only mode

3. **Review audit logs**
   - Check `logs/meraki_mcp_audit.log` after operations

4. **Gradual permissions**
   - Start with `MCP_READ_ONLY_MODE=true`
   - Test thoroughly
   - Only then consider disabling read-only mode

### 6. Safety Features Summary

| Feature | Environment Variable | Default | MCP Client Behavior |
|---------|---------------------|---------|---------------------|
| Read-Only Mode | `MCP_READ_ONLY_MODE` | false | Blocks all writes, returns clear message |
| Confirmations | `MCP_REQUIRE_CONFIRMATIONS` | true | Blocks operations needing input |
| Audit Logging | `MCP_AUDIT_LOGGING` | true | Logs all attempts to file |

### 7. Example Client Interactions

#### Trying to delete in read-only mode:
```
User: Delete network L_726205439913500692
Assistant: I'll delete that network for you.
[Calls delete_network tool]
Result: ❌ OPERATION BLOCKED - READ-ONLY MODE
The server is running in READ-ONLY mode for safety.
...
```

#### Successful read operation:
```
User: Show me all networks in organization 686470
Assistant: I'll list all networks in that organization.
[Calls get_organization_networks tool]
Result: # Networks in Organization (686470)
- **Reserve St** (ID: `L_726205439913500692`)
  - Type: combined
  - Tags: Skycomm, branch
...
```

The safety features ensure that MCP clients cannot accidentally delete or modify resources without explicit configuration changes on the server side.