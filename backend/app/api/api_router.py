from fastapi import APIRouter

from app.api import auth, users, children, practices, questions, wrong_questions, daily_tasks, streaks, achievements, leaderboards, stars, admin

api_router = APIRouter()

api_router.include_router(auth.router, tags=["auth"])
api_router.include_router(users.router, tags=["users"])
api_router.include_router(children.router, tags=["children"])
api_router.include_router(practices.router, tags=["practices"])
api_router.include_router(questions.router, tags=["questions"])
api_router.include_router(wrong_questions.router, tags=["wrong_questions"])
api_router.include_router(daily_tasks.router, tags=["daily_tasks"])
api_router.include_router(streaks.router, tags=["streaks"])
api_router.include_router(achievements.router, tags=["achievements"])
api_router.include_router(leaderboards.router, tags=["leaderboards"])
api_router.include_router(stars.router, tags=["stars"])
api_router.include_router(admin.router, tags=["admin"])
