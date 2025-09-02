#!/usr/bin/env python3
"""
Test HTTP/SSE server profiles to verify they work correctly.
"""

import requests
import json
import time
import subprocess
import os
import signal

def test_profile(profile, port):
    """Test a single profile server."""
    print(f"\n{'='*60}")
    print(f"Testing {profile} profile on port {port}")
    print('='*60)
    
    # Set environment variables
    env = os.environ.copy()
    env.update({
        'MCP_PROFILE': profile,
        'SERVER_PORT': str(port),
        'MERAKI_API_KEY': '1ac5962056ad56da8cea908864f136adc5878a43',
        'AUTH_TOKENS_ADMIN': f'admin-{profile.lower()}-token',
        'AUTH_TOKENS_READONLY': f'readonly-{profile.lower()}-token',
        'MCP_READ_ONLY_MODE': 'false'
    })
    
    # Start server
    proc = subprocess.Popen(
        ['.venv/bin/python', 'http_server.py'],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    
    # Wait for server to start
    time.sleep(3)
    
    try:
        # Test health endpoint
        health_url = f'http://localhost:{port}/health'
        health_response = requests.get(health_url, timeout=2)
        print(f"✅ Health check: {health_response.json()}")
        
        # Test list_tools endpoint
        tools_url = f'http://localhost:{port}/mcp'
        headers = {
            'Authorization': f'Bearer admin-{profile.lower()}-token',
            'Content-Type': 'application/json'
        }
        
        tools_response = requests.post(
            tools_url,
            json={'action': 'list_tools'},
            headers=headers,
            timeout=5
        )
        
        tools_data = tools_response.json()
        if tools_data.get('ok'):
            tool_count = len(tools_data.get('tools', []))
            print(f"✅ Tools loaded: {tool_count}")
            
            # Show first 5 tools as sample
            sample_tools = tools_data.get('tools', [])[:5]
            if sample_tools:
                print(f"   Sample tools: {', '.join(sample_tools)}")
        else:
            print(f"❌ Error listing tools: {tools_data.get('error')}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        # Stop server
        proc.terminate()
        try:
            proc.wait(timeout=2)
        except subprocess.TimeoutExpired:
            proc.kill()
        print(f"🛑 Server stopped")

def main():
    """Test all profiles."""
    print("🔍 Testing Meraki MCP HTTP/SSE Server Profiles")
    
    profiles = [
        ('ORGANIZATIONS', 8003),
        ('WIRELESS', 8001),
        ('NETWORK', 8002),
        ('MONITORING', 8004),
        ('MINIMAL', 8005),  # Test minimal profile too
    ]
    
    for profile, port in profiles:
        test_profile(profile, port)
        time.sleep(1)  # Brief pause between tests
    
    print("\n" + "="*60)
    print("✅ All profile tests completed!")
    print("\nNote: FULL profile (833 tools) skipped to avoid timeout")
    print("To test FULL profile manually: ./run_http_full.sh")

if __name__ == '__main__':
    main()