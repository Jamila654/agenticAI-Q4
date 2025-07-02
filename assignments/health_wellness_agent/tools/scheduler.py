# type:ignore
from agents import function_tool, RunContextWrapper
from context import UserSessionContext
from datetime import datetime, timedelta

@function_tool
async def checkin_scheduler_tool(
    wrapper: RunContextWrapper[UserSessionContext], 
    frequency: str = "weekly"
) -> str:
    """Schedule regular check-ins for progress tracking"""
    
    # Calculate next check-in dates
    today = datetime.now()
    
    if frequency.lower() == "weekly":
        next_checkin = today + timedelta(weeks=1)
        interval = "week"
    elif frequency.lower() == "daily":
        next_checkin = today + timedelta(days=1)
        interval = "day"
    else:
        next_checkin = today + timedelta(weeks=1)  # default to weekly
        interval = "week"
    
    # Create check-in schedule
    schedule_info = {
        "frequency": frequency,
        "next_checkin": next_checkin.strftime("%Y-%m-%d"),
        "created_at": today.strftime("%Y-%m-%d %H:%M")
    }
    
    # Add to context logs
    wrapper.context.progress_logs.append({
        "type": "schedule_created",
        "date": today.strftime("%Y-%m-%d"),
        "details": f"Check-in scheduled every {interval}"
    })
    
    return f"📅 Perfect! I've scheduled {frequency} check-ins for you.\n" \
           f"Your next check-in is on {next_checkin.strftime('%B %d, %Y')}.\n" \
           f"I'll ask about your progress, challenges, and help adjust your plan if needed!"