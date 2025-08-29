"""
RF Profiles and Air Marshal Tools for the Cisco Meraki MCP Server.
Implements RF profile management and Air Marshal security features.
"""

from typing import Optional, List, Dict, Any
import json

# Global variables to store app and meraki client
app = None
meraki_client = None

def register_wireless_rf_tools(mcp_app, meraki):
    """
    Register RF and Air Marshal tools with the MCP server.
    
    Args:
        mcp_app: MCP server instance
        meraki: Meraki client instance
    """
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    
    # Register all RF and Air Marshal tool handlers
    register_rf_profile_tools()
    register_air_marshal_tools()
    register_client_connectivity_tools()
    register_ssid_device_policy_tools()

# ==================== RF PROFILE MANAGEMENT ====================

def register_rf_profile_tools():
    """Register RF profile management tools."""
    
    @app.tool(
        name="get_network_wireless_rf_profile",
        description="📡📻 Get details of a specific RF profile"
    )
    def get_network_wireless_rf_profile(
        network_id: str,
        rf_profile_id: str
    ):
        """Get details of a specific RF profile."""
        try:
            result = meraki_client.dashboard.wireless.getNetworkWirelessRfProfile(
                network_id, rf_profile_id
            )
            
            response = f"# 📻 RF Profile Details\n\n"
            response += f"**Name**: {result.get('name', 'Unknown')}\n"
            response += f"**ID**: {result.get('id', 'Unknown')}\n"
            response += f"**Client Balancing**: {'Enabled ✅' if result.get('clientBalancingEnabled') else 'Disabled ❌'}\n\n"
            
            # Band selection
            band_selection = result.get('bandSelectionType', 'ap')
            response += f"**Band Selection**: {band_selection}\n"
            
            # AP Band Settings
            ap_band = result.get('apBandSettings', {})
            if ap_band:
                response += "\n## AP Band Settings:\n"
                response += f"- **Mode**: {ap_band.get('mode', 'Unknown')}\n"
                if ap_band.get('bands', {}).get('enabled'):
                    response += f"- **Enabled Bands**: {', '.join(ap_band['bands']['enabled'])}\n"
            
            # Two-four GHz settings
            two_four = result.get('twoFourGhzSettings', {})
            if two_four:
                response += "\n## 2.4 GHz Settings:\n"
                response += f"- **Max Power**: {two_four.get('maxPower', 'Auto')} dBm\n"
                response += f"- **Min Power**: {two_four.get('minPower', 'Auto')} dBm\n"
                response += f"- **Min Bitrate**: {two_four.get('minBitrate', 'Auto')} Mbps\n"
                response += f"- **Valid Channels**: {two_four.get('validAutoChannels', [])}\n"
                response += f"- **Ax Enabled**: {two_four.get('axEnabled', False)}\n"
                response += f"- **RX-SOP**: {two_four.get('rxsop', 'Auto')}\n"
            
            # Five GHz settings
            five = result.get('fiveGhzSettings', {})
            if five:
                response += "\n## 5 GHz Settings:\n"
                response += f"- **Max Power**: {five.get('maxPower', 'Auto')} dBm\n"
                response += f"- **Min Power**: {five.get('minPower', 'Auto')} dBm\n"
                response += f"- **Min Bitrate**: {five.get('minBitrate', 'Auto')} Mbps\n"
                response += f"- **Valid Channels**: {five.get('validAutoChannels', [])}\n"
                response += f"- **Channel Width**: {five.get('channelWidth', 'Auto')}\n"
                response += f"- **RX-SOP**: {five.get('rxsop', 'Auto')}\n"
            
            # Six GHz settings
            six = result.get('sixGhzSettings', {})
            if six:
                response += "\n## 6 GHz Settings:\n"
                response += f"- **Max Power**: {six.get('maxPower', 'Auto')} dBm\n"
                response += f"- **Min Power**: {six.get('minPower', 'Auto')} dBm\n"
                response += f"- **Min Bitrate**: {six.get('minBitrate', 'Auto')} Mbps\n"
                response += f"- **Valid Channels**: {six.get('validAutoChannels', [])}\n"
                response += f"- **Channel Width**: {six.get('channelWidth', 'Auto')}\n"
            
            # Transmission settings
            transmission = result.get('transmission', {})
            if transmission:
                response += "\n## Transmission Settings:\n"
                response += f"- **Enabled**: {transmission.get('enabled', False)}\n"
            
            return response
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    @app.tool(
        name="create_network_wireless_rf_profile",
        description="📡📻 Create a new RF profile"
    )
    def create_network_wireless_rf_profile(
        network_id: str,
        name: str,
        band_selection_type: Optional[str] = 'ap',
        client_balancing_enabled: Optional[bool] = None,
        min_bitrate_2_4: Optional[float] = None,
        min_bitrate_5: Optional[float] = None
    ):
        """Create a new RF profile."""
        try:
            kwargs = {
                'name': name,
                'bandSelectionType': band_selection_type
            }
            
            if client_balancing_enabled is not None:
                kwargs['clientBalancingEnabled'] = client_balancing_enabled
            
            # 2.4 GHz settings
            if min_bitrate_2_4 is not None:
                kwargs['twoFourGhzSettings'] = {'minBitrate': min_bitrate_2_4}
            
            # 5 GHz settings
            if min_bitrate_5 is not None:
                kwargs['fiveGhzSettings'] = {'minBitrate': min_bitrate_5}
            
            result = meraki_client.dashboard.wireless.createNetworkWirelessRfProfile(
                network_id, **kwargs
            )
            
            response = f"# ✅ Created RF Profile\n\n"
            response += f"**Name**: {result.get('name', 'Unknown')}\n"
            response += f"**ID**: {result.get('id', 'Unknown')}\n"
            response += f"**Band Selection**: {result.get('bandSelectionType', 'Unknown')}\n"
            
            return response
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    @app.tool(
        name="update_network_wireless_rf_profile",
        description="📡📻 Update an existing RF profile"
    )
    def update_network_wireless_rf_profile(
        network_id: str,
        rf_profile_id: str,
        name: Optional[str] = None,
        client_balancing_enabled: Optional[bool] = None,
        min_bitrate_2_4: Optional[float] = None,
        min_bitrate_5: Optional[float] = None,
        max_power_2_4: Optional[int] = None,
        max_power_5: Optional[int] = None
    ):
        """Update an existing RF profile."""
        try:
            kwargs = {}
            
            if name:
                kwargs['name'] = name
            
            if client_balancing_enabled is not None:
                kwargs['clientBalancingEnabled'] = client_balancing_enabled
            
            # 2.4 GHz settings
            two_four_settings = {}
            if min_bitrate_2_4 is not None:
                two_four_settings['minBitrate'] = min_bitrate_2_4
            if max_power_2_4 is not None:
                two_four_settings['maxPower'] = max_power_2_4
            if two_four_settings:
                kwargs['twoFourGhzSettings'] = two_four_settings
            
            # 5 GHz settings
            five_settings = {}
            if min_bitrate_5 is not None:
                five_settings['minBitrate'] = min_bitrate_5
            if max_power_5 is not None:
                five_settings['maxPower'] = max_power_5
            if five_settings:
                kwargs['fiveGhzSettings'] = five_settings
            
            result = meraki_client.dashboard.wireless.updateNetworkWirelessRfProfile(
                network_id, rf_profile_id, **kwargs
            )
            
            response = f"# ✅ Updated RF Profile\n\n"
            response += f"**Name**: {result.get('name', 'Unknown')}\n"
            response += f"**ID**: {rf_profile_id}\n"
            
            return response
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    @app.tool(
        name="delete_network_wireless_rf_profile",
        description="📡📻 Delete an RF profile"
    )
    def delete_network_wireless_rf_profile(
        network_id: str,
        rf_profile_id: str
    ):
        """Delete an RF profile."""
        try:
            meraki_client.dashboard.wireless.deleteNetworkWirelessRfProfile(
                network_id, rf_profile_id
            )
            
            return f"# ✅ Deleted RF Profile\n\n**ID**: {rf_profile_id}"
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    @app.tool(
        name="get_organization_wireless_rf_profiles_assignments",
        description="📡📻 Get RF profile assignments by device"
    )
    def get_organization_wireless_rf_profiles_assignments(
        organization_id: str,
        include_templates: Optional[bool] = False,
        network_ids: Optional[str] = None,
        product_types: Optional[str] = None,
        per_page: Optional[int] = 1000
    ):
        """Get RF profile assignments by device."""
        try:
            kwargs = {
                'includeTemplates': include_templates,
                'perPage': per_page
            }
            if network_ids:
                kwargs['networkIds'] = network_ids.split(',')
            if product_types:
                kwargs['productTypes'] = product_types.split(',')
            
            result = meraki_client.dashboard.wireless.getOrganizationWirelessRfProfilesAssignmentsByDevice(
                organization_id, **kwargs
            )
            
            response = f"# 📻 RF Profile Assignments\n\n"
            
            if isinstance(result, list):
                response += f"**Total Devices**: {len(result)}\n\n"
                
                # Group by RF profile
                profile_groups = {}
                for device in result:
                    profile_id = device.get('rfProfile', {}).get('id', 'None')
                    profile_name = device.get('rfProfile', {}).get('name', 'Default')
                    
                    if profile_id not in profile_groups:
                        profile_groups[profile_id] = {
                            'name': profile_name,
                            'devices': []
                        }
                    profile_groups[profile_id]['devices'].append(device.get('serial'))
                
                response += "## Profile Distribution:\n"
                for profile_id, data in profile_groups.items():
                    response += f"- **{data['name']}**: {len(data['devices'])} devices\n"
                    if len(data['devices']) <= 5:
                        for serial in data['devices']:
                            response += f"  - {serial}\n"
            
            return response
        except Exception as e:
            return f"❌ Error: {str(e)}"

