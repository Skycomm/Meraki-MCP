#!/usr/bin/env python3
"""
Automatically remove other administrators from Clone organizations.
Keeps only david@skycomm.com.au as the sole admin.
"""

from server.main import meraki
from datetime import datetime
import time

CLONE_ORGS = [
    {"name": "Clone (Q_EopcIe)", "id": "726205439913493748"},
    {"name": "Clone (CCxOPdIe)", "id": "726205439913493749"}
]

YOUR_EMAIL = "david@skycomm.com.au"

print("🧹 Automatically Removing Administrators from Clone Organizations")
print("=" * 60)
print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"👤 Keeping only: {YOUR_EMAIL}")
print("=" * 60)

total_removed = 0
total_failed = 0

for org in CLONE_ORGS:
    print(f"\n🏢 Processing: {org['name']}")
    print(f"   ID: {org['id']}")
    print("-" * 40)
    
    try:
        # Get current administrators
        admins = meraki.dashboard.organizations.getOrganizationAdmins(org['id'])
        print(f"   Current administrators: {len(admins)}")
        
        # Find admins to remove (everyone except you)
        to_remove = []
        your_admin_id = None
        
        for admin in admins:
            if admin['email'] == YOUR_EMAIL:
                your_admin_id = admin['id']
                print(f"   ✅ Keeping: {admin['name']} ({admin['email']})")
            else:
                to_remove.append(admin)
                
        if not your_admin_id:
            print(f"   ❌ ERROR: Your account ({YOUR_EMAIL}) not found!")
            continue
            
        print(f"\n   Removing {len(to_remove)} administrators:")
        
        removed_count = 0
        for admin in to_remove:
            try:
                print(f"   - Removing {admin['name']} ({admin['email']})...", end=" ")
                # Delete the admin
                meraki.dashboard.organizations.deleteOrganizationAdmin(
                    org['id'], 
                    admin['id']
                )
                print("✅")
                removed_count += 1
                total_removed += 1
                # Small delay to avoid rate limiting
                time.sleep(0.5)
            except Exception as e:
                print(f"❌ Failed: {str(e)}")
                total_failed += 1
                
        print(f"\n   Summary: Removed {removed_count} of {len(to_remove)} administrators")
        
        # Verify final state
        print("   Verifying final state...")
        final_admins = meraki.dashboard.organizations.getOrganizationAdmins(org['id'])
        print(f"   Final administrator count: {len(final_admins)}")
        
        if len(final_admins) == 1:
            print("   ✅ Organization ready for deletion!")
        else:
            print(f"   ⚠️  Warning: Still has {len(final_admins)} administrators")
            
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")

print("\n" + "=" * 60)
print(f"📊 Final Results:")
print(f"   ✅ Successfully removed: {total_removed} administrators")
print(f"   ❌ Failed to remove: {total_failed} administrators")
print("\n💡 Next step: Run 'python delete_clone_orgs.py' to delete the organizations")
print("=" * 60)