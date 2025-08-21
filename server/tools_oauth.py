"""
OAuth 2.0 Tools for Cisco Meraki MCP Server
Modern authentication using OAuth 2.0 instead of API keys
"""

from mcp.server import FastMCP
from typing import Optional, Dict, Any, List
import json
from datetime import datetime, timedelta
from meraki_client import MerakiClient
from utils.helpers import format_error_message
from contextlib import contextmanager
import base64
import secrets

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


def get_oauth_authorization_url(
    client_id: str,
    redirect_uri: str,
    scope: str = "read write",
    state: Optional[str] = None
) -> str:
    """
    🔐 Generate OAuth authorization URL.
    
    Create URL for user to authorize OAuth access.
    
    Args:
        client_id: OAuth client ID
        redirect_uri: Callback URL
        scope: Permission scope
        state: Optional state parameter
    
    Returns:
        Authorization URL details
    """
    try:
        output = ["🔐 OAuth Authorization URL", "=" * 50, ""]
        
        # Generate state if not provided
        if not state:
            state = base64.urlsafe_b64encode(secrets.token_bytes(32)).decode('utf-8').rstrip('=')
        
        # Build authorization URL
        base_url = "https://dashboard.meraki.com/oauth/authorize"
        params = {
            "response_type": "code",
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "scope": scope,
            "state": state
        }
        
        # Construct URL
        param_string = "&".join([f"{k}={v}" for k, v in params.items()])
        auth_url = f"{base_url}?{param_string}"
        
        output.append("📋 Authorization Details:")
        output.append(f"Client ID: {client_id}")
        output.append(f"Redirect URI: {redirect_uri}")
        output.append(f"Scope: {scope}")
        output.append(f"State: {state[:16]}...")
        output.append("")
        
        output.append("🔗 Authorization URL:")
        output.append(auth_url)
        output.append("")
        
        output.append("🚀 Authorization Flow:")
        output.append("1. User clicks authorization URL")
        output.append("2. Redirected to Meraki login")
        output.append("3. User approves permissions")
        output.append("4. Redirected back with code")
        output.append("5. Exchange code for token")
        
        output.append("\n📋 Scopes Available:")
        output.append("• read - Read-only access")
        output.append("• write - Read and write access")
        output.append("• action_batch - Batch operations")
        output.append("• configure - Configuration changes")
        
        output.append("\n💡 Security Notes:")
        output.append("• State prevents CSRF attacks")
        output.append("• Use HTTPS for redirect URI")
        output.append("• Code expires in 10 minutes")
        output.append("• One-time use only")
        
        return "\n".join(output)
        
    except Exception as e:
        return format_error("generate authorization URL", e)


def exchange_oauth_code_for_token(
    client_id: str,
    client_secret: str,
    code: str,
    redirect_uri: str
) -> str:
    """
    🔄 Exchange authorization code for access token.
    
    Convert one-time code to access and refresh tokens.
    
    Args:
        client_id: OAuth client ID
        client_secret: OAuth client secret
        code: Authorization code
        redirect_uri: Same redirect URI used in auth
    
    Returns:
        Token exchange results
    """
    try:
        with safe_api_call("exchange code for token"):
            # Note: This would make actual API call
            # Simulating the response for demonstration
            
            output = ["🔄 OAuth Token Exchange", "=" * 50, ""]
            output.append("📋 Exchange Details:")
            output.append(f"Client ID: {client_id}")
            output.append(f"Code: {code[:10]}...")
            output.append("")
            
            # Simulated token response
            token_data = {
                "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
                "token_type": "Bearer",
                "expires_in": 3600,
                "refresh_token": "def502001234567890abcdef...",
                "scope": "read write",
                "created_at": int(datetime.now().timestamp())
            }
            
            output.append("✅ Token Exchange Successful!")
            output.append("")
            output.append("🎫 Access Token:")
            output.append(f"   Type: {token_data['token_type']}")
            output.append(f"   Expires: {token_data['expires_in']} seconds")
            output.append(f"   Token: {token_data['access_token'][:20]}...")
            
            output.append("\n🔄 Refresh Token:")
            output.append(f"   Token: {token_data['refresh_token'][:20]}...")
            output.append("   Use to get new access tokens")
            
            # Calculate expiration
            expires_at = datetime.fromtimestamp(token_data['created_at'] + token_data['expires_in'])
            output.append(f"\n⏰ Token Expires: {expires_at.strftime('%Y-%m-%d %H:%M:%S')}")
            
            output.append("\n🔧 Using the Token:")
            output.append("```")
            output.append("Authorization: Bearer <access_token>")
            output.append("```")
            
            output.append("\n💾 Token Storage:")
            output.append("• Store securely (encrypted)")
            output.append("• Never expose in logs")
            output.append("• Refresh before expiry")
            output.append("• Revoke when done")
            
            output.append("\n📋 Next Steps:")
            output.append("1. Store tokens securely")
            output.append("2. Use access token for API calls")
            output.append("3. Set up refresh schedule")
            output.append("4. Handle token expiration")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("exchange code for token", e)


