from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class AchievementBase(BaseModel):
    name: str
    description: str
    category: str
    milestone_type: str
    milestone_value: int
    stars_reward: int


class AchievementResponse(BaseModel):
    id: int
    name: str
    description: str
    category: str
    milestone_type: str
    milestone_value: int
    stars_reward: int
    icon: Optional[str] = None

    class Config:
        from_attributes = True


class ChildAchievementProgress(BaseModel):
    achievement_id: int
    achievement_name: str
    category: str
    milestone_value: int
    current_value: int
    progress_percentage: float
    achieved: bool
    stars_rewarded: bool
    achieved_at: Optional[datetime] = None


class AchievementProgressResponse(BaseModel):
    child_id: int
    achievements: list[ChildAchievementProgress]
    total_achieved: int
    total_stars_earned: int


class AchievementCheckRequest(BaseModel):
    child_id: int
    achievement_type: str
