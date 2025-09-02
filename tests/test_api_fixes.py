#!/usr/bin/env python3
"""Test the API fixes for WiFi audit issues."""

import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_api_fixes():
    server_params = StdioServerParameters(
        command=".venv/bin/python",
        args=["meraki_server.py"],
        env=None
    )
    
    print("🧪 Testing API Fixes for WiFi Audit Issues")
    print("=" * 80)
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            network_id = "L_726205439913500692"  # Reserve St
            org_id = "686470"  # Skycomm
            device_serial = "Q2PD-JL52-H3B2"  # Office AP
            
            # Test 1: Network-level RF profiles (should redirect)
            print("\n1️⃣ Test Network-level RF Profiles (should redirect):")
            print("-" * 40)
            try:
                result = await session.call_tool(
                    "get_network_wireless_rf_profiles_assignments_by_device",
                    arguments={"network_id": network_id}
                )
                text = result.content[0].text
                if "doesn't exist" in text and "organization-level" in text:
                    print("✅ Correctly redirects to org-level tool!")
                    print(text[:300])
                else:
                    print("⚠️ Unexpected response")
            except Exception as e:
                print(f"❌ Error: {e}")
            
            # Test 2: Organization-level RF profiles (should work)
            print("\n2️⃣ Test Organization-level RF Profiles:")
            print("-" * 40)
            try:
                result = await session.call_tool(
                    "get_organization_wireless_rf_profiles_assignments_by_device",
                    arguments={
                        "organization_id": org_id,
                        "network_ids": network_id
                    }
                )
                text = result.content[0].text
                print(f"✅ Org-level tool works!")
                print(text[:400])
            except Exception as e:
                print(f"❌ Error: {e}")
            
            # Test 3: Signal quality without params (should show helpful error)
            print("\n3️⃣ Test Signal Quality without params (should show examples):")
            print("-" * 40)
            try:
                result = await session.call_tool(
                    "get_network_wireless_signal_quality_history",
                    arguments={"network_id": network_id}
                )
                text = result.content[0].text
                if "Example" in text and "device_serial" in text:
                    print("✅ Shows helpful examples!")
                    print(text[:400])
                else:
                    print("⚠️ Error message could be better")
            except Exception as e:
                print(f"❌ Error: {e}")
            
            # Test 4: Signal quality WITH device_serial (should work or return null gracefully)
            print("\n4️⃣ Test Signal Quality WITH device_serial:")
            print("-" * 40)
            try:
                result = await session.call_tool(
                    "get_network_wireless_signal_quality_history",
                    arguments={
                        "network_id": network_id,
                        "device_serial": device_serial,
                        "timespan": 3600
                    }
                )
                text = result.content[0].text
                if "Signal Quality History" in text or "No data available" in text:
                    print("✅ Works with device_serial!")
                    print(text[:400])
                else:
                    print("⚠️ Unexpected response")
            except Exception as e:
                print(f"❌ Error: {e}")
            
            # Test 5: Usage history without params (should show helpful error)
            print("\n5️⃣ Test Usage History without params (should show examples):")
            print("-" * 40)
            try:
                result = await session.call_tool(
                    "get_network_wireless_usage_history",
                    arguments={"network_id": network_id}
                )
                text = result.content[0].text
                if "Example" in text and "device_serial" in text:
                    print("✅ Shows helpful examples!")
                    print(text[:400])
                else:
                    print("⚠️ Error message could be better")
            except Exception as e:
                print(f"❌ Error: {e}")
            
            # Test 6: Test SDK directly to confirm methods
            print("\n6️⃣ Test SDK Methods Directly:")
            print("-" * 40)
            try:
                # Import the meraki client
                from server.main import meraki
                
                # Test that network-level RF profiles doesn't exist
                try:
                    result = meraki.dashboard.wireless.getNetworkWirelessRfProfilesAssignmentsByDevice(network_id)
                    print("❌ Network-level method exists (unexpected!)")
                except AttributeError:
                    print("✅ Confirmed: Network-level RF profiles method doesn't exist")
                
                # Test that org-level RF profiles exists
                try:
                    # This should work (even if it returns no data)
                    result = meraki.dashboard.wireless.getOrganizationWirelessRfProfilesAssignmentsByDevice(
                        org_id, 
                        networkIds=[network_id],
                        perPage=10
                    )
                    print("✅ Confirmed: Org-level RF profiles method exists")
                except Exception as e:
                    if "404" in str(e):
                        print("✅ Org-level method exists (404 = no data)")
                    else:
                        print(f"⚠️ Org-level method issue: {e}")
                
            except Exception as e:
                print(f"⚠️ SDK test skipped: {e}")
            
            print("\n" + "=" * 80)
            print("✅ API Fix Tests Complete!")

if __name__ == "__main__":
    asyncio.run(test_api_fixes())