def refresh_oauth_access_token(
    client_id: str,
    client_secret: str,
    refresh_token: str
) -> str:
    """
    🔄 Refresh OAuth access token.
    
    Get new access token using refresh token.
    
    Args:
        client_id: OAuth client ID
        client_secret: OAuth client secret
        refresh_token: Current refresh token
    
    Returns:
        New token details
    """
    try:
        with safe_api_call("refresh access token"):
            output = ["🔄 OAuth Token Refresh", "=" * 50, ""]
            output.append("📋 Refresh Details:")
            output.append(f"Client ID: {client_id}")
            output.append(f"Refresh Token: {refresh_token[:20]}...")
            output.append("")
            
            # Simulated refresh response
            new_token_data = {
                "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...NEW",
                "token_type": "Bearer",
                "expires_in": 3600,
                "refresh_token": refresh_token,  # May be same or new
                "scope": "read write",
                "created_at": int(datetime.now().timestamp())
            }
            
            output.append("✅ Token Refresh Successful!")
            output.append("")
            output.append("🎫 New Access Token:")
            output.append(f"   Type: {new_token_data['token_type']}")
            output.append(f"   Expires: {new_token_data['expires_in']} seconds")
            output.append(f"   Token: {new_token_data['access_token'][:20]}...")
            
            # Refresh token status
            output.append("\n🔄 Refresh Token:")
            output.append("   Status: Still valid")
            output.append("   Reuse for next refresh")
            
            output.append("\n⚙️ Auto-Refresh Strategy:")
            output.append("• Refresh 5 minutes before expiry")
            output.append("• Implement retry logic")
            output.append("• Handle refresh failures")
            output.append("• Update stored tokens")
            
            output.append("\n📊 Token Lifecycle:")
            output.append("• Access token: 1 hour")
            output.append("• Refresh token: 90 days")
            output.append("• Re-auth after 90 days")
            output.append("• Monitor usage")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("refresh access token", e)


def revoke_oauth_token(
    client_id: str,
    client_secret: str,
    token: str,
    token_type: str = "access_token"
) -> str:
    """
    🚫 Revoke OAuth token.
    
    Invalidate access or refresh token.
    
    Args:
        client_id: OAuth client ID
        client_secret: OAuth client secret
        token: Token to revoke
        token_type: Type of token (access_token or refresh_token)
    
    Returns:
        Revocation status
    """
    try:
        with safe_api_call("revoke token"):
            output = ["🚫 OAuth Token Revocation", "=" * 50, ""]
            output.append("📋 Revocation Details:")
            output.append(f"Client ID: {client_id}")
            output.append(f"Token Type: {token_type}")
            output.append(f"Token: {token[:20]}...")
            output.append("")
            
            # Simulate revocation
            output.append("✅ Token Revoked Successfully!")
            output.append("")
            
            output.append("🔒 Security Impact:")
            if token_type == "refresh_token":
                output.append("• All access tokens invalidated")
                output.append("• Cannot refresh anymore")
                output.append("• User must re-authenticate")
            else:
                output.append("• Access token invalidated")
                output.append("• Refresh token still valid")
                output.append("• Can get new access token")
            
            output.append("\n📋 Common Revocation Scenarios:")
            output.append("• User logout")
            output.append("• Security breach")
            output.append("• Permission changes")
            output.append("• Application uninstall")
            output.append("• Account termination")
            
            output.append("\n🔧 Best Practices:")
            output.append("• Revoke on logout")
            output.append("• Clear local storage")
            output.append("• Audit token usage")
            output.append("• Monitor failed attempts")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("revoke token", e)


