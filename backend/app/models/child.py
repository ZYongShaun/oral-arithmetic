"""
孩子档案模型
"""
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime


class Child(Base):
    """孩子档案表"""
    __tablename__ = "children"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(50), nullable=False)
    gender = Column(Integer)  # 1-男 2-女
    birth_date = Column(Date, nullable=True)
    grade = Column(String(20), default="一年级")
    is_active = Column(Integer, default=1)
    total_stars = Column(Integer, default=0)  # 累计星星数
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # 关系
    parent = relationship("User", back_populates="children")
    practices = relationship("Practice", back_populates="child")
    wrong_questions = relationship("WrongQuestion", back_populates="child")
    daily_tasks = relationship("DailyTask", back_populates="child")
    streak = relationship("Streak", back_populates="child", uselist=False)
