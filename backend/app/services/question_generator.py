from typing import List, Dict
import random


class QuestionGenerator:
    """智能口算题目生成器"""
    
    @staticmethod
    def generate_arithmetic_question(
        difficulty_level: int,
        question_type: str,
        include_mix: bool = False
    ) -> Dict:
        """
        生成单个口算题目
        
        Args:
            difficulty_level: 难度等级 (1-10以内, 2-20以内, 3-50以内, 4-100以内)
            question_type: 题型 ('addition', 'subtraction', 'mixed')
            include_mix: 是否包含混合题型
            
        Returns:
            题目字典
        """
        if include_mix:
            actual_type = random.choice(['addition', 'subtraction'])
        else:
            actual_type = question_type
        
        if actual_type == 'addition':
            return QuestionGenerator._generate_addition(difficulty_level)
        else:
            return QuestionGenerator._generate_subtraction(difficulty_level)
    
    @staticmethod
    def _generate_addition(difficulty_level: int) -> Dict:
        """生成加法题目"""
        ranges = {
            1: (1, 10),
            2: (1, 20),
            3: (1, 50),
            4: (1, 100)
        }
        
        min_val, max_sum = ranges.get(difficulty_level, (1, 10))
        
        num1 = random.randint(min_val, max_sum - 1)
        num2 = random.randint(min_val, max_sum - num1)
        
        actual_num2 = random.randint(min_val, max_sum - 1)
        if actual_num2 + num1 > max_sum:
            actual_num2 = max_sum - num1
        
        return {
            'question_text': f"{num1} + {actual_num2} = ?",
            'expected_answer': num1 + actual_num2,
            'question_type': 'addition',
            'difficulty_level': difficulty_level,
            'options': QuestionGenerator._generate_options(
                num1 + actual_num2,
                min_val,
                max_sum,
                is_addition=True
            )
        }
    
    @staticmethod
    def _generate_subtraction(difficulty_level: int) -> Dict:
        """生成减法题目"""
        ranges = {
            1: (1, 10),
            2: (1, 20),
            3: (1, 50),
            4: (1, 100)
        }
        
        min_val, max_val = ranges.get(difficulty_level, (1, 10))
        
        num1 = random.randint(min_val + 1, max_val)
        num2 = random.randint(min_val, min(num1, max_val))
        
        return {
            'question_text': f"{num1} - {num2} = ?",
            'expected_answer': num1 - num2,
            'question_type': 'subtraction',
            'difficulty_level': difficulty_level,
            'options': QuestionGenerator._generate_options(
                num1 - num2,
                min_val,
                max_val,
                is_addition=False
            )
        }
    
    @staticmethod
    def _generate_options(
        correct_answer: int,
        min_val: int,
        max_val: int,
        is_addition: bool
    ) -> List[int]:
        """生成干扰选项"""
        options = [correct_answer]

        min_bound = min_val
        max_bound = max_val
        candidate_offsets = [-10, -5, -3, -2, -1, 1, 2, 3, 5, 10]

        for offset in candidate_offsets:
            option = correct_answer + offset
            if min_bound <= option <= max_bound and option not in options:
                options.append(option)
            if len(options) == 4:
                break

        if len(options) < 4:
            for option in range(min_bound, max_bound + 1):
                if option not in options:
                    options.append(option)
                if len(options) == 4:
                    break
        
        random.shuffle(options)
        return options
    
    @staticmethod
    def generate_practice_questions(
        difficulty_level: int,
        question_types: List[str] = None,
        count: int = 20
    ) -> List[Dict]:
        """
        生成一套练习题目
        
        Args:
            difficulty_level: 难度等级
            question_types: 题型列表，None表示混合
            count: 题目数量
            
        Returns:
            题目列表
        """
        if question_types is None or len(question_types) > 1:
            include_mix = True
            types = ['addition', 'subtraction']
        else:
            include_mix = False
            types = question_types
        
        questions = []
        for i in range(count):
            question = QuestionGenerator.generate_arithmetic_question(
                difficulty_level=difficulty_level,
                question_type=types[i % len(types)],
                include_mix=include_mix
            )
            questions.append(question)
        
        random.shuffle(questions)
        return questions
    
    @staticmethod
    def adjust_difficulty(
        difficulty_level: int,
        consecutive_correct: int = 0,
        consecutive_wrong: int = 0
    ) -> int:
        """
        智能调节难度
        
        Args:
            difficulty_level: 当前难度
            consecutive_correct: 连续答对次数
            consecutive_wrong: 连续答错次数
            
        Returns:
            调整后的难度
        """
        new_level = difficulty_level
        
        if consecutive_correct >= 5 and difficulty_level < 4:
            new_level = difficulty_level + 1
        elif consecutive_wrong >= 3 and difficulty_level > 1:
            new_level = difficulty_level - 1
        
        return min(4, max(1, new_level))
