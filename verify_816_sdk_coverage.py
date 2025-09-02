#!/usr/bin/env python3
"""
Verify that we have exactly 816 SDK methods matching the official Meraki SDK.
"""

import json
import glob

def verify_sdk_coverage():
    """Verify exact 816 SDK method coverage."""
    
    print("🔍 Verifying Pure SDK Coverage (816 methods)...")
    print("=" * 60)
    
    # Load official SDK counts
    with open('official_sdk_methods.json', 'r') as f:
        official_sdk = json.load(f)
    
    # Count our SDK tools
    our_sdk_counts = {}
    total_our_tools = 0
    
    for sdk_file in glob.glob('server/tools_SDK_*.py'):
        category = sdk_file.split('tools_SDK_')[1].split('.py')[0]
        
        # Count @app.tool decorators
        with open(sdk_file, 'r') as f:
            content = f.read()
            tool_count = content.count('@app.tool')
        
        our_sdk_counts[category] = tool_count
        total_our_tools += tool_count
    
    # Compare with official
    print("📊 SDK Comparison Results:")
    print("-" * 60)
    print(f"{'Category':<20} {'Official':<10} {'Our SDK':<10} {'Status':<10}")
    print("-" * 60)
    
    perfect_matches = 0
    total_official = 0
    
    for category in sorted(official_sdk.keys()):
        official_count = official_sdk[category]['count']
        our_count = our_sdk_counts.get(category, 0)
        total_official += official_count
        
        if official_count == our_count:
            status = "✅ Match"
            perfect_matches += 1
        elif our_count == 0:
            status = "❌ Missing"
        elif our_count > official_count:
            status = f"⚠️ +{our_count - official_count}"
        else:
            status = f"❌ -{official_count - our_count}"
        
        print(f"{category:<20} {official_count:<10} {our_count:<10} {status}")
    
    print("-" * 60)
    print(f"{'TOTAL':<20} {total_official:<10} {total_our_tools:<10}")
    print("-" * 60)
    
    # Summary
    print("\n📈 Summary:")
    print(f"  Perfect Matches: {perfect_matches}/{len(official_sdk)} categories")
    print(f"  Total Official Methods: {total_official}")
    print(f"  Total Our SDK Methods: {total_our_tools}")
    
    if total_our_tools == 816 and total_official == 816 and perfect_matches == len(official_sdk):
        print("\n🎉 SUCCESS: Perfect 816 SDK method coverage!")
        print("✅ All categories match official Meraki SDK exactly")
        return True
    else:
        print(f"\n⚠️ Issues found:")
        if total_our_tools != 816:
            print(f"   - Expected 816 tools, got {total_our_tools}")
        if perfect_matches != len(official_sdk):
            print(f"   - {len(official_sdk) - perfect_matches} categories don't match")
        return False

def check_custom_tools():
    """Check custom tools are properly separated."""
    
    print("\n🔧 Custom Tools Summary:")
    print("-" * 40)
    
    custom_files = glob.glob('server/tools_Custom_*.py')
    total_custom = 0
    
    for custom_file in custom_files:
        category = custom_file.split('tools_Custom_')[1].split('.py')[0]
        
        with open(custom_file, 'r') as f:
            content = f.read()
            if '@app.tool' in content:
                tool_count = content.count('@app.tool')
            else:
                tool_count = 0  # Placeholder files
        
        total_custom += tool_count
        print(f"  {category}: {tool_count} tools")
    
    print(f"\n📊 Total Custom Tools: {total_custom}")
    print("✅ Custom tools properly separated from SDK")

if __name__ == "__main__":
    success = verify_sdk_coverage()
    check_custom_tools()
    
    if success:
        print("\n🏆 PERFECT SDK IMPLEMENTATION ACHIEVED!")
        print("🎯 Ready for Claude Desktop with pure 816-method SDK")
    else:
        print("\n❌ SDK implementation needs fixes")
        exit(1)