from dataclasses import dataclass
from agents import RunContextWrapper, Agent, Runner
from config import config
import asyncio

@dataclass
class UserInfo:
    uname: str
    uid: int
    contact_num: int


def userData(ctx: RunContextWrapper[UserInfo], agent: Agent)-> str:
    return f"you must greet {ctx.context.uname}"

async def main():
    # user_data = UserInfo(uname="jam", uid=123, contact_num=12345)
    # basic_agent = Agent[UserInfo](
    #     name="assistant",
    #     instructions=userData
    # )
    # res = await Runner.run(starting_agent=basic_agent, input="hey", run_config=config, context=user_data)
    # print(res.final_output)

    pirate_agent = Agent(
        name = "pirate agent",
        instructions = "write like a pirate"
    )
    robot_agent = pirate_agent.clone(
        name="robot agent",
        instructions="write like a robot"
    )
    res = await Runner.run(starting_agent=pirate_agent, input="hello", run_config=config)
    print(res.final_output)


if __name__ == "__main__":
    asyncio.run(main())
