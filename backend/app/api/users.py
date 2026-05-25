from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, or_

from app.core.database import get_db
from app.core.security import hash_password, verify_password
from app.models.user import User
from app.models.practice import Practice
from app.models.child import Child
from app.schemas.auth import UserProfile
from app.schemas.user import UserUpdate, PasswordChangeRequest
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/profile")
def get_profile(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "nickname": current_user.nickname,
        "phone": current_user.phone,
    }


@router.put("/profile")
def update_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    update_data = user_update.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(current_user, field, value)
    
    db.commit()
    db.refresh(current_user)
    
    return {
        "id": current_user.id,
        "username": current_user.username,
        "nickname": current_user.nickname,
        "phone": current_user.phone,
    }


@router.post("/password/change")
def change_password(
    password_request: PasswordChangeRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db.refresh(current_user)
    if not verify_password(password_request.old_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect old password"
        )
    
    hashed = hash_password(password_request.new_password)
    from sqlalchemy import update
    stmt = update(User).where(User.id == current_user.id).values(password_hash=hashed)
    db.execute(stmt)
    db.commit()
    
    return {"message": "Password changed successfully"}


@router.get("")
def get_user_list(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: str = Query(None),
    status_filter: str = Query("all", regex="^(all|0|1)$"),
    sort_by: str = Query("created_at", regex="^(created_at|question_count|username)$"),
    sort_order: str = Query("desc", regex="^(asc|desc)$"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取用户列表（管理员用）
    - 支持分页查询（page, page_size）
    - 支持搜索功能（username, phone, email 模糊匹配）
    - 支持状态筛选（all, 1, 0）
    - 支持排序功能（created_at, question_count, username）
    """
    # 构建查询
    query = db.query(User)
    
    # 搜索过滤
    if search:
        query = query.filter(
            or_(
                User.username.like(f"%{search}%"),
                User.phone.like(f"%{search}%"),
                User.email.like(f"%{search}%")
            )
        )
    
    # 状态过滤
    if status_filter != "all":
        status_value = 1 if status_filter == "1" else 0
        query = query.filter(User.status == status_value)
    
    # 计算总数
    total = query.count()
    
    # 排序
    sort_column = getattr(User, sort_by, User.created_at)
    if sort_by == "question_count":
        # 需要关联查询计算答题数
        query = query.outerjoin(Child).outerjoin(Practice)
        query = query.group_by(User.id)
        question_count_col = func.count(Practice.id).label("question_count")
        query = query.add_columns(question_count_col)
        
        # 排序
        if sort_order == "asc":
            query = query.order_by(question_count_col.asc())
        else:
            query = query.order_by(question_count_col.desc())
    else:
        # 普通排序
        if sort_order == "asc":
            query = query.order_by(sort_column.asc())
        else:
            query = query.order_by(sort_column.desc())
    
    # 分页
    users_data = query.limit(page_size).offset((page - 1) * page_size).all()
    
    # 构建响应
    users_list = []
    for user_row in users_data:
        if sort_by == "question_count":
            user = user_row[0]
            question_count = user_row[1] or 0
        else:
            user = user_row
            # 单独查询该用户的答题数
            question_count = db.query(func.count(Practice.id)).join(Child).filter(
                Child.user_id == user.id
            ).scalar() or 0
        
        users_list.append({
            "id": user.id,
            "username": user.username,
            "phone": user.phone,
            "email": user.email,
            "status": user.status,
            "created_at": user.created_at.isoformat() if user.created_at else None,
            "total_questions": question_count
        })
    
    return {
        "users": users_list,
        "total": total,
        "page": page,
        "page_size": page_size
    }
