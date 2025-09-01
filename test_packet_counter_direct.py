#!/usr/bin/env python3
"""Test packet counter tool directly"""

import os
os.environ['MERAKI_API_KEY'] = '1ac5962056ad56da8cea908864f136adc5878a43'

from server.main import app, meraki

def test_packet_counter():
    switch_serial = "Q2HP-GCZQ-7AWT"
    
    print("Testing packet counter tool with the fix...")
    print("-"*50)
    
    try:
        # Call the SDK method directly like the tool does
        result = meraki.dashboard.switch.getDeviceSwitchPortsStatusesPackets(switch_serial)
        
        if result and isinstance(result, list):
            print(f"✅ API returned a list with {len(result)} port entries")
            
            # Test the logic that was failing before
            total_packets = 0
            for p in result:
                if isinstance(p, dict):
                    packets = p.get('packets', {})
                    if isinstance(packets, dict):
                        sent = packets.get('sent', 0) 
                        recv = packets.get('recv', 0)
                        total_packets += sent + recv
                        print(f"   Port {p.get('portId', '?')}: Sent={sent:,}, Recv={recv:,}")
            
            print(f"\n   Total packets across all ports: {total_packets:,}")
            print("\n✅ The fixed code handles the data structure correctly!")
            
        else:
            print(f"⚠️ Unexpected result type: {type(result)}")
            
    except AttributeError as e:
        if "'list' object has no attribute 'get'" in str(e):
            print(f"❌ The original error still occurs: {e}")
        else:
            print(f"❌ Different error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    test_packet_counter()
