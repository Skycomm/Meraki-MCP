#!/usr/bin/env python3
"""
Cisco Meraki MCP Server - Fixed version with singleton registration check.
"""

from mcp.server import FastMCP
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from meraki_client import MerakiClient
from config import SERVER_NAME, SERVER_VERSION
from utils.helpers import create_resource, create_content, format_error_message

# Initialize the Meraki client
meraki = MerakiClient()

# Initialize MCP server with the modern FastMCP class
app = FastMCP(SERVER_NAME)

# Track if tools have been registered to prevent duplicate registration
_tools_registered = False

def register_all_tools():
    """Register all tools once and only once."""
    global _tools_registered
    
    if _tools_registered:
        print("[INFO] Tools already registered, skipping...")
        return
    
    print("[INFO] Registering tools...")
    
    # Import all resources and tools modules - they will register with the app
    from server.resources import register_resources
    from server.tools_organizations import register_organization_tools
    from server.tools_networks import register_network_tools
    from server.tools_pii import register_pii_tools
    from server.tools_devices import register_device_tools
    from server.tools_wireless import register_wireless_tools
    from server.tools_switch import register_switch_tools
    from server.tools_analytics import register_analytics_tools
    from server.tools_alerts import register_alert_tools
    from server.tools_appliance import register_appliance_tools
    from server.tools_camera import register_camera_tools
    from server.tools_sm import register_sm_tools
    from server.tools_licensing import register_licensing_tools
    from server.tools_policy import register_policy_tools
    from server.tools_monitoring import register_monitoring_tools
    from server.tools_beta import register_beta_tools
    from server.tools_live import register_live_tools
    from server.tools_dhcp import register_dhcp_tools
    from server.tools_dhcp_singlelan import register_single_lan_dhcp_tools
    from server.tools_dhcp_helper import register_dhcp_helper_tools
    from server.tools_traffic_shaping import register_traffic_shaping_tools
    from server.tools_firewall import register_firewall_tools
    from server.tools_monitoring_dashboard import register_monitoring_dashboard_tools
    from server.tools_troubleshooting import register_troubleshooting_tools
    from server.tools_event_analysis import register_event_analysis_tools
    from server.tools_client_troubleshooting import register_client_troubleshooting_tools
    from server.tools_alert_configuration import register_alert_configuration_tools
    from server.tools_vpn_configuration import register_vpn_configuration_tools
    from server.tools_uplink_monitoring import register_uplink_monitoring_tools
    from server.tools_change_tracking import register_change_tracking_tools
    from server.tools_diagnostic_reports import register_diagnostic_reports_tools
    from server.tools_firmware_management import register_firmware_management_tools
    from server.tools_helpers import register_helper_tools
    from server.tools_sensor import register_sensor_tools
    from server.tools_insight import register_insight_tools
    from server.tools_cellular_gateway import register_cellular_gateway_tools
    from server.tools_administered import register_administered_tools
    from server.tools_batch import register_batch_tools
    from server.tools_inventory import register_inventory_tools
    from server.tools_summary import register_summary_tools
    from server.tools_webhooks import register_webhooks_tools
    from server.tools_mqtt import register_mqtt_tools
    from server.tools_sdwan import register_sdwan_tools
    from server.tools_adaptivepolicy import register_adaptive_policy_tools
    from server.tools_syslog import register_syslog_tools
    from server.tools_snmp import register_snmp_tools
    from server.tools_saml import register_saml_tools
    from server.tools_branding import register_branding_tools
    from server.tools_licensing_v2 import register_enhanced_licensing_tools
    from server.tools_sm_v2 import register_enhanced_sm_tools
    from server.tools_oauth import register_oauth_tools
    from server.tools_api_analytics import register_api_analytics_tools
    from server.tools_config_templates import register_config_template_tools
    from server.tools_group_policies import register_group_policies_tools
    from server.tools_floor_plans import register_floor_plans_tools
    from server.tools_meraki_auth_users import register_meraki_auth_users_tools
    from server.tools_traffic_analysis import register_traffic_analysis_tools
    from server.tools_netflow import register_netflow_tools
    from server.tools_pii import register_pii_tools
    from server.tools_bluetooth_clients import register_bluetooth_clients_tools
    from server.tools_custom import register_custom_tools
    from server.tools_api_comparison import register_api_comparison_tools
    from server.tools_org_admins import register_org_admins_tools
    from server.tools_login_security import register_login_security_tools
    from server.tools_early_access import register_early_access_tools
    from server.tools_switch_dhcp_policy import register_switch_dhcp_policy_tools
    from server.tools_alternate_management import register_alternate_management_tools

    # Additional modules for 100% coverage
    from server.tools_organizations_additional import register_organizations_additional_tools
    from server.tools_networks_additional import register_networks_additional_tools
    from server.tools_devices_additional import register_devices_additional_tools
    from server.tools_wireless_additional import register_wireless_additional_tools
    from server.tools_switch_additional import register_switch_additional_tools
    from server.tools_appliance_additional import register_appliance_additional_tools
    from server.tools_sm_additional import register_sm_additional_tools
    from server.tools_camera_additional import register_camera_additional_tools
    from server.tools_sensor_additional import register_sensor_additional_tools
    from server.tools_cellularGateway_additional import register_cellularGateway_additional_tools
    from server.tools_insight_additional import register_insight_additional_tools
    from server.tools_licensing_additional import register_licensing_additional_tools
    from server.tools_administered_additional import register_administered_additional_tools
    from server.tools_batch_additional import register_batch_additional_tools

    # Register resources and tools
    register_resources(app, meraki)
    register_organization_tools(app, meraki)
    register_network_tools(app, meraki)
    register_device_tools(app, meraki)
    register_wireless_tools(app, meraki)
    register_switch_tools(app, meraki)
    register_analytics_tools(app, meraki)
    register_alert_tools(app, meraki)
    register_appliance_tools(app, meraki)
    register_camera_tools(app, meraki)
    register_sm_tools(app, meraki)
    register_licensing_tools(app, meraki)
    register_policy_tools(app, meraki)
    register_monitoring_tools(app, meraki)
    register_beta_tools(app, meraki)
    register_live_tools(app, meraki)
    register_dhcp_helper_tools(app, meraki)
    register_dhcp_tools(app, meraki)
    register_single_lan_dhcp_tools(app, meraki)
    register_traffic_shaping_tools(app, meraki)
    register_firewall_tools(app, meraki)
    register_monitoring_dashboard_tools(app, meraki)
    register_troubleshooting_tools(app, meraki)
    register_event_analysis_tools(app, meraki)
    register_client_troubleshooting_tools(app, meraki)
    register_alert_configuration_tools(app, meraki)
    register_vpn_configuration_tools(app, meraki)
    register_uplink_monitoring_tools(app, meraki)
    register_change_tracking_tools(app, meraki)
    register_diagnostic_reports_tools(app, meraki)
    register_firmware_management_tools(app, meraki)
    register_helper_tools(app, meraki)
    register_sensor_tools(app, meraki)
    register_insight_tools(app, meraki)
    register_cellular_gateway_tools(app, meraki)
    register_administered_tools(app, meraki)
    register_batch_tools(app, meraki)
    register_inventory_tools(app, meraki)
    register_summary_tools(app, meraki)
    register_webhooks_tools(app, meraki)
    register_mqtt_tools(app, meraki)
    register_sdwan_tools(app, meraki)
    register_adaptive_policy_tools(app, meraki)
    register_syslog_tools(app, meraki)
    register_snmp_tools(app, meraki)
    register_saml_tools(app, meraki)
    register_branding_tools(app, meraki)
    register_enhanced_licensing_tools(app, meraki)
    register_enhanced_sm_tools(app, meraki)
    register_oauth_tools(app, meraki)
    register_api_analytics_tools(app, meraki)
    register_config_template_tools(app, meraki)
    register_group_policies_tools(app, meraki)
    register_floor_plans_tools(app, meraki)
    register_meraki_auth_users_tools(app, meraki)
    register_traffic_analysis_tools(app, meraki)
    register_netflow_tools(app, meraki)
    register_pii_tools(app, meraki)
    register_bluetooth_clients_tools(app, meraki)
    register_custom_tools(app, meraki)
    register_api_comparison_tools(app, meraki)
    register_org_admins_tools(app, meraki)
    register_login_security_tools(app, meraki)
    register_early_access_tools(app, meraki)
    register_switch_dhcp_policy_tools(app, meraki)
    register_alternate_management_tools(app, meraki)
    
    # Additional modules for 100% coverage
    register_organizations_additional_tools(app, meraki)
    register_networks_additional_tools(app, meraki)
    register_devices_additional_tools(app, meraki)
    register_wireless_additional_tools(app, meraki)
    register_switch_additional_tools(app, meraki)
    register_appliance_additional_tools(app, meraki)
    register_sm_additional_tools(app, meraki)
    register_camera_additional_tools(app, meraki)
    register_sensor_additional_tools(app, meraki)
    register_cellularGateway_additional_tools(app, meraki)
    register_insight_additional_tools(app, meraki)
    register_licensing_additional_tools(app, meraki)
    register_administered_additional_tools(app, meraki)
    register_batch_additional_tools(app, meraki)
    
    _tools_registered = True
    print("[INFO] Tool registration complete")

# Register tools on import
register_all_tools()

# Export the app
__all__ = ['app']