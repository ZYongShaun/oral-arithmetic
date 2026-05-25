"""
练习记录模型
"""
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime


class Practice(Base):
    """练习记录表"""
    __tablename__ = "practices"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    child_id = Column(Integer, ForeignKey("children.id"), nullable=False)
    level = Column(Integer, nullable=False, comment="难度等级")
    total_questions = Column(Integer, default=20, comment="题目总数")
    correct_count = Column(Integer, default=0, comment="正确题数")
    wrong_count = Column(Integer, default=0, comment="错误题数")
    total_time = Column(Integer, comment="总用时（秒）")
    avg_time = Column(Float, comment="平均用时（秒）")
    accuracy = Column(Float, comment="正确率")
    stars_earned = Column(Integer, default=0, comment="本关获得星星")
    start_time = Column(DateTime, nullable=False, comment="开始时间")
    end_time = Column(DateTime, comment="结束时间")
    created_at = Column(DateTime, default=datetime.now)
    
    # 关系
    child = relationship("Child", back_populates="practices")
    details = relationship("PracticeDetail", back_populates="practice", cascade="all, delete-orphan")
