#!/usr/bin/env python3
"""
Native FastMCP Streamable HTTP Server for n8n Integration
Implements proper MCP protocol over HTTP with streaming support

This server uses FastMCP's native HTTP transport which provides:
- JSON-RPC 2.0 protocol compliance
- Streamable HTTP responses for long operations  
- Proper MCP message formatting
- Built-in error handling
- Authentication support
"""

import os
import sys
from server.main import app  # Use existing FastMCP app with all 816+ tools

def main():
    """Run the FastMCP server in native HTTP mode with streaming."""
    
    # Get configuration from environment
    host = os.getenv("SERVER_HOST", "0.0.0.0")
    port = int(os.getenv("SERVER_PORT", "8100"))
    
    # Authentication tokens (optional)
    auth_token = os.getenv("MCP_AUTH_TOKEN")
    
    print(f"🚀 Starting Native FastMCP Streamable HTTP Server")
    print(f"📍 Host: {host}")
    print(f"🔌 Port: {port}")
    print(f"🔗 Endpoint: http://{host}:{port}/mcp")
    print(f"🛡️  Auth: {'Enabled' if auth_token else 'Disabled'}")
    print(f"📊 Tools: 816+ Meraki API tools available")
    print(f"🌊 Streaming: Enabled (Streamable HTTP)")
    print("")
    print("📝 n8n Configuration:")
    print(f"   URL: http://localhost:{port}/mcp")
    print(f"   Protocol: MCP over HTTP (JSON-RPC 2.0)")
    if auth_token:
        print(f"   Auth Header: Authorization: Bearer {auth_token}")
    print("")
    print("Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        # FastMCP runs in stdio mode by default
        # For HTTP, we need to use uvicorn to run the server
        import uvicorn
        # Import the main module which has the FastMCP app
        uvicorn.run("server.main:app", host=host, port=port, reload=False)
    except KeyboardInterrupt:
        print("\n✋ Server stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Server error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()