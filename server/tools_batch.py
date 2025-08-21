"""
Action Batch Tools for Cisco Meraki MCP Server
Execute bulk configuration changes atomically
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


def create_organization_action_batch(
    org_id: str,
    actions: List[Dict[str, Any]],
    confirmed: bool = False,
    synchronous: bool = False,
    callback_url: Optional[str] = None,
    callback_shared_secret: Optional[str] = None
) -> str:
    """
    ➕ Create an action batch for bulk configuration.
    
    Execute multiple configuration changes atomically.
    All actions succeed or all fail - no partial execution.
    
    Args:
        org_id: Organization ID
        actions: List of action dictionaries with resource, operation, body
        confirmed: Execute immediately if True, otherwise create as draft
        synchronous: Run synchronously (max 20 actions) or async (max 100)
        callback_url: Webhook URL for completion notification
        callback_shared_secret: Secret for webhook verification
    
    Returns:
        Action batch details and status
    """
    try:
        with safe_api_call("create action batch"):
            # Build the batch request
            batch_request = {
                "confirmed": confirmed,
                "synchronous": synchronous,
                "actions": actions
            }
            
            # Add callback if provided
            if callback_url:
                batch_request["callback"] = {
                    "url": callback_url
                }
                if callback_shared_secret:
                    batch_request["callback"]["sharedSecret"] = callback_shared_secret
            
            # Create the batch
            batch = meraki.dashboard.organizations.createOrganizationActionBatch(
                org_id,
                **batch_request
            )
            
            output = ["➕ Action Batch Created", "=" * 50, ""]
            output.append(f"Batch ID: {batch.get('id', 'Unknown')}")
            output.append(f"Organization: {org_id}")
            output.append("")
            
            # Status information
            status = batch.get('status', {})
            if status:
                output.append("📊 Status:")
                output.append(f"   Completed: {'✅' if status.get('completed') else '⏳'}")
                output.append(f"   Failed: {'❌' if status.get('failed') else '✅'}")
                
                # Errors if any
                errors = status.get('errors', [])
                if errors:
                    output.append("\n❌ Errors:")
                    for error in errors:
                        output.append(f"   • {error}")
                
                # Created resources
                created = status.get('createdResources', [])
                if created:
                    output.append(f"\n✅ Created Resources: {len(created)}")
                    for resource in created[:5]:  # Show first 5
                        output.append(f"   • {resource.get('uri', 'Unknown')}")
                        output.append(f"     ID: {resource.get('id', 'N/A')}")
            
            # Actions summary
            output.append(f"\n📋 Actions: {len(actions)}")
            output.append(f"Mode: {'Synchronous' if synchronous else 'Asynchronous'}")
            output.append(f"Confirmed: {'Yes' if confirmed else 'No (Draft)'}")
            
            if callback_url:
                output.append(f"\n🔔 Webhook: {callback_url}")
            
            # Show action details
            output.append("\n📝 Action Details:")
            for i, action in enumerate(actions[:5], 1):  # Show first 5
                output.append(f"\n{i}. {action.get('operation', 'Unknown').upper()}")
                output.append(f"   Resource: {action.get('resource', 'Unknown')}")
                if action.get('body'):
                    output.append(f"   Body: {json.dumps(action['body'], indent=6)[:100]}...")
            
            if len(actions) > 5:
                output.append(f"\n... and {len(actions) - 5} more actions")
            
            # Important notes
            output.append("\n💡 Important:")
            output.append("• Batches run atomically - all or nothing")
            output.append("• Synchronous: Max 20 actions")
            output.append("• Asynchronous: Max 100 actions")
            output.append("• Max 5 concurrent batches")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("create action batch", e)


def get_organization_action_batches(
    org_id: str,
    status: Optional[str] = None
) -> str:
    """
    📋 List all action batches for an organization.
    
    Shows current and historical action batches with their status.
    
    Args:
        org_id: Organization ID
        status: Filter by status (completed, failed, pending)
    
    Returns:
        List of action batches
    """
    try:
        with safe_api_call("get action batches"):
            params = {}
            if status:
                params['status'] = status
            
            batches = meraki.dashboard.organizations.getOrganizationActionBatches(
                org_id,
                **params
            )
            
            output = ["📋 Action Batches", "=" * 50, ""]
            
            if not batches:
                output.append("No action batches found")
                return "\n".join(output)
            
            # Group by status
            by_status = {
                'pending': [],
                'completed': [],
                'failed': []
            }
            
            for batch in batches:
                batch_status = batch.get('status', {})
                if batch_status.get('failed'):
                    by_status['failed'].append(batch)
                elif batch_status.get('completed'):
                    by_status['completed'].append(batch)
                else:
                    by_status['pending'].append(batch)
            
            # Summary
            output.append(f"Total Batches: {len(batches)}")
            output.append(f"   ⏳ Pending: {len(by_status['pending'])}")
            output.append(f"   ✅ Completed: {len(by_status['completed'])}")
            output.append(f"   ❌ Failed: {len(by_status['failed'])}")
            output.append("")
            
            # Show recent batches by status
            for status_type, status_batches in by_status.items():
                if status_batches:
                    icon = {'pending': '⏳', 'completed': '✅', 'failed': '❌'}[status_type]
                    output.append(f"{icon} {status_type.capitalize()} Batches:")
                    
                    for batch in status_batches[:3]:  # Show first 3 of each
                        batch_id = batch.get('id', 'Unknown')
                        confirmed = batch.get('confirmed', False)
                        sync = batch.get('synchronous', False)
                        actions_count = len(batch.get('actions', []))
                        
                        output.append(f"\n   Batch ID: {batch_id}")
                        output.append(f"   Actions: {actions_count}")
                        output.append(f"   Type: {'Sync' if sync else 'Async'}")
                        output.append(f"   Confirmed: {'Yes' if confirmed else 'Draft'}")
                        
                        # Show errors for failed batches
                        if status_type == 'failed':
                            errors = batch.get('status', {}).get('errors', [])
                            if errors:
                                output.append(f"   Error: {errors[0][:80]}...")
                    
                    if len(status_batches) > 3:
                        output.append(f"\n   ... and {len(status_batches) - 3} more")
                    
                    output.append("")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("get action batches", e)


def get_organization_action_batch(
    org_id: str,
    action_batch_id: str
) -> str:
    """
    🔍 Get details of a specific action batch.
    
    Shows full details including all actions and their results.
    
    Args:
        org_id: Organization ID
        action_batch_id: Action batch ID
    
    Returns:
        Detailed batch information
    """
    try:
        with safe_api_call("get action batch"):
            batch = meraki.dashboard.organizations.getOrganizationActionBatch(
                org_id,
                action_batch_id
            )
            
            output = ["🔍 Action Batch Details", "=" * 50, ""]
            output.append(f"Batch ID: {action_batch_id}")
            output.append(f"Organization: {org_id}")
            output.append("")
            
            # Basic info
            output.append("📊 Configuration:")
            output.append(f"   Confirmed: {'Yes' if batch.get('confirmed') else 'No'}")
            output.append(f"   Synchronous: {'Yes' if batch.get('synchronous') else 'No'}")
            
            # Status details
            status = batch.get('status', {})
            if status:
                output.append("\n📈 Status:")
                completed = status.get('completed', False)
                failed = status.get('failed', False)
                
                if failed:
                    output.append("   Result: ❌ FAILED")
                elif completed:
                    output.append("   Result: ✅ COMPLETED")
                else:
                    output.append("   Result: ⏳ PENDING")
                
                # Errors
                errors = status.get('errors', [])
                if errors:
                    output.append("\n❌ Errors:")
                    for i, error in enumerate(errors, 1):
                        output.append(f"   {i}. {error}")
                
                # Created resources
                created = status.get('createdResources', [])
                if created:
                    output.append(f"\n✅ Created Resources ({len(created)}):")
                    for resource in created[:10]:  # Show first 10
                        output.append(f"   • {resource.get('uri', 'Unknown')}")
                        output.append(f"     ID: {resource.get('id', 'N/A')}")
                    
                    if len(created) > 10:
                        output.append(f"   ... and {len(created) - 10} more")
            
            # Actions
            actions = batch.get('actions', [])
            if actions:
                output.append(f"\n📝 Actions ({len(actions)}):")
                for i, action in enumerate(actions[:10], 1):  # Show first 10
                    operation = action.get('operation', 'Unknown')
                    resource = action.get('resource', 'Unknown')
                    
                    output.append(f"\n   {i}. {operation.upper()} {resource}")
                    
                    # Show body preview
                    body = action.get('body')
                    if body:
                        body_str = json.dumps(body, indent=6)
                        if len(body_str) > 200:
                            body_str = body_str[:200] + "..."
                        output.append(f"      Body: {body_str}")
                
                if len(actions) > 10:
                    output.append(f"\n   ... and {len(actions) - 10} more actions")
            
            # Callback info
            callback = batch.get('callback')
            if callback:
                output.append("\n🔔 Webhook Callback:")
                output.append(f"   URL: {callback.get('url', 'N/A')}")
                output.append(f"   ID: {callback.get('id', 'N/A')}")
                output.append(f"   Status: {callback.get('status', 'N/A')}")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("get action batch", e)


def update_organization_action_batch(
    org_id: str,
    action_batch_id: str,
    confirmed: bool = True,
    synchronous: Optional[bool] = None
) -> str:
    """
    ✏️ Update an action batch.
    
    Confirm a draft batch or change execution mode.
    
    Args:
        org_id: Organization ID
        action_batch_id: Action batch ID
        confirmed: Set to True to execute the batch
        synchronous: Change sync/async mode
    
    Returns:
        Updated batch information
    """
    try:
        with safe_api_call("update action batch"):
            update_params = {
                "confirmed": confirmed
            }
            
            if synchronous is not None:
                update_params["synchronous"] = synchronous
            
            batch = meraki.dashboard.organizations.updateOrganizationActionBatch(
                org_id,
                action_batch_id,
                **update_params
            )
            
            output = ["✏️ Action Batch Updated", "=" * 50, ""]
            output.append(f"Batch ID: {action_batch_id}")
            output.append("")
            
            # Show what changed
            output.append("📝 Updates Applied:")
            output.append(f"   Confirmed: {'✅ Yes (Executing)' if confirmed else '❌ No (Still Draft)'}")
            
            if synchronous is not None:
                output.append(f"   Mode: {'Synchronous' if synchronous else 'Asynchronous'}")
            
            # Current status
            status = batch.get('status', {})
            if status:
                output.append("\n📊 Current Status:")
                if status.get('failed'):
                    output.append("   ❌ FAILED")
                elif status.get('completed'):
                    output.append("   ✅ COMPLETED")
                else:
                    output.append("   ⏳ PENDING/EXECUTING")
            
            # Actions count
            actions_count = len(batch.get('actions', []))
            output.append(f"\n📋 Total Actions: {actions_count}")
            
            if confirmed and not status.get('completed'):
                output.append("\n⏳ Batch is now executing...")
                output.append("   Use get_organization_action_batch() to check status")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("update action batch", e)


def delete_organization_action_batch(
    org_id: str,
    action_batch_id: str
) -> str:
    """
    🗑️ Delete an action batch.
    
    Only pending/unconfirmed batches can be deleted.
    
    Args:
        org_id: Organization ID
        action_batch_id: Action batch ID
    
    Returns:
        Deletion confirmation
    """
    try:
        with safe_api_call("delete action batch"):
            meraki.dashboard.organizations.deleteOrganizationActionBatch(
                org_id,
                action_batch_id
            )
            
            output = ["🗑️ Action Batch Deleted", "=" * 50, ""]
            output.append(f"Batch ID: {action_batch_id}")
            output.append(f"Organization: {org_id}")
            output.append("")
            output.append("✅ Batch successfully deleted")
            output.append("")
            output.append("💡 Note: Only unconfirmed batches can be deleted")
            
            return "\n".join(output)
            
    except Exception as e:
        return format_error("delete action batch", e)


def create_batch_example() -> str:
    """
    📚 Show example action batch payloads.
    
    Provides templates for common batch operations.
    
    Returns:
        Example batch configurations
    """
    output = ["📚 Action Batch Examples", "=" * 50, ""]
    
    output.append("1️⃣ Create VLAN and Configure Switches:")
    output.append("""
