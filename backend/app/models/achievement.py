"""
数据库模型 - 成就和排行榜
"""
from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime


class Achievement(Base):
    """成就表（系统预定义）"""
    __tablename__ = "achievements"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    achievement_key = Column(String(50), unique=True, nullable=False, comment="成就键")
    name = Column(String(100), nullable=False, comment="成就名称")
    description = Column(String(255), comment="成就描述")
    category = Column(String(20), comment="分类：practice/streak/difficulty/speed")
    requirement = Column(Integer, comment="达成条件数值")
    reward_stars = Column(Integer, default=0, comment="奖励星星数")
    badge_icon = Column(String(255), comment="徽章图标URL")
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    
    # 关系
    child_achievements = relationship("ChildAchievement", back_populates="achievement")


class ChildAchievement(Base):
    """孩子成就进度表"""
    __tablename__ = "child_achievements"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    child_id = Column(Integer, ForeignKey("children.id"), nullable=False)
    achievement_id = Column(Integer, ForeignKey("achievements.id"), nullable=False)
    progress = Column(Integer, default=0, comment="当前进度")
    is_completed = Column(Integer, default=0, comment="是否已完成")
    completed_at = Column(TIMESTAMP, nullable=True, comment="完成时间")
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    
    # 关系
    child = relationship("Child")
    achievement = relationship("Achievement", back_populates="child_achievements")
    
    __table_args__ = (
        UniqueConstraint('child_id', 'achievement_id', name='uk_child_achievement'),
        {'extend_existing': True}
    )


class Leaderboard(Base):
    """排行榜表"""
    __tablename__ = "leaderboards"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    season_week = Column(Integer, nullable=False, comment="赛季周数")
    child_id = Column(Integer, ForeignKey("children.id"), nullable=False)
    group_level = Column(Integer, default=1, comment="小组等级：1-青铜 2-白银...")
    weekly_stars = Column(Integer, default=0, comment="本周获得星星")
    rank = Column(Integer, nullable=True, comment="当前排名")
    is_promoted = Column(Integer, default=0, comment="是否晋级")
    is_demoted = Column(Integer, default=0, comment="是否降级")
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    child = relationship("Child")
    
    __table_args__ = (
        UniqueConstraint('child_id', 'season_week', name='uk_child_week'),
        {'extend_existing': True}
    )


class StarTransaction(Base):
    """星星流水表"""
    __tablename__ = "star_transactions"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    child_id = Column(Integer, ForeignKey("children.id"), nullable=False)
    change_type = Column(String(20), nullable=False, comment="类型：earn/spend")
    source = Column(String(50), nullable=False, comment="来源：practice/task/achievement/ranking/shop")
    stars = Column(Integer, nullable=False, comment="变动数量（正数增加，负数减少）")
    balance_after = Column(Integer, comment="变动后余额")
    description = Column(String(255), comment="描述")
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    
    # 关系
    child = relationship("Child")
