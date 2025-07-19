#type: ignore
from agents import RunHooks, AgentHooks, RunContextWrapper, Tool
from typing import Any
from context import UserInfo

class DemoRunHooks(RunHooks[UserInfo]):
    def __init__(self):
        self.logs = []
        super().__init__()

    async def on_agent_start(self, context: RunContextWrapper[UserInfo], agent: Any) -> None:
        log = f"[Run Hook] Agent {agent.name} started for user: {context.context.name or 'Unknown'}\n"
        print(log)
        self.logs.append(log)

    async def on_handoff(self, context: RunContextWrapper[UserInfo], from_agent: Any, to_agent: Any) -> None:
        log = f"[Run Hook] Handoff from {from_agent.name} to {to_agent.name}\n"
        print(log)
        self.logs.append(log)

    async def on_tool_start(self, context: RunContextWrapper[UserInfo], agent: Any, tool: Tool) -> None:
        log = f"[Run Hook] Tool {tool.name} started by {agent.name}\n"
        print(log)
        self.logs.append(log)

    async def on_tool_end(self, context: RunContextWrapper[UserInfo], agent: Any, tool: Tool, result: str) -> None:
        log = f"[Run Hook] Tool {tool.name} ended with result: {result}\n"
        print(log)
        self.logs.append(log)

class DemoAgentHooks(AgentHooks[UserInfo]):
    def __init__(self):
        self.logs = []
        super().__init__()

    async def on_start(self, context: RunContextWrapper[UserInfo], agent: Any) -> None:
        log = f"[Agent Hook] {agent.name} started for user: {context.context.name or 'Unknown'}\n"
        print(log)
        self.logs.append(log)

    async def on_handoff(self, context: RunContextWrapper[UserInfo], agent: Any, source: Any) -> None:
        log = f"[Agent Hook] {agent.name} received handoff from {source.name}\n"
        print(log)
        self.logs.append(log)

    async def on_tool_start(self, context: RunContextWrapper[UserInfo], agent: Any, tool: Tool) -> None:
        log = f"[Agent Hook] {agent.name} started tool {tool.name}\n"
        print(log)
        self.logs.append(log)

    async def on_tool_end(self, context: RunContextWrapper[UserInfo], agent: Any, tool: Tool, result: str) -> None:
        log = f"[Agent Hook] {agent.name} ended tool {tool.name} with result: {result}\n"
        print(log)
        self.logs.append(log)