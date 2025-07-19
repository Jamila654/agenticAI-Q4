#type: ignore
from agents import Agent, handoff, RunContextWrapper
from config import model
from context import UserInfo
from tools.python_teacher import python_tool
from pydantic import BaseModel
from hooks import DemoAgentHooks

class EscalationData(BaseModel):
    reason: str

def on_handoff_python(ctx: RunContextWrapper[UserInfo], input_data: EscalationData):
    print(f"Handing off to python_agent...: {input_data.reason}\n")
    

python_agent = Agent[UserInfo](
    name="python_agent",
    instructions="You are a Python teacher. For any Python-related question, always call python_tool with the full query. Do not generate code or explanations directly.",
    model=model,
    tools=[python_tool],
    hooks=DemoAgentHooks()
)

handoff_obj_python = handoff(
    agent=python_agent,
    on_handoff=on_handoff_python,
    tool_name_override="transfer_to_python_tool",
    input_type=EscalationData,
)