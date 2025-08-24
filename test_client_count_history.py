#!/usr/bin/env python3
"""
Test script to check client count trends for Reserve St network
"""

import os
import meraki
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_client_count_history():
    """Test the get_network_wireless_client_count_history function."""
    
    # Initialize Meraki dashboard API
    api_key = os.getenv('MERAKI_API_KEY')
    if not api_key:
        print("Error: MERAKI_API_KEY not found in environment variables")
        return
        
    dashboard = meraki.DashboardAPI(api_key, suppress_logging=True)
    
    network_id = "L_726205439913500692"
    
    try:
        # Get client count history for the last 24 hours
        print("Getting client count history for Reserve St network...")
        print("=" * 60)
        
        history = dashboard.wireless.getNetworkWirelessClientCountHistory(
            network_id, 
            timespan=86400  # 24 hours
        )
        
        if not history:
            print("No client count history available.")
            return
            
        print(f"Total data points: {len(history)}")
        
        # Calculate statistics
        counts = [entry.get('clientCount', 0) for entry in history]
        if counts:
            max_clients = max(counts)
            min_clients = min(counts)
            avg_clients = sum(counts) / len(counts)
            
            print(f"\nStatistics for the last 24 hours:")
            print(f"  Peak Clients: {max_clients}")
            print(f"  Minimum Clients: {min_clients}")
            print(f"  Average Clients: {avg_clients:.1f}")
        
        # Show recent history
        print(f"\nRecent Client Count (last 10 data points):")
        print("-" * 60)
        for entry in history[-10:]:
            start_time = entry.get('startTs', 'Unknown')
            count = entry.get('clientCount', 0)
            bar = '█' * min(count, 50)
            print(f"{start_time[:19]}: {count:3d} clients {bar}")
            
        # Also get by band
        print("\n\nClient count by band (2.4 GHz):")
        print("=" * 60)
        history_2_4 = dashboard.wireless.getNetworkWirelessClientCountHistory(
            network_id, 
            timespan=86400,
            band='2.4'
        )
        
        if history_2_4:
            counts_2_4 = [entry.get('clientCount', 0) for entry in history_2_4]
            if counts_2_4:
                print(f"  Peak: {max(counts_2_4)}, Average: {sum(counts_2_4)/len(counts_2_4):.1f}")
        
        print("\nClient count by band (5 GHz):")
        print("=" * 60)
        history_5 = dashboard.wireless.getNetworkWirelessClientCountHistory(
            network_id, 
            timespan=86400,
            band='5'
        )
        
        if history_5:
            counts_5 = [entry.get('clientCount', 0) for entry in history_5]
            if counts_5:
                print(f"  Peak: {max(counts_5)}, Average: {sum(counts_5)/len(counts_5):.1f}")
                
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_client_count_history()