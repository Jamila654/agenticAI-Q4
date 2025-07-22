#type: ignore
from agents import Runner, Agent, ItemHelpers
from context import UserSessionContext
from openai.types.responses import ResponseTextDeltaEvent
import json


async def stream_conversation(agent: Agent[UserSessionContext], user_input: str, context: UserSessionContext, runner_hooks=None):
    """Stream conversation with real-time output using Runner.run_streamed."""
    try:
        result = Runner.run_streamed(
            starting_agent=agent,
            input=user_input,
            context=context,
            hooks=runner_hooks  # Pass runner hooks here
        )
        
        print("🔄 Starting conversation stream...\n", flush=True)
        
        async for event in result.stream_events():
            # Core streaming output: print incremental text deltas
            if event.type == "raw_response_event":
                # if hasattr(event, "data") and isinstance(event.data, ResponseTextDeltaEvent):
                #     if hasattr(event.data, 'delta') and event.data.delta:
                #         print(event.data.delta, end="", flush=True)
                pass
            elif event.type == "run_item_stream_event":
                if hasattr(event, "item") and event.item:
                    if event.item.type == "tool_call_item":
                        tool_name = getattr(event.item.raw_item, "name", "Unknown Tool")
                        print(f"Tool was called: {tool_name}")
                    elif event.item.type == "message_output_item":
                        text_output = ItemHelpers.text_message_output(event.item)
                        print(f"Message output:\n{text_output}")
                    else:
                        # For other item types, optionally handle or skip
                        pass
            # Agent handoff
            elif event.type == "agent_updated_stream_event":
                if hasattr(event, "data") and hasattr(event.data, "name"):
                    print(f"\n🤝 Handing off to {event.data.name}...", flush=True)
        
        print("\n\n🔚 Conversation stream ended.", flush=True)
        
    except Exception as e:
        print(f"\n❌ Error during streaming: {str(e)}", flush=True)
        print(f"Error type: {type(e).__name__}", flush=True)
        import traceback
        traceback.print_exc()
        print("Please try rephrasing your question.", flush=True)
    
  


