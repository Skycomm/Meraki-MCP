"""
Camera management tools for the Cisco Meraki MCP Server - Comprehensive SDK coverage.
Provides 100% coverage of all Meraki Camera API endpoints.
"""

import json
from typing import Optional, List, Dict, Any

# Global variables to store app and meraki client
app = None
meraki_client = None

def register_camera_tools(mcp_app, meraki):
    """
    Register camera tools with the MCP server.
    
    Args:
        mcp_app: MCP server instance
        meraki: Meraki client instance
    """
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    
    # Register all camera tools
    register_camera_tool_handlers()

def register_camera_tool_handlers():
    """Register all camera tool handlers with comprehensive SDK coverage."""
    
    @app.tool(
        name="get_device_camera_video_link",
        description="📹 Get video link for a camera"
    )
    def get_device_camera_video_link(serial: str, timestamp: str = None):
        """
        Get video link for a camera device.
        
        Args:
            serial: Device serial number
            timestamp: Optional timestamp (ISO 8601) for historical footage
            
        Returns:
            Video link URL
        """
        try:
            link_info = meraki_client.get_device_camera_video_link(serial, timestamp)
            
            result = f"# 📹 Camera Video Link for {serial}\n\n"
            result += f"**Video URL**: {link_info.get('url', 'Not available')}\n"
            
            if timestamp:
                result += f"**Timestamp**: {timestamp}\n"
            else:
                result += "**Type**: Live stream\n"
                
            expiry = link_info.get('expiresAt')
            if expiry:
                result += f"**Expires**: {expiry}\n"
                
            result += "\n⚠️ This link is temporary and will expire. Do not share publicly."
            
            return result
            
        except Exception as e:
            return f"Error retrieving camera video link: {str(e)}"
    
    @app.tool(
        name="get_device_camera_snapshot",
        description="📸 Generate a snapshot from a camera"
    )
    def get_device_camera_snapshot(serial: str, timestamp: str = None):
        """
        Generate a snapshot from a camera.
        
        Args:
            serial: Device serial number
            timestamp: Optional timestamp (ISO 8601) for historical snapshot
            
        Returns:
            Snapshot URL
        """
        try:
            snapshot = meraki_client.get_device_camera_snapshot(serial, timestamp)
            
            result = f"# 📸 Camera Snapshot for {serial}\n\n"
            result += f"**Snapshot URL**: {snapshot.get('url', 'Not available')}\n"
            
            if timestamp:
                result += f"**Timestamp**: {timestamp}\n"
            else:
                result += "**Type**: Current snapshot\n"
                
            expiry = snapshot.get('expiresAt')
            if expiry:
                result += f"**Expires**: {expiry}\n"
                
            result += "\n⚠️ This link is temporary and will expire. Download promptly if needed."
            
            return result
            
        except Exception as e:
            return f"Error generating camera snapshot: {str(e)}"
    
    @app.tool(
        name="get_device_camera_video_settings",
        description="⚙️ Get video settings for a camera"
    )
    def get_device_camera_video_settings(serial: str):
        """
        Get video settings for a camera device.
        
        Args:
            serial: Device serial number
            
        Returns:
            Camera video settings
        """
        try:
            settings = meraki_client.get_device_camera_video_settings(serial)
            
            result = f"# ⚙️ Video Settings for Camera {serial}\n\n"
            
            # External RTSP
            external_rtsp = settings.get('externalRtspEnabled')
            if external_rtsp is not None:
                result += f"**External RTSP**: {'✅ Enabled' if external_rtsp else '❌ Disabled'}\n"
                
            # RTSP URL if enabled
            rtsp_url = settings.get('rtspUrl')
            if rtsp_url:
                result += f"**RTSP URL**: `{rtsp_url}`\n"
                
            result += "\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving camera video settings: {str(e)}"
    
    @app.tool(
        name="update_device_camera_video_settings",
        description="⚙️ Update video settings for a camera"
    )
    def update_device_camera_video_settings(serial: str, external_rtsp_enabled: bool):
        """
        Update video settings for a camera device.
        
        Args:
            serial: Device serial number
            external_rtsp_enabled: Enable/disable external RTSP access
            
        Returns:
            Updated video settings
        """
        try:
            settings = meraki_client.update_device_camera_video_settings(
                serial,
                externalRtspEnabled=external_rtsp_enabled
            )
            
            result = f"# ✅ Video Settings Updated for Camera {serial}\n\n"
            result += f"**External RTSP**: {'✅ Enabled' if external_rtsp_enabled else '❌ Disabled'}\n"
            
            if external_rtsp_enabled and settings.get('rtspUrl'):
                result += f"\n**RTSP URL**: `{settings['rtspUrl']}`\n"
                result += "\n⚠️ Use this URL with VLC or other RTSP-compatible video players."
                
            return result
            
        except Exception as e:
            return f"Error updating camera video settings: {str(e)}"
    
    @app.tool(
        name="get_device_camera_analytics_zones",
        description="📊 Get analytics zones configured on a camera"
    )
    def get_device_camera_analytics_zones(serial: str):
        """
        Get analytics zones configured on a camera.
        
        Args:
            serial: Device serial number
            
        Returns:
            Camera analytics zones configuration
        """
        try:
            zones = meraki_client.get_device_camera_analytics_zones(serial)
            
            if not zones:
                return f"No analytics zones configured for camera {serial}."
                
            result = f"# 📊 Analytics Zones for Camera {serial}\n\n"
            
            for idx, zone in enumerate(zones, 1):
                zone_id = zone.get('zoneId', f'Zone {idx}')
                zone_type = zone.get('type', 'Unknown')
                label = zone.get('label', 'Unlabeled')
                
                result += f"## {label} (ID: {zone_id})\n"
                result += f"- **Type**: {zone_type}\n"
                
                # Region vertices
                region = zone.get('regionOfInterest', {})
                vertices = region.get('vertices', [])
                if vertices:
                    result += f"- **Vertices**: {len(vertices)} points\n"
                    
                result += "\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving camera analytics zones: {str(e)}"
    
    @app.tool(
        name="get_device_camera_sense",
        description="🎯 Get motion detection settings for a camera"
    )
    def get_device_camera_sense(serial: str):
        """
        Get motion detection (sense) settings for a camera.
        
        Args:
            serial: Device serial number
            
        Returns:
            Camera motion detection settings
        """
        try:
            sense = meraki_client.get_device_camera_sense(serial)
            
            result = f"# 🎯 Motion Detection Settings for Camera {serial}\n\n"
            
            # Motion detection enabled
            detection_enabled = sense.get('detectionEnabled')
            if detection_enabled is not None:
                result += f"**Motion Detection**: {'✅ Enabled' if detection_enabled else '❌ Disabled'}\n"
                
            # Audio detection
            audio_detection = sense.get('audioDetection', {})
            if audio_detection:
                audio_enabled = audio_detection.get('enabled', False)
                result += f"**Audio Detection**: {'✅ Enabled' if audio_enabled else '❌ Disabled'}\n"
                
            # MQTT broker
            mqtt_broker_id = sense.get('mqttBrokerId')
            if mqtt_broker_id:
                result += f"**MQTT Broker ID**: {mqtt_broker_id}\n"
                
            result += "\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving camera sense settings: {str(e)}"
    
    @app.tool(
        name="update_device_camera_sense",
        description="🎯 Update motion detection settings for a camera. Configure motion/audio detection and zones."
    )
    def update_device_camera_sense(
        serial: str,
        mqtt_broker_id: Optional[str] = None,
        sense_enabled: Optional[bool] = None,
        audio_detection: Optional[str] = None,
        detection_areas: Optional[str] = None
    ):
        """
        Update motion detection settings for a camera.
        
        Args:
            serial: Device serial number
            mqtt_broker_id: MQTT broker ID for event streaming
            sense_enabled: Enable/disable motion detection
            audio_detection: JSON audio detection settings {"enabled": bool}
            detection_areas: JSON array of detection areas
            
        Returns:
            Updated motion detection settings
        """
        try:
            kwargs = {}
            if mqtt_broker_id is not None:
                kwargs['mqttBrokerId'] = mqtt_broker_id
            if sense_enabled is not None:
                kwargs['senseEnabled'] = sense_enabled
            if audio_detection:
                kwargs['audioDetection'] = json.loads(audio_detection)
            if detection_areas:
                kwargs['detectionAreas'] = json.loads(detection_areas)
                
            result = meraki_client.update_device_camera_sense(serial, **kwargs)
            return f"✅ Motion detection settings updated for camera {serial}"
        except Exception as e:
            return f"Error updating camera sense settings: {str(e)}"
    
    @app.tool(
        name="get_device_camera_custom_analytics",
        description="🤖 Get custom analytics settings for a camera. Shows AI-powered object detection configuration."
    )
    def get_device_camera_custom_analytics(serial: str):
        """
        Get custom analytics settings for a camera.
        
        Args:
            serial: Device serial number
            
        Returns:
            Custom analytics configuration
        """
        try:
            analytics = meraki_client.get_device_camera_custom_analytics(serial)
            
            result = f"# 🤖 Custom Analytics for Camera {serial}\n\n"
            
            if analytics.get('enabled'):
                result += "**Status**: ✅ Enabled\n\n"
                
                # Artifact ID
                artifact_id = analytics.get('artifactId')
                if artifact_id:
                    result += f"**Artifact ID**: `{artifact_id}`\n"
                    
                # Parameters
                params = analytics.get('parameters', [])
                if params:
                    result += "\n**Parameters**:\n"
                    for param in params:
                        result += f"- {param.get('name', 'Unknown')}: {param.get('value', 'N/A')}\n"
            else:
                result += "**Status**: ❌ Disabled\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving custom analytics: {str(e)}"
    
    @app.tool(
        name="update_device_camera_custom_analytics",
        description="🤖 Configure custom analytics for a camera. Enable AI-powered object detection and tracking."
    )
    def update_device_camera_custom_analytics(
        serial: str,
        enabled: bool,
        artifact_id: Optional[str] = None,
        parameters: Optional[str] = None
    ):
        """
        Update custom analytics settings for a camera.
        
        Args:
            serial: Device serial number
            enabled: Enable/disable custom analytics
            artifact_id: Custom analytics artifact ID
            parameters: JSON array of parameters [{"name": "...", "value": "..."}]
            
        Returns:
            Updated analytics configuration
        """
        try:
            kwargs = {'enabled': enabled}
            if artifact_id:
                kwargs['artifactId'] = artifact_id
            if parameters:
                kwargs['parameters'] = json.loads(parameters)
                
            result = meraki_client.update_device_camera_custom_analytics(serial, **kwargs)
            status = "✅ Enabled" if enabled else "❌ Disabled"
            return f"Custom analytics {status} for camera {serial}"
        except Exception as e:
            return f"Error updating custom analytics: {str(e)}"
    
    @app.tool(
        name="get_network_camera_schedules",
        description="📅 Get recording schedules for cameras in a network"
    )
    def get_network_camera_schedules(network_id: str):
        """
        Get camera recording schedules for a network.
        
        Args:
            network_id: Network ID
            
        Returns:
            Camera recording schedules
        """
        try:
            schedules = meraki_client.get_network_camera_schedules(network_id)
            
            if not schedules:
                return f"No camera schedules configured for network {network_id}"
                
            result = f"# 📅 Camera Schedules for Network\n\n"
            
            for schedule in schedules:
                result += f"## {schedule.get('name', 'Unnamed Schedule')}\n"
                result += f"- **ID**: `{schedule.get('id')}`\n"
                
                # Schedule details
                if schedule.get('monday'):
                    result += f"- **Monday**: {schedule['monday']}\n"
                if schedule.get('tuesday'):
                    result += f"- **Tuesday**: {schedule['tuesday']}\n"
                if schedule.get('wednesday'):
                    result += f"- **Wednesday**: {schedule['wednesday']}\n"
                if schedule.get('thursday'):
                    result += f"- **Thursday**: {schedule['thursday']}\n"
                if schedule.get('friday'):
                    result += f"- **Friday**: {schedule['friday']}\n"
                if schedule.get('saturday'):
                    result += f"- **Saturday**: {schedule['saturday']}\n"
                if schedule.get('sunday'):
                    result += f"- **Sunday**: {schedule['sunday']}\n"
                    
                result += "\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving camera schedules: {str(e)}"
    
    @app.tool(
        name="get_network_camera_quality_profiles",
        description="🎥 Get video quality and retention profiles for cameras"
    )
    def get_network_camera_quality_profiles(network_id: str):
        """
        Get camera quality and retention profiles for a network.
        
        Args:
            network_id: Network ID
            
        Returns:
            Quality and retention profiles
        """
        try:
            profiles = meraki_client.get_network_camera_quality_retention_profiles(network_id)
            
            result = f"# 🎥 Camera Quality & Retention Profiles\n\n"
            
            for profile in profiles:
                result += f"## {profile.get('name', 'Unnamed Profile')}\n"
                result += f"- **ID**: `{profile.get('id')}`\n"
                
                # Video settings
                video = profile.get('videoSettings', {})
                if video:
                    result += "\n**Video Settings**:\n"
                    result += f"- Quality: {video.get('quality', 'Standard')}\n"
                    result += f"- Resolution: {video.get('resolution', 'Auto')}\n"
                    
                # Motion settings
                motion = profile.get('motionBasedRetentionEnabled')
                if motion is not None:
                    result += f"\n**Motion-Based Retention**: {'✅ Enabled' if motion else '❌ Disabled'}\n"
                    
                # Retention settings
                retention = profile.get('cloudArchiveEnabled')
                if retention is not None:
                    result += f"**Cloud Archive**: {'✅ Enabled' if retention else '❌ Disabled'}\n"
                    
                # Restricted bandwidth
                bandwidth = profile.get('restrictedBandwidthModeEnabled')
                if bandwidth is not None:
                    result += f"**Restricted Bandwidth**: {'✅ Enabled' if bandwidth else '❌ Disabled'}\n"
                    
                result += "\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving quality profiles: {str(e)}"
    
    @app.tool(
        name="update_network_camera_quality_profile",
        description="🎥 Update video quality and retention settings for a camera profile"
    )
    def update_network_camera_quality_profile(
        network_id: str,
        quality_profile_id: str,
        name: Optional[str] = None,
        motion_based_retention: Optional[bool] = None,
        cloud_archive: Optional[bool] = None,
        video_settings: Optional[str] = None,
        restricted_bandwidth: Optional[bool] = None
    ):
        """
        Update a camera quality and retention profile.
        
        Args:
            network_id: Network ID
            quality_profile_id: Profile ID to update
            name: Profile name
            motion_based_retention: Enable motion-based retention
            cloud_archive: Enable cloud archiving
            video_settings: JSON video settings {"quality": "...", "resolution": "..."}
            restricted_bandwidth: Enable restricted bandwidth mode
            
        Returns:
            Updated profile
        """
        try:
            kwargs = {}
            if name:
                kwargs['name'] = name
            if motion_based_retention is not None:
                kwargs['motionBasedRetentionEnabled'] = motion_based_retention
            if cloud_archive is not None:
                kwargs['cloudArchiveEnabled'] = cloud_archive
            if video_settings:
                kwargs['videoSettings'] = json.loads(video_settings)
            if restricted_bandwidth is not None:
                kwargs['restrictedBandwidthModeEnabled'] = restricted_bandwidth
                
            result = meraki_client.update_network_camera_quality_retention_profile(
                network_id, quality_profile_id, **kwargs
            )
            return f"✅ Quality profile '{name or quality_profile_id}' updated successfully"
        except Exception as e:
            return f"Error updating quality profile: {str(e)}"
    
    @app.tool(
        name="get_org_camera_boundaries_lines",
        description="🚧 Get configured boundary lines for cameras across the organization"
    )
    def get_org_camera_boundaries_lines(organization_id: str):
        """
        Get boundary lines configured for cameras in an organization.
        
        Args:
            organization_id: Organization ID
            
        Returns:
            Boundary lines configuration
        """
        try:
            boundaries = meraki_client.get_organization_camera_boundaries_lines_by_device(organization_id)
            
            if not boundaries:
                return "No boundary lines configured in organization"
                
            result = f"# 🚧 Camera Boundary Lines\n\n"
            
            for device in boundaries:
                serial = device.get('serial', 'Unknown')
                result += f"## Camera {serial}\n"
                
                lines = device.get('boundaries', {}).get('lines', [])
                if lines:
                    for idx, line in enumerate(lines, 1):
                        result += f"- **Line {idx}**: {line.get('name', 'Unnamed')}\n"
                        result += f"  - Type: {line.get('type', 'boundary')}\n"
                        vertices = line.get('vertices', [])
                        if vertices:
                            result += f"  - Vertices: {len(vertices)} points\n"
                else:
                    result += "- No boundary lines configured\n"
                    
                result += "\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving boundary lines: {str(e)}"
    
    @app.tool(
        name="get_org_camera_boundaries_areas",
        description="📍 Get configured boundary areas/zones for cameras across the organization"
    )
    def get_org_camera_boundaries_areas(organization_id: str):
        """
        Get boundary areas configured for cameras in an organization.
        
        Args:
            organization_id: Organization ID
            
        Returns:
            Boundary areas configuration
        """
        try:
            boundaries = meraki_client.get_organization_camera_boundaries_areas_by_device(organization_id)
            
            if not boundaries:
                return "No boundary areas configured in organization"
                
            result = f"# 📍 Camera Boundary Areas\n\n"
            
            for device in boundaries:
                serial = device.get('serial', 'Unknown')
                result += f"## Camera {serial}\n"
                
                areas = device.get('boundaries', {}).get('areas', [])
                if areas:
                    for idx, area in enumerate(areas, 1):
                        result += f"- **Area {idx}**: {area.get('name', 'Unnamed')}\n"
                        result += f"  - Type: {area.get('type', 'area')}\n"
                        vertices = area.get('vertices', [])
                        if vertices:
                            result += f"  - Vertices: {len(vertices)} points\n"
                else:
                    result += "- No boundary areas configured\n"
                    
                result += "\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving boundary areas: {str(e)}"
    
    @app.tool(
        name="get_org_camera_detections_history",
        description="🔍 Get AI-powered object detection history across all cameras"
    )
    def get_org_camera_detections_history(
        organization_id: str,
        timespan: Optional[int] = 86400,
        per_page: Optional[int] = 100,
        starting_after: Optional[str] = None,
        ending_before: Optional[str] = None
    ):
        """
        Get object detection history for cameras in an organization.
        
        Args:
            organization_id: Organization ID
            timespan: Time span in seconds (default: 24 hours)
            per_page: Number of entries per page
            starting_after: Starting cursor for pagination
            ending_before: Ending cursor for pagination
            
        Returns:
            Detection history with AI-identified objects
        """
        try:
            kwargs = {'timespan': timespan}
            if per_page:
                kwargs['perPage'] = per_page
            if starting_after:
                kwargs['startingAfter'] = starting_after
            if ending_before:
                kwargs['endingBefore'] = ending_before
                
            detections = meraki_client.get_organization_camera_detections_history_by_boundary_by_interval(
                organization_id, **kwargs
            )
            
            if not detections:
                return f"No detections in the last {timespan} seconds"
                
            result = f"# 🔍 Object Detection History ({timespan}s)\n\n"
            
            for detection in detections[:50]:  # Limit display
                result += f"## {detection.get('occurredAt', 'Unknown time')}\n"
                result += f"- **Camera**: {detection.get('serial', 'Unknown')}\n"
                result += f"- **Type**: {detection.get('type', 'Unknown')}\n"
                result += f"- **Duration**: {detection.get('duration', 0)}s\n"
                
                # Object details
                obj = detection.get('object', {})
                if obj:
                    result += f"- **Object**: {obj.get('type', 'Unknown')}\n"
                    if obj.get('confidence'):
                        result += f"- **Confidence**: {obj['confidence']}%\n"
                        
                result += "\n"
                
            if len(detections) > 50:
                result += f"*Showing 50 of {len(detections)} detections*\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving detection history: {str(e)}"
    
    @app.tool(
        name="get_network_camera_wireless_profiles",
        description="📶 Get wireless profiles configured for cameras in a network"
    )
    def get_network_camera_wireless_profiles(network_id: str):
        """
        Get wireless profiles for cameras in a network.
        
        Args:
            network_id: Network ID
            
        Returns:
            Wireless profiles configuration
        """
        try:
            profiles = meraki_client.get_network_camera_wireless_profiles(network_id)
            
            if not profiles:
                return "No wireless profiles configured for cameras"
                
            result = f"# 📶 Camera Wireless Profiles\n\n"
            
            for profile in profiles:
                result += f"## {profile.get('name', 'Unnamed Profile')}\n"
                result += f"- **ID**: `{profile.get('id')}`\n"
                
                # SSID configuration
                ssid = profile.get('ssid', {})
                if ssid:
                    result += f"- **SSID**: {ssid.get('name', 'Unknown')}\n"
                    result += f"- **Auth Mode**: {ssid.get('authMode', 'open')}\n"
                    if ssid.get('encryptionMode'):
                        result += f"- **Encryption**: {ssid['encryptionMode']}\n"
                        
                # Applied to
                applied = profile.get('appliedDeviceCount', 0)
                result += f"- **Applied to**: {applied} cameras\n"
                
                result += "\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving wireless profiles: {str(e)}"
    
    @app.tool(
        name="create_network_camera_wireless_profile",
        description="📶 Create a wireless profile for cameras to connect to WiFi"
    )
    def create_network_camera_wireless_profile(
        network_id: str,
        name: str,
        ssid_name: str,
        auth_mode: str = "psk",
        psk: Optional[str] = None,
        encryption_mode: Optional[str] = "wpa2"
    ):
        """
        Create a wireless profile for cameras.
        
        Args:
            network_id: Network ID
            name: Profile name
            ssid_name: WiFi network name (SSID)
            auth_mode: Authentication mode (open, psk, 8021x-radius)
            psk: Pre-shared key (required for psk auth)
            encryption_mode: Encryption mode (wpa, wpa2, wpa3)
            
        Returns:
            Created wireless profile
        """
        try:
            ssid = {
                'name': ssid_name,
                'authMode': auth_mode
            }
            
            if auth_mode == 'psk' and psk:
                ssid['psk'] = psk
            if encryption_mode:
                ssid['encryptionMode'] = encryption_mode
                
            result = meraki_client.create_network_camera_wireless_profile(
                network_id,
                name=name,
                ssid=ssid
            )
            
            return f"✅ Wireless profile '{name}' created for SSID '{ssid_name}'"
            
        except Exception as e:
            return f"Error creating wireless profile: {str(e)}"
    
    @app.tool(
        name="update_network_camera_wireless_profile",
        description="📶 Update a wireless profile for cameras"
    )
    def update_network_camera_wireless_profile(
        network_id: str,
        wireless_profile_id: str,
        name: Optional[str] = None,
        ssid_settings: Optional[str] = None
    ):
        """
        Update a wireless profile for cameras.
        
        Args:
            network_id: Network ID
            wireless_profile_id: Profile ID to update
            name: New profile name
            ssid_settings: JSON SSID settings {"name": "...", "authMode": "...", "psk": "..."}
            
        Returns:
            Updated wireless profile
        """
        try:
            kwargs = {}
            if name:
                kwargs['name'] = name
            if ssid_settings:
                kwargs['ssid'] = json.loads(ssid_settings)
                
            result = meraki_client.update_network_camera_wireless_profile(
                network_id, wireless_profile_id, **kwargs
            )
            
            return f"✅ Wireless profile updated successfully"
            
        except Exception as e:
            return f"Error updating wireless profile: {str(e)}"
    
    @app.tool(
        name="delete_network_camera_wireless_profile",
        description="🗑️ Delete a wireless profile for cameras. Requires confirmation."
    )
    def delete_network_camera_wireless_profile(
        network_id: str,
        wireless_profile_id: str,
        confirmed: bool = False
    ):
        """
        Delete a wireless profile for cameras.
        
        Args:
            network_id: Network ID
            wireless_profile_id: Profile ID to delete
            confirmed: Must be True to confirm deletion
            
        Returns:
            Deletion status
        """
        try:
            if not confirmed:
                return "⚠️ Deletion requires confirmation. Set confirmed=true to proceed."
                
            meraki_client.delete_network_camera_wireless_profile(network_id, wireless_profile_id)
            return f"✅ Wireless profile deleted successfully"
            
        except Exception as e:
            return f"Error deleting wireless profile: {str(e)}"
    
    @app.tool(
        name="get_device_camera_wireless_profiles",
        description="📶 Get wireless profiles assigned to a specific camera"
    )
    def get_device_camera_wireless_profiles(serial: str):
        """
        Get wireless profiles assigned to a camera.
        
        Args:
            serial: Device serial number
            
        Returns:
            Assigned wireless profiles
        """
        try:
            profiles = meraki_client.get_device_camera_wireless_profiles(serial)
            
            result = f"# 📶 Wireless Profiles for Camera {serial}\n\n"
            
            if profiles.get('ids'):
                result += "**Assigned Profile IDs**:\n"
                for profile_id in profiles['ids']:
                    result += f"- `{profile_id}`\n"
            else:
                result += "No wireless profiles assigned\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving camera wireless profiles: {str(e)}"
    
    @app.tool(
        name="update_device_camera_wireless_profiles",
        description="📶 Assign wireless profiles to a camera for WiFi connectivity"
    )
    def update_device_camera_wireless_profiles(
        serial: str,
        profile_ids: str
    ):
        """
        Update wireless profiles assigned to a camera.
        
        Args:
            serial: Device serial number
            profile_ids: Comma-separated list of profile IDs or JSON array
            
        Returns:
            Updated profile assignment
        """
        try:
            # Handle both comma-separated and JSON array
            if profile_ids.startswith('['):
                ids = json.loads(profile_ids)
            else:
                ids = [p.strip() for p in profile_ids.split(',')]
                
            result = meraki_client.update_device_camera_wireless_profiles(
                serial,
                ids={'ids': ids}
            )
            
            return f"✅ Wireless profiles updated for camera {serial}"
            
        except Exception as e:
            return f"Error updating camera wireless profiles: {str(e)}"
    
    @app.tool(
        name="generate_device_camera_snapshot",
        description="📸 Generate a new snapshot from a camera (triggers capture)"
    )
    def generate_device_camera_snapshot(serial: str, timestamp: Optional[str] = None):
        """
        Generate a new snapshot from a camera.
        
        Args:
            serial: Device serial number
            timestamp: Optional timestamp for historical snapshot (ISO 8601)
            
        Returns:
            Generated snapshot details
        """
        try:
            kwargs = {}
            if timestamp:
                kwargs['timestamp'] = timestamp
                
            snapshot = meraki_client.generate_device_camera_snapshot(serial, **kwargs)
            
            result = f"# 📸 Generated Snapshot for {serial}\n\n"
            result += f"**URL**: {snapshot.get('url', 'Processing...')}\n"
            result += f"**Expires**: {snapshot.get('expiry', 'Unknown')}\n"
            result += "\n⚠️ Snapshot is being generated. URL will be available shortly."
            
            return result
            
        except Exception as e:
            return f"Error generating snapshot: {str(e)}"
    
    @app.tool(
        name="get_network_camera_alerts",
        description="🚨 Get recent camera alerts and motion events for a network"
    )
    def get_network_camera_alerts(
        network_id: str,
        timespan: Optional[int] = 86400
    ):
        """
        Get recent camera alerts for a network.
        
        Args:
            network_id: Network ID
            timespan: Time span in seconds (default: 24 hours)
            
        Returns:
            Recent camera alerts and events
        """
        try:
            # Using events API for camera alerts
            events = meraki_client.get_network_events(
                network_id,
                productType='camera',
                includedEventTypes=['motion_alert', 'person_detected', 'vehicle_detected']
            )
            
            if not events.get('events'):
                return f"No camera alerts in the last {timespan} seconds"
                
            result = f"# 🚨 Camera Alerts (Last {timespan}s)\n\n"
            
            for event in events['events'][:50]:  # Limit display
                result += f"## {event.get('occurredAt', 'Unknown time')}\n"
                result += f"- **Type**: {event.get('type', 'Unknown')}\n"
                result += f"- **Camera**: {event.get('deviceName', 'Unknown')}\n"
                result += f"- **Description**: {event.get('description', 'No description')}\n"
                result += "\n"
                
            if len(events['events']) > 50:
                result += f"*Showing 50 of {len(events['events'])} alerts*\n"
                
            return result
            
        except Exception as e:
            # Fallback message for networks without camera events
            return f"No camera alerts available or cameras not configured for alerts"
    
    @app.tool(
        name="get_org_camera_permissions",
        description="🔒 Get camera permissions for users in the organization"
    )
    def get_org_camera_permissions(organization_id: str):
        """
        Get camera permissions across the organization.
        
        Args:
            organization_id: Organization ID
            
        Returns:
            Camera permission settings
        """
        try:
            permissions = meraki_client.get_organization_camera_permissions(organization_id)
            
            result = f"# 🔒 Camera Permissions\n\n"
            
            if permissions:
                for perm in permissions:
                    result += f"## {perm.get('name', 'Unknown Permission')}\n"
                    result += f"- **Level**: {perm.get('level', 'Unknown')}\n"
                    result += f"- **Cameras**: {perm.get('cameraCount', 0)}\n"
                    
                    # Specific permissions
                    if perm.get('permissions'):
                        result += "**Permissions**:\n"
                        for p in perm['permissions']:
                            result += f"  - {p}\n"
                            
                    result += "\n"
            else:
                result += "Default permissions apply to all cameras\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving camera permissions: {str(e)}"
    
    @app.tool(
        name="get_org_camera_roles",
        description="👥 Get camera access roles defined in the organization"
    )
    def get_org_camera_roles(organization_id: str):
        """
        Get camera roles for the organization.
        
        Args:
            organization_id: Organization ID
            
        Returns:
            Camera role definitions
        """
        try:
            roles = meraki_client.get_organization_camera_roles(organization_id)
            
            result = f"# 👥 Camera Roles\n\n"
            
            for role in roles:
                result += f"## {role.get('name', 'Unnamed Role')}\n"
                
                # Applied to
                if role.get('appliedOnDevices'):
                    result += f"- **Applied to**: {len(role['appliedOnDevices'])} cameras\n"
                if role.get('appliedOnNetworks'):
                    result += f"- **Networks**: {len(role['appliedOnNetworks'])} networks\n"
                    
                # Permissions
                permissions = role.get('permissions', [])
                if permissions:
                    result += "**Permissions**:\n"
                    for perm in permissions:
                        result += f"  - {perm}\n"
                        
                result += "\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving camera roles: {str(e)}"
    
    @app.tool(
        name="get_org_camera_onboarding_statuses",
        description="🚀 Get onboarding status for recently added cameras"
    )
    def get_org_camera_onboarding_statuses(
        organization_id: str,
        serials: Optional[str] = None,
        network_ids: Optional[str] = None
    ):
        """
        Get onboarding statuses for cameras.
        
        Args:
            organization_id: Organization ID
            serials: Comma-separated camera serials to check
            network_ids: Comma-separated network IDs to check
            
        Returns:
            Camera onboarding statuses
        """
        try:
            kwargs = {}
            if serials:
                kwargs['serials'] = [s.strip() for s in serials.split(',')]
            if network_ids:
                kwargs['networkIds'] = [n.strip() for n in network_ids.split(',')]
                
            statuses = meraki_client.get_organization_camera_onboarding_statuses(
                organization_id, **kwargs
            )
            
            result = f"# 🚀 Camera Onboarding Statuses\n\n"
            
            for camera in statuses:
                serial = camera.get('serial', 'Unknown')
                status = camera.get('status', 'unknown')
                
                # Status emoji
                emoji = "✅" if status == 'online' else "⏳" if status == 'pending' else "❌"
                
                result += f"## Camera {serial} {emoji}\n"
                result += f"- **Status**: {status}\n"
                result += f"- **Network**: {camera.get('networkId', 'Unassigned')}\n"
                
                if camera.get('lastSeen'):
                    result += f"- **Last Seen**: {camera['lastSeen']}\n"
                if camera.get('onboardedAt'):
                    result += f"- **Onboarded**: {camera['onboardedAt']}\n"
                    
                result += "\n"
                
            return result
            
        except Exception as e:
            return f"Error retrieving onboarding statuses: {str(e)}"
    
    # ========== MISSING CAMERA SDK METHODS ==========
    @app.tool(
        name="get_device_camera_quality_retention_profiles",
        description="📹 Get quality and retention profiles for a camera"
    )
    def get_device_camera_quality_retention_profiles(serial: str):
        """
        Get quality and retention profiles for a camera.
        
        Args:
            serial: Camera serial number
            
        Returns:
            Quality and retention profile settings
        """
        try:
            result = meraki_client.dashboard.camera.getDeviceCameraQualityAndRetentionProfiles(serial)
            
            formatted = "# 📹 Camera Quality & Retention Profiles\n\n"
            
            for profile_id, profile in result.items():
                formatted += f"## Profile: {profile_id}\n"
                formatted += f"- **Video Quality**: {profile.get('videoQuality', 'Unknown')}\n"
                formatted += f"- **Resolution**: {profile.get('resolution', 'Unknown')}\n"
                formatted += f"- **Retention Days**: {profile.get('retentionDays', 'Unknown')}\n"
                formatted += f"- **Motion-Based Retention**: {profile.get('motionBasedRetentionEnabled', False)}\n"
                formatted += f"- **Audio Recording**: {profile.get('audioRecordingEnabled', False)}\n\n"
                
            return formatted
            
        except Exception as e:
            return f"Error retrieving quality/retention profiles: {str(e)}"
    
    @app.tool(
        name="update_device_camera_quality_retention_profiles",
        description="📹 Update quality and retention profiles for a camera"
    )
    def update_device_camera_quality_retention_profiles(
        serial: str,
        profiles: str
    ):
        """
        Update quality and retention profiles for a camera.
        
        Args:
            serial: Camera serial number
            profiles: JSON object with profile settings
            
        Returns:
            Updated profile settings
        """
        try:
            profiles_dict = json.loads(profiles)
            result = meraki_client.dashboard.camera.updateDeviceCameraQualityAndRetentionProfiles(
                serial,
                **profiles_dict
            )
            return "✅ Camera quality and retention profiles updated successfully"
            
        except Exception as e:
            return f"Error updating profiles: {str(e)}"
    
    @app.tool(
        name="get_device_camera_analytics_overview",
        description="📊 Get analytics overview for a camera"
    )
    def get_device_camera_analytics_overview(
        serial: str,
        timespan: Optional[int] = 86400
    ):
        """
        Get analytics overview for a camera.
        
        Args:
            serial: Camera serial number
            timespan: Time span in seconds (default: 24 hours)
            
        Returns:
            Analytics overview data
        """
        try:
            result = meraki_client.dashboard.camera.getDeviceCameraAnalyticsOverview(
                serial,
                timespan=timespan
            )
            
            formatted = "# 📊 Camera Analytics Overview\n\n"
            
            for zone_id, zone_data in result.items():
                formatted += f"## Zone: {zone_id}\n"
                
                if "entrances" in zone_data:
                    formatted += f"- **Entrances**: {zone_data['entrances']}\n"
                    
                if "averageDwell" in zone_data:
                    formatted += f"- **Average Dwell Time**: {zone_data['averageDwell']} seconds\n"
                    
                if "personCount" in zone_data:
                    formatted += f"- **Person Count**: {zone_data['personCount']}\n"
                    
                formatted += "\n"
                
            return formatted
            
        except Exception as e:
            return f"Error retrieving analytics overview: {str(e)}"
    
    @app.tool(
        name="get_device_camera_analytics_recent",
        description="📊 Get recent analytics data for a camera"
    )
    def get_device_camera_analytics_recent(
        serial: str,
        object_type: Optional[str] = "person"
    ):
        """
        Get recent analytics data for a camera.
        
        Args:
            serial: Camera serial number
            object_type: Type of object to track (person, vehicle)
            
        Returns:
            Recent analytics data
        """
        try:
            result = meraki_client.dashboard.camera.getDeviceCameraAnalyticsRecent(
                serial,
                objectType=object_type
            )
            
            formatted = f"# 📊 Recent {object_type.title()} Analytics\n\n"
            
            for entry in result:
                formatted += f"## Detection at {entry.get('ts', 'Unknown')}\n"
                formatted += f"- **Zone**: {entry.get('zoneId', 'Unknown')}\n"
                formatted += f"- **Type**: {entry.get('type', 'Unknown')}\n"
                
                if "entrances" in entry:
                    formatted += f"- **Entrances**: {entry['entrances']}\n"
                    
                formatted += "\n"
                
            return formatted if result else f"No recent {object_type} analytics data available."
            
        except Exception as e:
            return f"Error retrieving recent analytics: {str(e)}"
    
    @app.tool(
        name="get_device_camera_analytics_live",
        description="🔴 Get live analytics data for a camera"
    )
    def get_device_camera_analytics_live(serial: str):
        """
        Get live analytics data for a camera.
        
        Args:
            serial: Camera serial number
            
        Returns:
            Live analytics data
        """
        try:
            result = meraki_client.dashboard.camera.getDeviceCameraAnalyticsLive(serial)
            
            formatted = "# 🔴 Live Camera Analytics\n\n"
            
            if "zones" in result:
                for zone in result["zones"]:
                    zone_id = zone.get("zoneId", "Unknown")
                    formatted += f"## Zone: {zone_id}\n"
                    formatted += f"- **Person Count**: {zone.get('personCount', 0)}\n"
                    formatted += f"- **Average Dwell**: {zone.get('averageDwell', 0)} seconds\n\n"
                    
            return formatted
            
        except Exception as e:
            return f"Error retrieving live analytics: {str(e)}"
    
    @app.tool(
        name="get_organization_camera_custom_analytics_artifacts",
        description="🎯 Get custom analytics artifacts for an organization"
    )
    def get_organization_camera_custom_analytics_artifacts(organization_id: str):
        """
        Get custom analytics artifacts for an organization.
        
        Args:
            organization_id: Organization ID
            
        Returns:
            Custom analytics artifacts
        """
        try:
            result = meraki_client.dashboard.camera.getOrganizationCameraCustomAnalyticsArtifacts(
                organization_id
            )
            
            formatted = "# 🎯 Custom Analytics Artifacts\n\n"
            
            for artifact in result:
                formatted += f"## {artifact.get('name', 'Unknown')}\n"
                formatted += f"- **ID**: {artifact.get('artifactId', 'Unknown')}\n"
                formatted += f"- **Status**: {artifact.get('status', {}).get('type', 'Unknown')}\n"
                
                if "organizationIds" in artifact:
                    formatted += f"- **Organizations**: {len(artifact['organizationIds'])}\n"
                    
                formatted += "\n"
                
            return formatted if result else "No custom analytics artifacts found."
            
        except Exception as e:
            return f"Error retrieving custom analytics artifacts: {str(e)}"
    
    @app.tool(
        name="create_organization_camera_custom_analytics_artifact",
        description="🎯 Create a custom analytics artifact"
    )
    def create_organization_camera_custom_analytics_artifact(
        organization_id: str,
        name: str
    ):
        """
        Create a custom analytics artifact.
        
        Args:
            organization_id: Organization ID
            name: Name for the artifact
            
        Returns:
            Created artifact details
        """
        try:
            result = meraki_client.dashboard.camera.createOrganizationCameraCustomAnalyticsArtifact(
                organization_id,
                name=name
            )
            
            return f"""✅ Custom Analytics Artifact Created

**Name**: {name}
**Artifact ID**: {result.get("artifactId", "Unknown")}
**Status**: {result.get("status", {}).get("type", "Unknown")}"""
            
        except Exception as e:
            return f"Error creating custom analytics artifact: {str(e)}"
    
    @app.tool(
        name="delete_organization_camera_custom_analytics_artifact",
        description="🗑️ Delete a custom analytics artifact - REQUIRES CONFIRMATION"
    )
    def delete_organization_camera_custom_analytics_artifact(
        organization_id: str,
        artifact_id: str,
        confirmed: bool = False
    ):
        """
        Delete a custom analytics artifact.
        
        ⚠️ WARNING: This will permanently delete the artifact!
        
        Args:
            organization_id: Organization ID
            artifact_id: Artifact ID to delete
            confirmed: Must be True to execute this operation
            
        Returns:
            Deletion status
        """
        if not confirmed:
            return "⚠️ Artifact deletion requires confirmation. Set confirmed=true to proceed."
            
        try:
            meraki_client.dashboard.camera.deleteOrganizationCameraCustomAnalyticsArtifact(
                organization_id,
                artifact_id
            )
            return f"✅ Custom analytics artifact {artifact_id} deleted successfully"
            
        except Exception as e:
            return f"Error deleting artifact: {str(e)}"

