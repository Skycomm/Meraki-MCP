"""
API Analytics Tools for Cisco Meraki MCP Server
Monitor API usage, rate limits, and performance metrics
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


def get_organization_api_requests_overview(
    org_id: str,
    timespan: int = 7200
) -> str:
    """
    📊 Get API requests overview.
    
    Shows API usage statistics and patterns.
    
    Args:
        org_id: Organization ID
        timespan: Time period in seconds (default 2 hours)
    
    Returns:
        API usage overview
    """
    try:
        with safe_api_call("get API requests overview"):
            # Get API requests overview
            overview = meraki.dashboard.organizations.getOrganizationApiRequestsOverview(
                org_id,
                timespan=timespan
            )
            
            output = ["📊 API Requests Overview", "=" * 50, ""]
            output.append(f"Organization: {org_id}")
            output.append(f"Time Period: {timespan/3600:.1f} hours")
            output.append("")
            
            # Response codes breakdown
            response_codes = overview.get('responseCodes', {})
            total_requests = sum(response_codes.values())
            
            output.append(f"📈 Total Requests: {total_requests:,}")
            output.append("")
            
            if response_codes:
                output.append("📊 Response Code Distribution:")
                
                # Success codes (2xx)
                success_codes = {k: v for k, v in response_codes.items() if k.startswith('2')}
                success_total = sum(success_codes.values())
                success_rate = (success_total / total_requests * 100) if total_requests > 0 else 0
                
                output.append(f"\n✅ Success (2xx): {success_total:,} ({success_rate:.1f}%)")
                for code, count in sorted(success_codes.items()):
                    output.append(f"   {code}: {count:,}")
                
                # Client errors (4xx)
                client_errors = {k: v for k, v in response_codes.items() if k.startswith('4')}
                if client_errors:
                    client_total = sum(client_errors.values())
                    client_rate = (client_total / total_requests * 100) if total_requests > 0 else 0
                    
                    output.append(f"\n⚠️ Client Errors (4xx): {client_total:,} ({client_rate:.1f}%)")
                    for code, count in sorted(client_errors.items()):
                        if code == '400':
                            output.append(f"   {code} Bad Request: {count:,}")
                        elif code == '401':
                            output.append(f"   {code} Unauthorized: {count:,}")
                        elif code == '403':
                            output.append(f"   {code} Forbidden: {count:,}")
                        elif code == '404':
                            output.append(f"   {code} Not Found: {count:,}")
                        elif code == '429':
                            output.append(f"   {code} Rate Limited: {count:,} 🚨")
                        else:
                            output.append(f"   {code}: {count:,}")
                
                # Server errors (5xx)
                server_errors = {k: v for k, v in response_codes.items() if k.startswith('5')}
                if server_errors:
                    server_total = sum(server_errors.values())
                    server_rate = (server_total / total_requests * 100) if total_requests > 0 else 0
                    
                    output.append(f"\n❌ Server Errors (5xx): {server_total:,} ({server_rate:.1f}%)")
                    for code, count in sorted(server_errors.items()):
                        output.append(f"   {code}: {count:,}")
            
            # Calculate requests per minute
            requests_per_minute = (total_requests / (timespan / 60)) if timespan > 0 else 0
            output.append(f"\n⏱️ Request Rate: {requests_per_minute:.1f} req/min")
            
            # Performance insights
            output.append("\n💡 Performance Insights:")
            if response_codes.get('429', 0) > 0:
                output.append("• ⚠️ Rate limiting detected - consider request spacing")
            if success_rate < 90:
                output.append("• ⚠️ Low success rate - check error patterns")
            if requests_per_minute > 300:
                output.append("• ⚠️ High request rate - monitor rate limits")
            if success_rate > 95:
                output.append("• ✅ Excellent API health")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("get API requests overview", e)


def get_organization_api_requests_overview_by_admin(
    org_id: str,
    timespan: int = 7200
) -> str:
    """
    👤 Get API usage by admin.
    
    Shows API usage breakdown by administrator.
    
    Args:
        org_id: Organization ID
        timespan: Time period in seconds
    
    Returns:
        Per-admin API usage
    """
    try:
        with safe_api_call("get API usage by admin"):
            # Get admin-specific overview
            admin_data = meraki.dashboard.organizations.getOrganizationApiRequestsOverviewByAdmin(
                org_id,
                timespan=timespan
            )
            
            output = ["👤 API Usage by Administrator", "=" * 50, ""]
            output.append(f"Organization: {org_id}")
            output.append(f"Time Period: {timespan/3600:.1f} hours")
            output.append("")
            
            if not admin_data:
                output.append("No API usage data available")
                return "\n".join(output)
            
            # Sort admins by request count
            sorted_admins = sorted(admin_data, key=lambda x: sum(x.get('responseCodes', {}).values()), reverse=True)
            
            output.append(f"📊 Active Admins: {len(sorted_admins)}")
            output.append("")
            
            # Show top admins
            for i, admin in enumerate(sorted_admins[:10], 1):
                admin_id = admin.get('adminId', 'Unknown')
                admin_name = admin.get('name', 'Unknown Admin')
                admin_email = admin.get('email', '')
                
                response_codes = admin.get('responseCodes', {})
                total_requests = sum(response_codes.values())
                
                output.append(f"{i}. 👤 {admin_name}")
                if admin_email:
                    output.append(f"   📧 {admin_email}")
                output.append(f"   🔑 ID: {admin_id}")
                output.append(f"   📊 Requests: {total_requests:,}")
                
                # Success rate
                success_count = sum(v for k, v in response_codes.items() if k.startswith('2'))
                success_rate = (success_count / total_requests * 100) if total_requests > 0 else 0
                output.append(f"   ✅ Success Rate: {success_rate:.1f}%")
                
                # Rate limit hits
                rate_limited = response_codes.get('429', 0)
                if rate_limited > 0:
                    output.append(f"   ⚠️ Rate Limited: {rate_limited} times")
                
                # Key errors
                errors_401 = response_codes.get('401', 0)
                errors_403 = response_codes.get('403', 0)
                if errors_401 > 0 or errors_403 > 0:
                    output.append(f"   🔒 Auth Issues: {errors_401 + errors_403}")
                
                output.append("")
            
            if len(sorted_admins) > 10:
                output.append(f"... and {len(sorted_admins) - 10} more admins")
            
            # Summary statistics
            total_all_requests = sum(sum(admin.get('responseCodes', {}).values()) for admin in admin_data)
            output.append(f"\n📈 Total API Calls: {total_all_requests:,}")
            
            # Identify heavy users
            output.append("\n💡 Usage Analysis:")
            if sorted_admins:
                top_user_requests = sum(sorted_admins[0].get('responseCodes', {}).values())
                if top_user_requests > total_all_requests * 0.5:
                    output.append("• ⚠️ Single admin using >50% of API calls")
                
                # Check for automation
                for admin in sorted_admins[:3]:
                    requests = sum(admin.get('responseCodes', {}).values())
                    rate = requests / (timespan / 60)
                    if rate > 10:
                        output.append(f"• 🤖 {admin.get('name', 'Admin')} likely using automation ({rate:.1f} req/min)")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("get API usage by admin", e)


def get_organization_api_requests(
    org_id: str,
    timespan: int = 3600,
    per_page: int = 100,
    admin_id: Optional[str] = None,
    path: Optional[str] = None,
    method: Optional[str] = None,
    response_code: Optional[int] = None
) -> str:
    """
    📋 Get detailed API requests.
    
    Shows individual API requests with filtering options.
    
    Args:
        org_id: Organization ID
        timespan: Time period in seconds
        per_page: Results per page
        admin_id: Filter by admin
        path: Filter by API path
        method: Filter by HTTP method
        response_code: Filter by response code
    
    Returns:
        Detailed API request log
    """
    try:
        with safe_api_call("get API requests"):
            # Build request parameters
            params = {
                "timespan": timespan,
                "perPage": per_page
            }
            
            if admin_id:
                params["adminId"] = admin_id
            if path:
                params["path"] = path
            if method:
                params["method"] = method
            if response_code:
                params["responseCode"] = response_code
            
            # Get requests
            requests = meraki.dashboard.organizations.getOrganizationApiRequests(
                org_id,
                **params
            )
            
            output = ["📋 API Request Details", "=" * 50, ""]
            output.append(f"Organization: {org_id}")
            output.append(f"Time Period: {timespan/3600:.1f} hours")
            
            # Show filters
            if any([admin_id, path, method, response_code]):
                output.append("\n🔍 Filters Applied:")
                if admin_id:
                    output.append(f"   Admin: {admin_id}")
                if path:
                    output.append(f"   Path: {path}")
                if method:
                    output.append(f"   Method: {method}")
                if response_code:
                    output.append(f"   Response: {response_code}")
            
            output.append("")
            
            if not requests:
                output.append("No matching API requests found")
                return "\n".join(output)
            
            output.append(f"📊 Requests Found: {len(requests)}")
            if len(requests) == per_page:
                output.append(f"   (Showing first {per_page} results)")
            output.append("")
            
            # Show requests
            for i, req in enumerate(requests[:20], 1):
                timestamp = req.get('ts', 'Unknown')
                method = req.get('method', 'GET')
                path = req.get('path', 'Unknown')
                response_code = req.get('responseCode', 0)
                
                # Format timestamp
                if timestamp != 'Unknown':
                    try:
                        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                        timestamp = dt.strftime('%Y-%m-%d %H:%M:%S')
                    except:
                        pass
                
                # Response code emoji
                if 200 <= response_code < 300:
                    code_emoji = "✅"
                elif 400 <= response_code < 500:
                    code_emoji = "⚠️"
                elif response_code >= 500:
                    code_emoji = "❌"
                else:
                    code_emoji = "❓"
                
                output.append(f"{i}. {timestamp}")
                output.append(f"   {method} {path}")
                output.append(f"   {code_emoji} Response: {response_code}")
                
                # Admin info
                if req.get('adminName'):
                    output.append(f"   👤 Admin: {req['adminName']}")
                
                # Response time if available
                if req.get('responseTime'):
                    output.append(f"   ⏱️ Time: {req['responseTime']}ms")
                
                # User agent
                if req.get('userAgent'):
                    ua = req['userAgent'][:50] + "..." if len(req['userAgent']) > 50 else req['userAgent']
                    output.append(f"   🖥️ Agent: {ua}")
                
                output.append("")
            
            if len(requests) > 20:
                output.append(f"... and {len(requests) - 20} more requests")
            
            # Path analysis
            output.append("\n📊 Path Analysis:")
            path_counts = {}
            for req in requests:
                path = req.get('path', 'Unknown')
                # Simplify path by removing IDs
                simplified = path
                for part in path.split('/'):
                    if len(part) > 20 and '-' in part:  # Likely an ID
                        simplified = simplified.replace(part, '{id}')
                
                path_counts[simplified] = path_counts.get(simplified, 0) + 1
            
            # Show top paths
            top_paths = sorted(path_counts.items(), key=lambda x: x[1], reverse=True)[:5]
            for path, count in top_paths:
                output.append(f"   {path}: {count} calls")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("get API requests", e)


def analyze_api_rate_limits(org_id: str) -> str:
    """
    🚦 Analyze API rate limit usage.
    
    Shows current rate limit status and recommendations.
    
    Args:
        org_id: Organization ID
    
    Returns:
        Rate limit analysis
    """
    try:
        with safe_api_call("analyze rate limits"):
            output = ["🚦 API Rate Limit Analysis", "=" * 50, ""]
            output.append(f"Organization: {org_id}")
            output.append("")
            
            # Get recent requests to analyze rate limit patterns
            overview = meraki.dashboard.organizations.getOrganizationApiRequestsOverview(
                org_id,
                timespan=3600  # Last hour
            )
            
            response_codes = overview.get('responseCodes', {})
            rate_limited = response_codes.get('429', 0)
            total_requests = sum(response_codes.values())
            
            output.append("📊 Rate Limit Status (Last Hour):")
            output.append(f"Total Requests: {total_requests:,}")
            output.append(f"Rate Limited (429): {rate_limited:,}")
            
            if rate_limited > 0:
                rate_limit_percentage = (rate_limited / total_requests * 100) if total_requests > 0 else 0
                output.append(f"Rate Limit Hit Rate: {rate_limit_percentage:.2f}%")
                
                if rate_limit_percentage > 10:
                    output.append("\n🚨 HIGH RATE LIMIT IMPACT!")
                elif rate_limit_percentage > 5:
                    output.append("\n⚠️ Moderate rate limit impact")
                else:
                    output.append("\n📢 Minor rate limit impact")
            else:
                output.append("\n✅ No rate limiting detected!")
            
            # Calculate request rate
            requests_per_second = total_requests / 3600
            output.append(f"\n⏱️ Average Rate: {requests_per_second:.2f} req/sec")
            
            # Rate limit tiers
            output.append("\n📋 Meraki Rate Limits:")
            output.append("• Standard: 10 requests/second")
            output.append("• Burst: Up to 30 requests")
            output.append("• Per-organization basis")
            output.append("• 429 responses don't count")
            
            # Current usage tier
            output.append("\n🎯 Usage Assessment:")
            if requests_per_second < 5:
                output.append("✅ Well within limits (<50%)")
            elif requests_per_second < 8:
                output.append("📢 Approaching limits (50-80%)")
            elif requests_per_second < 10:
                output.append("⚠️ Near limits (80-100%)")
            else:
                output.append("🚨 Exceeding limits (>100%)")
            
            # Recommendations
            output.append("\n💡 Optimization Recommendations:")
            
            if rate_limited > 0:
                output.append("• Implement exponential backoff")
                output.append("• Add request queuing")
                output.append("• Use batch endpoints where possible")
                output.append("• Cache frequently accessed data")
            
            if requests_per_second > 5:
                output.append("• Consider request consolidation")
                output.append("• Implement local caching")
                output.append("• Use webhooks for updates")
                output.append("• Optimize polling intervals")
            
            # Best practices
            output.append("\n🛡️ Rate Limit Best Practices:")
            output.append("• Monitor X-RateLimit headers")
            output.append("• Implement retry logic")
            output.append("• Use action batches")
            output.append("• Respect 429 responses")
            output.append("• Track usage patterns")
            
            # Sample retry logic
            output.append("\n📝 Sample Retry Logic:")
            output.append("```python")
            output.append("if response.status_code == 429:")
            output.append("    retry_after = response.headers.get('Retry-After', 1)")
            output.append("    time.sleep(int(retry_after))")
            output.append("    return retry_request()")
            output.append("```")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("analyze rate limits", e)


def get_api_usage_by_endpoint(org_id: str, timespan: int = 86400) -> str:
    """
    🎯 Get API usage by endpoint.
    
    Shows which API endpoints are used most frequently.
    
    Args:
        org_id: Organization ID
        timespan: Time period in seconds (default 24 hours)
    
    Returns:
        Endpoint usage analysis
    """
    try:
        with safe_api_call("get API usage by endpoint"):
            # Get detailed requests
            requests = meraki.dashboard.organizations.getOrganizationApiRequests(
                org_id,
                timespan=timespan,
                perPage=1000
            )
            
            output = ["🎯 API Usage by Endpoint", "=" * 50, ""]
            output.append(f"Organization: {org_id}")
            output.append(f"Time Period: {timespan/3600:.1f} hours")
            output.append("")
            
            if not requests:
                output.append("No API usage data available")
                return "\n".join(output)
            
            # Analyze endpoints
            endpoint_stats = {}
            method_stats = {}
            category_stats = {}
            
            for req in requests:
                path = req.get('path', 'Unknown')
                method = req.get('method', 'GET')
                response_code = req.get('responseCode', 0)
                
                # Simplify path
                simplified_path = path
                for part in path.split('/'):
                    if len(part) > 20 and '-' in part:
                        simplified_path = simplified_path.replace(part, '{id}')
                
                # Track endpoint
                endpoint_key = f"{method} {simplified_path}"
                if endpoint_key not in endpoint_stats:
                    endpoint_stats[endpoint_key] = {
                        'count': 0,
                        'success': 0,
                        'errors': 0
                    }
                
                endpoint_stats[endpoint_key]['count'] += 1
                if 200 <= response_code < 300:
                    endpoint_stats[endpoint_key]['success'] += 1
                else:
                    endpoint_stats[endpoint_key]['errors'] += 1
                
                # Track method
                method_stats[method] = method_stats.get(method, 0) + 1
                
                # Track category
                if '/organizations/' in path:
                    category = 'Organizations'
                elif '/networks/' in path:
                    category = 'Networks'
                elif '/devices/' in path:
                    category = 'Devices'
                elif '/sm/' in path:
                    category = 'Systems Manager'
                elif '/wireless/' in path:
                    category = 'Wireless'
                elif '/switch/' in path:
                    category = 'Switch'
                elif '/appliance/' in path:
                    category = 'Appliance'
                else:
                    category = 'Other'
                
                category_stats[category] = category_stats.get(category, 0) + 1
            
            # Show top endpoints
            output.append("📊 Top 10 Endpoints:")
            sorted_endpoints = sorted(endpoint_stats.items(), key=lambda x: x[1]['count'], reverse=True)
            
            for i, (endpoint, stats) in enumerate(sorted_endpoints[:10], 1):
                count = stats['count']
                success_rate = (stats['success'] / count * 100) if count > 0 else 0
                
                output.append(f"\n{i}. {endpoint}")
                output.append(f"   Calls: {count:,}")
                output.append(f"   Success Rate: {success_rate:.1f}%")
                if stats['errors'] > 0:
                    output.append(f"   Errors: {stats['errors']}")
            
            # Method distribution
            output.append("\n\n📊 HTTP Method Distribution:")
            total_methods = sum(method_stats.values())
            for method, count in sorted(method_stats.items(), key=lambda x: x[1], reverse=True):
                percentage = (count / total_methods * 100) if total_methods > 0 else 0
                output.append(f"   {method}: {count:,} ({percentage:.1f}%)")
            
            # Category distribution
            output.append("\n📊 API Category Usage:")
            total_categories = sum(category_stats.values())
            for category, count in sorted(category_stats.items(), key=lambda x: x[1], reverse=True):
                percentage = (count / total_categories * 100) if total_categories > 0 else 0
                output.append(f"   {category}: {count:,} ({percentage:.1f}%)")
            
            # Insights
            output.append("\n💡 Usage Insights:")
            
            # Most used category
            if category_stats:
                top_category = max(category_stats.items(), key=lambda x: x[1])
                output.append(f"• Most used: {top_category[0]} API")
            
            # Read vs Write ratio
            read_ops = method_stats.get('GET', 0)
            write_ops = sum(v for k, v in method_stats.items() if k in ['POST', 'PUT', 'DELETE'])
            if write_ops > 0:
                read_write_ratio = read_ops / write_ops
                output.append(f"• Read/Write ratio: {read_write_ratio:.1f}:1")
            
            # Error-prone endpoints
            error_endpoints = [(ep, stats) for ep, stats in endpoint_stats.items() if stats['errors'] > stats['count'] * 0.1]
            if error_endpoints:
                output.append(f"• {len(error_endpoints)} endpoints with >10% error rate")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("get API usage by endpoint", e)


def api_performance_dashboard(org_id: str) -> str:
    """
    📊 API performance dashboard.
    
    Comprehensive performance metrics and health status.
    
    Args:
        org_id: Organization ID
    
    Returns:
        Performance dashboard
    """
    try:
        with safe_api_call("generate performance dashboard"):
            output = ["📊 API Performance Dashboard", "=" * 50, ""]
            output.append(f"Organization: {org_id}")
            output.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            output.append("")
            
            # Get various time periods
            periods = [
                ("Last Hour", 3600),
                ("Last 24 Hours", 86400),
                ("Last 7 Days", 604800)
            ]
            
            for period_name, timespan in periods:
                try:
                    overview = meraki.dashboard.organizations.getOrganizationApiRequestsOverview(
                        org_id,
                        timespan=timespan
                    )
                    
                    response_codes = overview.get('responseCodes', {})
                    total = sum(response_codes.values())
                    success = sum(v for k, v in response_codes.items() if k.startswith('2'))
                    errors = sum(v for k, v in response_codes.items() if k.startswith('4') or k.startswith('5'))
                    rate_limited = response_codes.get('429', 0)
                    
                    success_rate = (success / total * 100) if total > 0 else 0
                    error_rate = (errors / total * 100) if total > 0 else 0
                    
                    output.append(f"📅 {period_name}:")
                    output.append(f"   Total Requests: {total:,}")
                    output.append(f"   Success Rate: {success_rate:.1f}%")
                    output.append(f"   Error Rate: {error_rate:.1f}%")
                    if rate_limited > 0:
                        output.append(f"   Rate Limited: {rate_limited:,}")
                    output.append("")
                except:
                    output.append(f"📅 {period_name}: Data unavailable")
                    output.append("")
            
            # Health Status
            output.append("🏥 API Health Status:")
            
            # Get last hour for health check
            try:
                recent = meraki.dashboard.organizations.getOrganizationApiRequestsOverview(
                    org_id,
                    timespan=3600
                )
                
                codes = recent.get('responseCodes', {})
                total = sum(codes.values())
                success = sum(v for k, v in codes.items() if k.startswith('2'))
                
                if total == 0:
                    output.append("   ⚫ No recent activity")
                else:
                    success_rate = (success / total * 100)
                    if success_rate >= 95:
                        output.append("   🟢 Excellent - All systems operational")
                    elif success_rate >= 90:
                        output.append("   🟡 Good - Minor issues detected")
                    elif success_rate >= 80:
                        output.append("   🟠 Fair - Degraded performance")
                    else:
                        output.append("   🔴 Poor - Major issues detected")
                    
                    # Specific issues
                    if codes.get('429', 0) > total * 0.05:
                        output.append("   ⚠️ High rate limiting detected")
                    if codes.get('401', 0) + codes.get('403', 0) > total * 0.05:
                        output.append("   ⚠️ Authentication issues detected")
                    if codes.get('500', 0) + codes.get('502', 0) + codes.get('503', 0) > 0:
                        output.append("   ⚠️ Server errors detected")
            except:
                output.append("   ⚫ Unable to determine health status")
            
            # Recommendations
            output.append("\n🎯 Performance Recommendations:")
            output.append("1. Monitor rate limit headers")
            output.append("2. Implement request caching")
            output.append("3. Use batch operations")
            output.append("4. Optimize polling frequencies")
            output.append("5. Set up error alerting")
            
            # Quick stats
            output.append("\n📈 Quick Stats:")
            output.append("• Rate Limit: 10 req/sec per org")
            output.append("• Burst Limit: 30 requests")
            output.append("• Auth Methods: API Key, OAuth 2.0")
            output.append("• API Version: v1.61.0")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("generate performance dashboard", e)


def api_analytics_help() -> str:
    """
    ❓ Get help with API analytics tools.
    
    Shows available tools and analytics concepts.
    
    Returns:
        Formatted help guide
    """
    return """📊 API Analytics Tools Help
