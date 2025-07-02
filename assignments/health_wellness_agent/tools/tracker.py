# type:ignore
from agents import function_tool, RunContextWrapper
from context import UserSessionContext
from datetime import datetime

@function_tool
async def progress_tracker_tool(
    wrapper: RunContextWrapper[UserSessionContext], 
    progress_update: str,
    metric_value: str,
) -> str:
    """Track user progress and update session context"""
    
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Create progress entry
    progress_entry = {
        "date": today,
        "update": progress_update,
        "metric": metric_value,
        "timestamp": datetime.now().strftime("%H:%M")
    }
    
    # Add to context
    wrapper.context.progress_logs.append(progress_entry)
    
    # Analyze progress
    total_logs = len(wrapper.context.progress_logs)
    
    # Generate encouraging response
    if any(word in progress_update.lower() for word in ['good', 'great', 'achieved', 'completed', 'success']):
        response = f"🎉 Fantastic progress! You're doing amazing!"
    elif any(word in progress_update.lower() for word in ['difficult', 'hard', 'struggle', 'missed']):
        response = f"💪 Don't worry, every journey has challenges. You're still making progress!"
    else:
        response = f"📈 Thanks for the update! Consistency is key to success."
    
    response += f"\n\nProgress logged for {today}:"
    response += f"\n• {progress_update}"
    if metric_value:
        response += f"\n• Metric: {metric_value}"
    
    response += f"\n\nTotal check-ins: {total_logs}"
    
    # Provide motivation based on user's goal
    if wrapper.context.goal:
        goal_type = wrapper.context.goal.get('goal_type', 'health')
        if goal_type == 'weight_loss':
            response += f"\n\n💡 Remember: Small daily choices lead to big results in weight loss!"
        elif goal_type == 'muscle_gain':
            response += f"\n\n💡 Keep it up! Muscle building is a marathon, not a sprint!"
        else:
            response += f"\n\n💡 You're building healthy habits that will last a lifetime!"
    
    return response