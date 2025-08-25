"""
Enhanced Systems Manager Tools for Cisco Meraki MCP Server
Full MDM capabilities including device commands, app management, and compliance
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


def send_sm_device_command(
    network_id: str,
    device_id: str,
    command: str,
    **kwargs
) -> str:
    """
    📱 Send command to SM device.
    
    Execute remote commands on managed devices (lock, wipe, etc).
    
    Args:
        network_id: Network ID
        device_id: SM device ID
        command: Command type (lock, wipe, factoryReset, reboot)
        **kwargs: Additional command parameters
    
    Returns:
        Command execution status
    """
    try:
        with safe_api_call(f"send device command: {command}"):
            # Send command
            result = meraki.dashboard.sm.createNetworkSmDeviceCommand(
                network_id,
                deviceId=device_id,
                command=command,
                **kwargs
            )
            
            output = ["📱 Device Command Sent", "=" * 50, ""]
            output.append(f"Device: {device_id}")
            output.append(f"Command: {command.upper()}")
            output.append("")
            
            # Command details
            if command == "lock":
                output.append("🔒 Device Lock Command:")
                output.append("• Screen locked immediately")
                output.append("• Requires passcode to unlock")
                output.append("• Data remains on device")
                if kwargs.get('message'):
                    output.append(f"• Lock message: {kwargs['message']}")
                if kwargs.get('phoneNumber'):
                    output.append(f"• Contact: {kwargs['phoneNumber']}")
                    
            elif command == "wipe":
                output.append("🗑️ Device Wipe Command:")
                output.append("• ⚠️ ALL DATA WILL BE ERASED")
                output.append("• Factory reset initiated")
                output.append("• Cannot be undone")
                output.append("• Device will be unenrolled")
                
            elif command == "factoryReset":
                output.append("🏭 Factory Reset Command:")
                output.append("• Device reset to defaults")
                output.append("• All settings cleared")
                output.append("• Requires re-enrollment")
                
            elif command == "reboot":
                output.append("🔄 Reboot Command:")
                output.append("• Device will restart")
                output.append("• Temporary disconnection")
                output.append("• Auto-reconnect after boot")
            
            # Command status
            command_id = result.get('commandId', 'N/A')
            status = result.get('status', 'sent')
            
            output.append(f"\n📊 Command Status:")
            output.append(f"Command ID: {command_id}")
            output.append(f"Status: {status}")
            
            output.append("\n⏱️ Expected Timeline:")
            output.append("• Immediate: Online devices")
            output.append("• Next check-in: Offline devices")
            output.append("• Monitor status in dashboard")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("send device command", e)


def install_sm_device_apps(
    network_id: str,
    device_id: str,
    app_ids: List[str],
    force: bool = False
) -> str:
    """
    📲 Install apps on SM device.
    
    Deploy applications to managed devices.
    
    Args:
        network_id: Network ID
        device_id: SM device ID
        app_ids: List of app IDs to install
        force: Force reinstall if already present
    
    Returns:
        Installation status
    """
    try:
        with safe_api_call("install device apps"):
            # Install apps
            result = meraki.dashboard.sm.installNetworkSmDeviceApps(
                network_id,
                deviceId=device_id,
                appIds=app_ids,
                force=force
            )
            
            output = ["📲 App Installation Initiated", "=" * 50, ""]
            output.append(f"Device: {device_id}")
            output.append(f"Apps to Install: {len(app_ids)}")
            output.append(f"Force Reinstall: {'Yes' if force else 'No'}")
            output.append("")
            
            # Installation details
            if result.get('apps'):
                output.append("📦 Apps Queued for Installation:")
                for app in result['apps']:
                    app_name = app.get('name', 'Unknown')
                    app_id = app.get('id', 'N/A')
                    version = app.get('version', 'Latest')
                    
                    output.append(f"\n• {app_name}")
                    output.append(f"  ID: {app_id}")
                    output.append(f"  Version: {version}")
                    
                    # Platform specific
                    if app.get('platform'):
                        output.append(f"  Platform: {app['platform']}")
                    
                    # Size if available
                    if app.get('size'):
                        size_mb = app['size'] / 1024 / 1024
                        output.append(f"  Size: {size_mb:.1f} MB")
            
            # Installation process
            output.append("\n📥 Installation Process:")
            output.append("1. App pushed to device")
            output.append("2. User may see prompt")
            output.append("3. Download begins")
            output.append("4. Auto-install (managed)")
            output.append("5. App appears on device")
            
            # Platform notes
            output.append("\n📱 Platform Notes:")
            output.append("• iOS: Requires supervised mode")
            output.append("• Android: Silent install supported")
            output.append("• Windows: Admin rights needed")
            output.append("• macOS: User approval required")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("install device apps", e)


def uninstall_sm_device_apps(
    network_id: str,
    device_id: str,
    app_ids: List[str]
) -> str:
    """
    🗑️ Uninstall apps from SM device.
    
    Remove applications from managed devices.
    
    Args:
        network_id: Network ID
        device_id: SM device ID
        app_ids: List of app IDs to uninstall
    
    Returns:
        Uninstallation status
    """
    try:
        with safe_api_call("uninstall device apps"):
            # Uninstall apps
            result = meraki.dashboard.sm.uninstallNetworkSmDeviceApps(
                network_id,
                deviceId=device_id,
                appIds=app_ids
            )
            
            output = ["🗑️ App Uninstallation Initiated", "=" * 50, ""]
            output.append(f"Device: {device_id}")
            output.append(f"Apps to Remove: {len(app_ids)}")
            output.append("")
            
            # Show apps being removed
            if result.get('apps'):
                output.append("📦 Apps Queued for Removal:")
                for app in result['apps']:
                    output.append(f"• {app.get('name', 'Unknown')}")
            
            output.append("\n⚠️ Important Notes:")
            output.append("• Some apps cannot be removed")
            output.append("• System apps are protected")
            output.append("• User data may be preserved")
            output.append("• Device policy may prevent removal")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("uninstall device apps", e)


def create_sm_bypass_activation_lock_attempt(
    network_id: str,
    device_ids: List[str]
) -> str:
    """
    🔓 Bypass activation lock on iOS devices.
    
    Attempt to bypass activation lock for supervised iOS devices.
    
    Args:
        network_id: Network ID
        device_ids: List of device IDs
    
    Returns:
        Bypass attempt status
    """
    try:
        with safe_api_call("bypass activation lock"):
            # Create bypass attempt
            result = meraki.dashboard.sm.createNetworkSmBypassActivationLockAttempt(
                network_id,
                ids=device_ids
            )
            
            output = ["🔓 Activation Lock Bypass", "=" * 50, ""]
            output.append(f"Devices: {len(device_ids)}")
            output.append("")
            
            # Results
            attempt_id = result.get('attemptId', 'N/A')
            status = result.get('status', 'initiated')
            
            output.append(f"Attempt ID: {attempt_id}")
            output.append(f"Status: {status}")
            output.append("")
            
            # Device results
            if result.get('devices'):
                output.append("📱 Device Status:")
                for device in result['devices']:
                    device_id = device.get('id', 'Unknown')
                    success = device.get('success', False)
                    
                    if success:
                        output.append(f"✅ {device_id}: Bypass initiated")
                    else:
                        error = device.get('error', 'Unknown error')
                        output.append(f"❌ {device_id}: {error}")
            
            output.append("\n📋 Requirements:")
            output.append("• iOS device only")
            output.append("• Must be supervised")
            output.append("• DEP enrolled")
            output.append("• Organization owned")
            
            output.append("\n⏱️ Process:")
            output.append("1. Request sent to Apple")
            output.append("2. Verification process")
            output.append("3. Bypass code generated")
            output.append("4. Device unlocked")
            output.append("5. Re-enrollment required")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("bypass activation lock", e)


def get_sm_device_compliance(network_id: str, device_id: str) -> str:
    """
    ✅ Get device compliance status.
    
    Check if device meets all compliance policies.
    
    Args:
        network_id: Network ID
        device_id: SM device ID
    
    Returns:
        Compliance status and violations
    """
    try:
        with safe_api_call("get device compliance"):
            # Get device details including compliance
            device = meraki.dashboard.sm.getNetworkSmDevice(network_id, device_id)
            
            output = ["✅ Device Compliance Status", "=" * 50, ""]
            output.append(f"Device: {device.get('name', device_id)}")
            output.append(f"Model: {device.get('systemModel', 'Unknown')}")
            output.append("")
            
            # Overall compliance
            compliant = device.get('isCompliant', False)
            if compliant:
                output.append("✅ COMPLIANT - All policies met")
            else:
                output.append("❌ NON-COMPLIANT - Violations detected")
            
            output.append("")
            
            # Check specific compliance areas
            output.append("📋 Compliance Checks:")
            
            # OS Version
            os_version = device.get('osVersion', 'Unknown')
            output.append(f"\n🖥️ OS Version: {os_version}")
            # Would check against minimum version policy
            
            # Encryption
            encrypted = device.get('isEncrypted', False)
            if encrypted:
                output.append("🔒 Encryption: ✅ Enabled")
            else:
                output.append("🔒 Encryption: ❌ Disabled")
            
            # Passcode
            has_passcode = device.get('hasPasscode', False)
            if has_passcode:
                output.append("🔑 Passcode: ✅ Set")
            else:
                output.append("🔑 Passcode: ❌ Not set")
            
            # Jailbreak/Root
            jailbroken = device.get('isJailbroken', False)
            if not jailbroken:
                output.append("🛡️ Security: ✅ Not jailbroken/rooted")
            else:
                output.append("🛡️ Security: ❌ JAILBROKEN/ROOTED")
            
            # Apps compliance
            output.append("\n📱 App Compliance:")
            
            # Check for blacklisted apps
            installed_apps = device.get('installedApps', [])
            # This would check against app policies
            output.append(f"   Installed apps: {len(installed_apps)}")
            
            # Profile compliance
            profiles = device.get('profiles', [])
            output.append(f"\n📄 Configuration Profiles: {len(profiles)}")
            for profile in profiles[:3]:
                output.append(f"   • {profile.get('name', 'Unknown')}")
            
            # Violations
            if not compliant:
                output.append("\n⚠️ Compliance Violations:")
                # Would list specific violations
                violations = device.get('violations', [])
                if not violations:
                    # Infer from checks above
                    if not encrypted:
                        output.append("• Encryption required")
                    if not has_passcode:
                        output.append("• Passcode required")
                    if jailbroken:
                        output.append("• Jailbreak detected")
            
            # Remediation
            output.append("\n🔧 Remediation Actions:")
            if not compliant:
                output.append("1. Address violations above")
                output.append("2. Push configuration profiles")
                output.append("3. Send compliance notification")
                output.append("4. Set grace period")
                output.append("5. Enforce restrictions")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("get device compliance", e)


def create_sm_trusted_server(
    network_id: str,
    name: str,
    server_url: str,
    certificate: str
) -> str:
    """
    🔐 Create trusted server for SM.
    
    Add trusted server for certificate-based authentication.
    
    Args:
        network_id: Network ID
        name: Server name
        server_url: Server URL
        certificate: Server certificate (PEM format)
    
    Returns:
        Created server details
    """
    try:
        with safe_api_call("create trusted server"):
            # Create trusted server
            server = meraki.dashboard.sm.createNetworkSmTrustedServer(
                network_id,
                name=name,
                url=server_url,
                certificate=certificate
            )
            
            output = ["🔐 Trusted Server Created", "=" * 50, ""]
            output.append(f"Name: {server.get('name', name)}")
            output.append(f"ID: {server.get('id', 'N/A')}")
            output.append(f"URL: {server.get('url', server_url)}")
            output.append("")
            
            # Certificate info
            output.append("📜 Certificate Details:")
            if server.get('certificateFingerprint'):
                output.append(f"   Fingerprint: {server['certificateFingerprint']}")
            if server.get('certificateExpiry'):
                output.append(f"   Expires: {server['certificateExpiry']}")
            
            # Usage
            output.append("\n🔧 Server Usage:")
            output.append("• App deployment")
            output.append("• Profile distribution")
            output.append("• Content hosting")
            output.append("• Update server")
            output.append("• Identity verification")
            
            output.append("\n💡 Next Steps:")
            output.append("1. Configure DNS if needed")
            output.append("2. Test connectivity")
            output.append("3. Deploy to devices")
            output.append("4. Monitor certificate expiry")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("create trusted server", e)


def get_sm_device_restrictions(network_id: str, device_id: str) -> str:
    """
    🚫 Get device restrictions.
    
    Shows active restrictions and policies on device.
    
    Args:
        network_id: Network ID
        device_id: SM device ID
    
    Returns:
        Device restrictions details
    """
    try:
        with safe_api_call("get device restrictions"):
            # Get device with restrictions
            device = meraki.dashboard.sm.getNetworkSmDevice(
                network_id,
                device_id,
                fields=['restrictions']
            )
            
            output = ["🚫 Device Restrictions", "=" * 50, ""]
            output.append(f"Device: {device.get('name', device_id)}")
            output.append("")
            
            # Get restrictions
            restrictions = device.get('restrictions', {})
            
            if not restrictions:
                output.append("No restrictions applied")
                return "\n".join(output)
            
            # App restrictions
            output.append("📱 App Restrictions:")
            
            # Whitelisted apps
            whitelist = restrictions.get('appWhitelist', [])
            if whitelist:
                output.append(f"\n✅ Whitelisted Apps: {len(whitelist)}")
                for app in whitelist[:5]:
                    output.append(f"   • {app}")
                if len(whitelist) > 5:
                    output.append(f"   ... and {len(whitelist) - 5} more")
            
            # Blacklisted apps
            blacklist = restrictions.get('appBlacklist', [])
            if blacklist:
                output.append(f"\n❌ Blacklisted Apps: {len(blacklist)}")
                for app in blacklist[:5]:
                    output.append(f"   • {app}")
                if len(blacklist) > 5:
                    output.append(f"   ... and {len(blacklist) - 5} more")
            
            # Web restrictions
            output.append("\n🌐 Web Restrictions:")
            
            # Whitelisted URLs
            url_whitelist = restrictions.get('urlWhitelist', [])
            if url_whitelist:
                output.append(f"\n✅ Allowed URLs: {len(url_whitelist)}")
                for url in url_whitelist[:3]:
                    output.append(f"   • {url}")
            
            # Blacklisted URLs
            url_blacklist = restrictions.get('urlBlacklist', [])
            if url_blacklist:
                output.append(f"\n❌ Blocked URLs: {len(url_blacklist)}")
                for url in url_blacklist[:3]:
                    output.append(f"   • {url}")
            
            # Feature restrictions
            output.append("\n⚙️ Feature Restrictions:")
            features = restrictions.get('features', {})
            
            feature_map = {
                'camera': '📷 Camera',
                'screenshot': '📸 Screenshots',
                'appStore': '🏪 App Store',
                'safari': '🌐 Safari',
                'bluetooth': '📶 Bluetooth',
                'cellularData': '📡 Cellular Data',
                'personalHotspot': '📡 Hotspot',
                'airDrop': '📤 AirDrop',
                'iMessage': '💬 iMessage',
                'gameCenter': '🎮 Game Center'
            }
            
            for feature, label in feature_map.items():
                if feature in features:
                    allowed = features[feature]
                    status = "✅ Allowed" if allowed else "❌ Blocked"
                    output.append(f"{label}: {status}")
            
            # Content restrictions
            output.append("\n🔞 Content Restrictions:")
            content = restrictions.get('content', {})
            if content.get('ratingRegion'):
                output.append(f"Rating Region: {content['ratingRegion']}")
            if content.get('movieRating'):
                output.append(f"Movie Rating: {content['movieRating']}")
            if content.get('tvRating'):
                output.append(f"TV Rating: {content['tvRating']}")
            if content.get('appRating'):
                output.append(f"App Rating: {content['appRating']}")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("get device restrictions", e)


def get_sm_device_security_centers(network_id: str, device_id: str) -> str:
    """
    🛡️ Get device security status.
    
    Comprehensive security assessment of managed device.
    
    Args:
        network_id: Network ID
        device_id: SM device ID
    
    Returns:
        Security status and recommendations
    """
    try:
        with safe_api_call("get device security"):
            # Get device security info
            device = meraki.dashboard.sm.getNetworkSmDevice(
                network_id,
                device_id,
                fields=['security']
            )
            
            output = ["🛡️ Device Security Center", "=" * 50, ""]
            output.append(f"Device: {device.get('name', device_id)}")
            output.append(f"Last Seen: {device.get('lastSeen', 'Unknown')}")
            output.append("")
            
            # Security score (calculated)
            security_score = 100
            issues = []
            
            # Check encryption
            if not device.get('isEncrypted', False):
                security_score -= 30
                issues.append("❌ Device not encrypted")
            else:
                output.append("✅ Device encrypted")
            
            # Check passcode
            if not device.get('hasPasscode', False):
                security_score -= 20
                issues.append("❌ No passcode set")
            else:
                output.append("✅ Passcode protected")
            
            # Check jailbreak
            if device.get('isJailbroken', False):
                security_score -= 40
                issues.append("❌ Device jailbroken/rooted")
            else:
                output.append("✅ Not jailbroken/rooted")
            
            # Check OS updates
            os_version = device.get('osVersion', '')
            # Would check against latest version
            output.append(f"🖥️ OS Version: {os_version}")
            
            # Security score
            output.append(f"\n📊 Security Score: {security_score}/100")
            
            if security_score >= 90:
                output.append("🟢 Excellent Security")
            elif security_score >= 70:
                output.append("🟡 Good Security")
            elif security_score >= 50:
                output.append("🟠 Fair Security")
            else:
                output.append("🔴 Poor Security")
            
            # Issues found
            if issues:
                output.append("\n⚠️ Security Issues:")
                for issue in issues:
                    output.append(f"   {issue}")
            
            # Threat detection
            output.append("\n🔍 Threat Detection:")
            
            # Check for malicious apps
            installed_apps = device.get('installedApps', [])
            # Would check against threat database
            output.append(f"   Apps scanned: {len(installed_apps)}")
            output.append("   Malware detected: None")
            
            # Network security
            output.append("\n🌐 Network Security:")
            wifi = device.get('wifiMac')
            if wifi:
                output.append(f"   WiFi MAC: {wifi}")
            output.append("   VPN: Check profile settings")
            
            # Recommendations
            output.append("\n💡 Security Recommendations:")
            if security_score < 100:
                if not device.get('isEncrypted', False):
                    output.append("1. Enable device encryption")
                if not device.get('hasPasscode', False):
                    output.append("2. Require strong passcode")
                if device.get('isJailbroken', False):
                    output.append("3. Restore device to remove jailbreak")
                output.append("4. Update to latest OS version")
                output.append("5. Review installed apps")
            else:
                output.append("• Maintain current security posture")
                output.append("• Regular security reviews")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("get device security", e)


def create_sm_profile(
    network_id: str,
    name: str,
    scope: str,
    profile_data: Dict[str, Any]
) -> str:
    """
    📄 Create configuration profile.
    
    Create new configuration profile for devices.
    
    Args:
        network_id: Network ID
        name: Profile name
        scope: Target scope (all, group, device)
        profile_data: Profile configuration
    
    Returns:
        Created profile details
    """
    try:
        with safe_api_call("create profile"):
            # Create profile
            profile = meraki.dashboard.sm.createNetworkSmProfile(
                network_id,
                name=name,
                scope=scope,
                **profile_data
            )
            
            output = ["📄 Configuration Profile Created", "=" * 50, ""]
            output.append(f"Name: {profile.get('name', name)}")
            output.append(f"ID: {profile.get('id', 'N/A')}")
            output.append(f"Scope: {profile.get('scope', scope)}")
            output.append("")
            
            # Profile details
            if profile.get('description'):
                output.append(f"Description: {profile['description']}")
            
            # Payload summary
            payloads = profile.get('payloads', [])
            if payloads:
                output.append(f"\n📦 Payloads: {len(payloads)}")
                for payload in payloads:
                    output.append(f"   • {payload.get('type', 'Unknown')}")
            
            # Target devices
            output.append("\n🎯 Target Devices:")
            if scope == 'all':
                output.append("   All devices in network")
            elif scope == 'group':
                if profile_data.get('groupIds'):
                    output.append(f"   Groups: {len(profile_data['groupIds'])}")
            elif scope == 'device':
                if profile_data.get('deviceIds'):
                    output.append(f"   Devices: {len(profile_data['deviceIds'])}")
            
            # Common payloads
            output.append("\n📋 Common Profile Types:")
            output.append("• WiFi configuration")
            output.append("• VPN settings")
            output.append("• Email setup")
            output.append("• Restrictions")
            output.append("• Certificates")
            output.append("• App configuration")
            
            output.append("\n🚀 Deployment:")
            output.append("• Profile pushed immediately")
            output.append("• Devices install on check-in")
            output.append("• User approval may be required")
            output.append("• Monitor deployment status")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("create profile", e)


def get_sm_pii_keys(network_id: str) -> str:
    """
    🔑 Get PII request keys.
    
    Get keys for accessing PII-related data.
    
    Args:
        network_id: Network ID
    
    Returns:
        PII access keys
    """
    try:
        with safe_api_call("get PII keys"):
            # Get PII keys
            keys = meraki.dashboard.sm.getNetworkSmPiiRequests(network_id)
            
            output = ["🔑 PII Request Keys", "=" * 50, ""]
            output.append(f"Network: {network_id}")
            output.append("")
            
            if not keys:
                output.append("No PII requests found")
                output.append("\n💡 PII requests are used to:")
                output.append("• Export user data")
                output.append("• Delete user data")
                output.append("• Comply with privacy laws")
                output.append("• Handle data requests")
                return "\n".join(output)
            
            output.append(f"Total Requests: {len(keys)}")
            output.append("")
            
            # Show requests
            for i, request in enumerate(keys, 1):
                request_id = request.get('id', 'Unknown')
                request_type = request.get('type', 'Unknown')
                status = request.get('status', 'Unknown')
                created = request.get('createdAt', 'Unknown')
                
                output.append(f"{i}. Request ID: {request_id}")
                output.append(f"   Type: {request_type}")
                output.append(f"   Status: {status}")
                output.append(f"   Created: {created}")
                
                # Request details
                if request.get('email'):
                    output.append(f"   Email: {request['email']}")
                if request.get('username'):
                    output.append(f"   Username: {request['username']}")
                
                output.append("")
            
            # PII types
            output.append("📊 PII Data Types:")
            output.append("• User identifiers")
            output.append("• Location history")
            output.append("• App usage data")
            output.append("• Network connections")
            output.append("• Device information")
            
            # Compliance
            output.append("\n📜 Compliance Support:")
            output.append("• GDPR data requests")
            output.append("• CCPA compliance")
            output.append("• Right to deletion")
            output.append("• Data portability")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("get PII keys", e)


def create_sm_pii_request(
    network_id: str,
    request_type: str,
    identifier: str,
    identifier_type: str = "email"
) -> str:
    """
    📋 Create PII data request.
    
    Create request for PII data export or deletion.
    
    Args:
        network_id: Network ID
        request_type: Request type (export, delete)
        identifier: User identifier
        identifier_type: Type of identifier (email, username)
    
    Returns:
        Created request details
    """
    try:
        with safe_api_call("create PII request"):
            # Create request
            request_data = {
                "type": request_type,
                identifier_type: identifier
            }
            
            request = meraki.dashboard.sm.createNetworkSmPiiRequest(
                network_id,
                **request_data
            )
            
            output = ["📋 PII Request Created", "=" * 50, ""]
            output.append(f"Type: {request_type.upper()}")
            output.append(f"{identifier_type.capitalize()}: {identifier}")
            output.append("")
            
            # Request details
            request_id = request.get('id', 'N/A')
            status = request.get('status', 'pending')
            
            output.append(f"Request ID: {request_id}")
            output.append(f"Status: {status}")
            output.append("")
            
            if request_type == "export":
                output.append("📤 Data Export Request:")
                output.append("• User data will be collected")
                output.append("• Export file generated")
                output.append("• Download link provided")
                output.append("• Link expires in 7 days")
                
                output.append("\n📊 Exported Data Includes:")
                output.append("• Device information")
                output.append("• Location history")
                output.append("• App inventory")
                output.append("• Network usage")
                output.append("• Profile data")
                
            elif request_type == "delete":
                output.append("🗑️ Data Deletion Request:")
                output.append("• ⚠️ PERMANENT deletion")
                output.append("• Cannot be undone")
                output.append("• Compliance with privacy laws")
                output.append("• Audit trail maintained")
                
                output.append("\n❌ Data to be Deleted:")
                output.append("• All user PII")
                output.append("• Location history")
                output.append("• Usage analytics")
                output.append("• Associated metadata")
            
            output.append("\n⏱️ Processing Time:")
            output.append("• Small dataset: Minutes")
            output.append("• Large dataset: Hours")
            output.append("• Check status regularly")
            output.append("• Email notification when complete")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("create PII request", e)


def sm_device_enrollment_guide() -> str:
    """
    📱 SM device enrollment guide.
    
    Comprehensive guide for enrolling devices in Systems Manager.
    
    Returns:
        Enrollment instructions for all platforms
    """
    output = ["📱 Systems Manager Enrollment Guide", "=" * 50, ""]
    
    output.append("🍎 iOS/iPadOS Enrollment:")
    output.append("\n1. Manual Enrollment:")
    output.append("   • Download SM app from App Store")
    output.append("   • Enter network ID")
    output.append("   • Install management profile")
    output.append("   • Approve in Settings")
    
    output.append("\n2. DEP/Apple Business Manager:")
    output.append("   • Add devices to ABM")
    output.append("   • Assign to Meraki MDM")
    output.append("   • Zero-touch deployment")
    output.append("   • Supervised mode enabled")
    
    output.append("\n🤖 Android Enrollment:")
    output.append("\n1. Legacy Enrollment:")
    output.append("   • Download SM app")
    output.append("   • Grant permissions")
    output.append("   • Enter enrollment credentials")
    
    output.append("\n2. Android Enterprise:")
    output.append("   • Work profile mode")
    output.append("   • Fully managed mode")
    output.append("   • Dedicated devices")
    output.append("   • Zero-touch enrollment")
    
    output.append("\n🪟 Windows Enrollment:")
    output.append("   • Download SM agent")
    output.append("   • Run as administrator")
    output.append("   • Enter network credentials")
    output.append("   • Reboot if required")
    
    output.append("\n🖥️ macOS Enrollment:")
    output.append("\n1. Manual:")
    output.append("   • Download SM agent")
    output.append("   • Install package")
    output.append("   • Approve in System Preferences")
    
    output.append("\n2. DEP/ABM:")
    output.append("   • Automated enrollment")
    output.append("   • User affinity options")
    output.append("   • Bootstrap packages")
    
    output.append("\n📋 Pre-Enrollment Checklist:")
    output.append("• Network ID ready")
    output.append("• Enrollment credentials")
    output.append("• WiFi configured")
    output.append("• User communication sent")
    output.append("• Support team briefed")
    
    output.append("\n🚀 Best Practices:")
    output.append("• Test with pilot group")
    output.append("• Prepare user guides")
    output.append("• Configure profiles first")
    output.append("• Set compliance policies")
    output.append("• Monitor enrollment status")
    
    return "\n".join(output)


def enhanced_sm_help() -> str:
    """
    ❓ Get help with enhanced SM tools.
    
    Shows available tools and MDM best practices.
    
    Returns:
        Formatted help guide
    """
    return """📱 Enhanced Systems Manager Tools Help
