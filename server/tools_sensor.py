"""
Environmental Sensor Tools for Cisco Meraki MCP Server
Monitor and manage environmental sensors across the network
"""

from mcp.server import FastMCP
from typing import Optional, Dict, Any, List
import json
from datetime import datetime, timedelta
from meraki_client import MerakiClient
from utils.helpers import format_error_message
from contextlib import contextmanager

# This will be set by register function
mcp_app = None
meraki = None

def format_error(operation: str, error: Exception) -> str:
    """Format error message with operation context."""
    return f"❌ Failed to {operation}: {format_error_message(error)}"

@contextmanager
def safe_api_call(operation: str):
    """Context manager for safe API calls with consistent error handling."""
    try:
        yield
    except Exception as e:
        raise Exception(f"Failed to {operation}: {str(e)}")


def get_network_sensor_alerts_profiles(network_id: str) -> str:
    """
    🚨 Get sensor alert profiles for a network.
    
    Shows configured alert profiles for environmental monitoring.
    
    Args:
        network_id: Network ID
    
    Returns:
        Formatted sensor alert profiles
    """
    try:
        with safe_api_call("get sensor alert profiles"):
            profiles = meraki.dashboard.sensor.getNetworkSensorAlertsProfiles(network_id)
            
            if not profiles:
                return f"No sensor alert profiles configured for network {network_id}"
            
            output = ["🚨 Sensor Alert Profiles", "=" * 50, ""]
            
            for profile in profiles:
                output.append(f"📋 Profile: {profile.get('name', 'Unnamed')}")
                output.append(f"   ID: {profile.get('profileId', 'N/A')}")
                
                # Conditions
                conditions = profile.get('conditions', [])
                if conditions:
                    output.append("   Conditions:")
                    for condition in conditions:
                        metric = condition.get('metric', 'Unknown')
                        threshold = condition.get('threshold', {})
                        
                        output.append(f"     • {metric}:")
                        if threshold.get('temperature'):
                            temp = threshold['temperature']
                            output.append(f"       Temperature: {temp.get('celsius', 'N/A')}°C")
                        if threshold.get('humidity'):
                            hum = threshold['humidity']
                            output.append(f"       Humidity: {hum.get('relativePercentage', 'N/A')}%")
                        if threshold.get('water'):
                            output.append(f"       Water: Present")
                        if threshold.get('door'):
                            output.append(f"       Door: Open")
                        
                        duration = condition.get('duration', 0)
                        if duration:
                            output.append(f"       Duration: {duration} minutes")
                
                # Recipients
                recipients = profile.get('recipients', {})
                emails = recipients.get('emails', [])
                if emails:
                    output.append(f"   📧 Email Recipients: {', '.join(emails)}")
                
                output.append("")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("get sensor alert profiles", e)


