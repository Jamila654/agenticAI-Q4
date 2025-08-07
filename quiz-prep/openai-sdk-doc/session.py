from agents import Agent, Runner, SQLiteSession, ModelSettings
from openai.types.responses import ResponseTextDeltaEvent
import asyncio
from config import config
async def main():
    agent = Agent(
        name="Assistant",
        instructions="You are a helpful assistant.Respond to user queries with accurate and concise information.",
    )
    

    session_id = "conversation_1"
    session = SQLiteSession(session_id=session_id)

    print("The agent will remember previous messages automatically.\nEnter 'exit' to end the conversation.\n")

    while True:
        user_input = input("User: ")
        if user_input.lower() == "exit":
            break
        try:
            result = Runner.run_streamed(agent, input=user_input, session=session, run_config=config)
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
                        # print(f"\n\n-- Message output:\n {ItemHelpers.text_message_output(event.item)}")
                        pass
                    else:
                        pass  # Ignore other event types
        except Exception as e:
            print(f"An error occurred: {e}")

    print()

if __name__ == "__main__":
    asyncio.run(main())