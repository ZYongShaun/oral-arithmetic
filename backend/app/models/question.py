"""
数据库模型 - 题目相关
"""
from sqlalchemy import Column, Integer, String, Float, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime


class Question(Base):
    """题目表"""
    __tablename__ = "questions"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    level = Column(Integer, nullable=False, comment="难度等级：10/20/50/100")
    type = Column(Integer, nullable=False, comment="题型：1-加法 2-减法 3-混合")
    question_text = Column(String(100), nullable=False, comment="题目文本")
    answer = Column(Integer, nullable=False, comment="正确答案")
    source = Column(Integer, default=1, comment="来源：1-系统生成 2-人工录入")
    status = Column(Integer, default=1, comment="状态：1-启用 0-禁用")
    difficulty = Column(Float, default=0.5, comment="难度系数 0-1")
    usage_count = Column(Integer, default=0, comment="使用次数")
    correct_count = Column(Integer, default=0, comment="正确次数")
    created_by = Column(Integer, ForeignKey("admins.id"), nullable=True, comment="创建人ID")
    created_at = Column(TIMESTAMP, default=datetime.now)
    updated_at = Column(TIMESTAMP, default=datetime.now, onupdate=datetime.now)
    # 关系
    practice_details = relationship("PracticeDetail", back_populates="question")
    wrong_questions = relationship("WrongQuestion", back_populates="question")
