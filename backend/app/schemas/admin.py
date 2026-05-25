from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class AdminLoginRequest(BaseModel):
    username: str
    password: str


class AdminLoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    admin_id: int
    username: str


class UserListItem(BaseModel):
    id: int
    username: str
    email: Optional[str] = None
    phone: Optional[str] = None
    created_at: datetime
    is_active: bool
    children_count: int

    class Config:
        from_attributes = True


class QuestionAdminCreate(BaseModel):
    grade_level: int
    difficulty_level: int
    question_type: str
    question_text: str
    expected_answer: str
    options: Optional[list] = None
    knowledge_point: Optional[str] = None
    source: str = "manual"


class QuestionAdminUpdate(BaseModel):
    grade_level: Optional[int] = None
    difficulty_level: Optional[int] = None
    question_type: Optional[str] = None
    question_text: Optional[str] = None
    expected_answer: Optional[str] = None
    options: Optional[list] = None
    knowledge_point: Optional[str] = None
    is_active: Optional[bool] = None


class SystemConfigUpdate(BaseModel):
    daily_task_target: Optional[int] = None
    streak_shield_cost: Optional[int] = None
    leaderboard_group_size: Optional[int] = None
    practice_question_count: Optional[int] = None
