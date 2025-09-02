"""
Cisco Meraki MCP Server - Camera SDK Tools
Complete implementation of all 45 official Meraki Camera API methods.

This module provides 100% coverage of the Camera category from the official Meraki Dashboard API SDK.
Each tool corresponds directly to a method in the meraki.dashboard.camera namespace.
"""

# Import removed to avoid circular import
import meraki


def register_camera_tools(app, meraki_client):
    """Register all camera SDK tools."""
    print(f"📷 Registering 45 camera SDK tools...")


@app.tool(
    name="create_network_camera_quality_retention_profile",
    description="Create cameraqualityretentionprofile"
)
def create_network_camera_quality_retention_profile(network_id: str, **kwargs):
    """
    Create cameraqualityretentionprofile
    
    Args:
        network_id: Network ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with cameraqualityretentionprofile data
    """
    try:
        result = meraki_client.dashboard.camera.createNetworkCameraQualityRetentionProfile(network_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="create_network_camera_wireless_profile",
    description="Create camerawirelessprofile"
)
def create_network_camera_wireless_profile(network_id: str, **kwargs):
    """
    Create camerawirelessprofile
    
    Args:
        network_id: Network ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with camerawirelessprofile data
    """
    try:
        result = meraki_client.dashboard.camera.createNetworkCameraWirelessProfile(network_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="create_organization_camera_custom_analytics_artifact",
    description="Create cameracustomanalyticsartifact"
)
def create_organization_camera_custom_analytics_artifact(organization_id: str, **kwargs):
    """
    Create cameracustomanalyticsartifact
    
    Args:
        organization_id: Organization ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with cameracustomanalyticsartifact data
    """
    try:
        result = meraki_client.dashboard.camera.createOrganizationCameraCustomAnalyticsArtifact(organization_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="create_organization_camera_role",
    description="Create camerarole"
)
def create_organization_camera_role(organization_id: str, **kwargs):
    """
    Create camerarole
    
    Args:
        organization_id: Organization ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with camerarole data
    """
    try:
        result = meraki_client.dashboard.camera.createOrganizationCameraRole(organization_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="delete_network_camera_quality_retention_profile",
    description="Delete cameraqualityretentionprofile"
)
def delete_network_camera_quality_retention_profile(network_id: str):
    """
    Delete cameraqualityretentionprofile
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with cameraqualityretentionprofile data
    """
    try:
        result = meraki_client.dashboard.camera.deleteNetworkCameraQualityRetentionProfile(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="delete_network_camera_wireless_profile",
    description="Delete camerawirelessprofile"
)
def delete_network_camera_wireless_profile(network_id: str):
    """
    Delete camerawirelessprofile
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with camerawirelessprofile data
    """
    try:
        result = meraki_client.dashboard.camera.deleteNetworkCameraWirelessProfile(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="delete_organization_camera_custom_analytics_artifact",
    description="Delete cameracustomanalyticsartifact"
)
def delete_organization_camera_custom_analytics_artifact(organization_id: str):
    """
    Delete cameracustomanalyticsartifact
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with cameracustomanalyticsartifact data
    """
    try:
        result = meraki_client.dashboard.camera.deleteOrganizationCameraCustomAnalyticsArtifact(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="delete_organization_camera_role",
    description="Delete camerarole"
)
def delete_organization_camera_role(organization_id: str):
    """
    Delete camerarole
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with camerarole data
    """
    try:
        result = meraki_client.dashboard.camera.deleteOrganizationCameraRole(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="generate_device_camera_snapshot",
    description="Manage generatecamerasnapshot"
)
def generate_device_camera_snapshot():
    """
    Manage generatecamerasnapshot
    
    Args:

    
    Returns:
        dict: API response with generatecamerasnapshot data
    """
    try:
        result = meraki_client.dashboard.camera.generateDeviceCameraSnapshot()
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_device_camera_analytics_live",
    description="Retrieve cameraanalyticslive"
)
def get_device_camera_analytics_live(serial: str):
    """
    Retrieve cameraanalyticslive
    
    Args:
        serial: Device serial number
    
    Returns:
        dict: API response with cameraanalyticslive data
    """
    try:
        result = meraki_client.dashboard.camera.getDeviceCameraAnalyticsLive(serial)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_device_camera_analytics_overview",
    description="Retrieve cameraanalyticsoverview"
)
def get_device_camera_analytics_overview(serial: str):
    """
    Retrieve cameraanalyticsoverview
    
    Args:
        serial: Device serial number
    
    Returns:
        dict: API response with cameraanalyticsoverview data
    """
    try:
        result = meraki_client.dashboard.camera.getDeviceCameraAnalyticsOverview(serial)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_device_camera_analytics_recent",
    description="Retrieve cameraanalyticsrecent"
)
def get_device_camera_analytics_recent(serial: str):
    """
    Retrieve cameraanalyticsrecent
    
    Args:
        serial: Device serial number
    
    Returns:
        dict: API response with cameraanalyticsrecent data
    """
    try:
        result = meraki_client.dashboard.camera.getDeviceCameraAnalyticsRecent(serial)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_device_camera_analytics_zone_history",
    description="Retrieve cameraanalyticszonehistory"
)
def get_device_camera_analytics_zone_history(serial: str, timespan: int = 86400):
    """
    Retrieve cameraanalyticszonehistory
    
    Args:
        serial: Device serial number
        timespan: Timespan in seconds (default: 86400)
    
    Returns:
        dict: API response with cameraanalyticszonehistory data
    """
    try:
        result = meraki_client.dashboard.camera.getDeviceCameraAnalyticsZoneHistory(serial, timespan=timespan)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_device_camera_analytics_zones",
    description="Retrieve cameraanalyticszones"
)
def get_device_camera_analytics_zones(serial: str):
    """
    Retrieve cameraanalyticszones
    
    Args:
        serial: Device serial number
    
    Returns:
        dict: API response with cameraanalyticszones data
    """
    try:
        result = meraki_client.dashboard.camera.getDeviceCameraAnalyticsZones(serial)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_device_camera_custom_analytics",
    description="Retrieve cameracustomanalytics"
)
def get_device_camera_custom_analytics(serial: str):
    """
    Retrieve cameracustomanalytics
    
    Args:
        serial: Device serial number
    
    Returns:
        dict: API response with cameracustomanalytics data
    """
    try:
        result = meraki_client.dashboard.camera.getDeviceCameraCustomAnalytics(serial)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_device_camera_quality_and_retention",
    description="Retrieve cameraqualityandretention"
)
def get_device_camera_quality_and_retention(serial: str):
    """
    Retrieve cameraqualityandretention
    
    Args:
        serial: Device serial number
    
    Returns:
        dict: API response with cameraqualityandretention data
    """
    try:
        result = meraki_client.dashboard.camera.getDeviceCameraQualityAndRetention(serial)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_device_camera_sense",
    description="Retrieve camerasense"
)
def get_device_camera_sense(serial: str):
    """
    Retrieve camerasense
    
    Args:
        serial: Device serial number
    
    Returns:
        dict: API response with camerasense data
    """
    try:
        result = meraki_client.dashboard.camera.getDeviceCameraSense(serial)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_device_camera_sense_object_detection_models",
    description="Retrieve camerasenseobjectdetectionmodels"
)
def get_device_camera_sense_object_detection_models(serial: str):
    """
    Retrieve camerasenseobjectdetectionmodels
    
    Args:
        serial: Device serial number
    
    Returns:
        dict: API response with camerasenseobjectdetectionmodels data
    """
    try:
        result = meraki_client.dashboard.camera.getDeviceCameraSenseObjectDetectionModels(serial)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_device_camera_video_link",
    description="Retrieve cameravideolink"
)
def get_device_camera_video_link(serial: str):
    """
    Retrieve cameravideolink
    
    Args:
        serial: Device serial number
    
    Returns:
        dict: API response with cameravideolink data
    """
    try:
        result = meraki_client.dashboard.camera.getDeviceCameraVideoLink(serial)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_device_camera_video_settings",
    description="Retrieve cameravideosettings"
)
def get_device_camera_video_settings(serial: str):
    """
    Retrieve cameravideosettings
    
    Args:
        serial: Device serial number
    
    Returns:
        dict: API response with cameravideosettings data
    """
    try:
        result = meraki_client.dashboard.camera.getDeviceCameraVideoSettings(serial)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_device_camera_wireless_profiles",
    description="Retrieve camerawirelessprofiles"
)
def get_device_camera_wireless_profiles(serial: str):
    """
    Retrieve camerawirelessprofiles
    
    Args:
        serial: Device serial number
    
    Returns:
        dict: API response with camerawirelessprofiles data
    """
    try:
        result = meraki_client.dashboard.camera.getDeviceCameraWirelessProfiles(serial)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_camera_quality_retention_profile",
    description="Retrieve cameraqualityretentionprofile"
)
def get_network_camera_quality_retention_profile(network_id: str):
    """
    Retrieve cameraqualityretentionprofile
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with cameraqualityretentionprofile data
    """
    try:
        result = meraki_client.dashboard.camera.getNetworkCameraQualityRetentionProfile(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_camera_quality_retention_profiles",
    description="Retrieve cameraqualityretentionprofiles"
)
def get_network_camera_quality_retention_profiles(network_id: str):
    """
    Retrieve cameraqualityretentionprofiles
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with cameraqualityretentionprofiles data
    """
    try:
        result = meraki_client.dashboard.camera.getNetworkCameraQualityRetentionProfiles(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_camera_schedules",
    description="Retrieve cameraschedules"
)
def get_network_camera_schedules(network_id: str):
    """
    Retrieve cameraschedules
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with cameraschedules data
    """
    try:
        result = meraki_client.dashboard.camera.getNetworkCameraSchedules(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_camera_wireless_profile",
    description="Retrieve camerawirelessprofile"
)
def get_network_camera_wireless_profile(network_id: str):
    """
    Retrieve camerawirelessprofile
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with camerawirelessprofile data
    """
    try:
        result = meraki_client.dashboard.camera.getNetworkCameraWirelessProfile(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_network_camera_wireless_profiles",
    description="Retrieve camerawirelessprofiles"
)
def get_network_camera_wireless_profiles(network_id: str):
    """
    Retrieve camerawirelessprofiles
    
    Args:
        network_id: Network ID
    
    Returns:
        dict: API response with camerawirelessprofiles data
    """
    try:
        result = meraki_client.dashboard.camera.getNetworkCameraWirelessProfiles(network_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_camera_boundaries_areas_by_device",
    description="Retrieve cameraboundariesareasby"
)
def get_organization_camera_boundaries_areas_by_device(organization_id: str):
    """
    Retrieve cameraboundariesareasby
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with cameraboundariesareasby data
    """
    try:
        result = meraki_client.dashboard.camera.getOrganizationCameraBoundariesAreasByDevice(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_camera_boundaries_lines_by_device",
    description="Retrieve cameraboundarieslinesby"
)
def get_organization_camera_boundaries_lines_by_device(organization_id: str):
    """
    Retrieve cameraboundarieslinesby
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with cameraboundarieslinesby data
    """
    try:
        result = meraki_client.dashboard.camera.getOrganizationCameraBoundariesLinesByDevice(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_camera_custom_analytics_artifact",
    description="Retrieve cameracustomanalyticsartifact"
)
def get_organization_camera_custom_analytics_artifact(organization_id: str):
    """
    Retrieve cameracustomanalyticsartifact
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with cameracustomanalyticsartifact data
    """
    try:
        result = meraki_client.dashboard.camera.getOrganizationCameraCustomAnalyticsArtifact(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_camera_custom_analytics_artifacts",
    description="Retrieve cameracustomanalyticsartifacts"
)
def get_organization_camera_custom_analytics_artifacts(organization_id: str):
    """
    Retrieve cameracustomanalyticsartifacts
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with cameracustomanalyticsartifacts data
    """
    try:
        result = meraki_client.dashboard.camera.getOrganizationCameraCustomAnalyticsArtifacts(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_camera_detections_history_by_boundary_by_interval",
    description="Retrieve cameradetectionshistorybyboundarybyinterval"
)
def get_organization_camera_detections_history_by_boundary_by_interval(organization_id: str, timespan: int = 86400):
    """
    Retrieve cameradetectionshistorybyboundarybyinterval
    
    Args:
        organization_id: Organization ID
        timespan: Timespan in seconds (default: 86400)
    
    Returns:
        dict: API response with cameradetectionshistorybyboundarybyinterval data
    """
    try:
        result = meraki_client.dashboard.camera.getOrganizationCameraDetectionsHistoryByBoundaryByInterval(organization_id, timespan=timespan)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_camera_onboarding_statuses",
    description="Retrieve cameraonboardingstatuses"
)
def get_organization_camera_onboarding_statuses(organization_id: str):
    """
    Retrieve cameraonboardingstatuses
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with cameraonboardingstatuses data
    """
    try:
        result = meraki_client.dashboard.camera.getOrganizationCameraOnboardingStatuses(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_camera_permission",
    description="Retrieve camerapermission"
)
def get_organization_camera_permission(organization_id: str):
    """
    Retrieve camerapermission
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with camerapermission data
    """
    try:
        result = meraki_client.dashboard.camera.getOrganizationCameraPermission(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_camera_permissions",
    description="Retrieve camerapermissions"
)
def get_organization_camera_permissions(organization_id: str):
    """
    Retrieve camerapermissions
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with camerapermissions data
    """
    try:
        result = meraki_client.dashboard.camera.getOrganizationCameraPermissions(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_camera_role",
    description="Retrieve camerarole"
)
def get_organization_camera_role(organization_id: str):
    """
    Retrieve camerarole
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with camerarole data
    """
    try:
        result = meraki_client.dashboard.camera.getOrganizationCameraRole(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="get_organization_camera_roles",
    description="Retrieve cameraroles"
)
def get_organization_camera_roles(organization_id: str):
    """
    Retrieve cameraroles
    
    Args:
        organization_id: Organization ID
    
    Returns:
        dict: API response with cameraroles data
    """
    try:
        result = meraki_client.dashboard.camera.getOrganizationCameraRoles(organization_id)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_device_camera_custom_analytics",
    description="Update cameracustomanalytics"
)
def update_device_camera_custom_analytics(serial: str, **kwargs):
    """
    Update cameracustomanalytics
    
    Args:
        serial: Device serial number
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with cameracustomanalytics data
    """
    try:
        result = meraki_client.dashboard.camera.updateDeviceCameraCustomAnalytics(serial, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_device_camera_quality_and_retention",
    description="Update cameraqualityandretention"
)
def update_device_camera_quality_and_retention(serial: str, **kwargs):
    """
    Update cameraqualityandretention
    
    Args:
        serial: Device serial number
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with cameraqualityandretention data
    """
    try:
        result = meraki_client.dashboard.camera.updateDeviceCameraQualityAndRetention(serial, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_device_camera_sense",
    description="Update camerasense"
)
def update_device_camera_sense(serial: str, **kwargs):
    """
    Update camerasense
    
    Args:
        serial: Device serial number
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with camerasense data
    """
    try:
        result = meraki_client.dashboard.camera.updateDeviceCameraSense(serial, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_device_camera_video_settings",
    description="Update cameravideosettings"
)
def update_device_camera_video_settings(serial: str, **kwargs):
    """
    Update cameravideosettings
    
    Args:
        serial: Device serial number
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with cameravideosettings data
    """
    try:
        result = meraki_client.dashboard.camera.updateDeviceCameraVideoSettings(serial, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_device_camera_wireless_profiles",
    description="Update camerawirelessprofiles"
)
def update_device_camera_wireless_profiles(serial: str, **kwargs):
    """
    Update camerawirelessprofiles
    
    Args:
        serial: Device serial number
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with camerawirelessprofiles data
    """
    try:
        result = meraki_client.dashboard.camera.updateDeviceCameraWirelessProfiles(serial, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_network_camera_quality_retention_profile",
    description="Update cameraqualityretentionprofile"
)
def update_network_camera_quality_retention_profile(network_id: str, **kwargs):
    """
    Update cameraqualityretentionprofile
    
    Args:
        network_id: Network ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with cameraqualityretentionprofile data
    """
    try:
        result = meraki_client.dashboard.camera.updateNetworkCameraQualityRetentionProfile(network_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_network_camera_wireless_profile",
    description="Update camerawirelessprofile"
)
def update_network_camera_wireless_profile(network_id: str, **kwargs):
    """
    Update camerawirelessprofile
    
    Args:
        network_id: Network ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with camerawirelessprofile data
    """
    try:
        result = meraki_client.dashboard.camera.updateNetworkCameraWirelessProfile(network_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_organization_camera_onboarding_statuses",
    description="Update cameraonboardingstatuses"
)
def update_organization_camera_onboarding_statuses(organization_id: str, **kwargs):
    """
    Update cameraonboardingstatuses
    
    Args:
        organization_id: Organization ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with cameraonboardingstatuses data
    """
    try:
        result = meraki_client.dashboard.camera.updateOrganizationCameraOnboardingStatuses(organization_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}

@app.tool(
    name="update_organization_camera_role",
    description="Update camerarole"
)
def update_organization_camera_role(organization_id: str, **kwargs):
    """
    Update camerarole
    
    Args:
        organization_id: Organization ID
        **kwargs: Additional parameters for the operation
    
    Returns:
        dict: API response with camerarole data
    """
    try:
        result = meraki_client.dashboard.camera.updateOrganizationCameraRole(organization_id, **kwargs)
        return result
    except meraki.APIError as e:
        return {"error": f"API Error: {e}"}
    except Exception as e:
        return {"error": f"Error: {e}"}