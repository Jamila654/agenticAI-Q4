#type: ignore
from agents import function_tool, RunContextWrapper
from context import UserInfo

@function_tool
async def maths_tool(wrapper: RunContextWrapper[UserInfo], query: str) -> str:
    """Helps {name} with a simple math question and answer."""
    name = wrapper.context.name or "Math Whiz"
    query = query.lower().strip()
    timestamp = wrapper.context.timestamp.strftime("%Y-%m-%d %H:%M:%S %Z")

    if "add" in query or "+" in query:
        return f"{name}, on {timestamp}, let's add: 2 + 3 = {2 + 3}"
    elif "multiply" in query or "*" in query:
        return f"{name}, on {timestamp}, let's multiply: 4 * 5 = {4 * 5}"
    else:
        return f"{name}, on {timestamp}, ask about 'add' or 'multiply' for a quick math answer!"