# type:ignore
from agents import (
    Runner, Agent, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig,
    GuardrailFunctionOutput, InputGuardrailTripwireTriggered, OutputGuardrailTripwireTriggered,
    RunContextWrapper, TResponseInputItem, input_guardrail, output_guardrail
)
from dotenv import load_dotenv
import os
from pydantic import BaseModel, field_validator

load_dotenv()


gemini_api_key = os.getenv("GEMINI_API_KEY")

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)



class HealthInputCheck(BaseModel):
    is_valid_health_request: bool
    reasoning: str

    @field_validator("reasoning")
    def reasoning_not_empty(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError("Reasoning must not be empty")
        return v

class HealthOutputCheck(BaseModel):
    is_relevant_health_response: bool
    reasoning: str

    @field_validator("reasoning")
    def reasoning_not_empty(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError("Reasoning must not be empty")
        return v


input_guardrail_agent = Agent(
    name="HealthInputGuard",
    instructions="""
You are a guardrail agent that determines if the user input is a valid health or wellness request that requires the assistant to take meaningful action.

Return true only if the input:
- Expresses a clear health or fitness goal (e.g., losing weight, gaining muscle, improving fitness)
- Requests a meal plan, workout routine, progress tracking, or scheduling a check-in
- Asks for advice or support related to nutrition, exercise, or wellness
- Responds affirmatively to the assistant's follow-up questions to continue planning or coaching

Return false if the input is off-topic, vague, or unrelated to health and wellness.

Your goal is to allow inputs that should trigger the assistant to analyze goals, call tools, and engage in a helpful, ongoing conversation.
""",
    output_type=HealthInputCheck,
    model=model
)

@input_guardrail
async def input_health_guardrail(
    ctx: RunContextWrapper, agent: Agent, input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    # Extract last user message
    user_input = input[-1]["content"] if isinstance(input, list) else input

    result = await Runner.run(input_guardrail_agent, user_input)

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=not result.final_output.is_valid_health_request
    )



output_guardrail_agent = Agent(
    name="HealthOutputGuard",
    instructions="""
You are a guardrail agent that verifies whether the assistant's response is appropriate and relevant to health and wellness topics setting a scheduled check-in or progress tracking.
""",
    output_type=HealthOutputCheck,
    model=model
)

@output_guardrail
async def output_health_guardrail(
    ctx: RunContextWrapper, agent: Agent, output: str
) -> GuardrailFunctionOutput:
    result = await Runner.run(output_guardrail_agent, output)

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=not result.final_output.is_relevant_health_response
    )

