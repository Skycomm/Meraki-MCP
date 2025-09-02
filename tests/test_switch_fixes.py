#!/usr/bin/env python3
"""Test the fixed switch tools for Skycomm Reserve St"""

import os
import time
os.environ['MERAKI_API_KEY'] = '1ac5962056ad56da8cea908864f136adc5878a43'

from server.main import app, meraki

def test_switch_fixes():
    print("🔍 Testing Switch Tool Fixes for Skycomm Reserve St")
    print("="*70)
    
    # Reserve St network and switch details
    network_id = "L_726205439913500692"
    switch_serial = "Q2HP-GCZQ-7AWT"  # MS220-8P
    
    # Test 1: Packet Counters (previously had 'list' object error)
    print("\n📊 Test 1: Packet Counters")
    print("-"*40)
    try:
        result = meraki.dashboard.switch.getDeviceSwitchPortsStatusesPackets(switch_serial)
        
        if result:
            print(f"✅ Packet counter API returned data")
            print(f"   Type of result: {type(result)}")
            if isinstance(result, list):
                print(f"   Number of ports with data: {len(result)}")
                # Check structure of first element
                if result and isinstance(result[0], dict):
                    print(f"   First port structure: {list(result[0].keys())}")
            else:
                print(f"   Result structure: {result}")
        else:
            print("⚠️ No packet counter data returned")
            
    except Exception as e:
        print(f"❌ Packet counter error: {str(e)}")
    
    # Test 2: Ping Test (previously didn't return ID)
    print("\n🏓 Test 2: Ping Test ID Return")
    print("-"*40)
    try:
        # Create a ping test
        result = meraki.dashboard.devices.createDeviceLiveToolsPing(
            switch_serial,
            target="8.8.8.8",
            count=3
        )
        
        print(f"✅ Ping test created")
        print(f"   Response keys: {list(result.keys())}")
        
        # Check which ID field is present
        test_id = result.get('pingId') or result.get('id') or result.get('testId')
        if test_id:
            print(f"   Test ID found: {test_id}")
            print(f"   ID field name: {'pingId' if 'pingId' in result else 'id' if 'id' in result else 'testId'}")
        else:
            print(f"   ⚠️ No ID field found in response")
            print(f"   Full response: {result}")
            
        # Wait a moment and check results
        if test_id:
            time.sleep(3)
            try:
                ping_result = meraki.dashboard.devices.getDeviceLiveToolsPing(
                    switch_serial,
                    test_id
                )
                print(f"   Ping test status: {ping_result.get('status', 'Unknown')}")
            except Exception as e:
                print(f"   Could not retrieve results: {str(e)}")
                
    except Exception as e:
        print(f"❌ Ping test error: {str(e)}")
    
    # Test 3: Storm Control (expected to fail on MS220-8P)
    print("\n🌊 Test 3: Storm Control (Expected to fail)")
    print("-"*40)
    try:
        result = meraki.dashboard.switch.getNetworkSwitchStormControl(network_id)
        print(f"⚠️ Unexpectedly got storm control data: {result}")
    except Exception as e:
        if "not supported" in str(e).lower():
            print(f"✅ Storm control correctly reports not supported")
        else:
            print(f"❌ Unexpected error: {str(e)}")
    
    print("\n" + "="*70)
    print("Testing complete!")

if __name__ == "__main__":
    test_switch_fixes()
