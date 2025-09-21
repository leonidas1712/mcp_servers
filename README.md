# MCP Demonstration Scripts

Code examples for my blog post, [MCP from first principles](https://www.leonidasr.com/posts/mcp-from-first-principles)

These scripts demonstrate MCP (Model Context Protocol) implementation from scratch, progressing from basic function calling to full MCP client-server communication.

## Script Overview

- **function_calling.py** - Baseline OpenAI function calling without MCP
- **fastmcp_server.py** - MCP server using FastMCP library
- **fastmcp_client.py** - MCP client using FastMCP library
- **simple_client.py** - Raw JSON-RPC client communicating with FastMCP server
- **simple_server.py** - Raw JSON-RPC server for FastMCP client to connect to
- **mcp_with_ai.py** - Integration of MCP tools with LLM function calling
- **http_mcp_server.py** - HTTP transport MCP server using FastAPI

## Running the Examples

Run these examples in order following the blog article:

## Plain Function Calling
```bash
uv run function_calling.py
```

## FastMCP Examples
```bash
# Run FastMCP client - change the server to run by changing the path given to Client
uv run fastmcp_client.py

# Run FastMCP server (STDIO)
uv run fastmcp_server.py
```

## Raw JSON-RPC Examples
```bash
# Run raw client talking to FastMCP server
uv run simple_client.py

# Run raw server (which FastMCP client can connect to)
uv run simple_server.py
```

## MCP + LLM Integration
```bash
uv run mcp_with_ai.py
```

## HTTP Transport Example
```bash
uv run http_mcp_server.py
```

Runs on port 8000. Change client accordingly:

```python
client = Client("http://127.0.0.1:8000/mcp")
```
