from pydantic import BaseModel, EmailStr, validator
from typing import Optional
import re


class RegisterRequest(BaseModel):
    """用户注册请求"""
    username: str
    password: str
    phone: Optional[str] = None
    email: Optional[str] = None
    nickname: Optional[str] = None
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 6 or len(v) > 20:
            raise ValueError('密码长度必须在 6-20 位之间')
        return v
    
    @validator('username')
    def validate_username(cls, v):
        if len(v) < 2 or len(v) > 20:
            raise ValueError('用户名长度必须在 2-20 位之间')
        return v


class QuickLoginRequest(BaseModel):
    """快速登录请求（仅用户名）"""
    username: str
    
    @validator('username')
    def validate_username(cls, v):
        if len(v) < 2 or len(v) > 20:
            raise ValueError('姓名长度必须在2-20个字符之间')
        if not re.match(r'^[\u4e00-\u9fa5a-zA-Z0-9_]+$', v):
            raise ValueError('只能输入中文、英文、数字和下划线')
        return v


class RecentUsersRequest(BaseModel):
    """最近用户请求"""
    user_ids: str  # 逗号分隔的用户ID字符串


class LoginRequest(BaseModel):
    """用户登录请求"""
    username: str
    password: str


class UserProfile(BaseModel):
    """用户信息"""
    id: int
    username: str
    phone: Optional[str] = None
    email: Optional[str] = None
    nickname: Optional[str] = None
    avatar: Optional[str] = None
    
    class Config:
        from_attributes = True


class AuthResponse(BaseModel):
    """认证响应"""
    access_token: str
    token_type: str
    user: Optional[UserProfile] = None


class TokenPayload(BaseModel):
    """Token 负载"""
    user_id: int
    username: str
