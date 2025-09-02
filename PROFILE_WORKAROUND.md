# Claude Desktop Tool Limit Workaround

## Problem Solved
Claude Desktop has a ~850 tool limit. With 833 tools, we were at the edge and couldn't add more without breaking Claude Desktop.

## Solution Implemented
Created a **profile-based loading system** that allows running different tool configurations based on use case.

## How to Use

### Quick Start
```bash
# Run wireless-focused server (179 tools)
./run_wireless.sh

# Run network infrastructure server (402 tools)
./run_network.sh

# Run organization admin server (126 tools)
./run_organizations.sh

# Run monitoring server (141 tools)
./run_monitoring.sh

# Run full server (833 tools - may hit limit)
./run_full.sh
```

### Environment Variables
```bash
# Select a profile
export MCP_PROFILE=WIRELESS

# Custom module selection
export MCP_MODULES="wireless,organizations_core,helpers"

# Exclude modules from a profile
export MCP_PROFILE=NETWORK
export MCP_EXCLUDE="switch,appliance_firewall"
```

## Available Profiles

| Profile | Tools | Focus Area |
|---------|-------|------------|
| WIRELESS | ~179 | Wireless networks, RF, SSIDs |
| NETWORK | ~402 | Switch, Appliance, VPN |
| ORGANIZATIONS | ~126 | Org-level admin |
| MONITORING | ~141 | Devices, cameras, analytics |
| OPERATIONS | ~85 | Batch, alerts, policy |
| MINIMAL | ~60 | Essential read-only |
| FULL | 833 | Everything (default) |

## Claude Desktop Configuration

Add to your Claude Desktop settings:

```json
{
  "mcpServers": {
    "meraki-wireless": {
      "command": "/path/to/.venv/bin/python",
      "args": ["/path/to/server/main.py"],
      "env": {
        "MCP_PROFILE": "WIRELESS",
        "MERAKI_API_KEY": "your-key"
      }
    }
  }
}
```

See `claude_desktop_configs/README.md` for complete examples.

## Benefits

✅ **Stay under tool limit** - Each profile well below 850 tools  
✅ **Fast startup** - Load only what you need  
✅ **Multiple servers** - Run different profiles simultaneously  
✅ **Backwards compatible** - Defaults to FULL if no profile set  
✅ **Flexible** - Custom module selection available  

## Module Groups

Use these in `MCP_MODULES` for common combinations:

- `core` - Essential helpers and search
- `wireless_all` - All wireless modules  
- `network_all` - All network infrastructure
- `org_all` - All organization modules
- `monitoring_all` - All monitoring/analytics
- `operations_all` - All operations/automation

## Implementation Details

- `server/profiles.py` - Profile definitions and logic
- `server/main.py` - Conditional module loading
- `run_*.sh` - Launcher scripts for each profile
- `claude_desktop_configs/` - Example configurations

## Testing

```bash
# Test a profile
MCP_PROFILE=WIRELESS .venv/bin/python -m server.main

# Test custom modules
MCP_MODULES="wireless,helpers" .venv/bin/python -m server.main
```

## Next Steps

1. Configure Claude Desktop with desired profiles
2. Use focused profiles for better performance
3. Switch profiles based on task requirements
4. Create custom combinations as needed

The system is fully implemented and ready to use!