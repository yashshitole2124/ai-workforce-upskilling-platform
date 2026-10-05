"""
AI Workforce Upskilling Platform - Core Modules
"""
from .resume_parser import ResumeParser
from .skill_extractor import SkillExtractor
from .role_engine import RoleEngine
from .gap_analyzer import SkillGapAnalyzer
from .recommender import Recommender
from .ai_mentor import AIMentor
from .assessment_engine import AssessmentEngine
from .jd_matcher import JDMatcher
from .career_analytics import CareerAnalytics

__all__ = [
    "ResumeParser",
    "SkillExtractor",
    "RoleEngine",
    "SkillGapAnalyzer",
    "Recommender",
    "AIMentor",
    "AssessmentEngine",
    "JDMatcher",
    "CareerAnalytics"
]
