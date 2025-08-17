"""
Camera management tools for the Cisco Meraki MCP Server - ONLY REAL API METHODS.
"""

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
    """Register all camera tool handlers using ONLY REAL API methods."""
    
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