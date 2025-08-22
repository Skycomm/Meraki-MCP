#!/usr/bin/env python3
"""
Delete test network and organization with confirmations.
Run this directly: python delete_test_network.py
"""

from server.main import meraki

# Test network and org IDs from earlier
TEST_NETWORK_ID = "L_669347494617971457"
TEST_ORG_ID = "669347494617945873"

print("🧹 Cleanup Test Resources")
print("=" * 50)

# Delete network
try:
    network = meraki.get_network(TEST_NETWORK_ID)
    print(f"\n📡 Found network: {network['name']} (ID: {TEST_NETWORK_ID})")
    
    response = input("Type 'DELETE' to delete this network: ")
    if response == "DELETE":
        meraki.delete_network(TEST_NETWORK_ID)
        print("✅ Network deleted successfully")
    else:
        print("❌ Deletion cancelled")
except Exception as e:
    print(f"❌ Network error: {e}")

# Delete organization
try:
    org = meraki.get_organization(TEST_ORG_ID)
    print(f"\n🏢 Found organization: {org['name']} (ID: {TEST_ORG_ID})")
    
    response = input("Type 'DELETE' to delete this organization: ")
    if response == "DELETE":
        meraki.delete_organization(TEST_ORG_ID)
        print("✅ Organization deleted successfully")
    else:
        print("❌ Deletion cancelled")
except Exception as e:
    print(f"❌ Organization error: {e}")

print("\n✨ Cleanup complete!")