# HTTP/SSE Server Setup with Profiles

## Overview
Your Claude Desktop is now configured to use HTTP/SSE servers with different profiles to avoid the ~850 tool limit. Each profile runs on a different port and provides focused functionality.

## Quick Start

### Start All Servers
```bash
./start_all_http_servers.sh
```

This starts 5 servers:
- **Port 8001**: Wireless (136 tools)
- **Port 8002**: Network (294 tools)  
- **Port 8003**: Organizations (126 tools)
- **Port 8004**: Monitoring (147 tools)
- **Port 8000**: Full (833 tools)

### Stop All Servers
```bash
./stop_all_http_servers.sh
```

## Claude Desktop Configuration

Your Claude Desktop config has been updated with 5 MCP servers:

| Server Name | Port | Tools | Focus |
|------------|------|-------|-------|
| meraki-wireless | 8001 | ~136 | Wireless, RF, SSIDs |
| meraki-network | 8002 | ~294 | Switch, Appliance, VPN |
| meraki-organizations | 8003 | ~126 | Org admin, policies |
| meraki-monitoring | 8004 | ~147 | Devices, cameras, analytics |
| meraki-full | 8000 | 833 | Everything (may hit limits) |

## Individual Server Control

Start specific servers as needed:

```bash
# Wireless only
./run_http_wireless.sh

# Network infrastructure  
./run_http_network.sh

# Organizations
./run_http_organizations.sh

# Monitoring
./run_http_monitoring.sh

# Full (all tools)
./run_http_full.sh
```

## Testing

### Health Check
```bash
curl http://localhost:8001/health
curl http://localhost:8002/health
curl http://localhost:8003/health
curl http://localhost:8004/health
curl http://localhost:8000/health
```

### List Tools
```bash
curl -H "Authorization: Bearer admin-wireless-token" \
     -H "Content-Type: application/json" \
     -d '{"action":"list_tools"}' \
     http://localhost:8001/mcp
```

### Test All Profiles
```bash
.venv/bin/python test_http_profiles.py
```

## Authentication Tokens

Each server uses different auth tokens for security:

| Profile | Admin Token | Readonly Token |
|---------|------------|----------------|
| Wireless | admin-wireless-token | readonly-wireless-token |
| Network | admin-network-token | readonly-network-token |
| Organizations | admin-org-token | readonly-org-token |
| Monitoring | admin-monitoring-token | readonly-monitoring-token |
| Full | admin-full-token | readonly-full-token |

## Logs

Server logs are stored in `logs/` directory:
- `logs/http_WIRELESS_8001.log`
- `logs/http_NETWORK_8002.log`
- `logs/http_ORGANIZATIONS_8003.log`
- `logs/http_MONITORING_8004.log`
- `logs/http_FULL_8000.log`

## Usage in Claude Desktop

1. **Restart Claude Desktop** after config change
2. You'll see 5 Meraki servers in the MCP menu
3. Enable the ones you need for your task
4. Each server works independently

## Benefits

✅ **Avoids tool limit** - Each profile stays well under 850 tools
✅ **Fast response** - Smaller tool sets load quickly
✅ **Focused functionality** - Use only what you need
✅ **Multiple servers** - Can use several profiles simultaneously
✅ **Ready for expansion** - Can add all SDK methods without hitting limits

## Troubleshooting

### Server won't start
- Check if port is already in use: `lsof -i :8001`
- Kill existing process: `pkill -f "python http_server.py"`
- Check logs in `logs/` directory

### Claude Desktop doesn't see servers
1. Restart Claude Desktop
2. Check config: `cat ~/Library/Application\ Support/Claude/claude_desktop_config.json`
3. Ensure servers are running: `curl http://localhost:8001/health`

### Tools not loading
- Check server logs: `tail -f logs/http_WIRELESS_8001.log`
- Verify profile is set: Look for "MCP Server Profile:" in logs
- Test with curl commands above

## Next Steps

You're now ready to:
1. Build out full SDK coverage without worrying about tool limits
2. Use focused profiles for better performance
3. Test all Meraki API functionality through Claude Desktop

The setup allows expanding to thousands of tools by using appropriate profiles!