# ==================== AIR MARSHAL SECURITY ====================

def register_air_marshal_tools():
    """Register Air Marshal security tools."""
    
    @app.tool(
        name="get_organization_wireless_air_marshal_rules",
        description="📡🚨 Get Air Marshal rules for organization"
    )
    def get_organization_wireless_air_marshal_rules(
        organization_id: str,
        network_ids: Optional[str] = None,
        per_page: Optional[int] = 1000
    ):
        """Get Air Marshal rules for organization."""
        try:
            kwargs = {'perPage': per_page}
            if network_ids:
                kwargs['networkIds'] = network_ids.split(',')
            
            result = meraki_client.dashboard.wireless.getOrganizationWirelessAirMarshalRules(
                organization_id, **kwargs
            )
            
            response = f"# 🚨 Air Marshal Rules\n\n"
            
            if isinstance(result, list):
                response += f"**Total Rules**: {len(result)}\n\n"
                
                for i, rule in enumerate(result[:10], 1):  # Show first 10
                    response += f"## Rule {i}: {rule.get('ruleId', 'Unknown')}\n"
                    response += f"- **Type**: {rule.get('type', 'Unknown')}\n"
                    
                    match_rule = rule.get('match', {})
                    if match_rule:
                        response += f"- **Match String**: {match_rule.get('string', 'Any')}\n"
                        response += f"- **Match Type**: {match_rule.get('type', 'Any')}\n"
                    
                    # Networks
                    networks = rule.get('networks', [])
                    if networks:
                        response += f"- **Applied to**: {len(networks)} networks\n"
                    
                    response += "\n"
            
            return response
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    @app.tool(
        name="create_network_wireless_air_marshal_rule",
        description="📡🚨 Create a new Air Marshal rule"
    )
    def create_network_wireless_air_marshal_rule(
        network_id: str,
        type: str,
        match_string: str,
        match_type: str = 'contains'
    ):
        """Create a new Air Marshal rule."""
        try:
            result = meraki_client.dashboard.wireless.createNetworkWirelessAirMarshalRule(
                network_id,
                type=type,
                match={
                    'string': match_string,
                    'type': match_type
                }
            )
            
            response = f"# ✅ Created Air Marshal Rule\n\n"
            response += f"**Type**: {result.get('type', 'Unknown')}\n"
            response += f"**Rule ID**: {result.get('ruleId', 'Unknown')}\n"
            response += f"**Match**: {result.get('match', {}).get('string', 'Unknown')}\n"
            
            return response
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    @app.tool(
        name="update_network_wireless_air_marshal_rule",
        description="📡🚨 Update an Air Marshal rule"
    )
    def update_network_wireless_air_marshal_rule(
        network_id: str,
        rule_id: str,
        type: Optional[str] = None,
        match_string: Optional[str] = None,
        match_type: Optional[str] = None
    ):
        """Update an Air Marshal rule."""
        try:
            kwargs = {}
            if type:
                kwargs['type'] = type
            if match_string or match_type:
                kwargs['match'] = {}
                if match_string:
                    kwargs['match']['string'] = match_string
                if match_type:
                    kwargs['match']['type'] = match_type
            
            result = meraki_client.dashboard.wireless.updateNetworkWirelessAirMarshalRule(
                network_id, rule_id, **kwargs
            )
            
            response = f"# ✅ Updated Air Marshal Rule\n\n"
            response += f"**Rule ID**: {rule_id}\n"
            response += f"**Type**: {result.get('type', 'Unknown')}\n"
            
            return response
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    @app.tool(
        name="delete_network_wireless_air_marshal_rule",
        description="📡🚨 Delete an Air Marshal rule"
    )
    def delete_network_wireless_air_marshal_rule(
        network_id: str,
        rule_id: str
    ):
        """Delete an Air Marshal rule."""
        try:
            meraki_client.dashboard.wireless.deleteNetworkWirelessAirMarshalRule(
                network_id, rule_id
            )
            
            return f"# ✅ Deleted Air Marshal Rule\n\n**Rule ID**: {rule_id}"
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    @app.tool(
        name="update_network_wireless_air_marshal_settings",
        description="📡🚨 Update Air Marshal settings for network"
    )
    def update_network_wireless_air_marshal_settings(
        network_id: str,
        default_policy: str = 'allow'
    ):
        """Update Air Marshal settings for network."""
        try:
            result = meraki_client.dashboard.wireless.updateNetworkWirelessAirMarshalSettings(
                network_id,
                defaultPolicy=default_policy
            )
            
            response = f"# ✅ Updated Air Marshal Settings\n\n"
            response += f"**Default Policy**: {result.get('defaultPolicy', 'Unknown')}\n"
            
            return response
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    @app.tool(
        name="create_organization_wireless_air_marshal_rule",
        description="📡🚨 Create a new Air Marshal rule"
    )
    def create_organization_wireless_air_marshal_rule(
        organization_id: str,
        type: str,
        match_string: Optional[str] = None,
        match_type: Optional[str] = None,
        network_ids: Optional[str] = None
    ):
        """Create a new Air Marshal rule."""
        try:
            kwargs = {'type': type}
            
            if match_string or match_type:
                kwargs['match'] = {}
                if match_string:
                    kwargs['match']['string'] = match_string
                if match_type:
                    kwargs['match']['type'] = match_type
            
            if network_ids:
                kwargs['networkIds'] = json.loads(network_ids) if isinstance(network_ids, str) else network_ids
            
            result = meraki_client.dashboard.wireless.createOrganizationWirelessAirMarshalRule(
                organization_id, **kwargs
            )
            
            response = f"# ✅ Created Air Marshal Rule\n\n"
            response += f"**Rule ID**: {result.get('ruleId', 'Unknown')}\n"
            response += f"**Type**: {result.get('type', 'Unknown')}\n"
            
            match_rule = result.get('match', {})
            if match_rule:
                response += f"**Match String**: {match_rule.get('string', 'N/A')}\n"
                response += f"**Match Type**: {match_rule.get('type', 'N/A')}\n"
            
            networks = result.get('networks', [])
            if networks:
                response += f"\n**Applied to {len(networks)} networks**\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error creating Air Marshal rule: {str(e)}"
    
    @app.tool(
        name="update_organization_wireless_air_marshal_rule",
        description="📡🚨 Update an existing Air Marshal rule"
    )
    def update_organization_wireless_air_marshal_rule(
        organization_id: str,
        rule_id: str,
        type: Optional[str] = None,
        match_string: Optional[str] = None,
        match_type: Optional[str] = None,
        network_ids: Optional[str] = None
    ):
        """Update an existing Air Marshal rule."""
        try:
            kwargs = {}
            
            if type:
                kwargs['type'] = type
            
            if match_string or match_type:
                kwargs['match'] = {}
                if match_string:
                    kwargs['match']['string'] = match_string
                if match_type:
                    kwargs['match']['type'] = match_type
            
            if network_ids:
                kwargs['networkIds'] = json.loads(network_ids) if isinstance(network_ids, str) else network_ids
            
            result = meraki_client.dashboard.wireless.updateOrganizationWirelessAirMarshalRule(
                organization_id, rule_id, **kwargs
            )
            
            response = f"# ✅ Updated Air Marshal Rule\n\n"
            response += f"**Rule ID**: {result.get('ruleId', 'Unknown')}\n"
            response += f"**Type**: {result.get('type', 'Unknown')}\n"
            
            match_rule = result.get('match', {})
            if match_rule:
                response += f"**Match String**: {match_rule.get('string', 'N/A')}\n"
                response += f"**Match Type**: {match_rule.get('type', 'N/A')}\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error updating Air Marshal rule: {str(e)}"
    
    @app.tool(
        name="delete_organization_wireless_air_marshal_rule",
        description="📡🚨 Delete an Air Marshal rule"
    )
    def delete_organization_wireless_air_marshal_rule(
        organization_id: str,
        rule_id: str
    ):
        """Delete an Air Marshal rule."""
        try:
            meraki_client.dashboard.wireless.deleteOrganizationWirelessAirMarshalRule(
                organization_id, rule_id
            )
            
            return f"✅ Successfully deleted Air Marshal rule {rule_id}"
            
        except Exception as e:
            return f"❌ Error deleting Air Marshal rule: {str(e)}"
    
    @app.tool(
        name="get_organization_wireless_air_marshal_settings_by_network",
        description="📡🚨 Get Air Marshal settings for all networks"
    )
    def get_organization_wireless_air_marshal_settings_by_network(
        organization_id: str,
        network_ids: Optional[str] = None,
        per_page: Optional[int] = 1000
    ):
        """Get Air Marshal settings for all networks."""
        try:
            kwargs = {'perPage': per_page}
            if network_ids:
                kwargs['networkIds'] = network_ids.split(',')
            
            result = meraki_client.dashboard.wireless.getOrganizationWirelessAirMarshalSettingsByNetwork(
                organization_id, **kwargs
            )
            
            response = f"# 🚨 Air Marshal Settings by Network\n\n"
            
            if isinstance(result, list):
                response += f"**Total Networks**: {len(result)}\n\n"
                
                # Group by default policy
                allow_networks = [n for n in result if n.get('defaultPolicy') == 'allow']
                block_networks = [n for n in result if n.get('defaultPolicy') == 'block']
                
                response += f"## Policy Distribution:\n"
                response += f"- **Allow by default**: {len(allow_networks)} networks\n"
                response += f"- **Block by default**: {len(block_networks)} networks\n"
                
                if block_networks:
                    response += f"\n## Networks with Block Policy:\n"
                    for network in block_networks[:5]:
                        response += f"- {network.get('network', {}).get('name', 'Unknown')} ({network.get('networkId', 'Unknown')})\n"
            
            return response
        except Exception as e:
            return f"❌ Error: {str(e)}"