==================================================

Available tools for API usage monitoring:

1. get_organization_api_requests_overview()
   - Overall usage statistics
   - Response code distribution
   - Success/error rates
   - Performance insights

2. get_organization_api_requests_overview_by_admin()
   - Per-admin breakdown
   - Identify heavy users
   - Auth issue tracking
   - Automation detection

3. get_organization_api_requests()
   - Detailed request logs
   - Filtering options
   - Path analysis
   - Error investigation

4. analyze_api_rate_limits()
   - Rate limit status
   - Usage assessment
   - Optimization tips
   - Retry strategies

5. get_api_usage_by_endpoint()
   - Endpoint popularity
   - Method distribution
   - Category analysis
   - Error patterns

6. api_performance_dashboard()
   - Multi-period analysis
   - Health status
   - Quick metrics
   - Recommendations

Key Metrics:
📈 Request Volume
✅ Success Rate
❌ Error Rate
🚦 Rate Limits
⏱️ Response Time
👤 User Activity

Response Codes:
• 2xx - Success
• 400 - Bad Request
• 401 - Unauthorized
• 403 - Forbidden
• 404 - Not Found
• 429 - Rate Limited
• 5xx - Server Error

Rate Limits:
• 10 req/sec standard
• 30 request burst
• Per-organization
• 429 don't count

