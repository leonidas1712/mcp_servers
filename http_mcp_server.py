from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
import logging
import json

app = FastAPI()

logging.basicConfig(level=logging.INFO, format="SERVER: [%(levelname)s] %(message)s")

PROTOCOL_VERSION = "2025-06-18"

@app.post("/mcp")
async def mcp_endpoint(req: Request):
    body = await req.json()
    logging.info(f"Received request: {body}")

    method = body.get("method")
    req_id = body.get("id")

    if method == "initialize":
        return JSONResponse({
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": PROTOCOL_VERSION,
                "capabilities": {"tools": {"listChanged": True}},
                "serverInfo": {"name": "SimpleHTTPServer", "version": "0.1"},
            }
        })
    elif method == "ping":
        return JSONResponse({
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {},
        })

    elif method == "tools/list":
        return JSONResponse({
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "greet",
                        "description": "Greet someone by name.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {"name": {"type": "string"}},
                            "required": ["name"],
                        },
                    }
                ]
            }
        })

    elif method == "tools/call":
        args = body["params"]["arguments"]
        name = args.get("name", "stranger")
        return JSONResponse({
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "content": [{"type": "text", "text": f"Hello, {name}!"}],
                "isError": False,
            }
        })

    elif method == "notifications/initialized":
        # Notifications don’t expect a response
        return JSONResponse(content=None, status_code=204)

    else:
        logging.warning(f"Unknown method: {method}")
        return JSONResponse({
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {"code": -32601, "message": "Method not found"},
        })


if __name__ == "__main__":
    logging.info("Starting HTTP MCP server...")
    uvicorn.run(app, host="127.0.0.1", port=8000)
