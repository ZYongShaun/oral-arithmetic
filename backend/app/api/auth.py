from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.core.database import get_db
from app.core.security import hash_password
from app.models.user import User
from app.models.practice import Practice
from app.models.child import Child
from app.schemas.auth import RegisterRequest, AuthResponse, UserProfile, TokenPayload, QuickLoginRequest
from app.services.auth_service import authenticate_user, create_access_token, get_current_user, create_or_get_user
from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/register", response_model=AuthResponse)
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(
        (User.username == request.username) | (User.phone == request.phone)
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or phone already registered"
        )
    
    user = User(
        username=request.username,
        password_hash=hash_password(request.password),
        phone=request.phone,
        email=request.email,
        nickname=request.nickname or request.username,
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    access_token = create_access_token(
        data={"sub": user.id},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "username": user.username,
            "nickname": user.nickname,
            "phone": user.phone,
            "email": user.email,
            "avatar": user.avatar,
        }
    }


@router.post("/login", response_model=AuthResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(
        data={"sub": user.id},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "username": user.username,
            "nickname": user.nickname,
            "phone": user.phone,
            "email": user.email,
            "avatar": user.avatar,
        }
    }


@router.get("/me")
def get_current_user_profile(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "nickname": current_user.nickname,
        "phone": current_user.phone,
        "email": current_user.email,
        "avatar": current_user.avatar,
    }


@router.post("/logout")
def logout(current_user: User = Depends(get_current_user)):
    return {"message": "Successfully logged out"}


@router.post("/quick-login", response_model=AuthResponse)
def quick_login(request: QuickLoginRequest, db: Session = Depends(get_db)):
    """
    快速登录接口 - 仅使用用户名，无需密码
    如果用户不存在则自动创建，返回长期有效的JWT token
    """
    try:
        user = create_or_get_user(db, request.username)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"用户名 '{request.username}' 已存在，请添加后缀重新输入（如：小明_1）"
        )
    
    access_token = create_access_token(
        data={"sub": user.id},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    from app.models.child import Child
    from app.models.practice import Practice
    
    total_questions = db.query(Practice).join(
        Child
    ).filter(
        Child.user_id == user.id
    ).count() or 0
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "username": user.username,
            "total_questions": total_questions
        }
    }


@router.get("/recent")
def get_recent_users(
    user_ids: str = None,
    db: Session = Depends(get_db)
):
    """
    获取最近使用用户列表
    用于在登录页显示快捷选择
    """
    if not user_ids:
        return {"recent_users": []}
    
    try:
        ids = [int(id_str.strip()) for id_str in user_ids.split(',') if id_str.strip()]
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user_ids format"
        )
    
    if not ids:
        return {"recent_users": []}
    
    users = db.query(User).filter(
        User.id.in_(ids),
        User.status == 1
    ).all()
    
    # 计算每个用户的答题总数
    recent_users = []
    for user in users:
        total_questions = db.query(Practice).join(
            Child
        ).filter(
            Child.user_id == user.id
        ).count() or 0
        
        recent_users.append({
            "id": user.id,
            "username": user.username,
            "total_questions": total_questions
        })
    
    return {"recent_users": recent_users}
