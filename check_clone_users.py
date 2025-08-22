#!/usr/bin/env python3
"""
Check users/administrators for the Clone organizations.
Run this directly: python check_clone_users.py
"""

from server.main import meraki
from datetime import datetime

# Clone organizations
CLONE_ORGS = [
    {"name": "Clone (Q_EopcIe)", "id": "726205439913493748"},
    {"name": "Clone (CCxOPdIe)", "id": "726205439913493749"}
]

print("👥 Clone Organizations - User Check")
print("=" * 60)
print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 60)

for org in CLONE_ORGS:
    print(f"\n🏢 Organization: {org['name']}")
    print(f"   ID: {org['id']}")
    print("-" * 40)
    
    try:
        # Get administrators
        admins = meraki.dashboard.organizations.getOrganizationAdmins(org['id'])
        
        print(f"   Total administrators: {len(admins)}")
        print("\n   Administrators:")
        
        for i, admin in enumerate(admins, 1):
            print(f"\n   {i}. {admin.get('name', 'Unknown')}")
            print(f"      Email: {admin.get('email', 'N/A')}")
            print(f"      Auth: {admin.get('authenticationMethod', 'N/A')}")
            print(f"      2FA: {'Yes' if admin.get('twoFactorAuthEnabled') else 'No'}")
            print(f"      Status: {admin.get('accountStatus', 'N/A')}")
            print(f"      Org Access: {admin.get('orgAccess', 'N/A')}")
            
            # Check last active
            last_active = admin.get('lastActive')
            if last_active:
                print(f"      Last Active: {last_active}")
            else:
                print(f"      Last Active: Never")
                
    except Exception as e:
        print(f"   ❌ Error getting administrators: {str(e)}")

print("\n" + "=" * 60)
print("💡 Note: Organizations can only be deleted when they have 1 user (you)")
print("   These Clone orgs have multiple users, preventing deletion.")