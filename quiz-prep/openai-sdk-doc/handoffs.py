from pydantic import BaseModel
from agents import Agent, handoff, RunContextWrapper, function_tool, Runner
from config import config
from openai.types.responses import ResponseTextDeltaEvent
from agents.extensions.handoff_prompt import prompt_with_handoff_instructions
import asyncio

class EscalationData(BaseModel):
    reason: str

async def on_handoff(ctx: RunContextWrapper[None], input_data: EscalationData):
    print(f"Escalation agent called with reason: {input_data.reason}")

@function_tool(name_override="escalation_tool")
async def esc_tool(a: int, b: int) -> int:
    """A tool that adds two numbers."""
    return a + b
    

agent = Agent(name="Escalation agent", instructions="only use tool dont answer by yourself", tools=[esc_tool], tool_use_behavior='stop_on_first_tool')

handoff_obj = handoff(
    agent=agent,
    on_handoff=on_handoff,
    input_type=EscalationData,
    tool_name_override="escalation_tool",
)

main_agent = Agent(name="Main agent", instructions=f"first handoff to escalation agent and resond the final answer of escalation agent {prompt_with_handoff_instructions}", handoffs=[handoff_obj])

async def main():
    #with reasoin for escalation

    try:
            result = Runner.run_streamed(main_agent, input="i want to talk to escalation agent because what is 2 + 2 ", run_config=config)
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


if __name__ == "__main__":
    asyncio.run(main())