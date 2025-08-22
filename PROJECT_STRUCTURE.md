# Cisco Meraki MCP Server - Project Structure

## Directory Layout

```
cisco-meraki-mcp-server-tvi/
├── README.md                 # Main documentation
├── SAFETY_FEATURES.md        # Safety features documentation
├── LICENSE                   # Project license
├── requirements.txt          # Python dependencies
├── config.py                 # Configuration and environment variables
├── meraki_server.py          # Main entry point
├── meraki_client.py          # Meraki API client wrapper
├── docker-compose.yml        # Docker configuration
├── Dockerfile               # Docker build file
│
├── server/                  # Server implementation
│   ├── __init__.py
│   ├── main.py             # MCP server initialization
│   ├── resources.py        # Resource handlers
│   ├── tools_alerts.py     # Alert management tools
│   ├── tools_analytics.py  # Analytics tools
│   ├── tools_appliance.py  # Appliance tools
│   ├── tools_beta.py       # Beta features
│   ├── tools_camera.py     # Camera tools
│   ├── tools_devices.py    # Device management tools
│   ├── tools_licensing.py  # License management
│   ├── tools_live.py       # Live tools
│   ├── tools_monitoring.py # Monitoring tools
│   ├── tools_networks.py   # Network management tools
│   ├── tools_organizations.py # Organization tools
│   ├── tools_policy.py     # Policy management
│   ├── tools_sm.py         # Systems Manager tools
│   ├── tools_switch.py     # Switch tools
│   └── tools_wireless.py   # Wireless tools
│
├── utils/                   # Utility functions
│   ├── __init__.py
│   └── helpers.py          # Helper functions and safety features
│
├── certs/                  # SSL certificates (git-ignored)
│   ├── cert.pem
│   └── key.pem
│
├── docs/                   # Documentation
│   └── [various .md files]
│
├── scripts/                # Utility scripts
│   ├── install_in_claude.sh
│   ├── run_meraki_server.sh
│   └── setup_github_secure.sh
│
├── tests/                  # Test scripts
│   └── [test_*.py files]
│
├── python_sse/             # SSE version (separate branch)
│   └── [SSE implementation]
│
└── logs/                   # Audit logs (git-ignored)
    └── meraki_mcp_audit.log
```

## Key Files

### Core Server Files
- `meraki_server.py` - Entry point, imports from server/main.py
- `config.py` - Environment configuration including safety features
- `meraki_client.py` - Meraki Dashboard API client wrapper

### Safety Features
- `utils/helpers.py` - Contains `require_confirmation()` and `log_operation()`
- `SAFETY_FEATURES.md` - Documentation of all safety features

### Tool Modules
Each `tools_*.py` file in the server/ directory contains related API tools:
- Organizations, networks, devices
- Wireless, switching, appliance
- Monitoring, analytics, alerts
- Systems Manager (SM/MDM)
- Beta features and live tools

## Environment Variables

### Required
- `MERAKI_API_KEY` - Your Meraki Dashboard API key

### Safety Features (Optional)
- `MCP_READ_ONLY_MODE` - Set to "true" for read-only mode
- `MCP_REQUIRE_CONFIRMATIONS` - Set to "false" to disable confirmations (not recommended)
- `MCP_AUDIT_LOGGING` - Set to "false" to disable audit logging

## Running the Server

### Direct Python
```bash
python meraki_server.py
```

### Using Docker
```bash
docker-compose up
```

### Using the run script
```bash
./scripts/run_meraki_server.sh
```