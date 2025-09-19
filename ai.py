from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

response = client.responses.create(
    model="gpt-5",
    input="Hey how are you? Tell me in 2 sentences.",
    tools=[
        
    ]
)

print(response)