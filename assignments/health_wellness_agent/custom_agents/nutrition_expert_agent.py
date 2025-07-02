# type:ignore
import os
from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel
from context import UserSessionContext

def create_nutrition_expert_agent():
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    client = AsyncOpenAI(
        api_key=gemini_api_key, 
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )
    model = OpenAIChatCompletionsModel(openai_client=client, model="gemini-2.0-flash")
    
    return Agent[UserSessionContext](
        name="NutritionExpertAgent",
        instructions="""
        You are a specialized nutrition expert for complex dietary needs.
        Handle questions about diabetes, food allergies, medical dietary restrictions.
        Always recommend consulting healthcare providers for medical conditions.
        Provide safe, general nutrition guidance while emphasizing professional medical advice.
        """,
        model=model
    )

def nutrition_expert_handoff(context: UserSessionContext) -> bool:
    """Trigger handoff for complex dietary needs"""
    dietary_keywords = [
        "diabetes", "diabetic", "allergy", "allergic", "celiac", 
        "medical", "condition", "doctor", "medication", "blood sugar"
    ]
    
    if context.diet_preferences:
        return any(keyword in context.diet_preferences.lower() for keyword in dietary_keywords)
    return False