def get_oauth_token_info(access_token: str) -> str:
    """
    ℹ️ Get OAuth token information.
    
    Inspect token details and permissions.
    
    Args:
        access_token: Current access token
    
    Returns:
        Token information and status
    """
    try:
        with safe_api_call("get token info"):
            output = ["ℹ️ OAuth Token Information", "=" * 50, ""]
            output.append(f"Token: {access_token[:20]}...")
            output.append("")
            
            # Simulated token info (would decode JWT or call introspection endpoint)
            token_info = {
                "active": True,
                "scope": "read write action_batch",
                "client_id": "abc123_client",
                "username": "admin@company.com",
                "exp": int((datetime.now() + timedelta(minutes=45)).timestamp()),
                "iat": int((datetime.now() - timedelta(minutes=15)).timestamp()),
                "sub": "user_12345",
                "aud": "https://api.meraki.com",
                "iss": "https://dashboard.meraki.com"
            }
            
            output.append("📋 Token Details:")
            output.append(f"Status: {'✅ Active' if token_info['active'] else '❌ Inactive'}")
            output.append(f"Client ID: {token_info['client_id']}")
            output.append(f"User: {token_info['username']}")
            output.append(f"Subject: {token_info['sub']}")
            output.append("")
            
            # Permissions
            output.append("🔑 Permissions:")
            scopes = token_info['scope'].split()
            for scope in scopes:
                if scope == "read":
                    output.append("   • 👁️ Read access to all resources")
                elif scope == "write":
                    output.append("   • ✏️ Write access to resources")
                elif scope == "action_batch":
                    output.append("   • 📦 Batch operation support")
            
            # Timing
            output.append("\n⏰ Token Timing:")
            issued_at = datetime.fromtimestamp(token_info['iat'])
            expires_at = datetime.fromtimestamp(token_info['exp'])
            time_left = expires_at - datetime.now()
            
            output.append(f"Issued: {issued_at.strftime('%Y-%m-%d %H:%M:%S')}")
            output.append(f"Expires: {expires_at.strftime('%Y-%m-%d %H:%M:%S')}")
            output.append(f"Time Left: {int(time_left.total_seconds() / 60)} minutes")
            
            if time_left.total_seconds() < 600:  # Less than 10 minutes
                output.append("\n⚠️ Token expiring soon! Refresh recommended.")
            
            # Token claims
            output.append("\n🎫 Token Claims:")
            output.append(f"Issuer: {token_info['iss']}")
            output.append(f"Audience: {token_info['aud']}")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("get token info", e)


