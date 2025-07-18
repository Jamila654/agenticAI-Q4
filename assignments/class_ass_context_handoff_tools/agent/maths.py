#type: ignore
from agents import Agent, handoff, RunContextWrapper
from config import model
from context import UserInfo
from tools.maths_teacher import maths_tool
from pydantic import BaseModel

class EscalationData(BaseModel):
    reason: str

def on_handoff_math(ctx: RunContextWrapper[UserInfo], input_data: EscalationData):
    print(f"Handing off to math_agent...: {input_data.reason}\n")

math_agent = Agent[UserInfo](
    name="math_agent",
    instructions="you are a helpful assistant. You are a maths teacher use the maths_tool",
    model=model,
    tools=[maths_tool],
)

handoff_obj_math = handoff(
    agent=math_agent,
    on_handoff=on_handoff_math,
    tool_name_override="transfer_to_math_tool",
    input_type=EscalationData,
)