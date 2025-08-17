#!/usr/bin/env python3
"""
Script to enable recommended network alerts for Reserve St network.
This demonstrates how to use the updated update_network_alerts_settings tool.
"""

# Example usage of the update_network_alerts_settings tool
# This would be called through the MCP server

network_id = "L_682851785713193693"  # Reserve St network

# The parameters to enable all recommended alerts
alert_params = {
    "network_id": network_id,
    "all_admins": True,  # Notify all network admins by default
    "enable_device_down": True,  # Enable device down alerts
    "enable_gateway_down": True,  # Enable gateway connectivity issues
    "enable_dhcp_failure": True,  # Enable DHCP failures
    "enable_high_usage": True,  # Enable high wireless usage
    "enable_ip_conflict": True  # Enable IP conflict detection
}

# In actual usage through MCP, you would call:
# update_network_alerts_settings(**alert_params)

print(f"To enable recommended alerts for Reserve St network ({network_id}), use these parameters:")
print("\nupdate_network_alerts_settings(")
for key, value in alert_params.items():
    print(f"    {key}={repr(value)},")
print(")")

print("\nThis will enable the following critical alerts:")
print("1. Device down alerts (gateway, repeater, switch, wireless)")
print("2. Gateway connectivity issues (VPN, uplink status)")
print("3. DHCP failures (no leases, server problems)")
print("4. High wireless usage")
print("5. IP conflict detection")
print("\nAll alerts will notify all network admins by default.")