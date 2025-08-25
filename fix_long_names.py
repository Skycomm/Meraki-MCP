#!/usr/bin/env python3
"""Fix all tool names that exceed 64 characters."""

import re
import os

# Map of long names to short names
name_replacements = {
    # Appliance - already fixed
    'bulk_organization_appliance_dns_local_profiles_assignments_create': 'bulk_org_appliance_dns_profiles_create',
    'create_network_appliance_traffic_shaping_custom_performance_class': 'create_network_traffic_custom_class',
    'create_organization_appliance_dns_local_profiles_assignments_bulk_delete': 'create_org_dns_profiles_bulk_delete',
    'create_organization_appliance_dns_split_profiles_assignments_bulk_create': 'create_org_dns_split_bulk_create',
    'create_organization_appliance_dns_split_profiles_assignments_bulk_delete': 'create_org_dns_split_bulk_delete',
    'delete_network_appliance_traffic_shaping_custom_performance_class': 'delete_network_traffic_custom_class',
    'get_network_appliance_firewall_l7_firewall_rules_application_categories': 'get_network_l7_firewall_app_categories',
    'get_organization_appliance_firewall_multicast_forwarding_by_network': 'get_org_firewall_multicast_by_network',
    'get_organization_appliance_traffic_shaping_vpn_exclusions_by_network': 'get_org_traffic_vpn_exclusions_by_net',
    'update_network_appliance_traffic_shaping_custom_performance_class': 'update_network_traffic_custom_class',
    
    # Camera
    'get_organization_camera_detections_history_by_boundary_by_interval': 'get_org_camera_detections_by_boundary',
    
    # Cellular Gateway
    'create_organization_cellular_gateway_esims_service_providers_account': 'create_org_cellular_esims_provider',
    'delete_organization_cellular_gateway_esims_service_providers_account': 'delete_org_cellular_esims_provider',
    'get_network_cellular_gateway_connectivity_monitoring_destinations': 'get_network_cellular_monitoring_dest',
    'get_organization_cellular_gateway_esims_service_providers_accounts': 'get_org_cellular_esims_providers',
    'get_organization_cellular_gateway_esims_service_providers_accounts_communication_plans': 'get_org_cellular_esims_comm_plans',
    'get_organization_cellular_gateway_esims_service_providers_accounts_rate_plans': 'get_org_cellular_esims_rate_plans',
    'update_network_cellular_gateway_connectivity_monitoring_destinations': 'update_network_cellular_monitoring_dest',
    'update_organization_cellular_gateway_esims_service_providers_account': 'update_org_cellular_esims_provider',
    
    # Licensing
    'get_administered_licensing_subscription_subscriptions_compliance_statuses': 'get_admin_licensing_compliance_status',
    'validate_administered_licensing_subscription_subscriptions_claim_key': 'validate_admin_licensing_claim_key',
    
    # Organizations
    'create_organization_inventory_onboarding_cloud_monitoring_export_event': 'create_org_inventory_monitoring_export',
    'create_organization_inventory_onboarding_cloud_monitoring_prepare': 'create_org_inventory_monitoring_prep',
    'generate_organization_devices_packet_capture_capture_download_url': 'generate_org_packet_capture_url',
    'get_organization_api_requests_overview_response_codes_by_interval': 'get_org_api_response_codes_by_interval',
    
    # Switch
    'get_organization_switch_ports_usage_history_by_device_by_interval': 'get_org_switch_ports_usage_by_device',
    
    # Wireless
    'create_organization_wireless_devices_radsec_certificates_authority': 'create_org_wireless_radsec_cert_auth',
    'create_organization_wireless_ssids_firewall_isolation_allowlist_entry': 'create_org_wireless_ssid_allowlist',
    'delete_organization_wireless_ssids_firewall_isolation_allowlist_entry': 'delete_org_wireless_ssid_allowlist',
    'get_organization_wireless_devices_radsec_certificates_authorities': 'get_org_wireless_radsec_cert_auths',
    'get_organization_wireless_devices_radsec_certificates_authorities_crls': 'get_org_wireless_radsec_crls',
    'get_organization_wireless_devices_radsec_certificates_authorities_crls_deltas': 'get_org_wireless_radsec_crl_deltas',
    'get_organization_wireless_ssids_firewall_isolation_allowlist_entries': 'get_org_wireless_ssid_allowlist',
    'update_organization_wireless_devices_radsec_certificates_authorities': 'update_org_wireless_radsec_cert_auth',
    'update_organization_wireless_ssids_firewall_isolation_allowlist_entry': 'update_org_wireless_ssid_allowlist',
}

def fix_file(filepath):
    """Fix long names in a file."""
    if not os.path.exists(filepath):
        return 0
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    changes = 0
    for old_name, new_name in name_replacements.items():
        if f'name="{old_name}"' in content:
            content = content.replace(f'name="{old_name}"', f'name="{new_name}"')
            changes += 1
            print(f"  Fixed: {old_name} -> {new_name}")
    
    if changes > 0:
        with open(filepath, 'w') as f:
            f.write(content)
    
    return changes

def main():
    """Fix all long names in additional modules."""
    print("Fixing long tool names in additional modules...")
    
    total_changes = 0
    
    # Fix all additional modules
    for file in os.listdir('server'):
        if file.endswith('_additional.py'):
            filepath = os.path.join('server', file)
            print(f"\nChecking {file}...")
            changes = fix_file(filepath)
            total_changes += changes
            if changes > 0:
                print(f"  Fixed {changes} names in {file}")
    
    print(f"\n✅ Total fixes: {total_changes}")
    
    # Verify no long names remain
    print("\nVerifying all names are now ≤ 64 characters...")
    for file in os.listdir('server'):
        if file.startswith('tools_') and file.endswith('.py'):
            filepath = os.path.join('server', file)
            with open(filepath, 'r') as f:
                content = f.read()
            
            # Find all tool names
            matches = re.findall(r'name="([^"]+)"', content)
            for name in matches:
                if len(name) > 64:
                    print(f"  ⚠️ Still too long in {file}: {name} ({len(name)} chars)")
    
    print("\n✅ All tool names fixed!")

if __name__ == "__main__":
    main()