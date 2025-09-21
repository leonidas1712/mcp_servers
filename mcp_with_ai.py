import asyncio, json
from openai import OpenAI
from fastmcp import Client
from dotenv import load_dotenv

load_dotenv()

openai_client = OpenAI()
mcp_client = Client("fastmcp_server.py")  # path to executable for MCP server process

async def main():
    async with mcp_client:
        # fetch tool list from MCP
        mcp_tools = await mcp_client.list_tools()
        
        print("MCP tools:", mcp_tools)
    
        openai_tools = mcp_tools_to_openai(mcp_tools)
        
        print("OpenAI formatted tools:", openai_tools)
        print()
        
        

        # step 1: send user query + tools to LLM
        input_list = [{"role": "user", "content": "Say hi to John, and also calculate and say the result of (800+256)*287"}]
        response = openai_client.responses.create(
            model="gpt-4.1",
            input=input_list, 
            tools=openai_tools
        )
        
        input_list += response.output

        # step 2: check if model wants to call a tool
        for item in response.output:
            if item.type == "function_call":
                
                args = json.loads(item.arguments)
                
                print(f"Model is calling MCP tool: {item.name}, with args: {args}")
                
                # forward to MCP
                mcp_result = await mcp_client.call_tool(item.name, args)
                
                print("MCP tool result:", mcp_result)

                # extract string result
                result_str = (
                    mcp_result.structuredContent.get("result")
                    if hasattr(mcp_result, "structuredContent")
                    else str(mcp_result)
                )

                # step 3: send tool output back to LLM
                input_list.append({
                    "type": "function_call_output",
                    "call_id": item.call_id,
                    "output": json.dumps({"result": result_str}),
                })

        print("\nFinal input list:")
        for item in input_list:
            print(item)
            
        # # step 4: get final natural-language answer
        final = openai_client.responses.create(
            model="gpt-4.1",
            input=input_list,
            tools=openai_tools,
        )
        print("\nFinal model output:",final.output_text)

def mcp_tools_to_openai(tools):
    return [
        {
            "type": "function",
            "name": t.name,
            "description": t.description or "",
            "parameters": t.inputSchema,
        }
        for t in tools
    ]

asyncio.run(main())
