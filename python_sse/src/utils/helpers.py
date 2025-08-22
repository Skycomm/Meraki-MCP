"""
Helper functions for the Cisco Meraki MCP Server.
"""

import json
import os
import time
import hashlib
from datetime import datetime
from typing import Dict, List, Any, Optional, Union
import mcp.types as types

def format_resource_uri(resource_type: str, resource_id: str = "") -> str:
    """
    Format a resource URI for consistent access patterns.
    
    Args:
        resource_type: Type of resource (organizations, networks, devices, etc.)
        resource_id: Optional ID of the specific resource
        
    Returns:
        Formatted URI string
    """
    base_uri = f"meraki://{resource_type}"
    if resource_id:
        return f"{base_uri}/{resource_id}"
    return base_uri

def create_resource(uri: str, name: str, description: Optional[str] = None, 
                   mime_type: str = "application/json") -> types.Resource:
    """
    Create an MCP resource object.
    
    Args:
        uri: Resource URI
        name: Human-readable name
        description: Optional description
        mime_type: MIME type for the resource
        
    Returns:
        MCP Resource object
    """
    return types.Resource(
        uri=uri,
        name=name,
        description=description,
        mimeType=mime_type
    )

def create_content(uri: str, data: Union[Dict, List], 
                   mime_type: str = "application/json") -> types.ResourceContents:
    """
    Create an MCP resource content object.
    
    Args:
        uri: Resource URI
        data: Resource data
        mime_type: MIME type for the resource
        
    Returns:
        MCP ResourceContents object
    """
    return types.ResourceContents(
        uri=uri,
        mimeType=mime_type,
        text=json.dumps(data, indent=2)
    )

def format_error_message(error: Exception) -> str:
    """
    Format an exception into a user-friendly error message.
    
    Args:
        error: The exception to format
        
    Returns:
        Formatted error message
    """
    if hasattr(error, 'message'):
        return f"Error: {error.message}"
    return f"Error: {str(error)}"

def require_confirmation(operation_type: str, resource_type: str, 
                        resource_name: str, resource_id: Optional[str] = None) -> bool:
    """
    Require user confirmation for destructive operations.
    
    Args:
        operation_type: Type of operation (delete, remove, reboot, etc.)
        resource_type: Type of resource (network, organization, device, etc.)
        resource_name: Name of the resource
        resource_id: Optional ID of the resource
        
    Returns:
        True if user confirmed, False otherwise
    """
    # Check if in read-only mode
    if os.getenv("MCP_READ_ONLY_MODE", "false").lower() == "true":
        print("\n❌ Operation blocked: Server is in READ-ONLY mode")
        return False
    
    # Check if confirmations are disabled (not recommended)
    if os.getenv("MCP_REQUIRE_CONFIRMATIONS", "true").lower() == "false":
        return True
    
    # Determine risk level
    DESTRUCTIVE_OPS = ["delete", "remove", "reboot"]
    risk_level = "🚨 HIGH RISK" if operation_type in DESTRUCTIVE_OPS else "⚠️  MEDIUM RISK"
    
    print(f"\n{'='*60}")
    print(f"{risk_level} OPERATION - CONFIRMATION REQUIRED")
    print(f"{'='*60}")
    print(f"Operation: {operation_type.upper()} {resource_type.upper()}")
    print(f"Target: {resource_name}")
    if resource_id:
        print(f"ID: {resource_id}")
    print(f"\nThis action cannot be undone!")
    print(f"\nTo confirm, type exactly: {operation_type.upper()}")
    print("Or press Enter to cancel")
    
    response = input("> ").strip()
    confirmed = response == operation_type.upper()
    
    # Log the attempt
    log_operation(operation_type, resource_type, resource_name, resource_id, confirmed)
    
    if confirmed and operation_type in DESTRUCTIVE_OPS:
        # Add countdown for destructive operations
        print("\nExecuting in:")
        for i in range(3, 0, -1):
            print(f"  {i}...")
            time.sleep(1)
    
    return confirmed

def log_operation(operation: str, resource_type: str, resource_name: str, 
                  resource_id: Optional[str], confirmed: bool) -> None:
    """
    Log all operations for audit trail.
    
    Args:
        operation: Operation type
        resource_type: Type of resource
        resource_name: Name of the resource
        resource_id: ID of the resource
        confirmed: Whether the operation was confirmed
    """
    # Check if audit logging is enabled
    if os.getenv("MCP_AUDIT_LOGGING", "true").lower() == "false":
        return
        
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "operation": operation,
        "resource_type": resource_type,
        "resource_name": resource_name,
        "resource_id": resource_id,
        "confirmed": confirmed,
        "user": os.getenv("USER", "unknown"),
        "api_key_hash": hashlib.sha256(
            os.getenv("MERAKI_API_KEY", "").encode()
        ).hexdigest()[:8]
    }
    
    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)
    
    # Write to audit log
    try:
        with open("logs/meraki_mcp_audit.log", "a") as f:
            f.write(json.dumps(log_entry) + "\n")
    except Exception as e:
        print(f"Warning: Failed to write audit log: {e}")
