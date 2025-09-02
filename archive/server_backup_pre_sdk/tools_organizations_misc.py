"""
Miscellaneous organization tools for Cisco Meraki MCP server.

This module provides additional organization management tools.
"""

from typing import Optional, Dict, Any, List
import json

# Global references
app = None
meraki_client = None

def register_misc_tools(mcp_app, meraki):
    """Register miscellaneous organization tools."""
    global app, meraki_client
    app = mcp_app
    meraki_client = meraki
    
    # ==================== ACTION BATCHES ====================
    
    @app.tool(
        name="get_org_action_batches",
        description="📦 List action batches in an organization"
    )
    def get_org_action_batches(
        organization_id: str,
        status: Optional[str] = None
    ):
        """Get action batches."""
        try:
            kwargs = {}
            if status:
                kwargs['status'] = status
            
            result = meraki_client.dashboard.organizations.getOrganizationActionBatches(
                organization_id, **kwargs
            )
            
            response = f"# 📦 Action Batches\n\n"
            if result and isinstance(result, list):
                response += f"**Total**: {len(result)}\n\n"
                for batch in result[:10]:
                    response += f"- **{batch.get('id', 'N/A')}**: {batch.get('status', 'N/A')}\n"
            else:
                response += "*No action batches found*\n"
            return response
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    @app.tool(
        name="get_org_action_batch",
        description="📦 Get details of a specific action batch"
    )
    def get_org_action_batch(
        organization_id: str,
        action_batch_id: str
    ):
        """Get action batch details."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationActionBatch(
                organization_id, action_batch_id
            )
            
            response = f"# 📦 Action Batch Details\n\n"
            if result:
                response += f"**ID**: {result.get('id', 'N/A')}\n"
                response += f"**Status**: {result.get('status', 'N/A')}\n"
                actions = result.get('actions', [])
                response += f"**Actions**: {len(actions)}\n"
            return response
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    @app.tool(
        name="create_org_action_batch",
        description="📦➕ Create a new action batch"
    )
    def create_org_action_batch(
        organization_id: str,
        actions: str,
        confirmed: bool = False,
        synchronous: bool = False
    ):
        """Create action batch."""
        try:
            result = meraki_client.dashboard.organizations.createOrganizationActionBatch(
                organization_id,
                actions=json.loads(actions) if isinstance(actions, str) else actions,
                confirmed=confirmed,
                synchronous=synchronous
            )
            
            response = f"# ✅ Created Action Batch\n\n"
            response += f"**ID**: {result.get('id', 'N/A')}\n"
            return response
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    @app.tool(
        name="update_org_action_batch",
        description="📦✏️ Update an action batch"
    )
    def update_org_action_batch(
        organization_id: str,
        action_batch_id: str,
        confirmed: Optional[bool] = None,
        synchronous: Optional[bool] = None
    ):
        """Update action batch."""
        try:
            kwargs = {}
            if confirmed is not None:
                kwargs['confirmed'] = confirmed
            if synchronous is not None:
                kwargs['synchronous'] = synchronous
            
            result = meraki_client.dashboard.organizations.updateOrganizationActionBatch(
                organization_id, action_batch_id, **kwargs
            )
            
            response = f"# ✅ Updated Action Batch\n\n"
            response += f"**ID**: {action_batch_id}\n"
            return response
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    @app.tool(
        name="delete_org_action_batch",
        description="📦❌ Delete an action batch"
    )
    def delete_org_action_batch(
        organization_id: str,
        action_batch_id: str
    ):
        """Delete action batch."""
        try:
            meraki_client.dashboard.organizations.deleteOrganizationActionBatch(
                organization_id, action_batch_id
            )
            return f"# ✅ Deleted Action Batch\n\n**ID**: {action_batch_id}\n"
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    # ==================== API REQUESTS ====================
    
    @app.tool(
        name="get_org_api_requests",
        description="🔌 Get API request logs"
    )
    def get_org_api_requests(
        organization_id: str,
        t0: Optional[str] = None,
        t1: Optional[str] = None,
        timespan: Optional[float] = None,
        per_page: int = 50,
        starting_after: Optional[str] = None,
        ending_before: Optional[str] = None,
        admin_id: Optional[str] = None,
        path: Optional[str] = None,
        method: Optional[str] = None,
        response_code: Optional[int] = None,
        source_ip: Optional[str] = None,
        user_agent: Optional[str] = None,
        version: Optional[int] = None,
        operation_ids: Optional[str] = None
    ):
        """Get API requests."""
        try:
            kwargs = {"perPage": per_page}
            
            if t0:
                kwargs["t0"] = t0
            if t1:
                kwargs["t1"] = t1
            if timespan:
                kwargs["timespan"] = timespan
            if starting_after:
                kwargs["startingAfter"] = starting_after
            if ending_before:
                kwargs["endingBefore"] = ending_before
            if admin_id:
                kwargs["adminId"] = admin_id
            if path:
                kwargs["path"] = path
            if method:
                kwargs["method"] = method
            if response_code:
                kwargs["responseCode"] = response_code
            if source_ip:
                kwargs["sourceIp"] = source_ip
            if user_agent:
                kwargs["userAgent"] = user_agent
            if version:
                kwargs["version"] = version
            if operation_ids:
                kwargs["operationIds"] = [o.strip() for o in operation_ids.split(',')]
            
            result = meraki_client.dashboard.organizations.getOrganizationApiRequests(
                organization_id, **kwargs
            )
            
            response = f"# 🔌 API Requests\n\n"
            if result and isinstance(result, list):
                response += f"**Total**: {len(result)}\n\n"
                for req in result[:10]:
                    response += f"- **{req.get('method', 'N/A')}** {req.get('path', 'N/A')}\n"
                    response += f"  - Response: {req.get('responseCode', 'N/A')}\n"
                    response += f"  - Time: {req.get('ts', 'N/A')}\n"
            return response
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    @app.tool(
        name="get_org_api_requests_overview",
        description="📊 Get API requests overview"
    )
    def get_org_api_requests_overview(
        organization_id: str,
        t0: Optional[str] = None,
        t1: Optional[str] = None,
        timespan: Optional[float] = None
    ):
        """Get API requests overview."""
        try:
            kwargs = {}
            if t0:
                kwargs["t0"] = t0
            if t1:
                kwargs["t1"] = t1
            if timespan:
                kwargs["timespan"] = timespan
            
            result = meraki_client.dashboard.organizations.getOrganizationApiRequestsOverview(
                organization_id, **kwargs
            )
            
            response = f"# 📊 API Requests Overview\n\n"
            if result:
                response += f"**Total**: {result.get('numberOfRequests', 0)}\n"
                response += f"**Success Rate**: {result.get('successRate', 0):.1f}%\n"
            return response
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    @app.tool(
        name="get_org_api_requests_overview_response_codes",
        description="📊 Get API response codes by interval"
    )
    def get_org_api_requests_overview_response_codes(
        organization_id: str,
        t0: Optional[str] = None,
        t1: Optional[str] = None,
        timespan: Optional[float] = None,
        interval: Optional[int] = None,
        version: Optional[int] = None,
        operation_ids: Optional[str] = None,
        source_ips: Optional[str] = None,
        admin_ids: Optional[str] = None,
        paths: Optional[str] = None
    ):
        """Get API response codes."""
        try:
            kwargs = {}
            if t0:
                kwargs["t0"] = t0
            if t1:
                kwargs["t1"] = t1
            if timespan:
                kwargs["timespan"] = timespan
            if interval:
                kwargs["interval"] = interval
            if version:
                kwargs["version"] = version
            if operation_ids:
                kwargs["operationIds"] = [o.strip() for o in operation_ids.split(',')]
            if source_ips:
                kwargs["sourceIps"] = [s.strip() for s in source_ips.split(',')]
            if admin_ids:
                kwargs["adminIds"] = [a.strip() for a in admin_ids.split(',')]
            if paths:
                kwargs["paths"] = [p.strip() for p in paths.split(',')]
            
            result = meraki_client.dashboard.organizations.getOrganizationApiRequestsOverviewResponseCodesByInterval(
                organization_id, **kwargs
            )
            
            response = f"# 📊 API Response Codes\n\n"
            if result and isinstance(result, list):
                for interval in result[:5]:
                    response += f"**{interval.get('startTs', 'N/A')}**\n"
                    counts = interval.get('counts', {})
                    for code, count in counts.items():
                        response += f"  - {code}: {count}\n"
            return response
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    # ==================== ORGANIZATION OPERATIONS ====================
    
    @app.tool(
        name="clone_organization",
        description="🔄 Clone an organization"
    )
    def clone_organization(
        organization_id: str,
        name: str
    ):
        """Clone organization."""
        try:
            result = meraki_client.dashboard.organizations.cloneOrganization(
                organization_id, name=name
            )
            
            response = f"# ✅ Cloned Organization\n\n"
            response += f"**New Name**: {name}\n"
            response += f"**New ID**: {result.get('id', 'N/A')}\n"
            return response
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    @app.tool(
        name="get_org_clients_overview",
        description="📊 Get clients overview"
    )
    def get_org_clients_overview(
        organization_id: str,
        t0: Optional[str] = None,
        t1: Optional[str] = None,
        timespan: Optional[float] = None
    ):
        """Get clients overview."""
        try:
            kwargs = {}
            if t0:
                kwargs["t0"] = t0
            if t1:
                kwargs["t1"] = t1
            if timespan:
                kwargs["timespan"] = timespan
            
            result = meraki_client.dashboard.organizations.getOrganizationClientsOverview(
                organization_id, **kwargs
            )
            
            response = f"# 📊 Clients Overview\n\n"
            if result:
                counts = result.get('counts', {})
                response += f"**Total**: {counts.get('total', 0)}\n"
                
                usage = result.get('usage', {})
                if usage:
                    response += f"\n## Usage\n"
                    response += f"- **Downstream**: {usage.get('downstream', 0)/1e9:.2f} GB\n"
                    response += f"- **Upstream**: {usage.get('upstream', 0)/1e9:.2f} GB\n"
            return response
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    @app.tool(
        name="get_org_login_security",
        description="🔐 Get login security settings"
    )
    def get_org_login_security(
        organization_id: str
    ):
        """Get login security."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationLoginSecurity(
                organization_id
            )
            
            response = f"# 🔐 Login Security\n\n"
            if result:
                response += f"**Enforce Two-Factor**: {result.get('enforceTwoFactorAuth', False)}\n"
                response += f"**Enforce Account Lockout**: {result.get('enforceAccountLockout', False)}\n"
                response += f"**Lockout Attempts**: {result.get('accountLockoutAttempts', 'N/A')}\n"
                response += f"**Idle Timeout**: {result.get('idleTimeoutMinutes', 'N/A')} minutes\n"
                response += f"**Enforce Password Expiration**: {result.get('enforcePasswordExpiration', False)}\n"
                response += f"**Password Expiration Days**: {result.get('passwordExpirationDays', 'N/A')}\n"
                response += f"**Enforce Strong Passwords**: {result.get('enforceStrongPasswords', False)}\n"
            return response
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    @app.tool(
        name="update_org_login_security",
        description="🔐✏️ Update login security settings"
    )
    def update_org_login_security(
        organization_id: str,
        enforce_two_factor_auth: Optional[bool] = None,
        enforce_account_lockout: Optional[bool] = None,
        account_lockout_attempts: Optional[int] = None,
        idle_timeout_minutes: Optional[int] = None,
        enforce_password_expiration: Optional[bool] = None,
        password_expiration_days: Optional[int] = None,
        enforce_strong_passwords: Optional[bool] = None,
        enforce_idle_timeout: Optional[bool] = None,
        enforce_login_ip_ranges: Optional[bool] = None,
        login_ip_ranges: Optional[str] = None,
        api_authentication: Optional[str] = None
    ):
        """Update login security."""
        try:
            kwargs = {}
            
            if enforce_two_factor_auth is not None:
                kwargs['enforceTwoFactorAuth'] = enforce_two_factor_auth
            if enforce_account_lockout is not None:
                kwargs['enforceAccountLockout'] = enforce_account_lockout
            if account_lockout_attempts:
                kwargs['accountLockoutAttempts'] = account_lockout_attempts
            if idle_timeout_minutes:
                kwargs['idleTimeoutMinutes'] = idle_timeout_minutes
            if enforce_password_expiration is not None:
                kwargs['enforcePasswordExpiration'] = enforce_password_expiration
            if password_expiration_days:
                kwargs['passwordExpirationDays'] = password_expiration_days
            if enforce_strong_passwords is not None:
                kwargs['enforceStrongPasswords'] = enforce_strong_passwords
            if enforce_idle_timeout is not None:
                kwargs['enforceIdleTimeout'] = enforce_idle_timeout
            if enforce_login_ip_ranges is not None:
                kwargs['enforceLoginIpRanges'] = enforce_login_ip_ranges
            if login_ip_ranges:
                kwargs['loginIpRanges'] = [r.strip() for r in login_ip_ranges.split(',')]
            if api_authentication:
                kwargs['apiAuthentication'] = json.loads(api_authentication) if isinstance(api_authentication, str) else api_authentication
            
            result = meraki_client.dashboard.organizations.updateOrganizationLoginSecurity(
                organization_id, **kwargs
            )
            
            response = f"# ✅ Updated Login Security\n\n"
            return response
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    @app.tool(
        name="get_org_openapi_spec",
        description="📋 Get OpenAPI specification"
    )
    def get_org_openapi_spec(
        organization_id: str,
        version: Optional[int] = None
    ):
        """Get OpenAPI spec."""
        try:
            kwargs = {}
            if version:
                kwargs['version'] = version
            
            result = meraki_client.dashboard.organizations.getOrganizationOpenapiSpec(
                organization_id, **kwargs
            )
            
            response = f"# 📋 OpenAPI Specification\n\n"
            if result:
                response += f"**Version**: {result.get('openapi', 'N/A')}\n"
                info = result.get('info', {})
                response += f"**Title**: {info.get('title', 'N/A')}\n"
                response += f"**API Version**: {info.get('version', 'N/A')}\n"
                
                paths = result.get('paths', {})
                response += f"\n**Endpoints**: {len(paths)}\n"
            return response
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    @app.tool(
        name="get_org_webhooks_logs",
        description="🔔 Get webhooks logs"
    )
    def get_org_webhooks_logs(
        organization_id: str,
        t0: Optional[str] = None,
        t1: Optional[str] = None,
        timespan: Optional[float] = None,
        per_page: int = 50,
        starting_after: Optional[str] = None,
        ending_before: Optional[str] = None,
        url: Optional[str] = None
    ):
        """Get webhooks logs."""
        try:
            kwargs = {"perPage": per_page}
            
            if t0:
                kwargs["t0"] = t0
            if t1:
                kwargs["t1"] = t1
            if timespan:
                kwargs["timespan"] = timespan
            if starting_after:
                kwargs["startingAfter"] = starting_after
            if ending_before:
                kwargs["endingBefore"] = ending_before
            if url:
                kwargs["url"] = url
            
            result = meraki_client.dashboard.organizations.getOrganizationWebhooksLogs(
                organization_id, **kwargs
            )
            
            response = f"# 🔔 Webhooks Logs\n\n"
            if result and isinstance(result, list):
                response += f"**Total**: {len(result)}\n\n"
                for log in result[:10]:
                    response += f"- **{log.get('alertType', 'N/A')}**\n"
                    response += f"  - URL: {log.get('url', 'N/A')}\n"
                    response += f"  - Response: {log.get('responseCode', 'N/A')}\n"
                    response += f"  - Time: {log.get('sentAt', 'N/A')}\n"
            return response
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    @app.tool(
        name="get_org_webhooks_callback_status",
        description="🔔 Get webhooks callback status"
    )
    def get_org_webhooks_callback_status(
        organization_id: str,
        callback_id: str
    ):
        """Get webhook callback status."""
        try:
            result = meraki_client.dashboard.organizations.getOrganizationWebhooksCallbacksStatus(
                organization_id, callback_id
            )
            
            response = f"# 🔔 Webhook Callback Status\n\n"
            if result:
                response += f"**ID**: {result.get('id', 'N/A')}\n"
                response += f"**Status**: {result.get('status', 'N/A')}\n"
                response += f"**URL**: {result.get('url', 'N/A')}\n"
            return response
        except Exception as e:
            return f"❌ Error: {str(e)}"