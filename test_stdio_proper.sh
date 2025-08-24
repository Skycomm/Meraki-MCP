#!/bin/bash
# Test stdio with proper JSON-RPC messages

# Initialize
echo '{"jsonrpc":"2.0","method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"test","version":"1.0.0"}},"id":1}'

# List tools
echo '{"jsonrpc":"2.0","method":"tools/list","params":{},"id":2}'

# Call a tool
echo '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"list_organizations","arguments":{}},"id":3}'