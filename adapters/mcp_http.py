from typing import Any, Dict, List
from server.main import app
from utils.helpers import get_read_only_message, format_error_message

WRITE_PREFIXES: List[str] = [
    "update_", "delete_", "create_", "remove_", "reboot_", "swap_", "toggle_", "add_", "set_", "enable_", "disable_",
]

def _is_destructive(tool_name: str) -> bool:
    lname = tool_name.lower()
    return any(lname.startswith(p) for p in WRITE_PREFIXES)

async def handle_request(payload: Dict[str, Any], role: str) -> Dict[str, Any]:
    action = payload.get("action")
    if not action:
        return {"ok": False, "error": "Missing 'action'"}

    if action == "ping":
        return {"ok": True, "action": "ping"}

    if action == "list_tools":
        try:
            tools = await app.list_tools()
            return {"ok": True, "tools": [getattr(t, "name", str(t)) for t in tools]}
        except Exception as e:
            return {"ok": False, "error": format_error_message(e)}

    if action == "call_tool":
        name = payload.get("name")
        args = payload.get("args") or {}
        if not name:
            return {"ok": False, "error": "Missing 'name' for call_tool"}
        if role != "admin" and _is_destructive(name):
            return {
                "ok": False,
                "readOnly": True,
                "message": get_read_only_message("modify", "resource", name),
            }
        try:
            result = await app.call_tool(name, args)
            return {"ok": True, "result": result}
        except Exception as e:
            return {"ok": False, "error": format_error_message(e)}

    if action == "list_resources":
        try:
            resources = await app.list_resources()
            out = []
            for r in resources:
                out.append({
                    "uri": getattr(r, "uri", None),
                    "name": getattr(r, "name", None),
                    "description": getattr(r, "description", None),
                    "mimeType": getattr(r, "mimeType", None),
                })
            return {"ok": True, "resources": out}
        except Exception as e:
            return {"ok": False, "error": format_error_message(e)}

    if action == "read_resource":
        uri = payload.get("uri")
        if not uri:
            return {"ok": False, "error": "Missing 'uri' for read_resource"}
        try:
            contents = await app.read_resource(uri)
            out = []
            for c in contents:
                out.append({
                    "uri": getattr(c, "uri", None),
                    "mimeType": getattr(c, "mimeType", None),
                    "text": getattr(c, "text", None),
                })
            return {"ok": True, "contents": out}
        except Exception as e:
            return {"ok": False, "error": format_error_message(e)}

    return {"ok": False, "error": f"Unsupported action '{action}'"}
