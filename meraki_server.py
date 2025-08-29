#!/usr/bin/env python3
"""
Cisco Meraki MCP Server - Main entry point.

SAFETY FEATURES:
- All destructive operations require user confirmation
- Read-only mode available (MCP_READ_ONLY_MODE=true)
- Audit logging enabled by default
- See SAFETY_FEATURES.md for details

API PAGINATION LIMITS:
- Most Meraki endpoints support perPage: 3-1000
- Some "statuses" endpoints are limited to perPage: 3-500
  - getNetworkWirelessMeshStatuses: max 500
  - getOrganizationWirelessSsidsStatusesByDevice: max 500
- Always check specific endpoint documentation before changing pagination
"""

from server.main import app

if __name__ == "__main__":
    app.run()
