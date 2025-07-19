#type: ignore
from agents import Runner, ItemHelpers, InputGuardrailTripwireTriggered, OutputGuardrailTripwireTriggered
import json
from openai.types.responses import ResponseTextDeltaEvent
from config import config
from main_agent import main_agent
from context import UserInfo
from hooks import DemoRunHooks

async def stream_main(name: str, query: str, hooks=None):
    try:
        print("Starting stream...\n")
        print(f"Starting agent: {main_agent.name}\n")
        user_info = UserInfo(name=name, text=query)
        
        result = Runner.run_streamed(
            main_agent,
            query,
            run_config=config,
            context=user_info,
            hooks=hooks or DemoRunHooks()
        )
        async for event in result.stream_events():
            if event.type == "raw_response_event":
                if hasattr(event, "data") and isinstance(event.data, ResponseTextDeltaEvent):
                    if hasattr(event.data, 'delta') and event.data.delta:
                        chunk = json.dumps({"chunk": event.data.delta})
                        yield f"data: {chunk}\n"
                        continue
            elif event.type == "agent_updated_stream_event":
                if hasattr(event, "new_agent") and hasattr(event.new_agent, "name"):
                    chunk = json.dumps({"agent_updated": event.new_agent.name})
                    yield f"data: {chunk}\n"
                    continue
            elif event.type == "run_item_stream_event":
                if hasattr(event, "item") and event.item:
                    if event.item.type == "tool_call_item":
                        tool_name = getattr(event.item.raw_item, "name", "Unknown Tool")
                        chunk = json.dumps({"tool_called": tool_name})
                        yield f"data: {chunk}\n"
                        print(f"Tool was called: {tool_name}")
                    elif event.item.type == "tool_call_output_item":
                        output = event.item.output if hasattr(event.item, "output") else ""
                        chunk = json.dumps({"tool_output": output})
                        yield f"data: {chunk}\n"
                        print(f"Tool output: {output}")
                    elif event.item.type == "message_output_item":
                        text_output = ItemHelpers.text_message_output(event.item)
                        chunk = json.dumps({"message_output": text_output})
                        yield f"data: {chunk}\n"
                        print(f"Message output:\n{text_output}")
                    else:
                        pass
            # Yield hook logs if available
            if hooks and hasattr(hooks, 'logs') and hooks.logs:
                for log in hooks.logs:
                    yield f"data: {json.dumps({'hook_log': log})}\n"
                hooks.logs.clear()  # Clear logs after yielding
    except InputGuardrailTripwireTriggered as e:
        reason = e.guardrail_result.output.tripwire_triggered
        error_msg = json.dumps({"error": f"Input rejected: {reason}"})
        print(f"❌ Input rejected: {reason}")
        yield error_msg
    except OutputGuardrailTripwireTriggered as e:
        reason = e.guardrail_result.output.output_info
        error_msg = json.dumps({"error": f"Output blocked: {reason}"})
        print(f"⚠️ Output blocked: {reason}")
        yield error_msg
    except Exception as e:
        error_msg = json.dumps({"error": f"Agent processing failed: {str(e)}"})
        print(f"Error during streaming: {e}")
        yield error_msg