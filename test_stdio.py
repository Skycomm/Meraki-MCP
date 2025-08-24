#!/usr/bin/env python3
"""Test script to verify stdio communication"""

import json
import sys

# Test initialize request
test_request = {
    "jsonrpc": "2.0",
    "method": "initialize",
    "params": {
        "protocolVersion": "1.0.0",
        "capabilities": {},
        "clientInfo": {
            "name": "test",
            "version": "1.0.0"
        }
    },
    "id": 1
}

print("Sending test request:", json.dumps(test_request), file=sys.stderr)

# Send request
print(json.dumps(test_request))
sys.stdout.flush()

# Read response
response = input()
print("Received response:", response, file=sys.stderr)

# Parse and verify response
try:
    resp_data = json.loads(response)
    if "result" in resp_data:
        print("✅ Server initialized successfully!", file=sys.stderr)
        print("Server info:", resp_data["result"]["serverInfo"], file=sys.stderr)
    else:
        print("❌ Initialization failed:", resp_data, file=sys.stderr)
except Exception as e:
    print("❌ Error parsing response:", e, file=sys.stderr)