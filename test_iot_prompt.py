#!/usr/bin/env python3
"""
Test script to simulate the IoT review prompt
"""

import json
import subprocess
import sys

def send_request(proc, method, params, req_id):
    """Send a JSON-RPC request and return the response"""
    request = json.dumps({
        'jsonrpc': '2.0',
        'method': method,
        'params': params,
        'id': req_id
    })
    
    proc.stdin.write(request + '\n')
    proc.stdin.flush()
    
    # Read response
    while True:
        line = proc.stdout.readline()
        if not line:
            break
        try:
            response = json.loads(line)
            if response.get('id') == req_id:
                return response
        except json.JSONDecodeError:
            continue
    return None

def main():
    # Start the server
    proc = subprocess.Popen(
        [sys.executable, 'meraki_server.py'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    try:
        # Initialize
        print("Initializing...")
        init_resp = send_request(proc, 'initialize', {
            'protocolVersion': '0.1.0',
            'capabilities': {}
        }, 1)
        
        if init_resp:
            print(f"Initialized: {init_resp.get('result', {}).get('serverInfo', {}).get('name', 'Unknown')}")
        
        # List tools to check for long names
        print("\nListing tools...")
        tools_resp = send_request(proc, 'tools/list', {}, 2)
        
        if tools_resp:
            tools = tools_resp.get('result', {}).get('tools', [])
            print(f"Total tools: {len(tools)}")
            
            # Check for long tool names
            long_tools = []
            for i, tool in enumerate(tools):
                name = tool.get('name', '')
                if len(name) > 60:
                    long_tools.append((i, len(name), name))
            
            if long_tools:
                print("\nTools with long names (>60 chars):")
                for idx, length, name in long_tools:
                    print(f"  Tool {idx}: {name} ({length} chars)")
            else:
                print("No tools with names >60 characters found")
                
            # Find tool at index 277
            if len(tools) > 277:
                tool_277 = tools[277]
                name_277 = tool_277.get('name', '')
                print(f"\nTool at index 277: {name_277} ({len(name_277)} chars)")
                print(f"Description: {tool_277.get('description', '')[:100]}...")
            
        # Now simulate the IoT review request
        print("\n\nSimulating IoT review request...")
        
        # First, list organizations
        print("1. Listing organizations...")
        org_resp = send_request(proc, 'tools/call', {
            'name': 'list_organizations',
            'arguments': {}
        }, 3)
        
        if org_resp and not org_resp.get('error'):
            print("   ✓ Organizations listed successfully")
        else:
            print(f"   ✗ Error: {org_resp.get('error', 'Unknown')}")
        
    finally:
        proc.terminate()
        proc.wait()

if __name__ == '__main__':
    main()