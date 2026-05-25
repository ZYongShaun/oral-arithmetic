from sqlalchemy.orm import Session
from datetime import date, datetime, timedelta
from typing import Dict, List, Optional
import calendar

from app.models.child import Child
from app.models.leaderboard import Leaderboard
from app.models.practice import Practice


class LeaderboardService:
    """排行榜系统服务"""
    
    # 小组等级定义
    GROUP_LEVELS = {
        1: '青铜组',
        2: '白银组',
        3: '黄金组',
        4: '铂金组',
        5: '钻石组',
        6: '大师组',
        7: '传奇组'
    }
    
    @staticmethod
    def get_current_week() -> int:
        """获取当前周数（从年初开始）"""
        today = date.today()
        week_num = today.isocalendar()[1]
        return week_num
    
    @staticmethod
    def get_or_create_leaderboard(db: Session, child_id: int, week: Optional[int] = None) -> Leaderboard:
        """
        获取或创建排行榜记录
        
        Args:
            db: 数据库会话
            child_id: 孩子ID
            week: 周数，默认当前周
            
        Returns:
            排行榜记录
        """
        if week is None:
            week = LeaderboardService.get_current_week()
        
        leaderboard = db.query(Leaderboard).filter(
            Leaderboard.child_id == child_id,
            Leaderboard.season_week == week
        ).first()
        
        if not leaderboard:
            child = db.query(Child).filter(Child.id == child_id).first()
            if not child:
                raise ValueError("Child not found")
            
            # 根据星星总数确定初始小组
            initial_level = LeaderboardService._calculate_initial_level(child.total_stars)
            
            leaderboard = Leaderboard(
                season_week=week,
                child_id=child_id,
                group_level=initial_level,
                weekly_stars=0,
                rank=0
            )
            db.add(leaderboard)
            db.commit()
            db.refresh(leaderboard)
        
        return leaderboard
    
    @staticmethod
    def update_weekly_stars(
        db: Session,
        child_id: int,
        stars: int,
        week: Optional[int] = None
    ) -> Dict:
        """
        更新本周星星数
        
        Args:
            db: 数据库会话
            child_id: 孩子ID
            stars: 增加的星星数
            week: 周数，默认当前周
            
        Returns:
            更新结果
        """
        if week is None:
            week = LeaderboardService.get_current_week()
        
        leaderboard = LeaderboardService.get_or_create_leaderboard(
            db, child_id, week
        )
        
        leaderboard.weekly_stars += stars
        db.commit()
        db.refresh(leaderboard)
        
        # 重新计算排名
        LeaderboardService._recalculate_rankings(db, week)
        
        return {
            'week': week,
            'weekly_stars': leaderboard.weekly_stars,
            'group_level': leaderboard.group_level,
            'rank': leaderboard.rank
        }
    
    @staticmethod
    def get_current_leaderboard(
        db: Session,
        child_id: int
    ) -> Dict:
        """
        获取当前排行榜信息
        
        Args:
            db: 数据库会话
            child_id: 孩子ID
            
        Returns:
            排行榜信息
        """
        week = LeaderboardService.get_current_week()
        my_Leaderboard = LeaderboardService.get_or_create_leaderboard(
            db, child_id, week
        )
        
        # 获取小组排名
        group_rankings = db.query(Leaderboard).filter(
            Leaderboard.season_week == week,
            Leaderboard.group_level == my_Leaderboard.group_level
        ).order_by(
            Leaderboard.weekly_stars.desc()
        ).all()
        
        my_rank = next((i + 1 for i, lb in enumerate(group_rankings) 
                       if lb.child_id == child_id), 0)
        
        # 小组信息
        group_info = {
            'level': my_Leaderboard.group_level,
            'name': LeaderboardService.GROUP_LEVELS.get(my_Leaderboard.group_level, ''),
            'total_users': len(group_rankings),
            'my_rank': my_rank,
            'my_stars': my_Leaderboard.weekly_stars
        }
        
        # 前几名用户
        top_users = []
        for i, lb in enumerate(group_rankings[:10]):
            child = db.query(Child).filter(Child.id == lb.child_id).first()
            top_users.append({
                'rank': i + 1,
                'child_name': child.name if child else '未知',
                'weekly_stars': lb.weekly_stars,
                'is_me': lb.child_id == child_id
            })
        
        return {
            'week': week,
            'group_info': group_info,
            'top_users': top_users,
            'stars_earned': my_Leaderboard.weekly_stars
        }
    
    @staticmethod
    def get_leaderboard_history(
        db: Session,
        child_id: int,
        weeks: int = 8
    ) -> List[Dict]:
        """
        获取历史排名记录
        
        Args:
            db: 数据库会话
            child_id: 孩子ID
            weeks: 查询周数
            
        Returns:
            历史记录列表
        """
        current_week = LeaderboardService.get_current_week()
        start_week = current_week - weeks
        
        records = db.query(Leaderboard).filter(
            Leaderboard.child_id == child_id,
            Leaderboard.season_week >= start_week,
            Leaderboard.season_week <= current_week
        ).order_by(
            Leaderboard.season_week.desc()
        ).all()
        
        return [
            {
                'week': rec.season_week,
                'group_level': rec.group_level,
                'group_name': LeaderboardService.GROUP_LEVELS.get(rec.group_level, ''),
                'weekly_stars': rec.weekly_stars,
                'rank': rec.rank,
                'is_promoted': rec.is_promoted,
                'is_demoted': rec.is_demoted
            }
            for rec in records
        ]
    
    @staticmethod
    def weekly_reset(db: Session):
        """
        周度重置，处理小组晋级和降级
        
        Args:
            db: 数据库会话
        """
        current_week = LeaderboardService.get_current_week()
        prev_week = current_week - 1
        
        # 获取上周所有排名记录
        prev_records = db.query(Leaderboard).filter(
            Leaderboard.season_week == prev_week
        ).all()
        
        # 按小组分组处理
        for level in range(1, 8):  # 7个小组等级
            level_records = [
                r for r in prev_records if r.group_level == level
            ]
            
            if not level_records:
                continue
            
            # 按星星排序
            level_records.sort(key=lambda x: x.weekly_stars, reverse=True)
            
            # 前5名晋级
            for i, record in enumerate(level_records[:5]):
                if i < 5 and level < 7:
                    # 创建新周记录，小组+1
                    new_record = Leaderboard(
                        season_week=current_week,
                        child_id=record.child_id,
                        group_level=level + 1,
                        weekly_stars=0,
                        rank=0,
                        is_promoted=True,
                        is_demoted=False
                    )
                    db.add(new_record)
                    
                    # 发放周排名奖励
                    if i == 0:
                        LeaderboardService._award_ranking_prize(db, record.child_id, current_week, 1)
                    elif i < 3:
                        LeaderboardService._award_ranking_prize(db, record.child_id, current_week, i + 1)
            
            # 后3名降级
            for record in level_records[-3:]:
                if level > 1:
                    new_record = Leaderboard(
                        season_week=current_week,
                        child_id=record.child_id,
                        group_level=level - 1,
                        weekly_stars=0,
                        rank=0,
                        is_promoted=False,
                        is_demoted=True
                    )
                    db.add(new_record)
            
            # 中间位置保持原小组
            for record in level_records[5:-3]:
                new_record = Leaderboard(
                    season_week=current_week,
                    child_id=record.child_id,
                    group_level=level,
                    weekly_stars=0,
                    rank=0,
                    is_promoted=False,
                    is_demoted=False
                )
                db.add(new_record)
        
        db.commit()
    
    @staticmethod
    def _recalculate_rankings(db: Session, week: int):
        """
        重新计算某个周的排名
        
        Args:
            db: 数据库会话
            week: 周数
        """
        # 按小组分别计算排名
        for level in range(1, 8):
            records = db.query(Leaderboard).filter(
                Leaderboard.season_week == week,
                Leaderboard.group_level == level
            ).order_by(
                Leaderboard.weekly_stars.desc()
            ).all()
            
            for rank, record in enumerate(records):
                record.rank = rank + 1
        
        db.commit()
    
    @staticmethod
    def _calculate_initial_level(total_stars: int) -> int:
        """
        根据星星总数计算初始小组等级
        
        Args:
            total_stars: 总星星数
            
        Returns:
            小组等级
        """
        if total_stars >= 500:
            return 7  # 传奇组
        elif total_stars >=300:
            return 6  # 大师组
        elif total_stars >= 200:
            return 5  # 钻石组
        elif total_stars >= 100:
            return 4  # 铂金组
        elif total_stars >= 50:
            return 3  # 黄金组
        elif total_stars >= 20:
            return 2  # 白银组
        else:
            return 1  # 青铜组
    
    @staticmethod
    def _award_ranking_prize(
        db: Session,
        child_id: int,
        week: int,
        rank: int
    ):
        """
        发放周排名奖励
        
        Args:
            db: 数据库会话
            child_id: 孩子ID
            week: 周数
            rank: 排名
        """
        from app.services.star_service import StarService
        
        if rank == 1:
            stars = 100
        elif rank in [2, 3]:
            stars = 50
        else:
            return
        
        StarService.award_ranking_stars(
            db=db,
            child_id=child_id,
            rank=rank,
            week=week
        )
    
    @staticmethod
    def get_group_info(db: Session, group_level: int, week: Optional[int] = None) -> Dict:
        """
        获取小组信息
        
        Args:
            db: 数据库会话
            group_level: 小组等级
            week: 周数，默认当前周
            
        Returns:
            小组信息
        """
        if week is None:
            week = LeaderboardService.get_current_week()
        
        records = db.query(Leaderboard).filter(
            Leaderboard.season_week == week,
            Leaderboard.group_level == group_level
        ).order_by(
            Leaderboard.weekly_stars.desc()
        ).all()
        
        users_info = []
        for rank, record in enumerate(records):
            child = db.query(Child).filter(Child.id == record.child_id).first()
            users_info.append({
                'rank': rank + 1,
                'child_id': record.child_id,
                'child_name': child.name if child else '未知',
                'weekly_stars': record.weekly_stars,
                'is_promoted': record.is_promoted,
                'is_demoted': record.is_demoted
            })
        
        return {
            'week': week,
            'group_level': group_level,
            'group_name': LeaderboardService.GROUP_LEVELS.get(group_level, ''),
            'total_users': len(records),
            'users': users_info
        }
    
    @staticmethod
    def get_all_groups(db: Session, week: Optional[int] = None) -> List[Dict]:
        """
        获取所有小组信息
        
        Args:
            db: 数据库会话
            week: 周数，默认当前周
            
        Returns:
            小组列表
        """
        if week is None:
            week = LeaderboardService.get_current_week()
        
        groups = []
        for level in range(1, 8):
            group_info = LeaderboardService.get_group_info(db, level, week)
            groups.append(group_info)
        
        return groups
