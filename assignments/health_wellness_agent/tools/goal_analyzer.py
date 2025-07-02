# type:ignore
from agents import function_tool, RunContextWrapper
from context import UserSessionContext
from guardrails import GoalInput
import re

@function_tool
async def goal_analyzer_tool(
    wrapper: RunContextWrapper[UserSessionContext], 
    goal_text: str
) -> str:
    """Analyze user's health goal and extract structured information"""
    try:
        goal_input = GoalInput(goal_text=goal_text)
    except Exception as e:
        return f"Please provide a clearer goal. Error: {str(e)}"
    
    text_lower = goal_input.goal_text.lower()
    
    # Extract goal type
    if any(word in text_lower for word in ['lose', 'weight', 'slim', 'diet']):
        goal_type = "weight_loss"
    elif any(word in text_lower for word in ['gain', 'muscle', 'bulk', 'strong']):
        goal_type = "muscle_gain"
    elif any(word in text_lower for word in ['fit', 'exercise', 'cardio', 'run']):
        goal_type = "fitness"
    else:
        goal_type = "general_health"
    
    # Extract numbers and timeframes
    numbers = re.findall(r'\d+', goal_input.goal_text)
    timeframe_words = ['week', 'month', 'day', 'year']
    timeframe = None
    
    for word in timeframe_words:
        if word in text_lower:
            timeframe = f"{numbers[0] if numbers else '4'} {word}s"
            break
    
    # Create structured goal
    structured_goal = {
        "goal_type": goal_type,
        "target_amount": numbers[0] if numbers else None,
        "timeframe": timeframe,
        "specific_goal": goal_input.goal_text
    }
    
    # Update context
    wrapper.context.goal = structured_goal
    
    return f"✅ Got it! I've analyzed your goal: {goal_type.replace('_', ' ').title()}. " \
           f"Target: {structured_goal.get('target_amount', 'Not specified')}. " \
           f"Timeframe: {timeframe or 'Flexible'}. Let's create a plan for you!"