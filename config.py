"""
Configuration utilities for the Cisco Meraki MCP Server.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).parent / ".env"
if env_path.exists():
    load_dotenv(env_path)

MERAKI_API_KEY = os.getenv("MERAKI_API_KEY") or os.getenv("Meraki_API") or ""

API_BASE_URL = "https://api.meraki.com/api/v1"
TIMEOUT = 600

SERVER_NAME = "meraki-mcp-server"
SERVER_VERSION = "1.0.0"

SERVER_HOST = os.getenv("SERVER_HOST", "0.0.0.0")
SERVER_PORT = int(os.getenv("SERVER_PORT", "8000"))

MCP_READ_ONLY_MODE = os.getenv("MCP_READ_ONLY_MODE", "false").lower() == "true"
MCP_REQUIRE_CONFIRMATIONS = os.getenv("MCP_REQUIRE_CONFIRMATIONS", "true").lower() == "true"
MCP_AUDIT_LOGGING = os.getenv("MCP_AUDIT_LOGGING", "true").lower() == "true"
