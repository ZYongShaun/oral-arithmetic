from sqlalchemy.orm import Session
from datetime import date, datetime
from typing import Dict, Optional
import calendar

from app.models.user import SystemConfig
from app.models.child import Child
from app.models.practice import Practice
from app.models.daily_task import DailyTask


class DailyTaskService:
    """每日任务系统服务"""
    
    @staticmethod
    def get_or_create_daily_task(db: Session, child_id: int) -> DailyTask:
        """
        获取或创建今日任务
        
        Args:
            db: 数据库会话
            child_id: 孩子ID
            
        Returns:
            今日任务对象
        """
        today = date.today()
        task = db.query(DailyTask).filter(
            DailyTask.child_id == child_id,
            DailyTask.task_date == today
        ).first()
        
        if not task:
            target_count = DailyTaskService._get_config_value(db, 'daily_task_target', 3)
            task = DailyTask(
                child_id=child_id,
                task_date=today,
                target_count=target_count,
                completed_count=0,
                is_completed=False,
                stars_earned=0
            )
            db.add(task)
            db.commit()
            db.refresh(task)
        
        return task
    
    @staticmethod
    def update_practice_count(
        db: Session,
        child_id: int,
        practice_id: int
    ) -> Dict:
        """
        更新练习次数
        
        Args:
            db: 数据库会话
            child_id: 孩子ID
            practice_id: 练习ID
            
        Returns:
            更新后的任务信息
        """
        today = date.today()
        task = db.query(DailyTask).filter(
            DailyTask.child_id == child_id,
            DailyTask.task_date == today
        ).first()
        
        # 如果没有今日任务，创建一个
        if not task:
            task = DailyTaskService.get_or_create_daily_task(db, child_id)
        
        # 检查该练习是否已经计入
        practice = db.query(Practice).filter(Practice.id == practice_id).first()
        if not practice:
            raise Exception("Practice not found")
        
        # 增加完成次数
        task.completed_count += 1
        
        # 检查是否完成任务
        bonus_stars = 0
        if task.completed_count >= task.target_count and not task.is_completed:
            task.is_completed = True
            
            # 发放任务奖励
            reward_stars = int(DailyTaskService._get_config_value(db, 'daily_task_stars', 10))
            task.stars_earned = reward_stars
            bonus_stars = reward_stars
            
            # 更新孩子的星星总数
            child = db.query(Child).filter(Child.id == child_id).first()
            if child:
                child.total_stars += reward_stars
        
        task.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(task)
        
        return {
            'target_count': task.target_count,
            'completed_count': task.completed_count,
            'is_completed': task.is_completed,
            'stars_earned': task.stars_earned,
            'bonus_stars': bonus_stars,
            'progress_percentage': min(100, (task.completed_count / task.target_count) * 100)
        }
    
    @staticmethod
    def get_daily_task_info(db: Session, child_id: int) -> Dict:
        """
        获取今日任务信息
        
        Args:
            db: 数据库会话
            child_id: 孩子ID
            
        Returns:
            今日任务信息
        """
        task = DailyTaskService.get_or_create_daily_task(db, child_id)
        
        return {
            'task_date': task.task_date.isoformat(),
            'target_count': task.target_count,
            'completed_count': task.completed_count,
            'is_completed': task.is_completed,
            'stars_earned': task.stars_earned,
            'progress_percentage': min(100, (task.completed_count / task.target_count) * 100)
        }
    
    @staticmethod
    def get_weekly_progress(db: Session, child_id: int) -> Dict:
        """
        获取本周任务进度
        
        Args:
            db: 数据库会话
            child_id: 孩子ID
            
        Returns:
            本周任务信息
        """
        today = date.today()
        days = [(today - datetime.timedelta(days=i)).date() for i in range(7)]
        
        tasks_info = []
        for day in days:
            task = db.query(DailyTask).filter(
                DailyTask.child_id == child_id,
                DailyTask.task_date == day
            ).first()
            
            if task:
                tasks_info.append({
                    'date': day.isoformat(),
                    'target_count': task.target_count,
                    'completed_count': task.completed_count,
                    'is_completed': task.is_completed
                })
            else:
                tasks_info.append({
                    'date': day.isoformat(),
                    'target_count': 3,
                    'completed_count': 0,
                    'is_completed': False
                })
        
        completed_days = sum(1 for t in tasks_info if t['is_completed'])
        
        return {
            'week_start': days[6].isoformat(),
            'week_end': days[0].isoformat(),
            'tasks': tasks_info,
            'completed_days': completed_days,
            'total_days': len(tasks_info)
        }
    
    @staticmethod
    def get_monthly_stats(db: Session, child_id: int, year: int, month: int) -> Dict:
        """
        获取月度统计
        
        Args:
            db: 数据库会话
            child_id: 孩子ID
            year: 年份
            month: 月份
            
        Returns:
            月度统计信息
        """
        # 获取该月的天数
        days_in_month = calendar.monthrange(year, month)[1]
        
        month_start = date(year, month, 1)
        month_end = date(year, month, days_in_month)
        
        tasks = db.query(DailyTask).filter(
            DailyTask.child_id == child_id,
            DailyTask.task_date >= month_start,
            DailyTask.task_date <= month_end
        ).all()
        
        total_tasks = len(tasks)
        completed_tasks = sum(1 for t in tasks if t.is_completed)
        total_stars_earned = sum(t.stars_earned for t in tasks)
        
        return {
            'year': year,
            'month': month,
            'total_days': days_in_month,
            'active_days': total_tasks,
            'completed_days': completed_tasks,
            'completion_rate': (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0,
            'total_stars_earned': total_stars_earned
        }
    
    @staticmethod
    def _get_config_value(db: Session, key: str, default: any) -> any:
        """
        获取配置值
        
        Args:
            db: 数据库会话
            key: 配置键
            default: 默认值
            
        Returns:
            配置值
        """
        config = db.query(SystemConfig).filter(
            SystemConfig.config_key == key
        ).first()
        
        if config:
            try:
                return int(config.config_value)
            except ValueError:
                return config.config_value
        
        return default
    
    @staticmethod
    def expire_old_tasks(db: Session):
        """
        过期旧任务（此方法应该在定时任务中调用）
        
        Args:
            db: 数据库会话
        """
        yesterday = date.today()
        old_tasks = db.query(DailyTask).filter(
            DailyTask.task_date < yesterday
        ).all()
        
        for task in old_tasks:
            if not task.is_completed:
                task.is_expired = True
        
        db.commit()
