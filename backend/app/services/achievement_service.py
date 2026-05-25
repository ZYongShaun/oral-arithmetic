from sqlalchemy.orm import Session
from datetime import datetime
from typing import Dict, List, Optional

from app.models.child import Child
from app.models.achievement import Achievement, ChildAchievement
from app.models.practice import Practice


class AchievementService:
    """成就系统服务"""
    
    # 成就定义
    ACHIEVEMENTS = {
        # 练习成就
        'first_practice': {
            'key': 'first_practice',
            'name': '初次尝试',
            'description': '完成第 1 次练习',
            'category': 'practice',
            'requirement': 1,
            'stars': 5,
            'badge': '🎯'
        },
        'practice_10': {
            'key': 'practice_10',
            'name': '坚持不懈',
            'description': '累计完成 10 次练习',
            'category': 'practice',
            'requirement': 10,
            'stars': 10,
            'badge': '🌟'
        },
        'practice_50': {
            'key': 'practice_50',
            'name': '练习达人',
            'description': '累计完成 50 次练习',
            'category': 'practice',
            'requirement': 50,
            'stars': 25,
            'badge': '⭐'
        },
        'practice_100': {
            'key': 'practice_100',
            'name': '口算大师',
            'description': '累计完成 100 次练习',
            'category': 'practice',
            'requirement': 100,
            'stars': 50,
            'badge': '🏆'
        },
        'perfect_performance': {
            'key': 'perfect_performance',
            'name': '完美表现',
            'description': '单次练习 100% 正确',
            'category': 'practice',
            'requirement': 1,
            'stars': 5,
            'badge': '💯'
        },
        # 连胜成就
        'streak_3': {
            'key': 'streak_3',
            'name': '小火苗',
            'description': '连胜 3 次',
            'category': 'streak',
            'requirement': 3,
            'stars': 10,
            'badge': '🔥'
        },
        'streak_7': {
            'key': 'streak_7',
            'name': '热情似火',
            'description': '连胜 7 次',
            'category': 'streak',
            'requirement': 7,
            'stars': 25,
            'badge': '🔥🔥'
        },
        'streak_15': {
            'key': 'streak_15',
            'name': '势不可挡',
            'description': '连胜 15 次',
            'category': 'streak',
            'requirement': 15,
            'stars': 50,
            'badge': '🔥🔥🔥'
        },
        'streak_30': {
            'key': 'streak_30',
            'name': '传奇之路',
            'description': '连胜 30 次',
            'category': 'streak',
            'requirement': 30,
            'stars': 100,
            'badge': '💎'
        },
        # 难度成就
        'level_10': {
            'key': 'level_10',
            'name': '入门新手',
            'description': '完成 10 以内难度练习',
            'category': 'difficulty',
            'requirement': 1,
            'stars': 5,
            'badge': '🎓'
        },
        'level_20': {
            'key': 'level_20',
            'name': '进步之星',
            'description': '完成 20 以内难度练习',
            'category': 'difficulty',
            'requirement': 1,
            'stars': 10,
            'badge': '🌠'
        },
        'level_50': {
            'key': 'level_50',
            'name': '进阶高手',
            'description': '完成 50 以内难度练习',
            'category': 'difficulty',
            'requirement': 1,
            'stars': 20,
            'badge': '🚀'
        },
        'level_100': {
            'key': 'level_100',
            'name': '挑战王者',
            'description': '完成 100 以内难度练习',
            'category': 'difficulty',
            'requirement': 1,
            'stars': 30,
            'badge': '👑'
        },
        # 速度成就
        'speed_fast': {
            'key': 'speed_fast',
            'name': '神速',
            'description': '单次练习平均用时 < 3 秒',
            'category': 'speed',
            'requirement': 1,
            'stars': 15,
            'badge': '⚡'
        },
        'speed_super': {
            'key': 'speed_super',
            'name': '闪电侠',
            'description': '单次练习平均用时 < 2 秒',
            'category': 'speed',
            'requirement': 1,
            'stars': 25,
            'badge': '⚡⚡'
        }
    }
    
    @staticmethod
    def check_and_unlock_achievements(
        db: Session,
        child_id: int,
        practice: Practice
    ) -> List[Dict]:
        """
        检查并解锁成就
        
        Args:
            db: 数据库会话
            child_id: 孩子ID
            practice: 练习记录
            
        Returns:
            新解锁的成就列表
        """
        unlocked = []
        
        # 检查练习成就
        practice_unlocked = AchievementService._check_practice_achievements(
            db, child_id, practice
        )
        unlocked.extend(practice_unlocked)
        
        # 检查难度成就
        difficulty_unlocked = AchievementService._check_difficulty_achievements(
            db, child_id, practice
        )
        unlocked.extend(difficulty_unlocked)
        
        # 检查速度成就
        speed_unlocked = AchievementService._check_speed_achievements(
            db, child_id, practice
        )
        unlocked.extend(speed_unlocked)
        
        return unlocked
    
    @staticmethod
    def _check_practice_achievements(
        db: Session,
        child_id: int,
        practice: Practice
    ) -> List[Dict]:
        """检查练习相关成就"""
        unlocked = []
        
        # 检查总练习次数
        total_practices = db.query(Practice).filter(
            Practice.child_id == child_id,
            Practice.completed_at != None
        ).count()
        
        practice_milestones = [1, 10, 50, 100]
        for milestone in practice_milestones:
            if total_practices >= milestone:
                key = f'practice_{milestone}'
                if not AchievementService._is_unlocked(db, child_id, key):
                    achievement_data = AchievementService.ACHIEVEMENTS[key]
                    unlocked_achievement = AchievementService._unlock_achievement(
                        db, child_id, achievement_data
                    )
                    if unlocked_achievement:
                        unlocked.append(unlocked_achievement)
        
        # 检查完美表现
        if practice.accuracy >= 100:
            key = 'perfect_performance'
            if not AchievementService._is_unlocked(db, child_id, key):
                achievement_data = AchievementService.ACHIEVEMENTS[key]
                unlocked_achievement = AchievementService._unlock_achievement(
                    db, child_id, achievement_data
                )
                if unlocked_achievement:
                    unlocked.append(unlocked_achievement)
        
        return unlocked
    
    @staticmethod
    def _check_difficulty_achievements(
        db: Session,
        child_id: int,
        practice: Practice
    ) -> List[Dict]:
        """检查难度相关成就"""
        unlocked = []
        
        difficulty_map = {
            1: 'level_10',
            2: 'level_20',
            3: 'level_50',
            4: 'level_100'
        }
        
        key = difficulty_map.get(practice.difficulty_level)
        if key and not AchievementService._is_unlocked(db, child_id, key):
            achievement_data = AchievementService.ACHIEVEMENTS[key]
            unlocked_achievement = AchievementService._unlock_achievement(
                db, child_id, achievement_data
            )
            if unlocked_achievement:
                unlocked.append(unlocked_achievement)
        
        return unlocked
    
    @staticmethod
    def _check_speed_achievements(
        db: Session,
        child_id: int,
        practice: Practice
    ) -> List[Dict]:
        """检查速度相关成就"""
        unlocked = []
        
        avg_time = practice.time_spent / 20  # 假设每套题20道
        
        if avg_time < 2:
            key = 'speed_super'
        elif avg_time < 3:
            key = 'speed_fast'
        else:
            key = None
        
        if key and not AchievementService._is_unlocked(db, child_id, key):
            achievement_data = AchievementService.ACHIEVEMENTS[key]
            unlocked_achievement = AchievementService._unlock_achievement(
                db, child_id, achievement_data
            )
            if unlocked_achievement:
                unlocked.append(unlocked_achievement)
        
        return unlocked
    
    @staticmethod
    def _check_streak_achievements(
        db: Session,
        child_id: int,
        streak_count: int
    ) -> List[Dict]:
        """检查连胜相关成就"""
        unlocked = []
        
        streak_milestones = [3, 7, 15, 30]
        for milestone in streak_milestones:
            if streak_count >= milestone:
                key = f'streak_{milestone}'
                if not AchievementService._is_unlocked(db, child_id, key):
                    achievement_data = AchievementService.ACHIEVEMENTS[key]
                    unlocked_achievement = AchievementService._unlock_achievement(
                        db, child_id, achievement_data
                    )
                    if unlocked_achievement:
                        unlocked.append(unlocked_achievement)
        
        return unlocked
    
    @staticmethod
    def _is_unlocked(db: Session, child_id: int, achievement_key: str) -> bool:
        """检查成就是否已解锁"""
        existing = db.query(ChildAchievement).join(Achievement).filter(
            ChildAchievement.child_id == child_id,
            Achievement.achievement_key == achievement_key
        ).first()
        
        return existing is not None
    
    @staticmethod
    def _unlock_achievement(
        db: Session,
        child_id: int,
        achievement_data: Dict
    ) -> Optional[Dict]:
        """解锁成就"""
        # 创建成就记录
        achievement = db.query(Achievement).filter(
            Achievement.achievement_key == achievement_data['key']
        ).first()
        
        if not achievement:
            achievement = Achievement(
                achievement_key=achievement_data['key'],
                name=achievement_data['name'],
                description=achievement_data['description'],
                category=achievement_data['category'],
                requirement=achievement_data['requirement'],
                reward_stars=achievement_data['stars'],
                badge_icon=achievement_data['badge']
            )
            db.add(achievement)
            db.flush()
        
        # 创建孩子成就记录
        child_achievement = ChildAchievement(
            child_id=child_id,
            achievement_id=achievement.id,
            progress=achievement_data['requirement'],
            is_completed=True,
            completed_at=datetime.utcnow()
        )
        db.add(child_achievement)
        
        # 奖励星星
        from app.services.star_service import StarService
        StarService.award_achievement_stars(
            db=db,
            child_id=child_id,
            achievement_name=achievement_data['name'],
            stars=achievement_data['stars']
        )
        
        db.commit()
        
        return {
            'achievement_key': achievement_data['key'],
            'name': achievement_data['name'],
            'description': achievement_data['description'],
            'stars': achievement_data['stars'],
            'badge': achievement_data['badge'],
            'unlocked_at': child_achievement.completed_at.isoformat()
        }
    
    @staticmethod
    def get_all_achievements(db: Session) -> List[Dict]:
        """获取所有成就定义"""
        return [
            {
                'key': key,
                'name': data['name'],
                'description': data['description'],
                'category': data['category'],
                'stars': data['stars'],
                'badge': data['badge'],
                'requirement': data['requirement']
            }
            for key, data in AchievementService.ACHIEVEMENTS.items()
        ]
    
    @staticmethod
    def get_child_achievements(db: Session, child_id: int) -> List[Dict]:
        """获取孩子的成就列表"""
        achievements = db.query(ChildAchievement).join(Achievement).filter(
            ChildAchievement.child_id == child_id,
            ChildAchievement.is_completed == True
        ).order_by(ChildAchievement.completed_at.desc()).all()
        
        return [
            {
                'achievement_key': ca.achievement.achievement_key,
                'name': ca.achievement.name,
                'description': ca.achievement.description,
                'category': ca.achievement.category,
                'stars': ca.achievement.reward_stars,
                'badge': ca.achievement.badge_icon,
                'unlocked_at': ca.completed_at.isoformat() if ca.completed_at else None
            }
            for ca in achievements
        ]
    
    @staticmethod
    def get_achievement_progress(db: Session, child_id: int) -> Dict:
        """获取成就进度"""
        all_achievements = AchievementService.get_all_achievements()
        unlocked = AchievementService.get_child_achievements(db, child_id)
        
        unlocked_keys = {a['achievement_key'] for a in unlocked}
        
        progress = []
        for achievement in all_achievements:
            is_unlocked = achievement['key'] in unlocked_keys
            
            progress_data = {
                **achievement,
                'is_unlocked': is_unlocked
            }
            
            # 未解锁的获取进度
            if not is_unlocked:
                current_progress = AchievementService._get_current_progress(
                    db, child_id, achievement
                )
                progress_data['progress'] = current_progress
                progress_data['percentage'] = min(
                    100, (current_progress / achievement['requirement']) * 100
                )
            
            progress.append(progress_data)
        
        total_count = len(all_achievements)
        unlocked_count = len(unlocked_keys)
        
        return {
            'achievements': progress,
            'total_count': total_count,
            'unlocked_count': unlocked_count,
            'completion_percentage': (unlocked_count / total_count) * 100 if total_count > 0 else 0
        }
    
    @staticmethod
    def _get_current_progress(db: Session, child_id: int, achievement: Dict) -> int:
        """获取当前进度"""
        key = achievement['key']
        category = achievement['category']
        
        if category == 'practice':
            if key == 'first_practice':
                return 0  # 需要一次性检查
            
            requirement = achievement['requirement']
            total_practices = db.query(Practice).filter(
                Practice.child_id == child_id,
                Practice.completed_at != None
            ).count()
            
            return total_practices
        
        if category == 'streak':
            from app.services.streak_service import StreakService
            streak_info = StreakService.get_streak_info(db, child_id)
            return streak_info['current_streak']
        
        if category == 'difficulty':
            difficulty_map = {1: 10, 2: 20, 3: 50, 4: 100}
            # 检查是否有该难度的练习
            for level, difficulty in difficulty_map.items():
                if key == f'level_{difficulty}':
                    existing = db.query(Practice).filter(
                        Practice.child_id == child_id,
                        Practice.difficulty_level == level,
                        Practice.completed_at != None
                    ).first()
                    return 1 if existing else 0
        
        if category == 'speed':
            # 获取最快用时
            practice = db.query(Practice).filter(
                Practice.child_id == child_id,
                Practice.completed_at != None
            ).order_by(Practice.time_spent.asc()).first()
            
            if practice:
                avg_time = practice.time_spent / 20
                if avg_time < 2:
                    return 2  # 超级闪电
                elif avg_time < 3:
                    return 1  # 神速
            
            return 0
        
        return 0