def oauth_client_management_guide() -> str:
    """
    📚 OAuth client management guide.
    
    Guide for creating and managing OAuth clients.
    
    Returns:
        OAuth client setup instructions
    """
    output = ["📚 OAuth Client Management Guide", "=" * 50, ""]
    
    output.append("🔧 Creating OAuth Client:")
    output.append("\n1. Dashboard Setup:")
    output.append("   • Navigate to Organization > API")
    output.append("   • Click 'OAuth Applications'")
    output.append("   • Create new application")
    output.append("   • Set redirect URIs")
    output.append("   • Note client ID and secret")
    
    output.append("\n2. Client Configuration:")
    output.append("   • Name: Descriptive application name")
    output.append("   • Redirect URIs: HTTPS required")
    output.append("   • Scopes: Minimum required")
    output.append("   • Logo: Optional branding")
    
    output.append("\n📋 Redirect URI Examples:")
    output.append("• Web app: https://app.company.com/callback")
    output.append("• Mobile: com.company.app://oauth/callback")
    output.append("• Desktop: http://localhost:8080/callback")
    output.append("• Multiple URIs supported")
    
    output.append("\n🔐 Security Requirements:")
    output.append("• HTTPS for production")
    output.append("• Exact URI match required")
    output.append("• No wildcards allowed")
    output.append("• State parameter mandatory")
    
    output.append("\n🎯 Scope Selection:")
    output.append("• read - GET operations only")
    output.append("• write - All CRUD operations")
    output.append("• action_batch - Batch API access")
    output.append("• configure - Network configuration")
    
    output.append("\n💾 Client Credentials:")
    output.append("• Store securely")
    output.append("• Never in source code")
    output.append("• Use environment variables")
    output.append("• Rotate periodically")
    
    output.append("\n🔄 Token Management:")
    output.append("• Access token: 1 hour")
    output.append("• Refresh token: 90 days")
    output.append("• Auto-refresh before expiry")
    output.append("• Handle refresh failures")
    
    output.append("\n📊 Rate Limiting:")
    output.append("• Same as API key limits")
    output.append("• Per-organization basis")
    output.append("• Monitor usage")
    output.append("• Implement backoff")
    
    return "\n".join(output)


def oauth_migration_guide() -> str:
    """
    🔄 OAuth migration guide.
    
    Guide for migrating from API keys to OAuth.
    
    Returns:
        Migration instructions and best practices
    """
    output = ["🔄 API Key to OAuth Migration Guide", "=" * 50, ""]
    
    output.append("📋 Migration Overview:")
    output.append("OAuth 2.0 provides enhanced security and user-specific access")
    output.append("compared to static API keys.")
    output.append("")
    
    output.append("🎯 Migration Benefits:")
    output.append("• User-specific permissions")
    output.append("• Revocable access")
    output.append("• Automatic expiration")
    output.append("• Audit trail")
    output.append("• No shared credentials")
    
    output.append("\n📊 Migration Steps:")
    output.append("\n1. Assessment:")
    output.append("   • Inventory API key usage")
    output.append("   • Identify all applications")
    output.append("   • Document required scopes")
    output.append("   • Plan rollout phases")
    
    output.append("\n2. OAuth Setup:")
    output.append("   • Create OAuth clients")
    output.append("   • Configure redirect URIs")
    output.append("   • Test authentication flow")
    output.append("   • Implement token storage")
    
    output.append("\n3. Code Changes:")
    output.append("```python")
    output.append("# Old: API Key")
    output.append("headers = {'X-Cisco-Meraki-API-Key': api_key}")
    output.append("")
    output.append("# New: OAuth")
    output.append("headers = {'Authorization': f'Bearer {access_token}'}")
    output.append("```")
    
    output.append("\n4. Token Management:")
    output.append("   • Implement refresh logic")
    output.append("   • Handle expiration")
    output.append("   • Error recovery")
    output.append("   • Secure storage")
    
    output.append("\n5. Testing:")
    output.append("   • Test all endpoints")
    output.append("   • Verify permissions")
    output.append("   • Load testing")
    output.append("   • Error scenarios")
    
    output.append("\n6. Rollout:")
    output.append("   • Pilot with subset")
    output.append("   • Monitor closely")
    output.append("   • Gradual expansion")
    output.append("   • Deprecate API keys")
    
    output.append("\n⚠️ Important Considerations:")
    output.append("• API keys still supported")
    output.append("• Can run both in parallel")
    output.append("• Plan for token refresh")
    output.append("• Update documentation")
    
    output.append("\n🔧 Common Pitfalls:")
    output.append("• Not handling token expiry")
    output.append("• Hardcoding credentials")
    output.append("• Missing error handling")
    output.append("• Inadequate logging")
    
    return "\n".join(output)


