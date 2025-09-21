import asyncio
from fastmcp import Client
import logging
import sys

# Run against SDK server
client = Client("fastmcp_server.py")

# Run against raw server
# client = Client("simple_server.py")

# Run against HTTP server
# client = Client("http://127.0.0.1:8000/mcp")

logging.basicConfig(
    stream=sys.stderr,
    level=logging.INFO,
    format="CLIENT: [%(levelname)s] %(message)s"
)

async def main():
    async with client:
        # Basic server interaction
        res = await client.ping()
        logging.info(f"ping {res}")
                
        # List available operations
        tools = await client.list_tools()
        logging.info(f"Tools: {tools}")
        
        res = await client.call_tool("greet", {"name": "John"})

        if res.content:
            text: str | None = getattr(res.content[0], "text", None)
            if text is not None:
                logging.info(f"Tool call result: {text}")
        
        
        # resources = await client.list_resources()
        # prompts = await client.list_prompts()
        
        # res = await client.call_tool("calculate", {"expression": "(2+5)*10"})
        # print(res.content)
        

asyncio.run(main())