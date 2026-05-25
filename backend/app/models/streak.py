"""
数据库模型 - 连胜记录
"""
from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime


class Streak(Base):
    """连胜记录表"""
    __tablename__ = "streaks"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    child_id = Column(Integer, ForeignKey("children.id"), nullable=False, unique=True)
    current_streak = Column(Integer, default=0, comment="当前连胜次数")
    best_streak = Column(Integer, default=0, comment="历史最高连胜")
    last_practice_at = Column(TIMESTAMP, nullable=True, comment="上次练习时间")
    shields = Column(Integer, default=0, comment="保护罩数量")
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    child = relationship("Child", back_populates="streak")
