from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.user import User
from app.models.child import Child
from app.schemas.child import ChildCreate, ChildUpdate, ChildResponse
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/children", tags=["children"])

def child_to_dict(child, nickname=None, avatar=None, grade_level=None, difficulty_level=None):
    return {
        "id": child.id,
        "user_id": child.user_id,
        "name": child.name,
        "nickname": nickname or child.name,
        "avatar": avatar or None,
        "grade": grade_level or child.grade,
        "difficulty_level": difficulty_level or getattr(child, 'difficultyLevel', 1),
        "is_active": 1 if child.is_active == 1 else 0,
        "stars": child.total_stars,
        "created_at": child.created_at.isoformat() if child.created_at else None,
    }


@router.get("/", response_model=List[ChildResponse])
def get_children(
    skip: int = 0,
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    children = db.query(Child).filter(
        Child.user_id == current_user.id,
        Child.is_active == True
    ).offset(skip).limit(limit).all()
    
    return [
        child_to_dict(child, child.name, None, child.grade, getattr(child, 'difficultyLevel', 1))
        for child in children
    ]


@router.post("/")
def create_child(
    child_data: ChildCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    existing_child = db.query(Child).filter(
        Child.user_id == current_user.id,
        Child.name == child_data.name
    ).first()
    
    if existing_child:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Child with this name already exists"
        )
    
    child = Child(
        user_id=current_user.id,
        name=child_data.name,
        gender=child_data.gender,
        birth_date=child_data.birth_date,
        grade=child_data.grade or "一年级",
        total_stars=0,
        is_active=True,
    )
    
    db.add(child)
    db.commit()
    db.refresh(child)
    
    return child_to_dict(
        child, 
        child_data.nickname or child_data.name, 
        child_data.avatar, 
        child_data.grade_level, 
        child_data.difficulty_level or 1
    )


@router.get("/{child_id}")
def get_child(
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
    
    return child_to_dict(child)


@router.put("/{child_id}")
def update_child(
    child_id: int,
    child_data: ChildUpdate,
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
    
    update_data = child_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(child, field, value)
    
    db.commit()
    db.refresh(child)
    
    return child_to_dict(child)


@router.delete("/{child_id}")
def delete_child(
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
    
    from sqlalchemy import update
    stmt = update(Child).where(Child.id == child_id).values(is_active=0)
    db.execute(stmt)
    db.commit()
    
    return {"message": "Child deleted successfully"}