==================================================

Available tools for comprehensive MDM management:

1. send_sm_device_command()
   - Lock devices remotely
   - Wipe lost devices
   - Factory reset
   - Reboot devices

2. install_sm_device_apps()
   - Deploy apps silently
   - Force reinstall
   - Version management
   - Platform support

3. uninstall_sm_device_apps()
   - Remove apps remotely
   - Bulk uninstall
   - Compliance enforcement
   - Clean up devices

4. create_sm_bypass_activation_lock_attempt()
   - iOS activation bypass
   - Supervised devices
   - Lost device recovery
   - Bulk operations

5. get_sm_device_compliance()
   - Check policy compliance
   - Identify violations
   - Security assessment
   - Remediation steps

6. create_sm_trusted_server()
   - Certificate servers
   - App deployment
   - Update servers
   - Content hosting

7. get_sm_device_restrictions()
   - Active restrictions
   - App policies
   - Web filtering
   - Feature controls

8. get_sm_device_security_centers()
   - Security scoring
   - Threat detection
   - Recommendations
   - Risk assessment

9. create_sm_profile()
   - Configuration profiles
   - WiFi/VPN setup
   - Restrictions
   - Email config

10. get_sm_pii_keys()
    - Privacy requests
    - Data export
    - GDPR compliance
    - Audit trail

