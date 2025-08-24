# Cisco Meraki MCP Server - STDIO Branch

This is the STDIO implementation of the Cisco Meraki MCP Server, designed for local use with Claude Desktop.

## Features

- **51 Tool Modules**: Comprehensive coverage of Meraki Dashboard API
- **400+ Functions**: Complete API v1.61.0 implementation
- **Natural Language**: Ask questions in plain English
- **Local Only**: Designed for Claude Desktop integration
- **Safety Features**: Built-in protections for production environments

## Quick Start

1. **Install Claude Desktop**: Download from https://claude.ai/download

2. **Set up API Key**:
   ```bash
   export MERAKI_API_KEY="your-meraki-api-key"
   ```

3. **Configure Claude Desktop**:
   Edit `~/Library/Application Support/Claude/claude_desktop_config.json`:
   ```json
   {
     "mcpServers": {
       "meraki": {
         "command": "python",
         "args": ["/path/to/cisco-meraki-mcp-server-tvi/meraki_server.py"],
         "env": {
           "MERAKI_API_KEY": "your-api-key"
         }
       }
     }
   }
   ```

4. **Restart Claude Desktop**

## Documentation

- [Claude Desktop Usage Guide](docs/CLAUDE_DESKTOP_USAGE.md)
- [Daily Operations Guide](docs/DAILY_OPERATIONS_GUIDE.md)
- [Quick Reference Card](docs/QUICK_REFERENCE_CARD.md)
- [Test Guide](docs/TEST_GUIDE.md)
- [Safety Features](SAFETY_FEATURES.md)

## Testing

Run the comprehensive test suite:
```bash
python comprehensive_mcp_test_suite.py
```

Or test specific functionality:
```bash
python test_mcp_natural_language.py
```

## Branch Information

- **stdio** (this branch): For Claude Desktop local integration
- **sse**: For HTTP/SSE server (n8n, remote access)
- **main**: Stable release branch

## Support

For issues or questions:
- GitHub Issues: [your-repo/issues]
- Documentation: See docs/ directory
- API Reference: https://developer.cisco.com/meraki/api-v1/