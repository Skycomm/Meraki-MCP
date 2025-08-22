# Merging Guide for Cisco Meraki MCP Server

This guide explains how to manually merge the modular components of the Cisco Meraki MCP Server if you prefer a single file implementation over the modular structure.

## Current Structure

The server is currently split into multiple files to avoid length limitations:

1. `meraki_server.py` - Main entry point
2. `server/main.py` - Core server setup
3. `server/resources.py` - Resource handling
4. `server/tools_organizations.py` - Organization tools
5. `server/tools_networks.py` - Network tools
6. `server/tools_devices.py` - Device tools
7. `server/tools_wireless.py` - Wireless tools
8. `server/tools_switch.py` - Switch tools

## Merging Steps

To create a single `meraki-server.py` file, follow these steps:

1. **Start with Imports and Initialization**:
   - Begin with the imports from `server/main.py`
   - Include the initialization code for the Meraki client and MCP server

2. **Add Resource Handlers**:
   - Copy the resource handler functions from `server/resources.py`
   - Include both `list_resources()` and `read_resource()`

3. **Add Tools in Sequence**:
   - Organization tools from `server/tools_organizations.py`
   - Network tools from `server/tools_networks.py`
   - Device tools from `server/tools_devices.py`
   - Wireless tools from `server/tools_wireless.py`
   - Switch tools from `server/tools_switch.py`

4. **Add Main Block**:
   - Copy the `if __name__ == "__main__":` block from `meraki_server.py`

## Merge Template

Here's a template to follow:

```python
#!/usr/bin/env python3
"""
Cisco Meraki MCP Server - Model Context Protocol server for Meraki API integration.
"""

import asyncio
import json
import mcp.server as mcp
import mcp.types as types
from mcp.server.stdio import stdio_server
from meraki_client import MerakiClient
from utils.helpers import format_resource_uri, create_resource, create_content, format_error_message
from config import SERVER_NAME, SERVER_VERSION

# Initialize Meraki client
meraki = MerakiClient()

# Initialize MCP server
app = mcp.Server(SERVER_NAME, SERVER_VERSION)

# ===== RESOURCES =====
# (Copy resource handlers from server/resources.py)
@app.list_resources()
async def list_resources() -> list[types.Resource]:
    # ...

@app.read_resource()
async def read_resource(uri: str) -> list[types.ResourceContent]:
    # ...

# ===== ORGANIZATION TOOLS =====
# (Copy tools from server/tools_organizations.py)
@app.tool(
    name="list_organizations",
    # ...
)
async def list_organizations() -> str:
    # ...

# ... (other organization tools)

# ===== NETWORK TOOLS =====
# (Copy tools from server/tools_networks.py)
# ...

# ===== DEVICE TOOLS =====
# (Copy tools from server/tools_devices.py)
# ...

# ===== WIRELESS TOOLS =====
# (Copy tools from server/tools_wireless.py)
# ...

# ===== SWITCH TOOLS =====
# (Copy tools from server/tools_switch.py)
# ...

# Run the server
if __name__ == "__main__":
    asyncio.run(stdio_server(app))
```

## Testing After Merging

After merging the files:

1. Make sure the file is executable:
   ```bash
   chmod +x meraki-server.py
   ```

2. Test the server:
   ```bash
   ./meraki-server.py
   ```

3. Check for any syntax or import errors and fix them as needed.

## Additional Notes

- You may need to adjust some imports if there are circular dependencies.
- Ensure all functions have the correct decorators after merging.
- Check indentation to make sure nested functions are properly structured.