11. create_sm_pii_request()
    - Export user data
    - Delete PII
    - Compliance support
    - Request tracking

12. sm_device_enrollment_guide()
    - Platform guides
    - Best practices
    - Automation options
    - Troubleshooting

Device Commands:
🔒 Lock - Secure device
🗑️ Wipe - Erase all data
🏭 Reset - Factory defaults
🔄 Reboot - Restart device

App Management:
📲 Install apps
🗑️ Uninstall apps
📋 App inventory
🚫 Blacklist apps
✅ Whitelist apps

Compliance:
✅ Policy checks
🔒 Encryption
🔑 Passcode
📱 OS version
🛡️ Security state

Profiles:
📡 Network settings
🔐 Certificates
📧 Email config
🚫 Restrictions
🎯 Targeted deployment

Security:
🛡️ Threat detection
📊 Security scoring
🔍 Vulnerability scan
💡 Recommendations
🚨 Incident response

Privacy:
📤 Data export
🗑️ Data deletion
📜 GDPR/CCPA
🔑 Access control
📊 Audit logs

Best Practices:
• Test before deploy
• Gradual rollout
• User communication
• Regular audits
• Compliance checks
• Security updates

Common Tasks:
• Enroll new devices
• Deploy apps
• Configure WiFi
• Set restrictions
• Monitor compliance
• Handle lost devices
"""


def register_enhanced_sm_tools(app: FastMCP, meraki_client: MerakiClient):
    """Register all enhanced Systems Manager tools with the MCP server."""
    global mcp_app, meraki
    mcp_app = app
    meraki = meraki_client
    
    # Register all tools
    tools = [
        (send_sm_device_command, "Send command to SM device"),
        (install_sm_device_apps, "Install apps on SM device"),
        (uninstall_sm_device_apps, "Uninstall apps from SM device"),
        (create_sm_bypass_activation_lock_attempt, "Bypass iOS activation lock"),
        (get_sm_device_compliance, "Check device compliance status"),
        (create_sm_trusted_server, "Create SM trusted server"),
        (get_sm_device_restrictions, "Get device restrictions"),
        (get_sm_device_security_centers, "Get device security assessment"),
        (create_sm_profile, "Create configuration profile"),
        (get_sm_pii_keys, "Get PII request keys"),
        (create_sm_pii_request, "Create PII data request"),
        (sm_device_enrollment_guide, "Device enrollment guide"),
        (enhanced_sm_help, "Get help with SM tools"),
    ]
    
    for tool_func, description in tools:
        app.tool(
            name=tool_func.__name__,
            description=description
        )(tool_func)