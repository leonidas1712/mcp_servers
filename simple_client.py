import subprocess
import json
import logging
import sys

# Configure logging: goes to stderr, prefixed with CLIENT:
logging.basicConfig(
    stream=sys.stderr,
    level=logging.INFO,
    format="CLIENT: [%(levelname)s] %(message)s"
)

proc = subprocess.Popen(
    # ["uv", "run", "simple_server.py"],
    ["uv", "run", "./simple_server"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    text=True
)

def send_msg(msg, label, get_stdout=True):
    global proc
    """Send a JSON-RPC message and optionally read one line of response."""
    if label:
        logging.info(label)

    json_data = json.dumps(msg)
    logging.info(f"Sending -> {json_data}")
    
    if proc.stdin and proc.stdout:
        proc.stdin.write(json_data + "\n")
        proc.stdin.flush()
        
        if get_stdout:
            line = proc.stdout.readline().strip()
            logging.info(f"Received <- {line}")


# ---- Step 1: initialize ----
init_msg = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
        "protocolVersion": "2025-06-18",
        "capabilities": {"tools": {}},
        "clientInfo": {"name": "raw-client", "version": "0.1"}
    }
}
send_msg(init_msg, "Initialize")

# ---- Step 2: send initialized notification ----
initialized_msg = {
    "jsonrpc": "2.0",
    "method": "notifications/initialized"
}
send_msg(initialized_msg, "Sending notification for initialized", False)

# ---- Step 3: list tools ----
tools_list_msg = {
    "jsonrpc": "2.0",
    "id": 2,
    "method": "tools/list"
}
send_msg(tools_list_msg, "List tools")

# ---- Step 4: call greet ----
call_greet = {
    "jsonrpc": "2.0",
    "id": 3,
    "method": "tools/call",
    "params": {
        "name": "greet",
        "arguments": {"name": "Leo"}
    }
}
send_msg(call_greet, "Call greet response", True)

