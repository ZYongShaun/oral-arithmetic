from sqlalchemy.orm import Session
from datetime import datetime
from typing import Dict, List, Optional

from app.models.child import Child
from app.models.practice import Practice
from app.models.achievement import StarTransaction
from app.models.user import SystemConfig


class StarService:
    """星星经济系统服务"""
    
    @staticmethod
    def get_star_balance(db: Session, child_id: int) -> Dict:
        """
        获取星星余额
        
        Args:
            db: 数据库会话
            child_id: 孩子ID
            
        Returns:
            星星余额信息
        """
        child = db.query(Child).filter(Child.id == child_id).first()
        
        if not child:
            return {
                'total_stars': 0,
                'available_stars': 0
            }
        
        return {
            'total_stars': child.total_stars,
            'available_stars': child.total_stars
        }
    
    @staticmethod
    def award_practice_stars(
        db: Session,
        child_id: int,
        accuracy: float,
        practice_id: int
    ) -> Dict:
        """
        发放练习奖励星星
        
        Args:
            db: 数据库会话
            child_id: 孩子ID
            accuracy: 正确率
            practice_id: 练习ID
            
        Returns:
            奖励信息
        """
        # 根据正确率计算星星奖励
        if accuracy >= 1.0:
            stars = 3
        elif accuracy >= 0.8:
            stars = 2
        elif accuracy >= 0.6:
            stars = 1
        else:
            stars = 0
        
        if stars > 0:
            StarService._add_stars(
                db=db,
                child_id=child_id,
                stars=stars,
                source='practice',
                description=f'练习奖励，正确率 {accuracy:.1%}',
                related_id=practice_id
            )
        
        return {
            'stars_earned': stars,
            'accuracy': accuracy
        }
    
    @staticmethod
    def award_task_stars(
        db: Session,
        child_id: int,
        task_id: int
    ) -> Dict:
        """
        发放任务奖励星星
        
        Args:
            db: 数据库会话
            child_id: 孩子ID
            task_id: 任务ID
            
        Returns:
            奖励信息
        """
        stars = int(StarService._get_config_value(db, 'daily_task_stars', 10))
        
        StarService._add_stars(
            db=db,
            child_id=child_id,
            stars=stars,
            source='task',
            description='完成每日任务',
            related_id=task_id
        )
        
        return {
            'stars_earned': stars
        }
    
    @staticmethod
    def award_achievement_stars(
        db: Session,
        child_id: int,
        achievement_name: str,
        stars: int
    ) -> Dict:
        """
        发放成就奖励星星
        
        Args:
            db: 数据库会话
            child_id: 孩子ID
            achievement_name: 成就名称
            stars: 奖励星星数
            
        Returns:
            奖励信息
        """
        StarService._add_stars(
            db=db,
            child_id=child_id,
            stars=stars,
            source='achievement',
            description=f'达成成就：{achievement_name}',
            related_id=None
        )
        
        return {
            'stars_earned': stars,
            'achievement_name': achievement_name
        }
    
    @staticmethod
    def award_ranking_stars(
        db: Session,
        child_id: int,
        rank: int,
        week: int
    ) -> Dict:
        """
        发放排名奖励星星
        
        Args:
            db: 数据库会话
            child_id: 孩子ID
            rank: 排名
            week: 周数
            
        Returns:
            奖励信息
        """
        if rank == 1:
            stars = 100
        elif rank in [2, 3]:
            stars = 50
        else:
            stars = 0
        
        if stars > 0:
            StarService._add_stars(
                db=db,
                child_id=child_id,
                stars=stars,
                source='ranking',
                description=f'周排名第 {rank} 名，第 {week} 周',
                related_id=None
            )
        
        return {
            'stars_earned': stars,
            'rank': rank,
            'week': week
        }
    
    @staticmethod
    def spend_stars(
        db: Session,
        child_id: int,
        amount: int,
        item_type: str,
        item_name: str
    ) -> Dict:
        """
        消费星星
        
        Args:
            db: 数据库会话
            child_id: 孩子ID
            amount: 消费星星数
            item_type: 物品类型
            item_name: 物品名称
            
        Returns:
            消费结果
        """
        child = db.query(Child).filter(Child.id == child_id).first()
        
        if not child or child.total_stars < amount:
            return {
                'success': False,
                'message': '星星余额不足'
            }
        
        child.total_stars -= amount
        
        StarService._add_stars(
            db=db,
            child_id=child_id,
            stars=-amount,
            source='shop',
            description=f'购买{item_name}',
            related_id=None
        )
        
        return {
            'success': True,
            'spent_stars': amount,
            'remaining_stars': child.total_stars
        }
    
    @staticmethod
    def buy_shield(db: Session, child_id: int) -> Dict:
        """
        购买保护罩
        
        Args:
            db: 数据库会话
            child_id: 孩子ID
            
        Returns:
            购买结果
        """
        shield_cost = int(StarService._get_config_value(db, 'streak_shield_cost', 50))
        
        return StarService.spend_stars(
            db=db,
            child_id=child_id,
            amount=shield_cost,
            item_type='shield',
            item_name='连胜保护罩'
        )
    
    @staticmethod
    def get_star_transactions(
        db: Session,
        child_id: int,
        skip: int = 0,
        limit: int = 50
    ) -> List[Dict]:
        """
        获取星星流水记录
        
        Args:
            db: 数据库会话
            child_id: 孩子ID
            skip: 跳过记录数
            limit: 返回记录数
            
        Returns:
            星星流水列表
        """
        transactions = db.query(StarTransaction).filter(
            StarTransaction.child_id == child_id
        ).order_by(
            StarTransaction.created_at.desc()
        ).offset(skip).limit(limit).all()
        
        return [
            {
                'id': t.id,
                'change_type': t.change_type,
                'source': t.source,
                'stars': t.stars,
                'balance_after': t.balance_after,
                'description': t.description,
                'created_at': t.created_at.isoformat() if t.created_at else None
            }
            for t in transactions
        ]
    
    @staticmethod
    def get_star_statistics(db: Session, child_id: int) -> Dict:
        """
        获取星星统计信息
        
        Args:
            db: 数据库会话
            child_id: 孩子ID
            
        Returns:
            星星统计信息
        """
        child = db.query(Child).filter(Child.id == child_id).first()
        
        if not child:
            return {
                'total_stars': 0,
                'earned': 0,
                'spent': 0,
                'by_source': {}
            }
        
        transactions = db.query(StarTransaction).filter(
            StarTransaction.child_id == child_id
        ).all()
        
        earned = sum(t.stars for t in transactions if t.stars > 0)
        spent = sum(-t.stars for t in transactions if t.stars < 0)
        
        by_source = {}
        for t in transactions:
            source = t.source
            if source not in by_source:
                by_source[source] = {'earned': 0, 'spent': 0}
            
            if t.stars > 0:
                by_source[source]['earned'] += t.stars
            else:
                by_source[source]['spent'] += -t.stars
        
        return {
            'total_stars': child.total_stars,
            'total_earned': earned,
            'total_spent': spent,
            'by_source': by_source
        }
    
    @staticmethod
    def _add_stars(
        db: Session,
        child_id: int,
        stars: int,
        source: str,
        description: str,
        related_id: Optional[int] = None
    ):
        """
        添加星星记录（内部方法）
        
        Args:
            db: 数据库会话
            child_id: 孩子ID
            stars: 星星数量（正数增加，负数减少）
            source: 来源
            description: 描述
            related_id: 关联ID
        """
        child = db.query(Child).filter(Child.id == child_id).first()
        
        if not child:
            return
        
        child.total_stars += stars
        
        transaction = StarTransaction(
            child_id=child_id,
            change_type='earn' if stars > 0 else 'spend',
            source=source,
            stars=stars,
            balance_after=child.total_stars,
            description=description,
            related_id=related_id
        )
        
        db.add(transaction)
        db.commit()
    
    @staticmethod
    def _get_config_value(db: Session, key: str, default: any) -> any:
        """
        获取配置值（内部方法）
        
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
