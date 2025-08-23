#!/usr/bin/env python3
"""
Script to disable content filtering for Skycomm Reserve St network.
This will allow all website categories.
"""

import meraki
import json
import sys

# Configuration
API_KEY = "1ac5962056ad56da8cea908864f136adc5878a43"
NETWORK_ID = "L_726205439913500692"
NETWORK_NAME = "Skycomm Reserve St"

def main():
    """Main function to disable content filtering."""
    try:
        # Initialize Meraki dashboard API
        print(f"Initializing Meraki API client...")
        dashboard = meraki.DashboardAPI(
            api_key=API_KEY,
            output_log=False,
            suppress_logging=True,
            wait_on_rate_limit=True,
            maximum_retries=5
        )
        
        # Get current content filtering settings
        print(f"\nGetting current content filtering settings for {NETWORK_NAME}...")
        current_settings = dashboard.appliance.getNetworkApplianceContentFiltering(NETWORK_ID)
        
        # Display current settings
        print("\nCurrent Content Filtering Settings:")
        print(f"- Blocked Categories: {len(current_settings.get('blockedUrlCategories', []))} categories")
        print(f"- Blocked URL Patterns: {len(current_settings.get('blockedUrlPatterns', []))} patterns")
        print(f"- Allowed URL Patterns: {len(current_settings.get('allowedUrlPatterns', []))} patterns")
        print(f"- URL Category List Size: {current_settings.get('urlCategoryListSize', 'topSites')}")
        
        if current_settings.get('blockedUrlCategories'):
            print("\nCurrently blocked categories:")
            for category in current_settings.get('blockedUrlCategories', []):
                print(f"  - {category}")
        
        # Disable content filtering by clearing all blocked categories
        print(f"\nDisabling content filtering for {NETWORK_NAME}...")
        print("This will allow access to all website categories.")
        
        # Update content filtering settings
        # Setting empty arrays for blocked categories and patterns effectively disables filtering
        updated_settings = dashboard.appliance.updateNetworkApplianceContentFiltering(
            NETWORK_ID,
            blockedUrlCategories=[],  # Empty array = no categories blocked
            blockedUrlPatterns=[],    # Clear any blocked URL patterns
            allowedUrlPatterns=current_settings.get('allowedUrlPatterns', []),  # Keep existing allowed patterns
            urlCategoryListSize=current_settings.get('urlCategoryListSize', 'topSites')  # Keep existing list size
        )
        
        # Verify the update
        print("\nContent filtering has been disabled!")
        print("\nUpdated Content Filtering Settings:")
        print(f"- Blocked Categories: {len(updated_settings.get('blockedUrlCategories', []))} categories")
        print(f"- Blocked URL Patterns: {len(updated_settings.get('blockedUrlPatterns', []))} patterns")
        print(f"- Allowed URL Patterns: {len(updated_settings.get('allowedUrlPatterns', []))} patterns")
        
        if len(updated_settings.get('blockedUrlCategories', [])) == 0:
            print("\n✅ SUCCESS: All website categories are now allowed!")
            print(f"Content filtering has been completely disabled for {NETWORK_NAME}.")
        else:
            print("\n⚠️ WARNING: Some categories may still be blocked.")
            print("Please check the Meraki dashboard for verification.")
        
        # Save a log of the change
        with open('content_filtering_change_log.json', 'w') as f:
            log_entry = {
                'network_id': NETWORK_ID,
                'network_name': NETWORK_NAME,
                'action': 'disabled_content_filtering',
                'timestamp': str(dashboard.organizations.getOrganizationDevicesUplinksLossAndLatency.__defaults__),
                'previous_settings': {
                    'blocked_categories_count': len(current_settings.get('blockedUrlCategories', [])),
                    'blocked_categories': current_settings.get('blockedUrlCategories', [])
                },
                'new_settings': {
                    'blocked_categories_count': len(updated_settings.get('blockedUrlCategories', [])),
                    'blocked_categories': updated_settings.get('blockedUrlCategories', [])
                }
            }
            json.dump(log_entry, f, indent=2)
            print(f"\nChange log saved to: content_filtering_change_log.json")
        
    except meraki.APIError as e:
        print(f"\n❌ ERROR: Meraki API error occurred:")
        print(f"  Status: {e.status}")
        print(f"  Message: {e.message}")
        print(f"  Details: {e.details}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERROR: An unexpected error occurred:")
        print(f"  {type(e).__name__}: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    print("=" * 60)
    print("DISABLE CONTENT FILTERING SCRIPT")
    print(f"Network: {NETWORK_NAME}")
    print(f"Network ID: {NETWORK_ID}")
    print("=" * 60)
    
    # Confirm before proceeding
    response = input("\n⚠️  This will disable ALL content filtering for this network.\nDo you want to proceed? (yes/no): ")
    if response.lower() != 'yes':
        print("\nOperation cancelled.")
        sys.exit(0)
    
    main()