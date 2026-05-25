"""
管理后台 API
"""
from datetime import datetime, timedelta
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from jose import JWTError, jwt

from app.core.database import get_db
from app.core.security import hash_password, verify_password
from app.core.config import settings
from app.models.user import User, Admin, SystemConfig
from app.models.child import Child
from app.models.practice import Practice
from app.schemas.auth import UserProfile  # if needed
from app.services.auth_service import create_access_token, oauth2_scheme

router = APIRouter(prefix="/admin", tags=["admin"])


def get_current_admin(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Admin:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        admin_id: int = payload.get("sub")
        if admin_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    admin = db.query(Admin).filter(Admin.id == admin_id).first()
    if admin is None:
        raise credentials_exception
    return admin


@router.post("/login", response_model=dict)
def admin_login(
    username: str = Query(...),
    password: str = Query(...),
    db: Session = Depends(get_db)
):
    admin = db.query(Admin).filter(Admin.username == username).first()
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    if not verify_password(password, admin.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    access_token = create_access_token(
        data={"sub": admin.id},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "admin_id": admin.id,
        "username": admin.username,
    }


@router.get("/stats")
def get_admin_stats(
    current_admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    total_users = db.query(User).count()
    total_children = db.query(Child).count()
    total_practices = db.query(Practice).count()
    
    return {
        "total_users": total_users,
        "total_children": total_children,
        "total_practices": total_practices,
    }


# ========== 父用户管理 API ==========

@router.get("/users")
def get_parent_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: Optional[str] = Query(None),
    status: str = Query("all", regex="^(all|1|0)$"),
    sort_by: str = Query("created_at", regex="^(created_at|question_count|username)$"),
    order: str = Query("desc", regex="^(asc|desc)$"),
    current_admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    获取家长用户列表
    """
    # 子查询：统计每个用户的总答题数
    total_q_subq = db.query(
        Child.user_id,
        func.sum(Practice.total_questions).label('total_questions')
    ).outerjoin(Practice, Practice.child_id == Child.id).group_by(Child.user_id).subquery()
    
    query = db.query(User).outerjoin(total_q_subq, total_q_subq.c.user_id == User.id)
    
    # 搜索过滤：用户名、手机、邮箱
    if search:
        query = query.filter(
            or_(
                User.username.like(f"%{search}%"),
                User.phone.like(f"%{search}%"),
                User.email.like(f"%{search}%")
            )
        )
    
    # 状态筛选
    if status != "all":
        status_val = 1 if status == "1" else 0
        query = query.filter(User.status == status_val)
    
    # 排序
    from sqlalchemy import desc, asc
    if sort_by == "question_count":
        sort_column = total_q_subq.c.total_questions
    elif sort_by == "username":
        sort_column = User.username
    else:
        sort_column = User.created_at
    
    if order == "desc":
        query = query.order_by(desc(sort_column))
    else:
        query = query.order_by(asc(sort_column))
    
    total = query.count()
    
    # 分页
    users = query.limit(page_size).offset((page - 1) * page_size).all()
    
    user_list = []
    for user in users:
        total_q = getattr(user, 'total_questions', None)
        if total_q is None:
            total_q = 0
        user_list.append({
            "id": user.id,
            "username": user.username,
            "phone": user.phone,
            "email": user.email,
            "status": user.status,
            "created_at": user.created_at.isoformat() if user.created_at else None,
            "total_questions": total_q
        })
    
    return {
        "users": user_list,
        "total": total,
        "page": page,
        "page_size": page_size
    }


@router.get("/users/{user_id}")
def get_parent_user_detail(
    user_id: int,
    current_admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    获取家长用户详情及关联的孩子列表
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="用户不存在")
    
    # 获取用户的所有孩子
    children = db.query(Child).filter(Child.user_id == user_id).all()
    children_data = []
    for child in children:
        child_total = db.query(func.sum(Practice.total_questions)).filter(
            Practice.child_id == child.id
        ).scalar() or 0
        children_data.append({
            "id": child.id,
            "name": child.name,
            "grade": child.grade,
            "is_active": child.is_active,
            "total_questions": child_total
        })
    
    # 用户总答题数
    total_questions = db.query(func.sum(Practice.total_questions)).join(Child).filter(
        Child.user_id == user_id
    ).scalar() or 0
    
    return {
        "id": user.id,
        "username": user.username,
        "phone": user.phone,
        "email": user.email,
        "status": user.status,
        "created_at": user.created_at.isoformat() if user.created_at else None,
        "total_questions": total_questions,
        "children": children_data
    }


@router.put("/users/{user_id}/status")
def update_parent_user_status(
    user_id: int,
    status_data: dict,
    current_admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    更新家长用户状态（启用/禁用）
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    new_status = status_data.get("status")
    if new_status not in [0, 1]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="状态值必须是 0 或 1"
        )
    
    user.status = new_status
    db.commit()
    
    return {
        "id": user.id,
        "status": user.status,
        "message": "用户状态已更新"
    }


@router.get("/users/export")
def export_parent_users(
    current_admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    导出家长用户数据为 CSV
    """
    import csv
    import io
    
    users = db.query(User).all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', '用户名', '手机号', '邮箱', '状态', '注册时间', '总答题数'])
    
    for user in users:
        total_q = db.query(func.sum(Practice.total_questions)).join(Child).filter(
            Child.user_id == user.id
        ).scalar() or 0
        writer.writerow([
            user.id,
            user.username,
            user.phone or '',
            user.email or '',
            '启用' if user.status == 1 else '禁用',
            user.created_at.strftime('%Y-%m-%d %H:%M:%S') if user.created_at else '',
            total_q
        ])
    
    output.seek(0)
    
    from fastapi.responses import StreamingResponse
    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename=users_export_{datetime.now().strftime('%Y-%m-%d')}.csv"
        }
    )


@router.get("/users/{user_id}/history")
def get_parent_user_history(
    user_id: int,
    days: int = Query(30, ge=1, le=90),
    current_admin: Admin = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    获取家长用户的历史趋势（聚合所有孩子的练习数据）
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="用户不存在")
    
    start_date = datetime.now() - timedelta(days=days)
    
    history_query = db.query(
        func.date(Practice.start_time).label('date'),
        func.count(Practice.id).label('practice_count'),
        func.sum(Practice.total_questions).label('question_count'),
        func.sum(Practice.total_time).label('time_seconds')
    ).join(Child).filter(
        Child.user_id == user_id,
        Practice.start_time >= start_date
    ).group_by(func.date(Practice.start_time))\
     .order_by(func.date(Practice.start_time).desc()).all()
    
    history = []
    total_questions = 0
    for item in history_query:
        q_count = item.question_count or 0
        history.append({
            "date": item.date.strftime('%Y-%m-%d'),
            "practice_count": item.practice_count,
            "question_count": q_count,
            "time_seconds": item.time_seconds or 0
        })
        total_questions += q_count
    
    summary = {
        "total_questions": total_questions,
        "total_practices": sum(h['practice_count'] for h in history),
        "avg_questions_per_day": round(total_questions / days, 2) if days > 0 else 0
    }
    
    return {
        "user_id": user_id,
        "username": user.username,
        "summary": summary,
        "history": history
    }
