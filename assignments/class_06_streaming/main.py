#type: ignore
import asyncio
from openai.types.responses import ResponseTextDeltaEvent
from agents import Agent, Runner, ItemHelpers, function_tool
from config import config, model
import random

@function_tool
def how_many_jokes() -> int:
    return random.randint(1, 10)


agent = Agent(
        name="Joker",
        instructions="First call the `how_many_jokes` tool, then tell that many jokes.",
        tools=[how_many_jokes],
        model=model
    )
async def main():
    try:
        result = Runner.run_streamed(agent, input="Hello", run_config=config)
        async for event in result.stream_events():
            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                print(event.data.delta, end="", flush=True)
                continue
            elif event.type == "agent_updated_stream_event":
                print(f"Agent updated: {event.new_agent.name}\n")
                continue
            elif event.type == "run_item_stream_event":
                if event.item.type == "tool_call_item":
                    print(f"Tool call: {event.item.raw_item.name}\n")
                elif event.item.type == "tool_call_output_item":
                    print(f"-- Tool output: {event.item.output}\n")
                elif event.item.type == "message_output_item":
                    print(f"\n\n-- Message output:\n {ItemHelpers.text_message_output(event.item)}")
                else:
                    pass  # Ignore other event types

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    asyncio.run(main())