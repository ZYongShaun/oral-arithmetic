from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class WrongQuestionBase(BaseModel):
    child_id: int
    question_id: int


class WrongQuestionCreate(WrongQuestionBase):
    practice_id: int
    user_answer: str


class WrongQuestionResponse(BaseModel):
    id: int
    child_id: int
    question_id: int
    practice_id: int
    user_answer: str
    expected_answer: str
    question_text: str
    question_type: str
    created_at: datetime
    reviewed: bool
    reviewed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class WrongQuestionPracticeRequest(BaseModel):
    child_id: int
    limit: int = Field(10, ge=1, le=50)


class WrongQuestionStatsResponse(BaseModel):
    total_count: int
    reviewed_count: int
    unreviewed_count: int
    by_type: dict
    recent_count: int
