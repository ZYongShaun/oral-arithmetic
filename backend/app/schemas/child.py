from pydantic import BaseModel
from typing import Optional


class ChildBase(BaseModel):
    """孩子档案基础模型"""
    name: str
    gender: Optional[int] = None
    birth_date: Optional[str] = None
    grade: str = "一年级"


class ChildCreate(ChildBase):
    """创建孩子请求"""
    nickname: Optional[str] = None
    avatar: Optional[str] = None
    grade_level: Optional[str] = None
    difficulty_level: Optional[int] = None


class ChildUpdate(BaseModel):
    """更新孩子信息请求"""
    name: Optional[str] = None
    gender: Optional[int] = None
    birth_date: Optional[str] = None
    grade: Optional[str] = None
    is_active: Optional[int] = None


class ChildResponse(ChildBase):
    """孩子信息响应"""
    id: int
    user_id: int
    stars: int
    is_active: int
    created_at: str
    nickname: Optional[str] = None
    avatar: Optional[str] = None
    grade_level: Optional[str] = None
    difficulty_level: Optional[int] = None
    
    class Config:
        from_attributes = True
