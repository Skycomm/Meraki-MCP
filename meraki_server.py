#!/usr/bin/env python3
"""
Cisco Meraki MCP Server - Main entry point.

SAFETY FEATURES:
- All destructive operations require user confirmation
- Read-only mode available (MCP_READ_ONLY_MODE=true)
- Audit logging enabled by default
- See SAFETY_FEATURES.md for details
"""

from server.main import app

if __name__ == "__main__":
    app.run()
