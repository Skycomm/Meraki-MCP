"""
Additional Sensor endpoints for Cisco Meraki MCP Server.
Auto-generated to achieve 100% API coverage.
"""

# Global variables to store app and meraki client
app = None
meraki_client = None

def format_dict_response(data: dict, resource_name: str) -> str:
    """Format dictionary response."""
    result = f"# {resource_name}\n\n"
    for key, value in data.items():
        if value is not None:
            result += f"**{key}**: {value}\n"
    return result

def format_list_response(data: list, resource_name: str) -> str:
    """Format list response."""
    if not data:
        return f"No {resource_name.lower()} found."
    
    result = f"# {resource_name}\n\n"
    result += f"**Total**: {len(data)}\n\n"
    
    for idx, item in enumerate(data[:10], 1):
        if isinstance(item, dict):
            name = item.get('name', item.get('id', f'Item {idx}'))
            result += f"## {name}\n"
            for key, value in item.items():
                if value is not None and key not in ['name']:
                    result += f"- **{key}**: {value}\n"
            result += "\n"
        else:
            result += f"- {item}\n"
    
    if len(data) > 10:
        result += f"\n... and {len(data) - 10} more items"
    
    return result

def register_sensor_additional_tools(mcp_app, meraki):
    """Register additional sensor tools with the MCP server."""
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    
    # Register all additional tools
    register_sensor_additional_handlers()

