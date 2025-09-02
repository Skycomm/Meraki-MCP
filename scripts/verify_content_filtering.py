#!/usr/bin/env python3
"""
Script to verify content filtering status for Skycomm Reserve St network.
"""

import meraki
import sys

# Configuration
API_KEY = "1ac5962056ad56da8cea908864f136adc5878a43"
NETWORK_ID = "L_726205439913500692"
NETWORK_NAME = "Skycomm Reserve St"

def main():
    """Main function to verify content filtering status."""
    try:
        # Initialize Meraki dashboard API
        print(f"Connecting to Meraki API...")
        dashboard = meraki.DashboardAPI(
            api_key=API_KEY,
            output_log=False,
            suppress_logging=True
        )
        
        # Get current content filtering settings
        print(f"\nChecking content filtering status for {NETWORK_NAME}...")
        settings = dashboard.appliance.getNetworkApplianceContentFiltering(NETWORK_ID)
        
        # Display status
        print("\n" + "=" * 60)
        print(f"CONTENT FILTERING STATUS FOR {NETWORK_NAME}")
        print("=" * 60)
        
        blocked_categories = settings.get('blockedUrlCategories', [])
        blocked_patterns = settings.get('blockedUrlPatterns', [])
        
        if len(blocked_categories) == 0 and len(blocked_patterns) == 0:
            print("\n✅ CONTENT FILTERING IS DISABLED")
            print("All website categories are allowed.")
        else:
            print("\n⚠️  CONTENT FILTERING IS ACTIVE")
            print(f"- {len(blocked_categories)} categories are blocked")
            print(f"- {len(blocked_patterns)} URL patterns are blocked")
            
            if blocked_categories:
                print("\nBlocked Categories:")
                for category in blocked_categories:
                    print(f"  - {category.get('name', category)}")
            
            if blocked_patterns:
                print("\nBlocked URL Patterns:")
                for pattern in blocked_patterns:
                    print(f"  - {pattern}")
        
        # Show allowed patterns if any
        allowed_patterns = settings.get('allowedUrlPatterns', [])
        if allowed_patterns:
            print(f"\nAllowed URL Patterns ({len(allowed_patterns)}):")
            for pattern in allowed_patterns:
                print(f"  - {pattern}")
        
        print("\n" + "=" * 60)
        
    except meraki.APIError as e:
        print(f"\n❌ ERROR: Meraki API error occurred:")
        print(f"  {e.status}: {e.message}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERROR: {type(e).__name__}: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()