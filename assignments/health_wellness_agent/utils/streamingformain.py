#type: ignore
from agents import Runner, Agent
from context import UserSessionContext
from openai.types.responses import ResponseTextDeltaEvent


def get_tool_name_from_item(item) -> str:
    """Extract tool name from stream item, prioritizing raw_item.name."""
    if not item:
        return "Unknown Tool"
    raw_item = None
    if isinstance(item, dict):
        raw_item = item.get('raw_item', None)
    elif hasattr(item, 'raw_item'):
        raw_item = getattr(item, 'raw_item')
    
    if raw_item:
        if isinstance(raw_item, dict) and 'name' in raw_item:
            return raw_item['name']
        elif hasattr(raw_item, 'name'):
            return getattr(raw_item, 'name')
    
    # Fallback to other keys or attributes
    for key in ['tool_name', 'name', 'function_name']:
        if isinstance(item, dict) and key in item and item[key]:
            return item[key]
    for attr in ['tool_name', 'name', 'function_name']:
        if hasattr(item, attr):
            val = getattr(item, attr)
            if val:
                return val
    tool = None
    if isinstance(item, dict):
        tool = item.get('tool', None)
    elif hasattr(item, 'tool'):
        tool = getattr(item, 'tool')
    
    if tool:
        if isinstance(tool, dict):
            for key in ['tool_name', 'name']:
                if key in tool and tool[key]:
                    return tool[key]
        else:
            for attr in ['tool_name', 'name']:
                if hasattr(tool, attr):
                    val = getattr(tool, attr)
                    if val:
                        return val
    
    return "Unknown Tool"

async def stream_conversation(agent: Agent[UserSessionContext], user_input: str, context: UserSessionContext, runner_hooks=None):
    """Stream conversation with real-time output using Runner.run_streamed."""
    try:
        result = Runner.run_streamed(
            starting_agent=agent,
            input=user_input,
            context=context,
            hooks=runner_hooks  # Pass runner hooks here
        )
        
        print("🔄 Starting conversation stream...")
        
        async for event in result.stream_events():
            # print(f"📨 Event type: {event.type}")  # Debug line
            
            if event.type == "raw_response_event":
                if hasattr(event, "data") and isinstance(event.data, ResponseTextDeltaEvent):
                    if hasattr(event.data, 'delta') and event.data.delta:
                        print(event.data.delta, end="", flush=True)
                        
            elif event.type == "run_item_stream_event":
                if hasattr(event, "item") and event.item:
                    if event.item.type == "tool_call_item":
                        tool_name = get_tool_name_from_item(event.item)
                        print(f"\n🔧 Using {tool_name}...", end="", flush=True)
                    elif event.item.type == "tool_call_output_item":
                        print(" Done.", end="", flush=True)
                        
            elif event.type == "agent_updated_stream_event":
                if hasattr(event, "data") and hasattr(event.data, "name"):
                    print(f"\n🤝 Handing off to {event.data.name}...", end="", flush=True)
                    
            elif event.type == "text_delta_event":
                if hasattr(event, "delta"):
                    print(event.delta, end="", flush=True)
                    
            elif event.type in ["tool_start_event", "tool_end_event"]:
                tool_name = "Unknown Tool"
                if hasattr(event, "tool"):
                    tool_name = get_tool_name_from_item(event.tool)
                elif hasattr(event, "item"):
                    tool_name = get_tool_name_from_item(event.item)
                print(f"\n🛠️  Tool event: {event.type} - {tool_name}")
                    
        print()  # New line after streaming
        
    except Exception as e:
        print(f"\n❌ Error during streaming: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        print("Please try rephrasing your question.")