actions = [
    {
        "resource": "/networks/{network_id}/appliance/vlans",
        "operation": "create",
        "body": {
            "id": 100,
            "name": "Guest-VLAN",
            "subnet": "192.168.100.0/24",
            "applianceIp": "192.168.100.1"
        }
    },
    {
        "resource": "/devices/{switch_serial}/switch/ports/1",
        "operation": "update",
        "body": {
            "name": "Guest Access",
            "type": "access",
            "vlan": 100,
            "enabled": true
        }
    }
]
""")
    
    output.append("\n2️⃣ Bulk Update Switch Ports:")
    output.append("""
actions = []
for port in range(1, 25):
    actions.append({
        "resource": f"/devices/{switch_serial}/switch/ports/{port}",
        "operation": "update",
        "body": {
            "type": "trunk",
            "allowedVlans": "1,100,200",
            "nativeVlan": 1
        }
    })
""")
    
    output.append("\n3️⃣ Create Network and Add Devices:")
    output.append("""
actions = [
    {
        "resource": "/organizations/{org_id}/networks",
        "operation": "create",
        "body": {
            "name": "New Branch",
            "productTypes": ["appliance", "switch", "wireless"],
            "timeZone": "America/Los_Angeles"
        }
    },
    {
        "resource": "/networks/{network_id}/devices",
        "operation": "claim",
        "body": {
            "serials": ["Q2XX-XXXX-XXXX", "Q2YY-YYYY-YYYY"]
        }
    }
]
""")
    
    output.append("\n💡 Tips:")
    output.append("• Use {network_id}, {device_serial} as placeholders")
    output.append("• Test with confirmed=False first")
    output.append("• Check resource paths in API docs")
    output.append("• Use synchronous=True for immediate feedback")
    output.append("• Group related changes together")
    
    return "\n".join(output)


def batch_help() -> str:
    """
    ❓ Get help with action batch tools.
    
    Shows available tools and best practices.
    
    Returns:
        Formatted help guide
    """
    return """🚀 Action Batch Tools Help
