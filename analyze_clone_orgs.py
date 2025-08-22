#!/usr/bin/env python3
"""
Deep analysis of Clone organizations to understand their purpose.
"""

from server.main import meraki
from datetime import datetime

CLONE_ORGS = [
    {"name": "Clone (Q_EopcIe)", "id": "726205439913493748"},
    {"name": "Clone (CCxOPdIe)", "id": "726205439913493749"}
]

# Also check main Skycomm org for comparison
SKYCOMM_ORG_ID = "686470"  # Main Skycomm organization

def check_organization_settings(org_id, org_name):
    """Check all settings for an organization."""
    print(f"\n{'='*60}")
    print(f"🏢 {org_name} (ID: {org_id})")
    print('='*60)
    
    # 1. Networks
    try:
        networks = meraki.get_organization_networks(org_id)
        print(f"\n📡 Networks: {len(networks)}")
        if networks:
            for net in networks[:3]:  # Show first 3
                print(f"   - {net['name']} ({net['id']})")
    except Exception as e:
        print(f"   ❌ Error getting networks: {e}")
    
    # 2. Devices
    try:
        devices = meraki.dashboard.organizations.getOrganizationDevices(org_id)
        print(f"\n📱 Devices in inventory: {len(devices)}")
        if devices:
            device_types = {}
            for device in devices:
                model = device.get('model', 'Unknown')
                device_types[model] = device_types.get(model, 0) + 1
            print("   Device types:")
            for model, count in device_types.items():
                print(f"   - {model}: {count}")
    except Exception as e:
        print(f"   ❌ Error getting devices: {e}")
    
    # 3. Alerts
    try:
        alerts = meraki.get_organization_alerts(org_id)
        print(f"\n🚨 Alert profiles: {len(alerts)}")
        if alerts:
            for alert in alerts[:3]:
                print(f"   - Type: {alert.get('type', 'Unknown')}")
    except Exception as e:
        print(f"   ❌ Error getting alerts: {e}")
    
    # 4. Webhooks
    try:
        webhooks = meraki.get_organization_webhooks(org_id)
        print(f"\n🔗 Webhooks: {len(webhooks)}")
        if webhooks:
            for webhook in webhooks:
                print(f"   - {webhook.get('name', 'Unnamed')} → {webhook.get('url', 'No URL')}")
    except Exception as e:
        print(f"   ❌ Error getting webhooks: {e}")
    
    # 5. Firmware settings
    try:
        firmware = meraki.get_organization_firmware_upgrades(org_id)
        print(f"\n💿 Firmware upgrade settings: {len(firmware)}")
    except Exception as e:
        print(f"   ❌ Error getting firmware: {e}")
    
    # 6. Licenses
    try:
        licenses = meraki.dashboard.organizations.getOrganizationLicenses(org_id)
        print(f"\n📜 Licenses: {len(licenses)}")
        if licenses:
            license_states = {}
            for lic in licenses:
                state = lic.get('state', 'Unknown')
                license_states[state] = license_states.get(state, 0) + 1
            for state, count in license_states.items():
                print(f"   - {state}: {count}")
    except Exception as e:
        print(f"   ❌ Error getting licenses: {e}")
    
    # 7. Policy objects
    try:
        policy_objects = meraki.dashboard.organizations.getOrganizationPolicyObjects(org_id)
        print(f"\n📋 Policy objects: {len(policy_objects)}")
    except Exception as e:
        print(f"   ❌ Error getting policy objects: {e}")
    
    # 8. Configuration templates
    try:
        templates = meraki.dashboard.organizations.getOrganizationConfigTemplates(org_id)
        print(f"\n📐 Configuration templates: {len(templates)}")
        if templates:
            for template in templates:
                print(f"   - {template.get('name', 'Unnamed')}")
    except Exception as e:
        print(f"   ❌ Error getting templates: {e}")

print("🔍 Deep Analysis of Clone Organizations")
print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Check each Clone organization
for org in CLONE_ORGS:
    check_organization_settings(org['id'], org['name'])

# Check main Skycomm for comparison
print("\n\n📊 For comparison - Main Skycomm Organization:")
check_organization_settings(SKYCOMM_ORG_ID, "Skycomm (Main)")

print("\n\n💡 Analysis Summary:")
print("="*60)
print("Clone organizations typically inherit:")
print("- Administrator list from source organization")
print("- License allocation")
print("- Some organization-wide settings")
print("\nThey usually DON'T copy:")
print("- Networks")
print("- Devices (but may show in inventory if shared licenses)")
print("- Alert configurations")
print("- Webhooks")
print("="*60)