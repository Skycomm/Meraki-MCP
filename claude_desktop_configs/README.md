# Claude Desktop Configuration Examples

These JSON snippets can be added to your Claude Desktop configuration to run different Meraki MCP server profiles.

## Setup Instructions

1. Open Claude Desktop settings
2. Navigate to MCP Servers configuration
3. Add one or more of the configurations below
4. Each profile appears as a separate server in Claude Desktop

## Configuration Examples

### Wireless Profile (179 tools)
Best for wireless network management, RF optimization, and SSID configuration.

```json
{
  "mcpServers": {
    "meraki-wireless": {
      "command": "/Users/david/docker/cisco-meraki-mcp-server-tvi/.venv/bin/python",
      "args": ["/Users/david/docker/cisco-meraki-mcp-server-tvi/server/main.py"],
      "env": {
        "MCP_PROFILE": "WIRELESS",
        "MERAKI_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

### Network Infrastructure Profile (402 tools)
For switch, appliance, and network configuration.

```json
{
  "mcpServers": {
    "meraki-network": {
      "command": "/Users/david/docker/cisco-meraki-mcp-server-tvi/.venv/bin/python",
      "args": ["/Users/david/docker/cisco-meraki-mcp-server-tvi/server/main.py"],
      "env": {
        "MCP_PROFILE": "NETWORK",
        "MERAKI_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

### Organizations Profile (126 tools)
For organization-level administration and policy management.

```json
{
  "mcpServers": {
    "meraki-organizations": {
      "command": "/Users/david/docker/cisco-meraki-mcp-server-tvi/.venv/bin/python",
      "args": ["/Users/david/docker/cisco-meraki-mcp-server-tvi/server/main.py"],
      "env": {
        "MCP_PROFILE": "ORGANIZATIONS",
        "MERAKI_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

### Monitoring Profile (141 tools)
For device monitoring, cameras, sensors, and analytics.

```json
{
  "mcpServers": {
    "meraki-monitoring": {
      "command": "/Users/david/docker/cisco-meraki-mcp-server-tvi/.venv/bin/python",
      "args": ["/Users/david/docker/cisco-meraki-mcp-server-tvi/server/main.py"],
      "env": {
        "MCP_PROFILE": "MONITORING",
        "MERAKI_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

### Full Profile (833 tools)
Complete API coverage - may approach Claude Desktop's limit.

```json
{
  "mcpServers": {
    "meraki-full": {
      "command": "/Users/david/docker/cisco-meraki-mcp-server-tvi/.venv/bin/python",
      "args": ["/Users/david/docker/cisco-meraki-mcp-server-tvi/server/main.py"],
      "env": {
        "MCP_PROFILE": "FULL",
        "MERAKI_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

### Custom Module Selection
Load specific modules only.

```json
{
  "mcpServers": {
    "meraki-custom": {
      "command": "/Users/david/docker/cisco-meraki-mcp-server-tvi/.venv/bin/python",
      "args": ["/Users/david/docker/cisco-meraki-mcp-server-tvi/server/main.py"],
      "env": {
        "MCP_MODULES": "wireless,wireless_advanced,organizations_core,helpers,search",
        "MERAKI_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

### Multiple Servers Configuration
Run multiple profiles simultaneously in Claude Desktop.

```json
{
  "mcpServers": {
    "meraki-wireless": {
      "command": "/Users/david/docker/cisco-meraki-mcp-server-tvi/.venv/bin/python",
      "args": ["/Users/david/docker/cisco-meraki-mcp-server-tvi/server/main.py"],
      "env": {
        "MCP_PROFILE": "WIRELESS",
        "MERAKI_API_KEY": "your-api-key-here"
      }
    },
    "meraki-network": {
      "command": "/Users/david/docker/cisco-meraki-mcp-server-tvi/.venv/bin/python",
      "args": ["/Users/david/docker/cisco-meraki-mcp-server-tvi/server/main.py"],
      "env": {
        "MCP_PROFILE": "NETWORK",
        "MERAKI_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

## Environment Variables

- `MCP_PROFILE`: Select a predefined profile (WIRELESS, NETWORK, ORGANIZATIONS, MONITORING, FULL)
- `MCP_MODULES`: Comma-separated list of specific modules to load
- `MCP_EXCLUDE`: Comma-separated list of modules to exclude from a profile
- `MERAKI_API_KEY`: Your Meraki Dashboard API key
- `MCP_READ_ONLY_MODE`: Set to "true" for safe read-only operation

## Module Groups

When using `MCP_MODULES`, you can use these predefined groups:
- `core`: Essential helpers and search tools
- `wireless_all`: All wireless-related modules
- `network_all`: All network infrastructure modules
- `org_all`: All organization modules
- `monitoring_all`: All monitoring and analytics modules
- `operations_all`: All operations and automation modules

Example: `"MCP_MODULES": "core,wireless_all"`

## Tips

1. Start with a focused profile for better performance
2. Use multiple profiles for different tasks
3. The FULL profile works but is close to Claude Desktop's limit
4. Custom module selection gives you precise control
5. Always test after changing configurations