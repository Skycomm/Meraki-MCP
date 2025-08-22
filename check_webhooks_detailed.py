#!/usr/bin/env python3
"""
Get detailed webhook information for Clone organizations.
"""

from server.main import meraki
from datetime import datetime

CLONE_ORGS = [
    {"name": "Clone (Q_EopcIe)", "id": "726205439913493748"},
    {"name": "Clone (CCxOPdIe)", "id": "726205439913493749"}
]

def check_webhooks_detailed(org_id, org_name):
    """Check webhook HTTP servers for an organization."""
    print(f"\n{'='*60}")
    print(f"🏢 {org_name} (ID: {org_id})")
    print('='*60)
    
    # Try to get webhook HTTP servers
    print("\n🔗 Checking webhook HTTP servers...")
    try:
        # Method 1: Try getOrganizationWebhooksHttpServers
        servers = meraki.dashboard.organizations.getOrganizationWebhooksHttpServers(org_id)
        print(f"Found {len(servers)} webhook HTTP servers:")
        for server in servers:
            print(f"\n   Server ID: {server.get('id', 'Unknown')}")
            print(f"   Name: {server.get('name', 'Unnamed')}")
            print(f"   URL: {server.get('url', 'No URL')}")
            print(f"   Shared Secret: {'Set' if server.get('sharedSecret') else 'Not set'}")
    except AttributeError:
        print("   ⚠️  getOrganizationWebhooksHttpServers method not found")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Check webhook alert types (what we got before)
    print("\n📋 Webhook Alert Types:")
    try:
        alert_types = meraki.dashboard.organizations.getOrganizationWebhooksAlertTypes(org_id)
        print(f"Found {len(alert_types)} alert types")
        # Show first 5
        for i, alert_type in enumerate(alert_types[:5]):
            print(f"   - {alert_type.get('alertTypeId', 'Unknown ID')}: {alert_type.get('name', 'Unnamed')}")
        if len(alert_types) > 5:
            print(f"   ... and {len(alert_types) - 5} more")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Try to check organization alerts configuration
    print("\n🚨 Alert Configuration:")
    try:
        alerts = meraki.dashboard.organizations.getOrganizationAlertsProfiles(org_id)
        print(f"Found {len(alerts)} alert profiles")
        for alert in alerts[:3]:
            print(f"   - {alert.get('description', 'No description')}")
            if 'alertCondition' in alert:
                print(f"     Condition: {alert['alertCondition']}")
            if 'recipients' in alert:
                print(f"     Recipients: {alert['recipients']}")
    except AttributeError:
        # Try alternative method
        try:
            # Check if there's a network-level webhook config
            networks = meraki.dashboard.organizations.getOrganizationNetworks(org_id)
            if networks:
                print(f"   ℹ️  Organization has {len(networks)} networks")
            else:
                print("   ℹ️  No networks in organization (checking org-level config only)")
        except Exception as e:
            print(f"   ❌ Error checking networks: {e}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

# Get organization info
print("🔍 Detailed Webhook Analysis for Clone Organizations")
print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Check available methods
print("\n📚 Checking available webhook methods in Meraki API...")
org_methods = [method for method in dir(meraki.dashboard.organizations) if 'webhook' in method.lower()]
print(f"Found {len(org_methods)} webhook-related methods:")
for method in org_methods:
    print(f"   - {method}")

# Check each Clone organization
for org in CLONE_ORGS:
    check_webhooks_detailed(org['id'], org['name'])

print("\n\n💡 Next Steps:")
print("="*60)
print("1. If webhook HTTP servers exist, we need their IDs to delete them")
print("2. The deleteOrganizationWebhooksHttpServer method should work with server ID")
print("3. Alert types are not the same as webhook servers")
print("="*60)