#type: ignore
from agents import Runner, Agent
from context import UserSessionContext
from openai.types.responses import ResponseTextDeltaEvent

def get_tool_name_from_item(item) -> str:
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
    """Async generator yielding text chunks as they stream."""
    try:
        result = Runner.run_streamed(
            starting_agent=agent,
            input=user_input,
            context=context,
            hooks=runner_hooks
        )
        
        async for event in result.stream_events():
            if event.type == "raw_response_event":
                if hasattr(event, "data") and isinstance(event.data, ResponseTextDeltaEvent):
                    if hasattr(event.data, 'delta') and event.data.delta:
                        yield event.data.delta
            elif event.type == "text_delta_event":
                if hasattr(event, "delta"):
                    yield event.delta
    except Exception as e:
        yield f"\n❌ Error during streaming: {str(e)}\nPlease try rephrasing your question."






