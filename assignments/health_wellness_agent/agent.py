# type:ignore
import os
from dotenv import load_dotenv
from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled

# Load environment variables
load_dotenv()
from context import UserSessionContext
from tools.goal_analyzer import goal_analyzer_tool
from tools.meal_planner import meal_planner_tool
from tools.workout_recommender import workout_recommender_tool
from tools.scheduler import checkin_scheduler_tool
from tools.tracker import progress_tracker_tool
from custom_agents.escalation_agent import create_escalation_agent
from custom_agents.nutrition_expert_agent import create_nutrition_expert_agent
from custom_agents.injury_support_agent import create_injury_support_agent

set_tracing_disabled(True)

# Setup Gemini client
gemini_api_key = os.getenv("GEMINI_API_KEY")
client = AsyncOpenAI(
    api_key=gemini_api_key, 
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
model = OpenAIChatCompletionsModel(openai_client=client, model="gemini-2.0-flash")

def create_health_agent():
    return Agent[UserSessionContext](
        name="HealthWellnessAgent",
        instructions="""
        You are a friendly Health & Wellness Assistant. Help users with:
        - Setting and analyzing fitness goals
        - Creating meal plans based on dietary preferences
        - Recommending workout routines
        - Tracking progress and scheduling check-ins
        - Do NOT concatenate tool names or call multiple tools in a single call.
        - Format tool calls clearly and separately.
        When users ask for meal plans, workout routines, or goal analysis, USE THE APPROPRIATE TOOLS IMMEDIATELY to provide helpful content.
        Tools have default parameters, so use them even if the user doesn't specify all details.
        ALWAYS INCLUDE THE COMPLETE TOOL RESULTS IN YOUR RESPONSE - don't just say 'I've created a plan', show the actual plan details.
        Be encouraging and supportive. Provide immediate value first, then ask follow-up questions for improvements.
        If users mention injuries, complex dietary needs, or want human support, use handoffs.
        """,

        tools=[
            goal_analyzer_tool,
            meal_planner_tool,
            workout_recommender_tool,
            checkin_scheduler_tool,
            progress_tracker_tool
        ],
        handoffs=[
            create_escalation_agent(),
            create_nutrition_expert_agent(),
            create_injury_support_agent()
        ],
        model=model
    )