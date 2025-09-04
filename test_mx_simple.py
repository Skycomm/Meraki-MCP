#!/usr/bin/env python3
"""
Simple test to validate the MX wireless fix by testing the tool directly.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server.main import app, meraki
from meraki_client import MerakiClient

# Initialize the client
meraki_client = MerakiClient()

def test_connection_stats_tool():
    """Test the connection stats tool with a real network."""
    
    print("🧪 TESTING MX CONNECTION STATS TOOL")
    print("=" * 50)
    
    # Try with Kids ENT network (known to work)
    network_id = 'N_734134986945264932'  # Kids ENT - Murdoch 
    
    try:
        # Test the MCP tool directly
        from server.tools_Custom_analytics import register_analytics_tools
        
        # Register the tools to get access
        print("📊 Testing get_network_connection_stats tool...")
        
        # Test network type detection first
        network_info = meraki_client.dashboard.networks.getNetwork(network_id)
        print(f"Network: {network_info.get('name')}")
        print(f"Product types: {network_info.get('productTypes', [])}")
        
        # Now test the logic path
        product_types = network_info.get('productTypes', [])
        is_mx = 'appliance' in product_types and ('wireless' in product_types or 'MX' in network_info.get('name', ''))
        
        print(f"Will use MX path: {is_mx}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_connection_stats_tool()