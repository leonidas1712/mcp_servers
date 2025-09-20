from openai import OpenAI
import json
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

tools = [
    {
        "type": "function",
        "name": "get_weather",
        "description": "Get the current weather in a city",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string"}
            },
            "required": ["city"]
        }
    }
]

# Step 1: Ask a question
messages = [{"role": "user", "content": "What’s the weather in Paris?"}]
response = client.responses.create(
    model="gpt-4.1",
    input=messages,
    tools=tools
)

# Step 2: Check if the model requested a tool call
for item in response.output:
    if item.type == "function_call":
        args = json.loads(item.arguments)
        # Fake tool execution
        result = {"result": f"sunny and 25°C in {args['city']}"}
        messages.append(item)
        messages.append({"type": "function_call_output", "call_id": item.call_id, "output": json.dumps(result)})

# Step 3: Send tool output back to the model
final = client.responses.create(
    model="gpt-4.1",
    input=messages,
    tools=tools,
)

print(final.output_text)
