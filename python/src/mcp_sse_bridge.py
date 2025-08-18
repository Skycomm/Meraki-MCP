#!/usr/bin/env python3
"""
MCP SSE Bridge - Handles MCP protocol over Server-Sent Events
"""

import json
import asyncio
import logging
from typing import Dict, Any, Optional
import uuid

logger = logging.getLogger(__name__)

class MCPSSEHandler:
    """Handles MCP protocol messages over SSE"""
    
    def __init__(self, tools: Dict[str, Any]):
        self.tools = tools
        self.session_id = str(uuid.uuid4())
        
    async def handle_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Process an MCP message and return response"""
        method = message.get("method", "")
        msg_id = message.get("id")
        
        # Handle initialization
        if method == "initialize":
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "protocolVersion": "0.1.0",
                    "serverInfo": {
                        "name": "meraki-hybrid",
                        "version": "1.0.0"
                    },
                    "capabilities": {
                        "tools": {},
                        "resources": {}
                    }
                }
            }
        
        # Handle list tools
        elif method == "tools/list":
            tools_list = []
            for name, func in self.tools.items():
                # Get function docstring and signature
                import inspect
                sig = inspect.signature(func)
                
                tool_info = {
                    "name": name,
                    "description": func.__doc__ or f"Execute {name}",
                    "inputSchema": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                }
                
                # Build parameters schema
                for param_name, param in sig.parameters.items():
                    if param_name == 'self':
                        continue
                    
                    # Simple type mapping
                    param_type = "string"
                    if param.annotation == int:
                        param_type = "integer"
                    elif param.annotation == bool:
                        param_type = "boolean"
                    
                    tool_info["inputSchema"]["properties"][param_name] = {
                        "type": param_type
                    }
                    
                    if param.default == param.empty:
                        tool_info["inputSchema"]["required"].append(param_name)
                
                tools_list.append(tool_info)
            
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "tools": tools_list
                }
            }
        
        # Handle tool execution
        elif method == "tools/call":
            params = message.get("params", {})
            tool_name = params.get("name")
            arguments = params.get("arguments", {})
            
            if tool_name not in self.tools:
                return {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "error": {
                        "code": -32601,
                        "message": f"Tool not found: {tool_name}"
                    }
                }
            
            try:
                # Execute tool
                tool_func = self.tools[tool_name]
                if arguments:
                    result = await tool_func(**arguments)
                else:
                    result = await tool_func()
                
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
            except Exception as e:
                logger.error(f"Error executing tool {tool_name}: {e}")
                return {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "error": {
                        "code": -32603,
                        "message": f"Tool execution error: {str(e)}"
                    }
                }
        
        # Unknown method
        else:
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "error": {
                    "code": -32601,
                    "message": f"Method not found: {method}"
                }
            }