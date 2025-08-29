#!/usr/bin/env python3
import os
import re

server_dir = "/Users/david/docker/cisco-meraki-mcp-server-tvi/server"

# Category mapping
categories = {
    "🏢 ORGANIZATION & ADMIN": ["organizations", "licensing", "policy"],
    "🌐 NETWORK CORE": ["networks", "devices", "monitoring"],
    "📡 WIRELESS": ["wireless"],
    "🔌 SWITCH": ["switch"],
    "🔒 SECURITY & VPN": ["appliance", "vpn"],
    "📹 CAMERA & IoT": ["camera", "sm"],
    "📊 ANALYTICS": ["analytics", "alerts", "event"],
    "🔧 LIVE TOOLS": ["live"],
    "🧪 BETA & HELPERS": ["beta", "helpers"],
}

print("=" * 70)
print("MCP SERVER TOOL FILES ORGANIZATION")
print("=" * 70)

total_tools = 0
file_list = []

# Scan all tool files
for file in os.listdir(server_dir):
    if file.startswith("tools_") and file.endswith(".py"):
        filepath = os.path.join(server_dir, file)
        with open(filepath, 'r') as f:
            content = f.read()
            tool_count = content.count("@app.tool(")
            file_list.append((file, tool_count))
            total_tools += tool_count

# Sort and display by category
for category, keywords in categories.items():
    category_files = []
    category_total = 0
    
    for filename, count in file_list:
        for keyword in keywords:
            if keyword in filename:
                category_files.append((filename, count))
                category_total += count
                break
    
    if category_files:
        print(f"\n{category} ({category_total} tools)")
        print("-" * 60)
        for filename, count in sorted(category_files):
            # Add description based on filename
            desc = ""
            if "wireless_firewall" in filename:
                desc = " - L3/L7 firewall, traffic shaping"
            elif "wireless_advanced" in filename:
                desc = " - Connection stats, network settings"
            elif "wireless_rf" in filename:
                desc = " - RF profiles, Air Marshal"
            elif "wireless_complete" in filename:
                desc = " - Hotspot, splash, schedules, Bluetooth"
            elif "wireless_final" in filename:
                desc = " - Organization analytics, packet loss"
            elif "wireless_100" in filename:
                desc = " - Identity PSKs, client stats, health"
            elif "wireless_missing" in filename:
                desc = " - Final SDK methods for 100% coverage"
            elif "wireless_all" in filename:
                desc = " - (Partial implementation)"
            elif filename == "tools_wireless.py":
                desc = " - Basic SSIDs, clients, usage"
            elif "appliance" in filename:
                desc = " - MX appliances, VLANs, firewall, uplinks"
            elif "vpn" in filename:
                desc = " - Site-to-site VPN configuration"
            elif "organizations" in filename:
                desc = " - Org management, inventory, claims"
            elif "networks" in filename:
                desc = " - Network CRUD, settings, topology"
            elif "devices" in filename:
                desc = " - Device management, status, config"
            elif "switch" in filename:
                desc = " - Switch ports, VLANs, STP, stacks"
            elif "analytics" in filename:
                desc = " - Traffic analytics, summaries"
            elif "alerts" in filename:
                desc = " - Alert history, settings, webhooks"
            elif "live" in filename:
                desc = " - Ping, traceroute, cable test, ARP"
            elif "monitoring" in filename:
                desc = " - Packet capture, health, connectivity"
            elif "camera" in filename:
                desc = " - Video settings, snapshots, analytics"
            elif "sm" in filename:
                desc = " - Systems Manager, MDM"
            elif "licensing" in filename:
                desc = " - License management, assignments"
            elif "policy" in filename:
                desc = " - Group policies, ACLs"
            elif "beta" in filename:
                desc = " - Beta features, experimental"
            elif "helpers" in filename:
                desc = " - Utility functions, batch operations"
            
            print(f"  {filename:35} {count:3} tools{desc}")

# Wireless breakdown
print("\n📡 WIRELESS DETAILED BREAKDOWN")
print("-" * 60)
wireless_total = 0
for filename, count in sorted(file_list):
    if "wireless" in filename:
        wireless_total += count

print(f"Total wireless tools: {wireless_total}")
print(f"SDK target: 116 methods")
print(f"Coverage: {(wireless_total/116)*100:.1f}% (includes some duplicates)")

print("\n" + "=" * 70)
print(f"🎯 TOTAL MCP TOOLS: {total_tools}")
print("=" * 70)

# Show how main.py registers them
print("\n📄 Registration in main.py:")
print("-" * 60)
with open(os.path.join(os.path.dirname(server_dir), "server/main.py"), 'r') as f:
    lines = f.readlines()
    in_imports = False
    in_registration = False
    
    for line in lines:
        if "from server.tools_" in line:
            if not in_imports:
                print("# Imports:")
                in_imports = True
            module = line.split("from server.")[1].split(" import")[0]
            print(f"  {module}")
        elif "register_" in line and "_tools(app, meraki)" in line:
            if not in_registration:
                print("\n# Registration order:")
                in_registration = True
            func = line.strip().split("(")[0]
            print(f"  {func}()")
