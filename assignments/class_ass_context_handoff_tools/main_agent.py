#type: ignore
from agents import Agent
from config import model
from context import UserInfo
from agent.maths import handoff_obj_math
from agent.python import handoff_obj_python
from guardrails import input_maths_or_python_guardrail, output_maths_or_python_guardrail
from hooks import DemoAgentHooks



main_agent = Agent[UserInfo](
    name="main_agent",
    instructions="You handoff to math_agent for math questions or python_agent for Python questions. Do not answer directly. if the user query unrelated to math or python, return false with reasoning and say 'I don't know how to help you with that'.",
    model=model,
    handoffs=[
        handoff_obj_math,
        handoff_obj_python
    ],
    input_guardrails=[input_maths_or_python_guardrail],
    output_guardrails=[output_maths_or_python_guardrail],
    hooks=DemoAgentHooks()
)