def get_network_sensor_readings(
    network_id: str,
    timespan: Optional[int] = 86400,
    metric: Optional[str] = None
) -> str:
    """
    📊 Get historical sensor readings.
    
    Shows environmental sensor data over time.
    
    Args:
        network_id: Network ID
        timespan: Time period in seconds (default: 86400 = 24 hours)
        metric: Specific metric (temperature, humidity, water, door, etc.)
    
    Returns:
        Formatted sensor readings
    """
    try:
        with safe_api_call("get sensor readings"):
            params = {'timespan': timespan}
            if metric:
                params['metric'] = metric
                
            readings = meraki.dashboard.sensor.getNetworkSensorAlertsCurrentOverviewByMetric(
                network_id,
                **params
            )
            
            output = ["📊 Sensor Readings", "=" * 50, ""]
            output.append(f"Time Period: Last {timespan // 3600} hours")
            if metric:
                output.append(f"Metric Filter: {metric}")
            output.append("")
            
            if readings:
                # Group by sensor
                by_sensor = {}
                for reading in readings:
                    sensor_name = reading.get('sensor', {}).get('name', 'Unknown Sensor')
                    if sensor_name not in by_sensor:
                        by_sensor[sensor_name] = []
                    by_sensor[sensor_name].append(reading)
                
                for sensor_name, sensor_readings in by_sensor.items():
                    output.append(f"🌡️ Sensor: {sensor_name}")
                    
                    # Get latest reading for each metric
                    metrics_data = {}
                    for reading in sensor_readings:
                        metric_type = reading.get('metric', 'Unknown')
                        value = reading.get('value', {})
                        
                        if metric_type == 'temperature':
                            temp_c = value.get('celsius')
                            temp_f = value.get('fahrenheit')
                            if temp_c is not None:
                                output.append(f"   🌡️ Temperature: {temp_c:.1f}°C ({temp_f:.1f}°F)")
                        elif metric_type == 'humidity':
                            humidity = value.get('relativePercentage')
                            if humidity is not None:
                                output.append(f"   💧 Humidity: {humidity:.1f}%")
                        elif metric_type == 'water':
                            present = value.get('present', False)
                            output.append(f"   💦 Water Detected: {'Yes ⚠️' if present else 'No ✅'}")
                        elif metric_type == 'door':
                            open_status = value.get('open', False)
                            output.append(f"   🚪 Door Status: {'Open 🔓' if open_status else 'Closed 🔒'}")
                        elif metric_type == 'tvoc':
                            tvoc = value.get('concentration')
                            if tvoc is not None:
                                output.append(f"   🌫️ Air Quality (TVOC): {tvoc} µg/m³")
                        elif metric_type == 'pm25':
                            pm25 = value.get('concentration')
                            if pm25 is not None:
                                output.append(f"   🌫️ PM2.5: {pm25} µg/m³")
                        elif metric_type == 'noise':
                            ambient = value.get('ambient', {})
                            level = ambient.get('level')
                            if level is not None:
                                output.append(f"   🔊 Noise Level: {level} dB")
                    
                    output.append("")
            else:
                output.append("No sensor readings available for this time period")
            
            # Add recommendations
            output.append("💡 Sensor Guidelines:")
            output.append("• Temperature: 20-24°C (68-75°F) optimal for comfort")
            output.append("• Humidity: 30-60% recommended range")
            output.append("• TVOC: <500 µg/m³ for good air quality")
            output.append("• PM2.5: <12 µg/m³ for healthy air")
            output.append("• Noise: <50 dB for office environments")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("get sensor readings", e)


def get_device_sensor_details(serial: str) -> str:
    """
    🌡️ Get details for a specific sensor device.
    
    Shows sensor configuration and current status.
    
    Args:
        serial: Device serial number
    
    Returns:
        Sensor device details
    """
    try:
        with safe_api_call("get sensor details"):
            # Get basic device info
            device = meraki.dashboard.devices.getDevice(serial)
            
            output = ["🌡️ Sensor Device Details", "=" * 50, ""]
            output.append(f"Name: {device.get('name', 'Unnamed')}")
            output.append(f"Model: {device.get('model', 'Unknown')}")
            output.append(f"Serial: {serial}")
            output.append(f"MAC: {device.get('mac', 'N/A')}")
            output.append("")
            
            # Get sensor-specific details
            if device.get('model', '').startswith('MT'):
                output.append("📊 Sensor Capabilities:")
                model = device['model']
                
                # MT sensor capabilities
                capabilities = {
                    'MT10': ['Temperature', 'Humidity'],
                    'MT11': ['Temperature', 'Humidity'],
                    'MT12': ['Temperature', 'Humidity', 'Water Detection'],
                    'MT14': ['Temperature', 'Humidity', 'Air Quality (TVOC)'],
                    'MT20': ['Door Open/Close'],
                    'MT30': ['Temperature', 'CO2', 'TVOC', 'PM2.5', 'Noise']
                }
                
                model_base = model.split('-')[0] if '-' in model else model
                caps = capabilities.get(model_base, ['Unknown'])
                for cap in caps:
                    output.append(f"   • {cap}")
                
                # Network info
                output.append(f"\n📡 Network: {device.get('networkId', 'N/A')}")
                
                # Connection info
                if device.get('gateway'):
                    output.append(f"🔗 Gateway: {device['gateway']}")
                if device.get('connectivity'):
                    output.append(f"📶 Connectivity: {device['connectivity']}")
                
                # Battery info for wireless sensors
                if device.get('batteryPercentage') is not None:
                    battery = device['batteryPercentage']
                    battery_icon = "🔋" if battery > 20 else "🪫"
                    output.append(f"{battery_icon} Battery: {battery}%")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("get sensor details", e)


