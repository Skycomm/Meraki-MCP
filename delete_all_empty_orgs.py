#!/usr/bin/env python3
"""
Delete all empty test and clone organizations with confirmations.
Run this directly: python delete_all_empty_orgs.py
"""

from server.main import meraki
from datetime import datetime

# List of all empty organizations (test orgs + clone orgs)
EMPTY_ORGS = [
    # Test organizations
    {"name": "Test Organization MCP", "id": "669347494617945864"},
    {"name": "Test Branch", "id": "669347494617945865"},
    {"name": "Test Branch (duplicate)", "id": "669347494617945866"},
    {"name": "Test Org", "id": "669347494617945867"},
    {"name": "Test Org (duplicate)", "id": "726205439913493747"},
    {"name": "Test-Org-Safety", "id": "726205439913493750"},
    # Clone organizations
    {"name": "Clone (Q_EopcIe)", "id": "726205439913493748"},
    {"name": "Clone (CCxOPdIe)", "id": "726205439913493749"}
]

print("🧹 Empty Organizations Cleanup")
print("=" * 60)
print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"📊 Found {len(EMPTY_ORGS)} empty organizations")
print("=" * 60)

# Show all organizations grouped by type
print("\n📋 Organizations to delete:")
print("\n🧪 Test Organizations:")
for org in EMPTY_ORGS[:6]:  # First 6 are test orgs
    print(f"   - {org['name']} (ID: {org['id']})")

print("\n🔄 Clone Organizations:")
for org in EMPTY_ORGS[6:]:  # Last 2 are clone orgs
    print(f"   - {org['name']} (ID: {org['id']})")

# Ask for confirmation
print("\n⚠️  WARNING: This will permanently delete these organizations!")
print("\nOptions:")
print("1. Type 'DELETE ALL' to delete all organizations")
print("2. Type 'DELETE TEST' to delete only test organizations")
print("3. Type 'DELETE CLONE' to delete only clone organizations")
print("4. Type 'SELECT' to choose which ones to delete")
print("5. Type anything else to cancel")

choice = input("\nYour choice: ").strip()

# Determine which orgs to process
if choice == "DELETE ALL":
    orgs_to_delete = EMPTY_ORGS
    print("\n🗑️  Deleting all empty organizations...")
elif choice == "DELETE TEST":
    orgs_to_delete = EMPTY_ORGS[:6]
    print("\n🗑️  Deleting test organizations only...")
elif choice == "DELETE CLONE":
    orgs_to_delete = EMPTY_ORGS[6:]
    print("\n🗑️  Deleting clone organizations only...")
elif choice == "SELECT":
    print("\n📝 Select organizations to delete")
    orgs_to_delete = []
    
    for org in EMPTY_ORGS:
        response = input(f"\nDelete '{org['name']}'? (y/n): ").strip().lower()
        if response == 'y':
            orgs_to_delete.append(org)
else:
    orgs_to_delete = []
    print("\n❌ Deletion cancelled")

# Perform deletions
if orgs_to_delete:
    deleted = 0
    failed = 0
    
    for org in orgs_to_delete:
        try:
            print(f"\n📡 Deleting: {org['name']}...", end=" ")
            meraki.delete_organization(org['id'])
            print("✅ Success")
            deleted += 1
        except Exception as e:
            print(f"❌ Failed: {str(e)}")
            failed += 1
    
    print(f"\n📊 Summary: {deleted} deleted, {failed} failed")

print("\n✨ Cleanup complete!")