from typing import Any, Dict

def handle_request(payload: Dict[str, Any], role: str) -> Dict[str, Any]:
    action = payload.get("action")
    if action in {"ping", "info"}:
        return {"ok": True, "action": action}
    return {"ok": False, "error": "Not implemented"}
