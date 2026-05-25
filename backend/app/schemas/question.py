from pydantic import BaseModel, Field
from typing import Optional


class QuestionBase(BaseModel):
    """题目基础模型"""
    level: int = Field(..., description="难度等级：10/20/50/100")
    type: int = Field(..., description="题型：1-加法 2-减法 3-混合")
    question_text: str = Field(..., description="题目文本")
    answer: int = Field(..., description="正确答案")


class QuestionCreate(QuestionBase):
    """创建题目请求"""
    source: int = 1
    status: int = 1
    difficulty: Optional[float] = 0.5
    knowledge_point: Optional[str] = None
    options: Optional[str] = None


class QuestionUpdate(BaseModel):
    """更新题目请求（可选字段）"""
    level: Optional[int] = None
    type: Optional[int] = None
    question_text: Optional[str] = None
    answer: Optional[int] = None
    source: Optional[int] = None
    status: Optional[int] = None
    difficulty: Optional[float] = None
    knowledge_point: Optional[str] = None
    options: Optional[str] = None


class QuestionResponse(BaseModel):
    id: int
    level: int = Field(alias='grade_level')
    type: int = Field(alias='question_type')
    question_text: str
    answer: int = Field(alias='expected_answer')
    difficulty: float = Field(alias='difficulty_level')
    source: int
    status: int
    usage_count: int
    correct_count: int
    created_at: str
    knowledge_point: Optional[str] = None
    options: Optional[str] = None

    class Config:
        from_attributes = True
        populate_by_name = True


class RandomQuestionsRequest(BaseModel):
    grade_level: int
    difficulty_level: Optional[float] = None
    count: int = 20
    question_types: Optional[list[int]] = None
