#!/usr/bin/env python3
"""Test new tools with any available MX network"""

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

# Find a network with MX device
print("Looking for networks with MX devices...")

try:
    orgs = meraki.get_organizations()
    mx_network = None
    
    for org in orgs[:10]:  # Check first 10 orgs
        try:
            networks = meraki.get_organization_networks(org['id'])
            for net in networks:
                if 'appliance' in net.get('productTypes', []):
                    # This network has an MX, let's use it
                    mx_network = net
                    org_name = org['name']
                    break
            if mx_network:
                break
        except Exception as e:
            continue
    
    if not mx_network:
        print("No network with MX device found")
        sys.exit(1)
    
    network_id = mx_network['id']
    network_name = mx_network['name']
    
    print(f"\nUsing network: {network_name} ({network_id})")
    print(f"Organization: {org_name}")
    print(f"Product types: {', '.join(mx_network.get('productTypes', []))}")
    print("=" * 60)
    
    # Test Traffic Shaping Tools
    print("\n🚦 TRAFFIC SHAPING TOOLS TEST")
    print("-" * 40)
    
    print("\n1. Check prerequisites:")
    try:
        result = check_traffic_shaping_prerequisites(network_id)
        print(result[:500] + "..." if len(result) > 500 else result)
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n2. Get current rules:")
    try:
        result = get_network_traffic_shaping_rules(network_id)
        print(result[:500] + "..." if len(result) > 500 else result)
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n3. Get application categories:")
    try:
        result = get_traffic_shaping_application_categories()
        print(result[:500] + "..." if len(result) > 500 else result)
    except Exception as e:
        print(f"Error: {e}")
    
    # Test Firewall Tools
    print("\n\n🔥 FIREWALL TOOLS TEST")
    print("-" * 40)
    
    print("\n1. Check prerequisites:")
    try:
        result = check_firewall_prerequisites(network_id)
        print(result[:500] + "..." if len(result) > 500 else result)
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n2. Get L3 rules:")
    try:
        result = get_firewall_l3_rules(network_id)
        print(result[:500] + "..." if len(result) > 500 else result)
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n3. Get L7 categories:")
    try:
        result = get_layer7_application_categories(network_id)
        print(result[:500] + "..." if len(result) > 500 else result)
    except Exception as e:
        print(f"Error: {e}")
    
    # Test Monitoring Dashboard
    print("\n\n📊 MONITORING DASHBOARD TEST")
    print("-" * 40)
    
    print("\n1. Check prerequisites:")
    try:
        result = check_monitoring_prerequisites(network_id)
        print(result[:500] + "..." if len(result) > 500 else result)
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n2. Get health summary (5 min):")
    try:
        result = get_network_health_summary(network_id, timespan=300)
        print(result[:800] + "..." if len(result) > 800 else result)
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n\n✅ All tests completed!")
    
except Exception as e:
    print(f"❌ Error during testing: {e}")
    import traceback
    traceback.print_exc()