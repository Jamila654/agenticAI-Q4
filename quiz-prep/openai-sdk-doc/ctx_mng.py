import asyncio
from dataclasses import dataclass
from config import config
from openai.types.responses import ResponseTextDeltaEvent
from agents import Agent, RunContextWrapper, Runner, function_tool, ModelSettings

@dataclass
class UserInfo:  
    name: str
    uid: int

@function_tool
async def fetch_user_age(wrapper: RunContextWrapper[UserInfo]) -> str:  
    """Fetch the age of the user. Call this function to get user's age information."""
    try:
        return f"The user {wrapper.context.name} is 47 years old"
    except AttributeError as e:
        return f"Error accessing context: {e}"
@function_tool
async def greet_user(wrapper: RunContextWrapper[UserInfo]) -> str:
    """Greet the user with their name."""
    try:
        return f"Hello {wrapper.context.name}, how can I assist you today?"
    except AttributeError as e:
        return f"Error accessing context: {e}"

async def main():

    user_inp_name = input("Enter your name: ")
    user_inp_uid = int(input("Enter your user ID: "))

    user_info = UserInfo(name=user_inp_name, uid=user_inp_uid)
    # user_info = UserInfo(name="John", uid=123)

    agent = Agent[UserInfo](  
        name="Assistant",
        instructions="first greet the user by calling the `greet_user` function and then respond to the user's query by calling the `fetch_user_age` function.",
        tools=[greet_user, fetch_user_age],
        
    )

    result = await Runner.run(  
        starting_agent=agent,
        input="hello",
        context=user_info,
        run_config=config,
    )

    print(result.final_output)  
    # The user John is 47 years old.

if __name__ == "__main__":
    asyncio.run(main())