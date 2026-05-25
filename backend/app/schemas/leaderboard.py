from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Optional


class LeaderboardEntry(BaseModel):
    rank: int
    child_id: int
    child_name: str
    avatar: Optional[str] = None
    total_stars: int
    weekly_practices: int
    weekly_accuracy: float
    is_current_user: bool = False


class LeaderboardResponse(BaseModel):
    week_start: date
    week_end: date
    group_id: int
    group_name: str
    entries: list[LeaderboardEntry]
    user_rank: Optional[int] = None
    total_in_group: int
    promotion_cutoff: int
    demotion_cutoff: int


class LeaderboardHistoryItem(BaseModel):
    week_start: date
    week_end: date
    rank: int
    group_id: int
    total_stars: int
    weekly_practices: int


class LeaderboardGroupInfo(BaseModel):
    group_id: int
    group_name: str
    member_count: int
    current_rank: int
    week_start: date
    week_end: date
    promotion_cutoff: int
    demotion_cutoff: int
