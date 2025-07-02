# type:ignore
import os
from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel
from context import UserSessionContext

def create_escalation_agent():
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    client = AsyncOpenAI(
        api_key=gemini_api_key, 
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )
    model = OpenAIChatCompletionsModel(openai_client=client, model="gemini-2.0-flash")
    
    return Agent[UserSessionContext](
        name="EscalationAgent",
        instructions="""
        You help users who want to speak with a human coach or trainer.
        Provide information about contacting human support while being understanding and helpful.
        Always acknowledge their request and provide next steps.
        """,
        model=model
    )

def escalation_handoff(context: UserSessionContext) -> bool:
    """Trigger handoff when user wants human support"""
    return any(phrase in context.name.lower() for phrase in [
        "human", "trainer", "coach", "person", "speak to someone", "real person"
    ])