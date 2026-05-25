from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List

from app.core.database import get_db
from app.models.user import User
from app.models.child import Child
from app.models.achievement import StarTransaction
from app.schemas.star import (
    StarBalanceResponse,
    StarTransactionResponse,
    StarSpendRequest,
    StarSpendResponse,
    StarShopItem,
)
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/stars", tags=["stars"])


@router.get("/balance/{child_id}", response_model=StarBalanceResponse)
def get_star_balance(
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
    
    total_transactions = db.query(StarTransaction).filter(
        StarTransaction.child_id == child_id
    ).all()
    
    spent_stars = sum(-t.amount for t in total_transactions if t.amount < 0)
    
    return StarBalanceResponse(
        child_id=child_id,
        total_stars=child.total_stars,
        available_stars=child.total_stars,
        spent_stars=spent_stars,
    )


@router.get("/transactions/{child_id}", response_model=List[StarTransactionResponse])
def get_star_transactions(
    child_id: int,
    limit: int = 50,
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
    
    transactions = db.query(StarTransaction).filter(
        StarTransaction.child_id == child_id
    ).order_by(
        StarTransaction.created_at.desc()
    ).limit(limit).all()
    
    return [
        StarTransactionResponse(
            id=t.id,
            child_id=t.child_id,
            amount=t.amount,
            balance_after=t.balance_after,
            transaction_type=t.transaction_type,
            description=t.description,
            reference_id=t.reference_id,
            created_at=t.created_at,
        )
        for t in transactions
    ]


@router.post("/spend", response_model=StarSpendResponse)
def spend_stars(
    request: StarSpendRequest,
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
    
    if child.total_stars < request.amount:
        return StarSpendResponse(
            success=False,
            message="Not enough stars",
            balance_before=child.total_stars,
            balance_after=child.total_stars,
        )
    
    balance_before = child.total_stars
    child.total_stars -= request.amount
    
    transaction = StarTransaction(
        child_id=request.child_id,
        amount=-request.amount,
        balance_after=child.total_stars,
        transaction_type=request.transaction_type,
        description=request.description,
    )
    db.add(transaction)
    db.commit()
    
    return StarSpendResponse(
        success=True,
        message="Stars spent successfully",
        balance_before=balance_before,
        balance_after=child.total_stars,
    )


@router.get("/shop", response_model=List[StarShopItem])
def get_star_shop(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    shop_items = [
        StarShopItem(
            item_id="streak_shield",
            name="Streak Shield",
            description="Protect your streak for 7 days",
            cost=50,
            icon="🛡️",
            available=True,
        ),
        StarShopItem(
            item_id="avatar_frame_1",
            name="Gold Frame",
            description="Decorative avatar frame",
            cost=200,
            icon="🖼️",
            available=True,
        ),
        StarShopItem(
            item_id="avatar_frame_2",
            name="Diamond Frame",
            description="Premium avatar frame",
            cost=500,
            icon="💎",
            available=True,
        ),
        StarShopItem(
            item_id="theme_classic",
            name="Classic Theme",
            description="Classic app theme",
            cost=300,
            icon="🎨",
            available=True,
        ),
    ]
    
    return shop_items
