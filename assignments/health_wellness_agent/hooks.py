#type:ignore
from agents import RunHooks, AgentHooks, Agent, Tool, RunContextWrapper
from context import UserSessionContext
from datetime import datetime

class HealthPlannerAgentHooks(AgentHooks[UserSessionContext]):
    """Agent-level hooks for individual agents"""
    
    def _get_tool_name(self, tool: Tool) -> str:
        """Safely get tool name from different tool types."""
        for attr in ['tool_name', 'name', 'function_name', 'type']:
            if hasattr(tool, attr):
                value = getattr(tool, attr)
                if value:
                    return str(value)
        return tool.__class__.__name__
    
    async def on_start(self, context: RunContextWrapper[UserSessionContext], agent: Agent[UserSessionContext]):
        log_message = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Agent {agent.name} started"
        context.context.handoff_logs.append(log_message)
        print(f"🚀 [AGENT HOOK] {log_message}")
    
    async def on_end(self, context: RunContextWrapper[UserSessionContext], agent: Agent[UserSessionContext], output):
        log_message = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Agent {agent.name} ended"
        context.context.handoff_logs.append(log_message)
        print(f"🏁 [AGENT HOOK] {log_message}")
    
    async def on_handoff(self, context: RunContextWrapper[UserSessionContext], agent: Agent[UserSessionContext], source: Agent[UserSessionContext]):
        log_message = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Handed off from {source.name} to {agent.name}"
        context.context.handoff_logs.append(log_message)
        print(f"🤝 [AGENT HOOK] {log_message}")
    
    async def on_tool_start(self, context: RunContextWrapper[UserSessionContext], agent: Agent[UserSessionContext], tool: Tool):
        tool_name = self._get_tool_name(tool)
        log_message = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Started tool {tool_name}"
        context.context.handoff_logs.append(log_message)
        print(f"🔧 [AGENT HOOK] {log_message}")
    
    async def on_tool_end(self, context: RunContextWrapper[UserSessionContext], agent: Agent[UserSessionContext], tool: Tool, result: str):
        tool_name = self._get_tool_name(tool)
        result_preview = result[:50] + "..." if len(result) > 50 else result
        log_message = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Ended tool {tool_name} with result: {result_preview}"
        context.context.handoff_logs.append(log_message)
        print(f"✅ [AGENT HOOK] {log_message}")


class HealthPlannerRunHooks(RunHooks[UserSessionContext]):
    """Runner-level hooks for the entire conversation"""
    
    def _get_tool_name(self, tool: Tool) -> str:
        """Safely get tool name from different tool types."""
        for attr in ['tool_name', 'name', 'function_name', 'type']:
            if hasattr(tool, attr):
                value = getattr(tool, attr)
                if value:
                    return str(value)
        return tool.__class__.__name__
    
    async def on_agent_start(self, context: RunContextWrapper[UserSessionContext], agent: Agent[UserSessionContext]):
        log_message = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Runner started agent {agent.name}"
        context.context.handoff_logs.append(log_message)
        print(f"🚀 [RUN HOOK] {log_message}")
    
    async def on_agent_end(self, context: RunContextWrapper[UserSessionContext], agent: Agent[UserSessionContext], output):
        log_message = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Runner ended agent {agent.name}"
        context.context.handoff_logs.append(log_message)
        print(f"🏁 [RUN HOOK] {log_message}")
    
    async def on_handoff(self, context: RunContextWrapper[UserSessionContext], from_agent: Agent[UserSessionContext], to_agent: Agent[UserSessionContext]):
        log_message = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Runner handoff from {from_agent.name} to {to_agent.name}"
        context.context.handoff_logs.append(log_message)
        print(f"🤝 [RUN HOOK] {log_message}")
    
    async def on_tool_start(self, context: RunContextWrapper[UserSessionContext], agent: Agent[UserSessionContext], tool: Tool):
        tool_name = self._get_tool_name(tool)
        log_message = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Runner started tool {tool_name}"
        context.context.handoff_logs.append(log_message)
        print(f"🔧 [RUN HOOK] {log_message}")
    
    async def on_tool_end(self, context: RunContextWrapper[UserSessionContext], agent: Agent[UserSessionContext], tool: Tool, result: str):
        tool_name = self._get_tool_name(tool)
        result_preview = result[:50] + "..." if len(result) > 50 else result
        log_message = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Runner ended tool {tool_name} with result: {result_preview}"
        context.context.handoff_logs.append(log_message)
        print(f"✅ [RUN HOOK] {log_message}")


# Alias for backward compatibility
HealthPlannerHooks = HealthPlannerAgentHooks



