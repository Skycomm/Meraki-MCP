#!/usr/bin/env python3
"""Test script for new MCP server tools"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from meraki_client import MerakiClient
from server.tools_traffic_shaping import (
    check_traffic_shaping_prerequisites,
    get_network_traffic_shaping_rules,
    get_traffic_shaping_application_categories,
    register_traffic_shaping_tools
)
from server.tools_firewall import (
    check_firewall_prerequisites,
    get_firewall_l3_rules,
    get_layer7_application_categories,
    register_firewall_tools
)
from server.tools_monitoring_dashboard import (
    check_monitoring_prerequisites,
    get_network_health_summary,
    register_monitoring_dashboard_tools
)
from mcp.server import FastMCP

# Initialize
meraki = MerakiClient()
app = FastMCP("test")

# Register tools
register_traffic_shaping_tools(app, meraki)
register_firewall_tools(app, meraki)
register_monitoring_dashboard_tools(app, meraki)

# Get South Perth network
try:
    orgs = meraki.get_organizations()
    org_id = orgs[0]['id']
    networks = meraki.get_organization_networks(org_id)
    
    # Find South Perth network
    network_id = None
    for net in networks:
        if 'south' in net['name'].lower() or 'perth' in net['name'].lower():
            network_id = net['id']
            network_name = net['name']
            break
    
    if not network_id:
        print("Could not find South Perth network")
        sys.exit(1)
        
    print(f"Testing tools on network: {network_name} ({network_id})")
    print("=" * 60)
    
    # Test Traffic Shaping Tools
    print("\n🚦 TRAFFIC SHAPING TOOLS TEST")
    print("-" * 40)
    
    print("\n1. Check prerequisites:")
    result = check_traffic_shaping_prerequisites(network_id)
    print(result[:500] + "..." if len(result) > 500 else result)
    
    print("\n2. Get current rules:")
    result = get_network_traffic_shaping_rules(network_id)
    print(result[:500] + "..." if len(result) > 500 else result)
    
    print("\n3. Get application categories:")
    result = get_traffic_shaping_application_categories()
    print(result[:500] + "..." if len(result) > 500 else result)
    
    # Test Firewall Tools
    print("\n\n🔥 FIREWALL TOOLS TEST")
    print("-" * 40)
    
    print("\n1. Check prerequisites:")
    result = check_firewall_prerequisites(network_id)
    print(result[:500] + "..." if len(result) > 500 else result)
    
    print("\n2. Get L3 rules:")
    result = get_firewall_l3_rules(network_id)
    print(result[:500] + "..." if len(result) > 500 else result)
    
    print("\n3. Get L7 categories:")
    result = get_layer7_application_categories()
    print(result[:500] + "..." if len(result) > 500 else result)
    
    # Test Monitoring Dashboard
    print("\n\n📊 MONITORING DASHBOARD TEST")
    print("-" * 40)
    
    print("\n1. Check prerequisites:")
    result = check_monitoring_prerequisites(network_id)
    print(result[:500] + "..." if len(result) > 500 else result)
    
    print("\n2. Get health summary:")
    result = get_network_health_summary(network_id, timespan=300)
    print(result[:500] + "..." if len(result) > 500 else result)
    
    print("\n\n✅ All tests completed!")
    
except Exception as e:
    print(f"❌ Error during testing: {e}")
    import traceback
    traceback.print_exc()