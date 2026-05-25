from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.user import User
from app.models.child import Child
from app.models.achievement import Achievement, ChildAchievement, StarTransaction
from app.schemas.achievement import (
    AchievementResponse,
    AchievementProgressResponse,
    ChildAchievementProgress,
)
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/achievements", tags=["achievements"])


@router.get("/", response_model=List[AchievementResponse])
def get_all_achievements(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    achievements = db.query(Achievement).filter(
        Achievement.is_active == True
    ).all()
    
    return [
        AchievementResponse(
            id=a.id,
            name=a.name,
            description=a.description,
            category=a.category,
            milestone_type=a.milestone_type,
            milestone_value=a.milestone_value,
            stars_reward=a.stars_reward,
            icon=a.icon,
        )
        for a in achievements
    ]


@router.get("/{child_id}/progress", response_model=AchievementProgressResponse)
def get_achievement_progress(
    child_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    child = db.query(Child).filter(
        Child.id == child_id,
        Child.user_id == current_user.id
    ).first()
    
    if not child:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Child not found"
        )
    
    achievements = db.query(Achievement).filter(
        Achievement.is_active == True
    ).all()
    
    child_achievements = db.query(ChildAchievement).filter(
        ChildAchievement.child_id == child_id
    ).all()
    
    child_achievement_map = {ca.achievement_id: ca for ca in child_achievements}
    
    progress_list = []
    total_achieved = 0
    total_stars_earned = 0
    
    for achievement in achievements:
        ca = child_achievement_map.get(achievement.id)
        
        current_value = 0
        achieved = False
        stars_rewarded = False
        achieved_at = None
        
        if ca:
            current_value = ca.current_value
            achieved = ca.achieved
            stars_rewarded = ca.stars_rewarded
            achieved_at = ca.achieved_at
            
            if achieved:
                total_achieved += 1
            if stars_rewarded:
                total_stars_earned += achievement.stars_reward
        
        progress_percentage = min(100, (current_value / achievement.milestone_value) * 100) if achievement.milestone_value > 0 else 0
        
        progress_list.append(ChildAchievementProgress(
            achievement_id=achievement.id,
            achievement_name=achievement.name,
            category=achievement.category,
            milestone_value=achievement.milestone_value,
            current_value=current_value,
            progress_percentage=progress_percentage,
            achieved=achieved,
            stars_rewarded=stars_rewarded,
            achieved_at=achieved_at,
        ))
    
    return AchievementProgressResponse(
        child_id=child_id,
        achievements=progress_list,
        total_achieved=total_achieved,
        total_stars_earned=total_stars_earned,
    )