# ==================== CLIENT CONNECTIVITY TOOLS ====================

def register_client_connectivity_tools():
    """Register client connectivity analysis tools."""
    
    @app.tool(
        name="get_network_wireless_client_connectivity_events",
        description="📡📊 Get client connectivity events"
    )
    def get_network_wireless_client_connectivity_events(
        network_id: str,
        client_id: str,
        per_page: Optional[int] = 1000,
        starting_after: Optional[str] = None,
        ending_before: Optional[str] = None
    ):
        """Get client connectivity events."""
        try:
            kwargs = {'perPage': per_page}
            if starting_after:
                kwargs['startingAfter'] = starting_after
            if ending_before:
                kwargs['endingBefore'] = ending_before
            
            result = meraki_client.dashboard.wireless.getNetworkWirelessClientConnectivityEvents(
                network_id, client_id, **kwargs
            )
            
            response = f"# 📊 Client Connectivity Events\n\n"
            response += f"**Client**: {client_id}\n\n"
            
            if isinstance(result, list):
                response += f"**Total Events**: {len(result)}\n\n"
                
                # Group by event type
                event_types = {}
                for event in result:
                    event_type = event.get('type', 'Unknown')
                    if event_type not in event_types:
                        event_types[event_type] = 0
                    event_types[event_type] += 1
                
                response += "## Event Distribution:\n"
                for event_type, count in event_types.items():
                    response += f"- **{event_type}**: {count} events\n"
                
                # Show recent events
                response += "\n## Recent Events:\n"
                for event in result[:5]:
                    response += f"- **{event.get('type', 'Unknown')}** at {event.get('occurredAt', 'Unknown')}\n"
                    response += f"  - SSID: {event.get('ssidNumber', 'Unknown')}\n"
                    response += f"  - AP: {event.get('deviceSerial', 'Unknown')}\n"
                    response += f"  - Band: {event.get('band', 'Unknown')}\n"
                    response += f"  - Channel: {event.get('channel', 'Unknown')}\n\n"
            
            return response
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    @app.tool(
        name="get_network_wireless_client_connection_stats",
        description="📡📈 Get aggregated client connection statistics"
    )
    def get_network_wireless_client_connection_stats(
        network_id: str,
        client_id: str,
        t0: Optional[str] = None,
        t1: Optional[str] = None,
        timespan: Optional[float] = 86400,
        ssid: Optional[int] = None,
        vlan: Optional[int] = None,
        ap_tag: Optional[str] = None
    ):
        """Get aggregated client connection statistics."""
        try:
            kwargs = {'timespan': timespan}
            if t0: kwargs['t0'] = t0
            if t1: kwargs['t1'] = t1
            if ssid is not None: kwargs['ssid'] = ssid
            if vlan is not None: kwargs['vlan'] = vlan
            if ap_tag: kwargs['apTag'] = ap_tag
            
            result = meraki_client.dashboard.wireless.getNetworkWirelessClientConnectionStats(
                network_id, client_id, **kwargs
            )
            
            response = f"# 📈 Client Connection Statistics\n\n"
            response += f"**Client**: {client_id}\n\n"
            
            if isinstance(result, dict):
                connection_stats = result.get('connectionStats', {})
                
                response += "## Connection Success Rates:\n"
                response += f"- **Overall**: {connection_stats.get('success', 0)}%\n"
                response += f"- **Authentication**: {connection_stats.get('auth', 0)}%\n"
                response += f"- **Association**: {connection_stats.get('assoc', 0)}%\n"
                response += f"- **DHCP**: {connection_stats.get('dhcp', 0)}%\n"
                response += f"- **DNS**: {connection_stats.get('dns', 0)}%\n"
            
            return response
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    @app.tool(
        name="get_network_wireless_client_latency_stats",
        description="📡⏱️ Get client latency statistics"
    )
    def get_network_wireless_client_latency_stats(
        network_id: str,
        client_id: str,
        t0: Optional[str] = None,
        t1: Optional[str] = None,
        timespan: Optional[float] = 86400,
        ssid: Optional[int] = None,
        vlan: Optional[int] = None,
        ap_tag: Optional[str] = None
    ):
        """Get client latency statistics."""
        try:
            kwargs = {'timespan': timespan}
            if t0: kwargs['t0'] = t0
            if t1: kwargs['t1'] = t1
            if ssid is not None: kwargs['ssid'] = ssid
            if vlan is not None: kwargs['vlan'] = vlan
            if ap_tag: kwargs['apTag'] = ap_tag
            
            result = meraki_client.dashboard.wireless.getNetworkWirelessClientLatencyStats(
                network_id, client_id, **kwargs
            )
            
            response = f"# ⏱️ Client Latency Statistics\n\n"
            response += f"**Client**: {client_id}\n\n"
            
            if isinstance(result, dict):
                response += "## Latency by Traffic Type:\n"
                
                for traffic_type in ['backgroundTraffic', 'bestEffortTraffic', 'videoTraffic', 'voiceTraffic']:
                    traffic_data = result.get(traffic_type, {})
                    if traffic_data:
                        response += f"\n### {traffic_type.replace('Traffic', ' Traffic').title()}:\n"
                        response += f"- **Average**: {traffic_data.get('avg', 0)}ms\n"
                        response += f"- **Min**: {traffic_data.get('min', 0)}ms\n"
                        response += f"- **Max**: {traffic_data.get('max', 0)}ms\n"
            
            return response
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    @app.tool(
        name="get_network_wireless_client_latency_history",
        description="📡📉 Get historical client latency data"
    )
    def get_network_wireless_client_latency_history(
        network_id: str,
        client_id: str,
        t0: Optional[str] = None,
        t1: Optional[str] = None,
        timespan: Optional[float] = 86400,
        resolution: Optional[int] = None,
        ssid: Optional[int] = None,
        ap_tag: Optional[str] = None
    ):
        """Get historical client latency data."""
        try:
            kwargs = {'timespan': timespan}
            if t0: kwargs['t0'] = t0
            if t1: kwargs['t1'] = t1
            if resolution: kwargs['resolution'] = resolution
            if ssid is not None: kwargs['ssid'] = ssid
            if ap_tag: kwargs['apTag'] = ap_tag
            
            result = meraki_client.dashboard.wireless.getNetworkWirelessClientLatencyHistory(
                network_id, client_id, **kwargs
            )
            
            response = f"# 📉 Client Latency History\n\n"
            response += f"**Client**: {client_id}\n\n"
            
            if isinstance(result, list):
                response += f"**Data Points**: {len(result)}\n\n"
                
                if result:
                    # Calculate averages
                    latencies = [point.get('latencyMs', 0) for point in result if point.get('latencyMs')]
                    if latencies:
                        response += f"## Latency Summary:\n"
                        response += f"- **Average**: {sum(latencies) // len(latencies)}ms\n"
                        response += f"- **Min**: {min(latencies)}ms\n"
                        response += f"- **Max**: {max(latencies)}ms\n\n"
                    
                    # Show recent data
                    response += "## Recent Measurements:\n"
                    for point in result[-5:]:
                        response += f"- {point.get('t', 'Unknown')}: {point.get('latencyMs', 0)}ms\n"
            
            return response
        except Exception as e:
            return f"❌ Error: {str(e)}"

