"""
统计管理 API
"""
from datetime import datetime, timedelta, date
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, extract

from app.core.database import get_db
from app.models.user import User
from app.models.child import Child
from app.models.practice import Practice
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/statistics", tags=["statistics"])


def get_current_admin(current_user: User = Depends(get_current_user)):
    """检查管理员权限"""
    # 这里简化处理，实际应该查询 admin 表
    # 暂时允许所有登录用户访问
    return current_user


@router.get("/today")
def get_today_statistics(
    admin=Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    获取今日数据统计
    """
    today = date.today()
    
    # 今日活跃用户数（通过练习记录统计）
    active_users_query = db.query(Practice.child_id).filter(
        func.date(Practice.created_at) == today
    ).distinct().subquery()
    
    active_users_count = db.query(func.count()).select_from(active_users_query).scalar() or 0
    
    # 今日答题总数
    total_questions = db.query(func.count()).filter(
        func.date(Practice.created_at) == today
    ).scalar() or 0
    
    # 今日总用时（分钟）
    total_time_seconds = db.query(func.sum(Practice.total_time)).filter(
        func.date(Practice.created_at) == today
    ).scalar() or 0
    total_time_minutes = int(total_time_seconds / 60) if total_time_seconds else 0
    
    # 今日前5名用户
    top_users_query = db.query(
        Practice.child_id,
        func.count().label('question_count'),
        func.sum(Practice.total_time).label('time_seconds')
    ).filter(
        func.date(Practice.created_at) == today
    ).group_by(Practice.child_id).order_by(func.count().desc()).limit(5).all()
    
    # 获取用户信息
    top_users = []
    child_ids = [item.child_id for item in top_users_query]
    children_map = {}
    if child_ids:
        children = db.query(Child).filter(Child.id.in_(child_ids)).all()
        children_map = {c.id: c for c in children}
    
    for item in top_users_query:
        child = children_map.get(item.child_id)
        if child:
            top_users.append({
                "id": child.id,
                "username": child.name,
                "question_count": item.question_count,
                "time_minutes": int(item.time_seconds / 60) if item.time_seconds else 0
            })
    
    return {
        "active_users": active_users_count,
        "total_questions": total_questions,
        "total_time_minutes": total_time_minutes,
        "top_users": top_users
    }


@router.get("/leaderboard")
def get_leaderboard(
    period: str = Query("weekly", regex="^(weekly|monthly|all)$"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=50),
    admin=Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    获取排行榜
    """
    # 时间范围筛选
    now = datetime.now()
    if period == "weekly":
        # 本周（周一到周日）
        start_date = now - timedelta(days=now.weekday())
        start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
    elif period == "monthly":
        # 本月
        start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    else:
        # 全部时间
        start_date = None
    
    # 构建查询
    query = db.query(
        Child.id,
        Child.name.label('username'),
        func.count(Practice.id).label('question_count')
    ).join(Practice, Practice.child_id == Child.id)
    
    if start_date:
        query = query.filter(Practice.created_at >= start_date)
    
    query = query.group_by(Child.id, Child.name)
    
    # 总数
    total = query.count()
    
    # 排序并分页
    leaderboard_data = query.order_by(func.count(Practice.id).desc())\
        .offset((page - 1) * page_size)\
        .limit(page_size)\
        .all()
    
    # 计算排名和得分（简单规则：每道题得1分）
    leaderboard = []
    start_rank = (page - 1) * page_size + 1
    for idx, item in enumerate(leaderboard_data):
        rank = start_rank + idx
        # 添加前3名图标
        icon = ""
        if rank == 1:
            icon = "🥇"
        elif rank == 2:
            icon = "🥈"
        elif rank == 3:
            icon = "🥉"
        
        leaderboard.append({
            "rank": rank,
            "id": item.id,
            "username": item.username,
            "question_count": item.question_count,
            "score": item.question_count,
            "icon": icon
        })
    
    return {
        "period": period,
        "leaderboard": leaderboard,
        "total": total,
        "page": page,
        "page_size": page_size
    }


@router.get("/user/{user_id}/history")
def get_user_history(
    user_id: int,
    days: int = Query(30, ge=1, le=90),
    admin=Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    获取单个用户历史趋势
    """
    # 检查用户是否存在
    child = db.query(Child).filter(Child.id == user_id).first()
    if not child:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    # 计算开始日期
    start_date = datetime.now() - timedelta(days=days)
    
    # 查询按天统计
    history_query = db.query(
        func.date(Practice.created_at).label('date'),
        func.count(Practice.id).label('question_count'),
        func.sum(Practice.total_time).label('time_seconds')
    ).filter(
        Practice.child_id == user_id,
        Practice.created_at >= start_date
    ).group_by(func.date(Practice.created_at))\
     .order_by(func.date(Practice.created_at).desc()).all()
    
    # 构建历史数据数组
    history = []
    total_questions = 0
    max_daily = 0
    
    for item in history_query:
        question_count = item.question_count
        history.append({
            "date": item.date.strftime('%Y-%m-%d'),
            "question_count": question_count,
            "score": question_count  # 暂时使用题数作为分数
        })
        total_questions += question_count
        if question_count > max_daily:
            max_daily = question_count
    
    avg_daily = total_questions / days if days > 0 else 0
    
    summary = {
        "total_questions": total_questions,
        "total_score": total_questions,
        "avg_daily_questions": round(avg_daily, 1),
        "max_daily_questions": max_daily,
        "created_at": child.created_at.isoformat() if child.created_at else None
    }
    
    return {
        "user_id": user_id,
        "username": child.name,
        "summary": summary,
        "history": history
    }


@router.get("/leaderboard/export")
def export_leaderboard(
    period: str = Query("all", regex="^(weekly|monthly|all)$"),
    admin=Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    导出排行榜为 CSV
    """
    import csv
    import io
    
    # 计算时间范围
    now = datetime.now()
    if period == "weekly":
        start_date = now - timedelta(days=now.weekday())
        start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
    elif period == "monthly":
        start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    else:
        start_date = None
    
    # 构建查询
    query = db.query(
        Child.id,
        Child.name.label('username'),
        func.count(Practice.id).label('question_count')
    ).join(Practice, Practice.child_id == Child.id)
    
    if start_date:
        query = query.filter(Practice.created_at >= start_date)
    
    query = query.group_by(Child.id, Child.name)
    query = query.order_by(func.count(Practice.id).desc())
    
    leaderboard_data = query.all()
    
    # 生成 CSV
    output = io.StringIO()
    writer = csv.writer(output)
    
    # 写入表头
    writer.writerow(['排名', 'ID', '姓名', '答题数', '得分'])
    
    # 写入数据
    for idx, item in enumerate(leaderboard_data, start=1):
        writer.writerow([
            idx,
            item.id,
            item.username,
            item.question_count,
            item.question_count  # 暂时用答题数作为得分
        ])
    
    output.seek(0)
    
    from fastapi.responses import StreamingResponse
    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename=leaderboard_{period}_export_{datetime.now().strftime('%Y-%m-%d')}.csv"
        }
    )
