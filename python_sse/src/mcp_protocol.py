#!/usr/bin/env python3
"""
MCP Protocol Handler for SSE/HTTP transport
Implements the Model Context Protocol specification
"""

import json
import logging
from typing import Dict, Any, List, Optional
import inspect

logger = logging.getLogger(__name__)

class MCPHandler:
    """Handles MCP protocol messages"""
    
    def __init__(self, tools: Dict[str, Any], metadata: Dict[str, Any]):
        self.tools = tools
        self.metadata = metadata
        
    async def handle_message(self, message: Dict[str, Any], user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process an MCP message and return response"""
        method = message.get("method", "")
        msg_id = message.get("id")
        
        # Handle different MCP methods
        if method == "initialize":
            return await self._handle_initialize(msg_id, message.get("params", {}))
        elif method == "tools/list":
            return await self._handle_tools_list(msg_id, user_data)
        elif method == "tools/call":
            return await self._handle_tool_call(msg_id, message.get("params", {}), user_data)
        else:
            return self._error_response(msg_id, -32601, f"Method not found: {method}")
    
    async def _handle_initialize(self, msg_id: Any, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle initialization request"""
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "protocolVersion": "2025-03-26",
                "serverInfo": {
                    "name": "cisco-meraki-mcp-server",
                    "version": "2.0.0"
                },
                "capabilities": {
                    "tools": {},
                    "resources": {}
                }
            }
        }
    
    async def _handle_tools_list(self, msg_id: Any, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle tools/list request"""
        tools_list = []
        
        # Dangerous tools that require privileges
        dangerous_tools = [
            "reboot_device", "confirm_reboot_device",
            "reboot_network_sm_devices", "confirm_reboot_network_sm_devices",
            "delete_organization", "delete_network",
            "delete_organization_policy_object"
        ]
        
        for tool_name in sorted(self.tools.keys()):
            # Skip dangerous tools for non-privileged users
            if tool_name in dangerous_tools and not user_data.get("is_privileged", False):
                continue
            
            metadata = self.metadata.get(tool_name, {})
            
            # Build input schema from parameters
            input_schema = {
                "type": "object",
                "properties": {},
                "required": []
            }
            
            for param in metadata.get("parameters", []):
                param_name = param["name"]
                param_type = param.get("type", "string")
                
                # Map Python types to JSON Schema types
                json_type = "string"
                if param_type in ["int", "integer"]:
                    json_type = "integer"
                elif param_type in ["bool", "boolean"]:
                    json_type = "boolean"
                elif param_type in ["float", "number"]:
                    json_type = "number"
                elif param_type in ["list", "List"]:
                    json_type = "array"
                elif param_type in ["dict", "Dict"]:
                    json_type = "object"
                
                input_schema["properties"][param_name] = {
                    "type": json_type,
                    "description": f"{param_name} parameter"
                }
                
                if param.get("required", True):
                    input_schema["required"].append(param_name)
            
            tools_list.append({
                "name": tool_name,
                "description": metadata.get("description", f"Execute {tool_name}"),
                "inputSchema": input_schema
            })
        
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "tools": tools_list
            }
        }
    
    async def _handle_tool_call(self, msg_id: Any, params: Dict[str, Any], user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle tools/call request"""
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        if not tool_name:
            return self._error_response(msg_id, -32602, "Missing tool name")
        
        if tool_name not in self.tools:
            return self._error_response(msg_id, -32602, f"Unknown tool: {tool_name}")
        
        # Check privileges for dangerous operations
        dangerous_tools = [
            "reboot_device", "confirm_reboot_device",
            "reboot_network_sm_devices", "confirm_reboot_network_sm_devices",
            "delete_organization", "delete_network",
            "delete_organization_policy_object"
        ]
        
        if tool_name in dangerous_tools and not user_data.get("is_privileged", False):
            return self._error_response(msg_id, -32603, "Permission denied: privileged operation")
        
        try:
            # Execute the tool
            tool_func = self.tools[tool_name]
            
            # Execute with or without arguments
            if arguments:
                result = await tool_func(**arguments)
            else:
                result = await tool_func()
            
            # Format result for MCP protocol
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": str(result)
                        }
                    ]
                }
            }
            
        except TypeError as e:
            # Parameter mismatch
            return self._error_response(msg_id, -32602, f"Invalid parameters: {str(e)}")
        except Exception as e:
            # General error
            logger.error(f"Error executing tool {tool_name}: {e}")
            return self._error_response(msg_id, -32603, f"Tool execution error: {str(e)}")
    
    def _error_response(self, msg_id: Any, code: int, message: str) -> Dict[str, Any]:
        """Create an error response"""
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "error": {
                "code": code,
                "message": message
            }
        }