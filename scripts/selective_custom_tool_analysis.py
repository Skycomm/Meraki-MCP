#!/usr/bin/env python3
"""
Analyze which custom tools are truly unique and should be re-enabled.
"""

def analyze_unique_custom_tools():
    """Identify unique custom tools worth preserving."""
    
    print("🔍 SELECTIVE CUSTOM TOOL ANALYSIS")
    print("=" * 50)
    
    print("\n## 📊 RECOMMENDATION SUMMARY\n")
    
    print("### ✅ SHOULD RE-ENABLE (Unique Functionality):")
    print("\n**ALERTS MODULE** - Webhook Management:")
    alerts_unique = [
        "get_organization_webhooks",
        "create_organization_webhook", 
        "delete_organization_webhook",
        "delete_all_organization_webhooks",
        "get_network_webhook_http_servers",
        "create_network_webhook_http_server",
        "delete_network_webhook"
    ]
    
    for tool in alerts_unique:
        print(f"   ✅ {tool}")
    print(f"   📊 {len(alerts_unique)} unique webhook management tools")
    
    print("\n**MONITORING MODULE** - Advanced Device Analytics:")
    monitoring_unique = [
        "get_device_memory_history",
        "get_device_cpu_power_mode_history", 
        "get_device_wireless_cpu_load",
        "get_organization_switch_ports_history",
        "get_organization_devices_migration_status",
        "get_organization_api_usage"
    ]
    
    for tool in monitoring_unique:
        print(f"   ✅ {tool}")
    print(f"   📊 {len(monitoring_unique)} unique monitoring/analytics tools")
    
    print("\n### ❌ SHOULD STAY DISABLED (Duplicate SDK Functions):")
    print("\n**LIVE MODULE** - All 14 tools duplicate Devices SDK")
    print("**POLICY MODULE** - All 6 tools duplicate Organizations SDK") 
    print("**VPN MODULE** - All 9 tools duplicate Appliance SDK")
    
    print("\n## 🎯 IMPLEMENTATION STRATEGY:")
    print("\n1. **Create filtered registration functions** for ALERTS and MONITORING")
    print("2. **Register only the unique tools**, skip the duplicates")
    print("3. **Keep SDK tools as primary** for all official API functions")
    print("4. **Add ~13 unique custom tools** to our 816 SDK tools")
    
    total_unique = len(alerts_unique) + len(monitoring_unique)
    print(f"\n**Result**: 816 SDK + {total_unique} unique custom = ~{816 + total_unique} total tools")
    
    print("\n## 🛠️ CODE CHANGES NEEDED:")
    print("""
1. Create filtered registration functions:
   - register_alerts_tools_filtered() - only webhook tools
   - register_monitoring_tools_filtered() - only unique analytics
   
2. Update server/main.py imports and registrations
   
3. Test for zero duplicates
""")
    
    return {
        'alerts_unique': alerts_unique,
        'monitoring_unique': monitoring_unique,
        'total_unique': total_unique
    }

if __name__ == "__main__":
    result = analyze_unique_custom_tools()
    print(f"\n🏁 Analysis complete: {result['total_unique']} unique tools identified")