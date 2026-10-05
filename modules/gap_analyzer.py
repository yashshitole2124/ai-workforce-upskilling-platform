"""
Skill Gap Analyzer Module
Compares learner profile with role competency requirements,
computes weighted readiness scores, and identifies prioritized skill gaps.
"""

from typing import Dict, Any, List

class SkillGapAnalyzer:
    PROFICIENCY_SCALE = {
        "None": 0,
        "Beginner": 1,
        "Intermediate": 2,
        "Advanced": 3
    }

    REV_PROFICIENCY = {v: k for k, v in PROFICIENCY_SCALE.items()}

    def __init__(self):
        pass

    def analyze_gap(self, learner_skills: Dict[str, Any], role_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform comprehensive gap analysis between extracted learner skills and target role competencies.
        """
        required_competencies = role_data.get("expected_competencies", [])
        extracted_skills_dict = learner_skills.get("skills", {})

        total_weight = 0.0
        earned_weight = 0.0

        matches = []
        partial_matches = []
        missing_skills = []
        detailed_matrix = []

        for comp in required_competencies:
            skill_id = comp["skill_id"]
            canonical_name = comp["canonical_name"]
            importance = comp.get("importance", "Medium")
            weight = comp.get("weight", 1.0)
            expected_prof_str = comp.get("expected_proficiency", "Intermediate")
            expected_prof_val = self.PROFICIENCY_SCALE.get(expected_prof_str, 2)

            total_weight += weight

            if skill_id in extracted_skills_dict:
                candidate_skill = extracted_skills_dict[skill_id]
                cand_prof_str = candidate_skill.get("estimated_proficiency", "Beginner")
                cand_prof_val = self.PROFICIENCY_SCALE.get(cand_prof_str, 1)

                ratio = min(1.0, cand_prof_val / max(1, expected_prof_val))
                earned_weight += weight * ratio

                if cand_prof_val >= expected_prof_val:
                    status = "Matched"
                    matches.append({
                        "skill_id": skill_id,
                        "canonical_name": canonical_name,
                        "candidate_proficiency": cand_prof_str,
                        "expected_proficiency": expected_prof_str,
                        "importance": importance,
                        "weight": weight
                    })
                else:
                    status = "Partial"
                    partial_matches.append({
                        "skill_id": skill_id,
                        "canonical_name": canonical_name,
                        "candidate_proficiency": cand_prof_str,
                        "expected_proficiency": expected_prof_str,
                        "importance": importance,
                        "gap_level": expected_prof_val - cand_prof_val,
                        "weight": weight
                    })
            else:
                cand_prof_str = "None"
                cand_prof_val = 0
                status = "Missing"
                missing_skills.append({
                    "skill_id": skill_id,
                    "canonical_name": canonical_name,
                    "candidate_proficiency": "None",
                    "expected_proficiency": expected_prof_str,
                    "importance": importance,
                    "gap_level": expected_prof_val,
                    "weight": weight
                })

            detailed_matrix.append({
                "skill_id": skill_id,
                "skill_name": canonical_name,
                "importance": importance,
                "weight": weight,
                "expected_level": expected_prof_str,
                "expected_val": expected_prof_val,
                "candidate_level": cand_prof_str,
                "candidate_val": cand_prof_val,
                "status": status,
                "gap": max(0, expected_prof_val - cand_prof_val)
            })

        # Calculate overall readiness percentage
        readiness_score = round((earned_weight / total_weight) * 100, 1) if total_weight > 0 else 0.0

        # Sort missing/partial skills by urgency: Critical first, then High, then Medium
        importance_rank = {"Critical": 1, "High": 2, "Medium": 3}
        prioritized_gaps = []

        for item in missing_skills:
            prioritized_gaps.append({
                "skill_id": item["skill_id"],
                "skill_name": item["canonical_name"],
                "gap_type": "Missing Essential Skill",
                "importance": item["importance"],
                "target_level": item["expected_proficiency"],
                "urgency": importance_rank.get(item["importance"], 3),
                "priority_label": f"P{importance_rank.get(item['importance'], 3)} - {item['importance']} Gap"
            })

        for item in partial_matches:
            prioritized_gaps.append({
                "skill_id": item["skill_id"],
                "skill_name": item["canonical_name"],
                "gap_type": f"Proficiency Gap ({item['candidate_proficiency']} → {item['expected_proficiency']})",
                "importance": item["importance"],
                "target_level": item["expected_proficiency"],
                "urgency": importance_rank.get(item["importance"], 3) + 0.5,
                "priority_label": f"P{importance_rank.get(item['importance'], 3)} - Skill Upgrade"
            })

        prioritized_gaps.sort(key=lambda x: x["urgency"])

        # Identify additional skills the candidate has outside this role
        role_skill_ids = {c["skill_id"] for c in required_competencies}
        extra_skills = [
            s["canonical_name"] 
            for s_id, s in extracted_skills_dict.items() 
            if s_id not in role_skill_ids
        ]

        # Readiness Tier Assessment
        if readiness_score >= 80:
            readiness_tier = "Job Ready (Interview Stage)"
            readiness_color = "#10B981" # Green
            verdict = "Strong alignment with role competencies. Minor refinement recommended."
        elif readiness_score >= 60:
            readiness_tier = "Nearly Ready (Targeted Upskilling Needed)"
            readiness_color = "#3B82F6" # Blue
            verdict = "Solid foundational profile. Bridge 2-3 critical gaps to achieve full role readiness."
        elif readiness_score >= 40:
            readiness_tier = "Developing (Guided Roadmap Required)"
            readiness_color = "#F59E0B" # Amber
            verdict = "Moderate overlap. Requires focused coursework and portfolio projects in core competencies."
        else:
            readiness_tier = "Entry / Transition Phase"
            readiness_color = "#EF4444" # Red
            verdict = "Substantial skill acquisition needed across foundational and role-specific domains."

        return {
            "readiness_score": readiness_score,
            "readiness_tier": readiness_tier,
            "readiness_color": readiness_color,
            "verdict": verdict,
            "total_role_skills": len(required_competencies),
            "fully_matched_count": len(matches),
            "partially_matched_count": len(partial_matches),
            "missing_count": len(missing_skills),
            "matches": matches,
            "partial_matches": partial_matches,
            "missing_skills": missing_skills,
            "prioritized_gaps": prioritized_gaps,
            "detailed_matrix": detailed_matrix,
            "extra_candidate_skills": extra_skills
        }
