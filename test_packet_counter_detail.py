#!/usr/bin/env python3
"""Test packet counter tool in detail"""

import os
os.environ['MERAKI_API_KEY'] = '1ac5962056ad56da8cea908864f136adc5878a43'

from server.main import app, meraki
from server.tools_switch import register_switch_tools

# Initialize tools
register_switch_tools(app, meraki)

def test_packet_counter():
    switch_serial = "Q2HP-GCZQ-7AWT"
    
    print("Testing packet counter tool that previously failed...")
    print("-"*50)
    
    # Call the Meraki API directly to see raw data format
    print("1. Testing raw API response:")
    try:
        raw_result = meraki.dashboard.switch.getDeviceSwitchPortsStatusesPackets(switch_serial)
        print(f"   Raw API returned: {type(raw_result)}")
        if isinstance(raw_result, list) and raw_result:
            print(f"   First item structure: {list(raw_result[0].keys())}")
            print(f"   First item sample: {raw_result[0]}")
        elif isinstance(raw_result, dict):
            print(f"   Dict keys: {list(raw_result.keys())}")
        else:
            print(f"   Raw result: {raw_result}")
    except Exception as e:
        print(f"   Raw API error: {str(e)}")
    
    # Now test via the tool (can't import directly, so use the API directly with formatting)
    print("\n2. Testing formatted output:")
    try:
        result = meraki.dashboard.switch.getDeviceSwitchPortsStatusesPackets(switch_serial)
        
        # Apply the same formatting as the tool
        response = f"# 📦 Switch Port Packet Statistics\n\n"
        response += f"**Switch**: {switch_serial}\n"
        response += f"**Timespan**: 3600 seconds\n\n"
        
        if result and isinstance(result, list):
            response += f"**Ports with Data**: {len(result)}\n\n"
            
            total_rx = 0
            total_tx = 0
            
            for port in result:
                port_id = port.get('portId', 'Unknown')
                packets = port.get('packets', {})
                
                rx_total = packets.get('recv', 0)
                tx_total = packets.get('sent', 0)
                
                total_rx += rx_total
                total_tx += tx_total
                
                response += f"## Port {port_id}\n"
                response += f"- **Received**: {rx_total:,} packets\n"
                response += f"- **Sent**: {tx_total:,} packets\n"
                
                # Detailed packet types
                desc = packets.get('desc', {})
                if desc:
                    response += "- **By Type**:\n"
                    for pkt_type, count in desc.items():
                        if count > 0:
                            response += f"  - {pkt_type}: {count:,}\n"
                
                # Rate info if available
                rate_per_sec = packets.get('ratePerSec', {})
                if rate_per_sec:
                    response += f"- **Rate**: {rate_per_sec.get('recv', 0)} rx/s, {rate_per_sec.get('sent', 0)} tx/s\n"
                
                response += "\n"
            
            response += f"## Totals\n"
            response += f"- **Total Received**: {total_rx:,} packets\n"
            response += f"- **Total Sent**: {total_tx:,} packets\n"
        else:
            response += "*No packet data available*\n"
        
        result = response
        
    except Exception as e:
        result = f"❌ Error getting port packet statistics: {str(e)}"
    
    # Check if it returns formatted output without errors
    if "Error" in result:
        print(f"❌ Tool still has error: {result}")
    else:
        print("✅ Tool executed successfully!")
        # Show first few lines of output
        lines = result.split('\n')[:10]
        for line in lines:
            print(f"   {line}")
        
        if len(result.split('\n')) > 10:
            print("   ...")

if __name__ == "__main__":
    test_packet_counter()
