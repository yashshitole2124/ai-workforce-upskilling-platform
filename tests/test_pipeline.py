"""
Pipeline Unit Tests for AI Workforce Upskilling Platform
Tests resume parsing, skill extraction, normalization, role mapping, gap analysis,
quiz assessment engine, JD semantic matcher, and career pathways.
"""

import os
import sys
import unittest

# Add project root to sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from modules.resume_parser import ResumeParser
from modules.skill_extractor import SkillExtractor
from modules.role_engine import RoleEngine
from modules.gap_analyzer import SkillGapAnalyzer
from modules.recommender import Recommender
from modules.ai_mentor import AIMentor
from modules.assessment_engine import AssessmentEngine
from modules.jd_matcher import JDMatcher
from modules.career_analytics import CareerAnalytics

class TestUpskillingPipeline(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser = ResumeParser()
        cls.extractor = SkillExtractor()
        cls.role_engine = RoleEngine()
        cls.analyzer = SkillGapAnalyzer()
        cls.recommender = Recommender()
        cls.mentor = AIMentor()
        cls.assessment = AssessmentEngine()
        cls.jd_matcher = JDMatcher(cls.extractor)
        cls.career_analytics = CareerAnalytics(cls.role_engine, cls.analyzer)

    def test_sample_ml_resume_parsing(self):
        sample_path = os.path.join(BASE_DIR, "data", "sample_resumes", "sample_ml_engineer.txt")
        self.assertTrue(os.path.exists(sample_path), "Sample ML resume should exist")

        parsed = self.parser.parse(sample_path)
        self.assertIn("contact_info", parsed)
        self.assertIn("alex.chen@example.com", parsed["contact_info"]["email"])
        self.assertTrue(len(parsed["raw_text"]) > 200)

    def test_skill_extraction_and_normalization(self):
        text = "Experienced in Python programming, PyTorch, Scikit-Learn, and building Docker containers. Familiar with SQL and Git."
        extracted = self.extractor.extract_skills(text)
        
        skills_found = extracted["skills"]
        self.assertIn("python", skills_found)
        self.assertEqual(skills_found["python"]["canonical_name"], "Python")
        self.assertIn("pytorch", skills_found)
        self.assertIn("docker", skills_found)
        self.assertIn("sql", skills_found)
        self.assertIn("git", skills_found)

    def test_role_engine_roles_available(self):
        roles = self.role_engine.get_all_roles()
        self.assertTrue(len(roles) >= 4)
        role_ids = [r["role_id"] for r in roles]
        self.assertIn("ml_engineer", role_ids)
        self.assertIn("data_analyst", role_ids)

    def test_gap_analysis_and_readiness_score(self):
        sample_path = os.path.join(BASE_DIR, "data", "sample_resumes", "sample_ml_engineer.txt")
        parsed = self.parser.parse(sample_path)
        extracted = self.extractor.extract_skills(parsed["raw_text"])
        
        ml_role = self.role_engine.get_role_by_id("ml_engineer")
        self.assertIsNotNone(ml_role)

        analysis = self.analyzer.analyze_gap(extracted, ml_role)
        self.assertIn("readiness_score", analysis)
        self.assertTrue(0 <= analysis["readiness_score"] <= 100)
        self.assertTrue(len(analysis["matches"]) > 0)
        self.assertTrue(len(analysis["missing_skills"]) > 0)

    def test_assessment_engine(self):
        ml_role = self.role_engine.get_role_by_id("ml_engineer")
        questions = self.assessment.get_questions_for_role(ml_role, max_questions=4)
        self.assertTrue(len(questions) > 0)

        # Test evaluation with perfect answers
        answers = {q["id"]: q["correct_index"] for q in questions}
        result = self.assessment.evaluate_quiz(answers, questions)
        self.assertEqual(result["score"], len(questions))
        self.assertEqual(result["accuracy_pct"], 100.0)
        self.assertTrue(result["passed"])

    def test_jd_matcher(self):
        sample_path = os.path.join(BASE_DIR, "data", "sample_resumes", "sample_ml_engineer.txt")
        parsed = self.parser.parse(sample_path)
        extracted = self.extractor.extract_skills(parsed["raw_text"])

        mock_jd = "Looking for a Machine Learning Engineer with deep experience in Python, PyTorch, Docker, and AWS."
        jd_result = self.jd_matcher.analyze_jd(mock_jd, parsed, extracted)
        self.assertIn("composite_match_score", jd_result)
        self.assertTrue(0 <= jd_result["composite_match_score"] <= 100)
        self.assertTrue(len(jd_result["matched_skills"]) > 0)

    def test_career_analytics(self):
        sample_path = os.path.join(BASE_DIR, "data", "sample_resumes", "sample_ml_engineer.txt")
        parsed = self.parser.parse(sample_path)
        extracted = self.extractor.extract_skills(parsed["raw_text"])

        career_result = self.career_analytics.analyze_all_roles(extracted)
        self.assertIn("role_evaluations", career_result)
        self.assertTrue(len(career_result["role_evaluations"]) >= 4)
        self.assertIn("highest_roi_skills", career_result)

if __name__ == "__main__":
    unittest.main()
