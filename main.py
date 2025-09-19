from fastmcp import FastMCP

mcp = FastMCP("My MCP Server")

@mcp.tool
def greet(name: str) -> str:
    """Greet someone by name."""
    return f"Hello, {name}! It's an awesome day to be an ML Engineer, don't you think?"

@mcp.tool
def calculate(expression: str) -> int | float:
    """Evaluate a mathematical expression."""
    return eval(expression)

if __name__ == "__main__":
    mcp.run()