#type: ignore
from pydantic import BaseModel
from agents import (
    Agent,
    GuardrailFunctionOutput,
    RunContextWrapper,
    Runner,
    TResponseInputItem,
    input_guardrail,
    output_guardrail,
)
from config import model, config

class MathsOrPython(BaseModel):
    is_maths_or_python_related: bool
    reasoning: str


input_guardrail_agent = Agent(
    name="InputmathsOrPythonGuard",
    instructions="Verify if the input is about maths or python only, not even 'hey' or 'hi'. If not, return false with reasoning.",
    output_type=MathsOrPython,
    model=model
)

@input_guardrail
async def input_maths_or_python_guardrail(
    ctx: RunContextWrapper, agent: Agent, input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    # Extract last user message
    user_input = input[-1]["content"] if isinstance(input, list) else input
    
    result = await Runner.run(input_guardrail_agent, user_input, run_config=config)
    
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=not result.final_output.is_maths_or_python_related
    )
    
output_guardrail_agent = Agent(
    name="OutputmathsOrPythonGuard",
    instructions="verify if the output is about maths or python. if not, return false.",
    output_type=MathsOrPython,
    model=model
)

@output_guardrail
async def output_maths_or_python_guardrail(
    ctx: RunContextWrapper, agent: Agent, output: str
) -> GuardrailFunctionOutput:
    result = await Runner.run(output_guardrail_agent, output, run_config=config)
    
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=not result.final_output.is_maths_or_python_related
    )
