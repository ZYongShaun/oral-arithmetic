from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import date, datetime, timedelta

from app.core.database import get_db
from app.models.user import User
from app.models.child import Child
from app.models.practice import Practice
from app.models.daily_task import DailyTask
from app.schemas.daily_task import (
    DailyTaskStatusResponse,
    DailyTaskClaimRequest,
    DailyTaskClaimResponse,
)
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/daily-tasks", tags=["daily-tasks"])


@router.get("/{child_id}", response_model=DailyTaskStatusResponse)
def get_daily_task_status(
    child_id: int,
    target_date: date = None,
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
    
    if target_date is None:
        target_date = date.today()
    
    task = db.query(DailyTask).filter(
        DailyTask.child_id == child_id,
        DailyTask.task_date == target_date
    ).first()
    
    if not task:
        practices_count = db.query(Practice).filter(
            Practice.child_id == child_id,
            Practice.end_time >= datetime.combine(target_date, datetime.min.time()),
            Practice.end_time < datetime.combine(target_date + timedelta(days=1), datetime.min.time())
        ).count()
        
        task = DailyTask(
            child_id=child_id,
            task_date=target_date,
            target_count=3,
            completed_count=practices_count,
            stars_earned=0,
        )
        db.add(task)
        db.commit()
        db.refresh(task)
    
    is_completed = task.completed_count >= task.target_count
    
    return DailyTaskStatusResponse(
        date=task.task_date,
        target_count=task.target_count,
        completed_count=task.completed_count,
        is_completed=is_completed,
        stars_earned=task.stars_earned,
        progress_percentage=(task.completed_count / task.target_count) * 100 if task.target_count > 0 else 0,
    )


@router.post("/claim", response_model=DailyTaskClaimResponse)
def claim_daily_task_reward(
    request: DailyTaskClaimRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    child = db.query(Child).filter(
        Child.id == request.child_id,
        Child.user_id == current_user.id
    ).first()
    
    if not child:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Child not found"
        )
    
    task_date = request.date or date.today()
    
    task = db.query(DailyTask).filter(
        DailyTask.child_id == request.child_id,
        DailyTask.task_date == task_date
    ).first()
    
    if not task:
        return DailyTaskClaimResponse(
            success=False,
            stars_earned=0,
            message="No task found for this date",
        )
    
    if task.completed_count < task.target_count:
        return DailyTaskClaimResponse(
            success=False,
            stars_earned=0,
            message="Task not completed yet",
        )
    
    if task.stars_claimed:
        return DailyTaskClaimResponse(
            success=False,
            stars_earned=0,
            message="Reward already claimed",
        )
    
    stars_earned = 10
    child.total_stars += stars_earned
    task.stars_claimed = True
    
    from app.models.achievement import StarTransaction
    transaction = StarTransaction(
        child_id=request.child_id,
        amount=stars_earned,
        balance_after=child.total_stars,
        transaction_type="daily_task",
        description=f"Daily task completed - {task_date}",
    )
    db.add(transaction)
    db.commit()
    
    return DailyTaskClaimResponse(
        success=True,
        stars_earned=stars_earned,
        message="Daily task reward claimed!",
    )