def create_sensor_alert_profile(
    network_id: str,
    name: str,
    conditions: List[Dict[str, Any]],
    recipients: Dict[str, List[str]]
) -> str:
    """
    ➕ Create a new sensor alert profile.
    
    Configure alerts for environmental conditions.
    
    Args:
        network_id: Network ID
        name: Profile name
        conditions: List of alert conditions
        recipients: Alert recipients (emails, etc.)
    
    Returns:
        Creation result
    """
    try:
        with safe_api_call("create sensor alert profile"):
            profile = meraki.dashboard.sensor.createNetworkSensorAlertsProfile(
                network_id,
                name=name,
                conditions=conditions,
                recipients=recipients
            )
            
            output = ["✅ Sensor Alert Profile Created", "=" * 50, ""]
            output.append(f"Name: {profile.get('name', name)}")
            output.append(f"Profile ID: {profile.get('profileId', 'N/A')}")
            output.append("")
            
            output.append("📋 Configuration:")
            output.append(f"   Conditions: {len(conditions)}")
            
            emails = recipients.get('emails', [])
            if emails:
                output.append(f"   Recipients: {', '.join(emails)}")
            
            output.append("\n💡 Next Steps:")
            output.append("• Assign this profile to sensors")
            output.append("• Test alert delivery")
            output.append("• Adjust thresholds as needed")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("create sensor alert profile", e)


def get_sensor_command_history(serial: str) -> str:
    """
    📜 Get sensor command history.
    
    Shows commands sent to a sensor device.
    
    Args:
        serial: Device serial number
    
    Returns:
        Command history
    """
    try:
        with safe_api_call("get sensor command history"):
            commands = meraki.dashboard.sensor.getDeviceSensorCommands(serial)
            
            if not commands:
                return f"No command history for sensor {serial}"
            
            output = ["📜 Sensor Command History", "=" * 50, ""]
            
            for cmd in commands[:10]:  # Show last 10 commands
                output.append(f"🔧 Command: {cmd.get('commandId', 'Unknown')}")
                output.append(f"   Operation: {cmd.get('operation', 'N/A')}")
                output.append(f"   Status: {cmd.get('status', 'Unknown')}")
                output.append(f"   Time: {cmd.get('createdAt', 'N/A')}")
                
                if cmd.get('errors'):
                    output.append(f"   ❌ Error: {cmd['errors']}")
                
                output.append("")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("get sensor command history", e)


def analyze_sensor_environment(network_id: str) -> str:
    """
    🏢 Analyze overall environmental conditions.
    
    Provides insights and recommendations based on sensor data.
    
    Args:
        network_id: Network ID
    
    Returns:
        Environmental analysis and recommendations
    """
    try:
        with safe_api_call("analyze sensor environment"):
            # Get recent readings
            readings = meraki.dashboard.sensor.getNetworkSensorAlertsCurrentOverviewByMetric(
                network_id,
                timespan=3600  # Last hour
            )
            
            output = ["🏢 Environmental Analysis", "=" * 50, ""]
            
            if not readings:
                output.append("No sensor data available for analysis")
                return "\n".join(output)
            
            # Analyze by metric type
            metrics_summary = {
                'temperature': {'values': [], 'locations': []},
                'humidity': {'values': [], 'locations': []},
                'air_quality': {'tvoc': [], 'pm25': [], 'co2': []},
                'security': {'doors': 0, 'water': 0}
            }
            
            for reading in readings:
                metric = reading.get('metric', '')
                value = reading.get('value', {})
                sensor = reading.get('sensor', {})
                location = sensor.get('name', 'Unknown')
                
                if metric == 'temperature':
                    temp = value.get('celsius')
                    if temp is not None:
                        metrics_summary['temperature']['values'].append(temp)
                        metrics_summary['temperature']['locations'].append((location, temp))
                elif metric == 'humidity':
                    hum = value.get('relativePercentage')
                    if hum is not None:
                        metrics_summary['humidity']['values'].append(hum)
                        metrics_summary['humidity']['locations'].append((location, hum))
                elif metric == 'tvoc':
                    tvoc = value.get('concentration')
                    if tvoc is not None:
                        metrics_summary['air_quality']['tvoc'].append((location, tvoc))
                elif metric == 'door':
                    if value.get('open', False):
                        metrics_summary['security']['doors'] += 1
                elif metric == 'water':
                    if value.get('present', False):
                        metrics_summary['security']['water'] += 1
            
            # Temperature analysis
            if metrics_summary['temperature']['values']:
                temps = metrics_summary['temperature']['values']
                avg_temp = sum(temps) / len(temps)
                output.append(f"🌡️ Temperature Overview:")
                output.append(f"   Average: {avg_temp:.1f}°C")
                output.append(f"   Range: {min(temps):.1f}°C - {max(temps):.1f}°C")
                
                # Find hotspots and cold spots
                for location, temp in metrics_summary['temperature']['locations']:
                    if temp > avg_temp + 3:
                        output.append(f"   🔥 Hotspot: {location} ({temp:.1f}°C)")
                    elif temp < avg_temp - 3:
                        output.append(f"   ❄️ Cold spot: {location} ({temp:.1f}°C)")
                output.append("")
            
            # Humidity analysis
            if metrics_summary['humidity']['values']:
                hums = metrics_summary['humidity']['values']
                avg_hum = sum(hums) / len(hums)
                output.append(f"💧 Humidity Overview:")
                output.append(f"   Average: {avg_hum:.1f}%")
                
                if avg_hum < 30:
                    output.append("   ⚠️ Low humidity - consider humidification")
                elif avg_hum > 60:
                    output.append("   ⚠️ High humidity - risk of mold/condensation")
                else:
                    output.append("   ✅ Humidity within recommended range")
                output.append("")
            
            # Air quality
            if metrics_summary['air_quality']['tvoc']:
                output.append("🌫️ Air Quality:")
                for location, tvoc in metrics_summary['air_quality']['tvoc']:
                    if tvoc > 1000:
                        output.append(f"   ⚠️ Poor air quality at {location}: {tvoc} µg/m³")
                    elif tvoc > 500:
                        output.append(f"   ⚠️ Moderate air quality at {location}: {tvoc} µg/m³")
                output.append("")
            
            # Security alerts
            if metrics_summary['security']['doors'] > 0 or metrics_summary['security']['water'] > 0:
                output.append("🚨 Security Alerts:")
                if metrics_summary['security']['doors'] > 0:
                    output.append(f"   🚪 {metrics_summary['security']['doors']} door(s) open")
                if metrics_summary['security']['water'] > 0:
                    output.append(f"   💦 Water detected at {metrics_summary['security']['water']} location(s)")
                output.append("")
            
            # Recommendations
            output.append("💡 Recommendations:")
            output.append("• Monitor temperature variations between zones")
            output.append("• Check HVAC efficiency in hotspot areas")
            output.append("• Ensure proper ventilation for air quality")
            output.append("• Set up alerts for critical thresholds")
            output.append("• Regular sensor calibration recommended")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("analyze sensor environment", e)


