#type: ignore
import asyncio
from agents import Agent, Runner, set_tracing_disabled, ItemHelpers, AsyncOpenAI,OpenAIChatCompletionsModel,function_tool
from dotenv import load_dotenv
import os
import random
import requests

load_dotenv()
set_tracing_disabled(True)  
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = AsyncOpenAI(api_key=GEMINI_API_KEY, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")

@function_tool
def how_many_jokes() -> int:
    random_num = random.randint(1, 10)
    url = f"https://official-joke-api.appspot.com/jokes/random/{random_num}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return "Error: Unable to fetch jokes"


async def main():
    agent = Agent(
        name = "Joker AI",
        instructions="First call the `how_many_jokes` tool, then tell that many jokes. If there are more than 1 joke print line by line.Before telling jokes tell the number or jokes you will tell.",
        model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
        tools=[how_many_jokes]
    )
    result = Runner.run_streamed(agent, "hello")
    print("starting...\n")
    async for event in result.stream_events():
        if event.type == "raw_response_event":
            continue
        elif event.type == "agent_updated_stream_event":
            print(f"Agent updated: {event.new_agent.name}")
            continue
        elif event.type == "run_item_stream_event":
            if event.item.type == "tool_call_item":
                print("-- Tool was called")
            elif event.item.type == "tool_call_output_item":
                print(f"-- Tool output: {event.item.output}")
            elif event.item.type == "message_output_item":
                print(f"-- Message output:\n {ItemHelpers.text_message_output(event.item)}")
            else:
                pass  # Ignore other event types
    print("done")


if __name__ == "__main__":
    asyncio.run(main())
