"""
Helper functions for the Cisco Meraki MCP Server.
"""

import json
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
