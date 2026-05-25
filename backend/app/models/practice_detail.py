"""
练习详情模型
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime


class PracticeDetail(Base):
    """练习详情表"""
    __tablename__ = "practice_details"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    practice_id = Column(Integer, ForeignKey("practices.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False, comment="题目ID")
    question_text = Column(String(100), nullable=False, comment="题目文本")
    user_answer = Column(Integer, comment="用户答案")
    correct_answer = Column(Integer, nullable=False, comment="正确答案")
    is_correct = Column(Integer, default=0, comment="是否正确")
    answer_time = Column(Integer, comment="答题用时（秒）")
    question_order = Column(Integer, comment="题目序号")
    created_at = Column(DateTime, default=datetime.now)
    
    # 关系
    practice = relationship("Practice", back_populates="details")
    question = relationship("Question", back_populates="practice_details")
