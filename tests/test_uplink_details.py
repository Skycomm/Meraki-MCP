#!/usr/bin/env python3
"""Get detailed uplink status for Murdoch network"""

import os
import json
os.environ['MERAKI_API_KEY'] = '1ac5962056ad56da8cea908864f136adc5878a43'

from server.main import app, meraki

# Test with Kids ENT organization ID
org_id = "669347494617941203"

try:
    uplink_statuses = meraki.dashboard.appliance.getOrganizationApplianceUplinkStatuses(org_id)
    
    for status in uplink_statuses:
        print(f"\n📍 Network: {status.get('networkName', 'Unknown')}")
        print(f"   Network ID: {status.get('networkId')}")
        print(f"   Serial: {status.get('serial')}")
        print(f"   Model: {status.get('model')}")
        print(f"   High Availability: {status.get('highAvailability', {})}")
        
        print("\n   Uplinks:")
        for uplink in status.get('uplinks', []):
            print(f"\n   {uplink.get('interface', 'Unknown')}:")
            print(f"     Status: {uplink.get('status')}")
            print(f"     IP: {uplink.get('ip')}")
            print(f"     Gateway: {uplink.get('gateway')}")
            print(f"     Public IP: {uplink.get('publicIp')}")
            print(f"     DNS: {uplink.get('dns')}")
            print(f"     VLAN: {uplink.get('vlan')}")
            print(f"     Using Static IP: {uplink.get('usingStaticIp')}")
            
except Exception as e:
    print(f"Error: {str(e)}")
