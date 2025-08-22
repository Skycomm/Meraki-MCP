#!/usr/bin/env python3
"""
Get detailed information about Clone organizations including creation time.
"""

from server.main import meraki
from datetime import datetime
import json

CLONE_ORGS = [
    {"name": "Clone (Q_EopcIe)", "id": "726205439913493748"},
    {"name": "Clone (CCxOPdIe)", "id": "726205439913493749"}
]

def check_org_details(org_id, org_name):
    """Get all possible details about an organization."""
    print(f"\n{'='*60}")
    print(f"🏢 {org_name} (ID: {org_id})")
    print('='*60)
    
    # 1. Basic organization info
    print("\n📋 Organization Details:")
    try:
        org = meraki.dashboard.organizations.getOrganization(org_id)
        print(f"   Name: {org.get('name')}")
        print(f"   ID: {org.get('id')}")
        print(f"   URL: {org.get('url')}")
        print(f"   API Enabled: {org.get('api', {}).get('enabled')}")
        print(f"   Cloud Region: {org.get('cloud', {}).get('region', {}).get('name')}")
        
        # Check for any timestamp fields
        for key, value in org.items():
            if 'time' in key.lower() or 'date' in key.lower() or 'created' in key.lower():
                print(f"   {key}: {value}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # 2. Check API request logs to find earliest activity
    print("\n🕒 API Request History (looking for earliest activity):")
    try:
        # Get API requests for last 30 days (max allowed)
        timespan = 30 * 24 * 60 * 60  # 30 days in seconds
        api_requests = meraki.dashboard.organizations.getOrganizationApiRequests(
            org_id, 
            timespan=timespan,
            perPage=1000
        )
        
        if api_requests:
            # Find earliest request
            earliest = min(api_requests, key=lambda x: x.get('ts', float('inf')))
            latest = max(api_requests, key=lambda x: x.get('ts', 0))
            
            print(f"   Total requests in last 30 days: {len(api_requests)}")
            print(f"   Earliest request: {earliest.get('ts')} - {earliest.get('path')}")
            print(f"   Latest request: {latest.get('ts')} - {latest.get('path')}")
            
            # Check for organization creation requests
            create_requests = [r for r in api_requests if 'create' in r.get('operation', '').lower() or 'clone' in r.get('path', '').lower()]
            if create_requests:
                print(f"\n   Found {len(create_requests)} creation-related requests:")
                for req in create_requests[:3]:
                    print(f"   - {req.get('ts')} - {req.get('operation')} {req.get('path')}")
        else:
            print("   No API requests found in last 30 days")
            
    except Exception as e:
        print(f"   ❌ Error getting API requests: {e}")
    
    # 3. Check action batches (might show clone operation)
    print("\n🔄 Action Batches:")
    try:
        batches = meraki.dashboard.organizations.getOrganizationActionBatches(org_id)
        if batches:
            print(f"   Found {len(batches)} action batches")
            for batch in batches[:3]:
                print(f"   - {batch.get('id')} - Status: {batch.get('status', {}).get('completed')}/{batch.get('status', {}).get('total')}")
                if batch.get('actions'):
                    print(f"     Actions: {len(batch['actions'])}")
        else:
            print("   No action batches found")
    except Exception as e:
        print(f"   ❌ Error getting action batches: {e}")
    
    # 4. Check inventory to see if devices were added
    print("\n📦 Inventory History:")
    try:
        devices = meraki.dashboard.organizations.getOrganizationInventoryDevices(org_id)
        if devices:
            print(f"   Total devices in inventory: {len(devices)}")
            # Check claimed dates
            claimed_dates = [d.get('claimedAt') for d in devices if d.get('claimedAt')]
            if claimed_dates:
                print(f"   Earliest device claim: {min(claimed_dates)}")
                print(f"   Latest device claim: {max(claimed_dates)}")
        else:
            print("   No devices in inventory")
    except Exception as e:
        print(f"   ❌ Error getting inventory: {e}")
    
    # 5. Check change log
    print("\n📝 Configuration Changes:")
    try:
        # Try to get change log (last 30 days)
        timespan = 30 * 24 * 60 * 60
        changes = meraki.dashboard.organizations.getOrganizationConfigurationChanges(
            org_id,
            timespan=timespan,
            perPage=1000
        )
        
        if changes:
            print(f"   Total changes in last 30 days: {len(changes)}")
            # Find earliest change
            earliest = min(changes, key=lambda x: x.get('ts', float('inf')))
            latest = max(changes, key=lambda x: x.get('ts', 0))
            
            print(f"   Earliest change: {earliest.get('ts')} - {earliest.get('label')}")
            print(f"   Latest change: {latest.get('ts')} - {latest.get('label')}")
            
            # Look for organization creation
            org_changes = [c for c in changes if 'organization' in c.get('label', '').lower()]
            if org_changes:
                print(f"\n   Organization-related changes:")
                for change in org_changes[:3]:
                    print(f"   - {change.get('ts')} - {change.get('label')}")
        else:
            print("   No configuration changes found in last 30 days")
            
    except Exception as e:
        print(f"   ❌ Error getting configuration changes: {e}")

# Run analysis
print("🔍 Detailed Analysis of Clone Organizations")
print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

for org in CLONE_ORGS:
    check_org_details(org['id'], org['name'])

print("\n\n💡 Summary:")
print("="*60)
print("Based on the analysis, we're looking for:")
print("1. Creation timestamps in API logs or configuration changes")
print("2. Webhook HTTP servers (not alert types)")
print("3. Any actual webhook configurations that need cleanup")
print("="*60)