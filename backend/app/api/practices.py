from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List
import random

from app.core.database import get_db
from app.models.user import User
from app.models.child import Child
from app.models.practice import Practice
from app.models.practice_detail import PracticeDetail
from app.schemas.practice import (
    PracticeStartRequest,
    PracticeQuestionResponse,
    PracticeSubmitRequest,
    PracticeSubmitResponse,
    PracticeHistoryItem,
    PracticeFullResponse,
    PracticeDetailResponse,
)
from app.services.auth_service import get_current_user
from app.services.practice_service import submit_practice
from app.services.question_generator import QuestionGenerator

router = APIRouter(prefix="/practices", tags=["practices"])


@router.post("/start")
def start_practice(
    request: PracticeStartRequest,
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
    
    question_types = request.question_types if hasattr(request, 'question_types') else None
    generated_questions = QuestionGenerator.generate_practice_questions(
        difficulty_level=request.difficulty_level,
        question_types=question_types,
        count=20
    )
    
    practice = Practice(
        child_id=request.child_id,
        difficulty_level=request.difficulty_level,
        started_at=datetime.utcnow(),
    )
    db.add(practice)
    db.flush()
    
    practice_details = []
    for idx, question in enumerate(generated_questions):
        detail = PracticeDetail(
            practice_id=practice.id,
            question_id=None,
            question_text=question['question_text'],
            expected_answer=question['expected_answer'],
            time_spent=0,
        )
        practice_details.append(detail)
    
    db.bulk_save_objects(practice_details)
    db.commit()
    db.refresh(practice)
    
    practice_questions = [
        PracticeQuestionResponse(
            id=idx,
            question_text=q['question_text'],
            question_type=q['question_type'],
            expected_answer=q['expected_answer'],
            options=q['options'],
        )
        for idx, q in enumerate(generated_questions)
    ]
    
    return {
        "practice": practice,
        "questions": practice_questions
    }


@router.post("/submit", response_model=PracticeSubmitResponse)
def submit_practice_endpoint(
    request: PracticeSubmitRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if request.practice_id is None:
        child_id = request.childId
        if child_id is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="practice_id or childId is required"
            )

        child = db.query(Child).filter(
            Child.id == child_id,
            Child.user_id == current_user.id
        ).first()
        if not child:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Child not found"
            )

        answer_details = request.answer_details or []
        total_questions = len(answer_details) or len(request.answers)
        correct_count = sum(1 for item in answer_details if item.get("isCorrect"))
        wrong_count = max(total_questions - correct_count, 0)
        accuracy = (correct_count / total_questions * 100) if total_questions else 0.0
        stars_earned = 3 if accuracy >= 100 else 2 if accuracy >= 80 else 1 if accuracy >= 60 else 0
        now = datetime.utcnow()

        practice = Practice(
            child_id=child_id,
            level=20,
            total_questions=total_questions,
            correct_count=correct_count,
            wrong_count=wrong_count,
            total_time=request.time_spent,
            avg_time=(request.time_spent / total_questions) if total_questions else 0,
            accuracy=accuracy,
            stars_earned=stars_earned,
            start_time=now,
            end_time=now,
        )
        db.add(practice)
        db.flush()

        if stars_earned:
            child.total_stars += stars_earned

        db.commit()
        db.refresh(practice)

        return PracticeSubmitResponse(
            practice_id=practice.id,
            score=int(accuracy),
            accuracy=accuracy,
            stars_earned=stars_earned,
            time_spent=request.time_spent,
            completed_at=practice.end_time,
            details=answer_details,
        )

    practice = db.query(Practice).filter(
        Practice.id == request.practice_id
    ).first()
    
    if not practice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Practice not found"
        )
    
    child = db.query(Child).filter(
        Child.id == practice.child_id,
        Child.user_id == current_user.id
    ).first()
    
    if not child:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized for this practice"
        )
    
    return submit_practice(
        db=db,
        practice_id=request.practice_id,
        answers=request.answers,
        time_spent=request.time_spent
    )


@router.get("/history", response_model=List[PracticeHistoryItem])
def get_practice_history(
    child_id: int,
    skip: int = 0,
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
    
    practices = db.query(Practice).filter(
        Practice.child_id == child_id,
        Practice.completed_at != None
    ).order_by(
        Practice.completed_at.desc()
    ).offset(skip).limit(limit).all()
    
    return [
        PracticeHistoryItem(
            id=p.id,
            child_id=p.child_id,
            score=p.score,
            accuracy=p.accuracy,
            stars_earned=p.stars_earned,
            difficulty_level=p.difficulty_level,
            completed_at=p.completed_at,
            time_spent=p.time_spent,
        )
        for p in practices
    ]


@router.get("/{practice_id}", response_model=PracticeFullResponse)
def get_practice_detail(
    practice_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    practice = db.query(Practice).filter(Practice.id == practice_id).first()
    
    if not practice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Practice not found"
        )
    
    child = db.query(Child).filter(
        Child.id == practice.child_id,
        Child.user_id == current_user.id
    ).first()
    
    if not child:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized for this practice"
        )
    
    details = db.query(PracticeDetail).filter(
        PracticeDetail.practice_id == practice_id
    ).all()
    
    detail_responses = [
        PracticeDetailResponse(
            id=d.id,
            practice_id=d.practice_id,
            question_id=d.question_id,
            question_text=d.question_text,
            user_answer=d.user_answer,
            expected_answer=d.expected_answer,
            is_correct=d.is_correct,
            time_spent=d.time_spent,
        )
        for d in details
    ]
    
    return PracticeFullResponse(
        id=practice.id,
        child_id=practice.child_id,
        score=practice.score,
        accuracy=practice.accuracy,
        stars_earned=practice.stars_earned,
        difficulty_level=practice.difficulty_level,
        completed_at=practice.completed_at,
        time_spent=practice.time_spent,
        details=detail_responses,
    )