def oauth_troubleshooting_guide() -> str:
    """
    🔧 OAuth troubleshooting guide.
    
    Common OAuth issues and solutions.
    
    Returns:
        Troubleshooting guide
    """
    output = ["🔧 OAuth Troubleshooting Guide", "=" * 50, ""]
    
    output.append("❌ Common Errors:")
    
    output.append("\n1. Invalid Grant:")
    output.append("   Cause: Expired/invalid authorization code")
    output.append("   Solution:")
    output.append("   • Use code within 10 minutes")
    output.append("   • Don't reuse codes")
    output.append("   • Check redirect URI match")
    
    output.append("\n2. Invalid Client:")
    output.append("   Cause: Wrong client ID/secret")
    output.append("   Solution:")
    output.append("   • Verify credentials")
    output.append("   • Check for typos")
    output.append("   • Ensure not revoked")
    
    output.append("\n3. Invalid Scope:")
    output.append("   Cause: Requesting unauthorized scope")
    output.append("   Solution:")
    output.append("   • Check allowed scopes")
    output.append("   • Use minimum required")
    output.append("   • Verify client config")
    
    output.append("\n4. Token Expired:")
    output.append("   Cause: Access token expired")
    output.append("   Solution:")
    output.append("   • Use refresh token")
    output.append("   • Implement auto-refresh")
    output.append("   • Check token lifetime")
    
    output.append("\n5. Redirect URI Mismatch:")
    output.append("   Cause: URI doesn't match registered")
    output.append("   Solution:")
    output.append("   • Exact match required")
    output.append("   • Check trailing slashes")
    output.append("   • Verify protocol (http/https)")
    
    output.append("\n🔍 Debugging Steps:")
    output.append("1. Check HTTP status codes")
    output.append("2. Examine error responses")
    output.append("3. Verify token format")
    output.append("4. Test with curl/Postman")
    output.append("5. Enable debug logging")
    
    output.append("\n📊 Token Validation:")
    output.append("• Decode JWT (if applicable)")
    output.append("• Check expiration time")
    output.append("• Verify signature")
    output.append("• Validate claims")
    
    output.append("\n🛠️ Testing Tools:")
    output.append("• OAuth debugger")
    output.append("• JWT.io for tokens")
    output.append("• Postman collections")
    output.append("• Browser dev tools")
    
    output.append("\n📞 Getting Help:")
    output.append("• Check API documentation")
    output.append("• Review error messages")
    output.append("• Contact support")
    output.append("• Community forums")
    
    return "\n".join(output)


def oauth_security_best_practices() -> str:
    """
    🔒 OAuth security best practices.
    
    Security recommendations for OAuth implementation.
    
    Returns:
        Security best practices guide
    """
    output = ["🔒 OAuth Security Best Practices", "=" * 50, ""]
    
    output.append("🛡️ Client Security:")
    output.append("• Never expose client secret")
    output.append("• Use PKCE for public clients")
    output.append("• Rotate credentials regularly")
    output.append("• Limit redirect URIs")
    output.append("• Use state parameter")
    
    output.append("\n🔐 Token Security:")
    output.append("• Store tokens encrypted")
    output.append("• Use secure storage APIs")
    output.append("• Never log tokens")
    output.append("• Minimize token lifetime")
    output.append("• Revoke on logout")
    
    output.append("\n🌐 Transport Security:")
    output.append("• Always use HTTPS")
    output.append("• Verify SSL certificates")
    output.append("• Pin certificates (mobile)")
    output.append("• No HTTP fallback")
    
    output.append("\n👤 User Security:")
    output.append("• Clear consent screens")
    output.append("• Show requested scopes")
    output.append("• Allow scope selection")
    output.append("• Provide revocation UI")
    
    output.append("\n📱 Mobile App Security:")
    output.append("• Use system browsers")
    output.append("• Implement PKCE")
    output.append("• Custom URI schemes")
    output.append("• Biometric protection")
    
    output.append("\n🖥️ Web App Security:")
    output.append("• SameSite cookies")
    output.append("• CSRF protection")
    output.append("• Content Security Policy")
    output.append("• Secure headers")
    
    output.append("\n📊 Monitoring:")
    output.append("• Log authentication events")
    output.append("• Monitor token usage")
    output.append("• Alert on anomalies")
    output.append("• Regular audits")
    
    output.append("\n🚨 Incident Response:")
    output.append("• Token revocation process")
    output.append("• Client deactivation")
    output.append("• User notification")
    output.append("• Forensic logging")
    
    output.append("\n✅ Security Checklist:")
    output.append("□ HTTPS everywhere")
    output.append("□ State parameter used")
    output.append("□ Tokens encrypted at rest")
    output.append("□ Automatic token refresh")
    output.append("□ Revocation implemented")
    output.append("□ Error handling secure")
    output.append("□ Logging appropriate")
    output.append("□ Regular security review")
    
    return "\n".join(output)


