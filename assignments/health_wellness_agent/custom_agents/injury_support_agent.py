# type:ignore
import os
from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel
from context import UserSessionContext

def create_injury_support_agent():
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    client = AsyncOpenAI(
        api_key=gemini_api_key, 
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )
    model = OpenAIChatCompletionsModel(openai_client=client, model="gemini-2.0-flash")
    
    return Agent[UserSessionContext](
        name="InjurySupportAgent",
        instructions="""
        You specialize in helping users with physical limitations or injuries.
        Provide modified, safe exercise recommendations for common injuries.
        Always emphasize the importance of medical clearance before exercising with injuries.
        Focus on low-impact, rehabilitation-friendly exercises and safety first.
        """,
        model=model
    )

def injury_support_handoff(context: UserSessionContext) -> bool:
    """Trigger handoff for injury-related concerns"""
    injury_keywords = [
        "injury", "injured", "pain", "hurt", "sore", "knee", "back", 
        "shoulder", "ankle", "physical therapy", "rehabilitation", "doctor"
    ]
    
    if context.injury_notes:
        return True
    
    return any(
        keyword in str(context.goal).lower() if context.goal else False
        for keyword in injury_keywords
    )