Best Practices:
• Monitor continuously
• Set up alerts
• Track trends
• Optimize usage
• Plan capacity
• Document patterns

Common Issues:
• Rate limiting
• Auth failures
• Malformed requests
• Server errors
• Timeout issues
• Version conflicts

Optimization:
• Request batching
• Caching strategies
• Webhook usage
• Polling reduction
• Error handling
• Retry logic

Analytics Uses:
• Capacity planning
• Cost optimization
• Error debugging
• User auditing
• Performance tuning
• Security monitoring
"""


def register_api_analytics_tools(app: FastMCP, meraki_client: MerakiClient):
    """Register all API analytics tools with the MCP server."""
    global mcp_app, meraki
    mcp_app = app
    meraki = meraki_client
    
    # Register all tools
    tools = [
        (get_organization_api_requests_overview, "Get API usage overview"),
        (get_organization_api_requests_overview_by_admin, "Get API usage by admin"),
        (get_organization_api_requests, "Get detailed API requests"),
        (analyze_api_rate_limits, "Analyze API rate limit usage"),
        (get_api_usage_by_endpoint, "Get API usage by endpoint"),
        (api_performance_dashboard, "API performance dashboard"),
        (api_analytics_help, "Get help with API analytics"),
    ]
    
    for tool_func, description in tools:
        app.tool(
            name=tool_func.__name__,
            description=description
        )(tool_func)