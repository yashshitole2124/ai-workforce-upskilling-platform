"""
Custom Job Description (JD) Semantic Matcher Module
Analyzes custom job postings, extracts required competencies using NLP,
computes semantic TF-IDF / Cosine Similarity, and identifies resume-to-JD alignment gaps.
"""

import re
from typing import Dict, Any, List
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class JDMatcher:
    def __init__(self, skill_extractor):
        self.skill_extractor = skill_extractor

    def analyze_jd(self, jd_text: str, resume_data: Dict[str, Any], extracted_skills: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform semantic and keyword-level alignment analysis between candidate resume and custom JD.
        """
        if not jd_text or len(jd_text.strip()) < 30:
            return {"error": "Job description text is too short. Please paste a full job posting."}

        # 1. Extract required skills from JD using skill extractor
        jd_skills_result = self.skill_extractor.extract_skills(jd_text)
        jd_skills_dict = jd_skills_result.get("skills", {})

        # Candidate skills
        candidate_skills_dict = extracted_skills.get("skills", {})

        # 2. Compute Cosine Semantic Similarity using TF-IDF
        resume_raw = resume_data.get("raw_text", "")
        vectorizer = TfidfVectorizer(stop_words="english", max_features=1000)
        
        try:
            tfidf_matrix = vectorizer.fit_transform([resume_raw, jd_text])
            sim_score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            semantic_score = round(float(sim_score) * 100, 1)
        except Exception:
            semantic_score = 50.0

        # 3. Keyword / Skill Overlap
        matched_skills = []
        missing_skills = []

        for skill_id, skill_meta in jd_skills_dict.items():
            if skill_id in candidate_skills_dict:
                cand_info = candidate_skills_dict[skill_id]
                matched_skills.append({
                    "skill_name": skill_meta["canonical_name"],
                    "category": skill_meta["category"],
                    "candidate_proficiency": cand_info["estimated_proficiency"],
                    "jd_frequency": skill_meta["frequency"]
                })
            else:
                missing_skills.append({
                    "skill_name": skill_meta["canonical_name"],
                    "category": skill_meta["category"],
                    "jd_frequency": skill_meta["frequency"]
                })

        total_jd_skills = len(jd_skills_dict)
        skill_coverage_pct = round((len(matched_skills) / total_jd_skills) * 100, 1) if total_jd_skills > 0 else 0.0

        # Combined composite match score (60% skill coverage + 40% semantic similarity)
        composite_score = round((skill_coverage_pct * 0.65) + (semantic_score * 0.35), 1)

        # Keyword density & recommendations
        recommendations = []
        if missing_skills:
            top_missing = [m["skill_name"] for m in missing_skills[:4]]
            recommendations.append(f"Incorporate missing target competencies: **{', '.join(top_missing)}** into your resume's technical skills or project descriptions.")
        if semantic_score < 40:
            recommendations.append("Align your resume's terminology and phrasing with the specific action verbs and industry phrases used in this job description.")
        else:
            recommendations.append("Strong semantic resonance detected between your experience summaries and this job posting.")

        return {
            "composite_match_score": composite_score,
            "skill_coverage_pct": skill_coverage_pct,
            "semantic_similarity_pct": semantic_score,
            "total_jd_skills_found": total_jd_skills,
            "matched_skills_count": len(matched_skills),
            "missing_skills_count": len(missing_skills),
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "recommendations": recommendations,
            "jd_summary": {
                "word_count": len(jd_text.split()),
                "top_categories": list(jd_skills_result.get("skills_by_category", {}).keys())
            }
        }
