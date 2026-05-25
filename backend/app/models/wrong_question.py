"""
错题模型
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, TIMESTAMP, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime


class WrongQuestion(Base):
    """错题表"""
    __tablename__ = "wrong_questions"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    child_id = Column(Integer, ForeignKey("children.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False, comment="题目ID")
    question_text = Column(String(100), nullable=False, comment="题目文本")
    correct_answer = Column(Integer, nullable=False, comment="正确答案")
    level = Column(Integer, nullable=False, comment="难度等级")
    wrong_count = Column(Integer, default=1, comment="错误次数")
    last_wrong_time = Column(DateTime, comment="最后错误时间")
    is_mastered = Column(Integer, default=0, comment="是否已掌握")
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # 关系
    child = relationship("Child", back_populates="wrong_questions")
    question = relationship("Question", back_populates="wrong_questions")
