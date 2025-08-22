#!/usr/bin/env python3
"""
Delete empty test organizations with confirmations.
Run this directly: python delete_empty_test_orgs.py
"""

from server.main import meraki
from datetime import datetime

# List of empty test organizations found
TEST_ORGS = [
    {"name": "Test Organization MCP", "id": "669347494617945864"},
    {"name": "Test Branch", "id": "669347494617945865"},
    {"name": "Test Branch (duplicate)", "id": "669347494617945866"},
    {"name": "Test Org", "id": "669347494617945867"},
    {"name": "Test Org (duplicate)", "id": "726205439913493747"},
    {"name": "Test-Org-Safety", "id": "726205439913493750"}
]

print("🧹 Empty Test Organizations Cleanup")
print("=" * 60)
print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"📊 Found {len(TEST_ORGS)} empty test organizations")
print("=" * 60)

# Show all organizations
print("\n📋 Organizations to delete:")
for i, org in enumerate(TEST_ORGS, 1):
    print(f"{i}. {org['name']} (ID: {org['id']})")

# Ask for confirmation
print("\n⚠️  WARNING: This will permanently delete these organizations!")
print("Type 'DELETE ALL' to delete all organizations")
print("Type 'SELECT' to choose which ones to delete")
print("Type anything else to cancel")

choice = input("\nYour choice: ").strip()

if choice == "DELETE ALL":
    print("\n🗑️  Deleting all test organizations...")
    deleted = 0
    failed = 0
    
    for org in TEST_ORGS:
        try:
            print(f"\n📡 Deleting: {org['name']}...", end=" ")
            meraki.delete_organization(org['id'])
            print("✅ Success")
            deleted += 1
        except Exception as e:
            print(f"❌ Failed: {str(e)}")
            failed += 1
    
    print(f"\n📊 Summary: {deleted} deleted, {failed} failed")

elif choice == "SELECT":
    print("\n📝 Select organizations to delete")
    to_delete = []
    
    for org in TEST_ORGS:
        response = input(f"\nDelete '{org['name']}'? (y/n): ").strip().lower()
        if response == 'y':
            to_delete.append(org)
    
    if to_delete:
        print(f"\n🗑️  Deleting {len(to_delete)} selected organizations...")
        deleted = 0
        failed = 0
        
        for org in to_delete:
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
        print("\n❌ No organizations selected for deletion")

else:
    print("\n❌ Deletion cancelled")

print("\n✨ Cleanup complete!")