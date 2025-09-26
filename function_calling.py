import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

openai_client = OpenAI()

# --- Define tools like normal function calling ---
def greet(name: str) -> str:
    """Greet someone by name."""
    return f"Hi there {name}! This is an MCP greeting."

def calculate(expression: str) -> str:
    """Evaluate a math expression."""
    try:
        # Warning: eval() is unsafe in production - use ast.literal_eval or a proper parser
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error: {e}"

# Map of available tools
TOOLS = {
    "greet": greet,
    "calculate": calculate,
}

# Define tool call schema for the model to work with, which we map back to our functions if the model calls tools
openai_tools = [
    {
        "type": "function",
        "name": "greet",
        "description": greet.__doc__,
        "parameters": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "The name of the person to greet"},
            },
            "required": ["name"],
        },
    },
    {
        "type": "function",
        "name": "calculate",
        "description": calculate.__doc__,
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {"type": "string", "description": "Math expression to evaluate"},
            },
            "required": ["expression"],
        },
    },
]

# --- Run one round of query, tool call, tool result, response ---
input_list = [
    {"role": "user", "content": "Say hi to John, and also calculate and say the result of (800+256)*287"}
]

# Step 1: Send query to LLM
response = openai_client.responses.create(
    model="gpt-4.1",
    input=input_list,
    tools=openai_tools,
)

# Add model's tool calls back to the input before we add tool results
input_list += response.output

# Step 2: Check if model wants to call a tool
for item in response.output:
    if item.type == "function_call":
        func_name = item.name
        args = json.loads(item.arguments)
        
        print(f"Model is calling tool: {func_name}, with args: {args}")

        if func_name in TOOLS:
            tool_result = TOOLS[func_name](**args)
            
            print(f"Result of tool {func_name}: {tool_result}")
            
            # Step 3: Add tool output back to input, to send to LLM
            input_list.append({
                "type": "function_call_output",
                "call_id": item.call_id,
                "output": tool_result,
            })
            
# Print final input list to show the full flow 
print("\nFinal input list:")
for item in input_list:
    print(item)

# Step 4: Get final natural-language answer
final = openai_client.responses.create(
    model="gpt-4.1",
    input=input_list,
    tools=openai_tools,
)

print(f"\nFinal model output: {final.output_text}")