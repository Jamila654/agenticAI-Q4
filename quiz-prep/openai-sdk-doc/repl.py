import asyncio
from agents import Agent, run_demo_loop, set_tracing_disabled
from config import model

set_tracing_disabled(True)
async def main() -> None:
    agent = Agent(name="Assistant", instructions="You are a helpful assistant.", model=model)
    await run_demo_loop(agent)

if __name__ == "__main__":
    asyncio.run(main())