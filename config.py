"""
Configuration utilities for the Cisco Meraki MCP Server.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
env_path = Path(__file__).parent / ".env"
if env_path.exists():
    load_dotenv(env_path)

# Get API key from environment variable
MERAKI_API_KEY = os.getenv("MERAKI_API_KEY")
if not MERAKI_API_KEY:
    raise EnvironmentError(
        "MERAKI_API_KEY environment variable not set. "
        "Please set this variable to your Meraki API key."
    )

# API configuration
API_BASE_URL = "https://api.meraki.com/api/v1"
TIMEOUT = 600  # Request timeout in seconds (10 minutes max for MCP)

# MCP server configuration
SERVER_NAME = "meraki-mcp-server"
SERVER_VERSION = "1.0.0"

# Safety features
MCP_READ_ONLY_MODE = os.getenv("MCP_READ_ONLY_MODE", "false").lower() == "true"
MCP_REQUIRE_CONFIRMATIONS = os.getenv("MCP_REQUIRE_CONFIRMATIONS", "true").lower() == "true"
MCP_AUDIT_LOGGING = os.getenv("MCP_AUDIT_LOGGING", "true").lower() == "true"

# Show safety mode status
if MCP_READ_ONLY_MODE:
    print("\n" + "="*60)
    print("🔒 MCP SERVER RUNNING IN READ-ONLY MODE")
    print("All write operations are BLOCKED")
    print("To enable writes, unset MCP_READ_ONLY_MODE")
    print("="*60 + "\n")
