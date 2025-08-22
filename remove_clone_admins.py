#!/usr/bin/env python3
"""
Remove other administrators from Clone organizations to prepare for deletion.
Only keeps david@skycomm.com.au (you) as the sole admin.
"""

from server.main import meraki
from datetime import datetime

CLONE_ORGS = [
    {"name": "Clone (Q_EopcIe)", "id": "726205439913493748"},
    {"name": "Clone (CCxOPdIe)", "id": "726205439913493749"}
]

YOUR_EMAIL = "david@skycomm.com.au"

print("🧹 Removing Administrators from Clone Organizations")
print("=" * 60)
print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"👤 Keeping only: {YOUR_EMAIL}")
print("=" * 60)

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
            
        # Confirm removal
        print(f"\n   Admins to remove ({len(to_remove)}):")
        for admin in to_remove:
            print(f"   - {admin['name']} ({admin['email']})")
        
        response = input(f"\n   Remove {len(to_remove)} admins from {org['name']}? (y/n): ").strip().lower()
        
        if response == 'y':
            removed_count = 0
            for admin in to_remove:
                try:
                    print(f"   Removing {admin['name']}...", end=" ")
                    # Delete the admin
                    meraki.dashboard.organizations.deleteOrganizationAdmin(
                        org['id'], 
                        admin['id']
                    )
                    print("✅")
                    removed_count += 1
                except Exception as e:
                    print(f"❌ Failed: {str(e)}")
                    
            print(f"\n   Summary: Removed {removed_count} of {len(to_remove)} administrators")
            
            # Verify final state
            final_admins = meraki.dashboard.organizations.getOrganizationAdmins(org['id'])
            print(f"   Final administrator count: {len(final_admins)}")
            
        else:
            print("   ❌ Skipped")
            
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")

print("\n" + "=" * 60)
print("✅ Admin removal complete!")
print("💡 You can now delete these organizations using delete_clone_orgs.py")