# guardrails.py
#type:ignore
from pydantic import BaseModel, validator
from typing import Optional

class GoalInput(BaseModel):
    goal_text: str
    
    @validator('goal_text')
    def validate_goal(cls, v):

        """
        Validate the goal text.
        
        Ensure the goal text is at least 5 characters long after stripping whitespace.
        If the goal text is too short, raise a ValueError.
        """

        if len(v.strip()) < 5:
            raise ValueError("Goal must be at least 5 characters long")
        return v.strip()

class GoalOutput(BaseModel):
    goal_type: str  # e.g., "weight_loss", "muscle_gain", "fitness"
    target_amount: Optional[str] = None  # e.g., "5kg", "10 pounds"
    timeframe: Optional[str] = None  # e.g., "2 months", "6 weeks"
    specific_goal: str

class DietPreferenceInput(BaseModel):
    preferences: str
    
    @validator('preferences')
    def validate_preferences(cls, v):
        if len(v.strip()) < 2:
            raise ValueError("Diet preferences must be specified")
        return v.strip().lower()

class MealPlanOutput(BaseModel):
    meal_plan: list
    dietary_type: str
    notes: Optional[str] = None