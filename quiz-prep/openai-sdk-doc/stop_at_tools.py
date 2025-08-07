from agents import Agent, Runner, function_tool
from agents.agent import StopAtTools
import asyncio
from config import config

@function_tool
def get_weather(city: str) -> str:
    """Returns weather info for the specified city."""
    return f"The weather in {city} is sunny"

@function_tool
def sum_numbers(a: int, b: int) -> int:
    """Adds two numbers."""
    return a + b

agent = Agent(
    name="Stop At Stock Agent",
    instructions="Get weather or sum numbers.",
    tools=[get_weather, sum_numbers],
    tool_use_behavior=StopAtTools(stop_at_tool_names=["get_weather"])
)
async def main():
    result = await Runner.run(agent, "what is 2 + 2?", run_config=config)
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())