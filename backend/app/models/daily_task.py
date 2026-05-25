"""
每日任务模型
"""
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime


class DailyTask(Base):
    """每日任务表"""
    __tablename__ = "daily_tasks"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    child_id = Column(Integer, ForeignKey("children.id"), nullable=False)
    task_date = Column(Date, nullable=False, comment="任务日期")
    target_count = Column(Integer, default=3, comment="目标次数")
    completed_count = Column(Integer, default=0, comment="已完成次数")
    is_completed = Column(Integer, default=0, comment="是否完成")
    stars_earned = Column(Integer, default=0, comment="获得的星星数")
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # 关系
    child = relationship("Child", back_populates="daily_tasks")
