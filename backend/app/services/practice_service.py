from datetime import datetime
from typing import List, Dict, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.question import Question
from app.models.practice import Practice
from app.models.practice_detail import PracticeDetail
from app.models.wrong_question import WrongQuestion
from app.models.child import Child
from app.models.streak import Streak
from app.models.achievement import StarTransaction
from app.schemas.practice import PracticeSubmitResponse
from app.services.streak_service import StreakService
from app.services.star_service import StarService
from app.services.daily_task_service import DailyTaskService


def calculate_stars_earned(accuracy: float) -> int:
    if accuracy >= 100:
        return 3
    elif accuracy >= 80:
        return 2
    elif accuracy >= 60:
        return 1
    return 0


def submit_practice(
    db: Session,
    practice_id: int,
    answers: Dict[int, str],
    time_spent: int
) -> PracticeSubmitResponse:
    """提交练习，集成连胜、星星奖励和每日任务系统"""
    practice = db.query(Practice).filter(Practice.id == practice_id).first()
    if not practice:
        raise ValueError("Practice not found")
    
    if practice.completed_at is not None:
        raise ValueError("Practice already completed")
    
    correct_count = 0
    details_data = []
    
    practice_details = db.query(PracticeDetail).filter(
        PracticeDetail.practice_id == practice_id
    ).all()
    
    for detail in practice_details:
        user_answer = str(answers.get(detail.id, ""))
        expected_answer = str(detail.expected_answer)
        is_correct = user_answer.strip() == expected_answer.strip()
        
        if is_correct:
            correct_count += 1
        
        detail.user_answer = user_answer
        detail.is_correct = is_correct
        
        details_data.append({
            "id": detail.id,
            "practice_id": detail.practice_id,
            "question_id": detail.question_id,
            "question_text": detail.question_text,
            "user_answer": user_answer,
            "expected_answer": expected_answer,
            "is_correct": is_correct,
            "time_spent": detail.time_spent,
        })
        
        if not is_correct:
            wrong_question_dict = {
                'chile_id': practice.child_id,
                'question_text': detail.question_text,
                'correct_answer': expected_answer,
                'wrong_count': 1,
                'last_wrong_time': datetime.utcnow()
            }
            existing_wrong = db.query(WrongQuestion).filter(
                WrongQuestion.child_id == practice.child_id,
                WrongQuestion.question_text == detail.question_text
            ).first()
            
            if not existing_wrong:
                wrong_question = WrongQuestion(**wrong_question_dict)
                db.add(wrong_question)
            else:
                existing_wrong.wrong_count += 1
                existing_wrong.last_wrong_time = datetime.utcnow()
    
    total_questions = len(practice_details)
    score = int((correct_count / total_questions) * 100) if total_questions > 0 else 0
    accuracy = (correct_count / total_questions) * 100 if total_questions > 0 else 0.0
    
    practice.score = score
    practice.accuracy = accuracy
    practice.time_spent = time_spent
    practice.completed_at = datetime.utcnow()
    
    # 1. 计算并奖励星星
    star_result = StarService.award_practice_stars(
        db=db,
        child_id=practice.child_id,
        accuracy=accuracy / 100,
        practice_id=practice_id
    )
    practice.stars_earned = star_result['stars_earned']
    
    # 2. 更新连胜
    streak_result = StreakService.check_and_update_streak(
        db=db,
        child_id=practice.child_id,
        accuracy=accuracy / 100
    )
    
    # 3. 更新每日任务
    task_result = DailyTaskService.update_practice_count(
        db=db,
        child_id=practice.child_id,
        practice_id=practice_id
    )
    
    db.commit()
    db.refresh(practice)
    
    return PracticeSubmitResponse(
        practice_id=practice.id,
        score=score,
        accuracy=accuracy,
        stars_earned=star_result['stars_earned'],
        time_spent=time_spent,
        completed_at=practice.completed_at,
        details=details_data,
        streak_info=streak_result,
        task_info=task_result
    )
