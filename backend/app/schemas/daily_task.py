from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Optional


class DailyTaskStatusResponse(BaseModel):
    date: date
    target_count: int
    completed_count: int
    is_completed: bool
    stars_earned: int
    progress_percentage: float


class DailyTaskClaimRequest(BaseModel):
    child_id: int
    date: Optional[date] = None


class DailyTaskClaimResponse(BaseModel):
    success: bool
    stars_earned: int
    message: str
