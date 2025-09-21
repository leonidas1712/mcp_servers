import sys
import json
import logging

# Configure logging to stderr (never stdout!)
logging.basicConfig(
    stream=sys.stderr,
    level=logging.INFO,
    format="SERVER: [%(levelname)s] %(message)s"
)

def send(msg):
    """Send a JSON-RPC message to stdout."""
    sys.stdout.write(json.dumps(msg) + "\n")
    sys.stdout.flush()

def recv():
    """Read one line from stdin and parse as JSON."""
    line = sys.stdin.readline()
    if not line:
        return None
    return json.loads(line)

def handle_request(req):
    logging.info(f"Received request: {req}")
    
    if req["method"] == "ping":
        return {
            "jsonrpc": "2.0",
            "id": req["id"],
            "result": {},
        }
        
    
    if req["method"] == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req["id"],
            "result": {
                "protocolVersion": "2025-06-18",
                "capabilities": {"tools": {"listChanged": True}},
                "serverInfo": {"name": "SimpleServer", "version": "0.1"},
            },
        }

    elif req["method"] == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req["id"],
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
                        "outputSchema": {
                            "type": "object",
                            "properties": {"result": {"type": "string"}},
                            "required": ["result"],
                        },
                    }
                ]
            },
        }

    elif req["method"] == "tools/call":
        args = req["params"]["arguments"]
        name = args.get("name", "stranger")
        return {
            "jsonrpc": "2.0",
            "id": req["id"],
            "result": {
                "content": [{"type": "text", "text": f"Hello, {name}!"}],
                "structuredContent": {"result": f"Hello, {name}!"},
                "isError": False,
            },
        }
    
    # this is a no-op but client has to send it, a proper implementation would track state so clients can't
    # request before this is done
    elif req["method"] == 'notifications/initialized':
        return None

    else:
        logging.warning(f"Unknown method: {req['method']}")
        return {
            "jsonrpc": "2.0",
            "id": req["id"],
            "error": {"code": -32601, "message": "Method not found"},
        }

if __name__ == "__main__":
    logging.info("Simple MCP server starting up...")
    while True:
        req = recv()
        if req is None:
            break
        resp = handle_request(req)
        if resp:
            send(resp)
