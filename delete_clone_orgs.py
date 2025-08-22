#!/usr/bin/env python3
"""
Delete the two empty Clone organizations with confirmations.
Run this directly: python delete_clone_orgs.py
"""

from server.main import meraki
from datetime import datetime

# List of clone organizations
CLONE_ORGS = [
    {"name": "Clone (Q_EopcIe)", "id": "726205439913493748"},
    {"name": "Clone (CCxOPdIe)", "id": "726205439913493749"}
]

print("🧹 Clone Organizations Cleanup")
print("=" * 60)
print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 60)

# Show the clone organizations
print("\n📋 Clone organizations to delete:")
for org in CLONE_ORGS:
    print(f"   - {org['name']} (ID: {org['id']})")

# Ask for confirmation
print("\n⚠️  WARNING: This will permanently delete these Clone organizations!")
print("Type 'DELETE' to confirm deletion")
print("Type anything else to cancel")

choice = input("\nYour choice: ").strip()

if choice == "DELETE":
    print("\n🗑️  Deleting clone organizations...")
    deleted = 0
    failed = 0
    
    for org in CLONE_ORGS:
        try:
            print(f"\n📡 Deleting: {org['name']}...", end=" ")
            meraki.delete_organization(org['id'])
            print("✅ Success")
            deleted += 1
        except Exception as e:
            print(f"❌ Failed: {str(e)}")
            failed += 1
    
    print(f"\n📊 Summary: {deleted} deleted, {failed} failed")
else:
    print("\n❌ Deletion cancelled")

print("\n✨ Cleanup complete!")