def register_sensor_additional_handlers():
    """Register additional sensor tool handlers."""

    @app.tool(
        name="create_device_sensor_command",
        description="➕ Create device sensor command"
    )
    def create_device_sensor_command(serial: str, **kwargs):
        """Create device sensor command."""
        try:
            result = meraki_client.dashboard.sensor.createDeviceSensorCommand(
                serial, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Device Sensor Command")
            elif isinstance(result, list):
                return format_list_response(result, "Device Sensor Command")
            else:
                return f"✅ Create device sensor command completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="create_network_sensor_alerts_profile",
        description="➕ Create network sensor alerts profile"
    )
    def create_network_sensor_alerts_profile(network_id: str, **kwargs):
        """Create network sensor alerts profile."""
        try:
            result = meraki_client.dashboard.sensor.createNetworkSensorAlertsProfile(
                network_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Sensor Alerts Profile")
            elif isinstance(result, list):
                return format_list_response(result, "Network Sensor Alerts Profile")
            else:
                return f"✅ Create network sensor alerts profile completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="delete_network_sensor_alerts_profile",
        description="🗑️ Delete network sensor alerts profile"
    )
    def delete_network_sensor_alerts_profile(network_id: str):
        """Delete network sensor alerts profile."""
        try:
            result = meraki_client.dashboard.sensor.deleteNetworkSensorAlertsProfile(
                network_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Sensor Alerts Profile")
            elif isinstance(result, list):
                return format_list_response(result, "Network Sensor Alerts Profile")
            else:
                return f"✅ Delete network sensor alerts profile completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_device_sensor_command",
        description="📊 Get device sensor command"
    )
    def get_device_sensor_command(serial: str):
        """Get device sensor command."""
        try:
            result = meraki_client.dashboard.sensor.getDeviceSensorCommand(
                serial
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Device Sensor Command")
            elif isinstance(result, list):
                return format_list_response(result, "Device Sensor Command")
            else:
                return f"✅ Get device sensor command completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_device_sensor_commands",
        description="📊 Get device sensor commands"
    )
    def get_device_sensor_commands(serial: str):
        """Get device sensor commands."""
        try:
            result = meraki_client.dashboard.sensor.getDeviceSensorCommands(
                serial
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Device Sensor Commands")
            elif isinstance(result, list):
                return format_list_response(result, "Device Sensor Commands")
            else:
                return f"✅ Get device sensor commands completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_device_sensor_relationships",
        description="📊 Get device sensor relationships"
    )
    def get_device_sensor_relationships(serial: str):
        """Get device sensor relationships."""
        try:
            result = meraki_client.dashboard.sensor.getDeviceSensorRelationships(
                serial
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Device Sensor Relationships")
            elif isinstance(result, list):
                return format_list_response(result, "Device Sensor Relationships")
            else:
                return f"✅ Get device sensor relationships completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_network_sensor_alerts_current_overview_by_metric",
        description="📊 Get network sensor alerts current overview by metric"
    )
    def get_network_sensor_alerts_current_overview_by_metric(network_id: str):
        """Get network sensor alerts current overview by metric."""
        try:
            result = meraki_client.dashboard.sensor.getNetworkSensorAlertsCurrentOverviewByMetric(
                network_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Sensor Alerts Current Overview By Metric")
            elif isinstance(result, list):
                return format_list_response(result, "Network Sensor Alerts Current Overview By Metric")
            else:
                return f"✅ Get network sensor alerts current overview by metric completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_network_sensor_alerts_overview_by_metric",
        description="📊 Get network sensor alerts overview by metric"
    )
    def get_network_sensor_alerts_overview_by_metric(network_id: str):
        """Get network sensor alerts overview by metric."""
        try:
            result = meraki_client.dashboard.sensor.getNetworkSensorAlertsOverviewByMetric(
                network_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Sensor Alerts Overview By Metric")
            elif isinstance(result, list):
                return format_list_response(result, "Network Sensor Alerts Overview By Metric")
            else:
                return f"✅ Get network sensor alerts overview by metric completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_network_sensor_alerts_profile",
        description="📊 Get network sensor alerts profile"
    )
    def get_network_sensor_alerts_profile(network_id: str):
        """Get network sensor alerts profile."""
        try:
            result = meraki_client.dashboard.sensor.getNetworkSensorAlertsProfile(
                network_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Sensor Alerts Profile")
            elif isinstance(result, list):
                return format_list_response(result, "Network Sensor Alerts Profile")
            else:
                return f"✅ Get network sensor alerts profile completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_network_sensor_mqtt_broker",
        description="📊 Get network sensor mqtt broker"
    )
    def get_network_sensor_mqtt_broker(network_id: str):
        """Get network sensor mqtt broker."""
        try:
            result = meraki_client.dashboard.sensor.getNetworkSensorMqttBroker(
                network_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Sensor Mqtt Broker")
            elif isinstance(result, list):
                return format_list_response(result, "Network Sensor Mqtt Broker")
            else:
                return f"✅ Get network sensor mqtt broker completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_network_sensor_relationships",
        description="📊 Get network sensor relationships"
    )
    def get_network_sensor_relationships(network_id: str):
        """Get network sensor relationships."""
        try:
            result = meraki_client.dashboard.sensor.getNetworkSensorRelationships(
                network_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Sensor Relationships")
            elif isinstance(result, list):
                return format_list_response(result, "Network Sensor Relationships")
            else:
                return f"✅ Get network sensor relationships completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_sensor_readings_history",
        description="📊 Get organization sensor readings history"
    )
    def get_organization_sensor_readings_history(organization_id: str):
        """Get organization sensor readings history."""
        try:
            result = meraki_client.dashboard.sensor.getOrganizationSensorReadingsHistory(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Sensor Readings History")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Sensor Readings History")
            else:
                return f"✅ Get organization sensor readings history completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="get_organization_sensor_readings_latest",
        description="📊 Get organization sensor readings latest"
    )
    def get_organization_sensor_readings_latest(organization_id: str):
        """Get organization sensor readings latest."""
        try:
            result = meraki_client.dashboard.sensor.getOrganizationSensorReadingsLatest(
                organization_id
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Organization Sensor Readings Latest")
            elif isinstance(result, list):
                return format_list_response(result, "Organization Sensor Readings Latest")
            else:
                return f"✅ Get organization sensor readings latest completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="update_device_sensor_relationships",
        description="✏️ Update device sensor relationships"
    )
    def update_device_sensor_relationships(serial: str, **kwargs):
        """Update device sensor relationships."""
        try:
            result = meraki_client.dashboard.sensor.updateDeviceSensorRelationships(
                serial, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Device Sensor Relationships")
            elif isinstance(result, list):
                return format_list_response(result, "Device Sensor Relationships")
            else:
                return f"✅ Update device sensor relationships completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="update_network_sensor_alerts_profile",
        description="✏️ Update network sensor alerts profile"
    )
    def update_network_sensor_alerts_profile(network_id: str, **kwargs):
        """Update network sensor alerts profile."""
        try:
            result = meraki_client.dashboard.sensor.updateNetworkSensorAlertsProfile(
                network_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Sensor Alerts Profile")
            elif isinstance(result, list):
                return format_list_response(result, "Network Sensor Alerts Profile")
            else:
                return f"✅ Update network sensor alerts profile completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"

    @app.tool(
        name="update_network_sensor_mqtt_broker",
        description="✏️ Update network sensor mqtt broker"
    )
    def update_network_sensor_mqtt_broker(network_id: str, **kwargs):
        """Update network sensor mqtt broker."""
        try:
            result = meraki_client.dashboard.sensor.updateNetworkSensorMqttBroker(
                network_id, **kwargs
            )
            
            if isinstance(result, dict):
                return format_dict_response(result, "Network Sensor Mqtt Broker")
            elif isinstance(result, list):
                return format_list_response(result, "Network Sensor Mqtt Broker")
            else:
                return f"✅ Update network sensor mqtt broker completed successfully!"
                
        except Exception as e:
            return f"Error: {str(e)}"
