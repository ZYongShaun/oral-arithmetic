from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
import random

from app.core.database import get_db
from app.models.user import User
from app.models.question import Question
from app.schemas.question import QuestionResponse, RandomQuestionsRequest, QuestionCreate, QuestionUpdate
from app.services.auth_service import get_current_user
from app.services.question_generator import QuestionGenerator

router = APIRouter(prefix="/questions", tags=["questions"])


def serialize_question(question: Question) -> QuestionResponse:
    return QuestionResponse(
        id=question.id,
        level=question.level,
        type=question.type,
        question_text=question.question_text,
        answer=question.answer,
        source=question.source,
        status=question.status,
        difficulty=question.difficulty,
        usage_count=question.usage_count,
        correct_count=question.correct_count,
        created_at=str(question.created_at),
        knowledge_point=getattr(question, "knowledge_point", None),
        options=getattr(question, "options", None)
    )


def grade_level_to_generator_difficulty(grade_level: Optional[int]) -> int:
    mapping = {
        10: 1,
        20: 2,
        50: 3,
        100: 4,
    }
    return mapping.get(grade_level, 2)


def serialize_generated_question(question: dict, index: int) -> QuestionResponse:
    type_mapping = {
        "addition": 1,
        "subtraction": 2,
        "mixed": 3,
    }
    generator_difficulty = question.get("difficulty_level", 2)
    reverse_level_mapping = {
        1: 10,
        2: 20,
        3: 50,
        4: 100,
    }
    return QuestionResponse(
        id=-(index + 1),
        level=reverse_level_mapping.get(generator_difficulty, 20),
        type=type_mapping.get(question.get("question_type"), 3),
        question_text=question["question_text"],
        answer=question["expected_answer"],
        source=1,
        status=1,
        difficulty=float(generator_difficulty),
        usage_count=0,
        correct_count=0,
        created_at="",
        knowledge_point=None,
        options=str(question.get("options")) if question.get("options") is not None else None
    )


@router.post("/random", response_model=List[QuestionResponse])
def get_random_questions(
    request: RandomQuestionsRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(Question).filter(Question.status == 1)
    
    if request.grade_level:
        query = query.filter(Question.level == request.grade_level)
    
    if request.difficulty_level is not None:
        query = query.filter(Question.difficulty == request.difficulty_level)
    
    if request.question_types:
        query = query.filter(Question.type.in_(request.question_types))
    
    questions = query.all()
    
    selected = random.sample(questions, min(len(questions), request.count))
    response_questions = [serialize_question(q) for q in selected]

    if len(response_questions) < request.count:
        generated_questions = QuestionGenerator.generate_practice_questions(
            difficulty_level=grade_level_to_generator_difficulty(request.grade_level),
            count=request.count - len(response_questions)
        )
        response_questions.extend(
            serialize_generated_question(question, index)
            for index, question in enumerate(generated_questions)
        )

    return response_questions


@router.get("/", response_model=List[QuestionResponse])
def get_questions(
    grade_level: Optional[int] = None,
    difficulty_level: Optional[float] = None,
    question_type: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(Question).filter(Question.status == 1)
    
    if grade_level:
        query = query.filter(Question.level == grade_level)
    if difficulty_level is not None:
        query = query.filter(Question.difficulty == difficulty_level)
    if question_type:
        query = query.filter(Question.type == question_type)
    
    questions = query.offset(skip).limit(limit).all()
    
    return [serialize_question(q) for q in questions]


@router.post("/", response_model=QuestionResponse)
def create_question(
    question_data: QuestionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    payload = question_data.model_dump(exclude_none=True)
    payload.pop("knowledge_point", None)
    payload.pop("options", None)
    question = Question(**payload)
    
    db.add(question)
    db.commit()
    db.refresh(question)
    
    return serialize_question(question)


@router.put("/{question_id}", response_model=QuestionResponse)
def update_question(
    question_id: int,
    question_data: QuestionUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    question = db.query(Question).filter(Question.id == question_id).first()
    
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )
    
    update_data = question_data.model_dump(exclude_unset=True)
    update_data.pop("knowledge_point", None)
    update_data.pop("options", None)
    for field, value in update_data.items():
        setattr(question, field, value)
    
    db.commit()
    db.refresh(question)
    
    return serialize_question(question)


@router.delete("/{question_id}")
def delete_question(
    question_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    question = db.query(Question).filter(Question.id == question_id).first()
    
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )
    
    question.status = 0
    db.commit()
    
    return {"message": "Question deleted successfully"}