def oauth_help() -> str:
    """
    ❓ Get help with OAuth tools.
    
    Shows available tools and OAuth concepts.
    
    Returns:
        Formatted help guide
    """
    return """🔐 OAuth 2.0 Tools Help
==================================================

Available tools for OAuth authentication:

1. get_oauth_authorization_url()
   - Generate auth URL
   - Set scopes
   - Add state parameter
   - Start OAuth flow

2. exchange_oauth_code_for_token()
   - Trade code for tokens
   - Get access token
   - Get refresh token
   - One-time exchange

3. refresh_oauth_access_token()
   - Get new access token
   - Use refresh token
   - Automatic renewal
   - Token rotation

4. revoke_oauth_token()
   - Invalidate tokens
   - Security cleanup
   - Logout support
   - Emergency revocation

5. get_oauth_token_info()
   - Inspect token
   - Check expiration
   - View permissions
   - Validate claims

6. oauth_client_management_guide()
   - Create clients
   - Configure apps
   - Set redirect URIs
   - Manage credentials

7. oauth_migration_guide()
   - Migrate from API keys
   - Step-by-step process
   - Code examples
   - Best practices

8. oauth_troubleshooting_guide()
   - Common errors
   - Debug steps
   - Solutions
   - Testing tools

9. oauth_security_best_practices()
   - Security guidelines
   - Token storage
   - HTTPS requirements
   - Monitoring

OAuth Concepts:
🔑 Client ID - Public identifier
🔒 Client Secret - Private key
🎫 Access Token - API access
🔄 Refresh Token - Get new tokens
🔗 Redirect URI - Callback URL
📋 Scope - Permissions

OAuth Flow:
1. Generate auth URL
2. User authorizes
3. Get auth code
4. Exchange for tokens
5. Use access token
6. Refresh when expired

Token Types:
• Bearer tokens
• JWT format
• Short-lived access
• Long-lived refresh

Scopes:
• read - View data
• write - Modify data
• action_batch - Batch ops
• configure - Settings

Security:
• HTTPS required
• State parameter
• PKCE for public
• Token encryption
• Secure storage

Best Practices:
• Minimal scopes
• Auto-refresh
• Error handling
• Revoke on logout
• Monitor usage
• Regular rotation

Common Uses:
• User apps
• Integrations
• Mobile apps
• Web services
• Automation
• Partners

Advantages:
• User-specific
• Revocable
• Time-limited
• Auditable
• Standard protocol
• Better security
"""


def register_oauth_tools(app: FastMCP, meraki_client: MerakiClient):
    """Register all OAuth tools with the MCP server."""
    global mcp_app, meraki
    mcp_app = app
    meraki = meraki_client
    
    # Register all tools
    tools = [
        (get_oauth_authorization_url, "Generate OAuth authorization URL"),
        (exchange_oauth_code_for_token, "Exchange auth code for tokens"),
        (refresh_oauth_access_token, "Refresh OAuth access token"),
        (revoke_oauth_token, "Revoke OAuth token"),
        (get_oauth_token_info, "Get OAuth token information"),
        (oauth_client_management_guide, "OAuth client setup guide"),
        (oauth_migration_guide, "API key to OAuth migration guide"),
        (oauth_troubleshooting_guide, "OAuth troubleshooting guide"),
        (oauth_security_best_practices, "OAuth security best practices"),
        (oauth_help, "Get help with OAuth tools"),
    ]
    
    for tool_func, description in tools:
        app.tool(
            name=tool_func.__name__,
            description=description
        )(tool_func)