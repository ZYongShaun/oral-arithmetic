# -*- coding: utf-8 -*-
# 导入所有模型，确保 Base 正确配置

# 先导入基础模型
from app.core.database import Base

# 然后按依赖顺序导入模型
from app.models.user import User, Admin, SystemConfig
from app.models.child import Child
from app.models.practice import Practice
from app.models.practice_detail import PracticeDetail
from app.models.wrong_question import WrongQuestion
from app.models.daily_task import DailyTask
from app.models.streak import Streak
from app.models.question import Question
from app.models.achievement import Achievement, ChildAchievement, Leaderboard, StarTransaction

__all__ = [
    "Base",
    "User",
    "Child", 
    "Admin",
    "SystemConfig",
    "Question",
    "Practice",
    "PracticeDetail",
    "WrongQuestion",
    "DailyTask",
    "Streak",
    "Achievement",
    "ChildAchievement",
    "Leaderboard",
    "StarTransaction"
]