# ==================== SSID DEVICE TYPE GROUP POLICIES ====================

def register_ssid_device_policy_tools():
    """Register SSID device type group policy tools."""
    
    @app.tool(
        name="get_network_wireless_ssid_device_type_group_policies",
        description="📡📱 Get device type group policies for SSID"
    )
    def get_network_wireless_ssid_device_type_group_policies(
        network_id: str,
        number: str
    ):
        """Get device type group policies for SSID."""
        try:
            result = meraki_client.dashboard.wireless.getNetworkWirelessSsidDeviceTypeGroupPolicies(
                network_id, number
            )
            
            response = f"# 📱 SSID {number} Device Type Policies\n\n"
            
            if isinstance(result, dict):
                enabled = result.get('enabled', False)
                response += f"**Status**: {'Enabled ✅' if enabled else 'Disabled ❌'}\n"
                
                if enabled:
                    policies = result.get('deviceTypePolicies', [])
                    if policies:
                        response += f"\n## Device Type Policies ({len(policies)}):\n"
                        for policy in policies:
                            response += f"- **{policy.get('deviceType', 'Unknown')}**\n"
                            response += f"  - Policy: {policy.get('devicePolicy', 'Unknown')}\n"
                            response += f"  - Group Policy ID: {policy.get('groupPolicyId', 'None')}\n"
            
            return response
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    @app.tool(
        name="update_network_wireless_ssid_device_type_group_policies",
        description="📡📱 Update device type group policies for SSID"
    )
    def update_network_wireless_ssid_device_type_group_policies(
        network_id: str,
        number: str,
        enabled: Optional[bool] = None,
        device_type_policies: Optional[str] = None
    ):
        """Update device type group policies for SSID."""
        try:
            kwargs = {}
            if enabled is not None:
                kwargs['enabled'] = enabled
            if device_type_policies:
                kwargs['deviceTypePolicies'] = json.loads(device_type_policies)
            
            result = meraki_client.dashboard.wireless.updateNetworkWirelessSsidDeviceTypeGroupPolicies(
                network_id, number, **kwargs
            )
            
            response = f"# ✅ Updated Device Type Policies\n\n"
            response += f"**Status**: {'Enabled ✅' if result.get('enabled') else 'Disabled ❌'}\n"
            
            policies = result.get('deviceTypePolicies', [])
            if policies:
                response += f"**Configured Policies**: {len(policies)}\n"
            
            return response
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    @app.tool(
        name="get_organization_wireless_clients_overview_by_device",
        description="📡📊 Get wireless client overview by device"
    )
    def get_organization_wireless_clients_overview_by_device(
        organization_id: str,
        t0: Optional[str] = None,
        t1: Optional[str] = None,
        timespan: Optional[float] = 86400,
        per_page: Optional[int] = 1000
    ):
        """Get wireless client overview by device."""
        try:
            kwargs = {'timespan': timespan, 'perPage': per_page}
            if t0: kwargs['t0'] = t0
            if t1: kwargs['t1'] = t1
            
            result = meraki_client.dashboard.wireless.getOrganizationWirelessClientsOverviewByDevice(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Wireless Clients Overview by Device\n\n"
            
            if isinstance(result, list):
                response += f"**Total Devices**: {len(result)}\n\n"
                
                # Find busiest APs
                sorted_devices = sorted(result, key=lambda x: x.get('counts', {}).get('total', 0), reverse=True)
                
                response += "## Top 10 Busiest APs:\n"
                for device in sorted_devices[:10]:
                    counts = device.get('counts', {})
                    response += f"- **{device.get('serial', 'Unknown')}**\n"
                    response += f"  - Total Clients: {counts.get('total', 0)}\n"
                    response += f"  - By Status: {counts.get('byStatus', {})}\n"
                
                # Usage statistics
                total_usage = sum(d.get('usage', {}).get('total', 0) for d in result)
                response += f"\n## Total Usage: {total_usage / (1024*1024*1024):.2f} GB\n"
            
            return response
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    @app.tool(
        name="get_organization_wireless_ssids_statuses_by_device",
        description="📡📊 Get SSID statuses by device"
    )
    def get_organization_wireless_ssids_statuses_by_device(
        organization_id: str,
        network_ids: Optional[str] = None,
        serials: Optional[str] = None,
        bssids: Optional[str] = None,
        per_page: Optional[int] = 1000
    ):
        """Get SSID statuses by device."""
        try:
            kwargs = {'perPage': per_page}
            if network_ids: kwargs['networkIds'] = network_ids.split(',')
            if serials: kwargs['serials'] = serials.split(',')
            if bssids: kwargs['bssids'] = bssids.split(',')
            
            result = meraki_client.dashboard.wireless.getOrganizationWirelessSsidsStatusesByDevice(
                organization_id, **kwargs
            )
            
            response = f"# 📊 SSID Statuses by Device\n\n"
            
            if isinstance(result, list):
                response += f"**Total Devices**: {len(result)}\n\n"
                
                # Count enabled SSIDs
                for device in result[:5]:
                    response += f"## Device: {device.get('serial', 'Unknown')}\n"
                    
                    basic_service_sets = device.get('basicServiceSets', [])
                    if basic_service_sets:
                        enabled_count = sum(1 for bss in basic_service_sets if bss.get('enabled'))
                        response += f"- **Enabled SSIDs**: {enabled_count}/{len(basic_service_sets)}\n"
                        
                        for bss in basic_service_sets[:3]:
                            if bss.get('enabled'):
                                response += f"  - SSID {bss.get('ssidNumber', '?')}: {bss.get('ssidName', 'Unknown')}\n"
                                response += f"    Band: {bss.get('band', 'Unknown')}, Channel: {bss.get('channel', 'Unknown')}\n"
                    response += "\n"
            
            return response
        except Exception as e:
            return f"❌ Error: {str(e)}"