==================================================

Available tools for bulk configuration:

1. create_organization_action_batch()
   - Create new batch with multiple actions
   - Atomic execution (all or nothing)
   - Sync or async execution
   - Optional webhook callbacks

2. get_organization_action_batches()
   - List all batches
   - Filter by status
   - See summary of pending/completed/failed

3. get_organization_action_batch()
   - Detailed batch information
   - View all actions and results
   - Check error details
   - See created resources

4. update_organization_action_batch()
   - Confirm draft batches
   - Change execution mode
   - Start batch execution

5. delete_organization_action_batch()
   - Remove unconfirmed batches
   - Clean up drafts
   - Cannot delete executing batches

6. create_batch_example()
   - Example action payloads
   - Common use cases
   - Best practices

Action Batch Limits:
• Synchronous: Max 20 actions
• Asynchronous: Max 100 actions
• 5 concurrent batches per org
• Atomic execution

Common Operations:
• create: Add new resources
• update: Modify existing
• destroy: Remove resources
• bind: Associate resources
• unbind: Disassociate
• claim: Add devices

Best Practices:
• Test with confirmed=False
• Use meaningful batch descriptions
• Group related changes
• Handle errors gracefully
• Monitor async batches
• Use webhooks for notifications

Error Handling:
• Batches fail atomically
• No partial execution
• Check error messages
• Validate resources exist
• Verify permissions

Use Cases:
• Initial network setup
• Bulk port configuration
• Mass VLAN deployment
• Device provisioning
• Policy rollouts
• Scheduled maintenance
"""


def register_batch_tools(app: FastMCP, meraki_client: MerakiClient):
    """Register all action batch tools with the MCP server."""
    global mcp_app, meraki
    mcp_app = app
    meraki = meraki_client
    
    # Register all tools
    tools = [
        (create_organization_action_batch, "Create action batch for bulk configuration"),
        (get_organization_action_batches, "List all action batches"),
        (get_organization_action_batch, "Get specific batch details"),
        (update_organization_action_batch, "Update/confirm action batch"),
        (delete_organization_action_batch, "Delete unconfirmed batch"),
        (create_batch_example, "Show example batch configurations"),
        (batch_help, "Get help with action batches"),
    ]
    
    for tool_func, description in tools:
        app.tool(
            name=tool_func.__name__,
            description=description
        )(tool_func)