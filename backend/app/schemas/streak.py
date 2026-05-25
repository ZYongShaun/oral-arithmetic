from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Optional


class StreakResponse(BaseModel):
    child_id: int
    current_streak: int
    last_practice_date: Optional[date] = None
    is_active: bool
    shield_active: bool
    shield_expires_at: Optional[datetime] = None
    best_streak: int
    total_practices: int

    class Config:
        from_attributes = True


class StreakUseShieldRequest(BaseModel):
    child_id: int


class StreakUseShieldResponse(BaseModel):
    success: bool
    message: str
    shield_expires_at: Optional[datetime] = None


class StreakMilestoneResponse(BaseModel):
    milestone_days: int
    achieved: bool
    stars_rewarded: int
    achieved_at: Optional[datetime] = None
