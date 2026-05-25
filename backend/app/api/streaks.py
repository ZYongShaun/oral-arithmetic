from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.user import User
from app.models.child import Child
from app.services.auth_service import get_current_user
from app.services.streak_service import StreakService

router = APIRouter(prefix="/streaks", tags=["streaks"])


@router.get("/{child_id}")
def get_streak_info(
    child_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取连胜信息"""
    child = db.query(Child).filter(
        Child.id == child_id,
        Child.user_id == current_user.id
    ).first()
    
    if not child:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Child not found"
        )
    
    streak_info = StreakService.get_streak_info(db, child_id)
    return streak_info


@router.post("/check")
def check_streak(
    child_id: int,
    accuracy: float,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """检查并更新连胜"""
    child = db.query(Child).filter(
        Child.id == child_id,
        Child.user_id == current_user.id
    ).first()
    
    if not child:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Child not found"
        )
    
    result = StreakService.check_and_update_streak(
        db=db,
        child_id=child_id,
        accuracy=accuracy
    )
    
    return result


@router.post("/use-shield")
def use_shield(
    child_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """使用保护罩"""
    child = db.query(Child).filter(
        Child.id == child_id,
        Child.user_id == current_user.id
    ).first()
    
    if not child:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Child not found"
        )
    
    result = StreakService.use_shield(db, child_id)
    
    if not result['success']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result['message']
        )
    
    return result


@router.get("/milestones")
def get_milestones(
    current_user: User = Depends(get_current_user)
):
    """获取所有里程碑"""
    return StreakService.get_milestones()
