"""
Sensor (MT) management tools for Cisco Meraki MCP server.

This module provides tools for managing MT sensors, alerts, MQTT brokers, and readings.
"""

from typing import Optional, Dict, Any, List
from datetime import datetime
import json

# Global references to be set by register function
app = None
meraki_client = None

def register_sensor_tools(mcp_app, meraki):
    """
    Register sensor tools with the MCP server.
    
    Args:
        mcp_app: MCP server instance
        meraki: Meraki client instance
    """
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    
    # ==================== SENSOR COMMANDS ====================
    
    @app.tool(
        name="create_device_sensor_command",
        description="🌡️📡 Send command to MT sensor (operations: reboot, blink)"
    )
    def create_device_sensor_command(
        serial: str,
        operation: str
    ):
        """
        Send a command to a sensor device.
        
        Args:
            serial: Device serial number
            operation: Command operation (e.g., 'reboot', 'blink')
        """
        try:
            result = meraki_client.dashboard.sensor.createDeviceSensorCommand(
                serial, operation=operation
            )
            
            response = f"# ✅ Sensor Command Sent\n\n"
            response += f"**Device**: {serial}\n"
            response += f"**Operation**: {operation}\n"
            response += f"**Command ID**: {result.get('id', 'N/A')}\n"
            response += f"**Status**: {result.get('status', 'pending')}\n\n"
            
            response += "Use get_device_sensor_command to check status.\n"
            
            return response
        except Exception as e:
            return f"❌ Error sending command: {str(e)}"
    
    @app.tool(
        name="get_device_sensor_command",
        description="🌡️🔍 Get status of a specific sensor command"
    )
    def get_device_sensor_command(
        serial: str,
        command_id: str
    ):
        """Get sensor command status."""
        try:
            result = meraki_client.dashboard.sensor.getDeviceSensorCommand(
                serial, command_id
            )
            
            response = f"# 🌡️ Sensor Command Status\n\n"
            response += f"**Command ID**: {command_id}\n"
            response += f"**Operation**: {result.get('operation', 'N/A')}\n"
            response += f"**Status**: {result.get('status', 'unknown')}\n"
            response += f"**Created**: {result.get('createdAt', 'N/A')}\n"
            
            # Show errors if any
            errors = result.get('errors', [])
            if errors:
                response += f"\n## Errors\n"
                for error in errors:
                    response += f"- {error}\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting command status: {str(e)}"
    
    @app.tool(
        name="get_device_sensor_commands",
        description="🌡️📋 List all commands sent to a sensor device"
    )
    def get_device_sensor_commands(
        serial: str,
        operations: Optional[str] = None,
        per_page: Optional[int] = 10
    ):
        """
        Get all commands for a sensor device.
        
        Args:
            serial: Device serial number
            operations: Comma-separated list of operations to filter
            per_page: Number of results per page
        """
        try:
            kwargs = {}
            if operations:
                kwargs['operations'] = [o.strip() for o in operations.split(',')]
            if per_page:
                kwargs['perPage'] = per_page
            
            result = meraki_client.dashboard.sensor.getDeviceSensorCommands(
                serial, **kwargs
            )
            
            response = f"# 🌡️ Sensor Commands History\n\n"
            response += f"**Device**: {serial}\n\n"
            
            if result and isinstance(result, list):
                for cmd in result:
                    status_icon = "✅" if cmd.get('status') == 'complete' else "⏳"
                    response += f"## {status_icon} {cmd.get('operation', 'Unknown')}\n"
                    response += f"- ID: {cmd.get('id')}\n"
                    response += f"- Status: {cmd.get('status')}\n"
                    response += f"- Created: {cmd.get('createdAt')}\n\n"
            else:
                response += "*No commands found*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting commands: {str(e)}"
    
    # ==================== SENSOR RELATIONSHIPS ====================
    
    @app.tool(
        name="get_device_sensor_relationships",
        description="🌡️🔗 Get sensor relationships (parent gateway/camera)"
    )
    def get_device_sensor_relationships(
        serial: str
    ):
        """Get sensor device relationships."""
        try:
            result = meraki_client.dashboard.sensor.getDeviceSensorRelationships(serial)
            
            response = f"# 🔗 Sensor Relationships\n\n"
            response += f"**Sensor**: {serial}\n\n"
            
            if result:
                # Show livestream relationship
                livestream = result.get('livestream')
                if livestream:
                    response += "## 📹 Livestream\n"
                    related = livestream.get('relatedDevices', [])
                    for device in related:
                        response += f"- {device.get('productType', 'Unknown')}: {device.get('serial')}\n"
                
                # Show other relationships
                for key, value in result.items():
                    if key != 'livestream' and value:
                        response += f"\n## {key.title()}\n"
                        response += f"- {value}\n"
            else:
                response += "*No relationships configured*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting relationships: {str(e)}"
    
    @app.tool(
        name="update_device_sensor_relationships",
        description="🌡️🔗 Update sensor relationships (link to camera/gateway)"
    )
    def update_device_sensor_relationships(
        serial: str,
        livestream_related_devices: Optional[str] = None
    ):
        """
        Update sensor relationships.
        
        Args:
            serial: Sensor serial number
            livestream_related_devices: Comma-separated camera serials for livestream
        """
        try:
            kwargs = {}
            
            if livestream_related_devices:
                devices = []
                for device_serial in livestream_related_devices.split(','):
                    devices.append({'serial': device_serial.strip()})
                kwargs['livestream'] = {'relatedDevices': devices}
            
            result = meraki_client.dashboard.sensor.updateDeviceSensorRelationships(
                serial, **kwargs
            )
            
            response = f"# ✅ Sensor Relationships Updated\n\n"
            response += f"**Sensor**: {serial}\n\n"
            
            if livestream_related_devices:
                response += f"**Linked Cameras**: {livestream_related_devices}\n"
            
            return response
        except Exception as e:
            return f"❌ Error updating relationships: {str(e)}"
    
    @app.tool(
        name="get_network_sensor_relationships",
        description="🌡️🔗 Get all sensor relationships in a network"
    )
    def get_network_sensor_relationships(
        network_id: str
    ):
        """Get all sensor relationships in network."""
        try:
            result = meraki_client.dashboard.sensor.getNetworkSensorRelationships(network_id)
            
            response = f"# 🔗 Network Sensor Relationships\n\n"
            
            if result and isinstance(result, list):
                response += f"**Total Sensors**: {len(result)}\n\n"
                
                for sensor in result:
                    device = sensor.get('device', {})
                    response += f"## {device.get('name', 'Unknown')} ({device.get('serial')})\n"
                    
                    relationships = sensor.get('relationships', {})
                    livestream = relationships.get('livestream', {})
                    related = livestream.get('relatedDevices', [])
                    
                    if related:
                        response += "- Linked cameras:\n"
                        for cam in related:
                            response += f"  - {cam.get('serial')}\n"
                    else:
                        response += "- No linked devices\n"
                    response += "\n"
            else:
                response += "*No sensors with relationships found*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting relationships: {str(e)}"
    
    # ==================== SENSOR ALERTS ====================
    
    @app.tool(
        name="get_network_sensor_alerts_profiles",
        description="🌡️🚨 List all sensor alert profiles in a network"
    )
    def get_network_sensor_alerts_profiles(
        network_id: str
    ):
        """Get all sensor alert profiles."""
        try:
            result = meraki_client.dashboard.sensor.getNetworkSensorAlertsProfiles(network_id)
            
            response = f"# 🚨 Sensor Alert Profiles\n\n"
            
            if result and isinstance(result, list):
                response += f"**Total Profiles**: {len(result)}\n\n"
                
                for profile in result:
                    response += f"## {profile.get('name', 'Unknown')}\n"
                    response += f"- ID: {profile.get('id')}\n"
                    
                    # Show conditions
                    conditions = profile.get('conditions', [])
                    if conditions:
                        response += f"- Conditions: {len(conditions)}\n"
                        for cond in conditions[:3]:
                            metric = cond.get('metric', 'unknown')
                            threshold = cond.get('threshold', {})
                            response += f"  - {metric}: {threshold.get('temperature', {}).get('celsius', 'N/A')}°C\n"
                    
                    response += "\n"
            else:
                response += "*No alert profiles configured*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting alert profiles: {str(e)}"
    
    @app.tool(
        name="get_network_sensor_alerts_profile",
        description="🌡️🚨 Get details of a specific sensor alert profile"
    )
    def get_network_sensor_alerts_profile(
        network_id: str,
        profile_id: str
    ):
        """Get sensor alert profile details."""
        try:
            result = meraki_client.dashboard.sensor.getNetworkSensorAlertsProfile(
                network_id, profile_id
            )
            
            response = f"# 🚨 Alert Profile Details\n\n"
            response += f"**Name**: {result.get('name', 'Unknown')}\n"
            response += f"**ID**: {profile_id}\n\n"
            
            # Show conditions
            conditions = result.get('conditions', [])
            if conditions:
                response += "## Alert Conditions\n\n"
                for cond in conditions:
                    metric = cond.get('metric', 'unknown')
                    direction = cond.get('direction', 'above')
                    threshold = cond.get('threshold', {})
                    
                    response += f"### {metric.title()}\n"
                    response += f"- Direction: {direction}\n"
                    
                    # Temperature thresholds
                    temp = threshold.get('temperature', {})
                    if temp:
                        response += f"- Temperature: {temp.get('celsius')}°C / {temp.get('fahrenheit')}°F\n"
                    
                    # Other thresholds
                    for key, value in threshold.items():
                        if key != 'temperature':
                            response += f"- {key.title()}: {value}\n"
                    response += "\n"
            
            # Show recipients
            recipients = result.get('recipients', {})
            if recipients:
                response += "## Recipients\n"
                emails = recipients.get('emails', [])
                if emails:
                    response += f"- Emails: {', '.join(emails)}\n"
                webhooks = recipients.get('httpServerIds', [])
                if webhooks:
                    response += f"- Webhooks: {len(webhooks)} configured\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting alert profile: {str(e)}"
    
    @app.tool(
        name="create_network_sensor_alerts_profile",
        description="🌡️➕ Create sensor alert profile (metrics: temperature/humidity/water/door, direction: above/below)"
    )
    def create_network_sensor_alerts_profile(
        network_id: str,
        name: str,
        metric: str,
        direction: str,
        temperature_celsius: Optional[float] = None,
        humidity_percent: Optional[int] = None,
        email_recipients: Optional[str] = None
    ):
        """
        Create sensor alert profile.
        
        Args:
            network_id: Network ID
            name: Profile name
            metric: Metric to monitor (temperature/humidity/water/door)
            direction: Alert direction (above/below)
            temperature_celsius: Temperature threshold in Celsius
            humidity_percent: Humidity threshold percentage
            email_recipients: Comma-separated email addresses
        """
        try:
            # Build conditions
            conditions = []
            condition = {'metric': metric, 'direction': direction, 'threshold': {}}
            
            if metric == 'temperature' and temperature_celsius:
                condition['threshold']['temperature'] = {
                    'celsius': temperature_celsius,
                    'fahrenheit': (temperature_celsius * 9/5) + 32
                }
            elif metric == 'humidity' and humidity_percent:
                condition['threshold']['relativePercentage'] = humidity_percent
            
            conditions.append(condition)
            
            kwargs = {
                'name': name,
                'conditions': conditions
            }
            
            # Add recipients
            if email_recipients:
                emails = [e.strip() for e in email_recipients.split(',')]
                kwargs['recipients'] = {'emails': emails}
            
            result = meraki_client.dashboard.sensor.createNetworkSensorAlertsProfile(
                network_id, **kwargs
            )
            
            response = f"# ✅ Alert Profile Created\n\n"
            response += f"**Name**: {name}\n"
            response += f"**ID**: {result.get('id')}\n"
            response += f"**Metric**: {metric} {direction} threshold\n"
            
            return response
        except Exception as e:
            return f"❌ Error creating alert profile: {str(e)}"
    
    @app.tool(
        name="update_network_sensor_alerts_profile",
        description="🌡️✏️ Update a sensor alert profile"
    )
    def update_network_sensor_alerts_profile(
        network_id: str,
        profile_id: str,
        name: Optional[str] = None,
        email_recipients: Optional[str] = None
    ):
        """Update sensor alert profile."""
        try:
            kwargs = {}
            if name:
                kwargs['name'] = name
            if email_recipients:
                emails = [e.strip() for e in email_recipients.split(',')]
                kwargs['recipients'] = {'emails': emails}
            
            result = meraki_client.dashboard.sensor.updateNetworkSensorAlertsProfile(
                network_id, profile_id, **kwargs
            )
            
            response = f"# ✅ Alert Profile Updated\n\n"
            response += f"**Profile ID**: {profile_id}\n"
            if name:
                response += f"**New Name**: {name}\n"
            
            return response
        except Exception as e:
            return f"❌ Error updating alert profile: {str(e)}"
    
    @app.tool(
        name="delete_network_sensor_alerts_profile",
        description="🌡️❌ Delete a sensor alert profile"
    )
    def delete_network_sensor_alerts_profile(
        network_id: str,
        profile_id: str
    ):
        """Delete sensor alert profile."""
        try:
            meraki_client.dashboard.sensor.deleteNetworkSensorAlertsProfile(
                network_id, profile_id
            )
            
            response = f"# ✅ Alert Profile Deleted\n\n"
            response += f"**Profile ID**: {profile_id}\n"
            
            return response
        except Exception as e:
            return f"❌ Error deleting alert profile: {str(e)}"
    
    # ==================== SENSOR ALERTS OVERVIEW ====================
    
    @app.tool(
        name="get_network_sensor_alerts_current_overview_by_metric",
        description="🌡️📊 Get current sensor alerts overview by metric"
    )
    def get_network_sensor_alerts_current_overview_by_metric(
        network_id: str
    ):
        """Get current alerts overview."""
        try:
            result = meraki_client.dashboard.sensor.getNetworkSensorAlertsCurrentOverviewByMetric(
                network_id
            )
            
            response = f"# 📊 Current Sensor Alerts Overview\n\n"
            
            if result:
                counts = result.get('counts', {})
                response += "## Alert Counts by Metric\n\n"
                
                for metric, count in counts.items():
                    icon = "🌡️" if metric == "temperature" else "💧" if metric == "humidity" else "🚪" if metric == "door" else "📊"
                    response += f"{icon} **{metric.title()}**: {count} alerts\n"
                
                # Show supported metrics
                supported = result.get('supportedMetrics', [])
                if supported:
                    response += f"\n**Supported Metrics**: {', '.join(supported)}\n"
            else:
                response += "*No current alerts*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting alerts overview: {str(e)}"
    
    @app.tool(
        name="get_network_sensor_alerts_overview_by_metric",
        description="🌡️📈 Get historical sensor alerts overview"
    )
    def get_network_sensor_alerts_overview_by_metric(
        network_id: str,
        t0: Optional[str] = None,
        t1: Optional[str] = None,
        timespan: Optional[float] = 86400,
        interval: Optional[int] = None
    ):
        """Get historical alerts overview."""
        try:
            kwargs = {}
            if t0:
                kwargs['t0'] = t0
            if t1:
                kwargs['t1'] = t1
            if timespan:
                kwargs['timespan'] = timespan
            if interval:
                kwargs['interval'] = interval
            
            result = meraki_client.dashboard.sensor.getNetworkSensorAlertsOverviewByMetric(
                network_id, **kwargs
            )
            
            response = f"# 📈 Sensor Alerts History\n\n"
            response += f"**Timespan**: {timespan/3600:.1f} hours\n\n"
            
            if result and isinstance(result, list):
                for entry in result[:5]:  # Show first 5 time periods
                    response += f"## {entry.get('startTs', 'N/A')}\n"
                    counts = entry.get('counts', {})
                    for metric, count in counts.items():
                        response += f"- {metric.title()}: {count}\n"
                    response += "\n"
                
                if len(result) > 5:
                    response += f"*...and {len(result)-5} more time periods*\n"
            else:
                response += "*No alert history available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting alerts history: {str(e)}"
    
    # ==================== SENSOR READINGS ====================
    
    @app.tool(
        name="get_organization_sensor_readings_latest",
        description="🌡️📍 Get latest sensor readings (metrics: temperature,humidity,water,door,tvoc,pm25,noise)"
    )
    def get_organization_sensor_readings_latest(
        organization_id: str,
        per_page: Optional[int] = 10,
        network_ids: Optional[str] = None,
        serials: Optional[str] = None,
        metrics: Optional[str] = None
    ):
        """
        Get latest sensor readings.
        
        Args:
            organization_id: Organization ID
            per_page: Results per page
            network_ids: Comma-separated network IDs
            serials: Comma-separated device serials
            metrics: Comma-separated metrics (temperature,humidity,water,door,etc)
        """
        try:
            kwargs = {}
            if per_page:
                kwargs['perPage'] = per_page
            if network_ids:
                kwargs['networkIds'] = [n.strip() for n in network_ids.split(',')]
            if serials:
                kwargs['serials'] = [s.strip() for s in serials.split(',')]
            if metrics:
                kwargs['metrics'] = [m.strip() for m in metrics.split(',')]
            
            result = meraki_client.dashboard.sensor.getOrganizationSensorReadingsLatest(
                organization_id, **kwargs
            )
            
            response = f"# 📍 Latest Sensor Readings\n\n"
            
            if result and isinstance(result, list):
                for reading in result:
                    response += f"## {reading.get('serial', 'Unknown')}\n"
                    response += f"**Network**: {reading.get('network', {}).get('name', 'N/A')}\n"
                    response += f"**Time**: {reading.get('ts', 'N/A')}\n\n"
                    
                    # Show all readings
                    for metric in ['temperature', 'humidity', 'water', 'door', 'tvoc', 'pm25', 'noise', 'indoorAirQuality']:
                        value = reading.get(metric)
                        if value is not None:
                            if metric == 'temperature':
                                response += f"- 🌡️ Temperature: {value.get('celsius', 'N/A')}°C\n"
                            elif metric == 'humidity':
                                response += f"- 💧 Humidity: {value.get('relativePercentage', 'N/A')}%\n"
                            elif metric == 'water':
                                response += f"- 💦 Water: {'Detected' if value.get('present') else 'Not detected'}\n"
                            elif metric == 'door':
                                response += f"- 🚪 Door: {'Open' if value.get('open') else 'Closed'}\n"
                            elif metric == 'noise':
                                ambient = value.get('ambient', {})
                                response += f"- 🔊 Noise: {ambient.get('level', 'N/A')} dBA\n"
                            elif metric == 'pm25':
                                response += f"- 🌫️ PM2.5: {value.get('concentration', 'N/A')} µg/m³\n"
                            elif metric == 'tvoc':
                                response += f"- 🌬️ TVOC: {value.get('concentration', 'N/A')} ppb\n"
                            elif metric == 'indoorAirQuality':
                                response += f"- 🏠 Air Quality: {value.get('score', 'N/A')}/100\n"
                    
                    response += "\n"
            else:
                response += "*No sensor readings available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting sensor readings: {str(e)}"
    
    @app.tool(
        name="get_organization_sensor_readings_history",
        description="🌡️📈 Get historical sensor readings (use serials param for specific sensors)"
    )
    def get_organization_sensor_readings_history(
        organization_id: str,
        t0: Optional[str] = None,
        t1: Optional[str] = None,
        timespan: Optional[float] = 3600,
        network_ids: Optional[str] = None,
        serials: Optional[str] = None,
        metrics: Optional[str] = None
    ):
        """Get historical sensor readings."""
        try:
            kwargs = {}
            if t0:
                kwargs['t0'] = t0
            if t1:
                kwargs['t1'] = t1
            if timespan:
                kwargs['timespan'] = timespan
            if network_ids:
                kwargs['networkIds'] = [n.strip() for n in network_ids.split(',')]
            if serials:
                kwargs['serials'] = [s.strip() for s in serials.split(',')]
            if metrics:
                kwargs['metrics'] = [m.strip() for m in metrics.split(',')]
            
            result = meraki_client.dashboard.sensor.getOrganizationSensorReadingsHistory(
                organization_id, **kwargs
            )
            
            response = f"# 📈 Sensor Readings History\n\n"
            response += f"**Timespan**: {timespan/3600:.1f} hours\n\n"
            
            if result and isinstance(result, list):
                # Group by serial
                by_serial = {}
                for reading in result:
                    serial = reading.get('serial', 'Unknown')
                    if serial not in by_serial:
                        by_serial[serial] = []
                    by_serial[serial].append(reading)
                
                for serial, readings in list(by_serial.items())[:3]:  # Show first 3 devices
                    response += f"## Device: {serial}\n"
                    
                    # Show latest 3 readings
                    for reading in readings[:3]:
                        response += f"- {reading.get('ts', 'N/A')}: "
                        
                        # Temperature
                        temp = reading.get('temperature')
                        if temp:
                            response += f"{temp.get('celsius')}°C "
                        
                        # Humidity
                        humidity = reading.get('humidity')
                        if humidity:
                            response += f"{humidity.get('relativePercentage')}% "
                        
                        response += "\n"
                    
                    if len(readings) > 3:
                        response += f"  ...and {len(readings)-3} more readings\n"
                    response += "\n"
            else:
                response += "*No historical data available*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting readings history: {str(e)}"
    
    # ==================== MQTT BROKERS ====================
    
    @app.tool(
        name="get_network_sensor_mqtt_brokers",
        description="🌡️📡 List all MQTT brokers configured for sensors"
    )
    def get_network_sensor_mqtt_brokers(
        network_id: str
    ):
        """Get all MQTT brokers."""
        try:
            result = meraki_client.dashboard.sensor.getNetworkSensorMqttBrokers(network_id)
            
            response = f"# 📡 Sensor MQTT Brokers\n\n"
            
            if result and isinstance(result, list):
                response += f"**Total Brokers**: {len(result)}\n\n"
                
                for broker in result:
                    enabled_icon = "✅" if broker.get('enabled') else "❌"
                    response += f"## {enabled_icon} {broker.get('name', 'Unknown')}\n"
                    response += f"- ID: {broker.get('mqttBrokerId')}\n"
                    response += f"- Host: {broker.get('host')}:{broker.get('port', 1883)}\n"
                    response += f"- Security: {broker.get('security', {}).get('mode', 'none')}\n\n"
            else:
                response += "*No MQTT brokers configured*\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting MQTT brokers: {str(e)}"
    
    @app.tool(
        name="get_network_sensor_mqtt_broker",
        description="🌡️📡 Get details of a specific MQTT broker"
    )
    def get_network_sensor_mqtt_broker(
        network_id: str,
        mqtt_broker_id: str
    ):
        """Get MQTT broker details."""
        try:
            result = meraki_client.dashboard.sensor.getNetworkSensorMqttBroker(
                network_id, mqtt_broker_id
            )
            
            response = f"# 📡 MQTT Broker Details\n\n"
            response += f"**Name**: {result.get('name', 'Unknown')}\n"
            response += f"**ID**: {mqtt_broker_id}\n"
            response += f"**Enabled**: {'✅' if result.get('enabled') else '❌'}\n\n"
            
            response += "## Connection\n"
            response += f"- Host: {result.get('host')}\n"
            response += f"- Port: {result.get('port', 1883)}\n"
            
            security = result.get('security', {})
            response += f"- Security Mode: {security.get('mode', 'none')}\n"
            
            if security.get('mode') == 'tls':
                tls = security.get('tls', {})
                response += f"- CA Certificate: {'Configured' if tls.get('caCertificate') else 'Not set'}\n"
                response += f"- Verify Hostname: {tls.get('verifyHostnames', False)}\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting MQTT broker: {str(e)}"
    
    @app.tool(
        name="update_network_sensor_mqtt_broker",
        description="🌡️📡 Update MQTT broker configuration"
    )
    def update_network_sensor_mqtt_broker(
        network_id: str,
        mqtt_broker_id: str,
        enabled: Optional[bool] = None,
        name: Optional[str] = None,
        host: Optional[str] = None,
        port: Optional[int] = None
    ):
        """Update MQTT broker."""
        try:
            kwargs = {}
            if enabled is not None:
                kwargs['enabled'] = enabled
            if name:
                kwargs['name'] = name
            if host:
                kwargs['host'] = host
            if port:
                kwargs['port'] = port
            
            result = meraki_client.dashboard.sensor.updateNetworkSensorMqttBroker(
                network_id, mqtt_broker_id, **kwargs
            )
            
            response = f"# ✅ MQTT Broker Updated\n\n"
            response += f"**Broker ID**: {mqtt_broker_id}\n"
            
            if name:
                response += f"**Name**: {name}\n"
            if enabled is not None:
                response += f"**Status**: {'Enabled' if enabled else 'Disabled'}\n"
            if host:
                response += f"**Host**: {host}:{port or 1883}\n"
            
            return response
        except Exception as e:
            return f"❌ Error updating MQTT broker: {str(e)}"