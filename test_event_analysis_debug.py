#!/usr/bin/env python3
"""
Debug Event Log Analysis Tools
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from server.tools_event_analysis import search_event_logs

# Test data
NETWORK_ID = "L_669347494617953785"  # Taiwan network

result = search_event_logs(
    network_id=NETWORK_ID,
    search_term="authentication",
    timespan=3600
)

print("Result:")
print(result)
print(f"\nLength: {len(result)}")
print(f"Contains 'Event Log Search': {'Event Log Search' in result}")
print(f"Contains 'No events found': {'No events found' in result}")