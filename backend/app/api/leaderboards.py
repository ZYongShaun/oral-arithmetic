from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import date, timedelta
from typing import List

from app.core.database import get_db
from app.models.user import User
from app.models.child import Child
from app.models.achievement import Leaderboard, StarTransaction
from app.schemas.leaderboard import (
    LeaderboardResponse,
    LeaderboardEntry,
    LeaderboardGroupInfo,
)
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/leaderboards", tags=["leaderboards"])


def get_week_range(d=None):
    if d is None:
        d = date.today()
    start = d - timedelta(days=d.weekday())
    end = start + timedelta(days=6)
    return start, end


@router.get("/current", response_model=LeaderboardResponse)
def get_current_leaderboard(
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
    
    week_start, week_end = get_week_range()
    
    leaderboard = db.query(Leaderboard).filter(
        Leaderboard.child_id == child_id,
        Leaderboard.week_start == week_start
    ).first()
    
    group_id = leaderboard.group_id if leaderboard else 1
    
    group_entries = db.query(Leaderboard).filter(
        Leaderboard.group_id == group_id,
        Leaderboard.week_start == week_start
    ).order_by(Leaderboard.rank).all()
    
    entries = []
    user_rank = None
    
    for idx, entry in enumerate(group_entries, 1):
        is_current_user = entry.child_id == child_id
        if is_current_user:
            user_rank = idx
        
        entries.append(LeaderboardEntry(
            rank=idx,
            child_id=entry.child_id,
            child_name=entry.child_name,
            avatar=None,
            total_stars=entry.total_stars,
            weekly_practices=entry.weekly_practices,
            weekly_accuracy=entry.weekly_accuracy,
            is_current_user=is_current_user,
        ))
    
    if not entries:
        entries.append(LeaderboardEntry(
            rank=1,
            child_id=child_id,
            child_name=child.name,
            avatar=child.avatar,
            total_stars=child.total_stars,
            weekly_practices=0,
            weekly_accuracy=0.0,
            is_current_user=True,
        ))
        user_rank = 1
    
    return LeaderboardResponse(
        week_start=week_start,
        week_end=week_end,
        group_id=group_id,
        group_name=f"Group {group_id}",
        entries=entries,
        user_rank=user_rank,
        total_in_group=len(entries),
        promotion_cutoff=5,
        demotion_cutoff=27,
    )


@router.get("/groups", response_model=LeaderboardGroupInfo)
def get_group_info(
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
    
    week_start, week_end = get_week_range()
    
    leaderboard = db.query(Leaderboard).filter(
        Leaderboard.child_id == child_id,
        Leaderboard.week_start == week_start
    ).first()
    
    group_id = leaderboard.group_id if leaderboard else 1
    
    member_count = db.query(Leaderboard).filter(
        Leaderboard.group_id == group_id,
        Leaderboard.week_start == week_start
    ).count()
    
    return LeaderboardGroupInfo(
        group_id=group_id,
        group_name=f"Group {group_id}",
        member_count=member_count,
        current_rank=leaderboard.rank if leaderboard else 0,
        week_start=week_start,
        week_end=week_end,
        promotion_cutoff=5,
        demotion_cutoff=27,
    )
