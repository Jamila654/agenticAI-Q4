from agents import function_tool, RunContextWrapper
from context import UserInfo

@function_tool
async def python_tool(wrapper: RunContextWrapper[UserInfo], query: str) -> str:
    """Helps {name} with a simple Python question and answer."""
    name = wrapper.context.name
    query = query.lower().strip()
    timestamp = wrapper.context.timestamp.strftime("%Y-%m-%d %H:%M:%S %Z")

    if "loop" in query:
        return f"{name}, on {timestamp}, here's a Python loop:\n```python\nfor i in range(3):\n    print(i)\n```"
    elif "function" in query:
        return f"{name}, on {timestamp}, here's a Python function:\n```python\ndef hi():\n    return 'Hello!'\n```"
    else:
        return f"{name}, on {timestamp}, ask about 'loop' or 'function' for a quick Python example!"