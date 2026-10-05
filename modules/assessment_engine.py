"""
Assessment Engine Module
Delivers dynamic skill proficiency quizzes, evaluates learner responses,
provides contextual explanations, and updates skill proficiency estimates in real-time.
"""

import os
import json
from typing import Dict, Any, List, Optional

class AssessmentEngine:
    def __init__(self, questions_path: str = None):
        if questions_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            questions_path = os.path.join(base_dir, "data", "assessment_questions.json")

        self.questions_path = questions_path
        self.questions = self._load_questions()

    def _load_questions(self) -> List[Dict[str, Any]]:
        if not os.path.exists(self.questions_path):
            return []
        with open(self.questions_path, "r", encoding="utf-8") as f:
            return json.load(f).get("questions", [])

    def get_questions_for_role(self, role_data: Dict[str, Any], max_questions: int = 5) -> List[Dict[str, Any]]:
        """
        Fetch relevant questions corresponding to the competencies required by the target role.
        """
        role_skills = {c["skill_id"] for c in role_data.get("expected_competencies", [])}
        matched_qs = [q for q in self.questions if q.get("skill_id") in role_skills]

        # If we have enough, return up to max_questions
        if matched_qs:
            return matched_qs[:max_questions]
        return self.questions[:max_questions]

    def evaluate_quiz(self, user_answers: Dict[str, int], question_subset: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Evaluate candidate's quiz answers, calculate score, provide explanations,
        and generate skill proficiency upgrades.
        """
        total = len(question_subset)
        if total == 0:
            return {"score": 0, "total": 0, "accuracy_pct": 0, "details": [], "upgrades": {}}

        correct_count = 0
        details = []
        skill_results = {}

        for q in question_subset:
            qid = q["id"]
            user_choice = user_answers.get(qid, None)
            is_correct = (user_choice == q["correct_index"])

            if is_correct:
                correct_count += 1

            skill_id = q["skill_id"]
            if skill_id not in skill_results:
                skill_results[skill_id] = {"correct": 0, "total": 0, "skill_name": q["skill_name"], "level": q["level"]}
            skill_results[skill_id]["total"] += 1
            if is_correct:
                skill_results[skill_id]["correct"] += 1

            details.append({
                "question_id": qid,
                "skill_name": q["skill_name"],
                "level": q["level"],
                "question_text": q["question"],
                "user_selected": q["options"][user_choice] if user_choice is not None and user_choice < len(q["options"]) else "Skipped / None",
                "correct_option": q["options"][q["correct_index"]],
                "is_correct": is_correct,
                "explanation": q["explanation"]
            })

        accuracy_pct = round((correct_count / total) * 100, 1)

        # Determine skill proficiency upgrade candidates
        upgrades = {}
        for skill_id, stats in skill_results.items():
            pass_rate = stats["correct"] / stats["total"]
            if pass_rate >= 0.7:
                upgrades[skill_id] = {
                    "skill_name": stats["skill_name"],
                    "tested_level": stats["level"],
                    "awarded_proficiency": stats["level"]
                }

        return {
            "score": correct_count,
            "total": total,
            "accuracy_pct": accuracy_pct,
            "details": details,
            "upgrades": upgrades,
            "passed": accuracy_pct >= 60.0
        }
