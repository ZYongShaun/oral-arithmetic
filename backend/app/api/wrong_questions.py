from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.core.database import get_db
from app.models.user import User
from app.models.child import Child
from app.models.wrong_question import WrongQuestion
from app.models.question import Question
from app.schemas.wrong_question import (
    WrongQuestionResponse,
    WrongQuestionPracticeRequest,
    WrongQuestionStatsResponse,
)
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/wrong-questions", tags=["wrong-questions"])


@router.get("/", response_model=List[WrongQuestionResponse])
def get_wrong_questions(
    child_id: int,
    reviewed: bool = None,
    skip: int = 0,
    limit: int = 100,
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
    
    query = db.query(WrongQuestion).filter(WrongQuestion.child_id == child_id)
    
    if reviewed is not None:
        query = query.filter(WrongQuestion.reviewed == reviewed)
    
    wrong_questions = query.order_by(
        WrongQuestion.created_at.desc()
    ).offset(skip).limit(limit).all()
    
    result = []
    for wq in wrong_questions:
        question = db.query(Question).filter(Question.id == wq.question_id).first()
        result.append(WrongQuestionResponse(
            id=wq.id,
            child_id=wq.child_id,
            question_id=wq.question_id,
            practice_id=wq.practice_id,
            user_answer=wq.user_answer,
            expected_answer=question.expected_answer if question else "",
            question_text=question.question_text if question else "",
            question_type=question.question_type if question else "",
            created_at=wq.created_at,
            reviewed=wq.reviewed,
            reviewed_at=wq.reviewed_at,
        ))
    
    return result


@router.post("/review")
def review_wrong_question(
    wrong_question_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    wq = db.query(WrongQuestion).filter(WrongQuestion.id == wrong_question_id).first()
    
    if not wq:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wrong question not found"
        )
    
    child = db.query(Child).filter(
        Child.id == wq.child_id,
        Child.user_id == current_user.id
    ).first()
    
    if not child:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )
    
    wq.reviewed = True
    wq.reviewed_at = datetime.utcnow()
    db.commit()
    
    return {"message": "Wrong question marked as reviewed"}


@router.delete("/{wrong_question_id}")
def delete_wrong_question(
    wrong_question_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    wq = db.query(WrongQuestion).filter(WrongQuestion.id == wrong_question_id).first()
    
    if not wq:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wrong question not found"
        )
    
    child = db.query(Child).filter(
        Child.id == wq.child_id,
        Child.user_id == current_user.id
    ).first()
    
    if not child:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )
    
    db.delete(wq)
    db.commit()
    
    return {"message": "Wrong question deleted"}


@router.get("/stats", response_model=WrongQuestionStatsResponse)
def get_wrong_question_stats(
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
    
    from sqlalchemy import func
    
    total_count = db.query(func.count(WrongQuestion.id)).filter(
        WrongQuestion.child_id == child_id
    ).scalar()
    
    reviewed_count = db.query(func.count(WrongQuestion.id)).filter(
        WrongQuestion.child_id == child_id,
        WrongQuestion.is_mastered == True
    ).scalar()
    
    unreviewed_count = total_count - reviewed_count
    
    by_type = db.query(
        Question.type,
        func.count(WrongQuestion.id)
    ).join(
        Question, WrongQuestion.question_id == Question.id
    ).filter(
        WrongQuestion.child_id == child_id
    ).group_by(Question.type).all()
    
    recent_count = db.query(func.count(WrongQuestion.id)).filter(
        WrongQuestion.child_id == child_id
    ).scalar()
    
    return WrongQuestionStatsResponse(
        total_count=total_count or 0,
        reviewed_count=reviewed_count or 0,
        unreviewed_count=unreviewed_count or 0,
        by_type=dict(by_type) if by_type else {},
        recent_count=recent_count or 0,
    )
