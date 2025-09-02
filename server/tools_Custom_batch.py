"""
Custom Batch operations tools for Cisco Meraki MCP server.

This module delegates to the SDK batch tools to avoid duplication.
The actual batch operations are implemented in tools_SDK_batch.py.
"""

from .tools_SDK_batch import register_batch_tools

# Global references to be set by register function
app = None
meraki_client = None

def register_custom_batch_tools(mcp_app, meraki):
    """
    Register custom batch tools with the MCP server.
    
    This function delegates to the SDK batch tools to avoid duplication.
    All batch operations are handled by the official SDK implementation.
    
    Args:
        mcp_app: MCP server instance
        meraki: Meraki client instance
    """
    # Delegate to SDK batch tools instead of duplicating them
    # This prevents the "Tool already exists" warnings
    pass  # SDK batch tools are already registered in main.py
