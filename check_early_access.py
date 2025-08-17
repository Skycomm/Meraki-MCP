#!/usr/bin/env python3
"""
Check early access features for Skycomm organization.
"""

from meraki_client import MerakiClient

# Initialize client
meraki = MerakiClient()
TEST_ORG_ID = "686470"  # Skycomm

print("🧪 Checking Early Access Features for Skycomm")
print("=" * 60)

# Get available features
print("\n📋 AVAILABLE EARLY ACCESS FEATURES:")
print("-" * 60)

try:
    features = meraki.get_organization_early_access_features(TEST_ORG_ID)
    
    for i, feature in enumerate(features, 1):
        print(f"\n{i}. {feature.get('name', 'Unknown')}")
        print(f"   ID: {feature.get('id')}")
        print(f"   Short Name: {feature.get('shortName', 'N/A')}")
        print(f"   Description: {feature.get('description', 'No description')}")
        print(f"   Documentation: {feature.get('documentationLink', 'N/A')}")
        
except Exception as e:
    print(f"Error: {e}")

# Get current opt-ins
print("\n\n✅ CURRENTLY ENABLED EARLY ACCESS FEATURES:")
print("-" * 60)

try:
    opt_ins = meraki.get_organization_early_access_features_opt_ins(TEST_ORG_ID)
    
    for i, opt_in in enumerate(opt_ins, 1):
        print(f"\n{i}. Feature: {opt_in.get('shortName', opt_in.get('id', 'Unknown'))}")
        print(f"   Opt-In ID: {opt_in.get('optInId')}")
        print(f"   Created: {opt_in.get('createdAt')}")
        
        # Check if limited to specific networks
        limited_access = opt_in.get('limitedAccess', [])
        if limited_access:
            print(f"   Limited to {len(limited_access)} networks")
        else:
            print("   Access: Organization-wide")
            
except Exception as e:
    print(f"Error: {e}")

print("\n" + "="*60)
print("✨ Early access check complete!")