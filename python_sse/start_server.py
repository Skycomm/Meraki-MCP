#!/usr/bin/env python3
"""
Start the Meraki MCP SSE/HTTP Server
"""

import os
import sys
from pathlib import Path

# Load environment variables from .env file if it exists
from dotenv import load_dotenv
env_path = Path(__file__).parent / '.env'
load_dotenv(env_path)

# Add src to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# Check for required environment variables
if not os.getenv("MERAKI_API_KEY"):
    print("ERROR: MERAKI_API_KEY environment variable not set!")
    print("\nPlease set it using:")
    print('  export MERAKI_API_KEY="your-api-key-here"')
    print("\nOr create a .env file with:")
    print('  MERAKI_API_KEY=your-api-key-here')
    sys.exit(1)

# Start the server
print("Starting Cisco Meraki MCP SSE/HTTP Server...")
print(f"Server will be available at: http://localhost:8000")
print("\nEndpoints:")
print("  - SSE: http://localhost:8000/sse")
print("  - REST API: http://localhost:8000/api/v1/tools")
print("  - Auth: POST http://localhost:8000/auth")
print("\nPress Ctrl+C to stop the server")

import uvicorn
from server import app

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)