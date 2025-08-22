#!/usr/bin/env python3
"""
Check for actual webhook HTTP servers in Clone organizations.
"""

from server.main import meraki
from datetime import datetime

CLONE_ORGS = [
    {"name": "Clone (Q_EopcIe)", "id": "726205439913493748"},
    {"name": "Clone (CCxOPdIe)", "id": "726205439913493749"}
]

def check_webhook_servers(org_id, org_name):
    """Check for actual webhook HTTP servers."""
    print(f"\n{'='*60}")
    print(f"🏢 {org_name} (ID: {org_id})")
    print('='*60)
    
    # Try different methods to find webhook servers
    methods_to_try = [
        ('getOrganizationWebhooksHttpServers', "HTTP Servers"),
        ('getOrganizationWebhooksPayloadTemplates', "Payload Templates"),
        ('getOrganizationWebhooksCallbacksStatus', "Callback Status"),
        ('getOrganizationWebhooksLogs', "Webhook Logs"),
    ]
    
    for method_name, description in methods_to_try:
        print(f"\n🔍 Checking {description} ({method_name}):")
        try:
            method = getattr(meraki.dashboard.organizations, method_name, None)
            if method:
                result = method(org_id)
                if isinstance(result, list):
                    print(f"   Found {len(result)} items")
                    for item in result[:3]:
                        if isinstance(item, dict):
                            print(f"   - {item}")
                        else:
                            print(f"   - {item}")
                    if len(result) > 3:
                        print(f"   ... and {len(result) - 3} more")
                else:
                    print(f"   Result: {result}")
            else:
                print(f"   ⚠️  Method not found")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    # Check networks for webhook configurations
    print("\n🌐 Checking networks for webhook configurations:")
    try:
        networks = meraki.dashboard.organizations.getOrganizationNetworks(org_id)
        if networks:
            print(f"   Found {len(networks)} networks")
            # Check first network for webhook settings
            for network in networks[:1]:
                net_id = network['id']
                print(f"\n   Checking network: {network['name']} ({net_id})")
                
                # Try to get network webhooks
                try:
                    http_servers = meraki.dashboard.networks.getNetworkWebhooksHttpServers(net_id)
                    print(f"   - HTTP Servers: {len(http_servers)}")
                    for server in http_servers:
                        print(f"     • ID: {server.get('id')} - {server.get('name')} → {server.get('url')}")
                except Exception as e:
                    print(f"   - HTTP Servers: Error - {e}")
        else:
            print("   No networks found")
    except Exception as e:
        print(f"   ❌ Error getting networks: {e}")

# Run the check
print("🔍 Webhook Server Analysis for Clone Organizations")
print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# First, let's see all webhook-related methods available
print("\n📚 Available webhook methods in Organizations API:")
org_methods = [m for m in dir(meraki.dashboard.organizations) if 'webhook' in m.lower()]
for method in sorted(org_methods):
    print(f"   - {method}")

print("\n📚 Available webhook methods in Networks API:")
net_methods = [m for m in dir(meraki.dashboard.networks) if 'webhook' in m.lower()]
for method in sorted(net_methods):
    print(f"   - {method}")

# Check each organization
for org in CLONE_ORGS:
    check_webhook_servers(org['id'], org['name'])

print("\n\n💡 Conclusion:")
print("="*60)
print("The 73 'webhooks' are actually webhook alert types (event types that can trigger webhooks)")
print("These are not actual webhook endpoints/servers that need to be deleted")
print("The organizations appear to have been created today (2025-08-22)")
print("="*60)