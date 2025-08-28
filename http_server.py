import os
import hmac
from typing import List, Optional

from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse

from config import SERVER_NAME, SERVER_VERSION

def _split_tokens(env_value: Optional[str]) -> List[str]:
    if not env_value:
        return []
    return [t.strip() for t in env_value.split(",") if t.strip()]

AUTH_TOKENS_ADMIN = _split_tokens(os.getenv("AUTH_TOKENS_ADMIN"))
AUTH_TOKENS_READONLY = _split_tokens(os.getenv("AUTH_TOKENS_READONLY"))

def get_role(request: Request):
    if request.url.path == "/health":
        return "public"
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing Bearer token")
    token = auth.removeprefix("Bearer ").strip()
    for t in AUTH_TOKENS_ADMIN:
        if hmac.compare_digest(token, t):
            return "admin"
    for t in AUTH_TOKENS_READONLY:
        if hmac.compare_digest(token, t):
            return "readonly"
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

api = FastAPI(title=SERVER_NAME, version=SERVER_VERSION)
api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@api.get("/health")
async def health():
    return {"status": "ok", "name": SERVER_NAME, "version": SERVER_VERSION}

@api.get("/sse")
async def sse_stream(role: str = Depends(get_role)):
    async def event_generator():
        yield "event: open\ndata: {}\n\n"
        while True:
            yield "event: ping\ndata: {}\n\n"
            import asyncio
            await asyncio.sleep(15)
    return StreamingResponse(event_generator(), media_type="text/event-stream")

@api.post("/mcp")
async def mcp_endpoint(request: Request, role: str = Depends(get_role)):
    try:
        payload = await request.json()
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid JSON")
    from adapters.mcp_http import handle_request
    result = handle_request(payload, role)
    return JSONResponse(result)

if __name__ == "__main__":
    import uvicorn
    host = os.getenv("SERVER_HOST", "0.0.0.0")
    port = int(os.getenv("SERVER_PORT", "8000"))
    uvicorn.run("http_server:api", host=host, port=port, reload=False)
