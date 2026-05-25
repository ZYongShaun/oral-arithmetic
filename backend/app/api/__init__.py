from fastapi import APIRouter

from app.api.auth import router as auth_router
from app.api.users import router as users_router
from app.api.children import router as children_router
from app.api.questions import router as questions_router
from app.api.practices import router as practices_router
from app.api.wrong_questions import router as wrong_questions_router
from app.api.daily_tasks import router as daily_tasks_router
from app.api.streaks import router as streaks_router
from app.api.achievements import router as achievements_router
from app.api.leaderboards import router as leaderboards_router
from app.api.stars import router as stars_router
from app.api.admin import router as admin_router

api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(children_router)
api_router.include_router(questions_router)
api_router.include_router(practices_router)
api_router.include_router(wrong_questions_router)
api_router.include_router(daily_tasks_router)
api_router.include_router(streaks_router)
api_router.include_router(achievements_router)
api_router.include_router(leaderboards_router)
api_router.include_router(stars_router)
api_router.include_router(admin_router)

__all__ = ["api_router"]