def sensor_monitoring_help() -> str:
    """
    ❓ Get help with sensor monitoring tools.
    
    Shows available tools and best practices.
    
    Returns:
        Formatted help guide
    """
    return """🌡️ Sensor Monitoring Tools Help
==================================================

Available tools for environmental monitoring:

1. get_network_sensor_alerts_profiles()
   - View configured alert profiles
   - See threshold settings
   - Check notification recipients

2. get_network_sensor_readings()
   - Historical sensor data
   - Filter by metric type
   - Temperature, humidity, air quality

3. get_device_sensor_details()
   - Specific sensor information
   - Battery status
   - Capabilities by model

4. create_sensor_alert_profile()
   - Configure new alerts
   - Set thresholds
   - Add recipients

5. get_sensor_command_history()
   - View command log
   - Check status
   - Troubleshoot issues

6. analyze_sensor_environment()
   - Environmental insights
   - Identify problem areas
   - Get recommendations

Common Sensor Types:
• MT10/11: Temperature & Humidity
• MT12: + Water detection
• MT14: + Air quality (TVOC)
• MT20: Door sensors
• MT30: Comprehensive environmental

Metric Guidelines:
🌡️ Temperature: 20-24°C optimal
💧 Humidity: 30-60% recommended
🌫️ TVOC: <500 µg/m³ good air quality
🌫️ PM2.5: <12 µg/m³ healthy
🔊 Noise: <50 dB for offices

Best Practices:
- Place sensors away from direct sunlight
- Avoid HVAC vents for accurate readings
- Regular calibration every 6 months
- Test alerts monthly
- Monitor battery levels
"""


def register_sensor_tools(app: FastMCP, meraki_client: MerakiClient):
    """Register all sensor monitoring tools with the MCP server."""
    global mcp_app, meraki
    mcp_app = app
    meraki = meraki_client
    
    # Register all tools
    tools = [
        (get_network_sensor_alerts_profiles, "View sensor alert profiles"),
        (get_network_sensor_readings, "Get historical sensor readings"),
        (get_device_sensor_details, "Get specific sensor device details"),
        (create_sensor_alert_profile, "Create new sensor alert profile"),
        (get_sensor_command_history, "View sensor command history"),
        (analyze_sensor_environment, "Analyze environmental conditions"),
        (sensor_monitoring_help, "Get help with sensor monitoring"),
    ]
    
    for tool_func, description in tools:
        app.tool(
            name=tool_func.__name__,
            description=description
        )(tool_func)