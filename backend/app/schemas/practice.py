from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class PracticeStartRequest(BaseModel):
    child_id: int
    difficulty_level: int = Field(1, ge=1, le=5, description="Difficulty level 1-5")


class PracticeQuestionResponse(BaseModel):
    id: int
    question_text: str
    question_type: str
    expected_answer: str
    options: Optional[list] = None


class PracticeSubmitRequest(BaseModel):
    practice_id: Optional[int] = None
    childId: Optional[int] = None
    answers: dict = Field(..., description="Dict of question_id -> user_answer")
    answer_details: Optional[list] = None
    time_spent: int = Field(0, description="Total time spent in seconds")


class PracticeSubmitResponse(BaseModel):
    practice_id: int
    score: int
    accuracy: float
    stars_earned: int
    time_spent: int
    completed_at: datetime
    details: list


class PracticeHistoryItem(BaseModel):
    id: int
    child_id: int
    score: int
    accuracy: float
    stars_earned: int
    difficulty_level: int
    completed_at: datetime
    time_spent: int

    class Config:
        from_attributes = True


class PracticeDetailResponse(BaseModel):
    id: int
    practice_id: int
    question_id: int
    question_text: str
    user_answer: str
    expected_answer: str
    is_correct: bool
    time_spent: int

    class Config:
        from_attributes = True


class PracticeFullResponse(BaseModel):
    id: int
    child_id: int
    score: int
    accuracy: float
    stars_earned: int
    difficulty_level: int
    completed_at: datetime
    time_spent: int
    details: list[PracticeDetailResponse]

    class Config:
        from_attributes = True
