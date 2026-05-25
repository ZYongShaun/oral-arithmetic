from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Dict, Optional

from app.models.child import Child
from app.models.streak import Streak
from app.models.practice import Practice


class StreakService:
    """连胜系统服务"""
    
    @staticmethod
    def check_and_update_streak(
        db: Session,
        child_id: int,
        accuracy: float
    ) -> Dict:
        """
        检查并更新连胜记录
        
        Args:
            db: 数据库会话
            child_id: 孩子ID
            accuracy: 正确率
            
        Returns:
            更新后的连胜信息和状态
        """
        streak = db.query(Streak).filter(Streak.child_id == child_id).first()
        
        if not streak:
            streak = Streak(
                child_id=child_id,
                current_streak=0,
                best_streak=0,
                shields=0
            )
            db.add(streak)
            db.commit()
            db.refresh(streak)
        
        is_streak_broken = False
        is_shield_used = False
        new_streak = streak.current_streak
        
        if accuracy < 0.6:
            if streak.shields > 0:
                is_shield_used = True
                streak.shields -= 1
            else:
                is_streak_broken = True
                new_streak = 0
        else:
            new_streak = streak.current_streak + 1
        
        streak.current_streak = new_streak
        streak.last_practice_at = datetime.utcnow()
        
        if new_streak > streak.best_streak:
            streak.best_streak = new_streak
        
        db.commit()
        db.refresh(streak)
        
        return {
            'current_streak': streak.current_streak,
            'best_streak': streak.best_streak,
            'shields': streak.shields,
            'is_streak_broken': is_streak_broken,
            'is_shield_used': is_shield_used,
            'milestone_reached': StreakService._check_milestone(new_streak)
        }
    
    @staticmethod
    def handle_practice_exit(db: Session, child_id: int) -> Dict:
        """
        处理练习中途退出
        
        Args:
            db: 数据库会话
            child_id: 孩子ID
            
        Returns:
            是否中断连胜
        """
        streak = db.query(Streak).filter(Streak.child_id == child_id).first()
        
        if not streak:
            return {'is_streak_broken': False, 'current_streak': 0}
        
        if streak.shields > 0:
            streak.shields -= 1
            db.commit()
            db.refresh(streak)
            return {
                'is_streak_broken': False,
                'is_shield_used': True,
                'current_streak': streak.current_streak,
                'shields': streak.shields
            }
        else:
            streak.current_streak = 0
            db.commit()
            db.refresh(streak)
            return {
                'is_streak_broken': True,
                'is_shield_used': False,
                'current_streak': 0,
                'shields': 0
            }
    
    @staticmethod
    def use_shield(db: Session, child_id: int) -> Dict:
        """
        主动使用保护罩
        
        Args:
            db: 数据库会话
            child_id: 孩子ID
            
        Returns:
            使用结果
        """
        streak = db.query(Streak).filter(Streak.child_id == child_id).first()
        
        if not streak or streak.shields <= 0:
            return {
                'success': False,
                'message': 'No shields available'
            }
        
        streak.shields -= 1
        db.commit()
        db.refresh(streak)
        
        return {
            'success': True,
            'shields_remaining': streak.shields
        }
    
    @staticmethod
    def get_streak_info(db: Session, child_id: int) -> Dict:
        """
        获取连胜信息
        
        Args:
            db: 数据库会话
            child_id: 孩子ID
            
        Returns:
            连胜信息
        """
        streak = db.query(Streak).filter(Streak.child_id == child_id).first()
        
        if not streak:
            return {
                'current_streak': 0,
                'best_streak': 0,
                'shields': 0,
                'last_practice_at': None
            }
        
        return {
            'current_streak': streak.current_streak,
            'best_streak': streak.best_streak,
            'shields': streak.shields,
            'last_practice_at': streak.last_practice_at.isoformat() if streak.last_practice_at else None
        }
    
    @staticmethod
    def _check_milestone(streak_count: int) -> Optional[Dict]:
        """
        检查是否达到里程碑
        
        Args:
            streak_count: 连胜次数
            
        Returns:
            里程碑信息或None
        """
        milestones = {
            3: {'badge': '青铜徽章', 'stars': 10, 'name': '小火苗'},
            7: {'badge': '白银徽章', 'stars': 25, 'name': '热情似火'},
            15: {'badge': '黄金徽章', 'stars': 50, 'name': '势不可挡'},
            30: {'badge': '钻石徽章', 'stars': 100, 'name': '传奇之路'},
            50: {'badge': '王者徽章', 'stars': 200, 'name': '传奇之路'},
            100: {'badge': '传奇徽章', 'stars': 500, 'name': '不朽传奇'},
        }
        
        return milestones.get(streak_count)
    
    @staticmethod
    def get_milestones() -> list:
        """
        获取所有里程碑
        
        Returns:
            里程碑列表
        """
        return [
            {
                'streak_count': 3,
                'badge': '青铜徽章',
                'stars': 10,
                'name': '小火苗',
                'icon': '🥉'
            },
            {
                'streak_count': 7,
                'badge': '白银徽章',
                'stars': 25,
                'name': '热情似火',
                'icon': '🥈'
            },
            {
                'streak_count': 15,
                'badge': '黄金徽章',
                'stars': 50,
                'name': '势不可挡',
                'icon': '🥇'
            },
            {
                'streak_count': 30,
                'badge': '钻石徽章',
                'stars': 100,
                'name': '传奇之路',
                'icon': '💎'
            },
            {
                'streak_count': 50,
                'badge': '王者徽章',
                'stars': 200,
                'name': '传奇之路',
                'icon': '👑'
            },
            {
                'streak_count': 100,
                'badge': '传奇徽章',
                'stars': 500,
                'name': '不朽传奇',
                'icon': '🏆'
            }
        ]
